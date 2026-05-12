"""Candidate ranking for the resume matching engine."""

from __future__ import annotations

from .vectorization import cosine_similarity


def rank_candidates(
    tfidf_vectors: list[dict],
    jd_vectors: list[list[int]],
    jd_names: list[str],
    top_n: int = 3,
) -> dict[str, list[dict]]:
    """Compute cosine similarity for every resume-JD pair and rank candidates."""
    results: dict[str, list[dict]] = {}
    similarity_matrix: dict[str, dict[str, float]] = {}

    for jd_idx, jd_vector in enumerate(jd_vectors):
        jd_name = jd_names[jd_idx]
        scores: list[tuple[str, float]] = []

        for resume in tfidf_vectors:
            raw_sim = cosine_similarity(resume["vector"], jd_vector)
            rounded = round(raw_sim, 2)
            scores.append((resume["name"], rounded))
            similarity_matrix.setdefault(resume["name"], {})[jd_name] = rounded

        scores.sort(key=lambda x: (-x[1], x[0]))

        results[jd_name] = [
            {"rank": r + 1, "name": name, "score": score}
            for r, (name, score) in enumerate(scores[:top_n])
        ]

    results["__matrix__"] = similarity_matrix  # type: ignore[assignment]
    return results
