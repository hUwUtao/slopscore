"""Research-backed composition defaults for prompt construction.

The data in this module intentionally stays compact and explainable.
It captures a small set of music-emotion heuristics that are repeatedly
supported in music cognition literature and makes them available as
structured prompt context.

The profiles are not presented as hard rules.  They are defaults a
composition system can start from before applying genre-specific
changes or deliberate counterpoint against the expected mood.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


RESEARCH_SOURCES: tuple[dict[str, str], ...] = (
    {
        "id": "eerola2013",
        "title": "Emotional expression in music: contribution, linearity, and additivity of primary musical cues",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3726864/",
        "summary": (
            "Synthesizes evidence that tempo, mode, dynamics, articulation, register and timbre "
            "are primary cues for perceived emotion in music."
        ),
    },
    {
        "id": "lorenzi2023",
        "title": "Temporal Cues in the Judgment of Music Emotion for Normal and Cochlear Implant Listeners",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10134148/",
        "summary": (
            "Reinforces that fast tempo with major mode is commonly heard as happy, while slow tempo "
            "with minor mode is commonly heard as sad."
        ),
    },
    {
        "id": "drumming2018",
        "title": "Communication of emotion via drumming",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6204489/",
        "summary": (
            "Separates arousal-heavy cues such as tempo, loudness and articulation from valence-heavy "
            "cues such as mode and harmony."
        ),
    },
    {
        "id": "phraseforms",
        "title": "The Phrase, Archetypes, and Unique Forms",
        "url": "https://viva.pressbooks.pub/openmusictheory/chapter/phrase-level-forms-2/",
        "summary": (
            "Explains phrase goals, sentence and period archetypes, and the weak-to-strong cadence logic "
            "behind antecedent-consequent design."
        ),
    },
    {
        "id": "cadences",
        "title": "Cadences",
        "url": "https://musictheory.pugetsound.edu/mt21c/cadences.html",
        "summary": (
            "Defines authentic, half, plagal and deceptive cadence functions for phrase endings."
        ),
    },
    {
        "id": "tendencytones",
        "title": "Tendency tones and functional harmonic dissonances",
        "url": "https://viva.pressbooks.pub/openmusictheorycopy/chapter/tendency-tones-and-functional-harmonic-dissonances/",
        "summary": (
            "Summarizes common scale-degree tendencies such as ti resolving to do and le tending to sol."
        ),
    },
    {
        "id": "smoothvoiceleading",
        "title": "Jazz Voicings",
        "url": "https://viva.pressbooks.pub/openmusictheorycopy/chapter/jazz-voicings/",
        "summary": (
            "States the core practical rule that voice leading should generally be smooth, favoring common tones "
            "and stepwise motion over leaps across chord changes."
        ),
    },
    {
        "id": "embellishingtones",
        "title": "Embellishing tones",
        "url": "https://viva.pressbooks.pub/openmusictheorycopy/chapter/embellishing-tones-old/",
        "summary": (
            "Defines passing tones and neighbor tones as stepwise melodic embellishments between stable chord tones."
        ),
    },
    {
        "id": "local_orchestral_slot_grammar",
        "title": "Orchestral Slot Grammar for Rule-Based Score Generation",
        "url": "/home/stdpi/Downloads/deep-research-report (2).md",
        "summary": (
            "Local deep-research report imported into this project. It argues for function-first orchestration: "
            "assign each line a slot, register band, articulation, dynamic ceiling, doubling logic, and playability "
            "reason before writing notation."
        ),
    },
)


@dataclass(frozen=True)
class EmotionProfile:
    """A compact prompt-ready profile for a target emotional direction."""

    mood: str
    arousal: str
    valence: str
    tempo_bpm: tuple[int, int]
    mode_bias: tuple[str, ...]
    dynamics: str
    articulation: str
    register_bias: str
    rhythmic_density: str
    harmonic_tension: str
    orchestration_notes: tuple[str, ...]
    evidence: tuple[str, ...]
    inference_note: str

    def to_prompt_block(self) -> str:
        """Render the profile as compact markdown for prompt injection."""
        return "\n".join(
            [
                f"Mood: {self.mood}",
                f"Arousal: {self.arousal}",
                f"Valence: {self.valence}",
                f"Tempo target: {self.tempo_bpm[0]}-{self.tempo_bpm[1]} BPM",
                f"Mode bias: {', '.join(self.mode_bias)}",
                f"Dynamics: {self.dynamics}",
                f"Articulation: {self.articulation}",
                f"Register bias: {self.register_bias}",
                f"Rhythmic density: {self.rhythmic_density}",
                f"Harmonic tension: {self.harmonic_tension}",
                f"Orchestration notes: {'; '.join(self.orchestration_notes)}",
                f"Evidence tags: {', '.join(self.evidence)}",
                f"Interpretation note: {self.inference_note}",
            ]
        )


EMOTION_PROFILES: dict[str, EmotionProfile] = {
    "calm": EmotionProfile(
        mood="calm",
        arousal="low",
        valence="positive to neutral",
        tempo_bpm=(60, 84),
        mode_bias=("major", "lydian", "ionian"),
        dynamics="soft to mezzo-piano with gradual swells",
        articulation="mostly legato or lightly detached",
        register_bias="mid to upper-mid register",
        rhythmic_density="sparse; leave space between attacks",
        harmonic_tension="low to moderate; favor consonant extensions",
        orchestration_notes=(
            "Favor sustained pads, piano, guitar, strings or soft synths",
            "Reduce transient-heavy percussion",
            "Use reverb and long decays to support spaciousness",
        ),
        evidence=("eerola2013", "drumming2018"),
        inference_note=(
            "This profile is inferred from low-arousal cue directions in the cited literature rather than "
            "from a single study labeling 'calm' directly."
        ),
    ),
    "happy": EmotionProfile(
        mood="happy",
        arousal="medium to high",
        valence="positive",
        tempo_bpm=(100, 132),
        mode_bias=("major", "mixolydian"),
        dynamics="mezzo-forte with energetic accents",
        articulation="lightly detached or crisp legato",
        register_bias="upper-mid to high register",
        rhythmic_density="moderate to busy; recurring hooks and syncopation",
        harmonic_tension="moderate; use clear cadences and stable tonic returns",
        orchestration_notes=(
            "Keep the lead line bright and exposed",
            "Use drum patterns with clear pulse definition",
            "Double hooks with octave or timbral reinforcement",
        ),
        evidence=("eerola2013", "lorenzi2023", "drumming2018"),
        inference_note=(
            "The tempo band is a practical prompt range derived from the literature's fast-tempo direction, "
            "not a universal BPM law."
        ),
    ),
    "sad": EmotionProfile(
        mood="sad",
        arousal="low",
        valence="negative",
        tempo_bpm=(50, 78),
        mode_bias=("minor", "aeolian", "dorian"),
        dynamics="soft with restrained peaks",
        articulation="legato and connected phrasing",
        register_bias="mid to low register",
        rhythmic_density="sparse to moderate; longer note values",
        harmonic_tension="moderate; allow suspensions and unresolved color tones",
        orchestration_notes=(
            "Use thinner textures and fewer simultaneous attacks",
            "Favor solo or exposed timbres over thick tutti scoring",
            "Let melody carry the emotional weight rather than percussion",
        ),
        evidence=("eerola2013", "lorenzi2023"),
        inference_note=(
            "The profile follows the literature's recurring slow-tempo and minor-mode pattern while leaving "
            "room for ambiguous modal color."
        ),
    ),
    "tense": EmotionProfile(
        mood="tense",
        arousal="high",
        valence="negative to ambiguous",
        tempo_bpm=(92, 140),
        mode_bias=("minor", "phrygian", "locrian-adjacent color"),
        dynamics="mezzo-forte to forte with abrupt contrasts",
        articulation="staccato, accented or aggressively separated attacks",
        register_bias="low bass pressure plus exposed high-register figures",
        rhythmic_density="busy; ostinati and short repeating cells work well",
        harmonic_tension="high; emphasize dissonance, pedal tension and delayed resolution",
        orchestration_notes=(
            "Use percussion and low-end ostinati to maintain pressure",
            "Exploit contrast between sub-bass weight and brittle upper-register attacks",
            "Reserve full release for late structural points",
        ),
        evidence=("eerola2013", "drumming2018"),
        inference_note=(
            "This profile is inferred from high-arousal negative cue patterns, especially tempo, loudness, "
            "articulation and harmonic tension."
        ),
    ),
}


THEORY_RULES: dict[str, tuple[str, ...]] = {
    "form_and_phrase": (
        "Plan in 4-bar or 8-bar phrases unless the brief suggests otherwise.",
        "Use either a sentence design (presentation then continuation) or a period design (antecedent then consequent).",
        "Make the first phrase cadence weaker than the second; half cadence then authentic cadence is a reliable default.",
        "Reserve your strongest cadence for the end of a section, not every phrase.",
    ),
    "melody": (
        "Build melodies from one or two short motives, then repeat with variation rather than introducing constant new material.",
        "Place chord tones on metrically strong positions, especially at phrase openings and cadential beats.",
        "Use stepwise motion as the default and treat leaps as marked events.",
        "After a large leap, recover by step in the opposite direction when possible.",
        "Keep the melodic high point intentional: usually once per phrase or once per section.",
    ),
    "harmony": (
        "Assign clear harmonic function: tonic for arrival, predominant for departure, dominant for tension.",
        "Use progressions that increase functional momentum into cadences, such as ii-V-I or IV-V-I.",
        "Tonicize secondary goals sparingly so the tonal center stays legible.",
        "Change harmony often enough to support phrase shape, but not so often that the melody loses grounding.",
    ),
    "voice_leading": (
        "Prefer common tones first, then stepwise motion, then small skips.",
        "Avoid piling leaps into multiple voices at the same chord change unless the style specifically wants that effect.",
        "Treat leading tones carefully: ti usually resolves to do in the same voice.",
        "Let tendency tones resolve before introducing fresh dissonance.",
    ),
    "non_chord_tones": (
        "Use passing tones to connect chord tones by step across a third.",
        "Use neighbor tones to decorate a sustained pitch and return to stability.",
        "Use suspensions when you want delayed resolution at a cadence or arrival point.",
        "Make embellishing tones feel controlled by placing stable chord tones at structurally important beats.",
    ),
    "cadence_defaults": (
        "Authentic cadence: V-I for strong closure.",
        "Half cadence: ends on V for a question mark or sectional handoff.",
        "Deceptive cadence: V-vi or V-VI when you want to defer closure.",
        "Plagal cadence: IV-I for soft reinforcement after stronger dominant motion.",
    ),
}


ORCHESTRATION_SLOT_RULES: dict[str, tuple[str, ...]] = {
    "function_first": (
        "Assign function before instrument: lead, countermelody, harmony, bass, ostinato, pad, color, effect, or punctuation.",
        "Every sounding part must have a reasoned slot and must explain how it supports the audible hierarchy.",
        "Keep one primary auditory axis in each texture so the listener knows what to follow.",
        "Let slot changes carry continuity when instrument color should remain stable.",
        "Let instrument changes carry color development when harmony or motive should remain stable.",
    ),
    "per_part_metadata": (
        "Every ABC voice must include metadata comments for slot, role, register, dynamic, articulation, and reason.",
        "A part without a reason is invalid, even if its notes are syntactically correct.",
        "Reasoning must be concrete: explain why the part exists in the texture, not just that it sounds nice.",
        "If a voice changes function mid-piece, mark the new slot near the bar where the function changes.",
    ),
    "register_balance": (
        "Avoid same-register competition with the lead unless the intent is unison reinforcement.",
        "Space bass and low harmony wider than upper harmony to prevent mud.",
        "Place sustained support below or softer than active staccato or motor layers.",
        "Reserve piercing high color, brass weight, and dense tutti for structural arrivals.",
    ),
    "doubling_blend": (
        "Use doubling to change meaning: reinforcement, softening, brightening, darkening, or de-individualizing.",
        "Prefer natural overlapping doublings such as violin+flute, violin+oboe, viola+clarinet, cello+bassoon, and horn+low strings.",
        "Use horn as a bridge between brass and non-brass families when a blended middle is needed.",
        "Avoid gratuitous same-color unison doubling when expressivity and independence matter.",
    ),
    "playability": (
        "Check breath feasibility for winds and brass.",
        "Check bow or pluck endurance for strings.",
        "Avoid extreme high winds or brass at true pianissimo unless the unusual strain is intended.",
        "Keep harp, percussion, and special effects bounded by practical pedal, stick, mute, or technique-change constraints.",
    ),
    "polyrhythm": (
        "Treat polyrhythm as routing: one anchor grid, one counter-grid, and optional color accents.",
        "Separate competing rhythmic identities by register, timbre, or articulation.",
        "Do not stack multiple similar attack profiles in the same register unless the section intentionally becomes chaotic.",
        "After a chaotic climax, make the anchor grid recoverable.",
    ),
}


def list_supported_moods() -> tuple[str, ...]:
    """Return the supported research profile keys in sorted order."""
    return tuple(sorted(EMOTION_PROFILES))


def get_emotion_profile(mood: str) -> EmotionProfile:
    """Return a normalized emotion profile.

    Parameters
    ----------
    mood:
        Mood label such as ``happy`` or ``tense``.  Matching is
        case-insensitive.
    """
    normalized = mood.strip().lower()
    try:
        return EMOTION_PROFILES[normalized]
    except KeyError as exc:
        supported = ", ".join(list_supported_moods())
        raise KeyError(f"Unsupported mood '{mood}'. Supported moods: {supported}") from exc


def build_prompt_context(
    mood: str,
    *,
    genre: str | None = None,
    instruments: Iterable[str] | None = None,
    bars: int | None = None,
) -> str:
    """Build a compact prompt fragment with research-backed defaults."""
    profile = get_emotion_profile(mood)
    lines = ["Use the following research-backed defaults as a starting point:"]
    if genre:
        lines.append(f"Genre anchor: {genre}")
    if bars is not None:
        lines.append(f"Requested length: about {bars} bars")
    if instruments:
        lines.append(f"Requested instruments: {', '.join(instruments)}")
    lines.append(profile.to_prompt_block())
    lines.append(
        "Treat these defaults as priors, not hard constraints; override them deliberately when the arrangement "
        "benefits from emotional contrast."
    )
    return "\n".join(lines)


def build_theory_prompt_block() -> str:
    """Render the theory rules as compact prompt guidance."""
    lines: list[str] = ["Use the following detailed theory guardrails:"]
    for section, rules in THEORY_RULES.items():
        pretty_name = section.replace("_", " ")
        lines.append(f"{pretty_name.title()}:")
        lines.extend(f"- {rule}" for rule in rules)
    return "\n".join(lines)


def build_orchestration_prompt_block() -> str:
    """Render the imported slot-grammar orchestration rules."""
    lines: list[str] = ["Use the following orchestration slot grammar:"]
    for section, rules in ORCHESTRATION_SLOT_RULES.items():
        pretty_name = section.replace("_", " ")
        lines.append(f"{pretty_name.title()}:")
        lines.extend(f"- {rule}" for rule in rules)
    return "\n".join(lines)
