# -*- coding: utf-8 -*-
"""Genera dibujo-a-mano.html con las tres pruebas vectorizadas."""
import sys, io, re; sys.path.insert(0,'.')
from vector import mascara_brillo, mascara_lapiz, vectorizar
from PIL import Image

BASE = r"c:/Users/F&F/.gemini/antigravity/scratch/Web invitación/Boda Guillermina"

def redondear(d):
    """Sin decimales: a este tamaño no se nota y el archivo baja un cuarto."""
    return re.sub(r'(\d+)\.\d+', r'\1', d)

def preparar(ruta, recorte, ancho_svg, modo, **kw):
    im = Image.open(ruta).convert('RGB')
    if recorte: im = im.crop(recorte)
    im = im.resize((kw.pop('trabajo', 900), 0), Image.LANCZOS) if False else im
    w = kw.pop('trabajo', 900)
    im = im.resize((w, round(w*im.height/im.width)), Image.LANCZOS)
    H = round(ancho_svg * im.height / im.width)
    m = mascara_brillo(im, kw.pop('corte_brillo', 175)) if modo == 'brillo' \
        else mascara_lapiz(im, kw.pop('des', 3.0), kw.pop('corte', 30))
    paths = vectorizar(m, ancho_svg, H, largo_min=kw.pop('lmin', 90), eps=kw.pop('eps', 1.8))
    return [redondear(d) for d, _ in paths], ancho_svg, H

PIEZAS = []

# 1 · EL CARTEL — logo blanco de alto contraste: la mejor materia prima
PIEZAS.append(('cartel', 'El cartel de la finca',
    'De la foto del cartel de la entrada. Es el que mejor sale: un logo '
    'blanco sobre fondo oscuro le da al trazador un borde perfecto.',
    preparar(f"{BASE}/Fotos/la josefina logo.jpeg", (150,60,760,400), 610,
             'brillo', corte_brillo=170, lmin=32, eps=1.4)))

# 2 · LA ESCENA — la acuarela del save the date
PIEZAS.append(('escena', 'Ellos frente al lago',
    'De la acuarela nueva. Se ven el muelle, las sillas, los árboles y el '
    'sol: es la que más se parece a lo que hace Andina.',
    preparar(f"{BASE}/web/save the date final.jpg", None, 600,
             'lapiz', des=2.4, corte=24, lmin=90, eps=1.8, trabajo=900)))

# 3 · EL BARQUITO — el que no sale, y por que
PIEZAS.append(('bote', 'El barquito',
    'De la foto del bote. El casco sale bien, pero ELLOS DOS se rompen en '
    'pedazos: ropa clara sobre agua clara no le da ningún borde que seguir.',
    preparar(f"{BASE}/Fotos/barquito.jpeg", (230,40,830,530), 560,
             'lapiz', des=3.0, corte=30, lmin=110, eps=1.8, trabajo=820)))

bloques = []
for clave, titulo, nota, (paths, W, H) in PIEZAS:
    cuerpo = "".join(f'<path class="t" d="{d}"/>' for d in paths)
    bloques.append(f'''
  <section class="pieza">
    <div class="cab">
      <h2>{titulo}</h2>
      <span class="cuenta">{len(paths)} trazos</span>
    </div>
    <p class="nota">{nota}</p>
    <div class="lienzo">
      <svg viewBox="0 0 {W} {H}" data-clave="{clave}">{cuerpo}</svg>
    </div>
    <button class="bt" data-para="{clave}">Dibujar de nuevo</button>
  </section>''')
    print(f"{clave}: {len(paths)} trazos, {len(cuerpo)//1024} KB")

PLANTILLA = io.open('plantilla-dibujo.html', encoding='utf-8').read()
salida = PLANTILLA.replace('<!--PIEZAS-->', "\n".join(bloques))
io.open(f"{BASE}/dibujo-a-mano.html", 'w', encoding='utf-8').write(salida)
print('total', len(salida)//1024, 'KB')
