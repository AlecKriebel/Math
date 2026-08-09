# Archival technical precursor: the 22/44-variable construction

> **Status update, 22 July 2026.** Discovery 07 is now the repository's
> canonical consequence paper. It incorporates this 22/44-variable
> construction and strengthens the quartic conclusion from collision-based
> nonvanishing to a closed every-order formula. This directory, its PDF, and
> its original timestamps remain unchanged as a technical precursor and exact
> certificate source.

> **Priority refresh, 9 August 2026.** The earlier Cassidy, Thompson, and
> Mikhail Szh predecessor findings were reconfirmed. Those components are
> externally preempted; no earlier source was found for the residual executed
> 22/44-variable certificate. See `PRIORITY_AUDIT.md`.

This package accompanies the provisional note:

> **An explicit 44-variable vanishing witness from a 22-variable cubic Keller
> map**

Author: **Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol**.

This was the consolidated paper for Explorations 01 and 02. Those archival
derivations remain available, the useful 13-variable reduction is incorporated
here, and the surviving uniform rational collision from Exploration 01 is
included as Appendix A. Discovery 07 now incorporates the parts of this
construction needed for the unified inverse-series theorem.

## Verification status

I am a complete amateur and cannot independently verify these claims. This is
an experiment in the limits of AI-assisted mathematics, not an established
result. The package has passed exact automated checks, but every theorem,
proof, attribution, and novelty statement requires independent expert review.

## Claimed outputs and corrected priority

1. A degree-eight potential in six variables over `Q(i)`, with 204 expanded
   terms, whose gradient is an identity-linear noninjective Keller map with
   symmetric Jacobian and determinant one. The three-point collision is
   explicit over `Q(i)`. This is a normalized presentation of the classical
   Meng/de Bondt--van den Essen lift, not a new discovery. A post-release audit
   found that Eliott Cassidy's repository had already executed the equivalent
   six-dimensional transport on 20 July 2026.
2. A 22-variable cubic homogeneous noninjective Keller map with nilpotent
   nonlinear Jacobian, obtained from a rank-compressed homogenization of the
   certified 13-variable stable model.
3. A 44-variable homogeneous quartic Hessian-nilpotent polynomial with 538
   expanded terms and an exact collision under `Z - gradient(P)`, explicitly
   witnessing failure of Zhao's Vanishing Conjecture.
4. An appendix giving a uniform rational two-point collision in one explicit
   weighted-lift specialization for every degree `n >= 3`. The broader
   monodromy theorem is credited to earlier work and is not claimed as novel.

William Thompson had priority for the rank-compression idea and published a
sparser 24-variable cubic map before this note. The candidate residual
contribution is narrower: a different construction with 22 ambient cubic
variables, followed through to the explicit 44-variable quartic certificate.
Nothing in this package is logically independent of the original
three-dimensional counterexample. See `PRIORITY_AUDIT.md` for source-specific
details and timestamps.

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

With Node.js, using an independent BigInt implementation:

```bash
node verify_exported_node.mjs
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
- `verify_exported_stdlib.py` — dependency-free Python certificate checker.
- `verify_exported_node.mjs` — independent JavaScript BigInt certificate checker.
- `PRIORITY_AUDIT.md` — corrected comparison with earlier public artifacts.
- `../discovery_01_symmetric_monodromy/verify.py` — exact checker for the
  appendix's weighted-lift collision.
- `output/` — expanded sparse polynomials and exact collisions.
- `search_*.py` — retained exploratory and negative-result scripts.
