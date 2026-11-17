# Adversarial deductions and falsification attempts

The full original theorem survives the following checks. These are independent deductions after the source-first boundary, not adopted archived audit outcomes or a repaired theorem.

## Domains, sharp cutoffs and the whole Fock space

On each antisymmetric sector, Fourier transform identifies T_n with multiplication by |p_1|²+…+|p_n|². Its domain is exactly antisymmetric H²(R^{3n}). The real symmetric multiplication L_n(L_n−κ) is bounded by n², preserves antisymmetry and gives self-adjoint H_n on the same domain by bounded perturbation. One may see the decisive resolvent step directly: for |Im z|>||B_n||, 1+B_n(T_n−z)^−1 has an inverse Neumann series, and its adjoint identity closes the symmetric perturbation. No constant uniform in n is needed. The maximal direct sum has the stated square-summability domain and is self-adjoint componentwise. Its unitary group is strongly continuous: first truncate a fixed vector to finitely many sectors, then bound the tail by twice its norm.

The sharp indicator is bounded multiplication and is never differentiated. Smooth χ maps H² to itself. The commutator identity is differentiated only for smooth initial orbitals in that preserved domain. Its estimate uses H¹ rather than H²; Cauchy–Schwarz on the two norms gives precisely Cχ=sqrt(||Δχ||∞²+4||∇χ||∞²). Multiplication by q is applied only after the identity. Thus the tempting objection that 1_Λ fails to preserve H² does not enter the argument. Neither a(f)D(H)⊂D(H) nor interacting CAR invariance is assumed: the bounded conjugated operator exists in B(F) without either assertion.

## Fixed geometry, Pauli packing and constants

The two bump denominators are everywhere positive because their nonpositive regions are disjoint. V=1 on the closed ball of radius8 and zero at radius≥9; χ=1 on radius≤3 and vanishes at radius≥3.5. Q lies strictly inside B3, disjoint from the support of f in the closed ball of radius1/3. The reference orbitals live in disjoint scaled interior subcubes, so Pauli exclusion gives an orthonormal family rather than forbidding large N. Their kinetic cost is Nℓ_N^−2||∇φ||²≤16||∇φ||²N^{5/3}. The fixed extra orbital in Ξ_N fits the same bound with actual n=N+1 and a fixed larger C0. All constants controlling geometry and one-body estimates are independent of N and κ.

The pair coefficient really is1 in an ordered sum. Inside Λ×Λ the selected difference potential is identically1, yielding L² including diagonal pairs and L(L−1) after their removal. For κ=0 the added diagonal term is a bounded one-body spatial potential per sector, not an ultraviolet smearing. The original statement covers both orderings explicitly. N=0 is not used in the time sequence (the normal-ordered denominator would vanish there); the vacuum sector and n=1 normal ordering present no domain problem. All claimed witness indices satisfy N≥1.

## Slater moment versus the misleading first-moment shortcut

For a free normalized Slater with occupied projection P, expanding the determinant gives <M²>=λ²+λ−Tr((PqP)²), λ=Tr(Pq). P is finite rank even though q has infinite rank; every trace used is finite. PqP is a positive contraction, so its squared trace is nonnegative. The eigenvalue boundary cases r=0 or1 give zero variance, and fractional r give Σr(1−r). This confirms the sign and the exchange subtraction.

A correlated superposition of an all-inside and all-outside n-particle vector can instead have Var M of order n². Therefore the variance bound must not be transferred to interacting states. The note does not do so: free evolution sends each initial Slater to another Slater, and the Duhamel reference is that free evolution times a scalar phase. No assumption that the actual interacting state remains Slater or close to its initial vector is used.

Summing the squared one-body leakage estimates gives λ≤β²s²n^{5/3}, followed by ||MΦ_n(s)||≤β|s|n^{5/6}+β²s²n^{5/3}. This is a bound on the norm of MΦ, not merely its expectation. It is exactly the distinction needed in Duhamel.

## Uniform two-sector and phase audit

Writing L=n−M gives H_n−K_n=−M(2n−κ−M). For both κ and every spectral value 0≤M≤n, its absolute value is≤2nM. The perturbation is bounded on each fixed sector; differentiating the interpolating two-group product and integrating proves the strong Duhamel identity. Its norm bound evaluates M only on free reference states. The integral is

E_n(t)≤β n^{11/6}|t|²+(2/3)β² n^{8/3}|t|³.

For n=N and N+1, n≤2N and t_N≤π/(2N); the powers are exactly −1/6 and −1/3. The potential, cutoff and observable remain fixed; only states and times vary. Replacing only the N-particle ket would leave an unestimated bra, but the note retains both errors E_N+E_{N+1}. A bound uniform on fixed particle truncations cannot be interchanged with the supremum over all sectors. In dimension2 the analogous powers vanish, and in dimension1 they grow; these failed routes do not contradict the stated dimension3 result.

With inner product linear in the second variable, free covariance gives a*(e^{ith}f). CAR reduces <a*(f)Ψ,a*(u)Ψ> to <f,u> because a(f)Ψ=0; it does not require u to remain orthogonal to occupied modes. The number-energy gap is2N+1−κ and the exact time makes its phase−1. Thus F_N^H(t_N)→−1. Taking adjoints gives <Ψ_N,D_NΞ_N>=conjugate(F_N^H(t_N)−1)→−2; the actual source pixel contains the conjugation bar, although extraction can obscure it. The upper norm bound2 then squeezes vector/operator norms to2, and ||D_NΞ_N+2Ψ_N||²≤8+4Re<Ψ_N,D_NΞ_N>→0. The creation operator-norm claim follows by taking adjoints, not by an unproved second vector construction.

## Topology and infinite-volume countercontrols

The same unitary group gives strong continuity for every fixed vector and every bounded observable. Its normal-state square difference is dominated by4 and tends to zero termwise in the state's spectral decomposition; trace summation is justified by summability. The states ω_N change with N, so there is no contradiction with that statement. No fixed density, bounded kinetic energy or common normal state controls the varying witnesses. The spatial one-particle Hilbert space is already L²(R³); there is no finite-box limit or hidden boundary condition in the kinetic energy. The interaction ball remains fixed. No full-space thermodynamic, all-potential/all-region, gauge-invariant-observable or CAR non-invariance conclusion is promoted.

## Independent check of the stated relation to the earlier phase mechanism

The actual 2026 primary theorem is for full-space difference potentials, so it cannot literally be cited as a theorem for the bounded symmetric kernel K(x,y)=1_Λ(x)1_Λ(y)V(x−y). Its proof nevertheless uses only multiplication, symmetry, a lower energy bound and a uniform multiplier bound in the cross-interaction. All hold for this bounded nonnegative K. The cutoff is not differentiated. Choose a small cluster neighborhood B around Q, a disjoint test neighborhood A around supp f, with both inside Λ; K=1 on A×B. For the qualitative two-mode argument a second test neighborhood outside Λ gives K=0 against the same cluster. The localized antisymmetrization estimate is geometric and unchanged. The earlier O(n²t²) error with t=θ/n is O(θ²), and a sufficiently small fixed θ gives the nonzero phase separation. Thus the note's qualitative adaptation claim is valid as a deduction, not a literally stated earlier cutoff theorem.

The claimed additional energy-bootstrap route can also be checked without reading archived audits. Let y(s)=<dΓ(χ_out²)> for a fixed smooth cutoff vanishing near Q and equal1 outside B, with B compactly inside Λ. Then M_Λ≤dΓ(χ_out²), and energy conservation for the selected local-number Hamiltonian gives

<T_n>_s ≤ C n^{5/3}+2n y(s).

The usual smooth-cutoff derivative bound yields |y'|≤C sqrt(y) sqrt(n^{5/3}+n y). Regularizing sqrt(y) at zero and integrating gives

sqrt(y(s))≤C |s| n^{5/6} exp(C sqrt(n)|s|).

Insert this refined leakage into the actual primary localized-antisymmetrization phase proof: its bad-cluster term is bounded by Cn sqrt(y(s)), its added-mode tail by Cn^{3/2}|s|, and its exact plateau term vanishes. Integration at t=O(1/n) produces O(n^{−1/6}+n^{−1/2}), hence tends to zero. For κ=0 absorb the diagonal 1_Λ into the added one-body Hamiltonian h'=−Δ+1_Λ; compactly supported test modes away from its boundary lie in D((h')²), giving the local H² time estimate by graph norms. Its cross phase2nt at the stated π/(2n+1) still tends toπ; κ=1 is immediate. This validates the source's already-disclosed audit-time cutoff deduction. It is not a repair, new priority claim, replacement of the explicit free-Slater proof or a new promoted theorem.

The 2026 Proposition2.6 explicitly proves the maximal2 limit for a constant full-space number interaction. The 2025 source constructs an extended algebra continuous in fixed-sector seminorms and a time-averaged subalgebra continuous in full operator norm, not norm continuity of the original unregularized CAR dynamics. These precise distinctions survive the manuscript's credit and scope. No broad literature search or firstness/open-status judgment is made.
