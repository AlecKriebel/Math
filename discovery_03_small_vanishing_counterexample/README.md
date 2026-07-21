# Discovery 03: symmetric and Hessian-nilpotent consequences

This package accompanies the provisional note:

> **An explicit symmetric Keller counterexample in six variables and a
> 44-variable vanishing witness**

Author: **Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol**.

## Verification status

I am a complete amateur and cannot independently verify these claims. This is
an experiment in the limits of AI-assisted mathematics, not an established
result. The package has passed exact automated checks, but every theorem,
proof, attribution, and novelty statement requires independent expert review.

## Claimed outputs

1. A degree-eight potential in six variables over `Q(i)`, with 204 expanded
   terms, whose gradient is an identity-linear noninjective Keller map with
   symmetric Jacobian and determinant one. The three-point collision is
   explicit over `Q(i)`.
2. A 22-variable cubic homogeneous noninjective Keller map with nilpotent
   nonlinear Jacobian, obtained from a rank-compressed homogenization of the
   certified 13-variable stable model.
3. A 44-variable homogeneous quartic Hessian-nilpotent polynomial with 538
   expanded terms and an exact collision under `Z - gradient(P)`, explicitly
   witnessing failure of Zhao's Vanishing Conjecture.

The six-variable construction is a direct explicit instance of Meng's
classical gradient lift. The 22- and 44-variable constructions are quantitative
compressions, not logically independent counterexamples to the original
Jacobian Conjecture.

## Reproduce

With SymPy installed:

```bash
python3 export_certificate.py
python3 verify.py
```

With only the Python standard library:

```bash
python3 verify_exported_stdlib.py
```

The second checker reads only the four exported JSON files. It differentiates
the sparse potentials itself, verifies the six-variable identity linear part
and three-point fiber, and verifies the 44-variable two-point collision. It is
not a stand-alone proof of Hessian nilpotence; that property is certified by
the structural reduction checked in `verify.py`.

## Contents

- `symmetric_keller_and_vanishing.md` — human-readable note.
- `symmetric_keller_and_vanishing.tex` — typeset source.
- `construction.py` — exact straight-line constructions.
- `stable_reduction.py` — self-contained 13-variable stable model.
- `compressed_construction.py` — rank-eight factorization and 22D cubic map.
- `export_certificate.py` — deterministic JSON exporter.
- `verify.py` — exact symbolic proof-side verifier.
- `verify_exported_stdlib.py` — dependency-free certificate checker.
- `output/` — expanded sparse polynomials and exact collisions.
- `search_*.py` — retained exploratory and negative-result scripts.
