# Invitaciones Digitales Oficial

## Qué es este proyecto

Sistema de invitaciones digitales personalizadas para eventos (15 años, casamientos, etc.). Cada evento tiene una URL única, configuración almacenada en Supabase, y se comparten links personalizados por WhatsApp a cada invitado.

**Stack:** HTML/CSS/JS vanilla — sin framework ni bundler.

⚠️ **Ya no es 100% estático.** Hay **una** función serverless: `api/i.js`, que arma la vista
previa de WhatsApp del lado del servidor (los robots no ejecutan JavaScript, así que no hay
otra forma). El rewrite `/i` → `/api/i` está en `vercel.json`. Es la única excepción y conviene
que siga siéndolo.

**Backend:** Supabase — proyecto `ldvosdztnhrvrqxnjuco` ("Lo de Inés"), schema `invitaciones`

## Archivos principales

| Archivo | Función |
|---|---|
| `invitacion.html` | Invitación visible al invitado — carga config desde Supabase según `?evento=` |
| `admin.html` | Panel de control — gestión de invitados, mesas, links, diseño |
| `index.html` | Landing page del servicio |
| `api/i.js` | **Vista previa de WhatsApp.** Los links se comparten como `/i?evento=...` |
| `vercel.json` | Rewrite `/i` → `/api/i` |
| `.vercelignore` | Qué NO se publica: `.md`, `sql/`, `publicidad/`, herramientas internas |
| `generar-hash-superadmin.html` | Genera el hash SHA-256 de la clave de superadmin (no se deploya) |
| `sql/001_schema_invitaciones.sql` | Schema, tablas, funciones y permisos |
| `sql/002_demos.sql` | Los 12 eventos demo de la landing |
| `sql/003_storage.sql` | Bucket de Storage y sus permisos |
| `logo.png` / `logo-og.png` | Marca. El `-og` es el respaldo de vista previa (1200×630, fondo oscuro) |
| `publicidad/agosto-a.html` | Placa de la campaña (1080×1080) |
| `publicidad/instagram.md` | Perfil, bio y prompts de las piezas. No se publica |
| `publicidad/ig-perfil.png` | Foto de perfil de Instagram (1080×1080) |
| `generate_logo.py` + `temp_logo.html` | Generación del logo |

## Vista previa al compartir (leer antes de tocar el `<head>`)

Los links van como **`/i?evento=...&invitado=...`**, no `/invitacion.html`. Los robots de
WhatsApp no ejecutan JavaScript, así que las etiquetas Open Graph las arma `api/i.js` del lado
del servidor.

Tres cosas que **no** hay que hacer:
1. **No borrar** los `<meta id="og-*">` ni el `<title id="pg-title">` de `invitacion.html`: el JS
   los busca por id y sin ellos corta el arranque — la invitación queda colgada con el splash vacío.
2. **No poner `Cache-Control` compartido en `/i`.** La respuesta cambia según el User-Agent y el
   CDN no distingue: un invitado real recibiría la página mínima del robot.
3. **`/_vercel/image` no existe** en un deploy estático: devuelve 404.

El saludo concuerda en género (`estás invitada` / `invitado` / `invitados`), con `&t=f|m|p` para
forzarlo desde el admin. Cuando no hay certeza usa "te esperamos" en vez de arriesgar.

## Fotos: se comprimen solas al subir

`admin.html` achica a 1920px y pasa a JPEG 85% **antes** de subir. Motivo: WhatsApp descarta las
imágenes de más de ~600 KB y la vista previa sale sin foto. Además la invitación carga mucho más
rápido con datos móviles.

En Storage, `anon` puede **leer e insertar pero no actualizar ni borrar**: así nadie puede pisar
las fotos de un cliente en producción. Por eso también `upsert: false`.

## Supabase

```
URL:    https://ldvosdztnhrvrqxnjuco.supabase.co
Schema: invitaciones   (NO `public`, que es del almacén "Lo de Inés")
```

**Por qué este proyecto:** el original `fybwovlewphtdmjmwyjn` quedó INACTIVE y no se
puede despertar — la cuenta `fernandoacusosa10` llegó al límite de 2 proyectos
activos del plan free. "Lo de Inés" (cuenta `fernando_22_19`) se usa a diario, así
que nunca se pausa por inactividad. **Es un puente, no el destino:** cuando haya
clientes pagando, esto merece proyecto propio.

⚠️ **El conector MCP de Supabase no llega a este proyecto** (apunta a la org de
`fernandoacusosa10`). El SQL se le pasa a Fer para que lo pegue en el SQL Editor,
y se verifica desde afuera con `curl` + anon key.

### Modelo de seguridad — leer antes de tocar la capa de datos

La app es 100% cliente con la anon key a la vista de cualquier invitado. **RLS no
alcanza:** filtra por *quién sos*, y acá el admin y un invitado son el mismo rol
`anon` con la misma key. Cualquier policy que le permita al admin leer los
invitados de un evento, se los permite a cualquiera.

Por eso:
- `anon` lee **solo `(id, config)`** de `eventos` — `admin_password` queda afuera por
  GRANT de columna. Un `select=*` devuelve `42501`.
- `anon` **no tiene ningún acceso** a `confirmaciones` ni a `ajustes`.
- Todo lo privilegiado pasa por funciones `SECURITY DEFINER` que verifican la clave
  dentro de Postgres. Todas con `set search_path = ''` — sin eso se pueden secuestrar.
- El hash de superadmin vive en `ajustes`, no en el código fuente.

**Nunca** volver a poner `.from('confirmaciones')` ni `select('admin_password')` en
el cliente. Si hace falta una operación nueva, va como función.

### Tablas (schema `invitaciones`)

**`eventos`** — `id` (slug), `config` (jsonb), `admin_password`, `created_at`, `updated_at`

**`confirmaciones`** — `id`, `evento_id` (FK), `invitado_url`, `nombre`, `apellido`,
`asiste` (`si`|`no`|`pendiente`, con CHECK), `personas` (siempre 1), `dieta`,
`mensaje` (canción sugerida), `mesa`, `created_at`

**`ajustes`** — `clave`/`valor`. Hoy solo `superadmin_hash`.

### Funciones (todo el acceso privilegiado)

| Función | Para qué |
|---|---|
| `verificar_clave(evento, clave)` | Devuelve `'super'` \| `'cliente'` \| `null` |
| `ya_confirmo(evento, invitado)` | Booleano — sin datos personales |
| `rsvp_enviar(evento, invitado, filas)` | Borra pre-cargadas + inserta, en una transacción |
| `admin_invitados(evento, clave)` | La lista completa, con clave |
| `admin_guardar_evento(evento, clave, config, nueva_clave)` | Crear o actualizar |
| `admin_prealta(evento, clave, invitado, cupos)` | Filas `pendiente` del generador de links |
| `admin_actualizar_fila(evento, clave, id, asiste, mesa)` | Editar desde el panel |
| `admin_borrar_fila(evento, clave, id)` | Borrar un invitado |

### Storage

Bucket `invitaciones` — archivos subidos desde el admin se guardan como `{eventoId}/{key}_{timestamp}.{ext}`.

## Schema de `config` (JSONB)

```json
{
  "nombre": "Valentina",
  "tipo": "MIS 15",
  "subtitulo": "Quiero que seas parte...",
  "fuente": "Jost",
  "color_1": "#1a1a1a",
  "color_2": "#d6ecc0",
  "color_bg": "#ffffff",
  "foto_splash": "https://...",
  "foto_hero": "https://...",
  "mensaje": "Texto personal...",
  "mensaje_firma": "Con amor, Valentina",
  "fecha_iso": "2025-06-14T21:00",
  "fecha_texto": "Sábado 14 de junio, 2025",
  "hora_texto": "21:00",
  "countdown_style": "flex | grid",
  "salon": "Salón Magnolia",
  "direccion": "Av. San Martín 1250",
  "maps_url": "https://maps.google.com/...",
  "dresscode_titulo": "ELEGANTE",
  "dresscode_texto": "Traje y vestido de fiesta",
  "alias_pago": "valentina.15.mp",
  "regalo_texto": "...",
  "hashtag": "#ValentinaXV",
  "hashtag_texto": "...",
  "foto_hashtag": "https://...",
  "instagram_url": "https://...",
  "tiktok_url": "https://...",
  "musica_url": "https://...",
  "foto_galeria_1": "https://...",
  "foto_galeria_2": "https://...",
  "foto_galeria_3": "https://...",
  "foto_galeria_4": "https://...",
  "rsvp_limite": "2 de junio",
  "layout": {
    "show_mensaje": true,
    "show_countdown": true,
    "show_gallery": true,
    "show_ubicacion": true,
    "show_dresscode": true,
    "show_gift": true,
    "show_hashtag": true,
    "show_rsvp": true,
    "order": ["hero", "mensaje", "countdown", "galeria", "ubicacion", "dresscode", "regalos", "hashtag", "rsvp"]
  }
}
```

## URL params de la invitación

```
invitacion.html?evento=valentina15&invitado=Juan+Perez&personas=2&mesa=5
```

- `evento` — ID del evento (default: `valentina15`)
- `invitado` — Nombre del invitado (pre-rellena el form y muestra saludo)
- `personas` — Cupos asignados (determina cuántas opciones de personas aparecen)
- `mesa` — Mesa pre-asignada (se muestra en el splash y en el RSVP)

## El celular es el dispositivo principal — de los dos lados

La invitación siempre fue mobile-first. **El panel no**, y eso se arrastró hasta el
06/08/2026: medía 787px de ancho sobre un viewport de 390. La culpable era la barra
superior, que no envolvía y estiraba todo lo de abajo con ella.

Regla: **antes de dar por terminada cualquier pantalla del panel, medirla a 390px** y
confirmar que `document.documentElement.scrollWidth === window.innerWidth`. Un elemento
que no envuelve estira el documento entero, no solo su fila.

Debajo de 860px: el menú lateral es un cajón, la barra baja a dos líneas, y cada fila de
tabla se convierte en ficha con el nombre de la columna al lado del dato (`data-col`).
Las celdas vacías llevan `class="vacio"` y allá se esconden — un "—" en la tabla es una
raya, en la ficha es un renglón entero que no dice nada.

## Admin

Acceso: `admin.html?evento=valentina15`

- **Clave cliente** — En `eventos.admin_password` (default `admin123`). Da acceso a: Resumen, Invitados, Links, Mesas, Vista Previa.
- **Clave superadmin** — Su hash SHA-256 está en `invitaciones.ajustes`. Desbloquea además: Editor de Secciones, Diseño Global, Historial. Para cambiarla: `generar-hash-superadmin.html` + `update` sobre esa tabla.

Ambas se verifican con `verificar_clave()` en Postgres. La clave queda en memoria
(`adminClave`) y se re-valida en **cada** operación: no alcanza con haber entrado una vez.

### Link generator

Al generar un link, el admin **pre-inserta filas en `confirmaciones`** con `asiste: 'pendiente'` para el titular y cada acompañante. Cuando el invitado confirma, esas filas se borran y se reinsertan con los datos reales.

⚠️ **Por eso el RSVP exige nombre Y apellido**, del titular y de cada acompañante.
Confirmar borra la pre-alta y la reemplaza por lo que mandó el invitado; una fila
incompleta no se guarda. Hasta el 06/08/2026, elegir 5 personas y dejar los campos en
blanco borraba 4 cupos en silencio — le pasó a cuatro grupos en el evento de una clienta.
El apellido pasó a ser obligatorio el 10/08/2026: sin él no se pueden armar las mesas ni
entregarle al salón una lista ordenada por apellido, que es la mitad del producto. El
`required` de los inputs no sirve acá: no hay submit de formulario, es un botón con
`onclick`.

⚠️ **Las tarjetas de acompañante se arman con `innerHTML` desde el JS y solo aparecen si
el invitado elige 2 o más personas.** Por eso se les escaparon los colores fijos cuando se
arreglaron los temas oscuros: una auditoría que fotografía la página no las ve, porque no
existen todavía. Sus tres etiquetas estaban en `rgba(0,0,0,0.5)` — **1,11:1 sobre
`zaira15`, o sea invisibles**. Cualquier bloque que se pinte desde JS hay que auditarlo
*después* de hacerlo aparecer.

### `currentConfig` se carga para los DOS roles

`loadConfig()` solo corría en `unlockSuperAdmin()`, así que con la clave de **cliente**
—la que usan los clientes— `currentConfig` quedaba vacío y los mensajes de WhatsApp salían
sin el nombre del evento. Va **primero y con `await`**: en paralelo con `loadData()` no
llega a tiempo y la lista se arma sin él.

### Pestaña "Mensajes y entrega" (solo superadmin)

Tres mensajes de venta listos para copiar o mandar por WhatsApp. **El texto viaja al
navegador**: quien abra el código fuente lo lee, así que ahí no van precios especiales para
un cliente puntual.

Alcance del servicio, decidido el 06/08/2026: **la música es obligatoria** (sección propia en
el mensaje) y **la lista de invitados NO se le pide al cliente** — los links los genera él
desde su panel, a su ritmo.

### Recordatorio a pendientes

Tarjeta en la pestaña Invitados con los que no contestaron, agrupados por `invitado_url`.
Los cupos salen de contar las filas `pendiente` de ese grupo — el `personas` original no
se guarda en ningún lado. Se arma con DOM, **no con `innerHTML`**: los nombres los escribe
el cliente y terminan dentro de una URL y de un mensaje.

### Mesas

- La columna `mesa` existe siempre. **Se eliminó el fallback a `localStorage`**: guardaba la mesa solo en ESE navegador, así que el plano del salón salía distinto según desde dónde se abriera.
- Capacidad dinámica: si se asignan más de 10 a una mesa, la mesa escala.
- Exporta PDF de distribución de salón ordenado por apellido.

## Identidad — una sola marca, dos dorados

Hasta el 06/08/2026 el panel y el logo eran rosa `#ff3b6f` y la web marfil y dorada: se
leían como dos empresas. Todo pasó al dorado de `index.html`.

```
Fondo oscuro     #08080a     (panel)      Títulos: Fraunces 600-700
Fondo claro      #FAF4EA     (landing)    Textos:  Instrument Sans 400-500
Dorado profundo  #A8761F     ← texto sobre fondo CLARO
Dorado claro     #F7CE84     ← texto sobre fondo OSCURO
Tinta            #191410
```

⚠️ **No hay un dorado único.** `#F7CE84` da 12,3:1 sobre el panel oscuro y **1,3:1 sobre
papel blanco**. Por eso el PDF de mesas usa `#8A5F17`, y el botón primario del panel lleva
texto oscuro sobre el dorado claro (el blanco cae a 1,6:1). En el panel las variables se
llaman `--oro/--oro2/--oro3`.

**El panel sigue oscuro a propósito**: es una herramienta de trabajo y las vistas previas de
invitaciones se ven mejor sobre fondo oscuro. Coherencia de marca no es mismo fondo.

**Tres imágenes de marca**, todas generadas renderizando HTML con puppeteer:
`logo.png` (transparente) · `logo-og.png` (1200×630 con fondo oscuro, para vistas previas —
el transparente desaparece sobre el blanco de WhatsApp) · `publicidad/ig-perfil.png`.

## Agendar: Google, no .ics

El botón abre Google Calendar. Se descartó el `.ics` porque se baja como archivo y pide
permiso, y el menú de dos opciones porque colgaba de un botón descentrado y se salía de
pantalla en 364px.

⚠️ **La URL de Google no acepta recordatorios.** Trece parámetros (`text`, `dates`, `ctz`,
`details`, `location`, `crm`, `trp`, `sprop`, `add`, `src`, `recur`, `vcon`, `action`) y
ninguno es de avisos. Verificado, no supuesto.

⚠️ **`fecha_iso` no tiene zona horaria.** Pasársela a `new Date()` hace que cada navegador la
lea en la suya: un invitado en Madrid se agendaba las 17:00 de Buenos Aires. Se parsea a
mano y se declara la zona con `ctz`. Se verifica con `page.emulateTimezone()`.

## CSS / Design

**Variables CSS principales:**
- `--primary` / `--secondary` / `--bg` — sobreescritas desde `config.color_1/2/bg`
- `--secondary` (`#d6ecc0` por defecto) — color de acento, botones, badges

**Fuentes — se elige una DUPLA, no una fuente suelta.** Tres variables: `--font-titulo`,
`--font`, `--font-label`. El objeto `DUPLAS` de `invitacion.html` tiene las 8 combinaciones y sus
claves deben coincidir con el `<select id="gi-fuente">` del admin.

⚠️ Cada dupla declara los pesos **exactos** que publica cada familia. Si se le pide a Google un
peso que la fuente no tiene, falla el pedido entero y no carga ninguna de las dos.

Hasta el 04/08/2026 el selector no hacía nada: bajaba la fuente y todos los `font-family` estaban
escritos a mano.

**Responsive:** Mobile-first. Galería: carousel en mobile, grid en desktop. Countdown: flex en mobile, grid 2×2 o 4 columnas en desktop.

## Flujo de confirmación (RSVP)

1. Invitado abre su link personal
2. Splash con foto → botón "Ingresar"
3. Navega la invitación (música autoplay)
4. Llega al form RSVP:
   - Si ya confirmó (`invitado_url` con `asiste !== 'pendiente'`), muestra mensaje de ya registrado
   - Si no, permite llenar datos propios + datos de acompañantes (nombre, apellido, asistencia individual, dieta, canción)
5. Al confirmar: borra las filas pre-cargadas e inserta todas las filas nuevas (titular + acompañantes)
6. Maneja error de columna `mesa` ausente con retry sin ese campo

## Fotos — especificaciones para generación

Cada evento puede tener hasta 7 fotos. Todas se suben desde el admin (superadmin → Editor de Secciones) y se guardan en Supabase Storage bucket `invitaciones`.

| Campo config | Dónde aparece | Crop visual | Tamaño ideal a generar |
|---|---|---|---|
| `foto_splash` | Pantalla de bienvenida — círculo flotante con borde color | Circular (`border-radius: 50%`) | **600×600 px cuadrada** |
| `foto_hero` | Hero full-screen — fondo con overlay oscuro 40% | Horizontal, `object-fit: cover` | **1920×1080 px** |
| `foto_galeria_1..4` | Carrusel en mobile / Grid en desktop | Cuadrada, `object-fit: cover` | **800×800 px** (hasta 4) |
| `foto_hashtag` | Sección Instagram — segundo círculo | Circular (`border-radius: 50%`) | **400×400 px cuadrada** |

**Tips para generar con IA (Gemini/Midjourney):**
- `foto_splash` y `foto_hashtag`: composición centrada — cara o detalle en el centro (se recortan las esquinas).
- `foto_hero`: asegurar que no sea muy clara/saturada (el overlay 40% negro mejora la legibilidad del texto blanco encima).
- `foto_galeria_*`: pueden ser de ambiente, detalles, o retratos. Se muestran en carrusel en mobile.

## Eventos demo en Supabase

Creados para la landing page (`index.html` → sección "Explorá nuestros diseños").

**15 años** (6 eventos):
| ID | Nombre | Paleta | Música |
|---|---|---|---|
| `valentina15` | Valentina | Dark/Verde acento (original) | — |
| `zaira15` | Zaira | Dark Silver `#0d0d1a / #b8b8cc` | Slow ♪ |
| `martina15` | Martina | Blanco Mármol `#fafaf8 / #c8b89a` | Slow ♪ |
| `luna15` | Luna | Verde Botánica `#f5f8f2 / #7ab87a` | Slow ♪ |
| `sofia15` | Sofía | Rosa Chicle `#fff0f7 / #ff6ba8` | Upbeat ♫ |
| `isabella15` | Isabella | Lila Aesthetic `#f8f5ff / #b8a0d6` | Upbeat ♫ |

`catalina15` **quedó afuera del set**: sus fotos se perdieron y no se regeneraron.
`valentina15` ocupa su lugar en la galería.

**Casamientos** (6 eventos):
| ID | Nombres | Paleta | Música |
|---|---|---|---|
| `boda-ana` | Ana & José | Clásico Dorado `#fffef9 / #c9a96e` | Slow ♪ |
| `boda-elena` | Elena & Pablo | Negro & Dorado `#0d0d0d / #d4af37` | Slow ♪ |
| `boda-maria` | María & Ramiro | Verde Rústico `#f5f5ee / #a0b880` | Slow ♪ |
| `boda-carolina` | Carolina & Martín | Terracotta `#faf6f0 / #d4845a` | Upbeat ♫ |
| `boda-valentina` | Valentina & Nicolás | Blush Pink `#fdf5f7 / #e8b4c0` | Upbeat ♫ |
| `boda-julieta` | Julieta & Tomás | Azul Noche `#080f1a / #7090c0` | Upbeat ♫ |

Todos con `admin_password: admin123`. **Las fotos son reales** y viven en `assets/<id>/`
con los nombres exactos de las claves del config (`foto_hero.jpg`, `foto_splash.jpg`,
`foto_galeria_1..4.jpg`, `foto_hashtag.jpg`), ya recortadas a las medidas del admin.
Para recargar los 12: correr `sql/002_demos.sql`, que es idempotente.

## index.html — estructura de la landing

Rediseñada con estética warm ivory/gold. Fuentes: Cormorant Garamond + Manrope. Variables: `--accent: #B0894C`, `--accent-deep: #856534`, `--rose: #CE9A8E`, fondo `#FBF7F1`.

1. **NAV** — logo izquierda, links + botón "Pedir invitación" + "PANEL"
2. **Hero** — texto izquierda + 3 iPhones flotantes con iframes reales (floatA/B/C animations):
   - Izquierdo: `zaira15` (198×418px, rotate -7°)
   - Central: `boda-ana` (232×486px, mayor z-index)
   - Derecho: `boda-valentina` (198×418px, rotate +7°)
3. **Marquee** — banda oscura con texto animado
4. **Trust Strip** — métricas (+200 eventos, 24–48h entrega, etc.)
5. **Experiencia Premium** — iPhone `martina15` (280×580px) + lista de features
6. **Demos Gallery** — tabs "MIS 15 AÑOS" / "CASAMIENTOS" + grid **3 columnas fijas (194px)** de iPhones con iframes reales:
   - 15 años: zaira15, martina15, luna15, sofia15, isabella15, valentina15
   - Casamientos: boda-ana, boda-elena, boda-maria, boda-carolina, boda-valentina, boda-julieta
7. **Beneficios** — cards con íconos
8. **CTA Final** — botón WhatsApp
9. **Footer**

### iPhone iframe pattern (index.html)

Todos los celulares usan iframes reales en lugar de contenido CSS dibujado:
```html
<!-- Carcasa del teléfono -->
<div style="width:WPX; height:HPX; background:linear-gradient(150deg,#3a342c,#1c1814); border-radius:Rpx; padding:Ppx; border:1.5px solid rgba(255,255,255,0.1);">
  <!-- Pantalla -->
  <div style="width:(W-2P)px; height:(H-2P)px; border-radius:(R-7)px; overflow:hidden; position:relative; background:#000;">
    <!-- Dynamic island -->
    <div style="position:absolute; top:9px; left:50%; transform:translateX(-50%); width:52px; height:15px; background:#000; border-radius:10px; z-index:10;"></div>
    <!-- iframe 2× escalado al 50% -->
    <iframe src="invitacion.html?evento=ID"
            style="width:(W-2P)*2 px; height:(H-2P)*2 px; border:none; position:absolute; top:0; left:0; transform:scale(0.5); transform-origin:top left; pointer-events:none;"
            loading="eager|lazy"></iframe>
  </div>
</div>
```
- `pointer-events:none` en el iframe para que el click pase al `<a>` padre
- Grid de demos: `loading="eager"` en 15años (visible), `loading="lazy"` en bodas (tab oculto)

## Deploy

El sitio está en Vercel con auto-deploy desde GitHub.
- Repo: `https://github.com/Acusosafer/invitacione-digitales`
- Para deployar: `git add`, `git commit`, `git push origin main`
- URL producción: `https://invitacionesdigitalesoficial.com` (dominio propio desde el 07/08/2026,
  Namecheap). El `.vercel.app` sigue activo y redirige, así que los links que ya se mandaron
  a invitados no se rompen.
- ⚠️ **Existe también `invitacionesdigitalesofical.com`** —sin la "i" de "oficial"— comprado
  por error el mismo día. No es el dominio del sitio. Si sirve para algo es como red para
  quien escriba mal la dirección.
- **La URL casi nunca va escrita a mano en el código.** `api/i.js` la toma de
  `x-forwarded-host`, y el generador de links del panel de `location.origin`: los dos se
  adaptan al dominio desde el que se abran. Sólo hay literales en el footer de
  `invitacion.html`, la constante `WEB` de `admin.html` y el mockup de chat de `index.html`.

## Los colores de la invitación siguen al tema (leer antes de tocar el CSS)

El cliente elige `color_1` (tinta), `color_2` (acento) y `color_bg` (papel). **Ningún color
puede estar escrito a mano en `invitacion.html`**, porque lo que sobre blanco es "gris
clarito" sobre `#0d0d1a` es "casi blanco".

Hasta el 10/08/2026 las tres invitaciones oscuras estaban **rotas en producción**: el
mensaje personal salía en negro sobre negro y las secciones Ubicación, Regalos y RSVP eran
bandas casi blancas con texto blanco encima. No era un problema de los demos — cualquier
clienta que eligiera colores oscuros recibía eso.

| Token | Qué significa | Se usa para |
|---|---|---|
| `--black` | **la tinta del evento** (= `--primary`) | textos, íconos, bordes |
| `--white` | **el papel del evento** (= `--bg`) | fondos de bloques invertidos |
| `--ink-soft` | tinta apagada, mezclada con el papel | subtítulos, direcciones |
| `--on-accent` | texto legible **sobre el acento** — lo calcula el JS | botones, chips, countdown, el ecualizador |
| `--velo-1` / `--velo-2` | un velo de tinta sobre el papel | franjas alternas, focos de campos, tarjetas |

**Dos excepciones, a mano y comentadas en el código:**
- **El hero**: atrás hay una foto con velo negro, no el fondo del evento. Texto blanco fijo.
- **El footer**: sus textos internos están escritos como `rgba(255,255,255,x)`, así que el
  bloque tiene que quedar oscuro sí o sí. Si algún día se cambia, hay que cambiar los seis.

**Cómo se verifica:** midiendo el contraste real de cada texto contra el fondo que
efectivamente tiene detrás, en los 12 demos, no a ojo. Ojo con `color-mix()`: se serializa
como `color(srgb 0.72 0.72 0.75)` con valores de 0 a 1, no de 0 a 255 — leerlos mal da 1:1
en todos lados y manda a perseguir fantasmas.

## El número de WhatsApp — dónde vive (leer antes de cambiarlo)

Hoy es `+54 9 11 2457-6536` (`5491124576536` en los links). Fer decidió el
10/08/2026 pasar el negocio a una **línea aparte**, para que su WhatsApp personal
siga siendo personal: un número vive en una sola cuenta, o WhatsApp o Business,
nunca las dos. Las dos apps sí conviven en el mismo teléfono con números distintos.

Cuando cambie, son **nueve lugares en cinco archivos** más **dos que no aparecen
en una búsqueda de texto**:

| Dónde | Qué |
|---|---|
| `index.html` ×4 | nav, hero, precio y cierre |
| `admin.html` ×2 | "pedime mi link" y el pie del login |
| `publicidad/agosto-a.html` | el número escrito en la placa |
| `publicidad/agosto-a-reel.html` | el número escrito en el reel |
| `publicidad/instagram.md` | el botón de contacto del perfil |
| ⚠️ **`publicidad/agosto-a-reel.mp4`** | **el número está en los píxeles.** Hay que regenerarlo: `node publicidad/generar-reel.js` |
| ⚠️ **La placa PNG de agosto** | ídem, hay que volver a exportarla |

⚠️ **Si la línea del negocio es prepaga, se vence sin uso.** El día que caduque,
el número muere y con él los botones de toda la web, el reel, la placa y el link
de la bio de Instagram — todos apuntando a un número que no existe. Conviene una
eSIM sobre el plan que ya paga, o una prepaga con recarga automática.

## Medición (leer antes de agregar cualquier script de terceros)

Instalado el 07/08/2026. Estos tres IDs **no son secretos** —cualquiera los lee en el código
fuente de cualquier web— así que van escritos en el HTML, no en un `.env`. Con ellos se puede
*mandar* datos a las cuentas, no *leerlos*.

| Qué | ID | Dónde vive |
|---|---|---|
| Google Tag Manager | `GTM-T7QNB7VR` | **En el HTML de `index.html`, y solo ahí** |
| Google Analytics 4 | `G-G7LL4G253B` | Dentro de GTM, como etiqueta |
| Píxel de Meta | `2024768681739346` | Dentro de GTM, como HTML personalizado |

**Solo GTM va en el código.** GA4 y el píxel se enchufan adentro de GTM. Si además se pegara
GA4 en el HTML, cada visita se contaría dos veces y todos los números saldrían al doble. Lo
que venga después (otro píxel, un mapa de calor, lo que sea) entra por GTM también.

⚠️ **Nada de esto puede ir en `invitacion.html` ni en `admin.html`.** La URL de la invitación
lleva `?invitado=Nombre+Apellido` y GA4 guarda la URL completa de cada visita: sería mandarle
a Google y a Meta la lista de invitados de los clientes. Aparte de estar mal, los términos de
Google prohíben mandarles datos personales y la sanción es la cuenta borrada con el historial
adentro.

**El boca a boca sí se mide**, pero del lado de la landing: los dos links del footer de la
invitación llevan `?utm_source=invitacion&utm_medium=footer` y se distinguen entre sí con
`utm_content=marca|cta`. El UTM viaja en el link, así que solo deja rastro si la persona hace
clic y llega a la web — el invitado que no hace nada no queda registrado en ningún lado.

`index.html` no tiene ni un `<form>` ni un `<input>` (el contacto es un link a WhatsApp). Por
eso la *coincidencia avanzada automática* del píxel de Meta no tiene nada personal que leer.
Si algún día se le agrega un formulario, **ese es el momento de volver a revisar esa opción**.

## Bugs corregidos (historial)

### Orden de secciones incorrecto (invitacion.html)
- **Causa:** `layout.order` incompleto en Supabase → secciones sin orden quedaban al inicio del DOM
- **Fix en invitacion.html:** Después de reordenar por `layout.order`, appendear las secciones faltantes al final del contenedor
- **Fix en admin.html `guardarTodo()`:** Normalizar `layout.order` antes de guardar — agregar todas las secciones de `SECTIONS` que no estén en el array
- **Fix en Supabase:** SQL UPDATE para forzar el array completo en todos los eventos

### La invitación arrancaba por la mitad (invitacion.html)
- **Causa:** dos cosas sumadas. El navegador **restaura el scroll al recargar**, y como
  el splash es `position:fixed` y tapa la pantalla entera, eso no se ve — la página de
  atrás ya está scrolleada. Y el botón "Ingresar" solo escondía el splash, nunca subía.
- **Fix:** `history.scrollRestoration = 'manual'` en el `<head>` (al final del `<body>`
  se llega tarde: la restauración ocurre al terminar de cargar), y `scrollTo(0,0)` en el
  handler **antes** de esconder el splash, con `scroll-behavior` apagado un instante —
  `<html>` lo tiene en `smooth` y si no, la invitación se ve "rebobinar" durante el fundido.
- Medido a 390px: antes 238px, después 0px. Los links de `/i` quedan cubiertos porque
  `api/i.js` trae `invitacion.html` entera y solo reescribe las etiquetas og.

### Foto hashtag invisible (invitacion.html)
- **Causa:** `src=""` en el `<img>` dispara `onerror` → `display:none` → JS no puede mostrarla después
- **Fix:** Remover el atributo `src=""` del elemento `<img id="txt-hashtag-foto">`

## Errores conocidos / workarounds

- **Autoplay de audio bloqueado:** El botón de la invitación solo intenta `play()` después de interacción del usuario.
- **`filter: darken(5%)`** en `.darken-func` — CSS inválido, no tiene efecto (es una función de SASS/PostCSS, no CSS nativo).
- **Los 12 demos no tienen `musica_url`** — no hay archivos de audio todavía.
- **`boda-julieta` y el resto usan fotos servidas desde Vercel** (`/assets/<id>/`), no Supabase Storage. Las de clientes reales sí van a Storage.
- **Riesgos aceptados a propósito** (no son fugas, son spam): crear un evento nuevo no pide clave — hace falta para dar de alta clientes; y confirmar asistencia es libre para quien sepa el slug, con tope de 20 filas por envío.
