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
  { seg: 4.0, a: '#sec-hero' },
  { seg: 3.6, a: '#sec-mensaje' },
  { seg: 4.0, a: '#sec-countdown' },
  { seg: 7.4, a: '#sec-galeria',   pascal: true },
  { seg: 4.0, a: '#sec-ubicacion' },
  { seg: 3.6, a: '#sec-dresscode' },
  { seg: 4.4, a: '#sec-regalos' },
  { seg: 4.0, a: '#sec-rsvp' },
  { seg: 3.0, a: 'FINAL' },
];

const suave = t => t < .5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2;

/* ⚠️⚠️ EL TIEMPO DEL NAVEGADOR NO ES EL TIEMPO DEL VIDEO.
   Cada captura tarda ~0,16 segundos REALES, pero avanza apenas 1/30 de
   segundo de video. O sea que las animaciones CSS corren casi CINCO
   VECES mas rapido de lo que se ve: los iconos laten a las corridas,
   Pascal entra y sale en dos cuadros, y nada se llega a entender.

   La solucion no es bajarles la velocidad a ojo: es SACARLES el reloj.
   Se pausan todas y en cada cuadro se les pone a mano el tiempo de
   video que corresponde. Asi el resultado es igual siempre, no depende
   de lo rapida que este la maquina.

   ⚠️ Cada animacion cuenta desde que APARECIO, no desde que arranco el
   reel: las secciones se animan al entrar en pantalla, y si se les pone
   el tiempo total ya nacen terminadas. */
const RELOJ = `(t => {
  window.__nace = window.__nace || new WeakMap();
  document.getAnimations().forEach(a => {
    if (!window.__nace.has(a)) window.__nace.set(a, t);
    try { a.pause(); a.currentTime = Math.max(0, (t - window.__nace.get(a)) * 1000); } catch (e) {}
  });
  const v = document.getElementById('hero-video');
  if (v && v.duration) { v.pause(); v.currentTime = t % v.duration; }

  // El carrusel: una foto cada 2,4 segundos DE VIDEO
  const pista = document.getElementById('carousel-track');
  if (pista && pista.children.length > 1) {
    const n = pista.children.length;
    const i = Math.floor(Math.max(0, t - (window.__gal0 || 0)) / 2.4) % n;
    pista.style.transition = 'transform .7s cubic-bezier(.22,.61,.36,1)';
    pista.style.transform = 'translateX(-' + (i * 100) + '%)';
  }

  // La cuenta regresiva, avanzando al ritmo del video y no al del reloj
  const dias = document.getElementById('days');
  if (dias && window.__cd) {
    let f = Math.max(0, Math.floor(window.__cd - t));
    const dd = String(Math.floor(f / 86400));
    const hh = String(Math.floor(f % 86400 / 3600)).padStart(2, '0');
    const mm = String(Math.floor(f % 3600 / 60)).padStart(2, '0');
    const ss = String(f % 60).padStart(2, '0');
    dias.textContent = dd.padStart(2, '0');
    document.getElementById('hours').textContent = hh;
    document.getElementById('mins').textContent = mm;
    document.getElementById('secs').textContent = ss;
  }
})`;

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

  await pg.evaluate(() => {
    // Sin carteles: los textos los pone Fer arriba, en Instagram.

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
    fin.append(fm, fw);
    document.body.appendChild(fin);

    document.documentElement.style.scrollBehavior = 'auto';
    window.scrollTo(0, 0);

    /* ⚠️ El carrusel de fotos y la cuenta regresiva avanzan con
       `setInterval`, o sea con el reloj REAL: 2 segundos reales son
       apenas 0,4 de video, y las fotos pasaban de a tres por segundo.
       Se cortan TODOS los intervalos y desde acá se manejan a mano, con
       el tiempo del video. */
    window.__cd = (instanteDelEvento() - Date.now()) / 1000;
    for (let i = 1; i < 99999; i++) clearInterval(i);
  });

  let n = 0, desde = 0;
  for (const tramo of GUION) {
    const cuadros = Math.round(tramo.seg * FPS);

    if (tramo.a === 'FINAL') {
      await pg.evaluate(() => {
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

    // Pascal se asoma cuando lo dice el guion. Su logica propia mide el
    // tiempo con el reloj REAL, que durante la grabacion no sirve.
    // ⚠️ Y NO se usa su clase `asomada`: entra por una transicion CSS, y el
    // control de reloj se la cancela (currentTime mayor que su duracion =
    // el navegador la descarta y vuelve al reposo). Se le calcula la
    // posicion a mano, cuadro por cuadro.
    await pg.evaluate((esGal, t0) => {
      const m = document.querySelector('.mascota');
      if (m) { m.classList.remove('asomada'); m.style.transition = 'none'; }
      // el carrusel arranca de la primera foto cuando la galeria entra
      if (esGal) window.__gal0 = t0;
    }, tramo.a === '#sec-galeria', n / FPS);

    for (let i = 0; i < cuadros; i++) {
      const y = desde + (hasta - desde) * suave(i / Math.max(1, cuadros - 1));
      await pg.evaluate((yy, t, reloj, pas, dentro) => {
        window.scrollTo(0, yy);
        eval(reloj)(t);
        const m = document.querySelector('.mascota');
        if (m) {
          if (!pas) { m.style.opacity = '0'; m.style.transform = 'translateX(110%)'; }
          else {
            // entra en 0,7s, se queda, y se va en los ultimos 0,7s
            const ent = Math.min(1, dentro / 0.7);
            const sal = Math.min(1, Math.max(0, (dentro - (pas - 0.7)) / 0.7));
            const p = ent * (1 - sal);
            const rebote = p < 1 ? 1 - Math.pow(1 - p, 3) : 1;
            m.style.opacity = String(Math.min(1, p * 1.6));
            m.style.transform = `translateX(${110 - 102 * rebote}%)`;
          }
        }
      }, y, (n / FPS), RELOJ, tramo.pascal ? tramo.seg : 0, (i / FPS));
      await pg.screenshot({ path: path.join(SALIDA, String(n).padStart(5, '0') + '.png') });
      n++;
    }
    desde = hasta;
  }

  console.log(`${n} cuadros = ${(n / FPS).toFixed(1)}s`);
  await pg.close();
  await b.disconnect();
})();
