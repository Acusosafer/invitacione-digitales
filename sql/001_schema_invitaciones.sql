-- =====================================================================
-- 001 — Schema `invitaciones`
-- Proyecto destino: ldvosdztnhrvrqxnjuco  ("Lo de Inés", cuenta fernando_22_19)
--
-- Modelo de seguridad
-- -------------------
-- La app es 100% cliente con la anon key a la vista de cualquier invitado.
-- Por lo tanto NADA sensible se protege con RLS (RLS filtra por *quién sos*,
-- y acá el admin y un invitado son el mismo rol `anon`).
--
-- En su lugar:
--   * `anon` puede leer SOLO las columnas (id, config) de `eventos`.
--     Nunca `admin_password`. Es un GRANT por columna, no una policy.
--   * `anon` NO tiene ningún acceso directo a `confirmaciones` ni a `ajustes`.
--   * Todo lo privilegiado pasa por funciones SECURITY DEFINER que verifican
--     la clave DENTRO de Postgres.
--
-- Idempotente: se puede correr más de una vez sin romper nada.
--
-- Todo va dentro de UNA transacción: si algo falla, no se aplica NADA.
-- No existe el escenario "quedó a medias".
-- =====================================================================

begin;

create schema if not exists invitaciones;

-- Que nadie tenga nada por defecto.
revoke all on schema invitaciones from public;
grant usage on schema invitaciones to anon, authenticated;


-- =====================================================================
-- TABLAS
-- =====================================================================

create table if not exists invitaciones.eventos (
  id             text primary key,
  config         jsonb       not null default '{}'::jsonb,
  admin_password text        not null default 'admin123',
  created_at     timestamptz not null default now(),
  updated_at     timestamptz not null default now()
);

comment on column invitaciones.eventos.admin_password is
  'Clave del cliente. `anon` NO tiene GRANT de lectura sobre esta columna.';

create table if not exists invitaciones.confirmaciones (
  id           bigint generated always as identity primary key,
  evento_id    text        not null references invitaciones.eventos(id) on delete cascade,
  invitado_url text        not null default 'general',
  nombre       text        not null,
  apellido     text        not null default '',
  asiste       text        not null default 'pendiente'
                 constraint confirmaciones_asiste_valido
                 check (asiste in ('si', 'no', 'pendiente')),
  personas     smallint    not null default 1 check (personas > 0),
  dieta        text        not null default '',
  mensaje      text        not null default '',
  mesa         text,
  created_at   timestamptz not null default now()
);

-- El acceso siempre es (evento_id) o (evento_id, invitado_url).
create index if not exists confirmaciones_evento_invitado_idx
  on invitaciones.confirmaciones (evento_id, invitado_url);

-- Ajustes globales. Acá vive el hash de superadmin: fuera del código fuente,
-- donde nadie puede leerlo ni romperlo por fuerza bruta.
create table if not exists invitaciones.ajustes (
  clave text primary key,
  valor text not null
);


-- =====================================================================
-- updated_at automático
-- =====================================================================

create or replace function invitaciones.tocar_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at := now();
  return new;
end;
$$;

drop trigger if exists eventos_updated_at on invitaciones.eventos;
create trigger eventos_updated_at
  before update on invitaciones.eventos
  for each row execute function invitaciones.tocar_updated_at();


-- =====================================================================
-- RLS
-- =====================================================================
-- `eventos`: lectura pública (la invitación tiene que poder leer su config).
-- La protección de `admin_password` NO es esta policy — es el GRANT por columna
-- de más abajo. Una policy de SELECT devuelve la fila ENTERA.

alter table invitaciones.eventos        enable row level security;
alter table invitaciones.confirmaciones enable row level security;
alter table invitaciones.ajustes        enable row level security;

drop policy if exists eventos_lectura_publica on invitaciones.eventos;
create policy eventos_lectura_publica
  on invitaciones.eventos
  for select
  to anon, authenticated
  using (true);

-- `confirmaciones` y `ajustes` quedan SIN policies a propósito:
-- RLS activo + cero policies = nadie entra por la puerta directa.
-- Solo se llega vía las funciones SECURITY DEFINER de abajo.


-- =====================================================================
-- GRANTS — mínimo indispensable
-- =====================================================================

revoke all on all tables in schema invitaciones from anon, authenticated;

-- Solo estas dos columnas. `admin_password` queda afuera a propósito:
-- con esto, `select=*` sobre eventos devuelve 42501 en vez de la clave.
grant select (id, config) on invitaciones.eventos to anon, authenticated;

-- Sobre `confirmaciones` y `ajustes`: ningún grant. Ni select.


-- =====================================================================
-- FUNCIONES — toda la lógica privilegiada
-- =====================================================================
-- Todas: SECURITY DEFINER + `set search_path = ''` + nombres calificados.
-- Sin search_path vacío, un search_path manipulado permitiría secuestrar
-- las llamadas internas. Es obligatorio, no opcional.

-- ---------------------------------------------------------------------
-- verificar_clave — reemplaza el `select admin_password` del cliente.
-- Devuelve 'super' | 'cliente' | null. La clave nunca vuelve al navegador.
-- ---------------------------------------------------------------------
create or replace function invitaciones.verificar_clave(
  p_evento text,
  p_clave  text
)
returns text
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_hash_super text;
  v_pass_event text;
begin
  if p_clave is null or p_clave = '' then
    return null;
  end if;

  -- ¿Superadmin? Se compara el SHA-256 hex, igual que hacía el JS.
  select a.valor into v_hash_super
    from invitaciones.ajustes a
   where a.clave = 'superadmin_hash';

  if v_hash_super is not null
     and v_hash_super <> 'PEGAR_HASH_ACA'
     and encode(sha256(convert_to(p_clave, 'utf8')), 'hex') = lower(v_hash_super)
  then
    return 'super';
  end if;

  -- ¿Clave del cliente para este evento?
  select e.admin_password into v_pass_event
    from invitaciones.eventos e
   where e.id = p_evento;

  if v_pass_event is not null and v_pass_event = p_clave then
    return 'cliente';
  end if;

  return null;
end;
$$;

-- ---------------------------------------------------------------------
-- ya_confirmo — para invitacion.html. Devuelve un booleano y nada más.
-- Antes esto era `select * from confirmaciones`, que mandaba al navegador
-- nombre, apellido, dieta, mensaje y mesa de todo el evento.
-- ---------------------------------------------------------------------
create or replace function invitaciones.ya_confirmo(
  p_evento   text,
  p_invitado text
)
returns boolean
language sql
security definer
set search_path = ''
stable
as $$
  select exists (
    select 1
      from invitaciones.confirmaciones c
     where c.evento_id    = p_evento
       and c.invitado_url = p_invitado
       and c.asiste      <> 'pendiente'
  );
$$;

-- ---------------------------------------------------------------------
-- rsvp_enviar — borra las filas pre-cargadas e inserta las reales,
-- en UNA transacción. Antes eran dos llamadas sueltas: si la segunda
-- fallaba, el invitado se quedaba sin fila y sin aviso.
-- ---------------------------------------------------------------------
create or replace function invitaciones.rsvp_enviar(
  p_evento   text,
  p_invitado text,
  p_filas    jsonb
)
returns integer
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_invitado text := coalesce(nullif(trim(p_invitado), ''), 'general');
  v_n        integer;
begin
  if not exists (select 1 from invitaciones.eventos e where e.id = p_evento) then
    raise exception 'Evento inexistente' using errcode = 'no_data_found';
  end if;

  if jsonb_typeof(p_filas) <> 'array' then
    raise exception 'Se esperaba un array de filas';
  end if;

  v_n := jsonb_array_length(p_filas);
  if v_n = 0 then
    raise exception 'No hay filas para guardar';
  end if;
  -- Techo defensivo: evita que alguien mande 10.000 filas de una.
  if v_n > 20 then
    raise exception 'Demasiadas personas en una sola confirmación';
  end if;

  delete from invitaciones.confirmaciones c
   where c.evento_id    = p_evento
     and c.invitado_url = v_invitado;

  insert into invitaciones.confirmaciones
    (evento_id, invitado_url, nombre, apellido, asiste, personas, dieta, mensaje, mesa)
  select
    p_evento,
    v_invitado,
    left(coalesce(f->>'nombre',   ''), 80),
    left(coalesce(f->>'apellido', ''), 80),
    case when f->>'asiste' in ('si', 'no', 'pendiente')
         then f->>'asiste' else 'pendiente' end,
    1,
    left(coalesce(f->>'dieta',   ''), 200),
    left(coalesce(f->>'mensaje', ''), 500),
    nullif(left(coalesce(f->>'mesa', ''), 20), '')
  from jsonb_array_elements(p_filas) as f
  where coalesce(trim(f->>'nombre'), '') <> '';

  get diagnostics v_n = row_count;
  return v_n;
end;
$$;

-- ---------------------------------------------------------------------
-- admin_invitados — la lista completa, SOLO con clave válida.
-- ---------------------------------------------------------------------
create or replace function invitaciones.admin_invitados(
  p_evento text,
  p_clave  text
)
returns setof invitaciones.confirmaciones
language plpgsql
security definer
set search_path = ''
as $$
begin
  if invitaciones.verificar_clave(p_evento, p_clave) is null then
    raise exception 'Clave incorrecta' using errcode = 'insufficient_privilege';
  end if;

  return query
    select c.* from invitaciones.confirmaciones c
     where c.evento_id = p_evento
     order by c.created_at desc;
end;
$$;

-- ---------------------------------------------------------------------
-- admin_guardar_evento — reemplaza el upsert abierto.
-- Evento nuevo: lo crea cualquiera (hace falta para dar de alta clientes).
-- Evento existente: exige la clave correcta.
-- ---------------------------------------------------------------------
create or replace function invitaciones.admin_guardar_evento(
  p_evento      text,
  p_clave       text,
  p_config      jsonb,
  p_nueva_clave text default null
)
returns text
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_existe boolean;
begin
  if coalesce(trim(p_evento), '') = '' then
    raise exception 'Falta el id del evento';
  end if;

  select exists (select 1 from invitaciones.eventos e where e.id = p_evento)
    into v_existe;

  if not v_existe then
    insert into invitaciones.eventos (id, config, admin_password)
    values (p_evento, coalesce(p_config, '{}'::jsonb),
            coalesce(nullif(trim(p_nueva_clave), ''), 'admin123'));
    return 'creado';
  end if;

  if invitaciones.verificar_clave(p_evento, p_clave) is null then
    raise exception 'Clave incorrecta' using errcode = 'insufficient_privilege';
  end if;

  update invitaciones.eventos e
     set config         = coalesce(p_config, e.config),
         admin_password = coalesce(nullif(trim(p_nueva_clave), ''), e.admin_password)
   where e.id = p_evento;

  return 'actualizado';
end;
$$;

-- ---------------------------------------------------------------------
-- admin_prealta — filas 'pendiente' del generador de links.
-- ---------------------------------------------------------------------
create or replace function invitaciones.admin_prealta(
  p_evento   text,
  p_clave    text,
  p_invitado text,
  p_cupos    integer
)
returns integer
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_invitado text := nullif(trim(p_invitado), '');
  v_cupos    integer := greatest(1, least(coalesce(p_cupos, 1), 20));
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

  return v_cupos;
end;
$$;

-- ---------------------------------------------------------------------
-- admin_actualizar_fila — cambiar `asiste` o `mesa` desde el panel.
-- ---------------------------------------------------------------------
create or replace function invitaciones.admin_actualizar_fila(
  p_evento text,
  p_clave  text,
  p_id     bigint,
  p_asiste text default null,
  p_mesa   text default null
)
returns boolean
language plpgsql
security definer
set search_path = ''
as $$
begin
  if invitaciones.verificar_clave(p_evento, p_clave) is null then
    raise exception 'Clave incorrecta' using errcode = 'insufficient_privilege';
  end if;

  update invitaciones.confirmaciones c
     set asiste = case
                    when p_asiste in ('si', 'no', 'pendiente') then p_asiste
                    else c.asiste
                  end,
         -- '' significa "sacar de la mesa"; null significa "no tocar".
         mesa   = case
                    when p_mesa is null then c.mesa
                    when trim(p_mesa) = '' then null
                    else left(trim(p_mesa), 20)
                  end
   where c.id = p_id
     and c.evento_id = p_evento;   -- ata la fila al evento cuya clave se validó

  return found;
end;
$$;

-- ---------------------------------------------------------------------
-- admin_borrar_fila
-- ---------------------------------------------------------------------
create or replace function invitaciones.admin_borrar_fila(
  p_evento text,
  p_clave  text,
  p_id     bigint
)
returns boolean
language plpgsql
security definer
set search_path = ''
as $$
begin
  if invitaciones.verificar_clave(p_evento, p_clave) is null then
    raise exception 'Clave incorrecta' using errcode = 'insufficient_privilege';
  end if;

  delete from invitaciones.confirmaciones c
   where c.id = p_id and c.evento_id = p_evento;

  return found;
end;
$$;


-- =====================================================================
-- EXECUTE — explícito, nunca por defecto
-- =====================================================================
-- Postgres le da EXECUTE a `public` automáticamente en toda función nueva.
-- Hay que revocarlo y otorgar una por una.

revoke execute on all functions in schema invitaciones from public, anon, authenticated;

grant execute on function invitaciones.verificar_clave(text, text)             to anon, authenticated;
grant execute on function invitaciones.ya_confirmo(text, text)                 to anon, authenticated;
grant execute on function invitaciones.rsvp_enviar(text, text, jsonb)          to anon, authenticated;
grant execute on function invitaciones.admin_invitados(text, text)             to anon, authenticated;
grant execute on function invitaciones.admin_guardar_evento(text, text, jsonb, text) to anon, authenticated;
grant execute on function invitaciones.admin_prealta(text, text, text, integer) to anon, authenticated;
grant execute on function invitaciones.admin_actualizar_fila(text, text, bigint, text, text) to anon, authenticated;
grant execute on function invitaciones.admin_borrar_fila(text, text, bigint)   to anon, authenticated;

-- `tocar_updated_at` es solo para el trigger: nadie la llama desde afuera.


-- =====================================================================
-- SEMILLA — hash de superadmin
-- =====================================================================
-- Sale del código fuente y entra acá, donde `anon` no puede leerlo.

insert into invitaciones.ajustes (clave, valor)
values ('superadmin_hash',
        '5cdfe19011b4fbb897f6b03ab72b187b8a8e87f289e531b75a48a1ccc731b9c7')
on conflict (clave) do update set valor = excluded.valor;

commit;


-- =====================================================================
-- EXPONER EL SCHEMA A LA API
-- =====================================================================
-- Preferible hacerlo por el Dashboard:
--   Settings → API → Exposed schemas → agregar `invitaciones`
-- Si no aparece la opción, descomentar estas dos líneas:
--
-- alter role authenticator set pgrst.db_schemas = 'public, graphql_public, invitaciones';
-- notify pgrst, 'reload config';
