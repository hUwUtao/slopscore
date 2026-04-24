# Canonical Score Patterns
### Orchestrational Archetypes Extracted for LLM Score Generation

> These analyses synthesize orchestration treatise evidence (Rimsky-Korsakov, Adler, Piston, Belkin)
> with pedagogical and public-domain score examination. Each section ends with an
> **extracted pattern** — a reusable rule for a generation engine.

---

## 1. Beethoven — Symphony No. 5 (Op. 67)
### Archetype: Economy with Headroom

**What the score does:**  
The famous four-note cell is **not** given to full bright tutti at the opening. In the score, flutes, oboes, horns, trumpets, and timpani are withheld at the very first attack — strings and clarinets carry the identity. The texture then thins to piano with long bassoon sustain against moving string material.

**Why it works:**  
The rhythmic cell is hyper-legible because it occupies a "mid-bright, speech-like" register without piercing competition. Brighter forces are held back for later structural arrivals, where they create genuine impact because they have not yet been heard.

**Extracted Pattern:**

> If the lead is a compact motivic cell, place it in a **mid-bright register** (strings + reed or clarinet), and withhold bright brass, piccolo, and percussion.  
> Use bassoon or lower strings for sustained harmonic gravity while the motive circulates.  
> This is especially effective when the piece wants **inevitability rather than spectacle** at the opening.

**Generation rule:** `if opening_cell = compact_motive → slot:[strings+cl for cell] [bn for harmonic gravity] [bright brass = reserved]`

---

## 2. Stravinsky — The Rite of Spring (1913)
### Archetype: Color Accretion and Reassigned Role

**What the score does:**  
The opening bassoon is written in an **extreme upper register**, so its identity is almost estranged from the instrument's usual character. Additional winds enter in disjunct, layered, folk-like fragments — vertical color accretion rather than ordinary accompaniment. Later, multiple ostinati and countermelodies are superimposed; simultaneous triplets, septuplets, and straight divisions coexist. The "Augurs of Spring" chord is treated as a rhythmic percussion event.

**Why it works:**  
Special timbre is created by **reassigning a familiar instrument to a non-default register**. The bassoon in its extreme high register puzzles the ear into attention before any "normal" musical discourse begins. Polyrhythms succeed because each layer occupies a distinct timbre, register, and articulation — the anchor remains perceptible even under accumulation.

**Extracted Pattern:**

> If the lead must sound archaic, uncanny, or ritualized, use **a normally supportive instrument in an exposed extreme register**, then layer short answer-fragments in timbrally adjacent instruments.  
> For polyrhythm: keep one line as anchor; let the rest operate as local pressure systems around it, never competing in the same register and articulation as the anchor.

**Generation rule:** `if mood = archaic|uncanny → lead instrument: normally-bass-role, register: extreme_high; layers: short_fragments in adjacent timbres`

---

## 3. Ravel — Boléro
### Archetype: Timbral Rotation as Form

**What the score does:**  
Boléro is orchestral function stripped to laboratory purity. A persistent snare-drum ostinato and a nearly static harmonic field repeat throughout. The only engine of development is **reorchestration** — each melodic repeat is stated by a new solo color or blend. Later, the ostinato itself absorbs more harmonic function as strings join in pizzicato arpeggiation and the texture thickens toward tutti.

**Why it works:**  
When harmony is intentionally static, slot movement must happen in **timbre, register, and density** alone. The listener experiences "progression" entirely through color change, not harmonic change.

**Extracted Pattern:**

> If the harmony is intentionally static, hold bass and ostinato nearly constant while **rotating the lead through sharply differentiated solo colors**.  
> Gradually convert rhythmic layers into harmonic layers, then into tutti reinforcement.  
> Density is itself a form parameter — track it as carefully as harmony.

**Generation rule:** `if harmony = static → form_engine: timbral_rotation; lead: solo_color_sequence; density: cumulative_crescendo`

---

## 4. Mahler — Symphony No. 1 ("Titan")
### Archetype: Pad Before Melody

**What the score does:**  
Mahler's First begins not with theme but with **environment**. Multiple octaves of the note A are spread through strings, many in harmonics, marked "like a sound of nature." Distant cuckoo-like calls appear as punctual color. The lead melody surfaces gradually from the atmospheric pad, not the reverse.

**Why it works:**  
The traditional expectation is theme first, accompaniment second. Mahler reverses this: the **texture-pad** is the first slot, and the lead is withheld until the ear has accepted the timbral environment as home ground. The melody, when it finally appears, feels like emergence rather than announcement.

**Extracted Pattern:**

> A large-form opening can begin with **pad before melody**.  
> Create a long-sustain field with sparse color-punctuation; delay lead commitment until the ear has accepted the environment.  
> Harmonics, remote woodwind calls, and long pedals are especially useful when the piece wants "distance" or mystery rather than immediate rhetoric.

**Generation rule:** `if opening_intent = distance|mystery → first_slot: pad; lead_entry: delayed; textures: harmonics+pedals+color_punctuation`

---

## 5. Holst — The Planets, "Mars" (Op. 32)
### Archetype: Ostinato as Identity

**What the score does:**  
"Mars" opens with an insistent 5/4 col legno string ostinato. The **wood-on-string attack** preserves registral placement while behaving percussively — sitting between pitch and noise. The 5/4 grid is deliberately unstable (it would throw a marching body off step). Brass fanfares and percussion later enter as punctuation and enlargement, never replacing the original grid.

**Why it works:**  
The rhythmic grid is the identity of the scene. Its success depends on giving it a timbre that **reads as both pitched and percussive** — a register between rhythm section and string section. Later additions (brass, percussion) are punctuation to the grid, not substitutes for it.

**Extracted Pattern:**

> If the rhythmic grid is the identity of the scene, give it a **timbre that sits between pitch and percussion** (col legno strings are ideal — they preserve register while behaving percussively).  
> Then add brass and percussion as punctuation and enlargement, not as replacements.  
> The grid must remain the audible anchor even at full orchestral force.

**Generation rule:** `if rhythmic_grid = identity → anchor_timbre: col_legno or low_strings; brass/perc: punctuation_role only; anchor: always_audible`

---

## 6. Williams — Star Wars (1977) / Harry Potter (2001)
### Archetype: Semantic Color Signatures

**What the score does:**  
Williams uses two contrasting archetypes:  
- **"Magic" themes** (Hedwig's Theme): introduced on celesta and passed through high winds and upper strings. Delicate, box-like, icy color.  
- **"Imperial/monumental" themes** (Imperial March): low brass, strong snare/march articulation, firm registral grounding, heavy sforzando articulation.

The bass trombone line in the Star Wars suite is not merely bass support but **themed, rhythmic, and highly articulated** — its marcato/sforzando behavior reads as authority rather than plumbing.

**Why it works:**  
Each semantic category ("magic", "empire", "hero", "villain") maps to a **specific instrumental color signature**. The audience learns to associate timbre with meaning rather than just mood. This is color used as **narrative grammar**.

**Extracted Pattern:**

> Separate **semantic theme** from **support grid** cleanly.  
> "Magic" themes → celesta, high winds, upper strings.  
> "Imperial/monumental" themes → low brass, strong snare profile, firm registral grounding.  
> In a generation system, attach reusable color rules to **narrative tags** and apply them consistently across the score.

**Generation rule:**

| Narrative tag | Instrument family | Articulation | Register |
|---|---|---|---|
| `magic` | Celesta, high winds, upper strings | detached, pp–mp | high |
| `imperial` | Low brass, snare, tuba | marcato, sfz, f–ff | low |
| `heroic` | Trumpet, upper strings, full winds | marc, bright | high-mid |
| `ominous` | Bass strings, bass clarinet, low brass | legato, dark | low |
| `pastoral` | Oboe, flute, horn | legato, mp | mid-high |

---

*This file is referenced by `prompt.md` § 7 (Orchestration Decision Pipeline — Headroom Patterns).*
