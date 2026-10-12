# Independent adversarial audit: two exceptional-sum partial results

Audit date: 12 October 2026 UTC. Target: frozen queue row 1741, problem 2350 / Erdős 864.

## Verdict and scope

**MATHEMATICAL PASS for both partial results.** No mathematical correction is required. The first proves a parameter-dependent weighted upper bound and reflected-core concentration near the existing square-root-two upper constant. The second exactly solves the specified macroscopic convolution relaxation and proves its uniform-profile rigidity. Neither closes the original asymptotic gap, improves the unrestricted leading constant, supplies an integer counterexample, or establishes novelty.

The audit independently reconstructs every analytic argument below. It also runs a separately written checker against the defining pair-sum condition. No author checker, imported author routine, or third-party program was executed. No publication or queue modification is part of this audit.

Audited texts:

- Weighted original (see INPUT_PINS.json): 10,287 bytes, SHA-256 `db58f5e14a2ab7aab21e3a942053cb5d3cdbdf0655d87e00adea57cd89572a72`.
- Continuum original (see INPUT_PINS.json): 9,366 bytes, SHA-256 `20d386e616648206d0dc9e5c3a58b444042394f3988dbb54af60dff4cf916da6`. This exact version is accepted without modifying its bytes.

One bibliographic erratum is recorded without editing the author's frozen note: the continuum note's original historical-source title included “and results,” whereas the 1992 paper is *Some of my Forgotten Problems in Number Theory*. This does not change the mathematical verdict.

## 1. Exact target, notation, and source limits

The retained row-1741 statement requires a set A contained in {1,...,N} such that at most one integer T has more than one unordered pair representation a+b, **including a=b**. The proposed upper constant is 2/sqrt(3). The conjecture is not the weak-Sidon variant that omits diagonal pairs, and not the much weaker condition that almost all sums be unique.

I read the retained frozen row, the prior partial proof, and both images of printed pages 39–40 of the original 1992 Erdős paper. These pages state the historical one-exception question and the 2/sqrt(3) benchmark. The retained PDF's 4,630,109 bytes and SHA-256 `51faf4558eacab8e188efbcb028937f75dcb10d37865ab71ef1522df33361c72` were independently rechecked. The original paper's brief formulation does not replace the explicit diagonal-inclusive convention in the frozen target.

Public source: [Erdős, Some of my Forgotten Problems in Number Theory](https://hrj.episciences.org/125/pdf). Fresh audit-time web retrieval of this PDF timed out; the already retained bytes and viewed page images supply the primary-source inspection. A fresh request to [the maintained problem page](https://www.erdosproblems.com/864) returned HTTP 403. No stale website status label is used to claim current global status.

I also directly inspected [the public Erdős Problem a Day working report](https://www.erdosproblemaday.com/report/864). Its structural section already states the difference–reflection lemma and duplicated-difference orbit count. Its ending gives the equivalent symmetric residual in different coordinates. The page identifies itself as an AI working report; its computational records, literature-exhaustion assertions, and numerical extremal values are outside this audit. The inspection confirms that the elementary structural observations must not be promoted here as newly discovered. The two audited notes appropriately make no novelty claim for their main partial results either.

The first note uses k for the size of the complete reflected core; the second uses k for the number of positive radii. They are different quantities. Below I write m=|A|, K=|C| for the full core, and q=|B| for positive radii. In a midpoint-free symmetric set, K=2q; with a midpoint, K=2q+1. I write L_A for A's diameter and R for the positive-radius horizon, avoiding the two notes' different uses of L.

## 2. Independent reflection and multiplicity proof

Assume the exceptional value T exists and put C=A intersect (T-A). If it does not exist, A is Sidon and set C empty. Consider two different ordered representations of one positive difference:

x-y=u-v=d>0.

Then x+v=u+y. Their unordered summand pairs are different: equality of the two multisets would force either x=u and v=y, contrary to the ordered pairs being different, or x=y and u=v, contrary to d>0. This remains valid if either new sum representation is diagonal. By the target hypothesis, x+v=u+y=T, so

(u,v)=(T-y,T-x).

Thus a second representation is uniquely determined by the first; three representations are impossible. All endpoints of a doubled difference belong to C. Conversely a core difference (x,y) has the reflected representation (T-y,T-x). Reflection fixes this ordered pair exactly when x+y=T. Otherwise it gives the second representation.

Let delta indicate whether T/2 belongs to A. Reflection partitions C into p=(K-delta)/2 two-element complementary orbits, plus the possible midpoint. Among its K(K-1)/2 distinct unordered pairs, exactly p are fixed under the corresponding pair-reflection operation. Every remaining pair belongs to an orbit of size two, and each such orbit corresponds to one doubled positive difference. Consequently

D = (K(K-1)/2-p)/2 = (K^2-2K+delta)/4.

This proof includes differences involving the midpoint: a pair (x,T/2) reflects to (T/2,T-x), giving exactly the expected doubled difference. There are no positive zero-difference pairs and no exceptional uncounted diagonal case.

For completeness, ordered additive energy equals ordered difference energy by rearranging a+b=c+d into a-c=d-b. Its zero-difference term is m^2. Positive differences contribute twice their squared multiplicities, so

E(A)=m^2+2[binom(m,2)+2D]
    =2m^2-m+K^2-2K+delta.

This verifies the ancillary identity independently. If no exceptional sum exists, K=delta=D=0 and the ordinary Sidon identity is recovered.

**Convention attack.** If diagonal sum pairs were omitted, A={1,2,3,4} would have only one repeated strict sum, but difference 1 has three representations. Therefore the reflection argument really uses the frozen target convention. It cannot be silently applied to the strict-summand variant.

## 3. Independent weighted-window proof and finite constants

Give points in C weight 1/sqrt(2), and points outside C weight 1. Write u=m-K and

W=u+K/sqrt(2),  Q=u+K/2.

For each d>0, the sum of products of the endpoint weights over all representations a-b=d is at most 1. A singly represented difference has product at most 1. A doubled difference has four core endpoints counted with multiplicity and contributes 2 times 1/2=1. A midpoint shared between the representations changes neither count nor product.

For an integer h>=1, let F(x) be the total weight of A-points in [x-h+1,x], with x an integer. Each point contributes to exactly h windows. Hence sum F=hW. All nonzero windows lie between min(A) and max(A)+h-1, an interval with exactly L_A+h integer points. The count is an upper bound on support size, even if gaps make the actual support smaller.

Two intervals of h consecutive integers displaced by d overlap in exactly max(h-d,0) points. Expanding the square gives

sum_x F(x)^2 = hQ+2 sum_{d=1}^{h-1}(h-d)r_w(d)
              <= hQ+h(h-1).

Cauchy–Schwarz on the finite window support now yields

h^2 W^2 <= (L_A+h) sum_x F(x)^2,

and therefore

W^2 <= (L_A+h)(Q+h-1)/h.                                      (A)

This proves the exact finite inequality for every integer h>=1, rather than only the finitely tested values. For a singleton, h=1 gives equality. The empty set is trivial separately, so no undefined min/max is used.

The explicit error is uniform in T, K, midpoint status, and all of A. Since every positive difference occurs at most twice,

m(m-1)/2 <= 2(N-1).

Thus m-1<=2 sqrt(N), and Q-1<=2 sqrt(N). Choose h=ceil(N^(3/4)). Because L_A<=N-1 and h-1<=N^(3/4), inequality (A) implies

W^2 <= (N+h-1)[1+(Q-1)/h]
    <= (N+N^(3/4))[1+2N^(-1/4)]
     = N+3N^(3/4)+2N^(1/2)
    <= [sqrt(N)+(3/2)N^(1/4)]^2.

Every factor used here is nonnegative for nonempty A, including Q+h-1. N>=1 is sufficient. Taking square roots proves

m-(1-1/sqrt(2))K <= sqrt(N)+(3/2)N^(1/4).                      (B)

There is no unspecified or parameter-dependent constant hidden in (B).

Since K=m-u, multiplying (B) by sqrt(2) gives

m+(sqrt(2)-1)u <= sqrt(2N)+(3/sqrt(2))N^(1/4).                (C)

If m/sqrt(N) tends to sqrt(2), the nonnegative u/sqrt(N) tends to zero. This is a conditional concentration theorem, not an assertion that such a near-extremal sequence exists. If K=o(sqrt(N)), inequality (B) instead gives m<=(1+o(1))sqrt(N).

For alpha=1-1/sqrt(2), a restriction K<=rho m+o(sqrt(N)), 0<=rho<=1, yields m<=[1/(1-alpha rho)+o(1)]sqrt(N); its denominator is bounded away from zero. The stated threshold rho=(1-sqrt(3)/2)/alpha is algebraically correct and gives the conjectured 2/sqrt(3) upper constant only for those restricted families. Setting K=m in (B) recovers sqrt(2), so the theorem cannot be advertised as an unrestricted constant improvement.

## 4. Location-sensitive estimate: independent uniformity check

For an actual exceptional T, put

ell=min(T/2-1,N-T/2).

The lower half C_-={a in C:a<T/2} lies in [max(1,T-N),T/2). This interval has length ell>=0. C_- is Sidon: all its pair sums are strictly below T, including diagonal pairs, so no repeated one is permitted. If s=|C_-| then K=2s+delta.

Here is a uniform Sidon bound without an external asymptotic theorem. Let b_1<...<b_s be an integer Sidon set of diameter at most H. When 1<=v<s, the positive differences b_(i+j)-b_i, for 1<=j<=v and 1<=i<=s-j, are all distinct. There are M=vs-v(v+1)/2 of them, and their sum is at least M(M+1)/2. For each fixed j, telescoping bounds their sum by jH. Therefore M^2<=v(v+1)H and

s <= sqrt((v+1)H/v)+(v+1)/2.

For H>=1, choosing v=floor(H^(1/4)) when s>v gives, for example,

s <= sqrt(H)+(3/2)H^(1/4)+1.

Indeed v>=H^(1/4)/2 and sqrt(1+1/v)-1<=1/(2v). If s<=v the bound is immediate, and H<1 implies s<=1. Thus one uniform bound valid for all H>=0 is the displayed expression with its +1.

Applying this with H=ell gives

K <= 2 sqrt(ell)+3 ell^(1/4)+3.

Substitute in (B), and use ell<=N and N>=1. The result is exactly

m <= sqrt(N)+(2-sqrt(2))sqrt(ell)+O(N^(1/4)),

with an absolute implied constant. Endpoint parity, very small ell, and varying T cause no loss of uniformity. The authored note's less explicit O-term is consequently justified.

## 5. Symmetric reduction, diagonal sums, parity, and midpoint restoration

Translate a reflected set by -T/2 and remove a possible midpoint. It becomes C_0=B union (-B), with B strictly positive. Because the uncentered points were integers, B lies either in the positive integers or in the positive half-integers. Translating changes every sum by the same constant and preserves all multiplicities. Removing one point preserves admissibility and costs only one in cardinality.

For t>0, the number of unordered representations in C_0 is precisely

r_C(t)=s_B(t)+d_B(t),

where s_B counts b+c=t with b<=c, including b=c, and d_B counts ordered positive differences b-c=t. Negative sums have the same counts by reflection. Zero has exactly |B| representations {-b,b} and is the sole permitted exception. Therefore the exact admissibility criterion is

s_B(t)+d_B(t)<=1 for every t>0.                               (D1)

For any finite real B, uniqueness of its unordered sums including diagonals is equivalent to uniqueness of positive differences. The forward implication uses the same cross-sum argument as Section 2. Conversely, two distinct equal-sum pairs can be ordered so that the smallest summand is strictly smaller in one pair, giving two distinct positive differences with the same value. No integrality or distinct-four-summands assumption is needed.

It follows that (D1) is equivalent to:

1. B is Sidon, in the diagonal-inclusive sense;
2. (B+B) intersect D^+(B) is empty.

Condition 2 is equivalent to B intersect (B+B+B) being empty: b_4-b_3=b_1+b_2 if and only if b_4=b_1+b_2+b_3. Every b_i is positive, so the difference automatically has the correct sign. All repetitions are allowed. In particular equations b_4=3b_1 are forbidden.

**Parity attack.** If B lies in Z+1/2, both B+B and B-B lie in Z. They occupy the same sum/difference lattice. There is no automatic parity separation. The reduction nevertheless holds verbatim; my independent checker covers both integer and half-integer radii using twice-radii integers.

**Diagonal attack.** With B={1,3}, the off-diagonal sum set {4} misses the positive difference {2}. But the diagonal sum 1+1=2 collides with 3-1=2, so ±B is invalid. This is why the written B+B must include diagonal sums.

**Midpoint attack.** Inserting 0 into ±B is not automatically valid. In addition to (D1), it requires B intersect (B+B) empty. Indeed the new positive representation 0+b may collide with either a positive sum or a positive difference; the condition B intersect D^+(B) empty is itself equivalent to B intersect (B+B) empty. The new pair 0+0 affects only the permitted zero sum. Example: ±{1,2} is admissible, but adding 0 produces repeated nonzero sums. The first note correctly discards the midpoint and explicitly warns against automatic restoration. The second note deliberately addresses a midpoint-free integer-radius subclass, which is enough for its stated relaxation barrier.

For a symmetric set of diameter L_A=2R, the conjecture would require |B|<=(1/sqrt(3)+o(1))sqrt(L_A), equivalently |B|<=(sqrt(2/3)+o(1))sqrt(R). The ordinary Sidon bound gives only sqrt(R)+O(R^(1/4)). Both notes use the correct normalization.

## 6. Independent derivation of the limiting measure constraints

Use the second note's integer subclass B_R subset {1,...,R}, with q_R=|B_R| and exact packing (D1). Define

nu_R=R^(-1/2) sum_{b in B_R} delta_(b/R).

Distinct positive differences imply q_R(q_R-1)/2<=R-1, so the masses are uniformly bounded. Every sequence R tending to infinity therefore has weakly convergent subsequences on the common compact support [0,1]. Let nu be one limit. Its total mass is the subsequential limit of q_R/sqrt(R); no probability normalization or extra factor two has been inserted.

The exact autocorrelation is

nu_R * tilde(nu_R)
 = (q_R/R)delta_0
   + (1/R)sum_{j=1}^{R-1}d_B(j)[delta_(j/R)+delta_(-j/R)].      (D2)

Since d_B(j)<=1, the off-diagonal measure is bounded by the complete unit-density lattice Riemann measure on [-1,1]. The diagonal coefficient q_R/R tends to zero. Weak convergence of the product measures and continuity of (x,y) mapsto x-y imply convergence of the convolutions; equivalently one can approximate a continuous test function of x-y uniformly by finite sums of products of continuous one-variable functions. Passing to the limit against every nonnegative compactly supported continuous test function gives

nu * tilde(nu) <= Lebesgue measure on all of R.                (D)

The phrase “on all of R” is essential. It includes tests whose support straddles zero. Domination only on the punctured line would fail to exclude an atom; in fact a multiple of delta_0 would satisfy both positive-only inequalities with arbitrarily large mass. The finite diagonal is correctly included and shown to vanish in the authored proof, so that defect does not occur.

Write S_R=(1/R)sum_j s_B(j)delta_(j/R). The exact sum relation is

S_R=(1/2)(nu_R*nu_R)+(1/(2R))sum_{b in B_R}delta_(2b/R).       (D3)

For b<c, the ordered convolution counts the pair twice, while the unordered sum measure counts it once. For b=c, the ordered convolution counts it once, so the positive correction of one-half restores its full unordered weight. This confirms both the sign and factor of the diagonal correction. The correction's total mass tends to zero.

For a nonnegative continuous test function compactly supported inside (0,infinity), use (D1), then (D2) and (D3), and pass to the Riemann-sum limit. This yields

(nu*tilde(nu))|_(0,infinity)+(1/2)(nu*nu)|_(0,infinity)
 <= Lebesgue measure|_(0,infinity).                          (P)

The step uses fixed macroscopic continuous test functions. Measure domination subsequently gives the equivalent inequality for nonnegative Borel tests of the limiting measures. It is not a statement that every arbitrary discontinuous lattice weight or R-dependent microscopic weight may be passed through a weak limit unchanged.

There is no claim that the limiting sum and difference measures retain disjoint supports. Mutually singular discrete measures can have overlapping weak limits. The correct retained relation is (P), exactly as in the authored note.

## 7. Difference domination really implies an L2 density

Let nu be a nonnegative finite measure supported on [0,1] satisfying (D). Choose the even averaging kernel

eta_epsilon = epsilon^(-1) 1_[-epsilon/2,epsilon/2].

It has integral one. By Tonelli, applied to a nonnegative integrand,

||nu*eta_epsilon||_2^2
 = integral (eta_epsilon*tilde(eta_epsilon))(t)
            d(nu*tilde(nu))(t)
 <= integral (eta_epsilon*tilde(eta_epsilon))(t)dt = 1.        (S)

The autocorrelation kernel is nonnegative and integrable. The measure inequality (D), already established across zero, legitimately applies to it. The pointwise form of the identity can also be checked by integrating eta_epsilon(x-a)eta_epsilon(x-b) in x; the resulting triangular kernel is even, so no reflection-sign ambiguity survives.

Select epsilon_n tending to zero. Weak sequential compactness of the L2 unit ball gives a subsequence nu*eta_epsilon_n converging weakly in L2 to some f with ||f||_2<=1. For every compactly supported continuous phi, its integrals against these smoothed densities converge to integral phi dnu by uniform continuity and the approximate-identity property. The same integrals converge to integral phi f dx by L2 weak convergence. Therefore nu=f dx as measures. Positivity and support of nu imply f>=0 and f=0 off [0,1]. Thus

integral_0^1 f^2<=1.                                       (L2)

This proves the desired regularity rather than assuming it from an undefined convolution “value at zero.” No atom, singular component, or hidden mass at an endpoint can survive this argument.

## 8. Exact relaxed optimum, uniqueness, stability, and logical scope

Let the relaxation consist of nonnegative finite measures supported on [0,1] satisfying (D) and (P). For a feasible measure of mass c, (L2) and Cauchy–Schwarz give

c^2=(integral_0^1 f)^2<=integral_0^1 f^2<=1.

If c=1, equality in Cauchy–Schwarz forces f to be constant almost everywhere on [0,1], and its mass forces f=1. Hence the only possible maximizer is uniform Lebesgue measure on that interval.

It is actually feasible. Its difference density is (1-|t|)_+, and its sum density is t for 0<t<1 and 2-t for 1<t<2, zero elsewhere. The positive difference-plus-half-sum density is therefore

1-t/2 for 0<t<2, and 0 for t>2.

This verifies both inequalities, including their correct coefficient one-half and both pieces of the sum convolution. Endpoint values are irrelevant for these absolutely continuous measures. Consequently the relaxed maximum mass is exactly 1, uniquely attained by the uniform measure.

The exact variance identity gives

integral_0^1 (f-c)^2 = integral_0^1 f^2-c^2 <= 1-c^2.

This is genuine L2 stability for feasible limiting densities. It is not L2 convergence of discrete empirical measures, which have no L2 densities. If an actual sequence satisfies q_R/sqrt(R) tending to 1, compactness and uniqueness imply all its weak limit points are uniform; thus the full empirical sequence converges weakly to that profile. This remains conditional on such integer sequences existing.

Similarly, if f vanishes almost everywhere outside a measurable set of length at most a, then c<=sqrt(a) by Cauchy–Schwarz on that set. A positive-radius macroscopic gap deleting the bottom third therefore gives c<=sqrt(2/3). No argument proves that arbitrary admissible sets have this gap, and the authors do not assert one.

Translate ±B_R by R+1 to place it in {1,...,2R+1}; it has 2q_R elements. The target 2/sqrt(3) bound would imply q_R/sqrt(R)<=sqrt(2/3)+o(1). The relaxed feasible uniform measure has mass 1, corresponding formally to the original sqrt(2) leading constant. Therefore **D and P alone do not imply the conjectured constant**, even though they are necessary for integer sets.

This is a counterexample to an analytic implication, not an integer counterexample. There is no constructed sequence of admissible integer sets tending to the relaxed maximizer. Likewise this barrier does not forbid arguments using R-dependent microscopic packing, higher correlations, modular arithmetic, interaction with nonsymmetric outliers, or additional identities. It rules out only an implication from the two stated measure dominations.

## 9. Independent diagnostics and controls

`independent_check.py` was newly written for this audit and does not read, import, or execute either author checker. It verifies pinned proof bytes before its computations. All comparisons involving sqrt(2) are exact integer comparisons: after multiplying weights by sqrt(2), expressions have the form a+b sqrt(2), with b>=0, and are compared by checking a nonnegative remainder and squaring it.

The complete finite run covers:

- Every A subset {1,...,N}, for 1<=N<=16: 131,070 subsets, of which 15,057 meet the original diagonal-inclusive condition.
- All 8,781 admissible exceptional-sum cases in that range, including 4,861 with a midpoint.
- Reflection multiplicity, exact doubled-difference count, ordered energy, preliminary cardinality bound, lower-half Sidon property, orbit count, and location interval.
- Direct window first and second moments and the finite weighted inequality for every h=1,...,N+2 on every nonempty admissible A: 243,711 window tests.
- All 16,384 subsets in each of two 14-site radius universes, one integral and one half-integral: 32,768 parity-tagged tests. The respective admissible counts are 511 and 432.
- Exact symmetric characterization, diagonal sum-measure correction, autocorrelation correction, and the additional criterion for restoring the midpoint.
- Uniform-convolution formulas at 371 exact rational test points, spanning negative, zero, interior, boundary, and outside-support points.
- Three negative controls showing why omitting equal summands, omitting diagonal B+B sums, or restoring the midpoint without a check is wrong.

The normal, Python -O, and Python -OO runs all returned PASS with byte-identical JSON output for the same pinned mathematical input. Checks use explicit exceptions rather than assert statements, so optimization does not disable validation. These are finite diagnostics and checker-integrity controls, not substitutes for Sections 2–8 or a new finite extremal-computation record.

## 10. Accepted claims and remaining problem

Accepted:

1. The weighted finite inequality (A), explicit uniform bound (B), core-concentration consequence (C), restricted-family corollaries, and location-sensitive estimate.
2. The exact midpoint-free symmetric reduction with all repetitions allowed.
3. The necessary weak-limit dominations D/P, their sharp relaxed mass bound 1, unique uniform maximizer, L2 stability, and support-length corollary.

Not established:

- An unrestricted bound below sqrt(2), including the proposed 2/sqrt(3) constant.
- Integer attainability of the relaxed uniform maximizer.
- A symmetric-subclass proof of the conjectured upper constant.
- A general reduction eliminating nonsymmetric additions.
- Priority or novelty of either partial result, or global current literature completeness.

The original gap remains. These two results are accepted as rigorous, carefully bounded partial progress and a method limitation, with no mathematical resolution classification authorized by this audit.

## Public-edition notice

This complete substantive independent audit is reproduced as a historical report. Its references to checker programs, diagnostic outputs, manifests, or source documents identify separately retained evidence; those materials are not distributed here. The original report digest and this edition digest are distinct and recorded in INPUT_PINS.json and MANIFEST.json. Acceptance means internal independent AI review, not external human peer review, journal acceptance, or formal proof-assistant certification.
