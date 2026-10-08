# Independent acceptance audit: shortest paths in line arrangements

## Decision

**Accept the frozen packet as correct partial mathematical work, with the source/output clarification below. The general target remains unresolved.** No proof establishes an exact subquadratic algorithm from implicit line equations, and no proof establishes a quadratic lower bound for unrestricted algorithms. No novelty or priority claim is accepted or needed.

The accepted input is identified by `INPUT_PINS.json`. Its manifest has SHA-256 `72d1f923599313b4f16be9505587277ac47aa232293972a7ef9737f99b82c23c`. The report has SHA-256 `bcd9f1b7e1db3e5add9db270adba50fc68fac1f94dc032979d6172b690f8dde7`, and the verifier has SHA-256 `842c4114b5440b68a11a6f948f3662aaedea9acde903c6814e6aeddc6d857903`. All seven input files were preserved byte-for-byte. The existing correction distinguishing the two-edge hop witness from the other one-bend route is accepted and must remain with the packet.

This audit covers the complete report and verifier, the source inventory and obtainable public-source evidence, fresh execution, independent exact geometry, and targeted semantic mutation tests. It adds no sixth proof-search route. It makes no repository or queue change.

## 1. Model and scope

The proofs correctly concern distinct complete affine lines, with equal Euclidean travel cost and no deleted portions. Coincident descriptions must be merged. Vertices are geometric points incident with at least two distinct lines, and graph edges join consecutive distinct vertices on one line. Concurrence gives one vertex; it does not create zero-length edges. Parallel lines, coincident input descriptions, concurrence, and identical endpoints are handled without an implicit general-position assumption.

The report correctly separates three outputs: distance, maximal straight runs, and all arrangement edges in order. It also separates implicit line equations from a preconstructed quadratic graph. Its real-RAM convention explicitly permits exact comparison of accumulated Euclidean lengths. This is not a bit-complexity result for arbitrary sums of square roots. The verifier intentionally covers only rational coordinates and rational lengths from Pythagorean directions.

Existence of a shortest path follows from a finite graph with positive edge lengths. With finite vertices present, all input lines belong to the connected union: two nonparallel lines are present, and every other line intersects at least one. An unbounded-ray excursion cannot improve a finite-vertex route. The elementary explicit algorithm has the claimed O(n² log n) real-RAM cost. The faster quadratic construction/planar-shortest-path result is imported historical context, not an implementation or independently re-proved algorithm in this packet.

## 2. Route-by-route mathematical audit

### Route 1: connected line intersections and the sharp edge bound

**Accepted.** The decisive fact is about every input line, including a line merely crossed by the path. If two points of a geodesic lie on one input line, the intervening subpath must be the monotone straight segment between them. Otherwise replacing it by that allowed segment strictly decreases Euclidean length. The equality condition in the triangle inequality excludes both off-line detours and on-line reversal. The conclusion applies to every shortest path, even when shortest paths are not unique.

For the incidence-sensitive bound, consider arrival at each path vertex along its incoming support line. Every other incident line is new: a previous encounter would force the intervening path onto that line, contradicting the nontrivial incoming edge's distinct support. Initially there are |I(s)| encountered lines; the q−1 internal vertices introduce at least one each; the terminal vertex introduces |I(t)|−1. The counted sets are disjoint, so

n ≥ |I(s)| + q−1 + |I(t)|−1,

and therefore q ≤ n−|I(s)|−|I(t)|+2 ≤ n−2. Endpoint concurrence strengthens this bound. The argument also works when s and t share a line; that shared support is the already encountered incoming line at t. The empty-path case s=t is correctly excluded from this incidence formula.

The horizontal line with n−1 vertical crossings proves sharpness for the fully expanded edge list. The stronger theorem rules out a quadratic output-size argument even for straight-through intermediate vertices. It does not provide a way to discover the unknown linear-size path in subquadratic time. The proposed O(nq) feasibility/expandedness check verifies a supplied route and its length, not its optimality; the report does not claim otherwise.

### Route 2: half-planes, ellipses, and ordinary A*

**Accepted.** Crossing out of a closed half-plane containing both endpoints and then returning would violate connected line intersection. If both endpoints lie on its boundary, the geodesic is their common-line segment. The ellipse condition follows by applying Euclidean lower bounds to the two portions of a shortest path, using any feasible upper bound U.

For the (m+1) by (m+1) orthogonal grid, n=2m+2, the exact distance is 2m and the common-side corridor is the entire square. The sum of the two focal distances is convex; all square corners have value at most 2m. Convexity therefore puts the full square, and all (m+1)² vertices, inside the ellipse even with U equal to the optimum.

At vertices i<m and j<m, the strict inequality √(a²+b²)<a+b for a,b>0 gives exact optimal A* priority below 2m. Consistency ensures every such vertex is settled before the target under ordinary minimum-priority vertex expansion, independently of tie-breaking. Thus the m² count is correct. It is a lower bound for this specified A* procedure and for explicit survivor enumeration, not a lower bound for all algorithms, other heuristics, or symbolic batching. The family is itself easy using its two directions.

### Route 3: the relaxation, the exact two-direction case, and the five-line obstruction

**Accepted.** Collecting signed directional displacement gives the relaxation lower bound. The polar inequalities |z·u|≤1 certify its dual bound, and the polygonal unit ball explains the existence of a relaxed optimum using at most two directions. This says nothing about whether the necessary translated lines exist.

With exactly two independent directions, basis-coordinate variation gives |α|+|β|, attained by the source's first-direction line followed by the target's second-direction line. The compressed path or its distance is available after a linear scan of unsorted line input. Ordered expanded edges can require sorting; this distinction is essential.

For the five-line fixture, independent graph construction and Bellman–Ford reproduce the true optimum 21. The two feasible one-bend corners both cost 65/3. The source and target incident lines rule out all other one-bend forms. The edge theorem bounds a geodesic by three edges; a genuine three-run optimum can only have E as middle support. Its four possible support sequences have lengths 21, 30, 39, and 48. Longer candidates that cross extra vertices cannot introduce an omitted better route.

The corrected two-edge hop witness is C∩D=(79/7,209/21). In contrast, the A∩B route crosses E twice and has four arrangement edges despite only one bend. Both have length 65/3. The packet's explicit correction and adjacency regression tests preserve this distinction. The true Euclidean optimum has three edges, so the two optimization criteria differ on this fixture.

The dual vector (1,1/5) satisfies all three unit-direction inequalities and has value 91/5 on displacement (18,1). The displayed primal decomposition attains that value exactly. Thus 91/5 < 21 < 65/3 is a valid strict separation between relaxation, optimum, and one-bend optimum.

### Route 4: exact distance envelopes

**Accepted.** A path arriving at a nonvertex point on a line first enters at an arrangement vertex, unless the source already lies on the line. Its length is at least the known-distance-to-entry term plus the straight-line distance from entry to destination. Conversely, that concatenation is feasible. This establishes the lower-envelope recurrence, including the direct-source term.

Distances on a line are 1-Lipschitz, but a lower envelope of convex V-functions need not be convex. Independent exact distances in the four-line fixture are 5,6,5 at consecutive positions −4,0,4, so the midpoint convexity inequality fails. The three ingress sites produce the report's exact profile. The O(r) prefix/suffix-minimum method is correct after sorting and after global site labels are known. Those unknown global labels are precisely why the recurrence alone is not a shortest-path algorithm. The report properly avoids a universal quadratic lower bound on envelope size.

### Route 5: sorting and output counting

**Accepted with its declared restrictions.** The horizontal sorting construction has one unique geometric geodesic and a length independent of input order. Its fully expanded ordered edge list reveals the sorted positions. In the comparison-sorting model, distinguishing m! label orders takes Ω(m log m) comparisons. The reduction proves nothing about the compressed answer or distance on that family, and it is not a reconstruction of the historical convex-hull-size-verification lower bound.

The O(n)-vertex theorem allows a discrete path to be encoded by O(n) pairs of line identifiers. Counting these encodings gives only O(n log n) bits. As the report expressly notes, this does not upper-bound algebraic decision-tree complexity: one output can have disconnected realization regions, and numerical predicates or exact values can carry further difficulty. Neither arrangement size nor this counting argument supplies the missing quadratic lower bound.

## 3. Source normalization and a nonblocking clarification

The historical page and its parent index were inspected in full retrieved HTML. The page asks about arrangement vertices and states a convex-hull-verification lower bound, but gives no modern output/bit-model specification. Its parent warns about stale status. The report correctly refuses to use it as proof of present-day openness. [Problem page](https://jeffe.cs.illinois.edu/open/algo.html#shortpath), [index warning](https://jeffe.cs.illinois.edu/open/).

Both four-page 2003 papers were read in text extraction; their first pages were also visually checked. Their grid-like two-pencil hypotheses require cross-pencil intersections on the same side of the center-joining line, with the designated opposite corners as endpoints. The boundary-route theorem is correctly attributed. Hart mentions a broader extension but omits its details; the packet appropriately does not depend on it. [Hart](https://www.cccg.ca/proceedings/2003/48.pdf), [Kavitha–Varadarajan](https://www.cccg.ca/proceedings/2003/17.pdf).

There is a genuine source-level discrepancy worth preserving rather than silently resolving: Hart's page 2 summarizes the k-orientation bound as O(n log k+k²), while Kavitha–Varadarajan's page 1 and Eppstein's bibliography state O(n+k²). The full 1999 paper was not inspected, so this audit cannot certify its grouping or output conventions. The frozen report's explicit bibliography-only attribution and conservative O(n log n) preprocessing allowance are safe. [Author bibliography](https://ics.uci.edu/~eppstein/pubs/geom-path.html).

Two independent issues must remain separate:

1. Input preprocessing: identifying/grouping orientations or merging duplicated descriptions may require sorting under an unsorted comparison input convention.
2. Output reporting: even already identified two-direction families can require sorting if the output must list every intervening edge in geometric order. Proposition 7's family demonstrates this independently of orientation grouping.

Consequently none of the imported linear or O(n+k²) summaries should be read as establishing a linear algorithm for the expanded ordered output on arbitrary unsorted inputs. The elementary two-direction length/compressed-path result remains linear. The structural theorem is independent of every imported complexity estimate. `CLARIFICATION.patch` is an optional additive wording refinement for this issue; it does not repair a failed proof or alter the accepted original.

The UBC catalogue and deposited DOI metadata establish the 2020 thesis identity. The deposited abstract says its author did not improve the general exact bound and studied approximation. Only that abstract, not the full thesis, supports the corresponding statement here. The stored landing page is a security-block response; no thesis PDF was inspected and no theorem, approximation constant, PDF hash, or PDF size is certified. [Catalogue](https://www.cs.ubc.ca/cs-theses/cs-theses-2020), [DOI metadata](https://api.datacite.org/dois/10.14288/1.0389809).

Fresh title/subquadratic searches during this audit found the same historical results and no general settlement. This is bounded negative evidence, not a current-openness theorem. The independent web reader failed on the index/DOI metadata and PDF screenshots; the already retrieved hash-matched HTML/JSON and local PDF page renders were inspected instead. No access restriction was bypassed. `SOURCES_AUDIT.json` records the byte-hash comparisons and inspection depth without redistributing source documents.

## 4. Executable audit

The complete 310-line verifier was reviewed. Its intersection formulas, canonical integer-line normalization, rational square-root guard, sorted per-line consecutive adjacency, Dijkstra, and Floyd–Warshall implementations are consistent. Global lexicographic point order is monotone on each nonvertical line and uses y-order on vertical lines. Coincident intersections are deduplicated before creating strictly positive edges. All correctness checks use explicit exceptions and remain active under optimization.

The frozen verifier was rerun with isolated Python and disabled bytecode writes in normal, -O, and -OO modes. Every run exited zero, reported 6,531 ordered distance queries, seven grid cases, and 120 sorting permutations, and demonstrated real/effective UID 1000 with both append-open and directory-create probes rejected by the operating system. Permissions were files 0444 and directory 0555. This demonstrates denied writes under those permissions, not an adversarial immutable-filesystem guarantee. All seven input hashes matched before and after.

Dijkstra and Floyd–Warshall in the original share a graph builder. Agreement alone would not catch a common geometry error. The supplemental `independent_checks.py` therefore uses different constructions:

- line intersections by substitution rather than the original determinant expression;
- pairwise endpoint adjacency, rejecting an edge when any vertex lies strictly in its interior, rather than sorting each line;
- layered Bellman–Ford shortest distances, rather than a heap or Floyd recurrence;
- enumeration of every shortest-path DAG route in six small fixtures, including tied paths;
- exact translation, quarter-turn, and scaling tests;
- independent primal/dual and one-bend calculations, plus targeted invalid-path rejection.

These checks compare 36 arrangements and 7,828 ordered distances, including 300 transformed distance queries. The six all-tie fixtures yield 890 shortest paths, counting trivial paths. All satisfy line-intersection connectedness, the incidence-sensitive edge bound, and the endpoint half-plane restrictions. The audit deliberately uses a different random seed from the original. The supplemental suite passes in all three optimization modes. Finite rational evidence does not establish correctness on arbitrary real input or enumerate ties in all possible arrangements.

The semantic mutation harness operates only on temporary copies. Six corruptions are rejected by the original tests in all three modes: taxicab edge cost, allowing edges to skip vertices, replacing Euclidean weights by hop weights, dropping reverse adjacency, resurrecting the obsolete hop witness, and making the edge bound one too strong. Two weakening mutations, disabling either structural check, survive the original positive examples. The supplemental adversarial tests detect both. The negative paths use real arrangement edges and truthful total costs; a remote extra line lets the repeated-crossing test reach the connected-intersection check without first exceeding its incidence bound.

This is meaningful but deliberately limited mutation coverage. In particular, the original generic `require(False)` check only certifies that explicit guards execute; it is not by itself a semantic test of geometry. `AUDIT_VALIDATION.json` records observed mode-by-mode results, including surviving original-suite mutants rather than concealing them.

## 5. Acceptance and remaining obligations

Accepted: all five partial routes, the sharp edge bound, exact counterexamples, metric/output separation, preserved hop correction, finite verifier, and qualified historical/source claims. No mathematical proof patch is required. The optional clarification and supplemental tests improve interpretability and regression coverage.

Not accepted as established: a solution to the general target; any quadratic lower bound for unrestricted implicit-input algorithms; an unqualified 2026 openness claim; bit-polynomial comparison of arbitrary sums of radicals; a complete inspection of the 1999 paper or 2020 thesis; exhaustive tie testing beyond the listed finite fixtures; or novelty of the elementary arguments.

The proper final classification remains **unfinished after five routes, with independently accepted partial results**. Publication of an acceptance packet must retain the model restrictions, source limits, original correction, and unresolved status. Only authored audit text/code and public verification metadata belong in that packet. Third-party PDF/HTML/JSON contents, datasets, private coordination, and identifying environment metadata are excluded.
