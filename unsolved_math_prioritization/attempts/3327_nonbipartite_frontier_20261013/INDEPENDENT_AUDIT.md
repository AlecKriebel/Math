# Independent acceptance audit: third documented surface-obstruction pass

Target: problem 3327 / OPG-172. This audit concerns the third newly documented substantive investigation. The lifetime investigation count remains unknown. The unrestricted problem remains unresolved.

## Accepted results

Subject to the exact accepted public-byte identities in the [acceptance record](ACCEPTANCE.json), the structural argument and complete small-order computation establish the following.

1. In a simple quartic triangle-free K_(2,3)-free graph having two or three squares through every edge, every pentagon contains at most two three-square edges.
2. For an h=2 simultaneous obstruction or an ordinary Euler hopper of Euler genus four, let T be its subgraph of three-square edges, D2 its degree-two vertices and F its degree-four vertices. The F vertices are independent. Every T-component containing F has a unique partition into squares. At least one other nontrivial component is a cycle of length at least six. The total length B of all such cycle components whose lengths are not four is a positive multiple of four and is at least eight. Moreover |D2| >= 2|F| + B >= 2|F| + 8.
3. Every h=2 simultaneous obstruction and every ordinary Euler hopper of Euler genus four has at least sixteen vertices. More precisely, every connected graph in the stated quartic square-rich class through order fifteen that passes the accepted pentagon-incidence conditions has Euler genus two.

These conclusions neither produce an obstruction nor eliminate the remaining isolated cycle components, larger orders, higher genus, or the positive orientably simple Euler-critical route. No novelty or historical global-status claim is accepted.

## 1. Dependencies and quantifier checks

The [first structural report](../3327_surface_obstruction_reductions_20261012/STRUCTURAL_REPORT.md), [second structural report](../3327_square_rotation_frontier_20261012/STRUCTURAL_REPORT.md), and [second independent mathematical audit](../3327_square_rotation_frontier_20261012/INDEPENDENT_AUDIT.md) were read. Their complete retained editions and exact public identities are preserved. The third pass inherits the triangle augmentation, quarticity, K_(2,3)-freeness, two/three-square condition, square-selection equivalence, and alternating contraction-face argument from those accepted reports. It does not independently re-prove the underlying cited literature.

The new pentagon lemma is a theorem about the entire stated graph class, with no minor or embedding assumption. Independence of F requires that every edge lie on a pentagon. The exact complementary-edge and square-propagation assertions require the contraction embedding conditions of an h=2 target or Euler-genus-four hopper. They are not inferred merely from a numerical pentagon count.

The extension to ordinary Euler-genus-four hoppers uses the accepted Euler-minor conditions, not an assumption that their minors embed in the Klein bottle. An Euler-genus-two certificate for a tested graph excludes it from both target classes here because those classes have Euler genus four. Surface orientation is reported only for the particular supplied square-disk certificate; a torus certificate alone is not used to rule out a separate Klein-bottle embedding.

## 2. Pentagon scarcity

For each vertex v_i of a fixed pentagon, the possible second common neighbor x_i of its two pentagon neighbors is unique by K_(2,3)-freeness. It is outside the pentagon: a chord in a pentagon creates a triangle. Two distinct x_i cannot coincide, since their prescribed pentagon-neighbor sets together contain adjacent vertices.

A three-square edge yields a perfect matching between the three other neighbors of its endpoints. This matching fact follows directly from the codegree bound. For example, two crossedges from a in A to b1,b2 in B would make a and the opposite original endpoint share three common neighbors. An early draft reversed the A/B names in this explanatory sentence; the corrected version is the accepted one.

If v_i v_(i+1) is a three-square edge, its two adjacent second-neighbor conditions hold. If the two next outward conditions also held, quarticity would exhaust both sets of three neighbors. Two matching pairs are already forced; the third would join x_(i-1) to x_(i+2). Those vertices already share v_(i+3), producing a triangle.

Three selected edges of a pentagon either cover all five vertices or are a consecutive three-edge path. In the first case all five second-neighbor conditions hold; in the second the middle edge has all four forbidden conditions. Both contradict the previous paragraph. This supplies the complete final combinatorial case rather than an informal statement that three edges must be adjacent.

If an edge joins two F vertices, a pentagon through that edge has three three-square edges: the edge itself and the other incident pentagon edge at each endpoint. Thus F is independent. Every neighbor of F belongs to D2, and counting the four incident edges of each F vertex gives |D2| >= 2|F|.

## 3. The contraction corner condition and full-link rigidity

At f in F, its four neighbors a,b,c,d have six distinct second neighbors x_ij. Their distinctness follows from the codegree bound, and the four original neighbors have no additional neighbor slots. Consequently each pentagon through f corresponds exactly to an edge between complementary pair labels, such as x_ab x_cd. An edge between overlapping labels would create a triangle.

There are only three complementary pairs. If r of their edges occur, f lies on exactly 4r pentagons and every edge incident with f lies on exactly 2r. These are complete counts: unknown edges farther away cannot create another pentagon through f, because the neighbors of f are already saturated.

The low-genus contraction rotation is an alternating six-cycle on the A and B edge ends. In the two-triangle face profile, exactly four remaining corners at the contracted vertex are quadrangular. Their faces lift to four distinct pentagons. In the three-triangle profile, the three triangle corners form a perfect matching in that six-cycle, so the other three corners form a second perfect matching. At least two of those corners are quadrangular and must therefore have different B ends.

For r=1 there are only two pentagons through an incident edge, and both yield corner pairs with the same B end. Neither profile is possible. This validates the stronger endpoint-pair argument; the scalar count of two pentagons would not by itself reject this case.

No new surface surgery is asserted. The argument uses the previously accepted alternating rotation and face profiles. Facial simplicity is essential: in a simple graph of minimum degree at least four a facial walk of length at most five cannot repeat a vertex, since a repeated vertex would split it into closed subwalks and force a loop or immediate reversal. Thus the unique pentagonal face visits the contracted vertex at most once. Distinct quadrangular faces give distinct lifted pentagons because the same square cannot bound two faces in this degree range.

At r=3, every radial edge from a neighbor of f to a second neighbor occurs in a pentagon already containing two three-square edges at f. The pentagon lemma would make every radial edge a two-square edge, contradicting the D2 status of the neighbor. Hence r=2 exactly. The sole absent complementary pair identifies the four radial edges that must be three-square edges. Together with the edges at f they give exactly two all-three-square squares, partitioning the four incident edges.

The additional contraction-face rigidity also checks: for r=2, one B end has no lifted-pentagon support and only its one possible triangular corner. The two-triangle profile cannot give that end degree two. Nor can the three-triangle profile when its pentagonal face avoids the contracted vertex. Thus the unique pentagonal face must pass through that vertex. This does not itself rule out such an embedding.

## 4. Global propagation and the unresolved component type

At a D2 vertex, every all-three-square square must use its two three-square edges. Two such squares with different opposite vertices would violate the codegree bound, so the square is unique whenever it exists. At an F vertex the preceding proof supplies exactly two such squares and covers all four edges.

Starting from an F vertex, covering either edge at a D2 vertex covers both. Reaching another F vertex supplies its two forced squares. The uniqueness at every shared D2 corner prevents overlap conflicts. Propagating along the connected component therefore yields a unique edge partition into squares. This is a genuine global compatibility proof, not an inference from arbitrary local links.

A nontrivial T-component without F is a connected two-regular simple graph, hence a cycle. Such a component is square-decomposable exactly when it has length four. Triangles are forbidden by triangle-freeness; pentagons entirely in T are forbidden by the new lemma. If all these components had length four, the accepted square-selection equivalence would give Euler genus two, contradicting genus four. Hence at least one has length at least six.

The incidence identity 4s = 2|E2| + 3|E3| = 4n + |E3| makes |E3| divisible by four. Removing the square-decomposed components leaves B, a positive multiple of four. Since each remaining component has at least six edges, B is at least eight. The assertion concerns the sum of the residual lengths. It does not independently exclude a length-six component accompanied by others. Those B cycle vertices have no F-neighbor, so the incidence count sharpens to 4|F| <= 2(|D2|-B), validating |D2| >= 2|F|+B.

## 5. Complete finite exhaustion through fifteen vertices

The root-pattern reduction was independently checked. With a root and its four neighbors fixed, every remaining vertex has at most two root-neighbor incidences. Each pair label appears at most once. The graph formed by the pair labels has degrees two or three on four vertices. Exhausting all 64 subsets of its six possible edges gives exactly three C4 patterns, six diamonds and one K4, each of which is represented by the author's canonical choice.

For p pair labels, there are 12-2p singleton labels and n+p-17 empty labels. The empty-label vertices are retained and separately labeled. The generator therefore covers every admissible connected graph up to a harmless relabeling of root neighbors and outside vertices. It does not assert that its leaves are distinct isomorphism classes. Unknown edges occur only between outside vertices.

The author's incremental triangle and codegree tests reject monotone violations, and its available-neighbor bound is an upper bound on future choices. Neither can discard a completable branch. Every row's higher-numbered neighbors determine one branch, so no adjacency is omitted. Disconnected intermediate graphs are permitted as a harmless superset; every square-rich survivor is independently checked to be connected before its surface certificate is used.

Orders below twelve are excluded directly. Twelve two-step walks from a root require at least six outside vertices. Equality at eleven vertices would make every vertex belong to six squares, giving a total of 66 vertex-square incidences, not divisible by four.

The independent enumerator does not import the author's generator. It first enumerates degree-sequence completions with disjoint root labels and degree-capacity pruning only, then applies whole-graph triangle and codegree tests. It deliberately omits the author's incremental triangle and codegree pruning. All twelve complete ordered leaf-adjacency stream hashes agree, not merely the surviving counts.

The exact residual-completion counts for root types p=4,5,6 are:

- n=12: 0, 1, 0
- n=13: 2, 0, 0
- n=14: 43, 56, 42
- n=15: 1464, 1386, 360

There are 3,354 leaves and 37 square-rich survivors. Independent reconstruction by opposite-vertex common-neighbor pairs finds the same square sets. Pentagons are reconstructed from an edge and a four-edge return path, separately from the author's depth-first cycles and the author's verification harness using vertex permutations.

Every one of the 31 positive certificates is checked for exact omitted-square multiplicities, two retained disks per graph edge, simple connected C4 vertex links and Euler characteristic zero. The independent orientation equations yield 19 orientable and 12 nonorientable supplied surfaces. The six remaining survivors have an explicitly verified bipartition and no pentagons. No failed exact-cover search is needed for their exclusion. The complete survivor-graph inventory agrees with the independent enumeration.

The n=12 result also has a short reconstruction proof: five pair labels and two singleton labels force the unique graph, while six pair labels plus one empty vertex would force that empty vertex to have degree six. The independently checked twelve-square surface certifies genus two.

## 6. Hostile controls, replay modes and preservation

Independent local controls exhaust 1,024 choices of pentagon-edge and second-neighbor flags; only zero, one or two selected three-square edges survive the necessary implications. They also inspect all eight complementary-pair edge subsets at an F vertex, all four incident contractions in each, and all six Hamilton six-cycles in K_(3,3). They recover the exact radial option count 3-r per neighbor and the exclusive r=2 contraction profile. These are finite corroborating checks, not substitutes for the unbounded written proof.

Positive surface controls use Q4 and C5 Cartesian C5. A separately reconstructed co-Heawood graph supplies a negative exact-cover control. Missing omitted squares, duplicated face catalogues and absent covers are rejected. Independent author-certificate mutations reject duplicate adjacency, a missing omitted square, a false pentagon count, a duplicated omitted square and a false full-stream hash.

The independent certificate replay and local rigidity replay were executed in normal Python, -O and -OO, with byte-identical respective outputs. The author's finite harness was also replayed in all three modes. Essential checks raise explicit exceptions; no assertion-only validation is accepted. Exact final author reports, certificates and verification programs are pinned in the complete audit manifest and acceptance record.

A compact recovery archive and a separately read-back byte store contain the actual author bytes, dependency reports, independent checks and audit outputs, rather than nested prior archives. Restoration rechecks the full inventory and re-executes the certificate and local checks in all three modes. Preservation details are recorded separately from the publication payload.

## Boundary of acceptance

The third pass gives a structural description of the surviving three-square components and a verified finite lower bound of sixteen vertices. It supplies no graph meeting all minor conditions and no contradiction for the remaining cycle components. The general simultaneous-obstruction question remains unresolved.

No new external source was retrieved. Public audit material contains authored mathematics and verification metadata only; raw discovery files, copied source documents and private coordination material are excluded.
