# Independent audit: exact counting of simple polygonalizations

Audit date: 8 October 2026. Mathematical target: TOPP Problem 16, 5500016 / AMR-054-0016.

## Decision

**Accept the frozen report as a collection of correct, carefully bounded partial results and the checker as a successful finite verification artifact. The unrestricted exact-counting problem is not solved.** No polynomial-time algorithm, hardness classification, fixed-parameter algorithm, or novelty conclusion follows from this package.

The entire 24,229-byte report and entire 14,014-byte checker were inspected. All eight files in the frozen public package were hashed; all seven entries in its self-excluding manifest match. The report, checker, expected output and original manifest have these SHA-256 identities:

- Report: `51ce97fa26e2f27f4f649b89a85711c118467ac8210835f518206990ef19e621`
- Checker: `c3598583dacd2695b4a245fafb23c9b253c31262c95e6f7a8fe8236b514eae33`
- Expected output: `bceedd5fd3210423942f9001d7e75ab0c8c1c15225917e2f2f2845ec82711959`
- Original manifest: `633ea7bc019fe35490faacdc2b42b31ce1e48048c60689f2f054bec813de08b5`

No mathematical correction to the frozen report is required. The clarifications below strengthen the audit trail without replacing its proofs. All original bytes and original read-only permissions were preserved. This audit contains newly authored analysis, synthetic mathematical fixtures, executable tests and public-source verification metadata. It contains no copied source document or dataset.

## 1. Definition and computational model

The counted object is an undirected simple Hamiltonian cycle on the fixed, distinctly located input points. Rotation and reversal of its vertex sequence identify the same object; geometric symmetries do not identify different edge sets. Distinct labels ensure the dihedral action on a full sequence is free for n at least 3. Starting at label 0 and requiring its next label smaller than its predecessor selects exactly one of the two directed traversals.

The principal hypotheses are rational binary coordinates and no three collinear points. Four cocircular points cause no problem for the report's geometric predicates. A separate, explicitly stated convention covers collinear inputs: straight-through boundary vertices are valid, while retracing, overlaps, vertex-through edges and nonadjacent contacts are invalid. The independent checker agrees with this convention, including the boundary perturbation changing the count from 1 to 4. Such a perturbation cannot be silently substituted for a counting-preserving reduction.

The rational bit model is correctly specified. A determinant or a constant-sized linear system involves polynomially many bits in the coordinate encoding, without an appeal to an unencoded real-number oracle. At most (n−1)!/2 objects gives O(n log n) answer bits, so exponential object count is not an exponential output-length obstruction.

The #P-membership argument is valid: use exactly n fixed-width vertex fields, reject out-of-range labels, repetitions, noncanonical sequences and nonsimple drawings. Every valid cycle has one accepting witness. If defining the function on all binary strings rather than promised inputs, malformed or out-of-promise inputs can be rejected in polynomial time. This proves membership, not hardness. Euclidean distances appear only in an existence argument below, so exact comparison of sums of square roots is not needed by this verifier.

## 2. Mathematical audit of the five approaches

### A. Subset/start/end state compression

For the six specified points, both prefixes A=(0,1,4,2) and B=(0,4,1,2) are simple, visit exactly the same labels and have the same start and end. Both possible completions of A fail. B's completion through 3 then 5 fails; its completion through 5 then 3 succeeds.

The independent segment-parameter implementation verifies all four completed cycles and the two prefixes. The printed crossing certificates are exactly (124,−13,−54,83) for edges 42/35 and (35,−36,−11,60) for edges 41/50. These give continuation counts 0 and 1.

This rejects a transition rule that assumes individual prefixes sharing this state have identical continuation counts. It does not reject every aggregate dynamic program or every possible state augmentation. The report expressly makes this distinction. Its full-prefix recursion is finite enumeration, with no claimed polynomial state bound.

### B. Polygon–triangulation incidences

A plane straight-line graph consisting of the polygon and hull edges can be augmented to a triangulation. Counting incidence pairs therefore gives sum_T |H(T)| = sum_Q e(Q), and reciprocal weighting by the positive extension count gives the second identity. No uniform denominator is implied.

For the five-point witness, independent geometry finds only the crossing pair 13/24. Both K5 minus 24 and K5 minus 13 are plane and have the maximal 9-edge count for this triangular hull. Every other triangulation must exclude at least one of this unique pair, so these are exactly the two triangulations.

Independent cycle enumeration finds eight polygons, four with one completion and four with two, for twelve incidences. Q1=(0,1,2,3,4) has multiplicity 2 and Q2=(0,1,2,4,3) has multiplicity 1. Both identities hold. The convex-five comparison has one polygon and five triangulations, so even a divisor depending only on n cannot fit these two point sets. This says nothing about hardness of counting cycles inside a triangulation.

The connectedness warning is essential. A degree-two spanning subgraph can be a union of cycles. Deleting the checker's connectivity condition is detected by its exact tests.

### C. Crossing-event inclusion–exclusion

In general position, nonincident crossings are precisely the forbidden pairwise events. For each abstract Hamiltonian cycle, the product of (1−I_x) is its crossing-free indicator. Expanding and exchanging finite sums proves the displayed formula with sign (−1)^|A| and forced edge union F(A). Degenerate forbidden contacts are not exhausted by proper crossings; the report correctly restricts the theorem.

For a forced graph F, degree greater than two or a proper cyclic component prevents a spanning cycle. A spanning cyclic component is itself the unique containing cycle. Otherwise the components are paths and isolated vertices, with m=n−|F| blocks and p nontrivial paths.

For m at least 3, ordering the distinguishable blocks around a directed circle and orienting each nontrivial path gives (m−1)!2^p directed cycles, and reversing the full cycle pairs them. The following explicit boundary checks remove any possible ambiguity from using a block-circle argument at small m:

- m=1: there is one spanning path, so p=1. Its two endpoints must be joined. There is exactly one undirected cycle, as 2·0!/2 predicts.
- m=2, p=1: a spanning path on n−1 vertices and one isolated vertex must be joined at the two path endpoints. There is one cycle.
- m=2, p=2: the two nontrivial paths have two ways to pair their endpoints across components. These are distinct undirected cycles, giving 2.
- m=2, p=0 would mean n=2 and is excluded. For a forest with n at least 3 there is no additional exception.

Thus 2^p(m−1)!/2 is correct in every stated forest case. Independent abstract edge-mask enumeration verifies every forced subgraph of K3, K4, K5 and K6, a total of 33,864 cases. This finite check supports the implementation; the proof above establishes the formula.

The convex four-point-group construction really supplies 2^r different event subsets with nonzero terms, because their forced edges are matchings on disjoint groups. It only obstructs algorithms explicitly enumerating all nonzero terms. It cannot exclude polynomial symbolic cancellation, and the report does not claim otherwise.

### D. Positivity and restricted reductions

The minimum-length Hamiltonian-cycle proof is sound. When edges ab and cd cross at x, the reconnection that yields one cycle has total length strictly less than |ax|+|xb|+|cx|+|xd|, by the strict triangle inequalities for the two replacement edges. This contradicts minimality. General position then excludes all other forbidden contacts. No efficient TSP algorithm is assumed.

Consequently every valid promised target with at least three points has positive count. An input of a source problem with count zero cannot map parsimoniously to that domain. The same obstruction applies when equality is modified only by a strictly positive multiplicative factor. It does not apply to additive-baseline, interpolation, multiple-query, or other reductions using a broader target domain. In particular it is not evidence against #P-hardness under Turing reductions.

No geometrically enforced allowed-edge mask, count-preserving gadget family or reconstruction scheme is supplied. The report correctly leaves those requirements open. Optimization hardness of polygon area or tour length alone is not a counting reduction.

### E. Hull order and interior-point parameter

The hull-order proof is valid under its stated general-position hypothesis. A polygon arc between consecutive vertices in the polygon's restricted hull-vertex order has only strictly interior vertices between its endpoints. If the endpoints were not hull neighbors, that arc would be a crosscut of the convex hull. Its complement along the polygon would have to connect points on both sides without meeting the crosscut, contrary to separation. When there are three hull vertices, every cyclic ordering is already the same order or its reverse.

Fixing the counterclockwise hull order removes reversal unambiguously because h is at least 3. Each ordering of the k interior labels and weak composition into h gaps describes exactly one candidate. Conversely a polygon determines exactly that pair. Hence the candidate count is k!·binomial(n−1,k)=(n−1)!/(h−1)!, and no extra factor of two is needed.

Each candidate can be checked with O(n²) exact predicates. Since the candidate product has k factors each at most n, the bound is n^{k+O(1)} with polynomial bit arithmetic. This is an XP bound. It is not an FPT bound, because the exponent depends on k. The k=0 count 1 and k=1 count h are correct. For triangular hulls the candidate count reverts to all (n−1)!/2 abstract cycles, so the unrestricted problem is not improved by this enumeration.

## 3. Primary-source and current-status audit

The source review is bounded, not a certificate of worldwide openness or priority. Public primary pages were checked on 8 October 2026, together with retained original source bytes that were independently rehashed. Fresh PDF text extractions also match the inspected retained text for all five retained PDFs. Details, scope and retrieval distinctions are in `SOURCE_AUDIT.json`.

- [TOPP Problem 16](https://topp.openproblem.net/p16) still displays an open status and the 18 June 2025 revision. Its broad wording around the exponent is not substituted for the primary theorem.
- [Marx–Miltzow, SoCG 2016](https://doi.org/10.4230/LIPIcs.SoCG.2016.52) and the [full version](https://arxiv.org/abs/1603.07340) state n^{O(sqrt(n))} for Hamiltonian cycles in Theorems 6 and 8 respectively. The 11+o(1) coefficient is for triangulations. The full version assumes noncocircularity in its constrained-Delaunay construction and expressly says a small affine transformation can achieve it. The report is conservative about tie handling; it does not claim to reimplement that argument.
- [Wettstein's manuscript](https://arxiv.org/abs/1604.05350) gives a spanning-cycle combination graph with base below 5.61804; constructing it adds the stated polynomial factor. This is exponential counting, not a polynomial-time exact solution. The journal DOI could not be fetched in this audit's web tool, so the manuscript and its theorem were used instead.
- [Eppstein's 2024 journal article](https://doi.org/10.1007/s00453-024-01255-y) provides output-polynomial enumeration and a constant-factor approximation of the logarithm of the count. Its conclusion explicitly discusses XP versus FPT and asks about #P-completeness. These points occur in the journal version; the retained 2023 preprint has a shorter conclusion. No exact polynomial counter is obtained from these results.
- [Counting Polygon Triangulations is Hard](https://arxiv.org/abs/1903.04737), v2, proves hardness for polygon domains with holes, under Turing reductions. Its closing discussion separates unconstrained point-set counting. It does not establish the target's hardness.
- The Tuggle–Snoeyink contribution in the [FWCG 2025 booklet](https://www.cs.qc.cuny.edu/goswami/Abstracts-FWCG-25.pdf), PDF pages 42–47, studies reachability pruning and experiments for path enumeration in embedded graphs. The [2026 Cruces–Huemer–Lara paper](https://doi.org/10.1007/s00373-026-03010-2) counts drawings of a fixed combinatorial triangulation. The inspected material does not resolve the unrestricted target.
- [Erickson's historical question](https://jeffe.cs.illinois.edu/open/randompoly.html) explicitly includes counting the same polygons. It establishes target overlap only; it is not current-status evidence or an equivalence proof between general counting and uniform sampling.

Two contemporary keyword searches, followed by primary-source inspection where relevant, did not locate a resolution. This is limited search evidence, not a theorem that no resolution exists. No new research approach was pursued in this audit.

## 4. Independent executable verification

The author uses orientation determinants and bounding boxes. The independent geometry instead solves a+t(b−a)=c+s(d−c) using exact rational elimination. Parallel lines are handled by one-dimensional parameter intervals. Its output distinguishes an empty intersection, a single point and positive-length overlap. The cycle checker examines every pair of edges, including adjacent pairs, and permits an intersection only when it is exactly their shared endpoint.

This implementation never calls the author's `orient`, `on_segment` or `intersects` to decide simplicity. Independently generated abstract cycles are deduplicated by their full undirected edge sets rather than the author's next/last-label convention. The independent enumerations still use standard mathematical identities and exact arithmetic; they are not a formal proof assistant or an independently audited Python runtime.

Results:

- All 6,561 ordered quadruples from the 3×3 integer grid give identical intersection decisions: 3,128 empty, 3,161 singleton and 272 overlapping.
- All 729 ordered grid triples agree on point-on-segment membership, including repeated endpoints and zero-length segments.
- All 12 author fixtures have the same independently computed counts: triangle 1; convex 4, 5, 6 and 7 all 1; triangle-plus-one 3; hull-four-plus-one 4; two-interior 8; six-mixed 13; collinear-four 0; straight boundary 1; inward perturbation 4.
- Every 3-, 4-, 5- and 6-point subset of the grid was tested, totaling 420 point sets and 7,014 cycle decisions. Collinear and contact degeneracies are included.
- Thirty deterministic seeded general-position examples, twenty of size 6 and ten of size 7, agree between independent enumeration, the author enumeration and hull-gap counting. Eighteen of these also run inclusion–exclusion with at most twelve events.
- A separate 17-event fixture has count 40 by both independent counting and inclusion–exclusion. A 19-event fixture with independent count 39 is rejected by the configured event cap. These exercise acceptance and rejection close to the cap.
- All 33,864 forced-edge graphs through K6 agree with independent abstract masks. Explicit one-block, two-block, proper-cycle, spanning-cycle and degree-three cases also pass.
- Five independent metamorphic tests cover an affine shear/translation, rational rescaling, relabeling, reflection and rational denominators at the input-bit boundary. Each keeps count 13.
- Six named geometry-boundary tests separately check a straight boundary, backtracking, nonadjacent touching, overlap, a crossing closing edge and the corresponding valid open prefix.
- Twenty-eight malformed-input or cap/degeneracy rejections, seven acceptance/label boundary checks, and a simulated non-1000 UID rejection pass. The actual executions run at real and effective UID 1000; the simulation only tests the harness guard.

All twelve deliberately incorrect variants are rejected: omitting proper crossings; contact membership; the closing edge; reversal normalization; connectivity; path orientations; forced-cycle division by two; proper-cycle rejection; a composition endpoint; the exact bit bound; general-position checking; or the exception-based validation guard. The exact modified-source hashes and failure reasons are recorded in the deterministic output. Mutation coverage is specific to these changes and does not imply complete fault coverage.

## 5. Execution, integrity and reproducibility

`run_validation.py` runs the complete frozen author checker and the complete independent audit in ordinary, `-O` and `-OO` modes. It compares every byte of stdout with the corresponding expected JSON. It requires UID 1000, checks read-only permissions and makes genuine create/append attempts that must raise PermissionError. Output capture is outside the read-only input directories.

The final receipt is `receipts/EXECUTION_RECEIPT.json`; all six complete stdout captures and all six stderr captures are retained alongside it. Every run exits 0, has empty stderr and exactly matches its expected output. Both input snapshots remain identical. `PYTHONDONTWRITEBYTECODE=1` prevents bytecode caching. The frozen author's full output is 7,683 bytes; the independent output is 25,560 bytes.

The execution receipt records the files present in the audit input directory during the run: its two scripts and expected JSON. The prose audit, source metadata, receipt copies and final package manifest are assembled afterward. They are not falsely represented as having been input files of the mathematical computation. The frozen author snapshot includes all eight original public files.

This establishes observed POSIX permission-bit protection under the actual unprivileged UID, not a separate mount namespace or container sandbox. The tests rely on explicit exceptions rather than removable assertions. Optimized-mode agreement is an execution observation, not a claim that every possible Python defect was excluded.

## 6. Accepted scope and remaining gaps

Accepted: all five stated partial claims; the model and degeneracy conventions; #P membership and polynomial answer length; source-scope distinctions; the original full output; the independently rechecked finite examples; and the executable guard/mutation behavior above.

Not established: a polynomial geometric state summary; a tractable uniformly weighted triangulation sum; polynomial aggregation of crossing-event terms; a geometric counting-hardness reduction; an FPT bound; a full audit or implementation of cited algorithms; exhaustive current-literature coverage; novelty; or a solution to unrestricted exact counting.

The original report's unresolved status should therefore remain unchanged.
