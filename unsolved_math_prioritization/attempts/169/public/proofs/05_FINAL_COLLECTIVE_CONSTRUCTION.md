# Stage 5: collective construction and the final unrestricted gap

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 5.

## Decision

No full affirmative construction, unconditional polynomial-scale smaller-budget mean, or verified negative answer was obtained. The exact original question remains unresolved. This is not a conclusion that a particular algorithm's failure establishes noncoverage.

The useful new positive result is a probability-amplification theorem: it would suffice to construct a 33k-centre near-cover with residual o(p^(5/6)) on a set of inputs of probability exp[-o(p^(1/6))]. A constant positive probability of a 33k-centre complete cover is already sufficient. Uniform-subset concentration then upgrades that small-budget event to a near-cover on almost every input, and the previously proved collective shift-and-repair construction finishes within the original cap. The required initial event has not been constructed with that probability.

An exact second-moment exchange condition also goes beyond averaged stationarity, and an exact random-restriction identity preserves every dependence on the parent optimizer. Neither gives the missing unconditional input. The strongest established unconditional residual upper bound remains of positive-density order, including at 33k and 49k.

Throughout, p is prime, k=floor(sqrt(p)), A is a uniform k-subset of G=Z/pZ, c=floor(100sqrt(p)), and

R_m(A)=min_{|T|<=m}|G\\(A+T)|.

All optimizers may depend on the whole A. The m=0 case is deterministic; concentration below assumes 1<=m<=p and k>=1. No result substitutes a product group or an untransferred Bernoulli sample.

## 1. A sharper unrestricted concentration constant

For fixed T, consider A=B union {a} and A'=B union {a'}, where |B|=k-1. Write S=B+T. Both sumsets are obtained from S by adjoining at most |T| new points. Hence

||A+T|-|A'+T|| <= |T| <= m.

This is a cardinality bound, not the looser symmetric-difference bound 2m. Comparing against a minimizer at each endpoint in turn gives

|R_m(A)-R_m(A')| <= m.                                      (1.1)

Expose a uniform k-subset through the first k positions of a random ordering. Conditional completions after two possible next elements can be coupled by exchanging those two elements; the completed sets agree or differ by one swap. Conditional expected residuals therefore differ by at most m. Each Doob increment has absolute value at most m. The conservative Azuma inequality gives, with mu_m=E R_m,

Pr(R_m <= mu_m-u), Pr(R_m >= mu_m+u)
 <= exp[-u^2/(2km^2)]  for u>=0.                            (1.2)

This improves the earlier conservative denominator 8km^2 by a factor of four, without changing any exponent scale. Optimizer stability, independence of centre sets, and a union bound over their number are unnecessary. No variance-O(p) claim for the optimum is made.

In particular, the negative sufficient bridge strengthens to

Pr(R_c=0) <= exp[-mu_c^2/(2kc^2)].                            (1.3)

A bound mu_c>=a c sqrt(k) on an unbounded prime subsequence, with fixed a>0, would give failure probability at least 1-exp(-a^2/2) there. No positive lower estimate for mu_c is established.

## 2. Positive-probability near-covers suffice

Suppose v>=0 and

alpha=Pr(R_m<=v)>0.

If mu_m<=v the following bound is immediate; otherwise apply (1.2) with u=mu_m-v and solve for mu_m. In either case,

mu_m <= v+m sqrt(2k log(1/alpha)).                           (2.1)

If alpha=1, the support bound R_m<=v almost surely gives mu_m<=v directly. A proved lower bound alpha>=a>0 can be used in place of alpha on the right. This theorem does not assume how the successful near-cover was found.

### Exact budget and rounding

For integers r>=1 and rm<=c, put

b=c-rm,     B=[(b+1)p^(r-1)]^(1/r).

The previously audited collective amplification theorem states

tau(A) <= rm+floor(R_m(A)^r/p^(r-1)).

It uses r relatively shifted copies of the same A-dependent near-cover, then one translate for each remaining hole. It follows exactly that

tau(A)>c  implies  R_m(A)>=B.                               (2.2)

There is no independence hypothesis. The b+1 is retained because the number of repaired holes is integral.

Combining (1.2), (2.1), and (2.2) proves the finite bound

Pr(tau>c)
 <= exp[-(B-v-m sqrt(2k log(1/alpha)))_+^2/(2km^2)].          (2.3)

Here x_+=max(x,0). If the bracket is nonpositive, the bound is the trivial one. Formula (2.3) remains valid when alpha is replaced by any proved positive lower bound for it.

### Consequence at 33k

Take m=33k and r=3. Since c>=100k, b>=k, and in fact b=k+O(1). Thus

B=(1+o(1))p^(5/6),
B^2/(2km^2)=(1+o(1))p^(1/6)/(2*33^2).

If one proves an event R_(33k)<=v_p of probability at least alpha_p, where

v_p=o(p^(5/6)),    log(1/alpha_p)=o(p^(1/6)),                 (2.4)

then (2.3) gives

Pr(tau>floor(100sqrt(p))) <= exp[-Omega(p^(1/6))].            (2.5)

In particular, a fixed positive probability of a 33k-centre complete cover, or even of an o(p^(5/6))-hole near-cover, would suffice. A quantitative version allows log(1/alpha_p) of order p^(1/6), provided its coefficient leaves a fixed positive gap in the bracket of (2.3).

For fixed r and m asymptotic to Ck, with c-rm a fixed positive k-scale margin, the corresponding sufficient regime is

v_p=o(p^(1-1/(2r))),
log(1/alpha_p)=o(p^(1/2-1/r)),                               (2.6)

for r>2. The exponent is zero at r=2, so a fixed positive success probability does not yield the same high-probability conclusion through this concentration argument at the 49k budget. The separate previously proved hypothesis E R_(49k)=o(p^(3/4)) remains sufficient by Markov and two-copy repair.

### Why the available rare complete covers do not supply (2.4)

Partition the cyclic group into k successive blocks of lengths floor(p/k) and ceil(p/k). A with one point in each block is covered by an interval of at most 2ceil(p/k)-1 centres. Its exact probability is

product_j |block_j| / binom(p,k) = exp[-k+O(log k)].

The gap bound follows by looking at two successive blocks, including the cyclic wrap. The probability asymptotic follows from Stirling and k^2/p->1. These are genuine covers with ample budget margin. However, their proved probability has logarithmic cost of order k=p^(1/2), far above the p^(1/6) allowance at 33k. Even using more copies at their smaller approximately 2k budget leaves a strictly smaller power than p^(1/2) in (2.6). This says that this known rare family does not close the new bridge; it does not upper-bound the probability of unrestricted small-budget covers.

## 3. What multiscale optimization actually guarantees

The shift argument extends to arbitrary nonnegative integer budgets m_1,...,m_r:

R_(m_1+...+m_r)(A)
 <= floor[product_i R_(m_i)(A) / p^(r-1)].                   (3.1)

Repeated application of the two-budget inequality proves this with the same A throughout. If a nonempty A is fixed, singleton repair gives a complete cover at cost at most

sum_i m_i+floor[product_i R_(m_i)(A)/p^(r-1)].               (3.2)

Thus genuinely unequal scales and different A-dependent near-covers are allowed. Formula (3.2) can be optimized over a complete residual profile. It is not necessary to assume that all stages use the same optimizer or have equal budgets.

What is missing is an input better than the ordinary averaging guarantee at some scale. Substituting R_(m_i)<=p exp[-km_i/p+o(1)] for a fixed number of k-scale stages gives only

p exp[-k sum_i m_i/p+o(1)]

holes before repair. Under a total O(k) budget this is still a positive-density upper bound. This calculation is solely the result of substituting the known estimates into (3.1); it is not a lower bound on the output of a multiscale algorithm, nor a prohibition on a better alignment of the hole sets.

## 4. Strongest unconditional bounds justified here

There is a slightly sharper integer version of the usual universal upper bound. Define

g_0=p,
g_(i+1)=g_i-ceil[k g_i/(p-i)]   for 0<=i<=p-k,

and g_i=0 for i>p-k+1. Then for every A of size k,

0<=R_i(A)<=g_i.                                             (4.1)

Indeed, if i distinct centres have left u holes, selected centres contribute zero incidence to those holes. Each hole has k potential covering centres among the remaining p-i centres. Some new centre covers at least ceil(ku/(p-i)) holes. For i<=p-k the map u -> u-ceil(ku/(p-i)) is nondecreasing on the integers. Induction therefore bounds the actual greedy residual by g_i, and the optimum is no larger. At i=p-k+1 every A+T covers G by the elementary pigeonhole argument.

Put Q_i=binom(p-k,i)/binom(p,i). For 1<=i<=p-k+1,

p Q_i-i < g_i <= p Q_i.                                    (4.2)

At i=0 both sides equal p with the lower inequality non-strict. The product recurrence for pQ_i has multiplier 1-k/(p-i). The rounded recurrence subtracts an additional number in [0,1), so the accumulated discrepancy is nonnegative and less than i. This proves (4.2), including the zero terminal product.

Consequently the unconditional mean bounds actually available are

0<=E R_(33k)<=g_(33k)=(e^(-33)+o(1))p,
0<=E R_(49k)<=g_(49k)=(e^(-49)+o(1))p,
0<=E R_c<=g_c=(e^(-100)+o(1))p.                              (4.3)

The O(k) rounding improvement does not alter their leading powers. The right sides in the first two lines, divided by p^(5/6) and p^(3/4) respectively, diverge. This does not say that the true means diverge at those ratios; it says that these upper bounds fail to establish the required estimates.

For completeness, these estimates do furnish the ordinary unconditional full cover with logarithmic overhead. Sampling s centres and repairing the expected residual gives

tau(A)<=s+floor[p binom(p-k,s)/binom(p,s)].                   (4.4)

Taking s=ceil[(p/k)log k] for sufficiently large p gives

tau(A)<=(p/k)(log k+1)+1=(1+o(1))sqrt(p)log(sqrt(p)).         (4.5)

This is an actual complete-cover guarantee, but it is eventually larger than 100sqrt(p). A tiny fixed coefficient e^(-100) in (4.3) cannot be treated as a vanishing power of p.

## 5. Random restriction with a fully adaptive parent cover

A natural attempt is to start with a larger random set S, find a collective cover there, and restrict back to k elements. The exact identity is as follows.

Fix |S|=K>=k and any T=T(S), |T|=m. Sample A uniformly among the k-subsets of S. Put

d_x=|(x-T) intersect S|.

Then, conditional on the full S,T,

E_A |G\\(A+T)| = sum_x binom(K-d_x,k)/binom(K,k).             (5.1)

If S was initially a uniform K-subset of G, the marginal A is exactly the required uniform k-set. Therefore an actual construction of T(S), together with an upper estimate on the right side of (5.1), would yield an upper bound for E R_m(A). Merely knowing S+T=G gives d_x>=1, which does not provide the needed estimate.

The convexity check is informative about the proposed thinning step. Let q(d)=binom(K-d,k)/binom(K,k), with impossible selections zero. Its piecewise-linear interpolation on 0,...,K is convex: for k>=2, its second discrete difference is

q(d)-2q(d+1)+q(d+2)=binom(K-d-2,k-2)/binom(K,k)>=0.

For k=1 it is linear. Since sum_x d_x=Km, Jensen gives

sum_x q(d_x)>=p q_bar(Km/p),                                (5.2)

where q_bar denotes that interpolation. For K/k tending to any fixed number a>1, m/k->C, and fixed d, q(d)->(1-1/a)^d. Thus the right side of (5.2) is a positive constant times p in that regime, even for optimally balanced parent multiplicities.

This is a statement about the expected holes of the retained parent T under random restriction. It is not a lower bound on E R_m(A), because after seeing the restricted A one may choose a different T. Reoptimizing, selecting among many parent constructions, or adding a collective repair remains possible. No bound for that reoptimization was proved. If K-k is much smaller, (5.2) can shrink, but obtaining a sufficiently good cover of such a barely enlarged parent is itself unproved.

## 6. Resampling beyond averaged stationarity

A direct attack on collective descent should retain fluctuations, not just the average exchange formula. Here is an exact strengthening available for every A,T.

Let |T|=m, u=|G\\(A+T)|, and choose a uniform q-subset D of T to delete and an independent uniform q-subset B of G\\T to add, for 1<=q<=min(m,p-m). Write H=|G\\(A+((T\\D) union B))|, M=E H, and V=Var H.

For every outcome,

0<=H<=H_max:=min(p,u+qk).

If M<H_max, a support-and-variance inequality gives

min H <= M-V/(H_max-M).                                   (6.1)

To prove it, let h=min H. The nonnegative product (H-h)(H_max-H) has expectation (M-h)(H_max-M)-V. Rearranging proves (6.1). If M=H_max, H is constant and min H=M.

If T is a global residual minimizer, every exchange has H>=u. With delta=M-u, the stronger necessary condition is

0<=delta<=qk,
V <= delta(qk-delta).                                      (6.2)

The same expectation calculation uses the actual support [u,u+qk]. In particular, an actual optimum with zero mean drift must have zero exchange variance. A positive-variance exchange with sufficiently small drift can produce a genuine improving move via (6.1). This is more information than the linear histogram inequalities alone.

### Exact pair formula needed to evaluate V

Put N_x=x-A, C_x=N_x intersect T, d_x=|C_x|. For x,y let

s_xy=|C_x intersect C_y|,
r_xy=|N_x intersect N_y|,
a_xy=d_x+d_y-s_xy,
b_xy=2k-d_x-d_y-r_xy+s_xy.

The probability that both x,y are uncovered after the exchange is exactly

(q)_(a_xy)/(m)_(a_xy)
 * binom(p-m-b_xy,q)/binom(p-m,q),                           (6.3)

with value zero if a_xy>q. Deletion must contain C_x union C_y; addition must avoid (N_x\\T) union (N_y\\T). These two choices are independent, which proves the formula. It includes x=y. Summing (6.3) over ordered pairs gives E H^2, and subtracting M^2 gives V. This keeps the actual additive overlap geometry rather than imposing a Poisson law.

A proof that an improving exchange exists at every relevant noncover would need to control both M-u and V uniformly for the evolving, fully adaptive T, or use an explicitly justified multi-step escape. No such estimate is established. The exact earlier plateau example p=11, A={0,1,2}, T={0,1,4,8} has u=1; at q=1 it has M=2 and V=8/7, compatible with no improving one-swap move. Its q=2 neighborhood does contain covers, but (6.1) with the universal H_max does not certify that minimum. Thus the stronger formula is a usable exact descent test, not a theorem that arbitrary collective resampling succeeds.

## 7. Precise final original gap

The unconditional statements established here and in the prior accepted passes do not decide whether R_c=0 with probability tending to one.

A positive answer would follow from any of the following still-unproved inputs, with full unrestricted optimizers:

- E R_(33k)=o(p^(5/6));
- E R_(49k)=o(p^(3/4));
- the small-probability near-cover event (2.4), which the new concentration-and-amplification theorem converts into a complete exact-budget cover;
- another collective construction with a proved net cost at most c and no remaining holes.

A sufficient negative input remains E R_c>=a c sqrt(k), with fixed a>0 on unbounded primes. The established unrestricted lower bound at c is only zero. The fact that every predetermined candidate, simple construction family, or typical full random restart leaves holes does not fill this gap.

The proposed closure attempts preserve their actual limits: multiscale shift alignment still needs a better initial residual; random restriction needs a parent multiplicity estimate and/or a justified reoptimization; variance-sensitive exchange needs quantitative control of adaptive joint overlaps. None supplies the missing expectation or probability estimate.
