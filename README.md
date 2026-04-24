# Music LLM Project

This repository is a small toolkit for building music-generation prompts that
are more structured than generic "write a song" instructions. It now has two
distinct layers of guidance:

- `prompt.md`: a detailed composition prompt with explicit theory rules
- `research.py`: compact research-backed defaults for emotion, phrasing, cadence, and voice leading
- `pipeline.py`: fixed output directories and file-writing helpers for autonomous agents

The goal is not to force one style. The goal is to give an LLM enough musical
structure that it can produce phrases, cadences, and motivic development
instead of wandering measure to measure.

## What Changed In This Revision

- Added `research.py` with reusable emotion profiles and theory guardrails
- Added `RESEARCH.md` documenting the source material used to shape the defaults
- Rewrote `prompt.md` to emphasize phrase structure, cadence planning, voice leading, non-chord-tone control, and per-part orchestration reasoning
- Fixed `pyproject.toml` so dependency metadata follows standard PEP 621 format
- Made `helper.py` import audio dependencies lazily so non-audio utilities remain importable

## Files

- `prompt.md`: the main prompt to give an LLM
- `research.py`: Python-accessible research data and prompt builders
- `pipeline.py`: canonical output layout for ABC, MusicXML, MIDI, audio, and spectrogram artifacts
- `RESEARCH.md`: source notes and interpretation choices
- `helper.py`: MusicXML/ABC conversion, CQT rendering, and sample extraction helpers

## Installation

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -e .
```

System tools still required for some helper functions:

- `ffmpeg`
- `abc2xml`
- `xml2abc`

## Usage

### Manual For Code Agents

Use this repository as the source of truth. A code agent should not invent a new
workflow; it should read the project prompt, produce reasoned ABC, then call the
pipeline.

Give the agent this instruction block:

```text
You are working inside music_llm_project.
Read prompt.md before composing.
Generate ABC notation only after planning form, phrase, harmony, slots, and part reasoning.
Every V: voice must have %slot=... metadata and a concrete %reason=...
Write the source ABC to workspace/outputs/abc/<slug>.abc.
After every iteration, build MusicXML and MIDI using write_abc_iteration().
Do not create new artifact folders.
Do not skip derivative generation.
```

The agent should then use this Python entry point:

```python
from music_llm_project import write_abc_iteration

abc_path, derivatives = write_abc_iteration(
    "Track Title",
    abc_text,
    run_id="track-title-v1",
)
```

Expected outputs:

- ABC source: `workspace/outputs/abc/<slug>.abc`
- MusicXML: `workspace/outputs/musicxml/<slug>.musicxml`
- MIDI: `workspace/outputs/midi/<slug>.mid`
- Run manifest: `workspace/runs/<run_id>.json`

Minimum valid ABC shape:

```abc
X:1
T:Track Title
M:3/4
L:1/8
Q:1/4=96
K:D
V:1 name="Lead" clef=treble
V:2 name="Support" clef=treble
%slot=lead %role=main_melody %register=upper_mid %dyn=mp %art=legato
%reason=Carries the singable motive in a clear register without same-register competition.
[V:1] A2 | d2 f2 e2 | d6 |]
%slot=harmony %role=soft_support %register=mid %dyn=p %art=broken_chords
%reason=Supports the lead with sparse harmony while staying softer and lower.
[V:2] z2 | F2 A2 d2 | F6 |]
```

Important constraints for agents:

- Use numeric voice IDs such as `V:1`, `V:2`, `V:3`; the derivative builder expects this generated-ABC subset.
- Keep tokens simple: notes, rests, accidentals, octave marks, and numeric durations.
- Avoid advanced ABC syntax unless the pipeline has been extended to parse it.
- Put reasoning comments before the music lines for the relevant voice.
- Treat ABC as the editable source; MusicXML and MIDI are generated artifacts.

### Manual For External API Agents

For a custom agent that calls an external OpenAI-compatible API, keep the model
stateless and let this repo own files.

Recommended flow:

1. Load `prompt.md`.
2. Optionally append `build_prompt_context(...)`, `build_theory_prompt_block()`, and `build_orchestration_prompt_block()`.
3. Ask the model to return only ABC text that follows the required metadata rules.
4. Validate that every `V:` voice has `%slot=` and `%reason=`.
5. Call `write_abc_iteration(title, abc_text, run_id=...)`.
6. Return the three artifact paths to the caller.

Minimal API caller skeleton:

```python
from pathlib import Path
from openai import OpenAI

from music_llm_project import (
    build_orchestration_prompt_block,
    build_prompt_context,
    build_theory_prompt_block,
    write_abc_iteration,
)

client = OpenAI()

title = "Wheatbreeze"
brief = "simple, chill, happy, childish, sweet, cold-breeze farm folk-classical melody"

system_prompt = Path("prompt.md").read_text(encoding="utf-8")
context = "\n\n".join(
    [
        build_prompt_context("happy", genre="folk classical", instruments=["tin whistle", "fiddle", "cello", "harp"], bars=16),
        build_theory_prompt_block(),
        build_orchestration_prompt_block(),
    ]
)

response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{context}\n\nCompose title: {title}\nBrief: {brief}\nReturn ABC only."},
    ],
)

abc_text = response.output_text
abc_path, derivatives = write_abc_iteration(title, abc_text, run_id="wheatbreeze-api-v1")

print(abc_path)
print(derivatives.musicxml)
print(derivatives.midi)
```

For OpenAI-compatible providers that use a different base URL:

```python
client = OpenAI(
    api_key="YOUR_KEY",
    base_url="https://your-provider.example/v1",
)
```

The model should not write files directly in API mode. The model returns ABC;
this repository writes the ABC, builds MusicXML, builds MIDI, and records the
run.

### Validation Checklist

Before accepting an iteration:

- The ABC has `X:`, `T:`, `M:`, `L:`, `Q:`, and `K:` headers.
- Every part is declared with a numeric `V:` voice.
- Every part has `%slot=...`.
- Every part has `%reason=...`.
- The source is written through `write_abc_iteration()`.
- MusicXML and MIDI are rebuilt after the ABC changes.
- `python -m pytest -q` passes.

### Build Research-Backed Prompt Context

```python
from music_llm_project import build_prompt_context, build_theory_prompt_block, ensure_workspace

ensure_workspace()
print(build_prompt_context("sad", genre="chamber pop", instruments=["piano", "cello"], bars=16))
print()
print(build_theory_prompt_block())
```

### Build Orchestration Slot Guidance

```python
from music_llm_project import build_orchestration_prompt_block

print(build_orchestration_prompt_block())
```

### Write A Complete Iteration

```python
from music_llm_project import ensure_workspace, write_abc_iteration

ensure_workspace()
abc_path, derivatives = write_abc_iteration(
    "Moonlit Procession",
    "X:1\nT:Moonlit Procession\nM:4/4\nL:1/8\nQ:1/4=72\nK:Em\nE2 F2 G2 A2|B4 A4|",
    run_id="demo-run",
)
print(abc_path)
print(derivatives.musicxml)
print(derivatives.midi)
```

### Convert Between Notation Formats

```python
from music_llm_project import midi_to_musicxml, musicxml_to_abc, abc_to_musicxml

xml_path = midi_to_musicxml("idea.mid")
abc_path = musicxml_to_abc(xml_path)
xml_roundtrip = abc_to_musicxml(abc_path)
```

### Generate A CQT Spectrogram

```python
from music_llm_project import generate_showcqt_spectrogram

image_path = generate_showcqt_spectrogram(
    "track.wav",
    "track_cqt.png",
    resolution="1280x720",
    fmin=55.0,
    fmax=1760.0,
    bins_per_octave=24,
)
```

### Extract Audio Samples

```python
from music_llm_project import extract_audio_samples

samples = extract_audio_samples("track.wav", "samples", sample_duration=2.0, step=1.0, sr=22050)
```

## Research Position

The project uses music-cognition and music-theory sources as priors, not
absolute laws. The most important change is that the prompt now forces the model
to think in terms of:

- motive and variation
- phrase archetypes
- cadence hierarchy
- harmonic function
- smooth voice leading
- controlled embellishment
- explicit reasoning for every score part

It also now enforces a tighter operational rule: autonomous agents should write
source compositions into `workspace/outputs/abc/` and keep derivative artifacts
inside the fixed workspace layout instead of inventing their own folders.

See [RESEARCH.md](RESEARCH.md) for source links and interpretation notes.
