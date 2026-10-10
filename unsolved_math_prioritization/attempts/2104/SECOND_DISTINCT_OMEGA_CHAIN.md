# Repaired distinct-prime-factor chain and the fixed-epsilon barrier

## Statement and scope

This is a bounded correction and projection of a prior proof, not a novelty claim.

Write omega(m) for the number of distinct prime factors of a positive integer m. The corrected sieve argument below establishes an absolute constant C>0 and infinitely many integers n such that

omega(n-k) <= C log k for every integer 2<=k<n.       (O1)

It follows that there is one fixed epsilon>0 and infinitely many integers N such that

m + epsilon omega(m) <= N for every positive integer m<N.    (O2)

This is the fixed-small-coefficient relaxation of Erdős problem #413. It does not establish coefficient 1. It makes no assertion about the stronger multiplicity-counting function Omega.

The starting construction and exact local factors are those in Cheuk Fung (Joshua) Lau, *On the Number of Prime Factors of Consecutive Integers*, arXiv:2604.15042v2 (24 June 2026), https://arxiv.org/pdf/2604.15042v2, §§5–6. The inspected PDF has SHA256 `90443d4ebbdfe9e05052e1a8115b8acd9d29d3ce7269d7e9c71cb09716c718d1`, 717637 bytes. The false absolute-value identity on p.28 is replaced by the authored argument in `SECOND_KERNEL_REPAIR.md`. This document provides the remaining chain specifically for distinct prime factors, rather than importing the manuscript's prime-power moment arguments.

All constants below are independent of x and k. The smoothing function and all fixed numerical parameters are chosen once.

## 1. Parameters and a single probability distribution

Let x tend to infinity, L=log x, and set

A=10, w=0.15 L, K=floor(L^0.001), K_plus=floor(x^0.01),
W=product_{p<=w} p^4.

For 1<=k<=K let R_k=exp(L/(100 k^50)) and ell_k=log R_k. For K<k<=K_plus set R_k=w. For each 2<=k<=K_plus put

r_k=ceil(4 log k), T_k=exp(L/(100 log k)).

Then 3<=r_k<=10 log k, including k=2. For k<=K, R_k<=T_k, since log k<=k^50. For any j<=r_k and distinct primes p_i<=T_k, their product d obeys

d<=T_k^r_k<=x^0.1.                                  (O3)

In particular (O3) holds for primes p_i<=R_k when k<=K.

Choose the fixed smoothing function eta from the construction on p.20: real, even, supported on [-1,1], eta(0)=1, 0<=eta<=1, Gevrey of order 2, with nonnegative Fourier transform h. Such a function is obtained by normalized autocorrelation of a nonzero nonnegative Gevrey-2 bump supported on [-1/2,1/2]. Put tilde_eta(u)=exp(-u)eta(u). Its Fourier representation is

tilde_eta(u)=integral_R h(t) exp(-(1+it)u) dt,

and h(t)<=C exp(-c sqrt(|t|)) for fixed C,c>0. For example this decay follows directly from repeated integration by parts and |eta^(m)|<=B^m(m!)^2, using m!<=m^m and m of order sqrt(|t|/B); it does not require the erroneous direction of a Stirling inequality appearing in the source's derivation.

Define the nonnegative weight

nu(n)=1_[x,2x](n) 1_{W|n}
      * product_{a=1}^K [sum_{d|n-a, (d,product_{p<=w}p)=1}
                          mu(d) tilde_eta(log d/ell_a)]^2.

Only d<=R_a contribute. The construction uses n-a rather than the source's n+a. This merely changes the congruence n=-a to n=a; all compatibility conditions depend on differences of the shifts and are unchanged.

Below we prove that Z=sum_n nu(n)>0 for sufficiently large x and choose n with probability nu(n)/Z. This is one distribution for all k simultaneously. The auxiliary r_k and T_k vary with k; the weight nu does not.

## 2. Exact arithmetic-to-Fourier formula and its uniform error

This section verifies the prerequisite of the kernel replacement in the range used here.

Expand all squares in nu. There are at most product_a R_a^2 nonzero coefficient choices, and each coefficient has absolute value at most one because 0<=tilde_eta(u)<=1 for u>=0. Moreover

log(product_a R_a^2)=(L/50) sum_{a<=K} a^(-50)
<=L/49<0.021 L.

The inequality follows from sum_{a>=1}a^(-50)<=1+integral_1^infinity t^(-50)dt=50/49.

Let q_a=[d_a,d'_a]. All prime factors of q_a exceed w. If a prime divides q_a and q_b for distinct a,b<=K, the congruences n=a (mod q_a), n=b (mod q_b) would force it to divide a-b, impossible because |a-b|<K<w. Thus contributing q_a are pairwise coprime. Their congruences are also coprime to W.

For a target shift k and squarefree d=p_1...p_j with primes>w, adding n=k (mod d) is compatible precisely when every overlap with q_a has p|(k-a). For each p>w, there is at most one such a<=K. Compatible congruences specify one residue class, whose count in [x,2x] is its density times x, with error O(1). Summing all coefficient errors gives O(x^0.021), uniformly in d.

Fourier-expand each tilde_eta and use the squarefree Möbius coefficients. The resulting exact density factor F_d has local factors

p not dividing d: 1-sum_{a=1}^K b_{p,a},
p dividing d with the unique compatible coordinate a:
 (1/p)(1-exp(-(log p/ell_a)(1+it_a)))
      (1-exp(-(log p/ell_a)(1+it'_a))),
p dividing d without such a coordinate: 1/p,

where b_{p,a} is the three-term expression defined in `SECOND_KERNEL_REPAIR.md`, §2. Consequently

P_k(d):=sum_n nu(n)1_{d|n-k}
=(x/W) integral_{R^(2K)} F_d(t,t') product_a h(t_a)h(t'_a) dt_a dt'_a
 +O(x^0.021).                                        (O4)

For d=1 there is no target condition and P_k(1)=Z. These formulas are absolutely convergent for each x; the positive real exponents are 1/ell_a.

Uniformly in all Fourier variables,

|F_d| <= (4^j/d) exp(O(K log L)).

Indeed |b_{p,a}|<=3/p^(1+1/L), since ell_a<=L, and zeta(1+1/L)=O(L). A union bound over 2K Fourier coordinates and the decay of h permit truncation to |t_a|,|t'_a|<=H=L^0.2 with error

O((4^j x/(Wd)) exp(-c L^0.1)).                       (O5)

Here c>0 has been reduced to absorb O(K log L), since K log L=o(L^0.1). The arithmetic error O(x^0.021) also fits (O5). To see this, the prime number theorem gives W=x^(0.6+o(1)), hence W<=x^0.61 eventually; together with (O3), x/(Wd)>=x^0.29. The margin 0.29-0.021 absorbs exp(-cL^0.1). No one-sided claim W<=x^0.6 is needed.

The same proof with j=0 gives the truncation formula for Z.

## 3. Repaired normalization and medium-prime factorial moments

Apply the detailed argument in `SECOND_KERNEL_REPAIR.md` to (O4)/(O5). With

c0=integral_0^infinity [(exp(-u)eta(u))']^2 du>=1,
C_a=(W/phi(W))/ell_a,
M_x=(x/W)c0^K product_a C_a,

it gives

Z=(1+o(1))M_x>0,
P_k(d)/Z <= C_B 8^r/d                               (O6)

for j<=r=r_k, p_i in (R_k,T_k], with an absolute C_B and all sufficiently large x uniformly in k. If that prime interval is empty, its factorial moments are zero. In particular no assumption R_k<T_k is needed when k>K.

For clarity, the essential uniform corrections are

||H_1-1||=O(K^2/w)=o(1),
||H_d||<=exp(O(K^2/w+jK/w))<=(1+o(1))2^j,

g_a=C_a A(1+O(L^(-0.7))) on the truncated box,

and the shifted finite-difference integrals cost at most 4 per paired divisor factor. A factor D^K is never introduced. The cost of the single-coordinate errors is (1+O(L^(-0.7)))^K=1+o(1).

## 4. The required repaired small-prime factorial moment

Only 2<=k<=K is considered here. Let r=r_k. For every 1<=j<=r we claim

sum_{w<p_1,...,p_j<=R_k, distinct}
 Pr(p_1...p_j | n-k) <= (C_C log(r+2))^r.             (O7)

The primes in (O7) are ordered, as appropriate for a factorial moment. This is the restricted form of Proposition 5.5(C) needed here. It is not a certification of all its arbitrary-A parameter ranges.

Because p>w>K and k<=K, every divisor factor acts on the same coordinate k. For an ordered prime tuple P let d=product P and

U_P(t,u)=product_{p in P}(1-exp(-(log p/ell_k)(1+it)))
                       (1-exp(-(log p/ell_k)(1+iu))),
B_P=integral_R2 |A(t,u)| |U_P(t,u)| h(t)h(u) dt du.

In the exact factorization F_d=(1/d)(product_a g_a)U_P H_d, expand H_d in nonnegative-translation monomials. Its coefficient norm is at most (1+o(1))2^j. Integrate the K-1 unaffected coordinates using the contraction estimate of the kernel replacement. Each contributes at most C_a[c0+O(L^(-0.7))D+tau_H]. Integrate coordinate k absolutely, using |g_k|<=C_k(1+O(L^(-0.7)))|A|. Every extra positive-translation monomial has modulus at most one. Thus, after normalization by Z, the main contribution for this tuple is at most an absolute constant times

2^j B_P/d.

The factor c0^(-1) can be omitted since c0>=1, and the accumulated unaffected-coordinate error is 1+o(1).

Use |1-exp(-a(1+it))|<=min(2,a(1+|t|)) for a>=0, and bound the primed factor by 2. Removing the distinctness restriction only enlarges the nonnegative sum, so

sum_P B_P/d
<=2^j integral_R2 |A(t,u)| h(t)h(u) S(t)^j dt du,

where

S(t)=sum_{p<=R_k} (1/p) min(2,(1+|t|)log p/log R_k)
<=C(1+log(1+|t|)).                                  (O8)

To justify (O8), split at log p=2 log R_k/(1+|t|). The lower portion is bounded using sum_{p<=y}(log p)/p<=C log y; the upper portion uses the upper Mertens bound for the prime harmonic sum. If the split falls below 2, the full prime harmonic sum is at most C+log log R_k<=C'(1+log(1+|t|)). Thus the estimate is uniform, including large |t|.

The elementary kernel bound

|A(t,u)| <= (1+|t|)(1+|u|)/2

and Gevrey decay now give

sum_P B_P/d <= (C log(r+2))^r.                       (O9)

Here is a uniform moment justification for (O9). After integrating u, it is enough to bound

integral_R (1+|t|)(1+log(1+|t|))^r exp(-c sqrt(|t|)) dt.

On |t|<=M(r+2)^4, the logarithmic factor is at most (C log(r+2))^r, while the remaining integrand has a fixed finite integral. Choose a fixed M sufficiently large in terms of c. On the complement, r log(1+log(1+|t|))<=(c/2)sqrt(|t|); the remaining integral with exp(-(c/2)sqrt(|t|)) is bounded by a fixed constant. Polynomial factors and fixed constants are absorbed by enlarging C. Since j<=r, the same bound applies to exponent j.

The additional 2^j from ||H_d|| is absorbed into C in (O9).

It remains to sum the truncation errors. The harmonic sum of primes up to R_k is O(log L). Therefore the normalized sum of (O5) is bounded by

exp(-cL^0.1+O(K log L)+O(r log log L)).

For k<=K, r=O(log L), so this tends to zero uniformly. Thus it is absorbed in (O7). This proves the needed small-prime factorial moment without extracting a frequency-dependent error from a complex integral.

## 5. Ordinary moments, including the finite small-k range

For a given k let

X_1(k)=sum_{w<p<=R_k}1_{p|n-k},
X_2(k)=sum_{R_k<p<=T_k}1_{p|n-k}.

When k>K, X_1(k)=0. Empty prime intervals give zero sums. Write r=r_k. For any nonnegative integer-valued X,

X^r=sum_{j=1}^r S(r,j)(X)_j,

where S(r,j) are Stirling numbers of the second kind and (X)_j is the ordered falling factorial.

For X_1, (O7) gives

E X_1^r <= B_r(C_C log(r+2))^r <= (C_1 r)^r,          (O10)

where B_r=sum_j S(r,j) is the Bell number. One convenient self-contained bound follows from its exponential generating function exp(exp(z)-1): positivity of coefficients and z=(1/2)log(r+1) yield

B_r <= r! exp(sqrt(r+1)-1) [(1/2)log(r+1)]^(-r)
<= [2e r/log(r+1)]^r for r>=3.

The ratio log(r+2)/log(r+1) is bounded. Thus C_1 is absolute, and (O10) includes r=3 at k=2.

For X_2, set lambda_k=sum_{R_k<p<=T_k}1/p. Uniformly in k,

lambda_k <= C_lambda log k <= C'_lambda r.           (O11)

If k<=K, log T_k/log R_k=k^50/log k, and an upper Mertens estimate gives (O11). If k>K and T_k>w, lambda_k<=C+log log x<=C' log k because log k>log K and log K is asymptotic to 0.001 log log x. If T_k<=w the sum is zero.

From (O6),

E X_2^r <= C_B 8^r sum_{j=1}^r S(r,j)lambda_k^j
         <= (C_2 r)^r.                              (O12)

For the last inequality, the exponential generating function of the sum is exp(lambda_k(exp(z)-1)). Bounding its r-th coefficient at any fixed positive z small enough in terms of C'_lambda, and using r!<=r^r, gives an absolute constant to the r-th power times r^r. The fixed factor C_B is absorbed because r>=3.

Choose one absolute B sufficiently large that (O10)/(O12) and r<=6 log k imply

Pr(X_i(k)>B log k)<=exp(-r)<=k^(-4), i=1,2.           (O13)

For example it is enough that 6 max(C_1,C_2)/B<=exp(-1). The same B works for all k>=2 and all sufficiently large x. No growing-k approximation excludes the finitely many smallest shifts.

## 6. Positive probability of all logarithmic bounds at once

By the union bound,

Pr(some 2<=k<=K_plus violates X_1(k)<=B log k or X_2(k)<=B log k)
<=2 sum_{k=2}^infinity k^(-4)<1.

A simple numerical-free bound is sum_{k=2}^infinity k^(-4)<=1/16+integral_2^infinity t^(-4)dt=5/48, so the displayed failure probability is at most 5/24.

On the complementary event, count the other prime factors. Since W|n, every prime p<=w dividing n-k also divides k. These primes contribute at most

omega(k)<=log k/log 2.

Primes p>T_k contribute at most

log(n-k)/log T_k <= log(2x)/(L/(100 log k)) <=200 log k

for sufficiently large x. If T_k<w, this last estimate may also count some primes already included in the tiny-prime bound; that is harmless for an upper bound. Every prime factor exceeding w is in one of the displayed middle ranges or exceeds T_k.

Hence some integer n in [x,2x] satisfies, simultaneously for all 2<=k<=K_plus,

omega(n-k)<=[1/log 2+2B+200] log k.                  (O14)

For K_plus<k<n, the deterministic estimate omega(n-k)<=log(2x)/log 2 is sufficient. Since k>=floor(x^0.01)+1>x^0.01,

omega(n-k)<= (200/log 2) log k

for all sufficiently large x. Taking one fixed C to be the maximum of these two constants proves (O1) for this n.

This argument works for every sufficiently large x with the same eta, A, B and C. Taking x=3^j for arbitrarily large integers j gives n_j in the disjoint intervals [3^j,2*3^j], hence infinitely many distinct witnesses.

## 7. One fixed epsilon and the endpoint shift

For every witness n from (O1), set N=n-1. Let m be any positive integer with m<N. Then k=n-m is an integer with 2<=k<n, so

omega(m)<=C log k.

For all integers k>=2, log k<=(k-1)log 2. This follows from k<=2^(k-1), proved by induction. Fix once and for all

epsilon=1/(C log 2)>0.

Then

m+epsilon omega(m)
<=m+log k/log 2
<=m+k-1=n-1=N.

Thus every positive m<N is included. The endpoint m=N-1 corresponds to k=2, not to the unavailable k=1. The witnesses N=n-1 remain infinite and unbounded. This proves (O2) with one fixed positive coefficient.

## Acceptance boundaries

This chain uses:

- the explicitly specified positive sieve weight;
- compatible CRT counting with a uniform error, checked in §2;
- the authored kernel normalization/divisor correction in `SECOND_KERNEL_REPAIR.md`;
- the newly proved restricted small-prime factorial estimate in §4;
- standard prime number theorem/Mertens bounds, elementary moment identities, and a union bound.

It does not use Proposition 5.5(D) or (E), prime-power moments, the p.16 uniform-in-m estimate, or the claimed Omega version of the main theorem. It does not establish a coefficient-1 barrier. It also does not show that the printed proof is correct as written: its p.28 identity remains false and the replacement argument is substantive.

The stronger Omega theorem and the coefficient-1 version of Erdős problem #413 remain outside this acceptance. The scientific claim assessed here is precisely the corrected omega-only logarithmic barrier and its fixed-epsilon consequence.

## Publication-edition scope clarification

This is the complete earlier distinct-only review, retained at its original
mathematical scope. The separate SECOND_MULTIPLICITY_AUDIT.md extends that
acceptance to the full corrected backwards omega<=Omega logarithmic theorem,
using fixed A=100 and s=ceil(4 log k). Its all-endpoints fixed-positive-epsilon
consequence is also accepted. Earlier statements that the full Omega theorem
is outside this document's acceptance describe this document alone; they are
not the final disposition of this edition. Coefficient one remains unresolved.

All mathematical acceptance here is independent internal AI review of the
specified authored arguments. This AI-assisted work is unrefereed; no external
human peer review, journal acceptance, or formal proof-assistant certification
is claimed. No novelty claim is made.
