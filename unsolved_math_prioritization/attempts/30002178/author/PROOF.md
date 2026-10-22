# Lower bounds for sums of roots of unity: five scoped approaches

Problem 30002178 / OWR-12014-013. Author investigation dated 2026-10-05.
Status: unresolved by this investigation; five substantive approach families exhausted. No claim of novelty or of an exhaustive proof that the global problem is still open.

## 0. Exact target and conventions

Write mu_N={exp(2 pi i a/N): a in Z}, and let F(m,N) be the minimum of |z_1+...+z_m| over NONZERO sums with z_j in mu_N. Repetition is allowed, and exactly m summands are counted, including multiplicities. This is complex absolute value, not algebraic norm, height, or a Galois-orbit average. N is a common multiple of the summands' orders; it need not be their least common multiple.

OWR 42/2012, Thang Le, “On homology growth of finite covering,” Conjecture 7 on printed p.2574 asks whether for every fixed m there is E=E(m) such that F(m,N)>N^{-E} for all sufficiently large N. That statement was checked in the publisher PDF, both extracted text and rendered page. Its surrounding Conjecture 6 is a polynomial-evaluation formulation, but we use the unambiguous modulus formulation in Conjecture 7.

Equivalently, for each fixed m there exist c_m>0 and e_m>0 with F(m,N)>=c_m N^{-e_m} for every N>=1. In one direction, choose the minimum of finitely many positive small-N values times N^E and 1. In the other, increase the exponent by 1 and take N>1/c_m. Thus the strict sign and missing leading constant do not change the question.

Signed integer coefficients can be encoded, but the bookkeeping matters: sum c_a zeta_N^a uses L=sum |c_a| roots of order dividing 2N, because a negative root is still in mu_{2N}. When N is even no enlargement is needed. The number of nonzero coefficients is not the number of summands. Arbitrarily large coefficients are not covered by a fixed-m result. If separate orders are merely bounded by d, their common multiple is at most d^m for m summands, not necessarily d; this changes exponents but preserves the existence of a polynomial bound for fixed m.

Identity check: the public descriptor catalog selects ID 30002178, rank 716, title and DOI 10.4171/owr/2012/42. The exact numeric website URL was attempted but inaccessible (HTTP 403). The raw dataset row, raw AI research corpus, and any earlier AI solution text were not inspected. The descriptor's stored statement hash is therefore not represented as a hash of newly verified source text.

## 1. Algebraic norm and Fourier energy

### 1.1 A complete universal exponential bound

Let S=sum_{j=1}^m zeta_N^{a_j} be nonzero. For N>=3 put d=phi(N). Every conjugate under Gal(Q(zeta_N)/Q) has modulus at most m. Since S is a nonzero algebraic integer, its field norm is a nonzero integer. Pairing complex-conjugate embeddings gives

1 <= |Norm(S)| <= |S|^2 m^{d-2}.

Therefore |S| >= m^{1-d/2}. The norm here is the field norm in the entire cyclotomic field, so repeated conjugate values cause no problem. For N=1 or 2, S is a nonzero integer, hence |S|>=1. For m=1 the modulus is exactly 1.

### 1.2 A sharper prime-order bound using multiplicity energy

For an odd prime p, write S=P(zeta_p), P(x)=sum_{a=0}^{p-1}c_a x^a, with c_a nonnegative integers, sum c_a=m, and H=sum c_a^2. Assume S!=0. Orthogonality gives

sum_{t=1}^{p-1}|P(zeta_p^t)|^2 = pH-m^2.

Indeed, summing over t=0,...,p-1 gives pH because sum_t zeta_p^{t(a-b)} is p for a=b and 0 otherwise; remove the t=0 term m^2. Let n=(p-1)/2 and let x_1,...,x_n be one squared modulus per conjugate pair, with x_1=|S|^2. Their product is the positive integer Norm(S), at least 1, and their sum is T=(pH-m^2)/2. For p>=5, the arithmetic-geometric mean inequality gives

1 <= x_1 (T/(n-1))^{n-1},

so |S| >= ((p-3)/(pH-m^2))^{(p-3)/4}.

This deliberately discards x_1 from the sum bound; it is valid even when several conjugate values coincide. For distinct roots H=m; with repetition H may be as large as m^2. If p=3 the single pair directly gives |S|>=1.

### Exact gap

The exponents still grow with phi(N) or p. A uniform exponent depending only on m cannot be read off from them. Positivity of a norm or Fourier energy does not control how many factors can concentrate away from one exceptionally small factor. This route is blocked at exactly that point.

## 2. Direct cancellation geometry for m<=4

We give deliberately nonoptimal constants with complete proofs. These are known cases of the problem, not claimed new. Barber's Proposition 3 gives much sharper values and corrects an older three-term formula.

Use sin x >=2x/pi for 0<=x<=pi/2. Two roots of mu_M whose sum is nonzero have sum modulus at least 2 sin(pi/(2M))>=2/M: the angular separation from exact opposition is at least pi/M. This bound is weaker than the parity-sensitive exact minimum and is valid uniformly.

### m=1 and m=2

F(1,N)=1. The preceding observation gives F(2,N)>=2/N for N>=2. N=1 is immediate.

### m=3

Group two terms as A u, where A>=0 and u is a 2N-th root of unity if A!=0. The half-angle identity gives A=2 cos t for t=j pi/N in [0,pi/2]. If A=0, the total has modulus 1. If A!=1, then |t-pi/3|>=pi/(3N), because 3j-N is a nonzero integer. Hence

|A-1| =4 sin((t+pi/3)/2) sin(|t-pi/3|/2) >=2/(3N).

The first sine is at least 1/2; the second is at least |t-pi/3|/pi. The reverse triangle inequality bounds the three-term sum below by |A-1|. If A=1, the total is a nonzero sum of two 2N-th roots, so its modulus is at least 1/N. Therefore F(3,N)>=2/(3N) for N>=2.

### m=4

Group terms in pairs, with respective magnitudes A=2 cos t and B=2 cos s for t,s in the same grid {j pi/N} intersected with [0,pi/2]. If A!=B, then t!=s and

|A-B|=4 sin((t+s)/2) sin(|t-s|/2)>=4/N^2,

because both nonnegative angles are at least pi/(2N) and at most pi/2. Reverse triangle inequality finishes this case.

If A=B=0 the sum is zero and excluded. If A=B>0, write the total as A(u+v) with u,v in mu_{2N}. A nonzero A is at least 2 sin(pi/(2N))>=2/N. A nonzero u+v is at least 1/N by the two-root bound with M=2N. Consequently F(4,N)>=2/N^2 for N>=2. (A parity-refined chord bound can improve the constant, but is unnecessary.)

### Exact gap

These proofs work because pair magnitudes belong to a one-dimensional cosine grid and the remaining comparison involves at most two lengths. At m=5, a triple magnitude varies with two relative angles; proximity to a pair magnitude is not controlled by separation of two single cosine-grid entries. The three-term proof bounds a triple away from zero, not away from every possible pair magnitude. Induction based solely on nonzero subsum bounds is invalid.

## 3. Factored sums and explicit small constructions

### 3.1 Products of nonzero chord differences

If S=u product_{j=1}^r(v_j-w_j), where u,v_j,w_j lie in mu_N and v_j!=w_j, then every factor has modulus at least 2 sin(pi/N)>=4/N for N>=2. Thus |S|>=(4/N)^r. Expanding gives 2^r signed roots, or exactly 2^r positive root terms in mu_{2N}; coincident terms still count with their multiplicities. This proves polynomial separation for this factorizable family. It does not assert that an arbitrary m-term sum factors this way.

### 3.2 An obstruction to small universal exponents

For even N, S=(1-zeta_N)^r is a nonzero sum of exactly 2^r N-th roots: expand the binomial, replace each negative occurrence by its antipode, and retain all multiplicities. Its modulus is

|S|=(2 sin(pi/N))^r <=(2pi/N)^r.

If an exponent E(2^r)<r satisfied the target, then for sufficiently large even N we would have (2pi)^r N^{-r}<N^{-E(2^r)}, a contradiction. Hence any admissible exponent must satisfy E(2^r)>=r. This is a lower constraint on the possible exponent, not a disproof of polynomial separation. Letting r grow with N changes m and cannot disprove the fixed-m statement.

### Exact gap

We have a lower bound for explicitly factored sums and a matching-order upper construction inside that restricted class. A general m-term sum is not shown to admit a product decomposition with a number of factors controlled by m. The coefficients in such a decomposition, if present, would also need control. The construction is compatible with the conjecture.

## 4. Exact finite-field counting reformulation

This approach is related to Zhuang-Cheng-Wen's 2022 counting method. The derivation below allows repetitions explicitly.

Let p>=3 be prime, 1<=m<p, P(x)=sum_{a=0}^{p-1}c_a x^a with nonnegative integer coefficients of total m. Then P(zeta_p^t)!=0 for every t!=0: otherwise the minimal polynomial 1+x+...+x^{p-1} divides P over Q, forcing P to be a constant multiple of it and m to be divisible by p. Put

D=product_{j=1}^{p-1}P(zeta_p^j)>0.

It is a positive integer since conjugates pair. In Z[x]/(x^p-1) form

R(x)=product_{j=1}^{p-1}P(x^j)=sum r_t x^t,
Q(x)=product_{j=2}^{p-2}P(x^j)=sum q_t x^t.

Empty products are 1. Coefficients count choices with multiplicity. Fourier evaluation gives R(1)=m^{p-1}, and R(zeta_p^b)=D for every nonzero b. Inverting the finite Fourier transform,

p r_0=m^{p-1}+(p-1)D.

Similarly Q(1)=m^{p-3}, and

Q(zeta_p^b)=D/[P(zeta_p^b)P(zeta_p^{-b})]=D/|P(zeta_p^b)|^2.

Thus, writing T=sum_{b=1}^{p-1}|P(zeta_p^b)|^{-2},

p q_0=m^{p-3}+D T,
T=(p-1)(p q_0-m^{p-3})/(p r_0-m^{p-1}).

If M(P)=min_{b!=0}|P(zeta_p^b)|, then

1/M(P)^2 <= T <= (p-1)/M(P)^2.

Consequently a bound T<=C_m p^{A_m}, uniform over all such coefficient vectors, would establish the desired polynomial lower bound for prime N. Conversely a uniform prime-case lower bound implies a polynomial bound for T. This is an exact reformulation up to a factor p, not a solution.

### Exact gap

Integrality gives only D>=1. The numerator involves deviations of counts of m^{p-3} choices; its trivial bound is exponential. The needed polynomial estimate of the displayed ratio has not been proved here. Moreover, even its proof for primes alone would not address all composite conductors. Our exact examples check the identities, not the missing estimate.

## 5. Sparse Taylor expansion near a fixed vanishing configuration

Let P(x)=sum_{j=1}^s c_j x^{a_j} be a nonzero integer polynomial with distinct exponents 0<=a_1<...<a_s<=A, A>=1, and L=sum |c_j|. Let q be the multiplicity of x=1 as a root, allowing q=0.

### 5.1 Sparsity bounds the multiplicity

One has q<=s-1. Otherwise P^{(k)}(1)=0 for k=0,...,s-1. These equations say sum_j c_j(a_j)_k=0, where (a)_k is the falling factorial. The evaluation matrix has determinant product_{i<j}(a_j-a_i), because the falling factorials are monic polynomials of degrees 0,...,s-1 and their basis-change matrix from monomials is triangular with diagonal 1. The determinant is nonzero. Thus all c_j would vanish, a contradiction.

### 5.2 A quantitative local bound

Write P=(x-1)^q Q with Q in Z[x] and Q(1)!=0, so |Q(1)|>=1. Division of an integer polynomial B of degree <=A with B(1)=0 by x-1 produces coefficients that are partial sums of B's coefficients. Hence ||B/(x-1)||_1 <= A ||B||_1. Iterating gives ||Q||_1<=L A^q. For |z|<=1, |Q'(z)|<=A||Q||_1<=L A^{q+1}.

The straight segment from 1 to any |z|=1 stays in the closed unit disk. Thus if |z-1|<=1/(2 L A^{q+1}), then |Q(z)-Q(1)|<=1/2 and |Q(z)|>=1/2. For z=zeta_N, N>=4 pi L A^{q+1} guarantees this smallness condition. The chord lower bound gives

|P(zeta_N)| >= (1/2)(4/N)^q.

This is a complete polynomial lower bound with q<=s-1 in a controlled small-exponent regime, including signed coefficients via the 2N convention above. For q=0 it says the value remains at least 1/2 once the same sufficient threshold holds.

### Exact gap

In the target problem the exponents can have spread A comparable with N; rotating a tuple makes one exponent zero but does not uniformly make all others small. The sufficient condition N>=4 pi L A^{q+1} then fails. Expanding around arbitrary vanishing configurations introduces coefficients depending on that configuration and rational-approximation issues that this integer-at-1 argument does not bound uniformly. A cover by local analytic charts would not itself provide the necessary arithmetic distance from their zero sets. This route is blocked by that missing uniform arithmetic estimate.

## Conclusion

All five routes yield complete scoped deductions, exact constructions, or an exact reformulation. None supplies an exponent depending only on m for all conductors and all nonzero m-term sums. The full target remains unresolved by this work. The small-m cases and general norm bounds are prior mathematics; no historical novelty is asserted for any lemma here.
