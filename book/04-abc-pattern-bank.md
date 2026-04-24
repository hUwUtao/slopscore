# ABC Pattern Bank
### Slot-Aware Schematic Etudes for Orchestral Score Generation

> These are **original schematic etudes** — not quotations from copyrighted scores.
>
> **How to use:**
> 1. Find the instrument's ABC Family in `book/03-instrument-map.md`.
> 2. Select the pattern for the required slot.
> 3. Transpose/respell to the instrument's written notation.
> 4. Copy `%slot=`, `%role=`, `%register=`, `%dyn=`, `%art=`, `%reason=` tags.
> 5. `Q:` always uses explicit `<beat-unit>=<bpm>` form (see `prompt.md` §12.1).

---

## Family Map

| ABC Family | Instruments |
|---|---|
| STR-H | Violin I/II; Flute/Piccolo octave variants |
| STR-M | Viola; mellow middle pads/inner voices |
| STR-L | Cello; lyric bass-support |
| WW-H | Flute, Piccolo |
| WW-R | Oboe, English Horn |
| WW-C | Clarinet family |
| WW-B | Bassoon family |
| BR-H | Trumpet |
| BR-M | Horn in F |
| BR-L | Trombone (tenor and bass) |
| BASS | Double Bass, Bass Clarinet, Contrabassoon, Tuba |
| HARP | Harp |
| KP | Celesta, Glockenspiel, Xylophone, Piano (color) |
| TIMP | Timpani |
| PERC | Snare, Bass Drum, Cymbals, Tam-tam |

---

## Group 1: High Strings / High Winds (STR-H, WW-H)

### Pattern 1 — Melody Slot
```abc
X:1
T:STR-H/WW-H melody
M:4/4
L:1/8
Q:1/4=88
K:G
V:1 clef=treble name="Lead"
%slot=lead %role=melody %dyn=mf %art=leg %register=high %family=string_or_high_ww
%reason=Carries singable stepwise motive in bright upper register; no same-register competition.
d2 g a b | d'2 c' b a | g4 a2 b2 | c'2 b2 ||
```

### Pattern 2 — Harmony Inner Slot
```abc
X:2
T:STR-H/WW-H harmony-inner
M:4/4
L:1/8
Q:1/4=88
K:G
V:1 clef=treble name="Inner"
%slot=harmony %role=inner %dyn=mp %art=leg %register=mid_high
%reason=Fills third/sixth below lead; lower dynamic avoids masking.
b2 d' e' d' | b2 a g f# | g4 f#2 e2 | d2 g2 ||
```

### Pattern 3 — Ostinato Slot (5/4)
```abc
X:3
T:STR-H/WW-H ostinato
M:5/4
L:1/8
Q:1/4=132
K:Dm
V:1 clef=treble name="Motor"
%slot=ostinato %role=rhythm %dyn=mp %art=stac %register=mid %cycle=1bar
%reason=Anchor rhythmic grid; staccato prevents blurring of lead.
a a a a a a a a a a | a a a a a a a a a a ||
```

### Pattern 4 — Color Slot
```abc
X:4
T:STR-H/WW-H color
M:3/4
L:1/8
Q:1/4=60
K:C
V:1 clef=treble name="Color"
%slot=color %role=texture %dyn=pp %art=tr_or_harmonic %register=high
%reason=Shimmering halo above melody at cadences; pp keeps it atmosphere only.
g'2 (a'/b/) g'2 | e'2 z2 g'2 | c''4 z2 ||
```

### Pattern 5 — Ensemble Excerpt (Lead + Inner + Bass)
```abc
X:5
T:Short ensemble
M:4/4
L:1/8
Q:1/4=96
K:Gm
V:Lead clef=treble name="Lead"
V:Inner clef=treble name="Inner"
V:Bass clef=bass name="Bass"
[V:Lead]
%slot=lead %role=melody %dyn=mf %art=leg %register=high
%reason=Primary melodic identity; upper register; no competition.
d'2 g' f' e' | d'4 c'2 b2 ||
[V:Inner]
%slot=harmony %role=inner %dyn=mp %art=leg %register=mid
%reason=Thirds/sixths below lead; lower dynamic avoids masking.
b2 d' c' b | a4 g2 f2 ||
[V:Bass]
%slot=bass %role=root_motion %dyn=mf %art=marc %register=low
%reason=Defines harmonic motion; wide intervals separate from inner voices.
G,2 D G, D | C,4 D,2 E,2 ||
```

---

## Group 2: Reeds and Middle-Register Carriers (WW-R, WW-C, WW-B)

### Pattern 6 — Countermelody Slot
```abc
X:6
T:WW-R/WW-C countermelody
M:4/4
L:1/8
Q:1/4=76
K:F
V:1 clef=treble name="Counter"
%slot=countermelody %role=answer %dyn=mp %art=leg_marc %register=mid
%reason=Answers lead with different contour and reed color; avoids same-register competition.
a2 c' d' c' | a2 g f e | f4 g2 a2 ||
```

### Pattern 7 — Inner Motion Slot
```abc
X:7
T:WW-R/WW-C inner-motion
M:4/4
L:1/8
Q:1/4=76
K:F
V:1 clef=treble name="Inner"
%slot=harmony %role=inner_voice %dyn=mp %art=tenuto %register=mid
%reason=Harmonic fill in middle register; tenuto keeps it tonal without drawing attention.
c2 c d e | f2 e d c | a,4 b,2 c2 ||
```

### Pattern 8 — Color-Lead Slot (Stravinsky-style high bassoon)
```abc
X:8
T:WW-B color-lead
M:3/4
L:1/8
Q:1/4=56
K:A
V:1 clef=tenor name="BassoonLike"
%slot=lead %role=color_melody %dyn=p %art=espressivo %register=high_unusual
%reason=Bassoon in extreme high register for archaic/estranged lead timbre (Stravinsky archetype).
c'3 b/ a2 | e'3 d'/ c'2 | b3 a/ g2 ||
```

---

## Group 3: Low Strings, Bass Winds, Low Brass (STR-L, WW-B, BR-L, BASS)

### Pattern 9 — Low Melody Slot
```abc
X:9
T:BASS melody
M:4/4
L:1/8
Q:1/4=72
K:Dm
V:1 clef=bass name="LowLead"
%slot=lead %role=melody %dyn=mf %art=leg_marc %register=mid_low
%reason=Intense cello-register melodic line; no high-register competition.
d2 f a g | f2 e d c | d4 a,2 c2 ||
```

### Pattern 10 — Pedal Bass Slot
```abc
X:10
T:BASS pedal
M:4/4
L:1/8
Q:1/4=72
K:Dm
V:1 clef=bass name="Pedal"
%slot=bass %role=pedal %dyn=mp %art=sustain %register=low
%reason=Sustained tonic pedal; low dynamic avoids competing with inner voices.
D,4 z4 | D,4 z4 | A,,4 z4 | D,4 z4 ||
```

### Pattern 11 — March-Ostinato Slot (Low Brass)
```abc
X:11
T:BR-L march-ostinato
M:4/4
L:1/8
Q:1/4=108
K:Gm
V:1 clef=bass name="LowBrass"
%slot=ostinato %role=rhythm %dyn=f %art=marc %register=low
%reason=Rhythmic motor in low brass; marcato gives authority without entering mid-register.
G,2 G,2 G,2 G,2 | D4 D4 | B,4 B,4 | G,4 z4 ||
```

---

## Group 4: Harp, Celesta, Timpani, Percussion (HARP, KP, TIMP, PERC)

### Pattern 12 — Harp Pad-Harmony
```abc
X:12
T:HARP pad-harmony
M:3/4
L:1/8
Q:1/4=72
K:C
V:1 clef=treble name="Harp"
%slot=pad %role=arpeggiated_harmony %dyn=pp %art=rolled %register=wide
%reason=Atmospheric harmonic shimmer across wide register; pp blends without muddying.
[ceg] z [egc'] z [gc'e'] z | [ac'e'] z [gbd'] z [c'e'g'] z ||
```

### Pattern 13 — Celesta Magic-Color Slot
```abc
X:13
T:KP magic-color
M:3/8
L:1/16
Q:3/8=58
K:Em
V:1 clef=treble name="Celesta"
%slot=color %role=lead_or_halo %dyn=pp %art=detached_legato %register=high
%reason=Magical icy lead color; celesta immediately identifiable; non-competitive timbre.
B2 e2 g2 | f2 d2 B2 | e2 a2 g2 ||
```

### Pattern 14 — Timpani Punctuation-Bass
```abc
X:14
T:TIMP punctuation-bass
M:4/4
L:1/8
Q:1/4=96
K:C
V:1 clef=bass name="Timpani"
%slot=punctuation %role=bass_root_fifth %dyn=mf %art=acc_roll %register=low
%reason=Articulates harmonic roots/fifths at cadential points; provides low-end weight.
C,2 G,2 z4 | C,2 G,2 z4 | G,2 z2 C,4 | C,4 z4 ||
```

### Pattern 15 — Snare Motor-Grid (Boléro / Mars archetype)
```abc
X:15
T:PERC motor-grid
M:5/4
L:1/8
Q:1/4=132
K:none
V:1 perc name="Snare"
%slot=ostinato %role=grid %dyn=mp %art=sticking_even %register=na
%reason=Anchor rhythmic grid; unpitched keeps it from competing harmonically.
z2 C C C C C C C C C | z2 C C C C C C C C C ||
```

---

## Transposition Quick Reference

| Instrument | Written pitch vs. sounding |
|---|---|
| Clarinet in B♭ | Written = sounding + M2 (write a step higher) |
| Clarinet in A | Written = sounding + m3 |
| English Horn | Written = sounding + P5 |
| Horn in F | Written = sounding + P5 |
| Trumpet in B♭ | Written = sounding + M2 |
| Bass Clarinet in B♭ (treble) | Written = sounding + M9 |
| Piccolo | Written = sounding - 8va (sounds higher) |
| Glockenspiel | Written = sounding - 2 oct (sounds higher) |
| Celesta | Written = sounding - 8va (sounds higher) |
| Xylophone | Written = sounding - 8va (sounds higher) |
| Contrabassoon | Written = sounding + 8va (sounds lower) |
| Double Bass | Written = sounding + 8va (sounds lower) |

## Slot Conflict Table

| Conflict | Problem | Fix |
|---|---|---|
| Two `lead` in same register | Masking | Lower one to `countermelody` or shift register |
| `pad` and `ostinato` same dynamic | Ostinato disappears | Drop `pad` by 2 dynamic levels |
| `bass` and `harmony` both below C3 | Muddy fundamental | Space harmony above C3 |
| Two `ostinato` same attack profile | Rhythmic noise | Differentiate timbre, register, or articulation |

---

*This file is referenced by `prompt.md` §10. Cross-reference `book/03-instrument-map.md` for range validation.*
