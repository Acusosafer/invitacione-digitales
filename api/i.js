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

  // La página real. No se pasa por /i, así que no hay bucle.
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
  const img    = absoluta(C.foto_hero || C.foto_splash || '/logo.png', base);

  const tags = `
  <title>${esc(titulo)}</title>
  <meta name="description" content="${esc(desc)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Invitaciones Digitales">
  <meta property="og:locale" content="es_AR">
  <meta property="og:title" content="${esc(titulo)}">
  <meta property="og:description" content="${esc(desc)}">
  <meta property="og:image" content="${esc(img)}">
  <meta property="og:image:width" content="1920">
  <meta property="og:image:height" content="1080">
  <meta property="og:url" content="${esc(base + '/i' + qs)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${esc(titulo)}">
  <meta name="twitter:description" content="${esc(desc)}">
  <meta name="twitter:image" content="${esc(img)}">
`;

  // Se BORRAN las etiquetas viejas antes de poner las nuevas. Dejar las dos
  // versiones haría que cada robot elija una distinta.
  html = html
    .replace(/<meta[^>]*id="og-[^"]*"[^>]*>\s*/gi, '')
    .replace(/<title[^>]*>[\s\S]*?<\/title>\s*/i, '')
    .replace('</head>', tags + '</head>');

  // El JS de la página vuelve a escribir las OG en el navegador; da igual,
  // el robot ya leyó las de arriba. Lo que el invitado ve no cambia.
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'public, max-age=0, s-maxage=300, stale-while-revalidate=86400');
  res.statusCode = 200;
  res.end(html);
};
