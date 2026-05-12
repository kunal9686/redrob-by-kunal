"""End-to-end pipeline for the resume matching engine."""

from __future__ import annotations

import logging

from .normalization import normalize_skills
from .ranking import rank_candidates
from .reporting import (
    print_jd_binary_table,
    print_normalized_skills,
    print_similarity_matrix,
    print_top3_results,
    print_tfidf_table,
    print_vocabulary,
)
from .vectorization import compute_jd_binary_vectors, compute_tfidf_vectors
from .vocabulary import build_vocabulary

log = logging.getLogger("ResumeEngine")


def run_pipeline(
    raw_resumes: dict[str, str],
    raw_jds: dict[str, str],
    top_n: int = 3,
) -> dict[str, list[dict]]:
    log.info("Step 1 & 2 — Normalizing and deduplicating skills …")
    candidate_names = list(raw_resumes.keys())
    normalized_resume_skills: list[set[str]] = [
        normalize_skills(raw) for raw in raw_resumes.values()
    ]
    print_normalized_skills(candidate_names, normalized_resume_skills)

    log.info("Step 3 — Building shared vocabulary …")
    vocabulary = build_vocabulary(normalized_resume_skills)
    print_vocabulary(vocabulary)

    log.info("Step 4a — Computing TF-IDF vectors …")
    tfidf_vectors = compute_tfidf_vectors(
        normalized_resume_skills, candidate_names, vocabulary
    )
    print_tfidf_table(tfidf_vectors, vocabulary)

    log.info("Step 4b — Computing JD binary vectors …")
    jd_names = list(raw_jds.keys())
    normalized_jd_skills: list[set[str]] = [
        normalize_skills(raw) for raw in raw_jds.values()
    ]
    jd_vectors = compute_jd_binary_vectors(normalized_jd_skills, vocabulary)
    print_jd_binary_table(jd_names, jd_vectors, vocabulary)

    log.info("Step 5 — Ranking candidates …")
    rankings = rank_candidates(tfidf_vectors, jd_vectors, jd_names, top_n)

    matrix = rankings.pop("__matrix__")  # type: ignore[arg-type]
    print_similarity_matrix(matrix, jd_names, candidate_names)
    print_top3_results(rankings, jd_names)

    return rankings
