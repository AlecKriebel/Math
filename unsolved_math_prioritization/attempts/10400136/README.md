# Phase ambiguity of quantum hyperbolic state sums

**Problem:** 10400136 / AMR-103-0136, Ohtsuki Problem 7.21 (Baseilhac–Benedetti).  
**Research date:** 3 October 2026.  
**Author-stage disposition:** unsolved after five substantive approaches; independent audit pending.

The target is to understand the Nth-root phase of H_N(T), and potentially refine K_N(W,L,ρ)=H_N(T)^N using extra geometric structure on a closed oriented 3-manifold with a nonempty link and flat B-bundle. This package supplies no complete solution and makes no novelty claim.

## What was established

- Determinant-one normalization leaves a genuine central-scalar freedom in general; an exact clock/shift countermodel shows why that inference alone cannot work.
- Root selection over parameter spaces has a precise winding-number criterion. A tautological root cover does not itself explain the geometric phase.
- Direct substitution yields explicit local charge/flattening formulas and identifies the global lattice calculation still required. Local phase changes are not asserted to survive a closed state-sum contraction.
- A move-graph descent criterion distinguishes an intrinsic correction from the circular normalization by an arbitrary base state sum.
- The recent phase-unambiguous tangle theory gives an exact peripheral Chern-Simons-root cancellation, but comparison and filling-compatible extension are still missing.

Current sources retain the relevant root ambiguities; the successful non-ambiguous cusped refinements do not settle the original closed-pair question. See [SOURCE_GATE.md](SOURCE_GATE.md) for scope and later-literature checks.

## Files and verification

- [Research log](RESEARCH_LOG.md)
- [Attempt 1: determinant normalization](turn_01.md)
- [Attempt 2: analytic root selection](turn_02.md)
- [Attempt 3: charge and symmetry factors](turn_03.md)
- [Attempt 4: move-calculus descent](turn_04.md)
- [Attempt 5: Chern-Simons transfer](turn_05.md)
- [Exact verifier](check_exact.py) and [results](exact_results.json)
- `FROZEN_AUTHOR_MANIFEST.json`: hashes of the author-stage files

Run with standard-library Python 3:

    python check_exact.py

The code checks 9,668 monomial-matrix products, 9,668 cocycle identities, 5,000 charge cancellations, 2,500 flattening-phase identities, and small graph/cover/peripheral controls. All assertions pass. These are exact diagnostic algebra checks; the code does not compute an actual QHI, build a global triangulation, or certify its move phases.

These are AI-assisted, unrefereed research notes. Generic countermodels reject proposed shortcuts only; they are not counterexamples to Problem 7.21.
