# Stage 1 argument 2: fixed-centre entropy bounds and the adaptive-counting obstruction

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 1.

## Result and status

This argument does **not** settle the unrestricted adaptive covering question. It establishes a restricted-family obstruction and proves that two natural unweighted first-moment arguments cannot possibly prove the requested negative answer.

1. A fixed translating set of size at most the exact cap covers with probability at most `exp(-a_100 k + O(log k))`, where `a_100 = -log(1-exp(-100))/100 > 0`.
2. Consequently, with probability tending to one, no translating set in any predetermined family of size `exp(o(k))` covers. Choosing a member of that family after inspecting all of A is allowed. This includes unions of `r=o(k/log p)` arithmetic progressions.
3. The order `exp(-Theta(k))` of a uniform fixed-T bound is optimal: an interval T at the cap has covering probability at least `exp(-k-2)` for all sufficiently large p.
4. The exact expected number of cap-sized covers diverges at least as `exp((99+o(1)) k log k)`. This is not merely an inadequacy in an upper estimate. The single rare outcome that A is an interval already supplies this contribution.
5. Restricting witnesses to inclusion-minimal covers does not repair the first moment. Its expectation diverges at least as `exp((1/2+o(1)) k log k)`.

The missing step is a count sensitive to the joint structure of A and T, or an independently justified typical-A truncation/weighted certificate argument. None is supplied here. No constant-divergence theorem for the optimal adaptive covering number is claimed.

## 1. Exact model and notation

Let p tend to infinity through primes, put `k=floor(sqrt(p))`, `c=floor(100 sqrt(p))`, and choose A uniformly among the k-element subsets of `G=Z/pZ`. For T contained in G write

`E_T = {A+T=G}`.

The target event is `E={there exists T, |T|<=c, E_T}`. Throughout, an admissible T may depend arbitrarily on A. Arguments with a fixed T are used only as components of explicitly stated family-wide arguments.

Since `k^2 <= p < (k+1)^2`, we have `p=k^2+O(k)` and `c=100k+O(1)`. The exact cap is retained in all finite statements. For all sufficiently large p, c is less than p.

## 2. Self-contained fixed-T entropy bound

Let first B be a Bernoulli subset of G, with each point included independently with probability rho, where `0<rho<1`. Fix a nonempty T of size t. For each x put `W_x=x-T`. The event `B+T=G` says that every window W_x contains at least one point of B. Each coordinate belongs to exactly t of the p windows.

We prove

`Pr_rho(B+T=G) <= [1-(1-rho)^t]^(p/t).`                 (2.1)

This is the translate specialization of the bound already recorded in BJR, Remark 4.3, p. 10. The following proof is included to expose the precise assumptions.

Let mu be the product Bernoulli law and, when the covering event has positive probability, let Q be mu conditioned on it. For an arbitrary joint law Q and a product law mu, the regular-window version of the entropy inequality is

`t D(Q || mu) >= sum_x D(Q_Wx || mu_Wx).`              (2.2)

To verify it, order the p coordinates. The entropy chain rule and the fact that conditioning cannot increase conditional entropy give

`H(Q_W) >= sum_{i in W} H_Q(X_i | all coordinates preceding i)`.

Sum over the windows. Every coordinate appears t times, so `sum_x H(Q_Wx) >= t H(Q)`. Meanwhile the cross-entropy terms against the product law sum exactly t times their global value. Subtracting gives (2.2).

Under Q, every W_x is nonempty. If a distribution R is supported on an event F, then

`D(R || nu) = D(R || nu(. | F)) - log nu(F) >= -log nu(F)`.

Apply this with `F={nonempty window}`; its product probability is `1-(1-rho)^t`. Also `D(Q||mu)=-log mu(B+T=G)`. Substitution in (2.2) proves (2.1). If the covering probability is zero, (2.1) is automatic.

Conditioning Bernoulli B on `|B|=k` gives exactly the contract's uniform model. Therefore, for every rho,

`Pr_k(E_T) <= [1-(1-rho)^t]^(p/t) / [binom(p,k) rho^k (1-rho)^(p-k)].`       (2.3)

The denominator is a conditioning probability, not an assumed probability-one size event. Thus the model transfer is explicit.

Take `rho=k/p`. Stirling's formula gives

`Pr_rho(|B|=k) = (1+o(1))/sqrt(2 pi k)`.

For `t=c`,

`(1-k/p)^c = exp(-100)(1+O(1/k))`,

and

`(p/c) log[1-(1-k/p)^c] = -a_100 k + O(1)`,

where

`a_100 = -log(1-exp(-100))/100 = 3.720075976... * 10^(-46)`.

Consequently,

`Pr_k(E_T) <= exp(-a_100 k + O(log k)).`               (2.4)

The implied constants are independent of T. If `|T|<c`, extend T to an arbitrary fixed c-element set. Covering is monotone in T, so (2.4) still holds. This extension is only a proof device; it does not constrain the user's adaptive choice.

The small numerical constant has no bearing on the asymptotic validity, but makes clear that this is not a useful moderate-p numerical bound.

### Optional optimization does not change the exponent scale

One can optimize rho in (2.3). For a fixed multiplicity constant C greater than one and `t=Ck+O(1)`, take `rho=z/k`. The logarithm of (2.3) is at most

`k[(1/C)log(1-exp(-Cz)) + z - 1 - log z] + O(log k)`.

Its minimizing positive z solves `z=1-exp(-Cz)`. The resulting positive rate is

`b_C = 1-z + (1-1/C)log z`.

This improves the constant in the order-k exponent; it cannot supply an order-`k log k` exponent. This optimization is not needed for any conclusion below.

## 3. Restricted adaptive families are excluded

Let `F_p` be a predetermined family of subsets of G, each of cardinality at most c. Suppose `log|F_p|=o(k)`. A union bound using (2.4) gives

`Pr[there exists T in F_p with A+T=G] <= |F_p| exp(-a_100 k+O(log k)) -> 0.`

This statement allows the choice from F_p to depend on every element of A. It is stronger than failure of independently sampled centres, but remains strictly weaker than failure of all T.

As an explicit example, describe a cyclic arithmetic progression using its start, a nonzero difference, and its length in `{0,...,p}`. There are fewer than p cubed such descriptions. Unions of at most r progressions have at most `p^(3r)` descriptions, by padding with empty progressions. Hence all unions of

`r=o(k/log p)`

progressions, subject to the cap, fail to cover with probability tending to one. This includes any bounded number of intervals or progressions, with starts and differences chosen adaptively.

The full collection of c-element T has

`log binom(p,c) = (100+o(1))k log k`,

which lies far outside this theorem.

## 4. No uniform fixed-T bound can be exp(-omega(k))

Take the deterministic interval `T0={0,...,c-1}`. Partition G, in cyclic order, into k consecutive cells whose lengths are either `floor(p/k)` or `ceil(p/k)`. Consider the family of A containing exactly one point in each cell.

The cyclic gaps between consecutive A points are at most `2 ceil(p/k)-1`. For all sufficiently large p this is at most c, since the left side is at most `2k+3` while c is at least 100k. Translates of the interval T0 by A therefore cover the circle.

The number of these A is the product of the k cell lengths. Thus

`Pr_k(A+T0=G) >= floor(p/k)^k / binom(p,k)`.

Using `binom(p,k) <= (ep/k)^k` and `floor(p/k)/(p/k) >= 1-1/k`, for k at least 2 we obtain

`Pr_k(A+T0=G) >= exp(-k)(1-1/k)^k >= exp(-k-2).`       (4.1)

Together with (2.4), this places this fixed T's probability between exponentials of constant multiples of k. In particular, any asserted upper bound `exp(-omega(k))` uniform over all cap-sized T is false. No unresolved adaptive claim is used here.

## 5. Exact raw first moment diverges

For fixed A define

`N_c(A) = number of c-element T such that A+T=G`.

Take the single possible outcome `A0={0,...,k-1}`. Partition G into c consecutive cells of lengths `floor(p/c)` or `ceil(p/c)`. Pick one T point in each cell. Every cyclic gap of T is at most `2 ceil(p/c)-1`, which is at most k for all sufficiently large p. Consequently A0+T=G for every such choice. Choices in disjoint cells give distinct T, so

`N_c(A0) >= floor(p/c)^c`.

As A0 has probability exactly `1/binom(p,k)`,

`E_A N_c(A) >= floor(p/c)^c / binom(p,k)`.

Taking logarithms and using `c=100k+O(1)` and `p=k^2+O(k)` gives

`log E_A N_c(A) >= (99+o(1))k log k -> infinity`.       (5.1)

This proves an intrinsic obstruction to the unweighted first moment

`Pr(E) <= E N_c`.

The right side really is huge; sharpening estimates for the same unrestricted sum cannot make it small. Padding is legitimate for the target event because a smaller cover can be extended to size c.

This does **not** show that random A is coverable. A0 is extremely rare, and many T can be witnesses for the same A. Expectations of witness counts need not approximate the probability of existence.

## 6. Inclusion-minimal witnesses still have divergent first moment

Call a cover T inclusion-minimal if removing any one of its points destroys coverage. This is distinct from minimum cardinality.

For the interval `A0={0,...,k-1}`, let the cyclic gaps of T be `g_1,...,g_m`. The exact conditions are:

- T covers if and only if every `g_i<=k`.
- A covering T is inclusion-minimal if and only if every adjacent sum `g_(i-1)+g_i>k`.

The second statement follows because deleting a centre merges exactly its two adjacent gaps.

Set

`m=ceil(3p/(2k))`, `w=floor(k/24)`, `q=floor(p/m)`.

Partition G into m consecutive cells of lengths q or q+1. In every cell choose its T point among the first w positions. There are exactly `w^m` distinct choices. Every gap lies in the interval

`q-w+1 <= g_i <= q+w`.                               (6.1)

The following exact inequalities suffice:

`w>=1`, `w<=q`, `q+w<=k`, `2(q-w+1)>k`.               (6.2)

They hold for all k at least 24 in the present range of p. Indeed, `p>=k^2` and the definition of m give

`2k/3 - 4/9 < p/m <= 2k/3`,

so `q>2k/3-13/9`. Since `w<=k/24`,

`q+w<=17k/24<k`,

and

`q-w+1>5k/8-4/9`,

whose double is greater than k for k at least 24. These bounds also give `q>=w>=1`.

Thus all `w^m` choices cover inclusion-minimally. Also `m=(3/2)k+O(1)<c` eventually. If M(A) denotes the number of inclusion-minimal covers of size at most c, then

`E_A M(A) >= w^m / binom(p,k)`,

and

`log E_A M(A) >= (1/2+o(1))k log k -> infinity`.       (6.3)

For a concrete arithmetic check, p=1,000,003 gives k=1000, m=1501, w=41, q=666, and allowable gaps between 626 and 707. Adjacent gap sums exceed 1000.

Therefore removing redundant/padded covers alone cannot rescue a negative first-moment proof. One must deal with rare A that carry many genuinely minimal witnesses.

## 7. What Janson and pair-dependence estimates actually give

In the Bernoulli model put `U_x=1_{B intersect (x-T) is empty}`, `U=sum_x U_x`, and `r(d)=|T intersect (T+d)|`. Then

`mu=E U=p(1-rho)^t`,

`E(U_x U_(x+d))=(1-rho)^(2t-r(d))`.

The dependency differences are exactly `D=T-T`. In the ordered-pair, diagonal-included convention used in the BJR proof, the Janson quantity is

`Delta=p sum_{d in D}(1-rho)^(2t-r(d))`.

Because `Delta>=p |D| (1-rho)^(2t)`,

`mu^2/Delta <= p/|D|`.                               (7.1)

Thus when `|T-T|>=eta p` for a fixed eta greater than zero, this standard Janson exponent is at most `1/eta`. Refining r(d) inside the same raw joint-probability expression cannot make this exponent tend to infinity in that case. The inequality is not asserting a lower bound on the true covering probability; it diagnoses the weakness of this particular upper bound.

The coarser BJR estimate `Delta<=t^2 mu` gives `Pr(U=0)<=exp(-mu/t^2)`. At `t~100k`, `p~k^2`, its exponent is only a constant. The read-t/entropy bound of Section 2 improves the exponent to order k, but Section 4 shows that no uniform improvement to order `k log k` is possible.

For the exact uniform model define

`b(s)=binom(p-s,k)/binom(p,k)`,

with b(s)=0 when p-s is less than k. Direct counting gives the exact moment identities

`E U=p b(t)`,

`Var U=p sum_{d in G}[b(2t-r(d))-b(t)^2]`.             (7.2)

Disjoint windows have negative covariance in this model. They cannot simply be treated as independent Bernoulli events. Replacing the Janson joint-probability Delta by a sum of covariances is not an instance of the quoted theorem. Even a small variance by itself supplies a polynomial-type second-moment bound, not the exponential family-wide estimate needed here.

## 8. Precisely what remains missing

Any negative result must control optimal adaptive T for a positive proportion of A along arbitrarily large primes; high-probability failure would be stronger. Neither fixed-T rarity nor the restricted-family theorem accomplishes that.

A potential truncated first-moment route would need an independently established typical event H_p with `Pr(H_p)=1-o(1)` and a proof such as

`sum_{|T|=c} Pr(A in H_p and A+T=G)=o(1)`.

The interval outcomes responsible for Sections 5-6 could be removed by a suitable H_p, but removing those examples is not a proof of this inequality. No such adequate typical event and estimate have been obtained.

A weighted count or an entropy-compression/container argument could instead identify many witnesses for the same A and avoid charging them independently. It would need a proved exhaustive certificate theorem, a count of certificates, and bounds on the number/probability of A compatible with each certificate. Simply stating that structured T are few, that small-overlap windows are nearly independent, or that a random covering algorithm fails does not supply those ingredients.

There is also a basic atomic warning: any fixed T that covers even one k-set A has probability at least `1/binom(p,k)=exp(-(1+o(1))k log k)`. A proposed `exp(-Omega(p))` estimate for such T is impossible in the uniform model. Strong bounds for a purported unstructured class must therefore either prove that no k-set covers those T, or explicitly exclude atypical A rather than ignoring this atom.

## 9. Independent audit and finite sanity checks

A separate audit of this argument checked the entropy/KL sign, conditioning cost, the coefficient 99 in (5.1), all rounding inequalities in Section 6, the ordered Janson convention against the primary PDF, and (7.2). No material defect was identified.

The historical entropy-reduction checker additionally read those independent exact cover counts and verifies (2.3), with rho=k/p, by integer arithmetic after raising to the t-th power. All 23 cardinality cases at p=5,7,11 pass. It also verifies the Section 6 sufficient parameter inequalities for all 39,825 integers p with 24<=floor(sqrt(p))<=200, and both cap-cell gap inequalities for all 30,401 integers p with 100<=floor(sqrt(p))<=200. The historical output pin identifies the exact synthetic snapshot used. This particular larger run is not included in the lightweight public replay.

These are sanity checks, not evidence for a high-probability conclusion beyond the proved restricted theorem. Small primes cannot meaningfully test the unrestricted cap 100, which exceeds the group order there.

## Sources and scope

- B. Bollobas, S. Janson and O. Riordan, *On covering by translates of a set*, arXiv:0910.3815v2. The inspected complete PDF, pp. 8-10, gives the Janson calculation and Remark 4.3's stronger read-t/Newman bound. Public URL: https://arxiv.org/pdf/0910.3815v2 . These tools alone do not settle the square-root regime.
- D. Gavinsky, S. Lovett, M. Saks and S. Srinivasan, *A Tail Bound for Read-k Families of Functions*, arXiv:1205.1478, Theorem 1.2 and the entropy discussion. Public URL: https://arxiv.org/pdf/1205.1478 . Used as an independent primary-source check on the read-family inequality, not as a theorem about adaptive translates.
- The exact target, rounding, and scope restrictions are those in the supplied construction contract and source-scope audit. No substitute Bernoulli, composite-group, fixed-k, or independent-centre model is claimed to resolve them.

 This is part of the shared Stage 1, not a new pass.

