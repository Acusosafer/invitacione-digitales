-- =====================================================================
-- VIDEO DE PORTADA — habilitar video en el bucket
--
-- El bucket `invitaciones` tiene lista blanca de tipos de archivo y no
-- incluia video: cualquier intento de subir un .mp4 devuelve
--     415 invalid_mime_type
-- Esto lo agrega, y sube el limite por archivo de 10 MB a 20 MB.
--
-- ⚠️ EL LIMITE ES A PROPOSITO. Un video de portada tiene que pesar
-- menos de 1 MB: el que lo abre es un invitado con datos moviles. El
-- panel lo avisa al subir. Los 20 MB son el techo del sistema, no el
-- objetivo — y con 10 MB no entraba ni el archivo sin comprimir que
-- manda un cliente.
--
-- Se corre una vez, en el SQL Editor del proyecto ldvosdztnhrvrqxnjuco.
-- Es idempotente: se puede correr de nuevo sin romper nada.
-- =====================================================================

update storage.buckets
   set allowed_mime_types = array[
         'image/jpeg','image/jpg','image/png','image/webp','image/gif',
         'audio/mpeg','audio/mp3','audio/mp4','audio/ogg','audio/wav',
         -- video de portada
         'video/mp4','video/webm','video/quicktime'
       ],
       file_size_limit = 20971520      -- 20 MB
 where id = 'invitaciones';

-- Comprobar:
-- select id, file_size_limit, allowed_mime_types
--   from storage.buckets where id = 'invitaciones';
