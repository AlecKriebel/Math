# Audit of spanning near squares of odd cycles

## Conclusion and attribution

**The universal spanning statement is false.** The counterexample claim belongs to Alper Ferudun, *Dirac Graphs Without a Spanning Near-Square of an Odd Cycle: A Negative Answer to a Question of Heinig*, version 1.0, dated 28 September 2026, DOI [10.5281/zenodo.23004012](https://doi.org/10.5281/zenodo.23004012). Its public status is an unrefereed preprint. This audit does not claim discovery of the counterexamples, certify absolute priority, or imply completed external peer review.

The audit checks Ferudun's all-odd-order construction under the two definitions in his Section 2. It also supplies a self-contained elementary proof of his stronger nine-vertex claim in Remark 3.5, which his manuscript supported computationally. The latter settles the original universal question without relying on a particular interpretation of the word *periphery*.

The original source is Peter Heinig's Question 2 in the problem session of *Combinatorics*, Oberwolfach Reports 11 (2014), Report 01/2014, printed page 82, DOI [10.4171/owr/2014/01](https://doi.org/10.4171/owr/2014/01), [report PDF](https://ems.press/content/serial-article-files/46491). The question concerns spanning, not necessarily induced, copies. It assumes odd n ≥ 7 and minimum degree at least ⌈n/2⌉. Its target starts with C_n² and loses edges until three vertices have degree 4 and all others degree 3. The immediately preceding Question 1 is about generation of the cycle space by Hamilton cycles. A negative answer to Question 2 does not negate Question 1.

## A definition independent nine vertex obstruction

### Theorem

Let M be any matching of three edges in C_9². Then C_9² − M is not isomorphic to a spanning subgraph of K_{4,4,1}.

The host has nine vertices. Each of the eight vertices in a part of size four has degree five; the vertex in the singleton part has degree eight. Thus its minimum degree is exactly 5 = ⌈9/2⌉.

### Proof

Label C_9 by 0,1,…,8 in cyclic order. Write H = C_9² − M. If a spanning copy of H lay in K_{4,4,1}, the preimage v of the singleton part would have the property that H − v is bipartite, since its image lies in K_{4,4}. Rotation allows us to take v = 0.

There are six triangles

T_i = {i,i+1,i+2},  1 ≤ i ≤ 6,

in C_9² − 0. For H − 0 to be bipartite, each triangle must lose an edge. An edge of C_9² belongs to at most two of these six triangles. It belongs to two precisely when it is one of

{2,3}, {3,4}, {4,5}, {5,6}, {6,7}.

A distance-two edge lies in at most one T_i; an edge incident to 0 lies in none. Three deletions can hit all six triangles only if each hits exactly two and their sets of hit triangles are disjoint. In T_1, the only edge capable of hitting two triangles is {2,3}, which also hits T_2. Among the remaining triangles T_3,…,T_6, disjoint double coverage forces {4,5} and then {6,7}. Consequently,

M = {{2,3},{4,5},{6,7}}.

But after these deletions the vertices 1,3,5,7,8, in this order, form a cycle of length five: its edges are {1,3}, {3,5}, {5,7}, {7,8}, and {8,1}. All belong to C_9² and none belongs to M. This contradicts bipartiteness of H − 0. Therefore no spanning copy exists. ∎

### Why this covers the original construction

C_9² is 4-regular. A target with six degree-3 vertices and three degree-4 vertices must delete exactly one incident edge at each of those six vertices, and none at the others. The deleted edges therefore form a three-edge matching. The theorem rules out every such target, even after removing restrictions about alternation, periphery, or which three vertices remain of degree four. It is thus stronger than what is needed to disprove the original quantified statement.

The same obstruction is the K_{4,4,1} claim already made in Ferudun's Remark 3.5. The proof above is an independently written verification of that credited claim, not a claim of a new counterexample.

## The two specified target families

For completeness, put n = 2s+1 with s ≥ 3, and label vertices by the residues modulo n. The edges of C_n² are

c_i = {i,i+1} and q_i = {i,i+2}.

All subscripts in graph edges are reduced modulo n.

**Cycle periphery R1.** Define H_n by removing

D = {{2j,2j+1}: 0 ≤ j ≤ s−2}.

The three untouched degree-4 vertices are F = {n−3,n−2,n−1}. Every other vertex loses one incident edge and has degree 3. There are (3n+3)/2 edges.

**Distance two periphery R2.** Since n is odd, the distance-two edges form the Hamilton cycle Q whose vertex order is 0,2,4,… modulo n. Remove alternate edges along Q until exactly three consecutive Q-vertices retain degree 4. Denote the result by H'_n. Every cycle edge c_i is retained, and the deleted q-edges are a matching along Q. The target has the same degree sequence and edge count as H_n.

The OWR page is prose and contains no drawing of the target. The audit does not assert that the author's intended periphery has been established uniquely. R1 is consistent with the usual even-order prism construction; R2 is the boundary cycle of the customary triangulated Möbius-band interpretation. The nine-vertex theorem makes this interpretive issue immaterial for the universal negative answer.

## Ferudun's host at every odd order

Take disjoint vertex sets A and B with |A| = s+1 and |B| = s. Put in every edge between A and B, and none inside B. Inside A put:

- a perfect matching when s is odd;
- one path of length two together with a perfect matching on the other s−2 vertices when s is even.

Call the result G_n. The second definition is possible because s−2 is nonnegative and even. Every B-vertex has degree s+1. Every A-vertex has degree s+1, except that the middle of the length-two path has degree s+2 in the second case. Hence δ(G_n) = s+1 = ⌈n/2⌉.

If H were a spanning subgraph of G_n, the preimage J of B under the spanning bijection would be an independent set of size s in H. The remaining graph H − J would embed into G_n[A]. This is a necessary condition for ordinary subgraph containment, so no induced-subgraph assumption is being introduced.

For any such J in either target family, double-counting incident edges gives

e(H − J) = (3n+3)/2 − (3s + |J∩F|) = 3 − |J∩F|,

where F means the three degree-4 vertices of that target.

## Verification for the distance two periphery

Suppose an independent s-set J exists in H'_n. It must be independent in the retained cycle C_{2s+1}. In cyclic order there are s gaps between consecutive vertices of J; the s+1 vertices outside J fill those gaps with one vertex each, except for one gap containing two. Thus J can be written

{i,i+2,…,i+2(s−1)}.

The consecutive pairs in this display are s−1 consecutive edges of Q. Because s≥3, at least two consecutive Q-edges are present between vertices of J. Both cannot have been deleted, since the deletion set is a matching. One survives in H'_n, a contradiction. Therefore H'_n has no independent s-set and cannot span G_n.

## Verification for the cycle periphery

Let J be an independent s-set in H_n. Consider its maximal runs along the original cyclic order.

A run has at most two vertices: a run of three would contain a retained distance-two edge. Every two-vertex run must be one of the deleted pairs {2j,2j+1}. After the last vertex x of any run, both x+1 and x+2 lie outside J. The first exclusion is maximality and the second is the retained edge {x,x+2}. Therefore every gap between runs contains at least two vertices.

Write r_1 and r_2 for the numbers of singleton and doubleton runs. Then

s = r_1 + 2r_2,
2s+1 ≥ s + 2(r_1+r_2),

so 2r_2 ≥ s−1. Distinct doubleton runs have indices j separated by at least two in {0,…,s−2}; hence r_2 ≤ ⌈(s−1)/2⌉.

### Odd s

Write s = 2t+1. The bounds force r_2=t and r_1=1; every gap has exactly two vertices. The circular arrangement consists of t blocks of length four (a pair followed by a gap) and one block of length three (a singleton followed by a gap).

Between consecutive pair starting points, the forward cyclic distance is four, except for one distance seven crossing the singleton block. Every pair starts at an even integer in {0,2,…,2s−4}. Since n is odd, a step of four cannot wrap from n−1 to 0 while preserving even starts; the step of seven must wrap. If p is the smallest start, all starts are therefore

p,p+4,…,p+4(t−1).

The last start is at most 2s−4=4t−2, forcing p to be either 0 or 2. This remains valid for t=1: the single seven-step runs from the pair to itself around the seven-cycle. Consequently J is one of exactly two sets:

J_0 = {4k,4k+1: 0≤k<t} ∪ {n−3},
J_2 = {4k+2,4k+3: 0≤k<t} ∪ {n−1}.

These displayed sets are indeed independent by the edge definition. In H_n−J_0 the edges {n−4,n−2} and {n−2,n−1} survive. In H_n−J_2 the edges {n−3,n−2} and {n−2,0} survive. Each pair of edges makes a path of length two. But G_n[A] is a matching when s is odd and cannot contain that path. Thus neither J allows an embedding.

### Even s

Write s=2t. The bounds give r_2=t and r_1=0. Selecting t pair indices, with consecutive chosen indices separated by at least two, from {0,…,2t−2} forces the indices 0,2,…,2t−2. Thus the only possible independent s-set is

J = {4k,4k+1: 0≤k<t}.

It is independent by direct inspection. It avoids all three vertices n−3,n−2,n−1. Those three retain their two consecutive cycle edges and their distance-two edge, so H_n−J contains a triangle. The graph G_n[A] is a forest and cannot contain it. This proves noncontainment also when s is even.

Together with R2, this verifies Ferudun's Theorem 1.1 for every odd n≥7.

## Figure and small order checks

For n=7, G_7 consists of K_{4,3} plus two disjoint edges inside its four-vertex side. Heinig's arXiv:1112.5101v1, Definition 28 on page 30, defines the graph X shown in Figure 4. Taking A={v_1,v_2,v_4,v_5} and B={v_3,v_6,v_7} in that definition gives all A–B edges, the A-edges v_1v_2 and v_4v_5, and no B-edges. Thus X is exactly this G_7 after relabeling. The figure and its caption concern a Hamilton-cycle basis, not a drawing that fixes the near-square periphery.

The broad n=9 obstruction should not be replaced by an unrestricted claim about G_7. Indeed G_7 contains C_7²−{{0,1},{3,5}}; the independent check records an explicit embedding. That example explains why the periphery qualification matters for the all-n family, even though it does not affect the universal negative answer.

## Independent finite verification and limits

Independent standard-library verification code was written for this audit. No claimant source archive or executable code was used. It checks:

1. Host minimum degrees, target degree sequences, and complete enumeration of independent s-sets for every odd 7≤n≤51, for both target definitions. The results exactly match the classifications above.
2. Direct injective backtracking for ordinary spanning containment, without the independent-set reduction, for n=7,9,11,13 and both readings. All eight host/target cases are negative. A relabeled target, or the target itself for n=9, is a positive control in each case.
3. All 177 labeled three-edge matchings in C_9² and all nine choices of deleted vertex. In all 1,593 cases the residual graph is nonbipartite. A separate test verifies the triangle-or-five-cycle certificate used in the analytic proof.
4. The broad n=7 positive control and the isomorphism between the explicitly transcribed Heinig graph X and G_7.

Finite checks supplement the proofs; they do not replace the quantified arguments. Ferudun's additional threshold claims for n=7 and n=9, his reported SAT runs, and his wider literature-search claims were not independently reproduced here. No conclusion about the exact optimal threshold beyond the counterexamples is needed. The audit also does not certify the current literature status of Question 1.

## Source version and review status

- Ferudun PDF: Zenodo record 23004012, version 1.0, publication date 2026-09-28; 86,693 bytes; SHA-256 `02ea0f37da91ece4bf3dcab399ef2dbe52f891b5cddc649ab3845ce3efed6824`. The deposited file's length and MD5 match the record metadata. All five pages were read in text; pages 2–4 were also visually inspected.
- Ferudun's deposited verification report was read as a statement of what the claimant reports having checked, not as independent evidence that those computations ran correctly.
- Original OWR PDF: 86 PDF pages; Question 2 is on PDF page 78, printed page 82, which was visually inspected. The adjoining Question 1 text was read for scope. The whole workshop report was not audited.
- Heinig: arXiv:1112.5101v1, 21 December 2011, 33 pages. Definition 28, Figure 4 and the adjacent Proposition 30 were inspected; this audit used the explicit edge list to verify X≅G_7. The complete article and its journal version were not re-audited.

Retrieval and byte-level metadata are recorded separately. The audit's mathematical conclusion is acceptance of the credited negative answer, with the unrefereed status and the limits above retained.
