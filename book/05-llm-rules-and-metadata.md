# LLM Rule System and Voice Metadata Schema
### Machine-Checkable Orchestration Rules for Score Generation

> This file defines the per-voice metadata schema and validation rules that a
> deterministic orchestration engine should enforce before emitting any notation.
> It is the normative specification for `%slot=`, `%role=`, `%register=`, and
> related comment tags in ABC output.

---

## 1. Decision Ordering

A deterministic orchestration engine must make decisions in this order — do not skip steps:

1. Choose ensemble and style envelope
2. Generate lead and bass lines
3. Assign **one primary slot per bar** to each voice
4. Validate written range and transposition
5. Choose doublings only where overlap is natural (see `book/01-functional-slot-grammar.md` §3.2)
6. Place sustained layers below percussive layers dynamically
7. Choose articulation family consistent with slot
8. Run human playability checks:
   - Breathing gaps for winds
   - Bow-change rate for strings
   - Pedal-change feasibility for harp
   - Page-turn and mute-change practicality
   - Duration limits for col legno, flutter tongue, extreme endurance writing

---

## 2. Per-Voice Metadata Schema

Every generated voice must carry a YAML-compatible metadata block expressed as
`%` comments in ABC, immediately before its first music line.

```yaml
voice_id:              Vln1_A
instrument:            violin_1
written_range:         G3-A7
sounding_transposition: unison
slot:                  lead
secondary_slot:        none
register_band:         high           # low | mid_low | mid | mid_high | high | extreme_high
dynamic:               mf             # ppp pp p mp mf f ff fff
dynamic_ceiling:       ff
articulation:          legato         # legato | staccato | marcato | tenuto | espressivo | ...
attack_class:          sustained_clear # sustained_clear | sustained_soft | staccato | percussive
sustain_class:         sustained       # sustained | short | roll | tremolo
doubling_partner:      flute_1         # or "none"
blend_family:          string+woodwind
rhythm_group:          anchor          # anchor | counter | color
polyrhythm_group:      A               # A = anchor, B = counter, C = color
vibrato:               normal          # none | normal | wide | flutter
mute:                  false
human_constraint:
  bow_change_rate:     moderate        # slow | moderate | fast | extreme
  breath_needed:       false
  page_turn_sensitive: false
```

### 2.1 ABC Comment Form

Minimal required inline form (one `%` line per attribute group):

```abc
V:Vln1 clef=treble name="Violin 1"
%slot=lead %role=melody %register=high %dyn=mf %art=legato
%doubling=flute_1 %blend=string+woodwind %rhythm_group=anchor %polyrhythm_group=A
%reason=Carries the primary melodic identity in its most identifiable register; no same-register competition.
```

The `%reason=` tag is **mandatory**. It must mention at least one of:
motive · register · balance · cadence · color · rhythmic anchor · playability

---

## 3. Machine-Checkable Validation Rules

These rules must be validated **per bar** before notation is emitted.

```yaml
rules:

  # Lead isolation
  - if slot == lead
    then avoid_same_register_competitor: true
    # No other voice at the same register_band unless slot == countermelody
    # and it has a distinct contour or articulation.

  # Sustained vs. staccato balance
  - if attack_class == sustained
       and concurrent_staccato == true
    then lower_dynamic_by: 2_levels
    # A pp sustained layer under an mf staccato layer needs to drop to ppp.

  # Extreme high register soft dynamics
  - if instrument in [piccolo, trumpet, horn, trombone]
       and register_band == extreme_high
       and dynamic in [pp, ppp]
    then reject: true
    reason: "These instruments cannot reliably play pianissimo in the extreme high register."

  # Bass spacing
  - if slot == bass
    then spacing_below_C3: wide
    # Avoid close intervals (seconds, thirds) in the bass below C3 — creates mud.

  # Doubling register overlap
  - if doubling_partner != none
    then require_overlap_register: true
    # Doubling partners must share at least some register overlap to blend.

  # Polyrhythm anchor requirement
  - if polyrhythm_group count > 2
    then require_anchor_group: true
    # At least one group must be designated anchor; others must differ
    # in at least two of: timbre, register_band, attack_class.

  # Harp pedal change rate
  - if instrument == harp
    then pedal_change_rate: bounded
    # Harp cannot change all 7 pedal positions simultaneously; allow one to
    # two changes per measure at moderate tempo.

  # Col legno duration
  - if instrument in [violin, viola, cello, double_bass]
       and articulation == col_legno
    then duration_limit: bounded
    # Extended col legno is fatiguing; limit to sections, not long movements.

  # Wind breath marking
  - if instrument in [flute, oboe, clarinet, bassoon, horn, trumpet, trombone, tuba,
                      piccolo, english_horn, bass_clarinet, contrabassoon]
       and phrase_length > breath_threshold
    then mark_breath: true
    # Default breath_threshold: 8 beats at quarter-note = 120 BPM.
    # Faster tempo or instrument → shorter threshold.

  # Extreme altissimo
  - if register_band == extreme_high
       and dynamic in [pp, ppp]
       and instrument in [flute, piccolo, oboe, trumpet, horn]
    then warn: "Extreme high register pp is unreliable; lower register or raise dynamic."

  # Vocal Prosody
  - if instrument in [soprano, mezzo, alto, tenor, baritone, bass_vocal]
    then require_lyric_stress_alignment: true
    # Primary stressed syllables must land on Beats 1 or 3 in 4/4; Beat 1 in 3/4.

  # Vocal Breath
  - if instrument in [soprano, mezzo, alto, tenor, baritone, bass_vocal]
       and phrase_length > vocal_breath_threshold
    then require_breath_gap: true
    # vocal_breath_threshold: 8 beats at QM=120.

  # Vocal Tessatura
  - if instrument in [soprano, tenor]
       and register_band == high
       and duration > 4_bars
    then warn: "Extended high tessatura is fatiguing; return to mid register."
```

---

## 4. Practical Composition Defaults (LLM)

Unless the brief explicitly overrides them:

| Rule | Default behavior |
|---|---|
| **Auditory axis** | Keep one clear auditory axis per texture; never let all voices compete for attention simultaneously |
| **Slot vs. instrument change rate** | Slot changes may happen more often than instrument changes when phrase wants continuity |
| **Instrument vs. harmonic change rate** | Instrument changes may happen more often than harmonic changes when phrase wants coloristic development |
| **Doubling** | Use `book/01-functional-slot-grammar.md` §3.2 preferred doublings; Horn is the principal blend mediator |
| **Color instruments** | Celesta, harmonics, piccolo, glockenspiel, stopped horn = color tags, not permanent defaults |
| **Polyrhythm anchor** | Put anchor on most rhythmically stable timbre: snare, col legno strings, low strings, repeated lower winds |
| **Climax separation** | May deliberately collapse timbral separation at climax ("orchestra as percussion"); restore clarity after |
| **Playability** | Mark breaths for winds; avoid impossible altissimo softness; avoid excessive unbroken col legno |

---

## 5. Validation Summary Checklist

Before emitting any score, verify:

- [ ] Every voice has `%slot=` and `%reason=` tags with concrete musical justification
- [ ] No two `lead` voices occupy the same `register_band` without a stated reason
- [ ] Sustained layers are dynamically lower than simultaneous staccato layers
- [ ] No extreme-high-register instrument is marked `pp` or `ppp`
- [ ] Bass voices use wide spacing below C3
- [ ] Doubling partners share register overlap
- [ ] Polyrhythm has a designated `polyrhythm_group: A` (anchor)
- [ ] Harp pedal changes are physically feasible at the written tempo
- [ ] Breath marks are inserted for wind phrases exceeding the breath threshold
- [ ] Col legno, flutter tongue, and other extended techniques are bounded in duration
- [ ] Vocal stressed syllables land on strong beats (Prosody Check)
- [ ] Vocal phrases have breathing gaps (Rest or long note) every 8 beats
- [ ] Vocal tessatura returns to the central range after excursions to high/low extremes

---

*This file is referenced by `prompt.md` §11 (Voice Metadata Schema) and §13 (Quality Checklist).*
