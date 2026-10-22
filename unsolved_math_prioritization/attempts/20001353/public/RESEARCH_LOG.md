# Research record and early stop

## Source and duplicate gate

Recovered the original open-ended examples request before using the catalogue's pair-stabilizer title. Checked the pinned original/clean fields and prior proof, tested the original and AIMPL URLs, read the official workshop context, and distinguished a braided-conjugacy PR from this task. The existing pair result is credited.

## Substantive proof attempt 1: invariant-equivalence collapse

Goal: extend from pairs to all nonempty finite dyadic subsets, without classifying the rapidly increasing number of circular orbitals.

The key step is to start with two distinct equivalent k-configurations A and B, move one point in A\B a short dyadic distance while fixing all other points of A∪B, and use invariance to force a local one-point-slide equivalence. Every such undirected slide has the same finite circular pattern. The graph of these slides is connected: cut away from both configurations, put k auxiliary points before them, and move coordinates left one at a time. Therefore the equivalence relation is universal.

PROOF.md gives the full finite-extension construction, the edge-orbit argument, the explicit length-at-most-2k connecting path, and the coset-equivalence proof of maximality. It also gives the exact index, a split F^k ⋊ C_k description using k dyadic partition intervals (not the generally nondyadic evenly spaced points i/k), and the finite-order invariant separating every k.

Attempted falsification covered: k=1; k=2; the two orientations of a local slide; preservation of the other configuration; wraparound in the circle; correct membership in T, including dyadic preservation for maps with no breakpoints; non-power-of-two k; exact torsion order; and the crucial pointwise/setwise distinction. None produces a counterexample to the stated theorem.

## Why no attempts 2–5 were spent

The all-k construction is proved completely in attempt 1 and is already explicitly announced in the September 2026 source. Additional attempts aimed at the same theorem would duplicate credited work. The task asks for examples, not a classification theorem. Accordingly, this is an early completion of a concrete example-producing answer, with **1/5 substantive author attempts**. It is not a claim to have exhausted all possible new maximal-subgroup constructions.

The recommended queue interpretation is **already_solved / 1/5 for the example-supplying construction**, provided that the entry's open-ended scope is stated prominently. The conservative equivalent prose disposition is “known examples supplied; no novel theorem; classification remains outside scope.” Final classification is subject to the independent mathematical/source audit and the parent publication gate.

## Verification

Run `python check_exact.py` from this directory. Its standard-library Fraction arithmetic reproduces exact_results.json: 59,629 assertions, including 3,984 configuration-pair paths on the eight-point dyadic grid for k≤3, 75 varied circular extension examples, and cyclic complements for 1≤k≤16.

These are small representative arithmetic and configuration diagnostics. The universal group-theoretic claims rest on the written proof, not extrapolation from the finite checks. No formal proof-assistant certification or external human peer review is claimed.
