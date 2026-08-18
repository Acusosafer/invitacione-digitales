# -*- coding: utf-8 -*-
"""
FOTO -> DIBUJO DE LINEA -> PATHS SVG ANIMABLES

potracer devuelve una sola curva (traza el fondo) y vtracer segfaultea con
Python 3.14, asi que el trazado va escrito aca. Son cuatro pasos:

  1. mascara binaria       (umbral sobre la foto o sobre el lapiz)
  2. seguimiento de borde  (Moore: se camina el contorno pixel a pixel)
  3. Douglas-Peucker       (de miles de puntos a decenas)
  4. Catmull-Rom -> Bezier (de una polilinea dura a una curva de mano)

⚠️ Lo que sale es el CONTORNO de cada mancha, no su linea central. Para un
trazo fino da igual —el contorno de una linea de 2px se ve como la linea—
pero si los trazos salen gordos, al animarlos se ve delinear un gusano en
vez de dibujar. Si eso pasa, hay que adelgazar la mascara, no engordarla.
"""
import numpy as np
from PIL import Image, ImageFilter, ImageOps

# ── 1 · MASCARAS ────────────────────────────────────────────────────

def mascara_brillo(im, corte=175):
    """Para logos claros sobre fondo oscuro."""
    return np.asarray(ImageOps.grayscale(im), dtype=np.float32) > corte

def mascara_lapiz(im, desenfoque=2.6, corte=26):
    """Bordes: el gris menos su propio negativo desenfocado (color dodge)."""
    g = ImageOps.grayscale(im)
    neg = ImageOps.invert(g).filter(ImageFilter.GaussianBlur(desenfoque))
    a = np.asarray(g, dtype=np.float32)
    b = np.asarray(neg, dtype=np.float32)
    lapiz = np.minimum(255.0, a * 255.0 / np.maximum(1.0, 255.0 - b))
    return (255.0 - lapiz) > corte

def adelgazar(m, vueltas=1):
    """Erosiona un pixel por vuelta: trazos finos = contornos que parecen linea."""
    for _ in range(vueltas):
        p = np.pad(m, 1, constant_values=False)
        m = (m & p[:-2,1:-1] & p[2:,1:-1] & p[1:-1,:-2] & p[1:-1,2:])
    return m

# ── 2 · SEGUIMIENTO DE BORDE (Moore) ────────────────────────────────

_VECINOS = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]

def contornos(m, largo_min=40):
    """Devuelve la lista de contornos cerrados, en pixeles (x, y)."""
    p = np.pad(m, 1, constant_values=False)
    # borde = activo con al menos un vecino apagado. Se calcula de una con
    # numpy: recorrer 800.000 pixeles en Python puro no termina nunca.
    interior = (p[:-2,1:-1] & p[2:,1:-1] & p[1:-1,:-2] & p[1:-1,2:])
    borde = m & ~interior
    visto = np.zeros_like(m, dtype=bool)
    alto, ancho = m.shape
    salida = []

    for y, x in zip(*np.nonzero(borde)):
        if visto[y, x]:
            continue
        camino = []
        cy, cx, dir0 = y, x, 0
        for _ in range(200000):                 # tope de seguridad
            camino.append((cx, cy))
            visto[cy, cx] = True
            hallado = False
            # se busca el proximo borde girando desde la direccion anterior
            for k in range(8):
                d = (dir0 + 5 + k) % 8
                ny, nx = cy + _VECINOS[d][0], cx + _VECINOS[d][1]
                if 0 <= ny < alto and 0 <= nx < ancho and borde[ny, nx]:
                    cy, cx, dir0 = ny, nx, d
                    hallado = True
                    break
            if not hallado or (cx, cy) == (x, y):
                break
        if len(camino) >= largo_min:
            salida.append(camino)
    return salida

# ── 3 · SIMPLIFICAR ─────────────────────────────────────────────────

def _dp(pts, eps):
    if len(pts) < 3:
        return pts
    a, b = np.array(pts[0], float), np.array(pts[-1], float)
    ab = b - a
    n = np.hypot(*ab)
    P = np.array(pts, float)
    if n == 0:
        d = np.hypot(*(P - a).T)
    else:
        # numpy 2 saco el producto cruz 2D, asi que va a mano
        v = P - a
        d = np.abs(ab[0]*v[:,1] - ab[1]*v[:,0]) / n
    i = int(np.argmax(d))
    if d[i] > eps:
        return _dp(pts[:i+1], eps)[:-1] + _dp(pts[i:], eps)
    return [pts[0], pts[-1]]

def simplificar(camino, eps=1.6):
    import sys
    lim = sys.getrecursionlimit()
    sys.setrecursionlimit(20000)
    try:
        return _dp(camino, eps)
    finally:
        sys.setrecursionlimit(lim)

# ── 4 · A CURVA ─────────────────────────────────────────────────────

def a_path(pts, ex=1.0, ey=1.0, tension=0.36):
    """Catmull-Rom cerrada -> cubicas de Bezier: saca el aire de polilinea."""
    n = len(pts)
    if n < 3:
        return None
    P = [(x*ex, y*ey) for x, y in pts]
    d = [f"M{P[0][0]:.1f} {P[0][1]:.1f}"]
    for i in range(n):
        p0 = P[(i-1) % n]; p1 = P[i]; p2 = P[(i+1) % n]; p3 = P[(i+2) % n]
        c1 = (p1[0] + (p2[0]-p0[0])*tension/3, p1[1] + (p2[1]-p0[1])*tension/3)
        c2 = (p2[0] - (p3[0]-p1[0])*tension/3, p2[1] - (p3[1]-p1[1])*tension/3)
        d.append(f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}")
    d.append("Z")
    return "".join(d)

def vectorizar(m, ancho_svg, alto_svg, largo_min=40, eps=1.6, tope=None):
    """La tuberia entera. Devuelve los paths ordenados de mayor a menor."""
    alto, ancho = m.shape
    ex, ey = ancho_svg / ancho, alto_svg / alto
    piezas = []
    for c in contornos(m, largo_min):
        s = simplificar(c, eps)
        d = a_path(s, ex, ey)
        if d:
            piezas.append((d, len(c) * ex))
    piezas.sort(key=lambda t: -t[1])          # los trazos grandes primero
    return piezas[:tope] if tope else piezas
