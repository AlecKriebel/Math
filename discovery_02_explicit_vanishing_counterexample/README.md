# Explicit quartic counterexample to Zhao's Vanishing Conjecture

**Byline:** Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol.

This folder contains a provisional research note and exact certificates for a
54-variable homogeneous quartic Hessian-nilpotent polynomial `P` such that the
Keller map `Z - gradient(P)` is noninjective.

**Verification disclaimer:** Alec Kriebel is a complete amateur and cannot
independently verify these mathematical claims. The note is an experiment in
the limits of AI-assisted mathematics and requires independent expert review.

## Reproduce

From this directory, using the virtual environment in the parent folder:

```bash
../.venv/bin/python verify.py
../.venv/bin/python export_certificate.py
python3 verify_exported_stdlib.py
```

The full verifier checks the original three-dimensional map, the six-gadget
stable reduction, the 27-dimensional cubic homogeneous model, the quartic
construction, and the 54-dimensional collision in exact arithmetic.

## Files

- `explicit_vanishing_counterexample.md` — source research note.
- `construction.py` — exact straight-line construction.
- `verify.py` — exact verifier.
- `verify_exported_stdlib.py` — dependency-free verification of the expanded
  JSON polynomial and collision, independent of the construction code.
- `export_certificate.py` — regenerates the expanded sparse polynomial and
  collision files.
- `output/potential_sparse.json` — 598-term expansion over `Q(i)`.
- `output/collision.json` — two exact colliding 54-tuples.
- `output/pdf/explicit_vanishing_counterexample.pdf` — rendered note.

## Status

The algebraic construction has passed the included exact checks.  The novelty
claim is provisional because this result was developed within a day of the
announced Jacobian counterexample.  Obtain an expert algebraic-geometry review
and rerun a same-day literature search before public posting.
