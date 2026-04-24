# Antigravity Music LLM Project

A research-backed framework for autonomous music composition using Large Language Models. This project bridges the gap between generic text prompts and structured, intentional music theory.

## 🌟 Core Philosophy

Instead of asking an LLM to "write a song," we provide a high-level composition engine that enforces:
- **Phrase Architecture**: Sentence and Period structures.
- **Harmonic Grammar**: Functional progressions with clear cadence hierarchies.
- **Orchestration Logic**: Function-first "slot" assignments (Lead, Ostinato, Pad, etc.).
- **Voice Leading**: Horizontal movement rules to prevent "note soup."

## 🎹 Featured Composition: "Windmill"

The showcase for this revision is **[Windmill](./example/claude-opus-4.6/)**, a 60-second loopable orchestral game soundtrack. It demonstrates:
- **Catchy Staccato Hooks**: A repeated 4-note motive with variation.
- **Intentional Drops**: Two planned texture breakdowns where rhythm cuts to solo harp and glockenspiel.
- **Orchestral Polyrhythm**: Interlocking 3-against-4 textures between pizzicato violins and marimba.
- **Clean Voice Leading**: A wandering flute melody harmonized by a soft oboe.

## 📂 Project Structure

- **Vocal Support**: Full integration for lyrics (`w:`), prosody alignment, and singing-part mapping.
- **Renderer Contract**: Mandatory `Q:` headers and MusicXML standardization for professional MuseScore output.

## 📂 Project Structure

- `prompt.md`: The "Command Center" — a slim entry point for LLMs.
- `book/`: The **Knowledge Base** — decomposed instruction files for theory, orchestration, instruments, and vocals.
  - `00-music-theory-guardrails.md`: Phrasing, harmony, and cadence grammar.
  - `01-functional-slot-grammar.md`: Pipeline decision ordering and slot taxonomy.
  - `02-canonical-score-patterns.md`: Reusable archetypes from Beethoven, Ravel, Stravinsky, etc.
  - `03-instrument-map.md`: Practical ranges and behavior for all families.
  - `04-abc-pattern-bank.md`: transposable schematic etudes.
  - `05-llm-rules-and-metadata.md`: Validation rules and YAML schema for voices.
  - `06-vocal-and-lyrics.md`: The guide for singing parts and lyric writing.
- `pipeline.py`: The pipeline for generating MIDI, MusicXML (with lyrics), and Audio.
- `research.py`: Programmatic access to research-backed defaults.
- `example/`: Curated outputs from different models.

## 🚀 Quick Start

### 1. Installation
```bash
uv venv .venv
source .venv/bin/activate
uv pip install -e .
```

### 2. Composition Workflow
1. **Plan**: Define the form, harmony, and orchestration slots.
2. **Draft**: Generate structured ABC notation following `prompt.md`.
3. **Build**: Use the pipeline to generate artifacts.
   ```bash
   cat score.abc | .venv/bin/python3 pipeline.py "title"
   ```

## 🎼 Examples

For a detailed breakdown of capability tiers, see the **[Complexity Benchmark Guide](./example/README.md)**.

| Model | Track | Key | Style | Artifacts |
|---|---|---|---|---|
| **Claude Opus** | **Windmill** | G Maj | Orchestral / Pastoral | [Folder](./example/claude-opus-4.6/) |
| **Gemini Pro** | Meadow | G Maj | Folk / Chamber | [Folder](./example/gemini-3.1-pro/) |
| **GPT-5.5** | Wheatbreeze | C Maj | Sweet / Folk | [Folder](./example/gpt5.5/) |

*Each example contains ABC source, MIDI, MP3 render, and PDF sheet music.*

---

**Antigravity**
*Advanced Agentic Coding*
