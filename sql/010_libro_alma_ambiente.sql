-- ═══════════════════════════════════════════════════════════════════
-- 010 · EL AMBIENTE DE ATRÁS DEL LIBRO DE ALMA
--
-- Lo que se ve ALREDEDOR del libro: hasta ahora era un verde plano y el
-- libro parecía recortado sobre nada. Con esto queda apoyado en el
-- jardín.
--
-- ⚠️ Aditivo, como el 009: `config || ...` conserva todo lo demás.
-- ⚠️ La imagen es muy clara (brillo 232 sobre 255). El nombre de arriba
-- y los botones de abajo se leen igual porque el velo de la pantalla es
-- una FRANJA oscura arriba y abajo, no una viñeta suave — justamente
-- para que sirva con un estanque de noche y con un jardín de mediodía.
-- ═══════════════════════════════════════════════════════════════════

update invitaciones.eventos
   set config = config || jsonb_build_object('libro_fondo', 'https://ldvosdztnhrvrqxnjuco.supabase.co/storage/v1/object/public/invitaciones/almamia15/libro_ambiente_1788819524.jpg'),
       updated_at = now()
 where id = 'almamia15';

select id,
       config ? 'libro_fondo' as tiene_ambiente,
       config ? 'libro_tapa'  as conserva_tapa,
       jsonb_array_length(config->'libro_hojas') as hojas,
       config ? 'nombre'      as conserva_nombre
  from invitaciones.eventos
 where id = 'almamia15';
