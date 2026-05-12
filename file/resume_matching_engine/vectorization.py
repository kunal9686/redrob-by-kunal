"""Vector construction and similarity calculations."""

from __future__ import annotations

import math


def compute_tfidf_vectors(
    all_skills: list[set[str]],
    candidate_names: list[str],
    vocabulary: list[str],
) -> list[dict]:
    CORPUS_SIZE: int = 10

    df: dict[str, int] = {skill: 0 for skill in vocabulary}
    for skill_set in all_skills:
        for skill in skill_set:
            if skill in df:
                df[skill] += 1

    vectors: list[dict] = []
    for idx, skill_set in enumerate(all_skills):
        N = len(skill_set)
        tf = (1.0 / N) if N > 0 else 0.0

        vector: list[float] = []
        for skill in vocabulary:
            if skill in skill_set:
                idf = math.log(CORPUS_SIZE / df[skill])
                vector.append(round(tf * idf, 10))
            else:
                vector.append(0.0)

        vectors.append({"name": candidate_names[idx], "vector": vector})

    return vectors


def compute_jd_binary_vectors(
    jd_skills_list: list[set[str]],
    vocabulary: list[str],
) -> list[list[int]]:
    return [
        [1 if skill in jd_skills else 0 for skill in vocabulary]
        for jd_skills in jd_skills_list
    ]


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))
    if mag_a == 0.0 or mag_b == 0.0:
        return 0.0
    return dot / (mag_a * mag_b)
