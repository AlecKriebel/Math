# Boundary geometry, exact sign balance, and a larger excluded quartic family

The [independent construction audit](CONSTRUCTION_AUDIT.md) reviews these results. The complete [authored rational certificate](SECOND_PASS_CERTIFICATE.json) and [mathematical reproduction conventions](REPRODUCTION.md) accompany this proof.

## Scope and outcome

This is one construction branch of the second newly documented substantive pass on row 1761 / problem 30002861 / OWR-13678-002, dated 2026-10-13 UTC. It is the same pass as the parallel conceptual work, not an additional count. The lifetime pass count remains unknown. Every coordinate in the new example below was authored in this work; no third-party dataset is reproduced.

The setting is the accepted fixed conforming straight-line triangulation of a polygonal disk, with nondegenerate triangles, arbitrary values and both gradient components at every vertex, and globally C1 piecewise polynomials of total degree at most four. No refinement, vertex movement, boundary conditions, or extra smoothness is introduced.

The accepted [first-edition reduction](first_edition/QUARTIC_REDUCTION.md) is Rm=Hj, with the [convex-support theorem](first_edition/CONVEX_SUPPORT.md) and [independent baseline acceptance](first_edition/QUARTIC_AUDIT.md). A nonzero left dependency of R exists precisely on a closed active row component whose edge propagation ratios multiply to one around every cycle. The previous convex-support theorem says that a closed component induces a convex triangulated polygon, with even induced degrees at strict boundary corners, odd induced degrees at straight boundary vertices, and at least three nonsingular degree-four interior vertices.

This branch establishes three partial results:

1. Every closed support has at least five strict convex boundary corners. Adjacent strict corners must have interior angles whose sum is greater than pi, even when their connecting side is subdivided by straight boundary vertices. Consequently neither the proposed octahedron-minus-face core with triangular boundary nor any quadrilateral core can acquire the required exterior attachments.
2. There is a completely verified rational 18-vertex disk with a closed 12-row support for which every cycle has positive sign. Its actual matrix has full row rank. Thus sign imbalance cannot be a universal explanation for quartic surjectivity; magnitudes are essential.
3. No admissible member of a three-parameter, threefold-symmetric alternating-radius hexagonal family can be cycle-balanced. A short exact identity in three edge balance equations contradicts the necessary geometric inequalities. This extends the first-pass homothetic-family exclusion.

No general quartic counterexample or universal surjectivity theorem is claimed.

## 1. The exterior attachment theorem

Let K be the convex induced complex of one closed active component. Collapse only the collinear subdivisions of its boundary and call the strict corners A_0,...,A_(k-1), counterclockwise. Let delta_i in (0,pi) be the positive exterior turning angle at A_i. Thus sum delta_i=2 pi.

Consider a strict side A_i A_(i+1), including any straight boundary subdivision vertices between its ends. Each constituent mesh edge has one incident triangle in K and one outside K. The third vertex of its outside triangle is outside the support.

At a straight boundary vertex the zero-ray classification gives exactly one exterior neighbor. Therefore the outside triangles on its two adjacent boundary edges have the same opposite vertex. Continuing along the subdivided side shows that every constituent edge has one common exterior opposite vertex Q_i.

At a strict corner there are exactly two adjacent exterior zero rays. The zero condition says that the neighbors on either side of a zero ray are opposite collinear rays. Consequently the exterior vertex adjacent to side A_i A_(i+1) lies on the outward continuation of the preceding side at A_i, and on the outward continuation of the following side at A_(i+1). In symbols,

Q_i = A_i + t_i (A_i-A_(i-1))
    = A_(i+1) + s_i (A_(i+1)-A_(i+2)),

with t_i,s_i strictly positive. The parameters absorb the possibly different side lengths. Straight subdivision vertices do not change these line directions.

To read the resulting angle restriction, place A_i=(0,0) and A_(i+1)=(L,0), L>0. The two unit outward directions are

(cos delta_i, -sin delta_i),
(-cos delta_(i+1), -sin delta_(i+1)).

If their positive rays meet with positive length parameters t,s, their coordinates give

t sin(delta_i+delta_(i+1)) = L sin delta_(i+1).

The right side and t are positive. Since the sum of the two turns lies in (0,2 pi), this forces

delta_i+delta_(i+1) < pi.

Equivalently, the two adjacent strict interior angles sum to more than pi. Summing over all strict sides gives 4 pi<k pi, hence k>=5.

For the proposed octahedron-minus-face core, this obstruction already occurs before cycle balance. With triangular boundary A,B,C, the opposite vertex across AB would have to lie on both A+t(A-C) and B+s(B-C), with t,s>0. Their supporting lines meet only at C, which belongs to neither positive outward ray. A valid triangular disk realization of that core cannot be extended into a closed support. The quadrilateral exclusion follows from the summed strict inequality. This reasoning does not presume a generic-position boundary and includes every legal straight subdivision.

## 2. An exact sign-balanced closed support

### 2.1 Coordinates and faces

Take the following six outer-core vertices, in counterclockwise order:

O_0,...,O_5 = (62,13), (25,29), (-41,32), (-49,8), (-22,-26), (31,-43).

Take the six inner vertices:

I_0,...,I_5 = (24,-1), (14,5), (-6,16), (-14,4), (-18,-5), (6,-7).

Let Q_i be the intersection of the lines O_(i-1) O_i and O_(i+1) O_(i+2). Exact arithmetic gives

Q_0=(29357/421,11353/421),
Q_1=(-4262/127,6899/127),
Q_2=(-49801/721,23992/721),
Q_3=(-9967/176,-2621/176),
Q_4=(37913/2566,-92773/1283),
Q_5=(47631/73,-17691/73).

For i modulo 6 include the four oriented triangles

(O_i,O_(i+1),I_(i+1)),
(O_i,I_(i+1),I_i),
(O_i,Q_i,O_(i+1)),
(O_i,Q_(i-1),Q_i).

Add the four central triangles

(I_0,I_1,I_2), (I_2,I_3,I_4), (I_4,I_5,I_0), (I_0,I_2,I_4).

There are 18 vertices,28 triangles,45 edges and 39 interior edges. The six Q vertices form the mesh boundary. All twelve O and I vertices are even-valence nonsingular interior vertices. The degree-four vertices are I_1,I_3,I_5.

Exact checks establish positive orientation of every triangle, all 378 pairwise triangle intersections against their prescribed common faces, the links at all 18 vertices, triangle connectedness, a single simple boundary cycle, and Euler characteristic 1. The certificate and reproduction conventions permit independent rational verification of every input and condition. Thus this is a complete conforming disk, rather than an algebraic arrangement with overlapping faces.

### 2.2 Signed and actual ranks

The edge matrix R has 12 rows and 45 columns. Every nonzero column has exactly two nonzero entries, and its active graph is connected. Thus all twelve rows form one closed support.

For reproducibility, order each vertex fan through counterclockwise triangle links starting from the least numbered neighbor, and use

r_(v,i)=(-1)^i det(d_(i-1),d_(i+1))/(a_(i-1) a_i),

a_i=det(d_i,d_(i+1)).

Number O_i by i, I_i by 6+i, and Q_i by 12+i. In row order 0,...,11 the entrywise sign matrix sign(R) has the full-support left null vector

(1,-1,-1,-1,-1,1,1,1,-1,1,-1,1).

Its rank is 11. Therefore every edge propagation cycle has positive sign. Different nonzero row normalizations only change the displayed signs of this vector; they do not change that conclusion.

The actual rational matrix R has rank 12, and adjoining all 54 jet columns leaves rank 12. The cycle O_0 to O_1 to I_1 to O_0 has exact propagation product

683875575 / 3191327216,

which is positive and unequal to 1. Thus this is a magnitude-unbalanced example, not a quartic obstruction.

The independent full remaining-coefficient system, constructed by evaluating differences of normal derivatives at 1/3 and 2/3 along every interior edge, has shape 78 by 129 and rank 78. Adjoining every prescribed-jet column preserves rank 78. Its edge traces and endpoint normal derivatives are also checked, and each two-equation pair is compared with the complete Bernstein residual system through an invertible exact change of equations.

This establishes arbitrary quartic Hermite interpolation on this mesh. Its purpose is to rule out universal proofs that use only the signs of the propagation ratios.

## 3. Excluding a threefold alternating-radius family

### 3.1 Family and necessary geometric inequalities

Use the same 28 faces and exterior-line construction as above. Let rho(x,y)=(-y,x-y), an affine-plane linear map of order 3. Set

O_0=(1,0), O_1=(r,r), O_2=(0,1),
O_3=(-r,0), O_4=(-1,-1), O_5=(0,-r),

I_0=(e,0), I_1=(b,b), I_2=(0,e),
I_3=(-b,0), I_4=(-e,-e), I_5=(0,-b).

The three parameters r,e,b permit independent alternating radii in both hexagons. The old homothetic family is the subfamily r=1 and e=b in (0,1), after an affine normalization.

We claim exclusion only for parameters giving an admissible convex core and conforming full disk. The following are necessary, and suffice for the contradiction:

r>1/2,  0<e<1,  0<b<r.

Indeed strict convexity at O_1 gives the positive determinant 2 r-1. The annulus triangle areas include r-b, r(1-e), b(1-e), and e(r-b). Positivity yields the remaining inequalities in the stated order.

### 3.2 Normalized edge balance and symmetry

For a core edge vw with opposite triangle vertices x,y, one may choose nonzero row normalizations using the checkerboard coloring of the core triangles. The core is face-checkerboard-colorable because every induced interior vertex has even degree. The normalized dependency weights k_v then obey

k_v det(x-y,v-y) + k_w det(x-y,w-y) = 0.

This is the signed transverse-diagonal intersection condition. In particular its ratio along an edge is exactly the usual cycle propagation ratio after a consistent vertex normalization. It is also the Ceva formulation of triangle balance.

Suppose the whole connected closed support were balanced. Its dependency weights are unique up to a common nonzero factor. The order-three rotation rho preserves the edge equations, so acts on that one-dimensional real solution space by a real scalar lambda with lambda^3=1. Thus lambda=1. Consequently the weights are constant on each of the four rotation orbits. Normalize them as

k_(O_even)=1, k_(O_odd)=s,
k_(I_even)=t, k_(I_odd)=u,

where s,t,u are nonzero. The checkerboard normalization can be chosen rotation-equivariantly: an odd-order rotation cannot interchange its two colors.

### 3.3 Three-equation contradiction

For the edges (O_1,I_1), (I_0,I_1), and (O_1,I_2), respectively, the exact normalized balance equations are

F_1 = u[b(e+1)-e] + s[e(r-1)+r] = 0,

F_2 = u[b(e+1)-e] + e(e-1)t = 0,

F_3 = b(1-e)t + (b-r)s = 0.

The opposite vertex pairs are (O_0,I_2), (O_0,I_2), and (O_2,I_1), so these equations follow by direct 2-by 2 determinants from the displayed coordinates. They can be independently reconstructed and compared as polynomial identities; the independent audit checks each of them.

Their short polynomial identity is

b F_1 - b F_2 - e F_3
  = s [r(eb+b+e)-2 eb].

Since s,e,b,r are nonzero, balance would require

2/r = 1 + 1/e + 1/b.

But e<1 and b<r make the right side strictly greater than 2+1/r. Therefore 1/r>2, or r<1/2, contradicting the necessary convexity condition r>1/2.

Thus the full twelve-row support of no admissible member of this three-parameter family can be closed and balanced. There is also no smaller closed component that could evade this argument: the only possible degree-four interior mesh vertices are I_1,I_3,I_5, and every closed component must contain at least three nonsingular degree-four interior vertices by the accepted convex-support theorem. It must therefore contain all three. Each such vertex has its full four-neighbor star in the component; a nonsingular four-star with zero coefficients would have only a local line segment, which the convex-support theorem excludes. Their neighbor sets together contain all twelve O and I vertices. If any of the three is singular, the same at-least-three theorem already rules out all closed components. Hence every admissible member of the displayed family has full row rank and admits arbitrary quartic vertex jets. The proof does not rely on a numerical rank threshold or on a few sampled parameter values.

## 4. Remaining mathematical question

All conclusions about the rational example follow from the displayed exact input and finite rational certificate. No general nonexistence conclusion or arbitrary-perturbation claim follows from this example or from the excluded symmetric family.

The remaining question is whether some admissible mesh has a genuinely cycle-balanced closed component. The [accepted theory](SECOND_PASS_THEORY.md) strengthens the local-jet part of the target: every nonsingular degree-four row has a nonzero gradient form, so the at-least-three degree-four vertices guaranteed inside a closed component would supply incompatible pure gradient data if exact balance were achieved. That conceptual result has its own [proof](SECOND_PASS_THEORY.md) and [audit](THEORY_AUDIT.md); it is not needed for any exclusion or positive interpolation certificate in this report.

The durable new restrictions are therefore geometric exterior feasibility, a demonstrated limit of sign-only reasoning, and an exact larger-family exclusion. They do not settle the general quartic assertion or determine its status throughout the literature.
