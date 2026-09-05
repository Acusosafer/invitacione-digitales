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

def jpg(nombre, ancho, q=78, limpiar=True):
    im = Image.open(f"{W}/{nombre}").convert('RGB')
    if im.width > ancho:
        im = im.resize((ancho, round(ancho*im.height/im.width)), Image.LANCZOS)
    if limpiar:
        im, medida = blanquear(im)
        if medida: print(f'    papel {medida[0]:.0f} -> {medida[1]:.0f}')
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True, progressive=True)
    print(f'  {nombre:26} {ancho}px {len(b.getvalue())//1024:4} KB')
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

def webp(ruta, q=88):
    im = Image.open(ruta)
    b = io.BytesIO(); im.save(b, 'WEBP', quality=q, method=6)
    print(f'  etiqueta                   {len(b.getvalue())//1024:4} KB')
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()

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
  'etiqueta': webp('etiqueta-lista.png'),
  'ellos':    jpg('ellos-tono.jpg', 720, 80, limpiar=False),
  'altar':    jpg('gemini-generated-image-fp6fmkfp6fmkfp6f.jpg', 700),
  'mapa':     jpg('mapa.jpg', 780, 76, limpiar=False),
  'luces':    jpg('guirnalda-de-luces.jpg', 620),
  'vela':     jpg('vela.jpg', 300),
  'ramo':     jpg('ramo-con-naranjas.jpg', 380),
  'olivo':    jpg('olivo.jpg', 420),
  'naranjas': jpg('medias-naranja.jpg', 420),
  'aperol':   jpg('aperol.jpg', 240),
  'copas':    jpg('copas-solas.jpg', 460),
}
VB_ESC, T_ESC = trazos('escena')
VB_CAR, T_CAR = trazos('cartel')

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

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Parisienne&family=Marcellus&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">

<style>
:root{
  --naranja:#E07A1F; --hondo:#A0451A; --terracota:#A84F2A;
  --oliva:#435F3A; --avena:#D7C3A1;
  --papel:#F6F2E8; --tinta:#3A302A; --tinta-2:#6B5D51;
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
  transform-origin:50% 0;animation:mecer 7s ease-in-out infinite}
@keyframes mecer{0%,100%{transform:rotate(-1deg)}50%{transform:rotate(1deg)}}
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
@keyframes caer{0%{transform:translate3d(0,-40px,0) rotate(0);opacity:0}
  12%{opacity:.8}85%{opacity:.65}
  100%{transform:translate3d(var(--dx),110%,0) rotate(var(--giro));opacity:0}}

/* ══════════ SECCIONES ══════════ */
.acto{padding:86px 0;text-align:center}
.acto.junto{padding-top:0}
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
/* El contador. Un número grande y nada más: la cuenta de los días es
   el dato, no un cartel. */
.cuenta{margin-top:34px;display:flex;flex-direction:column;align-items:center;gap:2px}
.cuenta .n{font-family:'Marcellus',serif;font-size:3.1rem;line-height:1;
  color:var(--hondo);font-variant-numeric:tabular-nums}
.cuenta .t{font-family:'Marcellus',serif;font-size:.62rem;letter-spacing:.32em;
  text-transform:uppercase;color:var(--tinta-2)}

.dato{margin-top:26px}
.dato .hora{font-family:'Marcellus',serif;font-size:2.4rem;color:var(--hondo);line-height:1}
.dato .donde{margin-top:8px;font-size:.95rem;color:var(--tinta-2)}
.acto .acuarela{max-width:520px;margin:0 auto 26px}
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
  <div class="wrap">
    <div class="escena rev" id="esc-ellos">
      <img class="acuarela" src="__ELLOS__"
           alt="Guillermina y Sebasti&aacute;n de espaldas frente al lago, al atardecer">
      <svg viewBox="__VB_ESC__" aria-hidden="true">__T_ESC__</svg>
    </div>
    <h2 class="rev" style="margin-top:26px"><em>Guillermina y Sebasti&aacute;n</em></h2>
    <p class="rot rev" style="margin-top:20px">S&aacute;bado 3 de abril de 2027</p>
    <p class="rev" style="margin-top:6px;color:var(--tinta-2);font-size:.95rem">
      Finca La Josefina &middot; Berisso</p>

    <!-- El cartel de la entrada, dibujándose EN BUCLE. Es lo que ven al
         llegar, y acá abajo de la fecha hace de firma del lugar.
         ⚠️ El bucle se apaga cuando el cartel sale de la pantalla: si no
         sigue redibujándose para nadie, gastando batería. -->
    <svg class="dibujo rev bucle" id="dib-cartel" viewBox="__VB_CAR__"
         style="width:100%;max-width:330px;margin-top:34px" aria-hidden="true">__T_CAR__</svg>

    <div class="cuenta rev" id="cuenta" hidden>
      <span class="n" id="cuenta-n">—</span>
      <span class="t" id="cuenta-t">d&iacute;as</span>
    </div>
  </div>
</section>

<img class="sep rev" src="__APEROL__" alt="" aria-hidden="true" style="width:56px">

<!-- ══════════ 2 · LA CEREMONIA ══════════ -->
<section class="acto junto" id="ceremonia" style="position:relative;overflow:hidden">
  <!-- ⚠️ Los pétalos van ENCIMA de la sección, no en un bloque aparte:
       suelto abajo dejaba 180px de papel vacío con un pétalo perdido,
       que se lee como un error y no como un efecto. -->
  <div class="petalos" id="petalos-ceremonia" aria-hidden="true"></div>
  <div class="wrap">
    <img class="acuarela rev" src="__ALTAR__" style="max-width:420px"
         alt="El altar sobre el pico que entra al lago" >
    <p class="rot rev" style="margin-top:22px">La ceremonia</p>
    <h2 class="rev">Sobre el <em>pico</em>, frente al agua</h2>
    <div class="dato rev">
      <p class="hora">18:00</p>
      <p class="donde">Finca La Josefina &middot; Berisso</p>
    </div>
  </div>
</section>

<!-- ══════════ 3 · CÓMO LLEGAR ══════════ -->
<section class="acto junto" id="mapa-sec">
  <div class="wrap">
    <p class="rot rev">C&oacute;mo llegar</p>
    <!-- El cartel ya dice "Finca La Josefina": repetirlo abajo en el
         titulo es decir dos veces lo mismo. Ac&aacute; va el dato que falta. -->
    <h2 class="rev">Berisso, <em>Buenos Aires</em></h2>
    <div class="mapa rev" id="mapa">
      <img src="__MAPA__" alt="Mapa de la finca: la entrada, el estacionamiento, el sal&oacute;n y el altar sobre el lago">
      <svg class="capa" viewBox="0 0 1000 758" preserveAspectRatio="none" aria-hidden="true">
        <path class="ruta" d="M170 700 C240 690 300 660 360 620 C420 582 470 566 512 560
                              C548 554 560 530 552 500 C544 468 556 442 590 430
                              C630 416 660 386 672 344 C682 310 700 290 726 280"/>
        <path class="punta" d="M706 292 L728 276 L732 302"/>
      </svg>
    </div>
    <a class="btn rev" href="https://maps.google.com/?q=Finca+La+Josefina+Berisso"
       target="_blank" rel="noopener">Abrir en el mapa</a>
  </div>
</section>



<!-- ══════════ 4 · LA FIESTA ══════════ -->
<section class="acto" id="fiesta">
  <div class="wrap">
    <!-- ⚠️ Acá había una copa dibujada a línea con hielos que caían.
         Se sacó a pedido de Fer: con la acuarela de las copas al lado
         eran dos copas seguidas diciendo lo mismo.
         ⚠️ Se saca ENTERA, no con `hidden`: la regla del navegador
         `[hidden]{display:none}` pierde contra `.dibujo{display:block}`
         y la copa se seguía viendo igual. -->
    <img class="acuarela rev" src="__COPAS__" style="max-width:300px;margin:0 auto" alt="">
    <img class="acuarela rev" src="__LUCES__" style="max-width:460px;margin-top:26px" alt="">
    <p class="rot rev" style="margin-top:22px">La fiesta</p>
    <h2 class="rev">En el mismo <em>lugar</em></h2>
    <div class="dato rev">
      <p class="hora">20:00</p>
      <p class="donde">A unos metros del lago</p>
    </div>
  </div>
</section>

<!-- ══════════ 5 · DRESS CODE ══════════ -->
<section class="acto junto" id="vestimenta">
  <div class="wrap">
    <!-- ⚠️ Acá iba la vela y no tenía nada que ver con el dress code.
         Falta la ilustración nueva: una flor de ojal con su alfiler. -->
    <p class="rot rev">Dress code</p>
    <h2 class="rev"><em>Elegante</em></h2>
  </div>
</section>

<!-- ══════════ 6 · REGALOS ══════════ -->
<section class="acto junto" id="regalos">
  <div class="wrap">
    <img class="motivo rev" src="__NARANJAS__" style="width:180px" alt="">
    <p class="rot rev" style="margin-top:8px">Si quer&eacute;s hacernos un regalo</p>
    <h2 class="rev">Ac&aacute; est&aacute; el <em>alias</em></h2>
    <div class="alias rev">
      <span id="alias" data-falta>guille.seba.boda</span>
      <button id="copiar" type="button">Copiar</button>
    </div>
  </div>
</section>

<img class="sep rev" src="__RAMO__" alt="" aria-hidden="true" style="width:82px">

<!-- ══════════ 7 · CONFIRMAR ══════════ -->
<section class="acto junto" id="rsvp">
  <div class="wrap">
    <img class="motivo rev" src="__OLIVO__" style="width:150px" alt="">
    <p class="rot rev">Queremos contar con vos</p>
    <h2 class="rev">Confirm&aacute; tu <em>lugar</em></h2>
    <p class="rev" style="margin-top:16px;color:var(--tinta-2);font-size:.95rem">
      Antes del 18 de febrero de 2027</p>
    <a class="btn lleno rev" id="btn-rsvp" href="#" data-falta>Confirmar asistencia</a>
  </div>
</section>

<footer>
  Guillermina &amp; Sebasti&aacute;n &middot; 3 de abril de 2027<br>
  <a href="https://www.invitacionesdigitalesoficial.com/?utm_source=invitacion&amp;utm_medium=footer&amp;utm_content=marca"
     target="_blank" rel="noopener">Invitaciones Digitales Oficial</a>
</footer>

<!-- "Sarà perché ti amo" — 46s desde el 0:28, mono, 96 kbps, 539 KB.
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
function petalos(cont,n){
  for(let i=0;i<n;i++){
    const s=document.createElementNS('http://www.w3.org/2000/svg','svg');
    const w=7+Math.random()*8;
    s.setAttribute('viewBox','0 0 20 26');
    s.setAttribute('width',w); s.setAttribute('height',w*1.3);
    s.innerHTML='<path d="M10 0C15.5 6 19 13 16.5 19.5C14.6 24.4 11.8 26 10 26C8.2 26 5.4 24.4 3.5 19.5C1 13 4.5 6 10 0Z"/>';
    s.style.fill=COL[i%COL.length]; s.classList.add('p');
    s.style.left=(Math.random()*94)+'%';
    s.style.setProperty('--dx',(Math.random()*90-45)+'px');
    s.style.setProperty('--giro',(Math.random()*540-270)+'deg');
    s.style.animationDuration=(9+Math.random()*8).toFixed(1)+'s';
    s.style.animationDelay=(-Math.random()*15).toFixed(1)+'s';
    s.style.opacity=(.3+Math.random()*.3).toFixed(2);
    cont.appendChild(s);
  }
}
petalos(document.getElementById('petalos-portada'),11);

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
  const dia = 86400000;
  const hoy = new Date();
  const faltan = Math.ceil((BODA - hoy) / dia);
  const c = document.getElementById('cuenta');
  if (faltan < 0) return;                       // ya pasó: no se muestra
  document.getElementById('cuenta-n').textContent = faltan;
  document.getElementById('cuenta-t').textContent =
    faltan === 0 ? 'es hoy' : faltan === 1 ? 'día' : 'días';
  c.hidden = false;
})();

/* ── Cada sección aparece al entrar en pantalla ──────────────────── */
const ojo=new IntersectionObserver(es=>{
  es.forEach(e=>{ if(e.isIntersecting){
    e.target.classList.add('on');
    e.target.querySelectorAll('.rev').forEach((el,i)=>
      setTimeout(()=>el.classList.add('on'), i*130));
    if(e.target.id==='ceremonia'){
      const c=document.getElementById('petalos-ceremonia');
      if(!c.childElementCount) petalos(c,9);
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
</body>
</html>
'''

CLAVES = {'etiqueta':'ETIQUETA','ellos':'ELLOS','altar':'ALTAR','mapa':'MAPA',
          'luces':'LUCES','vela':'VELA','ramo':'RAMO','olivo':'OLIVO',
          'naranjas':'NARANJAS','copas':'COPAS','aperol':'APEROL'}
for k, v in IM.items():
    HTML = HTML.replace('__' + CLAVES[k] + '__', v)
HTML = (HTML.replace('__VB_ESC__', VB_ESC).replace('__T_ESC__', T_ESC)
            .replace('__VB_CAR__', VB_CAR).replace('__T_CAR__', T_CAR))
sobran = [c for c in CLAVES.values() if '__'+c+'__' in HTML]
if sobran: print('⚠️ marcadores sin usar:', sobran)

io.open(f"{BASE}/cliente-guille-invitacion.html", 'w', encoding='utf-8').write(HTML)
print('\ncliente-guille-invitacion.html', len(HTML)//1024, 'KB')
