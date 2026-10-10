# Turn 4: an exact Schur complement for the circle-even normal operator

Original target remains unresolved at4/5. This turn identifies the remaining circle-even index problem with a specific three-dimensional nonlocal tensor form. It eliminates the circle-circle scalar component through a strictly positive inverse, preserving index and describing the kernel exactly. It does not compute the remaining nonspherical index or the unrestricted degree.

## 1. Setting and notation

Use the same known S¹×R³ metric and weight as in Turns2–3:

g=a²dθ²+g_B,   g_B=dr²+b²g_S²,   f=f(r),

with the normalization Ric+Hess f+(1/2)g=0. Put ℓ=log a and F₁=f−ℓ, and use the measure

dμ=e^(−F₁)dvol_B=a e^(−f)dvol_B

on the smooth quotient B=R³. Circle rotations and θ↦−θ preserve g,f. A circle-invariant reflection-even symmetric tensor has the unique form

h=S+q e¹⊗e¹,    e¹=a dθ,

where S is a symmetric two-tensor and q a scalar on B. There are no mixed circle/base components. After dividing by the positive circle-volume constant, the weighted norm is ||S||²_μ+||q||²_μ.

Let

Q₀(S)=∫[|∇^B S|²−2〈Rm_B(S),S〉+2|S(∇ℓ,·)|²]dμ,

ℛ(S)=〈Hess_B ℓ,S〉,

H=−Δ_(F₁)+2|∇ℓ|²,

where Δ_(F₁)=Δ_B−∇_(∇F₁) on scalars, with its closed weighted quadratic form. Then the exact full circle-even form is

Q_even(S,q)=Q₀(S)+〈q,Hq〉_μ+4〈q,ℛ(S)〉_μ.             (1)

The scalar H is strictly positive and has compact resolvent. Define

Q_eff(S)=Q₀(S)−4〈ℛ(S),H⁻¹ℛ(S)〉_μ.                   (2)

Then

index(Q_even)=index(Q_eff),                           (3)

and the circle-even kernel corresponds exactly to the kernel of Q_eff, with

q=−2H⁻¹ℛ(S).                                         (4)

These assertions include arbitrary angular dependence on S²; they are not restricted to the radial/cohomogeneity-one modes.

## 2. Geometric calculation of (1)

First use compactly supported smooth S,q. The base covariant derivatives of h give |∇^B S|²+|dq|². The only extra circle-direction derivatives are the mixed entries

(∇_(E₁)h)_(1i)=(∇_(E₁)h)_(i1)=S(∇ℓ,E_i)−q dℓ(E_i)

for base indices i. Hence

|∇^g h|²=|∇^B S|²+|dq|²+2|S(∇ℓ,·)−q dℓ|².

The base curvature tensor in the warped product is Rm_B. Its mixed sectional tensor is R_(1ij1)=−a⁻¹(Hess_B a)_(ij). The circle/base contribution to 〈Rm_g(h),h〉 is therefore −2q a⁻¹〈Hess_B a,S〉. Thus

−2〈Rm_g(h),h〉=−2〈Rm_B(S),S〉+4q a⁻¹〈Hess_B a,S〉.

Expanding the derivative square and using

a⁻¹Hess_B a−dℓ⊗dℓ=Hess_B ℓ

gives exactly (1). This identity already follows from warped-product geometry; no unproved sign estimate on a″ or b″ is used. The drift appears only through the integration measure and the scalar adjoint defining H.

In the radial frame, ℛ(S) is explicitly

ℛ(S)=[a″/a−(a′/a)²]S_(rr)+(a′b′/(ab))(S_(22)+S_(33)).

Its coefficient tensor is bounded: it is smooth at the core, bounded on compact regions, and decays quadratically on the conical end. The coefficients of ∇ℓ are bounded as well. These facts follow from the smooth positive a at the core and the C² asymptotically conical warped profiles. In particular ℛ is a bounded multiplication map from the weighted tensor L² space to scalar L².

## 3. Positivity and invertibility of H

The scalar form is

〈q,Hq〉_μ=∫(|dq|²+2|∇ℓ|²q²)dμ≥0.

It has no kernel. Equality forces dq=0, hence q is constant because B is connected. But the measure μ has infinite total mass: f is bounded above, while the conical volume density a b² grows like a positive constant times r³. Thus a nonzero constant is not in L²(μ).

Here the conclusion is a positive **spectral gap for each fixed soliton**, not just absence of a zero eigenvector. Compactness follows directly from the already verified full spectral theorem, avoiding an unsupported inference from a positive integrand. Bamler–Chen Proposition5.38 gives a discrete self-adjoint full Einstein spectrum with eigenvalues tending to infinity, and the associated shifted form norm is the weighted H¹ norm up to equivalence. Its form domain therefore embeds compactly into full weighted L²: in an eigenbasis, a bounded shifted-form norm gives a uniformly small L² tail beyond any sufficiently large eigenvalue.

The scalar subspace S=0 has exactly the form H and the corresponding L² norm, by (1). A sequence bounded in the shifted scalar form maps to a bounded sequence in the full tensor form domain. The compact embedding just described gives a convergent scalar L² subsequence. Thus H has compact resolvent. Since it is nonnegative with zero kernel, its first eigenvalue is strictly positive. Consequently H⁻¹ is a bounded positive self-adjoint operator on L²(μ).

The scalar form domain and the restriction from the full tensor form agree: the extra connection term is the bounded potential2|∇ℓ|². Compactly supported smooth quotient functions are a core, with the same origin/infinity cutoff argument as before. No boundary condition is added at the smooth origin. No gap uniform over the two-parameter family is claimed.

## 4. Completion of the square and exact inertia

Since ℛ is bounded and H⁻¹ is bounded, H⁻¹ℛ(S) belongs to the scalar operator domain, in particular to its form domain. Completing the square in (1) gives

Q_even(S,q)=Q_eff(S)+||H^(1/2)[q+2H⁻¹ℛ(S)]||²_μ.        (5)

This is an identity of closed quadratic forms. The transformation (S,q)↦(S,q+2H⁻¹ℛ(S)) is bounded and invertible between the relevant form domains. The correction in (2) is bounded with respect to the tensor L² norm, so Q_eff is closed and bounded below. Its form-domain embedding into tensor L² is compact, by the same restriction argument applied to the S-only subspace and boundedness of the correction.

For clarity, index equality does not require claiming that these operators are unitarily similar. If W is a negative-definite subspace for Q_even, projection (S,q)↦S is injective on W, since Q_even(0,q)≥0. For every nonzero projected vector, (5) gives Q_eff(S)≤Q_even(S,q)<0. This proves index(Q_even)≤index(Q_eff). Conversely, the graph S↦(S,−2H⁻¹ℛ(S)) embeds any negative-definite subspace of Q_eff into one for Q_even, proving the opposite inequality. All indices are finite by the established spectral setting.

For the kernel, use the polarized form. Varying q first gives Hq+2ℛ(S)=0, hence (4). Substituting this into the S equation is precisely the weak kernel equation for Q_eff. The converse is immediate. Elliptic regularity in the original coupled system supplies the usual smooth representatives. This proves (3)–(4) without equating nonzero spectra.

## 5. Remaining normal modes and implication for the degree route

All coefficients and operators above commute with the standard SO(3) action on the quotient. H⁻¹ does too, so Q_eff decomposes into SO(3) representation sectors. Let m_l denote the multiplicity of the real irreducible representation of dimension2l+1 in its finite negative space. Then

index(Q_even)=sum_(l≥0)(2l+1)m_l.

Together with the circle parity reduction and the vanishing of the odd sector in Turn3, this yields

index_full(−L) ≡ sum_(l≥0)m_l (mod2).

The l=0 contribution is the rotational sector; the parity of sum_(l≥1)m_l is the remaining nonspherical correction. No representation-theoretic argument forces it to vanish. The Schur term in (2) is **negative**, so positivity of the scalar block, or positivity of separate diagonal terms, does not imply positivity of the coupled tensor operator.

Likewise, full regularity requires the effective circle-even kernel to vanish and all nonzero Fourier kernels to vanish. Neither is proved here. The separate global issue of accounting for every solution over a symmetric cone also remains. Thus the known restricted degree cannot yet be promoted to deg_exp(S¹×D³).

The connected-sum part of the source remains unaddressed by a valid gluing theorem. Original status is unresolved at4/5; one substantive turn remains before any final partial-result disposition. These operator identities and reductions are unreviewed partials, with no novelty assertion.

## Verification

The new certificate expands the full connection and curvature contractions for arbitrary local base tensor entries, verifies the Hessian cross term and scalar square, and checks the exact block-inertia identity on finite rational positive matrices. The compact-domain and spectral arguments are the written proofs and the pinned Bamler–Chen theorem. A finite matrix certificate does not establish an unrestricted Ricci degree or a uniform analytic bound over a degenerating family.
