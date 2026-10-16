# Independent full review:5100021 / k403,b

**Verdict: PASS_COMPLETE_SOURCE_TARGET. No mandatory mathematical or source correction.**

The verdict binds the unchanged PROOF.md SHA256 `f7aada9e28e92c6fab920f1330366acd6eaba8006b4cd0ce52e2dbd58e7ef5b9` and FROZEN_MANIFEST.json SHA256 `3bc00c10fb0af01b733c05edb896f7e74e617796a79b6ec4486929e64c361596`. All15 manifest-bound author files and three complete source PDFs match. This is a separate AI mathematical audit, not human peer review, priority certification or proposer acceptance.

I did not contribute to this candidate or the parallel k404 derivation. Related earlier billiard work and prior reading of a shared compact-torus method are disclosed in SOURCE_AUDIT.md. The antipedal formula and complete product proof were independently reconstructed rather than accepted from that shared background.

## 1. Exact source and scope

Both actual Table5 pages were visually inspected. The target is the signed area of the pedal of the **original orbit**, times the signed area of its **original antipedal**, for a fixed original focus and primitive N divisible by4. The origin/odd row is k403,a. The candidate has not substituted that row, an outer-polygon construction, or a ratio. The source's surrounding strict confocal-ellipse model is retained, including primitive star winding classes. Signed straight-edge areas are used throughout.

The actual antipedal line through P_i is perpendicular to P_i−F. The original pedal foot lies on P_iP_(i+1), equivalently on its caustic tangent line. The distinct vertex phase w and contact phase w+v are consistently retained. Uniform scaling changes this product by the fourth power, and reversing traversal changes the sign of each area, not their product.

## 2. Independent line geometry

Stachel's canonical data have the correct modulus and coprime-period conventions. With caustic axes1,k', the billiard axes are dn(v)/cn(v), k'/cn(v), and the original foci are ±k. The midpoint contact parameter is w+v+iδ.

I derived the antipedal point independently by adding and subtracting the two source line equations. If M is the midpoint of the two orbit endpoints and E their half-difference, the system becomes

- (M−F)·R=|M|²+|E|²−F·M;
- E·R=(2M−F)·E.

Solving this system and reducing the Jacobi quadratic identities gives both coordinates in formula(4). The independent exact checker verifies those solved coordinates, rather than merely substituting the candidate into its own equations. It also derives the pedal foot directly by projection onto the actual endpoint chord and recovers formula(12).

The normal determinant is exactly formula(5). For real parameters every factor is positive: k', sn(v), dn(v), dn(x), cn(v), L and1+k sn(x) have the required strict signs. Hence all real antipedal intersections are finite. The apparent extra focal denominator in an unreduced solve is genuinely removable. A canceled complex degeneracy is only used through meromorphic continuation and is not mistaken for a real undefined vertex.

## 3. Complete antipedal pole audit

The only possible nonremovable coordinate poles in the reduced antipedal formula occur at L=0. On the sn² torus, these are exactly iK'±v. They are distinct and simple: at sn(x)=±1/(k sn(v)), neither cn(x) nor dn(x) vanishes for0<k,sn(v)<1. The degree-two divisor accounts for all roots. At common sn/cn poles the numerator and denominator orders are at most and exactly2 respectively, so these apparent singularities are removable. The fixed coefficients cn²(v) and k' are nonzero.

Therefore each antipedal vertex has at most a simple pole, and every cyclic edge determinant has order at most2. Passing from contact to vertex phase places all possible area poles in the reduced classes iK' and3iK'. There is no omitted focal-factor or common-Jacobi pole.

Central inversion cyclically relabels the even orbit and interchanges foci, proving equality of the focal antipedal areas. Reflection in the y-axis interchanges foci and reverses the parameter order; reflection and reversal each negate signed area, giving B(−w)=B(w). The imaginary shift2iK' fixes sn and negates cn, so it is an x-axis reflection of the complexified construction with the focus fixed and the same cyclic order; thus B(w+2iK')=−B(w). Bilinear dot products are essential here and are used correctly.

These identities make the Laurent germ at iK' odd. Since its order was bounded by2, the quadratic principal part vanishes. The same holds at all translated poles. This is a global cancellation argument and does not assume separated singular-vertex pairs. It covers N=4 even though all four antipedal vertices can be singular simultaneously. My direct complex-line controls include that case.

## 4. Trace uniqueness and permitted zero areas

The N-term dn trace has reduced real period h=2K/m and anti-period2iK'. At a representative pole, its two contributing terms have identical nonzero residues; they do not cancel. On the torus with periods h and4iK', it therefore has precisely two simple poles. The antipedal area has at most that same pole divisor and the same anti-periodic character.

Matching one residue matches the other. The remaining difference is holomorphic on the compact torus and constant; anti-periodicity makes it zero. Hence the focal antipedal area is a real scalar multiple of this trace. That scalar may be zero. The proof never divides by it or by the antipedal area, so a whole zero-area family is allowed without any undefined quotient.

Real-period2K can also be seen directly: shifting w by2K is the half-orbit cyclic relabeling for odd primitive turning number. It is not an assumed2K period of an individual fixed-focus antipedal vertex.

## 5. Pedal pole cancellation and strict positivity

The focal foot formula has possible poles only where sn(x)=1/k. At r=K+iK', the quarter-shift formulas express both sn(r+z) and cn(r+z) as even functions of z. The foot therefore has an even germ of pole order at most2. Its neighbors at r±δ are regular for0<δ<2K. In the two incident signed-area terms, the neighbor difference is odd and holomorphic. Multiplying it by the even double-pole germ gives at most a simple pole. Common-Jacobi expressions at a neighbor in N=4 are removable; they do not create a second adjacent singular factor.

The same reduced-lattice residue argument proves that the pedal area is a scalar multiple of T(w+K+v). The origin and focus are not interchanged in this step. Geometrically, q−F is a positive multiple of the outward caustic normal, since F lies strictly inside the caustic. A positive canonical step shorter than2K advances that normal by an angle strictly between0 andπ. Every edge determinant about F is positive, including stars. Therefore the signed pedal area and its trace coefficient are strictly positive. This is independent of any antipedal sign or zero.

## 6. The actual product parity and low period

For N divisible by4, m is even and τ odd, so K+v is h/2 modulo h. The companion k404 ratio's integer shift cannot be substituted here.

The trace is even. At h/2+iK' it is regular and equals its own negative by evenness followed by a real period and an imaginary anti-period, so it vanishes; the imaginary translate supplies another zero. The two distinct zeros exhaust the degree-two zero divisor and are simple. Thus T(w)T(w+h/2) is holomorphic on the compact torus and constant, positive on the real line. Multiplying the two area traces proves exactly the requested product, including a possible zero antipedal scalar.

I independently checked the N=4 examples at symbolic, variable aspect ratio using actual projections and line intersections. For the axis diamond, the two areas are

- pedal:4a³b³/(a²+b²)²;
- antipedal:4ab.

For the axis-aligned billiard rectangle, they are2a²b²/(a²+b²) and8a²b²/(a²+b²). Both products equal16a⁴b⁴/(a²+b²)², and their chords share the correct confocal caustic. At a=2,b=1 these give the candidate's32/25,8 and8/5,32/5, with common product256/25. This is a direct original-line check, not an outer-polygon relabeling.

## 7. Reproduction and independent checks

Both author checkers were read and replayed separately. Their exact12,029-control receipt and95-digit10,284-diagnostic receipt match byte-for-byte.

The independent exact checker passes6,469 assertions, including the midpoint line solve, actual chord projection, generic N=4 geometry at both foci, complete reduced pole classes, residue multiplicity and complementary zero/pole arithmetic over1,069 primitive rotations.

The separate110-digit diagnostic script passes14,932 checks. Real orbits are generated by physical ray reflection from an independently solved initial caustic tangent, then checked for closure, caustic tangency and agreement with canonical coordinates. Derived polygons use direct projections and line intersections. The controls cover39 physical billiard families, both foci, traversal reversal, scale, both observed antipedal signs, nonreal line geometry, near-pole cancellation, trace zeros and excluded-parity varying products. Their maximum scaled discrepancy is about7.89e−69. These are non-interval diagnostics, not a replacement for the universal written proof.

An initial structural-expression comparison in the reviewer's own symbolic code was normalized algebraically before sealing. It was not an author error. No frozen author bytes were changed.

## 8. Disposition

The complete source target is proved under the explicitly stated primitive, strictly nested confocal-elliptic domain. A first-turn claimed-result disposition is mathematically supported, retaining the shared campaign provenance and the natural signed-product treatment of zero antipedal area. No novelty or external acceptance is certified. The parent retains the publication gate.

Nine portable top-level review files, including this report and the review manifest, are supplied. Exclude reading/ and author_replay/, source PDFs, full texts and images.
