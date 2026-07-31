# Invitaciones Digitales Oficial

## Qué es este proyecto

Sistema de invitaciones digitales personalizadas para eventos (15 años, casamientos, etc.). Cada evento tiene una URL única, configuración almacenada en Supabase, y se comparten links personalizados por WhatsApp a cada invitado.

**Stack:** HTML/CSS/JS vanilla — sin framework, sin bundler, sin build step. Todo se sirve estático.

**Backend:** Supabase — proyecto `ldvosdztnhrvrqxnjuco` ("Lo de Inés"), schema `invitaciones`

## Archivos principales

| Archivo | Función |
|---|---|
| `invitacion.html` | Invitación visible al invitado — carga config desde Supabase según `?evento=` |
| `admin.html` | Panel de control — gestión de invitados, mesas, links, diseño |
| `index.html` | Landing page del servicio |
| `generar-hash-superadmin.html` | Genera el hash SHA-256 de la clave de superadmin |
| `sql/001_schema_invitaciones.sql` | Schema, tablas, funciones y permisos |
| `sql/002_demos.sql` | Los 12 eventos demo de la landing |
| `generate_logo.py` + `temp_logo.html` | Generación del logo |

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

## Admin

Acceso: `admin.html?evento=valentina15`

- **Clave cliente** — En `eventos.admin_password` (default `admin123`). Da acceso a: Resumen, Invitados, Links, Mesas, Vista Previa.
- **Clave superadmin** — Su hash SHA-256 está en `invitaciones.ajustes`. Desbloquea además: Editor de Secciones, Diseño Global, Historial. Para cambiarla: `generar-hash-superadmin.html` + `update` sobre esa tabla.

Ambas se verifican con `verificar_clave()` en Postgres. La clave queda en memoria
(`adminClave`) y se re-valida en **cada** operación: no alcanza con haber entrado una vez.

### Link generator

Al generar un link, el admin **pre-inserta filas en `confirmaciones`** con `asiste: 'pendiente'` para el titular y cada acompañante. Cuando el invitado confirma, esas filas se borran y se reinsertan con los datos reales.

### Mesas

- La columna `mesa` existe siempre. **Se eliminó el fallback a `localStorage`**: guardaba la mesa solo en ESE navegador, así que el plano del salón salía distinto según desde dónde se abriera.
- Capacidad dinámica: si se asignan más de 10 a una mesa, la mesa escala.
- Exporta PDF de distribución de salón ordenado por apellido.

## CSS / Design

**Variables CSS principales:**
- `--primary` / `--secondary` / `--bg` — sobreescritas desde `config.color_1/2/bg`
- `--secondary` (`#d6ecc0` por defecto) — color de acento, botones, badges

**Fuentes:** Cormorant Garamond (títulos serif), Jost (cuerpo), Montserrat (labels). La fuente principal se puede cambiar desde el admin (genera un `<link>` dinámico a Google Fonts).

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
- URL producción: `https://invitacionesdigitalesoficial.vercel.app`

## Bugs corregidos (historial)

### Orden de secciones incorrecto (invitacion.html)
- **Causa:** `layout.order` incompleto en Supabase → secciones sin orden quedaban al inicio del DOM
- **Fix en invitacion.html:** Después de reordenar por `layout.order`, appendear las secciones faltantes al final del contenedor
- **Fix en admin.html `guardarTodo()`:** Normalizar `layout.order` antes de guardar — agregar todas las secciones de `SECTIONS` que no estén en el array
- **Fix en Supabase:** SQL UPDATE para forzar el array completo en todos los eventos

### Foto hashtag invisible (invitacion.html)
- **Causa:** `src=""` en el `<img>` dispara `onerror` → `display:none` → JS no puede mostrarla después
- **Fix:** Remover el atributo `src=""` del elemento `<img id="txt-hashtag-foto">`

## Errores conocidos / workarounds

- **Autoplay de audio bloqueado:** El botón de la invitación solo intenta `play()` después de interacción del usuario.
- **`filter: darken(5%)`** en `.darken-func` — CSS inválido, no tiene efecto (es una función de SASS/PostCSS, no CSS nativo).
- **Los 12 demos no tienen `musica_url`** — no hay archivos de audio todavía.
- **`boda-julieta` y el resto usan fotos servidas desde Vercel** (`/assets/<id>/`), no Supabase Storage. Las de clientes reales sí van a Storage.
- **Riesgos aceptados a propósito** (no son fugas, son spam): crear un evento nuevo no pide clave — hace falta para dar de alta clientes; y confirmar asistencia es libre para quien sepa el slug, con tope de 20 filas por envío.
