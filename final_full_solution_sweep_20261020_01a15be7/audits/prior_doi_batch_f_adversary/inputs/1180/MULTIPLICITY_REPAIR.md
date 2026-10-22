# Authored repair of the multiplicity-counting consequence

This note continues the correction of the authenticated prior proof in Lau, arXiv:2604.15042v2, https://arxiv.org/pdf/2604.15042v2 . It is not a novelty claim. The false uniform prime-sum estimate on PDF page 16 is not used or asserted here. The independent distinct-omega reconstruction remains valid separately.

## 1. Scope and fixed parameters

Use the same backwards-shift probability weight and fixed smoothing function as DISTINCT_OMEGA_RECONSTRUCTION.md and the exact-Euler integration correction in KERNEL_REPAIR.md. Retain L=log x, K=floor(L^.001), w=.15L, W=product_{p<=w}p^4, and R_k=x^(1/(100k^50)) for k<=K, R_k=w otherwise. Now fix

    A=100,  T=x^(1/(1000 log k)),  s=ceil(4 log k),
    2<=k<=x^.01.

One still has 3<=s<=6 log k<A log k, T^s<=x^.006, and, for k<=K, R_k<=T and R_k^s<=x^.06. Indeed k^50>=10 log k for every integer k>=2. All CRT and Fourier formulas remain uniform. The normalization does not depend on A or on the queried k or s:

    Z=sum_n nu(n)=(1+o(1))(x/W)c0^K product_{r<=K} C_r,
    Z>=x^(.4-o(1)),
    C_r=(W/phi(W))/log R_r,  c0>=1.

The configuration count in the expansion of the squared sieve weight is at most x^.021. These facts will be used to bound signed-sum errors by absolute coefficient sums.

The arguments for the ordinary distinct-prime contributions X and Y in DISTINCT_OMEGA_RECONSTRUCTION.md §§4–5 continue to hold with this A. The interval prime-harmonic estimates change only an absolute constant, and the summed small-prime-range Fourier errors remain uniform. Hence for one absolute B,

    E X^s <=(B log k)^s,   E Y^s <=(B log k)^s,

where X counts distinct primes in (w,R_k] and Y those in (R_k,T], with empty ranges interpreted as zero. The stronger general first-power estimate

    P(p_1...p_j|n-k) << 8^s/(p_1...p_j)              (G)

also holds for any distinct p_i>w, p_i<=T, j<=s, regardless of whether p_i<=R_k. In the exact-Euler repair the local factor U_p is treated by a positive-translation contraction whenever it exists; that argument never requires p>R_k. Products of the imposed primes are at most T^s<=x^.006, so the CRT/Fourier error bounds apply.

## 2. Uniform higher-power comparison from signed main terms

For distinct p_1,...,p_j>w, each <=T, and any integers a_i>=2, let d=product p_i, D=product p_i^a_i, and b=product p_i^(a_i-1). Then for all sufficiently large x,

    |P(D|n-k)-P(d|n-k)/b| <= x^(-.3).              (HP)

There is no restriction D<=x in this assertion. To prove it, expand the sieve weight into its divisor configurations. A compatible base configuration restricts n to one residue class modulo

    q=W lcm([d_1,d'_1],...,[d_K,d'_K]).

At any p>w, q has exponent at most one because all divisor variables are squarefree and different shift coordinates cannot share p. If the imposed first-power conditions are incompatible with the base class, both indicators vanish. Otherwise imposing d gives one class modulo lcm(q,d); imposing D gives one class modulo lcm(q,D), with

    lcm(q,D)=b*lcm(q,d).

Both interval counts are their length-x densities plus O(1), uniformly even for moduli larger than x. Their density main terms cancel in the difference count(D)-count(d)/b. Since b>=1, the error for a configuration is bounded by an absolute constant, and its coefficient has modulus at most one. Thus the absolute unnormalized error is O(x^.021). Divide by Z>=x^(.4-o(1)); the result is O(x^(-.379+o(1))), which is at most x^(-.3) for sufficiently large x. This proves (HP) uniformly in all the primes and exponents. The proof preserves signed main terms and uses absolute coefficients only for the O(1) errors.

## 3. High-prime-power moments with a deliberate error margin

Let

    U=sum_{w<p<=T} sum_{a>=2, p^a<=2x} 1_{p^a|n-k}.

This is the extra multiplicity from primes above w and at most T. If T<=w, U=0. Otherwise the number Q of prime-power indicators in this finite sum satisfies

    Q<=T log(2x)/log w.

If Q=0 the error count is already zero. Otherwise, since T>w, one has log k<L/(1000 log w). Therefore, using s<=6 log k, for all sufficiently large x,

    log(Q^s)
      <=s(log T+log(2L))
      <=.006L + .006L log(2L)/log w
      <.02L.

In particular Q^s<=x^.02. This is the explicit uniform margin that is absent when one allows the moment order to use the entire original cutoff budget. We need only the fixed order s=ceil(4 log k), not the strongest general-order claim in the manuscript.

Expand U^s into its Q^s indicator tuples. Group tuple positions into blocks according to equal primes. For a block of size m at a prime p, the joint condition uses the maximum exponent a, and the number of exponent assignments with that maximum is at most a^m. By (HP) and (G), for r distinct block primes and their maximum exponents a_i, the joint probability is at most

    M 8^s / product_i p_i^a_i + x^(-.3)

for an absolute M. The total contribution from the comparison errors is at most Q^s x^(-.3)<=x^(-.28).

For the main terms define, after harmlessly dropping the restrictions p<=T and distinctness,

    W_m=sum_{p>w} sum_{a>=2} a^m p^(-a).

For w>=4 and a>=2 the integer integral bound gives sum_{p>w}p^(-a)<=2^(1-a). Also a^m<=m! binom(a+m-1,m). Hence

    W_m<=sum_{a>=1}a^m 2^(1-a)<=2^(m+1)m!.

The sum over partitions of {1,...,s} of the product of their block weights is the s-th exponential-series coefficient:

    sum_partitions product_blocks W_{|block|}
       =s! [z^s] exp(sum_{m>=1} W_m z^m/m!).

At z=1/4, the exponent is at most sum_{m>=1}2^(m+1)(1/4)^m=2. Positivity of coefficients yields an upper bound e^2 s!4^s. Therefore

    E U^s <= M e^2 8^s s!4^s + x^(-.28)
           <=(B_U s)^s <=(B'_U log k)^s            (UM)

for absolute constants. This bounds the complete extra multiplicity, not just indicators with p^a<=T. The upper bound p^a<=2x is automatic for a divisor of n-k>0.

This proves the needed moment bound without the invalid standalone estimate sum (log p)^(-m-1)<<T/(log T)^(m+2). It also avoids the intricate simplex error calculation that used that estimate. Only the actually required fixed moment orders are claimed.

## 4. Uniform small-prime excess and its summable tail

Let S be any subset of the primes p<=w with p^4|k, write e_p=v_p(k)>=4, and choose integers h_p>=1. Then

    P(v_p(n-k)-v_p(k)>=h_p for all p in S)
       <=product_{p in S}p^(-h_p)+x^(-.3).         (SP)

For each compatible base divisor configuration, q has exponent exactly 4 at these small primes. The new congruence n congruent to k modulo p^(e_p+h_p) is compatible with W because p^4|k, and multiplies q by p^(e_p+h_p-4). This factor is independent of the configuration. Put beta=product p^(-(e_p+h_p-4))<=product p^(-h_p). If M0 denotes the signed density main sum of the original expansion, then its restricted main sum is exactly beta*M0. The unrestricted mass is M0+O(x^.021), and the restricted mass is beta*M0+O(x^.021). Subtract beta times the first from the second, bound the interval-count errors absolutely, divide by Z, and use beta<=1. This proves (SP) uniformly, even when the extra modulus is larger than x. No termwise multiplication of inequalities by signed Mobius coefficients occurs.

Now put

    V=sum_{p<=w, p^4|k} (v_p(n-k)-v_p(k))_+,
    m=ceil(64 log k).

If there are r=0 primes in this sum, the desired tail is zero. Otherwise 4r log 2<=log k. If V>=m, some nonnegative allocation (h_p) with sum m is dominated coordinatewise by the excesses. Apply (SP) to its positive coordinates. Each allocation has probability at most 2^(-m)+x^(-.3), and there are binom(m+r-1,r-1) allocations.

For completeness, put R=log k/(4 log 2). The inequality binom(m+r,r)<=[e(m+r)/r]^r and monotonicity in r bound this count by

    k^b,   b=[1+log(256 log 2+5)]/(4 log 2)<3.

Here m<=64 log k+1, and 1<=log k/log 2 was used. The last numerical comparison is elementary: log 2>2/3, log 2<1, and e^6>343>261 give b<21/8<3. Thus the count is at most k^3. Moreover

    2^(-m)<=k^(-32),     x^(-.3)<=k^(-30)

because log 2>1/2 and k<=x^.01. Consequently

    P(V>64 log k)<=P(V>=m)
       <=k^3(k^(-32)+k^(-30))<=2k^(-27).          (VT)

If 64 log k happens to be an integer, the first containment is still valid; otherwise it is equality at the integer threshold. Both r=0 and r=1 are covered, and no division by r-1 is required.

## 5. All contributions to Omega and existence

For p<=w with v_p(k)<4, the support condition p^4|n gives v_p(n-k)=v_p(k). At the other small primes, v_p(n-k)<=v_p(k)+(v_p(n-k)-v_p(k))_+. Therefore the total small-prime multiplicity is at most

    Omega(k)+V <= log k/log 2 + V.

Primes above T, now counted with multiplicity, contribute at most log(2x)/log T<=20A log k. For primes w<p<=T, their first powers are covered by X+Y and their extra powers by U. If T<w, this gives a harmless overcount and U=X=Y=0. Thus, uniformly on the support,

    Omega(n-k)<= (20A+1/log 2)log k + X+Y+U+V.

By the ordinary moments and (UM), choose one absolute B>=1 bounding the three s-th moments by (B log k)^s. Put Q0=e^2B. Markov gives a failure probability at most k^(-8) for each of X,Y,U to exceed Q0 log k. Bound V by (VT). The total sum over k>=2 of all failures is less than 1, since

    3 sum_{k=2}^infinity k^(-8)+2 sum_{k=2}^infinity k^(-27)
      <=5 sum_{k=2}^infinity k^(-8)
      <=5(2^(-8)+2^(-7)/7)<1.

The same probability distribution is used for every shift k. Hence some n in [x,2x] satisfies

    Omega(n-k)<=C0 log k  for 2<=k<=x^.01,
    C0=20A+1/log 2+3Q0+64.

For x^.01<k<n, use Omega(n-k)<=log(2x)/log 2=O(log k), including the trivial value Omega(1)=0. One absolute C therefore works for all integers 2<=k<n. Arbitrarily large x yield unbounded n. Finally omega<=Omega, so this proves the full stated chain omega(n-k)<=Omega(n-k)<=C log k with the original strict k>1 endpoint.

Shifting to N=n-1 and taking epsilon=1/(C log 2) gives every-positive-m fixed-epsilon barriers for Omega and hence for omega. This is the prior theorem and its audited corollary with authored corrections. It supplies no coefficient-one terminal-window inequalities.

## 6. Acceptance boundary

The replacement proves the conclusion for the fixed moment schedule actually used in the union bound. It does not validate the false page-16 uniform prime-sum assertion, the full broad-parameter moment lemma as printed, or the signed inequalities on page 35. It replaces those parts by the explicit CRT comparisons, absolute error sum, and fixed-budget moments above. A second reviewer independently checked (HP), (SP), Q^s<=x^.02, the maximum-exponent block enumeration, the full decomposition and all uniformity, and accepted the complete multiplicity conclusion in the fixed A=100, s=ceil(4 log k) range.
