# -*- coding: utf-8 -*-
"""
El dibujo de línea ENCIMA de la acuarela — dos formas, para elegir.

  A · El trazo se dibuja sobre la acuarela, que ya está a la vista.
  B · El trazo se dibuja sobre el papel en blanco y, cuando termina,
      la acuarela aparece por debajo: el dibujo se pinta solo.

⚠️ El trazado salió de la acuarela ANTERIOR (antes del pelo). Encima de
la nueva, el pelo de ella no coincide. Se ve en A y no en B.
"""
import io, base64
from PIL import Image

BASE = r"c:/Users/F&F/.gemini/antigravity/scratch/Web invitación"
esc = io.open('svg-escena.txt', encoding='utf-8').read().split('\n', 1)
# ⚠️ Los trazos vienen con class="t" del generador; acá la clase es .trazo
VB, TRAZOS = esc[0], esc[1].replace('class="t"', 'class="trazo"')

im = Image.open(f"{BASE}/Boda Guillermina/web/pelo mas largo.jpg").convert('RGB')
im = im.resize((760, round(760*im.height/im.width)), Image.LANCZOS)
b = io.BytesIO(); im.save(b, 'JPEG', quality=82, optimize=True, progressive=True)
ACU = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

HTML = '''<!DOCTYPE html>
<html lang="es-AR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>El trazo sobre la acuarela</title>
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root{--hondo:#A0451A;--terracota:#A84F2A;--papel:#F6F2E8;--tinta:#3A302A;
      --tinta-2:#6B5D51;--ease:cubic-bezier(.22,.61,.36,1)}
*{box-sizing:border-box;margin:0}
body{background:var(--papel);color:var(--tinta);font-family:'Jost',sans-serif;
  line-height:1.7;padding:34px 18px 90px}
.fibra,.nube{position:fixed;inset:0;pointer-events:none;z-index:9;mix-blend-mode:multiply}
.fibra{opacity:.5;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='f'><feTurbulence type='fractalNoise' baseFrequency='.92' numOctaves='4'/><feColorMatrix type='saturate' values='0'/></filter><rect width='220' height='220' filter='url(%23f)' opacity='.42'/></svg>")}
.nube{opacity:.28;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='560' height='560'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.012' numOctaves='3'/><feColorMatrix type='saturate' values='0'/></filter><rect width='560' height='560' filter='url(%23n)' opacity='.5'/></svg>")}
.wrap{max-width:660px;margin:0 auto;position:relative;z-index:1}
h1{font-family:'Marcellus',serif;font-weight:400;font-size:clamp(1.4rem,5.6vw,1.9rem)}
.kicker{font-family:'Marcellus',serif;font-size:.62rem;letter-spacing:.3em;
  text-transform:uppercase;color:var(--hondo)}
h2{font-family:'Marcellus',serif;font-weight:400;font-size:1.1rem;margin-bottom:4px}
p.n{color:var(--tinta-2);font-size:.9rem;max-width:52ch}
.caso{margin-top:44px;padding-top:26px;border-top:1px solid rgba(160,69,26,.16)}

.escena{position:relative;margin-top:18px}
.escena img{width:100%;display:block;mix-blend-mode:multiply;
  transition:opacity 1.4s var(--ease)}
.escena svg{position:absolute;inset:0;width:100%;height:100%}
.trazo{fill:none;stroke:var(--terracota);stroke-width:1.1;
  stroke-linecap:round;stroke-linejoin:round}

/* A · la acuarela está desde el principio */
#a img{opacity:1}
/* B · la acuarela entra cuando el trazo terminó */
#b img{opacity:0}
#b.pintada img{opacity:1}
/* y el trazo se va apagando: queda la acuarela sola */
#b.pintada svg{opacity:0;transition:opacity 1.6s var(--ease) .5s}

.bt{margin-top:18px;font-family:'Marcellus',serif;font-size:.68rem;
  letter-spacing:.2em;text-transform:uppercase;color:var(--hondo);
  background:transparent;border:1px solid rgba(160,69,26,.4);border-radius:999px;
  padding:13px 26px;min-height:44px;cursor:pointer}
.bt:active{transform:scale(.98)}
@media (prefers-reduced-motion:reduce){.trazo{stroke-dashoffset:0!important}}
</style></head><body>
<div class="fibra"></div><div class="nube"></div>
<div class="wrap">
  <div class="kicker">Boda Guillermina &middot; prueba</div>
  <h1>El trazo sobre la acuarela</h1>
  <p class="n" style="margin-top:10px">Las dos formas, con el mismo dibujo
    de 201 trazos. Baj&aacute; despacio: cada una arranca al entrar en pantalla.</p>

  <div class="caso">
    <h2>A &middot; El trazo encima de la acuarela</h2>
    <p class="n">La acuarela est&aacute; a la vista desde el principio y la
      l&iacute;nea se dibuja arriba.</p>
    <div class="escena" id="a">
      <img src="__ACU__" alt="">
      <svg viewBox="__VB__" aria-hidden="true">__TRAZOS__</svg>
    </div>
    <button class="bt" data-para="a">Dibujar de nuevo</button>
  </div>

  <div class="caso">
    <h2>B &middot; Primero el trazo, despu&eacute;s el color</h2>
    <p class="n">El papel arranca en blanco. Cuando la l&iacute;nea termina,
      la acuarela aparece por debajo y el trazo se apaga: el dibujo se pinta solo.</p>
    <div class="escena" id="b">
      <img src="__ACU__" alt="">
      <svg viewBox="__VB__" aria-hidden="true">__TRAZOS__</svg>
    </div>
    <button class="bt" data-para="b">Dibujar de nuevo</button>
  </div>
</div>

<script>
/* ⚠️⚠️ "El primer trazo no se dibuja" volvió TRES veces y cada vez la
   causa fue otra. Esta es la versión que funciona:
     1 · UNA sola función para arrancar, siempre.
     2 · Leer getComputedStyle(t).strokeDashoffset de CADA trazo — leer
         offsetWidth fuerza el layout, y stroke-dashoffset es pintado: el
         navegador puede saltearse el recálculo. Y arrancar adentro de un
         doble requestAnimationFrame.
     3 · transition:'none' EXPLÍCITO al preparar. transition-property vale
         'all' por defecto, así que el transitionDuration que dejó el
         ciclo anterior sobrevive y el reset a "escondido" también
         transiciona: el trazo nunca llega a estar vacío. */
function dibujar(caja, demora, duracion){
  const t = [...caja.querySelectorAll('.trazo')];
  caja.classList.remove('pintada');
  t.forEach(x=>{
    x.style.transition='none';
    const L=x.getTotalLength();
    x.style.strokeDasharray=L; x.style.strokeDashoffset=L;
  });
  t.forEach(x=>getComputedStyle(x).strokeDashoffset);   // ⚠️ no sacar
  requestAnimationFrame(()=>requestAnimationFrame(()=>{
    t.forEach((x,i)=>{
      x.style.transition='';
      x.style.transitionProperty='stroke-dashoffset';
      x.style.transitionTimingFunction='cubic-bezier(.22,.61,.36,1)';
      x.style.transitionDuration=duracion+'ms';
      setTimeout(()=>{x.style.strokeDashoffset='0';}, i*demora);
    });
    setTimeout(()=>caja.classList.add('pintada'), t.length*demora + duracion + 200);
  }));
}
const D=14, DUR=520;
const ojo=new IntersectionObserver((es,o)=>es.forEach(e=>{
  if(e.isIntersecting){ o.unobserve(e.target); dibujar(e.target,D,DUR); }
}),{threshold:.3});
document.querySelectorAll('.escena').forEach(e=>ojo.observe(e));
document.querySelectorAll('.bt').forEach(b=>b.onclick=()=>
  dibujar(document.getElementById(b.dataset.para),D,DUR));
</script></body></html>'''

HTML = (HTML.replace('__ACU__', ACU).replace('__VB__', VB)
            .replace('__TRAZOS__', TRAZOS))
io.open(f"{BASE}/cliente-guille-trazo.html", 'w', encoding='utf-8').write(HTML)
print('cliente-guille-trazo.html', len(HTML)//1024, 'KB')
