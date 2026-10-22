# Proofs and exact controls

These statements concern the continuous-time binary-Yule Derrida–Retaux model defined in REPORT.md. Its established existence, uniqueness, and tree representation are imported from Hu–Mallein–Pain, Theorem 1.8. All subsequent deductions are given here. These partial results do not settle the general two-part question. Several elementary identities reproduce known results; no priority is asserted.

## Proposition 1. Mass balance and finite-time positivity certificates

Let m_0=E[X_0]. If m_0=∞, then E[X_t]=∞ for every finite t. If m_0<∞, write m(t)=E[X_t] and q(t)=P(X_t>0). Then m is locally absolutely continuous, m'=m−q almost everywhere, and

F = e^(−t)m(t) − ∫_t^∞ e^(−s)q(s) ds.

In particular F≥0 exists, and F=0 if and only if m(t)≤1 for every t≥0.

**Proof.** In the tree representation, the root amount is at most the sum of the independent initial leaf amounts. A rate-one binary Yule process started from one particle has E[N_t]=e^t; thus m(t)≤e^t m_0 when m_0 is finite. Each jump adds an independent μ_t amount, and the downward speed is 1_{X_t>0}. Taking expectations in the stochastic integral equation is justified by this locally integrable upper bound, giving

m(t)=m_0+∫_0^t(m(s)−q(s))ds.

Therefore d(e^(−t)m(t))/dt=−e^(−t)q(t) almost everywhere. The left side is nonincreasing and nonnegative, so it has a nonnegative limit F. Integration to infinity gives the asserted identity.

When F=0, it gives m(t)=∫_0^∞e^(−u)q(t+u)du≤1. Conversely, if m(t)≤1 for every t, its exponentially rescaled limit is zero. Moreover, F≥e^(−t)(m(t)−1), giving the finite-time positivity certificate.

For infinite initial mean, use the event that the tree has no split before time t, which has probability e^(−t). Conditional on that event its root amount is (X_0−t)_+, which has infinite expectation. Thus the unconditional mean is infinite for each finite t. ∎

## Proposition 2. Uniform tail and second-moment controls at zero free energy

If F=0, then for all t,x≥0,

P(X_t≥x)≤min(1,e^(1−x)),   E[X_t²]≤1/2.

Consequently the family of laws is tight and uniformly integrable, and sup_t E[X_t^k]<∞ for every positive integer k.

**Proof.** By Proposition 1, m(t)≤1. Fix s≥0 and put independent μ_t amounts at the leaves of a Yule tree of height s. At any binary merger, (a+b−c)_+≥(a−c)_++(b−c)_+ for a,b,c≥0. Induction through the finite tree therefore bounds the root amount below by the sum over leaves of (X_t^(u)−s)_+: the total root-to-leaf length is s. It follows that

m(t+s)≥e^s E[(X_t−s)_+]≥e^s P(X_t≥s+1).

The first claimed bound follows by taking s=x−1 when x≥1; when x<1 the bound by one suffices. Integration of this common exponential tail bounds every fixed positive moment uniformly, and supplies uniform integrability.

Apply the generator to x², using the moment bounds to justify truncation. Independent copies X,Y have E[(X+Y)²−X²]=m_2+2m², and drift contributes −2m. Hence

m_2'=m_2−2m+2m².

Multiplying by e^(−t), integrating from t to T, and letting T→∞ yields

m_2(t)=2∫_0^∞ e^(−u)m(t+u)(1−m(t+u))du≤1/2.

Here the terminal term vanishes because m_2 is uniformly bounded; 0≤m≤1 and x(1−x)≤1/4 complete the proof. We use only the non-strict bound. ∎

## Proposition 3. The atom–exponential family

Let μ_0=p_0δ_0+(1−p_0)Exp(λ_0), with 0≤p_0≤1 and λ_0>0. Its laws have the same form with parameters solving

p'=(1−p)(λ−p),   λ'=−λ(1−p).

For p_0<1 the free energy is zero exactly when

λ_0>1 and p_0≥λ_0(1−log λ_0).

The case p_0=1 is identically δ_0 for every λ_0. At a nontrivial critical point 1<λ_0≤e, p_0=λ_0(1−log λ_0),

λ(t)−1∼2/t,   P(X_t>0)=1−p(t)∼2/t²,   E[X_t]∼2/t².

**Proof.** Write q=1−p. The density on (0,∞) is qλe^(−λx). Its convolution with the full measure has positive density

2pqλe^(−λx)+q²λ²xe^(−λx).

The weak evolution on x>0 is ∂_t f=∂_x f+(μ*μ)|_(0,∞)−f. Equating the coefficients of x and 1 gives λ'=−qλ and p'=q(λ−p). The boundary flux at zero is qλ; convolution changes the atom by p²−p=−pq, giving the same p' and verifying the full weak equation. Existence and uniqueness identify this family with the given process.

The rectangle 0≤p≤1, λ>0 is invariant: at p=0 the vector field points inward, at p=1 it vanishes, and λ(t) cannot reach zero at finite time since −λ≤λ'≤0. The constant

H=p/λ+log λ

has derivative zero. Thus p=h(λ):=λ(H−log λ) and λ'=−λ[1−h(λ)]. For p_0<1, uniqueness keeps p(t)<1 at finite t and λ is strictly decreasing.

If λ has a positive limit a, its differential equation forces h(a)=1. A limit a<1 is impossible: h'(a)=1/a−1>0, so h(λ)>1 for λ just above a, contradicting p≤1. A limit a=1 is possible only when H=1 and λ_0>1. When λ_0≤1 the limit must therefore be zero. If λ_0>1 and H<1, h has global maximum exp(H−1)<1, so again λ→0. If λ_0>1 and H=1, the first root of h(λ)=1 encountered while λ decreases is a=1. If λ_0>1 and H>1, that first root is the larger root a>1. The condition H≥1 is exactly p_0≥λ_0(1−log λ_0).

In the positive-limit cases p→1 and m=q/λ→0, so F=0. In the remaining cases λ→0, and

λ(t)e^t=λ_0 exp(∫_0^t p(s)ds).

The integral converges: after substituting the decreasing variable λ,

∫_0^∞p(s)ds=∫_0^λ_0 [H−log x]/[1−x(H−log x)] dx.

The denominator stays positive on the interval, and near zero the integrand is O(1+|log x|), which is integrable. Thus λ(t)e^t→K∈(0,∞), p(t)→0, and e^(−t)m(t)→1/K>0.

For critical initial parameters, put a(t)=λ(t)−1>0. The invariant H=1 gives

q=1−λ+λlog λ=a²/2+O(a³),
a'=−(1+a)q=−a²/2+O(a³).

Since a→0, (1/a)'→1/2. Integrating gives a∼2/t, and hence q∼2/t² and m=q/λ∼2/t². ∎

**Comparison corollary.** If X_0 is stochastically dominated by a zero-free-energy member of the above family, then X_t→0 in probability and F=0. Couple the initial leaf amounts in their usual monotone coupling on the same finite tree. Every merger and erosion map is increasing, so the root amounts preserve the order. The dominating family has m(t)→0 by the proof. This proves the assertion by Markov's inequality and comparison of expectations. No universal domination assertion is made.

## Proposition 4. A pinned law passing all the listed time-zero necessary tests

Take X_0 with exponential rate 5/2. Then F>(2/5)e^(−40)>0, but the four classes of inequalities listed in Approach 2 of REPORT.md all hold at time zero.

**Proof of positive free energy.** Here p_0=0, λ_0=5/2, H=log(5/2)<1 since e>8/3>5/2. The invariant curve is p=x log(λ_0/x) for 0<x≤λ_0. Its maximum is λ_0/e<15/16. Thus 1−p>1/16. In the integral I from Proposition 3,

I=∫_0^λ_0 log(λ_0/x)/[1−x log(λ_0/x)] dx
 <16∫_0^λ_0 log(λ_0/x)dx=16λ_0=40.

The expression for K gives F=λ_0^(−1)e^(−I)>(2/5)e^(−40). The inequality e>8/3 follows, for instance, from the exponential series: its terms through degree three sum to 8/3 and all later terms are positive. No numerical integration is used.

**Proof of the tests.** Its tail is e^(−5x/2)≤e^(1−x) for every x≥0. The moment identities follow by integrating the exponential density:

E[X²]=8/25,   E[e^X]=5/3,   E[Xe^X]=10/9.

For 0<θ<1, put λ=5/2. Direct integration gives

E[(1−θX−2(1−θ)X²)e^(θX)]
= λ[(λ−θ)²−θ(λ−θ)−4(1−θ)]/(λ−θ)³
= λ[2(θ−7/8)²+23/32]/(λ−θ)³>0.

All denominators are positive and the numerator has an exact positive-square certificate. Thus these tests, even taken together at time zero, are insufficient for F=0. ∎

**Why these are necessary tests, and why the sign is not invariant.** For 0<θ<1 let g=E[e^(θX_t)], h=E[X_t e^(θX_t)], j=E[X_t²e^(θX_t)], and b=2(1−θ). Under F=0 the uniform tail bound makes all these quantities uniformly finite and permits differentiation. With p=P(X_t=0),

g'=g²−(1+θ)g+θp,
h'=(2g−1−θ)h−g+p,
j'=(2g−1−θ)j+2h²−2h.

For φ=g−θh−bj this implies

φ'=(2g−1−θ)φ+2b(h−h²)−g²+θg.

Since g≥1 and h−h²≤1/4, the last three terms are ≤b/2−(1−θ)=0. If φ were negative at some time, this inequality and 2g−1−θ≥1−θ>0 would force φ to tend to −∞. Its uniform boundedness rules that out. Hence φ≥0.

Letting θ↑1 requires more than the crude tail bound. The needed finite E[Xe^X] and the corresponding necessity E[Xe^X]≤E[e^X] are imported specifically from HMP Proposition 6.6(4); our counterexample has both moments finite by direct integration. No interchange at θ=1 is inferred from the tail bound alone.

Where these moments and the generator calculation at θ=1 are justified, D=E[(1−X)e^X] obeys

D'=2(g−1)D−g(g−1),   g=E[e^X].

For Exp(2), at t=0, g=2 and D=0, whence D'(0)=−2. This directly disproves preservation of the zero-sign boundary. The needed moments are finite in a time neighborhood of zero by Proposition 3, as λ(t) starts at 2>1.

## Proposition 5. A sufficient exponential-moment extinction criterion

Suppose θ>1 and g_0=E[e^(θX_0)]<θ. Then with c=θ−g_0>0,

E[e^(θX_t)]−1≤(g_0−1)e^(−ct),   t≥0.

Thus E[X_t]≤(g_0−1)e^(−ct)/θ, F=0, and X_t→0 in probability.

**Proof.** First cap every initial amount at K and cap a merged amount at K immediately after each merger in the finite tree construction. This defines bounded nonlinear dynamics on [0,K]. The same root decomposition as for the uncapped tree gives its generator with jump map min(K,x+y) and the usual reflected erosion. Write g_K(t)=E[e^(θX_t^K)] and p_K(t)=P(X_t^K=0). For these bounded variables the generator identity and e^(θ min(K,x+y))≤e^(θ(x+y)) give

g_K'≤g_K²−(1+θ)g_K+θp_K≤(g_K−1)(g_K−θ)

almost everywhere. The bounded test function calculation supplies local absolute continuity. Scalar differential-inequality comparison against y'=(y−1)(y−θ), with y(0)=g_0, shows 1≤g_K(t)≤y(t)≤g_0. This comparison also holds if equality occurs initially, by the standard integrating-factor argument for locally Lipschitz scalar fields: for the positive part of g_K−y, its upper derivative is bounded by a local Lipschitz constant times that positive part, and Gronwall gives zero.

Therefore (g_K−1)'≤−c(g_K−1) almost everywhere and

g_K(t)−1≤(g_0−1)e^(−ct).

For fixed t the Yule tree is finite almost surely and all initial leaf amounts are finite almost surely. As K increases, every capped root amount is increasing. Once K exceeds the sum of all its uncapped leaf amounts, no cap acts anywhere in this fixed tree, so its root amount equals the uncapped root amount. Thus X_t^K↑X_t in this coupling. Monotone convergence passes the displayed estimate to E[e^(θX_t)]. Finally e^(θx)−1≥θx and Markov's inequality give the remaining conclusions. ∎

For X_0=a deterministic, the condition is e^(θa)<θ. The maximum of log θ/θ over θ>1 is 1/e, attained at θ=e, proving the stated sufficient interval 0≤a<1/e. No conclusion about the endpoint a=1/e is needed or asserted here.

## Proposition 6. Stationary laws and the remaining convergence gap

The only finite-mean stationary probability law of this dynamics is δ_0. Furthermore, if F=0 and μ_t has a weak limit as t→∞, that limit is δ_0.

**Proof of stationary-law exclusion.** Let μ be stationary with finite mean. Then F=0 and Proposition 2 gives the exponential tail bound. Its moment-generating function M(z)=∫e^(zx)μ(dx) is analytic for |z|<1, with nonnegative Taylor coefficients. Put p=μ({0}). Substitution of the exponential test into the stationary generator identity is justified for real z<1 by the tail bound and independent-sum integrability; analytic continuation then gives

M(z)²−(1+z)M(z)+zp=0,   |z|<1.

The root with M(0)=1 is

M(z)=[1+z+√(1+2(1−2p)z+z²)]/2,

where the square root is the branch equal to one at zero. If p=1, the measure is δ_0. If p=0, this identity gives M(z)=1+z near zero, hence E[X]=1 and E[X²]=0, impossible for a nonnegative random variable.

Suppose 0<p<1. The discriminant has two distinct nonreal roots, each of modulus one. At each root the square root has a genuine nonremovable branch point: if M were analytic there, the analytic function 2M−1−z would square to a function with a simple zero, which is impossible. Consequently the Taylor series of M at zero has radius of convergence exactly one. But the displayed expression is analytic in a neighborhood of the positive real point z=1, since its discriminant there equals 4(1−p)>0. This contradicts the following elementary lemma.

**Positive-coefficient lemma.** A power series f(z)=Σ_(n≥0)a_n z^n with a_n≥0 and finite radius R>0 cannot be analytic at z=R by analytic continuation from its original disk.

To prove the lemma, assume an analytic extension exists in a disk centered at R of radius δ>0. Choose r<R sufficiently close to R, so a disk centered at r of radius δ/2 is contained in that extension disk and r+δ/4>R. Taylor's series centered at r converges absolutely at y=r+δ/4. Its coefficients satisfy f^(k)(r)/k!=Σ_(n≥k) binom(n,k)a_n r^(n−k)≥0, because r<R. Tonelli and the binomial theorem then give

Σ_(k≥0) [f^(k)(r)/k!](y−r)^k = Σ_(n≥0)a_n y^n <∞.

This contradicts radius R because y>R. ∎

**Proof of the conditional limit assertion.** For finite-mean laws μ,ν, couple leaf amounts with expected absolute difference arbitrarily close to their 1-Wasserstein distance. Erosion is 1-Lipschitz and addition has total Lipschitz constant one in each coordinate. On a fixed Yule tree, the difference of root amounts is at most the sum of leaf differences. Taking expectation yields

W_1(S_sμ,S_sν)≤e^s W_1(μ,ν),

where S_s is the law semigroup. Under F=0, Proposition 2 supplies tightness and a common exponential tail. If μ_t converges weakly to μ, these tail bounds imply convergence in W_1 and finite mean of μ. For fixed s≥0, continuity of S_s and the semigroup property give

S_sμ = lim_(t→∞)S_sμ_t = lim_(t→∞)μ_(t+s) = μ.

So μ is stationary and must be δ_0 by the first part. This proves the conditional assertion.

**Exact limitation.** A subsequential weak limit of μ_t is not known to be stationary merely because the trajectory is tight. The above argument uses convergence of the whole trajectory, so that μ_(t+s) has the same limit. Replacing that missing convergence by tightness would be circular. Nothing in this proposition excludes periodic, recurrent, or other nonconvergent law trajectories. ∎
