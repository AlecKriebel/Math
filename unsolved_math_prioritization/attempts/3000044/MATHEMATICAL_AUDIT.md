# Independent audit: convex-set independent arborescences

Problem 3000044 / AMR-029-0044. Audit date: 10 October 2026. Public proof-only edition.

## Verdict and exact scope

**Analytic verdict: ACCEPTED AS A STRUCTURAL PARTIAL, after editorial precision corrections.** The unrestricted arbitrary-root/arbitrary-overlap conjecture remains unresolved. No target counterexample and no literature-novelty claim is accepted. This target is distinct from the rainbow-arborescence problem 30004008.

This audit is AI-assisted and unrefereed. Acceptance does not mean external human peer review, journal acceptance, or formal proof-assistant certification.

The accepted main implication assumes that every overlap between two indices with different roots has at most one directed vertex-sequence path between any ordered pair, after parallel arcs are collapsed. There is no restriction on overlaps between indices with the same root. Under this additional condition, the original simultaneous terminalwise independent-path condition, the stated local bipartite matching condition, and existence of coherent independent prescribed-set out-arborescences are equivalent. The base theorem, its arbitrary-local-choice conclusion, the stronger root-group reconstruction, the depth-at-most-two corollary, and the explicit greedy-prefix obstruction are analytically valid.

This verdict does not depend on any finite census or random search. The separate computation results are reproducibility and implementation evidence. They may be omitted from a proof-only edition without weakening the analytic verdict. They must never be presented as proof for arbitrary graph order, arbitrary number of trees, or unrestricted different-root overlaps.

## Inputs, provenance, and limited corrections

This edition binds the distributed [PROOF.md](PROOF.md): 20,551 bytes, SHA-256 `5586cc0e905fda93c8f25052c18558aaf314e9fd7f945d7c4c8b14fc3dfb50ad`. The complete mathematical statements, analytic arguments, examples, scope restrictions and algorithmic hypotheses are preserved from the corrected proof accepted by this audit.

The audit’s precision corrections explicitly distinguished the self-contained base theorem from the credited common-root refinement, and removed singleton tasks before invoking the common-root algorithm while checking weak connectivity and charging membership preprocessing. These corrections remain present. Public editorial changes update status and file names, remove private provenance, and distinguish historical computational observations from this edition. No new proof correction is introduced here.

The exact source target and its conventions were checked during the audit. A spanning-to-roots or merely arc-disjoint paraphrase is not substituted for the original simultaneous independent-path condition. The audit did not certify an exhaustive worldwide literature search. Edition preparation performed no new scholarly-source retrieval, source-file rehash, source inspection, literature search, or mathematical computation rerun.

## Primary-source inspection

The audit records reading the complete seven-page primary paper as extracted text and successfully reopening its public author PDF. PDF pages 1, 4, and 7 were additionally rendered locally and visually inspected during the audit; the web screenshot route failed and was not counted as an inspection. The recorded PDF identity is 232,496 bytes, SHA256 `d40a08b63338bc6137855424683eb3b6b43325880946e876eac6dcd0a5d5b04a`. No source PDF, extracted text, or page image is distributed.

Frank–Fujishige–Kamiyama–Katoh, *Independent arborescences in directed graphs*, Discrete Mathematics 313 (2013), 453–459: [DOI](https://doi.org/10.1016/j.disc.2012.11.006), [author PDF](https://andrasfrank.web.elte.hu/cikkek/FrankJ63.pdf). Question 2 is the originating prescribed-convex-set problem. Theorem 4 supplies common-root DAG existence; Theorem 5 supplies its O(km) algorithm for weakly connected graphs and non-singleton sets. Theorems 6 and 7 concern arbitrary roots with each vertex in at most two sets; Theorem 7 has the analogous algorithm assumptions. The common-root DAG and overlap-at-most-two cases are prior results, not current new work. Cyclic counterexamples do not settle this DAG problem.

## Detailed mathematical audit

### 1. Exact path and tree conventions

All graphs are finite loopless directed multigraphs with an acyclic orientation. Arc identities remain distinct even when endpoints agree. Prescribed sets contain their roots and are convex with respect to every directed path in the ambient graph. In a DAG, walks cannot repeat a vertex, so the walk/path formulation agrees away from the permitted length-zero root paths.

At a terminal v, every active index must participate in one simultaneous path system. Independence means arc disjointness plus precisely the allowed vertex intersection: v, and the common root when roots agree. Pairwise feasibility selected independently for different pairs would be weaker and is not substituted. Trees must have exactly their own prescribed vertex sets and consistent root paths at every terminal. Arc-disjoint packing alone is not used as a substitute for vertex independence.

Empty active sets, repeated roots, repeated prescribed sets, singleton sets, and root-terminal coincidence are compatible with the proof. A singleton task contributes its root and no arc. If a different-root path ends at that singleton root, the shared vertex is the permitted common terminal. If a positive path visits another active root before reaching the terminal, independence forbids it.

### 2. Necessity and local resources

A terminalwise path system supplies distinct final arcs. Equal penultimate vertices can occur only when that vertex is the common root. If a penultimate vertex t is an active root belonging to a different root group, the relevant path necessarily intersects that other group's path at t; because t differs from the terminal, this is forbidden. These observations justify both resource types and their allowed incidences exactly.

An ordinary tail is a single resource even when several parallel arcs enter v from it. A tail that is an active root offers one resource for each individual arc, exclusively to its own root group. Thus different root groups have disjoint available predecessor tails at each head, while repeated-root paths can use distinct direct parallel arcs. Convexity places every final-arc tail inside its relevant prescribed set. Zero paths are correctly excluded from J(v).

Every saturating matching assigns one admissible incoming arc to every nonroot occurrence. The acyclic predecessor graph for a fixed index must terminate at its unique indegree-zero vertex, namely the specified root. This proves exact-set rooted out-arborescences, without retaining the original terminalwise paths. The use of matchings at a common head proves global arc disjointness.

### 3. Self-contained base theorem

Suppose two constructed root paths share a forbidden vertex w before v. Both w-to-v suffixes have endpoints in both prescribed sets. Applying convexity separately to each set forces both suffixes into their intersection. For equal roots, neither suffix can return to the common root: it has already occurred earlier on the root-to-w prefix, and a return creates a directed cycle.

Consequently both suffixes lie in the stated X_ij. Uniqueness of vertex-sequence paths forces equal penultimate vertices, even when the final arcs themselves are parallel and different. The local matching rules allow equal penultimate vertices only at the common root, which has been removed from X_ij. This contradiction establishes vertex independence. It does not confuse vertex-sequence uniqueness with arc-identity uniqueness, nor require globally vertex-disjoint trees.

The necessity, sufficiency, and arbitrary independent matching-choice assertions are therefore valid under the all-pairs structural assumption. Hall's reformulation is immediate. The stated conservative matching time O(k²m+kn) is reasonable for membership-table input; structural-assumption testing is separately acknowledged.

### 4. Root-group pools and preservation of the local path condition

This is the substantive point in the stronger theorem, and was checked independently rather than inferred from arc-disjointness.

For a root r, the selected arcs assigned to that root group form H_r. Each group vertex is reachable from r through the initially assembled tree of an index containing it. Every nonroot v has precisely g_r(v) incoming pool arcs. Parallel pool arcs can leave only r: all other tails have a single ordinary resource, or belong exclusively to another root group and therefore cannot occur in this pool.

Fix v and let q=g_r(v), with d pool arcs directly from r to v. Then 0≤d≤q. Remove these d arcs, producing H'. If d=q, the distinct direct arcs are the required independent paths. Otherwise Menger applies to the now nonadjacent pair r,v.

If a separator S of size less than q−d existed, consider the vertices W with a path to v in H'. Every w in W other than r lies on an r-to-v path in the ambient DAG: concatenate its H_r root prefix and its H' suffix. A repeated vertex in this concatenation would form a directed cycle. Every prescribed set of this root group containing v also contains r, so convexity forces w into each of those q sets. Hence g_r(w)≥q.

Take the earliest topological vertex w in W outside S and r that is unreachable from r in H'−S. Such a vertex exists because v is unreachable. Any entering tail in H' also lies in W. A tail outside S must be r or an earlier reachable vertex, contradicting w's unreachability. Hence all entering tails lie in S. None is r, so they are distinct; the indegree is at most |S|. But its indegree is at least q when w differs from v, and exactly q−d when w=v. Both cases contradict |S|<q−d.

There are therefore q−d internally vertex-disjoint indirect paths; adding the d distinct direct arcs gives q independent paths. Distinct indirect paths cannot share an arc, and direct arcs have no internal vertices. Convexity places each path in every group set containing v, permitting its assignment to any of those q indices. At r itself only zero paths are needed.

Deleting arcs cannot introduce a new path that violates convexity. Restricting to the union of the group's sets loses none of their vertices. Thus the common-root existence theorem applies to H_r with precisely the same prescribed sets and multiplicities. This is a valid application of credited work, not an unproved presumption that arbitrary restrictions preserve feasibility.

### 5. Cross-root coherence after reconstruction

Common-root reconstruction uses only arcs in H_r. Different groups' arc pools are disjoint, and their incoming-tail pools at a fixed head remain disjoint. A reconstructed path may use an arc originally assigned to a different index of its own root group; this does not affect the argument.

For different roots, a shared vertex w before terminal v would again produce two suffixes entirely inside U_i∩U_j by ambient convexity. Unique vertex-sequence paths there force the same final predecessor at v. That predecessor cannot occur in two different groups' pools, giving the required contradiction. No uniqueness hypothesis is used for equal-root overlaps in this step or in the pool construction. Arbitrary equal-root diamonds and arbitrary overlap multiplicity are genuinely allowed.

The corrected algorithm paragraph now matches the source hypotheses explicitly. Removing singleton tasks changes no pool arcs; nontrivial pools are weakly connected because they are root-reachable. The recorded finite list-based implementation is not credited with the source algorithm's O(km) performance.

### 6. Corollaries and examples

The undirected-forest overlap case is immediate. Directed uniqueness is weaker than undirected acyclicity, so it is proper to allow some undirected cycles.

For the no-three-arc-path corollary, two distinct vertex-sequence paths from w to v would include one with at least two arcs. In X_ij, w cannot be the common root of the pair; at least one relevant root differs from w. The original hypothesis supplies a positive root-to-w prefix. Its concatenation with the longer suffix is a directed path, since a repeated vertex would create a cycle. This gives at least three arcs, contradicting the depth assumption. This reasoning covers repeated roots and parallel arcs.

The shared-chain family has convex prescribed sets because a path starting in a private branch or in the common chain cannot visit another branch. Pairwise overlaps are exactly the common chain. The private two-arc root-to-terminal paths are simultaneously independent for any number of roots. Chain length is unbounded. This demonstrates scope beyond common-root and multiplicity-two restrictions without asserting novelty.

The nine-vertex obstruction is valid: all sets are convex and the specified prefix trees are independent. If the first two trees use the same final predecessor, they share that predecessor; the two unequal predecessor choices force sharing a or b. The third tree must use e. Thus exactly four extensions of that fixed prefix are possible and all fail. Replacing the crossed prefix choices by consistent a-only/b-only choices supplies a valid full family. Therefore the example refutes arbitrary-prefix extension, not the original existence conjecture and not sufficiency of local matchings outside the structural class.

## Recorded implementation and computational-evidence audit

The independent audit records inspection of all construction programs and saved observations. Programs and raw observations are excluded from this proof-only edition; the analytic acceptance requires none of them. The model explicitly enforces topologically labelled DAGs; distinct arc indices encode parallel arcs. The exact solver enumerates finite path systems and backtracks parent choices across terminals. Its failure-without-limit is exhaustion, while an explicit search limit raises an unknown-result exception. The witness checker reconstructs all paths and compares allowed vertex intersections and arc intersections. Its correctness still presumes the caller separately checks ambient convexity; that precondition is met in the reported enumerations.

The convex-set enumeration selects nonempty sets whose least vertex reaches all their vertices. For any feasible prescribed set in a forward-labelled DAG, its root must be its least vertex, so this loses no feasible rooted sets. Unordered triples with repetition remove only index permutations. The computation deliberately restricts its coherence census to not-all-equal roots with a three-way intersection. The common-root and multiplicity-at-most-two cases are credited analytically rather than silently counted as newly checked residual cases.

The common-root implementation chooses a direct root arc when present; otherwise it chooses the predecessor earliest in its auxiliary forward order and inserts the new vertex immediately after that predecessor. Other residual arcs point backwards in this order. This matches the credited eligible-tree construction after reversing the paper's order. Its deletion of vertices no longer present in remaining sets cannot remove an incoming arc needed by a surviving set: a root-to-that-head path through such a tail would contradict convexity. Parallel nonroot pool arcs never arise under the local matching rule.

The audit records that normal and optimized theorem replays both passed with the recorded counts. The obstruction and 2,000 equal-set mixed-root stress cases passed. All supplemental seeded searches reproduced their reported counts, including the eleven layered backtracking cases and 2,286-node maximum. The independent semantic oracle’s aggregate final counts are retained in [ACCEPTANCE.json](ACCEPTANCE.json). Its recorded DFS paths, convexity test, local-path selection, and backwards parent verification did not call the construction’s semantic checker. The constructors and coherent search were treated as code under test.

No complete population of sampled instances or every witness was originally saved, and this is accurately disclosed. The audit’s recorded seeds and source code supported replay at review time but are not distributed here. A failed or interrupted intermediate audit run is not evidence: only completed final runs counted. Edition preparation did not rerun the mathematical computations. Mathematical negative controls include shared/missing arcs, root conflicts, absent parallel capacity, nonconvexity, forbidden diamonds, and all four bad greedy-prefix extensions. Their rejection validates boundaries; it does not prove unrestricted nonexistence.

## Remaining limitation and actions

The unresolved case allows different-root overlaps with alternative directed paths. The accepted proof does not establish that all local matchings suffice there, nor that the original conjecture is false there. No global novelty or current-worldwide-open certification is made.

The original mathematical audit performed no publication or queue update. This proof-only edition preserves its analytic verdict and supplies authored analysis with public bibliographic and recorded verification metadata. It excludes programs, raw outputs, datasets, copied third-party source text, PDFs, images, and private coordination material. This edition changes no queue entry.
