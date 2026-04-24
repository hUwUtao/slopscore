"""Top level package for the music LLM composition pipeline.

Importing this package exposes the :mod:`helper` module which contains
functions for file format conversion, spectrogram generation and audio
sample extraction.  See :mod:`music_llm_project.helper` for details.
"""

from .helper import (
    midi_to_musicxml,
    musicxml_to_abc,
    abc_to_musicxml,
    generate_showcqt_spectrogram,
    extract_audio_samples,
)
from .pipeline import (
    DerivativePaths,
    PipelinePaths,
    abc_output_path,
    build_derivatives_from_abc,
    ensure_workspace,
    get_pipeline_paths,
    write_abc_output,
    write_abc_iteration,
)
from .research import (
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
    'midi_to_musicxml',
    'musicxml_to_abc',
    'abc_to_musicxml',
    'generate_showcqt_spectrogram',
    'extract_audio_samples',
    'PipelinePaths',
    'DerivativePaths',
    'abc_output_path',
    'build_derivatives_from_abc',
    'ensure_workspace',
    'get_pipeline_paths',
    'write_abc_output',
    'write_abc_iteration',
    'ORCHESTRATION_SLOT_RULES',
    'RESEARCH_SOURCES',
    'THEORY_RULES',
    'build_orchestration_prompt_block',
    'build_prompt_context',
    'build_theory_prompt_block',
    'get_emotion_profile',
    'list_supported_moods',
]
