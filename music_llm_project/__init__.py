"""Public package facade for the music LLM composition pipeline."""

from helper import (
    abc_to_musicxml,
    extract_audio_samples,
    generate_showcqt_spectrogram,
    midi_to_musicxml,
    musicxml_to_abc,
)
from pipeline import (
    DerivativePaths,
    PipelinePaths,
    abc_output_path,
    build_derivatives_from_abc,
    ensure_workspace,
    get_pipeline_paths,
    write_abc_iteration,
    write_abc_output,
)
from research import (
    ORCHESTRATION_SLOT_RULES,
    RESEARCH_SOURCES,
    THEORY_RULES,
    build_orchestration_prompt_block,
    build_prompt_context,
    build_theory_prompt_block,
    get_emotion_profile,
    list_supported_moods,
)

__all__ = [
    "abc_to_musicxml",
    "extract_audio_samples",
    "generate_showcqt_spectrogram",
    "midi_to_musicxml",
    "musicxml_to_abc",
    "DerivativePaths",
    "PipelinePaths",
    "abc_output_path",
    "build_derivatives_from_abc",
    "ensure_workspace",
    "get_pipeline_paths",
    "write_abc_iteration",
    "write_abc_output",
    "ORCHESTRATION_SLOT_RULES",
    "RESEARCH_SOURCES",
    "THEORY_RULES",
    "build_orchestration_prompt_block",
    "build_prompt_context",
    "build_theory_prompt_block",
    "get_emotion_profile",
    "list_supported_moods",
]
