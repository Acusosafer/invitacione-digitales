# -*- coding: utf-8 -*-
"""
RESCATE DE LOS INTERMEDIOS DE `invita.py`.

⚠️⚠️ POR QUÉ EXISTE ESTE ARCHIVO. El 09/09/2026 `invita.py` NO CORRÍA:
le faltaban los tres archivos que come — `etiqueta-lista.png`,
`svg-escena.txt` y `svg-cartel.txt`. Nunca estuvieron versionados
(`git ls-files` sobre la carpeta devuelve sólo los .py) y tampoco
estaban en el disco. O sea que la única copia del trabajo era el HTML
generado, y el generador que dice "los cambios a mano se pisan" no
podía pisar nada porque no arrancaba.

Se recuperan del propio HTML publicado, que los lleva adentro: la
etiqueta como data URI y los dos trazados en línea. Con esto el
generador vuelve a correr y lo generado vuelve a ser reproducible.

Se corre UNA sola vez. Después, los tres archivos van al repo.
"""
import io, re, base64, os

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(AQUI))
h = io.open(f'{BASE}/cliente-guille-invitacion.html', encoding='utf-8').read()

# ── La etiqueta ──────────────────────────────────────────────────────
# ⚠️ Se guarda como .webp con los bytes EXACTOS, no como .png. Pasarla a
# PNG y volver a comprimirla a webp q88 es una segunda vuelta de pérdida
# sobre una imagen que ya la tuvo, y esta imagen es la portada: es lo
# primero que ve el invitado.
d = re.search(r'data:image/webp;base64,([A-Za-z0-9+/=]+)', h).group(1)
open(f'{AQUI}/etiqueta-lista.webp', 'wb').write(base64.b64decode(d))
print('etiqueta-lista.webp', len(d)*3//4//1024, 'KB')

# ── Los dos trazados ─────────────────────────────────────────────────
# El formato del archivo es: viewBox en la primera línea, los <path> en
# la segunda. En el archivo la clase es "t"; `invita.py` la cambia a
# "trazo" al armar el HTML, así que acá se deshace ese cambio.
def sacar(clave, patron):
    m = re.search(patron, h, re.S)
    vb, cuerpo = m.group(1), m.group(2)
    cuerpo = cuerpo.replace('class="trazo"', 'class="t"')
    io.open(f'{AQUI}/svg-{clave}.txt', 'w', encoding='utf-8').write(vb + '\n' + cuerpo)
    print(f'svg-{clave}.txt      {cuerpo.count("<path"):4} trazos '
          f'{len(cuerpo)//1024:3} KB   viewBox {vb}')

sacar('escena', r'<svg viewBox="([^"]+)" aria-hidden="true">(.*?)</svg>')
sacar('cartel', r'<svg class="dibujo rev bucle" id="dib-cartel" viewBox="([^"]+)"[^>]*>(.*?)</svg>')
