# Research log: 30001893

All times UTC on 2026-10-05. Completion percentages are subjective estimates toward resolving the full mathematical question, not probabilities of correctness or percentages of elapsed work.

## 09:36:12 - Source and prior-attempt gate (5%)

Verified the local descriptor's ID 30001893, identifier OWR-11136-024, title, and source DOI. Did not treat the queued status or zero prior turns in that descriptor as proof of untouched history. Read the repository research policy. No remote mutation was performed.

The exact UnsolvedMath target URL was attempted through public web retrieval and direct HTTP retrieval. The web tool returned internal errors; direct retrieval returned HTTP 403, including the alternate hostname. The exact live statement and the upstream machine-generated report could not be inspected. This remains a source limitation.

## 09:37:03 - Original source and correction (15%)

Located OWR 44/2011, printed p.2539, Problem 2. It asks for the maximal realization-space dimension for n>3 convex regions of R^3. Its surrounding numerical statements use 4n-1 for regular three-dimensional diagrams. Located the 2015 Leon-Ziegler preprint and Leon's dissertation. The inspected later theorem gives regular dimension 4n-5, with full-space equality stated as a conjecture. The original question and later corrected conjecture were separated before developing the proof attempts.

## 09:38:46 - Bounded history and current literature (15%)

GitHub all-state PR searches for 30001893, 11136, and the phrase convex partition returned no target result. Broader partition and convex queries returned 13 and 41 results respectively; their titles and bodies were inspected for an exact match. The projective-partition problem PR70 is a different target, as are the other convexity, geometric, and polynomial tasks. Branch searches for the ID, 11136, and partition returned none; dimension and convex produced only other identified targets, with continuations consumed to exhaustion. The main attempt directory contained 61 entries and no 30001893 folder. Available local attempt-directory snapshots likewise contained no exact target folder. Default-branch code search for the ID returned none. A recursive-tree request failed in transport and was replaced by the successful actual-directory read. These are bounded checks, not an exhaustive claim about all past names, all history, or unavailable raw records.

Available task-history listing could not be read in this executor because it is not attached to the conversation service. No hidden history was inferred. The raw upstream AI corpora were not available and were not inspected.

Primary-literature searches covered the exact title; combinations of convex partitions, dimension, three dimensions, Leon, Ziegler; 4n-5 and 4n minus 5 variants; and date-qualified 2019-2026 queries. The 2015 sources directly state the conjecture. The author's institutional publications list verifies a 2018 chapter of the same title, but the publisher full text was not accessible. A later related paper, *On the Dimensions of the Realization Spaces of Polytopes*, arXiv:2007.00645, was inspected at abstract/full-text search level; no partition or Leon match was found. Other surfaced measure-equipartition papers concern different questions. No full resolution of this exact dimension question was located in this bounded pass. That does not establish current global openness or novelty.

## 09:40:26 - Five approaches developed (20%)

1. Supporting planes: proved polyhedrality without a face-to-face assumption and obtained a canonical graph-chart dimension upper bound 3*binomial(n,2). Gap: controlling compatibility codimension.
2. Regular liftings: removed the common affine-function and positive-scale gauges; proved the absence of further generic fibers using triangle propagation and a tetrahedral insertion construction. This recovers a prior 4n-5 result. Gap: nonregular strata.
3. Central fans: used the spherical graph Euler inequality V<=2n-4, with open ray-coordinate charts from simple polytopes, to get exact central subclass dimensions. Gap: multiple finite vertices and bounded faces in affine partitions.
4. Cylinders: constructed 4n-5 parameters with an injective quotient-coordinate description. An explicit four-cell planar partition has a nonzero outer-cycle determinant and cannot be regular; the obstruction survives extrusion. Gap: this family does not exceed 4n-5 and does not cover general pointed strata.
5. Incidence/rank: built a regular five-cell diagram with bounded tetrahedron and six unbounded quadrilateral-face coplanarity equations. The exact Jacobian has rank five, not six. A nonzero minor plus an injective regular family proves local dimension 15. Gap: no uniform all-strata rank certificate.

## 09:42:34 - Visual primary-source check (20%)

Rendered and visually inspected the actual OWR target page and the preprint's theorem/conjecture page. Confirmed that the printed discrepancy is real, not a text-extraction artifact. Source PDFs and rendered/extracted material remain excluded from the authored package.

## 09:50:39 - Exact controls and author checkpoint (20%)

Completed the retained proof manuscript. Self-review corrected the explicit outer-line determinant's sign to -1; nonzero was the relevant obstruction and the exact program now binds that sign. The Jacobian's selected five-by-five minor equals +1. Standard-library exact controls passed with 825 off-boundary grid points, 1,250 gauge pair checks, 2,540 mathematical checks/guards in the retained selftest run, and 12 rejected mathematical/status mutations. Ordinary and optimized Python outputs matched byte for byte. These controls do not substitute for the analytic arguments or prove the unproved global upper bound.

All five approaches are complete as partial attempts. No full solution or prior full solution was found, and no claim of novelty was established. A fresh independent audit is pending. Publication and repository changes remain outside this package's completed actions.
