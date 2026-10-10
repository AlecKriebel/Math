# Uniform heat convergence and affiliated innerness: domain distinctions and partial results

## Disposition

The general dense-domain version of the AIM question is **not resolved here**. The results below clarify its hypotheses, give conditional affirmative answers, and calculate an explicit boundary family in every II₁ factor. The factor family is based on Dabrowski–Ioana, Remark 4.2; it is not a new construction. The full-domain observation and the elementary reductions are not claimed as novel. None of the examples refutes affiliated innerness under the AIM hypothesis.

## 1. Exact mathematical target and conventions

The last question in Section 0.11 of the AIM *Free analysis* problem list, dated 24 August 2006, concerns a closable derivation into the coarse bimodule, its heat semigroup, uniform convergence on the operator-norm unit ball, and implementation by an affiliated operator. The printed page number 7 is not part of the question. The source writes the domain as M; it does not explicitly supply a dense subalgebra or a reality assumption.

Let (M,τ) be a finite von Neumann algebra with faithful normal tracial state. Put N=M⊗̄Mᵒᵖ, Tr=τ⊗τ and H=L²(N). The coarse actions are

x·ζ·y=(x⊗yᵒᵖ)ζ.

In particular both actions are represented by multiplication on the **left** in N. Define K(x)=x⊗1−1⊗xᵒᵖ. For a weakly dense unital *-algebra D⊂M, a derivation δ:D→H satisfies δ(xy)=(x⊗1)δ(y)+(1⊗yᵒᵖ)δ(x). Assume it is closable as an operator L²(M)→H, and write A=δ̄*δ̄. Then A is nonnegative self-adjoint, and S_t=e^(−tA) is a contraction on L²(M). Define

a(t)=sup{||(1−S_t)x||₂ : x∈M, ||x||∞≤1}.

The substantive target is whether a(t)→0 entails a single ξ∈Aff(N) with δ(x)=K(x)ξ for every x∈D. Aff(N) denotes closed densely defined operators affiliated with N, with algebra operations given by closure. Hilbert-innerness means that ξ can be chosen in H. An ordinary algebra commutator in N is a different formula and must not be substituted.

For arbitrary complex derivations the displayed spectral semigroup exists; its being Markov is not automatic from closability alone. Where Markov/dilation results are invoked below, δ is explicitly assumed **real**, in the usual coarse real structure J(a⊗bᵒᵖ)=b*⊗(a*)ᵒᵖ, meaning Jδ(x)=δ(x*). Real closable derivations on the customary unital dense *-core yield symmetric conservative completely Markov semigroups. No claim using this extra hypothesis is asserted for arbitrary complex δ.

### Proposition 1: the literal everywhere-defined reading

If D=M and δ:M→H is L²-closable, then δ is Hilbert-inner, without using the heat hypothesis.

**Proof.** Regard δ as a map from the Banach space (M,||·||∞) to H. Suppose x_j→x in operator norm and δ(x_j)→η in H. Since ||x_j−x||₂→0 and δ is closable, applying closability to x_j−x gives η=δ(x). Its graph is therefore closed and the closed graph theorem gives ||δ(x)||₂≤C||x||∞.

For u∈U(M), set α_u(η)=u·η·u*+δ(u)·u*. The derivation identity gives an affine isometric action; its orbit of 0 is bounded by C. Every bounded orbit of affine Hilbert-space isometries has a fixed point. For completeness, the function r(η)=sup_{v∈orbit}||η−v|| has a unique minimizer: the parallelogram identity makes a minimizing sequence Cauchy, and then gives uniqueness. The action preserves r and hence its minimizer η₀. The fixed-point equation gives δ(u)=η₀·u−u·η₀. Taking ξ=−η₀ and using that every element of a unital C*-algebra is a linear combination of unitaries proves the claim. ∎

This argument uses the circumcenter of the orbit, not the least-norm point of its convex hull; the latter is generally not fixed by an affine action. The proposition cannot be used to declare the intended unbounded dense-domain problem solved.

## 2. What the heat modulus controls, and what it does not

For the spectral projections E_A, put q(R)=sup_{x∈M₁}||E_A((R,∞))x||₂. Elementary spectral calculus gives

q(R)≤a(1/R)/(1−e^(−1)),

a(t)≤tR+q(R).

Thus a(t)→0 is equivalent to q(R)→0. This is a statement about energy projections on the **input** Hilbert space L²(M). It is not already a statement about singular-value projections of the output δ(x) in Aff(N).

The familiar square-function identity, with possibly infinite sides, is

∫₀^∞||(1−e^(−tA))x||₂² dt/t² = 2 log(2) ||A^(1/2)x||₂².

Indeed Tonelli reduces it to ∫₀^∞(1−e^(−u))²du/u²=2log(2), by integration by parts. Hence if J=∫₀¹a(t)²dt/t²<∞, every x∈M belongs to the form domain and ||δ̄(x)||₂²≤(J+1)/(2log2) on M₁. Restriction to D and the bounded-derivation argument of Proposition 1, after norm-continuous extension to C*(D), gives Hilbert-innerness on D. These spectral and square-Dini facts are standard elementary controls, not the new conclusion sought.

### Proposition 2: no purely spectral passage to output measure boundedness

There is a closed densely defined linear operator T:L²(X)→L²(Y), with T1=0 and a conservative symmetric Markov heat semigroup, whose heat maps converge uniformly on the L∞(X) unit ball, while the image under T of the finite-support unit ball is not bounded in measure. This T is **not asserted to be a derivation** into any coarse bimodule.

**Proof.** Take X=ℕ×{−1,1}, giving each point (n,±1) mass p_n/2 with p_n=2^(−n), and Y={−1,1}^ℕ with product fair-coin measure. Let r_n be the independent coordinate functions on Y. Let s_n have values ±1 on the n-th two-point block and 0 elsewhere, and put e_n=p_n^(−1/2)s_n. These form an orthonormal basis of the block-antisymmetric subspace. Define Te_n=p_n^(−1/2)r_n and let T vanish on the block-constant subspace, on the maximal square-summability domain. It is closed because its nonzero part is a diagonal closed operator followed by an isometry onto the closed span of the r_n. In particular T1=0. The operator T*T has eigenvalue p_n^(−1) on e_n and is 0 on block constants. Its heat semigroup is the direct sum of the two-point averaging semigroups, hence conservative symmetric Markov. Directly,

sup_{||x||∞≤1}||(1−e^(−tT*T))x||₂²
=∑ₙ p_n(1−e^(−t/p_n))² →0

by dominated convergence.

But for x^(m)=∑_{n≤m}s_n, which has ||x^(m)||∞=1, one has Tx^(m)=R_m=∑_{n=1}^m r_n. Independence gives E(R_m²)=m and E(R_m⁴)=3m²−2m≤3m². Paley–Zygmund applied to R_m² yields

P(|R_m|≥√(m/2))≥1/12.

For each threshold K, choosing m>2K² therefore gives P(|Tx^(m)|>K)≥1/12. The image is not bounded in measure. ∎

Thus a proof of the AIM question must use the derivation/bimodule structure at this step; uniform energy-tail tightness alone cannot justify output measure tightness. The example is an obstruction to a proposed proof route, not to the AIM assertion.

## 3. Two precise affiliated-extension criteria

### Proposition 3: a full-algebra extension is enough

If δ has an extension δ̃:M→Aff(N) that is continuous from operator norm to measure, then δ is affiliated-inner.

This is exactly an application of Popa–Vaes, Theorem 1, *Vanishing of the first continuous L²-cohomology for II₁ factors*, IMRN 2015, pp. 3899–3907, [arXiv:1401.1186](https://arxiv.org/abs/1401.1186). The theorem covers all finite von Neumann algebras. It does not assert existence of δ̃ for an arbitrary dense-domain δ. The heat hypothesis has not been shown here to furnish this extension.

### Proposition 4: approximate innerness plus one diffuse core element

Suppose D contains a self-adjoint a whose scalar spectral distribution under τ has no atoms. Then δ is affiliated-inner if and only if there is a net ξ_i∈H such that K(x)ξ_i→δ(x) in H for every x∈D. In the converse direction it even suffices that these convergences hold in measure.

**Proof.** The commuting self-adjoint operators a⊗1 and 1⊗aᵒᵖ have joint distribution μ_a⊗μ_a under Tr. Its diagonal has measure ∫μ_a({s})dμ_a(s)=0. Hence K(a) has zero kernel and has an inverse in Aff(N).

If K(x)ξ_i→δ(x) in measure, then ξ_i=K(a)^(−1)K(a)ξ_i→ξ=K(a)^(−1)δ(a) in measure, since multiplication in Aff(N) is jointly continuous for the measure topology. For each x, continuity of multiplication by K(x) gives δ(x)=K(x)ξ.

Conversely assume δ(x)=K(x)ξ. Put e_n=1_[0,n](|ξ|) and ξ_n=ξe_n. Then ξ_n is bounded, hence belongs to H. Also K(x)ξ_n=δ(x)e_n→δ(x) in H, because δ(x)∈H and e_n↑1. ∎

The diffuse-element assumption is explicitly additional; an arbitrary weakly dense algebra need not contain such an element. More importantly, no argument here derives pointwise approximate innerness from a(t)→0. This gives a sharply stated alternative missing step rather than a solution.

## 4. The known non-amenability-set case

Let M be a nonamenable II₁ factor, and suppose a finite set F⊂D satisfies a coarse spectral-gap estimate

||ζ||₂≤C∑_{y∈F}||K(y)ζ||₂  (ζ∈H).

For a real closable δ into the coarse bimodule, uniform convergence of its own heat semigroup implies Hilbert-innerness. This follows from the proof of Dabrowski–Ioana, Theorem 1.1, specifically Section 4.1: its dilation and spectral-gap argument bounds ||δ(x)||₂ on D₁ by a constant times ∑_{y∈F}||δ(y)||₂. Their proof uses uniform convergence of the particular semigroup at this point, so a hypothesis about every derivation on M is not needed for this implication.

Source: [Dabrowski–Ioana, arXiv:1212.6425](https://arxiv.org/abs/1212.6425), *Unbounded derivations, free dilations and indecomposability results for II₁ factors*, Trans. AMS 368 (2016), 4525–4560, DOI [10.1090/tran/6470](https://doi.org/10.1090/tran/6470).

Neither nonamenability of M alone nor weak density of D supplies a non-amenability set **inside D**. The source explicitly warns that this core condition matters. The family below makes the danger concrete.

## 5. An explicit factor boundary family

The underlying derivation is the family of Dabrowski–Ioana, Remark 4.2. We calculate its generator and heat semigroup directly, unitalize its core, and obtain a uniform estimate without assuming that the ambient factor is L²-rigid.

### Proposition 5

In every II₁ factor M there is a real closable derivation into its coarse bimodule, on a weakly dense unital *-algebra, with a(t)→0 but with no Hilbert-space implementer. It is nevertheless affiliated-inner. Thus restricting the problem to factors does not make Hilbert-innerness follow from its bare heat hypothesis.

**Construction.** Choose orthogonal projections p_n with τ(p_n)=q_n=2^(−n), ∑p_n=1. Set

c_n=2^n/√n,    a_n=c_n²q_n=2^n/n,

ξ=i∑ₙc_n(p_n⊗p_nᵒᵖ)∈Aff(N),

Q_k=∑_{n≤k}p_n,    D=ℂ1+⋃ₖ Q_k M Q_k,

δ(x)=K(x)ξ  (x∈D).

The affiliated sum is well defined: its finite coefficients lie on mutually orthogonal projections in a finite algebra; the complement is assigned the value 0. For a finite-corner element only finitely many summands of δ(x) are nonzero, so δ(D)⊂H. The core is a unital *-algebra and is weakly dense since Q_k→1 strongly. The Leibniz rule follows directly from K(xy)=(x⊗1)K(y)+(1⊗yᵒᵖ)K(x). Moreover Jξ=−ξ, which gives Jδ(x)=δ(x*).

**Closability.** Write P_n=p_n⊗p_nᵒᵖ. The right-cut component is

δ(x)P_n=i c_n[xp_n⊗p_nᵒᵖ−p_n⊗(p_nx)ᵒᵖ].

For fixed n this extends to a bounded linear map L²(M)→H, with bound 2c_n√q_n. If x_j→0 in L² and δ(x_j)→η in H, it follows that ηP_n=0 for all n. Every δ(x_j) has right support in P=∑P_n, so η=ηP=0. Therefore δ is closable.

**Closed form and generator.** For x in a finite corner, expansion of the tensor-product inner product gives

||δ(x)||₂²=∑ₙc_n²[q_nτ(p_nx*x)+q_nτ(p_nxx*)−2|τ(p_nx)|²].  (5.1)

Let B={∑b_np_n:(b_n)∈ℓ∞}. The trace-preserving conditional expectation is

E_B(x)=∑ₙq_n^(−1)τ(p_nx)p_n.

The orthogonal decomposition of L²(M) into the subspaces p_iL²(M)p_j, and the scalar/traceless splitting of each diagonal corner, diagonalizes (5.1). Its eigenvalues are

- a_i+a_j on p_iL²(M)p_j for i≠j;
- 2a_i on p_iL²(M)p_i⊖ℂp_i;
- 0 on L²(B).

The finite-corner core is a core for this diagonal closed form: truncate the orthogonal blocks at i,j≤k, which converges both in L² and in the weighted form norm. In particular this is the form of δ̄*δ̄, not a different extension. On the finite-corner core its generator is

Ax=hx+xh−2∑ₙc_n²τ(p_nx)p_n,    h=∑ₙa_np_n.

The formula is asserted on that core; the diagonal spectral description defines the full operator domain.

**Exact heat formula.** With b_t=e^(−th)=∑e^(−ta_n)p_n, the diagonalization gives, for x∈M,

S_t(x)=b_t x b_t+(1−b_t²)E_B(x).  (5.2)

This is normal unital completely positive: the first summand is completely positive, while the second is the sum of positive scalar functionals x↦q_n^(−1)τ(p_nx) multiplied by the positive coefficients (1−e^(−2ta_n))p_n. The two summands together preserve 1 and τ. The spectral formula also verifies symmetry and the semigroup law.

For ||x||∞≤1, conditional expectation is contractive and

||x−b_txb_t||₂≤2||1−b_t||₂,

||(1−b_t²)E_B(x)||₂≤||1−b_t²||₂≤2||1−b_t||₂.

Consequently

a(t)≤4[∑ₙq_n(1−e^(−ta_n))²]^(1/2)→0.  (5.3)

The convergence is dominated convergence with summable weights q_n. This argument works in every II₁ factor.

**Failure of Hilbert-innerness.** Each corner p_nMp_n is diffuse, so choose a unitary u_n in that corner with τ(u_n)=0. The finite sum x_k=∑_{n≤k}u_n belongs to D and has norm 1. Formula (5.1) gives

||δ(x_k)||₂²=2∑_{n≤k}c_n²q_n²=2∑_{n≤k}1/n→∞.

If η∈H implemented δ, then ||δ(x_k)||₂≤2||η||₂||x_k||∞≤2||η||₂, a contradiction. The affiliated ξ already displayed does implement δ, so this is not a negative answer to the AIM question. ∎

### Additional checks and scope

The full diagonal sum u=∑u_n is a unitary in M. It is not in the closed form domain, since its energy is 2∑1/n=∞, although S_tu→u uniformly as part of (5.3). Thus even in a factor the hypothesis does not imply M⊂D(δ̄). This explicitly rules out the shortcut that would apply Proposition 1 to the L²-closure.

The same diagonalization gives the lower bound

a(t)²≥∑ₙq_n(1−e^(−2ta_n))²

by testing on u. Also ||1−S_t||_{B(L²(M))}=1 for every t>0 because a_n→∞ and the nonzero traceless diagonal corners supply unbounded eigenvalues. Thus operator-norm uniformity on the L² unit ball is strictly stronger than the AIM uniformity on M₁.

For this family, the implementer belongs to L^p(N) exactly when ∑q_n²c_n^p<∞; with the displayed coefficients this holds for 0<p<2 and fails for p≥2. This is a property of the chosen implementer, not a general integrability theorem about all solutions of the problem.

## 6. Remaining issue

No implication from bare heat uniformity to either a norm-to-measure continuous full-algebra extension or pointwise approximate innerness is proved. The spectral linear countermodel shows why such an implication cannot be justified by input spectral tails alone. The factor example shows why one cannot first force L²-boundedness, full L² domain, or an L² implementer. The known non-amenability-set theorem handles a significant extra-hypothesis case, but not an arbitrary core.

This packet is therefore a bounded, unrefereed partial investigation. It is not a claimed resolution or a claim that the general problem is currently open in every source; no complete dense-domain resolution was located in the literature checked.

## References

1. AIM, *Free analysis*, 24 August 2006, Section 0.11, final question, printed p.7. https://aimath.org/WWN/freeanalysis/freeanalysis.pdf
2. J. Peterson, *A 1-cohomology characterization of property (T) in von Neumann algebras*, Pacific J. Math. 243 (2009), 181–199. https://arxiv.org/abs/math/0409527
3. J. Peterson, *L²-rigidity in von Neumann algebras*, Invent. Math. 175 (2009), 417–433. https://arxiv.org/abs/math/0605033
4. A. Thom, *L²-cohomology for von Neumann algebras*, Geom. Funct. Anal. 18 (2008), 251–270. https://arxiv.org/abs/math/0601447
5. V. Alekseev and D. Kyed, *Measure continuous derivations on von Neumann algebras and applications to L²-cohomology*, J. Operator Theory 73 (2015), 91–111. https://arxiv.org/abs/1110.6155
6. S. Popa and S. Vaes, *Vanishing of the first continuous L²-cohomology for II₁ factors*, IMRN 2015, 3899–3907. https://arxiv.org/abs/1401.1186
7. Y. Dabrowski and A. Ioana, *Unbounded derivations, free dilations and indecomposability results for II₁ factors*, Trans. AMS 368 (2016), 4525–4560. https://arxiv.org/abs/1212.6425
