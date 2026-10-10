# Authored reconstruction of Lau's distinct-prime consequence

This is a bounded correction and projection of the proof of a prior result, not a novelty claim or a new coefficient-one barrier solution. Source: Cheuk Fung (Joshua) Lau, *On the Number of Prime Factors of Consecutive Integers*, arXiv:2604.15042v2, 24 June 2026, https://arxiv.org/pdf/2604.15042v2 . The source PDF has SHA256 90443d4ebbdfe9e05052e1a8115b8acd9d29d3ce7269d7e9c71cb09716c718d1.

## Result and deliberate boundary

There is an absolute constant C>0 such that infinitely many positive integers n satisfy

    omega(n-k) <= C log k  for every integer 2<=k<n.

Consequently there is one fixed epsilon>0 and infinitely many N satisfying

    m + epsilon*omega(m) <= N  for every positive integer m<N.

Here omega counts distinct prime divisors. This separate reconstruction does not itself certify the corresponding multiplicity-counting Omega bound. The source's high-prime-power issue is treated and resolved by the companion MULTIPLICITY_REPAIR.md. It does not resolve the coefficient-one barrier question. The second displayed conclusion uses epsilon=1/(C log 2), N=n-1, and the complete endpoint argument in AUDIT.md.

## 1. Fixed setup and smoothing

Let x tend to infinity, L=log x, K=floor(L^(1/1000)), w=.15L and

    W=product_{p<=w} p^4,
    R_r=x^(1/(100r^50))  for 1<=r<=K.

The prime number theorem gives W=x^(.6+o(1)); no unsupported one-sided W<=x^.6 is needed. Choose once and for all a nonnegative, even, smooth, compactly supported Gevrey-2 eta on [-1,1], with eta(0)=1 and nonnegative Fourier transform h. Such a function is obtained by autocorrelating a nonzero nonnegative Gevrey-2 bump supported on [-1/2,1/2] and dividing by its value at zero. Cauchy–Schwarz gives eta<=1. Put tilde-eta(u)=exp(-u)eta(u).

Only fixed constants from this function enter the proof. Its derivative bound |eta^(m)|<=B^m(m!)^2, with a harmless fixed leading constant if necessary, implies |h(t)|<=C exp(-c sqrt(|t|)). For example, integrate by parts m times, use m!<=m^m, and take m=floor(sqrt(|t|/(4B))). This uses the upper factorial estimate, avoiding the reversed Stirling bound in the printed derivation.

For definiteness work directly with backwards shifts and the nonnegative weight

    nu(n)=1_{n in [x,2x]} 1_{W|n}
          product_{r=1}^K [sum_{d|n-r, (d,product_{p<=w}p)=1}
                            mu(d) tilde-eta(log d/log R_r)]^2.

For sufficiently large x all n-r in the weight are positive. A valid normalization is proved below, so this defines a probability distribution. It depends on x but not on a queried shift k or moment order.

Set throughout A=10. For any integer 2<=k<=x^(1/100) put

    s=s(k)=ceil(4 log k),  T=x^(1/(100 log k)),
    R=R_k if k<=K, and R=w if k>K.

Then 3<=s<=6 log k<10 log k. If k<=K, R_k<=T because log k<=k^50, and R_k^s<=x^(.1). Also T^s<=x^(.06)<x^(.1). All applications below therefore have the necessary small product of imposed primes. Fixing A and s here removes any circular dependence between a threshold constant and the allowed moment orders.

## 2. Exact CRT/Fourier representation and its error

Let d*=p_1...p_j be a squarefree product of distinct primes p_i>w, with j<=s and d*<=x^(.1). Expand the K squares. Each contributing divisor is squarefree and at most its R_r; coefficients have absolute value at most 1. Different shifts cannot share a prime above w>K. Incompatible congruence systems contribute zero; compatible ones have one residue class modulo the appropriate least common multiple.

The number of divisor configurations is at most

    product_r R_r^2
    =x^((1/50) sum_{r<=K}r^(-50)) < x^(.021).

Each CRT interval count differs from its density main term by O(1), uniformly in its modulus. Thus the total unnormalized CRT error is O(x^(.021)). The combined modulus is at most W d* product_r R_r^2=x^(.721+o(1)).

Insert the Fourier representation of tilde-eta into the density main term. The absolutely convergent divisor sums yield the exact Euler-product integrand F_d described in KERNEL_REPAIR.md. The backwards sign changes n congruent to -r into n congruent to r; local compatibility still depends on p|(k-r), so all its factors are unchanged. Let H=L^(.2). Uniformly in the Fourier variables, the absolute Euler-product bound is at most

    (4^j/d*) exp(O(K log L)).

The Gevrey tail, summed over 2K coordinates, therefore bounds the part outside [-H,H]^(2K) by

    (4^s/d*) exp(-c L^(.1)+O(K log L)).

The weighted count P_k(d*)=sum_n nu(n)1_{d*|n-k} is consequently x/W times the truncated exact integral, plus

    O((4^s x/(W d*)) exp(-c' L^(.1))).             (E)

After shrinking c'>0, (E) also absorbs the CRT error: x/(Wd*)>=x^(.3-o(1)), whereas the CRT error is O(x^(.021)). This proves the needed counterpart of (6.6) directly, including its denominator and the uniformity in k and s. It does not rely on the false many-coordinate absolute-value identity.

## 3. Corrected normalization and unsieved prime divisibility

KERNEL_REPAIR.md gives the full replacement integration argument. Its ingredients, checked here, are:

- Exact one-coordinate factors g_r=C_r a(t_r,u_r)(1+O(L^(-.7))) uniformly on the box, where C_r=(W/phi(W))/log R_r and a(t,u)=(1+it)(1+iu)/(2+i(t+u)). The single-coordinate zeta estimate is uniform because log R_r>=L^(.95)/100.
- The exact inter-coordinate correction is an absolutely summable series of nonnegative Fourier translations. Its coefficient norm differs from 1 by O(K^2/w) in the normalization case; with j divisor primes its norm is at most (1+o(1))2^j.
- Nonnegative right translations are L2([0,infinity)) contractions. A paired prime difference factor costs at most 4 in a squared norm. One-coordinate perturbations cost 1+O(L^(-.7)), which still tends to 1 after raising to K.

These facts prove, with c0=integral_0^infinity (tilde-eta'(u))^2 du>=1,

    Z:=sum_n nu(n)=(1+o(1))(x/W)c0^K product_r C_r,     (N)
    P(d*|n-k) << 8^s/d*.                              (B)

The implied constant is absolute and independent of x,k,s. Error (E) is negligible at this scale because product_r log R_r<=exp(O(K log L)), and exp(-c L^(.1)) dominates that factor. The 4^s numerator error is absorbed by 8^s. This also proves Z>0 for all sufficiently large x.

## 4. A corrected summed bound for the sieved prime range

Assume now 2<=k<=K. For any 1<=j<=s, let the sum below be over ordered, mutually distinct primes in (w,R_k]. We claim

    sum P(p_1...p_j|n-k) <= (B1 log(s+2))^s           (C)

for one absolute B1 and all sufficiently large x, uniformly in k,j,s=s(k).

Every imposed prime has the same compatible coordinate k, because k is among 1,...,K and p>w>K. Thus its exact extra factor is

    (1/p) U_p(t,u),
    U_p=(1-exp(-a_p(1+it)))(1-exp(-a_p(1+iu))),
    a_p=log p/log R_k.

Expand the correction H_d from KERNEL_REPAIR.md into its absolutely summable positive-translation monomials. Its coefficient norm is at most (1+o(1))2^j. For each monomial, all untouched coordinate integrals are bounded by their C_r c0 factors times (1+O(L^(-.7))) individually; their product is (1+o(1))c0^(K-1) product_{r!=k} C_r. In the affected coordinate, integrate absolutely. Additional positive translations have modulus at most 1, so that bound is uniform over every monomial, even though the coefficients depend on the tuple of primes.

For V=1+|t| one has

    |U_p(t,u)| <= 2 min(2,V log p/log R_k),
    |a(t,u)| <= (1+|t|)(1+|u|)/2.

The second inequality deliberately does not replace |t+u| by |t|+|u|. The elementary prime-harmonic bounds imply, uniformly for R>=w and V>=1,

    sum_{w<p<=R} (1/p) min(2,V log p/log R)
       <= C(1+log V).                               (P)

To check (P), split at log p=2 log R/V. Below the split use sum_{p<=y}(log p)/p=O(log y); above it use the interval bound for sum 1/p. If the split lies below 2, the whole prime-harmonic sum is O(log log R)=O(1+log V). If V<=2, the first weighted bound alone suffices.

Dropping distinctness enlarges the absolute sum. Hence after summing over prime tuples the affected-coordinate integral is bounded by a constant to the j-th power times

    integral_R2 (1+|t|)(1+|u|)
                (1+log(1+|t|))^j |h(t)h(u)| dt du.

Since j<=s and h has exp(-c sqrt(|t|)) decay, this is at most (C log(s+2))^s. For a direct proof, split |t| at a sufficiently large constant times (s+2)^4. On the inner range the logarithmic factor is O(log(s+2))^s and the remaining integral is bounded. On the tail, its logarithm is at most (c/2)sqrt(|t|), leaving a uniformly integrable decaying factor. This estimate is uniform in the positive translations.

Dividing by (N), the untouched normalizing factors cancel and c0>=1 absorbs the remaining 1/c0. The factor 2^j from the correction norm is absorbed into B1^s. Summed errors (E) are also negligible: sum 1/(p_1...p_j) is at most (C log L)^j, while s<=.004 log L+1 for k<=K. Therefore their relative size is bounded by

    exp(-c L^(.1)+O(K log L+s log log L))=o(1).

Enlarge B1 to absorb this error. This proves (C) without discarding a frequency-dependent error and without using the paper's high-prime-power argument.

## 5. Ordinary positive moments, avoiding prime powers

Define

    X=sum_{w<p<=R} 1_{p|n-k},
    Y=sum_{R<p<=T} 1_{p|n-k},

where an empty range contributes zero. When k>K, R=w and X=0.

For k<=K, grouping the s factors in X^s according to their distinct primes gives

    E X^s = sum_{j=1}^s S(s,j) sum_{ordered distinct p_1,...,p_j} P(p_1...p_j|n-k).

Here S(s,j) are Stirling numbers of the second kind. Bound the inner sum by (C), and the sum of S(s,j) by the Bell number B_s. Its generating function exp(exp(z)-1) has nonnegative coefficients. Evaluation at z=(1/2)log(s+1), with s!<=s^s and exp(sqrt(s+1)-1)<=exp(s), gives

    B_s <= (2e s/log(s+1))^s.

Consequently E X^s <=(B2 s)^s <=(B3 log k)^s for absolute constants B2,B3. This is also true when X=0.

For Y, put lambda=sum_{R<p<=T}1/p, zero when the range is empty. The ordinary prime-harmonic estimate gives lambda<=B4 log k uniformly. Indeed, when k<=K the logarithm of the ratio of logarithmic endpoints is at most 50 log k-log log k, up to an absolute additive constant. When k>K one has log k>(1/1000)log L, while log log T<=log L. Since log k>=log 2, all additive constants are absorbed.

Using (B), grouping repeated indices again yields

    E Y^s <=M 8^s sum_{j=1}^s S(s,j)lambda^j.

The polynomial on the right has exponential generating function exp(lambda(exp(z)-1)). With z=s/(s+lambda) in (0,1], its s-th coefficient gives

    sum_j S(s,j)lambda^j
       <=s! z^(-s) exp(lambda(exp(z)-1))
       <=[e^2(s+lambda)]^s,

using exp(z)-1<=2z. The case lambda=0 is immediate. Thus E Y^s <=(B5 log k)^s. The fixed factor M is absorbed into B5 because s>=3. These are positive moments; no centered-moment expansion or unavailable 2s-th joint-divisibility estimate is needed.

## 6. Summable tails and infinitely many witnesses

For every n in the support and 2<=k<=x^(1/100), each prime p<=w divides n-k exactly when it divides k. Thus their distinct contribution is at most omega(k)<=log k/log 2. Every prime factor above T contributes at most log(2x)/log T<=20A log k for all sufficiently large x. The intermediate primes are covered by X and Y. If T<w, both X and Y are zero and the same upper bound overcounts harmlessly. Therefore

    omega(n-k) <= (20A+1/log 2)log k + X+Y.

Let B=max(B3,B5,1) and Q=e^2 B. Markov's inequality and s>=4 log k give

    P(X>Q log k) <=e^(-2s)<=k^(-8),
    P(Y>Q log k) <=e^(-2s)<=k^(-8).

The sum of these failure probabilities over all k>=2 is strictly less than 1; for instance

    2 sum_{k=2}^infinity k^(-8)
       <=2(2^(-8)+2^(-7)/7)<1.

Since the same distribution was used for every k, a union bound leaves a witness n in [x,2x] for which

    omega(n-k) <= C0 log k  for 2<=k<=x^(1/100),
    C0=20A+1/log 2+2Q.

For x^(1/100)<k<n, the deterministic bound omega(n-k)<=log(2x)/log 2 is at most C1 log k for one absolute C1 and all sufficiently large x. The endpoint n-k=1 has omega(1)=0. Taking C=max(C0,C1) proves the stated backwards logarithmic result with one fixed C. The construction works for arbitrarily large x, and n>=x, hence yields infinitely many distinct witnesses.

Finally shift n to N=n-1 and use the endpoint proof in AUDIT.md. This proves the existential fixed-epsilon statement for distinct omega from the corrected, projected prior proof. The argument never bounds excess prime powers; it therefore does not itself establish the full Omega theorem, which is proved in the separate companion, and does not settle the finite terminal-window obligation for coefficient one.

## Verification boundary

This reconstruction relies on standard prime number and prime-harmonic estimates, elementary CRT, Fourier inversion for the fixed smooth bump, and the authored exact-Euler-product integration correction in KERNEL_REPAIR.md. It supplies the intermediate divisibility-sum and ordinary-moment details required for the distinct-prime projection. The invalid page-16 prime-power estimate and signed prime-power arguments are not used. No computational search for new barrier witnesses is part of this proof.
