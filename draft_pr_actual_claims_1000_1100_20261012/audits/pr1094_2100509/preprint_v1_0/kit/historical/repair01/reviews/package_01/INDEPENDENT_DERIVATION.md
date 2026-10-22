# Complete mathematical adversary, whole-package pass 01

The object tested is the original smooth compact-support classification, not
global constant Jordan type or a fixed Cartesian matrix. The source asks for
unchanged prescribed algebraic type on some open domain. Fixing numerical
real eigenvalues in a local commuting frame is stronger than that request.
The paper's converse excludes nonreal spectrum at every point. No conclusion
below certifies historical firstness or worldwide preexisting openness.

## Coordinate torsion and the ordered equation

In commuting coordinates the definition gives

    N^k_ij = sum_p L^p_i d_p L^k_j - L^p_j d_p L^k_i
                      - L^k_p d_i L^p_j + L^k_p d_j L^p_i.

For L = [[A,b],[0,lambda]] depending only on the last coordinate, the only
nonzero lower-row entry is L^n_n=lambda. Thus for angular i and last index n,
the first two derivative terms give -lambda A'_ki; the last term gives
(A A')_ki. All other components vanish, including the transverse component.
The b' and lambda' terms cancel rather than being assumed zero. The result
is (A-lambda I)A', in that order. This is not a commutativity assumption.

The independent exact first-jet controls use this full formula, not the
paper's reduced equation. They include arbitrary b/lambda derivatives and
conjugation by rational nontriangular coordinate transformations. The latter
transforms the derivative covector too: with y=Qx, d_a L_new is
(Q L' Q^-1)(Q^-1)_{n a}. This directly checks covariance of the valid stages.

## Every real Jordan pattern reaches zero

Take the last vector of one upper-superdiagonal block as transverse. Its
preceding angular hyperplane is invariant; the terminal arrow remains in b,
so the starting full matrix has precisely the original Jordan data. Removing
b with A fixed is legal. Align lambda with an active angular block mu I+K
while A stays fixed. The active equation becomes KK'=0, with the (j,j+2)
entry a_j a'_{j+1}. Delete a_1 first, then a_2, etc.; each predecessor is
already zero when needed. Earlier processed blocks and later unprocessed
blocks have zero derivative, so differing eigenvalues elsewhere cause no
cross term. Once the active block is scalar, move it to zero with lambda
equal to that same scalar function. Repeat finitely many times.

Singletons, zero eigenvalues, equal eigenvalues in separate blocks and
arbitrary choices of the distinguished block do not change the argument.
There are no spectral denominators and no hidden regularity assumption.
The last scalar stage leaves lambda zero as well. Dimension one is handled
separately by an ordinary scalar plateau bump; its alternating torsion is
automatically zero.

Choose a step whose raw parameter has small open plateaus beyond both ends
of [0,1]. Composing each finite stage with this step makes all derivatives
match at concatenations. A smooth reparametrization multiplies A' by one
scalar, preserving the equation. The stated even q(t)=S(2(t^2-1/16)) is zero
for |t|<=1/4 and one for |t|>=3/4: the latter endpoint follows from
2((3/4)^2-1/16)=1. Hence the two end bands are exactly zero. No nonsmooth
absolute value or arbitrary cutoff of a matrix was used.

Invalid alternatives matter. Cutting the second arrow before the first
gives a nonzero E13 term. A scalar cutoff of J4 has nonzero torsion ff'E13
in its angular block; J3 is a genuine valid boundary case and must not be
declared invalid. An unmatched scalar drift fails. Reversing product order
also falsely rejects a legal first-arrow deletion. The exact new controls
detect all these distinctions and the source polynomial-count example.

## Global geometry and support

The induction really embeds T^d in R^(d+1), rather than using the usual
product of planar circles in dimension 2d. Embed T^(d-1) in R^d with unit
normal nu; in R^(d+1) its normal disk bundle has the frame (nu,0),(0,1).
A sufficiently small disk bundle is embedded by the tubular-neighborhood
theorem. Its boundary is T^(d-1) x S1. Tubular coordinates recover the base
point and both circle components, proving injection and immersion. The
displayed normal (cos(phi)nu,sin(phi)) has unit length and is orthogonal to
the base derivatives (nu.df=nu.dnu=0) and the circle derivative. This proves
two-sidedness needed at the next induction. Compactness supplies one global
small tube radius; the finitely many rational curvature models are only
indexing controls for this geometric proof.

The final collar is open in the same R^n. Its product angular frame pushes
forward to commuting fields by naturality of Lie brackets. A compact subset
of the collar contains all nonzero values, because both end bands vanish.
That compact image lies strictly inside the open collar; exterior and collar
boundary points have zero neighborhoods. Extension by zero is globally
smooth with zero torsion by locality. A connected coordinate box in the
central band is the required open realization domain. No global exterior
frame or global angular functions are needed.

## Prior local ingredients and the exact nonreal obstruction

The local splitting theorem of BKM author-v2 3.1 applies at singular points
to separated characteristic factors, and gives independence of complementary
coordinates. The no-real-spectrum block of their Theorem 3.3 carries a
canonical complex structure under which its tensor coefficients, hence its
complex characteristic coefficients, are holomorphic. Neither statement
requires global gl-regularity or analyticity of the starting real tensor.

On a closed connected manifold, let mu be the largest positive imaginary
part, or zero when the spectrum is all real. Continuous dependence of roots
on coefficients makes mu continuous. If its maximum mu0 is positive, choose
the largest algebraic multiplicity m of any root on Im z=mu0. This maximum
exists because the possible integers are bounded by the dimension and at
least one such root exists. The locus E carrying such a root of multiplicity
m is closed: choose a converging subsequence of bounded roots and use
vanishing derivatives of the characteristic polynomial; a higher limit
multiplicity is excluded by the defining maximum.

At a point of E, separate that root and its conjugate from all other roots.
The complex factor P has degree m and is holomorphic in the block variables,
independent of the others. Its trace has imaginary part at most m mu0 and
attains that maximum. The holomorphic maximum principle forces its trace to
be constant locally. Every root then has imaginary part mu0, since each is
bounded above by mu0 and their sum attains the upper bound. The coefficients
of P(w+i mu0) are both real valued and holomorphic, hence locally constant.
At the selected point all roots equal lambda0, so that same polynomial
persists. E is open as well as closed. E therefore equals the connected
manifold and contradicts any zero point. This weaker argument suffices.

Compact support on R^n gives a smooth zero extension on S^n, with a zero
neighborhood of infinity. The preceding prior splitting/holomorphic
mechanism therefore excludes nonreal spectrum. The claim does not depend on
the final polynomial-induction sentence of the source's stronger persistence
proof. Indeed z -> z^2+1 maps both pairs +/-i and +/-i/2 to real numbers;
that sentence's literal count can fail without refuting the theorem. The
paper accurately qualifies that source proof and does not identify the
unread publisher PDF with author-v2 bytes.

## Boundaries of priority inferences

BKM 4.5/p28 realizes arbitrary types at points by independent characteristic
coefficient coordinates. Its generic semisimplicity and repeated-root
equations do not yield a fixed nonsemisimple type on an open domain, nor a
compact zero transition. The published Geometry III 1.10 is an analytic
regular-layer realization near a nonzero cyclic Jordan block (author-v1
1.4); it is not a zero-end compact-support theorem. Geometry IV output
symmetries really may be singular or zero. For n=3 and f3=0, its formula
f1(U)N^2+f2(U)N has second superdiagonal u2 f2'(u3)+f1(u3). This is not
periodic in u2 for a nonconstant transverse f2, so naive replacement of that
coordinate by an angle does not immediately globalize it. This excludes
only that immediate proposed implication, not all uses of the framework.

Direct sums of compact examples retain unbounded cylinders in Euclidean
product factors. Fixed functional calculus preserves diagonalizability and
cannot create nontrivial Jordan blocks from semisimple examples. Constant
type/parallel theorems have a separate globalization gap at zero. These are
checkable limitations of those immediate corollary routes; they are not a
proof that no historical antecedent exists. The paper and metadata keep full
result and mechanism priority UNKNOWN and give substantive prior credit.
