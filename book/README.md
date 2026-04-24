# Book — Music Composition Knowledge Base
### Decomposed instruction files for the LLM Music Composition System

This directory contains the detailed reference material that supports `prompt.md`.
Each file is self-contained and cross-referenced. Read any file in isolation or as
a linked set.

---

## Files

| File | What It Contains | Referenced By |
|---|---|---|
| `00-music-theory-guardrails.md` | **Grammar of intentional composition** — phrase/form archetypes, melody motive rules, harmonic function, all cadence types, voice leading order, non-chord tones (passing, neighbor, suspension, etc.), rhythm, meter notes, mode reference table | `prompt.md` §4 |
| `01-functional-slot-grammar.md` | **Function-first orchestration** — 9-slot taxonomy (lead, countermelody, harmony, bass, ostinato, pad, color, effect, punctuation), per-voice `%reason=` requirement, doubling rules, polyrhythm-as-routing, 12-step orchestration decision pipeline, headroom principles, practical LLM defaults | `prompt.md` §6, §7 |
| `02-canonical-score-patterns.md` | **Orchestrational archetypes from canonical scores** — Beethoven (economy + headroom), Stravinsky (color accretion + estranged register), Ravel (timbral rotation as form), Mahler (pad before melody), Holst (ostinato as identity), Williams (semantic color signatures). Each section ends with an extracted pattern and a generation rule. | `prompt.md` §7 |
| `03-instrument-map.md` | **Full orchestral instrument reference** — practical written ranges (conservative), slot profiles, timbre/register notes, common articulations, doubling partners, ABC family tags, special technique tables for strings and brass | `prompt.md` §8 |
| `04-abc-pattern-bank.md` | **15 original schematic etudes** organized by instrument family and slot — melody, harmony-inner, ostinato, color, ensemble excerpt, countermelody, inner-motion, color-lead (Stravinsky archetype), low melody, pedal bass, march-ostinato, harp pad, celesta magic-color, timpani punctuation, snare motor-grid. Includes transposition quick reference and slot conflict table. | `prompt.md` §10 |
| `05-llm-rules-and-metadata.md` | **Machine-checkable orchestration rule system** — per-voice YAML metadata schema (voice_id, slot, register_band, dynamic, attack_class, doubling_partner, polyrhythm_group, human_constraint, etc.), 9 YAML validation rules, practical composition defaults table, pre-emit validation checklist | `prompt.md` §11, §13 |

---

## Reading Order for Score Generation

1. **Start with `prompt.md`** — it is the operational top-level instruction and invocation point.
2. **Consult `00-music-theory-guardrails.md`** for any decision about phrase, harmony, melody, or cadence.
3. **Consult `01-functional-slot-grammar.md`** before assigning any voice or choosing any instrument.
4. **Consult `03-instrument-map.md`** when choosing which instrument to assign to a slot.
5. **Use `04-abc-pattern-bank.md`** as a copy-transpose-adapt source for each voice.
6. **Apply `05-llm-rules-and-metadata.md`** to validate the full score before emitting notation.
7. **Reference `02-canonical-score-patterns.md`** when a specific orchestrational archetype (headroom, color rotation, etc.) is needed.

---

## Relationship to prompt.md

`prompt.md` contains compact stubs for each expanded topic. The stubs give the LLM
enough context to operate without loading the full book, but direct it to the
appropriate book file when deeper reasoning is needed.

```
prompt.md  →  §4   →  book/00-music-theory-guardrails.md
           →  §6   →  book/01-functional-slot-grammar.md
           →  §7   →  book/01-functional-slot-grammar.md
                      book/02-canonical-score-patterns.md
           →  §8   →  book/03-instrument-map.md
           →  §10  →  book/04-abc-pattern-bank.md
           →  §11  →  book/05-llm-rules-and-metadata.md
           →  §13  →  book/05-llm-rules-and-metadata.md
```
