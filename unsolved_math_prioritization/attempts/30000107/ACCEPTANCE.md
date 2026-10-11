# Acceptance: exact generalized hive counterexamples

Decision: ACCEPT_EXACT_COUNTEREXAMPLES_WITH_SOURCE_CONFLICT_EXPLICIT.

The arbitrary-integral-right-hand-side integral-point assertion is false for the displayed primitive hive matrices. Both r=6 and r=7 instances are accepted as exact counterexamples. Each has integral boundary data, integral rhombus bounds and an explicit nonnegative rational feasible labeling, but no integral labeling, even when arbitrary real interior coordinates are allowed.

For r=6 the forced entry is h(1,1,4)=1/2; for r=7 it is h(1,4,2)=1/2. The proof is addition of explicitly listed rhombus inequalities with nonnegative integer weights. It is not inferred from a solver’s infeasibility status or merely from a fractional vertex.

## Included conclusions

1. All three primitive rhombus formulas agree with genuine geometric elementary rhombi and the published indexing/orientation. The triangular parameter is the sum of the three indices.
2. The witnesses are 1/2 at four listed interior points and zero elsewhere. Boundary data are zero and each integral bound is the ceiling of the witness’s rhombus value. Every nonzero bound is listed.
3. Both lower and upper weighted sums are displayed completely. They force a half-integral coordinate at every feasible real point.
4. The witnesses and slack are nonnegative, so the paper’s nonnegative augmented formulation is directly nonempty. Integer slack is automatic for integral labelings and integral bounds.
5. Boundary-coordinate, anchored difference and unanchored constant-level formulations cannot restore integrality. Relabeling requires the corresponding relabeling of bounds; arbitrary non-unimodular changes or rescalings are not asserted equivalent.
6. The augmented matrix has a determinant-one minor consisting of boundary columns and all slack columns; its integer column lattice is the full ambient lattice.
7. Every nonempty fixed-boundary fiber is bounded, by the telescoping and segment-concavity recession argument. The counterexamples are genuine polytopes.
8. Translating by q(i,j,k)=i²+j²+k² gives strictly positive boundary data, rhombus bounds and witness. Since Rq=2 in every row, integral points translate bijectively. The forced coordinates become 37/2 at r=6 and 43/2 at r=7.
9. The r=6 example contradicts the explicit integral-vertex consequence of De Loera–McAllister’s published Theorem 4.6 under its displayed generalized-fiber definitions. Both examples rule out the corresponding unimodular conical-cover assertion.

## Exclusions and historical accuracy

- No standalone verdict is made about an affine unimodular triangulation of conv(columns M). It is different from a unimodular conical cover, and no affine height-one hypothesis is available here.
- No historical computational implementation error, responsible step, corrected maximum rank, first discovery or priority is identified.
- Standard Littlewood–Richardson saturation has its special zero rhombus bounds and boundary family and is not challenged.
- The published r=4 example corrects the arXiv r=5 example label; this fact does not resolve the r≤6 theorem conflict.
- The bounded erratum search is not an exhaustive novelty or absence proof.
- The original candidate report’s pending-audit claim is historical. The later complete independent audit accepts the explicit mathematics; it does not resolve the cause of the source discrepancy.

The proof and complete audit appear in PROOF.md and AUDIT.md. Exact independent checks used an independently reconstructed triangle-adjacency geometry and optimization-safe rational arithmetic. Normal, -O and -OO runs agreed and rejected nine altered certificate inputs per rank per run. These are exact finite certificate checks supporting the displayed algebra, not a substitute for the written proof or formal proof-assistant certification.

This AI-assisted, unrefereed edition records an internal AI mathematical audit. Acceptance means the explicit counterexamples and their stated scope passed that audit; it is not external human peer review or formal proof-assistant certification. The complete hand-checkable inequalities are part of the authored proof. This is a written proof/correction/audit edition, not a computational reproduction package. Source inspection and exact certificate verification occurred in the preceding investigation on 11 October 2026; editorial preparation authenticated retained bytes without a fresh scholarly-source inspection or mathematical-program rerun.
