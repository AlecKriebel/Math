# Archival Exploration 01: a weighted-lift specialization

**Byline:** Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol.

This workspace contains a provisional research note and an exact symbolic
checker prompted by the polynomial counterexample to the Jacobian conjecture
announced on 19 July 2026.

> **Archived and subsumed.** Mikhail Szh published a stronger theorem for the
> entire Gallagher weighted-lift family before this note appeared. The
> monodromy and deck-group claims are therefore not novel. The particular seed
> and uniform rational collision were moved into Appendix A of Discovery 03,
> which is now itself a technical precursor to the canonical Discovery 07
> consequence paper. The weighted-lift appendix is not part of Discovery 07.

**Verification disclaimer:** Alec Kriebel is a complete amateur and cannot
independently verify these mathematical claims. The note is an experiment in
the limits of AI-assisted mathematics and requires independent expert review.

Starting from Gallagher's every-degree weighted-lift construction, itself a
follow-on to Alpoge's announced counterexample, the note isolates a particularly
simple explicit family `F_n : C^3 -> C^3`, one for every integer `n >= 3`, such
that:

- `det(J F_n) = 1`;
- the generic fiber has exactly `n` points;
- the Galois closure of `C(x,y,z) / C(F_n)` has group `S_n`;
- `F_n` has no nonidentity rational deck transformation; and
- two explicit rational points in one fiber give a finite noninjectivity
  certificate for every `n`.

The full proof, scope, and priority caveat are in
[`full_symmetric_monodromy.md`](full_symmetric_monodromy.md). A rendered
version is at [`output/pdf/full_symmetric_monodromy.pdf`](output/pdf/full_symmetric_monodromy.pdf).

## Exact verification

The checker requires Python 3 and SymPy:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install sympy
.venv/bin/python verify.py --max-n 8
```

For each `3 <= n <= max-n`, it checks polynomial cancellation, total component
degrees, the constant Jacobian identity, the inverse polynomial identity, and
the uniform two-point collision using exact rational arithmetic.

The announcement itself also has an independent, dependency-free checker
using a tiny polynomial-ring implementation:

```sh
python3 verify_announced_stdlib.py
```

## Status

This is an archival derivation, not a current paper. Its main theorem is
subsumed by earlier, stronger work. The exact checker and full proof remain
available for provenance. Only the explicit uniform rational collision is
retained in the archived Discovery 03 appendix, and even that narrow novelty
claim remains provisional pending expert review.
