# Surface and finite-encoding family — 21.127

As of October 24, 2026 UTC. **No complete solution of 21.127. No preprint or publication claim.** Best-guess completion toward the full mathematical target: 8%, reflecting useful local mechanisms but large unresolved encoding and realization gaps. This estimate is heuristic and may decrease.

The target is rationality of scl for arbitrary commutator-subgroup elements of arbitrary RAAGs. The work concentrated on the minimal path P4 and did not assume that selected chains, fixed gluing graphs, or congruence approximations settle that target.

## Strongest checkable results

1. `FIXED_GRAPH_FLOW.md`: a proved integral-flow criterion for a fixed graph of coordinate-torus pieces. For each generator coordinate, a component with no annular reservoir must have zero total fixed charge. The condition is sufficient by an integral spanning-tree construction. Each reservoir has an explicit extra inner boundary loop; nonzero homology is never absorbed by genus.
2. The same note proves an iff criterion for promoting all but o(m) target pieces to disks in degree-m covers: every all-target TREE component in every coordinate must have zero charge. Non-tree components can concentrate winding in one annular exception per long lift, using residual finiteness of a free group. Charged tree components cannot be repaired by taking covers.
3. The P4 8-cycle example has globally zero total charge and every piece separately adjustable, but forces at least 2m exceptions in every m-cover. Its two outer boundary labels can be taken as [ab,d] and [d,a]. Killing a,c sends the boundary chain to [b,d], so any claimed annular or asymptotically zero-cost realization is false. This is a mechanism counterexample for a chain, not irrationality of an element.
4. `P4_FIXED_GRAPH_OPTIMIZATION.md` refines this to an exact finite optimization for ONE fixed P4 gluing graph. After forced a/d exceptions, the persistent bad b-tree/c-tree components form a bipartite incidence graph. The stable exception loss is the number of those components minus its maximum matching, plus the forced exceptions. The remaining cyclic losses can be o(m). This is a matching program for local relative disk loss, not an absolute-scl program.
5. `FINITE_CONGRUENCE_OBSTRUCTION.md`: treating arbitrary finite winding congruence as an actual disk criterion fails on the SAME word [b,d]. If b^N is incorrectly cappable, an explicit (N+2)-holed sphere becomes an N-holed sphere, giving the false original-group upper bound 1/2-1/N. The original RAAG value is 1/2 by its free retract. No exact quotient optimum or convergence of relaxed optima is claimed.
6. `EXACT_CHAIN_CERTIFICATE.md` strengthens the two-boundary countermodel to the exact value scl([ab,d]+[d,a])=1. It uses an actual annular pairing for the upper bound and an explicit free-group homomorphism for the lower bound. The separate addendum passed a fresh delta audit in `review/DELTA_EXACT_CHAIN_AUDIT.md`, including independent character-word reductions and a second upper construction using disjoint punctured tori.
7. `FORMAL_LANGUAGE_GAP.md`: effective EDT0L descriptions of individual RAAG equations do not by themselves yield rational stable optimization. The finite endomorphism system A->ABA, B->AB gives ratios F_(2n+1)/F_(2n) decreasing to the irrational golden ratio, even after closing its count vectors under addition. This is an abstract countermodel to an inference, not a RAAG genus spectrum. The 2016 equation-description theorem and a new April2026 quadratic-periodicity theorem were inspected within their actual scope.

## Verification

The first three local results and the finite-congruence sphere received a fresh independent adversarial audit in `review/AUDIT.md`. One misleading sentence about convergence of relaxed optima was repaired; no substantive objection remained. The reviewer independently checked 18,888 incidence systems, 400 arbitrary permutation-voltage covers, sphere identities through N=150, and the elementary finite-endomorphism countermodel. The author's checks are in `CHECKS.json` and `FORMAL_LANGUAGE_CHECKS.json`.

The matching refinement passed a separate fresh delta audit in `review/DELTA_MATCHING_AUDIT.md`, with 2,000 independently checked defect minima (including 1,000 exact forest minima), 400 arbitrary cover scalings, a no-private-singleton case, and cyclic nonattainment examples. Author verification reproduced 250 fixed-forest optimization cases against exhaustive exception selection, 250 arbitrary cover-scaling cases, and 40 cyclic nonattainment examples (`P4_OPTIMIZATION_CHECKS.json`). These finite checks corroborate the proofs and do not replace them.

No human peer review, formal proof assistant verification, or originality certification was performed. None is implied by the independent AI review.

## Exact obstruction to a full finite program

The graph of pieces is not fixed when minimizing scl for one boundary word. It can have arbitrarily many polygons, and different coordinates have different overlapping component decompositions. The fixed-graph theorems do not bound these types or prove a semilinear/rational-polyhedral description of their joint boundary language. A finite program requires a proof that a finite representation attains the correct lower envelope over ALL such graphs, not just a search over selected examples.

Also, the surviving annular reservoirs have additional interior boundaries. A separate globally valid filling/gluing construction with the required asymptotic Euler cost is needed to turn the relative model into an admissible surface for the original element. Vanishing scl in the vertex tori does not permit filling a chain with nonzero vertex homology.

The word-equation route can decide fixed genus/exponent cases but has neither a uniform two-parameter finite-state encoding nor a rational-slope theorem. Finite endomorphism control alone is inadequate, as the explicit irrational-infimum countermodel shows.

These routes are blocked at the named mechanisms, not by lack of numerical evidence. Reopen them upon a genuinely new finite-generation/encoding theorem or an actual absolute surface-realization construction. The full 21.127 solution and publication gates remain closed.

## Reproduction

From this directory, standard Python 3 is enough:

    python3 check_flow.py
    python3 check_p4_optimization.py
    python3 check_formal_language.py
    python3 check_exact_chain.py

The primary-source provenance is in `SOURCE_MANIFEST.json`; raw PDFs/text are local source cache, not new mathematical findings. All work is isolated in this problem-specific folder. No external people were contacted and no git or publication operation was performed by this family.
