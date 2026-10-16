# Frozen independent claim, assumptions and source-risk map

Frozen UTC: 2026-10-15T11:57:03Z.
Audit head: 2180d64b648b81ac660a792f7823d0b715f9cf12. Original immutable submission: `../submitted/unsolved_math_prioritization/attempts/5100033`.

This map was authored after reading only INTAKE.json and the original PROOF.md, SOURCES.md, source_manifest.json. No original verification program, verification output, inherited independent review, readiness report or downstream audit has been read. Source assertions below are hypotheses until primary-source verification.

## Exact target hypothesis
For a noncircular real ellipse a>b>0, strictly nested confocal nondegenerate elliptical caustic, and any odd least billiard period N>=3, including every coprime star turning number tau with 0<tau<N/2, form the outer polygon by intersecting consecutive tangents at orbit vertices. Let B+ and B- be signed cross-product areas of the orthogonal projections of the two foci onto the consecutive outer side lines. The proposed theorem is that B+B- is independent of phase within the fixed Poncelet family. Claimed source identification: arXiv 2004.12497v11 Table 7 k605,a equals published Table 7 k606, and published k605 is different.

## Mechanism and assumptions to audit
1. Source domain: the invariant source actually uses confocal elliptical caustics and signed areas; prime denotes this tangent-intersection outer polygon. Check exact source restrictions on N, parity, primitive/repeated, winding and stars. Separate source-stated scope from the proof's extension.
2. Canonical coverage: Stachel Theorem 4.3 / (4.9) must cover all real physical families asserted, not merely convex tau=1 families or one orientation. Check modulus convention, confocal relation, 0<v<K, closure shift, least period, and turning number coprimality.
3. Geometry: derive orthogonal projection independently from tangent line; verify denominator nonvanishing for real w; match the order of outer sides to tangent order; check no parallel consecutive tangents, especially star configurations.
4. Complex continuation: Jacobi periods for Q, locations and orders of all possible poles; removable shared Jacobi poles; residue collinearity at adjacent poles; no overlooked coincident singular vertices. Check period reduction using Bezout and whether imaginary period enlargement changes count.
5. Divisor argument: derive reflection and imaginary character carefully, including index reversal. Establish zeros are regular distinct points and exhaust divisor; address T identically zero and no division by zero.
6. Odd focus switch: 2K is a half reduced period precisely for odd N. Check orientation reversal, cyclic indexing, circular limit, v->0 and v->K limiting cases; no unsupported extension to hyperbolic/degenerate caustics, repetitions, even product or unsigned areas.

## Falsification plan
Construct the actual orbit and outer vertices independently; recover outer side lines from adjacent outer vertices and project foci without using the submitted closed foot formula. Compare to independently derived formula and test signed product phase invariance across noncircular shape, eccentricity, N, coprime star winding, orientation reversal and even controls. Test cyclic-index and repeated-path effects. Numerical evidence is uncertified and cannot prove universal constancy or analytic pole counts. Derive or symbolically check all algebraic steps and analyze boundary assumptions. Verify sources by hashes, extracted context and rendered pages. Seek counterexamples to every claim stronger than the exact proven domain.

## Pre-evidence risk ranking
High: source edition mapping; exact source domain versus claimed restriction; Stachel canonical coverage for all primitive star families; simultaneous adjacent pole terms and exhaustion of singularities.
Medium: ordered outer-side correspondence, reflection reindexing, nonvanishing and compact-torus divisor argument.
Low but explicit: a>c real denominators, orientation reversal, circular standalone case.

Current disposition: no acceptance; approximately 10% complete toward an independent source/domain audit. The exact remaining gap is every source check and every proof verification listed above.
