> Editorial scope: This is the complete authored text of the accepted third-round source document, with operational identities and reproduction directions editorially removed or relabeled. Mathematical arguments and finite-scope counts are preserved. References to candidate status, packet contents, or narrower review scope record the original stage; the final combined decision is in [ACCEPTANCE_REPORT.md](ACCEPTANCE_REPORT.md). This public edition contains prose and public verification metadata only. It contains no programs, raw certificates, dataset contents, source documents, or runnable bundle. Original and distributed identities are different; [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json) identifies only the files actually distributed.

# Independent audit: the one-versus-four prescribed Clebsch extension

12 October 2026 UTC. Problem 3209, queue row 1752.

## Verdict and exact scope

**ACCEPT. No mathematical correction to the pinned elementary lemma is required.**

For every finite simple triangle-free subcubic graph and every specified cut whose complement is a matching, if exactly one matching edge lies in Y and at most four lie in X, the specified class extends: every cut edge has a unit-vector difference in F₂⁴ and every matching edge has difference J=1111. The cut need not be globally maximum, connectedness is unnecessary, and no signed degree-choosability theorem is a premise.

The accepted input is the complete original elementary lemma, accompanied by the tester’s complete report. Their original artifact identities are retained outside this edition.

The main manifest’s original identity is retained outside this edition. It covers exactly 99 payload files; the manifest itself is the one additional file. The separately pinned lemma manifest has an original identity retained outside this edition; it covers a 16-file subset of those payloads, not a second closed directory. These two different freeze conventions were checked as such. Every file's exact size and digest was checked, with a closed main inventory and no skipped datasets.

This audit also accepts the tester's bounded positive-certificate claims and the explicitly stated scopes of its two authored negative examples, as detailed below. The source catalogs' completeness up to isomorphism and nonisomorphism remain external provider assertions. The report does not claim novelty, solve or disprove the unrestricted Weak pentagon target, establish a universal global-maximum-cut theorem, or settle the universal mixed 2+2 four-demand case.

No frozen candidate file was edited. No remote action or publication was performed. This audit contains authored checking code, scalar verification receipts, and this mathematical analysis; it does not copy catalog records or third-party source documents.

## 1. Cube facts and initial demand orientations

An even-parity cube class has eight vertices arranged in four antipodal pairs. If h is odd, its four cube neighbors represent those four pairs exactly once. A translation takes any selected same-parity vertex to zero; each remaining distinct nonantipodal vertex has weight two. For at most three selected vertices, the two possible weight-two supports intersect unless they are disjoint complements. A unit vector in the intersection, or in the single support, supplies a common opposite-parity neighbor. Repetitions cause no extra constraint. Empty neighborhoods have an arbitrary neighbor of the required parity. No four-vertex common-neighbor claim is used.

Write rs for the unique Y-demand, R=N_B(r), and T=N_B(s). Each set has at most two elements because its endpoint already uses one degree on rs. Triangle-freeness implies R∩T is empty and neither R nor T contains both ends of one X-demand. Consequently, assigning distinct magnitudes to the at most four X-demands, with opposite signs on each pair, permits every R endpoint to be positive and every T endpoint to be negative. If both endpoints of a demand meet the boundary, they lie in opposite sets, so the requirements agree. A demand meeting neither set retains one independent sign choice.

Two already colored endpoints of different demands have different magnitudes, hence cannot be antipodal. The two endpoints of the same demand cannot have a common cut neighbor: that would form a triangle with the demand edge. These facts cover all ordinary-neighborhood constraints among initially colored vertices.

## 2. Boundary singleton graph and the degree-list bound

Let U be the unmatched X-vertices in R∪T. Its size b is at most four. Assign a vertex u the sign ε_u=+ on R and − on T, and leave only its magnitude to choose. The graph H joins two boundary singletons precisely when their signs are opposite and they share an ordinary Y-neighbor. Same-sign pairs cannot be antipodal and need no edge. Repeated witnesses produce one simple edge. In particular H is a subgraph of a bipartite graph with at most two vertices per side, but the greedy argument requires no stronger structural classification.

A boundary singleton already has its incident r or s edge. Its at most two other Y-neighbors each expose at most two other X-incidences, giving at most four slots, counted with multiplicity. Every distinct H-neighbor occupies a slot of an unmatched boundary vertex. Every forbidden magnitude occupies a slot of a colored demand endpoint with opposite sign. These categories are disjoint, and repetitions only decrease the count of distinct constraints. Therefore |A(u)|+d_H(u)≤4 and |L(u)|≥d_H(u).

Fix any H-edge uv and an ordinary Y-vertex witnessing it. If the witness has only u,v as X-neighbors, each endpoint uses only one slot there and has at most two elsewhere, so both have slack. If there is a third neighbor w, exhaust its possibilities:

- A colored demand endpoint has the same sign as one of u,v, contributing no forbidden magnitude at that endpoint.
- A boundary singleton has the same boundary sign as one of u,v, contributing no H-neighbor there.
- Any other unmatched X-vertex is still uncolored and contributes neither type of restriction.

Thus at least one endpoint has |A|+d_H≤3. This is stronger than needed: every edge has a slack endpoint, and hence every nontrivial component has a vertex with |L|≥d_H+1. It remains true after any choice of the free demand orientations. Duplicate slots or constraints cannot invalidate the surplus.

For each nontrivial component, root a spanning tree at a surplus vertex and process children before parents. A nonroot still has an uncolored parent, so at most d−1 colors are forbidden when its list has at least d. The root has at least d+1 colors against at most d colored neighbors. This proves list colorability component by component; no connectedness of the original graph or of H is assumed.

## 3. The isolated-list repair is valid

An isolated vertex requires a nonempty list; the inequality |L|≥d=0 alone would not suffice. The candidate correctly handles this separately.

If fewer than four X-demands exist, an unused magnitude remains in every list. When exactly four exist, an empty list requires all four magnitudes to be forbidden. The slot budget forces exactly four slots, each occupied by an endpoint of a different demand. In particular, each of the four demands appears exactly once in these slots. Let Z contain precisely isolated vertices with that structural pattern, independent of the signs currently chosen.

There are at most 4−b matched boundary vertices. Each forced demand orientation uses at least one such vertex, so at most 4−b demand orientations are forced. At least b demand orientations are therefore free, while |Z|≤b. Inject the vertices of Z into distinct free demands. The assigned demand appears exactly once in the assigned vertex's four slots. Orient it so this endpoint has sign ε_u. Its magnitude is then available at u. Different assigned demands give independent choices. Orienting a demand may affect other lists, but every repaired vertex keeps its own assigned available magnitude; the degree and component-surplus arguments remain valid for all orientations. Vertices outside Z cannot have four forbidden magnitudes in the first place.

This proves nonemptiness of every isolated list. It covers b=0, Z empty, fewer than four demands, repeated incidences, demands meeting both boundary sets, and all possible disconnected boundary components.

## 4. Greedy completion and edge verification

All remaining X-vertices are unmatched and outside R∪T. Hence none is adjacent to r or s. It has at most three ordinary Y-neighbors, each exposing at most two other X-neighbors. At most six already assigned colors can forbid their antipodes, leaving at least two of the eight signed colors. Later choices use the same exclusion rule, so each final ordinary Y-neighborhood has no antipodal pair.

There are no internal X-edges left to satisfy beyond the already assigned demands: the cut complement is exactly the matching. There are no internal Y-edges other than rs. Every ordinary Y-vertex has at most three X-neighbors, so the cube fact supplies its image independently. Set r=h and s=h+J. The boundary signs put their neighbors in N(h) and N(h+J), respectively. Every matching edge is antipodal by construction, and every cut edge is a cube edge.

All X-images may be chosen even and all Y-images odd, consistently even across disconnected components. An isolated X-vertex has the full eight-color choice; an isolated ordinary Y-vertex may take any odd image. Low-degree demand endpoints merely reduce restrictions. No hidden parity, degree, endpoint, or connectedness exception remains.

For cubic graphs, summing degrees in the two sides gives 3(|X|−|Y|)=2(|M_X|−|M_Y|). With five total demands, the only possible split is 4+1 up to exchange. With exactly one on the smaller demand side, possible larger counts are 1,4,7,… . The lemma therefore covers every five-demand cubic matching cut. Combined with the independently accepted 18-vertex 1+5 example and its 28-vertex cubic 1+7 completion, four is the sharp subcubic bound, and seven is the first possible failing larger count in this cubic subclass. This is a prescribed local-cut statement.

## 5. Independent finite certificate verification

The independent certificate checker was written for this audit and imports neither the packet's solver nor its checkers. It decodes and validates every graph6 record, checks cubicity, triangle-freeness and connectivity, rejects duplicate records, checks exact expected order and record count, and enumerates every normalized cut using a Gray-code score update with direct edge-sum checkpoints. This differs from the packet verifier's subset recurrence. It determines the full matching-complement target set before comparing it to the certificate. Every supplied label and edge difference is checked directly; omitted, duplicated, non-target, malformed, and extra certificate data are rejected.

Across the 8,738 supplied records at orders 6,8,…,18, the audit examined 1,049,918,752 normalized cuts and reproduced all 106,875 targets:

- 2+2: 64,221 local nonglobal and 9,426 global.
- 4+1: 33,201 local nonglobal and 27 global.
- Total: 97,422 local nonglobal and 9,453 global, each with a valid prescribed witness.

Exact per-order receipts are retained. This exhausts the supplied records, not an independently generated isomorphism classification.

The same new checker independently validated every record of all seven generated batches, totaling 520,000 distinct labeled graphs. It checked each exact designated cut and matching, canonical edge order, graph structure, within-batch uniqueness, exact count, and every witness difference. The batches have different orders, so within-batch uniqueness also gives uniqueness across this inventory. Their designated cuts are strict single-vertex local maxima because the graphs are cubic with matching complements; their global optimality was not claimed or computed. They are fixed-seed bounded samples, not a uniform isomorphism-class sample or an exhaustive theorem.

The candidate's entire 163,228-case construction test ran in normal Python, -O and -OO, reproducing the frozen output byte for byte in every mode: 33,228 catalog cases, 120,000 generated 4+1 cases, and 10,000 deterministic edge-deletion cases.

Independent extra construction tests covered every labeled simple triangle-free subcubic graph on 2 through 6 vertices and every normalized cut satisfying the lemma: 48,231 cases, including 27,128 disconnected cases and 21,668 cases with isolated vertices. Three additional relabeled/complemented examples exercise four structurally potentially empty isolated lists simultaneously, with isolated vertices in both cut sides. All passed in all three modes. These checks use the candidate constructor but an independent edge-by-edge output validator.

The independent finite-template checker independently reproduced all 75,265 orientation templates and all 588,768 allowed degree-list templates. The latter are checked by MRV backtracking rather than the candidate's rooted-tree greedy procedure. It also exhaustively checked 1,170 cube tuples. The packet's six local slot types and complete original template checker were replayed in all three modes. The finite template universes are precisely those stated by the packet; their relevance to arbitrary graphs follows from the written proof, not from extrapolating these counts.

The catalog boundary diagnostic was independently reconstructed in full: 213 degree/touch signatures on the 33,228 five-demand targets, including 226 cuts with four boundary paired entities all of signed degree six. The complete signature histogram matches. This finite observation invalidates the tempting simplification that all boundary pairs automatically have degree at most four; it is not a premise of the accepted elementary proof.

## 6. Negative examples and exact global-max witnesses

The separate symbolic audit independently reconstructed and accepted both obstructions, including the exact signed doubled-K₅ restriction and the five-versus-four antipodal-pair contradiction. Its externally pinned frozen audit manifest covers 27 payload files; the original manifest identity is retained outside this edition. This audit verified its complete inventory and all payload hashes, rather than relying on a summary.

Here both tester graphs were independently reconstructed from the literal neighborhoods and attachments, cross-identified with the symbolic auditor's actual exhaustive-enumeration inputs, and compared to both the tester JSON and raw maxcert forms. The tester's negative verifier was inspected and replayed under normal, -O and -OO. Unrestricted Clebsch witnesses and the gain-one switch {0,2,10} were independently checked.

- The 18-vertex graph has 26 edges, an obstructed cut of size 20, and true maximum 22. The coordinated independent enumeration examined all 131,072 normalized cuts and found exactly 7 maxima.
- The 28-vertex cubic graph has 42 edges, an obstructed cut of size 34, and true maximum 35. The coordinated independent enumeration examined all 134,217,728 normalized cuts and found exactly 72 maxima.

To avoid duplicating that expensive enumeration, this audit uses those frozen exhaustive counts after graph-identity verification. It independently checks all 7 and all 72 tester maximum-cut witnesses: each cut is normalized, distinct, of the verified maximum size, and every edge satisfies its prescribed difference. Since the distinct listed counts equal the complete exhaustive counts, every global maximum of each of these two particular graphs has an extension. This statement is stronger than checking one example maximum per graph, but says nothing universal about other graphs.

Both bad prescribed cuts are strict single-vertex local maxima and are nonglobal. Neither is a counterexample to the fixed-global-maximum strengthening or to the unrestricted Clebsch homomorphism target.

## 7. Optimization safety, hostile controls, and replay

The independent hostile-control suite contains 155 tests and ran under normal Python, -O and -OO with byte-identical outputs. It mutates and rejects every one of the 99 pinned payloads, including every catalog and certificate dataset. Additional checks reject a changed manifest, an extra file, a same-bytes symlink, wrong maxima, wrong and out-of-range labels, negative certificate flags, nonnormalized cuts, missing and duplicate targets, missing and extra records, coordinated catalog/certificate truncation, trailing fields, duplicate generated edges or graphs, incorrect designated cuts, removed negative constraints, corrupted unrestricted and maximum witnesses, and an omitted global maximum. Positive and restored-inventory controls also pass. Both the new certificate checker and the rebuilt packet checkers reject the corresponding certificate mutations.

All Python acceptance decisions are explicit checks, not removable assertions. Source inspection found no assertion-based validation in the candidate Python or C++ files. Complete construction, template, negative, independent diagnostic, inventory, and hostile-control outputs agree across normal, -O and -OO. The audit's own C++ code likewise uses explicit runtime checks.

The candidate author’s final replay receipt was exactly identified by byte count and digest, which are retained outside this edition. Its main and lemma manifest identities match the audited inputs. All three receipt-listed artifacts were hashed and sized, both replay logs were inspected for their terminal complete-success records, and the optimized construction output equals the frozen result. The receipt records complete normal replay and byte-for-byte regeneration of all catalog certificates and seeded generated streams. The independent audit did not redundantly rerun random generation: certificate validity was independently rechecked for every record, while exact seeded regeneration is supported by the pinned author's receipt and logs. Byte reproducibility retains the stated C++ standard-library dependency.

The undistributed original replay procedure rebuilds the checkers, replays these checks without changing frozen inputs or audit outputs, and compares the resulting receipts. The audit is separately frozen with an external manifest pin. These procedures verify the stated finite scopes; the universal one-versus-four theorem is accepted on the complete elementary argument in Sections 1–4.
