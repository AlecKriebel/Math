# Scope, conventions and independent arithmetic audit

## 1. Problem separation

The target is Problem 2 in Karpenkov (2017), §1.3, p. 3, not the entire section. The section title contains two subjects, but Problem 1 is the cosine-rule question and Problem 2 is the planar IKEA realization problem. The retained research record contains literature triage, not a proof attempt. Its unverified open-status assessment is superseded here by the published 2025 article.

The classification used here concerns bounded, full-dimensional convex polygons in R^2, with integer vertices and no redundant collinear vertices. Thus every interior angle lies strictly between 0 and pi. The 2017 sentence alone does not spell out convexity; this scope is fixed by the primary authors' subsequent formulation and theorem. Do not silently promote the result to a general nonconvex problem.

## 2. Equivalence and orientation conventions

Integer congruence uses affine maps x -> Mx+t with M in GL(2,Z) and t in Z^2. It is not Euclidean congruence. Absolute determinant and lattice length are invariants under all such maps. Signed determinant is multiplied by det(M); it is invariant only under orientation-preserving maps. The source's blanket signed-area invariance wording must be read with that correction.

For v=(a,b), its lattice length is gcd(|a|,|b|). For primitive, ordered, noncollinear rays u,v, the lattice sine is |det(u,v)|. The finite LLS block alternates sail-edge lattice lengths and sail-vertex lattice sines, beginning and ending with a length. It therefore has positive entries and odd length. This is the regular continued-fraction convention, not the negative Hirzebruch–Jung convention.

The checker uses clockwise polygon vertices and takes the ordered rays at a vertex to be (previous vertex minus current vertex, next vertex minus current vertex), so their determinant is positive. This is a coordinate convention; reflecting the entire polygon is allowed. The ordered blocks must not be independently reversed or arbitrarily permuted. A cyclic change of starting vertex moves the associated curvature entries with the angles. If one chooses an unoriented-angle convention instead, ray interchange must be explicitly translated into block reversal rather than silently identifying the two ordered inputs.

## 3. Normalization derived from primitive vectors

Let u=(u_x,u_y) and v be primitive with D=det(u,v)>0. Bezout gives r u_x+s u_y=1. The matrix with rows (r,s) and (-u_y,u_x) has determinant 1 and sends u to (1,0), v to (x,D). An integral shear fixes (1,0) and changes x by multiples of D. For D>1 choose 1<=x<D; primitivity implies gcd(x,D)=1. For D=1 choose x=1. The normalized lattice tangent is D/x>=1.

The Euclidean algorithm gives a positive regular continued fraction. If its length is even, replacing the last entry a by a-1,1 gives the odd-length expansion. The terminal a in this case is at least 2, so positivity is preserved. This is the block recovered by the checker. The calculation is exact integer arithmetic; floating-point slopes are not used.

## 4. Chord-curvature formula derived in edge coordinates

For four successive vertices A,B,C,D of a clockwise strict convex polygon, let e be the primitive vector along BC and let L be the lattice length of BC. Choose an integral coordinate system sending B to (0,0), C to (L,0), and the polygon interior into y>0. Write A=(a_x,a_y) and D-C=(d_x,d_y). Here a_y,d_y>0.

On the interior line y=1, the nearest integer points to the two adjacent side lines have abscissae

b'=ceil(a_x/a_y),    c'=L+floor(d_x/d_y).

The signed lattice displacement from the first to the second is c'-b'. Therefore the source's chord-curvature definition yields

c = L-(c'-b')-2 = ceil(a_x/a_y)-floor(d_x/d_y)-2.

Changing the Bezout coordinate by an integral shear adds the same integer to both quotients, leaving c unchanged. The side length L cancels. Consequently parallel dilation preserves the angle-curvature data, although it generally changes the affine-congruence class and area of the polygon. This explains why no uniqueness of the actual polygon is claimed here.

## 5. Why the closing denominator cannot vanish

For a word W=(w_1,...,w_m), multiply the matrices [[w_i,1],[1,0]] in the written order. The upper-left entry is K(W); for nonempty W, the lower-left entry is K(W with its first entry deleted). The product has determinant (-1)^m. These two entries are therefore relatively prime.

Put X=A_1 and U=(X,c_1,V). The concatenation identity gives

K(U) = (c_1 K(X)+K(X with its last entry deleted)) K(V)
       + K(X) K(V with its first entry deleted).

Since X is positive, K(X)>0. If K(V)=0, the coprimality just proved forces K(V with its first entry deleted) to be +1 or -1. Then K(U) cannot vanish. Thus K(U)=0 implies K(V) is nonzero, and the final floor quotient is well-defined. This justifies projecting the published angle-curvature criterion onto angle data by existentially quantifying the intermediate curvatures.

The recurrence retains the signs of continuants. Replacing them by normalized rational numerators with a positive denominator can flip signs and break the winding condition. Integer division in the implementation is floor division, including negative inputs, and zero entries are removed before sign changes are counted.

## 6. Verification limits and source cautions

The mathematical resolution is credited to Dolan–Karpenkov Theorem 3.3 and its proof. The packet does not re-prove that theorem in a formal system. Source inspection includes the sail-coordinate construction, the winding test, and the rational-polygon scaling step. The auxiliary Theorem 3.8 is unnecessary for the acceptance decision; its wording about uniqueness is not used to claim uniqueness of a polygon, in view of the source's Remark 5.1 and the dilation calculation above.

The checker is a finite witness audit. It rejects malformed input and supplies a conservative Boolean evaluation of the displayed criterion for given bounded-size data. Its input limits are implementation limits, not mathematical restrictions on Theorem 3.3. It does not search all integer curvature tuples or classify a tuple negatively just because a bounded search failed.

Random controls use a fixed seed and exact convex hulls. The 203 polygons and 19,531 signed words do not prove any universal statement by themselves. No claim is made that source-file hash equality establishes mathematical truth.

## References

- O. Karpenkov, [Open problems in geometry of continued fractions](https://arxiv.org/abs/1712.01450), 2017, §1.3, Problem 2.
- J. Dolan and O. Karpenkov, [Lattice angles of lattice polygons](https://doi.org/10.5802/jtnb.1345), JTNB 37(3), 2025, 873–896. Definitions §§2.2–2.6; Theorem 3.3; §5.1; Remark 5.1; §6.
