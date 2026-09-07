# -*- coding: utf-8 -*-
u"""Le saca a la tapa las dos líneas que Gemini copió de la captura.

⚠️ El rectángulo NO se elige a ojo: las dos líneas se ubicaron midiendo
el perfil de píxeles oscuros fila por fila (y 574..587 y y 613..626), y
los bordes se recortan para no comerse la mariposa de la izquierda, que
empieza en x 240.

El relleno es interpolación vertical del papel limpio de arriba y de
abajo, más el grano medido de una zona limpia: un relleno plano en un
papel con textura se nota como un parche.
"""
import io
import numpy as np
from PIL import Image, ImageFilter

R = u"c:/Users/F&F/.gemini/antigravity/scratch/Web invitaci\u00f3n/fotos Alma/portada libro.jpg"
im = Image.open(R).convert('RGB')
a = np.asarray(im).astype(np.float32)

Y0, Y1 = 564, 638          # las dos lineas, con aire
X0, X1 = 250, 700          # sin tocar la mariposa (termina en 240)
ARR = a[Y0-14:Y0-2, X0:X1].mean(axis=0)     # papel limpio de arriba
ABA = a[Y1+2:Y1+14,  X0:X1].mean(axis=0)    # papel limpio de abajo

# cuanto grano tiene el papel limpio, para no dejar un parche liso
limpio = a[Y0-16:Y0-2, X0:X1]
grano = float((limpio - limpio.mean(axis=0)).std())
print(u'grano del papel: %.2f' % grano)

alto = Y1 - Y0
t = np.linspace(0, 1, alto)[:, None, None]
relleno = ARR[None, :, :]*(1-t) + ABA[None, :, :]*t
rng = np.random.default_rng(7)
relleno = relleno + rng.normal(0, grano, relleno.shape)

b = a.copy()
b[Y0:Y1, X0:X1] = np.clip(relleno, 0, 255)
out = Image.fromarray(b.astype(np.uint8))

# un desenfoque MUY suave sólo en la costura, para que no se vea el corte
cost = out.crop((X0-6, Y0-6, X1+6, Y1+6)).filter(ImageFilter.GaussianBlur(.6))
out.paste(cost, (X0-6, Y0-6))
out.paste(im.crop((X0+4, Y0+4, X1-4, Y1-4)).point(lambda v: v), (X0+4, Y0+4)) if False else None
out.save('portada-limpia.jpg', quality=94, subsampling=0)

# ¿quedó texto? se vuelve a medir el perfil
c = np.asarray(out.convert('RGB')).astype(np.float32).mean(axis=2)
resto = (c[Y0:Y1, X0:X1] < 150).mean()
print(u'pixeles oscuros que quedan en la zona: %.4f%%' % (resto*100))
print('portada-limpia.jpg')
