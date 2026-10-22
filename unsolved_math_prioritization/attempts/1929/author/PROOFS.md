# Separated distances: verified reductions and known constructions

**Status:** Erdős Problem 100 is unresolved by this work. These are elementary reductions, restricted cases, and reconstructions of known examples. No novelty or priority is claimed. The proofs below, rather than the finite controls, carry the quantified assertions.

## 1. Exact target and notation

Let A be a finite set of n distinct points in the Euclidean plane, n >= 2. Write m for its minimum positive distance, D for its diameter, and S = {s_1 < ... < s_k} for its distinct positive distance values. The hypotheses are m >= 1 and s_(i+1)-s_i >= 1. Repetition of the same distance by different pairs is allowed. Distances need not be integers.

The full target asks for an absolute c > 0 and N such that D >= c n for every such A with n >= N. Replacing >= by > does not change the existence of an absolute constant, after decreasing it. The stronger eventual inequality D >= n-1 is a different conjecture. A fixed small counterexample to that stronger inequality does not disprove either eventual claim.

The imported problem is the planar target above. The older source [E85, section VI.5, pp. 8-9] explicitly imposes both hypotheses. The statement and credited nine-point construction are also in [E95, section III.4, author PDF p. 16].

## 2. Spectrum counting and the scale-invariance obstruction

**Proposition 1.** k <= floor(D-m)+1 <= floor(D).

**Proof.** Adding the k-1 successive gap inequalities gives D=s_k >= m+k-1. Because m >= 1, D >= k. The floor statements follow because k is integral. This includes k=1. QED.

Combining Proposition 1 with the imported Guth-Katz theorem [GK15, Theorem 1.1] gives D >= c_0 n/log n for n >= 2, with a positive absolute constant. We have checked the theorem's published statement; this packet does not reprove its 36-page proof. This deduction does not remove the logarithm.

**Proposition 2.** Every finite set of distinct planar points can be dilated into a set satisfying the target hypotheses.

**Proof.** Its finite nonempty positive spectrum has a positive minimum m_0. If it has at least two values, its minimum successive gap g_0 is positive; choose t >= max(1/m_0,1/g_0). If it has one value, choose t >= 1/m_0. Dilation by t multiplies every distance and every distance gap by t. QED.

In particular, the admissibility hypothesis alone cannot rule out a scale-invariant equality pattern of distances. For completeness, if f(s) counts unordered pairs at distance s and B=n(n-1)/2, then Cauchy-Schwarz gives B^2 <= k sum_s f(s)^2, hence D >= B^2/sum_s f(s)^2. A uniform O(n^3) energy bound would yield a linear diameter estimate by this route. However, such a scale-invariant bound cannot be justified just by admissibility: Proposition 2 would extend it to every planar configuration. In fact, using the standard lattice distinct-distance estimate recalled in [GK15, introduction], k is of order n/sqrt(log n) on square grids, so Cauchy-Schwarz already forces energy of order at least n^3 sqrt(log n) along that family. This last growth fact is imported; no new energy theorem is claimed. The desired diameter bound must retain scale information beyond equality multiplicities alone.

## 3. Two-anchor counting and an explicit n^(3/4) bound

**Proposition 3.** For every admissible A with n >= 2,

n-2 <= 2 k (2 floor(m)+1) <= 6 m D.

**Proof.** Choose distinct p,q in A with |p-q|=m. Each z outside {p,q} specifies radii r=|z-p| and s=|z-q| in S. The reverse triangle inequality gives |r-s| <= m. For any fixed r in S there are at most floor(m) spectrum values on each side within m of r: ordered values are at least 1 apart. Including r itself, this gives at most 2 floor(m)+1 possibilities for s. For each ordered pair (r,s), two circles centered at distinct points p and q have at most two intersections. The n-2 points are therefore bounded by twice the number of possible ordered pairs. Finally, k <= D and 2(2 floor(m)+1) <= 6m because m >= 1. QED.

This proves a linear estimate D >= (n-2)/(6M) whenever the extra hypothesis m <= M holds for a fixed constant M. That extra hypothesis is not present in the target.

**Proposition 4.** For n >= 3,

D >= sqrt((n-2)(sqrt(n)-1)/12).

**Proof.** Open disks of radius m/2 about points of A are pairwise disjoint. Fix p in A. All these disks lie in the disk about p of radius D+m/2. Area comparison yields n(m/2)^2 <= (D+m/2)^2, or m(sqrt(n)-1) <= 2D. Inserting this into n-2 <= 6mD gives n-2 <= 12D^2/(sqrt(n)-1), which is the stated result. QED.

This reconstructs the known exponent 3/4 with a nonoptimal explicit constant. The historical exponent is credited to Kanold, also directly mentioned in [E85, p. 9]. We have not identified and inspected the original Kanold proof, so we do not assert that the argument here is Kanold's precise argument or that its constant matches his.

**Corollary.** If admissible sets A_j with n_j -> infinity were to satisfy D_j/n_j -> 0, their minimum distances m_j would necessarily tend to infinity. Indeed, Proposition 3 implies m_j >= (n_j-2)/(6D_j). This is a necessary condition, not a counterexample construction or a proof of the target.

## 4. The exactly-unit-minimum case and the normalization trap

**Proposition 5.** If an admissible set contains a pair p,q at distance exactly 1, it lies in the union of the line pq and its perpendicular bisector. Consequently n <= 2 floor(D)+2, so D >= (n-2)/2.

**Proof.** For any z in A, write r=|z-p| and s=|z-q|. We have |r-s| <= 1. If r=s, z lies on the perpendicular bisector. If r != s, the gap hypothesis implies |r-s| >= 1; this is still true when z=p or q because then {r,s}={0,1}. Thus |r-s|=1. Equality in the reverse triangle inequality forces z,p,q to be collinear. Each of the two lines contains at most floor(D)+1 points of A, because its ordered consecutive points are at least unit distance apart and its total span is at most D. Summing the two bounds proves the claim, even if the two line subsets meet. QED.

The hypotheses of this proposition have a unit distance that is attained. In contrast, the full target only requires m >= 1. Dividing coordinates by m divides distance gaps by m, and need not preserve admissibility. The right triangle with vertices (0,0),(3,0),(0,4) has distance values 3,4,5 and is admissible. Scaling by 1/3 gives values 1,4/3,5/3, whose distinct gaps are 1/3.

This distinction is consequential in reading [PRV05/06, author preprint p. 13]: its concluding “admissible” variant specifies that the minimum distance is exactly 1. The reported lower bound n^(1/(d-1)) in that paragraph therefore does not solve the full target in dimension two. Proposition 5 supplies an elementary proof in that restricted dimension. We make no claim about novelty of this restricted observation.

## 5. Thin strips and bounded width

**Proposition 6.** Suppose an admissible set lies in a strip of width h with 0 <= h < 1. Then D >= (n-1)sqrt(1-h^2).

**Proof.** Rotate coordinates so the strip is horizontal. Two points cannot have the same first coordinate because their vertical separation is at most h<1. Order the n first coordinates. For each consecutive pair, unit minimum separation and vertical separation <=h imply a horizontal gap >=sqrt(1-h^2). Summing gives a horizontal span of at least (n-1)sqrt(1-h^2), and the Euclidean diameter is at least this span. QED.

**Proposition 7.** If the set lies in a strip of arbitrary finite width h, then D >= pi*n/[4(h+1)]-1.

**Proof.** The set lies in a rectangle whose horizontal span is at most D and whose vertical span is at most h. The pairwise disjoint open disks of radius 1/2 about its points lie in the expanded rectangle of side lengths D+1 and h+1. Their total area n*pi/4 is therefore at most (D+1)(h+1). Rearranging proves the result. QED.

For fixed h these are linear estimates; for h=o(1), Proposition 6 approaches the stronger coefficient 1. They use only point separation, and are elementary packing observations. They do not subsume Brass's sharper asymptotic half-strip result [Br96], whose publisher abstract was inspected but whose full proof was not retrieved. No theorem reducing arbitrary admissible configurations to bounded-width strips was proved. In particular, a hypothetical sublinear-diameter sequence must also have unbounded minimum enclosing strip width, by Proposition 7.

## 6. Exact grid-family control

Let a>=1 be an integer, and G_a={0,...,a}^2, with n=(a+1)^2. Its positive distances have form sqrt(u^2+v^2), with 0<=u,v<=a and not both zero.

**Proposition 8.** The dilated grid 4a G_a is admissible and has diameter 4sqrt(2)a^2. Conversely, every dilation t G_a that is admissible has diameter strictly greater than 2sqrt(2)a^2.

**Proof.** Distinct squared grid distances are integers between 1 and 2a^2. If b>c are two such integers, then sqrt(b)-sqrt(c)=(b-c)/(sqrt(b)+sqrt(c)) >= 1/(2sqrt(2)a). Dilation by 4a makes this gap at least sqrt(2)>1 and makes the minimum distance 4a>=1. The diameter is 4a times sqrt(2)a.

For the converse, G_a realizes both a and sqrt(a^2+1), using displacements (a,0) and (a,1). Thus t(sqrt(a^2+1)-a)>=1, so t>=sqrt(a^2+1)+a>2a. Multiplying by the grid diameter sqrt(2)a gives the strict lower bound. QED.

Therefore the canonical square-grid family, after a valid separation normalization, has diameter of order n. Its unscaled diameter of order sqrt(n) cannot be used as a counterexample. This is a family exclusion, not a lower bound for arbitrary configurations.

## 7. Piepmeyer's nine-point example: exact reconstruction

This is the finite construction credited to Piepmeyer in [E95, p. 16], not a new example. Set

x=(1+sqrt(2))*sqrt(2-sqrt(3)),
a=x/sqrt(3), b=a+x, c=-a-b,
U={(1,0),(-1/2,sqrt(3)/2),(-1/2,-sqrt(3)/2)},
A=aU union bU union cU.

There are nine points: the three nonzero signed radii give distinct triples, and none of the three directions in U is the negative of another. The triples aU and bU are concentric, equally oriented equilateral triangles; their corresponding vertices are distance x apart. For each direction u_i, c*u_i is equidistant from the four endpoints of the two sides opposite u_i. This follows by expanding the squared distances, or by the circle-center check in the exact code.

**Proposition 9.** The distinct positive distances are, in increasing order,

x, 1+sqrt(2), 2+sqrt(2), 2+sqrt(2)+x,

with unordered-pair multiplicities 6,18,6,6. Their smallest gap is exactly 1; the minimum distance exceeds 1; and D<5.

**Proof.** Distinct unit vectors in U have inner product -1/2. For equal directions the distance between r*u_i and s*u_i is |r-s|; for unequal directions its square is r^2+rs+s^2. Within each triple its side length is sqrt(3)|r|. Applying these formulas gives the following complete 36-pair partition:

- Within aU: 3 distances x
- Between aU and bU: 3 distances x, 6 distances 1+sqrt(2)
- Between aU and cU: 3 distances 2+sqrt(2), 6 distances 1+sqrt(2)
- Within bU: 3 distances 2+sqrt(2)
- Between bU and cU: 3 distances 2+sqrt(2)+x, 6 distances 1+sqrt(2)
- Within cU: 3 distances 2+sqrt(2)+x

The simplifications use sqrt(2-sqrt(3))=(sqrt(6)-sqrt(2))/2 and (1+sqrt(3))x=2+sqrt(2). All expressions belong to Q(sqrt(2),sqrt(3)); direct coefficient arithmetic verifies every squared-distance identity. All named lengths are positive, so equality of squares gives equality of distances.

For explicit inequalities, the rational bounds 1414/1000<sqrt(2)<1415/1000, 1732/1000<sqrt(3)<1733/1000, and 2449/1000<sqrt(6)<2450/1000 follow by squaring. They imply 1249/1000<x<1251/1000. Consequently the first gap 1+sqrt(2)-x exceeds 1, the second gap is exactly 1, and the third is x>1. Also D=2+sqrt(2)+x<4666/1000<5. QED.

The program verifies stronger rational bounds 4.663<D<4.664 and 1.249<x<1.250 without floating-point decisions. This confirms that D>=n-1 is false for all n without an eventual qualifier. It says nothing against the conjecture for sufficiently large n, and nothing against D>=c*n for a sufficiently small absolute c. Rescaling this example to minimum distance 1 also fails: the gap that was exactly 1 becomes 1/x<1.

## 8. Exact remaining gap

No argument supplies a constant c independent of both minimum distance and width. No family with D/n tending to zero has been constructed. The universal lower bound retained from existing literature remains c_0 n/log n. None of the finite tests, known small examples, conditional energy observations, or restricted results removes that logarithm.

## References

- [E85] Paul Erdős, *Problems and results in combinatorial geometry*, author archive, section VI.5, pp. 8-9: https://www.renyi.hu/~p_erdos/1985-23.pdf
- [E95] Paul Erdős, *Some of my Favourite Problems in Number Theory, Combinatorics, and Geometry*, Resenhas 2(2) (1995), 165-186, section III.4; author PDF p. 16: https://www.ime.usp.br/~yoshi/resenhas/abstracts/Erdos.pdf ; publisher record: https://doi.org/10.11606/resimeusp.v2i2.74798
- [GK15] Larry Guth and Nets Hawk Katz, *On the Erdős distinct distances problem in the plane*, Annals of Mathematics 181 (2015), 155-190, Theorem 1.1: https://annals.math.princeton.edu/2015/181-1/p02
- [PRV05/06] János Pach, Radoš Radoičić, Jan Vondrák, *On the diameter of separated point sets with many nearly equal distances*, European Journal of Combinatorics 27 (2006), 1321-1332. Inspected author preprint dated April 8, 2005, p. 13: https://www.renyi.hu/~pach/publications/distances040805.pdf ; DOI https://doi.org/10.1016/j.ejc.2006.05.007
- [Br96] Peter Brass, *On the Erdős-diameter of sets*, Discrete Mathematics 150 (1996), 415-419. Abstract only: https://doi.org/10.1016/0012-365X(95)00208-E
- Thomas F. Bloom, Erdős Problem 100: https://www.erdosproblems.com/100 . Direct live retrieval was unsuccessful on 2026-10-05; indexed page and discussion contents were consulted, not represented as a verified live snapshot.
