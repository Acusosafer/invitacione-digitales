# -*- coding: utf-8 -*-
"""
LA INVITACIÓN DE GUILLERMINA & SEBASTIÁN — armado completo.

⚠️⚠️ SE CAYERON LOS TRES ACTOS. El 04/09/2026 Guillermina escribió:
"frases no vamos a poner, y de nuestra historia no queremos fotos ni nada
de eso. Que tenga la info importante y ya."

O sea que se van: el relato de la portada, el "mensaje del corazón"
entero, el hashtag y toda prosa que no sea un dato. Lo que queda es una
invitación de INFORMACIÓN — y la emoción la cargan las acuarelas y el
movimiento, no el texto. Es una decisión de ella y se respeta.

Lo único narrativo que sobrevive es "PRÓXIMO DESTINO" en la etiqueta, y
sobrevive porque no es una frase: es lo que dice una etiqueta de valija.

⚠️ Autocontenida: `Boda Guillermina/` está en .vercelignore, así que las
imágenes van embebidas. Se regenera con este script; los cambios a mano
se pisan.
"""
import io, base64
from PIL import Image

BASE = r"c:/Users/F&F/.gemini/antigravity/scratch/Web invitación"
W = f"{BASE}/Boda Guillermina/web"

def blanquear(im):
    """El papel de la acuarela al blanco puro.

    ⚠️ Sin esto se ve un RECTÁNGULO alrededor de cada motivo. `multiply`
    funde el fondo sólo si ese fondo es blanco: el crema de estas
    ilustraciones es más oscuro que nuestro papel, así que multiplicado
    da una mancha más oscura con forma de caja. Se escala cada canal
    para que el color del borde caiga en 255 y el dibujo se conserva."""
    import numpy as np
    a = np.asarray(im, np.float32)
    marco = np.concatenate([a[:5].reshape(-1,3), a[-5:].reshape(-1,3),
                            a[:,:5].reshape(-1,3), a[:,-5:].reshape(-1,3)])
    bg = np.median(marco, axis=0)
    if bg.min() < 120:            # fondo oscuro: no es una ilustración suelta
        return im, None
    a = np.clip(a * (255.0 / np.maximum(bg, 1)), 0, 255)
    nueva = Image.fromarray(a.astype('uint8'))
    b2 = np.asarray(nueva, np.float32)
    m2 = np.concatenate([b2[:5].reshape(-1,3), b2[-5:].reshape(-1,3),
                         b2[:,:5].reshape(-1,3), b2[:,-5:].reshape(-1,3)])
    return nueva, (bg.mean(), np.median(m2, axis=0).mean())

def recortar_al_motivo(im, aire=14):
    """Le saca el margen de papel que traen las acuarelas generadas.

    ⚠️ Vienen con muchísimo aire: el motivo ocupa un tercio de un
    rectángulo casi vacío. Puesto en la página con un ancho fijo, lo que
    se ve es un dibujito diminuto flotando en el medio de la nada — y
    peor, dos ilustraciones al lado quedan de tamaños distintos según
    cuánto papel trajo cada una.

    Se compara cada píxel contra el color de la esquina, que es el papel.
    Lo que se despega, es dibujo.

    ⚠️⚠️ EL UMBRAL ES 20, NO 12. Con 12 entraban al recorte lavados tan
    tenues que no se ven, y la caja quedaba enorme: las alianzas medían
    894px de ancho cuando la tinta de verdad terminaba a los 481. Ese
    papel fantasma a la derecha era lo que hacía ver los anillos corridos
    a la izquierda — y como el CSS estaba perfecto, uno va a mirar el
    lugar equivocado. Medido en las ocho ilustraciones: de 12 a 20 la
    torre de copas pasa de 1130 a 499 de ancho."""
    from PIL import ImageChops
    fondo = Image.new('RGB', im.size, im.getpixel((2, 2)))
    caja = ImageChops.difference(im, fondo).convert('L').point(lambda v: 255 if v > 20 else 0).getbbox()
    if not caja:
        return im
    x0, y0, x1, y1 = caja
    return im.crop((max(0, x0-aire), max(0, y0-aire),
                    min(im.width, x1+aire), min(im.height, y1+aire)))

def centrar_el_peso(im):
    """Corre el marco para que el PESO del dibujo quede en el medio.

    ⚠️⚠️ RECORTAR AL MOTIVO NO ES CENTRARLO. El recorte deja la caja
    pegada al dibujo, y el navegador centra esa caja — pero si adentro
    el dibujo está desbalanceado, sigue viéndose corrido. Medido: las
    alianzas tenían el peso 23,5 puntos a la izquierda (los dos anillos
    macizos de un lado, una ramita finita del otro) y el dress code 16,2
    a la derecha (el traje verde oscuro pesa mucho más que el vestido).
    A ojo se ve como "no está centrado" y uno va a mirar el CSS, que
    está perfecto.

    Se mide cuánto se despega cada columna de píxeles del papel —eso es
    la tinta— y se agrega papel del lado liviano hasta que el centro de
    masa cae en el medio.

    ⚠️ El agregado tiene tope. Sin tope, las alianzas pedían 427px de
    papel en blanco: quedaban centradas y un 32% más chicas, con más
    aire adentro de la imagen. Justo lo contrario de lo que se busca."""
    import numpy as np
    a = np.asarray(im, np.float32)
    papel = np.median(np.concatenate([a[:4].reshape(-1, 3), a[-4:].reshape(-1, 3)]), axis=0)
    tinta = np.clip(papel.mean() - a.mean(2), 0, None)
    tinta[tinta < 8] = 0
    peso = tinta.sum(0)
    if peso.sum() <= 0:
        return im, 0.0
    AN = im.width
    cx = float((peso * np.arange(AN)).sum() / peso.sum())
    p = int(round(abs(AN - 2*cx)))
    tope = int(AN * .22)
    if p > tope:
        p = tope
    if p < 3:
        return im, cx/AN
    fondo = tuple(int(v) for v in papel)
    nueva = Image.new('RGB', (AN + p, im.height), fondo)
    nueva.paste(im, (p if cx < AN/2 else 0, 0))
    return nueva, cx/AN

def jpg(nombre, ancho, q=78, limpiar=True, recortar=False, centrar=False):
    im = Image.open(f"{W}/{nombre}").convert('RGB')
    if recortar:
        antes = im.size
        im = recortar_al_motivo(im)
        print(f'    recorte {antes[0]}x{antes[1]} -> {im.width}x{im.height}')
    if centrar:
        antes = im.width
        im, viejo = centrar_el_peso(im)
        print(f'    peso {100*viejo:.1f}% -> centrado, +{im.width-antes}px de papel')
    if im.width > ancho:
        im = im.resize((ancho, round(ancho*im.height/im.width)), Image.LANCZOS)
    if limpiar:
        im, medida = blanquear(im)
        if medida: print(f'    papel {medida[0]:.0f} -> {medida[1]:.0f}')
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True, progressive=True)
    print(f'  {nombre:26} {ancho}px {len(b.getvalue())//1024:4} KB')
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

def webp(ruta, q=88):
    """⚠️ Si el archivo YA es webp, se embebe tal cual, sin recomprimir.

    La etiqueta es la portada —lo primero que ve el invitado— y se
    recuperó del HTML publicado (ver `rescatar.py`), o sea que ya pasó
    por una compresión con pérdida. Volver a comprimirla acá le agrega
    una segunda vuelta encima, gratis y para siempre: cada vez que se
    corriera el generador quedaría un poco peor que la anterior."""
    if ruta.lower().endswith('.webp'):
        d = open(ruta, 'rb').read()
        print(f'  etiqueta (tal cual)        {len(d)//1024:4} KB')
        return 'data:image/webp;base64,' + base64.b64encode(d).decode()
    im = Image.open(ruta)
    b = io.BytesIO(); im.save(b, 'WEBP', quality=q, method=6)
    print(f'  etiqueta                   {len(b.getvalue())//1024:4} KB')
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()

def bombitas(nombre):
    """Encuentra las luces naranjas de la guirnalda y arma el halo que late.

    ⚠️⚠️ LAS BOMBITAS SON PÍXELES adentro del JPEG. Se ven como siete
    elementos sueltos pero son una sola imagen: no hay forma de
    encenderlas y apagarlas por separado. Lo que sí se puede es ponerles
    un halo dibujado ENCIMA, y para eso hay que saber dónde está cada
    una.

    ⚠️ Las posiciones NO se eligen a ojo. Se buscan acá, midiendo las
    manchas naranjas saturadas del propio archivo: si algún día se
    cambia la ilustración, los halos se mudan solos en vez de quedar
    flotando al lado de las luces.

    Devuelve el viewBox y los círculos, en coordenadas de la imagen."""
    import numpy as np
    from collections import deque
    im = Image.open(f"{W}/{nombre}").convert('RGB')
    a = np.asarray(im, np.float32); H, AN = a.shape[:2]
    r, g, b = a[...,0], a[...,1], a[...,2]
    mx, mn = a.max(2), a.min(2)
    sat = np.where(mx > 0, (mx-mn)/np.maximum(mx, 1), 0)
    m = (sat > .32) & (r > 135) & (b < r*.72) & (g < r*.92) & (g > r*.30)

    visto = np.zeros_like(m); luces = []
    for y0 in range(H):
        for x0 in range(AN):
            if not m[y0, x0] or visto[y0, x0]:
                continue
            q = deque([(y0, x0)]); visto[y0, x0] = True; pts = []
            while q:
                y, x = q.popleft(); pts.append((y, x))
                for dy, dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
                    ny, nx = y+dy, x+dx
                    if 0 <= ny < H and 0 <= nx < AN and m[ny, nx] and not visto[ny, nx]:
                        visto[ny, nx] = True; q.append((ny, nx))
            # ⚠️ El piso de 150 píxeles saca las motitas naranjas sueltas
            # de la acuarela. Sin él aparecían dos "bombitas" de 10px
            # latiendo en el aire, al lado de la soga y de una hoja.
            if len(pts) < 150:
                continue
            ys = np.array([p[0] for p in pts]); xs = np.array([p[1] for p in pts])
            luces.append((xs.mean(), ys.mean(), max(np.ptp(xs), np.ptp(ys))/2 + 1))
    luces.sort()

    # Cada una con su propio ritmo y su propio arranque: en unísono no
    # parecen luces, parecen un cartel de neón.
    ritmos = [(2.6, 0), (3.4, .7), (2.9, 1.5), (3.8, .3), (3.1, 1.1),
              (2.7, 1.9), (3.5, .9)]
    c = []
    for i, (x, y, rad) in enumerate(luces):
        dur, esp = ritmos[i % len(ritmos)]
        c.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad*2.1:.0f}" '
                 f'fill="url(#halo)" style="--dur:{dur}s;--esp:{esp}s"/>')
    print(f'  {nombre:26} {len(luces)} bombitas')
    return (f'0 0 {AN} {H}',
            '<defs><radialGradient id="halo">'
            '<stop offset="0%" stop-color="#FFC46B" stop-opacity=".95"/>'
            '<stop offset="45%" stop-color="#E07A1F" stop-opacity=".45"/>'
            '<stop offset="100%" stop-color="#E07A1F" stop-opacity="0"/>'
            '</radialGradient></defs>' + ''.join(c))

# Los dos dibujos de línea, trazados de una foto y de la acuarela.
# ⚠️ Vienen con class="t" del generador; acá la clase es .trazo.
def trazos(clave):
    d = io.open(f'svg-{clave}.txt', encoding='utf-8').read().split(chr(10), 1)
    n = d[1].count('<path')
    print(f'  {clave:26} {n:4} trazos {len(d[1])//1024:3} KB')
    return d[0], d[1].replace('class="t"', 'class="trazo"')

# El audio va como archivo aparte, NO embebido: `preload="none"` sólo
# funciona si el navegador puede decidir no bajarlo, y un data URI ya
# está adentro del HTML. Son 539 KB que nadie paga hasta tocar.
print('imágenes:')
IM = {
  'etiqueta': webp('etiqueta-lista.webp'),
  'ellos':    jpg('ellos-tono.jpg', 720, 80, limpiar=False),
  'altar':    jpg('gemini-generated-image-fp6fmkfp6fmkfp6f.jpg', 700),
  'mapa':     jpg('mapa.jpg', 780, 76, limpiar=False),
  'luces':    jpg('guirnalda-de-luces.jpg', 620),
  'vela':     jpg('vela.jpg', 300),
  'pareja':   jpg('ellos-acuarela.jpg', 720, 80),
  'naranjas': jpg('medias-naranja.jpg', 420),
  'aperol':   jpg('aperol.jpg', 240),
  # ⚠️ La torre de copas REEMPLAZA a `copas-brindis.jpg`, que era un plato,
  # una servilleta y dos copas de vino sobre un mantel: una cena sentada
  # con lugares asignados, justo la fiesta que NO van a hacer. Lo marcó
  # Guillermina — es fingerfood, bandejeo y livings.
  'copas':    jpg('torre-copas.jpg', 560, recortar=True, centrar=True),
  # Las cinco de setiembre. Todas con `recortar`: vienen con el motivo
  # chiquito en el medio de un rectángulo casi vacío.
  'alianzas': jpg('alianzas.jpg', 620, recortar=True, centrar=True),
  'mascara':  jpg('mascara.jpg', 460, recortar=True),
  'dresscode':jpg('dresscode.jpg', 620, recortar=True, centrar=True),
  'eiffel':   jpg('eiffel.jpg', 300, recortar=True),
  'coliseo':  jpg('coliseo.jpg', 380, recortar=True),
  'violin':   jpg('violin.jpg', 300, recortar=True),
  'piano':    jpg('piano.jpg', 340, recortar=True),
}
VB_ESC, T_ESC = trazos('escena')
VB_CAR, T_CAR = trazos('cartel')
VB_LUZ, T_LUZ = bombitas('guirnalda-de-luces.jpg')

HTML = r'''<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>Guillermina &amp; Sebasti&aacute;n &middot; 3 de abril de 2027</title>

<!-- ══════════════════════════════════════════════════════════════════
     ⚠️ NO ES LA ESTRUCTURA DE TRES ACTOS. Ella pidió el 04/09/2026:
     "frases no vamos a poner, y de nuestra historia no queremos fotos
     ni nada de eso. Que tenga la info importante y ya."
     Se fue el relato, se fue el mensaje del corazón, se fue el hashtag.
     La emoción la cargan las acuarelas y el movimiento.

     ⚠️ Se regenera con `herramientas/invita.py`. A mano se pisa.
     ══════════════════════════════════════════════════════════════════ -->

<!-- ⚠️ Estas cuatro etiquetas las REESCRIBE `api/i.js` del lado del
     servidor, buscándolas POR SU id, para que el link que llega por
     WhatsApp muestre el nombre del invitado y la foto. No se borran ni
     se les cambia el id: sin ellas la vista previa sale con el nombre
     del dominio pelado. -->
<meta id="og-title" property="og:title" content="Guillermina &amp; Sebasti&aacute;n">
<meta id="og-desc" property="og:description" content="3 de abril de 2027 &middot; Finca La Josefina, Berisso">
<meta id="og-img" property="og:image" content="">
<meta id="og-url" property="og:url" content="">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Parisienne&family=Marcellus&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">

<style>
:root{
  --naranja:#E07A1F; --hondo:#A0451A; --terracota:#A84F2A;
  --oliva:#435F3A; --avena:#D7C3A1;
  --papel:#F6F2E8; --papel-hondo:#EFE8D8; --tinta:#3A302A; --tinta-2:#6B5D51;
  --ease:cubic-bezier(.22,.61,.36,1);
}
*{box-sizing:border-box;margin:0}
html{scroll-behavior:smooth}
html,body{height:100%}
body{background:var(--papel); color:var(--tinta); overflow-x:hidden;
  font-family:'Jost',system-ui,sans-serif; font-size:17px; line-height:1.7;
  overflow-y:hidden}
body.adentro{overflow-y:auto}

/* El papel de algodón: fibra fina + nube grande, las dos en multiply. */
.fibra,.nube{position:fixed;inset:0;pointer-events:none;z-index:9;mix-blend-mode:multiply}
.fibra{opacity:.55;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='f'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.92' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23f)' opacity='.4'/%3E%3C/svg%3E")}
.nube{opacity:.3;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='420' height='420'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.012' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='420' height='420' filter='url(%23n)' opacity='.5'/%3E%3C/svg%3E")}

h1,h2{font-family:'Marcellus',Georgia,serif;font-weight:400;line-height:1.18;
  letter-spacing:.01em;text-wrap:balance}
.mano{font-family:'Parisienne',cursive;color:var(--terracota)}
.wrap{width:100%;max-width:620px;margin:0 auto;padding:0 28px}

/* Las acuarelas vienen sobre papel crema: multiply funde ese papel.
   ⚠️ Ningún ancestro con z-index, transform ni perspective, o el
   multiply se mezcla contra ese contexto y vuelve el rectángulo blanco. */
.acuarela{width:100%;height:auto;display:block;mix-blend-mode:multiply}
.motivo{margin:0 auto;mix-blend-mode:multiply;display:block}
/* ══════════ PROFUNDIDAD ══════════
   Tres cosas que hacen que una invitación ilustrada no se lea plana, y
   que no teníamos:

   1 · ACUARELAS DE BORDE A BORDE. Una ilustración con aire a los cuatro
       lados es una foto pegada en una hoja. La misma tocando los bordes
       ES la hoja, y el texto queda apoyado sobre ella.
   2 · MOTIVOS ANCLADOS AL MARGEN, entrando desde afuera. Un elemento
       cortado por el borde obliga a imaginar lo que sigue: eso es
       profundidad, y es gratis.
   3 · UNA BANDA DE COLOR detrás de una sección. Rompe la monotonía de
       un solo papel de punta a punta.
   ⚠️ Las tres, con medida: la referencia que mandó Fer usa las tres y
   además se le va la mano. Acá van una vez cada una. */
/* ⚠️ NO se hace con `width:100vw` + márgenes negativos: 100vw incluye
   la barra de scroll y en cualquier navegador que la dibuje encima del
   contenido la página se va 28px a la derecha. Se hace por estructura:
   estos bloques viven FUERA de `.wrap`, como hijos directos de la
   sección, que no tiene padding lateral. Medido: 390 de ancho, 390 de
   documento. */
.sangra{width:100%;max-width:none;margin-left:0;margin-right:0}
.sangra img{border-radius:0}

.banda{position:relative;background:var(--papel-hondo)}
.banda::before,.banda::after{content:'';position:absolute;left:0;right:0;
  height:34px;pointer-events:none}
.banda::before{top:-33px;background:linear-gradient(to bottom,transparent,var(--papel-hondo))}
.banda::after{bottom:-33px;background:linear-gradient(to top,transparent,var(--papel-hondo))}

/* ⚠️ Acá había un motivo anclado al margen, entrando desde afuera. Se
   sacó: colgado solo en medio del papel no daba profundidad, se veía
   olvidado. El truco funciona cuando el elemento ESTÁ CORTADO por el
   borde de la pantalla —la referencia lo hace con una pared de flores
   entera—, no con un dibujito chico flotando lejos del texto. De las
   tres cosas que dan profundidad quedan las otras dos: las acuarelas
   de borde a borde y la banda de color. */

/* Los separadores: los motivos sueltos, chiquitos, entre sección y
   sección. Es para lo que se dibujaron. */
.sep{width:74px;margin:0 auto;display:block;mix-blend-mode:multiply;opacity:.9}

/* ══════════ EL DIBUJO QUE SE PINTA SOLO ══════════
   El papel arranca en blanco, la línea se dibuja, y cuando termina la
   acuarela aparece por debajo mientras el trazo se apaga.
   ⚠️ NO va el trazo ENCIMA de la acuarela terminada: la acuarela ya es
   rica y doscientas líneas arriba se leen como un garabato. Y el
   trazado salió de la acuarela vieja, así que el contorno del pelo no
   coincide — en esta forma nunca conviven y no se nota. */
.escena{position:relative}
.escena .acuarela{opacity:0;transition:opacity 1.5s var(--ease)}
.escena.pintada .acuarela{opacity:1}
.escena svg{position:absolute;inset:0;width:100%;height:100%}
.escena.pintada svg{opacity:0;transition:opacity 1.7s var(--ease) .5s}
.trazo{fill:none;stroke:var(--terracota);stroke-width:1.1;
  stroke-linecap:round;stroke-linejoin:round}
.trazo.fino{stroke-width:.9}
.trazo.hoja{stroke:var(--oliva)}
.trazo.suave{stroke:#C08A5E}
/* Un dibujo suelto (el cartel, la copa): sin acuarela abajo, queda la línea. */
.dibujo{margin:0 auto;display:block}
/* Los hielos no se dibujan: CAEN adentro del vaso cuando la copa
   terminó. Un rebote corto — eso es lo que hace que se sienta un peso
   cayendo y no una caja deslizándose. */
.cae{opacity:0;transform:translateY(-34px) rotate(-14deg);
  transform-box:fill-box;transform-origin:center}
.cae.cayendo{opacity:1;transform:none;
  transition:transform .72s cubic-bezier(.34,1.42,.64,1) var(--retraso,0s),
             opacity .18s ease var(--retraso,0s)}

/* ══════════ LA PORTADA — la etiqueta ══════════
   ⚠️ La imagen va anclada ARRIBA DE TODO: su corte de soga queda fuera
   de la pantalla y la soga entra desde afuera. Nada de dibujarle una
   soga con CSS — el empalme se ve siempre. */
.portada{position:fixed;inset:0;z-index:8;background:var(--papel);
  transition:opacity 600ms linear}
.portada.ida{opacity:0;pointer-events:none}
.colgante{position:absolute;left:50%;top:-42px;width:246px;margin-left:-123px;
  transform-origin:50% 0;animation:mecer 5.4s ease-in-out infinite}
/* ⚠ El giro es chico en grados pero la etiqueta cuelga de arriba: a
   2,6° la punta de abajo se corre ~17px. A 1° se corría 6 y no se veía
   colgar de nada. */
@keyframes mecer{0%,100%{transform:rotate(-2.6deg)}50%{transform:rotate(2.6deg)}}
/* ⚠️ Sube ENTERA, sin tocarle la opacidad: apagándola a la vez que el
   papel, el viaje no se ve nunca. Y arranca con una caidita, porque una
   soga de verdad cede un instante antes de levantar. */
.colgante.sube{animation:levantar 1150ms cubic-bezier(.5,0,.75,.35) forwards}
@keyframes levantar{
  0%{transform:translateY(0) rotate(0)}
  9%{transform:translateY(11px) rotate(.6deg)}
  100%{transform:translateY(-155%) rotate(-2.5deg)}}
@media (max-height:760px){
  .colgante{width:210px;margin-left:-105px;top:-34px}
  .n1,.n2{font-size:23px} .amp{font-size:18px}}

.etiqueta{position:relative;width:100%;perspective:1000px;cursor:pointer}
.cara{position:relative;transition:transform 900ms var(--ease);transform-style:preserve-3d}
.volteada .cara{transform:rotateY(180deg)}
.etiqueta img{width:100%;display:block}
/* El rectángulo interior, MEDIDO sobre la acuarela. */
.escrito{position:absolute;left:11.9%;right:11.7%;top:25.6%;bottom:14.8%;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  padding:10px 6px;text-align:center;backface-visibility:hidden}
.dorso{transform:rotateY(180deg)}
.nom{font-family:'Parisienne',cursive;color:var(--terracota);line-height:.98}
.n1,.n2{font-size:26px}
.amp{font-size:20px;opacity:.85}
.dat{font-family:'Marcellus',serif;color:var(--tinta);text-transform:uppercase;
  letter-spacing:.16em;font-size:9.5px;line-height:2.1}
.dat .g{font-size:13px;letter-spacing:.1em;display:block;margin:6px 0}
.pie{position:absolute;left:0;right:0;bottom:calc(52px + env(safe-area-inset-bottom));
  text-align:center;transition:opacity 500ms linear}
.pie.ida{opacity:0}
.pie .rot{font-family:'Marcellus',serif;font-size:9.5px;letter-spacing:.34em;
  text-transform:uppercase;color:var(--tinta-2)}
.pie .toca{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--hondo);margin-top:9px;opacity:.75}
.pie .toca.avisa{animation:latir 1.5s ease-in-out 2}
@keyframes latir{50%{opacity:.28}}

/* ══════════ PÉTALOS ══════════
   No son adorno: son los que les van a tirar después de la ceremonia.
   Por eso caen en la portada y otra vez al terminar la ceremonia, y en
   ningún otro lado. */
.petalos{position:absolute;inset:0;pointer-events:none;overflow:hidden}
.p{position:absolute;top:-10%;animation:caer linear infinite}
/* ⚠⚠ El 110% de un translate se mide contra EL PROPIO PÉTALO, no contra
   la pantalla: un pétalo de 13px caía 14px y se apagaba ahí arriba. La
   caída entera va en --caida, que cada contenedor fija según su alto.
   Y el camino zigzaguea: una hoja que cae no baja en línea recta. */
@keyframes caer{0%{transform:translate3d(0,-40px,0) rotate(0);opacity:0}
  12%{opacity:.8}
  33%{transform:translate3d(calc(var(--dx) * -.6),calc(var(--caida) * .32),0)
      rotate(calc(var(--giro) * .3))}
  66%{transform:translate3d(calc(var(--dx) * .85),calc(var(--caida) * .66),0)
      rotate(calc(var(--giro) * .68))}
  85%{opacity:.65}
  100%{transform:translate3d(var(--dx),var(--caida),0) rotate(var(--giro));opacity:0}}

/* ══════════ SECCIONES ══════════ */
.acto{padding:58px 0;text-align:center}
.acto.junto{padding-top:0}
/* ⚠ La primera sección arranca PEGADA al borde de arriba: los 86px de
   papel en blanco entre la etiqueta que sube y la acuarela rompían la
   entrada. La acuarela es la portada, y una portada no tiene margen. */
#arriba{padding-top:0}
/* ⚠ Y va de borde a borde de verdad. `.acto .acuarela` la limitaba a
   520px, así que arriba de esa medida quedaba una estampita centrada
   mientras el trazo de encima (que sí abarcaba la sección entera) se
   dibujaba corrido. La acuarela mide 720px: en un monitor grande se
   agranda y se ablanda un poco, que es el precio de que llegue al borde. */
#esc-ellos .acuarela{max-width:none;margin:0}
.rot{font-family:'Marcellus',serif;font-size:.66rem;letter-spacing:.32em;
  text-transform:uppercase;color:var(--hondo)}
.acto h2{font-size:clamp(1.7rem,6vw,2.3rem);margin-top:14px}
.acto h2 em{font-style:normal;font-family:'Parisienne',cursive;
  color:var(--terracota);font-size:1.25em;line-height:.9}
/* La rayita que se dibuja sola abajo de cada título. */
.acto h2::after{content:'';display:block;width:44px;height:1px;margin:22px auto 0;
  background:var(--terracota);transform:scaleX(0);transform-origin:center;
  transition:transform 1.1s var(--ease) 200ms}
.acto.on h2::after{transform:scaleX(1)}
/* El contador. Cuatro casillas: días, horas, minutos, segundos.
   ⚠️ `tabular-nums` no es un detalle: sin eso, el 1 es más angosto que
   el 8 y los números bailan de izquierda a derecha cada segundo. */
.cuenta{margin-top:34px;display:flex;justify-content:center;align-items:flex-start;
  gap:4px}
.cuenta .c{display:flex;flex-direction:column;align-items:center;gap:3px;
  min-width:62px}
.cuenta .n{font-family:'Marcellus',serif;font-size:2.1rem;line-height:1;
  color:var(--hondo);font-variant-numeric:tabular-nums}
.cuenta .t{font-family:'Marcellus',serif;font-size:.54rem;letter-spacing:.24em;
  text-transform:uppercase;color:var(--tinta-2)}
.cuenta .dp{font-family:'Marcellus',serif;font-size:1.5rem;line-height:1.35;
  color:var(--terracota);opacity:.45}
@media (max-width:359px){ .cuenta .c{min-width:52px} .cuenta .n{font-size:1.8rem} }

.dato{margin-top:26px}
.dato .hora{font-family:'Marcellus',serif;font-size:2.4rem;color:var(--hondo);line-height:1}
.dato .donde{margin-top:8px;font-size:.95rem;color:var(--tinta-2)}

/* ══════════ EL HORARIO, FLANQUEADO ══════════
   Un dibujo de cada lado de la hora, con la hora en el medio: el violín
   y el piano en la ceremonia, la copita de Aperol y la máscara en la
   fiesta. Lo pidió Fer, y tiene un motivo de composición: apilados
   debajo empujaban las alianzas fuera del centro de la sección.

   ⚠️ SE EMPAREJAN POR ALTO, NO POR ANCHO. La máscara es apaisada y la
   copita es alta y flaca: al mismo ancho, la copa queda del doble de
   alto que la máscara y el renglón se ve desbalanceado. Igual la
   máscara lleva su propio tope de ancho, porque aun a la misma altura
   ocupa mucho más renglón.

   ⚠️ La línea de abajo ("Con violín y piano en vivo") NO entra en el
   renglón: a 390px quedan ~110px libres entre los dos dibujos y ahí
   sólo cabe la hora. Va debajo, a todo el ancho. */
.flanco{display:flex;align-items:center;justify-content:center;gap:16px}
.flanco .hora{flex:0 0 auto}
.flanco .ala{height:86px;width:auto;max-width:104px;object-fit:contain;
  flex:0 0 auto;mix-blend-mode:multiply}
/* La máscara: más chica que su par, a pedido de Fer. Aun emparejada por
   alto, un antifaz ocupa mucho más renglón que una copa. */
.flanco .ala.angosta{height:72px;max-width:104px}

/* ══════════ LA GUIRNALDA QUE TITILA ══════════
   ⚠️⚠️ LAS BOMBITAS SON PÍXELES adentro del JPEG: no se pueden encender
   y apagar por separado por más que se vean como siete elementos
   sueltos. Lo que sí se puede es ponerles ENCIMA un halo dibujado que
   late. Las posiciones no se eligen a ojo: las busca `bombitas()` en el
   propio archivo, midiendo las manchas naranjas saturadas. Si algún día
   se cambia la ilustración, los halos se mudan solos.

   ⚠️ El contenedor va `position:relative` SIN z-index: un z-index abre
   un stacking context y el `multiply` de la acuarela se mezclaría
   contra ese contexto —que es transparente— en vez de contra el papel,
   y la guirnalda volvería a quedar recortada en un rectángulo blanco.
   El SVG queda arriba igual, porque va después en el DOM. */
.luces{position:relative;max-width:400px;margin:14px auto 0}
.luces img{width:100%;display:block;mix-blend-mode:multiply}
.luces svg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.luces circle{animation:destello var(--dur,3s) var(--esp,0s) ease-in-out infinite}
@keyframes destello{0%,100%{opacity:.12}45%{opacity:.85}}
.acto .acuarela{max-width:520px;margin:0 auto 18px}
.acto .motivo{margin-bottom:16px}

.btn{display:inline-block;margin-top:26px;text-decoration:none;
  font-family:'Marcellus',serif;font-size:.72rem;letter-spacing:.22em;
  text-transform:uppercase;padding:15px 32px;border-radius:999px;
  border:1px solid var(--hondo);color:var(--hondo);background:transparent;
  cursor:pointer;transition:transform .16s var(--ease),background .25s,color .25s}
.btn:active{transform:scale(.97)}
.btn.lleno{background:var(--hondo);color:var(--papel);border-color:var(--hondo)}

.alias{display:inline-flex;align-items:center;gap:14px;margin-top:22px;
  padding:14px 20px;border:1px dashed rgba(160,69,26,.45);border-radius:8px;
  font-family:'Marcellus',serif;letter-spacing:.1em;color:var(--tinta)}
.alias button{font-family:'Jost',sans-serif;font-size:.7rem;letter-spacing:.14em;
  text-transform:uppercase;border:0;background:var(--hondo);color:var(--papel);
  padding:10px 15px;border-radius:999px;cursor:pointer;min-height:38px;
  transition:transform .16s var(--ease)}
.alias button:active{transform:scale(.95)}

/* Los dos monumentos de la luna de miel, uno al lado del otro y del
   mismo alto. ⚠️ El alto se fija acá y no el ancho: son dos dibujos de
   proporciones distintas, y emparejarlos por ancho deja al Coliseo del
   doble de alto que la torre. */
.duo{display:flex;justify-content:center;align-items:flex-end;gap:26px;margin:22px auto 0}
.duo img{height:104px;width:auto;mix-blend-mode:multiply}
.duo.chico{gap:18px;margin-top:18px}
.duo.chico img{height:74px}

/* ══════════════════════════════════════════════════════════════════
   EL FORMULARIO PARA CONFIRMAR

   ⚠️ NO HAY MESAS EN ESTA FIESTA. Es bandejeo y livings, la gente se
   sienta donde quiere. Así que acá no se pide mesa, no se muestra
   mesa y no se guarda mesa — el panel la deja vacía y listo.

   ⚠️ EL APELLIDO SÍ, Y ES OBLIGATORIO. Aunque no haya que armar
   mesas, el listado que se le entrega al salón se ordena por
   apellido y el catering cobra por persona: una fila "Juan" suelta
   no le sirve a nadie. `rsvp_enviar` no lo exige —descarta la fila
   sólo si falta el nombre—, así que la única defensa es esta
   validación. Si se afloja, entran filas a medias sin aviso.
   ══════════════════════════════════════════════════════════════════ */
.form{max-width:440px;margin:30px auto 0;text-align:left}
.campo{margin-top:18px}
.campo label{display:block;font-family:'Marcellus',serif;font-size:.64rem;
  letter-spacing:.24em;text-transform:uppercase;color:var(--tinta-2);margin-bottom:7px}
.campo input,.campo textarea{width:100%;font-family:'Jost',sans-serif;font-size:1rem;
  color:var(--tinta);background:rgba(255,255,255,.5);
  border:0;border-bottom:1px solid rgba(160,69,26,.35);
  padding:11px 4px;min-height:46px;transition:border-color .2s,background .2s}
.campo textarea{border:1px solid rgba(160,69,26,.28);border-radius:8px;
  resize:vertical;min-height:80px;padding:11px 12px}
.campo input:focus,.campo textarea:focus{outline:none;border-color:var(--hondo);
  background:rgba(255,255,255,.85)}
.campo input::placeholder,.campo textarea::placeholder{color:rgba(107,93,81,.55)}
.dos{display:flex;gap:14px}
.dos .campo{flex:1;min-width:0}

/* Los chips de sí/no y de dieta. ⚠️ 46px de alto: se tocan con el dedo. */
.chips{display:flex;flex-wrap:wrap;gap:9px}
.chip{font-family:'Jost',sans-serif;font-size:.86rem;color:var(--tinta);
  background:transparent;border:1px solid rgba(160,69,26,.35);border-radius:999px;
  padding:11px 18px;min-height:46px;cursor:pointer;
  transition:background .2s,color .2s,border-color .2s,transform .16s var(--ease)}
.chip:active{transform:scale(.96)}
/* ⚠️ El elegido va con el fondo HONDO y el texto en papel: es la única
   combinación que da contraste de sobra sobre el crema. Un chip elegido
   pintado sólo con el borde no se distingue del que no lo está. */
.chip.si{background:var(--hondo);color:var(--papel);border-color:var(--hondo)}

/* Cada acompañante, en su propia tarjeta.
   ⚠️⚠️ LAS TARJETAS SIGUEN A LA VISTA AUNQUE EL TITULAR DIGA QUE NO VA.
   Un link cubre a todo un grupo y cada uno contesta por su cuenta: el
   que recibió la invitación no decide por su pareja ni por sus hijos.
   Esconderlas hacía desaparecer los cupos de los demás, porque
   `rsvp_enviar` ya borró la pre-alta y esas filas no volvían ni como
   "no" ni como "pendiente". Le pasó a cuatro grupos en una fiesta. */
.acomp{margin-top:20px;padding:18px;border:1px solid rgba(160,69,26,.22);
  border-radius:12px;background:rgba(255,255,255,.38)}
.acomp .quien{font-family:'Marcellus',serif;font-size:.68rem;letter-spacing:.22em;
  text-transform:uppercase;color:var(--hondo)}
.aviso{margin-top:14px;font-size:.9rem;color:var(--tinta-2)}
/* El cartel de "ya confirmaste" y el de "listo". */
.cerrado{margin:30px auto 0;max-width:440px;padding:26px 22px;text-align:center;
  border:1px dashed rgba(160,69,26,.45);border-radius:12px;
  font-family:'Marcellus',serif;color:var(--tinta);line-height:1.6}
/* El mensaje flotante de error. ⚠️ Va arriba de todo: abajo lo tapa el
   teclado del celular justo cuando hace falta leerlo. */
.globo{position:fixed;left:50%;top:calc(14px + env(safe-area-inset-top));
  transform:translate(-50%,-140%);z-index:60;max-width:min(92vw,420px);
  background:var(--hondo);color:var(--papel);padding:13px 20px;border-radius:10px;
  font-size:.92rem;line-height:1.45;text-align:center;box-shadow:0 8px 26px rgba(58,48,42,.22);
  transition:transform .3s var(--ease)}
.globo.on{transform:translate(-50%,0)}

/* El mapa: la acuarela en planta, y el recorrido animado encima. */
.mapa{position:relative;margin:26px auto 0;max-width:560px}
.mapa img{width:100%;display:block;mix-blend-mode:multiply}
.capa{position:absolute;inset:0;width:100%;height:100%}
.ruta{fill:none;stroke:var(--hondo);stroke-width:3;stroke-linecap:round;
  stroke-dasharray:2 11;opacity:0;transition:opacity 1.2s var(--ease)}
.mapa.on .ruta{opacity:.9}
.punta{fill:none;stroke:var(--hondo);stroke-width:3;stroke-linecap:round;stroke-linejoin:round}

/* La música: un botón chiquito y fijo, no un cartel. */
.musica{position:fixed;right:16px;bottom:calc(16px + env(safe-area-inset-bottom));
  z-index:10;width:44px;height:44px;border-radius:50%;border:1px solid rgba(160,69,26,.35);
  background:rgba(246,242,232,.92);color:var(--hondo);cursor:pointer;
  display:none;align-items:center;justify-content:center;
  transition:transform .16s var(--ease)}
body.adentro.con-musica .musica{display:flex}
.musica:active{transform:scale(.94)}
.musica .barra{display:inline-block;width:2px;margin:0 1px;background:currentColor;
  border-radius:2px;height:9px;transform-origin:50% 100%}
.musica.sonando .barra{animation:eq .9s ease-in-out infinite}
.musica .barra:nth-child(2){animation-delay:.15s}
.musica .barra:nth-child(3){animation-delay:.3s}
@keyframes eq{50%{transform:scaleY(2)}}

.rev{opacity:0;transform:translateY(18px);
  transition:opacity 1.1s var(--ease),transform 1.1s var(--ease)}
.rev.on{opacity:1;transform:none}

footer{padding:56px 0 70px;text-align:center;font-size:.78rem;
  color:var(--tinta-2);letter-spacing:.04em}
footer a{color:var(--hondo);text-decoration:none}

@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .rev{opacity:1;transform:none;transition:none}
  .p{display:none}
  .trazo{stroke-dashoffset:0 !important;transition:none !important}
  .escena .acuarela{opacity:1}
  .escena svg{display:none}
  .cae{opacity:1 !important;transform:none !important}
  .acto h2::after{transform:scaleX(1);transition:none}
  .ruta{opacity:.9 !important}
  /* Las bombitas dejan de titilar y se quedan prendidas: apagarlas del
     todo dejaría la guirnalda más pálida que la ilustración original. */
  .luces circle{animation:none;opacity:.5}
}
</style>
</head>
<body>
<div class="fibra" aria-hidden="true"></div><div class="nube" aria-hidden="true"></div>

<!-- ══════════ LA PORTADA ══════════ -->
<div class="portada" id="portada">
  <div class="petalos" id="petalos-portada" aria-hidden="true"></div>
  <div class="colgante" id="colgante">
    <div class="etiqueta" id="eti" role="button" tabindex="0" aria-label="Abrir la invitación">
      <div class="cara">
        <img src="__ETIQUETA__" alt="">
        <div class="escrito">
          <div class="nom n1">Guillermina</div>
          <div class="nom amp">&amp;</div>
          <div class="nom n2">Sebasti&aacute;n</div>
        </div>
        <div class="escrito dorso">
          <div class="dat">S&aacute;bado<span class="g">03 &middot; IV &middot; 2027</span>
            Finca<br>La Josefina<br>Berisso</div>
        </div>
      </div>
    </div>
  </div>
  <div class="pie" id="pie">
    <div class="rot">Pr&oacute;ximo destino</div>
    <div class="toca" id="toca">Toc&aacute; la etiqueta</div>
  </div>
</div>

<!-- ══════════ 1 · ELLOS ══════════
     Sin relato: la acuarela, los nombres y la fecha. Nada más. -->
<section class="acto" id="arriba">
  <!-- De borde a borde: fuera de `.wrap`, que es quien pone el margen. -->
  <div class="escena rev sangra" id="esc-ellos">
    <img class="acuarela" src="__ELLOS__"
         alt="Guillermina y Sebasti&aacute;n de espaldas frente al lago, al atardecer">
    <svg viewBox="__VB_ESC__" aria-hidden="true">__T_ESC__</svg>
  </div>
  <div class="wrap">
    <h2 class="rev" style="margin-top:26px"><em>Guillermina y Sebasti&aacute;n</em></h2>

    <!-- El contador va PEGADO a los nombres, a pedido de Fer. Es lo
         primero que se mira en una invitación que llega con un año de
         anticipación: cuánto falta. -->
    <div class="cuenta rev" id="cuenta" hidden>
      <div class="c"><span class="n" id="cd">—</span><span class="t">d&iacute;as</span></div>
      <span class="dp">:</span>
      <div class="c"><span class="n" id="ch">—</span><span class="t">horas</span></div>
      <span class="dp">:</span>
      <div class="c"><span class="n" id="cm">—</span><span class="t">min</span></div>
      <span class="dp">:</span>
      <div class="c"><span class="n" id="cs">—</span><span class="t">seg</span></div>
    </div>

    <p class="rot rev" style="margin-top:36px">S&aacute;bado 3 de abril de 2027</p>

    <!-- ⚠ EL CARTEL ES EL ÚNICO LUGAR DEL CUERPO DONDE SE NOMBRA LA
         FINCA. Estaba escrita cuatro veces —abajo de la fecha, en el
         cartel, en la ceremonia y en el dorso de la etiqueta— y le
         quitaba peso justo al cartel, que es el que la dice dibujada.
         Queda acá y en el dorso de la etiqueta, que es una etiqueta de
         valija: ahí el destino corresponde.
         ⚠ El bucle se apaga cuando el cartel sale de la pantalla: si no
         sigue redibujándose para nadie, gastando batería. -->
    <!-- ⚠️ 330px -> 240px. Guillermina lo pidió y tiene razón: era el
         dibujo más ancho de toda la invitación, más que los nombres de
         ellos, así que el cartel de la finca le ganaba en protagonismo a
         los novios. No se achica el trazo ni se toca el dibujo: se achica
         la caja, y el SVG escala solo. -->
    <svg class="dibujo rev bucle" id="dib-cartel" viewBox="__VB_CAR__"
         style="width:100%;max-width:240px;margin-top:30px" aria-hidden="true">__T_CAR__</svg>
  </div>
</section>

<!-- ⚠️ ACÁ ESTABA LA COPITA DE APEROL, de separador entre los nombres y
     el mapa. Se movió abajo, entre la ceremonia y la fiesta: lo pidió
     Guillermina —"me encanta, me gusta para la parte de informar"— y
     tiene razón. Arriba era un adorno de 56px que separaba dos bloques;
     abajo es la bisagra entre el rato formal y el rato informal, que es
     justo lo que la copa cuenta. -->

<!-- ══════════ 2 · CÓMO LLEGAR ══════════ -->
<section class="acto junto" id="mapa-sec">
  <div class="wrap">
    <p class="rot rev">C&oacute;mo llegar</p>
    <!-- El cartel ya dice "Finca La Josefina": repetirlo abajo en el
         titulo es decir dos veces lo mismo. Ac&aacute; va el dato que falta. -->
    <h2 class="rev">Berisso, <em>Buenos Aires</em></h2>
  </div>
  <div class="mapa rev sangra" id="mapa">
      <img src="__MAPA__" alt="Mapa de la finca: la entrada, el estacionamiento, el sal&oacute;n y el altar sobre el lago">
      <svg class="capa" viewBox="0 0 1000 758" preserveAspectRatio="none" aria-hidden="true">
        <path class="ruta" d="M170 700 C240 690 300 660 360 620 C420 582 470 566 512 560
                              C548 554 560 530 552 500 C544 468 556 442 590 430
                              C630 416 660 386 672 344 C682 310 700 290 726 280"/>
        <path class="punta" d="M706 292 L728 276 L732 302"/>
      </svg>
  </div>
  <div class="wrap">
    <a class="btn rev" href="https://maps.google.com/?q=Finca+La+Josefina+Berisso"
       target="_blank" rel="noopener">Abrir en el mapa</a>
  </div>
</section>



<!-- ══════════ 3 · LA CEREMONIA ══════════
     Va DESPUÉS del mapa: el lugar ya quedó dicho por el cartel y por
     el recorrido, así que acá sólo hace falta la hora. -->
<section class="acto junto" id="ceremonia" style="position:relative;overflow:hidden">
  <!-- ⚠️ Los pétalos van ENCIMA de la sección, no en un bloque aparte:
       suelto abajo dejaba 180px de papel vacío con un pétalo perdido,
       que se lee como un error y no como un efecto. -->
  <div class="petalos" id="petalos-ceremonia" aria-hidden="true"></div>

  <!-- ⚠️ EL ALTAR VA A SANGRÍA, FUERA DE `.wrap`. Fer lo pidió más
       grande y en un celular no había otra forma: la columna de texto
       mide 334px de los 390 de pantalla, así que la acuarela ya estaba
       al 100% de lo que podía dentro del wrap y subirle el `max-width`
       no cambiaba un píxel. Sacándola del wrap gana los 56px del margen.
       ⚠️ `.acto .acuarela{max-width:520px}` le gana a `.sangra`, así que
       el tope se anula acá, en el elemento. Es el mismo problema que ya
       había dejado la acuarela de la portada como una estampita
       centrada mientras el trazo de encima abarcaba la sección entera. -->
  <img class="acuarela sangra rev" src="__ALTAR__" style="max-width:none"
       alt="El altar al borde del lago">

  <div class="wrap">
    <p class="rot rev" style="margin-top:22px">La ceremonia</p>
    <!-- ⚠️ Decía "Sobre el PICO, frente al lago". Guillermina avisó que no
         se entendía, y tiene razón: "pico" es jerga del mapa, no de una
         invitación. El invitado no tiene que descifrar nada acá.
         ⚠️ Y dice "el lago", no "el laguito": lo eligió Fer. Ella había
         dicho laguito, pero el diminutivo le baja el porte al lugar
         justo en la línea que lo presenta. -->
    <h2 class="rev">Al aire libre, <em>frente al lago</em></h2>

    <!-- ⚠️ EL VIOLÍN Y EL PIANO VAN A LOS COSTADOS DE LA HORA, uno de
         cada lado. No es capricho de composición: apilados debajo
         empujaban las alianzas fuera del centro de la sección, y las
         alianzas son las que cierran. -->
    <div class="dato rev">
      <div class="flanco">
        <img class="ala" src="__VIOLIN__" alt="">
        <p class="hora">18:00</p>
        <img class="ala" src="__PIANO__" alt="">
      </div>
      <p class="donde">Con viol&iacute;n y piano en vivo</p>
    </div>

    <!-- Las alianzas cierran la sección. ⚠️ VAN GRANDES A PROPÓSITO: el
         anillo trae grabado "03 - abr - 2027" y ese grabado mide 110px
         en una imagen de 1408. A 150px de ancho en la página es una
         manchita ilegible; a 300px se lee como lo que es. Es el único
         lugar de la invitación donde la fecha aparece escrita a mano. -->
    <img class="acuarela rev" src="__ALIANZAS__" style="max-width:290px;margin-top:12px"
         alt="Las alianzas, con la fecha grabada">
  </div>
</section>

<!-- ⚠️ ACÁ ESTUVO LA COPITA DE APEROL DE SEPARADOR, primero a 56px entre
     los nombres y el mapa, después a 104px como bisagra entre la
     ceremonia y la fiesta. Suelta en el medio del papel era "mucho"
     —palabra de Fer—: un dibujo grande, solo, sin nada que decir. Se
     mudó adentro de la fiesta, al costado del horario, donde tiene un
     trabajo. Ver el `.flanco` de abajo. -->

<!-- ══════════ 4 · LA FIESTA ══════════ -->
<section class="acto" id="fiesta">
  <div class="wrap">
    <!-- ⚠️ Acá había una copa dibujada a línea con hielos que caían.
         Se sacó a pedido de Fer: con la acuarela de las copas al lado
         eran dos copas seguidas diciendo lo mismo.
         ⚠️ Se saca ENTERA, no con `hidden`: la regla del navegador
         `[hidden]{display:none}` pierde contra `.dibujo{display:block}`
         y la copa se seguía viendo igual. -->
    <!-- ⚠️⚠️ LA MESA TENDIDA SE FUE, Y NO VUELVE. Acá había
         `copas-brindis.jpg`: un plato, una servilleta doblada y dos copas
         de vino sobre un mantel. O sea una CENA SENTADA con lugares
         asignados — justo la fiesta que NO van a hacer. Lo marcó
         Guillermina: es fingerfood, bandejeo, livings y gente parada, y
         nadie tiene mesa asignada. Una imagen que promete otra cosa es
         peor que no tener imagen.
         El archivo sigue en `web/` por si alguna vez sirve para otra
         boda, pero para ésta no se usa. -->
    <!-- Las dos que van CENTRADAS: la torre de copas y la guirnalda. -->
    <img class="acuarela rev" src="__COPAS__" style="max-width:240px"
         alt="Una torre de copas de champagne">

    <!-- ⚠️⚠️ LA GUIRNALDA TITILA, y las bombitas son PÍXELES adentro del
         JPEG: no se encienden por separado. Lo que late es un halo
         dibujado ENCIMA de cada una, y las posiciones las mide
         `bombitas()` en el propio archivo — no están escritas a mano.
         ⚠️ El contenedor va `position:relative` SIN z-index: un z-index
         abriría un stacking context y el `multiply` de la acuarela se
         mezclaría contra ese contexto en vez de contra el papel, y la
         guirnalda quedaría recortada en un rectángulo blanco. El SVG
         igual queda arriba, porque va después en el DOM. -->
    <div class="luces rev">
      <img src="__LUCES__" alt="Una guirnalda de luces c&aacute;lidas">
      <svg viewBox="__VB_LUZ__" aria-hidden="true">__T_LUZ__</svg>
    </div>

    <p class="rot rev" style="margin-top:22px">La fiesta</p>
    <h2 class="rev">En el mismo <em>lugar</em></h2>

    <!-- ⚠️ LA COPITA DE APEROL Y LA MÁSCARA, una de cada lado del
         horario, igual que el violín y el piano en la ceremonia. Las dos
         dicen lo mismo que el dato: que esto es informal, de pie y con
         copa en la mano.
         ⚠️ La máscara lleva `angosta`: emparejada por alto con la copa
         igual se come el doble de renglón, porque un antifaz es
         apaisado y una copa es alta y flaca. -->
    <div class="dato rev">
      <div class="flanco">
        <img class="ala" src="__APEROL__" alt="">
        <p class="hora">20:00</p>
        <img class="ala angosta" src="__MASCARA__" alt="">
      </div>
      <!-- Lo resumido que pidió ella: transcurre adentro y afuera del
           salón. Dos datos y se termina — la invitación no explica el
           catering, lo insinúan la torre de copas y la máscara. -->
      <p class="donde">Adentro y afuera del sal&oacute;n</p>
    </div>
  </div>
</section>

<!-- ══════════ 5 · DRESS CODE ══════════ -->
<section class="acto junto" id="vestimenta">
  <div class="wrap">
    <!-- ⚠️ Acá iba la vela y no tenía nada que ver con el dress code. Hoy
         está el traje y el vestido: prendas solas, sin personas. El
         invitado la mira y ya sabe qué ponerse, sin leer una palabra.
         ⚠️⚠️ El vestido es TERRACOTA y nunca claro: es la única imagen de
         la invitación que se lee como "vestite así", y un vestido crema
         dibujado acá termina en alguien vestida como la novia. Si algún
         día se regenera, ese es el primer control. -->
    <!-- ⚠️ 400 -> 260px, a pedido de Fer: quedaba muy grande. Es una
         referencia de qué ponerse, no una escena — no tiene por qué
         ocupar lo mismo que el altar o que la acuarela de ellos. -->
    <img class="acuarela rev" src="__DRESSCODE__" style="max-width:210px"
         alt="Un vestido largo terracota y un traje verde oliva">
    <p class="rot rev">Dress code</p>
    <h2 class="rev"><em>Elegante</em></h2>
  </div>
</section>

<!-- ══════════ 6 · REGALOS ══════════ -->
<section class="acto junto banda" id="regalos">
  <div class="wrap">
    <img class="motivo rev" src="__NARANJAS__" style="width:180px" alt="">
    <p class="rot rev" style="margin-top:8px">Regalos</p>
    <h2 class="rev">Nuestro mayor regalo es <em>compartir este d&iacute;a</em></h2>
    <p class="rev" style="margin-top:18px;color:var(--tinta-2);font-size:.95rem;
       max-width:30em;margin-left:auto;margin-right:auto">
      Pero si quer&eacute;s colaborar con nuestra luna de miel, pod&eacute;s hacerlo en la cuenta:</p>

    <!-- ⚠️ La torre y el Coliseo van JUSTO DEBAJO de la línea de la luna
         de miel, no arriba del rótulo: la luna de miel es en Francia e
         Italia, así que acá el dibujo no decora — explica el pedido. Es
         el mismo hilo que la etiqueta de valija y la máscara veneciana.
         ⚠️ Pareados por ALTO: la torre es alta y flaca y el Coliseo es
         ancho y bajo. Por ancho, la torre quedaría del doble de alto. -->
    <div class="duo rev">
      <img src="__EIFFEL__" alt=""><img src="__COLISEO__" alt="">
    </div>
    <div class="alias rev">
      <span id="alias" data-falta>guille.seba.boda</span>
      <button id="copiar" type="button">Copiar</button>
    </div>
  </div>
</section>

<!-- ══════════ 7 · CONFIRMAR ══════════ -->
<section class="acto junto" id="rsvp">
  <div class="wrap">
    <!-- ⚠ Acá había DOS motivos sueltos, uno arriba del otro: el ramo de
         naranjas y la rama de olivo. Dos adornos seguidos no dicen nada;
         ellos mirándose sí, y es el último dibujo antes de pedirle al
         invitado que confirme. -->
    <img class="acuarela rev" src="__PAREJA__"
         alt="Guillermina y Sebasti&aacute;n mir&aacute;ndose, frente al lago">
    <p class="rot rev">Queremos contar con vos</p>
    <h2 class="rev">Confirm&aacute; tu <em>lugar</em></h2>
    <p class="rev" style="margin-top:16px;color:var(--tinta-2);font-size:.95rem">
      Antes del 18 de febrero de 2027</p>

    <!-- El formulario lo arma el JS de abajo, porque depende de a quién
         está dirigido el link (?invitado= y cuántos cupos tiene). Hasta
         que contesta Supabase se muestra este cartel: sin él la sección
         queda como un título suelto y parece que falta algo. -->
    <div class="cerrado rev" id="rsvp-cargando">Un segundo&hellip;</div>
    <div class="form" id="rsvp-form" hidden>
      <div class="dos">
        <div class="campo"><label for="f-nom">Nombre</label>
          <input id="f-nom" type="text" autocomplete="given-name" placeholder="Tu nombre"></div>
        <div class="campo"><label for="f-ape">Apellido</label>
          <input id="f-ape" type="text" autocomplete="family-name" placeholder="Tu apellido"></div>
      </div>

      <div class="campo"><label>&iquest;Nos acompa&ntilde;&aacute;s?</label>
        <div class="chips" id="f-asiste">
          <button type="button" class="chip si" data-val="si">S&iacute;, ah&iacute; estar&eacute;</button>
          <button type="button" class="chip" data-val="no">No voy a poder</button>
        </div>
      </div>

      <!-- Cuántos son. Sólo aparece si el link trae más de un cupo: a
           quien viene solo, un desplegable de "1" no le dice nada. -->
      <div class="campo" id="f-cuantos-caja" hidden>
        <label>&iquest;Cu&aacute;ntos vienen en total?</label>
        <div class="chips" id="f-cuantos"></div>
      </div>

      <!-- ⚠️ La dieta del TITULAR se esconde si dice que no viene; las
           tarjetas de los acompañantes NO. Ver el comentario del CSS. -->
      <div class="campo" id="f-dieta-caja"><label>&iquest;Alguna preferencia con la comida?</label>
        <div class="chips" id="f-dieta">
          <button type="button" class="chip" data-d="Vegetariano">Vegetariano</button>
          <button type="button" class="chip" data-d="Vegano">Vegano</button>
          <button type="button" class="chip" data-d="Cel&iacute;aco">Cel&iacute;aco</button>
          <button type="button" class="chip" data-d="Sin lactosa">Sin lactosa</button>
        </div>
      </div>

      <div id="f-acomps"></div>

      <div class="campo" id="f-cancion-caja"><label for="f-cancion">Un tema que no puede faltar</label>
        <input id="f-cancion" type="text" placeholder="La canci&oacute;n que te hace bailar"></div>

      <div style="text-align:center">
        <button class="btn lleno" type="button" id="btn-rsvp">Confirmar asistencia</button>
      </div>
    </div>
  </div>
</section>

<footer>
  Guillermina &amp; Sebasti&aacute;n &middot; 3 de abril de 2027<br>
  <a href="https://www.invitacionesdigitalesoficial.com/?utm_source=invitacion&amp;utm_medium=footer&amp;utm_content=marca"
     target="_blank" rel="noopener">Invitaciones Digitales Oficial</a>
</footer>

<!-- "Sarà perché ti amo", VERSIÓN DE PIANO — 46s desde el 0:30, mono,
     96 kbps, 539 KB.
     ⚠️ Instrumental a pedido de Guillermina: "nos gustaría instrumental,
     como la que te mandé, que sea encantada". La versión cantada de
     Ricchi e Poveri quedó descartada.
     ⚠️ El tramo se eligió midiendo la energía del tema cada 2 segundos,
     no a ojo: el pico está entre el 0:32 y el 0:40, que es donde entra
     el estribillo. Igual esto hay que ESCUCHARLO — una medición dice
     dónde sube el volumen, no dónde empieza la melodía que se reconoce.
     ⚠️ La canción entera pesaba 4,3 MB: nadie con datos móviles en el
     medio del campo baja eso. Y un link de Spotify no sirve — no se
     reproduce embebido sin cuenta y sesión iniciada.
     ⚠️ `preload="none"` y archivo aparte, NO data URI: embebido ya está
     adentro del HTML y el "none" no sirve de nada. -->
<audio id="audio" loop preload="none">
  <source src="/guille-musica.mp3" type="audio/mpeg"></audio>
<button class="musica" id="musica" type="button" aria-label="Pausar la m&uacute;sica">
  <span class="barra"></span><span class="barra"></span><span class="barra"></span>
</button>

<script>
/* ── Los pétalos ─────────────────────────────────────────────────── */
const COL=['#E07A1F','#A84F2A','#D7C3A1','#A0451A','#C98B5A'];
function petalos(cont,n,caida){
  for(let i=0;i<n;i++){
    const s=document.createElementNS('http://www.w3.org/2000/svg','svg');
    const w=7+Math.random()*8;
    s.setAttribute('viewBox','0 0 20 26');
    s.setAttribute('width',w); s.setAttribute('height',w*1.3);
    s.innerHTML='<path d="M10 0C15.5 6 19 13 16.5 19.5C14.6 24.4 11.8 26 10 26C8.2 26 5.4 24.4 3.5 19.5C1 13 4.5 6 10 0Z"/>';
    s.style.fill=COL[i%COL.length]; s.classList.add('p');
    s.style.left=(Math.random()*94)+'%';
    s.style.setProperty('--dx',(Math.random()*170-85)+'px');
    s.style.setProperty('--giro',(Math.random()*840-420)+'deg');
    s.style.setProperty('--caida',caida||'105vh');
    s.style.animationDuration=(8+Math.random()*6).toFixed(1)+'s';
    s.style.animationDelay=(-Math.random()*15).toFixed(1)+'s';
    s.style.opacity=(.3+Math.random()*.3).toFixed(2);
    cont.appendChild(s);
  }
}
petalos(document.getElementById('petalos-portada'),14);

/* ── La entrada. UN SOLO TOQUE ────────────────────────────────────
   ⚠️ La música arranca ACÁ ADENTRO, en el gesto. Desde el setTimeout
   es sin gesto y el navegador la bloquea: la invitación abre muda. */
const GIRO=900, LEER=2500, SUBE=1150;
const audio=document.getElementById('audio');
const btnMus=document.getElementById('musica');
/* ⚠️ Sin archivo de audio no hay botón: un botón de música que no suena
   es peor que no tener música. */
const HAY_MUSICA = !!audio.querySelector('source').getAttribute('src');
if (HAY_MUSICA) document.body.classList.add('con-musica');
let abierto=false;
function abrir(){
  if(abierto) return; abierto=true;
  if(HAY_MUSICA) audio.play().then(()=>btnMus.classList.add('sonando')).catch(()=>{});
  document.getElementById('eti').classList.add('volteada');
  document.getElementById('pie').classList.add('ida');
  setTimeout(()=>document.getElementById('colgante').classList.add('sube'), GIRO+LEER);
  setTimeout(()=>{
    document.getElementById('portada').classList.add('ida');
    document.body.classList.add('adentro');
    window.scrollTo(0,0);
    arrancarSecciones();          // ⚠️ recién acá, con la portada fuera
  }, GIRO+LEER+SUBE-260);
}
const eti=document.getElementById('eti');
eti.onclick=abrir;
eti.onkeydown=e=>{ if(e.key==='Enter'||e.key===' '){e.preventDefault();abrir();} };
setTimeout(()=>{ if(!abierto) document.getElementById('toca').classList.add('avisa'); },6000);

btnMus.onclick=()=>{
  if(audio.paused){ audio.play().then(()=>btnMus.classList.add('sonando')).catch(()=>{}); }
  else { audio.pause(); btnMus.classList.remove('sonando'); }
};

/* ── Los dibujos que se dibujan solos ─────────────────────────────
   ⚠️⚠️ "El primer trazo no se dibuja" volvió TRES veces y cada vez la
   causa fue otra. Esta es la versión que funciona, y las tres cosas
   son necesarias:
     1 · UNA sola función para arrancar. Siempre.
     2 · Leer getComputedStyle(t).strokeDashoffset de CADA trazo y
         arrancar adentro de un DOBLE requestAnimationFrame. Leer
         offsetWidth fuerza el layout, y stroke-dashoffset es una
         propiedad de PINTADO: el navegador puede saltearse el recálculo.
     3 · transition:'none' EXPLÍCITO al preparar. transition-property
         vale 'all' por defecto, así que el transitionDuration que dejó
         el ciclo anterior sobrevive y el reset a "escondido" también
         transiciona: el trazo nunca llega a estar vacío.
   Y esto sólo se ve MIDIENDO el dashoffset: en una captura, un trazo
   que salta y uno que se dibuja rápido se ven igual. */
function dibujar(caja, demora, duracion){
  const t = [...caja.querySelectorAll('.trazo')];
  if(!t.length) return;
  caja.classList.remove('pintada');
  t.forEach(x=>{
    x.style.transition='none';
    const L=x.getTotalLength();
    x.style.strokeDasharray=L; x.style.strokeDashoffset=L;
  });
  t.forEach(x=>getComputedStyle(x).strokeDashoffset);       // ⚠️ no sacar
  requestAnimationFrame(()=>requestAnimationFrame(()=>{
    t.forEach((x,i)=>{
      x.style.transition='';
      x.style.transitionProperty='stroke-dashoffset';
      x.style.transitionTimingFunction='cubic-bezier(.22,.61,.36,1)';
      x.style.transitionDuration=duracion+'ms';
      setTimeout(()=>{x.style.strokeDashoffset='0';}, i*demora);
    });
    const fin = t.length*demora + duracion;
    // Los hielos caen DESPUÉS de que la copa terminó de dibujarse.
    caja.querySelectorAll('.cae').forEach(h=>
      setTimeout(()=>h.classList.add('cayendo'), fin));
    // Y la acuarela aparece por debajo, si esta caja tiene una.
    setTimeout(()=>caja.classList.add('pintada'), fin+200);
  }));
}
/* Cada dibujo con su ritmo: la escena tiene 201 trazos y va rápido o
   tarda medio minuto; la copa tiene 14 y puede darse el lujo. */
const RITMO={'esc-ellos':[13,480],'dib-cartel':[15,520],
             'dib-copa':[95,900],'dib-naranja':[130,1100]};

/* ── El contador de días ──────────────────────────────────────────
   ⚠️ La fecha se arma con el huso de Argentina escrito a mano (-03:00),
   no con new Date('2027-04-03T18:00'): sin huso, cada navegador la lee
   en el suyo y a un invitado en Madrid le faltarían días distintos. */
(function(){
  const BODA = new Date('2027-04-03T18:00:00-03:00');
  const caja = document.getElementById('cuenta');
  const el = {d:document.getElementById('cd'), h:document.getElementById('ch'),
              m:document.getElementById('cm'), s:document.getElementById('cs')};
  const dos = n => String(n).padStart(2,'0');
  let reloj = null;
  function tic(){
    const falta = BODA - new Date();
    if (falta <= 0){ clearInterval(reloj); caja.hidden = true; return; }
    const seg = Math.floor(falta/1000);
    el.d.textContent = Math.floor(seg/86400);
    el.h.textContent = dos(Math.floor(seg/3600) % 24);
    el.m.textContent = dos(Math.floor(seg/60) % 60);
    el.s.textContent = dos(seg % 60);
    caja.hidden = false;
  }
  tic();
  /* ⚠️ El tictac corre SÓLO mientras el contador está a la vista. Un
     setInterval de un segundo que sigue con la pestaña en el bolsillo
     es batería tirada, y al volver el navegador dispara todos los
     ciclos atrasados de una. */
  new IntersectionObserver(es=>es.forEach(e=>{
    if (e.isIntersecting){ if(!reloj){ tic(); reloj = setInterval(tic,1000); } }
    else { clearInterval(reloj); reloj = null; }
  }),{threshold:.2}).observe(caja);
})();

/* ── Cada sección aparece al entrar en pantalla ──────────────────── */
const ojo=new IntersectionObserver(es=>{
  es.forEach(e=>{ if(e.isIntersecting){
    e.target.classList.add('on');
    e.target.querySelectorAll('.rev').forEach((el,i)=>
      setTimeout(()=>el.classList.add('on'), i*130));
    if(e.target.id==='ceremonia'){
      const c=document.getElementById('petalos-ceremonia');
      /* Acá la caída es el alto de la sección, no el de la pantalla:
         con 105vh los pétalos se los coma el overflow a mitad de camino. */
      if(!c.childElementCount) petalos(c,11,c.offsetHeight+60+'px');
    }
    // Los dibujos de esta sección arrancan cuando la sección entra.
    e.target.querySelectorAll('[id^="esc-"],[id^="dib-"]').forEach(d=>{
      const [dem,dur]=RITMO[d.id]||[40,700];
      setTimeout(()=>dibujar(d,dem,dur), 320);
    });
    ojo.unobserve(e.target);
  }});
},{threshold:.16});
/* ⚠️⚠️ Los observadores NO arrancan hasta que la portada se fue. La
   primera sección está abajo de la etiqueta, así que se cruzaba con la
   pantalla desde el primer instante: los 201 trazos de la acuarela
   principal se dibujaban enteros DETRÁS de la portada y, cuando la
   etiqueta subía, ya estaba todo pintado. El efecto existía y no lo
   veía nadie. */
function arrancarSecciones(){
  document.querySelectorAll('.acto').forEach(s=>ojo.observe(s));
  document.querySelectorAll('.sep').forEach(x=>ojoSep.observe(x));
}

/* ── El cartel, dibujándose una y otra vez ────────────────────────
   ⚠️ El bucle se apaga cuando el cartel sale de la pantalla. Si no,
   sigue redibujándose para nadie: gasta batería y, con la pestaña en
   segundo plano, los timers se acumulan. */
(function(){
  const c = document.querySelector('.bucle');
  if(!c) return;
  const [dem,dur] = RITMO[c.id] || [15,520];
  const vuelta = c.querySelectorAll('.trazo').length*dem + dur + 3400;
  let reloj = null;
  new IntersectionObserver(es=>es.forEach(e=>{
    if(e.isIntersecting){
      if(reloj) return;
      reloj = setInterval(()=>dibujar(c,dem,dur), vuelta);
    } else { clearInterval(reloj); reloj = null; }
  }),{threshold:.25}).observe(c);
})();
/* ⚠️ Los separadores viven ENTRE las secciones, no adentro: el
   observador de `.acto` no los alcanza y se quedaban invisibles para
   siempre, en opacidad 0. Van con su propio observador. */
const ojoSep=new IntersectionObserver(es=>es.forEach(e=>{
  if(e.isIntersecting){ e.target.classList.add('on'); ojoSep.unobserve(e.target); }
}),{threshold:.5});
new IntersectionObserver(es=>es.forEach(e=>{
  if(e.isIntersecting){ e.target.classList.add('on'); }
}),{threshold:.3}).observe(document.getElementById('mapa'));

/* ── Copiar el alias ─────────────────────────────────────────────── */
document.getElementById('copiar').onclick=async function(){
  const t=document.getElementById('alias').textContent.trim();
  try{ await navigator.clipboard.writeText(t); this.textContent='Copiado'; }
  catch(e){ const r=document.createRange();
    r.selectNodeContents(document.getElementById('alias'));
    const s=getSelection(); s.removeAllRanges(); s.addRange(r);
    this.textContent='Copialo'; }
  setTimeout(()=>{this.textContent='Copiar';},2400);
};
</script>

<!-- ══════════════════════════════════════════════════════════════════
     CONFIRMAR ASISTENCIA — contra NUESTRO panel, el que ya funciona.

     Guillermina y Sebastián administran su fiesta desde
     `admin.html?evento=guille-sebas`, igual que cualquier cliente:
     generan los links, ven quién confirmó, bajan el listado para el
     salón y la lista para el DJ. Esta invitación es a medida en el
     diseño, no en el sistema.

     ⚠️ NADA DE ESTO TOCA LA BASE DIRECTO. Se llama a `ya_confirmo` y a
     `rsvp_enviar`, las dos funciones `security definer` de Postgres.
     La anon key está a la vista de cualquier invitado —es pública por
     diseño— y no puede leer `confirmaciones`: quien abra el código
     fuente no ve un solo dato de otro invitado.

     ⚠️ NO HAY MESAS: bandejeo, livings, nadie tiene lugar asignado.
     `mesa` va vacío y `rsvp_enviar` lo guarda como nulo.
     ══════════════════════════════════════════════════════════════════ -->
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script>
(function(){
const SUPA_URL='https://ldvosdztnhrvrqxnjuco.supabase.co';
const SUPA_KEY='__ANON__';
const EVENTO='__EVENTO__';
const sb=supabase.createClient(SUPA_URL,SUPA_KEY,{db:{schema:'invitaciones'}});

/* ⚠️ La query puede NO estar en la barra del navegador. Se entra por
   `/guille-invitacion`, que es una ruta limpia: Vercel le pasa la query
   a la función pero `location.search` queda VACÍO. `api/i.js` la deja
   en `window.__QS_SERVIDOR`. Sin esto, un link con ?invitado=Susana
   abriría el formulario en blanco y la fila se guardaría bajo
   'general', mezclando a todos los invitados en un solo grupo. */
const QS=new URLSearchParams(location.search || window.__QS_SERVIDOR || '');
const INVITADO=(QS.get('invitado')||'').trim();
const CUPOS=Math.max(1,Math.min(20,parseInt(QS.get('personas')||'1',10)||1));

const $=id=>document.getElementById(id);
const form=$('rsvp-form'), cargando=$('rsvp-cargando'), btn=$('btn-rsvp');

/* ── El globo de aviso ────────────────────────────────────────────
   ⚠️ Va con textContent, nunca innerHTML: acá adentro terminan
   nombres que escribe el invitado. */
let relojGlobo=null;
function avisar(txt){
  let g=document.querySelector('.globo');
  if(!g){ g=document.createElement('div'); g.className='globo';
          g.setAttribute('role','alert'); document.body.appendChild(g); }
  g.textContent=txt;
  requestAnimationFrame(()=>g.classList.add('on'));
  clearTimeout(relojGlobo);
  relojGlobo=setTimeout(()=>g.classList.remove('on'),4200);
}

/* ── Los chips ────────────────────────────────────────────────────
   Uno solo elegido en un grupo, o varios si es de dieta. */
function grupo(caja,unico,alCambiar){
  caja.addEventListener('click',e=>{
    const c=e.target.closest('.chip'); if(!c) return;
    if(unico) caja.querySelectorAll('.chip').forEach(x=>x.classList.remove('si'));
    c.classList.toggle('si', unico ? true : !c.classList.contains('si'));
    if(alCambiar) alCambiar();
  });
}
const elegido=caja=>caja.querySelector('.chip.si');
const dietaDe=caja=>[...caja.querySelectorAll('.chip.si')]
                      .map(c=>c.textContent.trim()).join(', ');

/* ── El prellenado ────────────────────────────────────────────────
   ⚠️⚠️ UN LINK NO SE LLAMA "FAMILIA FERREYRA". Partir el nombre en dos
   dejaba nombre="Familia", apellido="Ferreyra": los DOS campos llenos,
   o sea que la validación lo aceptaba, y a la fiesta iba a ir alguien
   llamado "Familia Ferreyra". Si la primera palabra es familia/flia/
   fam, los campos quedan vacíos y los escribe quien confirma. */
function prellenar(){
  if(!INVITADO) return;
  const p=INVITADO.split(/\s+/);
  if(/^(familia|familias|flia|fam)\.?$/i.test(p[0])) return;
  $('f-nom').value=p[0]||'';
  $('f-ape').value=p.slice(1).join(' ');
}

/* ── Las tarjetas de los acompañantes ─────────────────────────────
   ⚠️ Se arman con DOM y no con innerHTML: el nombre del link lo
   escribe el cliente en su panel y termina acá adentro. */
function tarjeta(i){
  const d=document.createElement('div'); d.className='acomp';
  const t=document.createElement('div'); t.className='quien';
  t.textContent='Acompañante '+i; d.appendChild(t);

  const dos=document.createElement('div'); dos.className='dos';
  [['Nombre','a-nom','given-name'],['Apellido','a-ape','family-name']]
    .forEach(([tit,cls,ac])=>{
      const c=document.createElement('div'); c.className='campo';
      const l=document.createElement('label'); l.textContent=tit;
      const inp=document.createElement('input');
      inp.type='text'; inp.className=cls; inp.autocomplete=ac;
      inp.id=cls+'-'+i; l.htmlFor=inp.id;
      c.append(l,inp); dos.appendChild(c);
    });
  d.appendChild(dos);

  const c2=document.createElement('div'); c2.className='campo';
  const l2=document.createElement('label'); l2.textContent='¿Viene?';
  const ch=document.createElement('div'); ch.className='chips a-asiste';
  [['si','Sí'],['no','No puede']].forEach(([v,tx],k)=>{
    const b=document.createElement('button');
    b.type='button'; b.className='chip'+(k===0?' si':''); b.dataset.val=v;
    b.textContent=tx; ch.appendChild(b);
  });
  grupo(ch,true); c2.append(l2,ch); d.appendChild(c2);

  const c3=document.createElement('div'); c3.className='campo';
  const l3=document.createElement('label'); l3.textContent='Preferencia con la comida';
  const ch3=document.createElement('div'); ch3.className='chips a-dieta';
  ['Vegetariano','Vegano','Celíaco','Sin lactosa'].forEach(x=>{
    const b=document.createElement('button');
    b.type='button'; b.className='chip'; b.textContent=x; ch3.appendChild(b);
  });
  grupo(ch3,false); c3.append(l3,ch3); d.appendChild(c3);
  return d;
}

function pintarAcomps(n){
  const caja=$('f-acomps'); caja.textContent='';
  for(let i=2;i<=n;i++) caja.appendChild(tarjeta(i));
}

/* ── Arranque ─────────────────────────────────────────────────────── */
(async function(){
  /* ⚠️ Se pregunta ANTES de pintar el formulario. Dejar que alguien
     complete siete campos para avisarle recién al enviar que ya había
     confirmado es la peor forma posible de decirlo.
     `ya_confirmo` devuelve un booleano y nada más: ningún dato personal
     viaja al navegador. */
  let ya=false;
  if(INVITADO){
    try{
      const {data}=await sb.rpc('ya_confirmo',{p_evento:EVENTO,p_invitado:INVITADO});
      ya=!!data;
    }catch(e){ /* si falla, se muestra el formulario: es preferible una
                  confirmación repetida a un invitado que no puede contestar */ }
  }
  if(ya){
    cargando.textContent='Ya recibimos tu confirmación. ¡Gracias! '
                        +'Si necesitás cambiar algo, escribinos.';
    return;
  }
  cargando.hidden=true; form.hidden=false;
  prellenar();

  grupo($('f-asiste'),true,()=>{
    /* ⚠️ Sólo se esconde la dieta del titular y su canción. Las
       tarjetas de los acompañantes SIGUEN A LA VISTA: el que dice que
       no puede ir no contesta por el resto de su grupo. */
    const va=elegido($('f-asiste')).dataset.val==='si';
    $('f-dieta-caja').hidden=!va;
    $('f-cancion-caja').hidden=!va;
    $('f-cuantos-caja').hidden=!va||CUPOS<2;
  });
  grupo($('f-dieta'),false);

  if(CUPOS>1){
    const caja=$('f-cuantos'); $('f-cuantos-caja').hidden=false;
    for(let i=1;i<=CUPOS;i++){
      const b=document.createElement('button');
      b.type='button'; b.className='chip'+(i===CUPOS?' si':'');
      b.textContent=String(i); b.dataset.n=String(i); caja.appendChild(b);
    }
    grupo(caja,true,()=>pintarAcomps(+elegido(caja).dataset.n));
    pintarAcomps(CUPOS);
  }
})();

/* ── Enviar ───────────────────────────────────────────────────────── */
btn.addEventListener('click',async function(){
  const nom=$('f-nom').value.trim(), ape=$('f-ape').value.trim();
  if(!nom||!ape){ avisar('Completá tu nombre y tu apellido.');
                  (nom?$('f-ape'):$('f-nom')).focus(); return; }

  const va=elegido($('f-asiste')).dataset.val;
  const filas=[{nombre:nom,apellido:ape,asiste:va,
                dieta:va==='si'?dietaDe($('f-dieta')):'',
                mensaje:va==='si'?$('f-cancion').value.trim():'',
                mesa:''}];

  /* ⚠️⚠️ LAS FILAS DE LOS ACOMPAÑANTES SE ARMAN SIEMPRE, vaya o no vaya
     el titular. `rsvp_enviar` borra TODAS las filas de este link antes
     de insertar: un acompañante que no se manda no queda en "no" ni en
     "pendiente" — desaparece, y la cuenta del catering da de menos sin
     que nadie se entere. */
  const tarjetas=[...document.querySelectorAll('.acomp')];
  const flojas=tarjetas.filter(t=>{
    const n=t.querySelector('.a-nom').value.trim();
    const a=t.querySelector('.a-ape').value.trim();
    return !n||!a;
  });
  if(flojas.length){
    /* El apellido es obligatorio también acá: el listado del salón se
       ordena por apellido. Si alguien no viene, se baja el número de
       arriba en vez de dejar la tarjeta a medias. */
    flojas[0].scrollIntoView({behavior:'smooth',block:'center'});
    avisar(flojas.length===1
      ? 'Falta el nombre y el apellido de un acompañante. '
        +'Si vienen menos, cambiá el número de arriba.'
      : 'Faltan los datos de '+flojas.length+' acompañantes. '
        +'Si vienen menos, cambiá el número de arriba.');
    return;
  }
  tarjetas.forEach(t=>{
    const cA=t.querySelector('.a-asiste .chip.si').dataset.val;
    filas.push({nombre:t.querySelector('.a-nom').value.trim(),
                apellido:t.querySelector('.a-ape').value.trim(),
                asiste:cA,
                dieta:cA==='si'?dietaDe(t.querySelector('.a-dieta')):'',
                mensaje:'', mesa:''});
  });

  /* ⚠️ El botón se bloquea ANTES de la llamada, no después. En el campo
     la conexión es mala, la respuesta tarda y el invitado vuelve a
     tocar: sin esto entra dos veces y el salón sirve el doble. */
  btn.disabled=true; const antes=btn.textContent; btn.textContent='Enviando…';

  const {error}=await sb.rpc('rsvp_enviar',
    {p_evento:EVENTO,p_invitado:INVITADO||'general',p_filas:filas});

  if(error){
    /* ⚠️ NO SE PIERDE NADA de lo que escribió: el formulario queda tal
       cual y el botón vuelve a habilitarse. Perder los datos que
       alguien acaba de cargar es lo peor que puede pasar acá. */
    btn.disabled=false; btn.textContent=antes;
    avisar('No pudimos guardarlo. Fijate la conexión y probá de nuevo.');
    return;
  }

  form.hidden=true; cargando.hidden=false;
  cargando.textContent=va==='si'
    ? '¡Listo! Ya te esperamos el 3 de abril.'
    : 'Gracias por avisarnos. Te vamos a extrañar.';
})
})();
</script>
</body>
</html>
'''

CLAVES = {'etiqueta':'ETIQUETA','ellos':'ELLOS','altar':'ALTAR','mapa':'MAPA',
          'luces':'LUCES','vela':'VELA','pareja':'PAREJA',
          'naranjas':'NARANJAS','copas':'COPAS','aperol':'APEROL',
          'alianzas':'ALIANZAS','mascara':'MASCARA','dresscode':'DRESSCODE',
          'eiffel':'EIFFEL','coliseo':'COLISEO','violin':'VIOLIN','piano':'PIANO'}
for k, v in IM.items():
    HTML = HTML.replace('__' + CLAVES[k] + '__', v)
HTML = (HTML.replace('__VB_ESC__', VB_ESC).replace('__T_ESC__', T_ESC)
            .replace('__VB_CAR__', VB_CAR).replace('__T_CAR__', T_CAR)
            .replace('__VB_LUZ__', VB_LUZ).replace('__T_LUZ__', T_LUZ))

# El evento de ellos en NUESTRO panel: admin.html?evento=guille-sebas.
# La invitación es a medida en el diseño, no en el sistema — los links,
# el listado del salón y la lista del DJ salen del panel de siempre.
#
# La anon key es pública por diseño: viaja en el código de toda
# invitación y sólo puede leer (id, config) de `eventos`. No alcanza
# para leer una sola fila de `confirmaciones`.
EVENTO = 'guille-sebas'
ANON = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxk'
        'dm9zZHp0bmhydnJxeG5qdWNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUyOTY1MjAsImV4c'
        'CI6MjEwMDg3MjUyMH0.u64wnWOA-Bp0NfOR3tLOAtSkG34P-ApTS00KwTEkGRM')
HTML = HTML.replace('__EVENTO__', EVENTO).replace('__ANON__', ANON)
sobran = [c for c in CLAVES.values() if '__'+c+'__' in HTML]
if sobran: print('⚠️ marcadores sin usar:', sobran)

io.open(f"{BASE}/cliente-guille-invitacion.html", 'w', encoding='utf-8').write(HTML)
print('\ncliente-guille-invitacion.html', len(HTML)//1024, 'KB')
