/* ══════════════════════════════════════════════════════════════════
   RECEPTOR DE FOTOS DE LA FIESTA — Google Apps Script
   Se pega en script.google.com y se publica como aplicación web con
   "Ejecutar como: Yo" y "Quién tiene acceso: Cualquier usuario".

   El invitado NUNCA ve Google: escanea el QR, la página /deseos le
   achica la foto en el celular y se la manda a este programa, que corre
   con la cuenta de Fer y la guarda en su Drive:

       Mi unidad / Fotos de las fiestas / <evento> / 0001 - mesa7 - Juan.jpg

   ⚠️ Esta URL la puede llamar cualquiera (así funciona sin login), así
   que se defiende sola:
     - sólo acepta los eventos de la lista EVENTOS, y hasta su fecha;
     - sólo JPEG (lo que manda la página después de achicar), hasta 6 MB;
     - un tope de fotos por evento, para que nadie llene los 15 GB.

   Para una fiesta nueva: agregarla a EVENTOS y "Implementar → Gestionar
   implementaciones → editar → Nueva versión". La URL no cambia.
   ══════════════════════════════════════════════════════════════════ */

const EVENTOS = {
  // hasta: último día en que se aceptan fotos (hora de Argentina).
  almamia15: { hasta: '2026-09-20', tope: 3000 },
};

const RAIZ = 'Fotos de las fiestas';
const PROPS = PropertiesService.getScriptProperties();

function doGet() {
  return json_({ ok: true, hola: 'receptor de fotos' });
}

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents);
    const ev = String(d.evento || '');
    const cfg = EVENTOS[ev];
    if (!cfg) return json_({ ok: false, error: 'cerrado' });
    if (cfg.hasta && new Date() > new Date(cfg.hasta + 'T23:59:59-03:00')) {
      return json_({ ok: false, error: 'cerrado' });
    }

    const datos = String(d.datos || '');
    if (datos.length > 8 * 1024 * 1024) return json_({ ok: false, error: 'grande' });
    const bytes = Utilities.base64Decode(datos);
    // JPEG empieza con FF D8 (en Apps Script los bytes vienen con signo).
    if (bytes.length < 3 || bytes[0] !== -1 || bytes[1] !== -40) {
      return json_({ ok: false, error: 'formato' });
    }

    // El número y la carpeta se sacan con candado: si dos fotos llegan a la
    // vez sin él, las dos crean su propia carpeta "almamia15".
    const lock = LockService.getScriptLock();
    lock.waitLock(20000);
    let n, carpeta;
    try {
      n = Number(PROPS.getProperty('n_' + ev) || 0) + 1;
      if (n > (cfg.tope || 2000)) return json_({ ok: false, error: 'lleno' });
      PROPS.setProperty('n_' + ev, String(n));
      carpeta = carpeta_(ev);
    } finally {
      lock.releaseLock();
    }

    const nombre = limpiar_(d.nombre).slice(0, 40);
    const mesa = limpiar_(d.mesa).slice(0, 10);
    const archivo = [('000' + n).slice(-4), mesa ? 'mesa ' + mesa : '', nombre]
      .filter(Boolean).join(' - ') + '.jpg';
    carpeta.createFile(Utilities.newBlob(bytes, 'image/jpeg', archivo));
    return json_({ ok: true, n: n });
  } catch (err) {
    console.error(err);
    return json_({ ok: false, error: 'interno' });
  }
}

function carpeta_(ev) {
  const guardada = PROPS.getProperty('carpeta_' + ev);
  if (guardada) {
    try { return DriveApp.getFolderById(guardada); } catch (e) { /* la borraron: se crea otra */ }
  }
  const raices = DriveApp.getFoldersByName(RAIZ);
  const raiz = raices.hasNext() ? raices.next() : DriveApp.createFolder(RAIZ);
  const hijas = raiz.getFoldersByName(ev);
  const carpeta = hijas.hasNext() ? hijas.next() : raiz.createFolder(ev);
  PROPS.setProperty('carpeta_' + ev, carpeta.getId());
  return carpeta;
}

// Lo que escribe el invitado termina en un nombre de archivo.
function limpiar_(s) {
  return String(s || '').replace(/[\\/:*?"<>|\u0000-\u001f]/g, '').replace(/\s+/g, ' ').trim();
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o))
    .setMimeType(ContentService.MimeType.JSON);
}

/* Correr UNA vez a mano desde el editor (botón ▶ con "autorizar" elegida
   arriba): dispara el pedido de permisos de Drive, y crea la carpeta. */
function autorizar() {
  const c = carpeta_('almamia15');
  console.log('Carpeta lista: ' + c.getUrl());
}
