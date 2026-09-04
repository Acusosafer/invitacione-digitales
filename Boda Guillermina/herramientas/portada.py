# -*- coding: utf-8 -*-
"""
LA PORTADA · segunda vuelta

Dos cambios pedidos por Fer:

1. ⚠️ NADA DE SOGA DIBUJADA CON CSS. Se veía el empalme: una soga que
   bajaba y de golpe pasaba a las dos hebras de la acuarela. Ahora la
   imagen se ancla ARRIBA DE TODO y su propio corte queda fuera de la
   pantalla: la soga entra desde afuera y no hay nada que empalmar.
   El 27% de arriba de la imagen es soga; con eso alcanza.

2. La entrada. UN SOLO TOQUE: la etiqueta gira, muestra la fecha y el
   lugar, y después sube y se va — y abajo ya está la invitación.
   ⚠️ La música arranca en el manejador del toque, no en el timeout:
   el permiso del navegador viene del gesto, no del reloj.
"""
import io, base64
from PIL import Image

im = Image.open('etiqueta-lista.png')
b = io.BytesIO(); im.save(b, 'WEBP', quality=88, method=6)
ETI = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()

lago = Image.open(r"c:/Users/F&F/.gemini/antigravity/scratch/Web invitación/Boda Guillermina/web/pelo mas largo.jpg").convert('RGB')
lago = lago.resize((760, round(760*lago.height/lago.width)), Image.LANCZOS)
b2 = io.BytesIO(); lago.save(b2, 'JPEG', quality=80, optimize=True, progressive=True)
LAGO = 'data:image/jpeg;base64,' + base64.b64encode(b2.getvalue()).decode()
print('etiqueta', len(b.getvalue())//1024, 'KB   lago', len(b2.getvalue())//1024, 'KB')

HTML = '''<!DOCTYPE html>
<html lang="es-AR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>La portada &middot; Guillermina &amp; Sebasti&aacute;n</title>
<link href="https://fonts.googleapis.com/css2?family=Parisienne&family=Marcellus&family=Jost:wght@300;400&display=swap" rel="stylesheet">
<style>
:root{--terracota:#A84F2A;--tinta:#3A302A;--tinta-2:#6E6055;--papel:#F6F2E8;
      --hondo:#A0451A;--ease:cubic-bezier(.22,.61,.36,1)}
*{box-sizing:border-box;margin:0}
html,body{height:100%}
body{background:var(--papel);font-family:'Jost',sans-serif;overflow:hidden;color:var(--tinta)}
body.adentro{overflow:auto}

.fibra,.nube{position:fixed;inset:0;pointer-events:none;mix-blend-mode:multiply;z-index:5}
.fibra{opacity:.5;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='f'><feTurbulence type='fractalNoise' baseFrequency='.92' numOctaves='4'/><feColorMatrix type='saturate' values='0'/></filter><rect width='220' height='220' filter='url(%23f)' opacity='.42'/></svg>")}
.nube{opacity:.28;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='560' height='560'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.012' numOctaves='3'/><feColorMatrix type='saturate' values='0'/></filter><rect width='560' height='560' filter='url(%23n)' opacity='.5'/></svg>")}

/* ── LA PORTADA ─────────────────────────────────────────────────────
   ⚠️ La etiqueta va anclada ARRIBA DE TODO, con su corte de soga fuera
   de la pantalla. Nada de dibujarle una soga con CSS: el empalme se ve
   siempre, por mejor que se elija el color. */
.portada{position:fixed;inset:0;z-index:4;background:var(--papel);
  transition:opacity 600ms linear}
.portada.ida{opacity:0;pointer-events:none}

.colgante{position:absolute;left:50%;top:-42px;width:246px;margin-left:-123px;
  transform-origin:50% 0;animation:mecer 7s ease-in-out infinite}
@keyframes mecer{0%,100%{transform:rotate(-1deg)}50%{transform:rotate(1deg)}}
/* ⚠️ La etiqueta NO se desvanece mientras sube. Antes se iba en opacidad
   al mismo tiempo que el papel de la portada, así que se apagaba en el
   lugar y el viaje no se veía NUNCA. Sube entera, y el papel recién se
   apaga cuando ya salió de la pantalla.
   Y arranca con una caidita: es alguien tirando del cordel, y una soga
   de verdad cede un instante antes de levantar. */
.colgante.sube{animation:levantar 1150ms cubic-bezier(.5,0,.75,.35) forwards}
@keyframes levantar{
  0%  {transform:translateY(0) rotate(0)}
  9%  {transform:translateY(11px) rotate(.6deg)}
  100%{transform:translateY(-155%) rotate(-2.5deg)}
}

/* Pantalla corta (un SE, o cualquier celular con la barra del navegador
   comiendose 120px): la etiqueta pisaba el pie. */
@media (max-height:760px){
  .colgante{width:210px;margin-left:-105px;top:-34px}
  .n1,.n2{font-size:23px} .amp{font-size:18px}
}
.etiqueta{position:relative;width:100%;perspective:1000px;cursor:pointer}
.cara{position:relative;transition:transform 900ms var(--ease);transform-style:preserve-3d}
.volteada .cara{transform:rotateY(180deg)}
.etiqueta img{width:100%;display:block}

/* El rectángulo interior, MEDIDO sobre la acuarela: la línea terracota
   va del 11,9% al 88,3% del ancho y del 25,6% al 85,2% del alto. */
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
/* Un solo empujoncito a los 6 segundos, no un latido eterno. */
.pie .toca.avisa{animation:latir 1.5s ease-in-out 2}
@keyframes latir{50%{opacity:.28}}

.petalos{position:absolute;inset:0;pointer-events:none;z-index:-1}
.p{position:absolute;top:-10%;animation:caer linear infinite}
@keyframes caer{0%{transform:translate3d(0,-40px,0) rotate(0);opacity:0}
  12%{opacity:.8}85%{opacity:.65}
  100%{transform:translate3d(var(--dx),105vh,0) rotate(var(--giro));opacity:0}}

/* ── LO QUE HAY ABAJO (acto 1, sólo para ver el pase) ─────────────── */
.acto{min-height:100dvh;display:flex;flex-direction:column;align-items:center;
  justify-content:center;text-align:center;padding:60px 26px;gap:22px}
.acto img{width:100%;max-width:520px;border-radius:3px;
  box-shadow:0 18px 40px -28px rgba(58,48,42,.55)}
.acto .antes{font-family:'Marcellus',serif;font-size:.62rem;letter-spacing:.32em;
  text-transform:uppercase;color:var(--tinta-2)}
.acto .relato{font-size:.98rem;line-height:1.85;color:var(--tinta-2);max-width:34ch}
.acto h1{font-family:'Parisienne',cursive;color:var(--terracota);font-weight:400;
  font-size:clamp(2.2rem,11vw,3rem);line-height:1.05}
</style></head><body>
<div class="fibra"></div><div class="nube"></div>

<div class="portada" id="portada">
  <div class="petalos" id="petalos"></div>
  <div class="colgante" id="colgante">
    <div class="etiqueta" id="eti">
      <div class="cara">
        <img src="__ETI__" alt="">
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

<section class="acto">
  <p class="antes">Antes de nuestro para siempre</p>
  <img src="__LAGO__" alt="">
  <p class="relato">Ella, siempre buscando un destino nuevo.<br>
    &Eacute;l, descubriendo el mundo al lado de ella.<br><br>
    Despu&eacute;s de tantos caminos, encontramos el lugar
    donde queremos empezar el pr&oacute;ximo.</p>
  <h1>Guillermina y Sebasti&aacute;n</h1>
</section>

<script>
const c=document.getElementById('petalos');
const COL=['#E07A1F','#A84F2A','#D7C3A1','#A0451A','#C98B5A'];
for(let i=0;i<11;i++){
  const s=document.createElementNS('http://www.w3.org/2000/svg','svg');
  const w=7+Math.random()*8;
  s.setAttribute('viewBox','0 0 20 26');s.setAttribute('width',w);s.setAttribute('height',w*1.3);
  s.innerHTML='<path d="M10 0C15.5 6 19 13 16.5 19.5C14.6 24.4 11.8 26 10 26C8.2 26 5.4 24.4 3.5 19.5C1 13 4.5 6 10 0Z"/>';
  s.style.fill=COL[i%COL.length];s.classList.add('p');
  s.style.left=(Math.random()*94)+'%';
  s.style.setProperty('--dx',(Math.random()*90-45)+'px');
  s.style.setProperty('--giro',(Math.random()*540-270)+'deg');
  s.style.animationDuration=(9+Math.random()*8).toFixed(1)+'s';
  s.style.animationDelay=(-Math.random()*15).toFixed(1)+'s';
  s.style.opacity=(.3+Math.random()*.3).toFixed(2);
  c.appendChild(s);
}

/* UN SOLO TOQUE: gira, deja leer la fecha, y se va.
   ⚠️ La música tiene que arrancar ACÁ ADENTRO, en el gesto. Llamar a
   play() desde el setTimeout es llamarlo sin gesto, y el navegador lo
   bloquea.

   Los tiempos, en orden y sin pisarse:
     0      toque · empieza a girar
     900    terminó de girar · empieza a leerse la fecha
     3400   sube — 2,5 segundos de lectura contados desde que quedó dada
            vuelta, NO desde el toque
     4290   ya salió de la pantalla: recién ahí se apaga el papel */
const GIRO=900, LEER=2500, SUBE=1150;
let abierto=false;
document.getElementById('eti').onclick=()=>{
  if(abierto) return; abierto=true;
  // audio.play();  ← acá va la música
  document.getElementById('eti').classList.add('volteada');
  document.getElementById('pie').classList.add('ida');
  setTimeout(()=>{
    document.getElementById('colgante').classList.add('sube');
  }, GIRO+LEER);
  setTimeout(()=>{
    document.getElementById('portada').classList.add('ida');
    document.body.classList.add('adentro');
  }, GIRO+LEER+SUBE-260);
};
// Un empujoncito a los 6 segundos, una sola vez.
setTimeout(()=>{ if(!abierto) document.getElementById('toca').classList.add('avisa'); },6000);
</script></body></html>'''

HTML = HTML.replace('__ETI__', ETI).replace('__LAGO__', LAGO)
io.open(r"c:/Users/F&F/.gemini/antigravity/scratch/Web invitación/cliente-guille-portada.html",
        'w', encoding='utf-8').write(HTML)
print('cliente-guille-portada.html', len(HTML)//1024, 'KB')
