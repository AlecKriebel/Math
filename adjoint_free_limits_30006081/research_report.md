# Adjoint-free recovery: five scoped approaches

Queue 1855, ID 30006081. Research date: 2026-10-21. Scoped mathematical report; overall status: UNSOLVED after five approaches. The broad Oberwolfach motivation is not a single unresolved conjecture. These are elementary model refinements and structured partials, not a claim to solve that umbrella or to establish novelty.

## Model and source/priority gate

A forward query returns the full vector Ax for one chosen vector x. A block with s columns costs s queries. The algorithm is measurable, may adapt and randomize independently of A, and its final matrix or factors depend only on its completed transcript and internal randomness. No hidden oracle occurrence in the output is allowed. Computation and exact arithmetic are free. Real inputs use real queries; complex inputs use complex queries. Norms below are distinguished explicitly.

Halikias–Hochstenbach–Townsend, *Transpose-free linear algebra*, arXiv:2606.01335v1, Theorem 5.1, already gives the randomized adaptive n-query worst-case/bounded-query obstruction for real m×n matrices with n≥m, finite relative Frobenius factor γ>1 and rank target 1≤k≤m. Rank-one Gaussian inputs drive its proof. Source: https://arxiv.org/html/2606.01335v1#S5.SS1 . It is a preprint, not a publication-status upgrade. Boullé–Halikias–Otto–Townsend, *Operator Learning Without the Adjoint*, JMLR 25(364), 2024, establishes geometric and regularity-based positive results: https://www.jmlr.org/papers/v25/24-0162.html . The source recovery and theorem scope audits remain authoritative provenance records.

None of the claims below is asserted novel. The expected-query calculation is an elementary stopping-time corollary of the same obstruction. Structural reconstruction uses standard linear algebra; the PDE estimate uses elementary energy bounds and the already-known Fourier projection principle. A targeted search is not a priority certificate.

## Approach 1: randomized stopping and matching-field extensions

### Exact minimax expected query cost

Fix m,n≥1, 1≤k≤min(m,n), success probability p∈[0,1], and finite γ≥1. Let algorithms stop almost surely on every input and return rank≤k matrices. Require, on every A, success probability at least p for

    ||A - Ahat|| ≤ γ inf_rank(B)≤k ||A-B||.

For either the Frobenius norm or spectral norm, the infimum over these algorithms of sup_A E[T|A] is exactly pn, for both matching-field models R and C.

**Lower bound.** Give A the distribution e₁g*, where g is a standard Gaussian vector over the appropriate field. The best-rank-k residual is zero, so success means Ahat=A. Fix the independent random seed. At each query the information about g is its scalar inner product with the chosen vector (or its conjugate). Decompose a new query into its old span component and a component in the orthogonal complement. A dependent query adds nothing. Conditional on the old transcript, the complement residual is isotropic Gaussian on that complement; the new independent scalar measurement removes exactly one field dimension. This holds inductively for measurable adaptive choices, using a measurable orthonormal completion. In C the residual is proper circular complex Gaussian and each query removes one complex dimension, not one real dimension.

At any deterministic finite time t, conditioned on a transcript whose query span has dimension d<n, the residual has a non-atomic Gaussian distribution on a positive-dimensional affine space. A transcript-measurable exact guess therefore has conditional probability zero. The event T=t is itself transcript-measurable and supplies no extra information. Union over t gives

    P(Ahat=A and rank(query span at T)<n)=0.

Consequently P(success)≤P(T≥n), and Tonelli plus the uniform success guarantee gives

    E_g E_seed T ≥ n P(success) ≥ np.

The supremum over fixed inputs is at least this average. This is NOT a lower bound np for every individual input. It also does not assert that every successful run at a specially selected deterministic input must use n queries; the almost-sure statement is under the continuous hard distribution.

**Upper bound.** With probability p make n coordinate queries, reconstruct A, and compute a truncated SVD; otherwise make no query and return zero. This has expected cost pn on every input and success probability at least p. For p=0 use zero queries.

### Bounded-query and field corollaries

If a global cap q<n is imposed, the same hard distribution gives zero average success, contradicting any positive uniform success probability. This proves n-query necessity for tall as well as wide matrices and for the complex matching-field model. Coordinate reconstruction proves sufficiency. These are separate proofs/extensions, not wording attributed to the source theorem. The spectral statement is justified by the same zero-residual argument, not by relabeling the source norm. Real matrices with complex queries are deliberately excluded: a complex query can encode two real probes.

**Failure of another route.** A transcript-dependent unseen vector chosen after a random run is not a valid randomized minimax argument. The fixed Gaussian distribution above is essential.

## Approach 2: a known row subspace and approximate priors

Let V have d orthonormal columns and be known. Query AV=B using d vectors. If A=AVV*, output BV*. This is an explicit exact reconstruction; no adjoint of the oracle is used. Among all matrices with row space contained in Range(V), the minimax expected cost for uniform success p and finite-factor best-rank-k approximation is pd (d≥1, k≥1). The proof embeds e₁g*V* with g∈F^d into Approach 1: arbitrary queries only reveal inner products with V*x. For the approximation task, truncate the reconstructed matrix to rank k, equivalently output B_k V*. The upper bound mixes this d-query procedure with a zero-query zero output.

For a nonexact prior, set δ=||A(I−VV*)||_F, and output B_k V*, with B_k a best rank-k approximation to the observed B. Orthogonality on the input side proves

    ||A-B_k V*||_F² = δ² + ||B-B_k||_F²
                       ≤ δ² + ||A-A_k||_F².

The inequality follows by comparing B_k against A_k V and using Frobenius contraction by V. Thus δ≤η||A-A_k||_F suffices for factor sqrt(1+η²). Here singular values beyond the available matrix dimensions are defined to be zero. For the spectral norm, writing E=A(I−VV*) and F=(AV−B_k)V* gives EF*=0, hence (A−B_k V*)(A−B_k V*)*=EE*+FF*. Therefore the spectral error squared is at most δ₂²+σ_(k+1)(AV)²≤δ₂²+σ_(k+1)(A)², where δ₂=||A(I−VV*)||₂. The assumption supplies actual row-space information; merely knowing a left range basis does not supply it. An absolute prior δ≤ε instead gives an additive squared-error guarantee, not a universal relative one. This prior tail bound is not certified by the d observations alone. This does not resolve the unrestricted task.

## Approach 3: equal row and column spaces (EP), including normal matrices

Suppose A is square, has known exact rank r≥1, and Range(A)=Range(A*). This EP assumption is weaker than normality. Let U be any fixed orthonormal basis of this common range, so A=U C U* for an invertible r×r C. Draw X∈F^(n×r) standard Gaussian and query Y=AX. With probability one U*X is invertible; hence Range(Y)=Range(U). Compute Q=orth(Y), and define

    Ahat = Y (Q*X)^(-1) Q*.

Since Q=UR for a unitary R, Q*X=R*U*X is invertible, and direct multiplication gives Ahat=A. Exactly r forward queries suffice. The output uses only X,Y,Q. There is no second Q-query batch and no unobserved Q*A. Rank zero needs no queries if known. The formula is an exact-arithmetic statement; near singularity of Q*X prevents any automatic stability/noise claim.

In the real model, this is a positive structured case compatible with zero-angle reconstruction in the 2024 paper. The complex EP result is proved directly here without relying on the paper's orthogonal/unitary notation. It is not evidence that unrestricted nonsymmetric recovery is possible, nor is a matching minimax lower bound for this EP class claimed here.

## Approach 4: an exactly solvable rank-one geometric slice

This approach studies a precise special slice of the asymmetric candidate geometry rather than claiming to close the general JMLR Remark 7 gap.

Let n≥2, a unit vector u be known in advance, and A=u v* with v≠0. Assume the prior

    |u*v| / ||v|| ≥ a,  0<a≤1.

Make the single query Au=αu and suppose α≠0. Since v*u=α, the candidates are exactly

    v = conjugate(α) u + w,  w⊥u,
    ||w|| ≤ |α| sqrt(a^(-2)−1).

The spectral and Frobenius distances between two corresponding rank-one matrices both equal the Euclidean distance between their v vectors. Thus the exact candidate diameter is

    2 |α| sqrt(a^(-2)−1),

and its optimal worst-case recovery radius is half this diameter, attained by the transcript-determined center Ahat=α u u*. The lower bound follows from opposite residual vectors of maximal norm; the triangle inequality gives radius≥half their distance. The center has rank at most one.

In the real rank-one model, the paper's near-symmetry parameter can be written a=1−ε, 0≤ε<1. For complex matrices this report explicitly uses the principal-angle/unitary convention in the displayed absolute-inner-product prior; it does not identify that convention with the paper's literal O(k) notation. As ε→0, the radius is asymptotic to |α|sqrt(2ε). A true input may itself sit on the prior boundary; the candidate diameter does not then vanish. This illustrates a limitation of a lower bound vanishing at equal true/prior asymmetry, but does not prove a global improvement for arbitrary X or higher rank. The known u is part of this model. Discovering u using an earlier random query would impose an additional data constraint, so the displayed set would no longer be the exact candidate set for the enlarged transcript.

## Approach 5: all-amplitude constant convection on an interval

Work in H=L²(0,1), with complex or real scalars. Let

    L_c u = -u'' + c u',  D(L_c)=H²(0,1)∩H₀¹(0,1), c∈R,
    A_c=L_c^(-1), L₀=-D².

For all c, the form is coercive because Re⟨c u',u⟩=0 under Dirichlet conditions. Lax–Milgram gives unique weak solutions, and the equation with constant coefficients implies H² regularity. The Hilbert adjoint is L_-c on the same domain, so A_c*=A_-c.

For u=A_c*f, integration by parts and Poincaré give

    ||u'||₂² = Re⟨f,u⟩ ≤ ||f||₂ ||u||₂ ≤ ||f||₂ ||u'||₂ / π,

hence ||u'||₂≤||f||₂/π and ||u||₂≤||f||₂/π², uniformly in c. The adjoint equation -u''-c u'=f then yields

    ||L₀ A_c*|| ≤ 1+|c|/π.

Let φ_j=√2 sin(jπx), and query y_j=A_c φ_j for j=1,...,s. The explicit rank≤s output is

    Ahat_s f = Σ_(j=1)^s y_j ⟨φ_j,f⟩.

It is determined by the s responses; unlike QQ*A, it has no hidden action of A. If P_s is the known sine projection, it equals A_c P_s, and

    ||A_c-Ahat_s|| = ||(I-P_s) A_c*||
      ≤ (1+|c|/π) / (π²(s+1)²).

The first equality is the operator norm adjoint identity, not an algorithmic adjoint query. The inequality follows by Fourier expansion and the lower eigenvalue π²(s+1)² on the complement. The same energy estimate gives a stronger drift-uniform companion: sine expansion implies ||(I−P_s)u||₂≤||u' ||₂/[π(s+1)], so the same output satisfies ||A_c−Ahat_s||≤1/[π²(s+1)]. Consequently its error is bounded by min{(1+|c|/π)/[π²(s+1)²], 1/[π²(s+1)]}. The first estimate is faster in s for fixed c, while the second is uniform in the drift amplitude.

This is a rigorous all-drift linear upper bound for a narrow constant-coefficient, one-dimensional, Dirichlet, L² operator-norm model. It does not claim actual error grows linearly, does not prove the general variable-coefficient elliptic conjecture, and is not a relative-to-best-rank guarantee. Variable drift introduces a divergence term into the energy identity and is not covered. The estimate is elementary and may already be known; novelty is unestablished.

## Outcome and remaining work

Five routes yield a sharp expected-query model refinement and four structured partials. The broad queue topic remains partially resolved, not solved by this report. The unrestricted bounded-query barrier was already known in the relevant source model. The general asymmetric candidate-set gap and broad large-perturbation PDE direction remain outside these results. Further research should first select one exact structured problem and perform a dedicated priority search rather than package these elementary corollaries as a breakthrough.

## Verification record

The independent stopping-time review is in `independent_review.md`; the separate structural/source review is in `structural_scope_review.md`. Its complex-parameter attribution correction has been incorporated. `sanity_checks.py` reproducibly tests real and complex EP recovery, row-space inequalities, the rank-one candidate diameter, and finite sine-Galerkin examples at five drift amplitudes. All checks passed in `sanity_results.json`; largest EP relative error was below 5×10⁻¹⁵. These are diagnostics, not substitutes for the proofs and not continuum convergence certification. The PDE oracle returns exact function-valued responses in an ideal Hilbert-space model; no finite-bit storage or numerical PDE solver complexity is claimed.
