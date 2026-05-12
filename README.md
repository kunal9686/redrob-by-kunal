# Resume Matching Engine

A standard-library-only Python implementation for the Redrob AI Campus Hackathon resume matching task.

The project normalizes candidate and JD skills, builds a shared vocabulary, computes TF-IDF vectors for resumes, builds binary vectors for job descriptions, and ranks the top 3 candidates for each JD using cosine similarity.

## Features

- Skill normalization with a mandatory `SKILL_ALIASES` map
- Multi-word phrase matching before single-token matching
- Deduplication of canonical skills
- Shared vocabulary built from the 10 resume corpus
- TF-IDF resume vectors and binary JD vectors
- Cosine similarity ranking with alphabetical tie-breaking
- Standard library only, no external dependencies

## Project Structure

```text
file/
├── README.md
├── resume_matching_engine_final.py
└── resume_matching_engine/
    ├── __init__.py
    ├── __main__.py
    ├── aliases.py
    ├── app.py
    ├── data.py
    ├── normalization.py
    ├── pipeline.py
    ├── ranking.py
    ├── reporting.py
    ├── vectorization.py
    └── vocabulary.py
```

## How To Run

### Manual Run Steps

1. Open a terminal in the `file` folder.
2. Make sure the workspace virtual environment exists at `.venv`.
3. Run the compatibility wrapper:

```powershell
c:/Users/Kunal/Desktop/OneDrive/Documents/Kunal/redrob/.venv/Scripts/python.exe .\resume_matching_engine_final.py
```

4. Or run the package directly:

```powershell
c:/Users/Kunal/Desktop/OneDrive/Documents/Kunal/redrob/.venv/Scripts/python.exe -m resume_matching_engine
```

5. Read the console output for the normalized skills, vocabulary, TF-IDF table, JD vectors, similarity matrix, and top 3 candidates per JD.

## Module Breakdown

- `aliases.py` contains the canonical skill alias map.
- `normalization.py` handles Steps 1 and 2: normalization and deduplication.
- `vocabulary.py` builds the shared sorted vocabulary.
- `vectorization.py` computes TF-IDF vectors, JD binary vectors, and cosine similarity.
- `ranking.py` ranks candidates for each JD.
- `reporting.py` prints the intermediate tables and final results.
- `data.py` stores the sample resumes and job descriptions used by the demo.
- `pipeline.py` wires the full workflow together.
- `app.py` is the CLI entrypoint.

## Notes

- The implementation uses only Python standard libraries.
- Scores are rounded to 2 decimal places.
- If you want to use your own dataset, replace the dictionaries in `data.py` or call `run_pipeline()` directly from your own script.
