# Symmetric lattice-polytope volume: verified partial results

Problem 30000638 / OWR-1394-015. Status: **PARTIAL, ORIGINAL QUESTION UNSOLVED**.
Research checked through 2026-10-06. This is an authored mathematical investigation,
not a claim of novelty, peer review, or a complete resolution.

## 1. Exact scope and attribution

Let P be a full-dimensional convex polytope in R^n, n >= 1, whose vertices
are in Z^n and which satisfies P = -P. Write I(P) = #(int(P) intersect Z^n),
B(P) = #(boundary(P) intersect Z^n), and V(P) = n! vol_n(P), where vol_n
is ordinary Lebesgue volume and the lattice has covolume one. The question is

    V(P) >= 2^(n-1) (I(P)+1).                                      (C)

This formulation is the normalized-volume version of Conjecture 4 on printed
p.3386 of Oberwolfach Report 56/2006, in Martin Henk's contribution with
Christian Bey and Jörg M. Wills [1]. The workshop took place in December 2006;
the source is sometimes bibliographically labeled 2007. The same question is
Conjecture 1.1 of Bey–Henk–Wills [2]. That work already establishes the planar
and crosspolytope cases. Its Remark 1.6 gives h*_i >= binomial(n,i).

The center is a lattice point: lattice translation allows any lattice center
to be moved to zero. A half-integral nonlattice center cannot be treated by
that reduction. We make no assertion here about the distinct nonlattice-center
problem. Full dimensionality is essential to this formulation: lower-dimensional
polytopes in a larger ambient space have ambient volume zero. To treat them one
must change both dimension and volume to the relative lattice conventions.
Origin symmetry implies I(P) is a positive odd integer.

Do not confuse (C) with the classical upper bound
vol_n(P) <= 2^(n-1)(I(P)+1), with Minkowski's successive-minima theorem,
or with the barycenter/one-interior-point Ehrhart volume conjecture.
The h*-coefficients below are binomial-basis Ehrhart coefficients, not the
monomial coefficients of the Ehrhart polynomial.

The public problem webpage was inaccessible in this retrieval (HTTP 403;
the web-reader also failed). Its full supplied record was reviewed, including
all fields and the absent research report represented by {}. The mathematical
target was then independently checked against the primary report's rendered
page and its definitions. No website-access success is being claimed.

## 2. Approach 1: triangulation, planar geometry, and coefficient bounds

### 2.1 Base cases

For n=1, P=[-a,a] with positive integer a. Then I=2a-1 and V=2a=I+1,
so equality holds in (C).

For n=2, Pick's theorem gives V=2I+B-2. A full-dimensional centrally
symmetric polygon has at least four vertices, all lattice points. Thus B>=4
and V>=2(I+1). Equality occurs exactly when B=4, equivalently when P is
a parallelogram whose boundary contains no lattice points except its vertices.
This is the known planar case, not a new solution.

In every dimension, P contains a lattice crosspolytope
C=conv{+/-v_1,...,+/-v_n}, where the v_i are linearly independent lattice
vertices of P. Its normalized volume is 2^n |det(v_1,...,v_n)| >= 2^n.
Consequently V(P)>=2^n, proving (C) whenever I(P)=1.

### 2.2 A boundary-sensitive sufficient condition

Let h*=(h_0,...,h_n). The identities

    h_0=1, h_1=I+B-n-1, h_n=I, V=sum h_i

and Hibi's inequalities h_i>=h_1 for 1<=i<=n-1 are recalled in [2,3].
Together with h_i>=binomial(n,i), valid for origin-symmetric lattice polytopes,
they give the rigorously justified combined bound

    V >= 1+I + sum_{i=1}^{n-1} max{binomial(n,i), I+B-n-1}.          (H)

In particular, for n>=2,

    V >= n I + (n-1) B - n^2 + 2.                                 (H')

Thus (C) follows for every P whose right side in (H) is at least
2^(n-1)(I+1). A simpler sufficient condition is

    (n-1)B >= (2^(n-1)-n) I + 2^(n-1) + n^2 - 2.                 (HB)

These are deductions from the cited inequalities, not a new assertion that
Hibi's bound alone solves the question.

### Corollary: all 3-polytopes with at most five interior lattice points

Every origin-symmetric lattice 3-polytope with I<=5 satisfies (C).
Indeed, B is even and B>=6. If B=6, the polytope has exactly six vertices
and is a crosspolytope, covered by Theorem A. Otherwise B>=8, and (H') gives
V>=3I+2B-7>=3I+9>=4I+4, because I<=5. Thus this statement covers every
polytope with I=1,3,5, without imposing a product decomposition or a search
box. It is an elementary corollary of established results; novelty is not
asserted.

### 2.3 The actual coefficient gap

The formal n=3 vector (1,11,11,7) passes all of the following numerical tests:
nonnegative integer coefficients; h_0=1; positive odd h_3; binomial floors;
the Hibi floors h_2>=h_1; h_1>=I+n-1; and parity congruences
h_i=binomial(n,i) modulo two. The implied boundary count is B=8. Yet its
sum is 30, below 4(7+1)=32. This is an **abstract constraint countermodel**,
not a lattice polytope and not a counterexample to (C). It proves that the
expressly listed coefficient constraints do not logically imply (C).

The stronger coefficient inequality on the same OWR page would imply (C)
by summation. We have not proved that inequality in general; using it as a
lemma would merely replace one open assertion with a stronger one.

Triangulating and pairing simplices by the antipodal map yields evenness of
the number of paired contributions, but does not by itself supply the
exponential factor 2^(n-1) per interior-point pair. Bound (H) makes one
precise version of this shortage visible rather than assuming it away.

## 3. Approach 2: an exact quotient-lattice argument

### Theorem A (known crosspolytope case, elementary proof)

Let A be an invertible integral n by n matrix, D=|det A|, and
C=A{y:sum |y_i|<=1}. Then

    I(C) <= 2D-1,       V(C)=2^n D,

and therefore C satisfies (C).

**Proof.** The sublattice A Z^n has exactly D cosets in Z^n. If x and x'
are distinct interior lattice points of C in the same coset, then
u=A^(-1)x and u'=A^(-1)x' have l1 norms below one, while u-u' is a
nonzero integral vector of l1 norm strictly below two. Hence u-u'=+/-e_i.

There cannot be three such points in a coset. After translating one to zero,
the other two differences would be distinct signed unit vectors; their
difference has l1 norm two, contradicting the preceding bound. Thus every
coset contains at most two interior points. In the zero coset, u is integral
of l1 norm below one, hence u=0, so that coset contains exactly one point.
It follows that I(C)<=1+2(D-1)=2D-1. Decomposing the standard crosspolytope
into its 2^n coordinate simplices gives volume 2^n/n!, proving the volume
formula after applying A. This proves the claim. QED.

The crosspolytope result itself is credited to [2, Proposition 1.4]. We do
not claim this elementary proof is new.

The stretched example C_{n,l}=conv{+/-l e_1,+/-e_2,...,+/-e_n}, l>=1,
has interior points exactly j e_1 for -l<j<l. Therefore I=2l-1 and
V=2^n l, so the conjectured constant is sharp for every positive odd I.

### Corollary A1 (interior-preserving containment certificate)

If C is a lattice crosspolytope contained in P and every interior lattice
point of P lies in int(C), then I(P)=I(C) and (C) holds for P by volume
monotonicity. Indeed int(C) is contained in int(P), since both bodies are
full-dimensional and C is contained in P. This certificate is sufficient,
not a claim that such a crosspolytope always exists.

The ordinary containment C subset P alone is insufficient for this argument.
For example, 2 conv{+/-e_1,+/-e_2,+/-e_3} is contained in [-2,2]^3,
but their interior counts are respectively 7 and 27. A lower bound in terms
of the smaller count cannot simply be rewritten using the larger count.
Both bodies in this example satisfy (C).

The accompanying residue checks use integer adjugate numerators, reduce
them modulo D, and count strictly inside the l1 inequality. Boundary points
are not included. These are finite cross-checks of the proof.

## 4. Approach 3: successive minima and its explicit obstruction

Write lambda_1,...,lambda_n for the successive minima of P with respect
to Z^n. Minkowski's second theorem yields

    V(P) >= 2^n / product_i lambda_i.

It therefore establishes (C) under the additional, explicit condition

    I(P)+1 <= 2 / product_i lambda_i.                              (M)

Condition (M) is not automatic. For P=[-2,2]^3 each minimum equals 1/2,
while I(P)=27. The right side of (M) is 16 and the left side is 28.
Minkowski's lower bound on V is 64, below the required 112, whereas the
actual V is 384. Thus this route can fail to certify a true case: the
failure is in the proposed proof mechanism, not in the conjecture.

The upper half of Minkowski's theorem and the van der Corput upper bound
have the opposite direction from what is needed. No reversal is valid.

## 5. Approach 4: all-dimensional construction theorems

The following closure statements provide genuine infinite families, beyond
checking a finite list of polytopes. They are elementary deductions; no
novelty claim is attached.

### Theorem B (Cartesian products)

If P in R^n and Q in R^m both satisfy the hypotheses and (C), with n,m>=1,
then P times Q satisfies (C), strictly.

**Proof.** Put I=I(P), J=I(Q), N=n+m. Product interiors and product lattices
give I(P times Q)=IJ. Fubini and normalization give

    V(P times Q)=binomial(N,n) V(P)V(Q)
      >= binomial(N,n) 2^(N-2) (I+1)(J+1).

Since binomial(N,n)>=2 and (I+1)(J+1)=IJ+I+J+1>IJ+1, this exceeds
2^(N-1)(IJ+1). All factors are positive and I,J>=1, so strictness is
justified. QED.

### Theorem C (free sum with a one-interior-point factor)

Suppose P satisfies (C), and Q is any full-dimensional origin-symmetric
lattice m-polytope with I(Q)=1. Then

    S=conv((P,0) union (0,Q)) in R^(n+m)

satisfies (C). Neither reflexivity of Q nor an Ehrhart-series product
identity is needed.

**Proof.** Let p and q be the gauges of P and Q. They are nonnegative,
vanish only at zero, and S={(x,y):p(x)+q(y)<=1}. Because Q has no
nonzero interior lattice point, every nonzero y in Z^m has q(y)>=1.
Thus an integral point in int(S) must have y=0, and its x coordinate is
in int(P). Consequently I(S)=I(P).

The x-section of S at y in Q is (1-q(y))P. Since
vol_m{y:q(y)<=t}=t^m vol_m(Q), layer integration gives

    vol_N(S)=vol_n(P) vol_m(Q) m integral_0^1 (1-t)^n t^(m-1) dt
            = vol_n(P) vol_m(Q) n!m!/(n+m)!.

Hence V(S)=V(P)V(Q). The base-case crosspolytope inclusion in Section 2
gives V(Q)>=2^m. Therefore
V(S)>=2^m 2^(n-1)(I(P)+1)=2^(N-1)(I(S)+1). QED.

In particular, a unit lattice bipyramid over P has I unchanged and V doubled.
Repeated unit bipyramids, or free sums with arbitrary origin-symmetric
one-interior-point lattice polytopes, preserve the normalized conjecture gap
up to the indicated volume multiplier. Products of certified bodies are also
certified. Starting from any origin-symmetric lattice polygon, any lattice
crosspolytope, or any origin-symmetric one-interior-point polytope gives an
explicitly specified class satisfying (C) in unbounded dimension.

These closure results do not show that all origin-symmetric lattice polytopes
admit such a decomposition. That is a precise remaining limitation.

## 6. Approach 5: the credited asymptotic theorem and exact boundary test

Henze [4, Theorem 1.1] proves that for every epsilon in (0,1] there is a
dimension threshold n(epsilon) such that, for all larger n and all
origin-symmetric convex bodies K whose lattice points span R^n,

    n! vol_n(K) >= (2-epsilon)^n #(K intersect Z^n).

The hypotheses hold for every P considered here. This is an important
published asymptotic result, but it is not the exact constant in (C).

More usefully for a fixed dimension, equation (2.4) in that proof supplies

    V(P) >= 2^n (I+B) / L_n^+(2),                                 (L)
    L_n^+(2) = sum_{k=0}^n binomial(n,k) 2^k/k!.

The superscript here explicitly records the positive-coefficient convention;
in the common alternating-sign Laguerre convention this is L_n(-2).
Thus (C) holds whenever

    2(I+B) >= L_n^+(2)(I+1).                                      (LB)

This implication is only algebra applied to the cited theorem. The finite
checker verifies the exact identity underlying the coefficient:

    sum_{i=0}^n binomial(n,i)^2 i!/2^i = n! L_n^+(2)/2^n.

Bounds (H), (L), and V>=2^n may be combined by taking their maximum.
For each fixed epsilon>0, (2-epsilon)^n / 2^(n-1) tends to zero;
one cannot take epsilon=0 in a theorem with an epsilon-dependent dimension
threshold. Also G(P)=I+B is not interchangeable with I+1. These distinctions
explain why the asymptotic theorem does not close the exact problem.

## 7. Finite exact evidence and remaining gap

The supplied suite contains 37 explicitly generated 3-dimensional lattice
hulls: stretched crosspolytopes and boxes, two skew crosspolytopes, a scaled
crosspolytope and cube, a hexagonal bipyramid, and 24 deterministic stress
examples. Every calculation uses integer arithmetic. Facet support planes
are recovered from triples of points; each facet is triangulated after an
injective coordinate projection; origin-cone determinants give normalized
volume. Strict facet inequalities count interior points. Independently
computed closed counts for dilations k=0,1,2,3 give h*, whose sum and last
entry are checked against the geometric volume and interior count.

All 37 pass (C) and the stronger displayed OWR coefficient inequalities.
Seven residue examples and 4,900 small product-parameter checks agree with
the general proofs; twenty exact Laguerre identities agree with (L).
These are finite tests and implementation checks, not proof in arbitrary
dimension and not an exhaustive classification of 3-polytopes.

The exact unresolved statement is (C) for arbitrary full-dimensional
origin-symmetric lattice polytopes not certified by the proven sufficient
conditions. No universal interior-preserving crosspolytope, suitable product/
free-sum decomposition, or missing coefficient inequality has been obtained.
The verified literature search found no authoritative complete resolution;
that is a bounded search result, not a proof that no resolution exists.

## References

1. Martin Henk, joint with Christian Bey and Jörg M. Wills, “Roots of Ehrhart
   polynomials,” in *Konvexgeometrie*, Oberwolfach Report 56/2006, pp.3384–3386;
   Conjecture 4, p.3386.
   https://doi.org/10.4171/owr/2006/56
   https://publications.mfo.de/bitstream/handle/mfo/2986/OWR_2006_56.pdf?isAllowed=y&sequence=1
2. Christian Bey, Martin Henk, Jörg M. Wills, *Notes on the roots of Ehrhart
   polynomials*, Discrete & Computational Geometry 38 (2007), 81–98.
   https://arxiv.org/abs/math/0606089
   https://doi.org/10.1007/s00454-007-1330-y
3. Martin Henk, Makoto Tagami, *Lower bounds on the coefficients of Ehrhart
   polynomials*, arXiv:0710.2665v2; especially the identities and Hibi
   inequality in the introduction.
   https://arxiv.org/abs/0710.2665
4. Matthias Henze, *A Blichfeldt-type inequality for centrally symmetric convex
   bodies*, Monatshefte für Mathematik 170 (2013), 371–379; Theorem 1.1 and
   equation (2.4) of the preprint.
   https://arxiv.org/abs/1203.4075
   https://doi.org/10.1007/s00605-012-0461-2
