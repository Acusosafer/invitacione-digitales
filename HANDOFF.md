# HANDOFF — estado al 07/08/2026

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

## Hecho el 10/08/2026 — el día que salió a la calle

**Instagram lanzado.** Primer dato real, y lo que dijo:

```
22 visitas de Argentina en 3 días  ·  9 s de permanencia
6 tocaron el botón de WhatsApp     ·  0 escribieron
```

- **La geografía es la buena noticia**: Buenos Aires, González Catán, Berazategui,
  El Palomar, **Posadas** y **Concordia**. Las dos últimas están a más de 900 km: eso no
  es su círculo, es Instagram distribuyendo de verdad el primer día.
- **6 de 22 es un 27% de clics.** No fue casualidad: clickearon para averiguar el precio.
- **El precio no estaba en ningún lado de la web.** Al llegar al chat tenían que hacer
  ELLAS la pregunta incómoda, y seis de seis decidieron que no valía la pena. Esconder el
  precio le pasa al cliente el costo de preguntar.

⚠️ **Cómo leer ese GA4 sin engañarse:** de 82 usuarios totales, la mayoría eran robots
escaneando el dominio nuevo. Se delatan por la ciudad — **Boardman** (Amazon), **Ashburn**
(el mayor nudo de servidores del mundo), **Council Bluffs** (Google) — y por los números:
5 s de permanencia global contra 9 s en Argentina, e inglés como idioma dominante en un
sitio 100% en español. **Mirar siempre con la comparación "País = Argentina" puesta.**
En GA4 el evento `click` es **clic de salida**: en esta landing es el botón de WhatsApp.

### Lo que se arregló

- **Las tres invitaciones oscuras estaban rotas en producción.** El mensaje personal salía
  en negro sobre negro y las secciones Ubicación, Regalos y RSVP eran bandas casi blancas
  con texto blanco: invisibles enteras. **No era cosa de los demos: cualquier clienta que
  eligiera colores oscuros recibía eso.** Causa: `--black`/`--white` fijos y las franjas
  alternas escritas a mano como `#f9f9f9`. Ver la sección de tokens en `CLAUDE.md`.
- **Login del panel.** Sin `?evento=` el panel abría CALLADO el evento de otro y rechazaba
  la clave con "Clave incorrecta". Una clienta no podía entrar desde el celular —había ido
  por el botón "Panel" de la web— y creía que su clave estaba mal.
- **El parpadeo al abrir una invitación.** Se veía 1,7 s otra invitación (blanco y verde,
  la paleta por defecto) antes de la propia. Ahora `api/i.js` sirve la paleta ya resuelta.
- **Encuadre de fotos**: marco arrastrable en el panel con la forma real de cada lugar.
- **Botón de música**: el triángulo de play genérico pasó a un ecualizador que muestra el
  estado con el movimiento.
- **Sección de precio publicada**: `$50.000`, "precio de agosto", sin lista de tildes.
- **Reel vertical** de la placa de agosto, generado por código (`publicidad/generar-reel.js`).
- La galería de la landing: las demos oscuras se fundían con el marco del celular.
- El título que faltaba en Dresscode.

### Decisiones de Fer

- **Precio a la vista: `$50.000`, "precio de agosto".** Solo sirve si en septiembre
  realmente cambia; un plazo que no se cumple se nota y quema la credibilidad.
- **WhatsApp del negocio en una línea aparte**, para no perder su perfil personal. Ver la
  sección "El número de WhatsApp" de `CLAUDE.md` antes de tocarlo.

---

## Hecho el 10/08/2026 a la tarde — el RSVP en grupo

Fer pidió que el RSVP exigiera apellido "para después poder organizar". Tirando de ese
hilo aparecieron cuatro cosas más, tres de ellas rotas en producción.

**El apellido, obligatorio** — del titular y de cada acompañante. Sin él no se arman las
mesas ni sale la lista ordenada para el salón, que es la mitad del producto.

**Los cupos que desaparecían.** Si el titular tocaba "No puedo ir" teniendo acompañantes,
se guardaba **1 fila de 4**: los otros tres no quedaban ni en `no` ni en `pendiente`.
Confirmar borra la pre-alta, y las filas de acompañantes se armaban solo si el titular iba.
Ahora cada persona del grupo contesta por su cuenta. **Estuvo vivo mientras los invitados
de Alma confirmaban** y no hay forma automática de detectar a quién le pasó, porque los
cupos asignados no se guardan en ningún lado.

**"Familia Ferreyra" entraba como una persona.** El prellenado partía el nombre en dos y
dejaba los dos campos llenos, así que la validación lo aceptaba.

**Las etiquetas de acompañante, invisibles en temas oscuros** — `rgba(0,0,0,0.5)`, o sea
**1,11:1 sobre `zaira15`**. Se le escaparon al arreglo de colores porque esas tarjetas las
pinta el JS y solo existen si el invitado elige 2 o más personas: una auditoría que le saca
una foto a la página no las ve. Quedaron en 8,94:1.

**Inyección de HTML por el parámetro `?invitado=`**, que se metía tal cual en el saludo del
hero. El `toUpperCase()` rompía la mayoría de los scripts, pero por casualidad.

También, más temprano: buscador en el Historial (y se le sacó el `innerHTML`, que con la
creación de eventos sin clave era un agujero real), el botón de música que aparecía sin
música, el mensaje de entrega que mandaba al dominio viejo, y la herramienta de clave de
superadmin, cuyas instrucciones apuntaban a un archivo que ya no existe.

### Decisiones de Fer

- **Cada persona del grupo contesta por su cuenta**, aunque el titular no vaya. Eligió el
  dato exacto por sobre la comodidad de un solo toque.
- **Sí a la red de seguridad para links llamados "Familia X".**
- **Guardar el teléfono al generar el link, pero no hoy**: primero deja circular más links.
  El objetivo es que "Recordar" abra el chat directo.

## Hecho el 07/08/2026

- **Google Safe Browsing levantado.** Chrome ya no marca el sitio. Instagram queda liberado.
- **Medición instalada** en la landing y **solo** en la landing: GTM `GTM-T7QNB7VR` en el HTML,
  con GA4 `G-G7LL4G253B` y el píxel de Meta `2024768681739346` adentro. Detalle completo y
  el porqué de cada decisión en la sección "Medición" de `CLAUDE.md`.
  Verificado en navegador real: la landing dispara los tres; la invitación y el panel no
  disparan ninguno; y con `?invitado=Juan+Perez` no viajó **ningún** dato hacia Google ni Meta.
  ⚠️ Al probar el píxel, Meta responde `[Meta pixel] Bot traffic detected and blocked` a un
  navegador automatizado. **Eso no es una falla**: el evento no sale y parece que no anda.
  Para verificarlo hay que espiar `img.src`/`sendBeacon` o usar Meta Pixel Helper a mano.
  La extensión "Meta Pixel Validator" (de un tercero) da falso negativo con píxeles que
  entran por GTM — la oficial es "Meta Pixel Helper", de Meta Platforms.
- **GA4 afinado:** retención subida de 2 a 14 meses y filtro de tráfico interno activo para
  la IP de Fer. ⚠️ Es una IP hogareña: si cambia, el filtro deja de agarrar y sus propias
  visitas vuelven a contarse como clientes.
- **Dominio propio: `invitacionesdigitalesoficial.com`** (Namecheap, $11,28 el primer año /
  $14,98 de renovación). A `@` → `216.198.79.1` y CNAME `www` → el host de Vercel. El
  `.vercel.app` sigue vivo y redirige, así que los links ya mandados no se rompen.
  Se descartaron los cortos porque están todos ocupados (`invitacionesdigitales.com`,
  `invitaciondigital.com`, `tuinvitacion.com`, `quienviene.com`), y los `.digital`/`.lat`
  que Namecheap ofrece a $2 porque renuevan a ~$42.
  ⚠️ En el camino se compró `invitacionesdigitalesofical.com` **mal escrito** —sin la "i" de
  "oficial"—. No es el dominio del sitio. Se pidió reembolso a Namecheap; si no sale, queda
  como red para quien tipee mal.
- **Una sola marca.** El panel y el logo estaban en rosa `#ff3b6f` con Syne y la web en
  marfil y dorado con Fraunces: dos empresas conviviendo. Todo pasó al dorado. El panel
  sigue oscuro a propósito. Dos logos nuevos (`logo.png` transparente y `logo-og.png`
  1200×630 para vistas previas) y `publicidad/ig-perfil.png` para Instagram.
- **Pestaña "Mensajes y entrega"** (solo superadmin): respuesta a una consulta, qué pedirle
  al cliente, y entrega con los links armados solos.
- **Footer de la invitación con link a la web** + "¿Querés una así para tu fiesta?".
- **Agendar de un toque**, sin descargas: abre Google Calendar. Se sacó el menú de dos
  opciones y el `.ics`.
- **Bug de zona horaria arreglado**: la fecha se leía en la zona del navegador, así que un
  invitado en España se agendaba las 17:00 de acá.
- **"Deslizá" por encima de la barra del navegador** (`100vh` no la descuenta; `100svh` sí).
- **Música obligatoria** y **la lista de invitados la carga el cliente**, no se le pide.
- **`publicidad/instagram.md`**: perfil, bio, y prompts de las seis piezas para Claude Design.

## Hecho el 05 y 06/08/2026

- **El RSVP ya no puede perder cupos.** Exige el nombre de cada acompañante antes de
  confirmar. Antes, elegir 5 y dejar los campos vacíos borraba 4 cupos sin avisarle a nadie.
- **Panel: botón de eliminar invitado** y estado ⏳ "Sin responder" con su propia tarjeta.
  Antes los pendientes se contaban como "No asistirán" — en el evento de una clienta eso
  mostraba 9 personas que "no venían" y en realidad no habían contestado.
- **Panel usable en el celular.** Medía 787px de ancho sobre 390. Ahora entra clavado.
- **Recordatorio a pendientes** con el mensaje de WhatsApp armado.
- **Botón "Agendar"** en la invitación (.ics con aviso el día anterior).
- **Indicador "Deslizá"** en el hero: muchos invitados se quedaban ahí sin saber que seguía.
- **Los asientos del croquis muestran el nombre**, con el completo al apoyar el mouse.

## Pendientes, en orden

0. ⚠️ **Hacer principal el dominio SIN www, en Vercel.** Hoy el apex devuelve un **308** al
   `www` y **el robot de WhatsApp no sigue redirecciones**: todo link al dominio sin www se
   comparte sin foto, con el nombre del dominio pelado. El `www` y el `.vercel.app` andan
   bien. Es un cambio de configuración en *Settings → Domains*, no de código. Se verifica
   con `curl -sI -A "WhatsApp/2.23" https://invitacionesdigitalesoficial.com/i?evento=X`:
   tiene que dar `200`. **Urge**, porque el dominio sin www es el que está impreso en el
   pie de las invitaciones, el reel, la placa y la bio de Instagram.

0.5. **Guardar el teléfono al generar el link**, para que "Recordar" abra el chat de esa
   persona en vez de dejar el texto para copiar. Fer lo pidió el 10/08 **para después de
   dejar circular más links**. Ver "Qué se puede saber de un link" en `CLAUDE.md`: son
   datos personales de invitados de un cliente, así que van por función `SECURITY DEFINER`
   y nunca al navegador del invitado. Junto con esto conviene **guardar los cupos
   asignados**, que hoy no se guardan y por eso nada de esto es auditable.

1. **La línea nueva de WhatsApp.** Fer la consigue, instala WhatsApp Business (nombre, logo
   y **mensaje de bienvenida automático** — ese es el que convierte), y pasa el número.
   Ahí hay que cambiarlo en los **nueve lugares de texto MÁS el MP4 del reel y el PNG de la
   placa**, que lo tienen en los píxeles. Lista completa en `CLAUDE.md`.
   ⚠️ **No publicar el reel actual en Instagram** si el número va a cambiar.
2. **Esperar el primer mensaje.** Es la única métrica que decide si el precio publicado
   arregló la fuga. Volver a mirar GA4 con Argentina aislada en 4-5 días:
   los clics deberían BAJAR (el precio filtra antes) y los mensajes subir.
3. **Terminar `almamia15`**: volver a subir la portada (la vieja pesa 2,26 MB) y cambiar
   `foto_galeria_2`, que todavía apunta a `/assets/valentina15/...` de cuando se copió ese evento.
7. **Escuchar dos temas** asignados con dudas: `luna15` (capoeira, se pidió folk de jardín) y
   `boda-julieta` (se llama "morning" y se pidió ambient nocturno).
8. **La landing tarda.** Medida en 4G con CPU de gama media: primer texto a los 2,4 s, pero
   **todo cargado recién a los 7,3 s** — son 14 iframes y 2 MB. La visita promedio dura 9 s,
   así que lo que mejor vende —los celulares con invitaciones moviéndose— aparece justo
   cuando la persona se está yendo. **No tocar hasta tener más datos**: con 22 visitas,
   cambiar por esto es leer ruido. Si con más tráfico el tiempo sigue en 9 s, el arreglo es
   que los tres del hero carguen ya y los doce de la galería recién al bajar.
9. **Dos mejoras de ergonomía del admin**: que `verificar_clave` distinga "falta configurar el
   hash" de "clave incorrecta" (hoy dice lo mismo para las dos cosas), y un formulario para
   cambiar la clave de superadmin sin pasar por SQL.
10. **Que el invitado pueda corregir su confirmación.** Hoy si se equivoca queda trabado y
   depende de que el cliente le borre la fila.
11. **Mail propio** (`fer@invitacionesdigitalesoficial.com`). Ahora que hay dominio se puede.
   Zoho Mail free alcanza; hay que cargar SPF, DKIM y MX en el Advanced DNS de Namecheap,
   **sin tocar** el A `@` ni el CNAME `www` que apuntan a Vercel.
12. **Verificar el dominio en Meta** (registro TXT en Namecheap). Solo importa el día que
   ponga plata en publicidad: sin eso el píxel mide con limitaciones a los que vienen de
   iPhone, que en su rubro son casi todos.

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
- **`valentina15` ya NO usa `admin123`.** Fer se la cambió en algún momento; el resto de los
  demos la conserva. Para probar contra la base conviene usar `boda-ana`.
- **Los textos de venta se leen en el código fuente** de `admin.html`. Es material público
  igual, pero ahí no van precios especiales para un cliente puntual.
- **Automatizar seguidores en Instagram no se hace.** Viola los términos y en una cuenta
  nueva es la forma más rápida de que la bloqueen. Se habló el 07/08 y quedó descartado.

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
