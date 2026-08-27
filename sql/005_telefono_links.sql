-- ═══════════════════════════════════════════════════════════════════
-- 005 · El teléfono del link
--
-- Para qué: hoy "Recordar" arma un `wa.me/?text=` sin número, así que
-- WhatsApp abre el selector de contactos y hay que buscar a la persona
-- a mano. Con el número guardado, el mismo botón abre SU chat.
--
-- ⚠️ Son datos personales de invitados de un cliente. Por eso NO van en
-- `confirmaciones` (que se borra y se reinserta en cada RSVP) sino en su
-- propia tabla, sin un solo grant para `anon`: se leen únicamente desde
-- funciones `security definer` que exigen la clave del panel.
--
-- De paso queda guardado `cupos`, que hasta hoy no se guardaba en ningún
-- lado y se deducía contando filas — así que una confirmación mal hecha
-- no tenía contra qué compararse.
-- ═══════════════════════════════════════════════════════════════════

create table if not exists invitaciones.links (
  evento_id    text        not null references invitaciones.eventos(id) on delete cascade,
  invitado_url text        not null,
  telefono     text        not null default '',
  cupos        smallint    not null default 1,
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now(),
  primary key (evento_id, invitado_url)
);

comment on table invitaciones.links is
  'Un renglón por link generado. Guarda el teléfono al que se mandó y los cupos asignados. `anon` no tiene NINGÚN grant sobre esta tabla.';

alter table invitaciones.links enable row level security;

-- Sin policies y sin grants: nadie llega por la API REST. Todo pasa por
-- las funciones de abajo, que son `security definer` y piden la clave.
revoke all on invitaciones.links from public, anon, authenticated;

-- ---------------------------------------------------------------------
-- admin_prealta — ahora con teléfono. Cambia la cantidad de parámetros,
-- así que hay que BORRAR la vieja: `create or replace` con otra firma
-- crea una sobrecarga y PostgREST no sabe cuál llamar.
-- ⚠️ El drop se lleva puesto el grant. Se vuelve a dar al final.
-- ---------------------------------------------------------------------
drop function if exists invitaciones.admin_prealta(text, text, text, integer);

create or replace function invitaciones.admin_prealta(
  p_evento   text,
  p_clave    text,
  p_invitado text,
  p_cupos    integer,
  p_telefono text default ''
)
returns integer
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_invitado text    := nullif(trim(p_invitado), '');
  v_cupos    integer := greatest(1, least(coalesce(p_cupos, 1), 20));
  v_tel      text    := coalesce(regexp_replace(coalesce(p_telefono, ''), '\D', '', 'g'), '');
  i          integer;
begin
  if invitaciones.verificar_clave(p_evento, p_clave) is null then
    raise exception 'Clave incorrecta' using errcode = 'insufficient_privilege';
  end if;
  if v_invitado is null then
    raise exception 'Falta el nombre del invitado';
  end if;

  -- Regenerar el link de alguien no debe duplicarle las filas.
  delete from invitaciones.confirmaciones c
   where c.evento_id    = p_evento
     and c.invitado_url = v_invitado
     and c.asiste       = 'pendiente';

  insert into invitaciones.confirmaciones
    (evento_id, invitado_url, nombre, apellido, asiste, mensaje)
  values
    (p_evento, v_invitado, v_invitado, '', 'pendiente', 'Invitación pre-cargada');

  for i in 2..v_cupos loop
    insert into invitaciones.confirmaciones
      (evento_id, invitado_url, nombre, apellido, asiste, mensaje)
    values
      (p_evento, v_invitado, 'Acompañante ' || i, 'de ' || v_invitado,
       'pendiente', 'Acompañante pre-cargado');
  end loop;

  -- ⚠️ Un teléfono vacío NO pisa el que ya estaba: regenerar un link sin
  -- volver a escribir el número no tiene que borrarlo.
  insert into invitaciones.links as l (evento_id, invitado_url, telefono, cupos)
  values (p_evento, v_invitado, v_tel, v_cupos)
  on conflict (evento_id, invitado_url) do update
     set cupos      = excluded.cupos,
         telefono   = case when excluded.telefono <> '' then excluded.telefono
                           else l.telefono end,
         updated_at = now();

  return v_cupos;
end;
$$;

-- ---------------------------------------------------------------------
-- admin_links — los links de un evento con su teléfono. Solo con clave.
-- ---------------------------------------------------------------------
create or replace function invitaciones.admin_links(
  p_evento text,
  p_clave  text
)
returns table (invitado_url text, telefono text, cupos smallint)
language plpgsql
security definer
set search_path = ''
as $$
begin
  if invitaciones.verificar_clave(p_evento, p_clave) is null then
    raise exception 'Clave incorrecta' using errcode = 'insufficient_privilege';
  end if;

  return query
    select l.invitado_url, l.telefono, l.cupos
      from invitaciones.links l
     where l.evento_id = p_evento;
end;
$$;

-- ---------------------------------------------------------------------
-- admin_link_telefono — cargar o corregir el número de un link que ya
-- existe. Hace falta para todos los links generados antes de hoy.
-- Con el teléfono vacío, BORRA el número guardado (para corregir un error).
-- ---------------------------------------------------------------------
create or replace function invitaciones.admin_link_telefono(
  p_evento   text,
  p_clave    text,
  p_invitado text,
  p_telefono text
)
returns text
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_invitado text := nullif(trim(p_invitado), '');
  v_tel      text := coalesce(regexp_replace(coalesce(p_telefono, ''), '\D', '', 'g'), '');
  v_cupos    smallint;
begin
  if invitaciones.verificar_clave(p_evento, p_clave) is null then
    raise exception 'Clave incorrecta' using errcode = 'insufficient_privilege';
  end if;
  if v_invitado is null then
    raise exception 'Falta el nombre del invitado';
  end if;

  -- Los links viejos no tienen fila en `links`: los cupos se deducen
  -- contando las filas pendientes, igual que hace el panel.
  select greatest(1, count(*))::smallint into v_cupos
    from invitaciones.confirmaciones c
   where c.evento_id    = p_evento
     and c.invitado_url = v_invitado
     and c.asiste       = 'pendiente';

  insert into invitaciones.links as l (evento_id, invitado_url, telefono, cupos)
  values (p_evento, v_invitado, v_tel, v_cupos)
  on conflict (evento_id, invitado_url) do update
     set telefono = excluded.telefono, updated_at = now();

  return v_tel;
end;
$$;

-- ---------------------------------------------------------------------
-- GRANTS — el drop de arriba se llevó el de admin_prealta.
-- ---------------------------------------------------------------------
grant execute on function invitaciones.admin_prealta(text, text, text, integer, text) to anon, authenticated;
grant execute on function invitaciones.admin_links(text, text)                        to anon, authenticated;
grant execute on function invitaciones.admin_link_telefono(text, text, text, text)    to anon, authenticated;

-- PostgREST cachea las firmas: sin esto, las funciones nuevas dan 404.
notify pgrst, 'reload schema';
