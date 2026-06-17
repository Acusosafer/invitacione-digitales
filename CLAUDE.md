# Invitaciones Digitales Oficial

## Qué es este proyecto

Sistema de invitaciones digitales personalizadas para eventos (15 años, casamientos, etc.). Cada evento tiene una URL única, configuración almacenada en Supabase, y se comparten links personalizados por WhatsApp a cada invitado.

**Stack:** HTML/CSS/JS vanilla — sin framework, sin bundler, sin build step. Todo se sirve estático.

**Backend:** Supabase (proyecto `fybwovlewphtdmjmwyjn`)

## Archivos principales

| Archivo | Función |
|---|---|
| `invitacion.html` | Invitación visible al invitado — carga config desde Supabase según `?evento=` |
| `admin.html` | Panel de control principal — gestión de invitados, mesas, links, diseño |
| `index.html` | Landing page del servicio |
| `preview.html` | Vista previa embebida |
| `mesas.html` | Prototipo estático (datos hardcodeados, sin Supabase — no es el activo) |
| `admin_v3.html` | Versión anterior del admin — referencia/legacy |
| `invitacion_v2.html` | Versión anterior de la invitación — legacy |
| `generate_logo.py` | Script Python para generar el logo |

## Supabase

```
URL:  https://fybwovlewphtdmjmwyjn.supabase.co
KEY:  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (anon key, está en los scripts)
```

### Tablas

**`eventos`**
- `id` — slug del evento (ej: `valentina15`)
- `config` — JSONB con toda la configuración (ver abajo)
- `admin_password` — clave del cliente

**`confirmaciones`**
- `id`, `evento_id`, `invitado_url` (nombre del param URL)
- `nombre`, `apellido`
- `asiste` — `'si'` | `'no'` | `'pendiente'`
- `personas` — siempre 1 (cada acompañante es una fila separada)
- `dieta`, `mensaje` (canción sugerida), `mesa`
- `created_at`

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

- **Clave cliente** — Definida en `eventos.admin_password` (default `admin123`). Da acceso a: Resumen, Invitados, Links, Mesas, Vista Previa.
- **Clave superadmin** — Hardcodeada como `"superadmin"`. Desbloquea además: Editor de Secciones, Diseño Global, Historial.

### Link generator

Al generar un link, el admin **pre-inserta filas en `confirmaciones`** con `asiste: 'pendiente'` para el titular y cada acompañante. Cuando el invitado confirma, esas filas se borran y se reinsertan con los datos reales.

### Mesas

- La columna `mesa` en `confirmaciones` puede no existir en Supabase (se creó después). El código tiene fallback a `localStorage` (`mesa_fallback_{eventoId}`).
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
| `catalina15` | Catalina | Dorado Glam `#0d0d06 / #d4af37` | Upbeat ♫ |

**Casamientos** (6 eventos):
| ID | Nombres | Paleta | Música |
|---|---|---|---|
| `boda-ana` | Ana & José | Clásico Dorado `#fffef9 / #c9a96e` | Slow ♪ |
| `boda-elena` | Elena & Pablo | Negro & Dorado `#0d0d0d / #d4af37` | Slow ♪ |
| `boda-maria` | María & Ramiro | Verde Rústico `#f5f5ee / #a0b880` | Slow ♪ |
| `boda-carolina` | Carolina & Martín | Terracotta `#faf6f0 / #d4845a` | Upbeat ♫ |
| `boda-valentina` | Valentina & Nicolás | Blush Pink `#fdf5f7 / #e8b4c0` | Upbeat ♫ |
| `boda-julieta` | Julieta & Tomás | Azul Noche `#080f1a / #7090c0` | Upbeat ♫ |

Todos con `admin_password: admin123`. Las fotos son placeholders de picsum — reemplazar desde el admin con fotos reales generadas por IA o del cliente.

## index.html — estructura de la landing

1. **Hero** — venue 3D SVG con pantalla LED (3 paneles CSS perspective) + siluetas de pareja
2. **Demos Gallery** — toggle 15 AÑOS / CASAMIENTOS + grid 3×2 de iPhones con iframes de invitaciones reales
3. **Demo Section** — iPhone con `valentina15` + lista de features del servicio
4. **Álbum QR section** — descripción del álbum compartido
5. **Preview Cards** — 6 features (countdown, ubicación, música, etc.)
6. **CTA final** — botón WhatsApp

## Errores conocidos / workarounds

- **Columna `mesa` ausente:** El código en `invitacion.html` y `admin.html` detecta error `42703` o `PGRST204` y reintenta sin el campo `mesa`, o usa localStorage como fallback.
- **Autoplay de audio bloqueado:** El botón de la invitación solo intenta `play()` después de interacción del usuario.
- **`filter: darken(5%)`** en `.darken-func` — CSS inválido, no tiene efecto (es una función de SASS/PostCSS, no CSS nativo).
- **Supabase free tier pausa** tras 1 semana sin actividad — usar MCP `restore_project(fybwovlewphtdmjmwyjn)` para reactivar.
