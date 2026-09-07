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
/* ⚠️ El texto curvo se apoyaba contra el anillo: hay que separar el radio
   del texto del radio del aro, no dejarlos pegados. El aro entra un poco
   y el texto se corre hacia adentro. */
const R_EXT = L / 2 - 26;
const R_INT = R_EXT - 92;

/* ⚠️ EL PISTACHO CLARO NO SE LEE. Medido con un lector real: #b5d99c da
   1,57:1 contra el papel y no lo lee en ningún tamaño; el salvia del
   evento (2,27:1) y el pistacho medio (3,12:1) leen en chico y FALLAN en
   grande — que es peor que no andar: funciona en la prueba y falla cuando
   el invitado acerca el celular. Desde 4,85:1 lee en todos los tamaños.

   Por eso van DOS verdes: el código en `color` (profundo, el que se lee)
   y el anillo, el centro y los adornos en `acento` (el pistacho que se
   quería). La pieza se ve pistacho y el código funciona. */
/* `fondo`:
     'blanco'       — la lámina entera blanca (la de siempre, para imprimir)
     'transparente' — sin nada atrás. ⚠️ El "blanco" del código pasa a ser
                      lo que haya abajo: sobre fondo claro y liso se lee,
                      sobre una foto NO.
     'disco'        — transparente afuera del círculo, blanco adentro. Es
                      el único que funciona apoyado sobre cualquier cosa. */
/* `estilo`:
     'anillo'  — la pieza circular completa: aro, texto curvo y número.
     'desnudo' — sólo el código y el número en el centro. Sin aro y sin
                 texto, el código puede ocupar TODO el lienzo en vez de
                 quedar inscripto en el círculo: al mismo tamaño de
                 papel, cada módulo mide un 40% más y se lee de más
                 lejos. ⚠️ Lo que NO se puede sacar es el margen: un QR
                 necesita 4 módulos de aire alrededor o el lector no
                 encuentra dónde termina. */
function pieza({ url, etiqueta, centro, color, acento, tinta, nombre,
                 fondo = 'blanco', estilo = 'anillo' }) {
  const transparente = fondo !== 'blanco';
  const desnudo = estilo === 'desnudo';
  const q = qrcode(0, 'H');
  q.addData(url); q.make();
  const n = q.getModuleCount();

  /* Con aro, el código va inscripto en el círculo interior (de ahí el
     0,707 = raíz de 2 sobre 2). Sin aro, ocupa el lienzo menos los 4
     módulos de zona quieta de cada lado — de ahí el n/(n+8). */
  const lado = desnudo ? Math.floor(L * n / (n + 8))
                       : Math.floor(R_INT * 2 * 0.707);
  const paso = lado / n;
  const x0 = CENTRO - lado / 2, y0 = CENTRO - lado / 2;

  const esOjo = (r, c) => (r < 7 && c < 7) || (r < 7 && c >= n - 7) || (r >= n - 7 && c < 7);

  /* ⚠️⚠️ EL HUECO DEL CENTRO ES REDONDO, NO CUADRADO — y no por gusto.
     Cuadrado, sus bordes caían en módulos enteros: con 65 módulos (que
     son los que usa esta URL) el centro de la grilla está en 32,5 y el
     hueco terminaba corrido MEDIO MÓDULO respecto al medallón, que se
     dibuja en el centro del lienzo. En las trece piezas el número se
     veía corrido hacia un costado, y a ojo parecía un problema del
     texto. Redondo, el hueco se calcula desde n/2 igual que el
     medallón: no hay paridad que valga y encima el disco lo tapa
     exacto, sin dejar las cuatro esquinas del cuadrado a la vista. */
  const h = Math.round(n * 0.24);          // el diámetro del hueco, en módulos
  const rMod = h / 2;
  const enHueco = (r, c) =>
    Math.hypot(r + 0.5 - n / 2, c + 0.5 - n / 2) <= rMod;
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

  const rTxt = R_EXT - 52;
  const arco = (arriba) => `M ${CENTRO} ${CENTRO} m ${-rTxt} 0 a ${rTxt} ${rTxt} 0 1 ${arriba ? 1 : 0} ${rTxt*2} 0`;
  const rHueco = rMod * paso;   // el mismo disco que se dejó sin pintar

  /* La placa de atrás. Con aro es un círculo; sin aro tiene que ser un
     cuadrado —redondeado— que cubra el código MÁS su zona quieta: un
     círculo del ancho del código le corta las cuatro esquinas, que es
     justo donde están dos de los tres ojos. */
  const placa = fondo === 'blanco'
    ? `<rect width="${L}" height="${L}" fill="#ffffff"/>`
    : fondo === 'disco'
      ? (desnudo
          ? `<rect x="${(CENTRO-lado/2-paso*4).toFixed(1)}" y="${(CENTRO-lado/2-paso*4).toFixed(1)}"
                 width="${(lado+paso*8).toFixed(1)}" height="${(lado+paso*8).toFixed(1)}"
                 rx="${(paso*3).toFixed(1)}" fill="#ffffff"/>`
          : `<circle cx="${CENTRO}" cy="${CENTRO}" r="${R_EXT + 8}" fill="#ffffff"/>`)
      : '';

  const aro = desnudo ? '' : `
  <circle cx="${CENTRO}" cy="${CENTRO}" r="${R_EXT}" fill="none" stroke="${color}" stroke-width="2.5" opacity=".5"/>
  <circle cx="${CENTRO}" cy="${CENTRO}" r="${R_EXT-14}" fill="none" stroke="${acento}" stroke-width="13"/>
  <circle cx="${CENTRO}" cy="${CENTRO}" r="${R_EXT-14}" fill="none" stroke="${color}" stroke-width="1.5" opacity=".45"/>

  <text font-family="Fraunces, Georgia, serif" font-size="38" font-weight="600"
        fill="${tinta}" letter-spacing="5">
    <textPath href="#ar" startOffset="50%" text-anchor="middle">DEJALE UN MENSAJE A ${nombre}</textPath>
  </text>
  <text font-family="Fraunces, Georgia, serif" font-size="31" font-weight="600"
        fill="${color}" letter-spacing="9">
    <textPath href="#ab" startOffset="50%" text-anchor="middle">${etiqueta}</textPath>
  </text>`;

  /* ⚠️ El medallón del centro NO es decorativo: tapa los módulos que
     sobresalen por los costados del hueco cuadrado. En transparente no
     hay blanco abajo, así que se agranda el de color hasta el mismo
     radio en vez de apoyarse sobre uno blanco. */
  const rMed = rHueco * (transparente ? 1 : 0.88);

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${L}" height="${L}" viewBox="0 0 ${L} ${L}">
  <defs>
    <path id="ar" d="${arco(true)}"/>
    <path id="ab" d="${arco(false)}"/>
  </defs>
  ${placa}
  ${aro}

  <g fill="${color}">${d}</g>
  ${marco(0,0)}${marco(0,n-7)}${marco(n-7,0)}

  ${transparente ? '' : `<circle cx="${CENTRO}" cy="${CENTRO}" r="${rHueco.toFixed(1)}" fill="#ffffff"/>`}
  <circle cx="${CENTRO}" cy="${CENTRO}" r="${rMed.toFixed(1)}" fill="${acento}"/>
  <circle cx="${CENTRO}" cy="${CENTRO}" r="${rMed.toFixed(1)}" fill="none" stroke="${color}" stroke-width="3"/>
  <text x="${CENTRO}" y="${CENTRO}" text-anchor="middle" dominant-baseline="central"
        font-family="Fraunces, Georgia, serif" font-weight="700"
        font-size="${(rHueco*1.02).toFixed(0)}" fill="${color}">${centro}</text>
</svg>`;
}

module.exports = { pieza };

/* Uso: node generar-qr.js <color> <acento> <carpeta> [mesas] [fondo] [estilo]
     fondo:  blanco | transparente | disco
     estilo: anillo | desnudo   (desnudo = sólo el código y el número)

   ⚠️⚠️ TRANSPARENTE NO ES UN DETALLE DE FORMATO. El "blanco" del código
   pasa a ser lo que haya atrás: sobre un fondo claro se lee igual que
   antes, sobre una foto o un fondo medio oscuro NO SE LEE. El pistacho
   sobre papel es 4,85:1; sobre una foto de fondo puede ser 1,2:1. Antes
   de imprimir, se compone contra el fondo REAL y se lee con jsQR. */
if (require.main === module) {
  const color  = process.argv[2] || '#5d7a42';   // el codigo: tiene que leerse
  const acento = process.argv[3] || '#b5d99c';   // los adornos: el pistacho
  const salida = process.argv[4];
  const mesas  = parseInt(process.argv[5] || '12');
  const fondo  = process.argv[6] || 'blanco';   // blanco | transparente | disco
  const estilo = process.argv[7] || 'anillo';   // anillo | desnudo
  const EVENTO = 'almamia15', NOMBRE = 'ALMA';
  const BASE = 'https://www.invitacionesdigitalesoficial.com/deseos';

  fs.mkdirSync(salida, { recursive: true });
  for (let m = 1; m <= mesas; m++) {
    fs.writeFileSync(path.join(salida, `qr-mesa-${String(m).padStart(2,'0')}.svg`),
      pieza({ url: `${BASE}?evento=${EVENTO}&mesa=${m}`, etiqueta: `MESA ${m}`,
              centro: m, color, acento, tinta: '#1a1a1a', nombre: NOMBRE, fondo, estilo }));
  }
  fs.writeFileSync(path.join(salida, 'qr-mesa-principal.svg'),
    pieza({ url: `${BASE}?evento=${EVENTO}&mesa=0`, etiqueta: 'MESA PRINCIPAL',
            centro: '★', color, acento, tinta: '#1a1a1a', nombre: NOMBRE, fondo, estilo }));
  console.log(`${mesas + 1} piezas (${estilo}, fondo ${fondo}) en ${salida}`);
}
