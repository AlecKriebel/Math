# Independent mathematical review: Bohr-radius characterization of ℓ¹

Review date: 2026-10-21.

Reviewed artifact: `RESEARCH_ATTEMPT.md`, SHA-256
`b2a6f3676810818eeded0d9e1af68415512cbd61dc43ab3ee676b21f037dbdaf`.

## Verdict

**Accepted as a partial-results and limitations report, not as a solution of the general characterization problem.** The five approaches and the easy-direction appendix are mathematically sound under their stated assumptions. No substantive correction is required in the reviewed version. The all-exponent block theorem and the explicit Lorentz example are valid. Neither establishes the unresolved implication for arbitrary unconditional sequence lattices.

## Claims checked

### 1. Quadratic witnesses, coordinate transfer, and block sums

The principal submatrix of a symmetric Sylvester Hadamard matrix has the asserted complex operator-norm bounds. Interpolation between ℓ¹→ℓ∞ and ℓ²→ℓ² gives the exponent 1/p′ for 1≤p≤2. Complex Hölder applies to the bilinear expression zᵀHz without needing conjugate symmetry.

Symmetry ensures that replacing the polynomial coefficients by their absolute values gives (Σzᵢ)²: diagonal coefficients have modulus 1 and off-diagonal coefficients have modulus 2. The resulting lower bounds

    χ₂(ℓᵖ_d) ≥ 2^(−1/p′)d^(1/p′),  1≤p≤2,
    χ₂(ℓᵖ_d) ≥ √(d/2),              2≤p≤∞,

are correct, including the endpoints and d=1. The distortion factor L⁻² follows from homogeneous ball inclusions. Coordinate inheritance follows from contractive coordinate projections and norm-preserving extension of a polynomial; it is not a statement about arbitrary abstract subspaces.

For an ℓ¹-sum of finite ℓᵖ blocks, these estimates prove the stated equivalence between positive uniform Bohr radius, bounded supⱼ dⱼ^(1/pⱼ′), and equality with ℓ¹ as sets. For pⱼ≤2 the distortion is at most √2 A², while pⱼ≥2 forces dⱼ≤2A⁴. Equality here means equivalent coordinate norms, not isometry. Uniform degree-two unconditionality already suffices for this restricted family.

### 2. Higher-degree random-sign inequality

Theorem 2.22 of the inspected primary source gives the stated bound when c_α=m!/α!. Indeed,

    c_α(α!/m!)^(1/r) = (m!/α!)^(1/r′) ≤ (m!)^(1/r′).

The unsigned polynomial has norm D_F^m. Applying χ_m(X_F)≤A^m to the supplied signed polynomial and taking mth roots gives equation (4) exactly. With m=max(2,ceil(log d)), both d^(1/m) and (log m)^(1/m) are uniformly bounded, while (m!)^(1/m)≤m=O(log(d+1)); thus equation (5) follows.

For normalized coordinate vectors, ||x||∞≤||x||X and Σ|xᵢ|^r≤||x||∞^(r−1)||x||₁ imply E_r(F)≤D_F^(1/r). Substitution yields only a logarithmic bound for D_F, with constants depending on fixed r. The report correctly does not send r to 1 or claim improvement over the published near-ℓ¹ bound.

### 3. Lorentz example and the near-ℓ¹ gap

The given decreasing positive weights define a Banach lattice norm on c₀₀. Completion embeds in c₀, contains ℓ¹ continuously, and has a canonical 1-unconditional Schauder basis. Chebyshev's inequality, with equality on constant vectors, proves D_n=n/W_n exactly.

The split at ceil(√n) proves W_n∼n/L(n): after division by n/L(n), the initial portion is O(L(n)/√n)=o(1), and the remaining upper bound tends to 1 because L(ceil(√n))/L(n)→1. Therefore D_n∼log log log n is unbounded while satisfying every asserted positive power of log log n for sufficiently large n.

The positive-series construction rigorously gives an element of X outside ℓ¹. Positivity permits Tonelli even if the supports overlap. This example disproves an inference from the near-ℓ¹ growth estimate alone to equality with ℓ¹. It supplies no positive-Bohr example and is not a counterexample to the target problem.

### 4. Projection-constant bridge

The proposed unqualified comparison λ(P_m(X_n))≤C^mχ_m(X_n) fails at m=1: P₁(X_n)=X_n* isometrically, its monomial constant is 1, and its projection constant is unbounded for Euclidean sections. This valid obstruction rules out the stated pointwise comparison, not a more subtle all-degrees implication. The report correctly distinguishes the projection hypothesis in Theorem 2.21 from the unresolved monomial-unconditionality hypothesis.

### 5. Fundamental functions without symmetry

For ℓ¹ on odd coordinates plus c₀ on even coordinates, all structural assumptions hold and φ(n)=ceil(n/2)+1 for n≥2. In fact D_n=floor(n/2) for n≥2, attained on the even coordinates. Thus φ(n) comparable to n does not force ℓ¹ equality without symmetry. The even-coordinate quadratic witnesses force the Bohr radii to vanish, so this space is only a counterexample to the fundamental-function shortcut.

### 6. Easy direction and set equality

Complex polarization gives ||T||≤(m^m/m!)||P|| for the associated symmetric multilinear form. On ℓ¹, its multilinear norm is the maximum absolute coordinate entry; hence the coefficient-absolute polynomial has norm at most ||T||. This proves χ_m(ℓ¹_d)≤m^m/m!≤e^m. Norm distortion L gives χ_m(X_d)≤(eL)^m, and the cited Bohr comparison gives the uniform lower bound 1/(3eL).

Uniform D_n implies the full ℓ¹ embedding by coordinate partial sums and monotone convergence. Conversely, equality of the underlying Banach sequence spaces gives equivalent norms by the closed graph theorem. Neither argument assumes normalized coordinates where they have not been specified.

## Evidence and limits of acceptance

The source-dependent checks used Defant, Galicer, Mansilla, Mastyło and Muro, *Local constants and Bohr's phenomenon for Banach spaces of analytic polynomials*, [arXiv:2509.26326v2](https://arxiv.org/pdf/2509.26326v2): Theorem 2.21 and its proof, the open-problem discussion, Theorem 2.22, Proposition 2.28, and Theorem 2.29. The latter two justify the A-versus-Bohr-radius constants used throughout.

This review validates the stated deductions and their limitations. It does not certify novelty, independently verify a later-literature search, or prove that every lattice with unbounded ℓ¹ distortion has the coordinate geometry needed by the successful special-case argument. The general problem remains unresolved by this work.
