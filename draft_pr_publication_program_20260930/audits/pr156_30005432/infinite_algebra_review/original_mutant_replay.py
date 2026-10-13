#!/usr/bin/env python3
"""Read-only replay exposing assertion optimization in the original verifier.

The original is never edited. A non-character epsilon is substituted only into
an in-memory copy, with the original __file__ retained for its artifact hash.
"""
from pathlib import Path

original = Path(__file__).resolve().parent.parent / "original_submission/files/unsolved_math_prioritization/attempts/30005432/verify.py"
source = original.read_text()
before = "def eps(c):return 1 if c%4 in (0,1) else -1"
after = "def eps(c):return 1 if c%4 in (0,1,3) else -1"
if source.count(before) != 1:
    raise RuntimeError("Cannot apply exactly one intended character mutation")
mutated = source.replace(before, after)
exec(compile(mutated, str(original), "exec"), {"__name__": "__main__", "__file__": str(original)})
