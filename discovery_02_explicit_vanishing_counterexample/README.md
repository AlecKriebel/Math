# Explicit Hessian-nilpotent quartic witnessing the failure of Zhao's Vanishing Conjecture

**Author:** Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol.

The paper contains a full AI-assistance and verification disclosure.

This folder contains a provisional research note and exact certificates for a
54-variable homogeneous quartic Hessian-nilpotent polynomial `P` such that the
Keller map `Z - gradient(P)` is noninjective, explicitly witnessing the failure
of Zhao's Vanishing Conjecture.

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

The standard-library verifier checks the exported polynomial's degree and term
count and the collision directly from the JSON files. It is not a stand-alone
verification of Hessian nilpotence.

Build the arXiv-ready PDF with [Tectonic](https://tectonic-typesetting.github.io/):

```bash
python3 src/render_note.py
```

## Files

- `explicit_vanishing_counterexample.md` — source research note.
- `explicit_vanishing_counterexample.tex` — canonical arXiv-ready typeset source.
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

The algebraic construction has passed the included exact checks. The scoped
novelty claim was searched again on 21 July 2026 and is stated cautiously in
the note. The result remains unreviewed, and independent expert review is
welcome.
