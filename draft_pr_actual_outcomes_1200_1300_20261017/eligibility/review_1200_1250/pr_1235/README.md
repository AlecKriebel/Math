# Generalized hive polytopes: exact integral-point counterexamples

Problem 30000107 / OWR-741-001, *Integrality of Constrained Polytope Families*.

For the primitive boundary and rhombus matrices displayed in De Loera–McAllister’s Definition 2.2, there are explicit integral right-hand sides at triangular side parameters r=6 and r=7 for which the generalized hive polytope is nonempty but has no integral point. Four entries of a feasible nonnegative array are 1/2 and the rest are zero; taking each rhombus bound to be the ceiling of its value gives integral bounds. Two short, exact nonnegative weighted sums of rhombus inequalities force one coordinate to be 1/2 in every feasible real array.

The r=6 example conflicts with the explicit integral-vertex consequence of the published 2006 Theorem 4.6 under those displayed definitions. This is a correction to that consequence and to the arbitrary-integral-right-hand-side integral-point assertion. No error in historical implementation is diagnosed, no priority is claimed, and no maximum valid parameter is established. Standard Littlewood–Richardson saturation is unaffected.

## Complete proof and scope

- [PROOF.md](PROOF.md) retains the historical candidate proof with its original pending-review status explicitly contextualized by the later acceptance. Accepted audit supplements provide the complete r=6 proof, both bound specifications, boundedness and all convention safeguards.
- [AUDIT.md](AUDIT.md) preserves the complete subsequent mathematical audit, including every r=6/r=7 inequality and weight, geometric orientation, indexing, exact witnesses, nonnegative slack, full integer column lattice, boundary normalization, positive translation and boundedness.
- [ACCEPTANCE.md](ACCEPTANCE.md) and [ACCEPTANCE.json](ACCEPTANCE.json) give the exact accepted scope and exclusions.
- [SOURCES.json](SOURCES.json) records public scholarly citations, PDF hashes and sizes, version dates and the earlier text/visual inspection history.
- [VERIFICATION.json](VERIFICATION.json) distinguishes exact certificate checks from byte authentication and records the selected-subset versus complete-retention distinction.
- [MANIFEST.json](MANIFEST.json) lists exactly eight files and hashes the other seven.

The examples rule out a unimodular conical cover by determinant-±1 column bases. They do not by themselves decide a separately interpreted affine unimodular triangulation of the convex hull of the matrix columns. Those assertions must not be conflated. The audit explains why the columns do not lie at affine height one and gives a simple counterexample to the general affine-to-conical implication.

This AI-assisted, unrefereed edition records an internal AI mathematical audit. Acceptance means the explicit counterexamples and their stated scope passed that audit; it is not external human peer review or formal proof-assistant certification. The complete hand-checkable inequalities are part of the authored proof. This is a written proof/correction/audit edition, not a computational reproduction package. Source inspection and exact certificate verification occurred in the preceding investigation on 11 October 2026; editorial preparation authenticated retained bytes without a fresh scholarly-source inspection or mathematical-program rerun.

The explicit finite mathematical tables are essential authored proof, not a raw data catalog. This edition distributes no raw JSON certificates, solver/checker code, source PDFs, source extracts, page images or private coordination material. No source-author code was executed. A bounded search found no verified erratum resolving the exact source conflict; it does not establish absence or novelty.
