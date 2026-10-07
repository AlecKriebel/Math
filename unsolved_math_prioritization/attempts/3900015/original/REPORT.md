# Reciprocal rectangles: bounded mathematical audit

Problem 3900015 / AMR-038-0015. Queue rank 928. Inspection date: 2026-10-06 UTC.

## Outcome and scope

The full packing problem remains unresolved by this investigation. Three substantive approaches were used; the work stopped at a bounded partial result. The results below are elementary reductions and obstructions to a particular proof strategy, not a claimed new solution or a claimed improvement on the best packing bound. No novelty is inferred from unsuccessful searches.

For each positive integer n, let R_n have side lengths 1/n and 1/(n+1). The question asks for all these rectangles inside the closed unit square with pairwise disjoint interiors. Boundary contact is permitted. There is no positive-clearance requirement. No rescaling, splitting, bending, or discarding of rectangles is permitted.

The statement does not explicitly restrict rotations. We distinguish the general rigid-motion problem from the stronger axis-parallel existence problem with independently chosen right-angle rotations. An axis-parallel construction would answer the general question positively; an obstruction confined to the axis-parallel model would not answer it negatively. Fixed orientations, allowing right-angle rotations, and arbitrary rotations are separate models. Equal-area packing implies coverage up to a null set, not necessarily pointwise coverage of the closed square.

## Source and prior-work gate

The complete catalog and problem corpora each contain exactly one matching ID. The complete inherited report was inspected, including its work-done field: it records literature searches and status triage, with no substantive mathematical attempt. It therefore passes the specified prior-work gate. Full-corpus and full-record-pair hashes are recorded separately. The default-branch queue confirmed rank 928 and queued 0/5 at the read; those fields were not used to override the report-level gate. Exact ID and exact problem-number connector searches found no code or PR matches; the ID commit search also found no matches. These are bounded search results, not proof that no earlier work exists.

The requested unsolvedmath web page could not be read live: the direct retrieval returned HTTP 403. Its complete exact-ID corpus record supplied the statement and source link. The actual source-listed Geometry Junkyard page was retrieved and inspected. Its linked historical Friedman page returned 404. The Meir--Moser 1968 publisher page could not supply full text; a nominal HTTP-200 response was an unavailable-site message, not a paper. We do not claim to have inspected that 1968 paper.

The primary literature changes the old triage in two important ways:

- Zhu--Joos, arXiv:2211.10356v1 (2022), reports packing 135,000,000,000 initial rectangles, combining a computation through 100,000,000,000 with an additional packing estimate. This computation was not independently rerun here. Its corollary gives a full packing in a square slightly larger than the unit square, not a unit-square solution.
- Kislovskiy--Lerner--Senkevich, arXiv:2412.17151v3 (2025), gives a Slack-Pack analysis conditional on two explicit assumptions. Its numerical evidence does not discharge those assumptions.
- Jiang, arXiv:2609.28791v1 (submitted 2026-09-23), claims exact-area axis-parallel packings for every tail n >= m >= 10^1000. The author explicitly leaves m=1 open. This is a recent preprint claim; neither its long probabilistic argument nor its claimed Lean checking was independently validated here. The downloaded PDF has a title-page date of September 25, while the arXiv submission and HTML display September 23; the precise downloaded bytes are hashed.
- Martin, *Compactness Theorems for Geometric Packings* (2002), already supplies the relevant compactness framework, including the finite-prefix variation on printed page 238. Thus the compactness result below is not novel. In particular, a negative answer cannot be explained by an obstruction that exists only after all finite prefixes.

See SOURCES.md and SOURCE_VERIFICATION.json for public links, inspected locations, hashes, and access limits.

## Approach 1: compactness locates the exact quantifier gap

**Proposition 1.** Fix one of these allowed orientation sets: a single fixed orientation for every rectangle; the two axis-parallel orientations; or all planar rotations. The entire sequence packs in the closed unit square if and only if every finite prefix does.

**Proof.** Center each reference rectangle at the origin. For a packing of the first N rectangles, record each center in [0,1]^2 and its allowed orientation. The orientation space is compact in each of the three cases. Fill in arbitrary coordinates for indices greater than N. Successive subsequence extraction for indices 1, 2, ... and a diagonal choice give a subsequence on which every fixed rectangle's center and orientation converge. Every fixed rectangle is eventually present. Its limiting position is contained in the square because its vertices converge and the square is closed and convex.

If two limiting interiors met, a point in their intersection would have positive distance from both boundaries. Small changes in center and orientation preserve membership in both interiors: equivalently, inverse rigid motions of that point converge to points strictly inside the two reference rectangles. Thus the two interiors would already intersect in sufficiently late finite packings, a contradiction. The limit is the required packing. Restriction proves the converse. No compatibility between the chosen finite packings is required. The use of interior-disjointness, rather than disjoint closed sets or a strict separation margin, is essential. QED.

For axis-parallel rectangles the closed condition is especially transparent: at least one of x_i+w_i <= x_j, x_j+w_j <= x_i, y_i+h_i <= y_j, y_j+h_j <= y_i must hold. These non-strict inequalities allow contact.

The area computation is exact:

sum from n=1 to N of 1/(n(n+1)) = 1 - 1/(N+1),

and sum from n=m to infinity = 1/m.

Since the open interiors are disjoint and the countable union of their boundaries has area zero, a full packing has complement of area zero. This does not assert that its union is closed or equals every point of the square.

**Consequence.** If the full problem has a negative answer in a chosen model, some finite prefix is already impossible in that same model. Knowing one enormous finite cutoff supplies none of the universal quantifier in Proposition 1. The missing ingredient is a proof for arbitrarily large cutoffs, not an additional limiting mechanism.

## Approach 2: finite axis-parallel feasibility has exact grid certificates

**Proposition 2.** A finite collection of axis-parallel rectangles whose dimensions lie in (1/D) Z, with either fixed orientations or right-angle rotations, packs in the unit square if and only if it has such a packing with all lower-left coordinates in (1/D) Z.

**Proof.** Start from any feasible real-coordinate packing and freeze its orientations. For each pair choose one satisfied non-strict separation inequality. Put the chosen horizontal inequality x_i+w_i <= x_j into a directed graph as the edge i -> j of weight w_i. Similarly put chosen vertical separations into a graph with edge weight h_i. Either graph is acyclic: summing inequalities along a directed cycle would require a sum of positive side lengths to be at most zero.

Add a source with zero-weight edges to every vertex. Set the new x-coordinate of each vertex to the largest weight of a source-to-vertex path in the horizontal graph. Define y similarly using the vertical graph. Path weights are sums of dimensions, so the new coordinates lie on the stated grid. Each selected inequality remains satisfied by the longest-path recursion. Every path weight to i was bounded above by the old x_i (respectively y_i), by summing the original inequalities and using the initial coordinate's nonnegativity. Thus the new coordinates are no larger than the original coordinates. They remain nonnegative and retain x_i+w_i <= 1 and y_i+h_i <= 1. Each pair retains its selected separation, giving a packing. The reverse implication is immediate. QED.

For R_1,...,R_N take D=lcm(1,...,N+1). This proves finite decidability and exact certificate sufficiency, not feasible running time and not existence at any unspecified N. The common denominator can be enormous. Arbitrarily rotated packings are not covered by this grid reduction.

## Approach 3: why an equal-area tail square cannot simply be inserted

Suppose one tries to combine a tail-square result with a finite packing by leaving one axis-parallel empty square H of side 1/sqrt(m), packing R_1,...,R_(m-1) outside its interior, and then placing the tail n >= m into H. This is a sufficient route if both parts exist in compatible models; a theorem concerning the tail alone does not construct the finite part.

**Proposition 3 (arithmetic obstruction to this splice).** For an axis-parallel finite prefix with right-angle rotations, such a square hole can exist only if m is a perfect square.

**Proof.** The prefix and H form a finite family of closed rectangles with pairwise disjoint interiors and total area 1. Their union must equal the closed unit square: its complement is relatively open, and any nonempty relatively open subset of a nondegenerate square has positive area. Choose a horizontal line strictly inside H and avoiding the finitely many horizontal tile edges. This line's unit interval is partitioned by the hole interval of length 1/sqrt(m) and finitely many tile intervals. Each tile interval has length either 1/n or 1/(n+1), hence rational. Therefore 1/sqrt(m) is rational. For a positive integer m this implies that m is a perfect square, by prime-factor exponents (or reduced fractions). QED.

The obstruction allows arbitrary real translations. It concerns one axis-parallel square hole and finitely many axis-parallel prefix rectangles; it makes no claim about arbitrary rotations, multiple gaps, or packings of the infinite sequence.

**Proposition 4 (the first nontrivial square index still fails).** R_1,R_2,R_3 and one 1/2 by 1/2 square cannot pack together axis-parallel in the unit square, although R_1,R_2,R_3 do pack there.

**Proof.** Rotate the entire arrangement if necessary so R_1 has width 1 and height 1/2. It spans the square horizontally. The hole cannot cross its interior, and it has height 1/2. Hence R_1 must lie against the top or bottom edge, leaving a 1 by 1/2 strip, in which the hole spans the full height.

If the hole is strictly between the strip's ends, it leaves two nonempty separated rectangular components. R_2 and R_3 cannot cross the hole, so each component must be filled by one rectangle. Both would need height 1/2, impossible for R_3. If the hole is at an end, the remaining component is a 1/2 square. A rectangle tiled by exactly two axis-parallel rectangles must be divided by a single straight horizontal or vertical cut; thus each piece spans a whole side. R_3 has neither side of length 1/2. This too is impossible.

For prefix feasibility, put R_1 at (0,0) with dimensions (1,1/2), R_2 at (0,1/2) with dimensions (1/2,1/3), and R_3 at (1/2,1/2) with dimensions (1/3,1/4). These are contained and interior-disjoint. QED.

The exact executable diagnostic independently enumerates all placements of these four pieces on the complete 1/12 grid, including both orientations. It finds no packing. Completeness for real translations follows from Proposition 2. This small obstruction refutes an automatic square-hole-completion inference; it does not refute Jiang's late-tail statement, whose range excludes m=4, or the original problem.

## Remaining gap and stopping point

No argument here produces packings for every prefix, proves a finite prefix impossible in the original model, or creates a compatible prefix around a sufficiently late tail square. For the one-square splice route, perfect-square m is only necessary, not sufficient; m=4 demonstrates the distinction. The threshold 10^1000 is itself a perfect square, so the arithmetic obstruction does not exclude all indices covered by the preprint.

The full question is left open. A promising next claim would need to supply a genuine uniform construction/finite-prefix theorem or a verified obstruction in the intended rotation model. More finite experiments, a single tiny positive area excess, or a tail theorem without a compatible prefix do not supply that missing claim. Three approaches were enough to expose these exact gaps, so no fourth or fifth speculative attempt was forced.

## Reproduction and evidentiary limits

Run `python verify_packet.py` or `python -O verify_packet.py` from any directory using the script's absolute path. The verifier checks the exact declared file inventory, bytes and SHA-256 values, then runs deterministic exact-arithmetic diagnostics and compares their full output with EXPECTED_DIAGNOSTICS.json. It uses explicit exceptions rather than disabled-under-optimization assertions. Hashes prove byte identity, not mathematical correctness. The external validation receipt records relocation and adversarial mutation tests. Independent review of the authored mathematics remains necessary.

No third-party PDFs, extracted source text, corpus records, private coordination, or raw connector responses are included in this safe packet. No GitHub or queue writes were performed by this investigation.
