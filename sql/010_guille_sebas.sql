-- =====================================================================
-- EL EVENTO DE GUILLERMINA & SEBASTIÁN EN EL PANEL
--
-- La invitación es a medida en el DISEÑO, no en el sistema: ellos
-- administran su fiesta desde `admin.html?evento=guille-sebas` igual que
-- cualquier cliente — generan los links, ven quién confirmó, bajan el
-- listado del salón y la lista del DJ.
--
-- Se corre UNA vez, pegándolo en el SQL Editor de Supabase (el conector
-- MCP no llega a este proyecto).
--
-- ⚠️ CAMBIÁ LA CLAVE ANTES DE CORRERLO. Abajo está en 'admin123', que es
-- la de los demos y la sabe cualquiera que haya visto una demo. Acá
-- adentro hay nombres, apellidos y preferencias alimentarias de los
-- invitados de una clienta que pagó $150.000.
-- =====================================================================

insert into invitaciones.eventos (id, config, admin_password)
values (
  'guille-sebas',
  jsonb_build_object(
    -- ⚠️ Estos campos NO pintan la invitación: la página de ellos es
    -- propia y trae sus textos adentro. Sirven para dos cosas nada más:
    --   1. la vista previa de WhatsApp, que la arma `api/i.js` leyendo
    --      `nombre`, `subtitulo`, `fecha_texto` y `salon`;
    --   2. los mensajes que el panel arma para mandar los links.
    'nombre',      'Guillermina & Sebastián',
    'tipo',        'Casamiento',
    'subtitulo',   'Nos casamos',
    'fecha_texto', 'Sábado 3 de abril de 2027',
    'hora_texto',  '18:00',
    'salon',       'Finca La Josefina, Berisso',
    'fecha_iso',   '2027-04-03T18:00',
    'zona_horaria','America/Argentina/Buenos_Aires'

    -- ⚠️⚠️ NO SE CARGAN `color_1`, `color_2` NI `color_bg`. Cuando
    -- existen, `api/i.js` inyecta un <style id="paleta-servidor"> que
    -- pisa --primary/--secondary/--bg. La página de ellos no usa esos
    -- nombres, así que hoy no rompe nada — pero es una bomba de tiempo:
    -- el día que alguien los cargue "para que se vea lindo en el panel",
    -- inyecta CSS en una invitación que no lo espera.
    --
    -- ⚠️ Tampoco va `foto_hero`. La vista previa cae entonces en
    -- `logo-og.png`, que es la placa de marca. Si se quiere la acuarela
    -- de ellos en la vista previa de WhatsApp, hay que SUBIRLA a Storage
    -- y poner acá su URL: la de la invitación está embebida como data
    -- URI adentro del HTML y un data URI no le sirve a ningún robot.
  ),
  'admin123'   -- ⚠️⚠️ CAMBIALA
)
on conflict (id) do update
  set config = excluded.config,
      updated_at = now();
-- ⚠️ El `do update` a propósito NO pisa `admin_password`: si esto se
-- vuelve a correr por cualquier motivo, no le cambia la clave a la
-- clienta en el medio de la fiesta.

-- Verificación: tiene que devolver una fila, y `admin_password` NO tiene
-- que poder leerse desde afuera (`anon` sólo lee id y config).
select id, config->>'nombre' as nombre, created_at
  from invitaciones.eventos
 where id = 'guille-sebas';
