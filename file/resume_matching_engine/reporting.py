"""Console reporting helpers for the resume matching engine."""

from __future__ import annotations


def _banner(title: str, width: int = 64) -> None:
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_normalized_skills(names: list[str], skill_sets: list[set[str]]) -> None:
    _banner("STEP 1 & 2 — Normalized Skills per Resume")
    for name, skills in zip(names, skill_sets):
        print(f"\n  {name}")
        print(f"    Skills ({len(skills)}): {', '.join(sorted(skills))}")


def print_vocabulary(vocabulary: list[str]) -> None:
    _banner("STEP 3 — Shared Vocabulary (alphabetically sorted)")
    for i, skill in enumerate(vocabulary, 1):
        print(f"  {i:>3}.  {skill}")
    print(f"\n  Total: {len(vocabulary)} unique canonical skills")


def print_tfidf_table(tfidf_vectors: list[dict], vocabulary: list[str]) -> None:
    _banner("STEP 4a — TF-IDF Vectors (non-zero entries only)")
    for resume in tfidf_vectors:
        nonzero = [
            (skill, val)
            for skill, val in zip(vocabulary, resume["vector"])
            if val > 0
        ]
        print(f"\n  {resume['name']}")
        for skill, val in nonzero:
            bar = "█" * int(val * 30)
            print(f"    {skill:<32} {val:.6f}  {bar}")


def print_jd_binary_table(
    jd_names: list[str],
    jd_vectors: list[list[int]],
    vocabulary: list[str],
) -> None:
    _banner("STEP 4b — JD Binary Vectors (required skills only)")
    for jd_name, bvec in zip(jd_names, jd_vectors):
        required = [skill for skill, bit in zip(vocabulary, bvec) if bit == 1]
        print(f"\n  {jd_name}")
        print(f"    Required skills ({len(required)}): {', '.join(required)}")


def print_similarity_matrix(
    matrix: dict[str, dict[str, float]],
    jd_names: list[str],
    names: list[str],
) -> None:
    _banner("STEP 5 — Full Cosine Similarity Matrix")
    col_w = 28
    header = f"  {'Candidate':<22}" + "".join(f"  {jd[:col_w]:<{col_w}}" for jd in jd_names)
    print(header)
    print("  " + "─" * (22 + (col_w + 2) * len(jd_names)))
    for name in names:
        row = f"  {name:<22}"
        for jd in jd_names:
            score = matrix.get(name, {}).get(jd, 0.0)
            row += f"  {score:<{col_w}.2f}"
        print(row)


def print_top3_results(
    rankings: dict[str, list[dict]],
    jd_names: list[str],
) -> None:
    _banner("STEP 5 - TOP 3 CANDIDATES PER JD")
    for jd_name in jd_names:
        top = rankings[jd_name]
        print(f"\n  +-- {jd_name}")
        for candidate in top:
            medal = {1: "[1]", 2: "[2]", 3: "[3]"}.get(candidate["rank"], "   ")
            bar = "#" * int(candidate["score"] * 20)
            print(
                f"  |  {medal}  #{candidate['rank']}  "
                f"{candidate['name']:<22}  Score: {candidate['score']:.2f}  {bar}"
            )
        print("  +" + "-" * 52)
