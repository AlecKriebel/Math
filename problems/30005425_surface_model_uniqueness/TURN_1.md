# Turn1: two finite gentle covers with different underlying topology

AI-assisted mathematical proof candidate; independent review pending.

**Scoped theorem:** one nine-dimensional string algebra has two eleven-dimensional saturated gentle covers whose standard surfaces have respective topological types (genus0, three boundary components) and (genus1, one boundary component). Both covers have an acyclic quiver and neither surface has punctures.

**Original OWR disposition remains unresolved.** This refutes uniqueness up to homeomorphism, including labelled/dissected homeomorphism. It is a counterexample to the OWR conjecture only if its permitted rotations preserve underlying surface topology. No formal definition of those tile-collection rotations has been recovered, and we do not assume that condition. A cut-and-reglue operation can change topology; nonhomeomorphism alone does not exclude such an equivalence.

## 1. Exact algebra and covers

Let k be algebraically closed. Use four vertices 0,1,2,3 and five arrows

a:0→1, b:0→2, c:1→2, d:1→3, e:2→3.

Paths in this note are written in traversal order: ac means first a, then c. Equivalently the ordered-pair relations below remove all convention ambiguity.

Let I=(ac,ad,be,ce), the ideal of all length-two paths, and A=kQ/I. It has the four vertex idempotents and five arrows as a basis, so dim A=9. The in/out degrees are at most two. No arrow has a permitted successor or predecessor in A, so the special-biserial uniqueness conditions are satisfied. Thus A is a finite-dimensional string algebra.

Define

J_0=(ac,be),   J_1=(ac,ce),   B_i=kQ/J_i.

At vertex1, the incoming arrow a has one forbidden and one permitted outgoing continuation. At vertex2, exactly one of b,c has a forbidden continuation to e and the other a permitted one. All other gentle conditions are immediate from the degree bounds. Both ideals are quadratic and both algebras are gentle. The quiver is acyclic, so neither can have arbitrarily long paths. More explicitly, each B_i has exactly two nonzero paths of length two and none of length three, giving dim B_i=4+5+2=11.

Both J_i are saturated among quadratic ideals J⊆I yielding locally gentle algebras. Adding ad to either creates two forbidden successors for a; adding the other missing relation at vertex2 creates two forbidden predecessors for e. There is no larger permissible quadratic ideal. Thus the example also lies in the saturated-cover convention of the2026 preprint.

Finally A=B_i/(I/J_i). In the labelled-surface description, the omitted relations become labels along permitted fans. For B_0 they are ad and ce; for B_1 they are ad and be. No infinite-dimensional cover is used.

## 2. Credited surface construction

We use the standard surface attached to a gentle bound quiver, not an arbitrary topological realization. Palu–Pilaud–Plamondon, [Non-kissing and non-crossing complexes for locally gentle algebras](https://arxiv.org/abs/1807.04730), Definition4.6 gives the blossomed-lozenge construction; Theorem4.10 identifies the correspondence and Remark4.11 gives boundary/genus calculations. Remark4.13 identifies the surface with the earlier Opper–Plamondon–Schroll ribbon construction. These are credited inputs.

A finite permitted thread gives a ribbon vertex whose incident half-edges are the quiver vertices in path order. A quiver vertex gives the edge pairing its two occurrences. For this example every vertex already occurs twice among the listed nontrivial threads, so no trivial-thread convention is needed. Thickening the ribbon graph yields the same underlying surface. We calculate its boundary cycles explicitly and also reproduce the full independent blossomed-lozenge gluing.

## 3. B_0: pair-of-pants topology

The maximal permitted threads, as vertex lists, are

(0,1,3), (0,2), (1,2,3).

Assign successive dart labels0,…,7 in that order. The cyclic-order permutation is

σ=(0 1 2)(3 4)(5 6 7),

and equal quiver-vertex occurrences give the edge involution

α=(0 3)(1 5)(2 7)(4 6).

Boundary components are cycles of σα. They are

(0 4 7), (1 6 3), (2 5).

There are three ribbon vertices, four edges and three boundary cycles. The connected thickening retracts onto this graph, so χ=3−4=−1. The equation χ=2−2g−b with b=3 gives g=0.

## 4. B_1: one-holed-torus topology

The permitted threads are now

(0,1,3), (0,2,3), (1,2).

With the same successive-dart convention,

σ=(0 1 2)(3 4 5)(6 7),
α=(0 3)(1 6)(2 5)(4 7).

The boundary permutation σα has a single cycle

(0 4 6 2 3 1 7 5).

Again χ=3−4=−1, now b=1, hence g=1. The two underlying surfaces cannot be homeomorphic because their genera and boundary-component counts differ.

Since Q is acyclic, neither its permitted nor its forbidden transition system has a cyclic thread. The standard construction consequently has no punctures of either colour. This is corroborated directly by the lozenge calculation, including all compatible source/sink blossom completions.

## 5. Independent finite certificates and provenance

`turn1/ribbon_certificate.py` computes the thread lists, permutations and complete cycles from the four-vertex data. `turn1/surface_gluing.py` implements the separate credited PPP lozenge construction, reusing and extending the previously reviewed finite surface checker from [PR301](https://github.com/AlecKriebel/Math/pull/301). That earlier PR concerns a different derived-invariant algorithm; it is neither a previous attempt at this conjecture nor an independently new source for the surface correspondence.

`turn1/verify_witness.py` verifies the string/gentle conditions, finite path dimensions, saturation among all16 quadratic subideals of I, all four compatible boundary blossom choices for each selected cover, and the dual-relation surface check. The ribbon and lozenge calculations agree. The certificates store exact integers and permutations; there is no floating-point topology classification. The proof above does not infer a universal theorem from a finite search.

A preliminary finite search located a larger witness, subsequently reduced to this explicit four-vertex example. That exploratory search is retained locally but is not needed by or represented as exhaustive evidence for this certificate.

## 6. Source comparison and unresolved rotation issue

The OWR report fixes A and varies finite locally gentle covers B; its imported clean statement instead fixes B and is not equivalent. The conjectural tile-collection rotations are not defined as formal moves in that short report. The expanded Baur–Coelho Simões [2024 preprint](https://arxiv.org/abs/2403.07810), Theorem3.1 and Remark3.2, supplies the cover construction but the retrieved text's rotation discussion concerns module arcs, not an equivalence generated by rotating tile collections. That is not a definition of the missing move.

Xin–Zhang [2026 preprint](https://arxiv.org/abs/2608.14360), Definition1.14, uses an orientation-preserving homeomorphism preserving colours, dissection and ordered labels. Its classification and examples are directly relevant prior work, but are not asserted to identify the OWR's coarser rotation quotient. Their finite-cover examples already show various labelled-model failures; no historical novelty is claimed for the present homeomorphism counterexample.

If every allowed rotation is supported inside a fixed surface or otherwise preserves homeomorphism type, Sections3–4 exclude equivalence. If rotations include topology-changing regluings, further analysis of the permitted moves is required. This conditional transfer is explicit. The exact source question is therefore not promoted to solved from this packet alone.

Completed substantive author turns:1/5. Informal completion estimate toward the exact original target:35%, with the main uncertainty now the rotation equivalence rather than algebraic finiteness or topology of the displayed covers.
