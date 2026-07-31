# HANDOFF — estado al 31/07/2026

> Contexto para retomar el trabajo en otra sesión. Leer junto con `CLAUDE.md`.

---

## Qué se hizo (noche del 30 al 31/07)

### ✅ Fotos organizadas — 11 eventos completos
57 fotos clasificadas por uso, renombradas y redimensionadas a las medidas exactas del admin
(splash 600×600 · hero 1920×1080 · galería 800×800 · hashtag 400×400), con crop centrado tipo
`object-fit: cover` (sin deformar).

Las carpetas de `assets/` ahora se llaman **igual que el ID del evento en Supabase**:
`boda-ana`, `boda-carolina`, `boda-elena`, `boda-maria`, `boda-valentina`,
`isabella15`, `luna15`, `martina15`, `sofia15`, `valentina15`, `zaira15`.

### ✅ Seguridad — superadmin fuera del código
`admin.html` ya no tiene `if (p === 'superadmin')` en texto plano. Ahora compara **hash SHA-256**
(constante `SUPERADMIN_HASH`, hoy en `'PEGAR_HASH_ACA'`).

**Pendiente de Fer:** abrir `generar-hash-superadmin.html`, escribir su clave, pegar el hash en
`admin.html`. Hasta entonces el superadmin no entra.

### ❌ Se perdieron 5 fotos (error de Claude)
Las de `catalina15` se borraron por un bug: en Windows `Catalina15` y `catalina15` son la misma
carpeta, el script la tomó como "destino existente" y la eliminó. `rmtree` no pasa por papelera →
irrecuperables. Quedó `RECUPERAR-catalina15-referencia.jpg` con las miniaturas de lo que había.

---

## Pendientes

1. **Regenerar `catalina15`** (5 fotos: splash, hero, galería ×2, hashtag) — paleta Dorado Glam
   `#0d0d06 / #d4af37`. Usar la referencia visual guardada.
2. **Generar `boda-julieta`** (Julieta & Tomás, Azul Noche) — prompts listos en `PROMPTS-FOTOS.md`.
3. **Rediseñar la landing** con dirección clara (ver abajo).
4. **Cargar los 13 demos + subir fotos** en Supabase.

---

## Situación de Supabase (el bloqueante)

El proyecto original **`fybwovlewphtdmjmwyjn` (Web invitaciones) está INACTIVE** y no se puede
despertar: la cuenta `fernandoacusosa10@gmail.com` llegó al **límite de 2 proyectos activos del
plan free** (los ocupan `Flor Nails` y `pacifica-carta`, este último de Bar Pacífica, cliente real).
Fer decidió no pausar ninguno.

### Caminos descartados
- **Transferir el proyecto a otra org:** Supabase no lo permite en plan free.
- **Invitar a `fernandoacusosa10` a la org de `fernando_22_19`:** callejón sin salida. Como
  *Developer* no se pueden autorizar integraciones ("does not have the necessary privileges"), y
  como *Administrator* el límite de 2 lo bloquea igual (se cuenta sobre todas las orgs donde sos
  admin u owner).
- **Reconectar el conector a las dos orgs:** la UI no deja marcar más de una.

### Camino elegido
**Usar el proyecto de Supabase de "Lo de Inés"** (cuenta `fernando_22_19`), que está activo y se
usa a diario → nunca se pausa por inactividad, que era el problema de fondo.

```
URL:      https://ldvosdztnhrvrqxnjuco.supabase.co
anon key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxkdm9zZHp0bmhydnJxeG5qdWNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUyOTY1MjAsImV4cCI6MjEwMDg3MjUyMH0.u64wnWOA-Bp0NfOR3tLOAtSkG34P-ApTS00KwTEkGRM
```

### ⚠️ Condiciones innegociables al compartir proyecto
1. **Tablas de invitaciones en un schema propio (`invitaciones`), NO en `public`.** Así no se
   mezclan con las del almacén y mañana se migra sin desenredar nada.
2. **RLS acotado en todo.** Ambas apps comparten la misma anon key, y la web de invitaciones es
   pública: esa key queda a la vista de cualquier invitado. Si una tabla del almacén quedara sin
   policy, un invitado curioso leería la caja del negocio familiar.
3. **Es un puente, no el destino.** Cuando haya clientes pagando por invitaciones, eso merece su
   propio proyecto.

### Auditoría hecha (31/07) — resultado
Con la anon key, desde afuera: raíz de la API `401`, `cierres_caja` `401` (existe, bloqueada ✅),
y `ventas`/`productos`/`caja`/`usuarios` `404` (no existen con esos nombres).
**Los datos del almacén no están expuestos.**

**Duda a resolver:** esa key no permite leer absolutamente nada, ni el catálogo de la API. Puede
ser una key legacy desactivada (Supabase migró a *publishable keys*). Verificar en
**Settings → API** si hay una publishable key vigente — si la legacy está apagada, la app de
invitaciones tampoco funcionaría con ella.

---

## Dirección para el rediseño de la landing

Fer pidió explícitamente: **nada genérico**. Sin las cards y tags iguales que usa todo el mundo.
Público real: chicas de 15 y parejas que se casan — tienen que enamorarse de la web.

**Referencia que le gustó** (captura de una landing de camperas): el color inunda toda la pantalla
con gradiente radial haciendo de luz, el producto flota como héroe sin caja que lo contenga, la nav
es una cápsula flotante, y la info respira sobre el fondo en vez de vivir en tarjetas.

**Traducción al proyecto:** cada evento ya tiene su paleta (Verde Botánica, Dorado Glam, Azul
Noche…). Que ese color **inunde toda la pantalla** en vez de ser un acento sobre fondo blanco, y
que la foto de la quinceañera o de la pareja flote como el producto de la referencia. Cada
invitación se sentiría un mundo propio, no la misma plantilla recoloreada.

Animaciones con criterio de la skill `emil-design-eng`: motivadas, no decorativas.
Usar también `ui-ux-pro-max`.

---

## Riesgos abiertos del proyecto

- **RLS de `confirmaciones` sin auditar.** Guarda nombre, apellido, dieta, mensaje y mesa de cada
  invitado. Con la anon key expuesta, hay que confirmar que nadie pueda listar los invitados de un
  evento ajeno.
- `admin_password` de los demos sigue siendo `admin123`.
- El `foto_hero` de `sofia15` es cuadrado (1024×1024), no 16:9 → se recorta mucho a pantalla completa.
- En `boda-ana` sobró 1 foto sin asignar (hay 8 y se usan 7).
