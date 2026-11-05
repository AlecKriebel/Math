Editorial note: Complete authored proof or audit prose is preserved below. Only operational artifact identities, byte counts, locations and obsolete replay directions have been replaced; all mathematical arguments, finite scopes and limitations remain. The public manifest identifies the actual distributed edition.

# Independent audit: clique-boundary flexibility and high-incidence core

## Decision and scope

**ACCEPTED as all-size structural partial results, including the separately frozen high-incidence-core addendum. No mathematical correction to either frozen proof is required. The unrestricted odd-hole-free division conjecture remains unresolved.**

A division colors the vertices of a finite simple graph with two colors so that every maximum clique meets both colors. Maximum is not interchangeable with inclusionwise maximal. The audited theorems concern clique number k at least three, count distinct maximum cliques in the original graph, and require no odd-hole-freeness assumption. Necessary conditions below are not sufficient conditions or a counterexample construction. No novelty claim is made.

The primary [clique-boundary-flexibility proof](BOUNDARY_EXTENSION_PROOFS.md) was checked against its separate external pin and complete original manifest. Its exact original identity was verified before review and preserved privately; the distributed proof edition is inventoried in this edition's public manifest.

The later, separately sealed [high-incidence-core addendum](HIGH_INCIDENCE_CORE_PROOFS.md) belongs to this same third pass and does not change the primary packet. Its external pin, manifest and complete proof identity were independently checked, and its dependency identity matches the checked primary pin.

This audit independently examines the all-size arguments, independently enumerates the stated finite universes, compares the author's exact visited cases, validates returned witnesses against separate Boolean oracles, and tests failure controls. It edits neither frozen input packet, makes no remote or queue changes, and begins no further research round.

## 1. Exact mixed-constraint characterization: accepted

The edge family may have repeated labelled occurrences, each counted toward vertex incidence. Every edge has at least two distinct vertices, and every vertex belongs to at most two occurrences. A B demand requires both colors; a one-sided demand forbids one monochromatic color.

An all-B odd-cycle component is necessarily unsatisfiable, since each size-two edge demands distinct endpoint colors. Conversely, a pure odd cycle containing any one-sided constraint is satisfiable: omit that constraint, alternate along the remaining even-length path, then globally swap the two colors so the equal-colored endpoints avoid its forbidden color. All other edges are bichromatic. Other one-sided demands, including opposing forbidden colors on different edges, cause no conflict because those other edges meet both colors.

For every remaining component the dual multigraph proof is valid. Each hyperedge occurrence is a real vertex, and an original vertex of incidence two supplies an edge between two distinct real vertices. Incidence-one vertices supply edges to the auxiliary vertex z. Thus there are no dual loops, but parallel edges are allowed. The original real degrees equal the hyperedge sizes. Adding one edge from every odd-degree real vertex to z makes all degrees even, including z.

When z is nonisolated, an Euler circuit starting at z gives balanced arrival/departure pairs at every real vertex, even if the circuit length is odd. Original degree-two real vertices retain one edge of each color. Odd original degrees are at least three, so after their one added edge is removed they still retain both colors. When z is isolated, all original degrees are even and no edge will be removed. Starting at a degree-at-least-four real vertex handles an odd circuit: its two color counts are d/2+1 and d/2-1, both positive. All other real vertices remain balanced. If every real degree is two, the connected loopless multigraph is a cycle; a parallel-edge two-cycle is even, and the odd case is precisely the exception already handled.

Connectivity of the original edge-intersection component ensures that this construction has only the relevant Euler component, apart from an isolated z. Empty families and isolated original vertices impose no conditions. Repeated identical two-edges form an even two-cycle rather than an omitted obstruction. These observations establish both directions of the characterization, not merely a sufficient condition.

## 2. Abstract precoloring and its sharpness: accepted

If all original edges have size at least r, r at least three, and at most r-2 vertices are prescribed, every unsatisfied residual edge has size at least two. Residual incidences outside the prescribed set cannot increase. Every residual size-two edge necessarily lost a prescribed vertex, so its demand is one-sided. Consequently an all-B size-two odd-cycle component cannot occur, and the exact mixed lemma supplies an extension.

The proof permits unrestricted incidence within the prescribed set, nonuniform original edges, empty families, and repeated labelled edges with incidence counted accordingly. It does not silently assume that residual edges stay distinct: distinct original edges can produce equal residual sets, and the mixed lemma already covers those repeated occurrences.

The sharpness example with a monochromatic set P of size r-1 and r additional vertices V is correct. Each edge P union {v} forces its v to the other color; the remaining edge V then fails. Each outside vertex has incidence exactly two, while an unrestricted mixed coloring of P and of V satisfies the family. Its shadow is the complete graph on 2r-1 vertices, so these r-edges cannot all be maximum r-cliques in any graph realizing their pair incidences. The example establishes sharpness of the abstract precolor-size bound, not a graph counterexample.

## 3. Every admissible clique-boundary coloring extends: accepted

If both boundary color classes have size at most k-2, discard the maximum cliques already meeting both colors. Every remaining maximum clique meets the boundary in one color and therefore loses at most k-2 vertices. This leaves at least two uncolored vertices. A residual B edge lost no vertex, so still has size k at least three; every size-two residual edge is one-sided. The mixed lemma applies. This covers an empty boundary, a proper monochromatic boundary of size at most k-2, and mixed boundaries up to size k whenever neither class has size k-1.

The only remaining case is a color class P of size k-1. There is at most one such class because k is at least three and the boundary is a clique of size at most k. Its common open neighborhood F is disjoint from P and stable: two adjacent members of F together with P would be a clique of size k+1. Every member of F is genuinely forced to the opposite color by the maximum clique P union {v}. Every originally prescribed boundary vertex outside P belongs to F and already has that opposite color, so the new prescriptions are consistent.

The stable-neighborhood step eliminates the potentially dangerous singleton residuals. A maximum clique meeting both P and F is already satisfied. A remaining clique disjoint from P meets F at most once and thus leaves at least k-1, hence at least two, uncolored vertices. A remaining clique meeting P is disjoint from F; it cannot contain all of P, since its last vertex would then be in F. It therefore loses at most k-2 colored vertices and again leaves at least two uncolored vertices. All still-uncolored vertices are outside the original boundary, so retain incidence at most two. Every size-two residual is still one-sided. The mixed lemma completes the extension.

This proves the theorem for every admissible clique boundary, including a maximum clique with a k-1 versus 1 coloring. No assumption about induced odd holes occurs anywhere. The abstract sharpness construction fails exactly where this proof uses the stable common neighborhood.

The clique-number threshold and the clique-boundary hypothesis are substantive. Independent scope controls exhibit the indivisible five-cycle at k=2 with empty boundary. They also exhibit a nine-vertex graph with a central triangle and one private two-vertex triangle attachment at each central vertex. The six private vertices form a nonclique boundary containing no maximum clique; coloring them all red forces all three central vertices blue. Each outside vertex belongs to exactly two maximum cliques, yet extension fails. This control does not satisfy the theorem's clique-boundary assumption.

## 4. Primary structural corollaries: accepted

Let X be the set of vertices belonging to at least three distinct maximum cliques. If X were a clique, it would have an admissible coloring: any coloring if its size is less than k, and a mixed coloring if its size is k. The boundary theorem extends that coloring. Thus any indivisible graph with k at least three has a nonedge within X, giving two nonadjacent high-incidence vertices.

For a separator side of local clique number k at least three, forbidding even one admissible clique-boundary coloring therefore requires a high-incidence vertex outside the boundary, with incidence counted in that side. A side whose clique number is below the global maximum-clique threshold imposes no constraint at that threshold. The equal-only and different-only size-two-boundary conclusions at k=4 are valid necessary restrictions. They neither construct a forcing side nor establish general compatibility of separator sides.

## 5. Separately frozen high-incidence-core addendum: accepted

### Proposition A

Let P contain X, and prescribe a coloring with no monochromatic (k-1)-clique. Every maximum clique not already satisfied meets P in a monochromatic clique of size at most k-2. Its residual therefore has at least two vertices. Vertices outside P have incidence at most two; a B residual has original size k; and a size-two residual is one-sided. The mixed lemma applies exactly as claimed. In particular, if the clique number of G[P] is at most k-2, every coloring of P extends, even when P is a large nonclique.

### Corollary B

For an indivisible graph, the following necessary conditions all follow:

- The clique number of G[X] is at least k-1, or Proposition A would extend every coloring of X.
- X is not a clique, by the full clique-boundary theorem.
- The chromatic number of G[X] is at least 2k-3. Otherwise a proper coloring with at most 2k-4 colors can be divided into two groups of at most k-2 proper color classes. Each resulting color has clique number at most k-2, and Proposition A extends.
- The size of X is at least 2k-2. Up to 2k-4 vertices can be split into color classes of size at most k-2. At the remaining order 2k-3, select a nonedge inside X and include its endpoints in a class of size k-1; the other class has size k-2. The first class is not a clique and hence also has clique number at most k-2. Proposition A again extends.

The last bound uses the nonedge conclusion; it is not just a rearrangement of the numerical clique and chromatic bounds. At k=4 these conditions give at least six high-incidence vertices, induced chromatic number at least five, induced clique number at least three, and noncompleteness. The statements remain necessary, not sufficient.

### Corollary C and the minimality convention

The addendum explicitly defines minimal indivisibility using proper nonedgeless induced subgraphs and their own clique numbers. This avoids the singleton-maximum-clique trap. If X is the whole vertex set, it plainly contains a maximum clique. If X is proper and has clique number at most k-1, then an edgeless G[X] has any coloring with color-class clique numbers at most one, which is at most k-2. Otherwise induced minimality supplies a division of G[X] at its own clique number t, making both color-class clique numbers at most t-1, hence at most k-2. Proposition A extends either coloring, a contradiction. Therefore X contains a maximum k-clique. This does not claim that X itself is a clique, or that an arbitrary induced-minimal subgraph retains the original graph's clique number.

## 6. Independent finite universes and witnesses

The mixed audit independently enumerates by family cardinality and combinations with replacement, rather than using the author's capacity-pruned recursion. A family has at most n edges because each edge has size at least two and the total vertex incidence is at most 2n. Every multiset of each allowed cardinality is examined and retained precisely when its incidence bound holds. This gives all 1,910 multisets on labelled orders zero through five and every positional assignment of B, 0, or 1, for 72,348 demand-labelled cases. Exactly 147 are unsatisfiable.

An independent full-coloring oracle and a separate component-obstruction test agree on every case. The author's constructor agrees with both, and every returned coloring is independently verified. Instrumentation compares the exact canonical case set, retaining the order of demands on identical repeated copies; no case is missing or repeated. The audited universe includes 2,936 demand-labelled cases with opposite one-sided demands on repeated identical edges, and 6,414 colorable cases that would be obstructed if every demand were changed to B.

The graph audit independently reconstructs cliques by testing all pairs in each subset. All maximum-clique lists, all clique lists, and clique numbers agree with the authored routine for all 33,868 labelled simple graphs of orders zero through six. For every eligible graph-boundary pair, an independent full-coloring oracle verifies all admissible boundary restrictions. Instrumentation compares the exact set of graph, boundary, and prescribed-pattern triples used by the author, not just totals. There are 400,508 eligible boundary pairs and 1,593,435 colorings. The almost-monochromatic common-neighborhood branch occurs 631,800 times; coverage also includes 19,947 empty-boundary pairs and 51,413 maximum-clique-boundary pairs.

The independent graph-case stream is encoded as decimal n, graph mask, boundary mask, and full-vertex color mask separated by commas and a newline. Its encoding differs from the author's JSON stream, so equality is established by exact case-set comparison rather than equating unlike digests. The author's own mandatory stream hashes are separately reproduced by its complete replay. These undistributed stream identities are omitted from this prose edition.

Additional independent checks cover all 2,457 assignments of the three demands to odd cycles of lengths three, five, and seven; all 27 demand assignments in an odd-length Euler component with real degrees 4,4,2 plus an isolated vertex; 2,441 abstract precolor-lemma cases in simple uniform families through order five, including 238 with a high-incidence precolored vertex; and repeated uniform-edge precolor examples at ranks three, four, and five. The authored odd-cycle fixtures of lengths three, five, seven, and nine and abstract sharpness fixtures at ranks three, four, and five are also replayed.

The generalized nonclique prescribed-set special case is checked on 23,897 colorings through graph order five, including 15,328 nonclique-boundary cases. The full addendum Proposition A is separately checked on 51,981 prescribed-color cases through order five, including 34,936 nonclique cases and 1,136 cases prescribing all vertices of a maximum clique. These are precisely bounded finite regressions; the addendum's universal statements and numerical necessary conditions are justified by their all-size proofs, not by these small graphs.

## 7. Optimization-resistant execution and integrity controls

The independent main replay, supplemental maximum-clique/scope replay, and addendum replay each pass under normal Python, -O, and -OO with identical outputs within each family. No acceptance gate uses Python assertions. Exact replay-output identities were checked and retained with the original audit; those undistributed-output identities are omitted from this prose edition.

Independent native lstat checks reject symlink path components, verify regular-file types, require the exact inventory, and check both the fixed external-pin identity and the fixed manifest identity before inspecting payloads. The addendum receives its own separate identity/dependency check. Every hostile mutation is confined to temporary writable copies; the read-only authored originals are rehashed afterwards.

The main independent control suite rejects 36 distinct mutations under each of normal, -O, and -OO, for 108 rejections. These cover removal, tampering, and symlink substitution of every packet member; missing, changed, and symlinked external pins; extra files, directories, and symlinks; wrong checker origin; missing mandatory arguments; root and ancestor symlinks; a pin placed inside the packet; duplicate JSON input keys; missing or changed mandatory inputs; changed fixture scope; and incorrect or missing expected results and coverage hashes. Semantic input/expected-result mutants are re-manifested and re-pinned inside their temporary copies so that they exercise semantic rejection rather than merely stale payload hashes.

The independent addendum suite rejects 13 distinct missing, changed, symlinked, or unexpected-file mutations under each Python mode, for 39 rejections. The author's primary terminal receipt was verified: every evidence member it names was independently rehashed, and its 31 negative controls per mode were checked. The author's primary executable outputs agree byte-for-byte with the independent direct executable replays. The later author addendum terminal receipt was also verified, including every evidence member and its 16 integrity controls per mode. That author addendum receipt is integrity-only; the independent all-size proof acceptance, 51,981 bounded mathematical cases, and 39 hostile-control rejections are recorded separately here. Both terminal receipts and their distinct scopes were checked; omitted receipt and output identities remain outside this public edition.

These checks certify the pinned static artifacts and the specified failure modes. They do not establish resistance to concurrent hostile filesystem races, every malformed input representation, or coordinated replacement of all trusted external anchors. Finite tests are a supplement to mathematical proof, not a substitute. No external theorem or literature priority claim is needed for this acceptance.

## Conclusion

The frozen primary proof and separately frozen high-incidence-core addendum are accepted at their stated scopes. The residual singleton issue, simultaneous one-sided requirements, repeated residual edges, odd Euler circuit parity, mixed and almost-monochromatic maximum boundaries, empty boundaries, graph realizability, and induced-minimality convention have all been explicitly checked. The resulting theorems significantly constrain a potential indivisible graph and a potential boundary-forcing separator side. They do not resolve the unrestricted odd-hole-free division conjecture.
