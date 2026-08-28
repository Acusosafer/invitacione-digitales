-- ═══════════════════════════════════════════════════════════════════
-- 007 · Cargar un invitado a mano
--
-- Para qué: hay gente que va a la fiesta y NUNCA recibe un link — los
-- padres, los hermanos, la agasajada misma. Hoy esa gente no existe en
-- el sistema, así que el contador de ubicados miente y **el listado que
-- se le entrega al salón está incompleto**. El salón cobra por cubierto.
--
-- ⚠️ No alcanzaba con reusar `admin_prealta`: esa mete el nombre entero
-- en `nombre` y deja `apellido` vacío, y el listado del salón se ordena
-- POR APELLIDO. Los padres quedarían todos juntos al final, sin apellido.
--
-- Esta migración SOLO AGREGA. No modifica ni borra nada de lo que ya
-- existe, así que se puede correr con un evento en curso.
-- ═══════════════════════════════════════════════════════════════════

create or replace function invitaciones.admin_agregar_invitado(
  p_evento   text,
  p_clave    text,
  p_nombre   text,
  p_apellido text,
  p_asiste   text default 'si',
  p_mesa     text default null
)
returns bigint
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_nombre   text := nullif(btrim(p_nombre), '');
  v_apellido text := nullif(btrim(p_apellido), '');
  v_asiste   text := coalesce(nullif(btrim(p_asiste), ''), 'si');
  v_mesa     text := nullif(btrim(coalesce(p_mesa, '')), '');
  v_n        integer;
  v_id       bigint;
begin
  if invitaciones.verificar_clave(p_evento, p_clave) is null then
    raise exception 'Clave incorrecta' using errcode = 'insufficient_privilege';
  end if;

  -- El apellido es obligatorio por la misma razón que en el RSVP: sin él
  -- no se puede armar la lista ordenada que se le da al salón.
  if v_nombre   is null then raise exception 'Falta el nombre'; end if;
  if v_apellido is null then raise exception 'Falta el apellido'; end if;

  if v_asiste not in ('si', 'no', 'pendiente') then
    raise exception 'Estado inválido';
  end if;

  -- Mismo tope que el RSVP: es spam lo que se está frenando, no una fuga.
  select count(*) into v_n
    from invitaciones.confirmaciones c
   where c.evento_id = p_evento;
  if v_n >= 2000 then
    raise exception 'Este evento ya tiene demasiados invitados cargados';
  end if;

  /* ⚠️ `invitado_url` va con una marca fija, no con un link inventado.
     La tarjeta de "Todavía no respondieron" del panel agrupa por
     `invitado_url` y arma un `wa.me` con ese texto adentro de la URL: si
     acá se guardara cualquier cosa, saldría un link roto a nombre del
     cliente. El panel saltea este valor en esa tarjeta. */
  insert into invitaciones.confirmaciones
    (evento_id, invitado_url, nombre, apellido, asiste, mesa, mensaje)
  values
    (p_evento, 'Cargado a mano', left(v_nombre, 60), left(v_apellido, 60),
     v_asiste, left(v_mesa, 12), '')
  returning id into v_id;

  return v_id;
end;
$$;

grant execute on function
  invitaciones.admin_agregar_invitado(text, text, text, text, text, text)
  to anon, authenticated;

-- PostgREST cachea las firmas: sin esto, la función nueva da 404.
notify pgrst, 'reload schema';
