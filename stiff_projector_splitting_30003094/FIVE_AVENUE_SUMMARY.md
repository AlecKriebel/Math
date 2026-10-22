# Five substantive research avenues and the remaining scope

Problem 30003094 / row 1829. Research checkpoint, 20 October 2026.

**Overall outcome: UNSOLVED, five substantive avenues completed (5/5); partial mathematical progress, not a resolution of the original unspecified PDE question.** The five avenues below are mathematical approaches, not a claim that five independent historical sessions occurred. Proofs are in RESEARCH_REPORT.md, SUBCLASS_BOUNDS.md and the supporting STRANG_OBSTRUCTION.md; independent audit is recorded separately.

## 1. Exact cancellation and invariant-subspace structure

Question: does stiffness alone already break direct exact-subflow KSL, and can full-step cancellation be expressed without bounding the backward S stage separately?

Result: homogeneous separable equations Y′=AY+YB are integrated exactly for arbitrary finite matrices A,B. The affine method is also exact when the column space is a fixed A-invariant r-dimensional space containing the forcing columns and the required ranks persist. For right-affine equations the endpoint is exactly the K-endpoint column projection of the exact affine endpoint; for left-affine equations an explicit cancellation identity separates the K part and a compressed-semigroup forcing remainder.

Consequence: standalone instability of the backward S solver is not evidence of inaccuracy of the exact full step. A useful obstruction must exploit how the forcing changes the selected subspace. The endpoint identities are proved at arbitrary rank and corroborated by rank-two tests.

## 2. Right-stiff small-forcing obstruction

Question: can a contractive analytic semigroup and uniformly small normal defect suffice for a stiff-uniform direct-method robust bound?

Result: the rank-one family B=diag(0,−λ), C=ηe₂e₁ᵀ, Y₀=e₁(1,1)/√2 has an exact K endpoint whose direction tends to e₂, discarding the order-one slow e₁ component. With λ=n² and τ=η=1/n the one-step error tends to 1/√2, while the initial error is zero and ε+τ tends to zero. All subflows are exact and finite-parameter QR ranks are nonzero.

Boundary: these exact initial data contain nonvanishing high-frequency content, so the example does not refute a theorem requiring uniform spatial regularity. It does refute the precisely stated unrestricted estimate based only on the displayed semigroup, forcing, normal-defect and Hilbert-norm data.

## 3. Smooth-target initialization robustness

Question: is roughness of the exact target the only cause of the obstruction?

Result: no. A fixed smooth rank-one target X₀=e₁e₁ᵀ with a vanishing but spatially rough rank-one initialization perturbation still leads to error tending to one. Both δ and ε+τ tend to zero. The exact target stays rank one; hence high intrinsic target rank is not responsible. The right-affine exact rank-one dynamical approximation can also be shown to remain nonsingular and to have modeling error at most ηt, so the large error is attributable to the splitting.

Boundary: the perturbation is not the exact Fourier projection of the fixed datum; its graph norm diverges. The result excludes arbitrary norm-small initialization errors under only Hilbert-norm control, not smooth consistently projected initialization. A one-step right-affine graph-norm bound explains this missing control but does not yield a global convergence theorem.

Symmetric-composition extension: STRANG_OBSTRUCTION.md proves the same limiting error one for standard KSL-half/LSK-half Strang. The key new estimate is that reversed LSK for right-affine dissipative stiffness differs from the exact affine step by at most 2h∥C∥. Thus the second half cannot restore the slow component lost by the first half. All QR ranks and intermediate scalar ranks are checked; the result is not merely a numerical suggestion or a separate bounded-ODE second-order counterexample.

## 4. Two-sided parabolic comparison with the modified method

Question: might the failure be a one-sided artifact or already excluded by the known stiff semilinear hypotheses?

Result: the two-sided family A=B=diag(0,−λ), C=ηI, Y₀=vvᵀ has direct KSL limit [[3/8,0],[1/8,0]] along λ=n², τ=η=1/n, while its error tends to 1/(4√2). The initial retained singular value is one and the numerical endpoint singular value tends to √10/8. The full and exact low-rank solutions are well defined. The 2019 semigroup and nonstiff-term hypotheses are uniform for the 2-by-2 family, yet that paper's modified G-then-linear scheme does not exhibit the same order-one discrepancy.

Consequence: importing the 2019 theorem into the unchanged full-F KSL method would be invalid. The example embeds into orthonormal Fourier-Galerkin heat dynamics, with explicitly nonuniform spatial regularity. On the active 2-by-2 block the normal remainder is bounded by η; on arbitrary rank-one matrices in the full Galerkin space the safe uniform bound is √2η, which has the same limiting significance.

## 5. Conditional positive left-affine PDE theorem

Question: can the endpoint cancellation still produce a rigorous mesh-uniform positive theorem for a specified direct-method subclass?

Result: yes, conditionally. For Y′=AY+C with dissipative A, the exact one-step error is bounded by

τ ε+τ²Γ∥C∥/2,

where ε bounds the mixed new-column/old-row forcing defect and Γ bounds the leakage ∥(I−U₊U₊ᵀ)AU₊∥₂ at the actual numerical endpoint basis. Exact-flow contractivity gives the global estimate δ+Tε+TτΓ∥C∥/2 without a numerical-map Lipschitz bound or inverse singular values. A periodic Fourier-Galerkin corollary for ∂_tz=∂_x²z+f adds explicit spatial projection tails and Sobolev rates in the true L² norm.

Boundary: numerical-subspace regularity and mixed near-tangency are assumptions, not consequences inferred from exact-solution smoothness. The theorem is affine, one-sided, exact-subflow and rank-preserving; it is not a general nonlinear or two-sided PDE theorem.

## Acceptance boundary

The source gate distinguishes the original full-F method from later modified/stabilized methods and stability-only results. The negative calculations and conditional theorem together provide a sharper formulation of what a satisfactory extension must control. They do not establish the full original request, a general robust second-order theorem, tensor-format coverage, adaptive-rank behavior, or inexact-subflow error bounds. No queue change or publication is part of this research checkpoint.
