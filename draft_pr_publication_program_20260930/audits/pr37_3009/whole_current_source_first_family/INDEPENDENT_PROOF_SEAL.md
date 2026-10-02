# Independent reconstruction seal

Sealed 2026-10-02 UTC before reading the candidate proof or any audit verdict. The mechanism below was reconstructed from the literal question, with theorem statements checked against independent live primary sources. It is a verification reconstruction of known lower-dimensional consequences, not an additional attempt to solve the unfinished higher-dimensional problem.

## Imported inputs and their coverage

I independently fetched and read the complete arXiv v3 text of Kolev–Pérouème, Recurrent Surface Homeomorphisms, math/0303258v3, corresponding to the 1998 publication. Its main result says that a nonidentity recurrent orientation-preserving homeomorphism of S^2 has two fixed points. Its definition of recurrence is uniform convergence to identity along positive exponents tending to infinity. Its introductory disk consequence is already explicit, so there is no discovery credit for that consequence. I read its prime-end/Birkhoff proof through the final contradiction and the remaining corollaries; this is imported proof coverage, not a self-contained reproof of prime-end theory, Brown–Kister, or Brouwer.

The Brown 1977 AMS PDF was attempted independently and returned HTTP403; the web open also failed. I instead directly inspected Hamilton's 1954 primary three-page paper, DOI10.4153/CJM-1954-056-8, whose Theorem A has exactly the needed conclusion: an orientation-preserving plane homeomorphism preserving a bounded nonseparating continuum has a fixed point in that continuum. Its proof reduces to a fixed-point-free plane homeomorphism agreeing on the continuum, contradicting compactness through Brouwer translation theory. Brown's exact proof is not claimed read. The theorem is a credited import; this audit does not silently claim proof coverage for every foundational citation.

## Line

Uniform orbit diameter implies |h(x)-x|<=D. A decreasing line homeomorphism sends x->+infinity to h(x)->-infinity, contradicting that bound. Hence h is increasing. If h(x)>x at some x, all positive iterates after the first are >=h(x)>x; convergence of h^{n_k}(x) to x is impossible. Apply the symmetric inequality if h(x)<x. Therefore h is identity. Without uniform orbit smallness, reflection is a nonidentity recurrent line example with separately bounded orbits, showing the exact quantifier matters.

## Plane: orientation and recurrence at infinity

The straight-line homotopy H_t(x)=x+t(h(x)-x) stays within D of x. It is uniformly proper in (x,t), since |H_t(x)|>=|x|-D. It extends continuously over the one-point compactification, fixes infinity, and joins identity to the extension of h. Its degree is therefore +1. A plane homeomorphism has orientation sign equal to this degree, so h preserves orientation. This does not require H_t to consist of homeomorphisms.

For every integer m and every x, |h^m(x)-x|<=D. In the standard chordal metric after stereographic identification, distances to infinity are (1+|x|^2)^(-1/2) up to the conventional constant. For |x|>R>D, both x and h^m(x) have norm at least R-D. Triangle inequality gives a uniform-in-m tail estimate <=2/sqrt(1+(R-D)^2). On |x|<=R, compact-open recurrence makes the spherical displacement tend uniformly to zero. For any tolerance, first choose R for the tail, then k for the compact ball. Thus the compactified extension F is recurrent uniformly on S^2. No Euclidean-uniform recurrence of h follows from this argument.

## Plane: many fixed points

Choose any x. The segment A joining x to h(x) lies in the closed Euclidean ball B(x,D). For every a in A, every m in Z, |h^m(a)-a|<=D, so h^m(A) is contained in B(x,2D). Consecutive arcs meet at h^{m+1}(x); their bi-infinite union is connected, and its closure K is a nonempty compact connected invariant set contained in B(x,2D). Let U be the unbounded component of R^2 minus K and set L=R^2 minus U. Every bounded complementary component has boundary in K; attaching them preserves connectedness. The outside of B(x,2D) is a connected unbounded set disjoint from K, so L is also inside that ball. Its complement U is connected, hence L is a nonseparating continuum. Properness and invariance of K force h to permute complementary components and preserve the unique unbounded one, so h(L)=L.

The imported Cartwright–Littlewood theorem gives a fixed point p_x in L, hence |p_x-x|<=2D. Picking widely separated x gives two distinct finite fixed points (indeed unboundedly many), in addition to infinity. The compactified F is recurrent, orientation preserving, and has more than two fixed points. Kolev–Pérouème therefore forces F=identity, and h=identity. Degenerate D=0 is immediate. No fill-versus-convex-hull invariance is assumed: only the containing ball localizes the filled continuum.

## Closed disk

A disk homeomorphism fixing the boundary extends by identity outside the disk to a plane homeomorphism; continuity, bijectivity, and the same extension for the inverse prove it is a homeomorphism. Its iterates move points only in the closed disk, so there is a common finite orbit bound. Compactness of the disk turns the prescribed compact-open recurrence into uniform convergence there, and the identity extension inherits compact-open recurrence on the plane. The planar result applies. Alternatively its sphere extension fixes every outside point, so the imported theorem gives the same conclusion once orientation is verified. The explicit 1998 disk statement already covers this result.

## Gap and falsifiable checks

This reconstruction proves only n=1 and n=2 (and boundary-fixed line interval/disk), conditional on named established topology theorems. Nothing here supplies the n>=3 theorem, the full local/manifold formulation, or the higher-dimensional C-infinity variant. Falsifiers to seek in the package are: swapped per-orbit/uniform quantifiers; compact-open replaced by Euclidean-uniform recurrence; circular use of compact cyclic closure; degree of the interpolation mistaken for an isotopy; disconnected raw orbit closure passed to Cartwright–Littlewood; filled hull localized without a containing ball; insufficient fixed-point count; or imported-theorem novelty/proof coverage inflated.
