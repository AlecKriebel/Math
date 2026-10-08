# Independent audit: GRAPH-043 / problem 1430

Audit date: 2026-10-08 UTC. Queue rank: 1015.

## Verdict

**Accept the corrected packet as an unresolved investigation with five substantive mathematical approaches, not as a solution.** The intended question is whether some finite simple word-representable graph of order N>=4 has representation number exceeding floor(N/2). Neither such a graph nor the universal opposite inequality has been established here.

The elementary arguments and bounded computational conclusions survive independent checking. The published dependencies used for the restricted cases have the stated hypotheses. The September 2026 bipartite result is accurately attributed to a primary preprint; its external certificate and Lean claims have not been independently reproduced in this audit.

Two substantive presentation repairs were required before source-free publication:

1. Replace the brief verbatim source question with an authored mathematical paraphrase. The original packet's source-free statements were too broad while that quotation remained. The original frozen bytes and the literal removal diff are excluded from the corrected publication slice.
2. In the summary of approach 3, qualify R(G)<=2c2(D) by noncompleteness. With the usual empty cover, a complete graph has c2(D)=0 and R(G)=1. The detailed proof already contained the qualification; this is a summary-level correction, not a failure of its argument.

The remaining edits describe the contemporary bipartite result as credited preprint mathematics rather than ambiguously calling it verified, describe the clique-dependent bound without implying it is strictly sharper for every clique size, and update the audit-completion statements. They do not change the unresolved status, approach count, witness data, verifier, or diagnostic result.

## Scope, parameter, and source question

Section 9 of [Kitaev's survey](https://arxiv.org/abs/1705.05924v1), printed page 35, asks the underlying half-order question without a lower order cutoff. Its [author-hosted rendering](https://personal.strath.ac.uk/sergey.kitaev/Papers/wrg-kitaev.pdf) was also inspected. The retained arXiv PDF and author-hosted rendering have different displayed dates; no claim that they have identical bytes is made.

The intended domain consists of finite simple undirected graphs that possess a word representation, with every vertex present in the word. Assigning infinity to non-word-representable graphs does not answer this question. Uniform multiplicity is the relevant parameter. The proof in A3 correctly converts any representing word with maximum multiplicity k to a k-uniform word: prepend only deficient letters in first-occurrence order, preserve alternating pairs, and retain each old nonalternating pair inside the unchanged suffix. Thus maximum-copy minimization and the least uniform multiplicity agree. Minimum unrestricted total word length and permutation-representation number are different parameters.

The stated exceptions at N=1,2,3 are valid. The single vertex has R=1; the two-vertex independent graph and the three-vertex path have R=2. Every one-uniform word represents a complete graph, providing the necessary lower bounds. Those exceptions diagnose the unqualified wording; they do not settle the expressly repaired N>=4 research question.

## Audit of the five approaches

### 1. Order dimension and apex extensions

B1 is correct with its minimum over posets having the given comparability graph. In a concatenation of permutations, an edge is exactly a pair whose relative order never changes. The intersection is a poset, and a realizer gives the converse.

B2 handles the often-omitted cyclic endpoint issue correctly. Equal multiplicities make linear alternation equivalent to cyclic alternation. Rotation therefore preserves nonedges as well as edges. Starting an apex representation at the apex partitions it into blocks containing exactly one of every other letter. The converse insertion creates every apex edge without altering old pair projections. Uniformity is essential: rotating 010 to 100 changes its represented two-vertex graph.

[Hiraguchi's original article](https://scirep.w3.kanazawa-u.ac.jp/articles/01-02-001.pdf), printed page 94, statement (7.5), was checked visually. It gives the maximum poset dimension floor(n/2) for n>=4. This verifies the cutoff used in B3. The comparability conclusion and the stronger apex-extension conclusion are valid, with the latter requiring base size at least four. Every bipartite graph is a comparability graph by orienting from one part to the other, so the exclusion of bipartite counterexamples to the half-order bound already follows from this classical route. It does not depend on the new preprint or its certificates.

For the crown-plus-apex family, the correct count is N=2m+1 and the value is R=m for m>=2. The supplied realizer orders all cross-part nondiagonal pairs correctly and reverses each missing diagonal in an appropriate order; same-part pairs receive both orders. For m>=3, connectedness of the crown forces any transitive orientation to orient all edges consistently from one part to the other: an incoming and outgoing pair at one vertex would force a within-part edge. The standard diagonal reversal cycle proves dimension at least m. The m=2 lower bound instead follows from noncompleteness. The m=1 apex graph is a three-vertex path and has R=2, so it is correctly excluded from the R=m formula.

The selected semi-transitive orientation of the three-vertex path is a valid counterexample to the proposed reachability-dimension transfer. Transitive closure inserts the missing edge, so its dimension cannot provide the desired graph bound. No general transfer theorem is obtained.

### 2. Components, padding, and twins

The padding prefix preserves every edge and leaves each nonedge obstruction in the old suffix. For two or more nonempty components, the formula max(2,R(G1),...) is exact: the extra 2 is necessary even for two isolated vertices, and concatenated k-uniform component words for k>=2 exclude every cross-component edge.

True-twin substitution preserves multiplicity and all required pair projections. False-twin substitution after padding to at least two copies creates a repeated symbol at the changed final boundary, while preserving projections against all other vertices. The resulting formula max(2,R(G)) is correct, including the one-uniform input exception.

Consequently a smallest counterexample in the intended regime is connected, twin-free, noncomparability, has no universal vertex, and has order at least six. The proof uses the explicit order-four and order-five witnesses before applying twin deletion. These are necessary restrictions; no argument ensures every remaining graph is reducible.

### 3. Compatible nonedge covers

The definition of compatibility agrees with the covering definition preceding Lemma 1 of [Halldórsson–Kitaev–Pyatkin](https://arxiv.org/abs/1501.07108v1): respecting every directed edge in the first-occurrence permutation also respects every directed path. Their Lemma 2 assumes a semi-transitive orientation and supplies a two-uniform word covering the nonedges incident with a specified vertex. These hypotheses were checked in the primary PDF. Their Theorem 3 gives 2(N-omega) for noncomplete graphs, and Corollary 1 gives 2N-4 for N>=3. The corrected packet does not import the superseded preliminary R<=N claim.

For an edge u->v, all compatible blocks project to repetitions of uv; concatenation preserves the edge. A nonedge obstructed inside one block remains obstructed after concatenation. Compatibility cannot be dropped: concatenating 0101 and 1010 destroys their common edge. A maximum clique's complement meets all nonedges, giving the stated cover bound. The large-clique arithmetic is correct.

The triangular prism has R=3. Its retained three-uniform witness was independently checked, and a separate exhaustive generator excludes every two-uniform representation up to relabeling. The known prism result is also correctly stated in Theorems 16-17 of [Kitaev's prism paper](https://arxiv.org/abs/1403.1616). Thus concatenating only complete two-uniform blocks cannot always attain floor(N/2): at N=6 it supplies either two copies, which is impossible for the prism, or at least four. This obstructs that restricted construction method, not the proposed bound.

### 4. Counting

There are 2^(ab) labeled graphs on a fixed bipartition of sizes a and b. They are all word-representable via a transitive orientation. Padding justifies comparing them with words of exactly kN positions. The N^(kN) overcount yields a valid lower-bound existence argument when kN log2(N)<ab, on the scale N/log N.

The sharper count (kN)!/(k!)^N is at least (N!)^k because concatenating k permutations is injective as a construction of words when block length N is fixed. The factorial estimate and the inequality k(N-1)>=ab at k=floor(N/2), N>=3, are correct. Hence this raw word-count comparison cannot force a graph beyond the target. The argument does not rule out stronger counting methods that control fibers or use other graph families.

### 5. Exact finite constraints and exhaustive small checks

The occurrence-order encoding is exact when each edge permits either alternating interleaving and each nonedge forbids both. Forbidding only the interleaving starting with one endpoint is unsound: the opposite alternating word remains an edge.

Every normalized double word corresponds uniquely to a perfect matching of its 2N positions, with pairs labeled in order of their first endpoint. Conversely every labeled double word normalizes by renaming. Thus the count (2N)!/(2^N N!) and the author's recursive exhaustiveness argument are correct. The independent audit instead generated perfect matchings of positions, never importing the author's generator or edge code.

All 1,099 retained masks through order five have valid two-uniform words. Both independent edge predicates agree. At order six, all 10,395 normalized words were independently regenerated. Exactly three give cubic graphs, all with zero triangles, so none can be a triangular prism. This proves the claimed bounded exclusion; it gives no conclusion at untested orders or multiplicities.

## Contemporary literature and provenance checks

- [Mozhui–Krishna, 2025](https://arxiv.org/abs/2506.01057v1): the primary paper's standing connected/reduced convention and its part-size notation were checked. Corollary 1 gives 1+ceil(m/2); the sharper odd-part theorem explicitly requires 5<=m<=n. Small odd parts must not be inferred from the abbreviated abstract. Reduction to disconnected graphs must retain the floor of two established here.
- [Colbrook–Drysdale, 24 September 2026](https://arxiv.org/abs/2609.35842v1): the public abstract, [HTML theorem statements](https://arxiv.org/html/2609.35842v1), and retained primary PDF agree on R<=ceil(N/4) for every finite simple bipartite graph with N>=9, including isolates, unequal parts, disconnected graphs, and twins. Corollary 1.2 gives crown values 2 for part sizes 1-3, 3 for part size 4, and ceil(m/2) for m>=5. This is a credited preprint theorem. Its finite certificate arguments and Lean formalization were not reproduced or certified here.
- [Akgün–Gent–Kitaev–Zantema](https://arxiv.org/abs/1808.01215): the reported table has maximum finite representation number 3 at orders 6-8 and 4 at order 9. The non-word-representable entries are separately identified by the surrounding text. Those published graph classifications were not rerun; they must not be conflated with this packet's own exhaustive checks.
- [Hefty–Horn–Muir–Owens, 2024](https://doi.org/10.37236/12806): Section 5.5 distinguishes fixed-orientation and graph representation numbers, consistent with the warning in this packet. No arbitrary transitive-closure inference is licensed.
- The two 2026 publisher-only references in the packet are background with restricted inspection claims. No full-text numerical theorem from either is used for acceptance. This audit is not a renewed global-openness or novelty search.

The two retained public corpus files were independently rehashed and parsed; their counts and hashes match CORPUS_VERIFICATION.json. The selected problem's canonical encoding is 3,479 bytes with the stated hash. All eight retained source PDFs match SOURCE_METADATA.json byte counts and SHA-256 values. SOURCE_INTEGRITY.json records public verification metadata only. File integrity does not by itself establish mathematical validity or a fresh download.

## Independent computations and replay controls

The independent mathematical checker performs 313,309 explicit checks, with no optimization-sensitive assertions. It confirms:

- 1,099 small graph witnesses;
- normalized matching counts 1, 3, 15, 105, 945, 10,395;
- 10,394 uniform-word rotations;
- 8,836 maximum-copy uniformization cases;
- 4,463 star constructions over all numerically topologically labeled semi-transitive orientations through five vertices;
- 9,576 compatible block-pair tests;
- exactly two transitive orientations of each tested connected crown, m=3,4;
- malformed alphabet rejection and mathematical countercontrols for missing uniformity, missing compatibility, one-sided nonedge constraints, the component floor, and false-twin padding.

The independent checker has identical output under normal Python, -O, and -OO. Original and corrected envelopes are separately replayed with externally recorded bootstrap and manifest pins. Each envelope has six passing bootstrap runs: the original location and a relocated copy under all three modes. Each also rejects 48 integrity-mutant executions and 30 direct malformed/semantic payload executions. The latter include a wrong graph witness, missing mask, Boolean letter, nonuniform word, duplicate key, nonfinite number, overflowed float, invalid JSON, oversized input, and wrong top-level type.

Replays run as a non-root user against mode-0444 files in mode-0555 directories. Attempts to open existing files for writing and create new files are denied by the operating system. Before/after snapshots agree. This is permission-enforced read-only verification of the packet and freeze, not a claim of whole-filesystem mount isolation or resilience to a concurrent hostile filesystem. Modified manifests fail the trust-anchor check before parsing; direct malformed payload tests independently exercise the verifier's parser and semantic checks. A resealed hostile verifier is rejected without executing its marker write.

## Publication boundary and remaining gap

The publishable slice consists solely of the corrected packet, corrected freeze and pins, this authored audit, independent checker and replay scripts, and sanitized verification metadata. It excludes original quotation-bearing files, the literal source-removal diff, source PDFs/extracts/screenshots, source dataset contents, private temporary paths, and coordination files. The sanitized author receipt removes its disposable path and retains only verification results and hashes.

The accepted status remains **unresolved, five of five approaches used**. A valid resolution still requires either a counterexample in the stated domain with a proved lower bound exceeding floor(N/2), or a theorem covering every remaining graph. None of the retained reductions, bounded enumerations, or attributed class-specific results supplies that missing step.
