# Structural reductions for simultaneous nonorientable obstructions

Target: problem 3327 / OPG-172. This is the first newly documented substantive investigation in this edition; the lifetime attempt count is unknown.

## Endpoint

No example or nonexistence proof is established here. The results below reduce the unrestricted existence question to two ordinary-graph genus phenomena, identify a rigorous amplification construction, prove triangle-freeness and minimum degree four, and sharply restrict the first possible genus h=2. The triangle exclusion is credited to Campbell (2017), with a direct explanation given here. The reductions are independently derived from the cited genus formulas; no novelty claim is made.

## Conventions and credited inputs

All graphs here are finite ordinary simple graphs. Contracting an edge suppresses loops and parallel copies. This does not change surface embeddability. Let E(G) denote Euler genus (minimum over orientable and nonorientable surfaces, with orientable genus doubled). Let n(G) denote the least positive integer h such that G embeds in the closed nonorientable surface N_h. Thus n(G)=1 for a planar graph, including a forest. This convention avoids the irrelevant tree exception in some combinatorial-embedding definitions. Set s(G)=n(G)-E(G).

For every graph, s(G) is 0 or 1; s(G)=1 implies E(G) is even and a minimum-Euler-genus embedding is orientable. For positive Euler genus this is precisely the usual notion of orientably simple. Indeed E=min(2g,n), while n<=2g+1: a crosscap may be added to an orientable minimum-genus embedding. If E<n, integrality gives n=E+1=2g+1.

We use Euler-genus additivity over blocks and components and the Stahl–Beineke nonorientable formula. For a 1-sum or disjoint union of cyclic nonplanar graphs A and B,

  E(A union B)=E(A)+E(B),
  n(A union B)=E(A)+E(B)+s(A)s(B).

Here "union" means either a 1-sum or disjoint union; the same block/component formula applies. Attaching or discarding a planar block does not affect actual positive-surface embeddability. The cyclic nonplanar form suffices for the main doubling proof. A single untouched nonorientably simple summand forces the resulting sum to have s=0, even when the other summand becomes planar. In that case the upper bound follows by embedding the planar summand in a disk, and the lower bound follows from Euler-genus additivity.

Sources: Mohar–Skoda, arXiv:1406.1341v1, Lemma 2.1, Theorems 2.2 and 6.2; these credit Stahl–Beineke for the block formula. Do NOT apply the printed 1-sum formula mechanically with that paper's special tree n=0 convention: that would incorrectly make a tree attachment lower the nonorientable genus of an orientably simple graph. The positive-surface convention here avoids that issue. No full audit of the original 1977 Stahl–Beineke proof has been performed. The positive-surface convention is also explicitly used by Parsons, Pica, Pisanski and Ventre, Orientably simple graphs, Mathematica Slovaca37(1987)391–394, https://dml.cz/handle/10338.dmlcz/129376; see the [source audit](SOURCE_AUDIT.md) for source identity and inspection scope.

## 1. Exact genus jump and elementary necessary conditions

Suppose G does not embed in N_(h+1), but every proper minor embeds in N_h, where h>=1. Adding one missing edge to an embedding costs at most one handle, or two crosscaps: take small disks near its endpoints, attach a tube disjoint from the graph, and route the edge through it. Consequently n(G)<=n(G-e)+2<=h+2 for any edge e. Since n(G)>=h+2, equality holds:

  n(G)=h+2 and n(G-e)=h for EVERY edge e.

Contractions satisfy n(G/e)<=h; no unjustified bound on the amount a contraction can lower genus is used. This proves that any two distinct nonorientable surfaces for which G is simultaneously a minor obstruction must be consecutive: if the smaller is N_a and the larger N_b, then b>=a+1 and a+2>=n(G)>=b+1, forcing b=a+1 and n(G)=a+2.

A target has no isolated vertex, degree-one vertex, degree-two vertex, bridge, loop, or parallel-edge redundancy. An isolated vertex can be discarded without affecting embeddings. A pendant edge or bridge can be contracted without affecting embeddability. A degree-two vertex can be suppressed by contraction; an embedding of the resulting graph extends by subdivision, including the case where simplification removes a duplicate edge. Loops and parallel copies can be drawn in a thin neighborhood and likewise do not create a minimal surface obstruction. In particular, every simple target has minimum degree at least three.

For a simple graph of positive minimum degree, checking deletion and contraction of every edge suffices to check all proper minors: deleting a vertex can start by deleting one incident edge, and every remaining minor operation is embedding-monotone. Isolated-vertex deletion must still be addressed if the minimum-degree hypothesis is absent.

## 2. Exact orientability dichotomy

Call an ordinary graph C Euler-critical if every proper minor has strictly smaller Euler genus. Call H an ordinary Euler hopper if E(H)>=2 and every proper minor has Euler genus at most E(H)-2. The positive genus floor excludes the vacuous empty graph. These definitions have no terminal labels or excluded terminal-edge operations.

### Proposition A: the orientably simple case

If C is nonplanar and s(C)=1, then C is a target if and only if C is Euler-critical.

Proof. Put r=E(C), so r is even and n(C)=r+1. If C is a target, every proper minor M has n(M)<=r-1, hence E(M)<=r-1. Conversely, suppose E(M)<=r-1 for every proper minor. If E(M)=r-1, its Euler genus is odd, so s(M)=0 and n(M)=r-1. If E(M)<=r-2, then n(M)<=E(M)+1<=r-1. Therefore all proper minors embed in N_(r-1), whereas C does not embed in N_r. Here r>=2, so h=r-1>=1. QED.

### Proposition B: the non-orientably-simple case

If s(G)=0 and r=E(G)=n(G)>=3, then G is a target if and only if:

  (i) G is an ordinary Euler hopper; and
  (ii) no proper minor M has E(M)=r-2 and s(M)=1.

Proof. The target condition is exactly n(M)<=r-2 for every proper minor. Since n(M)=E(M)+s(M), it implies both (i) and (ii), and these two conditions imply it. If r is odd, condition (ii) is automatic by parity, because r-2 is odd. Thus every odd-Euler-genus Euler hopper with s=0 is already a target. QED.

The word "Euler" cannot simply be omitted: an even-genus Euler hopper can have a top-level orientably simple minor, producing a drop of only one in nonorientable genus.

## 3. Doubling removes the exceptional-minor problem

### Proposition C

If any ordinary Euler hopper H exists, then a target exists. If s(H)=1, H itself works by Proposition A. If s(H)=0, the disjoint union of two copies of H is a target; a 1-sum of the two copies also works when H is connected.

Proof for the s=0 case. Put r=E(H)=n(H). The two-copy graph D has n(D)=E(D)=2r. Apply an elementary deletion or contraction to one copy, producing H'. The other copy H remains untouched and has s(H)=0. The block/component formula therefore gives

  n(H' union H)=E(H')+r<=2r-2.

If H' is planar, the equality is still valid by putting it into a disk, together with Euler-genus additivity for the lower bound. Isolated vertices in H or any genus-zero redundant block are incompatible with the all-proper-minor hopper condition. Therefore the all-proper-minor condition follows from the elementary checks. D is simultaneously an obstruction for N_(2r-2) and N_(2r-1). QED.

This construction is conditional. No ordinary Euler hopper has been supplied by this investigation.

### Corollary: equivalent existence problem

The unrestricted OPG target exists if and only if at least one of the following exists:

  (A) a nonplanar orientably simple Euler-critical ordinary graph;
  (B) an ordinary Euler hopper.

Forward implication is Propositions A and B; reverse implication is Propositions A and C. This reformulation retains both deletion and contraction and does not confuse terminal-labelled hopper classes with ordinary graphs.

Moreover, it suffices to find a 2-connected graph in either class A or B. Euler genus is block-additive. Euler criticality/hopping therefore passes to every positive-genus block, and no genus-zero block can occur in a critical graph. In class A, all positive-genus blocks are orientably simple by the same Stahl–Beineke formula. Thus a positive-genus 2-connected block lies in the same class. A 2-connected class-B graph can then be doubled using a 1-sum, giving a connected target. This is an existence reduction, NOT a claim that every target is 2-connected or 3-connected.

## 4. Triangle exclusion: a credited local augmentation lemma

Campbell's 2017 dissertation, Lemma 5.3 (printed pp.47–48), states that an obstruction for a surface S which contains a triangle embeds in the nonorientable surface of Euler genus gamma(S)+1. Applying this to S=N_h proves:

  EVERY target for OPG-172 is triangle-free.

This is not a new theorem claimed by this investigation. Campbell proves it by starting from an embedding of G-uv, where uvw is a triangle. If u and v share a face, uv can already be inserted. Otherwise write the cyclic order at w as (wu, X, wv, Y). Reverse the consecutive block X and reverse the signatures of the edges in X. This local crosscap insertion merges the two distinct faces at the ends of that block and preserves all other facial boundary walks. The merged boundary exposes u and v. Insert uv in that face with the compatible signature. The total Euler-genus increase is one; the modification has added a crosscap.

The consequence is valid regardless of the genus h, the connectivity of G, or the degrees of the triangle vertices. The previously available degree-three-triangle observation is strictly weaker. Complete graphs and any construction retaining even one triangle are excluded immediately.

The local construction also gives the following arbitrary-graph augmentation: if uv lies in a triangle, then n(G)<=E(G-uv)+1. Start with minimum-Euler-genus embeddings of the components of G-uv, perform the crosscap construction in the triangle component, and combine the remaining component embeddings. The changed component is nonorientable, so the genus of the combination is at most the sum of component Euler genera plus one. When the endpoints are already cofacial, insert uv first and, if needed, add a crosscap in a complementary disk. This argument does not require a cellular embedding of a disconnected graph. For an explicit orientability check, switch local signs so the two old triangle edges are positive; the inserted triangle edge is negative, making the completed triangle one-sided. The augmentation is independently explained here and has also received independent local signed-rotation checks; the credited source states the obstruction corollary.

Campbell's Theorem 5.5 (printed pp.48–50) further states that every minor obstruction for S that is not minimal under the enlarged double-wye-delta order embeds after adding one crosscap. Therefore a target must also be double-wye-delta-minimal for N_h. In particular, Y-to-triangle replacement at any cubic vertex, and the allowed double-Y move at adjacent cubic vertices, must yield an N_h-embeddable graph. This is a sourced restriction; the long local case proof has been read, but an independent full verification of all its rotation cases has not been completed. It is not needed for Propositions A–C or the triangle-free conclusion.

## 5. Cubic vertices are impossible: contraction is essential

### Proposition D

Every target is triangle-free and has minimum degree at least four. Both auxiliary classes A and B likewise are triangle-free with minimum degree at least four.

Proof. Triangle-freeness is Section 4. Vertices of degree at most two were already excluded. Suppose u has degree three with neighbors v,a,b. Contract uv, identifying the result with v, to obtain H. Because G is triangle-free, neither va nor vb was an edge of the original G; hence the edges va and vb in H arise uniquely from ua and ub. Subdivide va by a new vertex u, obtaining J. This does not change surface embeddability. Add the edge ub. Its endpoints have common neighbor v, so the arbitrary-graph triangle augmentation yields

  n(J+ub)<=E(J)+1=E(G/uv)+1.

Delete the old edge vb. The resulting graph is exactly G: its incident edges at u are ua,uv,ub, and the remaining original edges are unchanged. Therefore

  n(G)<=E(G/uv)+1.

For a target, E(G/uv)<=h, so this would embed G in N_(h+1), a contradiction. For an ordinary Euler hopper of Euler genus r, the same inequality implies E(G)<=r-1, again a contradiction. For an orientably simple Euler-critical graph, n(G)=r+1 but E(G/uv)<=r-1, giving n(G)<=r. QED.

For the auxiliary classes, the triangle exclusion itself follows from n(G)<=E(G-e)+1. If G is an Euler hopper, this contradicts E(G)<=n(G); if it is orientably simple Euler-critical, it contradicts n(G)=E(G)+1.

This is an independently derived consequence of the credited local triangle construction. It uses edge contraction and therefore does not apply automatically to the historical deletion-only question.

## 6. Counting consequences and the first possible genus

Write n=|V(G)|, m=|E(G)|, and c for the number of components of a target. The minimum degree gives m>=2n. Every deletion G-e still has minimum degree at least three and embeds in N_h. Use minimum-Euler-genus cellular embeddings of its components. Every facial boundary walk has length at least four: triangle-freeness excludes length three, and a facial immediate reversal at a simple edge requires degree one at its reversal vertex. Consequently, summing Euler's formula componentwise gives

  m-1<=2n-4c+2h.

Here deleting an edge does not change the component count because a target has no bridge. The sum of component Euler genera is at most h. Thus

  2n<=m<=2n+2h-4c+1,
  h>=2c.

In particular h>=2. This excludes the projective-plane/Klein-bottle pair by elementary arguments, without enumerating the 35 projective-plane forbidden minors.

The same argument excludes class A at Euler genus two and class B at Euler genus two or three: those cases would have all deletion Euler genera at most one (or zero), while minimum degree four and triangle-freeness give m>=2n. Thus every positive-genus block arising in the A/B reduction has Euler genus at least four. A target is Euler-critical, so it has no redundant genus-zero block; Euler block additivity implies E(G)>=4b, where b is its number of positive-genus blocks. Since E(G)<=h+2, targets with h<=5 have only one block and are 2-connected.

For h=2, c=1, n(G)=E(G)=4, and

  m=2n or m=2n+1.

The first case is 4-regular. In the second case, total degree excess over four is two, so the graph has one degree-six vertex or two degree-five vertices and every other vertex has degree four. Section 8 will eliminate that second case.

### Edge-deleted face profiles at h=2

For each e, the graph G-e is connected, triangle-free, and has minimum degree three. The density bounds force its Euler genus to be exactly two: m-1 is at least 2n-1, above the projective-plane bound 2n-2. Since it actually embeds in N_2, take a cellular Klein-bottle embedding. A cellular minimum-Euler-genus embedding could alternatively be orientable; no equality between orientable and nonorientable genus is inferred from density alone.

- If m=2n+1, then G-e has 2n edges and n faces. All facial boundary walks have length four.
- If m=2n, then G-e has 2n-1 edges and n-1 faces. The sum of (face length minus four) is two. Thus there is one length-six facial walk or two length-five facial walks, and all other facial walks have length four. In a bipartite graph only the length-six alternative occurs.

These are statements about facial boundary walks; no unsupported simplicity assumption about long facial walks is made.

## 7. Square incidence and the local rotation restriction

### Contraction lower bound at h=2

Contract an arbitrary edge e=uv. Triangle-freeness ensures no parallel-edge suppression, so G/e has n'=n-1 vertices and m'=m-1 edges. Its minimum degree is at least four. It embeds in N_2 and has Euler genus at most two. In cellular minimum-Euler-genus embeddings of its components, let F be the total number of faces and f_3 the number of triangular faces. There are no faces of length one or two. Therefore

  2m'>=3f_3+4(F-f_3),
  f_3>=4F-2m'>=2m'-4n'.

The last inequality uses F=m'-n'+2c'-E(G/e), with c'>=1 and E(G/e)<=2. A triangle cannot bound two faces here: that would use both angles between its two incident edges at each vertex, forcing those vertices to have degree two. Thus f_3 counts distinct graph triangles. Every triangle of G/e uses the contracted vertex and corresponds uniquely to a 4-cycle of G through e; G had no triangles. Consequently:

- if m=2n, every edge belongs to at least two distinct 4-cycles;
- if m=2n+1, every edge belongs to at least four distinct 4-cycles.

### Consecutive corners are forbidden

Fix an N_h embedding of G-uv and a 4-cycle u-a-b-v-u. If ba and bv were consecutive in the rotation at b, a and v would share the face corner along a-b-v. Add av in that face. Then the missing edge uv completes triangle u-a-v, so the local crosscap construction embeds G+av in N_(h+1). Deleting av contradicts the target condition. Hence ba and bv are NOT consecutive. By symmetry, au and ab are NOT consecutive either.

This conclusion holds in every N_h embedding of G-uv. Signatures do not affect the existence of the local face corner between consecutive edge ends.

Let A=N(u) minus {v} and B=N(v) minus {u}. They are disjoint because G is triangle-free. A square through uv is exactly an edge ab with a in A and b in B. At a vertex b of degree four, exactly one edge end is nonconsecutive to bv. Thus b can have at most one neighbor in A. The analogous statement holds for degree-four vertices in A. If the whole graph is quartic, the crossedges between A and B form a matching, so every edge lies in at most three squares.

More generally, if two vertices x,y have t common neighbors, choose one common neighbor a and delete xa. For each other common neighbor b, the cycle x-a-y-b-x shows that ya and yb must be nonconsecutive in the rotation at y. A degree-d vertex has exactly d-3 edge ends nonconsecutive to a fixed edge end. Hence

  t<=min(deg(x),deg(y))-2.

In particular, a quartic target is K_(2,3)-free. Combining the contraction lower bound with the matching upper bound, every edge of a quartic h=2 target lies in exactly two or three squares.

## 8. The degree-excess case at h=2 is impossible

Suppose m=2n+1. Every edge lies in at least four squares. Let v be a degree-four vertex and u any neighbor. If every vertex in N(v) minus {u} had degree four, each of those three vertices could be in at most one crossedge square through uv, by the preceding local rotation restriction. That would give at most three squares, a contradiction. Thus, for EVERY neighbor u of v, another neighbor of v has degree greater than four. Equivalently, every degree-four vertex has at least two high-degree neighbors.

If the degree excess is concentrated in one degree-six vertex, this is impossible. If the high-degree vertices are two degree-five vertices p,q, every degree-four vertex must be adjacent to both. There is at least one degree-four vertex, because a simple graph supported on only p,q could not realize degree five. Triangle-freeness now forbids p-q and forbids every edge between degree-four vertices (such an edge would form a triangle with p). A degree-four vertex would have only the two neighbors p,q, a contradiction.

Therefore:

  EVERY h=2 TARGET IS 4-REGULAR.

Its stronger necessary properties are: 3-connected, triangle-free, K_(2,3)-free, and every edge belongs to exactly two or three squares. The 3-connected restriction is justified by the published low-connectivity result, not by the counting alone: Mohar–Skoda Part I, arXiv:2002.00258, Theorem 5.11 proof (printed pp.13–14), explicitly rules out Euler genus above three for the connectivity-two cases; Corollary 6.5 identifies connectivity-two Klein-bottle obstructions with those Euler-genus-two obstructions. Our h=2 graph is a Klein-bottle obstruction of Euler genus four, so it cannot have connectivity two. Together with the block argument this gives connectivity at least three.

This restriction is specific to h=2. The original problem still allows every h>=2 and arbitrary connectivity.

### The all-two-square case is also excluded

Suppose a connected quartic triangle-free K_(2,3)-free graph has every edge in exactly two squares. Attach one disk along every square. Each edge is incident with two disks. At a vertex v, the link has four vertices, one for each incident edge. It is simple because two different squares using the same pair of incident edges would give three common neighbors to the opposite pair of vertices, contradicting K_(2,3)-freeness. Every link vertex has degree two because the corresponding graph edge lies in two squares. A simple 2-regular graph on four vertices is a 4-cycle. The resulting square complex is therefore a closed connected surface.

There are m/2=n square faces, so its Euler characteristic is n-2n+n=0. The surface is a torus or Klein bottle, giving E(G)<=2 and n(G)<=3. Hence it cannot be an h=2 target. Any surviving h=2 target must have at least one edge belonging to three squares.

### Optional size floor for h=2

From a vertex of a quartic triangle-free K_(2,3)-free graph, the 12 nonbacktracking two-step walks end at vertices outside its closed neighborhood, and each endpoint receives at most two such walks. Thus n>=11. If n=11, all six vertices outside each closed neighborhood are reached exactly twice, so every vertex lies on exactly six squares. Counting vertex-square incidences would give four times the number of squares equal to 6*11=66, impossible. Thus every h=2 target has at least 12 vertices.

## 9. Density obstruction to a tempting construction family

Suppose a nonplanar simple graph C of girth ell>=3 has positive even Euler genus r and attains the standard Euler/girth bound

  r=2-|V(C)|+(1-2/ell)|E(C)|.

Deleting an edge preserves the girth lower bound. The graph C-e cannot be a forest, since adding one edge to a forest produces a planar graph. Apply the facial-girth bound to its cyclic cores; tree components only decrease the right-hand side of the global lower bound. This gives

  E(C-e)>=ceil(r-(1-2/ell))=r.

Thus C is not Euler-critical and cannot supply class A or B. An orientably simple graph supplied by a tight triangular or quadrangular minimum embedding is not automatically useful. This is a conditional family exclusion, not a classification of orientably simple graphs.

## 10. A small exact near-miss: co-Heawood quadrangulations

As one concrete check within this investigation, construct the Fano plane from the nonzero vectors 1,...,7 of F_2^3, with lines {a,b,a xor b}. Form the point-line NONINCIDENCE graph: a point is adjacent to a line exactly when it does not lie on that line. The full labelled adjacency list, all 28 edges, and all 21 squares are retained in [the complete square certificate](COHEAWOOD_SQUARE_CERTIFICATE.json).

The checker verifies that this graph is quartic, triangle-free, K_(2,3)-free, and each edge lies in exactly three squares. An Euler-genus-two embedding would be quadrangular by density, with 14 square faces. A length-four facial walk in this graph must be a graph 4-cycle: a repeated vertex would force an immediate edge reversal at a degree-four vertex. A graph square cannot appear twice as a facial boundary, because occupying both of its sides would require degree two at its vertices. Thus the 14 faces would select 14 DISTINCT members of the list of 21 squares.

Because every graph edge belongs to exactly three squares, the seven omitted squares would contain each edge exactly once. The converse is also valid here: such an omitted-square partition leaves each edge in exactly two retained squares, and each quartic vertex link is K_4 minus a perfect matching, hence C_4, producing a closed quadrangular surface. For the negative result, only the forward implication is required.

The exact checker exhausts all seven-square edge partitions using deterministic edge-cover branching. At each node it chooses a remaining edge with the fewest eligible squares, where an eligible square uses only remaining edges. Any completion must choose one of these squares. A remaining edge with no eligible square is an exact dead-end. The saved certificate contains the entire 11-node search tree, not merely a solver exit code. All branches fail. Replay succeeds in normal Python, python -O, and python -OO; no Python assertions are used for verification.

Therefore this graph has no Euler-genus-two embedding, so E>=3. This DOES NOT establish E=4, n=4, any minor-minimality, or a solution to OPG-172. An N_3 embedding search was deferred at the end of this investigation and was not run here. The example is a precise future test of the narrowed square-selection frontier.

Certificate SHA256: 5791963edcc422d3a4eaa920e8db83b9a366e853ca93b0f536559a72ab0e32c4. The [certificate guide](CERTIFICATE_GUIDE.md) specifies a complete independent checking procedure.

## 11. Exact remaining work

No example or global nonexistence proof has been established. The precise remaining construction/proof obligations are:

1. Produce a triangle-free minimum-degree-four orientably simple Euler-critical graph of even Euler genus at least four, certifying every proper minor; OR
2. Produce an ordinary Euler hopper of Euler genus at least four (also triangle-free, minimum degree four), where doubling supplies a target; OR
3. Prove both classes empty in every genus.

The first direct genus h=2 has been narrowed to 3-connected, 4-regular, triangle-free, K_(2,3)-free graphs on at least 12 vertices, with every edge in two or three squares, at least one edge in three squares, and every edge deletion admitting a Klein-bottle embedding with one length-six face or two length-five faces. These necessary conditions are not claimed sufficient. Long-cycle Cartesian grids satisfy much of the combinatorial frontier but are already genus-two graphs. No finite size bound or unproved classification as cube covers is asserted.

The arbitrary-genus obstruction remains. Restricting a search to h=2 does not resolve OPG-172.

## Source identity and inspection scope

- Mohar–Skoda, *Cascades and Obstructions of Low Connectivity for Embedding Graphs into the Klein Bottle*, arXiv:1406.1341v1, https://arxiv.org/abs/1406.1341v1. PDF SHA256 7c33c7d1de424e9c8c0c03f2ccd06b174f58eeda343c6a77372a73875f5adf46, 767299 bytes. This investigation read Sections 2–6 relevant passages, especially Lemma2.1, Theorems2.2/6.2, definitions of hoppers, and Lemmas5.3–5.5. No whole-paper audit.
- Russell Campbell, *Finding Obstructions within Irreducible Triangulations*, PhD dissertation, University of Victoria, 2017. https://dspace.library.uvic.ca/bitstream/handle/1828/8212/Campbell_Russell_PhD_2017.pdf. PDF SHA256 a1e2c333ae79038eac1b4a6b23c9af4c6027f06bed7616ed9d3db8c267f8804a, 1531535 bytes, 134 PDF pages. Source title/abstract and Chapter5 definitions plus Lemma5.3/Theorem5.5 read; not a whole-thesis audit. Printed p.47 was rendered and visually inspected.
- The [source audit](SOURCE_AUDIT.md) records the 2024 journal publication identities of the 2020 successors and its bounded status check. No current-global-status claim is inferred from the historical sources.
