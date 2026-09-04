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
| `servicio-a-medida.html` | La página del servicio premium — ruta `/a-medida` |
| `api/i.js` | **Vista previa de WhatsApp.** Los links se comparten como `/i?evento=...` |
| `vercel.json` | Rewrite `/i` → `/api/i` |
| `.vercelignore` | Qué NO se publica: `.md`, `sql/`, `publicidad/`, herramientas internas |
| `generar-hash-superadmin.html` | Genera el hash SHA-256 de la clave de superadmin (no se deploya) |
| `sql/001_schema_invitaciones.sql` | Schema, tablas, funciones y permisos |
| `sql/002_demos.sql` | Los 12 eventos demo de la landing |
| `sql/003_storage.sql` | Bucket de Storage y sus permisos |
| `sql/005_telefono_links.sql` | La tabla `links` y el teléfono del generador |
| `sql/006_deseos.sql` | El libro de deseos: tabla, funciones y permisos |
| `sql/007_invitado_a_mano.sql` | Cargar invitados sin link (la familia, la agasajada) |
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

**`links`** — `evento_id` + `invitado_url` (PK), `telefono`, `cupos`, `created_at`,
`updated_at`. Un renglón por link generado. **Sin un solo grant para `anon`.**

**`deseos`** — `id`, `evento_id` (FK), `nombre`, `deseo`, `mesa`, `created_at`. El buzón del
libro de deseos. **Sin un solo grant para `anon`**: se escribe por función y leer exige clave.

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
| `admin_links(evento, clave)` | Los links con su teléfono y sus cupos |
| `admin_link_telefono(evento, clave, invitado, tel)` | Cargar o corregir el número de un link |
| `deseo_enviar(evento, nombre, deseo, mesa)` | **La única pública del libro.** Escribe y devuelve un número, nunca filas |
| `admin_deseos(evento, clave)` | Los mensajes del libro, para el panel |
| `admin_borrar_deseo(evento, clave, id)` | Borrar un mensaje |
| `admin_agregar_invitado(evento, clave, nombre, apellido, asiste, mesa)` | Alta a mano, para quien no recibe link |

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

### Los grupos: cada persona contesta por su cuenta

**Un link cubre a todo un grupo** (`invitado_url` es el mismo para los N cupos). Dos reglas
que salieron de dos bugs reales, los dos arreglados el 10/08/2026:

**1 · El titular que dice "No puedo ir" NO decide por el resto.** Las tarjetas de
acompañante siguen a la vista aunque él no vaya, y cada una trae su propio sí o no. Lo
único que se esconde es la dieta del titular. Antes se escondía todo el bloque y
`confirmar()` armaba las filas de acompañantes solo `if (asiste === 'si')`: de 4 cupos se
guardaba **1**, y los otros 3 no quedaban ni en `no` ni en `pendiente` — desaparecían,
porque `rsvp_enviar` ya había borrado la pre-alta. La cuenta del panel daba mal y no había
forma de notarlo.

**2 · Un link no se llama "Familia Ferreyra".** El prellenado parte el nombre en dos
—primera palabra al nombre, el resto al apellido— así que quedaba `nombre="Familia"`,
`apellido="Ferreyra"`: **los dos campos llenos, o sea que la validación lo aceptaba**, y a
la mesa iba a sentarse alguien llamado "Familia Ferreyra". Hoy, si la primera palabra es
`familia`, `familias`, `flia` o `fam` (con o sin punto), los campos quedan **vacíos** y los
escribe quien confirma. Igual, **la forma correcta de nombrar el link es con el nombre real
de una persona del grupo**: así ella lo recibe ya cargado.

⚠️ **`personas` (los cupos asignados) no se guarda en ningún lado.** Se deduce contando
filas `pendiente`. Por eso, cuando una confirmación sale mal, **no hay contra qué comparar
para detectarlo**. Si algún día se agrega la columna, esto se vuelve auditable.

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

### `mensaje` es la canción, y nada más

La columna `mensaje` de `confirmaciones` guarda **la canción sugerida**. Pero se usó también
como marca interna: la pre-alta escribe `Invitación pre-cargada`, y hasta el 10/08/2026 un
acompañante que no pedía tema quedaba con **`Acompañante de Fulano`** guardado ahí. En el
panel de una clienta con la fiesta en curso, la columna Canción mezclaba temas con
acompañantes.

El fallback ya no se escribe, pero **los eventos en curso lo tienen adentro**. Por eso el
filtro `cancionReal()` de `admin.html` es **de lectura**: limpia la vista sin tocar una sola
fila de la base de un cliente en plena fiesta. Se usa en las dos tablas, en el CSV y en la
lista del DJ — si aparece un lugar nuevo donde se muestre `mensaje`, va con el filtro.
Solo descarta el prefijo exacto `Acompañante de `: una canción que empiece con
"Acompañado por…" se conserva.

### Lista para el DJ

Tarjeta en la pestaña Invitados. Agrupa **por canción y no por persona**: si tres invitados
piden el mismo tema, el DJ lo ve una vez con el número al lado, y ordenado por cantidad de
pedidos. Sale como texto para pegar en WhatsApp o como PDF para imprimir.

Se arma con DOM, no con `innerHTML`. El texto lo escribe el invitado y antes entraba **como
HTML** en el panel del cliente (`tdCancion.innerHTML = \`🎵 ${inv.mensaje}\``).

### El hero recorta por ejes distintos según la pantalla

Los clientes suben **fotos verticales**, sacadas con el celular. El hero es a pantalla
completa, así que:

```
celular 390×844  →  se ve el 100% del alto y el  69% del ancho   (recorta a lo ANCHO)
PC 1920×1080     →  se ve el  38% del alto y el 100% del ancho   (recorta a lo ALTO)
```

El encuadre guardado es **uno solo** y el admin lo elige sobre un marco 9/16, o sea
pensando en el celular. En la PC ese "50% vertical" cae en la banda del medio de la foto:
**el torso, con la cara afuera**. Le pasaba a cualquier cliente con foto vertical.

Hoy, cuando el recorte es vertical, el punto de mira sube solo al 25%. Se recalcula al
girar el teléfono o agrandar la ventana. ⚠️ Si la foto tiene la cabeza pegada al borde de
arriba, ningún valor la salva: hay que pedirle al cliente una foto con más aire.

### `/muestra` — el link que se le manda a quien todavía no es cliente

`invitacionesdigitalesoficial.com/muestra` abre la invitación de `almamia15` con
`?muestra=1`: se ve y se recorre entera, se puede completar el RSVP, y **no guarda nada**.
Avisa dos veces que es una muestra — que alguien crea que confirmó de verdad en la fiesta
de otra persona sería peor que cualquier venta.

**Por qué es una ruta limpia y no `?evento=…&muestra=1`:** una URL con `?` y `&` es frágil
fuera de la web. **Instagram no la convierte en link tocable** — le llegó así a una
prospecta el 15/08 y desde el celular no podía hacer nada con ella. `/muestra` se convierte
en link en cualquier app y además se puede dictar por teléfono.

⚠️ **Una ruta limpia deja `location.search` VACÍO en el navegador.** El rewrite de Vercel
le pasa la query a `api/i.js`, pero la barra de direcciones sigue diciendo `/muestra`. La
primera versión mostraba la vista previa de Alma y después **abría la invitación de
`valentina15` —el evento por defecto— con el RSVP vivo, escribiendo filas de verdad.**
Hoy `api/i.js` deja la query en `window.__QS_SERVIDOR` y `invitacion.html` la usa cuando
`location.search` está vacío. **Cualquier ruta limpia nueva necesita eso.**

⚠️ El evento está escrito en `vercel.json`. Si algún día `almamia15` deja de ser el que
conviene mostrar, se cambia ahí. **`vercel.json` es JSON puro: no acepta comentarios ni
strings sueltos dentro de `rewrites`** — Vercel valida el esquema y el deploy falla.

### Qué se puede saber de un link, y qué no

**No se puede saber a qué número se mandó un link, ni reconstruirlo hacia atrás.** El panel
arma un `wa.me` que abre WhatsApp y ahí el contacto lo elige la persona a mano: esa
elección ocurre dentro de WhatsApp y la web nunca se entera. Tampoco se puede saber si el
link se reenvió a un tercero (es el mismo para todo el grupo) ni si lo leyeron sin abrirlo.

**Sí se sabe quién**, porque el nombre viaja en la URL (`?invitado=Susana+Ferreyra`).

Queda pendiente **registrar la apertura del link** (fecha y cuántas veces). Es la señal
que más ahorra trabajo: *"abrió tres veces y no confirmó"* pide otra insistencia que
*"nunca abrió"*. No agrega ningún dato personal nuevo, y la tabla `links` ya es el lugar.

### El teléfono del link (27/08/2026)

Campo **opcional** al lado de nombre y cupos. Si se carga, **"Recordar" abre el chat de esa
persona**: un toque y el mensaje está escrito. Antes armaba un `wa.me/?text=` sin número,
así que WhatsApp abría el selector de contactos y había que buscar a la persona a mano.

Vive en su propia tabla `invitaciones.links` (clave `evento_id + invitado_url`), **no** en
`confirmaciones`: esa se borra y se reinserta en cada RSVP, y el número se perdería al
confirmar. De paso guarda `cupos`, que hasta hoy no se guardaba en ningún lado.

⚠️ Son datos personales de invitados de un cliente. `links` no tiene **ningún** grant para
`anon`: se lee solo por `admin_links()` / se escribe por `admin_prealta()` y
`admin_link_telefono()`, las tres `security definer` con clave. Nunca viaja a la invitación.

⚠️ **Un número mal normalizado no es un detalle de formato**: `wa.me/<n>` abre el chat de
quien sea que tenga ese número. Por eso `normalizarTel()` no adivina — normaliza lo seguro
(el 0, el 15, el +54, el 9) y **rechaza** lo que no da 10 dígitos, en vez de guardarlo a
medias. Con **`+` adelante** se respeta el país tal cual, que es lo que la hace servir para
una clienta de Colombia. Y el número normalizado **se muestra en pantalla** antes de mandar.

⚠️ **Al generar un link se limpian nombre y teléfono.** Si el número quedara puesto, el link
del invitado siguiente se guardaría con el WhatsApp del anterior — y el recordatorio saldría
al chat equivocado con el link equivocado adentro.

⚠️ `admin_prealta` pasó de 4 a 5 parámetros, así que **hubo que borrarla y recrearla**
(`create or replace` con otra firma crea una sobrecarga y PostgREST no sabe cuál llamar), y
el drop se lleva puesto el grant. Mientras la migración `sql/005` no esté corrida, el panel
pide 5 parámetros a una función de 4 y da 404: por eso **`generarLink()` reintenta sin el
teléfono**. El generador de links —lo que más se usa del panel— nunca deja de funcionar.

### La mesa 0 es la Mesa Principal

Los padres, los hermanos y la agasajada se sientan en la mesa principal. Se resolvió
usando **el número 0**, no una mesa con nombre: `parseInt("0")` es un número, así que
funciona con todo el código que ya existía. Se descartó renombrar la Mesa 1 porque una
clienta ya la tenía armada con gente adentro.

⚠️⚠️ **El 0 es "falso" en JavaScript.** `inv.mesa ? inv.mesa : ''` funciona con `"5"` y
falla con `0` — y el panel, al guardar, convierte la mesa a **número**. O sea que hasta
recargar la página, la mesa principal **desaparecía del listado del salón**, del contador
de asignados y del croquis. Eran cinco lugares. Por eso existen `tieneMesa(inv)`,
`nroMesa(inv)` y `nombreMesa(n)`: **son la única forma correcta de preguntar por la mesa**,
y cualquier lugar nuevo que lea `mesa` tiene que usarlas.

La Mesa Principal **se dibuja solo si hay alguien sentado en ella** —un evento que no la
usa no ve una mesa vacía de más— pero **se ofrece siempre** en los desplegables, que es la
única forma de estrenarla. En ella entra cualquiera: los cargados a mano y también alguien
que llegó por su link.

⚠️ `mesasConfig.length` dejó de ser el número de la última mesa en cuanto existe la 0. El
tope sale del número más alto de verdad (`reduce(max)`), o "+ Agregar Mesa" pisa una que ya
existe.

### Cargar un invitado a mano (`admin_agregar_invitado`)

Hay gente que va a la fiesta y **nunca recibe un link**. Sin esto no figuraba en ningún
lado: el contador mentía y **el listado del salón salía incompleto** — y el salón cobra por
cubierto.

⚠️ No se podía reusar `admin_prealta`: mete el nombre entero en `nombre` y deja `apellido`
vacío, y el listado del salón **se ordena por apellido**. Por eso el apellido es obligatorio
también acá.

⚠️ Estas filas van con `invitado_url = 'Cargado a mano'`, y la tarjeta de "Todavía no
respondieron" **las saltea**: agrupa por `invitado_url` y arma un `wa.me` con ese texto
adentro de la URL, así que saldría un link roto a nombre del cliente.

⚠️ El botón se bloquea **antes** de la llamada: dos toques seguidos cargaban a la misma
persona dos veces, y el salón sirve dos cubiertos.

⚠️ **La tarjeta va plegada** (`<details>` nativo, sin JavaScript). Esto se usa tres veces
por evento y desplegada medía **508px en un celular de 844**: tapaba la tabla entera. Cerrada
mide 54px. La pista del título se esconde abajo de 860px — no entra al lado y cae a un
segundo renglón, dejando el chevron descolgado. Después de cargar a alguien **queda abierta**:
los papás, los hermanos y la agasajada se cargan de a varios seguidos.

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

## `/a-medida` — la página del servicio premium

`servicio-a-medida.html`, ruta corta en `vercel.json`. Salió de un diseño hecho en
Claude Design, que vino en **formato propio** (`<x-dc>`, `sc-for`, `{{ }}`, `support.js`)
y con **otra identidad** — Cormorant Garamond + Jost sobre fondo oscuro. Se tradujo a
HTML plano y a los tokens de `index.html`. ⚠️ **Nada de Claude Design se publica tal
cual**: ese formato necesita su runtime, y acá no hay build.

**Tres decisiones comerciales que están escritas en la página y conviene no aflojar:**

- **"Desde $150.000", no un número cerrado.** Un precio fijo pone el mismo techo para
  una familia y para un salón. El "desde" mantiene el ancla —que fue lo que destrabó
  las consultas cuando el precio salió a la vista— sin atarse.
- **Las secciones que no existen son un extra pago** ("Una sección que no existe",
  $30.000). El diseño original prometía cronograma y hoteles como si fueran un ajuste;
  son **código nuevo, campos de admin y un cambio de esquema, por evento**.
- **"La rehago sin costo" tiene límite: una vez.** Sin tope, un cliente difícil se
  come el margen entero.

⚠️ **Los extras van ARRIBA de los pilares, y es a propósito.** Base $50.000 + monograma
+ save the date llega casi al mismo ticket que una a medida **con una fracción del
trabajo y sin cuello de botella**. El a medida existe, es caro, y se hace poco: el
diseño exclusivo no escala, la plantilla sí.

**SEO:** `lang="es-AR"`, canonical a `/a-medida` (se sirve en dos direcciones y sin eso
Google reparte la fuerza entre las dos), Open Graph reusando `og-home.png`, y datos
estructurados de `Service` con el precio. **La landing la enlaza desde la sección de
precio** — una página sin links entrantes no posiciona. GTM sí va acá: la URL no lleva
ningún dato personal, a diferencia de `invitacion.html`.

## Boda Guillermina — la primera venta a medida (18/08/2026)

Guillermina (dermatóloga, 4 consultorios) y **Sebastián Scala**. Finca La
Josefina, Berisso. **3 de abril de 2027**, ceremonia 18:00, fiesta 20:00.
**Ceremonia y fiesta en el mismo lugar.** Save the date en octubre.

**Cerrada en $150.000 con el save the date incluido** — "es el mismo
diseño, no tiene sentido cobrártelo dos veces". Fue el primer trabajo del
servicio `/a-medida`, y **lo pidió ella**: mandó una web de casamiento de
`andina.graphic.design` preguntando si se podía hacer algo así.

⚠️ **Todo vive en `Boda Guillermina/`, que está en `.vercelignore`.** Son
fotos de una clienta y del salón que contrató: no se publica nunca.

### Cómo se hacen las ilustraciones

`prompts-ilustraciones.md` tiene 13 prompts, **uno por ilustración**. Los
trece comparten el **mismo primer párrafo** —paleta con hexadecimales,
técnica de acuarela, fondo blanco— y solo cambia el sujeto. Ese párrafo
repetido es lo único que hace que el set parezca del mismo pincel.

⚠️ **Nunca pedir varias en la misma imagen**: salen chicas, con estilos
distintos entre sí, y no se pueden separar después.

**Vienen sobre papel crema, no transparente.** Sueltas dejan un
rectángulo. Se resuelve con `mix-blend-mode: multiply`, que funde el papel
con el fondo. ⚠️ **Sobre fondo oscuro multiply las borra** — ahí va
`screen`.

⚠️⚠️ **Un `z-index` en cualquier ancestro rompe el multiply.** Un elemento
posicionado con `z-index` abre un *stacking context*, y desde ahí el
`mix-blend-mode` del hijo se mezcla contra el fondo de ESE contexto —que
es transparente— en vez de contra el papel. La acuarela vuelve a quedar
recortada en un rectángulo blanco, igual que si no tuviera multiply. Pasó
en `save-the-date.html` (`.tarjeta{z-index:1}`) y en la plantilla
(`.carilla > *{z-index:3}`), y **se ve idéntico a "me olvidé el multiply",
así que se persigue el fantasma equivocado**. Si las capas de papel son
`position:fixed/absolute` con z-index, el contenido no necesita z-index
propio: queda en el flujo y el papel le pasa por encima igual.

**Y también vienen con mucho margen de papel.** En una grilla los motivos
se ven diminutos dentro de un rectángulo casi vacío. Se recortan al
contenido comparando cada píxel contra el color de la esquina
(`ImageChops.difference` + `getbbox()`), con ~14px de respiro.

**Y pesan.** Las once primeras sumaban 8 MB. Redimensionadas a 900px los
motivos y 1400px las escenas, JPEG 82 progresivo, y después recortadas al
motivo: **768 KB las doce**. Van a `Boda Guillermina/web/`. ⚠️ Ese número
está escrito en la plantilla que ve la clienta: si se agregan o se sacan
ilustraciones hay que volver a medirlo, no estimarlo.

### Los dibujos que se dibujan solos — el diferencial

Un dibujo de línea es un **trazo**, y un trazo se puede animar: se mide con
`getTotalLength()` y se pinta desde cero con `stroke-dashoffset`. La línea
aparece como si una mano la dibujara, en vivo, cuando el invitado llega.
No es un video: son kilobytes de SVG y se ve nítido en cualquier pantalla.

**Andina publica sus dibujos como video en Instagram; esto pasa adentro de
la invitación.** Su web es Wix — no lo puede hacer. Ese es el partido.

⚠️⚠️ **"El primer trazo no se dibuja" volvió TRES veces, y cada vez la
causa fue otra.** El síntoma siempre es el mismo —el círculo de la naranja
aparece entero y de golpe, la hojita sí se dibuja— así que es fácil dar
por arreglado lo que no era. Las tres causas, todas reales:

1. **Dos funciones para arrancar** (el scroll y el botón) y solo una hacía
   el trabajo completo. → **Una sola función**, siempre.
2. **`void document.body.offsetWidth` no alcanza.** Leer `offsetWidth`
   fuerza el *layout*, y `stroke-dashoffset` es una propiedad de *pintado*:
   el navegador puede saltearse el recálculo. → Leer
   `getComputedStyle(t).strokeDashoffset` de **cada** trazo, y arrancar
   dentro de un **doble `requestAnimationFrame`**.
3. **`transition-property` vale `all` por defecto.** El
   `transitionDuration` inline que puso el ciclo anterior **no se va al
   sacar la clase**, así que el *reset* a "escondido" también transicionaba
   —en 1,15s y desde cero—: el trazo nunca llegaba a estar vacío. → En la
   función que prepara, `t.style.transition = 'none'` **explícito**, y
   `t.style.transition = ''` recién al arrancar.

⚠️ Esto **solo se ve midiendo**, no mirando: hay que registrar el
`strokeDashoffset` computado cada ~90ms. En una captura de pantalla, un
trazo que salta y uno que se dibuja rápido se ven igual. Con la causa 3
activa, el círculo marcaba **0 desde el milisegundo cero**.

Y no todo tiene que dibujarse: los hielos **caen** adentro del vaso y las
velas **se encienden**. Cada elemento puede tener su comportamiento — pero
**uno en movimiento por pantalla como máximo**, o parece una tarjeta de
cumpleaños.

### El papel es de algodón, no un color plano

Dos capas fijas con `multiply`: la **fibra** (grano fino, el poro del
algodón) y la **nube** (manchas grandes, la irregularidad de una hoja
prensada en frío). Con multiply oscurecen las fibras; con opacidad sobre
blanco solo agrisan la página. Son dos SVG embebidos, no baja ninguna
imagen.

### Tres actos, no una lista de secciones

1. **Emoción** — ellos de espaldas frente al lago. **Todavía no dice dónde
   es.** Se vende el sueño; el dato se descubre bajando.
2. **El momento** — el mensaje íntimo, la ceremonia, el mapa.
3. **La fiesta** — el brindis, los regalos, las fotos, confirmar.

El hilo es **viajar**: ella siempre buscando un destino nuevo, él
descubriendo el mundo al lado de ella, y la boda como el próximo destino.

⚠️ **Se descartó una transición amanecer→noche** que se había construido
entera. Era una idea mía y la clienta no la pidió. **Primero lo que le
gusta a ella, después lo que se me ocurre a mí.**

### ⚠️ Un degradado largo desacopla el fondo del contenido

Un solo degradado para toda la página se ve lindo pero deja bloques
pintados para fondo claro apoyados sobre fondo oscuro, y el texto
desaparece — el mismo error que dejó rotas las invitaciones oscuras en
producción. **Cada sección trae su propio suelo**, y si hay transición
pasa en una **banda sin contenido**. Y dos secciones con el mismo
degradado seguidas lo **reinician**: la segunda va lisa.

### El mapa

Acuarela en **planta pura** (el primer intento pedía vista "en ángulo" y
salía todo encimado) con los carteles y el recorrido animados encima en
SVG. ⚠️ **Lo que no puede faltar es el pico**: la ceremonia es sobre una
lengua de tierra metida en el lago, con agua por tres lados. Un lago
ovalado con el altar al costado es cualquier lago del mundo.

## `deseos.html` — el libro de deseos

Lo que ve el invitado cuando apoya el celular en el tag NFC de la mesa, o escanea el QR
del cartelito. Ruta corta **`/deseos?evento=X&mesa=7`**.

Hereda el tema del evento igual que la invitación: paleta, dupla tipográfica y foto. Si el
invitado toca el tag y aterriza en algo que parece otra web, duda y se va.

### Es un BUZÓN PRIVADO, no un muro (decidido el 27/08/2026)

Fer eligió que **los deseos no se muestren a los demás invitados**: van derecho al panel de
la clienta. Es lo más cuidadoso con datos de terceros y saca de raíz el riesgo del mensaje
fuera de lugar proyectado en el salón.

⚠️ **Eso saca el empuje de ver que otros ya escribieron**, que era lo que hacía participar.
Se compensa con el **contador**: *"sos el deseo 34º de la noche"*. Da la sensación de fiesta
entera participando **sin revelar un solo nombre**. Y el privado juega a favor: quien
escribe sabe que solo lo lee ella, y se anima a escribir en serio — la pantalla lo dice.

**El invitado escribe y nada más: no puede leer ni el suyo.** `deseo_enviar` devuelve **un
entero, nunca filas**. Si devolviera la lista, cualquiera con el slug del evento leería los
mensajes de todos los invitados de una clienta.

### La portada, y todo en una pantalla (04/09/2026)

La foto ocupa **el ancho entero** arriba de todo y se disuelve hacia abajo en el papel del
evento. Antes era un redondelito de 86px que no cumplía ninguna función; reconocer la cara de
la agasajada es lo que confirma, en medio segundo, que el que escaneó el QR está en el lugar
correcto.

**La pregunta vive adentro de la portada**, no en un bloque aparte que repite el nombre: son
~90px menos, que es exactamente lo que hace que **todo lo que hay que hacer entre en una
pantalla de celular sin scrollear**. Verificado en 390×844, 375×667 y 360×740, en tema claro,
oscuro y en el lila de Enredados: el botón de enviar siempre queda arriba del pliegue.

⚠️⚠️ **El texto NO se apoya sobre la foto.** Abajo del título sube una pared de papel
(`.marca::before`) que llega a opaca **4px antes** de la primera letra. Es la única garantía
posible: la foto la elige el cliente —puede ser un cielo blanco o una noche negra— y la misma
pantalla tiene que servir con papel blanco y con papel casi negro. No existe una opacidad que
funcione en los cuatro casos.

⚠️ **La pared va en px, no en %.** En porcentaje se corre según cuántos renglones ocupe la
pregunta, y *"¿Qué les deseás a Carolina & Martín?"* ocupa uno más que *"¿Qué le deseás a
Alma?"*.

⚠️ **La portada queda FUERA de los dos pasos**, así que la carta se va volando y la foto se
queda. Por eso `mostrar()` y `cerrado()` tienen que **esconder la pregunta**: si no, el libro
cerrado pregunta "¿qué le deseás?" y abajo avisa que no se puede contestar, y la pantalla de
"quedó guardado" vuelve a preguntar algo que la persona acaba de contestar.

⚠️ **Medir el contraste acá exige apagar las transiciones.** Los chips animan el color en
200ms: una captura sacada al instante los agarra todavía grises y da **3:1 en un chip que en
realidad se lee a 5,2:1**. Y se mide el rectángulo de las **letras** (un `Range` sobre el nodo
de texto), no el del elemento: en una píldora, el borde y las esquinas redondeadas caen adentro
de la caja y dan otro fantasma igual de convincente.

### El alias, después de enviar

Muchos invitados recibieron la invitación **meses antes** y para la noche de la fiesta ya no la
tienen a mano. El alias aparece en la pantalla de confirmación, con un botón para copiarlo.

**Va después de enviar el deseo, nunca antes.** Recién escribió algo cariñoso, está con el
celular en la mano y adentro de la fiesta: ese es el momento en que el alias sirve. Arriba,
compitiendo con el campo de texto, sería un cartel de cobro y le sacaría lugar a lo único que
hay que hacer en esa pantalla.

⚠️ **Con `modo_regalo: 'sobres'` no aparece**: en esa fiesta no hay nada que transferir y
mandaría a la gente a buscar un alias que no existe. Tampoco si el evento no tiene alias
cargado, ni en la pantalla de libro cerrado —una fiesta pausada o inexistente no tiene que
mandar a nadie a transferirle plata a nadie—.

### Decisiones que conviene sostener

- **Es una pregunta, no una caja vacía.** A "dejá tu mensaje" la gente le escribe
  "felicidades!!"; a "¿Qué le deseás a Alma?" le contesta.
- **Tres disparadores** ("Un recuerdo", "Un consejo", "Una promesa") que arrancan la frase.
  *"No sé qué poner"* es la razón número uno por la que alguien abre esto y lo cierra.
  ⚠️ **Un disparador reemplaza la frase del anterior, pero nunca lo que escribió la
  persona.** Hay que guardar cuál fue la última frase puesta: sin eso no se puede
  distinguir "lo que escribió" de "lo que pusimos nosotros", y tocar un segundo chip no
  cambiaba nada — encima quedaba marcado un chip que no correspondía al texto.
  ⚠️ **En cuanto escribe algo suyo, los chips se van** (y vuelven si borra todo): ya
  cumplieron, y con el teclado abierto el espacio es lo que falta.

### ⚠️ La paleta del cliente puede dejar la pantalla ilegible

`demo-enredados` tiene tinta `#f9f3ae` sobre papel `#b37fc3`: **2,74:1 a tinta plena**.
Ninguna variable arregla eso — es la combinación que eligió el cliente.

Por eso `pintarTema()` **no confía en `color_1`**: si no llega a 4,5:1 sobre el papel, usa
negro o blanco (el que gane). Y `--ink-soft` no es un 62% fijo —que se lee sobre blanco y
desaparece sobre un papel de color— sino la mezcla más suave que todavía llegue a 4,5:1.

⚠️ Ese cálculo va contra **`--velo-2`, no contra el papel**: los chips y los campos van
sobre el velo, que es el fondo más parecido a la tinta y por lo tanto el peor caso.
Midiendo contra el papel quedaban en 4,38:1 — apenas debajo, y a ojo no se nota.

Medido en los tres temas: claro 5,41:1 · oscuro 6,17:1 · el lila de Enredados 4,79:1.
- **Dos campos y nada más.** A la una de la mañana cada campo extra pierde gente.
- **El nombre es obligatorio**: "alguien te desea lo mejor" no sirve de recuerdo.
- Concordancia: en un casamiento son dos. Se deduce del nombre (`&`, ` y `) y se fuerza con `&t=p`.
- ⚠️ **El botón se bloquea ANTES de la llamada**: en un salón la conexión es mala, la
  respuesta tarda y el invitado vuelve a tocar. Sin eso el mismo deseo entra tres veces.
- ⚠️ **Si falla, el texto NO se pierde**: sigue en el campo, listo para reintentar. Perder
  un texto que alguien acaba de pensar es lo peor que puede pasar acá.
- ⚠️ **Se comprueba que el libro esté activo ANTES de pintar el formulario.** Dejar que
  alguien escriba diez renglones para avisarle recién al enviar es la peor forma de decirlo.

### Lo "juvenil" está en el movimiento, no en la tipografía

La fuente la elige la clienta y **la misma pantalla sirve para unos 15 y para un
casamiento**: una fuente juvenil fija rompe la boda de Guillermina. La personalidad la
ponen la entrada escalonada, la carta que se va volando, el sobre que se cierra y el número
que sube. Lo único tipográfico fijo es **la manuscrita de la firma** (Caveat), que funciona
bien en los dos — y se repite en el PDF del libro.

⚠️ **Un solo elemento animado en bucle** (el halo de la foto). Dos distraen.

Verificado a 390px en tema claro y oscuro: contraste peor **4,60:1 y 6,62:1**, ningún toque
menor a 44px, sin scroll horizontal.

### En el panel

**Editor de Secciones → 💫 Libro de Deseos** lo activa por evento (`config.deseos_activo`).
Apagado, la pantalla dice que esa fiesta no tiene libro de deseos.

**Invitados → 💫 Libro de deseos** muestra los mensajes y deja borrar el que no corresponda
(borra de verdad: en la fiesta de una clienta, un mensaje fuera de lugar no se esconde, se
saca). La tarjeta aparece con el libro activo **aunque no haya ninguno todavía**, o el
cliente no encuentra dónde bajar los carteles.

Dos PDF:
- **Carteles para las mesas** — uno por mesa asignada, A5 (dos por hoja A4), con su QR.
  ⚠️ El QR se genera con `qrcode-generator` **bajado bajo demanda** (56 KB): el panel se
  abre desde el celular y con datos. Verificado leyendo los QR renderizados a 38 mm / 300
  dpi con un lector de verdad (jsQR) — los siete devolvieron su URL con su mesa.
  ⚠️ El cartel dice **"escaneá el código"**, no "apoyá el celular": el tag NFC es opcional,
  el QR impreso está siempre.
- **Imprimir el libro** — lo que se le regala a la clienta cuando pasó todo. Va con aire y
  las firmas en manuscrita: tiene que leerse como un libro, no como una lista de tareas.

⚠️ **Los mensajes los escribe un invitado en una fiesta y terminan en la pantalla del
cliente**: la lista se arma con DOM, nunca con `innerHTML`, y en el PDF va con `escapeHtml`.

⚠️ **`🪧` no existe en Windows 10** (Unicode 13, año 2020): sale un cuadrito vacío. Antes de
usar un emoji nuevo en el panel, mirarlo en la máquina de Fer.

### ⚠️⚠️ Un `<select>` de sí/no guardaba la PALABRA "true"

`el.value` de un `<select>` es **siempre texto**. `guardarTodo()` hacía
`currentConfig[f.key] = el.value`, así que un desplegable de sí/no guardaba
`"true"`, no `true`. Y las pantallas comparan contra el booleano:

- activar el libro de deseos **no lo activaba** — decía "esta fiesta no tiene
  libro de deseos" con el interruptor en Activo;
- y, mucho peor, **pausar una invitación desde el panel NO la pausaba**. La función
  de cortar un link compartido estuvo rota en producción desde que se construyó.

Se arregló en los dos extremos: el panel convierte `"true"`/`"false"` a booleano al
guardar, y las pantallas aceptan **las dos formas** — los eventos guardados antes del
28/08/2026 tienen el texto adentro y no se van a volver a guardar solos.

⚠️ Cualquier campo de `config` que se lea con `=== true` necesita lo mismo. Se verifica
con las dos formas, no con una.

### Los QR de las mesas — `herramientas/generar-qr.js`

Una pieza circular por mesa: el QR adentro, el anillo con el texto curvo alrededor y el
número en el centro. **El QR sigue siendo cuadrado** — las tres esquinas grandes son las
que el celular usa para orientarse; lo que es redondo es la pieza.

⚠️⚠️ **Los módulos redondos SUELTOS no se leen.** Un círculo de radio 0,44 del paso cubre
el 61% de su celda: el lector promedia y la toma por blanca. De trece piezas no se leía
**ninguna**. La forma correcta es **unir los módulos vecinos** —un punto más un puente
hacia el de al lado—: en las zonas densas se funden en formas orgánicas, queda mejor que
los puntos sueltos, y la cobertura queda entera.

⚠️⚠️ **El pistacho claro no se lee.** Medido con jsQR sobre papel blanco:

| color | contraste | resultado |
|---|---|---|
| `#b5d99c` pistacho claro | 1,57:1 | no lee en ningún tamaño |
| `#99b57d` salvia | 2,27:1 | lee chico, **falla en grande** |
| `#7a9c5c` pistacho medio | 3,12:1 | lee chico, **falla en grande** |
| `#5d7a42` verde profundo | 4,85:1 | lee siempre |

Los del medio son los peligrosos: andan en la prueba y fallan cuando el invitado acerca
el celular. Por eso la pieza usa **dos verdes**: el código en el profundo y el anillo, el
centro y los adornos en el pistacho. Se ve pistacho y funciona.

⚠️ El marco de los ojos va de **6 módulos, no de 7**: el `stroke` de SVG se pinta mitad
adentro y mitad afuera, y un rect de 7 se come medio módulo de la zona quieta.

⚠️ El texto curvo necesita su **propio radio**, separado del aro: pegados, las letras se
apoyan contra la línea.

**Cada pieza se verifica leyéndola con jsQR a cuatro tamaños**, desde el que va a tener
impresa en la mesa. Un QR lindo que no se lee es un cartel inútil impreso trece veces.

### Riesgo aceptado

Quien sepa el slug del evento puede escribir un deseo, igual que puede confirmar asistencia.
Es spam, no una fuga: no puede leer nada. Tope de 2000 por evento.

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
⚠️ **El dominio sin www redirige al www con un 308, y el robot de WhatsApp no lo sigue.**
Detectado el 10/08/2026: `invitacionesdigitalesoficial.com/i?evento=…` devuelve 308 y la
vista previa sale sin foto, con el nombre del dominio pelado. El `www.…` y el `.vercel.app`
devuelven 200 con las etiquetas correctas. **La solución va en Vercel** —hacer principal el
dominio sin www y que el www redirija hacia él—, no en el código. Se verifica con:
`curl -sI -A "WhatsApp/2.23" https://invitacionesdigitalesoficial.com/i?evento=X` → tiene
que dar `200`, no `308`.

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

## Video de portada, mascota y zona horaria (agosto 2026)

Tres campos nuevos de `config`, los tres **opcionales**: sin ellos, los eventos
que ya existen no cambian en nada.

| Campo | Qué hace |
|---|---|
| `video_hero` | Video a pantalla completa en la portada |
| `mascota_url` | Un personaje que se asoma 2s al scrollear, como mucho cada 9 |
| `zona_horaria` | El país de la fiesta — **define la cuenta regresiva** |

⚠️ **El autoplay necesita `muted` + `playsinline` + `loop` juntos.** Sin
`playsinline`, iOS abre el video en pantalla completa y se come la invitación.
La foto del hero queda de `poster`, así que mientras baja se ve la foto y no un
rectángulo negro — y si el autoplay falla igual queda la foto de siempre.

⚠️ **Con video, el `hero-bg` aporta SOLO el velo.** La foto iría encima del
video y lo taparía entero.

⚠️ **El bucket rechazaba video con 415**: tenía lista blanca de tipos.
`sql/004_video_portada.sql` agrega mp4/webm/mov y sube el límite a 20 MB. **El
límite es el techo del sistema, no el objetivo**: un video de portada tiene que
pesar menos de 1 MB. El panel avisa arriba de 1,5 MB porque **el video no se
puede comprimir en el navegador** como las fotos.

### La cuenta regresiva estaba mal para todo evento fuera de Argentina

`fecha_iso` se guarda **sin zona** (`2026-12-04T19:00`): es la hora de un reloj,
pero no dice de cuál. El contador hacía `new Date(C.fecha_iso)`, que **cada
navegador lee en SU zona**. Para una fiesta en Cali, una invitada allá veía una
cuenta y su tía en Buenos Aires veía otra, con dos horas de diferencia.

Hoy el instante real se calcula con `Intl` y la zona del evento. ⚠️ **Va en DOS
PASADAS**: el primer tanteo puede caer del otro lado de un cambio de horario de
verano y devolver el desfasaje corrido una hora.

## Regalos: transferencia, lluvia de sobres, o las dos

`modo_regalo` = `transferencia` (por defecto) | `sobres` | `ambas`. Con `sobres`
desaparece el botón de copiar alias y aparece el cofre con su texto.

⚠️ **La sección ya NO depende de que haya alias.** Antes solo aparecía con
`alias_pago` cargado, así que para una fiesta sin transferencia había que
inventar un alias falso — en `sofiaenredados15` el alias era literalmente `♡`.

Si no cargan imagen de cofre hay un dibujo que toma los colores del evento.

## Pausar una invitación

`pausada: true` y los links ya compartidos muestran un aviso. **No se borra
nada** y se revierte con un clic. Es para el que probó y no contrató.

⚠️ La comprobación va **primero de todo** en `initApp` y hace `return`. Si fuera
después, o si solo escondiera el splash, alcanzaba con abrir las herramientas del
navegador para ver la invitación entera. Verificado: pausada da 0 secciones y
**cero fotos pedidas al Storage**.

## El grabador de reels — `herramientas/grabar-reel.js`

Abre la invitación en un navegador de verdad, la scrollea y guarda un PNG por
cuadro; ffmpeg los pega a 30 fps. Sale un 1080×1920 listo para Instagram.

⚠️⚠️ **EL TIEMPO DEL NAVEGADOR NO ES EL TIEMPO DEL VIDEO.** Cada captura tarda
~0,16 segundos **reales** pero avanza 1/30 de segundo de video: todo lo animado
corre **cinco veces más rápido** de lo que se ve. Los íconos laten a las
corridas, las fotos del carrusel pasan de a tres por segundo, y nada se entiende.

La solución no es bajarles la velocidad a ojo, es **sacarles el reloj**:

1. **Animaciones CSS** → se pausan todas y en cada cuadro se les pone el tiempo
   de video. ⚠️ Cada una cuenta **desde que apareció**, no desde que arrancó el
   reel: las secciones se animan al entrar en pantalla y con el tiempo total ya
   nacen terminadas.
2. **`setInterval`** (el carrusel y la cuenta regresiva) → se cortan todos y se
   manejan a mano. ⚠️ El carrusel cuenta **desde que la galería entra en
   pantalla**: si cuenta desde el inicio del reel, cuando se llega ya va por la
   tercera foto y la primera no se ve nunca.
3. **Transiciones CSS** (la mascota) → **no se pueden pausar**: con un
   `currentTime` mayor que su duración el navegador **las descarta** y el
   elemento vuelve al reposo. Hay que calcularles la posición a mano.

⚠️ **No usar el screencast de puppeteer**: entrega los cuadros cuando quiere, el
video sale con tirones y no dura lo que uno pidió.

⚠️ Dos cosas que delatan la captura: **la barra de scroll** (se esconde con CSS)
y los carteles de texto cayendo sobre el texto de cada sección. **Los textos no
van quemados en el video** — se ponen arriba en Instagram, donde se pueden
cambiar.

## `demo-enredados` — la demo de temática Disney

Nació de una venta perdida: la clienta de Cali no pagó y Fer quería hacer
contenido con esa invitación. **No se puede**: tenía su nombre, sus fotos, la
dirección exacta del salón, la fecha y su Instagram, y es una chica de 15 años
que además no era clienta.

La demo tiene la misma estética con datos inventados (Emilia), y **las imágenes
salen de cuadros del propio video**, que es generado por IA. Clave `demo1234`.

⚠️ **Nunca publicar la invitación de un cliente con sus datos reales.** Es
material de una persona real, y muchas veces menor de edad.

### Los archivos que mandan los clientes vienen con sorpresas

- El video traía la marca de agua de **KlingAI** abajo a la derecha
- El PNG de Pascal traía la firma de **otro autor**
- El "PNG transparente" del cofre tenía **el damero dibujado encima** — era una
  captura de pantalla de un editor

⚠️ **Revisar siempre las esquinas** de lo que se baja de generadores y bancos de
imágenes, antes de que salga en algo que se cobra.

⚠️ **El JPEG no tiene canal alfa. Nunca.** Un personaje recortado subido como
`.jpg` llega con un rectángulo blanco. Y comprimir un PNG a JPEG hace lo mismo.
Los campos marcados `transparente` en el panel avisan y no se convierten.

⚠️ **Para quitar un fondo va un relleno DESDE LOS BORDES**, no borrar todo lo
claro: si no, se comen los brillos de adentro de la figura.

## Cotizar afuera: la moneda al lado del número

La venta de Cali se cayó porque la clienta **confundió pesos colombianos con
argentinos**: 50.000 ARS son unos 150.000 COP, casi el triple de lo que entendió.
Un número sin moneda es un malentendido esperando pasar. **Cotizar en dólares o
en la moneda de quien lee.**

## ⚠️ Pendiente: invitaciones ilegibles en producción (28/08/2026)

Medido texto por texto, contra el fondo que efectivamente tiene detrás:

| evento | textos | peor | ilegibles |
|---|---|---|---|
| `demo-enredados` | 56 | 2,02:1 | **29** |
| `zaira15` | 57 | 1,09:1 | 7 |
| `almamia15` | 57 | 4,67:1 | 0 |

En `demo-enredados` **la mitad de los textos no se leen** — y es el demo con el que se
vende la temática Enredados y del que salió el reel. La causa es la paleta elegida: tinta
`#f9f3ae` sobre papel `#b37fc3` da **2,74:1 a tinta plena**. Ninguna variable lo arregla.

En `zaira15` los rotos son los que **se pintan desde JavaScript** (flechas del carrusel
1,09:1; botones "No puedo ir" y "Celíaco" 1,15:1): una auditoría que fotografía la página
no los ve.

`deseos.html` **ya se defiende sola** (ver su sección). `invitacion.html` no. Fer sabe del
problema; falta decidir el alcance: arreglar la paleta del demo (un dato, cinco minutos) o
blindar la invitación como el libro de deseos (toca clientas en producción).

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
