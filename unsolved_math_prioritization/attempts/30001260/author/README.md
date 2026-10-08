# Rank-one-isotropy actions of S5: five partial approaches

Problem 30001260 / OWR-3477-004; queue rank 970. Author packet dated 2026-10-07.

## Disposition

**Unsolved after five mathematical author approaches.** There is no construction of a smooth sphere action and no nonexistence proof in this packet. All five approaches below stop at an explicitly identified obstruction or gap. The packet is prepared for an independent audit, not presented as accepted or peer reviewed.

The target is whether some standard smooth sphere supports an S5 action whose point stabilizers contain no elementary abelian subgroup of rank two. Trivial stabilizers are allowed. If H is finite, rank_p(H) is the largest k with (C_p)^k contained in H, and rank(H) is the maximum over p. Thus “rank-one isotropy” means rank(G_x) <= 1, not that every stabilizer is nontrivial, cyclic, or of prime-power order.

For S5, the only relevant rank-two elementary abelian subgroups are Klein four groups: 9 and 25 do not divide 120, and the 2-rank is two. The exact checks enumerate all 20 Klein four subgroups, of two conjugacy types.

## Source and category control

The 2009 source is Ergün Yalçın's contribution, “Constructing group actions via orbit categories,” joint with Ian Hambleton and Semra Pamuk, in *Manifold Perspectives*, OWR 27/2009. Question 4 is on printed page 1499 (PDF page 13). Its category is smooth actions on spheres.

A current primary source is Hambleton–Yalçın's May 2026 survey, [arXiv:2605.02760v1, Remark 8.2](https://arxiv.org/html/2605.02760v1#S8). It explicitly retains this smooth existence problem. Theorem 8.1 credits their earlier work with Pamuk for the finite-CW result. This provides a dated open-status statement as of that manuscript, not a claim that every later communication has been searched.

The already established result is a finite S5-CW complex homotopy equivalent to a sphere, with cyclic 2-power isotropy; credit belongs to Hambleton–Pamuk–Yalçın, [*Equivariant CW-complexes and the orbit category*, Theorem A](https://ems.press/content/serial-article-files/43319). That theorem is not a smooth-manifold realization theorem. The more general 2016/2017 papers likewise do not turn this packet into a solution.

Keep distinct:

- Orthogonal representation spheres: ruled out here by an elementary reproduction of the known obstruction.
- Smooth actions on the standard sphere: the exact unresolved target.
- Smooth actions on a homotopy sphere: even a construction here would require attention to its smooth structure before claiming the standard-sphere target.
- Locally linear or arbitrary topological sphere actions: different categories; none is constructed or excluded here.
- Finite G-CW complexes merely homotopy equivalent to spheres: the credited existing positive theorem.

The source PDFs, extraction files, corpus contents, and coordination records are absent from this public packet. Only authored mathematics, authored exact checks, and public verification/citation metadata are included.

## Five author approaches

1. `TURN_1_LINEAR_OBSTRUCTION.md`: complete character-theoretic exclusion of all nonzero representation spheres.
2. `TURN_2_FIXED_SET_CONSTRAINTS.md`: necessary dimensions, coincident C2/C4 fixed sets, and orientation/normal-bundle consequences for a hypothetical smooth action.
3. `TURN_3_LOCAL_CHARACTERS.md`: explicit fusion-stable Sylow representations with common complex dimension 12; local compatibility does not yield a smooth global action.
4. `TURN_4_INDUCTION_AND_JOINS.md`: exact failure of ordinary induction from the S4 rotation action, and why joins cannot remove its forbidden fixed sets.
5. `TURN_5_THICKENING_AND_SURGERY.md`: conditional thickening construction analyzed by integral duality; the boundary has two extra homology groups that must be removed equivariantly.

These are mathematical attempts, not five retrieval or packaging operations. They carry no novelty claim. The representation obstruction and local-to-global finite-CW context are already in the literature; other elementary consequences may also be familiar.

## Verification

Run `python checks.py --self-test` from any working directory, using the absolute script path if needed. `CHECK_RESULTS.json` is the captured output. Normal and optimized Python outputs agree. The script builds S5 from permutations, constructs actual characters, checks their completeness, enumerates the forbidden subgroups, checks normalizers and fusion, and verifies induction through its defining character sum. A bounded dimension-equation check is a diagnostic of the written symbolic proof, not a proof by bounded search. The thickening checks verify degree arithmetic only.

`verify_packet.py` checks exact inventory, byte counts, hashes, and replays the mathematical checks in normal and optimized Python. It must be supplied the manifest digest recorded outside the archive. The manifest is not an independent signature. Neither script certifies Smith theory, Borel's theorem, Poincaré–Lefschetz duality, smooth realizability, or scholarly-source authenticity.

## Exact remaining problem

Produce a nonlinear smooth S5 action on a genuine sphere avoiding every Klein four fixed set, or find a further smooth obstruction applying to every possible dimension and permitted rank-one stabilizer. The necessary constraints and failures of specific constructions in this packet do not settle this disjunction.
