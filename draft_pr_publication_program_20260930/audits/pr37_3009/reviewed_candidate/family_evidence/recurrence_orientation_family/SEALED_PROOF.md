# Independent recurrence and orientation proof audit

Target: numeric 3009, KP-5.2. Original head
`84bb43d21b36e4d97229806e2518fbc135bee786`; original base
`c6975ca76f9f667f1250ba403d0e6da2aafe14d0`.

This proof was written after the complete literal source record and frozen
PARTIAL.md, and after reading the complete Kolev–Pérouème v3 primary paper.
No historical independent_review or root/sibling interpretation was read before
this file was sealed. It is a validation artifact, not an additional substantive
attempt to solve the unresolved full target.

## Exact hypotheses

Let h be a homeomorphism of Euclidean R^d. There is a SINGLE finite D >= 0
bounding the diameter of {h^k(x): k in Z}, for EVERY x. Recurrence means
h^(n_j) converges to id uniformly on each compact set, where positive integers
n_j tend to infinity. Repeated exponent zero would be a vacuous condition and
is excluded. Periodic maps are included because exponents can be distinct even
when the resulting maps coincide. The source's “subsequence of powers” is
interpreted in this conventional sense; the stronger smooth recurrence variant
is a separate condition.

The exact claims audited here are the all-integer displacement reformulation,
orientation, passage to the compact sphere, the one-dimensional conclusion, and
the validity/category of disk gluing. The planar identity conclusion then uses
the two stated classical planar theorems. The higher-dimensional, arbitrary
open-set, arbitrary manifold, and stronger smooth questions are not conclusions
of this argument.

## 1. Exact diameter/displacement equivalence

The diameter hypothesis immediately gives |h^k(x)-x| <= D, because x is the
zeroth point of its full orbit. Conversely, suppose this inequality holds for
all x and all k in Z. For arbitrary a,b in Z put y=h^b(x) and k=a-b. Then
|h^a(x)-h^b(x)|=|h^(a-b)(y)-y| <= D. This gives the SAME diameter constant,
not 2D. Negative exponents are legitimate because h is invertible. A bound on
just h(x)-x is insufficient: translation x -> x+1 satisfies that bound and has
unbounded full orbits. The case D=0 gives identity immediately.

## 2. Orientation requires a proper homotopy, not an isotopy

For every t in [0,1] define H(x,t)=x+t(h(x)-x). The one-step displacement bound
gives |H(x,t)| >= |x|-D. Thus if H(x,t) lies in a compact set contained in the
radius-M ball, x lies in the radius-(M+D) ball. Its inverse image is closed in
that ball times [0,1], hence compact. In particular the escape estimate is
uniform in t.

Extend by H(infinity,t)=infinity on the one-point compactification S^d. Given a
neighborhood of infinity with bounded complement, the same escape estimate
gives a neighborhood of infinity whose product with all [0,1] maps into it.
This proves continuity at every (infinity,t), including the endpoints. The
extended homotopy connects id to the extension of h. Therefore their induced
maps on H_d(S^d;Z) agree. The degree is +1; the plane extension and h preserve
orientation. None of H_t is asserted to be one-to-one or a homeomorphism.

Reflection of the line/plane is a genuine orientation-reversing recurrent map,
but its displacement is unbounded. It therefore does not satisfy the premise
used in this degree argument.

## 3. A uniform, quantified tail estimate

Stereographic coordinates give the chordal distance

q(x,y)=2|x-y| / (sqrt(1+|x|^2) sqrt(1+|y|^2)),
q(x,infinity)=2/sqrt(1+|x|^2).

For |x| >= R > D and any INTEGER k, the displacement bound gives
|h^k(x)| >= |x|-D >= R-D. Thus

q(h^k(x),x) <= 2D / (sqrt(1+R^2) sqrt(1+(R-D)^2)).

The uniformity in k is essential to this specific estimate. Choose R large
enough that the displayed bound is below epsilon. On the closed radius-R ball,
compact-open recurrence gives a J such that for j >= J the Euclidean
displacement is below epsilon/2. Since both denominator factors are at least
one, q <= 2 times Euclidean displacement. The tail and compact-ball estimates,
with the fixed infinity point, show sup_(S^d) q(hat(h)^(n_j),id) <= epsilon.

The quantifiers are R=R(D,epsilon), followed by J=J(R,epsilon), followed by
every j >= J and every sphere point. No uniform Euclidean convergence on all
of R^d has been used. This proof uses the orbit bound; it does not claim that
the bound is a necessary condition for every conceivable sphere-convergence
argument. Irrational plane rotation is a useful control: it recurs on compact
sets and on the sphere, yet its Euclidean displacement supremum is infinite
at every nonzero iterate. It is not a counterexample to sphere recurrence.

## 4. Exact imported sphere theorem and proof dependencies

The operative primary source is Kolev–Pérouème,
[Recurrent Surface Homeomorphisms, arXiv:math/0303258v3](https://arxiv.org/pdf/math/0303258),
Theorem 1.1, printed p.2. It restricts a nonidentity recurrent orientation
preserving S^2 homeomorphism to exactly two fixed points. Its p.1 recurrence is
uniform convergence with exponents tending to positive infinity. The p.2 disk
consequence is explicit. The manuscript date is 12 August 1996; arXiv v3 is
2 March 2009; the journal reference is Math. Proc. Cambridge Philos. Soc.
124(1), 161–168 (1998), DOI 10.1017/S0305004197002272. The DOI fetch failed;
this family read the v3 proof, not journal PDF bytes.

Sections 2–3 use prime ends (Epstein/Mather), inherited recurrence, the Birkhoff
continuum construction, a recurrent annulus lift fixed at a point, monotonicity
on its boundary lines, Brouwer translation arcs, and Brown–Kister invariance
of complementary domains. These are disclosed imports, not finite-computation
certificates. No equicontinuity or compact cyclic closure hypothesis occurs in
Theorem 1.1. The introduction explicitly distinguishes recurrence from regularity.

For the annulus lift step, independently check the normalization: if g^(n_j)
is uniformly close to id on a closed annulus, the displacement of a lift is
close to some integer on the horizontal coordinate, and close to zero on the
vertical coordinate. The integer is constant on the connected cover strip.
A lift fixing a chosen point has F^(n_j) fixing that point, so the integer is
zero. The resulting uniform return on boundary lines contradicts any strict
monotone displacement there. This explains why an arbitrary, unnormalized lift
cannot be substituted.

This family has read the complete v3 proof and disclosed its imports. It has
not rederived prime-end theory or reverified all cited foundational papers.
The Cartwright–Littlewood input is separately identified below; its historical
primary proof is not claimed read by this family.

## 5. Independent completion of the planar implication

Assume d=2 and D>0. For a point a let U be the union of h^k(B(a,2D)) over all
integers. Each summand is connected and meets B(a,2D), since it contains h^k(a)
and |h^k(a)-a| <= D. Therefore U is connected. Each summand is open; index
shift proves h(U)=U. For z in B(a,2D), |h^k(z)-a| < 3D. Consequently
B(a,2D) subset U subset B(a,3D).

C=closure(U) is a compact invariant continuum. Let V be the unbounded
component of R^2 minus C and K=R^2 minus V. This is the filled continuum.
Every point outside the closed 3D ball lies in V; every bounded complementary
component has boundary in C. The closure of each such component is connected
and meets C, so their union with C is connected. K is closed and bounded and
has connected complement V. Because a plane homeomorphism is proper, h maps
the unbounded component to itself. Thus h(K)=K.

Cartwright–Littlewood says that an orientation preserving plane homeomorphism
preserving a nonempty nonseparating continuum has a fixed point in it. Applied
to this K, it produces a fixed point in the closed 3D ball around each a.
Choose two centers at distance greater than 6D. Their two balls are disjoint,
so there are two distinct finite fixed points. Infinity is a third fixed point
of the recurrent orientation preserving sphere extension. Theorem 1.1 excludes
a nonidentity extension; h is identity.

The primary Cartwright–Littlewood/Brown proof is an imported dependency not
reproved by this audit family. The mechanism above checks every use of its
stated hypotheses. This is a known-theorem consequence, not a novelty claim.

## 6. The line and the boundary-fixed ball

A homeomorphism of R is strictly increasing or strictly decreasing. A
decreasing surjection has h(x) -> -infinity as x -> +infinity, contradicting
bounded |h(x)-x|. If an increasing h satisfies h(x)>x at one point, induction
gives h^m(x)>=h(x)>x for EVERY positive m. Recurrence at that point is then
impossible. The inequality h(x)<x gives the opposite contradiction. Hence
h=id. On a compact interval, fixing the two endpoints forces increasing
orientation and the same pointwise argument applies.

For a closed unit ball homeomorphism fixing the boundary pointwise, define g=h
on the ball and g=id outside. The two definitions agree on the boundary;
the pasting lemma gives continuity. Applying the same construction to h^-1
gives a continuous inverse, so g is a homeomorphism. All nontrivial full
orbits remain in the ball, with diameter at most 2; exterior points are fixed.
For a compact set C in R^d, its part in the ball is compact, and convergence
uniform on the whole ball bounds the displacement on C. Thus recurrence
extends. The cases d=1,2 follow from the conclusions already proved.

This construction is a topological extension even when h is smooth. It is not
a claimed smooth extension. As a category control, the smooth closed-ball map
h(x)=(1+(1-|x|^2)/4)x has radial derivative 1/2 and tangential derivative 1 on
the unit boundary. Its radial map is strictly increasing: derivative
5/4-3r^2/4 >= 1/2 on [0,1]. It is a smooth diffeomorphism fixing the boundary,
but gluing it to exterior identity produces radial derivatives 1/2 and 1 on
the two sides. The glued map is not C^1. This example is not recurrent and is
used only to falsify a smooth-gluing claim.

## 7. Actual controls and exact unresolved scope

1. Irrational rotation on R^2 has compact-open recurrence, no nonzero identity
   power, and unbounded orbit diameters as radii increase. Pell approximants
   make the return sequence explicit. It rejects Euclidean-uniform and
   periodicity replacements without contradicting the audited theorem.
2. The same rotation on the annulus D/6 < |x| < D/3 has orbit diameters < D,
   smooth recurrence, and is nonidentity. Therefore the naive local statement
   obtained by merely replacing R^2 with an arbitrary open set and keeping
   “one finite diameter bound” is false. The source's informal neighborhood
   smallness needs a separate precise formulation; the frozen PARTIAL claims
   no theorem for that variant.
3. On S^3 subset R^4, rotate the first two coordinates by an irrational angle
   and fix the other two. This orientation preserving recurrent smooth map
   has fixed circle S^1. The S^2 fixed-point count is dimension-specific. Its
   Euclidean stereographic form does not supply the full-orbit bound of KP-5.2.
4. There is an explicit compact-space recurrence/equicontinuity control.
   Put Y={0} union {1/j:j>=1}, X=Y times R/Z, epsilon_j=2^(-j-3).
   Let C_j be the circle homeomorphism that maps [0,epsilon_j] linearly to
   [0,1/2] and [epsilon_j,1] linearly to [1/2,1]. Put m_0=1 and
   m_j=2^(j+2)m_(j-1). On fiber j define f=C_j^-1 R_(1/m_j) C_j, and on
   fiber 0 define f=id. Both f and f^-1 converge uniformly to id as j grows,
   since C_j^-1 has Lipschitz constant at most 2 and a step displacement <=2/m_j.
   Thus this is a compact-space homeomorphism. At exponent n_k=m_k, fibers
   j<=k are fixed; on fibers j>k the displacement is <=2m_k/m_j<=2^(-k-2).
   Hence f^(m_k) -> id uniformly. In fiber j, points 0 and epsilon_j/2 have
   initial distance epsilon_j/2 ->0, but at exponent m_j/2 their distance is
   (1-epsilon_j)/2 >=1/4. Thus all iterates are not equicontinuous. Compactness
   of the cyclic closure would force equicontinuity (joint continuity on a
   compact family times compact X); it therefore also fails in this model.
   This is not a manifold or KP counterexample, and it does not independently
   settle whether this model's cyclic closure is locally compact. It does
   independently refute a general recurrence-to-equicontinuity/compactness
   inference. The surface-specific published example is disclosed above.

The remaining full target gap is a mechanism in dimensions >=3 under exactly
the stated assumptions, including the special ball and stronger smooth
versions; no such mechanism has been supplied. Adding periodicity, compact
cyclic closure, equicontinuity, or a locally compact acting group is extra
information, not a verified deduction of recurrence. The local/manifold
remarks also need precise quantitative hypotheses. The frozen low-dimensional
argument makes none of these substitutions.

No foreign person was contacted. No new literature search beyond the operative
frozen references was used, and no frozen or canonical research artifact was
edited. Computational replays below are controls for formulas/constructions;
they are not substitutes for the imported topological theorems.
