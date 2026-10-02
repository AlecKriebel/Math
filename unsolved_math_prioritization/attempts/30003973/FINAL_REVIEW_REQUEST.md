# Full independent five-turn review request

Audit the complete frozen packet for30003973 / OWR-16627-005. Original unresolved5/5. No sixth author search or new result is requested. Preserve all frozen author bytes, and return a scoped PASS or FAIL with required corrections and exact source/dependency limitations.

## Source scope

The exact primary question is Question6, printed p2736 of OWR44/2018. Read the whole Clemens contribution, pp2734–2736, and the source definitions. The problem concerns equality of all finite q-Ramsey host classes, equivalently minimal families, using ordinary subgraph copies and arbitrary edge colorings. It is not equality of numerical Ramsey numbers, an induced-copy condition, a vertex-color problem or just agreement on bounded hosts. Disconnected targets and isolated vertices are included. SOURCE_MANIFEST.json binds four local PDFs in sibling sources/. The exact overlapping record30004035 is noted.

The prior literature gives even/additive transfer and nested-target transfer. These are credited. The2024 sender paper treats asymmetric tuples of cliques and is not a solution for arbitrary targets. No long external sender construction or distinguishing-parameter proof is presented as independently recertified.

## Adversarial obligations

- Turn1: verify the all-host padding identity, core extraction by host isolates, cutoff max{h,r_q(F)}, Ramsey-number monotonicity and edgeless boundary. The P3 versus P3 plus an isolate example has the reverse direction only.
- Turn2: verify downward-family multiplication and fixed spanning vertex sets; the mixed-product condition must remain an extra assumption. Audit the asymmetric Ramsey implication, the two crossed hosts, the every-recoloring quantifiers, target incomparability and edge-count bounds. The five-element example only refutes automatic mixed inclusion and has equal cubes.
- Turn3: independently expand the seven-element facet certificate, verify common squares and unequal cubes, and check the direct cover-number argument. Its minimal nonfaces have different cardinalities. Audit why a single graph-copy avoidance family has uniform minimal forbidden edge count; do not promote the abstract example to a graph counterexample. No minimality-of-seven claim relies on a numerical infeasibility report.
- Turn4: check componentwise embedding for stars including K2, all threshold quantifiers, the necessity and constructive sufficiency of the quota inequality, the lattice-downset/max-plus translation and canonical-host statement. This characterization is restricted to star-forest hosts. Verify all-host rigidity for star and matching cores separately, using their explicit Ramsey witnesses and Turn1.
- Turn5: check the two-color triangle capacity list and extended threshold criterion. Reconstruct the all-q restricted-profile identity, all ten sharp inequalities for the53-vertex,45-edge host, the H'-avoiding coloring and every edge-deletion certificate. Ramsey-minimality requires no isolated host vertices and monotonicity. The two targets are already2-nonequivalent, so this is a rejected candidate, not an answer to the original implication.
- Check final scope and absence of novelty claims. All five turns are substantive, but none closes the original universal implication.

## Replay and integrity

From the frozen directory run python verify_turn1.py through python verify_turn5.py. Each script is standalone standard-library Python and should reproduce its TURN_n_CHECKS.json byte-exactly. Turn3 reads TURN_3_CERTIFICATE.json; Turn5 reads TURN_5_CERTIFICATE.json. The optional build_turn5_certificate.py is a deterministic standard-library generator; run it only in a disposable copy and compare its generated certificate to the frozen one. SciPy/HiGHS was used for discovery of the Turn3 abstract example but is not a verification dependency.

Verify TURN_1_MANIFEST.json through TURN_5_MANIFEST.json and FINAL_FROZEN_MANIFEST.json, plus source hashes. Raw sources, search scratch files, the optimizer model, private queue data and local receipts are excluded from the public packet. Reconstruct meaningful independent controls, especially for the star-forest and star/triangle threshold lemmas, rather than relying only on author output. Review artifacts must remain separate from the author packet.
