const puppeteer=require('puppeteer-core'), fs=require('fs');
const EDGE='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const DEST='c:/Users/F&F/.gemini/antigravity/scratch/Web invitación/publicidad/destacadas';
fs.mkdirSync(DEST,{recursive:true});

// Trazo idéntico en las cuatro: 5px, puntas redondeadas, dorado #E0AE55.
// Es lo que hace que se lean como un juego y no como cuatro dibujos sueltos.
const ICONOS = {
  'como-es': `
    <rect x="86" y="34" width="108" height="192" rx="20"/>
    <line x1="118" y1="62" x2="162" y2="62"/>
    <line x1="106" y1="112" x2="174" y2="112"/>
    <line x1="106" y1="140" x2="150" y2="140"/>
    <circle cx="140" cy="192" r="15"/>`,
  'el-panel': `
    <line x1="52" y1="86" x2="196" y2="86"/>
    <line x1="52" y1="130" x2="150" y2="130"/>
    <line x1="52" y1="174" x2="228" y2="174"/>
    <circle cx="216" cy="86" r="10"/>
    <circle cx="170" cy="130" r="10"/>`,
  'precios': `
    <path d="M40 140 L128 40 L240 40 L240 152 L140 240 Z"/>
    <circle cx="202" cy="78" r="16"/>`,
  'clientas': `
    <path d="M40 66 h150 a20 20 0 0 1 20 20 v78 a20 20 0 0 1 -20 20 h-92 l-44 40 v-40 h-14
             a20 20 0 0 1 -20 -20 v-78 a20 20 0 0 1 20 -20 z"/>
    <circle cx="88" cy="126" r="9" fill="#E0AE55" stroke="none"/>
    <circle cx="128" cy="126" r="9" fill="#E0AE55" stroke="none"/>
    <circle cx="168" cy="126" r="9" fill="#E0AE55" stroke="none"/>`,
};

const html = svg => `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:#08080a;display:flex;align-items:center;
     justify-content:center;position:relative;overflow:hidden}
/* El halo repite el tratamiento del logo: es lo que hace que se reconozcan
   como de la misma marca aunque el ícono cambie. */
.halo{position:absolute;width:1100px;height:1100px;border-radius:50%;
  background:radial-gradient(circle,rgba(247,206,132,.12),transparent 62%)}
.aro{position:absolute;width:880px;height:880px;border-radius:50%;
  border:3px solid rgba(247,206,132,.18)}
svg{position:relative;width:620px;height:620px;fill:none;stroke:#E0AE55;
    stroke-width:5;stroke-linecap:round;stroke-linejoin:round}
</style></head><body>
<div class="halo"></div><div class="aro"></div>
<svg viewBox="0 0 280 280">${svg}</svg>
</body></html>`;

(async()=>{
const b=await puppeteer.launch({executablePath:EDGE,headless:'new',args:['--no-sandbox']});
const p=await b.newPage(); await p.setViewport({width:1080,height:1920});
for (const [nombre,svg] of Object.entries(ICONOS)) {
  await p.setContent(html(svg),{waitUntil:'load'});
  await new Promise(r=>setTimeout(r,300));
  await p.screenshot({path:`${DEST}/${nombre}.png`});
  console.log(`  ${nombre}.png · ${(fs.statSync(`${DEST}/${nombre}.png`).size/1024).toFixed(0)} KB`);
}
// contacto: cómo se ven de verdad, en círculos de 64px y en fila
const tiras = Object.keys(ICONOS).map(n=>
  `<div style="text-align:center"><img src="data:image/png;base64,${fs.readFileSync(`${DEST}/${n}.png`).toString('base64')}"
   style="width:64px;height:64px;border-radius:50%;object-fit:cover;border:2px solid #333">
   <div style="font:11px system-ui;color:#888;margin-top:6px">${n}</div></div>`).join('');
await p.setViewport({width:420,height:120});
await p.setContent(`<body style="margin:0;background:#fff;display:flex;gap:22px;
  align-items:center;justify-content:center;height:120px">${tiras}</body>`,{waitUntil:'load'});
await new Promise(r=>setTimeout(r,300));
await p.screenshot({path:'C:/Users/F&F/AppData/Local/Temp/claude/c--Users-F-F--gemini-antigravity-scratch-Web-invitaci-n/084b99ff-945b-4ba5-8148-902951824024/scratchpad/destacadas-chicas.png'});
await b.close(); console.log('\ncontacto a 64px generado'); process.exit(0)})();
