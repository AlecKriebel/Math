# Source-only target and frozen route

Frozen UTC: 2026-10-04T23:02:33.471995+00:00. No candidate, author programs/results or inherited-review access has occurred.

## Primary target

- arXiv version 11 (29 Oct 2020), PDF printed p. 9, Table 7, k606: Abar_1/Abar_2 = Abar'_1/Abar'_2, marked all N, with value and proof unknown.
- Published Arnold Mathematical Journal 7 (2021), pp. 341-355, printed p. 349 (PDF page 9), Table 7, k607: A_1/A_2 = A'_1/A'_2, also marked all N, unknown value/proof.
- These are corresponding entries despite renumbering. The v11 k607 entry is a different antipedal statement and must not be substituted for the assigned target.

Define E: x²/a²+y²/b²=1, a>b>0, foci F±=(±sqrt(a²-b²),0). An elliptic billiard is a closed polygon inscribed in E whose chords are tangent to a strictly nested confocal ellipse, with reflection at the vertices. The outer polygon has sides equal to the tangent lines of E at the ordered billiard vertices (source Figure 1). A_± is the signed shoelace area of perpendicular feet from F± onto ordered billiard chord lines. A'_± is the same construction for the outer tangent polygon, namely feet on the ordered tangent lines. The ordering is cyclic and all polygon areas are signed by source equation (1); self-intersections are therefore relevant. The primed target areas are not antipedal/contrapedal areas.

The source does not state winding restrictions beyond N-periodic billiards and the strictly elliptic pair. Whether primitive stars are included must be checked geometrically. Repeating a smaller periodic traversal does not create a new primitive orbit; it multiplies each signed shoelace area by the repetition number. Reversing traversal negates every signed area. Quotients require A_2 and A'_2 nonzero, so a cross-product identity is weaker when either denominator vanishes.

## Independent direct route and falsifiable checks

For each line n·X=h and each focus F, compute Q=F+((h-n·F)/(n·n))n directly; compare with Cartesian chord projection Q=P+((F-P)·(R-P)/|R-P|²)(R-P). For tangent lines at P∈E, use n=(P_x/a²,P_y/b²), h=1. Compute outer intersections independently by a 2×2 solve and check that their sides have precisely these tangents. Antipedal intersections, if audited as a control, instead solve (P-F)·X=(P-F)·P and are geometrically different.

For a line tangent to a confocal ellipse with axes α,β, unit normal n=(cosφ,sinφ), support h=sqrt(α²cos²φ+β²sin²φ), the feet from the foci lie on the centered circle of radius α: |Q|²=c²+h²-c²cos²φ=α². This elementary deduction supplies a circle-locus check and does not prove the area-ratio claim.

Generate independent closed orbits using direct reflection from the normal at P, then solve the caustic parameter for the desired closure/winding. Validate ellipse membership, unit-velocity reflection, every caustic tangency, closure, primitivity and signed-area denominators separately. A symmetric exact 3-periodic triangle is a critical source-correction control; rational squared axes can make its algebra exact. Test focal labels simultaneously on both sides of the target; label swaps cannot correct a reciprocal mismatch.

Numerical route: sample independent phases, axes, primitive convex/star winding and N; finite high precision without interval bounds is falsification evidence only. Exact geometry is needed to settle target falsity or a universal correction. Excluded limiting cases include coincident-circle foci, caustic degeneration, vanishing chords and parallel consecutive outer tangents.

## Primary-source provenance

PDFs were acquired directly from https://arxiv.org/pdf/2004.12497v11 and https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf. Their target-table pages were rendered and visually inspected. SHA-256 values: arxiv c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da; published c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42.
