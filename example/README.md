# Composition Benchmarks

This directory contains examples generated using the project's composition framework. While each was generated from different prompts, they serve as a benchmark for how different LLMs handle varying levels of **structural and orchestral complexity**.

## 📊 Complexity Tiers

These examples are ranked by the density of their orchestration, rhythmic intricacy, and adherence to formal theory.

### 🔴 High Complexity: Orchestral Tier
**Track:** [Windmill](./claude-opus-4.6/)  
**Model:** Claude 3.5 Opus (Revision 4.6) (human p/s: neither i know what revision is, opus 4.6 it is)
- **Scope:** 24 bars, 10 distinct instrumental voices.
- **Advanced Features:** 
  - **Polyrhythm**: 3-against-4 interlocking textures (Marimba vs. Pizzicato Violins).
  - **Dynamic Contrast**: Two specific "texture drops" (arrangement stripping) and rebuilds.
  - **Sectional Design**: 2-phase rebuild architecture with a specific catchiness-optimized hook.
  - **Advanced Theory**: Explicit mirror voices (chiptune pulse) and soft woodwind harmonization.

### 🟡 Medium Complexity: Chamber Tier
**Track:** [Meadow](./gemini-3.1-pro/)  
**Model:** Gemini 3.1 Pro  
- **Scope:** 16 bars, 4 instrumental voices (Flute, Fiddle, Guitar, Upright Bass).
- **Features:** 
  - **Thematic Variation**: A clear two-part form (A-B).
  - **Folk-Classical Blend**: Staccato accompaniment vs. legato lead.
  - **Balanced Orchestration**: Clear role separation between lead, texture, and root-motion bass.

### 🟢 Low Complexity: Sketch Tier
**Track:** [Wheatbreeze](./gpt5.5/)  
**Model:** GPT-5.5  
- **Scope:** 8-16 bars, simple harmonic support.
- **Features:** 
  - **Melodic Focus**: Concentrates on a single clear, childish melody.
  - **Functional Harmony**: Basic I-IV-V grounding.
  - **Sketching**: Ideal for quickly validating a motive or a specific emotional "flavor" (Sweet/Chill).

---

## 🛠️ Performance Observations

- **Density Management**: Models at higher complexity levels (like Opus) demonstrate a better ability to manage 8+ voices without creating "clash" (same-register collision).
- **Rhythmic Stability**: Complexity requires a strong anchor grid. The Woodblock/Shaker layer in *Windmill* allows the lead to wander significantly more than in *Wheatbreeze*.
- **Theory Adherence**: Higher complexity tiers show more intentional use of CADENCE and PHRASE logic, whereas Sketch tiers tend to drift more freely.
