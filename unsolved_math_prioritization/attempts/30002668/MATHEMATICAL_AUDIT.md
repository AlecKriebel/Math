# Independent mathematical audit: three-color dual-path partial result

Problem 30002668 / OWR-13110-017. Audit date: 10 October 2026.

## Decision and precise scope

**ACCEPT the quadratic local-cycle packing theorem and its stated auxiliary lemmas as a partial result, with the source-scope correction supplied in REPORT_CORRECTION.patch. DO NOT ACCEPT a solution of the quadratic single-path target.** The public mathematical report already incorporates this correction.

The only required prose correction is in Section 4.1: the cited Hoffmann–Kleist–Miltzow Theorem 2 is stated for every **odd** positive integer k. The replacement retains this restriction. That infinite subsequence already disproves the proposed color-insensitive joining inference, so this correction does not change the partial theorem or its limitations.

The exact open target under examination is a uniform c > 0 and n0 such that every arrangement, for every n >= n0, of n red, n blue and n green lines in general position has a face-simple dual path with at least c n² edges and unequal consecutive colors. General position here excludes both parallel pairs and triple concurrence. A supporting line may be crossed more than once. No periodic RGB order is imposed. No counterfamily to this exact target, and no proof of this target, is accepted by this audit. No novelty or exhaustive literature-status conclusion is made.

## 1. Review status and the mathematical/evidentiary boundary

This is an independent internal AI mathematical and source-scope audit of an AI-assisted note. Both documents are unrefereed. No external human peer review, journal acceptance of these authored documents, or formal proof-assistant certification is claimed. Acceptance applies only to the stated partial result. Document integrity and finite-test success do not substitute for the uniform mathematical argument below.

The supplementary diagnostics checked fourteen finite fixtures in normal, -O, and -OO Python modes, including 168 deleted-line zones and 15 semantic mutation types in each mode. The public source metadata record inspected versions, PDF hashes and byte counts, and retrieval/inspection history. Edition preparation does not constitute a fresh visual source inspection. Published results are credited external dependencies within the stated scope; neither the cited two-color obstruction nor the planar zone theorem is independently reproved here.

## 2. What is counted

Write N for the number of geometric lines. M is the number of intersections of lines with different colors, not the number of dual edges, faces, all crossings, or chosen cycles. In general position each unordered pair of differently colored lines contributes exactly one different point.

For every two-dimensional arrangement face f, bounded or unbounded, d(f) counts the genuine arrangement boundary edges. Rays count; artificial edges at infinity do not. In this setting d(f) also equals its dual-graph degree. A convex cell cannot have two distinct boundary edges supported by the same geometric line: its intersection with that line is connected, and any other arrangement line meeting the relative interior would cut the cell rather than preserve that supporting boundary. Thus it occurs once in the incidence sum for each of exactly d(f) supporting lines.

Let S = sum_f d(f)², with the sum over **all** faces. Let t(f) count mixed-color arrangement vertices incident with f. For bounded cells the total finite-vertex count equals d(f); for unbounded cells it is d(f)-1. Therefore t(f) <= d(f) in both cases. Omitting unbounded faces would invalidate the conflict accounting and the subsequent line-incidence identity.

## 3. Local cycles and their conflicts

At a crossing v of differently colored lines a and b, general position supplies a sufficiently small disc meeting no other line. The four sectors have four different sign pairs relative to a and b. A global arrangement face has a fixed sign for every line, so these sectors belong to four different global faces. Each consecutive sector pair shares a nonzero portion of an arrangement edge. The four dual edges therefore form a genuine face-simple four-cycle with cyclic color word a,b,a,b. The closing edge is also differently colored from each of its neighbors.

Index these cycles by their mixed crossings. Different crossings cannot represent the same four-cycle: its two varying sign coordinates identify its supporting lines and their unique intersection. Build a simple conflict graph H on these M indexed objects; an edge records a shared dual vertex. Whenever two cycles conflict, their arrangement crossings both occur on the boundary of a common face. A face with t(f) such corners witnesses at most binomial(t(f),2) conflict pairs. Pairs witnessed by more than one face may be counted repeatedly, which increases an upper bound and is harmless. Hence

2|E(H)| <= sum_f t(f)(t(f)-1) <= S.

Select every vertex preceding all its neighbors in a uniformly random total ordering of H. Adjacent vertices cannot both be selected. The expected independent-set size is sum_v 1/(deg_H(v)+1). Cauchy–Schwarz gives

alpha(H) >= sum_v 1/(deg_H(v)+1) >= M²/(M+2|E(H)|) >= M²/(M+S).

An independent set selects pairwise vertex-disjoint dual cycles. The statement that an integer packing size is at least a real bound is legitimate: existence of an independent set at least its expectation establishes it. M > 0 avoids the vacuous zero-denominator case. The proof does not assert that a particular greedy heuristic always attains this lower bound; the submitted finite greedy certificates separately attain the bound on their actual fixtures.

## 4. Uniform squared-degree bound from zones

The inspected Edelsbrunner–Seidel–Sharir scan defines zone complexity as the sum of complexities of cells intersected by the query hyperplane, with a cell's complexity including its boundary faces. In dimension two this bounds the sum of boundary-edge counts of all cells cut by a line by C_z m for an absolute constant C_z. Its definition counts cell incidences; it is not merely a count of distinct edges in the union. It includes unbounded cells. Fix dimension two and enlarge the constant, if needed, for the finitely many small m; then one C_z works for every m >= 1 and every arrangement.

Remove a line ell from the N-line arrangement. The remaining N-1 crossings on ell are distinct. The N open intervals/rays between them lie in N different old cells: convexity prevents leaving and re-entering an old cell along a straight line. The query is transverse and misses every remaining vertex, as required here.

In a crossed old cell F, adding ell creates two cells F+ and F-. Every old boundary edge belongs to at least one of them. Only edges containing one of the at most two finite endpoints of ell intersected with the cell can be split. Each such split increases the combined old-edge count by one; the new segment or ray counts once for each child. Thus

d(F+) + d(F-) <= d(F) + 4.

This is valid for unbounded end cells as well; a missing finite endpoint decreases the possible increment. No artificial projective edge is inserted. All cells incident to a boundary edge on ell are exactly these children, and each child belongs to a unique old parent. Therefore

sum_{f incident to ell} d(f) <= C_z(N-1) + 4N <= (C_z+4)N.

Sum this over all N supporting lines. The incidence fact in Section 2 yields the exact identity

sum_ell sum_{f incident to ell} d(f) = sum_f d(f)².

Consequently S <= C N² with C = C_z+4 absolute. This source-based estimate is a complete uniform argument; it is not inferred by fitting a constant to finite examples. It includes N=2, where the deleted arrangement consists of one line and the unbounded-cell interpretation still applies.

## 5. Balanced specialization and what it does not prove

For n lines in each of three colors, N=3n and M=n²+n²+n²=3n². Therefore

packing size >= 9n⁴/(3n²+9Cn²) = n²/(C+1/3).

Thus the claimed Omega(n²) vertex-disjoint proper four-cycles follow uniformly over all the already-colored arrangements in the target's hypothesis. Removing one edge from each gives the same number of disjoint three-edge proper paths. Total length across many components must not be called the length of one path.

With the source restriction restored, [3, Theorem 2] supplies arrangements for every odd k with 3k lines of one color, 2k of another, and proper simple paths of length at most 14k. The packing argument nevertheless gives at least 36k²/(6+25C) disjoint proper local cycles there. Every face on one of these cycles is bichromatic, and [2, Lemma 3.1] supplies pairwise alternating connectivity between bichromatic faces. The odd subsequence alone proves that these two properties cannot imply a uniform quadratic simple alternating path in arbitrary two-color arrangements.

This adverse comparison is source-dependent: the cited arrangement construction is not independently reconstructed in this audit. It has two colors and unequal classes, so it is not a counterexample to the balanced three-color target. Pairwise reachability neither provides internally disjoint connectors nor controls connector endpoint colors. A joining theorem using a further balance-sensitive three-color property is still missing.

## 6. State lift and erasure counterexample

For y=x+1, y=2x+4, y=3x+9 colored R,B,G, respectively, a face's bit i records the positive sign of y-a_i x-b_i. The reported face walk

4, 0, 1, 3, 2, 0, 4

is a genuine dual walk with word G,R,B,R,B,G. Its lifted states

(4,R), (0,G), (1,R), (3,B), (2,R), (0,B), (4,G)

are all different and satisfy every transition rule, including the initial transition. Faces 0 and 4 repeat. Erasing the subwalk between the two visits to 0 leaves 4,0,4 with word G,G, which loses proper coloring and still repeats 4. Fully erasing the closed walk destroys its length. This is a counterexample to automatic projection and to that local erasure operation, not a proof that every erasure fails, not a hard asymptotic arrangement, and not a claim that no alternate simple path exists. The independently rebuilt geometric graph confirms all of these finite statements.

## 7. The 3n single-path guarantee

The original problem's edge-count convention agrees with [2]'s introduction: path length is the number of transitions, one less than the number of faces, and no face is repeated. Theorem 3.2 on printed page 328 gives length N for any nonmonochromatic two-color arrangement of N lines. Its preceding antipodal-cell argument explicitly requires crossing every supporting line, resolving any possible abstract-level off-by-one ambiguity.

Coarsen blue and green to one color and retain red as the other. The arrangement is unchanged and remains general-position and nonmonochromatic. The resulting face-simple alternating path has at least N=3n edges; its edges from different coarsened classes necessarily have different original colors. This valid source-derived lower bound neither uses balanced two-color classes nor claims a quadratic improvement. Trying three coarsenings does not supply such an improvement.

## 8. Insertion lemma and its limit

A face-simple path can be realized by selecting an interior point on every crossed arrangement edge and joining successive points by segments in the corresponding convex old cells; choose endpoints in the first and last cells. Choose the crossing points generically away from the newly added line ell, and avoid a path segment lying on ell. Every old face is used once, so the entire route within it crosses ell at most once and visits at most two refined faces. Refined faces in different old faces cannot coincide. No old crossing is lost.

If ell's color is absent from the old arrangement, an inserted ell-crossing differs in color from each neighboring old crossing. Consecutive old crossings not separated by ell remain properly colored. The refined path is face-simple, proper, and at least as long. A zero-edge original path is immediate. Thus Proposition 4 is valid as stated.

After the first new-color line is added, another line of that color no longer satisfies the lemma's hypothesis. Inside a fixed old cell, specified endpoints can lie on opposite sides of each of two newly inserted green lines; any route kept inside that old cell must then have at least two green crossings and no old-color crossing between them. This defeats the stated facewise refinement mechanism. It does not prove a general non-monotonicity theorem or a balanced three-color counterexample, and the report appropriately does not claim either.

## 9. Independent finite and integrity checks

A fresh implementation reconstructs every arrangement edge directly: for each input line, it sorts its exact rational intersection parameters and samples every intervening segment and both rays. The signs of all other lines identify the two incident faces. This does not import either submitted implementation, perform polygon clipping, or infer all edges solely by pairwise comparison of a precomputed face list.

For all fourteen fixed fixtures, the implementation checks the complete dual graph, N(N+1)/2+1 faces, N² edges, 2N unbounded faces, finite-corner versus edge incidence, local cyclic coloring, mixed-crossing identities, all conflict pairs, the Cauchy bound, reported statistics, and every supplied packing certificate. For every deleted supporting line it additionally reconstructs the old arrangement and verifies the N-cell zone, each split-parent degree inequality, and the summed squared-degree identity. These are supplementary finite diagnostics only; no longest-path search or new asymptotic target search is performed.

Semantic mutation controls reject missing faces and edges, altered local cycles or counts, duplicate packing choices, wrong color balance, falsified scope and state-lift data, face-repeating paths, diagonal jumps, same-color successive crossings, parallel lines, and triple concurrence. A proper R,B,R path crossing the same geometric line twice is accepted. The independently written verifier and mutation harness use explicit exceptions, not Python assert statements, and are run in normal, -O, and -OO modes. Separate byte-level controls exercise the externally anchored inventory. Exact counts and hashes are recorded in the acceptance metadata.

## References and inspection scope

[1] Discrete Geometry, Oberwolfach Reports 40/2014. Open problems collected by Tillmann Miltzow. The exact question and color convention were visually inspected on printed page 2288 / PDF page 54; the separate contribution is on printed page 2262 / PDF page 28. DOI: https://doi.org/10.4171/OWR/2014/40 . PDF: https://ems.press/content/serial-article-files/46530 .

[2] Oswin Aichholzer et al. Cell-paths in mono- and bichromatic line arrangements in the plane. DMTCS 16:3 (2014), 317–332. Definitions inspected on printed pages 317–318; Lemma 3.1, Theorem 3.2, and surrounding argument on pages 328–329, including a fresh visual check of PDF page 12. DOI: https://doi.org/10.46298/dmtcs.2088 . PDF: https://dmtcs.episciences.org/articles/2088/download .

[3] Udo Hoffmann, Linda Kleist, Tillmann Miltzow. Upper and Lower Bounds on Long Dual-Paths in Line Arrangements. arXiv:1506.03728v1, 11 June 2015. Theorem 2 and its odd-k restriction visually inspected on printed page 13 / PDF page 14, with the construction discussion read through printed page 15. Definitions and distinct random-coloring quantifiers inspected in the introduction. No journal-final text is represented as inspected. https://arxiv.org/abs/1506.03728v1 ; PDF: https://arxiv.org/pdf/1506.03728v1 .

[4] Herbert Edelsbrunner, Raimund Seidel, Micha Sharir. On the Zone Theorem for Hyperplane Arrangements. SIAM Journal on Computing 22:2 (1993), 418–429. The cell/zone complexity definitions and Zone Theorem were visually inspected on printed page 418 / PDF page 1 of the author-hosted scan. DOI: https://doi.org/10.1137/0222031 . PDF: https://pub.ista.ac.at/~edels/Papers/1993-02-OnZoneTheorem.pdf .

No copied source text, source PDF, dataset contents, or private coordination record is part of the candidate-public audit set.
