# Independent mathematical audit: consecutive nonorientable obstructions

## Status and scope

**ACCEPTED as a partial-result report.** The complete reviewed structural proof is reproduced in [the structural report](STRUCTURAL_REPORT.md). Its final change removes an unsupported named-cube example; the proved general density exclusion remains. No graph witnessing the original existence question and no proof of universal nonexistence has been obtained. The retained conclusions are conditional equivalences and necessary conditions. Finite checks below are regression evidence, not a search establishing existence or nonexistence.

The target is a finite ordinary graph G and an integer h≥1 such that G does not embed in N_(h+1), while every proper minor embeds in N_h. Both deletion and contraction are required. Isolated-vertex deletion is included. No connectedness assumption is imposed on the original target.

## 1. Corrections required or incorporated during review

1. Use ν(G)=min{j≥1:G embeds in N_j}. In particular every planar graph, including every forest, has ν=1. With E the Euler genus, σ=ν−E belongs to {0,1}, and σ=1 requires E even. Substituting a cellular tree convention ν(tree)=0 into a general block formula is invalid: attaching a leaf to K7 cannot lower ν from3 to2.
2. Require positive Euler genus in the definition of an ordinary Euler hopper. Otherwise the empty graph satisfies an all-proper-minor condition vacuously. For the σ=0 target criterion explicitly require r=E(G)≥3, so h=r−2≥1.
3. Euler-critical and hopper conditions must quantify over all proper minors, or explicitly remove isolated vertices before using edge operations. Adding an isolated vertex preserves edge-criticality but destroys minor-minimality.
4. The forest-free hypothesis needed for the girth bound must be supplied. The bare formula E≥2−n+(1−2/ℓ)m is false for some forests. In its intended application C is nonplanar, so C−e cannot be a forest: adding one edge to a forest is planar. An equivalent safe route in target applications uses δ(G−e)≥3.
5. Euler genus2 does not imply embeddability in the Klein bottle. Any low-genus argument relying on that inference is rejected. The direct minimum-degree/density proof below excludes h=1 without enumerating the35 projective-plane obstructions.
6. “Critical for Euler genus2” means minimal above the threshold2; it does not by itself mean that the graph has Euler genus3. For the connectivity-two exclusion, the required extra fact is explicitly proved in Mohar–Škoda's Theorem5.11, rather than following merely from their668 count or Corollary6.5.

## 2. Genus dichotomy and amplification

Every target has at least one edge. A missing edge can be restored using one added handle, so ν(G)≤ν(G−e)+2. Together with the target inequalities this gives

- ν(G)=h+2;
- ν(G−e)=h for every edge e;
- ν(G/e)≤h, without claiming that every contraction has the same drop.

The same argument shows that two distinct nonorientable surfaces sharing a minor obstruction must have consecutive indices. This is a normalization of the question, not a solution.

### Orientably simple case

Suppose r=E(G)>0 and σ(G)=1. Then r is even. G is a target exactly when every proper minor M has E(M)≤r−1. For the converse, E(M)=r−1 is odd and hence σ(M)=0; if E(M)≤r−2, ν(M)≤E(M)+1≤r−1. Thus h=r−1 works. The implication genuinely uses parity; the generic estimate ν(M)≤E(M)+1 alone would be insufficient at the top level.

### Non-orientably-simple case

For r=E(G)=ν(G)≥3, G is a target exactly when every proper minor has E(M)≤r−2 and no proper minor satisfies E(M)=r−2, σ(M)=1. The latter exception is automatically absent when r is odd.

### Double-copy construction

Let H be a positive-Euler-genus ordinary hopper, meaning E(M)≤E(H)−2 for all proper minors. If σ(H)=1, the preceding orientably simple case applies. If σ(H)=0 and r=E(H), let D be two disjoint copies of H. Euler additivity and the Stahl–Beineke correction give ν(D)=2r. After an elementary operation in one copy, the untouched copy still has σ=0, so

ν(H' ⊔ H)=E(H')+r≤2r−2.

The equality also holds when H' is planar: place it in a complementary disk and use Euler additivity for the lower bound. The all-proper-minor condition excludes isolated surplus vertices and genus-zero redundant pieces; consequently the elementary checks cover every proper minor. Thus D is a target with h=2r−2. When H is connected the same proof works for a1-sum.

Accordingly the target exists if and only if there is either a positive orientably simple Euler-critical graph or a positive ordinary Euler hopper. No such graph is supplied here.

### Block reduction

Each positive-genus block inherits the corresponding Euler-critical or hopper condition. To see this rigorously, first apply an elementary edge operation within the block. External block-cut-tree pieces remain attached by1-sums, so Euler additivity makes the change in the whole graph equal to the change in that block. A positive-genus block has no isolated vertices, so these elementary operations suffice for its all-proper-minor property. A graph in the orientably simple class has all positive-genus blocks orientably simple by the block formula. Genus-zero blocks and isolated components are incompatible with criticality. This establishes the existence reduction to2-connected building blocks, without claiming that every target itself is2-connected.

## 3. Local augmentation and the minimum-degree improvement

Campbell's Lemma5.3 gives the one-extra-crosscap embedding for an obstruction containing a triangle. The proof supports the following more general local statement:

**If uv is absent from X and u,w,v is a two-edge path in X, then ν(X+uv)≤E(X)+1.**

For a connected component containing that path, take a cellular Euler-minimum embedding. If u and v have a common face, insert uv there; add a crosscap in a complementary disk if necessary. Otherwise normalize the signatures on wu,wv to be positive and write the local order at w as (wu,X,wv,Y). Reverse the intervening block X and change the signatures on those incident edges. The two boundary faces at the block's ends merge, all other facial boundary walks are preserved, and the Euler genus increases by one. Insert uv in the merged face with negative signature. The triangle uvw is then one-sided, explicitly certifying nonorientability. This is a local surface operation, not a use of the connected Euler formula on a disconnected drawing.

For disconnected graphs, perform that construction on the path's component and combine minimum-Euler-genus embeddings of the remaining components by connected sums through complementary disks. The changed component is nonorientable, and the Euler genera add. This proves the stated bound with the total E(X).

It follows immediately that a target and an ordinary Euler hopper are triangle-free.

### Cubic reconstruction

Suppose a triangle-free target has a cubic vertex u with neighbors v,a,b. Contract uv to H. Triangle-freeness ensures that va and vb in H arise uniquely from ua and ub; no needed edge was merged with an original edge at v. Subdivide va by a new vertex named u, obtaining J. Add ub. It lies in the triangle u-v-b of J+ub, so

ν(J+ub)≤E(J)+1=E(H)+1≤h+1.

Deleting vb restores exactly the original G, contradiction. Thus every target has δ≥4. The same construction gives E(G)≤E(G/uv)+1, excluding cubic vertices from an ordinary Euler hopper as well. Positive orientably simple Euler-critical graphs are targets by the dichotomy, so they too have δ≥4.

No edge contraction was substituted for a deletion-only condition. The proof specifically requires the hypothesis on G/uv.

## 4. Density and low-genus consequences

For a triangle-free target, write n=|V|, m=|E|. Minimum degree4 gives m≥2n. Every G−e has minimum degree at least3 and embeds in N_h. Use cellular Euler-minimum embeddings of its c components; its total Euler genus is at most h and every facial walk has length at least4. Therefore

m−1≤2n−4c+2h≤2n−4+2h.

Hence h≥2c, in particular h≥2. This is an independent proof that no h=1 target exists.

An ordinary hopper cannot have E=2 by Kuratowski: a Kuratowski minor is then a proper minor of positive Euler genus. If a hopper had E=3, parity gives σ=0, so the exact criterion would make it an h=1 target, now excluded. The two auxiliary construction classes consequently require Euler genus at least4.

The conditional tight-girth family exclusion also survives review after its forest qualification: if a simple graph C with finite girth ℓ has positive even Euler genus r equal to 2−n+(1−2/ℓ)m, then C−e still has a cyclic component, and its global girth bound implies E(C−e)≥ceil(r−(1−2/ℓ))=r. Such a graph is not Euler-critical. This is a conditional density exclusion, not a classification of orientably simple graphs.

## 5. Necessary conditions for an h=2 target

Here ν(G)=E(G)=4: σ=1 would force the odd Euler genus3, which is impossible. G is therefore an ordinary Euler hopper satisfying the exceptional-minor restriction. The preceding inequalities imply connectedness and

m∈{2n,2n+1}.

Its degree sequence is consequently either4-regular, or all4 except for one6-vertex, or all4 except for two5-vertices.

### Triangles after contraction

Since G is triangle-free, contraction of e yields n'=n−1, m'=m−1 with no parallel suppression, and minimum degree at least4. Its total Euler genus is at most2. If it has c components and F faces in componentwise cellular Euler-minimum embeddings, then F=m'−n'+2c−E'. With f3 triangular faces,

f3≥4F−2m'=2m'−4n'+8c−4E'≥2m'−4n'.

A triangle cannot bound two faces here: that would require degree2 at each of its vertices. Every triangle of G/e contains the contracted vertex and corresponds uniquely to a4-cycle through e in G. Therefore each edge lies on at least2 four-cycles when m=2n, and at least4 when m=2n+1.

### Rotation/corner restriction and quartic case

Fix an embedding of G−uv in N_h. For a4-cycle u-a-b-v-u, the edges ba,bv cannot be consecutive at b: otherwise insert the auxiliary edge av in that corner, restore uv using the triangle augmentation bound, and obtain G in N_(h+1). Similarly au,ab cannot be consecutive at a.

When all degrees are4, an edge has a unique opposite edge in each cyclic rotation. Thus the edges from N(u)\{v} to N(v)\{u} form a matching, with at most3 edges. In the4-regular h=2 case, every edge lies in exactly2 or3 four-cycles and those cycles have disjoint internal vertices.

More generally, if x,y have t common neighbors and a is one of them, delete xa. At y, the t−1 edges to the other common neighbors must all be nonconsecutive to ya, leaving at most d(y)−3 positions. Thus t≤min(d(x),d(y))−2. In particular a target cannot contain K_(2,3) with either degree4 vertex in its size-two part. These are necessary local restrictions only.

### Eliminating the degree-excess case

Suppose m=2n+1. Every edge then lies in at least4 four-cycles. For any edge uv with d(v)=4, if all three vertices in N(v)\{u} have degree4, the corner restriction permits at most one corresponding crossedge at each of those three vertices. This gives at most3 four-cycles, contradiction. Thus for each neighbor u, a quartic vertex v must have a high-degree neighbor other than u. Every quartic vertex consequently has at least two high-degree neighbors.

The total degree excess is2. If there is only one6-vertex, this is impossible. If there are two5-vertices p,q, every quartic vertex must neighbor both. There is a quartic vertex because a simple graph on only one or two vertices cannot support those high degrees. Triangle-freeness forbids every edge between quartic vertices and forbids pq. A quartic vertex would have only p and q as neighbors, again impossible. Hence m=2n, and every h=2 target is4-regular.

Its square-link at a vertex is the simple graph on the four incident edges, joining a pair when they occur together in a4-cycle. K_(2,3)-freeness makes this definition unambiguous. Each link vertex has degree2 or3, so the link is C4, K4 minus one edge, or K4. This local classification does not establish a compatible global choice of quadrangular faces, and no global quadrangulation conclusion is accepted.

### Connectivity-two source dependency

Euler additivity and the genus≥4 lower bound on every positive block show that an h=2 target has just one positive block, hence is2-connected. To upgrade to3-connected, one needs a credited classification input: Mohar–Škoda, *Excluded minors for the Klein bottle I*, preprint arXiv:2002.00258v1, Theorem5.11 and its proof on printed pp.13–14, explicitly show that every connectivity-two graph critical above Euler genus2 has Euler genus3. An h=2 target would instead be such a graph of Euler genus4. The668 count alone is not the input. This classification was read and its exact claimed genus inspected; its computer-assisted dependencies were not independently reconstructed in this audit.

### The all-two-square case and size floor

If every edge is in exactly two squares, attach one disk along each square. Each edge meets two disks, and the simple square-link at each quartic vertex is a2-regular graph on four vertices, hence a circle. This is a closed connected surface with n vertices,2n edges and n faces, so its Euler characteristic is zero. It is a torus or Klein bottle. Consequently E≤2 and ν≤3, excluding an h=2 target. Therefore a target at h=2 must have an edge in three squares. This argument applies to the all-two-square case only; a compatible face selection in the mixed two/three-square case is still missing.

At any quartic vertex there are12 nonbacktracking two-step walks, ending outside its closed neighborhood with multiplicity at most2 by K_(2,3)-freeness. Thus n≥11. At n=11 all six possible endpoints have multiplicity2, so every vertex lies on six squares. Counting incidences would give4 times the number of squares equal to66, impossible. Hence n≥12.

### Edge-deleted face profiles

For the surviving quartic h=2 case, G−e has2n−1 edges and minimum degree3. Its density excludes Euler genus0 or1, while the target hypothesis supplies an N2 embedding. Since its nonorientable and Euler genera are both2, a cellular Klein-bottle minimum embedding exists. It has n−1 faces, and the total excess of face lengths over4 is2. Thus precisely one length-six facial walk or two length-five facial walks occur; all other faces have length4. A bipartite graph permits only the length-six alternative. These are boundary-walk lengths, without an unwarranted assertion that each long face boundary is a simple cycle.

### Independently verified co-Heawood near-miss

The final report constructs the14-vertex Fano point-line nonincidence graph, with28 edges and21 squares. Independent reconstruction confirms degree4, triangle-freeness, K_(2,3)-freeness and exactly three squares through each edge. An Euler-genus-two embedding would be quadrangular by density, with14 distinct square faces. Facial squares are distinct because two faces with the same cycle would force degree2 along that cycle. The seven omitted squares would partition all28 edges. Conversely such a partition would leave two squares per edge and C4 vertex links, although only the forward direction is needed for the negative certificate.

An independent verifier generated squares from point pairs and common nonincident lines, enumerated all116280 seven-square subsets, and found zero edge partitions. It also validated each state and every eligible branch in the saved11-node search tree, checking that no node or branch was omitted. Normal, -O and -OO outputs agree. The accepted certificate SHA256 is5791963edcc422d3a4eaa920e8db83b9a366e853ca93b0f536559a72ab0e32c4.

This establishes E≥3 for that graph. It does not prove E=4, ν=4, any proper-minor embeddability, or an OPG target. No N3 embedding search was performed as part of this certificate audit.

## 6. Actual finite verification

The independently run dependency-free finite verification uses explicit exceptions rather than assertions. Normal, -O and -OO executions completed successfully with byte-identical output.

- Algebraic genus tests through r=60:1425 σ=1 criterion cases,2788 σ=0 criterion cases,2611 double-copy cases.
- Named convention regressions: K5⊔K5 has ν=2; K5⊔K7 has ν=3; K7⊔K7 has ν=5; attaching a tree or planar cycle to K7 leaves ν=3. The intentionally invalid tree-σ=0 formula predicts2 and is explicitly rejected.
- All6229 labeled triangle-free graphs on at most6 vertices were generated locally. Their16872 ordered cubic-vertex/incident-edge reconstructions restore the exact original edge set. The31321 edge-contraction triangle sets agree exactly with their corresponding four-cycle sets. K4 is a negative control demonstrating that the reconstruction can fail without triangle-freeness.
- Signed-rotation tests cover16 embeddings of K4−e,27648 embeddings of K5−e, and1536 embeddings of the cubic-reconstruction intermediate obtained from K3,3. Spanning-tree signature normalization covers all signature classes. In the K5−e and K3,3-intermediate tests, respectively128 and32 embeddings need the partial vertex-block reversal. Each produces the required nonorientable one-higher-genus embedding with the inserted edge's negative signature. The remaining cases admit direct insertion with no genus increase.

The signed-dart face permutation is implemented independently of the structural report; every face has two directed boundary orbits. Gauge switching is checked to preserve genus and orientability. An additional independently replayed K4,4 certificate has8 vertices,16 edges,8 faces and unbalanced cycle signatures, proving a nonorientable Euler-genus2 embedding. Its graph and rotations are validated before evaluating the face permutation. This is a rejected candidate, not a target witness.

These checks stress the local surgery and exact reconstruction. They do not enumerate hoppers, prove the universal local theorem by computation, or independently verify the cited obstruction classifications.

## 7. Primary sources and inspection boundary

- Mohar–Škoda, *Cascades and Obstructions of Low Connectivity for Embedding Graphs into the Klein Bottle*, arXiv:1406.1341v1, https://arxiv.org/abs/1406.1341v1 . Definitions, block formula, low-genus statements and their surrounding context inspected. Full PDF SHA2567c33c7d1de424e9c8c0c03f2ccd06b174f58eeda343c6a77372a73875f5adf46;767299 bytes.
- Mohar–Škoda, *Excluded minors for the Klein bottle I. Low connectivity case*, https://arxiv.org/abs/2002.00258v1 ; published JCTB164(2024),299–320, https://doi.org/10.1016/j.jctb.2023.10.002 . Exact Theorem5.11 proof and Theorem6.2 formula inspected. This audit does not claim to have rerun the computer classifications.
- Campbell, *Finding obstructions within irreducible triangulations*, University of Victoria,2017, https://dspace.library.uvic.ca/items/cca9ac7d-a34e-4991-99ba-0b0d458e2e62 . Lemma5.3 on printed pp.47–48 and its local proof inspected. The stronger arbitrary-graph formulation and cubic consequence above are deductions, without a novelty claim. PDF SHA256a1e2c333ae79038eac1b4a6b23c9af4c6027f06bed7616ed9d3db8c267f8804a;1531535 bytes.
- Parsons–Pica–Pisanski–Ventre, *Orientably simple graphs*, Mathematica Slovaca37(1987),391–394, https://dml.cz/handle/10338.dmlcz/129376 . The positive-crosscap convention, including planar graphs and trees, and the cellular distinction inspected.
- Stahl–Beineke, *Blocks and the nonorientable genus of graphs*, J.Graph Theory1(1977),75–78, https://doi.org/10.1002/jgt.3190010114 . The formula is used through the explicit Mohar–Škoda restatement. The original1977 proof was not independently read in full.

No current global open-status certificate or novelty claim is made. The retained mathematical question remains unresolved by this investigation. The h=2 frontier is3-connected,4-regular, triangle-free, K_(2,3)-free, order at least12, with every edge in two or three squares and at least one in three; these conditions are not claimed sufficient.
