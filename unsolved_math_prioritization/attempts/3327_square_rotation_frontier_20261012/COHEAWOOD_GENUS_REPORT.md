# Co-Heawood: a certified genus-four near-miss

This is the computational part of the second newly documented investigation of problem 3327 / OPG-172. The lifetime investigation count is unresolved. No solution of the unrestricted existence problem is claimed.

## Result

Let G be the point-line nonincidence graph of the Fano plane, with the labels specified below, and let e=(0,10). Exact certificates and finite local-corner checks establish:

- E(G)=n(G)=4. Here E is minimum Euler genus and n is minimum positive nonorientable genus.
- E(G−e)=2 and n(G−e)=3. Its only Euler-genus-two embedding, up to independent vertex switches and rotations of cyclic orders, is orientable.
- E(G/e)≥3, while n(G/e)≤4 by minor monotonicity. This investigation does not decide between Euler genera three and four for this contraction.

Consequently G is neither the required simultaneous minor obstruction for N2 and N3 nor an ordinary Euler hopper. Its nonorientable genus four forces h=2 if it were a target; the displayed deletion does not embed in N2. Its displayed contraction has Euler genus at least three, so it does not meet the hopper drop of at least two. Its equality n(G)=E(G) also excludes the orientably simple Euler-critical route.

Only one specific edge is needed for these exclusions. No unverified edge-transitivity or all-minor claim is used.

## 1. Exact graph identity

The seven points are the nonzero vectors 1,...,7 in F2^3. The lines are the lexicographically ordered triples {a,b,c} with a XOR b XOR c=0:

(1,2,3), (1,4,5), (1,6,7), (2,4,6), (2,5,7), (3,4,7), (3,5,6).

Vertices 0,...,6 represent points 1,...,7; vertices 7,...,13 represent these lines. A point and a line are adjacent exactly when the point is not on the line. This defines 14 vertices, 28 edges, degree four at every vertex, no triangles, and exactly 21 distinct squares. The deletion removes (0,10). The contraction identifies 10 with 0 and removes the contracted edge; no parallel edges arise. The contracted graph has 13 vertices, 27 edges, degree six at vertex 0, degree four elsewhere, exactly three triangles and exactly eighteen squares.

The verifier reconstructs the graph directly from the XOR definition and checks every certificate's complete vertex set, edge set, rotations, and signs against it. It does not accept a certificate merely because the graph name matches.

## 2. Local-corner selection lemma

In a cellular embedding, the incident half-edges at a vertex v form a cyclic order. Its link is a simple cycle on deg(v) symbols, one for each incident edge. A facial graph cycle uses the corner between its two incident edges at v. Distinct faces cannot use the same corner.

Thus a selected collection of prospective facial cycles is necessarily compatible with a cyclic link at each vertex: its required corner pairs must be distinct and must be contained in some Hamilton cycle on that vertex's incident-edge symbols. At degree four there are exactly three unoriented cyclic orders; at degree three there is one; at degree six there are sixty. The finite check enumerates these entire lists, up to cyclic shift and reversal, and intersects the permitted orders with each required corner.

This is a necessary condition only; compatible corner selections are not automatically embeddings. In particular, disconnected partial paths in a link are allowed. A proper cycle on fewer than all incident-edge symbols is disallowed. A triangle is an allowed complete link at degree three but is disallowed at degrees four and six. These distinctions are explicitly tested.

All graphs here have minimum degree at least three and are simple. A length-three or length-four facial walk, when possible, is a simple graph cycle: a repeated vertex would force an immediate reversal at a vertex of degree one, or a loop. The same graph triangle or square cannot appear as two distinct faces: both sides at every vertex would require degree two. Therefore these short faces select distinct members of the complete graph-cycle lists. The statement concerns short faces only; no simplicity is assumed for longer facial walks.

## 3. Lower bound E(G)≥4

Every cellular embedding of G is bipartite, so every facial walk has even length at least four. Exhaustive corner selection checks every one of the C(21,11)=352,716 eleven-square subsets. None is locally compatible. Hence any cellular embedding has f4≤10 square faces.

If F is the total number of faces, then

56 = 2|E(G)| ≥ 4f4 + 6(F−f4) = 6F−2f4 ≥ 6F−20.

Thus F≤12. Euler's formula gives E=2−14+28−F≥4 for every cellular embedding. Capping a regular neighborhood of any embedding cannot increase Euler genus, so this is also a lower bound against arbitrary, possibly noncellular embeddings.

The initial discovery separately checked all 293,930 twelve-square subsets and found none; this is redundant for the final proof because an admissible twelve-square set would contain an admissible eleven-square set. No failed heuristic search is used for the lower bound.

### Compact independent orbit certificate

[COHEAWOOD_SQUARE_ORBIT_CERTIFICATE.json](COHEAWOOD_SQUARE_ORBIT_CERTIFICATE.json) provides a much smaller exhaustive certificate in addition to the direct 352,716-subset check. The 168 invertible linear maps of F2^3 act on points, lines and the twenty-one squares. Each map is specified by its images of the basis vectors 1,2,4. The verifier reconstructs and checks every resulting graph automorphism.

At any vertex, the six graph squares use the six different neighbor pairs. A subset of these pairs extends to a four-cycle exactly when it contains neither a three-edge star nor a triangle. Thus incompatibility is witnessed by a triple of square indices. Across all vertices there are eighty-four distinct forbidden triples; all are explicitly recorded and independently regenerated from the full link-cycle test.

Starting with the empty set, the certificate lists a canonical representative for every compatible square-set orbit. Every possible addition of one square to every listed representative is checked. An incompatible extension contains a recorded forbidden triple; a compatible extension is mapped by a verified automorphism into the next listed level. Induction therefore covers every compatible subset without assuming that the list is complete merely from its length.

The numbers of orbit representatives for subset sizes zero through eleven are

1, 1, 4, 14, 39, 83, 128, 119, 67, 17, 2, 0.

The corresponding full numbers of compatible subsets are

1, 21, 210, 1246, 4725, 11655, 18438, 17874, 9765, 2604, 252, 0.

The empty size-eleven level is an exact lower-bound certificate. Its replay rejects missing representatives, missing automorphisms, missing forbidden triples, and altered squares. This orbit argument and the direct subset enumeration agree; neither relies on solver status or a heuristic stopping condition.


## 4. Exact N4 embedding

[COHEAWOOD_N4_CERTIFICATE.json](COHEAWOOD_N4_CERTIFICATE.json) specifies all rotations and edge signatures. The signed-dart face permutation has twelve physical faces: ten of length four, one of length six, and one of length ten. Therefore χ=14−28+12=−2.

A negative-sign simple cycle is included and checked; equivalently the signed orientation double cover is connected. The embedding is nonorientable, so the surface is N4. This proves n(G)≤4. Section 3 then proves E(G)=n(G)=4.

The independent flag-involution replay also checks that the edge, side and corner identifications form a closed connected surface; it computes faces and orientability by a different procedure.

## 5. The deletion is toroidal but not Klein-bottle embeddable

Write D=G−(0,10). It is connected and bipartite with 14 vertices, 27 edges and minimum degree three. The girth/Euler inequality gives E(D)≥2. If D embedded in N2, its capped regular-neighborhood embedding would have Euler genus exactly two. Equality forces the complementary regions to be disks, so the capped surface would also be N2. Such an embedding has F=13 and total face length 54; therefore its face profile is twelve squares and one length-six walk.

D has eighteen graph squares. All C(18,12)=18,564 twelve-square subsets are checked. Exactly one has compatible corners. At the two degree-three endpoints the link is K3; at every other vertex it is C4. For this one subset every local unoriented cyclic order is forced.

Normalize each local cyclic order by placing its least neighbor first and choosing the direction with second entry less than last entry. This chooses one representative of each local order modulo reversal. Independent reversals at vertices, accompanied by negating the signs of incident edges, are vertex switches and do not change the embedded surface.

For an oriented square q=(v0,v1,v2,v3), let ti=+1 when vi+1 immediately follows vi−1 in the normalized rotation at vi, and let ti=−1 when it immediately precedes it. The edge signature required for the square to be a face is

sign(vi,vi+1)=ti ti+1.

All twelve selected squares give consistent equations. They cover all 27 edges, so all edge signs are forced. Thus there is exactly one normalized signed-rotation completion; there are no leftover edge-sign variables or local-order choices. Its explicit certificate is [COHEAWOOD_DELETE_0_10_TORUS_CERTIFICATE.json](COHEAWOOD_DELETE_0_10_TORUS_CERTIFICATE.json).

Replay gives twelve square faces and one hexagon, χ=0, and an orientable surface. The certificate includes a vertex sign potential p with sign(uv)=p(u)p(v) on every edge, an exact orientability witness. This unique completion is a torus embedding, so no N2 embedding exists. A torus embedding plus a crosscap in a disjoint disk embeds D in N3. Therefore E(D)=2 and n(D)=3.

The uniqueness claim is restricted to Euler-genus-two cellular embeddings. It is not a classification of higher-genus embeddings.

## 6. The contraction has Euler genus at least three

Write C=G/(0,10). It has 13 vertices and 27 edges, with exactly three graph triangles and eighteen graph squares. In a cellular embedding let f3 be the number of triangular faces. By the short-face observation, f3≤3. All other faces have length at least four. If E(C)≤2, Euler's formula gives F≥14, while

54 ≥ 3f3+4(F−f3) = 4F−f3 ≥ 4F−3.

Hence F=14 and E(C)=2. The excess identity is

Σ over faces of (length−4) = 54−56 = −2.

It follows that f3 is two or three, with exactly these possible profiles:

- Two triangles and twelve squares.
- Three triangles, ten squares, and one length-five face.

For the first profile all 3*C(18,12)=55,692 triangle/square selections are checked. For the second all C(18,10)=43,758 selections are checked. None passes the necessary local-corner test. The degree-six link at the contracted vertex is checked against all sixty unoriented cyclic orders; proper subcycles are not mistaken for a valid link. The remaining links are degree four.

Therefore E(C)≥3. The proof does not assume that the possible length-five face is a simple cycle and does not need to construct it. Contraction monotonicity from the N4 certificate gives n(C)≤4.

## 7. Verification, scope, and remaining work

The exact verifier regenerates all short cycles from graph adjacency, checks complete enumeration counts, independently replays the signed-rotation certificates, and verifies the deletion's canonical completion uniqueness. Vertex-switch controls cover every vertex. Hostile mutations include false face counts, false orientability, duplicate rotation neighbors, missing edges, zero signatures and a wrong Fano line. The corner checker includes disconnected-path positive controls and proper-cycle negative controls. All checks use explicit exceptions rather than Python assertions and are run in ordinary Python, -O and -OO modes.

The discovery scripts and raw search output are retained separately from the authored mathematical report and exact certificates. A bounded 100,000-proposal constructive walk for a genus-three contraction embedding found no witness. That failure has no nonexistence meaning and contributes nothing to the contraction lower bound. No claim is made that E(C)=4 or that C has no N3 embedding.

This is a precise exclusion of one natural graph on the first-genus frontier. The unrestricted simultaneous-minor-obstruction problem remains unresolved. The [structural report](STRUCTURAL_REPORT.md) establishes broader exclusions; none is needed for this graph-specific proof.
