# Research Notes

This project now separates two kinds of evidence-backed guidance:

- `research.py` emotion profiles for prompt defaults
- `prompt.md` theory guardrails for phrase structure, cadence, voice leading, and melodic design

The project does not treat the literature as immutable law. It uses the
sources below as compact priors that help an LLM start from musically plausible
 defaults instead of vague style adjectives.

## Sources Used

1. Eerola, Friberg, and Bresin, "Emotional expression in music: contribution, linearity, and additivity of primary musical cues"
   Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC3726864/
   Used for: tempo, mode, dynamics, articulation, register, and timbre as primary emotional cues.

2. Hofbauer et al., "Temporal Cues in the Judgment of Music Emotion for Normal and Cochlear Implant Listeners"
   Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC10134148/
   Used for: the robust happy/sad mapping between fast-major and slow-minor combinations.

3. Canales-Johnson et al., "Communication of emotion via drumming"
   Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC6204489/
   Used for: the separation between arousal-heavy cues such as tempo, loudness, articulation, and rhythmic features versus valence-heavy cues such as mode and harmony.

4. Peterson, "The Phrase, Archetypes, and Unique Forms"
   Link: https://viva.pressbooks.pub/openmusictheory/chapter/phrase-level-forms-2/
   Used for: sentence and period designs, antecedent-consequent logic, and weak-to-strong cadence planning.

5. Music Theory for the 21st-Century Classroom, "Cadences"
   Link: https://musictheory.pugetsound.edu/mt21c/cadences.html
   Used for: authentic, half, plagal, and deceptive cadence roles.

6. Open Music Theory, "Tendency tones and functional harmonic dissonances"
   Link: https://viva.pressbooks.pub/openmusictheorycopy/chapter/tendency-tones-and-functional-harmonic-dissonances/
   Used for: leading-tone and tendency-tone resolution guidance.

7. Open Music Theory, "Embellishing tones"
   Link: https://viva.pressbooks.pub/openmusictheorycopy/chapter/embellishing-tones-old/
   Used for: passing tones, neighbor tones, and suspension-style embellishment logic.

8. Open Music Theory, "Jazz Voicings"
   Link: https://viva.pressbooks.pub/openmusictheorycopy/chapter/jazz-voicings/
   Used for: smooth voice-leading guidance centered on common tones and minimal motion.

9. Local deep research report, "Orchestral Slot Grammar for Rule-Based Score Generation"
   Link: /home/stdpi/Downloads/deep-research-report (2).md
   Used for: function-first orchestration, score-part slot metadata, register/balance checks, doubling logic, polyrhythm routing, and human-playability validation.

## How The Project Uses These Sources

- The emotion profiles are intentionally conservative. They give the model a starting tempo band, modal bias, articulation style, and texture density.
- The theory rules are more important than the mood defaults. They tell the model how to turn a vibe into phrase-level structure.
- Several prompt rules are informed inferences rather than direct one-to-one quotations from a single paper. Where that happens, the code labels them as heuristic or inferred defaults.
- The local orchestration report is treated as imported project knowledge. Its central rule is now enforced in `prompt.md`: every score part must be reasoned with explicit slot metadata and a concrete explanation.

## Practical Interpretation

If the user asks for "sad piano music", the system should not only lower the
tempo and prefer minor color. It should also:

- build phrases with a cadence plan
- keep melody stepwise with deliberate leaps
- place stable chord tones on strong beats
- use thinner texture
- preserve smooth voice leading across harmonic changes

That is the main upgrade in this revision: the project now encodes theory-level
constraints, not only mood adjectives.

## Orchestration Import

The imported report adds a stricter rule for generated scores: do not start with
"which instrument should play?" Start with "what function must be audible?"

Every generated part should now carry:

- slot
- role
- register band
- dynamic and articulation
- reason for existing in the texture
- balance relationship to the lead or anchor
- human-playability check when relevant

For ABC output, this means each `V:` voice should be followed by comments such
as:

```abc
V:Lead name="Flute"
%slot=lead %role=main_melody %register=upper_mid %dyn=mp %art=legato
%reason=Carries the singable motive in a clear register without same-register competition.
```
