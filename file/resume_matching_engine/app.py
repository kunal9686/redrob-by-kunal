"""Command-line entrypoint for the resume matching engine demo."""

from __future__ import annotations

import logging
import sys

from .data import RAW_JDS, RAW_RESUMES
from .pipeline import run_pipeline


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s │ %(message)s",
    )
    run_pipeline(RAW_RESUMES, RAW_JDS, top_n=3)
