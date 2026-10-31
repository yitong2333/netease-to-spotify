"""User-facing matching strictness settings."""

MATCH_LEVELS = ("strict", "balanced", "relaxed")
DEFAULT_MATCH_LEVEL = "balanced"

# Similarity is only used after exact title keys and curated aliases fail.
TITLE_SIMILARITY = {
    "strict": (1.0, 0),
    "balanced": (0.92, 3),
    "relaxed": (0.90, 4),
}


def normalize_match_level(value: str | None) -> str:
    level = (value or DEFAULT_MATCH_LEVEL).strip().lower()
    if not level:
        return DEFAULT_MATCH_LEVEL
    if level not in MATCH_LEVELS:
        options = ", ".join(MATCH_LEVELS)
        raise ValueError(f"MATCH_LEVEL must be one of: {options}.")
    return level
