# Final author result: Kourovka21.9

**Original unresolved, five of five substantive turns.** Author search is stopped; independent full source/proof review is pending. No full resolution or historical novelty is claimed.

## Exact target

Y. Barnea asks whether every nonabelian finite-rank free pro-p group F admits a finite family of open subgroups, including F, whose only common contained characteristic subgroup is1. The current October2026 Kourovka21st edition leaves Problem21.9 unannotated on printed177. The same question remains Question4 on p53 of Barnea–Ershov–Le Boudec–Reid–Vannacci–Weigel, arXiv:2507.04120v3,22September2026. The paper explicitly separates it from its discrete-free-group results and its finite-individual-automorphism question.

The arbitrary/closed subgroup and abstract/continuous automorphism readings are reconciled in Turn2 by the credited strong-completeness theorem and taking closures. No source quantifier is silently discarded.

## Five scoped directions

1. A common characteristic subgroup for F and any index-p subgroup U lies in the closed derived subgroup of U. More generally the obstruction holds whenever the inclusion image U_ab->F_ab is not a scalar lattice. The proof treats actual images of possibly nonclosed subgroups. Such a common subgroup cannot be open or contain a nontrivial power of a primitive element. All index-p choices lie in one Aut(F)-orbit and impose the same condition once characteristicity in F is required.
2. Cyclic characteristic-core descent through a fixed family has an exact maximal common characteristic limit. Every step is open and can be computed in a suitable finite Frattini quotient, with the full automorphism lifting step proved. The initial index-p descent is U -> Phi(F) -> Phi(U). Its cycle indices grow strictly, but triviality requires cofinality at every Frattini depth; no convergence theorem is claimed. A finite family from a characteristic chain cannot work.
3. Explicit iterated commutators have nonzero Schreier abelianization at every lower-central depth. In a p-cycle block the minimum coefficient valuation of (S-1)^k e_0 is floor((k-1)/(p-1)). Hence no common characteristic subgroup can contain a finite lower-central term, and its quotient cannot have finite nilpotency class. A fixed modulus eventually hides the nonzero witnesses. This does not exclude arbitrary deep characteristic subgroups.
4. The credited pro-p Hall theorem, together with an explicit finite-wreath separating quotient, shows that a nontrivial normal subgroup of F cannot be confined to any closed finite-rank infinite-index subgroup. Any nontrivial common characteristic survivor must have infinitely generated closure. Finite normal generation, including what a finite quotient presentation would supply, does not close this gap.
5. Complete comparison classifications expose a lifting failure. In Z_p^d, d>=2, a family has a nonzero common characteristic subgroup exactly when all its open lattices are scalar. In the p-adic Heisenberg group every finite open-subgroup family has a nonzero common characteristic central subgroup; nevertheless its mod-p finite quotient has a two-subgroup family with trivial common characteristic core, for every prime. **These comparison groups are not nonabelian free pro-p groups and are not source counterexamples.** The extra finite-quotient automorphism that cannot lift is explicit.

## Exact remaining gap

No finite family has been shown to force its entire common characteristic core to1. Nor has a nontrivial common characteristic subgroup been constructed for every finite family. The possible infinitely generated common core is not eliminated by primitive-element tests, finite-class quotients, finite-rank searches, growing indices, or successful finite-quotient analogues.

## Reproducibility and scope

All five standard-library Python receipts replay exactly:75,293;837;11,101;614;51,455 assertions, total139,300. These are bounded exact supplementary controls, not exhaustive computations in an infinite free pro-p group. The universal results have written proofs with external inputs credited precisely.

Run `python REPLAY_ALL.py` from any location. It verifies the historical manifests, all five receipts, and the final manifest when present. Optional `--source-dir /absolute/path/to/sources` checks locally held source bytes. Source PDFs/PNGs, raw imports and inventory logs are excluded from the public whitelist. The scripts require only Python's standard library.

Historical state files and the first-turn research log remain unchanged; this final wrapper records the current five-turn status. Final subjective progress toward the original problem:20%, neither a correctness probability nor a completeness assertion.
