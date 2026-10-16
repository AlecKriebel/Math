# Independent reconstruction of the replica and martingale inputs

Written before consulting any inherited `independent_review` verdict. This lane covers precisely the analytic inputs (B)–(G) of current PROOF.md, including the full TURN_2 restricted-scale theorem. It does not audit the later coalescence or moving-strip closure.

## Exact hypotheses and success criterion

The environment is iid over both time and position, with a single fixed law on (0,1). Put q=E p, a=q(1−q), δ=E[p(1−p)] and σ²=Var(p). Positivity gives 0<q<1 and 0<δ≤a≤1/4, with σ²=a−δ. None of these inequalities requires a uniform ellipticity constant or an inverse moment. Success in this lane means establishing every stated input B–G for all deterministic times, lengths and interval alignments, with law-dependent finite constants. A finite computation is diagnostic only.

## Replica kernel and return bound

For two walks independent conditional on their common environment, their current positions always share parity. Their half-difference D=(X−Y)/2 is integer. At a nonzero gap, the two newly encountered variables are independent and the probabilities of a gap increase and decrease are both q(1−q)=a. At a zero gap they share p, and each separation direction has probability E[p(1−p)]=δ. The holding probabilities are 1−2a and 1−2δ, respectively. Fresh time layers make this an annealed Markov kernel; no conditional independence is claimed for fixed-environment paths.

Thus E I_n=P_0(D_n=0)=g_n exactly. To reconstruct the transform, let ρ=E_1[z^τ0]. The bounded solution off zero is ρ^d, where azρ²−(1−(1−2a)z)ρ+az=0 and the smaller root is selected. A first-return decomposition yields

G(z)=1/[1−(1−2δ)z−2δzρ]
=1/[(1−δ/a)(1−z)+(δ/a)√((1−z)(1−(1−4a)z))].

At z=0 the expression extends continuously to 1. Since 1−(1−4a)z≥4a and δ≤a,

G(z)≤[√a/(2δ)](1−z)^(−1/2).

This alone would not justify a coefficient estimate. The separate spectral argument is valid: π(0)=a/δ and π(d)=1 elsewhere satisfy detailed balance; Jensen plus invariance makes the Markov operator an l²(π) contraction. Moreover 2P−Id is a reversible Markov contraction, because every holding probability is at least 1/2. Hence spec(P)⊂[0,1], and g_n is the nth moment of a probability measure on [0,1]. In particular g_n decreases. For n≥1 choose z=n/(n+1) and use

g_n[1−z^(n+1)]/(1−z)≤G(z),  z^(n+1)≤e^(−1).

Consequently g_n≤C_g/√(n+1), where C_g=√a/[2δ(1−e^(−1))] also covers n=0. All constants are explicit and finite for each fixed admissible law.

## Backward profile and conditional occupation moments: B and C

Let u_t(d)=P_d(D_t=0). It is essential to use the backward profile, not the forward mass P_0(D_t=d), because the defect chain is not counting-measure symmetric. Set v_t(d)=u_t(d)−u_t(d+1) for d≥0. Symmetry and the backward equation give

v_(t+1)(d)=a v_t(d−1)+(1−2a)v_t(d)+a v_t(d+1) (d≥1),
v_(t+1)(0)=(1−2δ−a)v_t(0)+a v_t(1).

Every coefficient is nonnegative, including 1−2δ−a≥1/4. The initial v has value 1 at zero and 0 otherwise. Thus u_t is radially nonincreasing and 0≤u_t(d)≤u_t(0)=g_t. This argument is unaffected by q≠1/2 because the half-difference is symmetric even when the individual walks are biased.

Conditional on F_s, the starting joint law is μ_s⊗μ_s and fresh layers are independent. Therefore

E[I_(s+t)|F_s]=Σ_(x,y) μ_s(x)μ_s(y)u_t((x−y)/2)≤g_t.

This includes t=0, where I_s≤1. For V=Σ_(j=0)^(L−1) I_(s+j), expanding V^k and ordering the indices costs at most k!. In the ordered sum, condition at the penultimate time and sum the final index over its deterministic remaining range; the conditional sum is at most A_L=Σ_(j<L)g_j. The earlier factors, including the penultimate one, are nonnegative and F at that time measurable. Iteration proves E[V^k|F_s]≤k! A_L^k≤k! C^k L^(k/2). Equal indices cause no failure: the bound at a zero gap is precisely I≤1. This is a conditional Kac-type bound for an occupation sum, not a bound E[I_N^k]=O(N^(−k/2)).

For m≤N and fixed η>0, Markov at order k gives P(Σ_(s<m) I_s>N^η√N)≤k!C^k N^(−kη). Choose k>K/η for each desired K. Times and lengths are deterministic throughout. Constants may depend on k and hence on K.

## Layer martingale and the joint-event tail estimate: D and E

For a deterministic bounded terminal f and horizon m, the Doob martingale is M_s=Σ_x μ_s(x)T_(m−s)f(x). Its increment at layer s is exactly

D_(s+1)=Σ_x μ_s(x)(p_(s,x)−q)[T_(m−s−1)f(x+1)−T_(m−s−1)f(x−1)].

The μ_s and gradient are F_s measurable. The layer variables are independent and centered, so

E[D_(s+1)²|F_s]=σ²Σ_x μ_s(x)² h_s(x)².

All sums concern finite reachable sets. Orthogonality yields the exact variance identity after summing these conditional variances. If f has Lipschitz constant 1/r, convolution with the averaged walk preserves it and |h_s|≤2/r. Then |D_(s+1)|≤2/r and Q≤4σ² r^(−2)Σ_(s<m)I_s. The same statement holds if the last layers have already been averaged: simply stop the layer martingale earlier and retain the larger smoothing time in h_s.

For |D|≤b and λb≤1, e^x≤1+x+x² on [−1,1] gives E[e^(λD)|past]≤exp(λ² E[D²|past]). Hence exp(λΣD−λ²Q) is a nonnegative supermartingale of expectation at most 1. On {ΣD≥u,Q≤w} its value is at least exp(λu−λ²w). Taking λ=u/[2(w+bu)] ensures λb≤1/2 and λu−λ²w≥u²/[4(w+bu)]. Apply also to −D. This proves E exactly as stated, including its use on a joint event; conditioning the martingale law on the future good event is unnecessary.

## Parity-aware kernel gradients and coarse expectation: F

Write B_t(j)=Binomial(t,q){j} and b_t(k)=B_t((k+t)/2) on the reachable parity, zero elsewhere. An independent global proof of the needed gradient bounds uses Fourier inversion on j, rather than a local ratio argument. Its characteristic function φ(θ)=1−q+qe^(iθ) satisfies |φ(θ)|²=1−4a sin²(θ/2). On [−π,π], this yields an integrable Gaussian bound C exp(−c_q t θ²). Fourier inversion gives max B_t≤C/√(t+1). The adjacent-difference multiplier |1−e^(iθ)|≤|θ| gives max_j |B_t(j+1)−B_t(j)|≤C/(t+1). Binomial unimodality, with zero extension, gives Σ_j |B_t(j+1)−B_t(j)|=2 max B_t. These facts include t=0 by enlarging C.

For a partition cell I_j with M consecutive integer sites, h_j(x)=T_t1_(I_j)(x+1)−T_t1_(I_j)(x−1). Summation on the parity lattice telescopes into two endpoint masses, so max_j|h_j|≤2 max b_t. The difference estimate also gives max_j|h_j|≤M max_k|b_t(k+2)−b_t(k)|. Since the cells partition the lattice, Σ_j|h_j|≤Σ_k|b_t(k+2)−b_t(k)|. Therefore

Σ_j h_j(x)²≤C min((t+1)^(−1), M(t+1)^(−3/2)).

Use the exact martingale variance identity and E I_s=g_s to obtain the sum of cell variances bounded by

C Σ_(s<N)(s+1)^(−1/2) min((N−s)^(−1),M(N−s)^(−3/2)).

For s≤N/2 the contribution is at most C min(N^(−1/2),M/N). For the other half it is at most C N^(−1/2)Σ_(k≤N)min(k^(−1),Mk^(−3/2)). Split at k=M², using only the relevant part if M²>N. This is at most C N^(−1/2)[1+log(1+min(M,√N))]. All estimates are uniform in cell alignment.

At most 2R√N/M+2 cells intersect [vN−R√N,vN+R√N]. Cauchy–Schwarz over those cells gives the first term in F. Every remaining cell is entirely outside this window, and the expected absolute discrepancy there is at most twice the averaged tail, at most 8a/R² by Var(X_N)=4aN. This proves F for N≥2. For fixed R, its first term vanishes whenever N,M→∞, including M≫√N; then let R→∞. Thus the infimum over R≥1, capped by 2, supplies the deterministic ρ used by current PROOF. The two limits do not impose a rate on M.

## Full auxiliary coarse-scale theorem: G

It is enough to prove any fixed γ∈(1/4,1/2); larger γ reduce to such a smaller exponent. Set d=γ−1/4, β=1/4+d/2, η=d/4, r=N^β and ℓ=floor(N^(2β)/(log N)²), m=N−ℓ. For large N, 1≤ℓ≤N/2 and r/M→0 uniformly in M≥N^γ. Let ν=μ_m T_ℓ, a conditional future average.

For every deterministic |f|≤1, the layer gradients before m are bounded by C/√(N−s), by the binomial total variation just proved. Thus b≤C/√ℓ and Q≤CΣ_(s<m) I_s/(N−s). Partition s by N−s−1∈[h_j,2h_j), h_j=2^jℓ. The blocks are deterministic consecutive intervals of length at most h_j. The occupation-moment bound shows that the single event E={Σ_(s∈B_j)I_s≤N^η√h_j for every j} has superpolynomially small complement: there are O(log N) blocks, and choosing a slightly larger fixed moment order absorbs this factor. On E, Q≤C N^ηΣ h_j^(−1/2)≤C N^η/√ℓ. For fixed u>0, E gives

P(|ν(f)−α_N(f)|>u,E)≤2exp(−c_u N^(β−η)/log N).

Let the central window have radius √N log N. It meets J≤C N^(1/2−γ)log N+2 cells. Their L1 discrepancy is the maximum over 2^J deterministic sign tests. The good-event failure is charged once, not separately for each sign test. The union bound is superpolynomial because

β−η−(1/2−γ)=5d/4>0.

Averaged bounded-increment tails outside the window are exp(−c(log N)²); the expectation of ν's tail is the same. Markov at a fixed tail threshold handles the outside cells. Therefore ν is superpolynomially close to α_N in coarse L1.

For the actual last ℓ layers, compare endpoints to the real position X_m+vℓ. They are in the same real half-open cell unless X_m is within r of a shifted cell boundary or |X_N−X_m−vℓ|>r. The expectation of the latter quenched event is ≤Cexp(−cr²/ℓ)≤Cexp(−c(log N)²). Markov gives a superpolynomial environmental tail at any fixed positive threshold.

Choose a periodic [0,1] majorant f_B of the boundary strips, Lipschitz 1/r and supported within 2r. Eventually strips are disjoint. There are O(r+1) supported lattice residues modulo M. For a unimodal lattice mass with peak p_*, any arithmetic progression with index spacing h has mass ≤1/h+2p_*: compare the monotone pieces with the integral of a unimodal interpolation, allowing the two peak-adjacent errors. On the parity sublattice the progression spacing in binomial index is M/2 for even M and M for odd M, so each lattice residue has averaged mass ≤2/M+2p_*. Consequently E μ_m(f_B)≤C r/M+C r/√N=o(1), uniformly in alignment.

For this single deterministic test, b≤2/r and Q≤C r^(−2)V_(0,m). On the common occupation good event, Q≤C N^(η+1/2−2β). Its fixed-u environmental upper tail is superpolynomial by E because

2β−1/2−η=3d/4>0.

Thus μ_m(boundary strips) exceeds any fixed positive constant only with superpolynomial probability. The coupling bounds are L1≤2μ_m(boundary strips)+2(endpoint deviation) for μ_N versus the translated old law, and the identical bound with the deterministic averaged deviation for ν. Their sum restores μ_N and proves G. The factor two is correct for the stated L1 convention.

## Boundary and quantifier audit

- q≠1/2 causes drift only in the single-walk center vN; the half-difference remains symmetric. Every use of a half-gap is between same-parity positions.
- δ=a (a deterministic p=q law) is allowed. Here σ²=0 and the quenched law is identically annealed, so the conclusions hold trivially; the arguments remain consistent.
- Merely elliptic laws may have support accumulating at 0 and 1 with no inverse moments. Every estimate above still uses only the two fixed numbers q and δ. Uniform ellipticity is not implicit.
- The random-arrow boundary δ=0 is excluded and genuinely different: the quenched endpoint is a point mass, while for M=o(√N) its annealed cell mass vanishes; its L1 discrepancy tends to 2. This is a boundary diagnostic, not an admissible counterexample.
- For p∈{ε,1−ε}, the preferred-arrow path has quenched probability (1−ε)^N for every environment. Thus L1≥2[(1−ε)^N−max_cell α_N(cell)]. At Nε≪1 and M≪√N this stays large, showing why the constants and eventual threshold cannot be uniform as δ→0. It does not contradict a theorem for each fixed ε>0.
- TURN_2 uses fixed γ>1/4. Its margins vanish at γ=1/4, so it cannot by itself be used at arbitrary slowly diverging M_N. Current PROOF uses it only at the auxiliary polynomial H; this lane does not assert the later closure valid.
- All good events are common over deterministic terminal tests. The argument never assumes independence of interval masses or independence of I_s across time.

## Provisional lane conclusion

The complete analytic reconstruction validates inputs B–G under their stated hypotheses. No mathematical gap or counterexample was found in this assigned earlier-turn family. The strongest independently reconstructed theorem in this lane is G, the superpolynomial environmental coarse-L1 tail for every fixed γ>1/4 and every M≥N^γ, together with the all-diverging-scale expectation convergence F. The exact remaining whole-PR gap for this lane is verification of the new coalescing/final-strip closure and the source/claim relation by their separately assigned lanes. Novelty and priority have not been assessed.
