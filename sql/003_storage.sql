-- =====================================================================
-- 003 — Bucket de Storage `invitaciones`
--
-- Al migrar de proyecto de Supabase se crearon el schema, las tablas y las
-- funciones, pero NO el bucket. Resultado: toda subida de fotos o música
-- fallaba con "Bucket not found", el error se ignoraba en el cliente, y
-- quedaban guardadas en el config URLs de archivos que nunca existieron.
--
-- Correr una sola vez. Es idempotente.
-- =====================================================================

begin;

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'invitaciones', 'invitaciones',
  true,                     -- público: las fotos las ve cualquier invitado
  10485760,                 -- 10 MB por archivo (la música ronda los 3-5 MB)
  array['image/jpeg','image/jpg','image/png','image/webp','image/gif',
        'audio/mpeg','audio/mp3','audio/mp4','audio/ogg','audio/wav']
)
on conflict (id) do update
  set public             = true,
      file_size_limit    = excluded.file_size_limit,
      allowed_mime_types = excluded.allowed_mime_types;


-- ---------------------------------------------------------------------
-- Permisos
--
-- El admin sube desde el navegador con la anon key, así que `anon` necesita
-- poder INSERTAR. Pero NO se le da UPDATE ni DELETE a propósito: sin eso,
-- cualquiera con la anon key podría pisar o borrar las fotos de un cliente
-- que ya está en producción. Los nombres llevan timestamp, así que nunca
-- hace falta sobrescribir.
-- ---------------------------------------------------------------------

drop policy if exists invitaciones_leer  on storage.objects;
drop policy if exists invitaciones_subir on storage.objects;

create policy invitaciones_leer
  on storage.objects for select
  to anon, authenticated
  using (bucket_id = 'invitaciones');

create policy invitaciones_subir
  on storage.objects for insert
  to anon, authenticated
  with check (bucket_id = 'invitaciones');

commit;


-- =====================================================================
-- Chequeo: debe devolver una fila con public = true
-- =====================================================================
-- select id, public, file_size_limit from storage.buckets where id = 'invitaciones';
