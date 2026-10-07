# Verification scope

The proof's homotopy-theoretic arguments are written arguments depending on cited results. The finite programs check only the claims described here. They do not prove linking-system existence/uniqueness, the mapping-space theorem, Postnikov convergence, or general obstruction vanishing.

## Complete finite fusion calculation

check_fusion.py uses explicit permutations and exact integer operations. It constructs S=D8 from two generators, enumerates its ten subgroups, and constructs the ambient groups D8 (8 elements), Sigma_4 (24 elements), and A_6 (360 elements). The parity-twist inclusion is tested on every pair of Sigma_4 elements.

It generates every homomorphism D8→D8 from the presentation, verifies the homomorphism identity on every pair, and obtains 36 distinct maps. For each of nine ordered ambient pairs it tests the equation for every source morphism P→S against all target conjugators. This is a whole-subgroup test, not an element-conjugacy proxy. The output lists every passing map and its extension mechanism. The source and target in this calculation are only these three specified systems.

The same complete morphism data determines all strongly closed subgroups and the hyperfocal subgroup by all odd-order local automorphisms. It separately confirms four source fusion automorphisms for Sigma_4 and eight for A_6, including inverse fusion preservation where used.

## Exact obstruction-method controls

check_obstructions.py:

- Computes normalized cochain matrices for H^2(C_p;F_p), p=2,3,5,7, with trivial action. Gaussian elimination proves dimension one and that the carry cocycle is not a coboundary. The full cocycle equation and telescoping witness are checked.
- Enumerates all linear forms on F_p^n for p=2,3,5 and n=p or p−1. Adjacent-transposition invariance forces constant coefficients. Divisible n kills their restriction to the diagonal; prime-to-p n admits a retraction.
- Checks the cyclic periodic-resolution H^1 and H^2 formulas on all one-dimensional F_p modules, p=2,3,5,7 and coprime group orders 1≤m≤8. This illustrates the averaging mechanism; the written proof supplies the result for arbitrary finite p'-groups and all higher homotopy modules.

## Replay and negative controls

verify.py validates manifest member hashes/sizes and rejects missing, extra, symlinked, or altered packet members. It executes each checker with the current interpreter and compares the complete bytes against the frozen JSON output. Ordinary and optimized Python invocations reproduce the same results. A relocated copy is checked as well. Deliberately changed result data, a changed proof byte, an extra member, a missing member, and a rebound mutation replacing the asserted 36 endomorphisms by 35 are rejected. The last mutation updates the manifest to reach the mathematical checker itself; it is not merely a checksum failure. A rebound carry-cocycle mutation must also fail after reaching the algebraic checker.

These controls demonstrate the documented replay/integrity boundaries; they are not adversarial mathematical peer review. No source PDF, extraction, screenshot, imported dataset row, or private coordination record belongs to this packet.
