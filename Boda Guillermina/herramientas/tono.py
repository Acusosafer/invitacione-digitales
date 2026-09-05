import numpy as np
from PIL import Image
G = r"c:/Users/F&F/.gemini/antigravity/scratch/Web invitación/Boda Guillermina/web"
def a_lab(a):
    a=a/255.0; a=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
    M=np.array([[.4124,.3576,.1805],[.2126,.7152,.0722],[.0193,.1192,.9505]])
    xyz=a@M.T/np.array([.9505,1.0,1.089])
    f=np.where(xyz>.008856,np.cbrt(xyz),7.787*xyz+16/116)
    return np.stack([116*f[...,1]-16,500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2])],-1)
def de_lab(lab):
    L,A,B=lab[...,0],lab[...,1],lab[...,2]
    fy=(L+16)/116; fx=fy+A/500; fz=fy-B/200
    g=lambda t: np.where(t**3>.008856,t**3,(t-16/116)/7.787)
    xyz=np.stack([g(fx),g(fy),g(fz)],-1)*np.array([.9505,1.0,1.089])
    M=np.array([[3.2406,-1.5372,-.4986],[-.9689,1.8758,.0415],[.0557,-.2040,1.0570]])
    rgb=xyz@M.T
    rgb=np.where(rgb<=.0031308,12.92*rgb,1.055*np.power(np.clip(rgb,0,None),1/2.4)-.055)
    return np.clip(rgb,0,1)*255
def dibujo(im): return np.asarray(im,np.float32).mean(axis=2)<238
def llevar(src, ref, fuerza):
    s=np.asarray(src,np.float32); ls=a_lab(s); lr=a_lab(np.asarray(ref,np.float32))
    ms=dibujo(src); mr=dibujo(ref); out=ls.copy()
    for i in range(3):
        mu,sd=ls[...,i][ms].mean(),ls[...,i][ms].std()
        mr2,sr=lr[...,i][mr].mean(),lr[...,i][mr].std()
        out[...,i]=ls[...,i]*(1-fuerza)+((ls[...,i]-mu)*(sr/max(sd,1e-3))+mr2)*fuerza
    n=Image.fromarray(de_lab(out).astype('uint8'))
    return Image.composite(n, src, Image.fromarray((ms*255).astype('uint8')))
