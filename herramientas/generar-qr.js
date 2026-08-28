/* ══════════════════════════════════════════════════════════════════
   LOS QR DE LAS MESAS

   Un QR cuadrado no se puede recortar en círculo: las tres esquinas
   grandes son las que el celular usa para orientarse. Lo que sí se puede
   es meterlo DENTRO de una pieza circular, con el anillo y el texto
   curvo alrededor.

   ⚠️⚠️ LOS MÓDULOS REDONDOS SUELTOS NO SE LEEN. Un círculo de radio
   0,44 del paso cubre el 61% de su celda, y el lector promedia esa celda
   y la toma por blanca: ninguno de los trece se leía. La forma correcta
   es UNIR los módulos vecinos —un punto más un puente hacia el de al
   lado—: en las zonas densas se funden en formas orgánicas, queda más
   lindo que los puntos sueltos, y la cobertura queda entera.

   ⚠️ El marco de los ojos va de 6 módulos, no de 7: el stroke de SVG se
   pinta mitad adentro y mitad afuera, así que un rect de 7 se come medio
   módulo de la zona quieta y corre el patrón.

   ⚠️ Nivel de corrección 'H': es lo que permite tapar el centro con el
   número de mesa sin perder la lectura.
   ══════════════════════════════════════════════════════════════════ */
const qrcode = require('qrcode-generator');
const fs = require('fs');
const path = require('path');

const L = 1200, CENTRO = L / 2;
const R_EXT = L / 2 - 6;
const R_INT = R_EXT - 76;

/* ⚠️ EL PISTACHO CLARO NO SE LEE. Medido con un lector real: #b5d99c da
   1,57:1 contra el papel y no lo lee en ningún tamaño; el salvia del
   evento (2,27:1) y el pistacho medio (3,12:1) leen en chico y FALLAN en
   grande — que es peor que no andar: funciona en la prueba y falla cuando
   el invitado acerca el celular. Desde 4,85:1 lee en todos los tamaños.

   Por eso van DOS verdes: el código en `color` (profundo, el que se lee)
   y el anillo, el centro y los adornos en `acento` (el pistacho que se
   quería). La pieza se ve pistacho y el código funciona. */
function pieza({ url, etiqueta, centro, color, acento, tinta, nombre }) {
  const q = qrcode(0, 'H');
  q.addData(url); q.make();
  const n = q.getModuleCount();

  const lado = Math.floor(R_INT * 2 * 0.707);
  const paso = lado / n;
  const x0 = CENTRO - lado / 2, y0 = CENTRO - lado / 2;

  const esOjo = (r, c) => (r < 7 && c < 7) || (r < 7 && c >= n - 7) || (r >= n - 7 && c < 7);
  const h = Math.round(n * 0.22);
  const h0 = Math.floor((n - h) / 2), h1 = h0 + h;
  const enHueco = (r, c) => r >= h0 && r < h1 && c >= h0 && c < h1;
  const pinta = (r, c) => r >= 0 && r < n && c >= 0 && c < n
    && q.isDark(r, c) && !esOjo(r, c) && !enHueco(r, c);

  let d = '';
  for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) {
    if (!pinta(r, c)) continue;
    const cx = x0 + c * paso + paso / 2, cy = y0 + r * paso + paso / 2;
    d += `<circle cx="${cx.toFixed(2)}" cy="${cy.toFixed(2)}" r="${(paso*.52).toFixed(2)}"/>`;
    if (pinta(r, c + 1))
      d += `<rect x="${cx.toFixed(2)}" y="${(cy-paso*.52).toFixed(2)}" width="${paso.toFixed(2)}" height="${(paso*1.04).toFixed(2)}"/>`;
    if (pinta(r + 1, c))
      d += `<rect x="${(cx-paso*.52).toFixed(2)}" y="${cy.toFixed(2)}" width="${(paso*1.04).toFixed(2)}" height="${paso.toFixed(2)}"/>`;
  }

  const marco = (fr, fc) => {
    const x = x0 + fc * paso + paso / 2, y = y0 + fr * paso + paso / 2, s = paso * 6;
    return `<rect x="${x.toFixed(2)}" y="${y.toFixed(2)}" width="${s.toFixed(2)}" height="${s.toFixed(2)}"
              rx="${(s*.30).toFixed(2)}" fill="none" stroke="${color}" stroke-width="${paso.toFixed(2)}"/>
            <rect x="${(x0+fc*paso+paso*2).toFixed(2)}" y="${(y0+fr*paso+paso*2).toFixed(2)}"
              width="${(paso*3).toFixed(2)}" height="${(paso*3).toFixed(2)}"
              rx="${(paso*1.0).toFixed(2)}" fill="${color}"/>`;
  };

  const rTxt = R_EXT - 40;
  const arco = (arriba) => `M ${CENTRO} ${CENTRO} m ${-rTxt} 0 a ${rTxt} ${rTxt} 0 1 ${arriba ? 1 : 0} ${rTxt*2} 0`;
  const rHueco = h * paso * 0.56;

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${L}" height="${L}" viewBox="0 0 ${L} ${L}">
  <defs>
    <path id="ar" d="${arco(true)}"/>
    <path id="ab" d="${arco(false)}"/>
  </defs>
  <rect width="${L}" height="${L}" fill="#ffffff"/>

  <circle cx="${CENTRO}" cy="${CENTRO}" r="${R_EXT}" fill="none" stroke="${color}" stroke-width="2.5" opacity=".5"/>
  <circle cx="${CENTRO}" cy="${CENTRO}" r="${R_EXT-14}" fill="none" stroke="${acento}" stroke-width="13"/>
  <circle cx="${CENTRO}" cy="${CENTRO}" r="${R_EXT-14}" fill="none" stroke="${color}" stroke-width="1.5" opacity=".45"/>

  <text font-family="Fraunces, Georgia, serif" font-size="43" font-weight="600"
        fill="${tinta}" letter-spacing="6">
    <textPath href="#ar" startOffset="50%" text-anchor="middle">DEJALE UN MENSAJE A ${nombre}</textPath>
  </text>
  <text font-family="Fraunces, Georgia, serif" font-size="35" font-weight="600"
        fill="${color}" letter-spacing="10">
    <textPath href="#ab" startOffset="50%" text-anchor="middle">${etiqueta}</textPath>
  </text>

  <g fill="${color}">${d}</g>
  ${marco(0,0)}${marco(0,n-7)}${marco(n-7,0)}

  <circle cx="${CENTRO}" cy="${CENTRO}" r="${rHueco.toFixed(1)}" fill="#ffffff"/>
  <circle cx="${CENTRO}" cy="${CENTRO}" r="${(rHueco*.88).toFixed(1)}" fill="${acento}"/>
  <circle cx="${CENTRO}" cy="${CENTRO}" r="${(rHueco*.88).toFixed(1)}" fill="none" stroke="${color}" stroke-width="3"/>
  <text x="${CENTRO}" y="${CENTRO}" text-anchor="middle" dominant-baseline="central"
        font-family="Fraunces, Georgia, serif" font-weight="700"
        font-size="${(rHueco*1.02).toFixed(0)}" fill="${color}">${centro}</text>
</svg>`;
}

module.exports = { pieza };

// Uso directo: node qr-final.js <color> <carpeta> [mesas]
if (require.main === module) {
  const color  = process.argv[2] || '#5d7a42';   // el codigo: tiene que leerse
  const acento = process.argv[3] || '#b5d99c';   // los adornos: el pistacho
  const salida = process.argv[4];
  const mesas  = parseInt(process.argv[5] || '12');
  const EVENTO = 'almamia15', NOMBRE = 'ALMA';
  const BASE = 'https://www.invitacionesdigitalesoficial.com/deseos';

  fs.mkdirSync(salida, { recursive: true });
  for (let m = 1; m <= mesas; m++) {
    fs.writeFileSync(path.join(salida, `qr-mesa-${String(m).padStart(2,'0')}.svg`),
      pieza({ url: `${BASE}?evento=${EVENTO}&mesa=${m}`, etiqueta: `MESA ${m}`,
              centro: m, color, acento, tinta: '#1a1a1a', nombre: NOMBRE }));
  }
  fs.writeFileSync(path.join(salida, 'qr-mesa-principal.svg'),
    pieza({ url: `${BASE}?evento=${EVENTO}&mesa=0`, etiqueta: 'MESA PRINCIPAL',
            centro: '★', color, acento, tinta: '#1a1a1a', nombre: NOMBRE }));
  console.log((mesas + 1) + ' piezas en ' + salida);
}
