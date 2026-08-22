/* ══════════════════════════════════════════════════════════════════
   GRABADOR DE REEL

   Abre la invitación en un navegador de verdad, la scrollea con un
   movimiento suave, y guarda un PNG por cuadro. Después ffmpeg los
   pega a 30 fps.

   ⚠️ NO se usa el screencast de puppeteer: entrega los cuadros cuando
   el navegador quiere, así que el video sale con tirones y la duración
   no es la que uno pidió. Capturando de a un cuadro por vez, el reloj
   lo manejamos nosotros: cada captura ES un cuadro exacto.

   ⚠️ El video de portada se mueve solo. Como cada captura tarda su
   tiempo, el video avanza más rápido de lo que avanza el reel. Por eso
   durante la portada se le fija el `currentTime` a mano, cuadro por
   cuadro: así se ve a la velocidad correcta.
   ══════════════════════════════════════════════════════════════════ */
const p = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const EVENTO = process.argv[2] || 'demo-enredados';
const SALIDA = process.argv[3] || 'cuadros';
const FPS = 30;

/* El guion: cada tramo dice cuánto dura y dónde tiene que estar el
   scroll al terminar. `texto` es el cartel que se muestra encima. */
/* ⚠️ El destino de cada tramo es una SECCION, no un multiplo de la
   altura de pantalla. Con multiplos, el scroll llegaba al fondo a mitad
   del guion y los ultimos cinco tramos mostraban todos el formulario. */
const GUION = [
  { seg: 2.8, a: '#sec-hero',      texto: 'Esto no es una foto',        sub: '' },
  { seg: 1.6, a: '#sec-hero',      texto: '',                            sub: '' },
  { seg: 2.4, a: '#sec-mensaje',   texto: '',                            sub: '' },
  { seg: 2.6, a: '#sec-countdown', texto: 'La cuenta baja sola',         sub: '' },
  { seg: 2.6, a: '#sec-galeria',   texto: '',                            sub: '' },
  { seg: 2.6, a: '#sec-ubicacion', texto: 'Con el mapa adentro',         sub: '' },
  { seg: 2.4, a: '#sec-dresscode', texto: '',                            sub: '' },
  { seg: 2.6, a: '#sec-regalos',   texto: 'Y detalles que nadie espera', sub: '' },
  { seg: 2.6, a: '#sec-rsvp',      texto: 'Confirman desde el celular',  sub: '' },
  { seg: 3.0, a: 'FINAL',          texto: '',                            sub: '' },
];

const suave = t => t < .5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2;

(async () => {
  fs.rmSync(SALIDA, { recursive: true, force: true });
  fs.mkdirSync(SALIDA, { recursive: true });

  const b = await p.connect({ browserURL: 'http://localhost:9222' });
  const pg = await b.newPage();
  await pg.setCacheEnabled(false);

  // Que ninguna grabación escriba en la base
  await pg.setRequestInterception(true);
  pg.on('request', r => /rpc\/(rsvp_|admin_)/.test(r.url()) ? r.abort() : r.continue());

  // 1080×1920 es el tamaño de un reel. Se trabaja a la mitad y con
  // deviceScaleFactor 2: así el layout es de celular y la imagen sale nítida.
  await pg.setViewport({ width: 540, height: 960, deviceScaleFactor: 2 });
  await pg.goto(`http://localhost:8899/invitacion.html?evento=${EVENTO}`, { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 3500));

  // El cartel de texto, encima de todo
  await pg.evaluate(() => {
    const c = document.createElement('div');
    c.id = '__cartel';
    c.style.cssText = 'position:fixed;left:0;right:0;top:0;z-index:99999;' +
      'text-align:center;pointer-events:none;padding:9% 8% 13%;opacity:0;' +
      'transition:opacity .45s ease;' +
      /* velo propio: sin esto el cartel cae sobre el texto de la seccion
         y no se lee ninguno de los dos */
      'background:linear-gradient(to bottom,rgba(0,0,0,.62),rgba(0,0,0,.34) 62%,transparent)';
    const t = document.createElement('div');
    t.id = '__t';
    t.style.cssText = "font-family:'Cinzel Decorative',Georgia,serif;font-size:34px;" +
      'font-weight:700;color:#fff;line-height:1.25;' +
      'text-shadow:0 2px 18px rgba(0,0,0,.85),0 0 34px rgba(0,0,0,.6)';
    const s = document.createElement('div');
    s.id = '__s';
    s.style.cssText = "font-family:'Jost',system-ui,sans-serif;font-size:17px;" +
      'letter-spacing:.16em;color:rgba(255,255,255,.92);margin-top:10px;' +
      'text-shadow:0 2px 12px rgba(0,0,0,.9)';
    c.append(t, s);
    document.body.appendChild(c);

    // Entrar sin tocar: el splash tapa todo y el reel tiene que arrancar
    // mostrando la invitación.
    const sp = document.getElementById('splash');
    if (sp) sp.remove();
    // la barra de scroll se ve en la grabacion y delata que es una captura
    const est = document.createElement('style');
    est.textContent = '::-webkit-scrollbar{width:0;height:0}html{scrollbar-width:none}';
    document.head.appendChild(est);

    // Placa final de marca, escondida hasta el ultimo tramo
    const fin = document.createElement('div');
    fin.id = '__final';
    fin.style.cssText = 'position:fixed;inset:0;z-index:99998;display:flex;opacity:0;' +
      'flex-direction:column;align-items:center;justify-content:center;text-align:center;' +
      'background:#08080a;color:#F7CE84;transition:opacity .5s ease;padding:10%';
    const fm = document.createElement('div');
    fm.style.cssText = "font-family:'Cinzel Decorative',Georgia,serif;font-size:44px;" +
      'font-weight:700;line-height:1.2;color:#F7CE84';
    fm.textContent = 'Invitaciones Digitales';
    const fw = document.createElement('div');
    fw.style.cssText = "font-family:'Jost',system-ui,sans-serif;font-size:19px;" +
      'letter-spacing:.16em;margin-top:20px;color:rgba(247,206,132,.72)';
    fw.textContent = 'invitacionesdigitalesoficial.com';
    const fc = document.createElement('div');
    fc.style.cssText = "font-family:'Jost',system-ui,sans-serif;font-size:22px;" +
      'margin-top:40px;color:#fff;line-height:1.5';
    fc.textContent = '¿Querés una así para tu fiesta?';
    fin.append(fm, fw, fc);
    document.body.appendChild(fin);

    document.documentElement.style.scrollBehavior = 'auto';
    window.scrollTo(0, 0);
  });

  let n = 0, desde = 0;
  for (const tramo of GUION) {
    const cuadros = Math.round(tramo.seg * FPS);

    if (tramo.a === 'FINAL') {
      await pg.evaluate(() => {
        document.getElementById('__cartel').style.opacity = '0';
        document.getElementById('__final').style.opacity = '1';
      });
      for (let i = 0; i < cuadros; i++) {
        await pg.screenshot({ path: path.join(SALIDA, String(n).padStart(5, '0') + '.png') });
        n++;
      }
      continue;
    }

    // La seccion se centra en pantalla; si es mas alta, se alinea arriba.
    const hasta = await pg.evaluate(sel => {
      const e = document.querySelector(sel);
      if (!e) return scrollY;
      const r = e.getBoundingClientRect();
      const y = r.top + scrollY;
      const centrado = y - Math.max(0, (innerHeight - r.height) / 2);
      return Math.max(0, Math.min(centrado, document.body.scrollHeight - innerHeight));
    }, tramo.a);

    await pg.evaluate((tx, sb) => {
      document.getElementById('__t').textContent = tx;
      document.getElementById('__s').textContent = sb;
      document.getElementById('__cartel').style.opacity = tx ? '1' : '0';
    }, tramo.texto, tramo.sub);

    for (let i = 0; i < cuadros; i++) {
      const y = desde + (hasta - desde) * suave(i / Math.max(1, cuadros - 1));
      await pg.evaluate((yy, t) => {
        window.scrollTo(0, yy);
        // el video de portada, cuadro a cuadro, para que corra a su ritmo
        const v = document.getElementById('hero-video');
        if (v && v.duration) { v.pause(); v.currentTime = t % v.duration; }
      }, y, (n / FPS));
      await pg.screenshot({ path: path.join(SALIDA, String(n).padStart(5, '0') + '.png') });
      n++;
    }
    desde = hasta;
  }

  console.log(`${n} cuadros = ${(n / FPS).toFixed(1)}s`);
  await pg.close();
  await b.disconnect();
})();
