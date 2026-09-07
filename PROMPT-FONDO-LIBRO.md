# El fondo del libro de deseos

El libro (`/libro?evento=...`) funciona **sin imagen**: la escena se dibuja
sola en SVG. La imagen es un extra que lo levanta mucho, y va en
`config.libro_fondo` (una URL del Storage — se sube desde el admin igual
que cualquier foto).

## Qué tiene que ser esa imagen

Es **ambiente, no protagonista**. Arriba se apoya el papel crema donde se
lee, así que la imagen se ve por los costados y por detrás, con un velo
oscuro encima. Si tiene una figura grande en el centro, no se va a ver.

- **Formato vertical, 1080 × 1920.** Se recorta a lo ancho en pantallas
  anchas, así que lo importante va en la franja central.
- **Oscura y de poco contraste.** Es el fondo de una escena de noche.
- **Sin texto de ningún tipo.**
- **Los bordes de arriba y de abajo, casi negros**, para que el
  encabezado ("Alma · 11 de septiembre") y los botones se lean encima.

## El prompt

> Vertical 9:16 illustration of a still bayou pond at night, seen from
> slightly above. Dark jade and deep teal water with soft golden
> reflections. Large lily pads scattered across the surface, a few white
> water lilies half open. Tall reeds and hanging spanish moss framing the
> left and right edges only, leaving the centre open and calm. Warm golden
> fireflies floating over the water as small soft points of light. Painted
> in delicate watercolour with visible paper grain, muted and low
> contrast, cinematic and quiet. The top and bottom of the image fade to
> near black. No text, no characters, no people, no frogs.

**Variante más cálida** (si el jade queda muy frío al lado del pistacho de
Alma): cambiar `dark jade and deep teal` por `dark moss green and warm
olive`, y `golden` por `amber`.

## ⚠️ Dos cuidados

1. **Nada de Tiana ni del sapo de la película.** El ambiente —los
   nenúfares, las luciérnagas, el pantano, el verde y el dorado— dice
   "Princesa y el Sapo" sin usar un personaje que es de Disney. Esto es
   material por el que se cobra, y en `demo-enredados` ya nos pasó que un
   PNG "suelto" traía la firma de otro autor.
2. **Revisá las esquinas antes de subirla.** Los generadores meten marcas
   de agua abajo a la derecha, y acá esa esquina se ve.

## Cómo se prueba antes de dársela a la clienta

Abrir `/libro?evento=almamia15` y mirar que:
- el nombre de arriba y la fecha se sigan leyendo sobre la imagen;
- el papel crema no se pierda contra el fondo;
- en un celular real, no aparezca una franja clara justo detrás de los
  botones de abajo.
