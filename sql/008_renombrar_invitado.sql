-- ═══════════════════════════════════════════════════════════════════
-- 008 · CORREGIR EL NOMBRE DE UN INVITADO
--
-- Faltaba, y se nota en dos casos que pasan en toda fiesta:
--
--   1 · Un link se llamó "Familia Ferron" y quien vino es Tomás Ferron.
--       El prellenado parte el nombre en dos, así que en la lista del
--       salón se sienta alguien llamado "Familia Ferron".
--   2 · Un grupo avisa por WhatsApp que va — mandan la captura — y hay
--       que pasar sus filas de `pendiente` a confirmadas CON SUS
--       NOMBRES. Sin esto, la única salida era borrar las filas
--       pre-cargadas y volver a cargarlas a mano: se pierde el link, se
--       pierde la dieta y la canción, y si uno se distrae el salón
--       cuenta a la familia dos veces.
--
-- ⚠️ Va como función NUEVA y no como parámetros agregados a
-- `admin_actualizar_fila`: cambiarle la cantidad de parámetros a una
-- función obliga a borrarla y recrearla —`create or replace` con otra
-- firma crea una sobrecarga y PostgREST no sabe cuál llamar— y el drop
-- se lleva puesto el grant. En un evento en curso eso es dejar el panel
-- roto por el tiempo que tarde en correrse la migración.
--
-- ⚠️ El apellido es OBLIGATORIO, igual que en el alta a mano: el listado
-- que se le entrega al salón se ordena por apellido, y una fila sin
-- apellido queda arriba de todo sin que nadie sepa de quién es.
-- ═══════════════════════════════════════════════════════════════════

create or replace function invitaciones.admin_renombrar_fila(
  p_evento   text,
  p_clave    text,
  p_id       bigint,
  p_nombre   text,
  p_apellido text
)
returns boolean
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_nombre   text := btrim(coalesce(p_nombre, ''));
  v_apellido text := btrim(coalesce(p_apellido, ''));
begin
  if invitaciones.verificar_clave(p_evento, p_clave) is null then
    raise exception 'Clave incorrecta' using errcode = 'insufficient_privilege';
  end if;

  if v_nombre = '' or v_apellido = '' then
    raise exception 'Hacen falta el nombre y el apellido';
  end if;

  update invitaciones.confirmaciones c
     set nombre   = left(v_nombre, 80),
         apellido = left(v_apellido, 80)
   where c.id = p_id
     and c.evento_id = p_evento;   -- ata la fila al evento cuya clave se validó

  return found;
end;
$$;

revoke all on function
  invitaciones.admin_renombrar_fila(text, text, bigint, text, text) from public;
grant execute on function
  invitaciones.admin_renombrar_fila(text, text, bigint, text, text) to anon, authenticated;

-- Sin esto PostgREST no ve la función nueva y el panel recibe un 404.
notify pgrst, 'reload schema';
