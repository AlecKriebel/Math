# Independent audit: totally mixed face posets

Problem 30004231 / OWR-17135-028. Audited 10 October 2026.

Public proof-only edition. This AI-assisted audit is unrefereed; acceptance is not external human peer review, journal acceptance or formal proof-assistant certification. All described scholarly inspections and mathematical computations are historical audit activity. Finite checks are supplementary; the complete mathematical arguments below and in PROOF.md require no omitted program or generated certificate.

**Verdict: ACCEPT_COMPLETE_NEGATIVE_RESOLUTION.** Both universal assertions in the printed problem are false. The accepted proof uses full-dimensional lattice polytopes in dimension five and the standard order complex of the qualifying face poset. No change to the candidate proof is required. This is a correctness verdict, not a novelty claim.

## Source and exact scope

I independently opened the official [Oberwolfach Report 39/2019](https://ems.press/content/serial-article-files/46818) and visually inspected printed page 2464, PDF page 70. Sam Payne's question selects faces of a two-polytope Minkowski sum by positive summand dimensions and equality between the sum-face dimension and the sum of the two dimensions. It asks both about shellability and about rational homology modeled on a wedge of spheres of dimension n−2. The printed paragraph imposes no genericity, full-dimensionality, simpliciality, or facets-only hypothesis. The candidate preserves these conditions and answers both questions using one pair of full-dimensional polytopes.

“Realization of a poset” is interpreted as its order complex, whose simplices are finite nonempty strict chains. The proof does not add a minimum or maximum. Empty faces cannot satisfy the positive-dimension requirement. The whole sum does not satisfy the dimension equality in any of the three examples, so proper-face versus all-face conventions make no difference here. Reversing the order preserves all chains.

## Independent mathematical reconstruction

Let D be the standard four-simplex with vertices v0=0 and vi=ei for 1≤i≤4, and let I=[0,1]. The proposed pair is P1=D×I and P2=(−D)×I in R5. Both have dimension five and integer vertices.

### 1. Complete classification of faces of a simplex difference

For a simplex with m+1 affinely independent vertices and any nonconstant affine value list, the indices attaining the maximum and minimum are disjoint nonempty sets A and B. The exposed face of the difference is

F(A,B)=conv{vi:i∈A}+conv{−vj:j∈B}.

Every disjoint nonempty pair occurs. Assign values 1 to A, −1 to B, and 0 elsewhere, then subtract the value assigned to v0 to obtain a genuine linear functional on the standard simplex. This correctly handles pairs containing the zero vertex. All nonempty proper faces arise this way, because polytopal faces are exposed. A zero functional gives the whole sum, separately handled.

The direction spaces of the two summand faces meet only at zero: a nonzero common vector would give an affine dependence on the disjoint vertex sets, with coefficient sum zero on each set. Affine independence excludes this. Therefore dim F(A,B)=|A|+|B|−2, and the positive-dimension requirement is exactly |A|,|B|≥2.

The inclusion criterion is also exact. If F(A,B) lies in F(C,E), every difference vi−vj with i∈A,j∈B attains the support value of F(C,E). Each of its two summands must attain its own extremal value, so A⊆C and B⊆E. The converse is immediate. This proves both injectivity of the labels and every comparison, rather than merely matching cardinalities.

### 2. No alternate decomposition creates more qualifying faces

If a face F of P+Q exposed by u equals G+H with G⊆P and H⊆Q nonempty, the equality of u-support values forces every point of G and H into the canonical exposed faces P^u and Q^u. For every other functional w, the deficits h(P^u,w)−h(G,w) and h(Q^u,w)−h(H,w) are nonnegative and sum to zero. Both deficits vanish for every w, so G=P^u and H=Q^u. Thus even an existential reading of a decomposition cannot rescue a nonadditive face. The conclusion also applies to the whole sum, using u=0.

The independent computation additionally checked every pair of nonempty summand faces in the three concrete examples. For the main example there are 93 faces of each summand and 8,649 pairs. Exactly 543 pairs give faces of the sum, one canonical decomposition per face; no alternate equal decomposition occurs.

### 3. The base mixed poset is a connected pure graph

For m=4, disjoint mixed pairs have sizes (2,2), (2,3), or (3,2). There are 30 minimal elements of the first type and 20 maximal elements of the other two types. Each minimum is covered by two maxima; each maximum covers three minima. There are no other strict comparisons. Thus the order complex has 50 vertices and 60 edges, and every vertex is incident with an edge.

Suppressing its degree-two vertices gives the bipartite double cover of the graph on two-subsets of a five-element set, adjacent when disjoint. The latter graph is connected: intersecting distinct two-subsets have a common neighbor, their union's two-element complement. It has the explicit odd cycle 01,23,04,12,34,01. A walk lifts to the double cover with parity controlling its final sheet. Detouring to that odd cycle, traversing it, and returning changes parity. Hence the double cover, and the subdivided mixed graph, are connected.

The rational boundary rank is 49 and the first Betti number is 60−49=11. This follows mathematically from a spanning tree and was independently checked by rational Gaussian elimination. A constructive edge shelling of this connected graph is a positive control: the base example does not itself refute shellability.

### 4. The common interval factor excludes every bridge

The sum is (D−D)×[0,2]. Any exposing functional has the form (u,t). When t>0 or t<0, the interval faces of both summands are respectively their upper or lower endpoint. The qualifying faces are then exactly the base mixed faces at height two or zero.

When t=0, both interval faces are the full interval. If the base summand dimensions are a,b and the base sum dimension is c, then the product summand dimensions sum to a+b+2 but the resulting face has dimension c+1≤a+b+1. Additivity is impossible. This covers vertex base faces, higher base faces, and the full base. When u=0 and t≠0, an endpoint face instead has dimension four, while its canonical summand dimensions sum to eight. It also fails.

These cases exhaust every nonempty face. Distinct endpoint layers have no inclusion relations. The mixed poset is therefore a disjoint union of two copies of the base poset.

### 5. Both assertions are false

The order complex is a disjoint union of two connected pure one-dimensional complexes, each with 50 vertices and 60 edges. In any proposed shelling, the first edge from the other component has empty intersection with all earlier facets, whereas a one-dimensional shelling requires a nonempty zero-dimensional intersection. This rules out ordinary pure shellability. Standard nonpure shellability agrees with this requirement on a pure graph, so it does not evade the obstruction.

The complete ordinary rational Betti sequence is (2,22,0,0,…); equivalently, the reduced zeroth Betti number is one. A wedge of three-spheres is connected and has no first homology, including the zero-fold wedge. Hence the rational-homology assertion also fails. No use is made of an empty complex or negative-dimensional sphere convention.

### 6. Smaller control and sharp convention checks

For a three-simplex and its negative in R3, the only mixed pairs partition four vertices into two sets of size two. There are six incomparable faces and hence six isolated vertices in the order complex. Its Betti sequence is (6,0,0,…), inconsistent with a wedge of circles. A zero-dimensional complex is shellable under the usual convention, so this smaller example proves only the homology failure. The candidate explicitly preserves that distinction.

Adding an artificial top would cone off a poset and change the problem. Taking only facets would also change it: the R5 example has mixed faces of dimensions two and three, and no mixed facets of dimension four. The counterexample is deliberately nongeneric; no general-position variant is accepted as resolved.

## Independent exact checks

The independent program does not import or call the candidate verifier. It starts from integer simplex coordinates, constructs all difference points, and discovers every supporting facet hyperplane by enumerating dimension-many point tuples and taking exact integer cofactors. Active-normal ranks verify that the retained boundary points are genuine vertices. All nonempty faces are recovered by intersections of facets. The product facets follow from the independently verified base and the explicit interval product.

A sum of all active outward normals exposes each recovered face. Maximizing that functional on the summand vertices gives the canonical summand faces. All dimensions use rational Gaussian elimination. The code then checks the complete geometric face lattice against the pair-label classification, only after geometric reconstruction.

| Example | Nonempty faces of sum | All ordered face pairs checked | Summand-face pairs checked | Mixed vertices, edges | Betti numbers |
|---|---:|---:|---:|---:|---:|
| D3 and −D3 | 51 | 2,601 | 225 | 6, 0 | 6, 0 |
| D4 and −D4 | 181 | 32,761 | 961 | 50, 60 | 1, 11 |
| D4×I and (−D4)×I | 543 | 294,849 | 8,649 | 100, 120 | 2, 22 |

For the main example the full face counts by dimensions 0 through 5 are 40,140,200,130,32,1. The mixed counts are 0,0,60,40,0,0. Its boundary map has exact rational rank 98. Normal and optimized Python runs produce byte-identical results. The connected base edge shelling and the shellable six-point complex are positive controls. Deliberately removing additivity, admitting vertex summands, forgetting endpoint layers in inclusion, changing the claimed Betti number, or corrupting either shellability distinction must fail; these negative controls run in both Python modes.

The accepted author's strict packet verifier was also rerun normally and with optimization against the frozen external manifest hash, with exact replay enabled. Its successful replay supports reproducibility but is not the basis of the independent proof review.

## Literature and status boundaries

The independently inspected [Adiprasito–Brinkmann–Padrol–Paták–Patáková–Sanyal paper](https://arxiv.org/abs/1607.00347) uses a different condition involving facets of the summands. The [published IMRN article](https://academic.oup.com/imrn/article/2019/6/1894/4085561), 2019(6), 1894–1919, labels the relevant Gale statement Lemma 3.8; the inspected arXiv v1 labels it Lemma 3.7. Those results are not needed for this counterexample, and no contradictory interpretation is assigned to them. The bibliographic status and definition were checked on the current publisher page as well as the local arXiv PDF page 3.

The bounded literature searches are not an exhaustive novelty certificate, and this audit does not turn them into one. The mathematical conclusion is a complete negative answer for the printed unrestricted two-part question under the standard poset-realization convention. It is not a theorem about an unprinted intended variant.

The completed verdict is ACCEPT_COMPLETE_NEGATIVE_RESOLUTION for both printed assertions. The public status and acceptance records reflect that verdict. This edition introduces no mathematical correction and makes no general-position, facets-only or altered-realization claim.

## Accepted bytes and reproducibility

This edition binds the distributed [PROOF.md](PROOF.md): 14,824 bytes, SHA-256 `b6e32c893f45447951cf920777adaaf012b1eb5a9e5a8072a8822fc8fcf2ff28`. [ACCEPTANCE.json](ACCEPTANCE.json) binds both that proof and this complete mathematical audit. All accepted mathematical arguments and substantive audit findings are preserved; changes are editorial only. [MANIFEST.json](MANIFEST.json) records the seven other distributed members. File integrity is not a substitute for the mathematical arguments above.

This proof-only edition includes only the authored proof, complete audit, acceptance, status, source review, README and public verification metadata. Programs, raw outputs, generated certificates, datasets, copied third-party source documents/text/images and private coordination material are excluded. Historical computational methods, finite results and controls are reported above for transparency, without distributing their artifacts.

Edition preparation rechecked the frozen accepted package bytes, including the previously obtained source PDF identities, and checked publication integrity. It did not rerun the original mathematical programs or perform new scholarly retrieval, source-text inspection or literature search. The complete proof and mathematical reconstruction stand independently of the omitted computational artifacts.
