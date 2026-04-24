# Vocal Support — Lyrics, Ranges, and MusicXML Export
### Write lyrics · Assign vocal parts · Pack into MusicXML

> Vocals are treated as a first-class slot in this system.
> The pipeline parses ABC `w:` lyrics and embeds them as `<lyric>` elements in MusicXML,
> which MuseScore renders with syllable hyphens, melisma lines, and breath marks.

---

## 1. Vocal Part Slot Grammar

Assign vocal voices the same slot logic as any other instrument. The most common vocal slots:

| Slot | Vocal Function | Example |
|---|---|---|
| `lead` | Primary melodic vocal line with lyrics | Lead singer, aria |
| `countermelody` | Backing vocal answering the lead | Harmonized response |
| `harmony` | Inner choral fill (alto, tenor in SATB) | Choir inner voices |
| `bass` | Low foundation vocal line | Bass part of SATB |
| `pad` | Sustained vocal texture (wordless, "ah", "mm") | Choir sustains |
| `ostinato` | Repeated rhythmic vocal figure | Vocalise groove |

---

## 2. Vocal Range Reference

Conservative practical ranges for score generation. Exceeding these without stylistic intent creates unsingable parts.

| Voice Type | Comfortable Range (written = sounding) | ABC Name Tag | Tessatura Center |
|---|---|---|---|
| **Soprano** | C4–A5 (up to C6 with training) | `name="Soprano"` | E4–E5 |
| **Mezzo-soprano** | A3–F5 | `name="Mezzo"` | C4–C5 |
| **Alto / Contralto** | F3–D5 | `name="Alto"` | A3–A4 |
| **Tenor** | B2–G4 (sounds as written in treble 8vb) | `name="Tenor"` | D3–D4 |
| **Baritone** | G2–E4 | `name="Baritone"` | A2–A3 |
| **Bass** | E2–C4 | `name="Bass"` | C3–C4 |

> **Tessatura** = the region where the voice sits most of the time. Keep most notes there;
> use the extremes for expression, not as the norm.

### Clef Conventions

| Voice | ABC clef tag |
|---|---|
| Soprano, Mezzo, Alto | `clef=treble` |
| Tenor | `clef=treble` (notates an octave higher than sounding; pipeline uses treble) |
| Baritone | `clef=treble` (or `clef=bass` if preferred) |
| Bass | `clef=bass` |

---

## 3. ABC Notation for Vocals

### 3.1 Declaring a Vocal Voice

```abc
V:Vox clef=treble name="Soprano"
%slot=lead %role=vocal_melody %register=mid_high %dyn=mf %art=legato
%reason=Carries the lyric melody in the soprano's expressive tessatura.
```

### 3.2 Writing Lyrics — The `w:` Field

Place a `w:` line **immediately after** the music body line it belongs to.
Syllables map sequentially to notes (skipping rests automatically in playback,
but the pipeline maps them to all notes including rests in the cursor — keep this in mind).

```abc
[V:Vox] c2 d2 e4 | d2 c2 B4 | c8 |
w: Hel- lo, world! Good- bye.  here.
```

#### `w:` Syllable Syntax

| Token | Meaning |
|---|---|
| `word` | Single-syllable word — maps to one note |
| `syl-` | Syllable continues (hyphen in score display) — map next part to next note |
| `_` | **Hold / melisma** — the previous syllable extends over this note (no new text) |
| `*` | **Skip** — this note has no lyric (e.g. pickup, ornament) |
| `\|` | Bar alignment marker — ignored by parser, helpful for readability |

#### Example with continuation and hold

```abc
[V:Vox] c4 d4 | e2 e2 f4 | g8 |
w: Beau- ti- ful | morn- ing _ |
```

Renders as:
- c → "Beau-"
- d → "ti-"
- e+e → "morn-" / "ing"  
- f → *(skipped — already used `_` to hold)*
- g → *(hold from "ing")*

### 3.3 Multi-voice ABC Example (Soprano + Alto + Bass)

```abc
X:1
T:Simple Hymn
M:4/4
L:1/4
Q:1/4=72
K:G
V:S clef=treble name="Soprano"
V:A clef=treble name="Alto"
V:B clef=bass name="Bass"

[V:S]
%slot=lead %role=vocal_melody %register=high %dyn=mf %art=legato
%reason=Carries primary lyric melody in soprano tessatura.
d2 e d | c4 | B2 c d | e4 |
w: All my days I'll _ | sing your _ | praise for- ev- er- more |

[V:A]
%slot=harmony %role=inner_voice %register=mid %dyn=mp %art=legato
%reason=Inner choral harmony; thirds below soprano avoid register conflict.
B2 c B | A4 | G2 A B | c4 |
w: All my days I'll _ | sing your _ | praise for- ev- er- more |

[V:B]
%slot=bass %role=root_motion %register=low %dyn=mf %art=marc
%reason=Bass roots define harmonic progression; lower register grounds the texture.
G,2 G,2 | D,4 | G,2 G,2 | C,4 |
w: All _ _ _ | _ _ | _ _ _ _ | _ |
```

---

## 4. Lyric Writing Guidelines

### 4.1 Prosody — Stress Alignment

> **The most important rule:** stressed syllables must land on strong beats or
> strong metric positions. Misaligned stress makes lyrics feel wrong even when
> the melody is good.

| Principle | Example |
|---|---|
| Word stress matches beat stress | "BEA-yoo-tiful" → stressed "BEA" on beat 1 |
| Short unstressed words on weak beats | "the", "a", "and", "of" on upbeats or inner beats |
| Sentence peak on melodic apex | The most important word → highest or longest note |
| Punctuation at phrase endings | Full stop / question → cadential bar |

### 4.2 Syllabification Rules

The `w:` field syllabifies words using hyphens. Follow standard English (or target language) syllabification:

| Rule | Example |
|---|---|
| Split between consonants | `bet-ter`, `win-ter` |
| Single consonant between vowels → goes with following vowel | `be-lieve`, `a-lone` |
| Compound words → split at compound boundary | `sun-shine`, `heart-break` |
| Never split a diphthong | "moon" stays as one syllable: `moon` |
| One-syllable words → never split | `the`, `and`, `love` |

### 4.3 Vowel / Consonant Cautions

- **Long vowels on long notes**: sustained notes need open vowels (ah, oh, ee) not closed consonants (m, n).
- **Final consonants on short notes**: closing consonants (t, k, p) work best on short, detached notes.
- **Plosives on attack**: b, d, g, p, t, k work at the start of a note; avoid placing them mid-sustain.
- **Open vowels for high notes**: forcing "ee" or "ih" on high soprano notes creates tension — prefer "ah" or "oh" in extreme high passages.

### 4.4 Melisma (Multiple Notes Per Syllable)

When one syllable spans multiple notes, use `_` in `w:` for each additional note:

```abc
[V:Vox] c d e f | g4 |
w: Glo- _ _ _ | ri-  |
```

Renders: c=Glo, d=_(hold), e=_(hold), f=_(hold), g=ri

MuseScore draws a melisma line under the sustained syllable automatically.

---

## 5. Human Vocal Considerations

### 5.1 Breath Marks

Singers **must breathe**. Mark breath points with a comma under the score (in ABC, add a `%breath` comment and note it in the `%reason=` tag):

```abc
[V:Vox] c2 d2 e4 | f2 e2 d4 |  % breath after bar 1
w: sing- ing  hap- pi- | ly  to-  day. |
```

Practical breath rules:
- Allow at least one rest or a long note (quarter note ≥) at natural phrase boundaries.
- Avoid phrases longer than 8 beats at moderate tempo without a breath gap.
- Rests are preferred breath positions; fermatas on final long notes also give breathing room.
- Never write a vocal line that is entirely quarter notes for 16+ bars straight.

### 5.2 Tessatura Fatigue

Sustained singing in the **extremes** of the comfortable range is tiring:
- Soprano above A5 for more than 2–3 bars → fatiguing
- Bass below E2 for more than a bar → strained and inaudible
- Tenor above G4 (passaggio) for entire sections → breaks or strain

**Solution:** return to tessatura center after excursions to extremes.

### 5.3 Interval Considerations

- Leaps larger than an octave are difficult for untrained singers.
- Diminished and augmented intervals are harder to pitch accurately without accompaniment.
- Prefer stepwise motion and simple leaps (thirds, fourths, fifths) for accessibility.
- If a large interval is needed: approach it from the direction of the leap (ascending leap → ascending approach step) or prepare with a common tone in another voice.

---

## 6. Pipeline Integration — `w:` → MusicXML

The pipeline's `_score_from_simple_abc` function parses `w:` lyrics and attaches them to notes via music21's `note.addLyric()`. The resulting MusicXML contains `<lyric>` elements that render in MuseScore as:

- Syllables positioned below each note
- Hyphens between continuation syllables (e.g. "beau-ti-ful")
- Melisma underscores for held syllables
- Proper lyric numbering for multi-verse support

### Workflow

```
1. Write ABC with [V:VoiceName] music lines
          ↓
2. Add w: lyric line immediately after each [V:...] music line
          ↓
3. Run pipeline: cat <<'EOF' | .venv/bin/python3 pipeline.py "slug"
          ↓
4. Pipeline writes ABC → builds MusicXML with <lyric> elements
          ↓
5. Open MusicXML in MuseScore 4 → lyrics render with proper syllabification
          ↓
6. Export to PDF / MP3 from MuseScore (see prompt.md §16)
```

### Voice Instrument Names (for pipeline auto-detection)

The pipeline maps `name=` values to music21 voice instruments:

| `name=` contains | music21 instrument | MusicXML part name |
|---|---|---|
| `Soprano` | `instrument.Soprano` | Soprano |
| `Mezzo` | `instrument.MezzoSoprano` | Mezzo-Soprano |
| `Alto` / `Contralto` | `instrument.Alto` | Alto |
| `Tenor` | `instrument.Tenor` | Tenor |
| `Baritone` | `instrument.Baritone` | Baritone |
| `Bass` (Voice / Vocal) | `instrument.Bass` | Bass |
| `Voice` / `Vocal` / `Vox` / `Singer` (unspecified) | `instrument.Soprano` | Voice |

---

## 7. Vocal Slot ABC Pattern

```abc
X:1
T:Vocal Pattern — lead slot
M:4/4
L:1/4
Q:1/4=80
K:G
V:Vox clef=treble name="Soprano"
%slot=lead %role=vocal_melody %register=mid_high %dyn=mf %art=legato
%reason=Primary lyric melody in soprano tessatura; stepwise motion for singability.
[V:Vox] d2 e d | c4 | B c d e | d4 |
w: Sing- ing in the | light, | reach- ing for the | sky. |
```

---

*This file is referenced by `prompt.md` §17 (Vocal Support). Cross-reference `book/04-abc-pattern-bank.md` for instrumental patterns and `book/00-music-theory-guardrails.md` for prosody alignment with phrase structure.*
