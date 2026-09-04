# -*- coding: utf-8 -*-
"""Arma cliente-guille-color.html con las imagenes embebidas."""
import io, json

RAIZ = r"c:/Users/F&F/.gemini/antigravity/scratch/Web invitación"
P = json.load(open('piezas.json'))

HTML = r'''<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>El color de la letra · Guillermina &amp; Sebastián</title>

<!-- ══════════════════════════════════════════════════════════════════
     LAS TRES RESPUESTAS · muestra para la clienta

     Eligió la opción 4 (Parisienne) y preguntó tres cosas: el color de
     la letra, el pelo del dibujo, y si se pueden agregar flores.

     ⚠️ Autocontenida: `Boda Guillermina/` está en .vercelignore, así que
     las imágenes van EMBEBIDAS como data URI. No hay carpeta de assets.
     Se regenera con `armar-color.py`; los cambios a mano se pisan.

     ⚠️ Los pétalos no son una foto: caen de verdad, con un botón para
     apagarlos. La pregunta era "¿quedaría muy cargado?" y eso no se
     contesta describiéndolo.
     ══════════════════════════════════════════════════════════════════ -->

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Parisienne&family=Marcellus&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">

<style>
:root{
  --naranja:#E07A1F; --hondo:#A0451A; --terracota:#A84F2A;
  --oliva:#435F3A; --salvia:#A3B18A; --avena:#D7C3A1;
  --papel:#F6F2E8; --tinta:#3A302A; --tinta-2:#6E6055;
  --linea:rgba(160,69,26,.16);
}
*{box-sizing:border-box}
body{margin:0; background:var(--papel); color:var(--tinta);
  font-family:'Jost',system-ui,sans-serif; line-height:1.6;
  padding:34px 18px 80px; overflow-x:hidden}

/* El papel de algodón, igual que en las otras muestras. feTurbulence da
   ruido A COLOR: sin el feColorMatrix sale manchado de verde y rosa. */
.fibra,.nube{position:fixed; inset:0; pointer-events:none; z-index:9;
  mix-blend-mode:multiply}
.fibra{opacity:.5;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='f'><feTurbulence type='fractalNoise' baseFrequency='.92' numOctaves='4'/><feColorMatrix type='saturate' values='0'/></filter><rect width='220' height='220' filter='url(%23f)' opacity='.42'/></svg>")}
.nube{opacity:.28;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='560' height='560'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.012' numOctaves='3'/><feColorMatrix type='saturate' values='0'/></filter><rect width='560' height='560' filter='url(%23n)' opacity='.5'/></svg>")}

.wrap{max-width:660px; margin:0 auto; position:relative; z-index:1}
header{text-align:center}
.kicker{font-family:'Marcellus',serif; font-size:.64rem; letter-spacing:.3em;
  text-transform:uppercase; color:var(--hondo)}
h1{font-family:'Marcellus',serif; font-weight:400; margin:14px 0 0;
  font-size:clamp(1.5rem,6vw,2rem); line-height:1.2}
.bajada{max-width:46ch; margin:12px auto 0; color:var(--tinta-2);
  font-size:.92rem; text-align:center}

h2{font-family:'Marcellus',serif; font-weight:400; font-size:1.15rem;
  margin:0 0 6px; line-height:1.3}
.paso{margin-top:52px; padding-top:26px; border-top:1px solid var(--linea)}
.paso .n{font-family:'Marcellus',serif; font-size:.6rem; letter-spacing:.28em;
  text-transform:uppercase; color:var(--hondo)}
.paso p{color:var(--tinta-2); font-size:.93rem; max-width:52ch; margin:10px 0 0}
.paso p b{color:var(--tinta); font-weight:500}

/* ── Las tarjetas de color ─────────────────────────────────────────── */
.op{margin-top:22px; padding:24px 18px 20px; text-align:center;
  background:#FFFDF9; border:1px solid rgba(58,48,42,.08); border-radius:8px}
.op.reco{border-color:rgba(160,69,26,.45); box-shadow:0 0 0 3px rgba(160,69,26,.06)}
.letra{font-family:'Marcellus',serif; font-size:.6rem; letter-spacing:.28em;
  text-transform:uppercase; color:var(--hondo)}
.sobre{font-family:'Marcellus',serif; font-size:.6rem; letter-spacing:.26em;
  text-transform:uppercase; margin-top:16px; color:var(--c)}
.nom{font-family:'Parisienne',cursive; line-height:1.02; margin:6px 0 2px;
  padding:0 4px; font-size:clamp(1.9rem,8.5vw,2.6rem); color:var(--c)}
.datos{font-family:'Marcellus',serif; font-size:.62rem; letter-spacing:.2em;
  text-transform:uppercase; margin-top:12px; line-height:2; color:var(--c)}
.pie{margin-top:16px; padding-top:12px; border-top:1px solid var(--linea);
  font-size:.72rem; color:#9A8C7D; letter-spacing:.04em}
.pie b{color:var(--hondo); font-weight:500}
.pie .ojo{color:#B0552A}

/* La recomendada mezcla: los nombres en color, lo demás en tinta */
.op.reco .sobre, .op.reco .datos{color:var(--tinta-2)}

/* ── Antes y después ──────────────────────────────────────────────── */
.par{display:grid; gap:14px; margin-top:20px}
@media (min-width:560px){ .par{grid-template-columns:1fr 1fr} }
.par figure{margin:0}
.par img{width:100%; display:block; border-radius:6px;
  border:1px solid rgba(58,48,42,.1)}
.par figcaption{font-family:'Marcellus',serif; font-size:.58rem;
  letter-spacing:.24em; text-transform:uppercase; color:var(--tinta-2);
  margin-top:8px; text-align:center}
.par .ahora figcaption{color:var(--hondo)}
.entera{margin:18px 0 0}
.entera img{width:100%; display:block; border-radius:6px;
  border:1px solid rgba(58,48,42,.1)}
.entera figcaption{font-size:.76rem; color:var(--tinta-2); margin-top:8px;
  text-align:center}

/* ── Los motivos que ya existen ───────────────────────────────────── */
.motivos{display:grid; grid-template-columns:repeat(3,1fr); gap:12px;
  margin-top:20px; align-items:end}
.motivos img{width:100%; display:block; mix-blend-mode:multiply}

/* ── Los pétalos, cayendo de verdad ───────────────────────────────── */
.demo{margin-top:22px; position:relative; overflow:hidden; border-radius:8px;
  background:#FFFDF9; border:1px solid rgba(58,48,42,.08);
  padding:44px 18px 40px; text-align:center; min-height:230px}
.demo .sobre2{font-family:'Marcellus',serif; font-size:.58rem;
  letter-spacing:.26em; text-transform:uppercase; color:var(--tinta-2)}
.demo .nom2{font-family:'Parisienne',cursive; color:var(--hondo);
  font-size:clamp(1.8rem,8vw,2.4rem); line-height:1.05; margin:6px 0 0}
.demo .dat2{font-family:'Marcellus',serif; font-size:.6rem; letter-spacing:.2em;
  text-transform:uppercase; color:var(--tinta-2); margin-top:12px}
/* ⚠️ Los pétalos van DETRÁS de la caligrafía. Un pétalo cruzando por
   arriba de los nombres se lee como un error, no como un detalle. */
.petalos{position:absolute; inset:0; pointer-events:none; z-index:0}
.demo .sobre2, .demo .nom2, .demo .dat2{position:relative; z-index:1}
.petalos.off{display:none}
.p{position:absolute; top:-8%; opacity:0;
   animation:caer linear infinite}
@keyframes caer{
  0%  {transform:translate3d(0,-40px,0) rotate(0deg);   opacity:0}
  12% {opacity:.85}
  85% {opacity:.7}
  100%{transform:translate3d(var(--dx),300px,0) rotate(var(--giro)); opacity:0}
}
.bt{margin-top:16px; font-family:'Jost',sans-serif; font-size:.7rem;
  letter-spacing:.18em; text-transform:uppercase; color:var(--hondo);
  background:transparent; border:1px solid var(--linea); border-radius:40px;
  padding:12px 22px; min-height:44px; cursor:pointer}
.bt:active{transform:scale(.98)}

.cierre{margin-top:44px; padding:20px 22px; border-radius:8px;
  background:rgba(224,122,31,.07); border:1px solid var(--linea)}
.cierre p{margin:0; font-size:.94rem; color:var(--tinta-2); max-width:54ch}
.cierre b{color:var(--tinta); font-weight:500}
.cierre p + p{margin-top:10px}

@media (prefers-reduced-motion:reduce){ .p{animation:none; display:none} }
</style>
</head>
<body>
<div class="fibra"></div><div class="nube"></div>

<div class="wrap">
  <header>
    <div class="kicker">Guillermina &amp; Sebastián</div>
    <h1>El color, el pelo y las flores</h1>
    <p class="bajada">
      Las tres cosas que preguntaron, contestadas acá abajo. La primera
      necesita que elijan una letra.
    </p>
  </header>

  <!-- ══ 1 · EL COLOR ══ -->
  <section class="paso">
    <div class="n">Primero</div>
    <h2>El color de la letra</h2>
    <p>
      Tienen razón, aunque por una razón distinta a la que parece: lo que
      vieron <b>no era negro</b>, era una tinta marrón oscura. Pero en el
      celular una caligrafía tan fina en un tono tan oscuro se lee dura
      igual. Estas son las que valen la pena. <b>Díganme una letra.</b>
    </p>

    <div class="op" style="--c:#3A302A">
      <div class="letra">A · Tinta cálida</div>
      <div class="sobre">Celebramos la boda de</div>
      <div class="nom">Guillermina &amp; Sebastián</div>
      <div class="datos">Sábado 3 de abril 2027<br>Finca La Josefina · Berisso</div>
      <div class="pie">La que vieron. Marrón muy oscuro, no negro.</div>
    </div>

    <div class="op" style="--c:#A0451A">
      <div class="letra">B · Bordó</div>
      <div class="sobre">Celebramos la boda de</div>
      <div class="nom">Guillermina &amp; Sebastián</div>
      <div class="datos">Sábado 3 de abril 2027<br>Finca La Josefina · Berisso</div>
      <div class="pie">El naranja quemado de la paleta. <b>Es el que yo elegiría.</b></div>
    </div>

    <div class="op" style="--c:#A84F2A">
      <div class="letra">C · Terracota</div>
      <div class="sobre">Celebramos la boda de</div>
      <div class="nom">Guillermina &amp; Sebastián</div>
      <div class="datos">Sábado 3 de abril 2027<br>Finca La Josefina · Berisso</div>
      <div class="pie">Un paso más cálido y más claro que el bordó.</div>
    </div>

    <div class="op" style="--c:#435F3A">
      <div class="letra">D · Olivo</div>
      <div class="sobre">Celebramos la boda de</div>
      <div class="nom">Guillermina &amp; Sebastián</div>
      <div class="datos">Sábado 3 de abril 2027<br>Finca La Josefina · Berisso</div>
      <div class="pie">El verde de la paleta. Más sereno, menos otoñal.</div>
    </div>

    <div class="op" style="--c:#E07A1F">
      <div class="letra">E · Clementina</div>
      <div class="sobre">Celebramos la boda de</div>
      <div class="nom">Guillermina &amp; Sebastián</div>
      <div class="datos">Sábado 3 de abril 2027<br>Finca La Josefina · Berisso</div>
      <div class="pie"><span class="ojo">Ojo:</span> es la que se ve más
        finita, pero también la que peor se lee — al sol, de lejos, o en
        una pantalla con poco brillo.</div>
    </div>

    <div class="op reco" style="--c:#A0451A">
      <div class="letra">F · Bordó sólo en los nombres</div>
      <div class="sobre">Celebramos la boda de</div>
      <div class="nom">Guillermina &amp; Sebastián</div>
      <div class="datos">Sábado 3 de abril 2027<br>Finca La Josefina · Berisso</div>
      <div class="pie"><b>Mi recomendación.</b> El color en los nombres y
        la letra chica en tinta: los nombres se despegan y la información
        se sigue leyendo cómoda.</div>
    </div>

    <p style="margin-top:22px">
      Una aclaración honesta sobre <b>“más finita”</b>: la Parisienne
      viene en un solo grosor, así que no se puede afinar de verdad. Lo
      que sí cambia el peso visual es el color — cuanto más claro, más
      liviana se ve. Por eso la E parece la más fina, y por eso también es
      la más floja de leer. Si la quieren <i>de verdad</i> más fina, hay
      que cambiar de letra (la 2 y la 5 eran las delgadas), pero pierden
      esta que les gustó.
    </p>
  </section>

  <!-- ══ 2 · EL PELO ══ -->
  <section class="paso">
    <div class="n">Segundo</div>
    <h2>El pelo</h2>
    <p>
      Hecho: él un poco más oscuro, ella un poco más largo. <b>No volví a
      generar el dibujo</b> — lo retoqué. Si lo generaba de nuevo cambiaba
      la escena entera: otro atardecer, otro muelle, otras sillas. Lo que
      les gustó es este dibujo, así que se tocó el pelo y nada más.
    </p>
    <div class="par">
      <figure><img src="__ANTES__" alt="El pelo como estaba">
        <figcaption>Como estaba</figcaption></figure>
      <figure class="ahora"><img src="__AHORA__" alt="El pelo cambiado">
        <figcaption>Ahora</figcaption></figure>
    </div>
    <figure class="entera">
      <img src="__ENTERA__" alt="El dibujo entero con el pelo cambiado">
      <figcaption>Y así queda el dibujo entero — lo demás no se tocó</figcaption>
    </figure>
    <p style="margin-top:16px">
      Si quieren más —el pelo bastante más largo, o él bastante más
      oscuro— díganmelo y lo empujo un poco más. Preferí quedarme corto:
      es más fácil agregar que volver atrás.
    </p>
  </section>

  <!-- ══ 3 · LAS FLORES ══ -->
  <section class="paso">
    <div class="n">Tercero</div>
    <h2>Las flores, los pétalos y las copas</h2>
    <p>
      <b>No queda cargado, pero no van adentro de ese dibujo.</b> Esa
      acuarela ya está llena: el atardecer, los árboles, el muelle, las
      luces, las sillas. Meterle flores encima le saca el aire que es
      justo lo que la hace linda.
    </p>
    <p style="margin-top:14px">
      Van <b>repartidas por la invitación</b>, una por sección — y de eso
      ya hay doce dibujadas con el mismo pincel, esperando su lugar:
    </p>
    <div class="motivos">
      <img src="__RAMO__" alt="El ramo">
      <img src="__COPAS__" alt="Las copas del brindis">
      <img src="__OLIVO__" alt="La rama de olivo">
    </div>

    <p style="margin-top:24px">
      Y los <b>pétalos cayendo</b> sí, pero como pasa en la pantalla, no
      pintados. Miren:
    </p>

    <div class="demo">
      <div class="petalos" id="petalos"></div>
      <div class="sobre2">Celebramos la boda de</div>
      <div class="nom2">Guillermina &amp; Sebastián</div>
      <div class="dat2">Sábado 3 de abril 2027</div>
    </div>
    <div style="text-align:center"><button class="bt" id="bt">Apagar los pétalos</button></div>

    <p style="margin-top:18px">
      Mi consejo: que caigan <b>en un solo momento</b> —al abrir la
      invitación— y después paren. Todo el tiempo y en todas las secciones
      cansa, y además compite con los dibujos que se dibujan solos, que
      es lo que de verdad no tiene nadie.
    </p>
  </section>

  <div class="cierre">
    <p><b>Lo único que necesito de ustedes es una letra</b> (A, B, C, D, E
      o F) para el color.</p>
    <p>Lo del pelo y lo de los pétalos ya está resuelto — díganme
      solamente si quieren más o menos de cada cosa.</p>
  </div>
</div>

<script>
/* Los pétalos. Formas distintas y velocidades distintas: doce pétalos
   iguales cayendo a la misma velocidad se ven como una animación de
   plantilla, no como pétalos. */
(function(){
  const cont = document.getElementById('petalos');
  const COLORES = ['#E07A1F','#A84F2A','#D7C3A1','#A0451A','#C98B5A'];
  for (let i = 0; i < 12; i++) {
    const s = document.createElementNS('http://www.w3.org/2000/svg','svg');
    const w = 7 + Math.random()*9;
    // Un pétalo de verdad: punta arriba y panza abajo. Con una elipse
    // pareja se ven doce confetis cayendo, que es otra cosa.
    s.setAttribute('viewBox','0 0 20 26');
    s.setAttribute('width', w); s.setAttribute('height', w*1.3);
    s.innerHTML = '<path d="M10 0C15.5 6 19 13 16.5 19.5C14.6 24.4 11.8 26 10 26'
                + 'C8.2 26 5.4 24.4 3.5 19.5C1 13 4.5 6 10 0Z"/>';
    s.style.fill = COLORES[i % COLORES.length];
    s.classList.add('p');
    s.style.left = (Math.random()*96) + '%';
    s.style.setProperty('--dx', (Math.random()*80 - 40) + 'px');
    s.style.setProperty('--giro', (Math.random()*520 - 260) + 'deg');
    s.style.animationDuration = (7 + Math.random()*7).toFixed(1) + 's';
    s.style.animationDelay = (-Math.random()*12).toFixed(1) + 's';
    s.style.opacity = (.32 + Math.random()*.3).toFixed(2);
    cont.appendChild(s);
  }
  const bt = document.getElementById('bt');
  bt.onclick = () => {
    const off = cont.classList.toggle('off');
    bt.textContent = off ? 'Encender los pétalos' : 'Apagar los pétalos';
  };
})();
</script>
</body>
</html>
'''

HTML = (HTML.replace('__ANTES__', P['antes']).replace('__AHORA__', P['ahora'])
            .replace('__ENTERA__', P['entera'])
            .replace('__RAMO__', P['ramo']).replace('__COPAS__', P['copas'])
            .replace('__OLIVO__', P['olivo']))
io.open(f"{RAIZ}/cliente-guille-color.html", 'w', encoding='utf-8').write(HTML)
print('cliente-guille-color.html', len(HTML)//1024, 'KB')
