/* Exporta `og-home.png` (1200×630) a partir de `og-home.html`.

   Es la imagen que ve cualquiera que comparta la web por WhatsApp.

   USO (hace falta un servidor local: con file:// el iframe no carga):
       npm i puppeteer-core                ← una sola vez
       python -m http.server 8899          ← desde la raíz del proyecto
       node publicidad/generar-og-home.js

   Se conecta a un Edge headless ya abierto:
       msedge --headless=new --remote-debugging-port=9222 --user-data-dir=<tmp>
   `puppeteer.launch()` no arranca en esta máquina (Code: 0, stderr vacío).

   ⚠️ El PNG sale en la RAÍZ, no en publicidad/: `publicidad/` está en
   .vercelignore y la imagen tiene que ser pública para que Meta la lea.
*/
const fs   = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const URL    = process.env.OG_URL || 'http://localhost:8899/publicidad/og-home.html';
const SALIDA = path.join(__dirname, '..', 'og-home.png');

(async () => {
  const browser = await puppeteer.connect({ browserURL: 'http://127.0.0.1:9222' });
  const page = await browser.newPage();

  // deviceScaleFactor 1: el PNG tiene que medir 1200×630 EXACTOS, que es lo
  // que declaran las etiquetas og:image:width/height. A 2× salía de
  // 2400×1260 y 809 KB — y WhatsApp descarta la imagen de la vista previa
  // pasados los ~600 KB, así que la tarjeta habría salido sin foto.
  // La nitidez no se pierde: el iframe ya se dibuja al doble y se achica a la
  // mitad por CSS, así que la invitación queda a resolución 1:1 igual.
  await page.setViewport({ width: 1200, height: 630, deviceScaleFactor: 1 });
  await page.goto(URL, { waitUntil: 'networkidle2' });

  // La invitación de adentro trae su config de Supabase y recién ahí pinta el
  // splash. Se espera a que la clase `listo` aparezca DENTRO del iframe.
  const marco = await (await page.$('iframe')).contentFrame();
  await marco.waitForSelector('#splash.listo', { timeout: 20000 });
  await marco.waitForFunction(() => {
    const img = document.getElementById('splash-img');
    return !img || !img.src || img.complete;
  }, { timeout: 20000 });

  // Un respiro para las fuentes y el fundido de opacidad del splash.
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 1200));

  const el = await page.$('.placa');
  const buf = await el.screenshot({ type: 'png' });
  fs.writeFileSync(SALIDA, buf);

  const { width, height } = await el.boundingBox();
  console.log(`✔ ${path.relative(process.cwd(), SALIDA)}`);
  console.log(`  caja CSS   : ${width}×${height}`);
  console.log(`  peso       : ${(fs.statSync(SALIDA).size / 1024).toFixed(0)} KB`);

  await page.close();
  await browser.disconnect();
})();
