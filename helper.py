"""Helper functions for the Music‑LLM composition pipeline.

This module provides utilities to convert between music file formats,
generate visualisations from audio and extract samples.  The functions
here are designed to be used by an orchestration agent or notebook
that constructs prompts for a large language model (LLM).  They rely on
external tools such as **music21**, **ffmpeg** and the `abc2xml`/`xml2abc`
utilities.  See the accompanying ``README.md`` for installation
instructions and further context.

Functions
---------
* :func:`midi_to_musicxml` – Convert a MIDI file to MusicXML using
  ``music21``.
* :func:`musicxml_to_abc` – Convert a MusicXML file to ABC notation via
  the ``xml2abc`` command‑line utility.
* :func:`abc_to_musicxml` – Convert ABC notation to MusicXML via
  ``abc2xml``.
* :func:`generate_showcqt_spectrogram` – Produce a constant‑Q
  spectrogram montage (video or image) from an audio file using
  ``ffmpeg``'s ``showcqt`` filter.  The constant‑Q transform uses
  logarithmic frequency spacing, making it well suited to musical
  applications【770927889230779†L84-L104】.
* :func:`extract_audio_samples` – Slice an audio file into
  overlapping samples using ``librosa``.

Note
----
These helpers raise exceptions on failure rather than swallowing
errors.  They return the path of the generated file for convenience.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Iterable, Optional, Tuple

def midi_to_musicxml(midi_path: str | Path, output_xml_path: Optional[str | Path] = None) -> str:
    """Convert a MIDI file to MusicXML using the :mod:`music21` library.

    Parameters
    ----------
    midi_path:
        Path to the input MIDI file.
    output_xml_path:
        Optional path for the resulting MusicXML.  If omitted,
        ``midi_path`` will be used with a ``.xml`` extension.

    Returns
    -------
    str
        The filesystem path of the generated MusicXML file.

    Raises
    ------
    FileNotFoundError
        If the input MIDI does not exist.
    RuntimeError
        If ``music21`` cannot parse the MIDI or write MusicXML.

    Examples
    --------
    >>> xml_path = midi_to_musicxml('example.mid')
    >>> print(xml_path)
    'example.xml'

    This uses the ``music21.converter.parse()`` function under the hood,
    which loads MIDI files and converts them into a stream object
    representing the score.  The stream is then written to MusicXML
    using the ``write('musicxml', ...)`` method.
    """
    midi_path = Path(midi_path)
    if not midi_path.exists():
        raise FileNotFoundError(f"MIDI file does not exist: {midi_path}")
    # Lazily import music21 to avoid heavy startup cost when not needed
    from music21 import converter

    try:
        stream = converter.parse(str(midi_path))
    except Exception as exc:
        raise RuntimeError(f"Failed to parse MIDI file {midi_path}: {exc}") from exc

    if output_xml_path is None:
        output_xml_path = midi_path.with_suffix('.xml')
    output_xml_path = Path(output_xml_path)

    try:
        stream.write('musicxml', fp=str(output_xml_path))
    except Exception as exc:
        raise RuntimeError(f"Failed to write MusicXML to {output_xml_path}: {exc}") from exc

    return str(output_xml_path)


def musicxml_to_abc(
    xml_path: str | Path,
    output_abc_path: Optional[str | Path] = None,
    *,
    xml2abc_binary: str = 'xml2abc',
) -> str:
    """Convert a MusicXML file to ABC notation using the ``xml2abc`` command.

    The `xml2abc` utility is part of the `abc2xml` project.  It
    translates MusicXML into ABC notation and can handle single or
    multi‑part scores.  See the project page for installation details【194094322856984†L0-L10】.

    Parameters
    ----------
    xml_path:
        Path to the MusicXML file.
    output_abc_path:
        Path for the output ``.abc`` file.  If omitted the suffix is
        changed to ``.abc``.
    xml2abc_binary:
        Name or path of the ``xml2abc`` executable.  Defaults to
        ``xml2abc`` assuming it is on the system ``PATH``.

    Returns
    -------
    str
        Filesystem path of the generated ABC file.

    Raises
    ------
    FileNotFoundError
        If the input file cannot be found.
    RuntimeError
        If the `xml2abc` command returns a non‑zero exit status.
    """
    xml_path = Path(xml_path)
    if not xml_path.exists():
        raise FileNotFoundError(f"MusicXML file does not exist: {xml_path}")
    if output_abc_path is None:
        output_abc_path = xml_path.with_suffix('.abc')
    output_abc_path = Path(output_abc_path)

    cmd = [xml2abc_binary, str(xml_path), '-o', str(output_abc_path)]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Cannot find '{xml2abc_binary}' executable. Install abc2xml and ensure it is on your PATH"
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"xml2abc failed with exit code {exc.returncode}: {exc.stderr.decode('utf-8', errors='ignore')}"
        ) from exc

    return str(output_abc_path)


def abc_to_musicxml(
    abc_path: str | Path,
    output_xml_path: Optional[str | Path] = None,
    *,
    abc2xml_binary: str = 'abc2xml',
) -> str:
    """Convert an ABC notation file to MusicXML using the ``abc2xml`` tool.

    The `abc2xml` program is a command‑line utility that reads an ABC
    file and writes MusicXML【194094322856984†L0-L10】.  This wrapper calls the
    tool via :func:`subprocess.run` and returns the path of the
    generated MusicXML.  It does not parse ABC files directly; for
    parsing ABC inside Python see the `music21.abc` module.

    Parameters
    ----------
    abc_path:
        Path to the ABC file to convert.
    output_xml_path:
        Optional path to write the MusicXML.  Defaults to ``.xml``
        suffixed file.
    abc2xml_binary:
        Name or path of the executable.  Defaults to ``abc2xml``.

    Returns
    -------
    str
        Filesystem path of the generated MusicXML.

    Raises
    ------
    FileNotFoundError
        If the ABC file or ``abc2xml`` binary is missing.
    RuntimeError
        If ``abc2xml`` fails.
    """
    abc_path = Path(abc_path)
    if not abc_path.exists():
        raise FileNotFoundError(f"ABC file does not exist: {abc_path}")
    if output_xml_path is None:
        output_xml_path = abc_path.with_suffix('.xml')
    output_xml_path = Path(output_xml_path)

    cmd = [abc2xml_binary, str(abc_path), '-o', str(output_xml_path)]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Cannot find '{abc2xml_binary}' executable. Install abc2xml and ensure it is on your PATH"
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"abc2xml failed with exit code {exc.returncode}: {exc.stderr.decode('utf-8', errors='ignore')}"
        ) from exc

    return str(output_xml_path)


def generate_showcqt_spectrogram(
    audio_path: str | Path,
    output_path: str | Path,
    *,
    resolution: str = '1920x1080',
    fps: int = 25,
    fmin: float = 27.5,
    fmax: float = 4186.0,
    bins_per_octave: int = 36,
) -> str:
    """Generate a constant‑Q spectrogram montage using ffmpeg's ``showcqt`` filter.

    The constant‑Q transform (CQT) uses a logarithmic frequency axis; this
    property makes it particularly suitable for music analysis【770927889230779†L84-L104】.
    The `showcqt` filter in ffmpeg renders the CQT as an image sequence or
    video【257277270614161†L188-L193】.  This function wraps ffmpeg to produce a
    single image by limiting frames to 1.

    Parameters
    ----------
    audio_path:
        Path to the input audio file (e.g., WAV, MP3).
    output_path:
        Path to the output file.  The extension determines the
        container (e.g., ``.png`` or ``.mp4``).  To create a still
        image, choose an image format and specify ``-frames:v 1``.
    resolution:
        Frame resolution passed to ffmpeg in WxH notation.  Default is
        ``1920x1080``.
    fps:
        Frames per second.  Because we limit to one frame, this value
        influences only intermediate processing.
    fmin, fmax:
        Minimum and maximum frequency for the CQT display.
    bins_per_octave:
        Number of bins per octave.  A higher number yields finer
        frequency resolution; default 36 (three bins per semitone).

    Returns
    -------
    str
        Filesystem path of the created spectrogram image/video.

    Raises
    ------
    FileNotFoundError
        If the input audio file cannot be found.
    RuntimeError
        If ffmpeg returns an error.
    """
    audio_path = Path(audio_path)
    output_path = Path(output_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file does not exist: {audio_path}")
    # Build the ffmpeg command.  We request only one frame (image) output.
    # The side panel (sideright) is disabled to focus on the CQT display.
    showcqt_filter = (
        f"showcqt=s={resolution}:fps={fps}:fmin={fmin}:fmax={fmax}"
        f":csp=bt709:basefreq=440:bins_per_octave={bins_per_octave}"
    )
    cmd: list[str] = [
        'ffmpeg', '-y', '-i', str(audio_path), '-lavfi', showcqt_filter,
        '-frames:v', '1', str(output_path)
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            "ffmpeg executable not found. Install ffmpeg and ensure it is on your PATH"
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"ffmpeg failed with exit code {exc.returncode}: {exc.stderr.decode('utf-8', errors='ignore')}"
        ) from exc
    return str(output_path)


def extract_audio_samples(
    audio_path: str | Path,
    output_dir: str | Path,
    *,
    sample_duration: float = 1.0,
    step: float = 0.5,
    sr: int = 44100,
) -> Tuple[str, ...]:
    """Slice an audio file into overlapping samples and write them to disk.

    This function loads an audio file, divides it into windows of
    ``sample_duration`` seconds with an overlap determined by
    ``step``, and writes each window as a separate WAV file in
    ``output_dir``.  It uses ``librosa`` to load audio and ``soundfile``
    (`sf.write`) to save each segment.

    Parameters
    ----------
    audio_path:
        Path to the source audio file.
    output_dir:
        Directory in which to place the extracted samples.  It will be
        created if it does not exist.
    sample_duration:
        Length of each sample in seconds.
    step:
        Hop length between successive samples in seconds.  Must be
        positive; values less than ``sample_duration`` result in
        overlapping windows.
    sr:
        Sample rate for loading the audio.  If the file has a
        different sample rate it will be resampled.

    Returns
    -------
    tuple[str, ...]
        A tuple of file paths for the extracted samples.

    Raises
    ------
    FileNotFoundError
        If the source audio cannot be found.
    ValueError
        If invalid parameters are provided.
    """
    audio_path = Path(audio_path)
    output_dir = Path(output_dir)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file does not exist: {audio_path}")
    if sample_duration <= 0:
        raise ValueError("sample_duration must be > 0")
    if step <= 0:
        raise ValueError("step must be > 0")
    # Lazily import the heavier audio stack so format-conversion helpers
    # can still be imported in environments that do not need librosa.
    import librosa
    import soundfile as sf

    # Load audio using librosa.  This returns a mono signal.
    y, _sr = librosa.load(str(audio_path), sr=sr)
    n_samples = int(sample_duration * sr)
    hop_length = int(step * sr)
    total_len = len(y)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[str] = []
    index = 0
    start = 0
    while start + n_samples <= total_len:
        segment = y[start : start + n_samples]
        segment_path = output_dir / f"sample_{index:05d}.wav"
        sf.write(str(segment_path), segment, sr)
        paths.append(str(segment_path))
        index += 1
        start += hop_length
    return tuple(paths)
