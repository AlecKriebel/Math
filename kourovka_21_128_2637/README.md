# Commensurability of the spherical Artin groups F4 and H4

Kourovka Notebook 21.128 · UnsolvedMath 2637 · queue rank 473

**Status: unresolved after five substantive proof attempts. No full resolution or historical-priority claim.**

The question asks whether A[F4] and A[H4] have isomorphic finite-index subgroups, with no requirement that the two indices be equal. The October 2026 Notebook states this question on printed p196. This package records partial calculations and failed routes; it must not be read as a solution.

## Main reusable calculations

Let G_X=A[X]/Z(A[X]).

1. Rational Euler characteristics are chi(G_F)=-5/12 and chi(G_H)=-7/10. A common torsion-free subgroup would have respective indices (252k,150k). This is a necessary condition only.
2. Explicit torsion-free cyclic covers K_F and K_H have respective indices 12 and 60, Euler characteristics -5 and -42, and exact first rational Betti numbers 3 and 0.
3. An explicitly specified subgroup V of index five in K_H, hence index 300 in G_H, has b1(V)=0. It cannot be isomorphic to any finite-index subgroup of K_F. This rejects one Euler-compatible candidate; it does not classify all index-five subgroups.
4. Both pure central quotients surject onto F2. Hence both original groups have infinite virtual first Betti number and virtually surject onto every finite group. Coarse existential virtual-quotient tests cannot separate them.
5. The full L2-Betti vectors only reproduce the Euler index ratio. A sufficient commensurator torsion obstruction is stated precisely, but its necessary premise remains unproved.

The central-reduction and torsion-classification theorems, reflection-arrangement facts, and L2 theorem are credited prior work. The exact computational deductions are author calculations requiring independent review; no novelty is asserted.

## Reproduce

Python 3.12 and SymPy 1.14.0 were used. SymPy is needed for exact rational row reduction in cover_homology.py; other arithmetic is exact integer or finite-field arithmetic.

Run from this directory:

    python checks/run_all.py

This runs four deterministic checks and compares the generated mathematical results against explicit expected values. It does not prove the cited external theorems or solve the original question. In particular, the degree-300 cover rank modulo 101 certifies rational vanishing because it reaches a separately established characteristic-zero upper bound.

## Files

- attempts/turn_01.md through turn_05.md: the five mathematical attempts, in order, including exact remaining gaps.
- checks/: reproducible scripts and complete small result files.
- SOURCES.md and SOURCE_GATE.md: primary references, exact identity, access limits and scope.
- AUDIT_SCOPE.md: the main points requiring adversarial review.
- status.json: machine-readable honest result classification.

No primary-source PDFs, screenshots, raw catalogue corpus, or private correspondence are included. No result here authorizes publication as a solved problem.
