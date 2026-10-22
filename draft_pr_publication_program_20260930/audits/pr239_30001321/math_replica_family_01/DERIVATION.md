# Independent derivation: replica, return, overlap and coarse expectation

This is an independently written audit of the fixed-law inputs (B), (D), (F) and the same-parity reflection input (K)–(L) used in PR239. The authenticated PROOF.md, TURN_1.md, TURN_2.md and TARGET.json were read before any historical independent review, supplied checker or current family report. None of those reviews or checkers was read or executed in this audit.

## Model and exact two-replica kernel

For a fixed iid space-time law with 0<p<1 almost surely, write q=E p, a=q(1−q), δ=E[p(1−p)], and σ²=Var(p)=a−δ. Strict positivity of p and 1−p implies 0<q<1 and δ>0. Jensen or the variance identity gives δ≤a≤1/4. These facts require no uniform lower support bound.

Given the environment, take two independent transition-coin walks X,Y. Averaging a fresh layer is legitimate even conditional on their full joint past: the visited sites are past-measurable, and the next time layer is independent of that past. At different sites their right probabilities average independently to q. At a common site the four joint step probabilities are

- (++): E p²=q−δ;
- (--): E(1−p)²=1−q−δ;
- (+−) and (−+): δ each.

Both walks have the same time parity. Their half-difference D=(X−Y)/2 therefore lives in Z. Its jump rates to each neighbor are a off zero and δ at zero. Its holding rates are respectively 1−2a and 1−2δ. The averaged law of D is Markov because these conditional probabilities depend only on whether the current difference is zero. No position-independence after fixing the environment is being assumed.

The identity E sum_x μ_s(x)²=P_0(D_s=0)=g_s follows by conditioning the replica pair on the environment. Drift cancels in D even for q≠1/2.

## Return transform and pointwise return bound

Let ρ(z)=E_1[z^{τ_0}] for the chain away from zero, 0<z<1. The bounded solution of the second-order hitting recurrence is ρ(z)^d, where the smaller root satisfies

a z ρ²−[1−(1−2a)z]ρ+a z=0.

The first-return transform from zero is (1−2δ)z+2δ zρ(z). Thus

G(z)=Σ_{n≥0}g_n z^n
=1 / { (1−δ/a)(1−z)+(δ/a) sqrt[(1−z)(1−(1−4a)z)] }.

The branch is positive on [0,1). All terms in the displayed denominator are nonnegative. Since 1−(1−4a)z≥4a,

G(z) ≤ sqrt(a)/(2δ sqrt(1−z)).

An averaged bound on coefficients would be insufficient, so the separate monotonicity argument matters. Detailed balance holds for π(0)=a/δ and π(d)=1 off zero. Jensen's inequality and stationarity make P a contraction on ℓ²(π); detailed balance makes it self-adjoint. Since all holding probabilities are at least 1/2, Q=2P−I is itself a reversible Markov contraction, so spec(P)⊂[0,1]. The spectral measure of 1_{0} then gives g_n=∫_{[0,1]} λ^n dν(λ), with ν a probability measure. Hence g_n is nonincreasing.

Consequently g_n(1−z^{n+1})/(1−z)≤G(z). Set z=n/(n+1) for n≥1; z^{n+1}≤e^{−1}. This proves g_n≤C(q,δ)/sqrt(n+1). The case n=0 is absorbed by increasing C. No coefficient-transfer theorem, asymptotic local limit theorem or uniformity as δ↓0 is needed.

## Why the backward hitting profile is maximized at zero

Set u_n(d)=P_d(D_n=0). It is symmetric. For d≥0 define v_n(d)=u_n(d)−u_n(d+1). The backward equation yields exactly

v_{n+1}(0)=(1−2δ−a)v_n(0)+a v_n(1),

and for d≥1,

v_{n+1}(d)=a v_n(d−1)+(1−2a)v_n(d)+a v_n(d+1).

Here 1−2δ−a≥1−3a≥1/4 and the other coefficients are nonnegative. Initially v_0(0)=1 and every other v_0(d)=0. Induction proves u_n(d)≤u_n(0)=g_n for all integers d.

For the old quenched distribution μ_s, which is F_s-measurable and supported on one parity,

E[I_{s+t}|F_s]
=Σ_{x,y} μ_s(x)μ_s(y)u_t((x−y)/2)
≤g_t.

This argument establishes the needed conditional bound for an arbitrary old probability mixture, without asserting that I_s are independent.

For V=Σ_{j=0}^{L−1}I_{s+j}, expand V^k and order the k indices, overcounting by at most k!. Conditional on the penultimate time, the sum over the last index is bounded by A_L=Σ_{j=0}^{L−1}g_j; earlier products are nonnegative and measurable there. Iterate. Repeated indices are covered by the gap-zero bound I_t≤1=g_0, so no factor of I_t is silently treated as independent. Thus E[V^k|F_s]≤k! A_L^k≤k! C^k L^{k/2}. This proves (B), hence (C) by Markov and a separately chosen fixed k for each requested polynomial power.

## A separate Fourier proof of the annealed gradient estimates

Write the averaged parity-lattice position as 2B_t−t, with B_t binomial(t,q), and φ(θ)=1−q+q e^{iθ}. Then

|φ(θ)|²=1−4a sin²(θ/2),

so for |θ|≤π and t≥1,

|φ(θ)|^t≤exp[−2at θ²/π²].

Fourier inversion bounds max_j P(B_t=j) by C(q)t^{−1/2}. Inserting the extra factor |e^{iθ}−1|≤|θ| bounds the maximum adjacent-binomial difference by C(q)t^{−1}. The cases t=0 are finite and give the same bounds with t+1.

Unimodality, with zeros outside the finite binomial support, gives the exact identity Σ_j |b(j+1)−b(j)|=2 max_j b(j). In the spatial lattice these are shifts by two, not by one. This proves all three estimates (10) without relying on the source's shorter adjacent-mass-ratio sketch.

For any partition interval I and h_I(x)=T_t 1_I(x+1)−T_t 1_I(x−1), the parity-supported sum telescopes to a difference of two endpoint masses. Thus |h_I(x)|≤C(t+1)^{−1/2}. Bounding each contributing adjacent difference separately gives |h_I(x)|≤CM(t+1)^{−1} for an M-site interval. Summing absolute interval gradients over a partition is bounded by the total variation of the shifted binomial kernel, because disjoint intervals cannot increase the L1 norm of a signed measure. Therefore

Σ_I h_I(x)²
≤max_I |h_I(x)| Σ_I |h_I(x)|
≤C min[(t+1)^{−1}, M(t+1)^{−3/2}].

All statements are uniform in x and deterministic alignment. For intersections with real intervals of length M, replace the site-count factor by M+1; telescoping and contraction remain valid.

## Martingale variance and the expectation bound (F)

Exposing layers before time s makes μ_s measurable. The next environment-layer increment for μ_N(f) is exactly

Σ_x μ_s(x)(p_{s,x}−q)[T_{N−s−1}f(x+1)−T_{N−s−1}f(x−1)].

Given F_s, the variables p_{s,x}−q are independent and centered. Cross-site conditional covariances vanish; different time increments are orthogonal. Thus the sum of increment variances gives equation (8) exactly. Only finitely many reachable sites occur at a fixed N. The coordinate test f(x)=x is also valid on this finite reachable set and yields Var(E_ω X_N)=4σ²Σ_{s<N}g_s.

Summing over interval tests and inserting the return and gradient bounds gives

Σ_I Var(μ_N(I))
≤C Σ_{s=0}^{N−1}(s+1)^{−1/2}
 min[(N−s)^{−1}, M(N−s)^{−3/2}].

For s≤N/2 the contribution is at most C min[N^{−1/2},M/N]. For s>N/2 put k=N−s and bound (s+1)^{−1/2}≤C/√N. The remaining sum splits at k=M²:

Σ_{k≤N} min(k^{−1},M k^{−3/2})
≤C[1+log(1+min(M,√N))].

Therefore the sum of interval variances is bounded as in (13).

The window [vN−R√N,vN+R√N] meets at most 2R√N/M+2 cells. Cauchy–Schwarz on this finite collection bounds its expected L1 discrepancy by the square root of its cell count times the variance sum. Every cell outside that collection lies outside the window; its expected discrepancy is at most twice its annealed mass. Chebyshev for the annealed variance 4aN bounds the total latter contribution by 8a/R². This is (F), with a law-dependent constant.

For fixed R, if M≤√N the term log(1+M)/M tends to zero when M→∞, and the remaining log term divided by √N tends to zero. If M>√N, the whole logarithmic term is O_R(log N/√N). Let N,M→∞ first, then R→∞. This justifies a deterministic expectation bound ρ(N,M)→0 with no lower divergence rate on M. Taking an infimum over R does not impose a quantitative rate that has not been proved. Expectation convergence alone is not (A); the final-segment argument is still essential.

## Same-parity reflection and the closure interfaces

The quenched coalescing coupling uses separate transition coins until meeting and common coins afterwards. Same-parity nearest-neighbor paths cannot cross without meeting. Before meeting, fresh distinct-site environment variables average independently, so their positive half-gap is the homogeneous lazy walk with rates a,a,1−2a, killed at zero. Reflection fixes holding steps and gives survival from d≥1 exactly as

Σ_{j=1−d}^{d} p_ell(j).

The homogeneous maximum-mass estimate is C(q)/√(ell+1), so survival is at most 2d C(q)/√(ell+1). The coupling inequality gives the L1 kernel difference in (L), with |x−y|=2d. Opposite parity is expressly unavailable and is unnecessary for μ_m and α_m.

I also checked the interfaces to the closure, without adopting another family's audit. Replacing within a cell by the conditional α_m law keeps cell masses and changes starting positions by at most H; averaging the quenched coupling proves (M). Equation (N) is exact cellwise scaling. Translation of a starting point changes only the target partition alignment in (F), which proves (O). These operations preserve the fixed-law uniformity required in (P).

The displayed old-law concentration exponents are consistent: r=N^{3/8}, η=κ=1/32 give quadratic variation O(N^{−7/32}), deviation squared N^{−1/16}, and exponent N^{5/32}. The strip influences are deterministic; only alive path sites are queried. A change of one strip has output oscillation at most twice its old starting mass. A site belongs to at most six influence intervals, making the bounded-differences denominator at most a constant times the maximum such mass. This audit found no dependence on a forbidden quenched heat-kernel bound, unsupported instantaneous-overlap moment, cross-strip independence of endpoint masses, or opposite-parity coalescence at these interfaces.

## Boundary controls and limits of this audit

At δ=0 (the excluded iid deterministic-arrow law), D starting from zero never leaves zero, so g_n=1 and the diffusive return estimate fails. The quenched endpoint is then a point mass; for M=o(√N), its coarse L1 discrepancy is at least 2[1−CM/√N] and tends to two. Thus nonuniformity as δ↓0 is substantive. This does not contradict any fixed strictly elliptic law in the statement.

Allowing an unrelated chain with a=1/4 and δ=1/2 makes u_1(1)=1/4>u_1(0)=0, demonstrating that the model constraint δ≤a is needed for the profile proof. Such parameters cannot arise from the source's environment, since they would give Var(p)<0.

For opposite-parity starting positions, endpoint supports are disjoint at every fixed time and L1 distance is two. The source correctly restricts coupling to same parity.

The exact finite checks are evidence for the algebra and boundary handling. The general deductions above, rather than those tests, establish the assigned inputs for arbitrary fixed laws, including laws whose support approaches 0 or 1. The finitely supported test laws themselves each have a positive support lower bound; they are not represented as empirical coverage of every non-uniformly-elliptic law. This report supplies no priority conclusion, source-model-scope certification, publication approval or complete proof audit outside the assigned mechanism.
