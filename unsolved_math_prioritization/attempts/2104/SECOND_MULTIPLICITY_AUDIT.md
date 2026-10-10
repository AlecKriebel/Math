# Independent supplement: the fixed-schedule multiplicity repair

## Accepted conclusion and exact scope

The bounded correction below proves that one absolute C>0 satisfies

omega(n-k) <= Omega(n-k) <= C log k

for every integer 2<=k<n, for infinitely many positive integers n. Here Omega counts prime factors with multiplicity. This accepts the backwards conclusion of Theorem 1.3 in Cheuk Fung (Joshua) Lau, *On the Number of Prime Factors of Consecutive Integers*, arXiv:2604.15042v2, 24 June 2026, with authored corrections rather than the printed proof as written.

Public source: https://arxiv.org/pdf/2604.15042v2 . Inspected PDF: 717637 bytes, SHA256 `90443d4ebbdfe9e05052e1a8115b8acd9d29d3ce7269d7e9c71cb09716c718d1`.

This supplement extends the preceding distinct-omega acceptance; the earlier packet is unchanged. It uses the same fixed sieve weight, its corrected normalization, and the already verified small-prime and medium-prime distinct-factor moments. It proves the extra multiplicity estimates only for A=100 and s=ceil(4 log k), the schedule actually used by the union bound. It does not accept the source's arbitrary-order prime-sum estimate on p.16, all broad-parameter moment claims, or the signed inequalities on p.35. Those steps are replaced below.

The coefficient-1 version of Erdős problem #413 remains unresolved by this work. This is a correction and verification of a prior consequence, not a novelty claim.

## 1. Fixed weight and the uniform error available for new CRT comparisons

Use the weight and smoothing in `SECOND_KERNEL_REPAIR.md` and `SECOND_DISTINCT_OMEGA_CHAIN.md`: L=log x, w=.15L, K=floor(L^.001), W=product_{p<=w}p^4, R_a=exp(L/(100a^50)) for a<=K, with backwards shifts n-a. The weight is a product of squared divisor sums, times 1_[x,2x](n) and 1_{W|n}; its expansion coefficients have absolute value at most one.

There are at most

N_cfg=product_{a<=K} R_a^2 <=x^.021

divisor configurations. Their normalization, already proved using the corrected kernel argument, is

Z=(1+o(1))(x/W)c0^K product_{a<=K}[(W/phi(W))/log R_a],
c0>=1.

In particular Z=x^(.4+o(1)). Indeed W=x^(.6+o(1)), and all other logarithms have total size O(K log L)=o(L). Even the elementary bound W/phi(W)<=floor(w) suffices for this observation. Thus Z>=x^.39 eventually. Any sum of O(1) errors over at most N_cfg signed configurations has normalized absolute size at most x^(-.3) for sufficiently large x. This uniform bound has no dependence on the size of any later imposed prime-power modulus.

Now fix

A=100, T_k=exp(L/(1000 log k)), s=ceil(4 log k),
2<=k<=floor(x^.01).

Then 3<=s<=6 log k and T_k^s<=x^.006. For k<=K, R_k<=T_k because k^50>=10 log k, so R_k^s<=x^.006 as well. No maximal order near A log k is required.

The general squarefree estimate from the kernel repair is

Pr(d|n-k) <=M 8^s/d,                               (S1)

for any product d of at most s distinct primes in (w,T_k]. It applies also when some primes are at most R_k: every associated local factor is controlled by the same positive-translation contraction. The repair never uses p>R_k, only p>w and the bound d<=x^.1; here the stronger d<=x^.006 holds.

The previous distinct-factor moment argument likewise applies with this T_k. Define

X=sum_{w<p<=R_k}1_{p|n-k},
Y=sum_{R_k<p<=T_k}1_{p|n-k},

where R_k=w for k>K and an empty interval gives zero. The verified min-factor, Bell-number, and Touchard arguments give

E X^s <=(B_X log k)^s, E Y^s <=(B_Y log k)^s         (S2)

with absolute constants. The change from A=10 to A=100 leaves the weight and normalization unchanged, preserves R_k<=T_k when needed, and only changes fixed constants in the prime-harmonic estimates.

## 2. Arbitrary prime powers: cancellation before taking absolute errors

Let p_1,...,p_j be distinct primes in (w,T_k], j<=s, and let a_i>=2 be arbitrary integers. Write

d=product_i p_i, D=product_i p_i^a_i, b=product_i p_i^(a_i-1).

Then

|Pr(D|n-k)-Pr(d|n-k)/b| <=x^(-.3)                  (S3)

uniformly in all exponents, even if D is larger than x.

To prove this, take one expanded divisor configuration. Incompatible base congruences contribute zero. A compatible configuration defines a residue class modulo q=W lcm([d_a,d'_a]:a<=K). Every prime above w has exponent at most one in q, since the divisor variables are squarefree. Compatibility of the additional first-power conditions is exactly the same as compatibility of the higher-power conditions: at a prime already in q, both require the same congruence modulo p, while q imposes no higher power of that prime.

If compatible, the two moduli are lcm(q,d) and lcm(q,D)=b lcm(q,d). Their length-x density terms are therefore in the ratio 1/b. Interval counts each equal their density times x plus O(1), uniformly in the modulus. Subtract the first-power count divided by b from the higher-power count. The density terms cancel exactly. The error is O(1), because 1/b<=1.

Only now sum the signed coefficients and take absolute values on the interval errors. The unnormalized difference is O(N_cfg), hence (S3) follows from §1. This is an equality-of-main-terms argument, not an inequality multiplied termwise by Möbius signs.

## 3. The number of repeated prime-power configurations is small enough

Let

U=sum_{w<p<=T_k} sum_{a>=2, p^a<=2x}1_{p^a|n-k}.

It counts every extra multiplicity from primes in (w,T_k]. No exponent that could occur for n-k>0 has been omitted. If T_k<=w, U=0.

Otherwise let Q be the number of prime-power indicators in this sum. For sufficiently large x,

Q<=T_k log(2x)/log w,
log(Q^s)<=s(log T_k+log(2L)).

The condition T_k>w gives log k<L/(1000 log w), and s<=6 log k. Hence

log(Q^s)
<=.006L + .006L log(2L)/log w
<.02L                                                   (S4)

uniformly in k for sufficiently large x. The numerical margin is explicit: for L>=100, (0.15L)^2>=2L, so log(2L)/log w<=2 and the preceding exponent is at most .018L<.02L. If Q=0 the assertion is unnecessary; U is again zero.

Expand U^s as a sum of at most Q^s indicator tuples. For each tuple, group equal primes and replace all exponents belonging to a prime by their maximum. Apply (S3) exactly once to this grouped configuration. Its comparison error is at most x^(-.3), independent of the number of blocks and their exponents. Thus the sum of all comparison errors is at most

Q^s x^(-.3)<=x^(-.28).                              (S5)

No second moment, 2s-th joint estimate, or unbounded repetition count is hidden in this step.

## 4. Exact block enumeration for the main high-power moment

For a block of m tuple positions carrying one prime p, suppose its largest exponent is a>=2. The number of exponent assignments is

(a-1)^m-(a-2)^m <= a^m.

Combining (S3) with (S1), the main probability of a grouped tuple is at most M8^s/product p_i^a_i. Drop distinctness between block primes and extend the exponent and prime ranges; all summands are nonnegative. The weight available to a block of size m is then

W_m=sum_{p>w}sum_{a>=2} a^m p^(-a).

For w>=4 and a>=2,

sum_{p>w}p^(-a)<=sum_{n>=5}n^(-a)
<=4^(1-a)/(a-1)<=2^(1-a).

Also a^m<=m! binom(a+m-1,m). Therefore

W_m<=sum_{a>=1}a^m 2^(1-a)
<=m! sum_{a>=1}binom(a+m-1,m)2^(1-a)
=2^(m+1)m!.                                        (S6)

The last equality is the negative-binomial series after setting n=a-1. Thus no asymptotic bound uniform in a large m is being imported from the flawed p.16 estimate.

Every tuple has a unique partition of its s labelled positions by equal primes. The sum over all set partitions of their block weights is

s! [z^s] exp(sum_{m>=1} W_m z^m/m!).

By (S6), at z=1/4 the exponent is at most 2. Its coefficients are nonnegative, so this is at most e^2 s!4^s. Equations (S1), (S5) now imply

E U^s <=M e^2 8^s s!4^s+x^(-.28)
        <=(B_U s)^s <=(B'_U log k)^s.               (S7)

All constants are fixed, and s>=3 absorbs fixed prefactors. This controls all extra prime powers above w and below T_k, not merely the subset satisfying p^a<=T_k.

## 5. Tiny-prime excess: another exact signed-main identity

Let S be any subset of {p<=w:p^4|k}, put e_p=v_p(k)>=4, and choose integers h_p>=1. Then

Pr(v_p(n-k)-e_p>=h_p for every p in S)
<=product_{p in S}p^(-h_p)+x^(-.3).                 (S8)

For a compatible base divisor configuration, the modulus q has exponent exactly 4 at every p in S: W contributes p^4, and all divisor variables avoid primes at most w. Imposing n=k modulo p^(e_p+h_p) is compatible with the base condition n=0 modulo p^4. It changes the modulus by the same factor product p^(e_p+h_p-4) for every configuration. Thus the restricted signed density main sum is exactly beta times the unrestricted one, with

beta=product p^(-(e_p+h_p-4))<=product p^(-h_p)<=1.

Subtract beta times the unrestricted count before taking absolute errors. The two uniform O(1) interval errors per configuration give O(N_cfg); divide by Z to get (S8). The argument applies even if the extra modulus exceeds x. There is no termwise inequality involving a signed coefficient.

Set

V=sum_{p<=w,p^4|k}(v_p(n-k)-v_p(k))_+,
m=ceil(64 log k).

If r is the number of primes in this sum, then 4r log 2<=log k. If r=0, V=0. Otherwise V>=m implies that some weak composition of m among these r primes is coordinatewise at most the excesses. Its active coordinates have joint probability at most 2^(-m)+x^(-.3) by (S8).

The number of these weak compositions is binom(m+r-1,r-1), at most binom(m+r,r). With R=log k/(4 log 2), use the increasing function r log(e(m+r)/r), and m<=64 log k+1, to bound the count by

k^b, b=[1+log(256 log 2+5)]/(4 log 2)<3.             (S9)

One exact check of the last inequality is e(256 log 2+5)<3*261<2^12, using e<3 and log 2<1. Thus the composition count is at most k^3, including r=1.

Since log 2>1/2 and k<=x^.01,

2^(-m)<=k^(-32), x^(-.3)<=k^(-30).

The union bound therefore gives

Pr(V>64 log k)<=Pr(V>=m)
<=k^3(k^(-32)+k^(-30))<=2k^(-27).                  (S10)

This uses all tiny primes at once; its error count is bounded explicitly rather than hidden in an implied constant.

## 6. Completion of the backwards multiplicity bound

For p<=w with v_p(k)<4, the condition p^4|n gives v_p(n-k)=v_p(k). For the remaining tiny primes, v_p(n-k)<=v_p(k)+(v_p(n-k)-v_p(k))_+. Thus the total tiny-prime multiplicity is at most Omega(k)+V<=log k/log 2+V.

All prime factors p>T_k, now counted with multiplicity, contribute at most

log(n-k)/log T_k<=log(2x)/log T_k<=2000 log k.

Primes in (w,T_k] contribute X+Y+U. If T_k<w, all three are zero and the large-prime bound may double-count some tiny primes, which is harmless. Hence on the entire support,

Omega(n-k)<=(2000+1/log 2)log k+X+Y+U+V.            (S11)

Choose an absolute B>=1 such that each of the three s-th moments in (S2)/(S7) is at most (B log k)^s. With Q_0=e^2 B, Markov's inequality gives probability at most exp(-2s)<=k^(-8) that any one of X,Y,U exceeds Q_0 log k. The tiny-prime tail is (S10).

The total failure probability, summed over every k from 2 to floor(x^.01), is at most

3 sum_{k>=2}k^(-8)+2 sum_{k>=2}k^(-27)
<=5 sum_{k>=2}k^(-8)
<=5(2^(-8)+2^(-7)/7)<1.                            (S12)

All events use the same normalized sieve distribution. Thus some n in [x,2x] obeys Omega(n-k)<=C_0 log k simultaneously throughout this range, with one fixed C_0=2000+1/log 2+3Q_0+64. In particular k=2 is included, with s=3; no finite exceptional initial range is dropped.

For floor(x^.01)<k<n, the elementary bound Omega(n-k)<=log(2x)/log 2 is at most (200/log 2)log k for sufficiently large x. Enlarging C once gives the required inequality for every 2<=k<n. Taking x=3^j produces witnesses in disjoint intervals [3^j,2*3^j], so they are infinitely many and distinct.

Finally set N=n-1 and epsilon=1/(C log 2). For every positive m<N, k=n-m lies in [2,n-1]; using log k<=(k-1)log 2 gives

m+epsilon Omega(m)<=m+log k/log 2<=m+k-1=N.

Since omega(m)<=Omega(m), this also gives the distinct-omega fixed-epsilon barrier. The same one positive epsilon works for all witnesses and every positive m below each witness. Coefficient 1 is not supplied.

## Independent acceptance record

The complete fixed-schedule `MULTIPLICITY_REPAIR.md` was checked against the separate derivation above. The following critical points pass:

- higher-power compatibility and density cancellation, with no bound on the power modulus;
- uniform error O(N_cfg/Z), independent of exponents and repeated configurations;
- explicit Q^s<=x^.02 and accumulated error <=x^(-.28);
- unique grouping of tuple positions by prime and maximum exponent;
- the exact negative-binomial and exponential-series bounds;
- configuration-independent tiny-prime main-term scaling;
- all weak-composition counts and their error accumulation;
- the T_k<w case, the common distribution, the smallest shifts, and infinite witness production;
- the fixed epsilon and complete endpoint shift.

Acceptance is the repaired backwards multiplicity conclusion in this fixed schedule and its fixed-epsilon consequences. It is not acceptance of the false p.16 estimate, the p.28 L1 identity, all arbitrary-A/order statements, or the coefficient-1 barrier. No broader exploration is needed for the accepted conclusion.

## Publication-edition review boundary

Acceptance means independent internal AI review of the stated corrected
mathematical arguments. This AI-assisted work is unrefereed. No external human
peer review, journal acceptance, formal proof-assistant certification, or
novelty is claimed. The fixed A=100 multiplicity repair and fixed-positive-
epsilon consequence are accepted; coefficient one remains unresolved.
