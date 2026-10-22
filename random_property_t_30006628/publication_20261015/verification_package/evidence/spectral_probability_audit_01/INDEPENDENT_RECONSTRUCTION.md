# Independent reconstruction before prior audits or external theorem bodies

Timestamp UTC: 2026-10-15T07:35:05.344552+00:00

Read only frozen PROOF.md and its SOURCE_MANIFEST metadata; no original INDEPENDENT/SECOND reports, checkers, package verdicts, or other agents' findings read. This memo records the initial reconstruction, not an acceptance verdict.

Target: fixed finite inverse-closed nonidentity alphabets in at least three nontrivial factors, density strictly above 1/3, every length residue, independent cyclically factor-reduced samples with replacement. The triangular formal generators are inverse pairs of non-involutory length-L and possibly length-(L+1) words. Actual factor torsion is allowed through the quotient map, not through formal generator involutions.

For three retained blocks, a fixed link vertex can occur at most once per block position (an occurrence written x contributes endpoints x and x^{-1}, different formal vertices). Thus single-sample degree <=3, three-edge Laplacian norm <=6, and sample matrices—not their three edges—are independent.

If endpoint deletion is uniformly negligible, a corner count has adjacency A[a,c] times a remaining-block completion T_h(b,f). Sum over destination class multiplicity ~lambda^{u-1}r_c r_f, completion ~lambda^{h+1}r_b r_f, then sum_c A[a,c]r_c=lambda r_a and sum_f r_f^2=1. This yields expected degree proportional to N/Z lambda^{ell-t+1}r_a r_b h_t. The row limit after division is Q[t,u] P[a,c] r_f^2, with uneven type frequencies already encoded by h_t and c_tu.

For unequal types Q has spectrum {1,-1/2}; P has spectrum {1} plus (-1,0]. Hence the nonprincipal positive walk eigenvalues can reach rho/2, not zero. Limiting Laplacian gap >=1-rho/2>1/2. The proof's gamma=1/2+(1-rho)/4 is safely smaller than that limiting bound by (1-rho)/4. Fixed-alphabet assumption is essential if rho approaches one.

After expected-degree normalization every sample kills z=barD^{1/2}1, so deterministic restriction to z-perp allows lower matrix Chernoff without claiming an impossible full-space positive minimum. Bound R=6/delta and mean minimum >=gamma give exponent -epsilon^2 gamma delta/12. Actual upper degrees suffice: generalized max-min permits the fixed codimension-one barD-orthogonal subspace, even though actual D differs. A second random-kernel vector would contradict the lower bound after subtracting a constant; connectivity then gives positive degrees.

Pending adversarial checks: retrieve and read exact primary matrix Chernoff theorem (constants/range); exact triangular presentation criterion (finite symmetric formal generators, inverse convention, repetitions/multigraphs, no torsion exclusions); independently enumerate nonuniform alphabets/type endpoint multiplicities and reject deliberately wrong type and degree models; verify there is no hidden cyclic-reduction or repeated-corner restriction. Finite experiments will be labelled evidence only. Boundary d=1/3, two factors (periodicity/rho=1), varying alphabets, and free involutory formal letters are outside the target.
