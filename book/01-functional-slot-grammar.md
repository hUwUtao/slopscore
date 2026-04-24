# Functional Slot Grammar and Orchestration Decision Pipeline
### Research-Backed · Function-First · Score-Generation-Ready

> **Research basis:** Rimsky-Korsakov *Principles of Orchestration* · Adler *The Study of Orchestration* ·  
> Piston *Orchestration* · Belkin online orchestration materials · canonical score analysis  
> (Beethoven, Stravinsky, Ravel, Mahler, Holst, Williams).

---

## 1. Core Principle: Function Before Instrument

The most reliable orchestration model for score generation is **function first**:

1. Assign every sounding line a **slot** (lead, countermelody, bass, etc.)
2. Choose register bands that make that slot legible
3. Choose the instrument whose timbre, articulation, and blend behavior best serves the slot
4. Validate range, balance, doubling, articulation, and human playability
5. Emit notation

> **Do not choose an instrument before knowing what it must do in the texture.**

---

## 2. Slot Definitions

Every sounding part must be assigned exactly one **primary slot** per bar.

| Slot | Musical Job | Typical Writing Habits | Orchestrational Test |
|---|---|---|---|
| `lead` | Carries the idea the ear must remember | Clear contour, strongest identity, few same-register competitors | Can a first-time listener sing it back? |
| `countermelody` | Secondary line that enriches or answers the lead | Distinct rhythm or contour; different color/register | Does it support without stealing form? |
| `harmony` | Fills triadic or contrapuntal middle | Thirds/sixths, held tones, moving inner parts | Is the harmony audible without mud? |
| `bass` | Roots, pedals, propulsion, abyss | Longer notes or repetitive cells; wide spacing below | Is the fundamental clear? |
| `ostinato` | Repeated motor or grid | Simple, memorable rhythm; often timbrally stable | Does it remain perceptible when layered? |
| `pad` | Sustained atmosphere or harmonic field | Tremolo, harmonics, held winds/brass, muted strings | Does it blur or clarify the scene? |
| `color` | Specialized timbre not needed continuously | Celesta, harmonics, stopped horn, piccolo halo | Is the color distinct from the core plane? |
| `effect` | Non-neutral sound event | Rolls, trills, col legno, sul pont., flutter, cluster | Is it deliberate rather than accidental noise? |
| `punctuation` | Accents, caesurae, arrivals | Timpani, brass stabs, cymbal/tam-tam, sfz wind chord | Does it mark form without flattening dynamics? |

### 2.1 Part Reasoning — Required for Every Voice

Every `V:` voice in a score **must** carry metadata comments immediately before its first music line:

```abc
V:Lead name="Flute"
%slot=lead %role=main_melody %register=upper_mid %dyn=mp %art=legato
%reason=Carries the singable sky-blue motive in a clear register without same-register competition.
```

The `%reason=` line must explain **why the part exists** in the texture, mentioning at least one concrete musical function: motive, register, balance, cadence, color, rhythmic anchor, or playability.

> **A voice without an explicit purpose is invalid.** Every part must justify its existence.

---

## 3. Register, Voicing, Doubling, and Dynamics

### 3.1 Six High-Confidence Rules

1. **Natural register order** — In woodwind harmony, Piccolo–Flute–Oboe–Clarinet–Bassoon is the natural top-to-bottom order. Inverting it creates an "unnatural tone" (Rimsky-Korsakov). Only break this when estrangement is intended.

2. **Chord economy** — When voicing is sparse: remove the fifth first, keep the third (defines mode), keep the seventh (defines dominant function). Double the root first, then the fifth. Avoid gratuitous third doublings.

3. **Sustained vs. staccato balance** — Sustained lines must sit **at least 2 dynamic levels below** simultaneous staccato layers or they will swamp the texture.

4. **Extreme high winds/brass cannot play true pp** — Do not mark piccolo, high trumpet, high horn in an extreme high register at pp and expect it to be achievable.

5. **Same-color unison doublings** — Increase power but reduce expressivity and individuality. Use only when you want blend and weight.

6. **Strings + woodwinds blend more readily than strings + brass** — Horn + cello is the important partial exception.

### 3.2 Preferred Natural Doublings

| Upper voice | Natural partners |
|---|---|
| Violin I/II | Flute, Oboe, Clarinet, (Trumpet at unison for brightness) |
| Viola | Clarinet, English Horn, Bassoon |
| Cello | Clarinet, Bass Clarinet, Bassoon, Trombone, Horn |
| Double Bass | Bass Clarinet, Bassoon, Contrabassoon, Tuba |
| Trumpet | Trombone (at octave below) |
| Horn | Cello, Bassoon, Low strings — Horn is the principal "blend mediator" between brass and non-brass |

- Use **celesta, harmonics, piccolo, glockenspiel, stopped horn** as color tags, not permanent defaults.
- Double melodies only when you want emphasis, weight, or timbral blend.
- Use doubling as a **meaning decision**: reinforcement, softening, brightening, darkening, or blending.

---

## 4. Polyrhythm as a First-Class Orchestration Problem

Polyrhythm should be treated as a **routing** problem, not just a notation problem.

### 4.1 The Anchor Rule

| Layer | Role | Timbre requirement |
|---|---|---|
| **Anchor grid** | The metrically stable reference all other layers relate to | Most rhythmically stable timbre: snare, col legno strings, low strings, repeated lower winds |
| **Counter-grid** | Higher-energy competing subdivision | Contrasting timbre and non-adjacent register |
| **Color / accent layer** | Does not occupy the same register and attack profile as anchor | Light, specific, sparse |

> **Never place two competing rhythmic identities with similar articulation, similar onset density, and similar register in adjacent desks — unless the intent is climax or chaos.**  
> If you need chaos, the anchor must be retrievable after the event.

### 4.2 Canonical Polyrhythm Examples

| Score | Technique | Key lesson |
|---|---|---|
| Stravinsky *Rite of Spring* | Simultaneous triplets, septuplets, straight divisions; multiple ostinati superimposed | Success depends on **timbral separation, register spacing, and attack differentiation** |
| Holst *Mars* (Planets) | Insistent 5/4 col legno ostinato; 5/4 is deliberately unstable (would throw a marching body off step) | Ostinato **always** the audible anchor even as layers accumulate |

---

## 5. Orchestration Decision Pipeline

Make decisions in this exact order — do not jump ahead.

```
1.  Choose ensemble and style envelope
          ↓
2.  Assign slot grid (one primary slot per voice per bar)
          ↓
3.  Compose lead and bass lines
          ↓
4.  Compose harmony and countermelody
          ↓
5.  Choose register bands per slot
          ↓
6.  Choose instrument by slot fit
          ↓
7.  Validate written range and transposition
          ↓
8.  Validate balance and doubling
     ├── Avoid same-register masking of lead
     ├── Preserve one audible axis
     └── Reserve headroom for climaxes
          ↓
9.  Choose articulation family consistent with slot
          ↓
10. Apply dynamics
     └── Sustained layers ≥ 2 dynamic levels below simultaneous staccato
          ↓
11. Run human playability checks
     ├── Breath length (winds)
     ├── Bow/pluck endurance (strings)
     ├── Extreme-register softness feasibility
     └── Special-technique duration limits
          ↓
12. Emit notation (parts + score)
```

### Decision Timeline (Phase Model)

| Phase | Steps | Focus |
|---|---|---|
| **Sketch** | 1–2 | Define form and slot grid |
| **Pitch** | 3–4 | Compose lead, bass, harmony, countermelody |
| **Orchestration** | 5–8 | Register bands → instruments → doublings → headroom |
| **Human check** | 9–11 | Breath, bow, articulation, dynamics |
| **Output** | 12 | Parts, notation cleanup, `%` metadata |

---

## 6. Headroom Patterns from Canonical Scores

**General rule:** Begin with restricted color; save bright brass, upper winds, and percussion for later dramatic expansion.

| Score | Opening Strategy | Headroom Pattern |
|---|---|---|
| **Beethoven Symphony No. 5** | Famous 4-note cell in mid-bright strings + clarinet; flutes, horns, trumpets, timpani withheld | Reserve bright color → deploy at structural arrivals |
| **Stravinsky *Rite of Spring*** | Bassoon in extreme upper register as color-lead; successive winds enter in disjunct fragments | Vertical color accretion; estranged timbre for archaic/ritual feel |
| **Ravel *Boléro*** | Persistent rhythmic ostinato + static harmonic field; form driven entirely by reorchestration | Timbral rotation as the only engine of development |
| **Mahler Symphony No. 1** | Multi-octave sustained A in string harmonics; "sound of nature" before any melody | Pad before melody; emerge from atmosphere |
| **Holst *Mars*** | 5/4 col legno strings; percussive attack without losing pitch placement | Ostinato is the identity; brass added as punctuation/enlargement |
| **Williams *Star Wars* / *Harry Potter*** | Magic themes: celesta/high winds → Imperial themes: low brass/snare | Semantic color signatures: narrative tags map to instrument families |

---

## 7. Practical Composition Rules (LLM Defaults)

Unless intentionally overridden:

- Keep one clear **auditory axis** in every texture.
- Let **slot changes** happen more often than instrument changes when the phrase wants continuity.
- Let **instrument changes** happen more often than harmonic changes when the phrase wants coloristic development.
- **Prefer overlapping doublings** from the natural blend table (Section 3.2).
- Use Horn as the principal **blend mediator** between brass and non-brass groups.
- Use celesta, harmonics, piccolo, glockenspiel, stopped horn as **color tags** — not permanent defaults.
- For polyrhythm: **anchor on the most rhythmically stable timbre**; put conflicting subdivisions in contrasting timbres and non-adjacent registers.
- At climaxes, you may deliberately collapse timbral separation ("orchestra treated as percussion"), but that is the exception — return to clarity after.
- Mark **breaths for winds**, avoid impossible altissimo softness, avoid excessive unbroken col legno or extreme endurance writing.

---

*This file is referenced by `prompt.md` § 6 (Functional Slot Grammar) and § 7 (Orchestration Decision Pipeline).*
