# HANDOFF — estado al 05/08/2026

> Para retomar en otra sesión. Leer junto con `CLAUDE.md`.

---

## Dónde vive todo

**Supabase:** proyecto `ldvosdztnhrvrqxnjuco` ("Lo de Inés"), cuenta **`fernando_22_19`** — NO
la de `fernandoacusosa10`. Schema propio `invitaciones`. El conector MCP **no llega** a ese
proyecto: el SQL se le pasa a Fer para el SQL Editor y se verifica desde afuera con `curl`.

```
https://supabase.com/dashboard/project/ldvosdztnhrvrqxnjuco/sql/new
```

**Migraciones:** `sql/001` schema y funciones · `sql/002` los 12 demos · `sql/003` bucket de
Storage. Las tres ya corridas. Las tres son idempotentes.

**El sitio ya no es 100% estático.** Hay una función serverless (`api/i.js`) y un `vercel.json`.

---

## Lo que quedó funcionando

- **Seguridad de datos.** `anon` sólo lee `(id, config)` de `eventos`; no toca `confirmaciones`
  ni `ajustes`. Todo lo privilegiado pasa por 8 funciones `SECURITY DEFINER`.
- **Storage.** Bucket `invitaciones`: `anon` puede leer y subir, **no actualizar ni borrar** —
  así nadie puede pisar las fotos de un cliente en producción.
- **Regla de contraste.** Ningún cliente puede armar una invitación ilegible, elija los colores
  que elija. 48 combinaciones verificadas, piso 4,50:1.
- **Duplas tipográficas.** Ocho combinaciones ya probadas. El selector antes no hacía nada.
- **Vista previa de WhatsApp.** Los links se comparten como `/i?evento=...`. Muestra foto,
  nombre, fecha y salón, y saluda con el género correcto.
- **12 demos** con fotos y música reales.
- **Landing rediseñada**: el color inunda la pantalla y cambia con cada invitación.

---

## Pendientes, en orden

1. **Google Safe Browsing.** Revisión pedida el 31/07. Hasta que la levanten, Chrome muestra
   "Peligroso" y **no hay que publicar la campaña de agosto**.
2. **Dominio propio** (~15 USD/año). Es el arreglo de fondo del punto 1: `vercel.app` es
   reputación compartida y la marca puede volver sin que haya nada que corregir.
3. **Identidad en el footer del sitio público.** Falta que Fer defina cómo firma el negocio,
   qué contacto va y si tiene Instagram. Hoy el sitio no dice quién es en ninguna parte.
4. **Cuántas horas lleva una invitación** de punta a punta. Sin ese dato no se sabe si los
   $50.000 cierran o si está trabajando barato.
5. **Terminar `almamia15`**: volver a subir la portada (la vieja pesa 2,26 MB) y cambiar
   `foto_galeria_2`, que todavía apunta a `/assets/valentina15/...` de cuando se copió ese evento.
6. **Escuchar dos temas** asignados con dudas: `luna15` (capoeira, se pidió folk de jardín) y
   `boda-julieta` (se llama "morning" y se pidió ambient nocturno).
7. **Álbum compartido con QR** — lo único relevante que tiene la competencia y no está acá.
   Acotado: Storage + link público por evento.
8. **Dos mejoras de ergonomía del admin**: que `verificar_clave` distinga "falta configurar el
   hash" de "clave incorrecta" (hoy dice lo mismo para las dos cosas), y un formulario para
   cambiar la clave de superadmin sin pasar por SQL.

---

## Cosas que conviene no olvidar

- **No borrar `google03f5ed89092823df.html`**: si desaparece, Google revoca la verificación de
  Search Console.
- **`.vercelignore`** saca del deploy los `.md`, `sql/`, `publicidad/`,
  `generar-hash-superadmin.html` y las utilidades. Antes estaban todos públicos, y `HANDOFF.md`
  exponía la anon key y nombres de clientes.
- **`generar-hash-superadmin.html` ya no está publicado.** Se abre desde la copia local.
- **`admin123` es la clave de CLIENTE** — sólo desbloquea Resumen, Invitados, Links, Mesas y
  Vista Previa. Los tres módulos de armado son de superadmin.
- **Si Fer pierde la clave de superadmin**: genera un hash nuevo con la herramienta local y
  corre un `insert ... on conflict do update` sobre `invitaciones.ajustes`.
- **Chrome traduciendo la página rompe el panel de Supabase** (error `removeChild`). Se
  desactiva con "Nunca traducir supabase.com", o se usa una ventana de incógnito.
- **Riesgos aceptados a propósito** (son de spam, no fugas): crear un evento nuevo no pide clave
  —hace falta para dar de alta clientes— y confirmar asistencia es libre para quien sepa el
  slug, con tope de 20 filas por envío.

---

## Trampas conocidas

- **`/i` no puede tener caché compartida.** La respuesta cambia según el User-Agent y el CDN no
  distingue: un invitado real terminaría recibiendo la página mínima del robot.
- **No borrar los `<meta id="og-*">` ni el `<title id="pg-title">`** de `invitacion.html`: el JS
  los busca por id y sin ellos corta el arranque, dejando la invitación colgada.
- **`/_vercel/image` no existe** en un deploy estático sin framework: devuelve 404.
- **Los pesos de Google Fonts tienen que ser los reales de cada familia.** Si se pide uno que no
  existe, falla el pedido entero y no carga ninguna fuente.
- **WhatsApp cachea la vista previa por URL.** Para probar cambios hay que usar un nombre de
  invitado distinto cada vez.

---

## Campaña de agosto

Pieza en `publicidad/agosto-a.html` (1080×1080, se exporta con F12 → captura de nodo).
"Agosto es de las A": 40% off sobre $50.000 a cambio de poder mostrar la invitación como
ejemplo. Escasez honesta: "tomo 15 este mes, las hago yo una por una".
Contexto de precio y competencia en la memoria `precio-y-competencia`.
