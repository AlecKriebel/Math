# Symmetric monodromy in an Alpoge-Gallagher subfamily

**Byline:** Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol.

This workspace contains a provisional research note and an exact symbolic
checker prompted by the polynomial counterexample to the Jacobian conjecture
announced on 19 July 2026.

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

This is a research draft, not a peer-reviewed publication. Its residual
contribution is deliberately narrow: the elementary subfamily, its uniform
rational collision, and the all-degree `S_n` statement with trivial rational
deck group. Searches performed on 20 July 2026 found the newly posted
every-degree construction and a separate analysis of `S_3` monodromy for the
original cubic example, but did not find this uniform refinement. That is
evidence of novelty, not a priority guarantee. An expert in affine algebraic
geometry should review the monodromy argument before submission.
