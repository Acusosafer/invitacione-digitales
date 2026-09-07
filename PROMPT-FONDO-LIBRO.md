# Las imágenes del libro de deseos

El libro (`/libro?evento=...`) **funciona sin ninguna imagen**: la escena se
dibuja sola en SVG. Las imágenes son lo que lo levanta de "lindo" a
"hecho para ella".

## Lo que se sacó de las fotos de Alma

Mirando `fotos alma/`, la fiesta no es un pantano de noche — es esto:

- **Vestido verde menta / agua**, corset bordado en plata, falda de tul.
- **Jardín japonés**: puente rojo lacado, glicinas lilas colgando,
  estanque, juncos, cerezos.
- **De día y luminoso.** Nada oscuro.

Así que la paleta es: **pistacho y menta**, crema, **dorado suave**, con el
lila de las glicinas de acento y el rojo del puente como toque puntual —
un toque, no un protagonista.

## Son dos cosas distintas, no una

| Campo | Qué es | Cuántas |
|---|---|---|
| `libro_fondo` | el **ambiente** que rodea la hoja, se ve por los costados | 1 |
| `libro_hojas` | la **página** donde se escribe, con su marco | 1 a 5 |

Con varias hojas, el libro **las va alternando** página por página: treinta
deseos no se leen como la misma estampita repetida treinta veces.

---

## Reglas que valen para TODAS

1. **Formato vertical.** El 768 × 1376 que te da Gemini está perfecto.
2. **Sin una sola letra.** El nombre de Alma, "El libro de deseos" y el
   número de página los escribe la web encima, con la tipografía del
   evento. Si el texto viene quemado en la imagen no se puede cambiar, no
   sirve para la próxima clienta, y encima queda dos veces.
3. **El centro tiene que quedar LIMPIO.** Ahí va el deseo. Todo lo
   ilustrado va en los bordes: arriba, abajo y los costados.
4. **Claro y de poco contraste en el medio.** El texto va oscuro encima.
5. **Nada de Tiana, ni el sapo, ni castillos.** El ambiente ya dice la
   temática; el personaje es de Disney y esto se cobra.
6. **Mirá las cuatro esquinas antes de subirla.** Los generadores meten
   marcas de agua abajo a la derecha, y ahí es donde se ve.

---

## 1 · La portada

> Vertical 9:16 watercolour illustration on warm cream paper. An elegant
> thin gold double frame with soft art-nouveau corners, leaving a large
> clean empty area in the centre. Around the frame: pale pistachio and
> mint green watercolour washes, white water lilies, delicate reeds, and a
> few hanging wisteria branches in soft lilac at the top corners. Small
> gold dots and tiny butterflies scattered. Very light, airy and luminous,
> visible paper grain, muted pastel palette, generous white space in the
> middle. No text, no characters, no people.

## 2 · Hoja A — para las páginas

> Vertical 9:16 watercolour illustration on warm cream paper. Soft
> pistachio and mint green watercolour washes in the upper left corner and
> the lower right corner, with white water lilies, lily pads and slender
> reeds. A thin gold line frame, simple and geometric. The entire centre
> of the image is clean cream paper with nothing on it. Delicate, airy,
> low contrast, visible paper grain. No text, no characters, no people.

## 3 · Hoja B — la misma idea, espejada

Igual que la A, pero: `upper right corner and the lower left corner`, y
cambiá `water lilies` por `hanging wisteria in soft lilac and small
cherry blossoms`.

## 4 · Hoja C — más suelta

> Vertical 9:16 watercolour illustration on warm cream paper. A tall
> cluster of slender green reeds and cattails rising along the left edge
> only, with two dragonflies and a few floating gold specks. A very thin
> gold vertical line down the right side. The centre and the whole right
> half are clean cream paper. Extremely minimal, pale pistachio and sage
> palette, visible paper grain. No text, no characters, no people.

## 5 · La hoja del cierre

> Vertical 9:16 watercolour illustration on warm cream paper. A calm pond
> painted across the bottom third: still pale green water, lily pads,
> three open white water lilies, soft reflections. A thin gold frame line.
> The upper two thirds are clean cream paper with only a few tiny gold
> dots. Pale pistachio, mint and cream palette, luminous and airy,
> visible paper grain. No text, no characters, no people.

## 6 · El ambiente de atrás (`libro_fondo`)

⚠️ Este reemplaza al estanque de noche. Va **claro**, como la fiesta.

> Vertical 9:16 watercolour illustration of a serene japanese garden pond
> in soft daylight. Pale mint and pistachio green water with gentle
> reflections, lily pads and white water lilies, tall reeds at the edges,
> hanging wisteria in soft lilac, and a hint of a red lacquered bridge in
> the distance. Delicate, luminous and low contrast, painted in light
> watercolour with visible paper grain. Nothing important in the centre of
> the frame. No text, no characters, no people.

---

## La silueta — ya está hecha

Vive en el Storage y el libro la usa en la portada y en el cierre, apoyada
en el borde de abajo y por debajo del texto.

### ⚠️⚠️ Vino como `.jpg`, y el JPEG NO TIENE CANAL ALFA. NUNCA.

Lo que parecía transparencia eran **los cuadraditos del editor pintados
encima**: una captura de pantalla. Es exactamente lo que pasó con el cofre
de la demo de Enredados.

Se arregló porque la figura era verde sólido y el damero gris claro, así
que se pudo separar por color. **Pero no siempre se puede.** Cuando pidas
un recorte, pedilo en **PNG**, y antes de mandármelo mirá si el fondo son
cuadraditos o es realmente nada.

⚠️ **El damero también estaba ADENTRO de la figura** — en el escote, entre
el brazo y el cuerpo, en la tiara. Esos son huecos del dibujo: sacar sólo
el fondo de afuera deja los cuadraditos puestos donde más se ven.

⚠️ Va **al 38% de alto y corrida al borde**. Al 46% y centrada, la cabeza
llegaba justo donde termina el último renglón. Un motivo anclado al margen
se lee como profundidad; en el medio de la hoja se lee como un sticker.
Verificado midiendo: no toca ni una letra.

## Si alguna vez hay que hacer otra

En la hoja que hiciste te gustó la silueta. Se puede hacer **con su foto
de verdad**: su vestido, su falda de tul, su pose, recortada y rellena en
un solo tono verde profundo o dorado. No se le ve la cara y sin embargo
es ella, no una ilustración de banco.

Sirven las de `fotos alma/` donde está de cuerpo entero y bien separada
del fondo. Decime cuál te gusta y la recorto.

## Cuando las tengas

Dejámelas en la carpeta y yo las optimizo (una hoja no puede pesar más de
~250 KB: son cinco y el libro se abre con datos móviles), las subo al
Storage y las cargo en el evento. Después te paso el link para que lo
mires en el celular.
