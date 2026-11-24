# Independent acceptance audit: weak pentagon continuation, round one

Audit date: 12 October 2026 UTC.

## Verdict and limits

**ACCEPT the expressly restricted mathematics in the frozen candidate.** No mathematical correction was found. The finite calculations were independently reconstructed and agree with the candidate. In particular, the equality case in Lemma 4.2 is valid, and the overlapping-arm cases needed in Theorem 6.1 are genuinely covered.

The acceptance does **not** establish the triangle-free cubic Clebsch conjecture, the fixed-global-maximum-cut strengthening, literature novelty, a complete current literature frontier, or independent correctness of any cited paper's entire proof or computer-assisted certificate. The 19/8 corollary is an elementary, strictly weaker consequence of a known 12/5 result with target C5.

There is one reproducibility limitation requiring explicit disclosure: the submitted Python verification suite uses `assert`. Under `python -O` or `python -OO`, those assertions are removed. Optimized runs of that original script reproduce its output but are **not verification runs**. Acceptance here instead rests on the written proofs, an independent fail-closed checker, normal-mode execution of the original suite, and semantic/input-integrity controls in all three interpreter modes. The original packet has not been modified.

An optional hardened replacement preserves all submitted checks as explicit runtime conditions active in every mode and reproduces the frozen results byte-for-byte. The audit retained the exact hardening changes. This is a checker-hardening correction, not a mathematical proof correction. Neither the program nor its patch is distributed in this prose edition.

## Exact input boundary

All five entries of the original input manifest were verified before testing. The independent checker embedded fixed identity pins for that manifest and the original authored proof, then checked every listed byte length and hash. Its success was therefore tied to the frozen input rather than to a later unpinned replacement. Historical undistributed input identities are omitted here.

For this edition, the corresponding distributed proof is [THEORY.md](THEORY.md), 23,168 bytes, SHA-256:

`78acbe195252f92b5ac4dbc71c6f57466b36eb5f42ce9c523d34679fbc4a9ce1`

This is the identity of the editorial edition, not a claim that the earlier audit ran against revised bytes. Its changes reconcile completed audits, scope disclosures and reader references; the complete mathematical proof-review body below is retained. The actual distributed files are bound by this edition's public manifest. A later changed edition requires reconciliation against its changes.

No original author's program for the girth-17 theorem was executed. No remote repository action was performed. Source documents are not included in this audit's deliverable files.

## Proof review

### 1. Conventions and the model

Finite, simple, undirected graphs are explicitly assumed. Homomorphisms may identify nonadjacent vertices and need not preserve nonedges. The coloring is not assumed proper, and empty color classes are permitted. These conventions are sufficient for every argument below. For a bipartite edge subgraph, containment in a cut does not by itself imply equality with a cut; the candidate correctly distinguishes these notions.

The five generators in F2^4 have only the empty and all-five dependencies. This proves that any four are a basis and that every permutation of the five generators induces an invertible linear map. Translations preserve differences. The quotient-of-the-five-cube identification follows by mapping its five coordinate generators to these five vectors: the kernel is the span of the all-ones vector, so quotienting identifies antipodes.

### 2. Cycle parity, cut complements, and normalization

Lemma 2.1 is valid. Summing edge differences around a cycle gives the sole dependency alternatives, so all five color counts have the same parity. Conversely, the assumed parity makes every simple cycle sum zero. Every closed walk has a cycle-space decomposition modulo two, so root-path sums are independent of the chosen path and produce a homomorphism. On a cycle, summing five equal parity bits recovers the cycle-length parity. Fundamental cycles suffice because the edge-sum condition is linear over F2.

The linear functional for color 5 is the sum of all four coordinates. For color i at most 4 it is the sum of the other three coordinates. It takes value zero on generator i and one on every other generator. Thus the four-color complement is exactly the cut defined by that functional. This is an explicit cut certificate, not an arbitrary choice of bipartitions of disconnected complement components.

Theorem 3.1 is valid for every original witness and every independent choice of the four complementary bipartitions. For an original color j at most 4, the three other coordinates flip, whereas coordinate j may or may not flip. The difference is therefore J or J+e_j. For color 5 all four flip. The map T(x)=x+(sum x_i)J is an involution because the parity of J is zero; it fixes J and sends J+e_i to e_i. It follows that only moves from a color at most 4 into color 5 occur.

Every odd cycle in an original witness contains every color, since a missing color would leave the whole odd cycle in a bipartite complement. A pentagon is consequently rainbow. Its normalized image must also be rainbow by cycle parity. Moving its sole edge of any color at most 4 would remove that color and is impossible. More generally, if color i at most 4 appears once on an odd cycle, the complementary path has even length, forcing equal i-th bipartition coordinates at its endpoints. Hence that edge is fixed. Color 5 is always fixed by construction.

Corollary 3.2 follows immediately. Its direct proof is also sound: the four-edge complementary path in each rainbow pentagon puts the endpoints of an i-colored edge on the same side of every compatible complementary bipartition. If every edge lies on a pentagon, the original assignment itself has exact cut complements. This does not provide an assignment on an arbitrary graph.

### 3. Neighborhood facts and the spectral equality case

Lemma 4.1 is valid. A triangle would supply a three-generator dependency. Distinct unordered two-generator sums are distinct, since equality between two such sums would give a nonempty dependency of size at most four. The ten sums exhaust the ten nonzero nongenerators. This gives exactly two common neighbors for each distinct nonadjacent pair and none for an adjacent pair.

In the even-subset model, translate an independent set to contain the empty set. The other members are 2-subsets, and they are pairwise intersecting. Such a family is a star of at most four members or is contained in the three pairs of a triangle. Thus its size is at most four, proving independence number five after restoring the empty set. A neighborhood is an independent five-set. For an independent triple translated to the empty set, {1,2}, {1,3}, a common neighbor is a 4-subset whose missing element belongs to both pairs. The only missing element possible is 1, giving exactly one common neighbor. Repeated images reduce to the one- or two-distinct-image cases. Conversely, an adjacent pair of neighbor images cannot have a common neighbor because the target is triangle-free. The stated single-vertex extension criterion is therefore an equivalence for degree at most three.

For Lemma 4.2, the exact common-neighbor counts give Q²=3I−2Q+2·11ᵀ. Since Q is real symmetric and Q1=5·1, its eigenvalues on 1-perp solve λ²+2λ−3=0 and are 1 or −3. For two six-sets, their centered indicators x and y have squared norm 15/4. In the absence of a cross edge,

0=45/4+xᵀQy,

while

xᵀQy ≥ −||x||||Qy|| ≥ −3||x||||y||=−45/4.

Both inequalities must be equalities. Write y=y_1+y_−3 in the orthogonal eigenspaces. Equality in ||Qy||≤3||y|| forces ||y_1||=0, since its squared contribution is weighted by 1 rather than 9. Thus Qy=−3y. Equality in the first inequality now gives xᵀy=||x||||y||. The vectors have the same nonzero norm, so x=y. Consequently A=B, and the absent cross edges say A is an independent six-set. This contradicts Lemma 4.1. In particular, overlapping A and B introduce no loophole; overlap is already included in the indicator calculation. Larger sets reduce to six-element subsets.

The stronger finite fact about six-set neighborhood unions is correctly labeled supplemental. It is not needed by the spectral proof.

### 4. Walks and arbitrary-boundary extensions

Lemma 4.3 is valid. At length two the displacements are zero and the ten two-generator sums. At length three, repetition yields generators and three distinct generators sum to the complementary pair, giving all nonzero displacements and never zero. At length four, four distinct generators yield the omitted fifth generator, while repetitions give zero and all two-generator sums. All group elements are therefore reachable. Once the whole group is reachable, adding another generator preserves the whole group. This also proves the triangle-free cycle statements under the simple-graph conventions.

The boundary hypotheses in Section 5 are essential and adequate. Centers and arm-interior vertices are distinct uncolored vertices, disjoint from the already-colored outside vertices; terminals may coincide with each other. There are no unaccounted-for incident edges at an interior vertex. Existing outside edges are handled by the assumed outside homomorphism. Enumerating all assignments to separate terminal positions is stronger than enumerating assignments consistent with any identification of terminals.

For Theorem 5.1, three open neighborhoods have total union size at most 15, so a possible center image remains. A center image outside a terminal's open neighborhood is equal to or nonadjacent to that terminal image, precisely the length-two condition. The independent arm interiors can then be chosen separately.

For Theorem 5.2, the complement of two open neighborhoods has size at least six, including repeated terminal images. Lemma 4.2 produces adjacent allowed center images, after which each length-two arm extends.

For the cross-pair variant, each matched pair replaces its two outside-terminal incidences by an edge between the two interior vertices. It forms a length-three path between the centers. Each center has at most two remaining terminal restrictions and hence at least six allowable images. The central edge makes the selected center images distinct. Lemma 4.3 then extends every length-three cross path, independently of the remaining length-two arms. Two cross-pairs remain disjoint, and no further interior incidences are present. All seven possible cross-matchings were independently tested.

### 5. Critical-graph reductions and the density argument

Theorem 6.1 is valid, including the cases in which outside terminals coincide.

An H-critical graph is connected: different components could be colored separately. Degree-zero and degree-one vertices can be restored because H has vertices and every target vertex has neighbors. If there is a cut vertex v, each piece consisting of v and one component of G−v is proper and hence colorable. Translate the colorings so that all images of v coincide, then combine them. Thus there is no cut vertex. A connected graph all of whose vertices have degree two is a cycle; triangle-freeness excludes the only uncolorable cycle length, three. Hence degree-three vertices exist.

Follow each degree-two chain until a degree-three endpoint. A closed chain returning to the same degree-three endpoint uses two of its three edges; the remaining edge leads outside the chain, making that endpoint a cut vertex. A chain consisting of the whole graph was already handled as a cycle. Thus all relevant threads have distinct degree-three endpoints. A thread with at least three degree-two interior vertices can be deleted and then restored over any coloring of the proper remainder, because its length is at least four. Parallel threads after suppression are harmless; incidence counts are made with multiplicity at their endpoints.

If a degree-three vertex v has three degree-two neighbors, those neighbors are distinct by simplicity and have no edges between them by triangle-freeness. Their other endpoints are outside the deleted center-and-neighbor set, although they can coincide with each other. This is exactly Theorem 5.1.

If adjacent degree-three vertices u,v each have two degree-two neighbors, a neighbor shared by the centers would form a triangle. All four degree-two neighbors are therefore distinct. No pair on the same center can be adjacent, again by triangle-freeness. Each neighbor has only one unused incidence, so the remaining edges among the four neighbors form a matching across the two centers. Every unmatched neighbor has its remaining endpoint outside the deleted set. This is exactly the cross-pair variant of Theorem 5.2; terminal coincidences cause no additional edge constraint on an uncolored vertex. No assumption that all four outside endpoints are distinct is needed.

Let a,b,c denote the three permitted degree-three vertex types. The number of endpoint incidences of nonempty threads is 2a+b. Every such thread uses two endpoint incidences and has at most two degree-two interiors, giving n2≤2a+b. Every a-vertex has one direct degree-three neighbor, and the preceding reduction prevents that neighbor from being another a-vertex. The available direct incidences at b- and c-vertices number 2b+3c, so a≤2b+3c. Since c is nonnegative, a≤2b+5c also holds, yielding

3n2≤6a+3b≤5a+5b+5c=5n3.

Equivalently, 8(2n2+3n3)−19(n2+n3)=5n3−3n2≥0, proving average degree at least 19/8. Any noncolorable triangle-free subcubic graph has an inclusion-minimal noncolorable subgraph, which retains those hypotheses. Its average degree contradicts mad(G)<19/8. The strict inequality in the corollary is necessary for this deduction; no conclusion at equality is asserted.

These arguments do not exclude a cubic critical graph. Thus they do not close the conjecture.

### 6. Negative examples and fixed-cut scope

The square obstruction is correct. With terminal images (x,y,y,x), where x and y are adjacent, the two adjacent square vertices next to the middle y,y terminals would both belong to the independent set N(y), impossible. Both proposed reconnection edges nevertheless map to xy. The restored graph can be triangle-free and subcubic and can have another, unpinned homomorphism. Therefore this disproves arbitrary extension of that particular outside coloring, not existence of any homomorphism. The candidate's 961 count is over all 4,096 normalized boundaries. It is not a count restricted to boundaries satisfying both reconnection edges; the latter contains 400 cases and 45 failures.

K3,3 maps by collapsing its two parts to the ends of a target edge. Local injectivity would give three distinct images of each part. Two distinct images in one part would then have the three distinct images of the other part as common neighbors, contrary to the maximum common-neighbor count of two. Distinct generator colors on incident edges are exactly distinct neighbor images at that vertex. Hence matching canonical color classes would imply local injectivity and are impossible. This is fully compatible with proper original weak-pentagon colorings of the bipartite graph. Choosing the same bipartition in all four normalization coordinates sends every edge to color 5 and explicitly shows how properness can be destroyed.

The fixed-color-5 formulation in Section 8 is exact: removing the J-edges leaves only coordinate-generator edges, so the remainder maps to Q4 and every removed pair is antipodal. A mere bipartition of the remainder does not supply these antipodal constraints. For a locally optimal cut in a subcubic graph, two noncrossing incidences at a vertex would exceed half its degree; flipping that vertex would enlarge the cut. The complement is therefore a matching. Any cut crosses every cycle evenly, so its complement meets an odd cycle oddly. A matching meets a pentagon at most twice, hence exactly once. None of these facts proves that an arbitrary maximum-cut complement can be prescribed as the canonical color-5 class.

## Independent computation and adversarial controls

The submitted suite was rerun in isolated copies rather than allowed to rewrite its frozen input directory. Normal mode passed and reproduced the recorded verification results byte-for-byte. Optimized copies also produced those bytes, but their disabled assertions make these output-reproduction observations only. Replacing the expected six-set neighborhood minimum 13 by the false value 12 made the original normal-mode script fail, whereas both optimized scripts exited zero. The audit recorded this defect explicitly.

The independent checker constructs vertices as the even subsets of a five-element set and defines adjacency by symmetric-difference cardinality four. It does not import the submitted script. It verifies an explicit isomorphism to the candidate's Cayley labeling, then uses subset enumeration, integer matrix multiplication, exact characters, and a generic edge-constraint backtracking solver. Its principal results are:

- Unique generator relation masks: 0 and 31.
- Pair types: 40 adjacent pairs with zero common neighbors and 80 nonadjacent pairs with two.
- Independent-set counts by size 0 through 5: 1, 16, 80, 160, 120, 16; none larger.
- All 160 independent triples have one common neighbor; the complete ordered single-vertex boundary criterion also passes all 4,096 triples, including repetitions.
- Exact spectrum: 5 with multiplicity 1, 1 with multiplicity 10, −3 with multiplicity 5; Q² identity checked entrywise.
- All 65,536 vertex subsets are enumerated for neighborhood unions. Among the 8,008 six-sets, union-size counts are 160 at 13, 1,800 at 14, 3,312 at 15, and 2,736 at 16. Thus no six-set has six vertices with which it has no cross edge, even allowing overlap. A five-by-five empty cross relation exists, for example the same independent neighborhood on both sides.
- Walk supports for every ordered endpoint pair and lengths one through seven match Lemma 4.3. Counts, not merely Boolean support, were calculated by integer matrix multiplication.
- A generic CSP solver extends all 256 normalized claw boundaries and all 4,096 normalized double-claw boundaries. It also checks all seven cross-matchings: the empty matching's 4,096 cases, four one-edge matchings with 16 normalized boundaries each, and two perfect matchings with one boundary-free case each.
- The same generic solver obtains 961 square failures out of 4,096, including the explicit obstruction. Among the 400 valid-reconnection boundaries, precisely 45 fail.
- It rejects a triangle, supplies witnesses for cycles of lengths four through twelve, accepts K3,3 ordinarily, rejects every locally injective K3,3 map after translation normalization, and verifies the Petersen graph's standard 2-subset embedding and coverage by 12 pentagons. It also verifies both existence of another homomorphism and failure of the prescribed boundary for the restored-square example.
- All 3,125 five-color assignments on C5 and all 78,125 assignments on C7 are tested. The valid original-witness counts are respectively 120 and 16,800. Deterministic normalization changes none of the C5 witnesses and 14,616 C7 witnesses; all retain their singleton odd-cycle colors and have explicit exact-cut certificates. This finite test samples one deterministic choice of complementary bipartitions per valid witness; the general arbitrary-choice claim is established by the symbolic proof, not by claiming to enumerate every component orientation.
- The submitted 28,840 integer-density sanity cases are independently reproduced. They corroborate the elementary inequality and are not used as a substitute for its proof.

All final independent results are identical under normal, `-O`, and `-OO` execution. The hardened submitted checker also produces the original results in all three modes. In every mode, a removed target edge, a false square failure count, a changed candidate byte stream, and a changed input manifest are rejected by the independent checker. A false neighborhood-union expectation is rejected by the hardened submitted checker. Each rejected run exits nonzero without emitting a success artifact. The audit recorded 21 expected outcomes: six successful substantive runs and fifteen rejecting controls.

The negative mathematical examples are deliberate scope controls, not evidence against the original conjecture. The finite enumeration bounds are stated explicitly and do not purport to enumerate all triangle-free cubic graphs.

## Literature and credit boundary

The candidate properly credits DeVos–Šámal's equivalence and high-girth theorem rather than claiming them as new. Its finite/simple conventions and original conjecture identification agree with the provided primary-source inspection record. The relevant primary citation is *High-girth cubic graphs are homomorphic to the Clebsch graph*, [arXiv:math/0602580v2](https://arxiv.org/abs/math/0602580v2), with journal identity [DOI 10.1002/jgt.20580](https://doi.org/10.1002/jgt.20580). The high-girth proof's original computer-assisted component was not audited here.

The source inspection record verifies that Borodin–Hartke–Ivanova–Kostochka–West's *Circular (5,2)-coloring of sparse graphs*, [primary journal record](https://www.mathnet.ru/semr116), Theorem 5 on printed page 418, assumes triangle-freeness and mad<12/5 and concludes a C5 homomorphism, without a subcubic assumption. Since C5 maps to H and 19/8<12/5, this really does strictly subsume the candidate's sparse corollary. The audit independently checks the arithmetic and the C5-to-H implication; it does not represent itself as an audit of that paper's full discharging proof.

The inspected later signed-projective-cube and K5-minor-free results retain hypotheses not possessed by arbitrary triangle-free cubic graphs. No such result is silently promoted to a solution of the target. Search silence and an older source's conjecture label are not proof of current openness. The accepted status is **unresolved by this work; a full published resolution was not verified by the bounded source review**.

No novelty claim is made or accepted for the normalization refinement, extension toolkit, or local obstructions. Their validity and useful scope are separate from priority in the literature.

## Reproduction and disposition

The retained audit workflow runs an input-pinned independent checker with the same active checks in normal Python, -O and -OO, then runs successful modes, rejection controls and hardened-checker comparisons without modifying the frozen input. The original unmodified checker is verification only in normal mode. A revised executable workflow would need either explicit runtime checks or an explicit failure when assertions are disabled.

This edition intentionally distributes no programs or private input bundle, so those historical commands are not public reproduction instructions. Readers can check the full symbolic proofs and displayed examples directly. The complete prose of the independent mathematical review and its bounded outcomes is retained here; [Reproduction scope](REPRODUCTION.md) distinguishes that record from a runnable package.

The mathematical packet is accepted within the narrow scope above. The original assert-based checker must not be advertised as fail-closed under optimization. No correction to the proof statements is required by this audit.
