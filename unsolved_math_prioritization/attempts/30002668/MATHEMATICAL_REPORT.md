# Balanced three-color dual paths: partial result

Problem 30002668 / OWR-13110-017. Mathematical status: **PARTIAL; THE QUADRATIC SIMPLE-PATH TARGET IS UNRESOLVED.**

## Review status of this edition

This is an AI-assisted mathematical note with an independent internal AI mathematical audit. Both are unrefereed. No external human peer review, journal acceptance of these authored documents, or formal proof-assistant certification is claimed. Acceptance concerns only the explicitly stated partial results. Published theorems retain their original authors' credit and remain external dependencies; the cited two-color obstruction and planar zone theorem are not independently reproved here. The correction in REPORT_CORRECTION.patch is already incorporated below.

## 1. Exact target and conclusion

Let A be any already-colored arrangement of N = 3n distinct real affine lines, exactly n in each of red, blue, and green. Assume that every pair intersects and no three are concurrent. The target is an absolute c > 0 and integer n0 such that, for every n >= n0 and every such A, the dual graph has a simple path of at least c n² edges on which successive edge colors differ.

A dual vertex is an arrangement face. Simplicity forbids repeating a face, rather than repeating a supporting geometric line. The color word need only have unequal adjacent entries; it need not follow a cyclic RGB order. The total face count is (3n)(3n+1)/2 + 1, so a quadratic upper bound is automatic. The unresolved part is the uniform quadratic lower bound.

This report establishes a different, precisely delimited fact: A contains Ω(n²) pairwise vertex-disjoint properly colored dual four-cycles. It gives an arrangement-specific packing bound and a complete deduction from the classical planar zone theorem. It does **not** join those cycles into one path. The single-path lower bound justified here remains the source-derived bound 3n. Neither a proof of the target nor a violating balanced three-color family has been found. The partial statements below are not asserted to be novel.

## 2. Source scope

The original question is Miltzow's Problem 1 in the open-problem session of OWR 40/2014, printed page 2288, PDF page 54 [1]. Its short definition expressly permits any adjacent-unequal color word. The contribution on printed page 2262, PDF page 28, concerns uncolored paths, a two-color obstruction, and random coloring; it is a separate result.

Aichholzer et al. define cell-paths as face-simple sequences and measure length in crossed edges [2, introduction]. Their Theorem 3.2, printed page 328, supplies the linear lower bound used below. Their Lemma 3.1 supplies alternating connectivity between bichromatic faces.

The inspected Hoffmann–Kleist–Miltzow body is arXiv:1506.03728v1, dated 11 June 2015 [3]. It is treated as that manuscript, not as an inspected journal-final text. Its Theorem 2 and Section 3 give the 3:2 two-color family used only as an adverse control; Section 4's favorable random-coloring result has different quantifiers from the target.

The additional geometric input is the zone theorem of Edelsbrunner, Seidel, and Sharir [4, printed page 418]. Its two-dimensional specialization is all that is used. A bounded current search on 10 October 2026 did not identify a source resolving the exact target. This is a search outcome, not a certificate of exhaustive literature coverage, openness, or novelty.

## 3. Quadratic local-cycle packing

### Notation

For a face f of an arrangement of N >= 2 lines, let d(f) be its number of arrangement boundary edges, including unbounded edges but no artificial edge at infinity. Let

S(A) = sum over faces f of d(f)².

Color the lines with any finite set of colors, and let M be the number of intersection points at which the two supporting lines have different colors. The following proposition is not restricted to three colors or to balanced classes.

### Proposition 1: an exact packing bound

If M > 0, the dual graph contains at least

M² / (M + S(A))

pairwise vertex-disjoint properly colored four-cycles. The assertion means that the integer packing size is at least this real lower bound. A slightly stronger bound is M²/(M + 2e), where e is the edge count of the conflict graph defined in the proof.

**Proof.** At each differently colored crossing v, a sufficiently small disc meets only its two supporting lines. Its four sectors lie in four distinct faces: their signs with respect to the two lines are distinct. Consecutive sectors share an arrangement edge. Thus these four dual vertices form a four-cycle Q_v, with edge colors a,b,a,b and a != b.

Make a simple conflict graph H whose M vertices are these crossings; join v and w when Q_v and Q_w share a dual vertex, equivalently when v and w occur on the boundary of one arrangement face. If t(f) is the number of these M crossings on the boundary of f, then t(f) <= d(f). For bounded cells the total number of boundary vertices equals d(f); for unbounded cells it is smaller, so the inequality still holds. Hence

2e(H) <= sum_f t(f)(t(f)-1) <= sum_f d(f)² = S(A).

Multiple shared faces only overcount a pair, which is harmless in this upper bound.

Give the vertices of H a uniformly random total ordering and choose every vertex that precedes all its neighbors. The chosen set is independent. A vertex of degree delta is chosen with probability 1/(delta+1). Therefore some independent set has size at least

sum_v 1/(deg_H(v)+1) >= M² / sum_v (deg_H(v)+1)
= M² / (M+2e(H)) >= M² / (M+S(A)),

where the middle inequality is Cauchy–Schwarz. Independent vertices of H give the required vertex-disjoint cycles. QED.

The assertion is a packing theorem, not a claim about the length of one cycle. Deleting one edge from each selected four-cycle instead gives equally many vertex-disjoint proper three-edge paths. Their aggregate length is quadratic in the balanced case; it is not the length of one path.

### Lemma 2: the relevant sum-of-squares estimate

There is an absolute constant C such that S(A) <= C N² for every simple arrangement of N >= 2 lines.

**Proof from the planar zone theorem.** Use the standard planar zone theorem in the following weaker form: for an arrangement of m >= 1 lines, the sum of the numbers of boundary edges of all cells cut by another line is at most C_z m, for an absolute C_z. This follows from [4], whose cell-complexity count includes these edges.

Fix one line ell of A and remove it. The remaining N-1 lines meet ell in N-1 distinct points, so ell passes through exactly N old cells. For an old cell F crossed by ell, inserting ell splits it into two cells F+ and F-. At most two old edges are split, and the newly inserted segment or ray contributes one boundary edge to each side. Consequently

d(F+) + d(F-) <= d(F) + 4.

This argument also covers the two unbounded end cells: there can be fewer than two split old edges, which only improves the inequality. All new cells having an edge on ell arise this way. Thus

sum_{f having an edge on ell} d(f) <= C_z(N-1) + 4N <= (C_z+4)N.

Every cell is convex. A supporting arrangement line therefore accounts for at most one of its boundary edges. A cell with d(f) edges appears in the last sum for exactly d(f) different choices of ell. Summing over the N arrangement lines gives

sum_f d(f)² <= (C_z+4)N².

Take C=C_z+4. No numerical value of the zone constant, and no computational fit for such a constant, is being claimed. QED.

### Corollary 3: balanced three-color packing

For n lines of each of three colors, every red-blue, red-green, and blue-green pair has a distinct crossing, so M=3n² and N=3n. Propositions 1 and Lemma 2 give a packing of size at least

9n⁴ / (3n²+9Cn²) = n²/(C+1/3).

The constant is absolute. The conclusion is uniform over all already-colored arrangements satisfying the hypotheses. There are consequently Ω(n²) distinct faces lying on these proper local cycles.

This establishes an abundance of disjoint usable local pieces. It does not establish compatible, disjoint connecting routes between them.

## 4. Why the joining step remains a genuine gap

### 4.1 A known geometric adverse control

For every odd positive integer k, consider the source-credited simple arrangement of [3, Theorem 2]: 3k lines of one color and 2k of another, with every proper simple dual path of length at most 14k. The infinite odd-k subsequence suffices for the adverse comparison below. Here N=5k and M=6k². The same packing proof gives at least

36k²/(6+25C)

vertex-disjoint proper dual four-cycles. Moreover, [2, Lemma 3.1] supplies an alternating path between any two bichromatic faces. Thus even within actual line arrangements, a quadratic packing of proper local cycles and pairwise alternating connectivity do not, by themselves, imply a quadratic simple alternating path.

This is not a counterexample to the question: the family has two colors and the wrong balance. It falsifies only a color-insensitive joining principle based on those two inputs. A successful three-color proof must use a genuinely additional feature of all three balanced classes. This report does not supply such a feature or reconstruct the cited obstruction independently.

### 4.2 A finite state lift does not preserve face simplicity

A natural auxiliary digraph has states (f,c), meaning that the walk is at face f after crossing color c. A transition (f,c) -> (g,d) is allowed when f and g share a d-colored edge and c != d. Directed walks project to properly colored dual walks. However, a simple directed path in this auxiliary graph can use (f,R) and (f,B), thereby repeating the original face f.

This failure occurs already in a balanced three-line arrangement. Take

ell_0: y=x+1, color R;
ell_1: y=2x+4, color B;
ell_2: y=3x+9, color G.

Represent a face by the binary mask of the lines above which a point of the face lies. The masks 4,0,1,3,2,0,4 form a dual walk with color word

G,R,B,R,B,G.

Every adjacent pair of colors differs. The corresponding state sequence, beginning with the auxiliary state (4,R), is

(4,R),(0,G),(1,R),(3,B),(2,R),(0,B),(4,G).

All seven states are distinct, but faces 0 and 4 repeat. Deleting the intervening four-cycle between the two appearances of face 0 leaves the two-edge word G,G; that local loop erasure loses proper coloring. Erasing the entire closed walk leaves no useful path length. An ordinary state-graph path theorem therefore cannot be projected without a separate quantitative face-simplicity argument. These facts are verified using exact rational geometry in the diagnostics.

This example neither obstructs the original asymptotic target nor asserts that its endpoints cannot be joined by some proper simple path. It invalidates the specific automatic projection and local-erasure steps.

## 5. Two further mechanisms and their limits

### 5.1 Coarsening colors: a valid linear guarantee

Merge blue and green into one color and retain red as the other. Apply [2, Theorem 3.2] to the resulting nonmonochromatic arrangement of 3n lines. It has a proper simple dual path of length at least 3n. Successive edges of that path belong to different merged classes, and hence also have different original colors. Thus the original arrangement has such a path of length at least 3n.

This is an immediate application of an existing theorem, not a newly improved path bound. The merged class sizes are n and 2n; neither the balanced two-color question nor a favorable recoloring theorem applies. Taking three possible coarsenings does not prove that one contains a quadratic path.

### 5.2 Inserting one entirely new color

**Proposition 4.** Suppose a properly colored simple dual path exists in an arrangement A. Add a line ell, in general position with A, whose color did not occur in A. The refined arrangement has a properly colored simple dual path of at least the old length.

**Proof.** Realize the old path by choosing points in the relative interiors of its crossed edges and joining successive points through each intervening old face. Choose these points generically so they avoid ell. Since every old face is convex, the portions inside it can be chosen as segments, each crossing ell at most once. Endpoints are chosen in the initial and final old faces. The refined path therefore visits at most two refined faces inside any one old face; each old face was visited just once, so no refined face repeats. At most one edge of the new color is inserted between two consecutive old crossed edges. Its color differs from both; unchanged successive old colors were already distinct. The refined path is proper and retains every old crossing. QED.

This insertion lemma helps only for the first line of an entirely new color. Repeating it for the remaining green lines violates its hypothesis. With two green lines inside one old face, specified entry and exit points can be separated by both lines. A route confined to that face then has to cross two green edges without an old-color edge between them. No general simultaneous insertion argument was proved. This route is recorded as blocked at precisely that step, rather than used as an implicit induction.

## 6. Deterministic finite checks

The diagnostics construct actual arrangements with rational arithmetic, clip cells against a sufficiently large square containing every intersection, and recover the dual graph using feasible sign masks. Two differently colored crossing lines define the four local faces directly. All geometry is exact; no tolerance, numerical perturbation, or floating-point general-position test is used.

Fourteen fixtures were checked:

- The 3n lines y=ax+a², a=1,...,3n, for n in {1,2,3,4,6,8}, with both contiguous color blocks and interleaved RGB colors.
- Two further balanced arrangements of 12 integer-coefficient lines with deterministic seeds 1374 and 2668, rejecting any triple concurrence.

The independent checker reconstructs feasible face masks from all pairwise intersections instead of polygon clipping. It independently rebuilds dual edges, mixed-crossing cycles, conflict edges, squared face degrees, and the stated packing certificates. It checks the exact face count N(N+1)/2+1 and edge count N².

For the 24-line fixtures, M=192. The certified greedy packings have 48 and 57 disjoint four-cycles. These are feasible packing sizes, not claimed optima. The two additional 12-line examples have 17 and 16 cycles. Every fixture checks the conflict inequality and certificate disjointness. None computes the exact longest simple proper path, and none extrapolates a path bound to all n.

Adverse checks reject a repeated face, a nonadjacent face jump, two successive distinct supporting lines of the same color, a parallel pair, and triple concurrence. Positive checks accept a proper three-edge path that crosses the same supporting line twice and has word R,B,R, deliberately excluding both an erroneous line-simple rule and an erroneous periodic-RGB rule. The lifted-path counterexample in Section 4.2 is independently replayed.

## 7. Remaining target and decision

The exact missing step is a three-color, balance-sensitive mechanism that selects and connects Ω(n²) local progress into one face-simple properly colored path, or a counterfamily showing that no such mechanism can always succeed. Local density, cycle packing, pairwise reachability, random favorable coloring, and a simple path in a finite color-state lift each leave that step unjustified.

The conclusion of this report is partial. There is no candidate proof of the original claim to accept. No claim of independent external mathematical audit or novelty is made. The diagnostics and integrity verification test the stated finite artifacts; they are not a formal verification of an all-n solution.

## References

[1] Discrete Geometry, Oberwolfach Reports 40/2014, open problems collected by Tillmann Miltzow, printed pp. 2262 and 2288. DOI: https://doi.org/10.4171/OWR/2014/40 . Inspected PDF: https://ems.press/content/serial-article-files/46530 .

[2] Oswin Aichholzer, Jean Cardinal, Thomas Hackl, Ferran Hurtado, Matias Korman, Alexander Pilz, Rodrigo I. Silveira, Ryuhei Uehara, Pavel Valtr, Birgit Vogtenhuber, and Emo Welzl. Cell-paths in mono- and bichromatic line arrangements in the plane. DMTCS 16:3 (2014), 317–332. https://doi.org/10.46298/dmtcs.2088 . Inspected journal PDF: https://dmtcs.episciences.org/articles/2088/download .

[3] Udo Hoffmann, Linda Kleist, and Tillmann Miltzow. Upper and Lower Bounds on Long Dual-Paths in Line Arrangements. arXiv:1506.03728v1 (2015). https://arxiv.org/abs/1506.03728v1 . Inspected manuscript PDF: https://arxiv.org/pdf/1506.03728v1 .

[4] Herbert Edelsbrunner, Raimund Seidel, and Micha Sharir. On the Zone Theorem for Hyperplane Arrangements. SIAM Journal on Computing 22:2 (1993), 418–429. https://doi.org/10.1137/0222031 . Inspected author-hosted scan: https://pub.ista.ac.at/~edels/Papers/1993-02-OnZoneTheorem.pdf .
