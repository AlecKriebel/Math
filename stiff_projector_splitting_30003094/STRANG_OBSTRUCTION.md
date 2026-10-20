# The same stiff obstruction for standard exact-subflow Strang PSI

Problem 30003094 / queue row 1829. Authored research, 20 October 2026.

## Scope

This is an additional result for the original direct projector-splitting method, not for the modified 2019 stiff/nonstiff scheme. It concerns the standard symmetric composition obtained by taking a KSL half step and then its reversed-order LSK half step, with all component subflows exact. The conclusion is a failure of a **specified unrestricted stiffness-uniform robust convergence bound** under only the weak assumptions described below. It is not a claim about every PDE regularity class, and not a claimed general resolution of the original open question.

Write Ψ_h for exact KSL and Ψ_h* for exact LSK. Each individual K, S or L map is an autonomous exact subflow; its inverse is its negative-time subflow as long as the needed ranks are maintained. Therefore reversing KSL gives its adjoint Ψ_h*=(Ψ_{−h})⁻¹. The symmetric full step is

Σ_τ=Ψ*_{τ/2}∘Ψ_{τ/2}.

In execution order it is K(τ/2), S(τ/2), L(τ/2), L(τ/2), S(τ/2), K(τ/2). The two consecutive L subflows freeze the same column space, so their exact composition is L(τ). Changes of orthonormal gauge at a QR factorization leave the represented matrix and this flow unchanged. This is the usual five-stage K–S–L–S–K Strang sequence, not a different artificial composition.

## 1. A stable coarse error bound for reversed LSK under right stiffness

Let F(Y)=YB+C, B+Bᵀ≤0, C constant. Start from rank-r Y=USVᵀ. The first L flow is

L′=BᵀL+CᵀU,  L(0)=VSᵀ.

Factor L(h)=V₊Ŝᵀ with V₊ orthonormal and set b=V₊ᵀBV₊. Define J_b(h)=∫₀ʰ exp(sb)ds. Transposing the left-affine identity of SUBCLASS_BOUNDS.md gives

Ψ_h*(Y)=U L(h)ᵀ+(I−UUᵀ)C V₊J_b(h)V₊ᵀ.

The exact flow is

Φ_h(Y)=Yexp(hB)+C J_B(h)
       =U L(h)ᵀ+(I−UUᵀ)C J_B(h).

Both B and b generate contractions. Therefore, whenever the LSK step is defined,

∥Ψ_h*(Y)−Φ_h(Y)∥≤2h∥C∥,
∥Ψ_h*(Y)∥≤∥Y∥+3h∥C∥.

These estimates are deliberately coarse. They make no claim of O(h²) local consistency, but are sufficient for the stiff counterexample because the forcing and first half-step output both tend to zero.

## 2. A smooth exact target with norm-small rough initialization

For integers n≥2 define

αₙ=1/n,  cₙ=√(1−n⁻²),  λₙ=n⁴,
τₙ=ηₙ=1/n,  hₙ=τₙ/2,
Bₙ=diag(0,−λₙ),  Cₙ=ηₙe₂e₁ᵀ,
Y₀,ₙ=e₁(cₙ,αₙ),  X₀=e₁e₁ᵀ.

The exact target is

Xₙ(t)=(e₁+ηₙt e₂)e₁ᵀ,

which is rank one, smooth in the Fourier embedding and represented exactly in every chosen Galerkin space. The initialization error is δₙ=√(2−2cₙ)∼1/n. The global normal remainder for the full field on rank-one matrices is bounded by ηₙ because the right-linear term is tangent and ∥Cₙ∥=ηₙ. The semigroup is contractive and analytic uniformly in n.

For the first KSL half step the compressed right generator is −λₙαₙ²=−n². Thus the K endpoint is

kₙ=exp(−n/2)e₁+(cₙ/n³)(1−exp(−n/2))e₂.

It is nonzero for every finite n; its normalized vector uₙ tends to e₂. The exact full flow from the numerical initializer at hₙ is

Φ_{hₙ}(Y₀,ₙ)
 =[[cₙ, n⁻¹ exp(−n³/2)], [1/(2n²), 0]].

The right-affine endpoint identity gives

Zₙ:=Ψ_{hₙ}(Y₀,ₙ)=uₙuₙᵀΦ_{hₙ}(Y₀,ₙ)→0.

Its two represented row coefficients uₙᵀΦ_{hₙ}(Y₀,ₙ) are strictly positive. In particular, Zₙ has rank one for every finite n, even though its singular value tends to zero.

Apply the coarse bound from Section 1 to the second LSK half step:

∥Σ_{τₙ}(Y₀,ₙ)∥=∥Ψ*_{hₙ}(Zₙ)∥
 ≤∥Zₙ∥+3hₙηₙ→0.

Since Xₙ(τₙ)→e₁e₁ᵀ, it follows that

lim_{n→∞}∥Σ_{τₙ}(Y₀,ₙ)−Xₙ(τₙ)∥=1,

although δₙ+εₙ+τₙ=O(1/n), with εₙ=ηₙ. The same contradiction applies to a τ(1+|log τ|) temporal term.

## 3. No rank-degenerate QR is hidden in the composition

The first half step has a strictly positive K first component, its S cancellation gives the positive scalar uₙ,₁, and its L endpoint has strictly positive row coefficients, as shown above.

For the second half, write Zₙ=uℓᵀ with u,ℓ having strictly positive components and ∥u∥=1. The first adjoint L equation has

ℓ₁(t)=ℓ₁(0)+ηₙu₂t>0,
ℓ₂(t)=ℓ₂(0)exp(−λₙt)>0.

Thus L(hₙ)≠0 and its QR can be taken with positive normalization V₊=L(hₙ)/∥L(hₙ)∥. After the S and K stages, the final K vector from the endpoint identity is

K_final=u∥L(hₙ)∥+(I−uuᵀ)CₙV₊J_b(hₙ).

Its component along u is exactly ∥L(hₙ)∥>0, so K_final is nonzero. Both QR stages and the returned rank-one matrix are therefore well defined for every n.

Even the intermediate scalar S can be kept positive in this example. Put β=−b≥0 and d=uᵀCₙV₊=ηₙu₂(V₊)₁. For 0≤t≤hₙ,

S(t)=exp(βt)[∥L(hₙ)∥−d J_{−β}(t)].

Since J_{−β}(t)≤hₙ, (V₊)₁≤1, and ∥L(hₙ)∥≥ℓ₁(0)+ηₙu₂hₙ, the bracket is at least ℓ₁(0)>0. During the last K flow the component in direction u solves the scalar inverse equation and stays positive as well. No singular projector event is required for the failure.

## 4. PDE meaning and what is not claimed

Use the orthonormal periodic Fourier embedding of the main report with high right frequency N=n², so λₙ=N². The exact datum is fixed and smooth, the forcing shape is fixed and smooth with amplitude ηₙ, and the numerical initializer differs in L² by O(1/n). Its right graph norm is n³, so it is not a uniformly spatially regular initializer and is not the exact projection of the fixed datum.

This proves that standard Strang symmetrization does not remove the **same weak-assumption stiff obstruction** established for direct Lie KSL. The reversed symmetric L–S–K–S–L ordering has the corresponding obstruction after transposing the equation and data; that changes right diffusion into left diffusion. No assertion is made that both orderings fail on exactly the same untransposed data.

This is not the separate published/preprint question of a second-order robust bound for bounded smooth ODEs. Here even first-order convergence with constants based only on the displayed weak semigroup/forcing/initial-norm assumptions fails uniformly in increasing stiffness. Positive theorems with additional numerical-stage regularity or compatible initialization remain possible.
