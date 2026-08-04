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
  const titulo = invitado ? `${invitado}, estás invitado — ${nombre}`
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
  const img = absoluta(C.foto_hero || C.foto_splash || '/logo.png', base);

  // A los robots se les devuelve una página mínima con SOLO las etiquetas.
  // La invitación completa pesa 73 KB y no le sirve de nada a un robot: le
  // da más para leer, más para tardar y más para equivocarse. Con esto la
  // vista previa se resuelve en un par de KB.
  if (bot) {
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('Cache-Control', 'public, s-maxage=600, stale-while-revalidate=86400');
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

  // Las que no existen en el HTML original se agregan al final del head.
  const extra = `
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
  html = html.replace('</head>', extra + '</head>');

  // El JS de la página vuelve a escribir las OG en el navegador; da igual,
  // el robot ya leyó las de arriba. Lo que el invitado ve no cambia.
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'public, max-age=0, s-maxage=300, stale-while-revalidate=86400');
  res.statusCode = 200;
  res.end(html);
};
