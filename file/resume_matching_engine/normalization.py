"""Skill normalization and deduplication."""

from __future__ import annotations

import logging

from .aliases import SKILL_ALIASES, _SORTED_ALIAS_KEYS

log = logging.getLogger("ResumeEngine")


def normalize_skills(raw_skill_string: str) -> set[str]:
    """Convert a raw comma-separated skill string into canonical skills."""
    if not raw_skill_string or not raw_skill_string.strip():
        return set()

    canonical: set[str] = set()

    for entry in raw_skill_string.split(","):
        working = entry.strip().lower()
        if not working:
            continue

        for phrase in _SORTED_ALIAS_KEYS:
            if phrase in working:
                canonical.add(SKILL_ALIASES[phrase])
                working = working.replace(phrase, " ", 1)

        for token in working.split():
            token = token.strip()
            if token in SKILL_ALIASES:
                canonical.add(SKILL_ALIASES[token])

    log.debug("normalize_skills result: %s", sorted(canonical))
    return canonical
