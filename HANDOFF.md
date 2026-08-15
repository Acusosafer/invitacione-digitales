# HANDOFF — estado al 12/08/2026

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

## Hecho el 12/08/2026 — las dos fugas de la vista previa

Se cerraron los dos agujeros por los que un link compartido salía sin foto. Los dos eran
invisibles desde el navegador: Chrome sigue los redirects solo y no muestra las
metaetiquetas, así que abrir la web y verla bien **no prueba nada**.

**1. El apex ya no redirige.** Era el pendiente 0. En Vercel → Settings → Domains, el
dominio sin `www` estaba en *Redirect to Another Domain* y pasó a *Connect to an
environment → Production*. **No había que tocar el código 308**, sino el radio button.

```
antes  invitacionesdigitalesoficial.com  →  308 Permanent Redirect   (WhatsApp se iba)
ahora  invitacionesdigitalesoficial.com  →  200 OK
```

Verificado con `curl -sI -A "WhatsApp/2.23.20.0"`: da `200`, y `/i?evento=boda-ana` sirve
`og:image` con las URLs ya apuntando al apex. El dominio impreso en el pie de las
invitaciones, el reel, la placa y la bio de Instagram vuelve a compartirse con foto.

**2. La landing no tenía NINGUNA etiqueta Open Graph** — y esto no lo causaba el redirect:
faltaban desde siempre, en los dos dominios. Compartir `invitacionesdigitalesoficial.com`
a secas mostraba un renglón gris sin imagen. Es el link de la bio de Instagram, o sea el
que más circula. `logo-og.png` (1200×630) ya existía en la carpeta y no lo usaba nadie.
Se agregó el bloque completo en el `<head>` de `index.html`, con el mismo criterio que
`api/i.js` usa para las invitaciones.

⚠️ **Cómo NO verificar esto:** abriendo la web. Se verifica con `curl` haciéndose pasar por
el robot, o compartiendo el link por WhatsApp **con una URL nueva** (el caché es por URL).

**Estado al cierre del 12/08:** commit `eaea28b`, pusheado y deployado. Producción devuelve
las 12 etiquetas y `logo-og.png` responde `200`. Medido en producción, para que nadie vuelva
a buscar el problema donde no está:

```
HTML            54 KB        og:title   byte 3.558     respuesta  0,14 s
logo-og.png     171 KB       og:image   byte 3.899     apex       200 OK
```

**Pero WhatsApp seguía sin mostrar la tarjeta**, y del lado del servidor no queda nada por
arreglar. Quedan dos causas, las dos fuera del código — ver el pendiente 0.2.

### Cómo verificar una vista previa, de una vez por todas

```bash
# lo que ve el robot (NO lo que ve tu navegador)
curl -s -A "WhatsApp/2.2429.5 N" "https://invitacionesdigitalesoficial.com/" \
  | tr '>' '>\n' | grep -E 'og:(title|image"|url)'

# que el apex no redirija: tiene que dar 200, nunca 308
curl -sI -A "WhatsApp/2.2429.5 N" "https://invitacionesdigitalesoficial.com/" | head -1
```

Chrome sigue los redirects solo y encima **esconde el `www.` de la barra de direcciones**:
por eso el 308 fue invisible durante días mientras la web "se veía bien".

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

## Hecho el 15/08/2026 — la primera venta en curso

Fer comentó un reel viral de unos 15 (marzo 2027, a 7 meses) y **la madre le contestó
"pasame y chusmeo"**. Es el primer prospecto real que llega por Instagram. Todo lo de este
día salió de ahí.

**Modo muestra (`?muestra=1`) y la ruta `/muestra`.** Le manda la invitación de Alma —con
permiso de la familia— entera y navegable, con el RSVP funcionando, pero sin guardar nada.
El RSVP se muestra funcionando a propósito: es la mitad de lo que se está vendiendo, y el
momento en que se entiende el producto es justo cuando la persona lo completa.

⚠️ **Dos bugs graves, los dos encontrados antes de que el link se mandara.** Instagram no
convierte en link una URL con `?` y `&`, así que el primer mensaje llegó con la dirección
en texto plano: desde el celular no se podía tocar. Y la ruta limpia que lo arreglaba
**abría la invitación de `valentina15` con el RSVP vivo**, porque una ruta limpia deja
`location.search` vacío. Ver la sección `/muestra` de `CLAUDE.md`.

**El hero en PC mostraba el torso y no la cara.** Una foto vertical se recorta a lo ancho
en el celular y a lo alto en la PC; el encuadre guardado es uno solo y está elegido para el
celular. Le pasaba a cualquier cliente con foto vertical.

**Canciones y acompañantes estaban mezclados** en el panel de Alma: un acompañante que no
pedía tema quedaba con "Acompañante de Fulano" guardado en el campo de la canción. El
fallback dejó de escribirse, y el filtro que limpia lo viejo es **de lectura**, para no
tocar la base de una clienta con la fiesta en marcha. Salió de ahí la **lista para el DJ**,
agrupada por canción y no por persona.

**La tarjeta al compartir la web** ya no es el logo: es un celular con la invitación de
Alma. 1200×630 y 245 KB, las dos medidas verificadas — la primera versión pesaba 809 KB y
habría salido sin foto.

**Maqueta del libro de deseos** (`deseos.html`), para aprobar el diseño antes de construirlo.

### Decisiones de Fer

- **La invitación de Alma como muestra**, ya hablado con la familia.
- **NFC: NTAG213**, 15 o 20 para las mesas, no cien souvenirs.
- **No poner precio en el primer mensaje.** A 7 meses la venta es ahora, pero primero que
  vea el producto.

### Lo que quedó pendiente de esa conversación

⚠️ **El chat de Instagram tiene los mensajes temporales activados**: lo que le escribe se
borra a las 24 horas. Hay que apagarlo antes de seguir esa charla.

Y quedó prometido un descuento ("hay descuento?" → "obvioooo"). **No fijar un número en
pesos con meses de anticipación**: se honra sobre el precio que esté vigente ese día.

## Pendientes, en orden

0. ✅ **HECHO el 12/08.** Era: hacer principal el dominio sin www. Ver la sección del 12/08.

0.1. **Que `www` redirija al apex.** Hoy los dos sirven la web, así que Google la ve
   duplicada. En *Settings → Domains* → `www...` → *Redirect to Another Domain* → 308 →
   `invitacionesdigitalesoficial.com`. Es prolijidad de SEO, no urgencia: los links viejos
   con `www` funcionan igual. Hacerlo cuando haya un rato, y después avisarle a Search
   Console cuál es la versión buena.

0.2. ⚠️ **Forzar el re-scrape en Meta.** Lo tiene que hacer Fer: necesita su cuenta.

   > **developers.facebook.com/tools/debug** → pegar `https://invitacionesdigitalesoficial.com/`
   > → **Depurar** → **Volver a extraer** (*Scrape Again*)

   WhatsApp usa el scraper de Facebook. El dominio estuvo roto desde que se compró, así que
   Meta lo tiene cacheado como "acá no hay preview" y no vuelve a mirar por su cuenta.
   Re-extraer limpia el caché de Facebook, Instagram y WhatsApp a la vez.

   Y al probar: **mandar el mensaje de verdad, y desde el celular**. WhatsApp Desktop no
   genera la vista previa de forma confiable en el campo de escritura — el 12/08 se probó
   dos veces ahí y pareció que el arreglo no había funcionado, cuando ya estaba en línea.
   Cada URL probada queda cacheada con lo que devolvió esa vez: usar una nueva cada intento
   (`/?ok=1`, `/?ok=2`), **nunca el link limpio**, que hay que dejar sin quemar.

0.25. **Seguir la charla con la madre del reel** (`maltech2024`). Es el único prospecto
   real que hay. Antes de escribirle: **apagar los mensajes temporales** del chat, o lo que
   le mande se borra en 24 horas. El link a mandarle es
   `invitacionesdigitalesoficial.com/muestra`. La fiesta es en **marzo 2027** y las
   invitaciones se mandan dos o tres meses antes, así que decide entre diciembre y enero.

0.28. **Conectar el libro de deseos a la base.** Hoy `deseos.html` es una maqueta que no
   guarda nada. Falta la tabla, que el cliente pueda borrar un deseo desde su panel, y
   decidir si el muro lo ven todos o solo el agasajado. Es ~1 día. El evento de septiembre
   es el laboratorio.

0.3. ✅ **HECHO el 15/08.** Era: cambiar el logo por una invitación real en la tarjeta al
   compartir. Hoy es `og-home.png`, un celular con la invitación de Alma. Se regenera con
   `node publicidad/generar-og-home.js`. **Si algún día cambia, verificar las dos medidas:**
   1200×630 exactos y menos de ~600 KB, o WhatsApp la descarta y la tarjeta sale sin foto.

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
3. ✅ **HECHO.** Era: terminar `almamia15`. Verificado el 11/08 contra Supabase — las siete
   fotos y la música son archivos propios en Storage (ya no hay ninguna prestada de
   `valentina15`), y las portadas pesan bien: hero 197 KB, splash 454 KB, las dos por
   debajo del límite de ~600 KB con el que WhatsApp descarta la imagen de la vista previa.
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

## Lo que viene: libro de deseos y galería de fotos

Charlado el 12/08. Es lo único que el producto no tiene y la competencia tampoco, y lo que
más se parece a un motivo para elegirlo.

**El evento real de septiembre es el laboratorio.** Es el único que hay, está regalado a una
pariente, así que se puede estrenar sin riesgo comercial. De ahí salen las dos cosas que hoy
faltan: saber si la gente realmente lo usa, y **material de Instagram con una fiesta de
verdad**, que vende mucho más que cualquier placa de diseño.

### Orden recomendado

| | Qué | Cuánto | Por qué en ese orden |
|---|---|---|---|
| 1 | **Libro de deseos** | ~1 día | Texto puro. Cero storage, cero riesgo. La mitad del valor emocional por la décima parte del trabajo. |
| 2 | **Galería de fotos** | ~3-4 días | El diferencial fuerte, pero se lleva todos los problemas de abajo. |
| 3 | NFC en las mesas | 1 tarde | Accesorio opcional, 10-15 tags. Ver abajo. |

### Dónde van las fotos: ya está resuelto y no es Google Drive

Se descartó Google Drive y OneDrive/Hotmail: para subir a una carpeta compartida el invitado
necesita cuenta e iniciar sesión, y encima consume el espacio de alguien. En una fiesta, de
noche, eso no lo hace nadie.

**Va en el bucket `invitaciones` de Supabase Storage, que ya existe y ya está probado**
(`sql/003_storage.sql`): `anon` puede leer y subir, no actualizar ni borrar. Es exactamente
lo que necesita una galería colaborativa — el invitado abre el link, elige y sube. Sin
cuenta, sin login, sin app.

### La compresión no es opcional

```
100 invitados × 10 fotos × 4 MB  =  4 GB en UNA fiesta
Supabase free                    =  1 GB
```

El primer evento revienta el plan gratis. Hay que **comprimir en el navegador antes de
subir**, con canvas y JS puro: a 1920 px de lado largo y calidad 0,82 una foto de 4 MB baja
a ~400 KB. Eso lleva la fiesta a ~400 MB.

⚠️ **La compresión es irreversible.** Si después se manda el pack por WeTransfer, viaja lo
comprimido. Nunca prometer "las fotos en calidad original": para eso habría que guardar los
originales y el costo se multiplica.

**No hace falta prometerlo.** La calidad alta ya la cubre el fotógrafo — para eso lo
contratan. La galería colaborativa es otra cosa: la mesa riéndose, el abuelo bailando, la
coreografía filmada por una amiga. Esas fotos se ven en el celular, no van a un cuadro. A
1920 px se ven perfectas incluso impresas en 10×15, y **WhatsApp comprime más fuerte que
eso** cuando los invitados se las mandan entre ellos.

Para septiembre: arrancar en 1920 y **medir cuánto pesó de verdad**. "10 fotos por invitado"
es un número de manual; en la práctica sube el 20-30% de la gente. Con el dato real se decide
si conviene subir a 2560 px (~900 KB, indistinguible del original hasta impreso grande).

### ⚠️ Seguridad: son fotos de menores

Una galería abierta en una fiesta de 15 son **fotos de chicas de quince y sus amigas, subidas
por invitados**, en un bucket donde `anon` puede leer. Antes de que esto exista:

- **Rutas con token aleatorio largo.** Nada de `/galeria/evento/1`: si es adivinable, alguien
  recorre todos los eventos de todos los clientes.
- **`noindex` + robots.txt.** Que Google no indexe ni una foto.
- **Que el cliente pueda borrar**, por función `SECURITY DEFINER` como todo lo privilegiado.
  `anon` sigue sin poder.
- **Validar el archivo de verdad**: tipo real (no la extensión), tamaño máximo y cantidad
  máxima por persona.

Son los puntos 1 y 2 de las reglas post-Pappos Cars, con un agravante: acá no se filtra un
precio de compra. **Si esto sale mal no es un bug, es el fin del producto.**

### El NFC, en su lugar

La idea original era un souvenir NFC. Conclusión de la charla: **es un accesorio, no el
producto**, y va último. Con cero ventas todavía, agregarle un objeto físico a algo que no
vendió una sola unidad es construir el segundo piso antes que el primero.

Lo que sí conviene, en septiembre: **10 o 15 tags NTAG213 en las mesas, no cien souvenirs**.
Cuesta unos pocos miles de pesos y sirve para dos cosas — ver si la gente realmente toca, y
filmar a alguien apoyando el celular en la mesa para subir fotos. Ese video vale más que
cualquier placa.

Notas técnicas por si se hace: **NTAG213 alcanza** (144 bytes; el 215/216 es pagar de más
por memoria que no se usa). **Grabar siempre un redirect corto propio**, nunca la URL final,
porque si no hay que reescribir los tags uno por uno. **Bloquear (read-only) recién en
producción**, nunca en las pruebas: es irreversible. El NFC le gana al QR acá por una razón
concreta y no de marketing: de noche, con luz baja, la cámara no enfoca el QR.

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
