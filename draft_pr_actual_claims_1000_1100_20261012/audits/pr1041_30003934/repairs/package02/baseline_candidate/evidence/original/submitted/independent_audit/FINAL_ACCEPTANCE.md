# Final independent acceptance

Date: 2026-10-09.

Verdict: **ACCEPTED for the stated target. No unresolved mathematical blocker remains in the audited proof.**

This verdict is bound to the following exact manuscript:

- File: `PROOF.md`
- Bytes: 13,596
- SHA-256: `5392acc347fe0eaf8597ac619341b2946d21781e6118676248a4ee83baad6c1b`

The independently audited result is coNP-completeness of deciding uniqueness of the mixed-strategy equilibrium pair in explicitly encoded rational, variable-dimension bimatrix games with `rank(A+B)=1`, without a nondegeneracy promise. The hardness construction has a known strict pure equilibrium, with a second equilibrium if and only if the input PARTITION instance is yes.

The final frozen manuscript incorporates every correction requested by this audit:

1. The ternary cost perturbation preserves all strict residual-path comparisons, so its SSP run is a permitted original-cost run. The primary source imposes no special SSP tie rule. This closes the selected-path versus all-optimal-flow issue.
2. The generic-cost statement concerns nontrivially projected simple residual cycles, excluding formal cancellation two-cycles. The distinct-optima argument uses a sign-conformal decomposition and optimality's nonnegative-cycle property.
3. The uniform exact-penalty argument establishes an optimal dual vertex through pointedness and the optimal face, and gives a polynomial-bit determinant bound. It rules out every infeasible minimizer, with no nondegeneracy assumption.
4. The simplex representation is injective, all candidate parameter values are covered, and the yes witness lies strictly below the upper embedding boundary.
5. The negative-parameter argument proves uniqueness of both strategies at the strict default pair; exact rank one, payoff signs, and both directions of the zero-sum equivalence check out.
6. The graph dimensions, output dimensions, and binary encoding bounds are polynomial. The maximum flow value is correctly distinguished from the largest arc capacity.

The primary network formulas and orientations were checked against the PDF figures and source proof, not only against extracted text. The complete derivations and explicit accepted/rejected claims are recorded in `AUDIT.md`; its initial conditional verdict describes the earlier manuscript and is superseded by this hash-specific acceptance.

The exact-arithmetic verification script was also inspected and independently rerun. All 6 original full-game checks and 39 network checks reproduced exactly. Four additional full-game cases passed. Those tests are supplementary; universal correctness is supplied by the mathematical proof. Rerun details are in `exact_rerun.json`.

Scope limits: this does not establish hardness under a promise that the full game is nondegenerate. It is an independent audit within this research task, not a claim of external peer review or publication. No publication or queue action was performed by this auditor. Any material manuscript change requires renewed hash-specific review.
