# HANDOFF — estado al 31/07/2026 (noche)

> Para retomar en otra sesión. Leer junto con `CLAUDE.md`.

---

## Lo que quedó funcionando

**Supabase migrado.** El proyecto viejo (`fybwovlewphtdmjmwyjn`) quedó abandonado.
Todo vive ahora en `ldvosdztnhrvrqxnjuco` ("Lo de Inés", cuenta `fernando_22_19`),
schema propio `invitaciones`. El conector MCP **no llega** a ese proyecto: el SQL se
le pasa a Fer para el SQL Editor y se verifica desde afuera con `curl` + anon key.

**Seguridad rehecha.** La app es 100% cliente con la anon key pública, así que RLS no
alcanza. `anon` solo lee `(id, config)` de `eventos` y no toca `confirmaciones` ni
`ajustes`; todo lo privilegiado pasa por 8 funciones `SECURITY DEFINER`. El hash de
superadmin salió del código y vive en `ajustes`.

**12 demos cargados** (6 quinceañeras + 6 casamientos) con fotos y música reales.
`catalina15` quedó afuera: sus fotos se perdieron. `valentina15` ocupa su lugar.

**Landing rediseñada.** El color inunda la pantalla y cambia con cada invitación.
Ver la memoria `index-landing-design`.

**Regla de contraste.** Ningún cliente puede armar una invitación ilegible, elija los
colores que elija. 48 combinaciones verificadas, piso 4.50:1. Ver `color-contrast-rule`.

---

## Pendientes, en orden

1. **Esperar la revisión de Google Safe Browsing** (pedida el 31/07). Hasta que la
   levanten, Chrome muestra "Peligroso" y **no hay que publicar la campaña**.
2. **Dominio propio** (~15 USD/año). Es el arreglo de fondo del punto 1: `vercel.app`
   es reputación compartida y la marca puede volver.
3. **Footer del sitio público con la identidad de Fer** — falta que él defina cómo
   firma el negocio, qué contacto público va y si tiene Instagram. Hoy el sitio no
   dice quién es en ninguna parte.
4. **Cuántas horas lleva una invitación** de punta a punta. Sin ese dato no se sabe si
   $50.000 cierra o si está trabajando barato.
5. **Escuchar dos temas** que asigné con dudas: `luna15` (capoeira, se pidió folk de
   jardín) y `boda-julieta` (se llama "morning" y se pidió ambient nocturno).
6. **Álbum compartido con QR** — es lo único relevante que tiene la competencia y él no.
   Acotado: Storage de Supabase + link público por evento.

---

## Cosas que conviene no olvidar

- **No borrar `google03f5ed89092823df.html`**: si desaparece, Google revoca la
  verificación de Search Console.
- **`.vercelignore`** saca del deploy los `.md`, `sql/`, `publicidad/`,
  `generar-hash-superadmin.html` y las utilidades. Antes estaban todos públicos.
- **Clave de superadmin**: su hash está en `invitaciones.ajustes`. Si Fer la pierde,
  genera una nueva con `generar-hash-superadmin.html` (local) y un `update` de una línea.
- `admin123` es la clave de **cliente** — solo desbloquea Resumen, Invitados, Links,
  Mesas y Vista Previa. Los tres módulos de armado son de superadmin.
- **Riesgos aceptados a propósito** (son de spam, no fugas): crear un evento nuevo no
  pide clave (hace falta para dar de alta clientes), y confirmar asistencia es libre
  para quien sepa el slug, con tope de 20 filas por envío.

---

## Campaña de agosto

Pieza en `publicidad/agosto-a.html` (1080×1080, se exporta con F12 → captura de nodo).
"Agosto es de las A": 40% off sobre $50.000 a cambio de poder mostrar la invitación
como ejemplo. Escasez honesta: "tomo 15 este mes, las hago yo una por una".
Contexto de precio y competencia en la memoria `precio-y-competencia`.
