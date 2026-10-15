# Weak pentagon: second-round restricted results and acceptance

12 October 2026 UTC. Problem 3209 / OPG434, queue row 1752. Proposed repository sibling: `unsolved_math_prioritization/attempts/3209_weak_pentagon_round2_20261012/`.

**Accepted partial results; no full resolution and no novelty claim.** This is the second confirmed continuation round. The earlier lifetime total is unknown; no larger total is inferred. No later-round result is included.

## Results

- Every cut complement of size at most two in a finite simple triangle-free graph extends to the specified cube/antipodal Clebsch class, without a degree or matching assumption.
- Every matching cut complement of size at most three in a triangle-free subcubic graph extends.
- Every one-sided matching cut complement in a triangle-free subcubic graph extends, with no size bound, using the explicitly cited signed degree-choosability theorem.
- An authored 15-vertex graph of maximum degree eight has a unique global maximum cut up to side exchange with three matching complement edges, but no homomorphism to any loopless triangle-free graph of maximum degree at most seven. It is not a cubic counterexample.
- For a matching cut complement in a simple triangle-free cubic graph, three-stability and four-stability are equivalent to the cut-induced graph on matching endpoints having maximum degree at most one. The sharp local bound is |M|≤3n/8. A necessary five-switch restriction implies |M|≤n/3, with no converse or sharpness claim.
- No cubic completion injectively retaining the specified 19-edge obstruction core and all edge statuses can make that prescribed cut globally maximum. This leaves redesigned or simulated cores outside the claim.
- Audited constructed samples contain 33,400 positive graph–cut records and 33,386 distinct labeled graph–cut pairs. Exactly the 1,600 pentagon-family prescribed cuts have the family-wide global-maximum certificate. The other 31,800 records carry no general global-optimality claim.

## Reading guide

1. [Small-complement proofs](SMALL_COMPLEMENT_PROOFS.md), including the complete grid lemma and signed reduction.
2. [High-degree addendum](HIGH_DEGREE_ADDENDUM.md), with its full unrestricted target-degree argument.
3. [Switching proofs](SWITCHING_PROOFS.md), including the sharp 16-vertex example and sealed-core barrier.
4. [Small-complement acceptance audit](SMALL_COMPLEMENT_AUDIT.md) and [switching acceptance audit](SWITCHING_AUDIT.md), preserving the substantive independent reasoning.
5. [Signed-dependency audit](SIGNED_DEPENDENCY_AUDIT.md), with the exact external contract, saturation analysis, and both brick exclusions.
6. [Additional explicit examples](ADDITIONAL_EXAMPLES.md), [reproduction scope](REPRODUCTION_SCOPE.md), and [source metadata](SOURCES.md).
7. [Edition acceptance report](ACCEPTANCE_REPORT.md) and the closed [public manifest](PUBLIC_MANIFEST.json).

## Evidence and distribution boundary

The original symbolic checker used assertions: its optimized runs are not semantic verification, and its missing-catalog branch is not accepted as completed checking. The independent checker used explicit exceptions and rejected 32 negative controls in normal, -O, and -OO modes. The original switching checker required an independent integrity wrapper; that independent suite rejected 18 negative controls in all three modes.

This edition distributes complete authored mathematical prose, substantive audits, small explicit authored graphs and vectors, permitted public dataset/PDF metadata, and the edition's manifest. Programs, raw collections, logs, control artifacts, copied sources, private coordination, and their operational identities are excluded. Exact original full-run replay is unavailable from this prose edition alone. The public manifest's hashes identify only actual distributed files; other public hashes identify only public datasets or scholarly PDFs.

The one-sided theorem's external dependency is explicit. No finite experiment proves the unrestricted weak pentagon conjecture or the all-global-maxcuts strengthening, and no exhaustive literature-status claim is made.
