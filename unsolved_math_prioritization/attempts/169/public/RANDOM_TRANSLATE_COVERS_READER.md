# Random translate covers at square root size

## Original question and result

**The original question remains UNSOLVED by this five-stage study.** In the prime cyclic group G=Z/pZ, choose A uniformly among its k=⌊√p⌋-element subsets. Is it true that

    P[∃T⊆G, |T|≤c=⌊100√p⌋, A+T=G] → 1

as p tends to infinity through all primes? T may depend arbitrarily on all of A. This is the precise operational interpretation of Ben Green's square-root random-translates question, Problem 39 in *100 Open Problems*. Its fixed-size and rounding conventions are explicit here; they are not quoted as a more precise formulation than the source gives.

An affirmative answer must prove that limit. A negative answer must exhibit ε>0 and an unbounded prime sequence with success probability at most 1−ε. The study does neither. The purpose of this reader is to preserve the useful mathematics and explain exactly what would still be needed.

## Executive explanation

A typical fixed choice of about 100√p translating centres leaves about e⁻¹⁰⁰p holes. That is a very small fixed fraction, but it grows linearly with p. More importantly, the question allows choosing the best set after seeing A, among exponentially many candidates. Fixed-candidate calculations and failed simple constructions do not decide that optimization.

The most useful positive reduction is constructive: take several shifted copies of any good near-cover of the same A, intersect their hole sets by averaging, then repair each remaining hole with one translate. At a 33k-centre starting budget, an expected residual o(p^(5/6)) would suffice. Even a near-cover with that residual on an event of probability exp[−o(p^(1/6))] would suffice after concentration. Neither initial estimate is proved.

The most direct negative reduction controls the unrestricted optimum itself. If its mean residual at the full cap were at least a c√k on arbitrarily large primes, for some a>0, concentration would force a positive failure probability. That lower mean remains unproved; its established unrestricted lower bound is zero.

The other contributions locate why tempting shortcuts fail and retain exact structure for future work: budgeted heavy-block removal, low-degree conditioned completion, adaptive exchange flux, actual additive cycle equations, and a correctly normalized canonical count. None is promoted to a solution.

## 1 The model and the elementary baseline

Write

    f_{A,T}(x)=|{(a,t)∈A×T:a+t=x}|,
    U(A,T)=|{x:f_{A,T}(x)=0}|,
    R_m(A)=min_{|T|≤m}U(A,T),   μ_m=E_A R_m(A),
    τ(A)=min{|T|:U(A,T)=0}.

Binomial coefficients with impossible choices are zero. Statements about c-subsets apply on the eventual prime tail c<p. Covers can be padded to c elements without losing coverage; a different observable, such as the bounded score below, need not be monotone under that padding.

For fixed A with |A|=k and a uniform m-subset T,

    E_T U(A,T)=p binom(p−k,m)/binom(p,m).

For fixed T of size m and uniform A the equivalent expression is

    E_A U(A,T)=p binom(p−m,k)/binom(p,k).

Consequently, for every A,

    0≤R_m(A)≤floor[p binom(p−k,m)/binom(p,m)].                 (1)

For m/k→C with C fixed, the upper bound is (e^(−C)+o(1))p. This is an upper bound on the optimum, not its value or a lower bound.

The ordinary fractional translate-covering optimum is exactly p/k: weight every translate by 1/k, and sum the p covering inequalities for the reverse bound. The same fractional matching optimum does not control an integral matching when uniformity grows. A universal complete cover follows by choosing s centres and repairing the expected residual:

    τ(A)≤s+floor[p binom(p−k,s)/binom(p,s)].

With s=ceil[(p/k)log k], this gives τ(A)≤(p/k)(log k+1)+1 for large p. This standard logarithmic overhead is eventually larger than the requested constant 100.

A sharper integer greedy baseline is useful for diagnostics. Let g₀=p and

    g_{i+1}=g_i−ceil[k g_i/(p−i)]   (0≤i≤p−k),

and let g_i=0 thereafter. Unused centres have exactly k incidences per remaining hole, so some new centre removes at least the displayed average rounded up. The update is nondecreasing in the integer residual. Thus R_i≤g_i. For i≥1 in the stated range,

    p binom(p−k,i)/binom(p,i)−i < g_i ≤ p binom(p−k,i)/binom(p,i).

The rounding gain is O(i), so it does not change the positive-density asymptotic in (1).

The operational caps satisfy 0≤c−100k≤99. A proof of τ≤(100+o(1))√p without a one-sided endpoint margin would not settle the exact cap. A positive margin whose product with √p diverges safely absorbs bounded cap changes. No unproved equivalence between floor and ceiling formulations is assumed.

## 2 Concentration of the unrestricted optimum

This is a reduction about all possible A-dependent centre sets. Suppose A=B∪{a} and A′=B∪{a′}, with |B|=k−1. For a fixed T, both sumsets arise from B+T by adding between zero and |T| new points. Therefore

    |U(A,T)−U(A′,T)|≤|T|,
    |R_m(A)−R_m(A′)|≤m.                                    (2)

For the minimum, compare using an optimizer at one endpoint and reverse the comparison. No stability of the optimizer is assumed.

Expose a uniform k-set through a random ordering. Conditional completions after different next values can be coupled by exchanging those two values, so conditional expected residuals differ by at most m. The Doob increments are bounded by m. Azuma gives both tails

    P[R_m≤μ_m−u], P[R_m≥μ_m+u] ≤ exp[−u²/(2km²)].             (3)

This improves the earlier valid conservative denominator 8km². The historical supplements retain that older bound; this reader uses (3).

In particular,

    P[τ≤c]=P[R_c=0] ≤ exp[−μ_c²/(2kc²)].                     (4)

Thus μ_c≥a c√k along unbounded primes is a sufficient negative premise, giving failure at least 1−exp(−a²/2) there. It is not necessary for a negative answer. If the success probability tends to one, (4) forces μ_c=o(c√k); the converse is false as a deduction because a small mean on that scale need not make the integer residual zero.

No positive lower estimate at the required p^(3/4) scale is proved. Estimates for any fixed T cannot be moved through the minimum in the needed direction.

## 3 Same-set amplification and exact-budget repair

For two optimizing near-covers of the same A at budgets m,n, let their hole sets be U,V. If the second centre set is shifted by d, the combined holes are U∩(V+d). The identity

    Σ_d |U∩(V+d)|=|U||V|

gives the fully adaptive inequality

    R_{m+n}(A)≤floor[R_m(A)R_n(A)/p].                        (5)

No independence is used. Optimizers and the chosen shift may all depend on A. Repeating the argument at arbitrary budgets m₁,…,m_r yields

    R_{Σm_i}(A)≤floor[∏R_{m_i}(A)/p^(r−1)].

Choose a₀∈A. Each remaining hole x is covered by the one new centre x−a₀. In particular,

    τ(A)≤rm+floor[R_m(A)^r/p^(r−1)].                         (6)

For rm≤c, put b=c−rm and B=[(b+1)p^(r−1)]^(1/r). The exact integer implication is

    τ(A)>c ⇒ R_m(A)≥B.                                     (7)

The b+1 is essential. Markov now gives failure probability at most min(1,μ_m/B). Hence each of the following unproved inputs would settle the affirmative question:

- μ_(49k)=o(p^(3/4)), using two copies and at least 2k repair centres;
- μ_(33k)=o(p^(5/6)), using three copies and at least k repair centres.

There is also a probability bridge. If α=P[R_m≤v]>0, (3) implies

    μ_m≤v+m√(2k log(1/α)).

Combining with (7) and the upper tail of (3),

    P[τ>c]≤exp{−[B−v−m√(2k log(1/α))]_+²/(2km²)}.           (8)

For m=33k,r=3 it suffices to find v=o(p^(5/6)) and log(1/α)=o(p^(1/6)). Then failure is exp[−Ω(p^(1/6))]. A constant positive probability of a complete 33k-cover would be enough. For fixed r>2 and a fixed k-scale repair margin, the analogous scales are v=o(p^(1−1/(2r))) and log(1/α)=o(p^(1/2−1/r)). These are conditional consequences, not success rates achieved by the study.

Known stratified complete covers have probability exp[−k+O(log k)], too rare for (8). Substituting only the baseline positive-density estimates into any fixed number of amplification stages leaves a positive-density upper bound. This failure to prove a better bound is not a lower bound on the actual method or on R_m.

Means cannot be multiplied without control: (5) gives E[R_mR_n]/p, not μ_mμ_n/p. At p=11 a diagnostic has E R₄=E R₄²=2/3>(E R₄)². Pointwise budget convexity and submodularity also fail in finite examples; no theorem about averaged versions is inferred from finite searches.

## 4 What simple-family exclusion really proves

### Fixed envelopes and additive structure

For deterministic |S|≤M√p, its uncovered count has mean at least (e^(−M)−o(1))p and exchange bound |S|. Thus P[A+S=G]≤exp(−c_M√p), for fixed M and a positive c_M. This excludes every predetermined family of exp(o(√p)) envelopes, even if a member is selected after seeing A. It does not exclude arbitrary T, whose number has logarithm Θ(√p log p).

The Green–Ruzsa structure theorem puts a small-doubling T inside a bounded-rank coset progression of O_K(|T|) size. In a prime cyclic group of this size the subgroup part is trivial. Polynomially many progression parameter descriptions suffice, and the fixed-envelope tail beats that count. Hence for fixed C,K, with high probability no T of size ≤C√p and doubling |T+T|≤K|T| covers. A quantitative extension is valid when K_p⁴log²(K_p+2)=o(log log p). Petridis's theorem converts a small-difference hypothesis |T−T|≤H|T| to |T+T|≤H²|T|. These statements do not classify all covers.

### Bounded elementwise maps and seed descriptions

Fix r and arbitrary predetermined maps φ₁,…,φ_r:G→G. For T_Φ(A)=∪φ_j(A), the study proves

    E|G\(A+T_Φ(A))|≥(e^(−r)−o(1))p.

One proof first uses Bernoulli sampling: for a target x, Harris positive correlation of the decreasing edge-avoidance events and Jensen yield the mean bound, including loops and repeated events. A monotone coupling transfers the mean to exactly k elements. An exchange changes at most 4rk sum values; direct fixed-size concentration then permits a predetermined exp(o(k))-sized menu of map tuples. The resulting positive-density holes cannot be repaired by o(k) arbitrary extra centres. This includes fixed-size affine-copy envelopes; it does not include unrestricted maps designed after observing A.

For a predetermined decoder F taking an s-element seed B⊆A to at most m=C√p centres, condition on B⊆A. The remaining k−s elements are uniform outside B. At least p−sm targets lie outside B+F(B), so their conditional uncovered mean is at least

    (p−sm) binom(p−s−m,k−s)/binom(p−s,k−s).

Its exchange bound is m. Counting eligible seeds uses binom(k,s), not binom(p,s), through the seed-containment probability. For s=o(k), even an exp(o(k)) menu of decoders leaves positive-density holes with high probability. The linear-seed sufficient exclusion condition, if s/k→α<min(1,1/C) and log L/k→ρ, is

    ρ+h(α)<(1−Cα)² exp[−2C(1−α)]/[2(1−α)C²].

It is only a sufficient exclusion region. A weighted countable decoder family with total weights ≤1 gives an analogous criterion: a universal cover decoder with sublinear seeds and weight exp(−o(k)) would imply noncoverage. The essential universal compression premise is not proved. Hardcoding a cover does not pay for its description.

### Why some first moments fail

Rare interval inputs support exp(Θ(k log k)) inclusion-minimal covers. An explicit cyclic-gap construction gives E[number of inclusion-minimal covers]≥exp[(1/2+o(1))k log k]. Thus the untruncated witness first moment cannot prove nonexistence. Divergence of that mean does not imply a typical cover exists.

A one-point-per-balanced-cell input family has probability exp[−k+O(log k)] and is covered by a fixed interval of roughly 2k centres. It can also satisfy joint standard autocorrelation, Fourier, and energy bounds. Padding these small cores gives divergent unweighted witness counts even under that particular typicality truncation. Stronger legal typicality excluding interval covers removes the family.

A separate Singer-based construction on infinitely many nearby prime cyclic groups gives exceptional deterministic floor-size A with small codegrees, energy O(k²), spectrum O(√k log p), and covers of at most 6k+3 centres. The prime transfer uses the Baker–Harman–Pintz short-interval theorem; it does not assume infinitely many Singer moduli are prime. The construction is contained, up to O(1) extra centres, in eight translates of −A, so it violates the proved bounded-affine-envelope hole condition. It does not defeat every typicality truncation and is not evidence for the random-A limit. Its spectral threshold is weaker than O(√(k log p)), and those bounds are not conflated.

A valid typical event is a specified finite intersection of already proved simultaneous properties. One cannot intersect exclusions over all conceivable singleton centre menus: doing so simply assumes the original negative answer.

## 5 Adaptive construction and exchange obstructions

### Marginal gains and private points

For a sequence of distinct centres let u_i be the holes after i choices, q=1−k/p, and let e_i be the gain above (k/p)u_(i−1). Then exactly

    u_m=pq^m−Σ_i q^(m−i)e_i.

A cap-sized cover needs total positive excess at least (e^(−100)−o(1))p. No such uniform aggregate-excess obstruction is proved. A pointwise mixing estimate for every adaptive residual is false: choosing centres only in G\(A−A) can cover a positive fraction while protecting all of A, leaving centre zero with full marginal gain k. This is a deliberately constrained path, not a description of unrestricted greedy optimization.

For fixed typical A with L=max_{d≠0}|A∩(A+d)|=O(log p/log log p), a uniform m=C√p centre set has about e^(−C)k private points at each selected centre, simultaneously, with high probability. Conditional on t∈T, the exact mean is

    k binom(p−k,m−1)/binom(p−1,m−1).

One exchange of another centre changes that private count by at most L. Almost every candidate is therefore private-rich and still has about e^(−C)p holes. Irredundancy alone pays essentially none of the candidate entropy. Private points chosen after A,T are known cannot be treated as independent certificates.

If every old translate has at least v private points and A+T⊆A+T′ while some centre is deleted, at least v/L new centres must be added. The support-containment condition matters; equal or greater covered cardinality is insufficient. Nonmonotone collective repairs are not excluded.

### Exact centre exchange and variance

For fixed A,T, |T|=m, delete a uniform q-subset of T and add an independent uniform q-subset of G\T. If d_x=|(x−A)∩T|, the miss probability at x is exactly

    (q)_{d_x}/(m)_{d_x} · binom(p−m−k+d_x,q)/binom(p−m,q).

Every global residual optimizer satisfies the corresponding expected-hole lower bounds for all q. At q=1, eventually, they imply N₁≥mkN₀/(p−m−k+1). They do not characterize an optimizer: the p=11 example A={0,1,2}, T={0,1,4,8} has one hole and passes every averaged q-exchange inequality, yet six two-exchanges yield covers.

The final variance-sensitive version retains more information. Let H be the holes after exchange, M=E H, V=Var H, and H_max=min(p,u+qk). If M<H_max,

    min H≤M−V/(H_max−M).

For a true optimum with u holes, δ=M−u satisfies 0≤δ≤qk and V≤δ(qk−δ). Pair probabilities are explicit. Put C_x=(x−A)∩T, s_xy=|C_x∩C_y|, r_xy=|(x−A)∩(y−A)|,

    a_xy=d_x+d_y−s_xy,
    b_xy=2k−d_x−d_y−r_xy+s_xy.

Then P[x,y both missed]=(q)_{a_xy}/(m)_{a_xy} times binom(p−m−b_xy,q)/binom(p−m,q), zero if a_xy>q. Summing gives E H². A uniform quantitative improvement for actual adaptive optimizers is still missing.

For a full random restart conditional on A, the exact variance is

    Var U=pQ_k(1−Q_k)+pΣ_{d≠0}(Q_{2k−r_A(d)}−Q_k²),
    Q_s=binom(p−s,m)/binom(p,m).

The finite-population correction cancels the first-order overlap contribution, yielding Var U=O_C(p+E(A)), hence O(p) under energy O(k²). This random-T variance is not a variance estimate for R_m under random A and does not control the extreme best candidate.

### Restricting a larger parent set

For |S|=K≥k and any T=T(S), let A be a uniform k-subset of S and d_x=|(x−T)∩S|. Exactly,

    E[U(A,T)|S,T]=Σ_x binom(K−d_x,k)/binom(K,k).

A uniform parent S gives the correct uniform marginal A. The interpolation of q(d)=binom(K−d,k)/binom(K,k) is convex because its second difference is binom(K−d−2,k−2)/binom(K,k). Jensen therefore lower-bounds the retained-T expectation by p q̄(Km/p). When K/k→a>1 and m/k→C, that is positive-density order. It is a limitation of retaining the parent T under thinning; it is not a lower bound after reoptimizing T for A.

## 6 Heavy blocks and the budgeted completion problem

Fix δ>0, h=ceil(δk). Repeatedly remove the actual block B_i=T_current∩(x_i−A) when it has at least h elements. The disjoint removed union B lies in X−A with |X|≤floor(c/h), while S=T\B satisfies

    |B|+|S|≤c,   max_y |S∩(y−A)|≤h−1.

Let H_B=G\(A+B). A cover exists precisely when some such actual data admit S covering H_B. Replacing B by the entire envelope X−A can destroy the budget information.

For each fixed R, with high probability simultaneously over |X|=r≤R,

    H_X=G\(X+A−A),  |H_X|=(e^(−r)+o(1))p,
    |(A+s)∩H_X|=0                         if s∈X−A,
    |(A+s)∩H_X|=(e^(−r)+o(1))k            otherwise.           (9)

The proof combines sparse forbidden-graph sampling with an endpoint Lipschitz extension on one shared codegree event; it does not assume a shortest swap path remains typical. Uniform errors and the fixed-R quantifier are essential. Every full or o(p)-hole cover therefore needs at least (1−o(1))k centres outside every bounded pencil union. Spending ≥(99+η)k centres inside one leaves a positive-density residual at the cap.

The fractional completion remains too inexpensive. Give each available centre t∉B weight 1/k. Its convolution is 1−f_{A,B}(y)/k, which equals one on H_B and lies in [0,1] everywhere. Its cost is (p−|B|)/k, and (9) supplies the matching first-order lower bound (1+o(1))k for bounded-pencil B. Even global lightness with threshold h≥2 does not repair this relaxation. It gives no integral rounding theorem.

The exact remaining integer system, on V=G\B, n=p−|B|, m=c−|B|, is

    z_t∈{0,1};  Σ z_t≤m;
    Σ_{t∈(y−A)∩V}z_t≥1      for y∈H_B;
    Σ_{t∈(y−A)∩V}z_t≤h−1    for every y∈G.                 (10)

Every residual neighbourhood has exactly k elements. The actual B and its cost remain in (10).

### Exact-cardinality cylinder obstruction

Take a real uniform m-subset S of an n-set V, with 1≤k≤m<n and 0≤r≤min(k,m,n−m). A cylinder specifies P⊆S and Q∩S=∅, disjoint, with a+b≤r. For a fixed k-set N, u=|P∩N|, v=|Q∩N|,

    E[|S∩N||P⊆S,Q∩S=∅]=u+(m−a)(k−u−v)/(n−a−b).

The sharp minimum over these cylinders is m(k−r)/(n−r). If n≥m+k, the sharp maximum for neighbourhoods of size at most k is

    r+(m−r)(k−r)/(n−r).

Multiply every covering, lightness, box, or budget inequality in (10) by any nonnegative cylinder monomial of degree ≤r and take expectations. The uniform m-set moments satisfy all these inequalities if

    (m−1)r≤mk−n,
    r+(m−r)(k−r)/(n−r)≤h−1                                 (11)

(the second condition is needed for lightness). Constraint products use moments through degree r+1. The law has exact budget pointwise and consistent Boolean moments, but is not supported on covers.

With B=∅, the covering inequalities alone pass through r=floor((ck−p)/(c−1))=(0.99+o(1))k. If |B|/k→β<99, D=100−β>1, and h=ceil(δk), any r=floor(αk) with 0<α<min(1−1/D,δ) passes both tests eventually. This is a barrier for this specified coordinate-conditioned linear mechanism, not for arbitrary nonlinear, semidefinite, or cover-conditioned arguments.

At p=19, A={0,1,2,4}, m=6, r=1, the displayed moments pass all degree-one cover constraints and a lightness limit two, yet exhaustive enumeration gives R₆(A)=1. This is a finite separation at an auxiliary budget; the original coefficient-100 cap is trivial there.

Allowing roughly log k full pencils changes the problem: a high-probability construction makes H_X have at most k points, then patches them with a light S. The envelope costs O(k log k), outside the requested budget. A quantitative hole theorem survives only in a smaller growing-R range, stated in the detailed supplement; it is not a fixed-density or full-budget conclusion.

## 7 Moment certificates and the bounded adaptive score

Uniform high-order Poisson moment matching fails even before one asks for a cover: T=−A has f(0)=k. A light full-budget class can retain subthreshold pencil spikes large enough to destroy every fixed factorial moment of order ≥3 at relevant cutoffs. Clipping preserves the zero set but need not preserve additive realizability: a cap-sized padded pencil can have one value k and all others ≤M<k, so clipping changes total mass from kc to kc−k+M, not divisible by k. Every actual integral translate convolution has total divisible by k.

There is also a parity obstruction. At T=A, off-diagonal representations occur in pairs except at diagonal sums. A union of 100 translates of A, followed by an o(k)-sized correction to reach c, has clipped odd mass o(1), whereas a Poisson law of mean near 100 has positive odd mass. No universal Poisson-law approximation is valid over all these candidates.

A zero-free distribution can match the first 99 factorial moments of Poisson(λ) for λ≥√9900. One exact construction changes the Poisson masses at 0,…,100 by the alternating binomial correction e^(−λ)(−1)^j binom(100,j); the 100th finite difference annihilates lower-degree polynomials. A finite-support version rules out a degree≤99 polynomial zero-indicator minorant with positive Poisson expectation near λ=100. These abstract laws are not claimed to factor as A*T.

A positive minorant exists at degree 201. The Charlier construction in the supplement produces P₁₀₀(x)=(1−x)[Q(x)/Q(0)]², with P(0)=1, P(n)≤0 for all positive integers, and

    E_{Poisson(100)}P=199·99!/(40000·100^99)>0.

A suitably small weighted moment error would give holes. That adaptive moment estimate is unproved, and its uniform unconditioned form is false. The older order-399 Bonferroni certificate remains a valid but higher-degree sufficient bridge, not an independent resolution.

### A bounded score avoids exploding spikes

For 0<q≤1/2 put g_q(n)=(1−n)q^n. It is one at zero and lies in [−q²,0] at positive integers. Thus for the at-most-cap score B_q=min_{|T|≤c}Σ_xg_q(f(x)),

    R_c−q²p≤B_q≤R_c.

The same sandwich holds for the separately defined exactly-c minimum B_q^=. They are not identified: the score is not monotone under padding. A cover implies either score is ≤0. For q²p<1, a nonpositive minimum also implies R_c=0. The exchange bound is c(1+q²), so a positive score expectation on the c√k scale would yield a negative answer by concentration.

The fixed-candidate score mean has a hypergeometric generating-function formula and a Poisson limit. A drift-free compound-Poisson law of mean at most 100 has positive mean score when q<1/100, including clustered and parity laws. A deterministic positive drift destroys this positivity. No adaptive approximation theorem placing every optimizer in this class is proved. Choosing q=o(p^(−1/8)) makes the score-residual difference o(c√k), but then one has merely restated the missing mean estimate at the required precision.

### The exact adaptive selection flux

For any deterministic exactly-m selector T(A), exchange a uniform y∈A with z∉A to form A′. Let

    H_q(A,T)=p^−1Σ_xq^{f_{A,T}(x)},
    D_q=E[H_q(A′,T(A′))−H_q(A′,T(A))].

With X uniform in G, Z=f_{A,T(A)}(X), F=E q^Z, M=E Zq^Z, M₂=E Z²q^Z, λ=km/p, K=k(p−k), exact stationarity gives

    (1−q)M₂+[p−(1−q)(k+m)]M−qkmF=−qK D_q/(1−q).            (12)

Conditional on old multiplicity n, the frozen-selector birth and death probabilities are (k−n)(m−n)/K and n(p−k−m+n)/K. They prove (12); reoptimization flux cannot be silently discarded.

Covariance gives M≤λF and Jensen gives F≥q^λ. Set

    α=1−λq−λ(1−q)(k+m)/p, C_q=qk(p−k)/[(1−q)p].

When α≥0,

    E g_q(Z)≥αq^λ+C_qD_q.                                  (13)

At m=c and fixed q<1/100, the unproved condition liminf kD_q≥0 for a score-minimizing selector would force positive-density mean score and high-probability noncoverage. The unconditional bound is only −(1−q)/k≤D_q≤(1−q)m/(p−k), too weak for (13).

The sign really matters: at p=5,k=2,m=3,q=1/2 a minimizing selector has D_q=−1/30. It is a diagnostic, not a counterexample to the asymptotic sufficient condition. Any zero-free subsequential occupancy limit requires a strictly negative scaled flux for q<1/C; drift-free compound-Poisson limits give nonnegative flux. No theorem excluding the required negative adaptive flux is established.

## 8 Actual additive graphs and exactly normalized counting

Choose one representation a_i+t_j=x for each target x of a genuine cover. This gives a p-edge subgraph J of K_(k,t), with the actual edge label a_i+t_j and a bijection onto F_p. Let v=k+t, h count all connected components including isolated vertices, and r=v−h. The plus-incidence matrix B has rank r over F_p; negating right columns converts it to an oriented incidence matrix.

Let N_J be the number of permutation label vectors in im B. With no coordinate-distinctness requirement, Q_J^all=p^hN_J. Let Q_J impose distinct coordinates within each side. Then Q_J≤Q_J^all, not necessarily equality. For a distinct covering tuple z, R_z=∏_xf_z(x) counts its representation selections, and exactly

    Σ_J Q_J=Σ_z R_z.                                       (14)

All target equations and all cycle constraints remain present.

### Fourier and collision formulas

For ξ∈F_p^p define C_p(ξ)=(1/p!)Σ_{ℓ permutation}exp(2πi ξ·ℓ/p). Orthogonality yields

    N_J=p! p^{−(p−r)}Σ_{ξ∈ker Bᵀ}C_p(ξ).                   (15)

There is also a finite collision-partition formula. For a partition π of the edge set let D_π equate edge labels inside each block and let mob(π)=∏_C(−1)^(|C|−1)(|C|−1)!. Then

    Q_J^all=Σ_π mob(π)p^{v−rank_Fp(D_πB)}.                  (16)

The ranks are in characteristic p. Absolute-value bounds lose the cancellation that enforces distinct labels.

Any nonzero N_J is divisible by p(p−1), through the free affine action on permutation labels. At t=O(√p), the zero Fourier term p!p^{−(p−r)} has logarithm −p+O(√p log p). Thus every feasible graph needs total nonzero-mode contribution at least exp[p−O(√p log p)]. Treating its cycle equations as independent would give a positive count below one. This refutes that graphwise approximation; it does not refute an averaged count supported on a sparse exceptional family.

### Sparse compatible graphs and representation multiplicity

Set λ=kt/p≥1. AM-GM gives R_z≤λ^p. A free affine action on ordered vertex tuples gives Q_J≥p²(p−1) whenever Q_J>0. Therefore

    #{J:Q_J>0}≤(p)_k(p)_t λ^p/[p²(p−1)].                   (17)

Relative to all binom(kt,p) graphs, if λ stays in a compact subset of (1,∞), this is at most exp[−d_λp+O(√p log p)], where d_λ=−(λ−1)log(1−1/λ)>0. At the cap d₁₀₀=0.9949832495…. This is graph sparsity, not random-A failure probability. Balanced integer multiplicities sharpen λ^p to floor(λ)^(p−s)(floor(λ)+1)^s, s=kt−p floor(λ).

For an actual cover let L=max_{d≠0}r_A(d), μ=λ−1>0, and V=L t(t−1)/p−λ+1. The true second-moment identity implies μ²≤E(f−1)²≤V. The convex function log(1+y)/y and size-biased Jensen give

    log R_z≥p(μ²/V)log(1+V/μ).                             (18)

With the proved typical L=O(log p/log log p), (18) gives Ω(p log L/L), improving the earlier Ω(p/L) bound. It is still o(p). Abstract equality cases of that moment inequality are not declared additively realizable. Minimal-cover private-target bounds apply only to minimal covers, not padded cap-sized selectors.

### Canonicality and multiplicity are removed once

Fix a specified noncircular high-probability event H_p. For each successful A let K_c(A) be the lexicographically first c-set covering it. For every graph J define

    W_J=Σ_{z distinct within each side; B_Jz permutation}
          1[A∈H_p]1[T=K_c(A)]/R_z.

Then exactly

    P[H_p and τ≤c]=Σ_JW_J/[(p)_k c!].                     (19)

For each successful unordered A there are k!c! orderings and R_z representation selections for each ordering; the weight cancels precisely the latter. There is no additional p! or division by the number of covers. Removing canonicality counts all covers instead. Dividing by R_z twice undercounts. The public finite normalization checker distinguishes these errors.

Combining (17), (18), and a loose graphwise tuple bound still gives a positive leading exponent p(log100−o(1)) and hence only probability ≤1. Graph support and inverse representation weight must be controlled jointly under canonicality and H_p. The missing sufficient negative inequality is

    Σ_JW_J≤(1−ε)(p)_k c!

on unbounded primes, for fixed ε>0. Nothing in the package proves it.

An equivalent route through a soft minimum retains all additive structure. Put F_c(β;A)=binom(p,c)^−1Σ_{|T|=c}exp[−βU(A,T)]. The exact identity

    Σ_{|T|=t}z^{U(A,T)}=Σ_{X⊆G}(z−1)^|X|binom(p−|X−A|,t)

holds even for complex z. A valid read-k Laplace bound after explicit Bernoulli-to-fixed-size conditioning supplies only order-k suppression against order-k-log-k candidate entropy. The stronger still-unproved bound

    E log F_c(β_p;A)≤−log binom(p,c)−β_p a c√k

would imply μ_c≥a c√k. Dropping high-order cancellation, inverse weights, or canonical restrictions cannot supply that conclusion.

## 9 The exact remaining gap

The strongest unconditional full-budget estimate established here is

    0≤μ_c≤g_c=(e^(−100)+o(1))p.

The lower bound is zero. This interval contains both possible answers to the original question. The following are sufficient missing inputs, not established conclusions:

1. Positive direction: μ_(33k)=o(p^(5/6)), μ_(49k)=o(p^(3/4)), the probability premise in (8), or another complete exact-budget construction.
2. Negative direction: μ_c≥a c√k on unbounded primes; an adequate adaptive bounded-score or exchange-flux bound; a properly normalized weighted-count bound; or an integral infeasibility theorem for the actual budgeted system.

The local-relaxation barriers, exceptional deterministic examples, algorithmic plateaux, divergent witness expectations, and abstract moment laws do not disprove Green's assertion. Conversely, tiny fixed hole densities and good finite auxiliary examples do not prove it. All preserved partial results retain this boundary.

The detailed supplements provide the full proofs and historical qualifications. The public scripts check finite algebra, exact optimization examples, conditioning, graph normalization, and deliberate false variants. They do not test or certify the asymptotic probability limit.
