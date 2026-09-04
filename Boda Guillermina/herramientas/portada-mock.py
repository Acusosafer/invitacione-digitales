# -*- coding: utf-8 -*-
"""
La portada de Guillermina: la etiqueta colgada, con los nombres encima.

La pregunta que contesta es una sola: ¿entra la caligrafía adentro de la
etiqueta y se lee? Eso no se sabe mirando la acuarela sola.

⚠️ El rectángulo interior de la etiqueta está MEDIDO sobre la imagen
(la línea terracota), no estimado a ojo: 8,1% / 88,6% del ancho y
27,9% / 85,3% del alto de la imagen recortada.
"""
import io, base64
from PIL import Image

# ⚠️ Va el PNG SIN FONDO, no la acuarela con su papel blanco y multiply:
# la etiqueta se voltea, voltearse pide `perspective`, y `perspective`
# abre un stacking context desde donde el multiply se mezcla contra la
# nada y reaparece el rectángulo blanco. Ver `sacar-fondo`.
im = Image.open('etiqueta-lista.png')
b = io.BytesIO(); im.save(b, 'WEBP', quality=88, method=6)
ETI = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
print('etiqueta', im.size, len(b.getvalue())//1024, 'KB')

HTML = '''<!DOCTYPE html>
<html lang="es-AR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Portada</title>
<link href="https://fonts.googleapis.com/css2?family=Parisienne&family=Marcellus&family=Jost:wght@300;400&display=swap" rel="stylesheet">
<style>
:root{--terracota:#A84F2A; --tinta:#3A302A; --tinta-2:#6E6055; --papel:#F6F2E8;
      --avena:#D7C3A1; --naranja:#E07A1F; --hondo:#A0451A;}
*{box-sizing:border-box;margin:0}
html,body{height:100%}
body{background:var(--papel); font-family:'Jost',sans-serif; overflow:hidden}

/* El papel de algodón: dos capas en multiply, la fibra y la nube. */
.fibra,.nube{position:fixed; inset:0; pointer-events:none; mix-blend-mode:multiply; z-index:2}
.fibra{opacity:.5;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='f'><feTurbulence type='fractalNoise' baseFrequency='.92' numOctaves='4'/><feColorMatrix type='saturate' values='0'/></filter><rect width='220' height='220' filter='url(%23f)' opacity='.42'/></svg>")}
.nube{opacity:.28;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='560' height='560'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.012' numOctaves='3'/><feColorMatrix type='saturate' values='0'/></filter><rect width='560' height='560' filter='url(%23n)' opacity='.5'/></svg>")}

.pantalla{position:relative; height:100dvh; display:flex; flex-direction:column;
  align-items:center; justify-content:center; gap:0; z-index:1}

/* El cordel sigue hacia arriba hasta salirse de la pantalla: la etiqueta
   cuelga de algo, no flota.
   ⚠️ Va con `bottom:100%` colgado de la etiqueta, NO con una altura en
   px calculada a ojo: así engancha exactamente donde termina el cordel
   pintado, en cualquier pantalla. Y del mismo ancho y color, o se ve un
   segundo hilo al lado del de la acuarela. */
.etiqueta::before{content:''; position:absolute; left:50%; bottom:100%;
  width:5px; margin-left:-2.5px; height:100vh;
  background:linear-gradient(180deg,#C6B69B,#A8977A);
  opacity:.9}

.colgante{transform-origin:50% -6%; animation:mecer 6.5s ease-in-out infinite}
@keyframes mecer{0%,100%{transform:rotate(-1.1deg)} 50%{transform:rotate(1.1deg)}}

.etiqueta{position:relative; width:212px; perspective:900px; cursor:pointer}
.cara{position:relative; transition:transform 900ms cubic-bezier(.22,.61,.36,1);
  transform-style:preserve-3d}
.volteada .cara{transform:rotateY(180deg)}
.etiqueta img{width:100%; display:block}

/* ⚠️ El rectángulo interior está MEDIDO sobre la acuarela, no estimado:
   la línea terracota va del 8,1% al 88,6% del ancho y del 27,9% al 85,3%
   del alto. Los nombres van adentro de eso, con aire. */
.escrito{position:absolute; left:11.9%; right:11.7%; top:25.6%; bottom:14.8%;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  padding:10px 6px; text-align:center; backface-visibility:hidden}
.dorso{transform:rotateY(180deg)}
.dorso .escrito{backface-visibility:hidden}

.nom{font-family:'Parisienne',cursive; color:var(--terracota); line-height:.98}
.n1{font-size:26px}
.amp{font-size:20px; margin:0; opacity:.85}
.n2{font-size:26px; margin-top:0}

.dat{font-family:'Marcellus',serif; color:var(--tinta); text-transform:uppercase;
  letter-spacing:.16em; font-size:9.5px; line-height:2.1}
.dat .g{font-size:13px; letter-spacing:.1em; display:block; margin:6px 0}

.pie{margin-top:26px; text-align:center; z-index:1}
.pie .rot{font-family:'Marcellus',serif; font-size:9.5px; letter-spacing:.34em;
  text-transform:uppercase; color:var(--tinta-2)}
.pie .toca{font-family:'Jost',sans-serif; font-size:10.5px; letter-spacing:.2em;
  text-transform:uppercase; color:var(--hondo); margin-top:9px; opacity:.75}

/* Los pétalos. Son los que les van a tirar después de la ceremonia. */
.petalos{position:absolute; inset:0; pointer-events:none; z-index:0}
.p{position:absolute; top:-10%; animation:caer linear infinite}
@keyframes caer{
  0%{transform:translate3d(0,-40px,0) rotate(0);opacity:0}
  12%{opacity:.8} 85%{opacity:.65}
  100%{transform:translate3d(var(--dx),105vh,0) rotate(var(--giro));opacity:0}}
</style></head><body>
<div class="fibra"></div><div class="nube"></div>
<div class="pantalla">
  <div class="petalos" id="petalos"></div>
  <div class="colgante">
    <div class="etiqueta" id="eti">
      <div class="cara">
        <img src="__ETI__" alt="">
        <div class="escrito">
          <div class="nom n1">Guillermina</div>
          <div class="nom amp">&amp;</div>
          <div class="nom n2">Sebasti&aacute;n</div>
        </div>
        <div class="escrito dorso">
          <div class="dat">
            S&aacute;bado
            <span class="g">3 &middot; IV &middot; 2027</span>
            Finca<br>La Josefina<br>Berisso
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="pie">
    <div class="rot">Pr&oacute;ximo destino</div>
    <div class="toca">Toc&aacute; la etiqueta</div>
  </div>
</div>
<script>
const c=document.getElementById('petalos');
const COL=['#E07A1F','#A84F2A','#D7C3A1','#A0451A','#C98B5A'];
for(let i=0;i<11;i++){
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
  c.appendChild(s);
}
document.getElementById('eti').onclick=e=>e.currentTarget.classList.toggle('volteada');
</script></body></html>'''

HTML = HTML.replace('__ETI__', ETI)
io.open('portada-mock.html', 'w', encoding='utf-8').write(HTML)
print('portada-mock.html', len(HTML)//1024, 'KB')
