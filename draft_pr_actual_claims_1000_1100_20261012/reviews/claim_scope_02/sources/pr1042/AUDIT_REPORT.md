# Edition notice for the complete independent audit

The full original audit follows unchanged. Its PASS is limited to the stated partial results and finite checks; it does not settle the original universal coloring question. The review was an independent AI mathematical audit, not human peer review or formal proof-assistant verification.

The audit's input report had 15,666 bytes and SHA-256 da5d518f1182197e4d3766e5f2628c3c74315298e631c7130b7cc05795d86849. That exact report text is retained after the edition notice in [APPROACH1_REPORT.md](APPROACH1_REPORT.md). Hashes of the complete edition files, including these notices, are listed separately in this edition's [MANIFEST.json](MANIFEST.json).

The audit's references to 21 original files, its input manifest, AUDIT_MANIFEST.json, programs, certificate fixtures, per-move records and computational result files are a historical account of the original review. Those auxiliary files are not supplied here. Its reproduction commands require the original complete research packet and cannot be run from this edition. The prose records their reported checks; it does not make all such checks reproducible from the included files. The PG(2,5) positive coloring and the supplementary local-search examples do not have their full witnesses included. The 15-vertex edge list, starting coloring, histogram and three-vertex repair are present in the report because they were already part of its authored mathematical text.

[SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) and [SOURCE_CHECKS.json](SOURCE_CHECKS.json) retain public source metadata only. [PRECISION_NOTE.md](PRECISION_NOTE.md) states the nonblocking Local Lemma wording clarification separately. The original audit begins below and is preserved as one unchanged byte sequence.

---

# Independent audit: approach 1, problem 30004361

## Verdict and exact scope

**PASS for the explicitly stated partial results. The original universal coloring question remains unresolved.** No mathematical error was found in the reductions, restricted existence results, or finite certificates. This is not acceptance of a full proof or of a counterexample to the target problem.

The audited target is a finite hypergraph with six distinct vertices in every edge and six indexed incident edges at every vertex. Different indexed edges may coincide. A desired coloring is a map into three colors with no color occurring more than three times in any edge. The audit includes the equivalent maximum-degree-six formulation and the report's maximum-degree-three and at-most-eleven-vertices special cases.

The frozen primary report has 15,666 bytes and SHA-256:

`da5d518f1182197e4d3766e5f2628c3c74315298e631c7130b7cc05795d86849`

All 21 entries in the author's `MANIFEST.json` were checked against actual bytes before and after verification. `AUDIT_MANIFEST.json` binds those inputs, the author's manifest itself, and this audit's deliverables. This audit is limited to approach 1; it did not pursue another approach, modify a queue, or publish anything.

## 1. Source identity and conventions

The problem statement and attribution were independently checked in the public [Oberwolfach Report 1/2020](https://ems.press/content/serial-article-files/46836?nt=1), printed page 83 / PDF page 79. The digraph motivation continues onto printed page 84 / PDF page 80. The corresponding question and construction were checked in [Anastos–Lamaison–Steiner–Szabó, Majority Colorings of Sparse Digraphs](https://page.mi.fu-berlin.de/szabo/PDF/MajorityColorings.pdf), page 13, with May 17, 2021 on the title page.

Both passages support the target as restated in the report. Neither inspected passage explicitly requires distinct hyperedges. The digraph construction indexes edges by vertices, and equal underlying sets are possible. Thus retaining indexed-edge multiplicities is appropriate; the regularization equivalence also makes the two universal conventions mathematically equivalent.

The available PDF bytes were independently hashed and exactly match the author's source manifest:

- Oberwolfach PDF: 1,278,806 bytes; `2fb3fa1a0dd303250b210c0cd0605181f0aabe0004f32362e82ed81fa7abb845`.
- Majority Colorings PDF: 562,714 bytes; `41a0a7de780e4f008021ed947d285c9955289c3a08a9e59ac7c86d19ec6a0f79`.

The Brooks citation was checked against the [publisher's bibliographic page](https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/abs/on-colouring-the-nodes-of-a-network/546AD533E0FDCFD02755AC34B0972D0E). The applicable theorem statement was also read in the [public reprint of Brooks' original paper](https://www.tu-ilmenau.de/fileadmin/Bereiche/MN/komgra/BackMatterSMM.pdf), appendix A, first page. Its specialization to maximum degree three and absence of a complete four-vertex component is exactly what the argument needs.

These checks establish statement identity and the cited theorem's applicability. They do not establish a comprehensive current literature status or novelty. The packet only claims that this particular approach leaves the question unresolved and makes no novelty claim for the elementary lemmas. No copied source documents or source passages are included in the audit packet.

## 2. General proof review

### Lemma 1 and Corollary 2: regularization and multiplicities

**Accepted.** The 36-copy construction works over residues modulo six without requiring that six be prime. For each deficit slope `t`, a vertex `(v,a,c)` has exactly one corresponding intercept `b=c-a*t`, so its added degree is exactly the deficit. The first coordinate `v`, then positions `a=0` and `a=1`, uniquely recover an added edge's parameters. The slope lies in `0,...,5`, so equality modulo six is equality of the permitted slope labels. Added edges cannot equal original-copy edges because the former use only one original vertex label while the latter use six distinct original labels.

For each fixed coordinate pair, the copy of the original hypergraph is present and receives a valid coloring by restriction. Deleting repeated indexed edges changes no coloring constraint and does not increase any degree. The implications among simple regular, indexed regular, and maximum-degree-six instances therefore hold. Isolated vertices and an empty starting hypergraph cause no exception.

As a consistency check, the independent verifier tested all 128 simple six-uniform hypergraphs on seven labeled vertices, plus the empty-vertex case, one isolated vertex, and a nonregular eight-vertex example: 131 cases. It checked simplicity, degree six, and recovery of the original hypergraph in all 36 coordinate cells of each completion. These finite tests supplement the general proof; they are not its justification.

### Lemma 3: pairing equivalence

**Accepted.** Keeping pair occurrences makes the multigraph degree exactly the indexed hypergraph degree. A proper three-coloring of the pairing graph limits each color to at most one vertex per pair, hence three per hyperedge. Conversely, in a color-sorted six-vertex list, equal colors form blocks of at most three, so positions differing by three cannot have the same color. The construction is independent in each hyperedge and is unaffected by repeated indexed edges.

The independent checker additionally examined all 729 labeled edge colorings and all 15 perfect matchings of six labeled vertices. It confirmed both the good-coloring pairing and the optimized monochromatic-pair potential identity for every case.

### Proposition 4: maximum degree at most three

**Accepted.** A complete four-vertex component in the underlying simple pairing graph consumes all three degree units at each of its vertices, so its graph edges have no parallel occurrences. In the six-vertex hyperedge supplying a chosen pair from this component, another pair must lie wholly outside the component: at least two hyperedge vertices are outside, and no existing pair crosses a component boundary.

The proposed switch uses four distinct vertices in the same hyperedge and preserves its perfect matching and every multigraph degree. Deleting one edge from the complete four-vertex component leaves it connected. Deleting the outside pair from its component either leaves that component connected or splits it into two pieces containing the two endpoints; the new cross-pairs attach all such pieces. Consequently the two former components merge into one component of at least six vertices. No other component changes, and the number of complete four-vertex components strictly decreases. Finiteness gives termination. The resulting underlying simple graph is three-colorable by the stated Brooks consequence.

No step covers maximum degree four, five, or six; the report correctly preserves that limitation.

### Potential and one-vertex change identity

**Accepted.** At most one color exceeds three in a six-element edge. If that color has size `k>3`, at most `6-k` majority vertices can be matched to minority vertices, leaving at least `k-3` monochromatic pairs. Pairing every minority vertex to a different majority vertex and pairing the remaining majority vertices attains the bound. The good-edge case is Lemma 3.

A move from old color `a` to different color `b` decreases the old-color excess exactly when its previous count was at least four, and increases the new-color excess exactly when its previous count was at least three. Summing over indexed incident edges proves the stated formula. The independent checker verified all 8,748 one-vertex changes among the 729 labeled edge colorings.

### Proposition 5: at most eleven vertices

**Accepted, including repeated indexed edges.** The incidence count gives `m<=n`. The whole vertex set can be partitioned into three classes of size at most three for `n<=9`. For ten vertices, the only possible bad class has size four, giving probability `1/14`; with at most ten edges the union bound is strict.

For eleven vertices and class sizes `(4,4,3)`, the two four-vertex classes are disjoint, so a six-element edge cannot contain both. The bad probability is `1/11`. When there are eleven indexed edges, choose any two distinct edge indices. Their sets intersect in at least one vertex. If the intersection size is at least four, one whole four-vertex color class can lie in that intersection, and the remaining seven vertices can be split into classes of four and three. For intersection sizes at most three, choose a four-subset of the first edge meeting the second edge at most once; the second edge then has at least five vertices available for a disjoint four-subset. This produces a balanced coloring making both edges bad. Repeated equal edges are covered by intersection size six.

The improved union bound subtracting this one positive pairwise intersection is valid pointwise: whenever both selected bad events occur, the sum of all indicators overcounts the union indicator by at least one. This is sufficient even if other intersections also occur. Thus the union probability is strictly less than one.

The independent checker exhausted the two labeled balanced sample spaces:

- Ten vertices: 4,200 partitions; 300 bad for a fixed six-set, exactly `1/14`.
- Eleven vertices: 11,550 partitions; 1,050 bad for a fixed six-set, exactly `1/11`.
- For overlap sizes `1,2,3,4,5,6`, simultaneous bad-event counts were respectively `250,122,48,82,350,1050`, all positive.

This validates the proof's finite arithmetic and strictness, but is not an enumeration of all hypergraphs. The proof itself establishes the entire claimed small-order theorem. A counterexample, if one exists, must have at least twelve vertices.

### Projective-plane counting obstruction

**Accepted.** Incidence counting gives `6s=62+t`. Every pair of selected points lies on a unique line, giving `binom(s,2)=31+2t`. Eliminating `t` yields `s²−25s+186=0` with discriminant `−119`. There is therefore no subset meeting every line in two or three points. Both required incidence properties and the arithmetic were independently verified. The result rules out a stronger preliminary extraction requirement, not the desired three-coloring.

### Elementary Local Lemma calculation

**Accepted in the limited sense stated.** Exhaustion of the 729 assignments gives 73 with a specified color occurring at least four times, and 219 bad assignments in total. Hence the probability is exactly `73/243`. An indexed edge has at most 30 other indexed edges intersecting it, by summing the five other incidences at each of its six vertices. Both the elementary `e*p*31<=1` sufficient criterion and the optimized symmetric criterion `p<=30^30/31^31` fail for this probability and dependency bound.

One minor wording clarification: the report's word “Equivalently” should not be read as claiming the two numerical sufficient thresholds coincide in general. They differ; both fail here, and the optimized criterion was checked separately with exact rational arithmetic. This wording does not invalidate a mathematical conclusion or require changing the frozen packet for scoped acceptance.

## 3. Exact certificate verification

The audit's `verify_independently.py` does not import an author module, trust a solver status, use floating-point arithmetic, or rely on Python assertions. It reads but does not modify the frozen inputs. Both normal and optimized Python executions produced identical output.

For all four local-search examples it independently checked six distinct vertices per edge, valid integer vertex and color domains, distinct hyperedges, exactly six incident edges per vertex, every stored degree, initial potential one, all expected moves exactly once, every stored move's delta, and the supplied valid coloring.

| Certificate | Vertices | Move class | Moves checked | Delta histogram |
|---|---:|---|---:|---|
| `local_minimum.json` | 12 | Single-vertex recolor | 24 | `0:13, 1:10, 2:1` |
| `swap_minimum_411.json` | 12 | Nontrivial color swap | 48 | `0:29, 1:12, 2:6, 3:1` |
| `combined_minimum_15.json` | 15 | Single recolor or swap | 105 | `0:48, 1:38, 2:14, 3:5` |
| `two_vertex_minimum_15.json` | 15 | Every recoloring at distance one or two | 450 | `0:52, 1:89, 2:110, 3:76, 4:71, 5:34, 6:16, 7:2` |

All 627 stored move records match independent recomputation. The strongest certificate includes 30 one-vertex changes and 420 exact-two-vertex changes. It is a **non-strict** local minimum: 52 of the 450 moves are neutral. The report's edge list was parsed and compared directly with the certificate. Its initial coloring, first-edge counts `(4,2,0)`, and absence of any other bad edge agree.

Changing vertex 0 to color 1 and vertices 7 and 9 to color 0 yields potential zero. This coloring is at Hamming distance three from the starting coloring. Since potential one at distance zero and the exhaustive checks exclude valid colorings at distances one and two, the exact minimum distance is three. The separate valid coloring stored in the JSON is also correct. The earlier combined recolor/swap example has a valid arbitrary two-vertex repair, also checked, so the move classes are not conflated.

For `projective_plane_5.json`, the audit generated projective representatives by normalizing all 124 nonzero vectors, independently of the author's filtering implementation. It then checked all 31 point representatives, all 31 dot-product line edges, six incidences per point and line, all 465 line pairs, and all 465 point pairs. It checked the valid coloring, class sizes `(11,10,10)`, and every stored three-color edge-count vector.

`swap_minimum.json` contains only an exploratory solver infeasibility status. It is not an exact nonexistence certificate and is not mathematical evidence for this audit. Neither the accepted report nor this audit relies on it. Search generators were not rerun: finding a certificate again is unnecessary once its finite claimed properties have been exhaustively checked.

## 4. Author checker reruns and reproducibility

The author's checkers were rerun in a temporary copy of the frozen packet because `verify_certificates.py` writes witness and result files. The original packet was never rewritten. All three invocations exited zero with empty stderr:

1. `python verify_certificates.py`
2. `python verify_bitsets.py`
3. `python -O verify_bitsets.py`

Their outputs matched the saved expected outputs byte for byte. The temporary copy's 21 files still matched the original manifest after the run, and the source packet also remained unchanged. The rerun environment used Python 3.12.14. The main author checker uses assertions and should be run normally as documented; the bitset checker and this audit's checker use explicit checks that remain active under optimization.

From this audit directory, reproduce the independent results with:

`python verify_independently.py`

The same output is produced by `python -O verify_independently.py`. To reproduce the isolated author reruns, use:

`python rerun_author_checkers.py`

`INDEPENDENT_RESULTS.json` records the independent checks. `AUTHOR_RERUN_RESULTS.json` records author-checker exit codes and byte-level output matches. `SOURCE_CHECKS.json` records public-source inspection and PDF hash matches. `AUDIT_MANIFEST.json` binds the exact input and audit files.

## 5. Acceptance boundary

Accepted: the regularization equivalence, pairing equivalence, degree-three theorem, at-most-eleven-vertices theorem, potential and recoloring identities, all supplied positive coloring certificates, the exact two-vertex local-search obstruction, the projective-plane extraction obstruction, and the limited probabilistic calculation.

Not established: the full six-regular/six-uniform coloring assertion; a counterexample to it; a general theorem guaranteeing three-vertex repairs or successful neutral-move paths; global failure of the Local Lemma; exhaustive classification beyond the finite certificate neighborhoods; or novelty/current literature completeness.

The correct final mathematical status remains **unresolved after approach 1, with verified partial results and a verified obstruction to a particular strictly decreasing local-search method**.
