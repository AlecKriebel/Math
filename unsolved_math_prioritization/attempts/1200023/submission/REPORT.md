# Boundary-distance sums in transitive graphs

**Target:** 1200023 / AMR-011-0023, rank 638.  
**Status:** `unsolved`; five substantive approaches completed.  
**Result:** credited reconstruction of the known unimodular case, an elementary nonunimodular example family, an exact finite-support optimization criterion, and explicit gaps. No full resolution or novelty claim.

## 1. Source and intended scope

Miklós Ábert, *Some questions*, dated 2 November 2010, Section 4, Question 23, printed page 4, asks for the following inequality. For an infinite vertex-transitive graph G, finite vertex set A and a vertex b, put

S_b(A) = sum over x in the outer vertex boundary of A of d_G(b,x).

The target is S_b(A) >= |A|. The outer boundary consists of vertices outside A adjacent to A; distances are ambient shortest-path distances. Neither A nor its induced subgraph is assumed connected. The basepoint b need not belong to A. The source immediately records the unimodular case as known. This restriction was omitted from the imported summary claiming a general literature resolution.

Primary source: https://www.renyi.hu/~abert/questions.pdf (also retrieved from https://renyi.hu/~abert/questions.pdf). Source page 4 was inspected in both extracted text and a rendered page. The PDF is 102130 bytes, SHA256 576000d7a042147021311cb8fd944e414d8d49db73642fcaf06dd9c2d90aa4e1.

There is a convention issue: connectedness is not printed. Taken without the usual connected graph-metric convention, the countable disjoint union of triangles is an infinite vertex-transitive graph. Taking A to be a complete component gives empty boundary and 0 < 3. This is a literal-wording warning, not a proposed resolution of the intended problem. The substantive target throughout this report is the connected case.

Local finiteness is not printed either. In a connected vertex-transitive graph of infinite degree, every nonempty finite A has infinite boundary, so the nonnegative boundary sum is infinite. Thus the only nontrivial connected case is locally finite. A empty is immediate. The remaining discussion treats connected, locally finite, simple undirected graphs. Loops and parallel edges do not affect the stated vertex metric/boundary target.

## 2. Approach 1: geodesic incidence and unimodular mass transport

This reconstructs a case already credited in the source. It also exposes a precise sufficient condition for the general case.

For n >= 1, consider every oriented geodesic segment of n edges in G. Let M_n be the number starting at a specified vertex, and N_n the number containing a specified vertex anywhere. Transitivity makes each count independent of the vertex; local finiteness makes the counts finite, and infinitude/connectedness make them positive.

Let A be nonempty, D = diam_G(A), and n > D. A segment cannot have both endpoints in A. The number with at least one endpoint in A is exactly 2|A|M_n. Each segment has at most D+1 vertices in A, because the first and last such vertices on a geodesic have index difference at most D.

For a segment whose endpoints are outside A and which meets A, let u be the vertex immediately before its first visit to A and v the vertex immediately after its last visit. Both belong to the outer boundary. If their indices are i < j, then

|A intersect segment| <= j-i-1 = d_G(u,v)-1 <= d_G(b,u)+d_G(b,v)-1.

In particular, it is at most the sum of d_G(b,x) over boundary vertices on that segment. The segment is simple, so this sum has no repeated vertices. Sum over all segments meeting A, bounding the endpoint-in-A segments by D+1 instead. The sums are finite because only finitely many length-n segments meet a fixed finite set. We obtain

N_n |A| <= N_n S_b(A) + 2(D+1)|A|M_n.               (1)

Consequently any such transitive graph satisfying

liminf as n tends to infinity of M_n/N_n = 0        (2)

satisfies the target, by applying (1) along a subsequence. This is a sufficient condition, not an asserted theorem for all transitive graphs.

For a unimodular transitive graph, fix a position i in {0,...,n} and let F_i(x,y) count the length-n oriented geodesics starting at x whose i-th vertex is y. This is diagonally invariant. Its outgoing sum is M_n. The unweighted mass-transport principle says its incoming sum is also M_n. Summing positions, and using that a geodesic does not repeat vertices, gives N_n=(n+1)M_n. Condition (2) follows and proves the known unimodular result.

The general mass-transport formula and its unimodular specialization are verified in Lyons--Peres, *Probability on Trees and Networks*, version 19 August 2026, Theorem 8.7, Corollary 8.8 and equation (8.4), printed pages 279--280. https://rdlyons.pages.iu.edu/prbtree/book_pb.pdf

**Gap:** condition (2), or an alternative invariant weighted geodesic family with vanishing endpoint contribution, was not established for arbitrary nonunimodular transitive graphs. Applying unweighted mass transport there is invalid.

## 3. Approach 2: diameter expansion and radial truncation

A standard geodesic-counting estimate gives

|A| <= (diam_G(A)+1)|boundary A|.

It applies to infinite locally finite vertex-transitive graphs without a unimodularity assumption; a proof is recorded as the Babai--Szegedy estimate in Matt DeVos, *Pretty Theorems on Vertex Transitive Graphs*, Theorem 2, page 2. https://www.sfu.ca/~mdevos/notes/misc/vertex-trans.pdf

The mechanism counts length-(D+1) geodesics passing through A. Each contains at most D+1 vertices of A and at least one boundary vertex. Uniform total incidence at each vertex suffices, so this route avoids mass transport.

The estimate does not replace a maximum distance by the desired sum with unit constant. The infinite one-sided ray supplies an exact failed-inference control: A={0,...,4}, b=5. Its diameter is 4, its only boundary vertex is 5, the diameter estimate holds with equality, but S_b(A)=0. Indeed every nonempty finite set in the ray satisfies the diameter estimate since its size is at most diameter+1. The ray is not vertex-transitive, so this is not a counterexample to the target; it shows that the diameter estimate alone cannot imply it.

Trying the diameter bound on A intersect B(b,r) introduces boundary vertices lying in A itself. Even in the integer line, truncating a large interval by a smaller ball creates exactly such artificial boundary points. No control converting those new boundaries into the original distance-weighted boundary was obtained.

**Gap:** a sharp summable radial inequality, retaining the original boundary and arbitrary basepoint, remains missing.

## 4. Approach 3: modular orbit counting and positive expansion

For an automorphism-invariant directed orbit of adjacent pairs, write p for its out-degree and q for its in-degree. If p>q, double counting arcs from a finite A to A union boundary A gives

p|A| <= q(|A|+|boundary A|),

hence |boundary A| >= (p/q-1)|A|. This is genuine positive vertex expansion. It supplies no general unit coefficient for S_b(A); in particular, b may itself be a boundary vertex of zero weight.

The ordinary mass-transport identity fails concretely on the binary grandparent graph. Sending one unit from every vertex to its distinguished grandparent gives outgoing mass 1 and incoming mass 4. The general formula weights each of the four incoming contributions by 1/4. This example and its automorphism invariance are recorded in Lyons--Peres, Section 8.2, page 279. The verifier checks the analogous q^2 versus 1 calculation for q=2,3,4. Dropping the stabilizer ratios is not a harmless normalization.

Positive expansion by itself also fails to imply the boundary-distance target. Attach one pendant leaf to every vertex of the 3-regular tree. For a finite set A, let C be its core-tree vertices and O the leaves in A whose parents are outside C. If C is nonempty, its core boundary has at least |C|+2 vertices, all in boundary A. Also the distinct parents of O belong to boundary A. Since |A| <= 2|C|+|O|, we get |A| <= 3|boundary A|. If C is empty, |boundary A|=|A|. This connected bounded-degree graph therefore has positive vertex expansion, yet a singleton leaf with b its parent has S_b(A)=0. Again it is nontransitive and is only a failed-inference control.

The cited Benjamini--Schramm paper *Every graph with a positive Cheeger constant contains a tree with a positive Cheeger constant* (1997), DOI 10.1007/PL00001625, has an institutional abstract about positive-expansion trees and spanning forests under integer expansion thresholds. The abstract was inspected, not its full text. It does not by itself establish the imported general boundary-distance claim. https://weizmann.esploro.exlibrisgroup.com/esploro/outputs/journalArticle/Every-graph-with-a-positive-Cheeger/993267451603596

**Gap:** neither the modular weighted identity nor positive expansion has been converted to the unweighted unit-constant boundary-distance inequality. No full-resolution theorem was verified in the bounded literature search.

## 5. Approach 4: spanning-tree expansion and nonunimodular examples

**Proposition.** If G contains, on its full vertex set, a spanning (q+1)-regular tree T with q>=2, then for every finite nonempty A and every b,

S_b(A) >= |A|+1.

**Proof.** Let B be the outer boundary of A in T and let e_A be the number of T-edges internal to A. The induced forest on A union B has at least

(q+1)|A|-e_A

edges: internal A-edges plus all edges leaving A. It has at most |A|+|B|-1 edges. Thus |B| >= q|A|-e_A+1. Since e_A <= |A|-1, we get |B| >= (q-1)|A|+2 >= |A|+2. Adding edges cannot remove an outer boundary vertex, so |boundary_G A| >= |A|+2. Every boundary vertex except possibly b contributes at least 1 to S_b(A), proving the assertion. QED.

This applies to every usual q-ary grandparent/grandfather graph (q>=2), which adds grandparent edges to its spanning regular tree. Thus a principal nonunimodular test family is covered for arbitrary finite A, arbitrary b and the actual shortcut metric. The conclusion is not asserted to be new.

For additional nonunimodular tests we used the standard Diestel--Leader horocyclic product models DL(2,3) and DL(3,4). Their exact neighbor oracles are documented in the verifier. They are finite-support tests only; no all-set theorem for those families is claimed here.

**Gap:** an arbitrary nonunimodular transitive graph was not shown to have such a spanning tree, a comparable expansion threshold, or another structure yielding the same estimate.

## 6. Approach 5: exact finite-support min-cut formulation

Fix b and a finite allowed support U. Let W=U union boundary U and c(v)=d_G(b,v). Construct a directed network with a source s, sink t, one a-node for each v in U and one z-node for each w in W:

- s -> a_v has capacity c(v)+1.
- a_v -> z_w has capacity L for each w in the closed neighborhood of v.
- z_w -> t has capacity c(w).

Let K=sum over v in U of (c(v)+1), and use L=K+1. The empty set gives a cut of capacity K, so a minimum cut never severs an L-edge. If A is the set of a-nodes on the source side, all z-nodes for the closed neighborhood of A must also be there. Placing any other positive-capacity z-node there can only increase cut capacity. Therefore the minimum cut value is exactly

K + min over A subset U of (S_b(A)-|A|).             (3)

Conversely every A realizes its displayed canonical cut, proving equality, including zero-capacity vertices and A empty. Thus a feasible flow of value K certifies the inequality for every A subset U, simultaneously. This is a finite-support certificate and not a proof uniform in U.

`verify.py` uses integer arithmetic and an explicit infinite-graph neighbor oracle, not the induced graph of a cropped ball. For U=B(b,R), a complete breadth-first search through radius R+1 gives exact distances for every boundary vertex of every A subset U. Flow feasibility, capacity bounds, conservation, residual cut separation and flow/cut equality are all checked. Small cases are separately checked by subset enumeration; finite cycles and paths detect an overbroad conclusion.

The final runs certify all subsets supported in these balls:

- Z: radii 0 through 7 (largest support 15 vertices).
- Z²: radii 0 through 6 (85 vertices).
- Binary grandfather graph: radii 0 through 4 (681 vertices).
- DL(2,3): radii 0 through 5 (648 vertices).
- DL(3,4): radii 0 through 4 (650 vertices).

The minimum deficit is zero, realized by A empty, in all 31 networks. Each run supplies a saturated-source flow certificate generated and checked on replay. The five radius-one brute-force comparisons check 872 subsets. Further exact controls check 30595 geodesic interval cases, 15 tree-boundary subsets, three modular ratios and negative finite/disconnected/nontransitive examples.

**Gap:** proving saturation in (3) for every finite support in every connected nonunimodular transitive graph is the remaining original problem, not an established consequence of the bounded runs.

## 7. Final assessment and reproduction

Run `python3 verify.py` and compare its output with `CONTROL_RESULTS.json`; `verify_manifest.py` checks the frozen file hashes. The verifier has no network or external-data dependency and uses Python's standard library only.

The intended connected problem remains unresolved in this attempt. The known unimodular case and the elementary spanning-tree family do not settle the full nonunimodular target. No connected transitive counterexample was found in the certified bounded supports. No general prior resolution was verified. This is a conservative research-status result, not a claim that no later resolution exists.

Five distinct substantive approach families have been recorded. A subjective completion estimate toward a general resolution is 15%; it is a planning estimate, not a probability or a theorem. The finite verifier checks encoded combinatorics and flow certificates; it does not constitute peer review or verify literature completeness.
