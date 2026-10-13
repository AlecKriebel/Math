# Independent publication-edition acceptance: third surface-obstruction investigation

Verdict: **ACCEPTED WITH STATED SCOPE.** Problem 3327 / OPG-172 remains unresolved. This is the third newly documented substantive investigation; the lifetime count is unknown. The acceptance concerns the exact publication edition identified below. It is a machine-assisted independent review, not human peer review.

## 1. Accepted mathematical result and limits

The complete [structural report](STRUCTURAL_REPORT.md), [finite report](FINITE_REPORT.md), [mathematical audit](INDEPENDENT_AUDIT.md), and all 37 objects in the [finite certificate](ENUMERATION_CERTIFICATE.json) are accepted in their stated scopes. Reading and checking their mathematical content was required in addition to byte verification.

In the simple quartic, triangle-free, K_(2,3)-free class with two or three squares through every edge, every pentagon contains at most two three-square edges. For an h=2 simultaneous obstruction, or an ordinary Euler hopper of Euler genus four, the three-square-edge subgraph has the following necessary structure:

- Its degree-four vertices are independent and have degree-two neighbors in that subgraph.
- At each degree-four vertex precisely two of the three complementary second-neighbor edges occur. There are precisely two all-three-square-edge squares through it, partitioning its incident edges.
- Every component containing a degree-four vertex has a unique square partition. Nontrivial components without such vertices are cycles.
- At least one residual cycle has length at least six. The total length B of residual cycles whose length is not four is a positive multiple of four, with B at least eight. In the report's notation, |D2| is at least 2|F|+B.
- Complete rooted labeled enumeration through order fifteen leaves no graph in either target class. Every such target has at least sixteen vertices.

These statements do not provide a target graph, an upper order bound, a universal nonexistence theorem, or an exclusion at order sixteen or above. The total-length divisibility assertion does not separately exclude a six-cycle. Higher-genus and positive orientably simple Euler-critical routes remain unresolved. The surface orientation counts describe the particular supplied surfaces, not minimum positive nonorientable genus. No novelty or exhaustive current-literature claim is accepted.

## 2. Independent proof review

### Pentagon scarcity

The cross-neighbor graph at a three-square edge is a perfect matching. A repeated endpoint would give the opposite endpoint and a neighbor three common neighbors, contradicting K_(2,3)-freeness. For a fixed pentagon the second common neighbor x_i, when present, is unique, external to the pentagon, and distinct from the other x_j: otherwise a triangle or a forbidden common-neighbor triple results.

A selected three-square pentagon edge forces the two adjacent second-neighbor conditions. If the next two outward conditions also held, quarticity exhausts the endpoint neighbor sets. Two square-matching edges are forced, and the third would join vertices already adjacent to a common pentagon vertex, making a triangle. Three selected pentagon edges either cover all five pentagon vertices or form a consecutive three-edge path. The first arrangement makes all second-neighbor conditions true; the middle edge in the second arrangement has the four forbidden conditions. This establishes the claimed upper bound of two without any embedding hypothesis.

A pentagon through an edge with two degree-four endpoints would already use three selected edges. Consequently such endpoints cannot be adjacent when every edge lies on a pentagon. Counting the four incident edges of each full-link vertex gives the initial bound |D2|≥2|F|.

### Full-link rigidity and contraction profiles

For a full-link vertex f with four neighbors, the six second neighbors indexed by pairs are distinct. Each original neighbor's four adjacency slots are already exhausted. Therefore every pentagon through f comes from an edge joining complementary pair labels; each such edge yields exactly four pentagons through f and exactly two through each incident edge.

One complementary edge cannot support a permissible low-genus contraction rotation. In the two-triangle profile, four distinct quadrangular corners would need four lifted pentagons, while only two exist. In the three-triangle profile, the remaining three corners form a second matching in an alternating six-cycle. At least two quadrangular corners must then use distinct B ends, but the two available lifted pentagons use the same B end. This is an endpoint-incidence contradiction, not just a scalar counting argument. It uses the accepted facial simplicity and alternating-rotation results.

Three complementary edges are also impossible. Every radial edge would appear in a pentagon with two already selected edges at f, forcing all radial edges into the two-square class. The degree-two status of f's neighbors requires one radial three-square edge each. Thus exactly two complementary edges occur; the missing pair determines the four forced radial edges and the unique pair of squares through f.

The additional face-profile observation is valid within the stated contraction hypotheses: a B end with no lifted-pentagon support must receive its second corner from the pentagonal face. No contradiction for all such embeddings is claimed.

### Global compatibility and residual cycles

At a degree-two vertex of the three-square-edge subgraph, any all-three-square square must use both incident edges. There cannot be two such squares, since their opposite vertices would violate the common-neighbor bound. This uniqueness prevents overlap conflicts as forced squares propagate through a component containing a degree-four vertex. Reaching a degree-two vertex covers both edges; reaching another degree-four vertex covers all four. The propagation proves a unique complete edge partition, rather than assuming local choices automatically fit globally.

A nontrivial component with no degree-four vertex is a simple cycle. Triangles are excluded by hypothesis and pentagons by the proved scarcity lemma. If every remaining cycle were a four-cycle, the accepted square-selection equivalence would give Euler genus two, contradicting the target Euler genus four. Hence a cycle of length at least six remains. The identity 4s=4n+|E3| shows |E3| is divisible by four; removing square-decomposed components gives the stated divisibility of B. The B residual-cycle vertices have no full-link neighbor, so 4|F|≤2(|D2|−B). These are necessary structural conditions only.

## 3. Independent complete generation and exact certificates

The root-label reduction was checked directly. A root has four independent neighbors. Every outside vertex has at most two neighbors among those four, and each two-element label occurs at most once. The pair-label graph has every degree equal to two or three, so it is a four-cycle, a diamond, or K4. For p pair vertices, the singleton count is 12−2p and the empty-label count is n+p−17. Empty-label vertices are included and remain separately labeled. Thus the three canonical root patterns cover every graph in the stated class after relabeling; the counts are not counts of isomorphism classes.

The new edition-review generator imports neither the author generator nor the mathematical-audit generator. It reconstructs root adjacencies and enumerates every possible higher-numbered neighbor subset needed to fill the current vertex. A tentative edge is tested by recomputing every vertex-pair codegree, rather than using the author's incremental codegree formula. Triangles and excessive codegrees are monotone violations. The only additional capacity bound deliberately overestimates the number of future neighbors by counting all remaining vertices with a free slot. Consequently its pruning cannot discard a valid completion. Every completed adjacency has a unique row-by-row branch.

The independent enumeration reproduced all twelve pattern counts and matched each complete ordered leaf-adjacency stream against its retained original. Every square-rich survivor was compared by its full adjacency, rather than relying on a count or a graph name.

| Order | Root type 4 completions | Root type 5 completions | Root type 6 completions | Square-rich survivors |
|---|---:|---:|---:|---:|
| 12 | 0 | 1 | 0 | 1 |
| 13 | 2 | 0 | 0 | 2 |
| 14 | 43 | 56 | 42 | 10 |
| 15 | 1,464 | 1,386 | 360 | 24 |

The total is 3,354 rooted labeled completions and 37 square-rich survivors. Orders below twelve are excluded by the complete written argument: twelve two-step walks require at least six outside vertices, while equality at order eleven would yield 66 vertex-square incidences, impossible modulo four. The hand reconstruction at order twelve agrees with the sole certified graph.

The edition-review certificate checker independently enumerates simple cycles beginning at their unique least vertex and orders the two adjacent cycle vertices to remove reversal duplicates. It checks all adjacency entries, degree four, symmetry, absence of loops and duplicate neighbors, connectivity, triangle-freeness, codegrees, square and pentagon counts, and the complete list of edges failing the pentagon condition.

For every supplied omitted-square list, the checker verifies that the distinct listed cycles are actual squares and cover precisely the three-square edges once each. The retained square disks meet every graph edge twice, and each vertex link is a simple connected four-cycle. There are n retained faces, so the closed connected surface has Euler characteristic zero. The quartic triangle-free density bound supplies the matching lower bound E≥2. The surface therefore proves E=2. Independent orientation equations find 19 orientable and 12 nonorientable supplied surfaces. All 31 also pass the numerical pentagon filter.

The six null-cover graphs are independently shown to be connected and bipartite, with no pentagons. Their exclusion does not depend on trusting a failed exact-cover solver or identifying them as co-Heawood graphs. No failed embedding heuristic is used as a certificate.

## 4. Hostile controls and optimized-mode execution

The new checker exhausts all 1,024 pentagon-edge and second-neighbor flag assignments. Exactly 32 assignments with zero selected edges, 30 with one, and 10 with two survive the necessary implications; none with three or more survive. It constructs all six alternating Hamilton six-cycles on the two labeled endpoint classes and confirms that the single-complementary-edge case has no permitted contraction profile. All eight complementary-edge patterns have the predicted 3−r radial options per neighbor.

The mathematical checker directly rejects seven corruptions while bypassing every byte-manifest gate: duplicate adjacency, a missing omitted square, a duplicated omitted square, a false pentagon count, an altered failure list, a false square count, and a wrong vertex count. These semantic failures use explicit exceptions and remain active under optimization.

The edition's separate 28-control suite was also replayed. It rejects altered or missing source bytes, unsafe or nested-archive paths, incomplete and false reversible maps, unauthorized executable payloads, private paths, copied source text, broken links, changed historical companions, unverified citations, false source sizes, false solved/history statements, altered finite counts, and missing or duplicated survivor records, together with the certificate corruptions.

The independent complete generator and certificate review, edition validator, and 28-control suite were executed against the frozen original, actual archive restoration, and actual byte-store restoration in normal Python, -O, and -OO. Their respective outputs agree byte-for-byte across modes and restore paths. The actual restored author finite and local checkers and the earlier independent mathematical-audit checkers were separately executed in all three modes from both source restorations. No assertion-only validation or successful process exit without semantic output is accepted.

## 5. Publication completeness, source identities, and history

The accepted packet contains eleven new public files and twenty-five unchanged historical companions: twelve from the first edition and thirteen from the second, including its separate independent edition acceptance. Every historical byte was compared with its retained identity. The earlier reports retain their original historical scope and are supplemented by this edition. The prior independent mathematical-certificate checker was also re-executed in normal Python, -O, and -OO on these historical public files, with identical outputs. It checks the K4,4 nonorientable-genus-two signed surface, the co-Heawood nonorientable-genus-four signed surface, the edge-deletion torus signed surface, complete square-orbit coverage, the first square-partition certificate, and the deletion/contraction profile counts. This is a fresh replay of the retained prior checker, not a claim that it was newly authored for this review.

All authored mathematical prose, generation reasoning, theorem counts, adjacency certificates, omitted-square certificates, cycle counts, and pentagon-failure lists survive in full. The thirty-five full-text mappings reconstruct both directions exactly, including unchanged spans and the final suffix. The public manifest is generated verification metadata and has no earlier source text to reconstruct.

The only removed fields in the finite certificate identify undistributed operational material or search effort. Removing those two fields recursively from the complete original produces the public certificate exactly. The independent acceptance's conclusions, limitations, result counts, and twelve complete-stream agreement conclusions are unchanged. Its artifact identities are correctly rebound to the actual public-edition bytes. Executable-program and undistributed-output identities are excluded from the new public metadata; their complete original evidence is retained separately. These edits do not remove a mathematical proof or weaken a certified graph object.

The public payload consists only of authored mathematical documents, exact small mathematical certificates, and permitted verification and citation metadata. It contains no executable programs, raw search streams, copied third-party source documents, private coordination material, or new results from a fourth investigation. Local links resolve within the complete edition set. No queue or remote repository changes were made during this review.

The seven entries in [SOURCE_IDENTITIES.json](SOURCE_IDENTITIES.json) were checked against actual retained PDF bytes, including byte length, SHA256, PDF signature, and the matching title in extracted text. Six titles occur in the first two pages; the English title of the seventh is present later in the document. The bounded inspection history remains in the [first source audit](../3327_surface_obstruction_reductions_20261012/SOURCE_AUDIT.md). This is identity and preservation verification, not a new retrieval or a claim that the bibliography exhausts the current literature. Campbell's contribution remains attributed in the original reports.

## 6. Actual recovery and acceptance boundary

Both the compact recovery archive and the separately stored content-addressed objects were read and reconstructed into fresh destinations. Full frozen-file inventories agree. The complete set of 531 named source files, represented by 204 unique byte objects totaling 8,120,054 bytes, was materialized from each restoration and checked exactly. No historical archive is nested in the recovered packet. Previously recorded execution outputs were checked as actual files, and new restored executions were performed. There was no post-replay byte drift.

The review and its verification evidence have their own compact archive and separately read-back byte store. Actual restored replays, including complete generation and certificate semantics under all three Python modes, are required before final sealing. Recovery proves byte reconstruction and executed checks; it does not transform finite evidence into an unbounded nonexistence proof.

The acceptance is limited to the public identities below and the historical companions bound by their unchanged manifests and independent acceptance identities. The general problem remains unresolved, and the lifetime investigation count remains unknown.

## 7. Exact accepted public identities

| File | Bytes | SHA256 |
|---|---:|---|
| ACCEPTANCE.json | 2943 | 56522dbb1d69f9d18dfa4328d83cc159838d780675cb8cfb822905cab200921c |
| CERTIFICATE_GUIDE.md | 4441 | d0ee6aeebb09bc717ac23d38e090519cdbd9cdd91db410959ccd94f70e8732eb |
| ENUMERATION_CERTIFICATE.json | 74754 | 68ad9c22725173b07dec5fe089e1850909a7d3c4f7031f4bbbc1c9ddac2b7c33 |
| FINITE_REPORT.md | 10182 | d0311dba38b69ef3193bd03c707bbe257470575074bd444ae488045dc9a52834 |
| INDEPENDENT_AUDIT.md | 15397 | 6eb034a966ff9137fcf38c36515b0b709b63e368597e3713a557f23ecadd56f9 |
| INTEGRATION_AND_ACCEPTANCE.md | 2924 | c80adc52c81495d66017fa06c0dffa7203d7e54a777c414b2b647bb0bc947114 |
| PUBLIC_MANIFEST.json | 1626 | 15c16cf1d93a85ab5814de808dfff74d8cb33eacf611c85a51250c43a8ed171f |
| README.md | 2990 | 04bb56936f40237e1ef6f9afcd504401c2545ef51fb654f7323afa39e06c83cd |
| SOURCE_IDENTITIES.json | 2144 | 0ede2f8972b0c3d28b8f52c6387c0e56671c77534d20d7b5f59a2120b00b8c70 |
| STRUCTURAL_REPORT.md | 14631 | b6f00b284476162d8c014d390a474da2010d3b86e5ecd94a4ec4638dd41ccc16 |
| VERIFICATION_METADATA.json | 1099 | aa8e046563725635bd19cc693f162e662dac24115c24285c0c504b04e71baafd |

Historical manifest and separate acceptance identities:

| Edition / file | SHA256 |
|---|---|
| 3327_surface_obstruction_reductions_20261012 / PUBLIC_MANIFEST.json | cd42ee4cc48296552f957df78f680e326124f257be5e618b4665c0b331d59483 |
| 3327_surface_obstruction_reductions_20261012 / INDEPENDENT_EDITION_ACCEPTANCE.md | 0023827a56ef7281bb95cd217fed61190905a7cb1b18adc83f72e6b5b3e802ad |
| 3327_square_rotation_frontier_20261012 / PUBLIC_MANIFEST.json | d080c63f0024c49dcf07a98236352268fc8b63b800bf4b088c12ff18a2744547 |
| 3327_square_rotation_frontier_20261012 / INDEPENDENT_EDITION_ACCEPTANCE.md | a0cd29599f5eecfe77d413d76212157ecf699b2819bcf93c46dda9908742a338 |
