# Independent reconstruction of the reduced-lattice estimate

Date: 12 October 2026. This file reconstructs a proposed argument; acceptance of an author's manuscript requires a separate frozen-byte audit.

Let g(k) be the least n>k+1 for which no prime p≤k divides binom(n,k). Fix a in (1/2,1), k≥9, put L=lcm(1,...,k), and set

M = L × product_{p≤sqrt(k)} p / product_{ak<p≤k} p.

Every product here is over primes. The three disjoint prime sets are forced primes p≤sqrt(k), retained primes sqrt(k)<p≤ak, and omitted primes ak<p≤k. Since k≥9, ak>sqrt(k). In particular omitted primes occur to exponent exactly one in L and are completely removed from M. Forced primes receive exactly one extra factor beyond their largest power ≤k.

For n=tM−1:

* Forced primes pass Lucas' digit criterion in every relevant position.
* Retained p have M=pc with p∤c. The units digit of n is p−1; the tens digit is (tc−1) mod p. Exactly b_p=floor(k/p) classes of t mod p fail.
* For omitted p, k=p+(k−p), with 0≤k−p<p. The map t↦tM−1 modulo p² is a bijection. A passing n has its units digit in [k−p,p−1], giving 2p−k choices, and its tens digit in [1,p−1], giving p−1 choices. The two digits jointly give (2p−k)(p−1) good classes. Thus

C_p=p²−(2p−k)(p−1)=p(k−p)+2p−k,
w_p=C_p/p²=k/p−1+2/p−k/p².

At p=k the failure weight is 1/p, not zero: the leading digit is still required. The correction term is positive and uniformly O_a(1/k) on the omitted interval.

For an active prime let q_p=p and C_p=b_p if retained; q_p=p² and C_p as above if omitted. The moduli q_p are pairwise coprime, even though they are mixed first and second powers. Every joint rejection set indexed by J has exactly product_{p∈J} C_p classes modulo product_{p∈J} q_p. On [1,T], its count therefore differs from T product_{p∈J}w_p by at most product_{p∈J} C_p. This bound covers the error even when the modulus exceeds T.

For even r define E=sum_{j=1}^{r−1} e_j(C), rho=product(1−w), and R=z^(−r) product(1+zw), with z>1. The odd Bonferroni inequality and its next even companion give

N(T)≥T(rho−R)−E.

This proves an actual initial-interval survivor once R≤rho/2 and T=floor(2E/rho)+1. Full-period density alone is never used as a first-survivor assertion.

Every survivor is in the required domain. All primes removed exceed k/2, so M is divisible by lcm(1,...,m), m=floor(k/2). This lcm is a multiple of m(m−1). For k≥9, m(m−1)−1>k+1. Thus every t≥1 gives tM−1>k+1, regardless of its digit conditions.

## Asymptotic estimates

All a,z,A below are fixed independently of k. PNT implies logM=(a+o(1))k.

The retained-prime contribution to either −log rho or log product(1+zw) is O_z(sqrt(k)log k)=o(k/log k). To see this, split at 2sqrt(k). Below that point, 1−b_p/p≥1/p and the crude integer count bounds the negative logarithm by O(sqrt(k)log k); the positive logarithm is O_z(sqrt(k)). Above it, b_p/p≤k/p²≤1/4, and summing k/m² over integers m>2sqrt(k) costs O(sqrt(k)). This argument requires no prime-density uniformity near sqrt(k).

On omitted primes w_p=f(p/k)+O_a(1/k), f(u)=u^(−1)−1. Since a>1/2, f(u) is bounded away from one. Both logarithms have bounded derivatives on the relevant compact weight range for sufficiently large k. The total replacement error is O_a,z(1), using even the crude bound that there are at most k primes. Weighted PNT on the fixed compact interval [a,1] gives

−log rho=(I(a)+o(1))k/log k,
log product(1+zw)=(J(a,z)+o(1))k/log k,

I(a)=integral_a^1 −log(2−1/u) du,
J(a,z)=integral_a^1 log(1+z(1/u−1)) du.

Thus I+J=K(a,z)=integral_a^1 log((z+(1−z)u)/(2u−1)) du.

Choose even r=2ceil(Ak/(2log k)) with A logz>K. Then log(R/rho)=[K−Alogz+o(1)]k/log k tends to minus infinity. In particular R≤rho/2 eventually.

The larger endpoint cost at omitted primes is essential. With B=sum C_p, the elementary bound B≤2k³ gives e_j(C)≤B^j/j!. Put m=r−1 and U=2k³. Since m≤U eventually,

E≤mU^m/m!≤m(eU/m)^m.

As m=(A+o(1))k/log k, logU−logm=2log k+loglog k+O_A(1), so logE≤(2A+o(1))k. Also −logrho=O(k/logk)=o(k). The specified T satisfies logT≤(2A+o(1))k. Therefore

limsup log g(k)/k ≤ a+2A,

for every fixed A>K(a,z)/logz. Taking the limsup first and then decreasing A gives the sharper variational expression a+2K(a,z)/logz.

## Proposed rational parameters

At a=6/7,z=4,

K=(10/21)log(10/7)+(5/14)log(5/7).

Take A=9/250. Independent exact rational interval evaluation proves

0.0002300415 < (9/250)log4−K < 0.0002300416.

Hence a+2A=813/875<93/100<1. If the frozen author's proof contains these steps accurately, it establishes g(k)<exp(0.93k) for sufficiently large k. PNT also gives logL_k/k→1, so eventually logL_k>0.95k while logg(k)<0.93k; consequently g(k)<L_k eventually. Neither a numerical starting value for these eventual statements nor their validity at every k follows from the asymptotic proof.

The exact finite criterion is effective for each specified k,r,z. This reconstruction does not produce an explicit threshold for the asymptotic assertions. It does not establish exp(o(k)), successive-ratio statements, or priority.
