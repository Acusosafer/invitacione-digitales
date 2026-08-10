-- =====================================================================
-- 004 — `delfina15`: evento de demostración con 100 invitados reales
--
-- Para qué existe
-- ---------------
-- Sacar capturas de pantalla para material comercial (carrusel de
-- Instagram, propuestas, la web). Los 12 demos de la landing tienen la
-- invitación linda pero CERO invitados cargados, así que el panel se ve
-- vacío: no sirve para mostrar mesas, pendientes ni el PDF del salón.
--
-- Este evento NO aparece en la galería de la landing (esa lista está
-- escrita a mano en index.html). Se llega solo por URL directa.
--
-- Los 100 nombres son inventados. No hay una sola persona real acá.
--
-- Composición, pensada para que cada captura muestre algo:
--   80 confirmados  → 8 mesas de 10, todas llenas  (captura del croquis)
--    7 no asisten   → sin mesa                     (captura del resumen)
--   13 pendientes   → en 4 grupos familiares       (captura de recordatorios)
--  ---
--  100 invitados
--
-- Las fotos apuntan a /assets/martina15/, que ya está en el repo. Es un
-- demo interno: no vale la pena generar siete fotos nuevas para un evento
-- del que solo se fotografía el panel.
--
-- Idempotente: borra y recarga. Se puede correr las veces que haga falta.
-- Todo en UNA transacción.
-- =====================================================================

begin;

-- ---------------------------------------------------------------------
-- El evento
-- ---------------------------------------------------------------------
insert into invitaciones.eventos (id, config, admin_password)
values ('delfina15', '{
  "nombre": "Delfina",
  "tipo": "MIS 15",
  "subtitulo": "Quiero que seas parte de esta noche",
  "fuente": "Jost",
  "color_1": "#1a1a1a",
  "color_2": "#c8b89a",
  "color_bg": "#fafaf8",
  "foto_splash": "/assets/martina15/foto_splash.jpg",
  "foto_hero": "/assets/martina15/foto_hero.jpg",
  "foto_galeria_1": "/assets/martina15/foto_galeria_1.jpg",
  "foto_galeria_2": "/assets/martina15/foto_galeria_2.jpg",
  "foto_galeria_3": "/assets/martina15/foto_galeria_3.jpg",
  "foto_hashtag": "/assets/martina15/foto_hashtag.jpg",
  "musica_url": "/assets/martina15/musica.mp3",
  "mensaje": "Hay noches que se esperan toda la vida. Esta es la mía, y no la quiero sin vos.",
  "mensaje_firma": "Con amor, Delfina",
  "fecha_iso": "2026-11-14T21:00",
  "fecha_texto": "Sábado 14 de noviembre, 2026",
  "hora_texto": "21:00",
  "countdown_style": "flex",
  "salon": "Salón Alvear",
  "direccion": "Av. del Libertador 3200, Vicente López",
  "maps_url": "https://maps.google.com/?q=Av.+del+Libertador+3200+Vicente+Lopez",
  "dresscode_titulo": "ELEGANTE",
  "dresscode_texto": "Elegante sport. Evitá el blanco.",
  "alias_pago": "delfina.15.mp",
  "regalo_texto": "Tu presencia es el mejor regalo. Si querés hacerme un obsequio, podés colaborar con mi viaje de egresados.",
  "hashtag": "#DelfiXV",
  "hashtag_texto": "Sacá muchas fotos y subilas con el hashtag. ¡Quiero verlas todas!",
  "instagram_url": "https://instagram.com",
  "rsvp_limite": "1 de noviembre",
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
}'::jsonb, 'admin123')
on conflict (id) do update
  set config = excluded.config,
      admin_password = excluded.admin_password;


-- ---------------------------------------------------------------------
-- Los 100 invitados
-- ---------------------------------------------------------------------
-- Se borra primero para que correr el archivo dos veces no deje 200.
delete from invitaciones.confirmaciones where evento_id = 'delfina15';

insert into invitaciones.confirmaciones
  (evento_id, invitado_url, nombre, apellido, asiste, personas, dieta, mensaje, mesa)
values

-- ============ MESA 1 — familia directa y abuelos ============
('delfina15','Roberto Sosa','Roberto','Sosa','si',1,'','Los Redondos - Ji Ji Ji','1'),
('delfina15','Roberto Sosa','Mariana','Sosa','si',1,'','','1'),
('delfina15','Roberto Sosa','Tomás','Sosa','si',1,'','','1'),
('delfina15','Roberto Sosa','Camila','Sosa','si',1,'Vegetariano','','1'),
('delfina15','Roberto Sosa','Julián','Sosa','si',1,'','','1'),
('delfina15','Roberto Sosa','Renata','Sosa','si',1,'','','1'),
('delfina15','Alfredo Sosa','Alfredo','Sosa','si',1,'','','1'),
('delfina15','Alfredo Sosa','Nélida','Sosa','si',1,'Sin sal','','1'),
('delfina15','Héctor Pereyra','Héctor','Pereyra','si',1,'','','1'),
('delfina15','Héctor Pereyra','Susana','Pereyra','si',1,'','','1'),

-- ============ MESA 2 — familia paterna ============
('delfina15','Gustavo Sosa','Gustavo','Sosa','si',1,'','','2'),
('delfina15','Gustavo Sosa','Verónica','Ledesma','si',1,'','','2'),
('delfina15','Gustavo Sosa','Matías','Sosa','si',1,'','','2'),
('delfina15','Gustavo Sosa','Lucía','Sosa','si',1,'','','2'),
('delfina15','Fernando Sosa','Fernando','Sosa','si',1,'','La Renga - El Twist del Pibe','2'),
('delfina15','Fernando Sosa','Paula','Bianchi','si',1,'Celíaco','','2'),
('delfina15','Fernando Sosa','Ignacio','Sosa','si',1,'','','2'),
('delfina15','Fernando Sosa','Josefina','Sosa','si',1,'','','2'),
('delfina15','Marcelo Sosa','Marcelo','Sosa','si',1,'','','2'),
('delfina15','Marcelo Sosa','Andrea','Quiroga','si',1,'','','2'),

-- ============ MESA 3 — familia materna ============
('delfina15','Diego Pereyra','Diego','Pereyra','si',1,'','','3'),
('delfina15','Diego Pereyra','Carolina','Méndez','si',1,'','','3'),
('delfina15','Diego Pereyra','Bautista','Pereyra','si',1,'','','3'),
('delfina15','Diego Pereyra','Emilia','Pereyra','si',1,'','','3'),
('delfina15','Ariel Pereyra','Ariel','Pereyra','si',1,'','','3'),
('delfina15','Ariel Pereyra','Silvina','Rossi','si',1,'Vegano','','3'),
('delfina15','Ariel Pereyra','Facundo','Pereyra','si',1,'','','3'),
('delfina15','Ariel Pereyra','Milagros','Pereyra','si',1,'','','3'),
('delfina15','Norberto Pereyra','Norberto','Pereyra','si',1,'Diabético','','3'),
('delfina15','Norberto Pereyra','Graciela','Ibáñez','si',1,'','','3'),

-- ============ MESA 4 — amigas del colegio ============
('delfina15','Catalina Vega','Catalina','Vega','si',1,'','Tini - Cupido','4'),
('delfina15','Morena Duarte','Morena','Duarte','si',1,'','','4'),
('delfina15','Guadalupe Ferreyra','Guadalupe','Ferreyra','si',1,'Vegetariano','','4'),
('delfina15','Abril Sandoval','Abril','Sandoval','si',1,'','','4'),
('delfina15','Zoe Maldonado','Zoe','Maldonado','si',1,'','Emilia - No_Se_Ve.mp3','4'),
('delfina15','Malena Ochoa','Malena','Ochoa','si',1,'','','4'),
('delfina15','Jazmín Ríos','Jazmín','Ríos','si',1,'','','4'),
('delfina15','Bianca Cabrera','Bianca','Cabrera','si',1,'','','4'),
('delfina15','Antonella Vera','Antonella','Vera','si',1,'','','4'),
('delfina15','Pilar Escobar','Pilar','Escobar','si',1,'','','4'),

-- ============ MESA 5 — amigas del club ============
('delfina15','Martina Aguirre','Martina','Aguirre','si',1,'','','5'),
('delfina15','Sol Benítez','Sol','Benítez','si',1,'','','5'),
('delfina15','Victoria Peralta','Victoria','Peralta','si',1,'Celíaco','','5'),
('delfina15','Julieta Navarro','Julieta','Navarro','si',1,'','María Becerra - Automático','5'),
('delfina15','Agustina Coronel','Agustina','Coronel','si',1,'','','5'),
('delfina15','Brenda Molina','Brenda','Molina','si',1,'','','5'),
('delfina15','Luana Figueroa','Luana','Figueroa','si',1,'','','5'),
('delfina15','Ámbar Godoy','Ámbar','Godoy','si',1,'','','5'),
('delfina15','Candela Ávila','Candela','Ávila','si',1,'','','5'),
('delfina15','Ariana Suárez','Ariana','Suárez','si',1,'','','5'),

-- ============ MESA 6 — amigos ============
('delfina15','Thiago Ramírez','Thiago','Ramírez','si',1,'','Duki - Goteo','6'),
('delfina15','Benjamín Acosta','Benjamín','Acosta','si',1,'','','6'),
('delfina15','Santino Herrera','Santino','Herrera','si',1,'','','6'),
('delfina15','Lautaro Ojeda','Lautaro','Ojeda','si',1,'','','6'),
('delfina15','Valentino Cáceres','Valentino','Cáceres','si',1,'','','6'),
('delfina15','Bruno Miranda','Bruno','Miranda','si',1,'','','6'),
('delfina15','Ciro Domínguez','Ciro','Domínguez','si',1,'Sin lactosa','','6'),
('delfina15','Nicolás Barrios','Nicolás','Barrios','si',1,'','','6'),
('delfina15','Franco Villalba','Franco','Villalba','si',1,'','','6'),
('delfina15','Gael Paz','Gael','Paz','si',1,'','','6'),

-- ============ MESA 7 — amigos de los padres ============
('delfina15','Eduardo Lombardi','Eduardo','Lombardi','si',1,'','','7'),
('delfina15','Eduardo Lombardi','Patricia','Salvatierra','si',1,'','','7'),
('delfina15','Claudio Genovese','Claudio','Genovese','si',1,'','','7'),
('delfina15','Claudio Genovese','Mónica','Alessandro','si',1,'Vegetariano','','7'),
('delfina15','Sergio Bustamante','Sergio','Bustamante','si',1,'','','7'),
('delfina15','Sergio Bustamante','Alejandra','Cabral','si',1,'','','7'),
('delfina15','Ricardo Fontana','Ricardo','Fontana','si',1,'','','7'),
('delfina15','Ricardo Fontana','Liliana','Mansilla','si',1,'','','7'),
('delfina15','Osvaldo Zapata','Osvaldo','Zapata','si',1,'','','7'),
('delfina15','Osvaldo Zapata','Beatriz','Olivera','si',1,'','','7'),

-- ============ MESA 8 — compañeros de trabajo ============
('delfina15','Javier Constantino','Javier','Constantino','si',1,'','','8'),
('delfina15','Javier Constantino','Natalia','Rinaldi','si',1,'','','8'),
('delfina15','Pablo Echeverría','Pablo','Echeverría','si',1,'','','8'),
('delfina15','Pablo Echeverría','Romina','Cardozo','si',1,'','','8'),
('delfina15','Hernán Casaretto','Hernán','Casaretto','si',1,'Celíaco','','8'),
('delfina15','Hernán Casaretto','Vanina','Sotelo','si',1,'','','8'),
('delfina15','Leandro Paladino','Leandro','Paladino','si',1,'','','8'),
('delfina15','Leandro Paladino','Cecilia','Arrieta','si',1,'','','8'),
('delfina15','Marcos Bruzzone','Marcos','Bruzzone','si',1,'','','8'),
('delfina15','Marcos Bruzzone','Daniela','Prato','si',1,'','','8'),

-- ============ NO ASISTEN (7) — sin mesa ============
('delfina15','Adrián Fiorentino','Adrián','Fiorentino','no',1,'','¡Qué lástima! Estamos de viaje esa semana. Mandale un beso enorme a Delfi.',null),
('delfina15','Adrián Fiorentino','Marisa','Cantero','no',1,'','',null),
('delfina15','Rubén Alcaraz','Rubén','Alcaraz','no',1,'','',null),
('delfina15','Rubén Alcaraz','Nora','Basualdo','no',1,'','',null),
('delfina15','Cristian Palacios','Cristian','Palacios','no',1,'','',null),
('delfina15','Cristian Palacios','Yamila','Ledesma','no',1,'','',null),
('delfina15','Esteban Correa','Esteban','Correa','no',1,'','',null),

-- ============ PENDIENTES (13) — 4 grupos que nunca contestaron ============
-- Estas son filas de pre-alta: las creó el generador de links y siguen
-- intactas. Son las que alimentan la tarjeta de recordatorios.
('delfina15','Familia Nardelli','Oscar','Nardelli','pendiente',1,'','',null),
('delfina15','Familia Nardelli','Estela','Nardelli','pendiente',1,'','',null),
('delfina15','Familia Nardelli','Rocío','Nardelli','pendiente',1,'','',null),
('delfina15','Familia Nardelli','Ignacio','Nardelli','pendiente',1,'','',null),
('delfina15','Alberto Zanetti','Alberto','Zanetti','pendiente',1,'','',null),
('delfina15','Alberto Zanetti','Mirta','Zanetti','pendiente',1,'','',null),
('delfina15','Familia Cabezas','Walter','Cabezas','pendiente',1,'','',null),
('delfina15','Familia Cabezas','Sandra','Cabezas','pendiente',1,'','',null),
('delfina15','Familia Cabezas','Nahuel','Cabezas','pendiente',1,'','',null),
('delfina15','Familia Cabezas','Ailén','Cabezas','pendiente',1,'','',null),
('delfina15','Familia Cabezas','Thiago','Cabezas','pendiente',1,'','',null),
('delfina15','Gabriel Puglisi','Gabriel','Puglisi','pendiente',1,'','',null),
('delfina15','Gabriel Puglisi','Elisa','Puglisi','pendiente',1,'','',null);


-- ---------------------------------------------------------------------
-- Control: tiene que dar 100 / 80 / 7 / 13 y 8 mesas
-- ---------------------------------------------------------------------
select
  count(*)                                            as total,
  count(*) filter (where asiste = 'si')               as confirmados,
  count(*) filter (where asiste = 'no')               as no_asisten,
  count(*) filter (where asiste = 'pendiente')        as pendientes,
  count(distinct mesa)                                as mesas,
  count(distinct invitado_url)                        as links
from invitaciones.confirmaciones
where evento_id = 'delfina15';

commit;
