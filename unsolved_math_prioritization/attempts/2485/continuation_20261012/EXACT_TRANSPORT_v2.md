# Exact factor obstructions and composite-step transport for EP-1095

Authored research, 12 October 2026. This is a structural continuation, not a solution of either successive-ratio conjecture or a claim of novelty.

Write A_k(n) for n >= k with no prime <= k dividing binomial(n,k), and retain

g(k) = min{n > k+1 : A_k(n)}.

For a positive integer x let s_k(x) = product_{p<=k} p^{v_p(x)}. An integer is k-rough when s_k(x)=1; this includes 1.

## 1. A factor-by-factor identity

For k >= 1 and 0 <= j < k, put

c_{k,j} = k binomial(k-1,j) = k!/[j!(k-1-j)!].

**Theorem 1.** For every n >= k >= 1,

binomial(n,k) = lcm_{0<=j<k} ((n-j)/gcd(n-j,c_{k,j})).                 (1)

Consequently,

A_k(n) iff s_k(n-j) divides c_{k,j} for every 0 <= j < k.            (2)

The condition in (2) involves every factor, not just the endpoints.

**Proof.** Fix a prime p. For every j, the integral identity

c_{k,j} binomial(n,k)
 = (n-j) binomial(n,j) binomial(n-j-1,k-j-1)

implies

v_p(binomial(n,k)) >= max(0, v_p(n-j)-v_p(c_{k,j})).                 (3)

Choose j for which a=v_p(n-j) is maximal among the k consecutive integers n,n-1,...,n-k+1. Necessarily k < p^{a+1}, since any p^{a+1} consecutive integers contain a multiple of p^{a+1}. Thus for i != j we have v_p(i-j) <= a. If this valuation is less than a, the non-Archimedean valuation rule gives v_p(n-i)=v_p(i-j). If it equals a, then v_p(n-i)>=a; maximality of a gives equality again. Therefore

sum_{i!=j} v_p(n-i) = v_p(j!)+v_p((k-1-j)!).

The factorial formula now gives

v_p(binomial(n,k)) = a-v_p(c_{k,j}).                              (4)

This is nonnegative because the binomial coefficient is an integer. Equations (3) and (4) show that its valuation is exactly the maximum of the valuations on the right of (1). This holds for every prime p, proving (1). A least common multiple is k-rough exactly when all its constituent quotients are k-rough, giving (2). No Lucas theorem or distribution hypothesis is needed. QED.

**Size of the fixed coefficients.** Each c_{k,j} divides L_k=lcm(1,...,k). Indeed, for each p the Legendre expression

v_p(c_{k,j}) = sum_{r>=1} [floor(k/p^r)-floor(j/p^r)-floor((k-1-j)/p^r)]

has each summand equal to 0 or 1, and all summands with p^r>k vanish. Hence v_p(c_{k,j})<=floor(log_p k). The stronger row identity lcm_j c_{k,j}=L_k is the established Farhi identity cited below; it is not claimed here as new.

**A finite forbidden-class description.** Equation (2) is equivalently the avoidance, for every j and every p<=k, of

n = j (mod p^{v_p(c_{k,j})+1}).                                  (5)

This is an exact obstruction system for the first surviving integer. It makes no assertion that its first gap is comparable with the reciprocal of its density.

## 2. Endpoint restrictions and full valuation defects

The j=0 and j=k-1 cases give necessary conditions

s_k(n) | k,    s_k(n-k+1) | k.                                   (6)

The two smooth parts in (6) are coprime: any common prime would divide k as well as their endpoint difference k-1.

Thus a k-survivor has n=d*u and n-k+1=e*v, where d and e are coprime divisors of k and u,v are k-rough. Equivalently, d*u-e*v=k-1. These endpoint conditions are not sufficient. For example k=3,n=5 has smooth endpoint parts 1 and 3, but binomial(5,3)=10 is even. The interior factor n-1=4 fails (2), since c_{3,1}=6. A composite example is k=4,n=10: the endpoint smooth parts 2 and 1 divide 4, whereas binomial(10,4)=210 is not 4-rough.

**Theorem 2 (composite defects).** Let K be composite, n >= K, and assume A_K(n). Set d=s_K(n) and e=s_K(n-K+1). Then

s_{K-1}(binomial(n-1,K-1)) = K/d,
s_{K-1}(binomial(n,K-1))   = K/e.                                (7)

In particular, the predecessor at n-1 is a (K-1)-survivor exactly when d=K, and the predecessor at n is one exactly when e=K.

**Proof.** As K is composite, the prime sets <=K and <=K-1 agree and all prime divisors of K belong to them. Use the exact identities

binomial(n-1,K-1)=K*binomial(n,K)/n,
binomial(n,K-1)=K*binomial(n,K)/(n-K+1).

Taking each small-prime valuation gives (7). QED.

For K=p^a, a>=2, (6) says d=p^r and e=p^s with 0<=r,s<=a and min(r,s)=0. The two preceding binomial coefficients in (7) therefore have exact small-prime parts p^{a-r},p^{a-s}; at least one has small-prime part exactly p^a. This isolates precisely the defect which prime transport cannot ignore.

## 3. Exact composite boundary transport

**Theorem 3.** Let K be composite. Every (K-1)-survivor m satisfies K | (m+1). For t>=2, let m=Kt-1. Then

A_K(Kt-1) iff A_{K-1}(Kt-1) and t-1 is K-rough,
A_K(Kt)   iff A_{K-1}(Kt-1) and t is K-rough.                     (8)

**Proof.** Put B=binomial(m,K-1). The integrality of

binomial(m+1,K)=(m+1)B/K

forces v_p(m+1)>=v_p(K) for every p|K when B is (K-1)-rough. Hence K|(m+1). Conversely, at m=Kt-1 the two exact identities are

binomial(Kt-1,K)=(t-1)B,
binomial(Kt,K)=tB.

As the forbidden prime sets at K and K-1 coincide, either product is K-rough exactly when both factors are. QED.

The lattice statement itself is already in Lukes-Scheidler-Williams (1997), printed p.1715, with credit there to earlier work. The present use retains the extra roughness filters in (8).

### Consequences for actual first minima

Let b(K) be the least K-survivor n>K+1 with n mod K in {0,K-1}. It exists: sufficiently large integers n congruent to -1 modulo L_K product_{p<=K}p satisfy every digit condition and are -1 modulo K. Then (8) gives an exact first-survivor formula for b(K), in terms of the old survivors m=Kt-1 and the two roughness tests on t-1 and t. In particular:

1. b(K) >= g(K-1).
2. If t0=(g(K-1)+1)/K and t0-1 is K-rough, then b(K)=g(K-1), so g(K)<=g(K-1).
3. If t0 is K-rough, then b(K)<=g(K-1)+1, so g(K)<=g(K-1)+1.
4. If g(K)<g(K-1), its residue modulo K belongs to {1,...,K-2}. Equivalently, its two endpoint smooth parts in (6) are both proper divisors of K.
5. For any real R>=1, g(K)<g(K-1)/R is equivalent to the existence of an interior-residue K-survivor satisfying K+1<n<g(K-1)/R. The transported boundary layers cannot cause it. This is an exact separation, not an existence assertion.

For point 3, t0-1 is even when t0 is odd, so apart from the exceptional integer 1 at most one of the two boundary filters can pass. No unconditional upper bound for g(K) in terms of g(K-1) follows by dropping these filters.

For comparison, when K=q is prime the two displayed binomial identities instead show that every q-survivor n>q+1 has both A_{q-1}(n-1) and A_{q-1}(n), and both n and n-q+1 have no prime factor below q. The separate q-adic condition remains necessary. Thus g(q)>=g(q-1)+1, recovering the prior theorem. The entirely different composite behavior is the nontrivial defect K/d or K/e in (7).

## 4. Actual boundary minima and why they matter

An authored monotone search computes the first K-survivor in residues 0,-1 modulo K. An independent verifier checks every integer in these two residue classes below its reported value using exact integer binomial coefficients and gcd with the primorial. This second verification uses neither the Lucas search routine nor the quotient-lcm identity. Selected results:

| K | g(K-1), previously certified | g(K), previously certified | b(K), independently verified here |
|---|---:|---:|---:|
| 8 | 143 | 44 | 143 |
| 9 | 44 | 159 | 269 |
| 16 | 719 | 241 | 2096 |
| 25 | 193049 | 2105 | 395225 |
| 27 | 36287 | 1119 | 88479 |
| 32 | 341087 | 371942 | 1507967 |

For K=25, actual g(25)=2105 occurs much earlier than either transported old boundary layer (b(25)=395225). This is a finite, exact failure of replacing the actual first survivor by the first surviving transported boundary point. Prime powers do not always cause downward steps: K=9 and K=32 go upward, while K=8,16,25,27 go downward. None of these computations proves an asymptotic ratio statement.

## 5. Primary-source attribution check

Targeted checks located two closely related established results:

- Bakir Farhi, *An identity involving the least common multiple of binomial coefficients and its application*, arXiv:0906.2295v2, Theorem 1: lcm_j binomial(k-1,j)=L_k/k. This identifies the exact lcm of the fixed coefficients c_{k,j}. Primary author preprint: https://arxiv.org/pdf/0906.2295v2 .
- Bakir Farhi, *Nontrivial lower bounds for the least common multiple of some finite sequences of integers*, Journal of Number Theory 125 (2007), 393-411; author preprint arXiv:0803.0290, Theorems 11-12 and the proof of Theorem 12 on preprint pp.14-15. These compare interval lcms with binomial coefficients and use an integral product-of-binomials identity. Primary author preprint: https://arxiv.org/pdf/0803.0290 .
- R. F. Lukes, R. Scheidler and H. C. Williams, *Further tabulation of the Erdos-Selfridge function*, Mathematics of Computation 66 (1997), 1709-1717, especially printed pp.1711-1712 for prime-power residue changes and p.1715 for the composite lattice. Primary author-hosted PDF: https://cspages.ucalgary.ca/~rscheidl/Papers/es.pdf .

The exact quotient-lcm formula (1) and its smooth-part presentation were not located in these targeted primary checks. That is not evidence of novelty. The proof above is complete and independent, and the surrounding lcm theory and known composite lattice must be credited. No literature-priority claim is made.

## 6. Scope

The useful new-to-this-work outputs are the exact all-factor obstruction, two-sided composite defect theorem, boundary first-minimum transport, and independently verified finite boundary minima. They sharpen what a successive-ratio proof must control: interior new survivors for downward jumps, and surviving filtered old candidates for upward jumps. They do not provide an asymptotically stronger bound on g, establish either ratio conjecture, or justify density-to-first-hit substitution. The explicit elementary proofs stand independently of the finite tests.

## Verification record

The independent exact-arithmetic script passes in normal, -O, and -OO modes: 31,264 quotient-lcm identities; 31,264 full-factor equivalence checks; 231 sampled positive composite defect cases; 89,910 boundary equivalence cases; all 46 previously certified minimum witnesses; and 135,564 exact-binomial rejections proving the 13 new boundary minima. Seven negative controls pass by rejecting false shortcuts. The repeated modes produce byte-identical diagnostic results. No source-author code was run.
