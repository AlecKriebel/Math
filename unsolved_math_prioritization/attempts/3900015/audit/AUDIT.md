# Independent audit of reciprocal rectangle packing reductions

Problem 3900015 / AMR-038-0015, rank 928. Reviewed 2026-10-06 UTC.

## Decision

Accept the unchanged author packet as an unresolved bounded partial investigation with three substantive approaches. The four propositions are correct in their stated models. No mathematical or artifact correction is required. The appropriate proposed queue disposition remains **unsolved, 3/5**. This audit neither changes the queue nor publishes anything.

Acceptance applies exactly to the 16,824-byte author archive with SHA-256 `abaee91d08a6173ca929bde0aa28578486e5d4412bca3a8ce23230a970502612` and the ten members pinned by the included author external manifest. The original archive remains unchanged and is included verbatim. No replacement proof packet is being silently substituted.

The audit independently checked all authored mathematical arguments, complete input-file hashes, the complete exact-ID problem/report pair, relevant primary-source claims, and isolated artifact replay. A separate implementation exhaustively enumerates both grid placements and all orientation/separation systems for the four-piece obstruction. It does not import the author's diagnostic implementation.

## Model and scope

For each positive integer n, R_n has side lengths 1/n and 1/(n+1). The container is the closed unit square. Rectangles are rigid and unsplit, their interiors are pairwise disjoint, and boundary contact is allowed. The report correctly distinguishes a fixed orientation, independent right-angle rotations, and arbitrary rotations. Its negative finite statements concern an axis-parallel prefix together with a specific single square hole. They are not negative results for the original infinite packing problem.

The telescoping area identities are exact. A full countable packing has complement of area zero; countable unions of closed rectangles need not be closed, so pointwise coverage is not inferred. In contrast, the finite family used in the square-hole proof is closed, making its equal-area complement relatively open. This finite-versus-countable distinction is essential and is handled correctly.

## Proposition 1 and arbitrary rotations

The finite-prefix equivalence is valid in all three stated orientation models. Here is an independent check of each compactness step.

A rectangle centered at the origin is represented by a center in the square and a rotation in SO(2), or in the relevant finite orientation set. Its center belongs to the square whenever the rectangle is contained there. The product of these center and orientation spaces for a fixed rectangle is compact and metrizable. Given one packing for every finite prefix, fill unused coordinates by arbitrary points of these spaces. Extract a convergent subsequence for the first rectangle, then a subsequence for the second, and so on. The diagonal sequence has a limit in each coordinate, and its finite-prefix lengths tend to infinity. No compatibility between the initial finite packings is needed.

Containment is closed: each limiting vertex lies in the closed square, and convexity then contains the whole limiting rectangle. Interior nonoverlap is also closed under this convergence. If two limit interiors overlapped, select a point strictly inside both. Applying the inverse rigid motions sends it into the interior of both reference rectangles. These inverse maps depend continuously on center and rotation, so the same point lies inside both nearby rectangles, contradicting the finite packing. This argument permits contact and excludes any hidden positive-clearance assumption.

Restriction gives the converse. Consequently, nonexistence in a chosen fixed model entails failure of some finite prefix in that same model. This implication does not identify a cutoff, and any one large finite computation leaves the universal quantifier unproved.

The reference to Greg Martin's compactness framework is appropriate, and printed page 238 explicitly discusses finite-prefix hypotheses. The authored diagonal proof is complete on its own; it does not depend on unproved general topological shortcuts or on Jiang's recent preprint. No novelty is claimed.

## Proposition 2 and the exact rational grid

The common-denominator reduction is correct for finite axis-parallel packings with positive dimensions in (1/D) Z, where D is a positive integer. First freeze the orientation of each rectangle. Two axis-parallel interiors are disjoint if and only if at least one of the four weak coordinate-separation inequalities holds. Select one satisfied inequality for every pair.

For an inequality x_i + w_i <= x_j, use a directed edge i to j of weight w_i; form the analogous vertical graph. A directed cycle would sum to a strictly positive number at most zero. Thus each graph is acyclic. Add a source with edges of weight zero to all vertices and take longest-path lengths. These lengths are nonnegative grid multiples and satisfy every selected inequality.

The upper container bounds also survive. Every path ending at i has total weight at most the original coordinate x_i, since its first coordinate is nonnegative and all original inequalities hold. The new x_i is therefore no larger than the original x_i, so the original width still satisfies x_i + w_i <= 1. The vertical argument is identical. Each pair retains a selected separator, so moving all coordinates this way cannot introduce an overlap. This completes both feasibility and grid-completeness claims.

For a finite reciprocal prefix, lcm(1,...,N+1) is a valid denominator. Arbitrarily rotated rectangles do not satisfy the axis-parallel separator premise, so the report correctly avoids applying this reduction to that model. Grid completeness proves decidability, not tractability and not existence for untested prefixes.

## Proposition 3 and a single square hole

Suppose R_1 through R_(m-1), with right-angle rotations allowed, coexist with an axis-parallel square H of side 1/sqrt(m). Their areas sum exactly to one. Their finite union is closed in the unit square and has full area. A nonempty relatively open subset of the square has positive two-dimensional area, even when it contains a point on the square's boundary. Hence the complement is empty.

Choose a horizontal line at a height strictly between the top and bottom of H and unequal to any horizontal edge height of the finitely many other rectangles. Its intersection with the unit square is partitioned, apart from shared endpoints, into complete width intervals of the crossed rectangles and one interval of length 1/sqrt(m). Every crossed prefix interval has rational length. Subtracting those lengths from one proves that 1/sqrt(m) is rational. For positive integer m, this occurs exactly when m is a perfect square.

This reasoning allows all real translations and is not an artifact of the computational grid. It imposes a necessary condition only. It does not apply to multiple holes, oblique rectangles, a rotated hole with oblique boundaries, or an arbitrary infinite residual set. The report respects each restriction.

## Proposition 4 and the m equals 4 obstruction

The finite geometric proof is sound. Rotate the entire square by 90 degrees if necessary so R_1 spans its width and has height 1/2. Any half-unit square hole is vertically separated from R_1. The free vertical intervals above and below R_1 have combined height 1/2, so one can contain the hole only when R_1 is flush with the opposite boundary. The remaining region is a 1 by 1/2 strip, and the hole spans the strip's height.

If the hole is strictly interior horizontally, the remainder has two positive-width components. Since the four pieces have total area one, both components must be filled. A positive-area connected rectangle cannot straddle the hole, so R_2 and R_3 must fill one component each. Each component has height 1/2, but neither orientation of R_3 has that height.

If the hole touches an end, the remaining region is a 1/2 by 1/2 square tiled by R_2 and R_3. For two axis-parallel rectangles tiling a rectangle, the shared separator is a full horizontal or vertical cut: choosing a valid horizontal separator forces both widths to span the container, while choosing a vertical one forces both heights to span it. Thus each piece must have a side of length 1/2. R_3 has sides 1/3 and 1/4, again impossible.

The explicit prefix-only packing in the author report fits. Therefore perfect-square m is not sufficient for this splice. The m=4 example does not contradict a late-tail theorem with a vastly larger threshold. In particular, 10^1000 itself is (10^500)^2, so the arithmetic obstruction does not eliminate every candidate in Jiang's stated range.

## Two independent complete exact computations

The author code was read in full. It builds all integer placements, uses exact cell masks with permitted boundary contact, sorts pieces deterministically, and memoizes by depth and occupied cells. At a fixed depth the remaining pieces are fixed, so memoization does not lose geometric information. The reported counts are reproducible: placement counts 14, 126, 180, 49; piece order 0, 3, 1, 2; 75 visited states and 10,204 candidate trials; no four-piece packing.

The new `independent_checks.py` has two separate checks:

1. A coordinate-interval enumerator on the complete 1/12 grid. It uses natural input order, x-major positions, no cell masks, no memoization, and no symmetry pruning. There are 3,064 labeled grid placements of the three-rectangle prefix and zero after adding the hole. The four-piece search visits 1, 14, 204, 3,064, 0 nodes at its successive depths and examines 188,634 placement candidates overall. These different counters are expected because its search order and representation differ from the author implementation.
2. An orientation/separation-system enumerator. For every orientation choice and every one of the four separating inequalities for each pair, it solves the two difference-constraint systems by synchronous longest-path relaxation. Positive edge weights make an n-th-round improvement equivalent to a directed cycle; otherwise at most n-1 edges suffice for every longest path. It tests all 8 * 4^6 = 32,768 systems for the four pieces. Of these, 24,960 have acyclic horizontal and vertical graphs, but zero fit in the container. For the three-piece prefix, 32 of 512 systems are feasible. This is a second exhaustive certificate independent of cell occupancy and grid placement loops.

The exact grid bridge and separator completeness are mathematical arguments, not conclusions inferred merely from test success. Additional diagnostics check telescoping sums, boundary contact, a positive overlap of width 10^-50, admissible square indices through 100, and the perfect-square threshold. None certifies an infinite packing or novel literature progress.

## Complete corpus and provenance audit

All three complete corpora were read as bytes, hashed, and fully JSON-parsed. The catalog and problems each have 15,458 entries; the report mapping has 6,701. Their complete-file byte counts and hashes match the original metadata, not merely small projected records. Exactly one matching ID appears in each of catalog and problems, and the catalog rank is 928.

The full problem object and full report object were selected afresh and serialized with the declared Python JSON defaults. The result is exactly 4,960 bytes and has SHA-256 `24e97cc97da5043fe972e9bfecb2ceb7ffcd8879316a9fea453065c61b6c573f`. It is byte-identical to the author record pair. The inherited report, including its full work-done field, contains literature triage rather than a substantive mathematical attempt. The gate is correctly classified as eligible literature-only prior work. The inherited suggestion of a purely limiting obstruction is corrected by the valid compactness argument.

The author's complete raw bounded-search responses and the retrieved queue context were also inspected privately. They support the historical metadata of queued 0/5, rank 928, and no matches in the stated exact-ID/problem-number code and PR searches and exact-ID commit search. This is inspection of recorded search responses, not an independent fresh repository-wide history search. Neither absent matches nor stale queue fields establish that no earlier work exists.

## Primary sources and honest limitations

All five pinned public source files were hashed in full. All four PDFs were independently re-extracted with `pdftotext -layout`; every extracted file is byte-identical to the author's complete extraction. The PDFs contain 39, 7, 24, and 14 pages for Jiang, Zhu--Joos, Slack-Pack, and Martin respectively. Complete source byte verification must not be confused with validating every mathematical argument inside those sources.

- The [Geometry Junkyard source entry](https://ics.uci.edu/~eppstein/junkyard/open.html) was inspected from the full retrieved HTML and independently through the web reader. It states the same reciprocal-rectangle question.
- [Martin's published paper](https://personal.math.ubc.ca/~gerg/papers/downloads/CTGP.pdf), especially the packing definition, closedness argument, and finite-prefix discussion on printed page 238, supports the attribution. That final page was independently rendered and visually checked.
- [Zhu and Joos, arXiv:2211.10356v1](https://arxiv.org/abs/2211.10356v1), was read from the complete seven-page extraction, including Section 2.1, Theorem 2.1, Corollary 2.2, and references. The 1.35 * 10^11 prefix claim and slightly enlarged square are reported accurately. The huge computation was not rerun, and no certificate for it was independently validated.
- [Kislovskiy, Lerner and Senkevich, arXiv:2412.17151v3](https://arxiv.org/abs/2412.17151v3), revised 2025-07-23, explicitly makes its main tail-packing conclusion conditional on Assumptions 1 and 2. The assumption and theorem passages were inspected in their full page context; page 11 was independently rendered. Numerical plausibility does not discharge those assumptions.
- [Jiang, arXiv:2609.28791v1](https://arxiv.org/abs/2609.28791v1), was freshly retrieved directly from the versioned arXiv URL after the web reader returned a cache miss. The versioned PDF is exactly 567,362 bytes with SHA-256 `7911796db6dad3216b395622a24aea81ec0425e5c94b2496094a8df0b663c9e8`, identical to the author PDF. The abstract, Theorem 1.1 and rotation convention, Theorem 11.6, Section 12, and stated Section 13 threshold were independently checked; page 3 was rendered and visually inspected. The claim is an equal-area axis-parallel packing for every tail beginning at m >= 10^1000. The abstract explicitly leaves the m=1 full sequence open. The arXiv submission date is 2026-09-23 while the PDF title page says September 25. Its full probability argument and claimed Lean checking have **not** been independently validated by this audit.

The original Meir--Moser 1968 paper was not available for inspection. The saved nominal-200 response is a 195-byte unavailable-site HTML page, not a paper. The author's HTTP 403 limitation for the unsolvedmath target and 404 limitation for the linked historical Friedman page remain disclosed as recorded retrieval outcomes. The complete corpus record, not an invented live read, supports the target statement. Neither this audit nor the source searches constitute a guaranteed exhaustive literature review or a claim that no later revision could appear.

## Artifact verification and acceptance boundary

The author archive and external manifest are independently pinned before extraction. ZIP member names, uniqueness, regular-file status, inventory, sizes, and hashes are checked. Twenty-two isolated subprocess tests run the unmodified and relocated author verifier in normal and optimized Python, and check append and same-size mutations of the report and expected output, code mutation, a missing file, an unexpected file, a source symlink, and a wrong inner-manifest hash. All have the expected outcomes. A separate coordinated report-plus-inner-manifest mutation is rejected by the original external pins.

The standalone inner manifest is not a cryptographic signature or an independent trust root: an attacker able to replace both content and its manifest can manufacture a self-consistent bundle. Acceptance therefore pins the author archive and external manifest outside the packet; the audit wrapper embeds those author digests. The audit's own exact archive must likewise be checked against its external manifest or independently trusted digest. All tests and checks use explicit exceptions and remain active under Python optimization.

The audit packet contains only authored analysis and code, safe original authored files in the unchanged archive, and permitted verification metadata. It excludes third-party PDFs, extracts, screenshots, full corpus or record contents, private source files, raw connector responses, and private coordination. It does not modify GitHub or queue state.

## Remaining mathematical gap

No accepted result constructs all finite prefixes, finds a forbidden prefix in the original rotation model, or supplies a compatible finite prefix around a sufficiently late tail square. A proof of any of those appropriate missing claims would be new work. The present audit accepts a correctly bounded partial investigation and no resolution claim.
