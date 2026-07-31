-- =====================================================================
-- 002 — Los 12 eventos demo de la landing (6 de 15 años + 6 casamientos)
-- Correr DESPUÉS de 001_schema_invitaciones.sql
--
-- `catalina15` quedó afuera: sus fotos se perdieron y no se regeneraron.
-- Su lugar en la galería lo ocupa `valentina15`, que antes solo existía
-- como evento original sin card propia.
--
-- Las fotos apuntan a /assets/<id>/, que se sirve desde Vercel junto al
-- sitio. No pasan por Supabase Storage: son demos fijos, no material de
-- cliente. Cuando un cliente real suba las suyas desde el admin, esas sí
-- van a Storage y el config queda con la URL absoluta.
--
-- Fechas: todas futuras a propósito. Un countdown en negativo en la
-- galería de demos se lee como un sitio abandonado.
-- =====================================================================

begin;

-- Limpieza del evento que usé para auditar el schema.
delete from invitaciones.eventos where id = '_test_audit';


with base as (
  -- Lo que comparten los 13. Cada evento pisa lo que necesita.
  select '{
    "fuente": "Jost",
    "countdown_style": "flex",
    "hora_texto": "21:00",
    "dresscode_titulo": "ELEGANTE",
    "dresscode_texto": "Elegante sport. Evitá el blanco.",
    "regalo_texto": "Tu presencia es el mejor regalo. Si querés hacernos un obsequio, podés colaborar con nuestra luna de miel.",
    "hashtag_texto": "Sacá muchas fotos y subilas con el hashtag. ¡Queremos verlas todas!",
    "instagram_url": "https://instagram.com",
    "layout": {
      "show_mensaje": true,
      "show_countdown": true,
      "show_gallery": true,
      "show_ubicacion": true,
      "show_dresscode": true,
      "show_gift": true,
      "show_hashtag": true,
      "show_rsvp": true,
      "order": ["hero","mensaje","countdown","galeria","ubicacion","dresscode","regalos","hashtag","rsvp"]
    }
  }'::jsonb as b
),

datos(id, extra) as (values

-- ---------------------------------------------------------------- 15 AÑOS

('valentina15', '{
  "nombre": "Valentina", "tipo": "MIS 15",
  "subtitulo": "Quiero que seas parte de esta noche",
  "color_1": "#1a1a1a", "color_2": "#d6ecc0", "color_bg": "#ffffff",
  "foto_splash": "/assets/valentina15/foto_splash.jpg",
  "foto_hero": "/assets/valentina15/foto_hero.jpg",
  "foto_galeria_1": "/assets/valentina15/foto_galeria_1.jpg",
  "foto_galeria_2": "/assets/valentina15/foto_galeria_2.jpg",
  "foto_hashtag": "/assets/valentina15/foto_hashtag.jpg",
  "mensaje": "Hay noches que se esperan toda la vida. Esta es una de ésas, y no la quiero vivir sin vos.",
  "mensaje_firma": "Con amor, Valentina",
  "fecha_iso": "2026-11-14T21:00", "fecha_texto": "Sábado 14 de noviembre, 2026",
  "salon": "Salón Magnolia", "direccion": "Av. San Martín 1250, Vicente López",
  "maps_url": "https://maps.google.com/?q=Av.+San+Martin+1250+Vicente+Lopez",
  "alias_pago": "valentina.15.mp",
  "hashtag": "#ValentinaXV", "rsvp_limite": "1 de noviembre"
}'::jsonb),

('zaira15', '{
  "nombre": "Zaira", "tipo": "MIS 15",
  "subtitulo": "Una noche para brillar",
  "color_1": "#f2f2f7", "color_2": "#b8b8cc", "color_bg": "#0d0d1a",
  "foto_splash": "/assets/zaira15/foto_splash.jpg",
  "foto_hero": "/assets/zaira15/foto_hero.jpg",
  "foto_galeria_1": "/assets/zaira15/foto_galeria_1.jpg",
  "foto_galeria_2": "/assets/zaira15/foto_galeria_2.jpg",
  "foto_hashtag": "/assets/zaira15/foto_hashtag.jpg",
  "mensaje": "Crecí escuchando que este día iba a llegar. Ya llegó, y lo único que me importa es con quién lo comparto.",
  "mensaje_firma": "Te espero, Zaira",
  "fecha_iso": "2026-10-03T21:30", "fecha_texto": "Sábado 3 de octubre, 2026",
  "hora_texto": "21:30",
  "salon": "Palacio Sans Souci", "direccion": "Rivadavia 1236, San Fernando",
  "maps_url": "https://maps.google.com/?q=Palacio+Sans+Souci+San+Fernando",
  "alias_pago": "zaira.quince", "dresscode_titulo": "BLACK TIE",
  "dresscode_texto": "Vestido largo y traje oscuro.",
  "hashtag": "#ZairaXV", "rsvp_limite": "20 de septiembre"
}'::jsonb),

('martina15', '{
  "nombre": "Martina", "tipo": "MIS 15",
  "subtitulo": "Te espero para celebrar",
  "color_1": "#2b2620", "color_2": "#c8b89a", "color_bg": "#fafaf8",
  "foto_splash": "/assets/martina15/foto_splash.jpg",
  "foto_hero": "/assets/martina15/foto_hero.jpg",
  "foto_galeria_1": "/assets/martina15/foto_galeria_1.jpg",
  "foto_galeria_2": "/assets/martina15/foto_galeria_2.jpg",
  "foto_galeria_3": "/assets/martina15/foto_galeria_3.jpg",
  "foto_hashtag": "/assets/martina15/foto_hashtag.jpg",
  "mensaje": "No quería una fiesta enorme. Quería la gente justa, y vos entrás en esa lista.",
  "mensaje_firma": "Con cariño, Martina",
  "fecha_iso": "2026-12-05T21:00", "fecha_texto": "Sábado 5 de diciembre, 2026",
  "salon": "Estancia La Linda", "direccion": "Ruta 25 km 8, Pilar",
  "maps_url": "https://maps.google.com/?q=Estancia+La+Linda+Pilar",
  "alias_pago": "martina.15", "countdown_style": "grid",
  "hashtag": "#MartiXV", "rsvp_limite": "22 de noviembre"
}'::jsonb),

('luna15', '{
  "nombre": "Luna", "tipo": "MIS 15",
  "subtitulo": "Bajo las estrellas",
  "color_1": "#23301f", "color_2": "#7ab87a", "color_bg": "#f5f8f2",
  "foto_splash": "/assets/luna15/foto_splash.jpg",
  "foto_hero": "/assets/luna15/foto_hero.jpg",
  "foto_galeria_1": "/assets/luna15/foto_galeria_1.jpg",
  "foto_galeria_2": "/assets/luna15/foto_galeria_2.jpg",
  "foto_hashtag": "/assets/luna15/foto_hashtag.jpg",
  "mensaje": "Va a haber jardín, luces colgando de los árboles y música hasta que se haga de día. Sólo faltás vos.",
  "mensaje_firma": "Con amor, Luna",
  "fecha_iso": "2027-03-13T20:30", "fecha_texto": "Sábado 13 de marzo, 2027",
  "hora_texto": "20:30",
  "salon": "Quinta Los Aromos", "direccion": "Camino Real 450, Moreno",
  "maps_url": "https://maps.google.com/?q=Quinta+Los+Aromos+Moreno",
  "alias_pago": "luna.quince.15",
  "dresscode_texto": "Elegante sport. Ojo con los tacos finos: hay pasto.",
  "hashtag": "#LunaXV", "rsvp_limite": "28 de febrero"
}'::jsonb),

('sofia15', '{
  "nombre": "Sofía", "tipo": "MIS 15",
  "subtitulo": "¡Se viene la fiesta!",
  "color_1": "#3a1f2b", "color_2": "#ff6ba8", "color_bg": "#fff0f7",
  "foto_splash": "/assets/sofia15/foto_splash.jpg",
  "foto_hero": "/assets/sofia15/foto_hero.jpg",
  "foto_galeria_1": "/assets/sofia15/foto_galeria_1.jpg",
  "foto_galeria_2": "/assets/sofia15/foto_galeria_2.jpg",
  "foto_galeria_3": "/assets/sofia15/foto_galeria_3.jpg",
  "foto_galeria_4": "/assets/sofia15/foto_galeria_4.jpg",
  "foto_hashtag": "/assets/sofia15/foto_hashtag.jpg",
  "mensaje": "Vengo planeando esto desde los doce. Preparate: se baila hasta que cierren.",
  "mensaje_firma": "Nos vemos, Sofi",
  "fecha_iso": "2026-09-19T22:00", "fecha_texto": "Sábado 19 de septiembre, 2026",
  "hora_texto": "22:00",
  "salon": "Club Náutico Hacoaj", "direccion": "Av. del Libertador 3300, Tigre",
  "maps_url": "https://maps.google.com/?q=Club+Nautico+Hacoaj+Tigre",
  "alias_pago": "sofia.xv.mp", "dresscode_titulo": "FIESTA",
  "dresscode_texto": "Ponete lo que te haga sentir bien. Zapatillas bienvenidas.",
  "hashtag": "#SofiXV", "rsvp_limite": "5 de septiembre"
}'::jsonb),

('isabella15', '{
  "nombre": "Isabella", "tipo": "MIS 15",
  "subtitulo": "Quiero que estés ahí",
  "color_1": "#2e2440", "color_2": "#b8a0d6", "color_bg": "#f8f5ff",
  "foto_splash": "/assets/isabella15/foto_splash.jpg",
  "foto_hero": "/assets/isabella15/foto_hero.jpg",
  "foto_galeria_1": "/assets/isabella15/foto_galeria_1.jpg",
  "foto_galeria_2": "/assets/isabella15/foto_galeria_2.jpg",
  "foto_hashtag": "/assets/isabella15/foto_hashtag.jpg",
  "mensaje": "Cumplir quince es raro: seguís siendo la misma y todos te miran distinto. Quiero pasarlo con la gente que me conoce de verdad.",
  "mensaje_firma": "Con amor, Isa",
  "fecha_iso": "2027-04-24T21:00", "fecha_texto": "Sábado 24 de abril, 2027",
  "salon": "Casona del Pilar", "direccion": "Los Robles 780, Pilar",
  "maps_url": "https://maps.google.com/?q=Casona+del+Pilar",
  "alias_pago": "isabella.15", "countdown_style": "grid",
  "hashtag": "#IsaXV", "rsvp_limite": "10 de abril"
}'::jsonb),

-- ------------------------------------------------------------ CASAMIENTOS

('boda-ana', '{
  "nombre": "Ana & José", "tipo": "NOS CASAMOS",
  "subtitulo": "Nos gustaría que nos acompañes",
  "color_1": "#2e2820", "color_2": "#c9a96e", "color_bg": "#fffef9",
  "foto_splash": "/assets/boda-ana/foto_splash.jpg",
  "foto_hero": "/assets/boda-ana/foto_hero.jpg",
  "foto_galeria_1": "/assets/boda-ana/foto_galeria_1.jpg",
  "foto_galeria_2": "/assets/boda-ana/foto_galeria_2.jpg",
  "foto_galeria_3": "/assets/boda-ana/foto_galeria_3.jpg",
  "foto_galeria_4": "/assets/boda-ana/foto_galeria_4.jpg",
  "foto_hashtag": "/assets/boda-ana/foto_hashtag.jpg",
  "mensaje": "Después de nueve años juntos decidimos hacerlo oficial. Nos encantaría tenerte ese día.",
  "mensaje_firma": "Ana & José",
  "fecha_iso": "2026-11-21T19:00", "fecha_texto": "Sábado 21 de noviembre, 2026",
  "hora_texto": "19:00",
  "salon": "Estancia Villa María", "direccion": "Ruta 205 km 52, Ezeiza",
  "maps_url": "https://maps.google.com/?q=Estancia+Villa+Maria+Ezeiza",
  "alias_pago": "ana.jose.boda", "dresscode_titulo": "FORMAL",
  "hashtag": "#AnaYJose", "rsvp_limite": "5 de noviembre"
}'::jsonb),

('boda-elena', '{
  "nombre": "Elena & Pablo", "tipo": "NOS CASAMOS",
  "subtitulo": "Nos casamos y queremos festejarlo con vos",
  "color_1": "#f5f0e6", "color_2": "#d4af37", "color_bg": "#0d0d0d",
  "foto_splash": "/assets/boda-elena/foto_splash.jpg",
  "foto_hero": "/assets/boda-elena/foto_hero.jpg",
  "foto_galeria_1": "/assets/boda-elena/foto_galeria_1.jpg",
  "foto_galeria_2": "/assets/boda-elena/foto_galeria_2.jpg",
  "foto_galeria_3": "/assets/boda-elena/foto_galeria_3.jpg",
  "foto_hashtag": "/assets/boda-elena/foto_hashtag.jpg",
  "mensaje": "Va a ser de noche, con velas y la gente que más queremos. Contamos con vos.",
  "mensaje_firma": "Elena & Pablo",
  "fecha_iso": "2027-02-27T20:00", "fecha_texto": "Sábado 27 de febrero, 2027",
  "hora_texto": "20:00",
  "salon": "Four Seasons Buenos Aires", "direccion": "Posadas 1086, Retiro",
  "maps_url": "https://maps.google.com/?q=Four+Seasons+Buenos+Aires",
  "alias_pago": "elena.pablo", "dresscode_titulo": "BLACK TIE",
  "dresscode_texto": "Vestido largo y smoking.",
  "hashtag": "#ElenaYPablo", "rsvp_limite": "13 de febrero"
}'::jsonb),

('boda-maria', '{
  "nombre": "María & Ramiro", "tipo": "NOS CASAMOS",
  "subtitulo": "Al aire libre, entre amigos",
  "color_1": "#2b3024", "color_2": "#a0b880", "color_bg": "#f5f5ee",
  "foto_splash": "/assets/boda-maria/foto_splash.jpg",
  "foto_hero": "/assets/boda-maria/foto_hero.jpg",
  "foto_galeria_1": "/assets/boda-maria/foto_galeria_1.jpg",
  "foto_galeria_2": "/assets/boda-maria/foto_galeria_2.jpg",
  "foto_hashtag": "/assets/boda-maria/foto_hashtag.jpg",
  "mensaje": "Queríamos campo, asado y baile hasta tarde. Eso vamos a hacer, y nos gustaría que estés.",
  "mensaje_firma": "María & Ramiro",
  "fecha_iso": "2026-10-24T18:00", "fecha_texto": "Sábado 24 de octubre, 2026",
  "hora_texto": "18:00",
  "salon": "Campo Los Nogales", "direccion": "Camino de los Remedios s/n, Cañuelas",
  "maps_url": "https://maps.google.com/?q=Canuelas+Buenos+Aires",
  "alias_pago": "maria.ramiro",
  "dresscode_texto": "Elegante sport. Es al aire libre: traé abrigo para la noche.",
  "hashtag": "#MariYRami", "rsvp_limite": "10 de octubre"
}'::jsonb),

('boda-carolina', '{
  "nombre": "Carolina & Martín", "tipo": "NOS CASAMOS",
  "subtitulo": "Se viene el gran día",
  "color_1": "#3a2a20", "color_2": "#d4845a", "color_bg": "#faf6f0",
  "foto_splash": "/assets/boda-carolina/foto_splash.jpg",
  "foto_hero": "/assets/boda-carolina/foto_hero.jpg",
  "foto_galeria_1": "/assets/boda-carolina/foto_galeria_1.jpg",
  "foto_galeria_2": "/assets/boda-carolina/foto_galeria_2.jpg",
  "foto_hashtag": "/assets/boda-carolina/foto_hashtag.jpg",
  "mensaje": "Doce años, dos mudanzas y un perro después, nos casamos. Vení a festejar con nosotros.",
  "mensaje_firma": "Caro & Tincho",
  "fecha_iso": "2027-01-16T19:30", "fecha_texto": "Sábado 16 de enero, 2027",
  "hora_texto": "19:30",
  "salon": "Finca Madero", "direccion": "Ruta 8 km 60, Pilar",
  "maps_url": "https://maps.google.com/?q=Finca+Madero+Pilar",
  "alias_pago": "caro.martin.boda", "countdown_style": "grid",
  "hashtag": "#CaroYTincho", "rsvp_limite": "2 de enero"
}'::jsonb),

('boda-valentina', '{
  "nombre": "Valentina & Nicolás", "tipo": "NOS CASAMOS",
  "subtitulo": "Queremos que seas parte",
  "color_1": "#3b2830", "color_2": "#e8b4c0", "color_bg": "#fdf5f7",
  "foto_splash": "/assets/boda-valentina/foto_splash.jpg",
  "foto_hero": "/assets/boda-valentina/foto_hero.jpg",
  "foto_galeria_1": "/assets/boda-valentina/foto_galeria_1.jpg",
  "foto_galeria_2": "/assets/boda-valentina/foto_galeria_2.jpg",
  "foto_hashtag": "/assets/boda-valentina/foto_hashtag.jpg",
  "mensaje": "Nos conocimos en un casamiento ajeno. Nos pareció justo invitarte al nuestro.",
  "mensaje_firma": "Vale & Nico",
  "fecha_iso": "2027-03-27T19:00", "fecha_texto": "Sábado 27 de marzo, 2027",
  "hora_texto": "19:00",
  "salon": "Jardín Escondido", "direccion": "Gorriti 4945, Palermo",
  "maps_url": "https://maps.google.com/?q=Jardin+Escondido+Palermo",
  "alias_pago": "vale.nico.2027",
  "hashtag": "#ValeYNico", "rsvp_limite": "13 de marzo"
}'::jsonb),

('boda-julieta', '{
  "nombre": "Julieta & Tomás", "tipo": "NOS CASAMOS",
  "subtitulo": "Una noche para recordar",
  "color_1": "#e8eef7", "color_2": "#7090c0", "color_bg": "#080f1a",
  "foto_splash": "/assets/boda-julieta/foto_splash.jpg",
  "foto_hero": "/assets/boda-julieta/foto_hero.jpg",
  "foto_galeria_1": "/assets/boda-julieta/foto_galeria_1.jpg",
  "foto_galeria_2": "/assets/boda-julieta/foto_galeria_2.jpg",
  "foto_hashtag": "/assets/boda-julieta/foto_hashtag.jpg",
  "mensaje": "Nos casamos de noche, bajo las estrellas. Nos haría muy felices que vengas.",
  "mensaje_firma": "Julieta & Tomás",
  "fecha_iso": "2027-02-13T20:30", "fecha_texto": "Sábado 13 de febrero, 2027",
  "hora_texto": "20:30",
  "salon": "Puerto Madero Eventos", "direccion": "Olga Cossettini 1031, Puerto Madero",
  "maps_url": "https://maps.google.com/?q=Olga+Cossettini+1031+Puerto+Madero",
  "alias_pago": "juli.tomas.boda", "dresscode_titulo": "FORMAL",
  "hashtag": "#JuliYTomi", "rsvp_limite": "30 de enero"
}'::jsonb)

)
insert into invitaciones.eventos (id, config, admin_password)
select d.id, base.b || d.extra, 'admin123'
  from datos d cross join base
    on conflict (id) do update
       set config = excluded.config;

commit;


-- =====================================================================
-- Chequeo rápido: deben salir 12 filas, todas con fecha futura.
-- =====================================================================
-- select id,
--        config->>'nombre'      as nombre,
--        config->>'fecha_texto' as fecha,
--        (config->>'fecha_iso')::timestamp > now() as fecha_futura,
--        (config ? 'foto_hero')                    as tiene_fotos
--   from invitaciones.eventos
--  order by id;
