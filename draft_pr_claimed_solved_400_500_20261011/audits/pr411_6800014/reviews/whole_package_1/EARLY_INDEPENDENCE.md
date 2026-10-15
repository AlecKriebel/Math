# Early independent criteria and reconstruction

Sealed before reading any root/peer/component verdict, report, or verification script.

## Prior exposure
The assignment exposed the expected main theorem, target identity, package hashes, and priority warning, but no component conclusions beyond their existence. I read the final theorem/derivation source and independently reconstructed it in a newly authored SymPy program. Native original PR-body inspection was incidentally required by the gate and is historical, not evidence of the proposed complete-body state. No peer/root conclusions or candidate code had been read before this seal.

## Exact target and success criteria
Morgan–Pansu §11 Question 14, printed p.12, asks whether solvsolitons are the only local maxima of F=Scal²/|Ric|² among left-invariant metrics on a fixed solvable group. Its definition is Ric=cI+D with D a derivation of that group's Lie algebra. The candidate suffices only if a fixed simply connected five-dimensional group admits a finite defined non-strict neighborhood maximum in the full positive-definite inner-product cone and the original Lie algebra fails that equation. The asserted comparison metric F=9/17 and Ricci-soliton alternative presentation are secondary claims needing verification. No novelty premise or strict-maximum premise is allowed.

## Reconstruction and attempted falsification
1. Direct Koszul connection/curvature trace in dimension five produced Ric=diag(-u²/2,0,0,u²/2,-u²/2) and F=1/3. The two necessary diagonal-derivation equations are c+u²/2=0 and c+3u²/2=0; incompatible for u>0.
2. An arbitrary full Gram matrix gives an orthogonal complement e0 shifted by a vector of the abelian ideal. This vector has zero adjoint action on the ideal. Its Schur-complement normalization contributes only scalar c; the ideal Gram square root contributes conjugation. All nearby metrics, including cross terms, are covered and continuity preserves the local chart.
3. On the conjugacy orbit, E=I+A² is a smooth idempotent onto the generalized zero space. The explicit p=Ee4, Ap frame construction has nonzero denominators at u0>0. Invariance gives an upper-right zero block, with an unrestricted lower-left block. Trace and determinant constrain C, not L. The Sylvester map Y↦YC−NY is invertible because the spectra are disjoint; independent symbolic solution confirms every L lies in a conjugate orbit, eliminating a hidden block-diagonal restriction.
4. Independently constructed full M gives exactly the displayed s, Q, R with k²=1+a²+b². No slice direction was removed to obtain positivity. The mixed quadratic blocks have determinant 1−4v², and the det/trace lower bound is valid on a fixed compact interval I strictly inside (0,1/2). The cubic bound uses k−1=h²/(k+1) and is uniform in v. The constructive radius c0/100 yields P≥c0ρ²/2 and, by continuous slice coordinates, an actual neighborhood in the full metric cone. The flat family is exact, so no semidefinite-Hessian sufficiency is assumed.
5. Independent seed-6800014 sampling verified the rigorous local bound on 4,000 points in the unrestricted six-coordinate slice for u0 ranging from .01 to .499. This is falsification evidence only; the exact identity/estimate supplies proof.
6. The omitted endpoint u=0 is flat with zero Ricci and undefined F. At u=1/2, the actual same-orbit slice path a=b=y=z=0, w=t, x=−t/2 has P=−t⁴; the local-maximum extension fails. For u>1/2 the analogous path has negative quadratic coefficient. Thus the open interval restriction is material and accurate.
7. Direct conjugacy products verify HA_uH⁻¹=A_1 and T_BA_1T_B⁻¹=B. The comparison has s=3/2,q=8,F=9/17. The original group presentation is part of the target; the Euclidean rotation norm and Heisenberg coframe show the same Riemannian manifold is R²×H3. Its displayed product derivation has central weight equal to the sum of Heisenberg horizontal weights and integrates to automorphisms. This does not repair the original algebraic equation.

## Mechanism family status and exact gaps
- Curvature/derivation and global comparison: independently verified exact symbolic identities; no remaining mathematical gap found.
- Full metric/orthogonal slice/uniform estimate: independently verified deductions and exact expansion; no remaining mathematical gap found.
- Boundary attack: endpoint counterexample found, but outside the claim and confirms its restriction.
- Priority/attribution, entire historical/package code, all manifests/ZIPs, clean reproduction, PDF render, full source context, metadata, and proposed full body: not yet reviewed. No whole-package verdict exists at this checkpoint.
