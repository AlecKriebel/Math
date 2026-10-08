# Independent audit of KP 2 28 type preserving RAAG embeddings

## Conclusion

**Accept the mathematical packet as partial and unresolved after five substantive routes. Require the separately supplied verifier correction for optimization-safe, read-only reproduction.** No error was found in the authored Schottky construction, graph criterion, selected support-model obstruction, cycle-cover obstruction, free-target obstruction, or finite-cover argument. None resolves the general existence question or supplies a counterexample to every embedding.

The frozen report is not modified by this audit. The original seven-file edition has manifest SHA-256 `00949c87a3adfa815c55af7b95df7e72da00ca64f382f401c0ca97f3ba0c7f19`, 1,198 bytes. Its six listed payload files all match their advertised hashes and sizes. `ORIGINAL_FREEZE_RECHECK.json` records the independent comparison. The audit also rechecked the original after execution tests; all seven files remained unchanged.

The concrete verification defect is consequential but does not invalidate the written proofs: the original verifier contains 15 Python `assert` statements. Python optimization removes all 15. Deliberately false graph, cycle, word, matrix, and clique specimens all returned `all_checks_passed: true` under both `-O` and `-OO`. The corrected verifier uses explicit always-active conditions, preserves the mathematical tests and result schema, and provides stdout or an explicit output destination.

## Audit boundary and source identity

The full original `RESEARCH_REPORT.md`, `LITERATURE_AND_SCOPE.md`, `verify_exact.py`, both manifests, README, and frozen results were read. The report's mathematical arguments were checked independently. A second implementation was written without importing the original checker.

Six locally available public-source PDFs were hashed independently and match the source manifest, including the 6,578,041-byte K3 book and the 521,624-byte published Runnels article. Fresh PDF-to-text extraction of all five article PDFs matches the text inspected in the audit. These identity checks are recorded as metadata only in `SOURCE_IDENTITY_RECHECK.json` and `SOURCE_EXTRACTION_RECHECK.json`. No PDF, page image, extracted passage, dataset, or private coordination file is included in this audit packet.

The K3 problem pages 108–109 were visually inspected, and page 84 was read from the pinned PDF. Their conventions support finite generating graphs, oriented finite-type surfaces, and pointwise boundary fixing when boundary is present. The intended map is a homomorphism: the adjacent embedding discussion rules out treating an arbitrary set injection as a mathematical solution. The theorem must concern every loxodromic element simultaneously. [K3 source](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf)

The full Runnels thesis was not available among the audited PDFs. A fresh web retrieval also failed. The packet's prior report of HTTP 403 is retrieval history, not an inspected thesis proof. The located thesis announcement remains a novelty/scope warning only; it is not used to certify existence for any family in this audit. [Thesis URL](https://libraetd.lib.virginia.edu/downloads/6d56zx52j?filename=1_Runnels_Ian_2021_PHD.pdf)

The current Oh–Park manuscript was screened at the introduction, structural statements and question list. This audit does not certify its proofs. Its intermediate-RAAG mechanism does not by itself establish preservation of the relevant all-surface pseudo-Anosov type. A bounded literature pass cannot establish that no unpublished or unindexed full solution exists. [Oh–Park v2](https://arxiv.org/pdf/2608.09535v2)

## Conventions that must be preserved

1. The intrinsic predicate is nonidentity and not conjugate into an induced nontrivial join subgroup of the original RAAG. For a cyclically reduced element, use containment of its support in an ambient join, not merely whether the support's induced graph is itself a join.
2. Koberda–Mangahas–Taylor's extension-graph and rank-one identifications are invoked in their finite, connected, anti-connected, at-least-two-vertex setting. The report correctly uses an intrinsic definition for disconnected graphs rather than imposing a path metric on a disconnected extension graph. Its free-group treatment is consistent with that definition.
3. The same source's Corollary 1.5 retains both finite generation and admissibility. No conclusion about all embeddings or all infinitely generated subgroups follows from that corollary. [KMT](https://www.nsm.buffalo.edu/~mangahas/files/KMT_transactions.pdf)
4. The all-surface target matters. A pseudo-Anosov component on a proper supporting subsurface does not make the ambient mapping class pseudo-Anosov.
5. Boundary twists can enlarge centralizers when boundaries are fixed pointwise. The report does not use a boundaryless pseudo-Anosov centralizer argument as a general converse.
6. In Proposition 6.2, loxodromicity remains relative to the original ambient RAAG. A finite-index subgroup need not arrive with a RAAG presentation. Restricting the same representation to that subgroup is the operation being obstructed; a newly chosen representation is a different problem.

## Route I audit of the all word Schottky construction

The base matrix has determinant `34·13 − 21² = 1`. Its pole is strictly inside the excluded minus interval; the inverse matrix's pole is strictly inside the excluded plus interval. Exact endpoint arithmetic gives the two compact images `[8/5,18/11]` and `[-7/11,-3/5]`. Because each map is a homeomorphism of the projective line and the pole is in the excluded open interval, the closed complementary projective arc maps to the finite closed interval between the calculated endpoints. Merely checking endpoints without this pole/topology observation would not suffice; the report supplies it.

Translation by `10i` makes all plus and minus closed intervals pairwise disjoint for every finite rank. Conjugation by the corresponding translation matrix transfers the interval inclusions to each generator and its inverse. This is an explicit construction for arbitrary rank, not just the three-generator sample.

For a nonempty cyclically reduced word `W=s1···sk`, the rightmost letter acts first. Cyclic reduction makes the forbidden domain of `sk` disjoint from the closure of the domain of `s1`. Reducedness ensures the next domain is never the next letter's inverse domain. Thus the letter inclusions compose to a strict self-inclusion of the first domain's closure. Repeating the argument for the inverse word gives a strict self-inclusion of the domain belonging to `sk⁻¹`. The two domains have disjoint closures.

Each restriction is a continuous interval self-map and therefore has a fixed point. A fixed point of the inverse is also a fixed point of the original word. The resulting two distinct real projective fixed points, together with strict containment excluding the projective identity, imply a hyperbolic element of `PSL(2,R)` and hence absolute trace greater than two for the determinant-one representative. Both `I` and `−I` are excluded. Every nontrivial reduced word is conjugate to a nonempty cyclically reduced word; trace and hyperbolicity are invariant under conjugacy. This proves injectivity into `SL(2,Z)` and the all-word claim.

The once-punctured torus convention, rather than a once-holed torus with pointwise-fixed boundary, gives the stated `SL(2,Z)` identification. The rank-one case works. If an empty graph on zero vertices is admitted, its trivial group adds only a vacuous case. The construction settles the free case and provides no mechanism for additional commuting edges.

## Route II audit of domination and support realization

For nonempty `U`, the equivalence between avoiding every ambient join and connected closed domination in the opposite graph is exact.

- A disconnected opposite subgraph on `U` separates `U` into two nonempty parts with every original-graph cross edge, so the original induced graph is a join.
- If an outside vertex lacks an opposite-graph neighbor in `U`, adjoining it makes a join with `U`.
- Conversely, if `U` is contained in a join with nonempty sides, meeting both sides disconnects the opposite subgraph. Meeting only one side leaves an outside vertex of the other side undominated.

For a singleton, connectivity is automatic. Closed domination holds precisely when its vertex is adjacent in the opposite graph to every outside vertex, equivalently when that vertex is isolated in the original graph. Such a singleton is intrinsically loxodromic. A total-domination convention would incorrectly exclude it. For connected sets with at least two vertices, every inside vertex has a neighbor inside, so closed and total domination coincide.

Finite descent to inclusion-minimal connected dominating sets is valid. Filling is monotone under enlarging the support family. A positive word containing each label once is nonidentity and cyclically reduced; its support is exactly the prescribed set. Therefore an essential curve missed by that support family supplies a genuine loxodromic witness whose image fixes that curve. Larger common generator powers continue to fix it.

### Exact Runnels dependency

The published 2021 article, not the inspected 2020 preprint, contains Theorems 2–3 and their combined Theorem 6. The input is an irredundant collection of pure classes with connected essential supports. The common exponent depends on the chosen geometric data; the proof allows enlarging it. For the report, the needed consequence is only that a cyclically reduced word whose participating supports fill the whole ambient surface has pseudo-Anosov image. Section 4.3 explicitly uses filling. [Published article](https://par.nsf.gov/servlets/purl/10232333)

The source's support convention matters: additional twists about boundary components count as separate annular support components and can destroy connectedness. Annular twists should not be described as ordinary Nielsen–Thurston pseudo-Anosovs merely because the article uses a broad support label. Neither arbitrary boundary-fixed variants nor arbitrary pure collections are certified without the source hypotheses. The report's conditional Proposition 3.2 retains those hypotheses, so its inference is valid. `SCOPE_CLARIFICATIONS.patch` makes these limits more explicit without altering any mathematical result.

### The C5 conclusion is local to the support model

The five inclusion-minimal connected dominating sets are the consecutive triples. A clique in `C5` is empty, a singleton, or an edge. The complement of an edge is a consecutive triple; every singleton is contained in an edge, and the empty case is immediate. Hence a curve meeting only clique-labeled regions misses one such triple.

This excludes private essential handles and essential curves localized to selected clique-overlap gadgets. It does not assert that every possible realization must contain such a curve. Disk overlaps may have no essential curve, and a global support arrangement may make every essential curve meet nonclique labels. No counterexample to general `C5` type-preserving embeddings follows.

## Route III audit of the cycle cover diagonal

The diagonal formula is the one used in Section 4 of Kim–Koberda. Same-label vertices of the covering tree are nonadjacent, so the corresponding target generators commute. Original commuting labels have no edge between any of their lifts, so the generator assignment is a homomorphism. This is the opposite-graph convention and must not be reversed. [Kim–Koberda](https://arxiv.org/abs/1312.6465)

A finite subtree of the universal cover of a cycle is a consecutive path. After choosing an endpoint, orientation and cycle labeling, its labels are `j mod n`. Meeting every label forces at least `n` vertices. For `n≥5`, removing labels 1 and 2 leaves a connected path in the base cycle, with 1 dominated by 0 and 2 by 3. This is a loxodromic positive source support.

Its lifted positive support contains the actual path vertices 0 and 3 but excludes the intervening vertices 1 and 2. A path has no alternate connection, so the induced lifted support is disconnected. Its opposite induced graph is consequently a nontrivial join. Positivity prevents cancellation and makes the image nonidentity, even if the whole diagonal homomorphism is not injective.

The argument applies to every such finite subtree, including the enlarged subtrees used for injectivity. It does not obstruct a different anti-tree embedding or a direct mapping-class embedding. Quasi-isometric embeddedness alone gives no type-preservation conclusion.

## Route IV audit of the P4 witness

Set `w=[[a,c],[b,d]]` with the report's commutator convention. An independently checked exact conjugacy certificate is

`q=bac`, and `q⁻¹ w q = a⁻¹ d b⁻¹ d⁻¹ a c⁻¹ a⁻¹ d b d⁻¹ a c`.

To derive it, first conjugate by `b⁻¹`; `b` commutes with `[a,c]`. The expanded inverse pair of `c` letters cancels across a subword involving only `b,d`, both of which commute with `c`. Conjugating the resulting word by the inverse of its initial `ac` gives the displayed representative. The independent letter-reduction algorithm verifies the conjugacy identity directly.

Every consecutive circular pair of occurrences of `a` has a `c` or `d` blocker. The two `b` arcs have a `d` blocker, the two `c` arcs have an `a` blocker, and the consecutive `d` arcs have `a` or `b` blockers. These blockers cannot commute past the relevant generator. In particular no opposite-sign pair can become adjacent, linearly or across the circular boundary. The representative is cyclically reduced and nonempty, with full support. The opposite graph of `P4` is the connected path `c-a-d-b`; full support dominates vacuously. The graph lemma therefore proves intrinsic loxodromicity.

Universal vanishing is an algebraic proof rather than a finite target search. For any target with abelian centralizers of nonidentity elements, write the four images as `A,B,C,D`. If `B=1` or `C=1`, one inner commutator is immediately trivial. Otherwise the relations place `A,C` in the abelian centralizer of `B`, and `B,D` in that of `C`. Both inner commutators then vanish. This covers every free group, including trivial and rank-one targets, and every product of such targets coordinatewise. No finite-generation assumption or bound on detector count is used.

Mapping class groups are not generally in that target class. The obstruction is therefore to free-target detection, not to all mapping-class embeddings. The independent search confirms 2,308 reachable commutation/cancellation/rotation states and minimum length 12. Its no-insertion search is corroboration; the explicit circular normal-form argument supplies the mathematical cyclic-reduction justification.

## Route V audit of covers and finite index restrictions

For an unbranched finite covering of finite-type hyperbolic surfaces, the lift of an essential nonperipheral curve remains essential and nonperipheral. Choosing a complete hyperbolic metric with geodesic boundary where applicable makes this direct: lifted closed geodesics cannot be nullhomotopic or peripheral. The full preimage of an invariant multicurve is nonempty and invariant under any lift of the relevant positive power. If representatives are initially preserved only up to isotopy, lift the corresponding isotopy; the mapping-class conclusion is unchanged. Removing duplicate isotopy classes still leaves a nonempty invariant multicurve.

This proves curve reducibility and excludes pseudo-Anosov dynamics. It matches the invariant-multicurve convention in the K3 chapter. The proof does not involve puncture filling, boundary capping, forgetting marked points or branching. Those operations can change essentiality and are outside the conclusion.

For a finite-index subgroup `H` of the original RAAG, the action of powers of `g` on the finite coset set gives a positive `k` with `g^k∈H`. A cyclically reduced loxodromic representative has no circular cancellation; concatenating positive copies remains cyclically reduced with the same support. Thus the power is still loxodromic in the original ambient RAAG. The invariant multicurve of the original image persists under powers. Restricting the same embedding cannot remove the bad witness.

No new intrinsic RAAG classification for `H` is asserted, and no obstruction to choosing an unrelated embedding of `H` is proved. The optional clarification patch states this ambient qualification explicitly. The finite-cover theorem is proved geometrically, not computationally verified.

## Executable findings and correction

### Baseline reproduction

The independent implementation `independent_exact_check.py` uses set-based graph traversal and induced-join bipartitions, an independent signed-letter reduction and cyclic search, flat integer matrices, and direct finite-word enumeration. It reproduces:

- 1,099 labeled graphs and 32,767 nonempty supports, with no graph-criterion mismatch.
- 616 cycle-cover cases.
- Five minimal C5 triples, ten nonempty cliques and no clique transversal.
- The explicit conjugator `bac`, 20 directed inverse-pair arcs, 2,308 search states and cyclic length 12.
- The two exact rational interval images, 3,918 cyclic words and minimum absolute trace 47.

All its conditions are explicit calls that remain active under optimization. It succeeds in normal, `-O` and `-OO` modes.

### Read only execution and negative controls

The executable audit ran as real UID 1000 and effective UID 1000 on Python 3.12.14. Read-only specimens used 0444 input files and 0555 current directories. Actual attempted writable opens of input files and attempted file creation in the current directory returned permission errors. This is not a root run with permission bits treated as a sufficient test.

The original CLI fails at its mandatory neighboring result-file write in all three modes. To examine its mathematical functions without altering the original program, `readonly_core_runner.py` loads it with a non-main module name, invokes the same five functions, and constructs the same result dictionary. These are explicitly core-function runs, not successful unmodified CLI runs. Baseline core results equal the frozen JSON in every mode, although optimized equality alone provides no evidence that the stripped conditions ran.

Five separate mutations test false graph domination, a connected lifted cycle support, a non-cyclically-reduced word, the identity Schottky matrix, and an invalid full-vertex C5 clique. All five are rejected in normal mode. Under each optimized mode the original core falsely accepts all five. In particular, the cycle and clique mutations can return exactly the frozen result dictionary even though the tested mathematical statement is wrong. The identity-matrix specimen reports minimum trace 2 alongside its false success flag.

The corrected CLI rejects all five mutations in all three modes, for 15 successful negative controls. Its valid stdout is byte-for-byte equal to the original 2,985-byte frozen `VERIFICATION_RESULTS.json` in all three modes. Explicit external-output runs also produce those same bytes, while leaving the read-only input and current directory untouched. The execution record contains 42 verifier process runs plus three independent-implementation runs.

### Minimal patch scope

`VERIFIER_CORRECTION.patch` and `verify_exact_corrected.py`:

1. Replace all 15 removable assertions with explicit `require` calls that raise on failure.
2. Use stdout for complete JSON by default, or an explicit `--output` path.
3. Replace the unused hashing import with the required argument-parser import.

The graph domains, words, matrices, sampled bounds, equations and result content are unchanged. The patch does not transform finite testing into a proof of the unbounded statements. The independently written checker supplies additional corroboration, not a formal proof certificate.

`SCOPE_CLARIFICATIONS.patch` is optional editorial tightening of the Runnels sentence and finite-index ambient wording. It changes no proposition, example, route count, conclusion or novelty assessment. It is supplied separately and has not been applied to the freeze.

## Acceptance conditions and remaining question

The correct disposition remains **partial / unresolved, five routes, no established novelty**. The literature assessment remains bounded. No inaccessible thesis proof is credited, and no claim of a general negative result is supported.

For reproducible acceptance, retain the original freeze and use the separately pinned correction with this audit. The authored mathematics passes this audit within the stated external theorem dependencies. The original optimized checker by itself is not an acceptable verification certificate.

A full affirmative solution still needs a graph-uniform method producing an injective homomorphism with simultaneous whole-surface pseudo-Anosov images for every intrinsic loxodromic. A full negative solution must rule out every such homomorphism for a specified graph. The five routes reviewed here do neither.
