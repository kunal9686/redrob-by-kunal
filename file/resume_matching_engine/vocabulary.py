"""Vocabulary construction for the resume matching engine."""

from __future__ import annotations

import logging

log = logging.getLogger("ResumeEngine")


def build_vocabulary(all_skills: list[set[str]]) -> list[str]:
    """Build the shared vocabulary from all resume skill sets."""
    union: set[str] = set()
    for skill_set in all_skills:
        union.update(skill_set)
    vocab = sorted(union)
    log.info("Vocabulary built: %d unique canonical skills.", len(vocab))
    return vocab
