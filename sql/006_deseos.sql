-- ═══════════════════════════════════════════════════════════════════
-- 006 · El libro de deseos
--
-- Lo que escribe el invitado cuando apoya el celular en el tag NFC de la
-- mesa, o escanea el QR del cartelito.
--
-- ⚠️ ES UN BUZÓN PRIVADO, decidido el 27/08/2026. El invitado ESCRIBE y
-- nada más: no puede leer un solo deseo, ni el suyo. Los lee la clienta
-- desde su panel, con su clave. Por eso `deseos` no tiene ningún grant
-- para `anon` y la única función pública devuelve un número, no filas.
--
-- ⚠️ El texto lo escribe un invitado y termina en el panel de la clienta.
-- Se guarda como texto plano y en el panel se pinta con DOM, nunca con
-- innerHTML — igual que la lista del DJ.
-- ═══════════════════════════════════════════════════════════════════

create table if not exists invitaciones.deseos (
  id         bigint generated always as identity primary key,
  evento_id  text        not null references invitaciones.eventos(id) on delete cascade,
  nombre     text        not null,
  deseo      text        not null,
  mesa       text,
  created_at timestamptz not null default now()
);

comment on table invitaciones.deseos is
  'Buzón privado del libro de deseos. El invitado solo inserta (por función); leer exige la clave del panel. `anon` no tiene NINGÚN grant sobre esta tabla.';

create index if not exists deseos_evento_idx
  on invitaciones.deseos (evento_id, created_at desc);

alter table invitaciones.deseos enable row level security;

-- Sin policies y sin grants: nadie llega por la API REST.
revoke all on invitaciones.deseos from public, anon, authenticated;

-- ---------------------------------------------------------------------
-- deseo_enviar — LA ÚNICA función pública. Escribe y devuelve el número
-- de deseo que le tocó, que es lo que ve el invitado en pantalla.
--
-- ⚠️ Devuelve un entero, NUNCA filas: si devolviera la lista, cualquiera
-- con el slug del evento leería los mensajes de todos los invitados.
--
-- Riesgo aceptado, el mismo del RSVP: quien sepa el slug puede escribir.
-- Es spam, no una fuga. Por eso el tope de 2000 por evento.
-- ---------------------------------------------------------------------
create or replace function invitaciones.deseo_enviar(
  p_evento text,
  p_nombre text,
  p_deseo  text,
  p_mesa   text default null
)
returns integer
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_nombre text := nullif(btrim(p_nombre), '');
  v_deseo  text := nullif(btrim(p_deseo), '');
  v_mesa   text := nullif(btrim(coalesce(p_mesa, '')), '');
  v_cfg    jsonb;
  v_n      integer;
begin
  select e.config into v_cfg
    from invitaciones.eventos e
   where e.id = p_evento;

  if v_cfg is null then
    raise exception 'El evento no existe';
  end if;

  -- Se activa desde el panel. Un evento que no lo contrató no recibe nada.
  if coalesce((v_cfg->>'deseos_activo')::boolean, false) is not true then
    raise exception 'El libro de deseos no está activo para este evento';
  end if;

  -- Una invitación pausada no recibe deseos, igual que no recibe RSVP.
  if coalesce((v_cfg->>'pausada')::boolean, false) is true then
    raise exception 'Esta invitación está pausada';
  end if;

  if v_deseo  is null then raise exception 'Falta el deseo'; end if;
  if v_nombre is null then raise exception 'Falta el nombre'; end if;

  select count(*) into v_n
    from invitaciones.deseos d
   where d.evento_id = p_evento;

  if v_n >= 2000 then
    raise exception 'Este libro de deseos ya está completo';
  end if;

  insert into invitaciones.deseos (evento_id, nombre, deseo, mesa)
  values (p_evento, left(v_nombre, 60), left(v_deseo, 600), left(v_mesa, 12));

  return v_n + 1;
end;
$$;

-- ---------------------------------------------------------------------
-- admin_deseos — la lista completa, SOLO con clave.
-- ---------------------------------------------------------------------
create or replace function invitaciones.admin_deseos(
  p_evento text,
  p_clave  text
)
returns setof invitaciones.deseos
language plpgsql
security definer
set search_path = ''
as $$
begin
  if invitaciones.verificar_clave(p_evento, p_clave) is null then
    raise exception 'Clave incorrecta' using errcode = 'insufficient_privilege';
  end if;

  return query
    select d.* from invitaciones.deseos d
     where d.evento_id = p_evento
     order by d.created_at desc;
end;
$$;

-- ---------------------------------------------------------------------
-- admin_borrar_deseo — para el que no corresponde. Borra de verdad: en
-- una fiesta de una clienta, un mensaje fuera de lugar no se esconde,
-- se saca.
-- ---------------------------------------------------------------------
create or replace function invitaciones.admin_borrar_deseo(
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

  delete from invitaciones.deseos d
   where d.id = p_id and d.evento_id = p_evento;

  return found;
end;
$$;

-- ---------------------------------------------------------------------
-- GRANTS
-- ---------------------------------------------------------------------
grant execute on function invitaciones.deseo_enviar(text, text, text, text)   to anon, authenticated;
grant execute on function invitaciones.admin_deseos(text, text)               to anon, authenticated;
grant execute on function invitaciones.admin_borrar_deseo(text, text, bigint) to anon, authenticated;

-- PostgREST cachea las firmas: sin esto, las funciones nuevas dan 404.
notify pgrst, 'reload schema';
