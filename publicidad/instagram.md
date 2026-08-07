# Instagram — perfil y publicaciones

> No se publica: `publicidad/` está en `.vercelignore`.
>
> ⚠️ **No arrancar hasta tener el dominio propio y Safe Browsing limpio.** Cada persona que
> le dé clic al link de la bio hoy ve "Peligroso" en Chrome. Esa es la primera impresión y
> no hay segunda.

---

## 1 · El perfil

**Foto:** `publicidad/ig-perfil.png` (1080×1080). El logo horizontal no se lee en un
círculo de 110px; esta versión tiene el texto al doble de tamaño y en dos líneas.

**Nombre** — es el campo que Instagram indexa en la búsqueda, así que no va solo la marca:

```
Invitaciones Digitales | 15 años y Casamientos
```

**Usuario:** el que ya tenés. Si todavía se puede cambiar, que sea corto y sin puntos ni
guiones bajos — se dicta por teléfono y se escribe mal.

**Bio** (150 caracteres). Tres opciones, distinto ángulo cada una:

```
A · El problema
Dejá de perseguir gente por WhatsApp.
Tu invitación se abre en el celular y te dice quién viene.
15 años · Casamientos · Buenos Aires
```

```
B · El producto
No es una plantilla con tu nombre encima.
Tus colores, tus fotos, tu música. Lista en 24 h.
📍 Buenos Aires
```

```
C · Directa
Invitaciones digitales para 15 años y casamientos.
Un link por invitado. Confirmaciones en vivo. Mesas armadas.
Escribime 👇
```

Recomendación: **la A**. Abre con el dolor, no con lo que vendés.

**Categoría:** Servicio de eventos.
**Botón de contacto:** WhatsApp con tu número (`+54 9 11 2457-6536`).
**Link:** tu dominio, cuando lo tengas.

**Historias destacadas** — cuatro, en este orden:

| Nombre | Qué va adentro |
|---|---|
| `Cómo es` | Recorrida en video de una invitación de punta a punta |
| `El panel` | Confirmaciones entrando, mesas armándose |
| `Precios` | Qué incluye y cuánto sale |
| `Clientas` | Capturas de mensajes reales (con permiso) |

---

## 2 · Cómo pedirle las piezas a Claude Design

**Pegá SIEMPRE este bloque primero.** Sin él salen genéricas y no se parecen a tu web.

```
IDENTIDAD DE MARCA — respetala en todo:

Paleta:
· Fondo oscuro    #08080a
· Fondo claro     #FAF4EA (marfil cálido)
· Dorado profundo #A8761F   ← para texto sobre fondo claro
· Dorado claro    #F7CE84   ← para texto sobre fondo oscuro
· Tinta           #191410

Tipografías:
· Títulos: Fraunces (serif con carácter), peso 600-700
· Textos:  Instrument Sans, peso 400-500

Reglas:
· Formato EXACTO 1080×1080 px. Cuadrado perfecto, NO apaisado.
· La composición tiene que ocupar TODO el alto. Aire repartido,
  no un bloque arriba y la mitad de abajo vacía.
· Sin emojis: al lado de una serif elegante quedan como manchones.
· Al pie, chiquito: INVITACIONES DIGITALES
· NADA de gradientes azul-violeta, tags de colores, ni cards
  idénticas con ícono+título+descripción
· Sin fotos de stock de gente sonriendo
· Si hay un número, que cuente algo — no que decore
· Nada de datos inventados: ni dominios, ni marcas, ni cifras.
  Si falta un dato, dejá el lugar marcado.
· Pregunta de control: ¿esto podría ser de cualquier empresa?
  Si sí, rehacelo.
· Contraste mínimo 4.5:1 entre texto y fondo
```

> Estas cinco reglas salieron de la primera pasada real: devolvió una pieza apaisada, con
> el 40% inferior vacío, un emoji que peleaba con la tipografía, sin la marca en ningún
> lado y con un dominio inventado.

### Las seis piezas

**1 · Presentación (el post fijado)**

```
Pieza 1/6. Fondo oscuro #08080a.
Un solo mensaje, tipografía grande, mucho aire:
   "Tu fiesta empieza
    mucho antes de la fiesta"
"mucho antes" en Fraunces itálica y dorado claro; el resto en marfil.
Abajo, chico y espaciado: INVITACIONES DIGITALES · 15 AÑOS · CASAMIENTOS
Sin íconos. Sin bordes. Que respire.
```

**2 · El problema**

```
Pieza 2/6. Fondo marfil #FAF4EA.
Arriba, en Fraunces oscuro y grande:
   "Tenés 120 invitados
    y 120 conversaciones"
Debajo, texto chico en Instrument Sans:
   "Cada uno pregunta lo mismo: dirección, horario, si puede
    llevar a alguien. Y vos anotás todo en una libreta."
Abajo del todo, en dorado profundo:
   "Hay otra forma →"
Composición asimétrica, el texto pegado a la izquierda.
```

**3 · Cómo funciona**

```
Pieza 3/6. Fondo oscuro.
Cuatro pasos en una línea de tiempo VERTICAL a la izquierda,
unidos por una línea fina dorada. Nada de cuatro cajas iguales.
   01  Nos contás la fiesta
   02  La diseñamos entera
   03  Mandás un link por WhatsApp
   04  Ves quién viene, en vivo
Números en Fraunces dorado y grandes; textos en marfil, chicos.
El paso 04 un poco más destacado que el resto.
```

**4 · El link personalizado**

> La primera versión de este prompt salía con **una sola burbuja**, y el titular dice
> "cada invitado recibe el suyo": lo visual contradecía al texto. Además dejaba el 40%
> inferior vacío. Esta versión usa ese espacio justamente para mostrar la idea.

```
Pieza 4/6. Formato EXACTO 1080×1080 px, cuadrado perfecto.
Fondo marfil #FAF4EA.

Composición en tres bandas que ocupan TODO el alto:

ARRIBA — en Fraunces oscuro #191410, dos líneas, grande:
   "Cada invitado recibe el suyo,
    con su nombre ya puesto"

AL MEDIO — una burbuja de mensaje protagonista: fondo #08080a,
esquinas muy redondeadas, rotada -2°, sombra suave y difusa.
   "¡Hola Familia González! Están invitados a nuestro casamiento.
    Confirmen acá"
y debajo, en dorado claro #F7CE84 subrayado:
   "invitacionesdigitales.com/familia-gonzalez"
Sin emojis: rompen la elegancia de la tipografía.

ABAJO — acá está la clave, y es lo que hoy queda vacío. Tres burbujas
más, mucho más chicas, apiladas y desvaneciéndose hacia el borde
inferior, cada una con otro nombre:
   "¡Hola Tía Marta!..."  "¡Hola Lu y Marian!..."  "¡Hola Los Pérez!..."
Que se entienda de un vistazo que no es un mensaje: es uno por cada
invitado.

PIE — centrado, muy chico, en dorado profundo #A8761F:
   INVITACIONES DIGITALES
```

⚠️ **El link tiene que ser tu dominio real.** Claude Design inventó `fiesta.link/gonzalez`
en la primera pasada. Poner un dominio que no es tuyo en material comercial confunde y no
suma nada.

**5 · El panel**

> Los números son ILUSTRATIVOS: el panel de una fiesta, no las métricas del negocio. Por
> eso el prompt exige el encabezado con el nombre del evento — sin él, alguien lee "47"
> como si fueran tus clientes.

```
Pieza 5/6. Fondo oscuro #08080a.

Tiene que leerse como EL PANEL DE UNA FIESTA, no como métricas de la
empresa. Arriba a la izquierda, chiquito y en gris, como encabezado
de pantalla:
   CASAMIENTO DE ANA & JOSÉ · 21 DE NOVIEMBRE

Debajo, el titular en Fraunces marfil, grande:
   "Y del otro lado, vos"

En la banda media, tres datos alineados a la izquierda, sin cajas ni
bordes, muy separados entre sí:
   47   confirmados
    9   sin responder
    6   mesas armadas
Números enormes en dorado claro #F7CE84, etiquetas chicas en gris.

Cerrando abajo, en Instrument Sans marfil, una sola línea:
   "Sin una sola planilla de Excel."
```

**6 · Cierre**

> La primera versión decía "Nada más, que el vacío haga el trabajo", que se contradice con
> la regla del bloque base de ocupar todo el alto. Y "Escribime por WhatsApp" no es una
> acción posible dentro de una imagen: en Instagram se responde por mensaje o por el link
> de la bio, así que el cierre nombra esas dos.

```
Pieza 6/6. Fondo marfil #FAF4EA.
Composición equilibrada: con aire, pero repartido de arriba a abajo.
NO dejes la mitad inferior vacía.

ARRIBA, ocupando la mitad superior, en Fraunces oscuro #191410:
   "Que empiece bien
    desde el primer mensaje
    que mandás"

AL MEDIO, una línea fina dorada #A8761F de unos 200 px, centrada.

ABAJO, anclado cerca del borde inferior, en dorado profundo y más
chico que el titular:
   "Escribime por acá"
y debajo, en gris y más chico todavía:
   "o tocá el link de la bio"
```

---

## 3 · Textos de los posts

**1 · Presentación**
> La invitación no es el papel. Es el momento en que alguien se entera de que va a ser
> parte de algo.
>
> Hago invitaciones digitales para 15 años y casamientos. Se abren en el celular, suenan,
> cuentan los días que faltan y te van diciendo quién viene.
>
> Una para cada fiesta. Ninguna igual a otra.

**2 · El problema**
> Si estás organizando, esto lo viviste: mandás la invitación al grupo y empiezan a llegar
> los mensajes sueltos. "¿Dónde era?" "¿A qué hora?" "¿Puedo llevar a mi novio?"
>
> Y vos anotando en una libreta quién va y quién no.
>
> Con una invitación digital eso no pasa: cada uno confirma en su link y a vos te llega
> ordenado. Sin planillas y sin perseguir a nadie.

**3 · Cómo funciona**
> Cuatro pasos y ya la estás mandando. Sin apps que bajar y sin que nadie se cree una
> cuenta.
>
> Nos contás la fiesta, la diseño entera con tus colores y tus fotos, y en 24 a 48 horas
> la tenés. Después mandás un link por WhatsApp y listo.

**4 · El link personalizado**
> Este es el detalle que más sorprende.
>
> No mandás el mismo link a todos: cada invitado recibe el suyo, con su nombre ya escrito
> y los lugares que vos le diste. Abre y lee "Hola Familia González, están invitados".
>
> Los armás vos, desde tu panel, a medida que vas invitando.

**5 · El panel**
> Mientras tus invitados abren la suya, vos tenés un panel donde pasa todo lo demás.
>
> Quién confirmó, quién come sin TACC, qué tema pidió. Las mesas se arman arrastrando y al
> final imprimís el plano ordenado por apellido.
>
> Sin una sola planilla de Excel.

**6 · Cierre**
> Tu fiesta se prepara durante meses. La invitación es lo primero que ve tu gente.
>
> Escribime y te cuento cómo sería la tuya. Sin compromiso.

---

## 4 · Lo que va a funcionar mejor que todo esto

**Capturas y videos de invitaciones reales.** Tenés doce demos y clientas de verdad. Una
grabación de pantalla recorriendo una invitación —con la música sonando— rinde más que
cualquier placa de diseño. Las placas son para sostener la grilla entre publicación y
publicación.

**Los proveedores, no los seguidores.** Salones, fotógrafos, DJs, pasteleras,
organizadoras. Ven a la misma quinceañera que vos, tres meses antes, y ya tienen su
confianza. Un acuerdo con dos salones de tu zona vale más que 2.000 seguidores fríos.

**Seguir a mano y comentando.** De a 20-30 por día, comentando antes de seguir. Automatizar
follows viola los términos de Instagram y en una cuenta nueva es la forma más rápida de
que te bloqueen las acciones.
