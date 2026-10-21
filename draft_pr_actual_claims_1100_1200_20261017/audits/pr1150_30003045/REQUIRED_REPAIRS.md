# Required mathematical clarification found in PR1150 review

2026-10-17 UTC. Source input remains byte-pinned historical evidence; this record is not an edit to the PR.

The exponent-two counterexample and universal three-summand exclusion are unaffected. The first auxiliary bullet in COUNTEREXAMPLE.md Section6 claims that replacing b by a square u² in the base gives xi=[s^-1,1+uz) in that base by the same differential calculation. The calculation is not justified there: df=u dz+z du, and du need not vanish. Mere descent of f does not justify the claimed symbol equality. A counterexample to that differential identity alone is not a proof that the two cohomology classes differ, and no such stronger conclusion is claimed here.

Minimal rigorous replacement:

> If b=u² is already a square in the base and beta²=u, then L/F has exponent at most one. In L, du=0 and the original computation gives xi_L=[s^-1,1+uz)_L. Since f=1+uz belongs to the base, xi-[s^-1,f) lies in H₂²(L/F), while [s^-1,f) lies in H₂²(K/F). Thus xi belongs to the sum of the inseparable and separable kernels, and cannot witness failure of the exponent-one splitting theorem. No equality of xi with that single symbol in the base is needed.

This is an operative correction to any new exposition/acceptance relying on the auxiliary claim. Any future paper, verification documentation, acceptance record and PR repair must use the corrected sum-membership statement and distinguish the preserved historical inputs. No new publication decision has yet been made.
