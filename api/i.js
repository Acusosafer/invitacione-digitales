/**
 * Vista previa de la invitación para WhatsApp, Instagram y demás.
 *
 * EL PROBLEMA
 * `invitacion.html` escribe las etiquetas Open Graph con JavaScript, después
 * de traer el config de Supabase. Pero los robots que arman la vista previa
 * NO ejecutan JavaScript: piden el HTML crudo, leen lo que encuentran y se
 * van. Veían siempre `logo.png` y un texto genérico, para toda invitación.
 *
 * LA SOLUCIÓN
 * Esta función sirve la misma página, pero con las etiquetas ya escritas del
 * lado del servidor. El invitado ve exactamente lo mismo que antes; el robot
 * ve el nombre, la foto y la fecha de ESE evento.
 *
 * Se usa como `/i?evento=...` (ver el rewrite en vercel.json).
 * `/invitacion.html` sigue existiendo tal cual para los iframes de la landing.
 */

const SUPA_URL = 'https://ldvosdztnhrvrqxnjuco.supabase.co';
// Anon key: es pública por diseño y sólo puede leer (id, config) de eventos.
const SUPA_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdm9zZHp0bmhydnJxeG5qdWNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUyOTY1MjAsImV4cCI6MjEwMDg3MjUyMH0.u64wnWOA-Bp0NfOR3tLOAtSkG34P-ApTS00KwTEkGRM';

/** Escapa para meter texto dentro de un atributo HTML sin romper nada. */
function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

/* ════════════════════════════════════════════════════════════════════
   CÓMO SALUDAR AL INVITADO

   "estás invitada" / "estás invitado" / "están invitados".

   Regla de oro: sólo se afirma el género cuando hay certeza. Equivocarse
   acá no es un detalle — a alguien le llega SU invitación con el género
   cambiado, y eso queda peor que una frase neutra.

   En castellano el final del nombre es muy confiable: -a es de mujer, -o
   es de varón. Con lo que termina en consonante no hay regla (Isabel y
   Nicolás terminan igual de "mal"), así que ahí sólo se decide si el
   nombre está en las listas; si no, se usa una frase que sirve para
   cualquiera. El admin puede forzarlo con &t= cuando lo sabe.
   ════════════════════════════════════════════════════════════════════ */

// Nombres de mujer que la regla del final NO acierta: terminan en
// consonante o en -o. Pesan mucho los de origen extranjero, que es donde
// una regla mecánica más se equivoca.
const NOMBRES_F = new Set(['isabel','raquel','beatriz','ines','mercedes','carmen',
  'pilar','soledad','abril','esther','ruth','judith','noemi','miriam','karen',
  'jennifer','jazmin','belen','ailen','aylen','rocio','milagros','dolores',
  'lourdes','nair','maribel','jaqueline','jacqueline','yanet','janet','nicol',
  'guadalupe','caridad','trinidad','libertad','anahi','magali','itati','soledad',
  'consuelo','rosario','socorro','amparo','remedios','mercedes','luz','flor',
  'estefani','yamila','shirley','jessica','vanesa','ashley','britney']);

// Nombres de varón que la regla tampoco acierta: terminan en -a o en
// consonante. Los que terminan en consonante son los más comunes del país,
// y dejarlos sin resolver daba "Juan, te esperamos", que suena a que no
// sabemos quién es.
const NOMBRES_M = new Set([
  // terminan en -a
  'bautista','luca','nicola','elia',
  // terminan en -s
  'lucas','tomas','matias','elias','tobias','jeremias','isaias','zacarias',
  'jesus','luis','carlos','marcos','andres','alexis','dionisis','nicolas',
  // terminan en -n
  'juan','martin','sebastian','julian','adrian','fabian','cristian','christian',
  'damian','german','hernan','esteban','gaston','agustin','joaquin','benjamin',
  'fermin','simon','ramon','alan','ivan','kevin','brian','jonathan','jonatan',
  'dylan','jean','efrain','marlon','milton','nelson','wilson','edison',
  // terminan en -l
  'gabriel','daniel','manuel','miguel','rafael','ismael','joel','axel',
  'ezequiel','nahuel','samuel','emanuel','leonel','lionel','uriel','abel',
  // otras consonantes
  'javier','walter','oscar','nestor','hector','victor','edgar','omar','cesar',
  'salvador','amadeo','josue','ander','alexander','michael','peter']);

// Deliberadamente FUERA de las dos listas, porque en Argentina se usan para
// ambos: ariel, noel, rene, cruz, yael, robin, alexis(m mayormente pero...).
// Caen en la frase neutra, que es lo correcto cuando de verdad no se sabe.

function normalizar(s) {
  return String(s || '').toLowerCase()
    .normalize('NFD').replace(/[̀-ͯ]/g, '')   // saca tildes
    .replace(/[^a-z\s]/g, ' ').trim();
}

/**
 * Devuelve cómo dirigirse al invitado.
 * @param {string} invitado  lo que escribió el admin
 * @param {string} forzado   'f' | 'm' | 'p' si el admin lo eligió a mano
 */
function saludoPara(invitado, forzado) {
  if (forzado === 'f') return 'estás invitada';
  if (forzado === 'm') return 'estás invitado';
  if (forzado === 'p') return 'están invitados';

  const t = normalizar(invitado);
  if (!t) return 'te esperamos';

  // Grupo: "Familia González", "Los Ramírez", "Ana y José".
  if (/^(familia|flia|los|las)\b/.test(t) || /\sy\s/.test(t)) return 'están invitados';

  const nombre = t.split(/\s+/)[0];
  // Las listas van primero: son las excepciones a la regla del final.
  if (NOMBRES_F.has(nombre)) return 'estás invitada';
  if (NOMBRES_M.has(nombre)) return 'estás invitado';

  const fin = nombre.slice(-1);
  if (fin === 'a') return 'estás invitada';
  if (fin === 'o') return 'estás invitado';

  // Consonante y fuera de las listas: no hay forma de saberlo. Antes de
  // arriesgar y errarle, se usa algo que le sirve a cualquiera.
  return 'te esperamos';
}

/** Las OG exigen URL absoluta: una ruta tipo /assets/... no le sirve al robot. */
function absoluta(url, base) {
  if (!url) return '';
  if (/^https?:\/\//i.test(url)) return url;
  return base + (url.startsWith('/') ? '' : '/') + url;
}

module.exports = async function handler(req, res) {
  const url   = new URL(req.url, 'http://x');
  const qs    = url.search || '';
  const proto = (req.headers['x-forwarded-proto'] || 'https').split(',')[0];
  const host  = req.headers['x-forwarded-host'] || req.headers.host;
  const base  = `${proto}://${host}`;

  const evento   = (url.searchParams.get('evento') || 'valentina15').trim();
  const invitado = (url.searchParams.get('invitado') || '').trim();
  // t=f|m|p — lo pone el admin cuando quiere decidirlo a mano.
  const trato    = (url.searchParams.get('t') || '').toLowerCase();

  // ¿Es un robot armando la vista previa, o una persona?
  const ua  = String(req.headers['user-agent'] || '');
  const bot = /whatsapp|facebookexternalhit|facebookcatalog|twitterbot|slackbot|discordbot|telegrambot|linkedinbot|pinterest|skypeuripreview|embedly|redditbot|bingbot|googlebot|iframely/i.test(ua);

  // El config del evento. Si falla, se sirve la página igual: perder la vista
  // previa es molesto, no poder abrir la invitación sería grave.
  let C = {};
  try {
    const r = await fetch(
      `${SUPA_URL}/rest/v1/eventos?select=config&id=eq.${encodeURIComponent(evento)}`,
      { headers: { apikey: SUPA_KEY, Authorization: `Bearer ${SUPA_KEY}`,
                   'Accept-Profile': 'invitaciones' } });
    if (r.ok) C = (await r.json())[0]?.config || {};
  } catch (e) { /* se sigue con lo que haya */ }

  const nombre = C.nombre || 'Nuestra fiesta';
  const tipo   = C.tipo   || '';
  const titulo = invitado ? `${invitado}, ${saludoPara(invitado, trato)} — ${nombre}`
                          : [nombre, tipo].filter(Boolean).join(' · ');
  const desc   = [C.subtitulo, C.fecha_texto, C.salon].filter(Boolean).join(' · ')
                 || 'Abrí tu invitación y confirmá tu asistencia.';
  // Se publica la foto tal cual está guardada.
  //
  // Se probó pasarla por el optimizador de Vercel (/_vercel/image) para
  // garantizar el tamaño, pero en un sitio estático sin framework ese
  // endpoint no existe: devuelve 404. Habría publicado una imagen rota, que
  // es peor que una pesada.
  //
  // El control del peso queda entonces del lado del admin, que desde ahora
  // comprime a 1920px y JPEG 85% ANTES de subir. Lo que ya estaba cargado hay
  // que volver a subirlo una vez.
  // Sin fotos cargadas cae en la placa de marca: 1200x630 y con fondo
  // oscuro. `logo.png` es transparente y en WhatsApp, que la muestra
  // sobre blanco, los dorados claros desaparecían.
  const img = absoluta(C.foto_hero || C.foto_splash || '/logo-og.png', base);

  // A los robots se les devuelve una página mínima con SOLO las etiquetas.
  // La invitación completa pesa 73 KB y no le sirve de nada a un robot: le
  // da más para leer, más para tardar y más para equivocarse. Con esto la
  // vista previa se resuelve en un par de KB.
  if (bot) {
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    // Sin caché compartida: esta respuesta CAMBIA según el User-Agent, y el
    // CDN no distingue por eso. Con s-maxage, el primero que entraba —robot o
    // persona— dejaba su versión guardada para todos, y un invitado podía
    // recibir la página mínima del robot en vez de su invitación.
    res.setHeader('Cache-Control', 'private, no-store');
    res.statusCode = 200;
    return res.end(`<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8">
<title>${esc(titulo)}</title>
<meta name="description" content="${esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Invitaciones Digitales">
<meta property="og:locale" content="es_AR">
<meta property="og:title" content="${esc(titulo)}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:image" content="${esc(img)}">
<meta property="og:image:secure_url" content="${esc(img)}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="675">
<meta property="og:image:alt" content="${esc(nombre)}">
<meta property="og:url" content="${esc(base + '/i' + qs)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${esc(titulo)}">
<meta name="twitter:description" content="${esc(desc)}">
<meta name="twitter:image" content="${esc(img)}">
</head><body><a href="/invitacion.html${esc(qs)}">${esc(titulo)}</a></body></html>`);
  }

  // Para personas: la invitación de verdad. No se pasa por /i, no hay bucle.
  let html;
  try {
    const r = await fetch(`${base}/invitacion.html`);
    if (!r.ok) throw new Error('HTTP ' + r.status);
    html = await r.text();
  } catch (e) {
    res.statusCode = 302;
    res.setHeader('Location', '/invitacion.html' + qs);
    return res.end();
  }

  // Las etiquetas existentes se REESCRIBEN conservando su id. No se borran:
  // el JS de la invitación hace document.getElementById('og-title').content
  // y si el elemento no está, tira TypeError y corta initApp() antes de
  // pintar el splash. La página quedaba colgada con el círculo vacío.
  const reemplazar = (h, id, etiqueta) =>
    h.replace(new RegExp(`<meta[^>]*id="${id}"[^>]*>`, 'i'), etiqueta);

  html = reemplazar(html, 'og-title', `<meta id="og-title" property="og:title" content="${esc(titulo)}">`);
  html = reemplazar(html, 'og-desc',  `<meta id="og-desc" property="og:description" content="${esc(desc)}">`);
  html = reemplazar(html, 'og-img',   `<meta id="og-img" property="og:image" content="${esc(img)}">`);
  html = reemplazar(html, 'og-url',   `<meta id="og-url" property="og:url" content="${esc(base + '/i' + qs)}">`);
  html = html.replace(/<title([^>]*)>[\s\S]*?<\/title>/i, `<title$1>${esc(titulo)}</title>`);

  // ── La paleta, servida ya resuelta ────────────────────────────────────
  // Sin esto la página arranca con los valores por defecto del CSS —fondo
  // blanco y acento verde, que son los de valentina15— y recién cuando
  // Supabase contesta salta a los colores de verdad. Medido en una conexión
  // de celular: 1,7 segundos viendo OTRA invitación antes de la propia.
  //
  // No cuesta un pedido más: el config ya se trajo arriba para armar la vista
  // previa. Acá solo se escribe en el head, que el navegador lee antes de
  // pintar el primer píxel.
  //
  // Los colores los elige el cliente desde el panel y terminan dentro de una
  // etiqueta <style>, así que se validan uno por uno: solo hexadecimal. Un
  // valor raro se descarta y esa variable se queda con la del CSS.
  const hex = v => (typeof v === 'string' && /^#(?:[0-9a-f]{3}|[0-9a-f]{6})$/i.test(v.trim())) ? v.trim() : '';
  const paleta = [
    ['--primary', hex(C.color_1)],
    ['--secondary', hex(C.color_2)],
    ['--bg', hex(C.color_bg)],
  ].filter(([, v]) => v).map(([k, v]) => `${k}:${v}`).join(';');

  // Las que no existen en el HTML original se agregan al final del head.
  const extra = `${paleta ? `<style id="paleta-servidor">:root{${paleta}}</style>` : ''}
  <meta name="description" content="${esc(desc)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Invitaciones Digitales">
  <meta property="og:locale" content="es_AR">
  <meta property="og:image:width" content="1920">
  <meta property="og:image:height" content="1080">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${esc(titulo)}">
  <meta name="twitter:description" content="${esc(desc)}">
  <meta name="twitter:image" content="${esc(img)}">
`;
  // ── La query, para el navegador ───────────────────────────────────────
  // Cuando se entra por una ruta limpia como /muestra, el rewrite de Vercel
  // le pasa `?evento=…&muestra=1` a ESTA función, pero la barra del navegador
  // sigue diciendo /muestra: `location.search` queda VACÍO.
  // Sin esto, /muestra armaba la vista previa con los datos de Alma y después
  // abría la invitación de valentina15 —el evento por defecto— con el RSVP
  // vivo, escribiendo filas reales. Verificado antes de arreglarlo.
  const extraQs = `<script id="qs-servidor">window.__QS_SERVIDOR=${
    JSON.stringify(qs)};</script>`;

  html = html.replace('</head>', extra + extraQs + '</head>');

  // El JS de la página vuelve a escribir las OG en el navegador; da igual,
  // el robot ya leyó las de arriba. Lo que el invitado ve no cambia.
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  // Misma razón: la respuesta depende del User-Agent, así que no puede vivir
  // en una caché compartida. La función responde en menos de un segundo y el
  // volumen es bajo, así que no cachear no cuesta nada.
  res.setHeader('Cache-Control', 'private, no-store');
  res.statusCode = 200;
  res.end(html);
};
