# Independent supplement: KS angular balance is SL(2)-minimality

This mechanism was raised by the root reviewer after the initial reconstruction. I independently verified every step. It resolves an interpretation issue in the package, without changing the validity of either displayed theorem.

Fix a finite seminorm s and set J(A)=I_avg(s composed with A), for all real 2 by 2 matrices A. A seminorm is convex; its square is convex because the squaring function is convex and increasing on nonnegative reals. Therefore each A -> s(Av)^2 is convex, and the circular integral J is convex. Near I in GL+(2), J(A)=det(A) F_s(A) is smooth by the manuscript angular-substitution identity. Consequently DJ(I)[D]=T(s):D+I_avg(s) trace(D).

If T(s)=0, the supporting-plane inequality for differentiable convex J gives

    J(S) >= J(I) + J(I)(trace(S)-2).

For positive symmetric S of determinant one, the eigenvalues are lambda and lambda^-1, hence trace(S)>=2. This yields J(S)>=J(I). For arbitrary A in SL(2), take its right polar decomposition A=S R, with S positive symmetric of determinant one and R in SO(2). Circular integration is invariant under the substitution v -> Rv, so J(A)=J(S R)=J(S)>=J(I). Thus s is SL(2)-minimal in the exact energy sense used by Lytchak-Wenger.

Conversely, if J(A)>=J(I) for all A in SL(2), use A(epsilon)=exp(epsilon D) for arbitrary traceless D. Two-sided differentiation gives DJ(I):D=0, hence T(s):D=0. Symmetry and tracelessness of T permit D=T(s), so T(s)=0. Zero and degenerate seminorms are included in this argument; minimality then independently rules out nonzero degenerate seminorms by the older lemma.

Therefore the two conditions are equivalent for KS energy. The old pointwise bound 2 sqrt(2)+sqrt(6) from the inspected LW manuscript Section 3.3 can be applied AFTER the manuscript's own local-domain-variation, global-holomorphic-stress, sphere-vanishing argument. Merely observing different initial variational hypotheses cannot establish that the sharper bound is inapplicable to the conclusion.

The displayed elementary 4+sqrt(17) estimate is still correct and explicitly nonsharp. A repair should state the supplied implication and credit the sharper existing bound; it may retain the elementary proof and its bound as a source-independent quantitative estimate. An earlier exact unrestricted locally KS-minimizing sphere theorem is still not authenticated solely by this pointwise observation, since the global stress-vanishing argument is required. First priority remains unresolved.

Required current-package clarification: manuscript final KS comparison paragraph, and active priority notes that label a stationarity-to-SL(2)-minimality step unsupported or inapplicable. Preserve the sealed historical review, mark the correction as later evidence, and rehash/rebuild current materials.
