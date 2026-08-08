/* ═══════════════════════════════════════════════════════════════════
   Arma el MP4 del reel a partir de `agosto-a-reel.html`.

   Cómo funciona: abre la página, y en vez de dejar que el celular
   scrollee "en vivo", mueve el scroll del iframe CUADRO POR CUADRO y
   saca una foto de cada posición. Después ffmpeg pega los cuadros.

   Por qué así y no grabando la pantalla: una grabación depende de lo
   rápido que vaya la máquina, y el movimiento sale a los tirones. Esto
   da 30 cuadros por segundo exactos siempre, en cualquier compu.

   Antes de la pasada buena baja una vez hasta el final: la invitación
   tiene animaciones de aparición y, si no se las dispara antes, las
   secciones entran a destiempo mientras se graba.

   USO (hace falta un servidor local, no vale abrir el archivo suelto:
   con file:// el iframe no carga):
       python -m http.server 8899          ← desde la raíz del proyecto
       node publicidad/generar-reel.js
   Sale `publicidad/agosto-a-reel.mp4`.
   ═══════════════════════════════════════════════════════════════════ */
const fs   = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const puppeteer = require('puppeteer-core');
const ffmpeg    = require('ffmpeg-static');

const EDGE   = process.env.EDGE_PATH || 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const URL    = process.env.REEL_URL  || 'http://localhost:8899/publicidad/agosto-a-reel.html';
const SALIDA = path.join(__dirname, 'agosto-a-reel.mp4');
const TMP    = path.join(require('os').tmpdir(), 'reel-cuadros');

const FPS      = 30;
const QUIETO   = 1.6;   // seg mirando el principio, para que se lea el titular
// La invitación mide ~4560px de recorrido. En 10 seg pasa a 450px/seg y no
// se llega a leer nada; a 13,5 queda en ~340 y se sigue con la vista.
const BAJANDO  = 13.5;
const FINAL    = 1.8;   // seg quieto abajo antes de cortar

// Suave al arrancar y al frenar. Un scroll lineal se nota mecánico.
const suave = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

(async () => {
  fs.rmSync(TMP, { recursive: true, force: true });
  fs.mkdirSync(TMP, { recursive: true });

  const browser = await puppeteer.launch({
    executablePath: EDGE, headless: 'new',
    args: ['--no-sandbox', '--force-device-scale-factor=1', '--hide-scrollbars'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await page.goto(URL, { waitUntil: 'networkidle2', timeout: 120000 });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 4000));

  const marco = page.frames().find(f => /invitacion\.html/.test(f.url()));
  if (!marco) throw new Error('No encontré el iframe de la invitación. ¿Está levantado el servidor local?');

  // Pasada de calentamiento: dispara las animaciones de aparición.
  await marco.evaluate(async () => {
    const alto = document.body.scrollHeight;
    for (let y = 0; y < alto; y += 250) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 90)); }
    window.scrollTo(0, 0);
  });
  await new Promise(r => setTimeout(r, 2500));

  const recorrido = await marco.evaluate(() => document.body.scrollHeight - window.innerHeight);
  console.log(`recorrido del scroll: ${recorrido}px`);

  const placa   = await page.$('.placa');
  const cuadros = Math.round((QUIETO + BAJANDO + FINAL) * FPS);
  const desde   = Math.round(QUIETO * FPS);
  const hasta   = Math.round((QUIETO + BAJANDO) * FPS);

  for (let i = 0; i < cuadros; i++) {
    let y;
    if (i < desde)      y = 0;
    else if (i >= hasta) y = recorrido;
    else                 y = recorrido * suave((i - desde) / (hasta - desde));

    await marco.evaluate(v => window.scrollTo(0, v), Math.round(y));
    await placa.screenshot({ path: path.join(TMP, String(i).padStart(4, '0') + '.png') });

    if (i % 60 === 0) console.log(`  cuadro ${i}/${cuadros}`);
  }
  await browser.close();

  console.log('codificando…');
  execFileSync(ffmpeg, [
    '-y', '-framerate', String(FPS),
    '-i', path.join(TMP, '%04d.png'),
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',      // sin esto no se ve en celulares ni en Instagram
    '-profile:v', 'high', '-level', '4.1',
    '-crf', '18',
    '-movflags', '+faststart',  // arranca a reproducir sin bajar todo el archivo
    SALIDA,
  ], { stdio: 'inherit' });

  fs.rmSync(TMP, { recursive: true, force: true });
  const mb = (fs.statSync(SALIDA).size / 1048576).toFixed(1);
  console.log(`\nlisto: ${SALIDA}  (${mb} MB, ${(cuadros / FPS).toFixed(1)} seg)`);
})();
