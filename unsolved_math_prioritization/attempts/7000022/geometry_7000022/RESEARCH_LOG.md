# Research log for Problem 7000022

Date: 2026-10-05 UTC. Target: Ghomi Problem 5.3, AMR-069-0022, rank 749.

## Source and prior-work checkpoint

15:25-15:35 UTC. The requested numeric landing page was attempted first and was unavailable to the web reader. The author's complete 2019 PDF was downloaded and its exact named Problem 5.3 inspected in text and in a rendering of printed page 14. The target concerns convex-hull surface area of an arbitrary finite-length closed space curve, with doubled planar area.

The pinned source corpus was available locally. Both full files were independently rehashed and matched the live repository manifest. The numeric problem record and the unique matching AMR-069-0022 report were inspected in full. The report contains status triage and no mathematical proof. Repository checks included the current main queue, main attempts directory, exact-ID/code PR searches, issue search, branch search, the original individual desk review, the later adversarial correction, and related-target groups. No prior exact-target attempt was found in these checks. The searches are not an exhaustive scan of every unpublished or deleted branch.

The earlier projection proposal was explicitly revised in the repository because Jensen does not upper-bound the second moment by the squared first moment. The present investigation preserves and quantifies this obstruction. Unrelated personal-context retrieval hits were not treated as actual work on this target.

Primary-source status checks located Ghomi's October 2024 restatement of the same question and Zalgaller's 1996 Section 7 discussion. Ghomi-Wenk's 2024 inradius theorem and the 2026 Bohr-Markvorsen-Raffaelli volume result were distinguished from surface-area maximization. Neither supplies the missing assertion. The scholarly status check is targeted, not exhaustive.

Exact-target completion estimate at this checkpoint: 0% verified resolution; the prior triage does not count as a proof.

## Approach 1 Polygonal compactness and few-vertex controls

Mechanism: approximate every rectifiable loop by closed polygons, pass hull area through the Cauchy projection formula, and inspect finite hull combinatorics.

Output: a complete polygonal equivalence proof, existence of a normalized maximizer, and `A <= L^2/8` for hulls with at most four vertices. The square shows sharpness of the four-vertex coefficient. Complete arguments appear in Sections 2.1-2.3 of `PROOFS.md`.

Gap: no estimate uniform over arbitrarily many vertices with the circle constant has been obtained. Existence of a maximizer supplies no planarity theorem. Status: partial, blocked at the general polygonal inequality. Full-target completion estimate: 0% verified resolution.

## Approach 2 Integral geometry of planar projections

Mechanism: combine the Cauchy surface-area formula with planar convexification and isoperimetry, then compute projected-length moments.

Output: `A <= 2L^2/(3*pi)` with a full derivation. The doubled segment has second moment `2L^2/3` and squared mean `pi^2 L^2/16`. Moreover Jensen forces the second moment above `L^2/2` for every nonzero curve, so the length-only moment route cannot be made sharp by a stronger universal moment bound. An exact averaged-deficit identity specifies the missing term.

Gap: a lower bound for averaged projected isoperimetric deficits linked to the space-curve length is unavailable. Status: blocked; the reversed Jensen step is disproved. Full-target completion estimate: 0% verified resolution.

## Approach 3 Mean width and support functions

Mechanism: estimate directional variation of a closed curve, then use the spherical support-function representation of surface area and Poincare's inequality.

Output: `A <= pi*L^2/16`, a stronger universal bound than Approach 2, plus a sufficient mean-width-slack threshold for the conjectured bound. The classical geometric inequality is independently derived at the level stated, with a smooth-approximation argument for nonsmooth hulls.

Gap: the universal coefficient remains larger than the target by the factor `pi^2/8`. The slack condition does not cover circles. Status: partial; no assertion of a new best bound. Full-target completion estimate: 0% verified resolution.

## Approach 4 Intrinsic boundary disks and optimal tours

Mechanism: use the established nonpositive-curvature disk proof for curves lying on their hull boundary, then test whether an arbitrary optimal loop can be moved there without length increase.

Output: the known conditional application of Weil's inequality is made explicit. For the octahedron with poles at height plus/minus `1/10` and equatorial vertices plus/minus the first two coordinate unit vectors, all shortest Euclidean tours have an interior pole-to-pole edge. Their common length is strictly less than the exact shortest boundary-tour length. A proof valid for the entire height family and an exact 60-cycle check are supplied.

Gap: the boundary replacement step is false for a fixed hull; the established boundary case does not cover the full target. The octahedron itself satisfies the target strictly. Status: blocked reduction with exact witness. Full-target completion estimate: 0% verified resolution.

## Approach 5 Plateau fillings and area comparison

Mechanism: seek to control convex-hull area by the area of a spanning disk, to import a disk isoperimetric estimate.

Output: the closed walk on the three coordinate arms has positive tetrahedral hull area and an explicit zero-area Lipschitz cone filling. Every fixed-factor comparison of hull area with minimum filling area fails for this admissible curve.

Gap: a filling argument requires extra geometric information that retains convex-hull area despite collapsing or folded fillings. Status: blocked reduction with exact witness; no counterexample to the target. Full-target completion estimate: 0% verified resolution.

## Author freeze checkpoint

The five-approach budget is exhausted. The authored proofs and exact controls are ready for independent audit; authorship did not include an independent audit. Verification may correct errors in these stated results but must not become a sixth proof-search route. No remote writes, releases, outside communications, or source-content publications occurred. The investigation deliverable is complete; the exact sharp general inequality remains unresolved.
