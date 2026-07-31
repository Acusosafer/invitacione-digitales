# Prompts para generar las fotos de los demos

> Para pegar en Higgsfield. **Siempre pedir `use_unlim: true`** en cada generación (si no, consume créditos).
> Faltan 9 eventos: 3 de quince y los 6 casamientos.

---

## Cómo usar esto

Cada evento tiene un **PERSONAJE** — la descripción física fija de la persona o pareja. Esa descripción se copia **textual al principio de los 5 prompts del evento**. Es lo único que garantiza que sea la misma chica (o la misma pareja) en todas las fotos y no cinco personas distintas.

Si Higgsfield te deja usar una imagen de referencia: generá primero el `foto_splash`, y usá esa cara como referencia para las otras cuatro. Sale mucho mejor.

### Tamaños y dónde va cada foto

| Archivo | Tamaño | Formato | Nota |
|---|---|---|---|
| `foto_splash` | 600×600 | Cuadrada → se recorta en círculo | Cara centrada, dejar aire en los bordes |
| `foto_hero` | 1920×1080 | Horizontal | **Debe ser oscura/desaturada** — lleva overlay negro 40% y texto blanco encima |
| `foto_galeria_1` | 800×800 | Cuadrada | |
| `foto_galeria_2` | 800×800 | Cuadrada | |
| `foto_hashtag` | 400×400 | Cuadrada → círculo | Cara centrada |

**Guardar en:** `assets/{eventoId}/foto_splash.png`, etc. Respetar esos nombres exactos.

---

# 15 AÑOS

## valentina15 — Dark / Verde acento (`#1a1a1a` / `#d6ecc0`)

**PERSONAJE:** `A 15-year-old Argentine girl with long dark wavy hair, warm olive skin, brown eyes, natural light makeup, wearing an elegant floor-length sage green formal gown,`

1. **foto_splash (600×600)**
```
[PERSONAJE] centered square portrait, head and shoulders, looking at camera with 
a soft genuine smile, dark charcoal studio background, soft key light from the 
left, subtle rim light separating her from the background, generous empty space 
around her head, professional portrait photography, 85mm lens, f/2.0
```

2. **foto_hero (1920×1080)**
```
[PERSONAJE] full body, standing in an elegant dimly lit ballroom at night, 
dark moody atmosphere, warm string lights blurred in the deep background, 
she is positioned on the right third of the frame leaving empty dark space on 
the left, low key lighting, desaturated dark tones, cinematic wide shot, 35mm
```

3. **foto_galeria_1 (800×800)**
```
[PERSONAJE] square format, candid moment laughing while her dress spins, 
dark elegant venue, sage green accent lighting, shallow depth of field, 
joyful and natural, editorial event photography, 50mm
```

4. **foto_galeria_2 (800×800)**
```
Square detail shot, close-up of sage green formal shoes and the hem of a dark 
green gown on a polished dark wooden floor, soft warm light pooling, elegant 
party details, shallow depth of field, moody dark tones, macro, no people faces
```

5. **foto_hashtag (400×400)**
```
[PERSONAJE] centered square close-up portrait, looking slightly off camera, 
soft smile, dark background, sage green bokeh lights behind her, warm intimate 
lighting, face centered in frame with space around it, 85mm, f/1.8
```

---

## martina15 — Blanco Mármol (`#fafaf8` / `#c8b89a`)

**PERSONAJE:** `A 15-year-old Argentine girl with straight light brown hair pulled into an elegant low bun, fair skin, hazel eyes, soft natural makeup, wearing a champagne beige satin floor-length gown,`

1. **foto_splash (600×600)**
```
[PERSONAJE] centered square portrait, head and shoulders, serene elegant 
expression, bright white marble wall background, soft diffused natural light, 
airy and clean, minimal, generous empty space around her, editorial portrait 
photography, 85mm, f/2.0
```

2. **foto_hero (1920×1080)**
```
[PERSONAJE] full body, standing in a luxurious bright hall with white marble 
floors and tall windows, elegant classical architecture, soft overcast daylight, 
she stands on the left third leaving open space on the right, muted beige and 
cream palette, slightly desaturated so white text reads well, cinematic wide, 35mm
```

3. **foto_galeria_1 (800×800)**
```
[PERSONAJE] square format, walking down a wide marble staircase, hand on the 
railing, looking back over her shoulder, soft natural light, cream and beige 
tones, elegant editorial fashion photography, 50mm
```

4. **foto_galeria_2 (800×800)**
```
Square detail shot, elegant table setting with white marble surface, champagne 
glasses, beige linen napkins and small white flower arrangements, soft window 
light from the side, luxurious and minimal, warm neutral palette, shallow depth 
of field, no people
```

5. **foto_hashtag (400×400)**
```
[PERSONAJE] centered square close-up portrait, gentle smile looking down, 
bright airy white background, soft natural light, minimal clean composition, 
face centered with space around it, 85mm, f/1.8
```

---

## luna15 — Verde Botánica (`#f5f8f2` / `#7ab87a`)

**PERSONAJE:** `A 15-year-old Argentine girl with long curly dark brown hair worn loose, tan skin, dark eyes, fresh natural makeup, wearing a flowing white cotton dress with delicate green botanical embroidery,`

1. **foto_splash (600×600)**
```
[PERSONAJE] centered square portrait, head and shoulders, bright genuine smile, 
lush green garden foliage softly blurred behind her, dappled natural sunlight, 
fresh and vibrant, generous space around her head, outdoor portrait photography, 
85mm, f/2.0
```

2. **foto_hero (1920×1080)**
```
[PERSONAJE] full body walking through a lush botanical garden with tall green 
plants and ferns, golden hour backlight filtering through leaves, she is on the 
right third of frame with open greenery on the left, rich but slightly darkened 
green tones so white text stays readable, cinematic wide shot, 35mm
```

3. **foto_galeria_1 (800×800)**
```
[PERSONAJE] square format, sitting on a stone bench in a garden surrounded by 
plants, relaxed candid pose looking away and smiling, warm afternoon light, 
natural greens and creams, lifestyle photography, 50mm
```

4. **foto_galeria_2 (800×800)**
```
Square detail shot, close-up of hands holding a bouquet of white and green 
wildflowers and eucalyptus, natural daylight, fresh botanical textures, soft 
green background bokeh, macro, shallow depth of field, no faces
```

5. **foto_hashtag (400×400)**
```
[PERSONAJE] centered square close-up portrait, laughing naturally, soft green 
foliage bokeh background, warm sunlight on her face, joyful and fresh, face 
centered with space around it, 85mm, f/1.8
```

---

# CASAMIENTOS

> En todos: la **misma pareja** en las 5 fotos del evento. Copiar el PERSONAJE textual.

## boda-ana — Ana & José · Clásico Dorado (`#fffef9` / `#c9a96e`)

**PERSONAJE:** `An Argentine couple in their early thirties: the bride has dark hair in a soft elegant updo, olive skin, wearing a classic ivory A-line wedding gown with a long veil; the groom has short dark hair, light beard, wearing a black classic tuxedo with bow tie,`

1. **foto_splash (600×600)**
```
[PERSONAJE] centered square portrait of the couple, head and shoulders, foreheads 
gently touching, eyes closed, soft smiles, warm ivory and gold background softly 
blurred, golden warm light, romantic and timeless, generous space around them, 
85mm, f/2.0
```

2. **foto_hero (1920×1080)**
```
[PERSONAJE] full body, standing together in an elegant classic church with warm 
golden light streaming through tall windows, ornate architecture, they are on 
the right third leaving open space on the left, warm gold and ivory palette 
slightly darkened for white text overlay, cinematic wide shot, 35mm
```

3. **foto_galeria_1 (800×800)**
```
[PERSONAJE] square format, first dance, the groom spinning the bride, her gown 
flowing, warm golden chandelier light, elegant ballroom softly blurred behind, 
joyful movement, wedding editorial photography, 50mm
```

4. **foto_galeria_2 (800×800)**
```
Square detail shot, two gold wedding rings resting on an ivory silk fabric next 
to a small bouquet of white roses, warm golden light from the side, luxurious 
classic textures, macro, shallow depth of field, no people
```

5. **foto_hashtag (400×400)**
```
[PERSONAJE] centered square close-up, the bride laughing while the groom kisses 
her cheek, warm golden bokeh background, intimate candid moment, faces centered 
with space around them, 85mm, f/1.8
```

---

## boda-elena — Elena & Pablo · Negro & Dorado (`#0d0d0d` / `#d4af37`)

**PERSONAJE:** `An elegant Argentine couple in their thirties: the bride has sleek dark hair worn straight and long, pale skin, bold makeup, wearing a fitted satin ivory gown with thin straps; the groom has dark hair combed back, clean shaven, wearing a black velvet tuxedo,`

1. **foto_splash (600×600)**
```
[PERSONAJE] centered square portrait of the couple, head and shoulders, looking 
at camera confidently, deep black background, dramatic golden rim lighting from 
behind, high fashion editorial style, generous dark space around them, 85mm, f/2.0
```

2. **foto_hero (1920×1080)**
```
[PERSONAJE] full body, standing in a dark luxurious ballroom at night, golden 
chandeliers glowing in the deep background, dramatic low key lighting, they are 
on the right third with dark empty space on the left, black and gold palette, 
very dark and moody, cinematic wide shot, 35mm
```

3. **foto_galeria_1 (800×800)**
```
[PERSONAJE] square format, dancing closely under warm golden lights in a dark 
venue, elegant and intimate, black background with gold bokeh, dramatic 
contrast, luxury wedding editorial, 50mm
```

4. **foto_galeria_2 (800×800)**
```
Square detail shot, two crystal champagne glasses touching in a toast against a 
pure black background, golden light catching the glass edges, gold confetti 
floating, dramatic dark luxury, shallow depth of field, no people
```

5. **foto_hashtag (400×400)**
```
[PERSONAJE] centered square close-up of the couple kissing, dark background with 
warm golden bokeh lights behind them, dramatic intimate lighting, faces centered 
with space around them, 85mm, f/1.8
```

---

## boda-maria — María & Ramiro · Verde Rústico (`#f5f5ee` / `#a0b880`)

**PERSONAJE:** `An Argentine couple in their late twenties: the bride has wavy light brown hair worn loose with small flowers, freckled skin, natural makeup, wearing a simple flowing bohemian ivory gown; the groom has curly brown hair, short beard, wearing a beige linen suit with no tie,`

1. **foto_splash (600×600)**
```
[PERSONAJE] centered square portrait of the couple, head and shoulders, laughing 
together naturally, soft green countryside foliage blurred behind, warm golden 
hour light, relaxed and rustic, generous space around them, 85mm, f/2.0
```

2. **foto_hero (1920×1080)**
```
[PERSONAJE] full body walking hand in hand through a rustic olive grove at golden 
hour, warm sunlight filtering through green leaves, wooden fence and rolling 
countryside behind, they are on the right third with open field on the left, 
sage green and cream palette slightly darkened, cinematic wide, 35mm
```

3. **foto_galeria_1 (800×800)**
```
[PERSONAJE] square format, outdoor rustic reception under string lights hanging 
between trees, the couple toasting with guests blurred around them, warm evening 
light, natural greens and warm wood tones, documentary wedding photography, 50mm
```

4. **foto_galeria_2 (800×800)**
```
Square detail shot, a long rustic wooden table set outdoors with eucalyptus 
garlands, simple ceramic plates and small glass jars with wildflowers, warm 
golden hour light, countryside wedding details, shallow depth of field, no people
```

5. **foto_hashtag (400×400)**
```
[PERSONAJE] centered square close-up, the couple pressing foreheads together and 
smiling, soft green natural bokeh behind, warm golden light, relaxed and intimate, 
faces centered with space around them, 85mm, f/1.8
```

---

## boda-carolina — Carolina & Martín · Terracotta (`#faf6f0` / `#d4845a`)

**PERSONAJE:** `An Argentine couple in their thirties: the bride has dark hair in a loose textured updo, warm tan skin, sun-kissed natural makeup, wearing a modern ivory gown with open back; the groom has dark hair, well groomed beard, wearing a warm terracotta brown suit,`

1. **foto_splash (600×600)**
```
[PERSONAJE] centered square portrait of the couple, head and shoulders, warm 
genuine smiles looking at camera, terracotta clay wall background softly blurred, 
warm sunset light, earthy and modern, generous space around them, 85mm, f/2.0
```

2. **foto_hero (1920×1080)**
```
[PERSONAJE] full body standing in a desert-toned open courtyard with terracotta 
walls and dried pampas grass, warm sunset light casting long shadows, they are on 
the right third leaving warm textured wall space on the left, terracotta and cream 
palette, slightly darkened for text overlay, cinematic wide shot, 35mm
```

3. **foto_galeria_1 (800×800)**
```
[PERSONAJE] square format, the couple walking away from camera holding hands under 
a warm terracotta archway, sunset light flaring, romantic and modern, earthy warm 
tones, editorial wedding photography, 50mm
```

4. **foto_galeria_2 (800×800)**
```
Square detail shot, a bouquet of dried pampas grass, terracotta roses and dried 
palm leaves resting against a warm clay textured wall, sunset light, earthy modern 
boho wedding details, shallow depth of field, no people
```

5. **foto_hashtag (400×400)**
```
[PERSONAJE] centered square close-up of the bride laughing with the groom behind 
her holding her waist, warm terracotta bokeh background, golden sunset light on 
their faces, faces centered with space around them, 85mm, f/1.8
```

---

## boda-valentina — Valentina & Nicolás · Blush Pink (`#fdf5f7` / `#e8b4c0`)

**PERSONAJE:** `An Argentine couple in their late twenties: the bride has soft blonde hair in loose romantic waves, fair rosy skin, delicate makeup, wearing a soft tulle ivory gown with blush pink undertones; the groom has light brown hair, clean shaven, wearing a light grey suit with a blush pink tie,`

1. **foto_splash (600×600)**
```
[PERSONAJE] centered square portrait of the couple, head and shoulders, soft 
tender expressions looking at each other, pale blush pink background softly 
blurred, very soft diffused light, dreamy and romantic, generous space around 
them, 85mm, f/2.0
```

2. **foto_hero (1920×1080)**
```
[PERSONAJE] full body in a garden full of blooming pale pink roses and cherry 
blossoms, soft overcast diffused daylight, dreamy pastel atmosphere, they are on 
the right third with flowering branches on the left, blush pink and cream palette 
slightly darkened so white text is legible, cinematic wide shot, 35mm
```

3. **foto_galeria_1 (800×800)**
```
[PERSONAJE] square format, the groom lifting the bride and spinning her while she 
laughs, surrounded by soft pink blossoms, tulle gown floating, soft romantic light, 
pastel palette, joyful editorial wedding photography, 50mm
```

4. **foto_galeria_2 (800×800)**
```
Square detail shot, a soft bouquet of blush pink garden roses, peonies and baby's 
breath on a pale linen surface, soft diffused natural light, delicate romantic 
pastel tones, macro, shallow depth of field, no people
```

5. **foto_hashtag (400×400)**
```
[PERSONAJE] centered square close-up of the couple with foreheads touching and 
eyes closed, soft blush pink bokeh background, gentle diffused light, tender and 
romantic, faces centered with space around them, 85mm, f/1.8
```

---

## boda-julieta — Julieta & Tomás · Azul Noche (`#080f1a` / `#7090c0`)

**PERSONAJE:** `An Argentine couple in their thirties: the bride has very dark hair in a sleek low bun, olive skin, defined elegant makeup, wearing a structured ivory silk gown; the groom has black hair, short beard, wearing a midnight navy blue tuxedo,`

1. **foto_splash (600×600)**
```
[PERSONAJE] centered square portrait of the couple, head and shoulders, calm 
confident expressions, deep midnight blue background, cool moonlight key light 
with soft blue rim light, elegant and cinematic, generous dark space around them, 
85mm, f/2.0
```

2. **foto_hero (1920×1080)**
```
[PERSONAJE] full body standing outdoors at night under a deep blue starry sky, 
distant warm venue lights blurred far behind, cool blue moonlight as main light, 
they are on the right third with dark blue night sky on the left, very dark 
midnight blue palette, cinematic wide shot, 35mm
```

3. **foto_galeria_1 (800×800)**
```
[PERSONAJE] square format, the couple dancing outdoors at night under hanging 
string lights, deep blue night atmosphere with warm light accents on their faces, 
romantic and cinematic, dark blue palette, 50mm
```

4. **foto_galeria_2 (800×800)**
```
Square detail shot, elegant table setting at night with deep navy blue linen, 
silver cutlery, white candles glowing and small white flowers, dark moody 
atmosphere, warm candlelight against deep blue tones, shallow depth of field, 
no people
```

5. **foto_hashtag (400×400)**
```
[PERSONAJE] centered square close-up of the couple kissing under the night sky, 
deep blue background with soft warm bokeh lights, cool moonlight on their faces, 
faces centered with space around them, 85mm, f/1.8
```

---

## Notas finales

- **Generá 2-3 variantes de cada `foto_splash` primero.** Elegí la cara que más te guste y usala como referencia para las otras 4 del mismo evento. Es lo que más impacta en el resultado final.
- **Los `foto_hero` tienen que quedar oscuros.** Si te sale muy claro, agregá al prompt: `darker exposure, moody, low key`. Encima va un overlay negro al 40% con texto blanco: si la foto es clara, el texto no se lee.
- **Cero texto en las imágenes.** Si aparecen letras deformes, agregá: `no text, no letters, no watermarks`.
- **Renombrar al guardar**: `foto_splash.png`, `foto_hero.png`, `foto_galeria_1.png`, `foto_galeria_2.png`, `foto_hashtag.png` dentro de `assets/{eventoId}/`.
- Los eventos ya hechos (Catalina15, Isabella15, Zaira15) tienen los archivos con el nombre crudo de Gemini — conviene renombrarlos con este mismo criterio.
