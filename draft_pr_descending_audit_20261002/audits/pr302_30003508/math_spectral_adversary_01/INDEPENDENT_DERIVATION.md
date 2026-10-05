# Independent deterministic reconstruction for PR302

This derivation was built from the original TURN_1 and the relevant norm statements in TURN_2, with no inherited review conclusions. It applies to their stated smooth reversible conormal model. Let Hμ=L²(D,μ dx), H=L²(D,dx), U:Hμ→H be Uf=√μ f, and L be the nonpositive self-adjoint realization associated with the form ∫∇fᵀS∇f dx on H¹(D). The smooth realization has boundary condition n·S∇f=0. Fix Δ>0.

## Density conjugation and local unknowns

The observation kernel satisfies Pf(x)=∫pΔ(x,y)f(y)dy. Hence

    U P U⁻¹ f(x) = ∫√μ(x) pΔ(x,y) f(y)/√μ(y) dy
                   = ∫q(x,y) f(y)/√(μ(x)μ(y)) dy.

Detailed balance makes q symmetric. T=UPU⁻¹ is positive, compact and self-adjoint. If Lu_k=ν_k u_k with ∥u_k∥Hμ=1, then φ_k=Uu_k is an orthonormal H basis and Tφ_k=κ_kφ_k, κ_k=e^(Δν_k)>0. The generator's constant zero mode has κ=1; it is not a zero eigenvalue of T. Zero is a spectral accumulation point of T, not a true eigenvalue.

Put M=μ⁻¹ᐟ² and W=MT=P U⁻¹. Thus Wφ_k=κ_k u_k. Its actual kernel is

    K_W(x,y)=μ(x)⁻¹ q(x,y) μ(y)⁻¹ᐟ².

There are two x multipliers of exponent−1/2 before combination. Differentiating only one would be wrong. For a symmetric tensor,

    div(S∇u)=Σ_i S_ii ∂ii u + Σ_i<j 2S_ij ∂ij u
               + Σ_j (Σ_i ∂i S_ij) ∂j u.

Consequently the stated m=d(d+1)/2+d jet convention is correct. The last components of θ are div S, not the diffusion drift. The actual covariance is 2S/μ and the actual drift is (div S)/μ. Normalizing ∫μ=1 and knowing Δ fix the otherwise formal simultaneous coefficient/time scaling ambiguity.

An exactly solvable nonconstant-density control is μ(x)=2(1+x)/3 on [0,1], z=(2x+x²)/3 and S=1/μ. Then z′=μ, μ⁻¹∂x(S∂x)=∂z², and cos(kπz) has ν=−k²π² and zero endpoint conormal flux. In particular S u″+S′u′=ν μu. This checks the density factor in the eigenfunction equation independently. The control is one-dimensional, whereas the candidate theorem covers d≥2.

## The two required operator norms

Write ε_n=∥μ_n−μ∥∞ and assume the common positive lower bound. The maps t↦t⁻¹ᐟ² and t↦t⁻¹ are locally Lipschitz on this positive range; all needed x derivatives through order2 converge on an interior compact E. The T_n kernel difference is bounded in L²(D²) by a fixed multiple of

    ∥q_n−q∥L²(D²) + ε_n ∥q∥L²(D²).

The multiplier ranges are bounded, since uniformly converging μ_n have an eventual upper bound. Hilbert–Schmidt domination therefore gives ∥T_n−T∥H→H→0.

For W_n, expand ∂x^α[μ_n(x)⁻¹ q_n(x,y) μ_n(y)⁻¹ᐟ²] by Leibniz. Subtract the true expression. Each summand contains either a converging x multiplier derivative, a uniformly converging y multiplier, or one of the assumed derivative-row differences of q_n. Their remaining factors are uniformly bounded in the corresponding compact sup/L² norms. Thus

    max_|α|≤2 sup_x∈E ∥∂x^α(K_Wn−K_W)(x,·)∥L²(D) →0.

Cauchy–Schwarz now gives ∥W_n−W∥H→C²(E)→0. Hilbert-valued continuity ensures the derivatives are legitimate and the compact evaluation/jet functionals e_n(x) and B_n(x) vary continuously. Their norms and differences are uniformly controlled on E.

This is a substantive assumption. On (0,2π), r_n(x,y)=n⁻¹cos(nx)cos(ny) is a symmetric rank-one kernel with operator norm π/n→0, while sup_x∥∂xx r_n(x,·)∥₂=n√π→∞. Ordinary operator convergence cannot replace the derivative-row hypotheses. The candidate does not make that replacement.

## Functional calculus and the fourth power

For any nonzero empirical eigenvalue t and eigenfunction φ, W_nφ=t u. Accordingly

    B_nφ=t J u,        e_nφ=t u.

Using g(t)=t² for t>0 and0 otherwise, and h(t)=t²log t for t>0 and0 otherwise, both continued at0, gives exactly

    B_n g(T_n) B_n* = Σ_t>0 t⁴ (J u)(J u)ᵀ,
    μ_n/Δ B_n h(T_n) e_n* = Σ_t>0 t⁴ (log t/Δ) μ_n u J u.

Both outer factors contribute one t; g or h contributes the other two. Negative, zero, tiny positive and greater-than-one empirical eigenvalues are all treated by these identities. No logarithm is taken at a nonpositive argument. A zero empirical eigenvalue also has W_nφ=0. The true stationary κ=1 mode contributes neither jet excitation nor a right-hand side.

Inside a repeated eigenspace t, the contribution depends on its orthogonal projector, not a basis. Splitting, crossing, or rotating empirical eigenvectors is irrelevant. The same observation makes the estimator measurable through finite-dimensional matrix functions even if an eigensolver's arbitrary basis choices jump.

Since T_n→T, the spectra lie eventually in one real bounded interval. For a polynomial p, the telescoping identity for powers gives p(T_n)→p(T) in norm. Uniform polynomial approximation of a continuous real function f on that interval then gives f(T_n)→f(T). This requires continuity, not operator-Lipschitz continuity or separation of individual eigenvalues. Both g and h qualify, because t²log t→0 as t↓0. Composing these convergences with uniformly converging B_n,e_n and μ_n proves uniform compact convergence A_n→A and b_n→b.

For the infinite true sums, bounded row functionals give Σ_k|Bφ_k|²<∞ and Σ_k|eφ_k|²<∞. Bounded g(T),h(T) and Cauchy–Schwarz justify the relevant sums, uniformly under compact row bounds. The smooth positive-time heat kernel supplies those row bounds. Termwise use of the true eigenfunction PDE then proves b=Aθ. This argument does not assume the reconstructed coefficients satisfy any finite-data PDE.

## Full spectral jets and compact coercivity

Let ξᵀA(x)ξ=0 at an interior point. All summands are nonnegative, and every κ_k>0, so ξ·J u_k(x)=0 for every k. This implication would fail if some true modes had zero semigroup weight; the elliptic self-adjoint semigroup has no such modes.

Let f∈C_c^∞(D). The differential operator L preserves compact support in D. Thus f and every L^r f vanish near the boundary; all iterated conormal conditions hold. In particular f lies in D((1−L)^j) for every integer j. Its eigenfunction partial sums f_K converge to f in the graph norm of (1−L)^j:

    ∥(1−L)^j(f−f_K)∥Hμ²
      = Σ_k>K (1−ν_k)^(2j) |⟨f,u_k⟩Hμ|² →0.

For smooth coefficients and a smooth domain, the smooth elliptic conormal domain-of-powers theorem embeds D((1−L)^j) continuously into H^(2j)(D). Weighted and ordinary L² norms are equivalent. The shift1 avoids the generator's zero mode. Sobolev embedding with 2j>d/2+2 gives C² convergence. Therefore ξ·Jf(x)=0.

The needed import is compatible with the candidate: the principal symbol of1−L is μ⁻¹ ξᵀSξ, uniformly positive. In flattened boundary coordinates, with tangential frequency ζ and S split into tangential/normal blocks, the conormal boundary symbol at the decaying characteristic root is, up to sign,

    sqrt(S_dd ζᵀS_ttζ−(S_dtζ)²),

which is nonzero for ζ≠0 by the positive Schur complement of S. Hence this is an elliptic Neumann-type boundary condition, rather than an arbitrary boundary trace.

Choose a cutoff χ supported in D and equal to1 near x. For any desired jet v, a polynomial in z=y−x with linear terms v_gradient z, diagonal quadratic terms(v_diagonal/2)z_i² and cross quadratic terms(v_cross/2)z_i z_j has exactly J(χp)(x)=v. Thus all m coordinates are independently realizable, and ξ=0. No finite-K excitation hypothesis is assumed.

Continuity of the compact row functionals gives continuity of A(x). Since every A(x) is positive definite, compactness of E×{unit ξ} gives α_E=min ξᵀA(x)ξ>0. This number can be arbitrarily small when the model or lag changes; there is no asserted class-uniform bound.

One can also justify a finite cutoff after proving the full result. If κ_k are ordered decreasingly and M_B=sup_E∥B(x)∥, then the tail bound

    sup_E∥A−A_K∥ ≤ M_B² κ_(K+1)² →0

follows from A=B g(T) B*. Hence some finite K works throughout E for this fixed model. It is not an explicit universally adequate K. This is consistent with using the entire finite empirical positive spectrum.

## Ridge, clipping, and the TURN_2 norm bridge

Eventually A_n≥α_E I/2. For every λ_n>0,

    θ_n−θ=(A_n+λ_n I)⁻¹[(b_n−b)+(A−A_n)θ−λ_nθ].

The inverse norm is at most2/α_E, so uniform compact convergence follows for any λ_n→0. No noise/ridge rate coupling is needed after fixed-model coercivity has been established. At earlier sample sizes, positive ridge still defines a unique estimator, including when A_n is singular or the positive empirical spectrum is empty.

Extracting the symmetric tensor from θ is a fixed linear map, so the tensor converges locally. Frobenius projection onto {ell I≤S≤Lambda I} is nonexpansive and fixes the true S. The projected error is bounded by2√d Lambda; a countable compact exhaustion gives interior pointwise convergence, and dominated convergence over finite-volume D gives global L² convergence. No boundary derivative convergence is inferred.

TURN_2 claims, on one probability-one event, μ_j→μ in C²(D-bar) and q_j→q uniformly in all mixed derivatives through order2 in each variable. These conclusions imply the exact conditional inputs: for all |α|≤2,

    sup_x∈E∥∂x^α(q_j−q)(x,·)∥₂
       ≤ vol(D)¹ᐟ² ∥∂x^α(q_j−q)∥∞ →0,
    ∥q_j−q∥L²(D²) ≤ vol(D)∥q_j−q∥∞ →0.

Their density clipping/normalization gives a fixed lower bound c/(4C vol(D)). Once the raw density is uniformly close to μ∈[c,C], the smooth clip is exactly the identity throughout D; its derivatives cause no persistent bias. Normalization Z_j→1 preserves the C² limit. The symmetrized feature pair kernel is finite rank, and multiplication by a positive density preserves finite rank. Positivity of the empirical kernel, equality of its empirical marginals, conormal conditions on empirical eigenfunctions and empirical mass normalization of q_j are not required by this deterministic theorem.

The dyadic index j=floor(log₂N) tends to infinity along all N, so a pathwise result indexed by j transfers to the whole sample sequence. This review checks the norm bridge and its deterministic consequences. It is not a substitute for a separate independent audit of the proof that the observation model actually yields TURN_2's probability-one event.

## Primary analytic imports and boundaries

Grubb's domain characterization for powers of smooth elliptic Neumann-type realizations, Theorem2.2 and Corollary2.3, supports the graph-to-Sobolev step after shifting1−L. Its iterated boundary conditions are satisfied by the compactly supported tests. The elementary Sobolev embedding threshold is given in Corollary6.12 of the author's text. These are imported analytic results; the finite algebra controls do not reprove them. [Grubb, spectral regularity](https://web.math.ku.dk/~grubb/MN16.pdf), [Grubb, Sobolev chapter](https://web.math.ku.dk/~grubb/dist6.pdf).

The proof requires fixed Δ>0, a known smooth domain, smooth uniformly elliptic S, smooth positive μ, exact observation coordinates, a reversible conormal realization, and exact mathematical spectral/integral calculations. It does not establish efficiency, rates, a coefficient-uniform conditioning bound, rough-boundary/coefficient extensions, nonreversible reconstruction, or tolerance to unmodeled observation or numerical error.
