"""Opinionated workspace pipeline for generated music artifacts.

This module gives the project a fixed directory layout so autonomous
agents do not invent output locations ad hoc.  The primary contract is:

1. create or reuse the workspace layout
2. write ABC files into ``workspace/outputs/abc/``
3. derive any downstream artifacts from those ABC files

The layout is intentionally conservative so generated source notation can
be kept, while heavier derivative files remain ignored by git.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple


def _slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "untitled"


@dataclass(frozen=True)
class PipelinePaths:
    """Resolved project paths for generation outputs."""

    root: Path
    workspace: Path
    prompts: Path
    outputs: Path
    abc: Path
    musicxml: Path
    midi: Path
    audio: Path
    spectrograms: Path
    runs: Path

    def as_strings(self) -> dict[str, str]:
        return {key: str(value) for key, value in asdict(self).items()}


class DerivativePaths(NamedTuple):
    """Paths generated from an ABC source file."""

    musicxml: Path
    midi: Path


def get_pipeline_paths(root: str | Path | None = None) -> PipelinePaths:
    """Return the canonical workspace layout."""
    root_path = Path(root) if root is not None else Path(__file__).resolve().parent
    workspace = root_path / "workspace"
    outputs = workspace / "outputs"
    return PipelinePaths(
        root=root_path,
        workspace=workspace,
        prompts=workspace / "prompts",
        outputs=outputs,
        abc=outputs / "abc",
        musicxml=outputs / "musicxml",
        midi=outputs / "midi",
        audio=outputs / "audio",
        spectrograms=outputs / "spectrograms",
        runs=workspace / "runs",
    )


def ensure_workspace(root: str | Path | None = None) -> PipelinePaths:
    """Create the canonical workspace layout and placeholder files."""
    paths = get_pipeline_paths(root)
    for directory in (
        paths.workspace,
        paths.prompts,
        paths.outputs,
        paths.abc,
        paths.musicxml,
        paths.midi,
        paths.audio,
        paths.spectrograms,
        paths.runs,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    # Preserve empty directories in git where useful.
    for keep_path in (
        paths.abc / ".gitkeep",
        paths.musicxml / ".gitkeep",
        paths.midi / ".gitkeep",
        paths.audio / ".gitkeep",
        paths.spectrograms / ".gitkeep",
        paths.runs / ".gitkeep",
    ):
        keep_path.touch(exist_ok=True)

    # Directory-specific ignore rules keep noisy artifacts local while
    # retaining the canonical folder structure in the repository.
    ignore_specs = {
        paths.abc / ".gitignore": "*.abc\n!README.md\n!.gitkeep\n",
        paths.musicxml / ".gitignore": "*\n!README.md\n!.gitkeep\n",
        paths.midi / ".gitignore": "*\n!README.md\n!.gitkeep\n",
        paths.audio / ".gitignore": "*\n!README.md\n!.gitkeep\n",
        paths.spectrograms / ".gitignore": "*\n!README.md\n!.gitkeep\n",
        paths.runs / ".gitignore": "*\n!README.md\n!.gitkeep\n",
    }
    for ignore_path, contents in ignore_specs.items():
        ignore_path.write_text(contents, encoding="utf-8")

    readme_specs = {
        paths.abc / "README.md": (
            "# ABC Outputs\n\n"
            "Agents must write generated `.abc` source files into this directory.\n"
        ),
        paths.musicxml / "README.md": (
            "# MusicXML Outputs\n\n"
            "Derived MusicXML files belong here. They are generated from ABC or MIDI sources.\n"
        ),
        paths.midi / "README.md": (
            "# MIDI Outputs\n\n"
            "Derived MIDI playback files belong here.\n"
        ),
        paths.audio / "README.md": (
            "# Audio Outputs\n\n"
            "Rendered or extracted audio artifacts belong here.\n"
        ),
        paths.spectrograms / "README.md": (
            "# Spectrogram Outputs\n\n"
            "Generated spectrogram images and videos belong here.\n"
        ),
        paths.runs / "README.md": (
            "# Run Metadata\n\n"
            "Per-run manifests and transient metadata belong here.\n"
        ),
    }
    for readme_path, contents in readme_specs.items():
        if not readme_path.exists():
            readme_path.write_text(contents, encoding="utf-8")

    return paths


def abc_output_path(title: str, root: str | Path | None = None) -> Path:
    """Return the canonical path for a generated ABC file."""
    paths = ensure_workspace(root)
    return paths.abc / f"{_slugify(title)}.abc"


def write_abc_output(
    title: str,
    abc_text: str,
    *,
    root: str | Path | None = None,
    run_id: str | None = None,
) -> Path:
    """Write a generated ABC composition into the canonical output directory."""
    output_path = abc_output_path(title, root)
    output_path.write_text(abc_text.rstrip() + "\n", encoding="utf-8")

    if run_id:
        paths = ensure_workspace(root)
        manifest_path = paths.runs / f"{_slugify(run_id)}.json"
        manifest = {
            "run_id": run_id,
            "title": title,
            "abc_path": str(output_path),
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
        }
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    return output_path


def _abc_pitch_to_music21(token: str) -> tuple[str | None, float]:
    """Parse a simple ABC note/rest token into a pitch name and quarter length."""
    match = re.fullmatch(r"(?P<acc>\^|_|=)?(?P<name>[A-Ga-gz])(?P<oct>[,']*)(?P<len>\d*)", token)
    if not match:
        raise ValueError(f"Unsupported ABC token: {token}")

    length = int(match.group("len") or "1") * 0.5
    name = match.group("name")
    if name == "z":
        return None, length

    pitch_name = name.upper()
    accidental = match.group("acc") or ""
    if accidental == "^":
        pitch_name += "#"
    elif accidental == "_":
        pitch_name += "-"

    octave = 5 if name.islower() else 4
    for marker in match.group("oct"):
        octave += 1 if marker == "'" else -1
    return f"{pitch_name}{octave}", length


def _instrument_for_name(name: str):
    from music21 import instrument

    lowered = name.lower()
    if "whistle" in lowered or "flute" in lowered:
        return instrument.Flute()
    if "fiddle" in lowered or "violin" in lowered:
        return instrument.Violin()
    if "cello" in lowered:
        return instrument.Violoncello()
    if "harp" in lowered:
        return instrument.Harp()
    return instrument.Piano()


def _score_from_simple_abc(abc_path: Path):
    """Create a measured music21 score from the generated ABC subset."""
    from music21 import clef, duration, key, metadata, meter, note, stream, tempo

    text = abc_path.read_text(encoding="utf-8")
    title = abc_path.stem
    time_signature = "4/4"
    key_signature = "C"
    tempo_bpm = 120
    voice_defs: dict[str, dict[str, str]] = {}
    voice_bars: dict[str, list[list[str]]] = {}

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("T:"):
            title = line[2:].strip()
        elif line.startswith("M:"):
            time_signature = line[2:].strip()
        elif line.startswith("Q:"):
            numbers = re.findall(r"\d+", line)
            if numbers:
                tempo_bpm = int(numbers[-1])
        elif line.startswith("K:"):
            key_signature = line[2:].strip()
        elif line.startswith("V:"):
            voice_id = line[2:].split()[0]
            name_match = re.search(r'name="([^"]+)"', line)
            clef_match = re.search(r"clef=([a-zA-Z]+)", line)
            voice_defs[voice_id] = {
                "name": name_match.group(1) if name_match else voice_id,
                "clef": clef_match.group(1) if clef_match else "treble",
            }
            voice_bars.setdefault(voice_id, [])
        elif line.startswith("[V:"):
            prefix, music = line.split("]", 1)
            voice_id = prefix[3:].strip()
            # Remove chord markers and repeat symbols before splitting into bars
            sanitized_music = re.sub(r'"[^"]*"', "", music)
            # Remove inline ABC tags like [Q:1/4=120] or [M:4/4]
            sanitized_music = re.sub(r"\[[A-Z]:[^\]]*\]", "", sanitized_music)
            sanitized_music = sanitized_music.replace("|:", "|").replace(":|", "|").replace("|]", "|")
            bars = [bar.strip() for bar in sanitized_music.split("|")]
            for bar in bars:
                if bar:
                    # Find all note/rest tokens in the bar using regex
                    # This handles clumps like 'GABc' as well as [CEG]2 chords
                    tokens = re.findall(r"\[[^\]]+\]\d*|[\^|_|=]?[A-Ga-gz][,']*\d*", bar)
                    if tokens:
                        voice_bars.setdefault(voice_id, []).append(tokens)

    score = stream.Score(id=title)
    score.insert(0, metadata.Metadata())
    score.metadata.title = title
    score.metadata.composer = "Music LLM Project"
    score.insert(0, tempo.MetronomeMark(number=tempo_bpm))

    from music21 import chord

    for voice_id, definition in voice_defs.items():
        part = stream.Part(id=f"V{voice_id}")
        part.partName = definition["name"]
        part.insert(0, _instrument_for_name(definition["name"]))
        part.insert(0, clef.BassClef() if definition["clef"] == "bass" else clef.TrebleClef())
        part.insert(0, meter.TimeSignature(time_signature))
        part.insert(0, key.Key(key_signature))

        for index, tokens in enumerate(voice_bars.get(voice_id, []), start=1):
            measure = stream.Measure(number=index)
            for token in tokens:
                if token.startswith("["):
                    # Extract multiplier after the bracket, e.g., [CEG]2 -> 2
                    m_len = re.search(r"\](\d*)$", token)
                    multiplier = int(m_len.group(1) or "1") if m_len else 1
                    
                    chord_notes = re.findall(r"[\^|_|=]?[A-Ga-gz][,']*\d*", token)
                    pitches = []
                    ql = 0.5 * multiplier
                    if chord_notes:
                        for cn in chord_notes:
                            p, dur = _abc_pitch_to_music21(cn)
                            if p:
                                pitches.append(p)
                            ql = dur * multiplier # Inherit internal duration if present
                        element = chord.Chord(pitches)
                    else:
                        element = note.Rest()
                    element.duration = duration.Duration(ql)
                else:
                    pitch_name, quarter_length = _abc_pitch_to_music21(token)
                    element = note.Rest() if pitch_name is None else note.Note(pitch_name)
                    element.duration = duration.Duration(quarter_length)
                measure.append(element)
            part.append(measure)
        score.append(part)

    return score


def build_derivatives_from_abc(
    abc_path: str | Path,
    *,
    root: str | Path | None = None,
) -> DerivativePaths:
    """Build MusicXML and MIDI derivatives from an ABC file.

    The output filenames use the ABC stem and are written into the
    canonical pipeline derivative folders.
    """
    paths = ensure_workspace(root)
    source_path = Path(abc_path)
    if not source_path.exists():
        raise FileNotFoundError(f"ABC file does not exist: {source_path}")

    score = _score_from_simple_abc(source_path)
    musicxml_path = paths.musicxml / f"{source_path.stem}.musicxml"
    midi_path = paths.midi / f"{source_path.stem}.mid"
    score.write("musicxml", fp=str(musicxml_path))
    score.write("midi", fp=str(midi_path))
    return DerivativePaths(musicxml=musicxml_path, midi=midi_path)


def write_abc_iteration(
    title: str,
    abc_text: str,
    *,
    root: str | Path | None = None,
    run_id: str | None = None,
) -> tuple[Path, DerivativePaths]:
    """Write ABC and immediately build MusicXML plus MIDI derivatives."""
    abc_path = write_abc_output(title, abc_text, root=root, run_id=run_id)
    derivative_paths = build_derivatives_from_abc(abc_path, root=root)
    return abc_path, derivative_paths


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Music LLM Pipeline CLI")
    parser.add_argument("title", help="Slugified title for the composition")
    parser.add_argument("--run-id", help="Optional run ID for manifest tracking")
    
    args = parser.parse_args()
    
    # Read ABC content from stdin
    abc_content = sys.stdin.read()
    if not abc_content.strip():
        print("Error: No ABC content provided via stdin.", file=sys.stderr)
        sys.exit(1)
        
    try:
        abc_path, derivatives = write_abc_iteration(args.title, abc_content, run_id=args.run_id)
        print(f"SUCCESS")
        print(f"ABC: {abc_path}")
        print(f"MusicXML: {derivatives.musicxml}")
        print(f"MIDI: {derivatives.midi}")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
