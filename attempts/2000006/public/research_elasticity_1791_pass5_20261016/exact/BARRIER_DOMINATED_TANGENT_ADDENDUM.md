# Exact addendum for barrier dominated weighted tangents

16 October 2026. Final shared pass only. This independently certifies the barrier-dominated extension in `counterexample/DEGENERATE_TANGENT_OBSTRUCTIONS.md`, finalized after the main exact certificate. It leaves the sealed main report and its 201 exact checks and 14 quadrature comparisons unchanged. E-6322 remains unresolved.

## Exact normalization

Use the notation of Section 5 of `FINAL_EXACT_CERTIFICATION.md`, but assume

\[
s+3m>6,\qquad \gamma=s-3>0,
\]

and only a C¹ angular profile. Strong W¹,∞ annular convergence and a nontrivial limiting determinant are still explicit hypotheses. For D_r=diag(r^(α_i−1))=r^(m−1)L_r, degree-six homogeneity gives

\[
r^{2\gamma}W(D_rP)
=r^{2(s+3m-6)}H(L_rP)+d(\det P)^{-2}.
\]

The positive exponent follows from 2γ+6(m−1)=2(s+3m−6). On bounded matrix sets, L_r is uniformly bounded and H(L_rP) has uniformly bounded first derivatives. Thus its stress vanishes after multiplication by the displayed positive power of r.

Strong gradient convergence preserves J_U≥0. Its nontriviality and continuity supply a positive patch. On any compact subset of that patch, the approximating determinants are bounded below, so the componentwise physical variations described in the main certificate justify the full limiting system

\[
\operatorname{div}[J_U^{-3}(\operatorname{cof}DU)_i]=0,
\qquad i=1,2,3.
\]

No second derivative of U is used here.

## Local target chart calculation

At any point with J_U>0, the C¹ inverse function theorem supplies a local chart X=U(z). Fix one row i and χ∈C_c∞ in that target chart. The test ψ(z)=χ(U(z)) is C¹ with compact support in the source chart; approximation in C¹ allows its use in the weak equation, whose coefficient is continuous and locally bounded.

Writing F=DU and J=det F, the cofactor identity gives

\[
\begin{aligned}
0&=\int J^{-3}(\operatorname{cof}F)_i\cdot D(\chi\circ U)\,dz\\
 &=\int J^{-3}J\,\partial_{X_i}\chi(U(z))\,dz\\
 &=\int J(U^{-1}(X))^{-3}\partial_{X_i}\chi(X)\,dX.
\end{aligned}
\]

Thus every distributional target derivative of the continuous function J∘U⁻¹ raised to power −3 vanishes. It is constant in each connected local chart. Consequently J is locally constant on its positive set.

Homogeneity contradicts this immediately. For any positive-J point z and t sufficiently near one, the short radial segment stays in its local positive chart, whereas

\[
J_U(tz)=t^\gamma J_U(z),\qquad \gamma>0,
\]

is strictly nonconstant. Therefore no such tangent exists.

## Exact scope

This rules out the barrier-dominated range s+3m>6 under strong W¹,∞ annular convergence, C¹ angular profile and nontrivial limiting determinant, including profiles initially allowed to have angular zeros. It requires neither an axis preimage nor a positive-degree argument. Together with the main certificate, the corresponding C²-profile ranges now excluded are barrier-dominated, balanced, and the specified simple-minimum subcritical case with dense positive set.

The argument supplies no tangent existence, no exclusion of determinant-identically-zero leading profiles, no general subcritical coupled system theorem, and no boundary degeneration theorem. It is an independent analytic check of a conditional exclusion, not a computation establishing global minimization or a solution of the frozen benchmark.
