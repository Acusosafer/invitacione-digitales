-- ═══════════════════════════════════════════════════════════════════
-- 009 · EL LIBRO ANIMADO DE ALMA
--
-- Deja el evento `almamia15` listo para /libro?evento=almamia15: la
-- tapa que se abre, las cuatro hojas ilustradas con su zona de
-- escritura medida, y la silueta.
--
-- ⚠️ El UPDATE es ADITIVO: `config || jsonb_build_object(...)` fusiona
-- a nivel raíz y CONSERVA todo lo demás del evento (los colores, las
-- fotos, la fecha, el layout). Un `set config = '{...}'` a secas le
-- borraría la invitación entera a una clienta con la fiesta pasada.
--
-- ⚠️ Las zonas (t/r/b/l) NO son a ojo: salieron de medir cada imagen
-- —hasta dónde llega la franja sin nada oscuro— porque el alto útil va
-- del 27% al 70% según la hoja. Si algún día se cambia una imagen, hay
-- que volver a medirla, no estimarla.
--
-- ⚠️ `agua` es el alto en % de la franja de agua dibujada: ahí y sólo
-- ahí pasa el brillo. Un destello cruzando papel en blanco se lee como
-- un error.
-- ═══════════════════════════════════════════════════════════════════

update invitaciones.eventos
   set config = config || jsonb_build_object(
         'libro_tema', 'sapo',

         'libro_tapa',
           'https://ldvosdztnhrvrqxnjuco.supabase.co/storage/v1/object/public/invitaciones/almamia15/libro_tapa_1788817090.jpg',

         'libro_silueta',
           'https://ldvosdztnhrvrqxnjuco.supabase.co/storage/v1/object/public/invitaciones/almamia15/libro_silueta_1788815690.png',

         'libro_hojas', jsonb_build_array(
           jsonb_build_object(
             'u','https://ldvosdztnhrvrqxnjuco.supabase.co/storage/v1/object/public/invitaciones/almamia15/libro_hoja1_1788805780.jpg',
             't', 9,  'r',13, 'b',21, 'l',13),
           jsonb_build_object(
             'u','https://ldvosdztnhrvrqxnjuco.supabase.co/storage/v1/object/public/invitaciones/almamia15/libro_hoja2_1788805780.jpg',
             't',16, 'r',13, 'b',24, 'l',13),
           jsonb_build_object(
             'u','https://ldvosdztnhrvrqxnjuco.supabase.co/storage/v1/object/public/invitaciones/almamia15/libro_hoja3_1788805780.jpg',
             't',38, 'r',13, 'b',25, 'l',13),
           jsonb_build_object(
             'u','https://ldvosdztnhrvrqxnjuco.supabase.co/storage/v1/object/public/invitaciones/almamia15/libro_portada_1788805780.jpg',
             't', 8,  'r',13, 'b',46, 'l',13, 'agua',44),
           jsonb_build_object(
             'u','https://ldvosdztnhrvrqxnjuco.supabase.co/storage/v1/object/public/invitaciones/almamia15/libro_cierre_1788805780.jpg',
             'rol','cierre', 't',32, 'r',13, 'b',41, 'l',13, 'agua',34)
         )
       ),
       updated_at = now()
 where id = 'almamia15';

-- Para comprobar que quedó bien y que NO se perdió nada de lo anterior:
select id,
       config ? 'libro_tapa'                as tiene_tapa,
       jsonb_array_length(config->'libro_hojas') as hojas,
       config ? 'nombre'                    as conserva_nombre,
       config ? 'fecha_iso'                 as conserva_fecha,
       config ? 'deseos_activo'             as libro_de_deseos_activo
  from invitaciones.eventos
 where id = 'almamia15';
