# Independent adversarial review: 5100014 / k303,a

**Verdict: PASS_COMPLETE_SOURCE_TARGET for candidate v2. No mandatory correction.**

Exact reviewed CANDIDATE.md SHA256:
`e48aa989fb9282d09fdf58e7e4f6eee78e757ff0686f4cc35dc691e21f3d1fd3`.
Author FROZEN_MANIFEST.json SHA256:
`44caa83299a1951fa4a30605795ba349ec287f4112a3e8c98d310550b0a13962`.
All fourteen current manifest entries match their hashes and sizes.
The only proof-file difference from the initial freeze is the author's
removal of an extraneous circular-boundary extension sentence; I verified
that substituting back that single sentence reproduces the old proof hash.
The source theorem has a>b throughout. This audit is independent of the
author's derivation and contains no shared-author proof contribution.

## 1. Exact target and inputs

The pinned 5100014 statement and complete source Table4 were inspected.
Both arXiv v11 p6 and the published p346 retain **k303,a = A' A'_M**,
N=2 modulo4, all fixed M. The relevant pedal vertices are feet to the
outer tangent polygon's side lines, namely the tangents to E at P_i.
They are not feet to original billiard chords, caustic contacts, or
antipedal intersections. Signed traversal-area conventions are preserved.
The imported centroid notation is context, not an extra conclusion.

The complete Chavez-Caliz paper was read at its signed-area definition,
complex general-position definition, flag-curve construction (p98), and
Theorem6/proof (p104). The latter two pages were visually checked.
The candidate verifies the four transverse complex intersections rather
than treating real strict nesting as a substitute for general position.
The published AA' theorem is correctly credited and used only after the
new outer-pedal proportionality is established.

Primary sources:
- https://arxiv.org/pdf/2004.12497v11
- https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf
- https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf

## 2. Flag curve, central inversion, and quotient

For the transverse pair, the degree-two projection of flags to E has four
simple branch points E∩C and gives a smooth connected genus-one curve X.
The involution conventions and T=tau sigma agree with the primary source.
T has exact order N, and all nonidentity powers acting as translations
are fixed-point-free.

The proof of I=T^(N/2) is valid. On either real orientation component,
strict nesting gives a circle of flags. Central inversion preserves that
component: it preserves the choice of which side of the oriented tangent
contains C. Both I and T preserve its orientation, commute, and generate
a finite group. An averaged circle metric makes the action isometric;
orientation-preserving circle isometries are rotations and have a unique
nonidentity involution. I and T^(N/2) are therefore identical there.
Neither can become the identity on that circle without becoming the
identity globally by analytic continuation. Equality then extends to X.
This reasoning includes primitive star rotation numbers, not only tau=1.

The free quotient Y=X/<T> is unramified and genus one. Cyclic area functions
really descend to Y. The reversal tau normalizes <T>, so it also acts on Y.
Because it reverses the order of the same projected points, it negates
both A and B_M while leaving the *fixed point M* unchanged. No spatial
reflection of M or mistaken complex conjugation is invoked.

## 3. Original area poles and the two-dimensional function space

Each of E's two points at infinity has two unramified flags above it.
The affine coordinates have simple poles there because the line at
infinity intersects E transversely. Central inversion fixes each base
infinite point but exchanges its flags, since I is a nontrivial translation.
Thus their images on Y form a set S of at most two points.

The proof correctly excludes adjacent infinite vertices. Distinct infinite
points would require the line at infinity to be tangent to C. Equal ones
would require the tangent to E there also to touch C, ruled out by the
nonzero displayed dual quadratic value. Every area determinant therefore
has at most one singular factor. This proves *at most* simple poles; it
does not require guessing residues or asserting poles survive cancellation.

Nonconstancy is established independently. A real orbit oriented with C on
the left has every det(P_i,P_(i+1))>0, since O lies strictly on that side of
each chord. This remains true for star traversals. Thus A>0 on that real
component, whereas the reversal identity would force a globally constant
A to be zero. A genus-one curve has no nonconstant function with at most
one simple pole. Consequently the two members of S are distinct and
A,1 span L(D), D=sum S.

The invoked genus-one Riemann–Roch specialization is valid: deg D=2,
g=1, and deg(K−D)<0 give l(D)=2. The standard Riemann–Roch/duality
statement was checked at https://stacks.math.columbia.edu/tag/0BS6.

## 4. Exhaustive pedal-pole audit

The projection formula Q=M+(1−R·M)R/(R·R), R=BP, is the exact orthogonal
projection onto the tangent at P for real data. Complexification uses the
bilinear dot product, so it is a meromorphic rational formula. At infinity
its denominator has order two and nonzero leading coefficient
1/a²−1/b². Its numerator has at most the same order; the singularity is
removable for every M.

The only remaining candidates are the four simple zeros of d=R·R,
with x²=a⁴/c², y²=−b⁴/c². Both coordinates are nonzero. I checked the
formulas showing these lie on E, have isotropic normal, and their lines
are exactly the common tangents to E and C. Conversely the two normalized
dual tangent equations imply d=0. The computed C equation residual is
−lambda²/(alpha²beta²), so none is a branch point of pi. Each individual
foot has at most a simple pole on X, with possible residue zero for special
M. There are no additional finite or infinite poles omitted here.

For a common-tangent flag z, sigma z=z and Tz=tau z. When N=2m with m odd,
2k≡1−m modulo2m has a solution and yields tau(T^k z)=I(T^k z).
Since pi is tau-invariant, the projected point is fixed by central
inversion. The only such points on projective E are its two infinite
points (the other projective fixed point O is not on E). Thus all pedal
pole flags lie over S. The parity restriction is genuinely used; the
congruence has no solution when m is even.

## 5. Multiplicity cancellation and arbitrary M

Along the orbit of sigma-fixed z, another T^j z is sigma-fixed precisely
when N divides2j, hence j=0 or m. Each common-tangent base point has only
two flags, the sigma-fixed one and its tau=T image. Therefore the complete
list of singular feet is exactly the *possible* indices 0,1,m,m+1.
Calling them possible also covers special M where residues vanish.

With m≥3, the only adjacent pairs in that list are (0,1) and (m,m+1).
The paired vertices coalesce respectively to P and −P. Both leading
residue vectors within each pair are scalar multiples of the same finite
normal R(P), so their determinant is zero. The apparent order-two pole
cancels even for an arbitrary fixed M. All other determinant terms contain
at most one simple-pole factor. No pole of order two or greater survives.
Unramified passage to Y preserves these local orders, giving B_M∈L(D).

Consequently B_M=c_M A+d_M. Applying reversal with the same M forces
d_M=0; this is not an assumed zero-mean condition or an unchecked character.
The credited AA' theorem then gives A'B_M=c_M(AA'), proving the full target.
No division by B_M is used, and its zero or negative signed values cause
no exception. Real tangent intersections and all real projection feet are
finite under the stated strict caustic hypotheses. N=2 is impossible:
a two-bounce chord is a diameter and cannot touch the strictly interior
nondegenerate elliptical caustic.

## 6. Controls, corrections, and limits

The two author-written exact SymPy programs were inspected and replayed.
The axis-orbit output matches the frozen output bytes; both symbolic
arbitrary-M products simplify to40(u²+v²+9)/9. The separate generic
six-period phase closes exactly and reproduces A'B_0=40 and B_0/A=9/8.
These programs do not claim to prove general period.

My separate checker passes **1,757 exact assertions**, including universal
common-tangency/unramified/transversality identities, symbolic cancellation
of the second-order residue, all relevant dihedral congruences and complete
singular-index lists through N=1002, and opposite-parity negative controls.
It also passes **26,568 numerical diagnostics at80 digits**, using direct
outer tangent intersections and direct foot projections for primitive
N=6,10,14,18,22, all admissible tested star turns, multiple phases and M.
The maximum scaled residual is about2.03e-79. These are numerical diagnostics,
not interval certificates; the general result rests on the audited proof.

No core mathematical gap or mandatory correction remains in v2. The
scope-only circular aside was removed by the author before final verdict;
I did not supply a replacement derivation. Preserve the strict a>b,
primitive-period, elliptical-caustic, signed-area, arbitrary-fixed-M scope
and all source credits. A bounded literature check and this AI audit do
not establish historical novelty or human peer review.
