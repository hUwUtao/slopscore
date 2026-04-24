from pipeline import abc_output_path, ensure_workspace, get_pipeline_paths, write_abc_iteration, write_abc_output
from research import (
    ORCHESTRATION_SLOT_RULES,
    RESEARCH_SOURCES,
    build_orchestration_prompt_block,
    build_prompt_context,
    build_theory_prompt_block,
    get_emotion_profile,
    list_supported_moods,
)


def test_supported_moods_are_sorted_and_stable():
    assert list_supported_moods() == ("calm", "happy", "sad", "tense")


def test_emotion_profile_contains_expected_ranges():
    profile = get_emotion_profile("happy")
    assert profile.tempo_bpm == (100, 132)
    assert "major" in profile.mode_bias


def test_prompt_context_contains_requested_inputs():
    text = build_prompt_context("sad", genre="chamber pop", instruments=["piano"], bars=16)
    assert "Genre anchor: chamber pop" in text
    assert "Requested instruments: piano" in text
    assert "Tempo target: 50-78 BPM" in text


def test_theory_prompt_block_mentions_cadence_and_voice_leading():
    text = build_theory_prompt_block()
    assert "Cadence Defaults:" in text
    assert "Voice Leading:" in text


def test_orchestration_prompt_block_requires_reasoned_parts():
    text = build_orchestration_prompt_block()
    assert "Per Part Metadata:" in text
    assert "A part without a reason is invalid" in text
    assert "function_first" in ORCHESTRATION_SLOT_RULES
    assert any(source["id"] == "local_orchestral_slot_grammar" for source in RESEARCH_SOURCES)


def test_workspace_layout_and_abc_write(tmp_path):
    paths = ensure_workspace(tmp_path)
    assert paths.abc.exists()
    assert (paths.abc / ".gitignore").exists()

    output_path = write_abc_output(
        "Moonlit Procession",
        "X:1\nT:Moonlit Procession\nK:C\nCDEF|",
        root=tmp_path,
        run_id="demo-run",
    )
    assert output_path == abc_output_path("Moonlit Procession", tmp_path)
    assert output_path.read_text(encoding="utf-8").startswith("X:1")
    assert (get_pipeline_paths(tmp_path).runs / "demo-run.json").exists()


def test_abc_iteration_builds_derivatives(tmp_path):
    abc_text = "\n".join(
        [
            "X:1",
            "T:Tiny Tune",
            "M:4/4",
            "L:1/4",
            "Q:1/4=90",
            "K:C",
            "V:Lead name=\"Lead\" clef=treble",
            "%slot=lead %role=main_melody %register=mid %dyn=mp %art=legato",
            "%reason=Carries a minimal test motive so derivative generation has a valid source.",
            "[V:Lead] C D E F | G4 |",
        ]
    )
    abc_path, derivatives = write_abc_iteration("Tiny Tune", abc_text, root=tmp_path, run_id="tiny")
    assert abc_path.exists()
    assert derivatives.musicxml.exists()
    assert derivatives.midi.exists()
