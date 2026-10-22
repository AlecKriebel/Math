# Proof 06  Finiteness at each prescribed noneven exponent

This earlier counting proof is retained as optional background. The stronger all-exponent circuit-mass bound and finite-shape reduction are in [Proof 29](29_uniform_mass_and_finite_shapes.md).

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Proof dependencies included in this package: [Circuit obstructions and positive uncentered blocks](01_circuit_obstructions.md).

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## Property and credited analytic input

Write MP_p(Gamma) for the constant-one majorant inequality for all finitely supported **real** coefficient families |a_n| <= A_n on Gamma subset Z^d. Let p>0 not be a positive even integer, q=p/2, and m=floor(q).

We use the dominant-coefficient expansion from Gressman–Guo–Pierce–Roos–Yung, *On the strict majorant property in arbitrary dimensions*, Q. J. Math. 74 (2023), 139–161, Proposition 4.1 (arXiv v2 Proposition 10). DOI: https://doi.org/10.1093/qmath/haac021; https://arxiv.org/abs/2106.12538v2. Its circuit specialization, including real signs and the remainder, is proved in the [circuit proof](01_circuit_obstructions.md). The present argument uses only the following necessary consequence:

(C) Every primitive affine circuit lambda, of mass K=sum(lambda_i>0)lambda_i=sum(lambda_i<0)(-lambda_i), satisfies

    binom(q,K) binom(q,K-|lambda_i|) > 0

at every circuit entry i. The strict sign is equivalent to the nonnegative condition because q is nonintegral and none of these binomials is zero. Circuit entries are nonzero, the gcd of all entries is 1, and their sum is 0. The circuit support has at least three points because the frequencies are distinct.

No simultaneous-all-p classification is used. The structural and counting deductions below are consequences of (C). Primitive leading tests are not sufficient for MP_p, as the witness on {0,2,7} in [Proof 19](19_uniform_027.md) proves, in particular at p=5.

## Theorem

Let Gamma be nonempty, with affine dimension r-1, where 1<=r<=d+1. If MP_p(Gamma) holds, then Gamma is finite. More quantitatively:

- If m=0, then |Gamma|<=r. In fact Proof 01 gives the exact affine-independence classification.
- If m>=1 is odd, then

      |Gamma| <= 2m (4m+1)^r.

- If m>=2 is even, let L_m be the smallest power of two strictly greater than m. For r>=2,

      |Gamma| <= 2m (4m+1)^r
                  + L_m (m/2) binom(r,2) (m+1)^(r-2).

  If r=1, Gamma is a singleton.

These deliberately generous bounds depend only on p and the ambient dimension. For even m, every collinear subset of Gamma has at most L_m points. In particular, for 4<p<6, every line contains at most four points.

For infinite Gamma, the theorem has the intended finite-test meaning: there is a finite subset and finitely supported real coefficients witnessing failure. It does not discuss convergence of any infinite Fourier series.

## 1. Binomial signs and general circuit restrictions

Put B(k)=binom(q,k) for integer k>=0. Then B(k)>0 for k<=m+1, and for k>m+1,

    sign B(k)=(-1)^(k-m-1).

Suppose K>m+1. Primitiveness gives an odd circuit entry. If B(K)<0, then K has the parity opposite to m+1. For any odd a=|lambda_i|, the complementary integer K-a has the parity of m+1. Its binomial is positive, whether it lies in the initial positive range or in the alternating tail. This contradicts (C). Consequently

    K == m+1 (mod 2), and B(K)>0.

For an odd entry a, the complementary K-a has the opposite parity and therefore must lie in the initial positive range. Since its parity differs from m+1, actually K-a<=m. Thus every odd entry satisfies

    a >= K-m.                                             (1)

### Odd m

Here K is even when K>m+1. A side containing an odd entry must contain an even positive number of odd entries, because its total K is even. In particular it contains at least two. Formula (1) gives 2(K-m)<=K, hence K<=2m. If K<=m+1, the same conclusion follows from m+1<=2m. Thus every circuit has mass K<=2m.

### Even m

If K>2m (and m>=2), then K>m+1, K is odd, and (1) gives each odd entry size greater than K/2. Each sign side has odd sum K, so each side contains exactly one odd entry. All other entries are even, and the sum of those other entries on each side is at most m. In particular each such even entry is at most m in absolute value.

For m=0, the same initial sign argument forces any circuit to have odd K and its odd entries to have size K. Both sides then have a singleton entry, contradicting circuit support size at least three. This recovers the necessary affine-independence condition.

## 2. Collinear counting lemma for even m

Let S be a finite set of at least two collinear integer points such that every three-point subset passes (C). Parametrize the integer points on their rational affine line by distinct integers. Translate and divide the parameters by the gcd of all parameter differences. We obtain an integer set T with gcd of all differences equal to 1, without changing any primitive triple relation. In particular T contains both even and odd integers.

For a triple with normalized distinct parameters 0<a<b and gcd(a,b)=1, the three vertex tests are

    B(b) B(a)>0,  B(b)>0,  B(b) B(b-a)>0.

(The omitted factors are positive multinomial coefficients.) Therefore B(a), B(b-a), B(b) must all be positive. Equivalently, the binomial indexed by each of the three pairwise distances, divided by their common gcd, must be positive.

For even m, a positive **even** index k has B(k)>0 only when k<=m: the tail positive indices have odd parity, and m+1 is odd.

Suppose u!=v in T have the same residue modulo L_m. They have the same parity, so choose w in T of opposite parity. The common gcd

    g=gcd(|u-w|,|v-w|)=gcd(|u-v|,|u-w|)

is odd. Thus the primitive normalized distance |u-v|/g is a positive multiple of L_m, in particular an even integer greater than m. Its binomial is negative, contradicting the triple condition. Therefore reduction T -> Z/L_m Z is injective, and |S|=|T|<=L_m.

Sets with zero or one point satisfy the same bound. This argument requires no estimate on the original distances.

## 3. A minimum-volume affine basis

We prove the quantitative statements first for finite Gamma. Set v_n=(1,n), and let V be their r-dimensional rational span. The lattice V intersect Z^(d+1) has rank r. Choose an integer basis of this lattice to measure determinants of r independent augmented vectors.

Among all bases drawn from {v_n:n in Gamma}, choose B=(b_1,...,b_r) with smallest positive absolute determinant D. If v in {v_n:n in Gamma} has coordinate expansion

    v=sum_j x_j b_j,

then sum_j x_j=1 because the first coordinates are all 1. If x_j!=0, replacing b_j by v gives determinant of absolute value |x_j|D, so minimality gives

    |x_j|>=1 whenever x_j!=0.                            (2)

For v not in B, its support in this coordinate expansion, together with v, is the unique fundamental affine circuit. Write its primitive relation as

    t v + sum_j lambda_j b_j=0,      t>0,

with zeros at unused basis positions. Then x_j=-lambda_j/t. Its mass is denoted K. Thus (2) says every nonzero basis coefficient satisfies |lambda_j|>=t.

## 4. Counting low-mass points

If K<=2m, then 1<=t<=2m and each lambda_j is an integer in [-2m,2m]. Hence each such point has a coordinate vector in the finite list

    (-lambda_1/t,...,-lambda_r/t),
    1<=t<=2m, lambda_j in {-2m,...,2m}.

This list has at most 2m(4m+1)^r entries. It also includes the r basis vectors (take t=1 and the corresponding numerator -1). Distinct augmented points have distinct coordinate vectors. We have deliberately not deducted tuples violating the sum-one condition or creating duplicates.

For odd m, Section 1 says every nonbasis point is of this type, proving the odd-m bound.

## 5. Covering high-mass points by finitely many lines

Assume m>=2 is even, and consider a fundamental circuit with K>2m. By Section 1 its two sign sides each have exactly one odd entry, each of magnitude at least K-m>m; all remaining entries are even and each side's even total is at most m.

The distinguished coefficient t cannot be odd. If it were, it would exceed m. Since the circuit has at least three entries and has just two odd entries, there is at least one nonzero even entry. It would be a basis coefficient of magnitude at most m<t, contradicting (2).

Consequently t is an even integer with 2<=t<=m. The two odd entries occupy two distinct basis positions i,j. All other basis coefficients lambda_k are even integers in [-m,m]. There are at most

    (m/2) binom(r,2) (m+1)^(r-2)                         (3)

choices for t, the unordered pair {i,j}, and these remaining coefficients. This is just an overcount; impossible choices can be retained.

For any fixed such choice, the affine relation has coefficient sum zero, so

    lambda_i+lambda_j = s := -t-sum_(k!=i,j)lambda_k.

Substitution gives

    v = -(1/t) [lambda_i (b_i-b_j) + s b_j
                         + sum_(k!=i,j)lambda_k b_k].

As lambda_i varies, these augmented vectors lie on a single affine line parallel to b_i-b_j. The first coordinate is 1, so it is an ordinary rational affine line in frequency space. Its direction is nonzero because the basis points are distinct. Every high-mass point therefore lies on one of the lines counted in (3).

Section 2 bounds the number of Gamma points on each line by L_m. Add this to the low-mass bound; multiple counting of points or coincident lines only enlarges the upper bound. This proves the even-m formula.

## 6. Infinite sets

Every finite subset of an MP_p set is again MP_p. For finite subsets, use r<=d+1 in the displayed bounds; the resulting right-hand side is bounded above by the same formula with r=d+1 (with the singleton case handled separately). An infinite Gamma would contain finite subsets of arbitrarily large size, contradicting that uniform bound. Therefore no infinite subset of Z^d has MP_p at any prescribed non-even p>0.

This is a necessary finiteness theorem only. It is not a sufficient classification of the finitely many cardinalities or the infinitely many affine shapes surviving the local tests.
