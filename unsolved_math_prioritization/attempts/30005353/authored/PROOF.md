# Cycle-filling costs: five partial approaches

Problem 30005353, Karim Adiprasito's Question 12 in *Combinatorics*, Oberwolfach Reports 20 (2023), 83–84. Authored 7 October 2026. **The unbounded-ratio question remains unresolved.** The results below are elementary partial results, not claims of mathematical novelty. They need independent review before publication.

## 0. Definitions and normalization

Let G be a finite connected simple unweighted graph of positive cycle rank r = |E|−|V|+1. A cycle means a simple unoriented graph cycle, with an orientation chosen only to define an attaching map. Let a₂(G) be the smallest sum of cycle lengths of a collection whose attached disks kill H₁(−;F₂), and let aπ(G) be the analogous minimum for π₁. The attached disks may outnumber r. All minima exist: a spanning-tree fundamental-cycle family works, and costs are positive integers. Trees have both costs zero and are excluded from ratios.

The source says homology vanishes, rather than explicitly H₁. Over a field, minimizing H₁-killing and minimizing reduced-acyclic fillings have the same value. Indeed, the boundary vectors of attaching disks must span the r-dimensional cycle space. Select a basis subfamily. It has no larger cost, kills H₁, and has injective ∂₂, hence H₂ = 0. No higher-dimensional cells exist. This observation is only used for a₂, not to identify integral generating sets with integral bases.

Allowing arbitrary closed edge walks does not change either minimum. Delete spurs. A closed walk with a repeated vertex splits at that vertex into two shorter closed walks. Recursion yields simple cycles of total length no greater than the original length. In homology the original class is the sum of the resulting classes. In π₁ the original based loop is a product of conjugates of these cycles: when splitting a loop based elsewhere, conjugate the subloop by the path from the base point to its splitting vertex. Consequently, the normal closure of the replacement cycles contains the original loop. Replacing every walk in an H₁-killing or π₁-killing family therefore still kills the corresponding invariant and does not increase cost. The reverse inequality follows because simple cycles are walks. A cellular circle map with collapsed edge intervals can first be tightened to an edge walk. Constant loops can be dropped. Repetitions and multiple traversals are charged with multiplicity before tightening.

Collapsing a spanning tree T identifies π₁(G) with a free group F_r, and H₁(G;F₂) with F₂^r. The a₂ condition is linear spanning of signed edge-cycle vectors reduced mod 2. The aπ condition is normal generation of F_r. No implication from linear independence to free generation or normal generation is assumed.

## Approach 1. Algebraic cycle bases and explicit torsion

### 1.1 The cycle-basis reduction and a sufficient equality criterion

The preceding linear-algebra argument proves that a₂ is exactly the minimum total length of an F₂ cycle-space basis. In particular, at least r cycles are necessary in any homology-killing or homotopy-killing family, so a₂ ≥ 3r and aπ ≥ a₂.

A cycle basis C₁,…,C_r is weakly fundamental if its order has an edge e_i in C_i that belongs to none of C₁,…,C_{i−1}. Attaching its disks gives a contractible space. To prove this, remove the last disk together with its edge e_r by an elementary collapse; e_r is a free face because it lies in no earlier disk. The graph G−e_r stays connected since e_r lay on C_r. Repeat in descending order. At stage i, none of the edges e_j removed at later indices belonged to C_i, so the indicated cycle and free edge remain. After r steps a connected rank-zero graph remains, hence a tree, which collapses to a point. Thus, whenever a minimum F₂ basis is weakly fundamental, aπ = a₂. This is a sufficient criterion, not a statement that all minimum bases have this property.

### 1.2 An explicit simplicial Moore complex

Fix an integer p ≥ 2. Put q = 3, introduce vertices a_i for i in Z/(3p), base vertices b_j for j in Z/3, and a vertex c. Define K_p by taking the following triangles and all their faces, for every i:

- {a_i,a_{i+1},b_{i+1 mod 3}}
- {a_i,b_{i mod 3},b_{i+1 mod 3}}
- {c,a_i,a_{i+1}}

All a's, b's, and c are distinct. Indices on a are modulo 3p. The first two rows triangulate the mapping cylinder of the simplicial degree-p covering from the a-circle to the b-circle: each strip is a quadrilateral split by the diagonal a_i b_{i+1}. The last row is a cone disk on the a-circle. Therefore K_p is the mapping cone of the degree-p circle map, with presentation ⟨x | x^p⟩. Its integral cellular homology in positive degrees is H₁ = Z/p and H₂ = 0; these conclusions can also be read from the one-cell-per-degree chain complex with ∂₂ multiplication by p.

Its face counts are (3p+4, 12p+3, 9p). Let X_p = sd K_p and G_p = X_p^(1). Vertices of sd K_p are nonempty faces of K_p, and simplices are inclusion chains. Thus X_p is flag: pairwise comparable faces form a chain. Every triangle in G_p is consequently a 2-simplex of X_p. Direct counting gives

v(G_p) = 24p+7,   e(G_p) = 78p+6,   f₂(X_p) = 54p,   r(G_p) = 54p.

The subdivided b-circle B has length six and represents the generator x of Z/p.

### 1.3 No essential cycle of length less than six in a barycentric subdivision

For any simplicial complex K, every edge loop of length at most five in sd K is nullhomotopic in |K|. Its vertices are faces of K. Whenever three consecutive distinct faces are monotonically nested, remove the middle face by the triangle homotopy in the order complex. Remove spurs as well. A nonconstant loop remaining after these moves alternates between local inclusion-minima and inclusion-maxima, and hence has even length 2t, with t ≤ 2. Choose a vertex of K in each inclusion-minimum face. The two minima neighboring a maximum both lie in that maximum simplex. The corresponding old subpath and the edge joining the two chosen vertices are homotopic inside that simplex, allowing a constant edge when the vertices coincide. This replaces the whole loop by a closed edge walk of K of length at most t. A loop of length at most two in a simplicial graph is constant or a backtrack, so is nullhomotopic. The deletion steps were homotopies, proving the assertion.

Applied to X_p, this proves that every G_p cycle nontrivial in π₁(X_p) has length at least six. B realizes six. The same is true for cycles nonzero in H₁(X_p;F_ℓ) whenever a prime ℓ divides p: their classes are nontrivial in π₁, and B has nonzero class.

### 1.4 Exact costs

For odd p, the triangle boundaries of X_p are linearly independent over F₂ and span all r graph cycles, because the multiplication-by-p cellular complex is F₂-acyclic. There are exactly r triangles. Therefore

**a₂(G_p) = 3r = 162p.**

Any aπ filling requires at least r cycles. At least one of them must have nontrivial image in π₁(X_p): otherwise the quotient map π₁(G_p) → π₁(X_p) = Z/p would factor through the allegedly trivial filled group. That cycle has length at least six, and all others have length at least three. Therefore aπ(G_p) ≥ 3(r−1)+6 = 3r+3.

For the matching upper bound, omit one small triangle from the subdivided cone disk, attach the other r−1 triangles, and attach one disk along B. A triangulated closed disk with the interior of one triangle removed, but all edges retained, is homotopy equivalent relative to its original boundary to that boundary. Here is a collapse proof, also covering an omitted triangle incident to the boundary. Root a spanning tree of the interior-edge dual graph at the omitted triangle. Remove each other triangle along the edge toward its already removed parent, in increasing distance from the root. That edge is free because its only two incident triangles were the triangle and its parent; no original boundary edge is removed. After all triangle-edge pairs are removed, a connected graph of rank one remains and contains the entire original boundary circle. Its other edges form trees attached to that circle, so prune them. All collapses fix the original boundary. Equivalently, the puncture releases its sole filling relation. Hence the remaining mapping-cylinder-plus-punctured-disk complex deformation retracts, up to homotopy relative to the base circle, to the mapping cylinder and then to the b-circle. Attaching B kills its sole generator and makes π₁ trivial. The cost is 3(r−1)+6. Thus

**aπ(G_p) = 162p+3,     aπ(G_p)/a₂(G_p) = 1 + 1/(54p), for odd p ≥ 3.**

The Python controls independently reduce the full triangle presentation to one generator with relator x^p, the omitted-triangle presentation to a free cyclic group, and that presentation plus B to the trivial presentation, for p=2,3,5,7,9. These are finite controls; the mapping-cylinder argument proves the family.

For p=2, K_p is a triangulation of RP². Its mod-2 triangle span has codimension one. Any F₂-killing family contains a cycle nonzero in H₁(X_p;F₂), hence one of length at least six. The same construction gives

**a₂(G₂) = aπ(G₂) = 327.**

**Outcome of Approach 1.** Normal generation can cost strictly more than a minimum F₂ cycle basis, with an explicit exact example (486 versus 489). Raising the torsion order in this family decreases the ratio toward one. This does not establish unbounded ratios.

## Approach 2. Amplification by sums and subdivisions

### 2.1 Exact additivity under bridge joining and one-point sums

Let graphs G₁,…,G_k be connected together by bridges arranged in a tree, or wedged at articulation vertices without forming new cycles. Every simple cycle belongs to one original block: it cannot cross a bridge, and crossing an articulation into another block would require revisiting the articulation to close. The graph's H₁ is the direct sum of the component H₁ groups. Its π₁ is their free product. For cycles lying in the separate factors, quotienting by their normal closures gives the free product of the factor quotients, which is trivial exactly when all factor quotients are trivial (each factor embeds, or retracts, in a free product). It follows, separately for τ=2 and τ=π, that

aτ(G) = Σ_i aτ(G_i).

Thus the combined ratio is a positive-denominator weighted average of the component ratios. Copies of a fixed example cannot amplify the ratio. In particular, bridge-joining k copies of G₃ gives a₂=486k and aπ=489k, so the additive gap 3k is unbounded but the ratio stays 163/162. Choosing two fixed vertices in each copy as bridge endpoints bounds the degrees uniformly in k. This supplies a valid connected bounded-degree additive-gap family.

### 2.2 Exact scaling under uniform edge subdivision

Replace every original edge by a path of L edges. A simple cycle in the subdivided graph traverses every such path it enters completely, since internal subdivision vertices have degree two; rotate its start if necessary. On suppressing those vertices, it becomes a simple original cycle. Conversely every original cycle lifts uniquely. The corresponding homeomorphism identifies both homology and π₁, and every length is multiplied by L. Hence aτ(S_L G)=L aτ(G) for τ=2,π. Uniform subdivision preserves the ratio exactly.

Consequently any iteration of these two operations starting from a family with uniformly bounded ratios still has uniformly bounded ratios. This rules out the two most direct amplification mechanisms, not general graph compositions.

### 2.3 Coefficient-sensitive projective-plane check

Let K be any finite simplicial triangulation of RP², let G=K^(1), let r=e−v+1, and let s be the length of the shortest graph cycle nonzero in H₁(RP²;F₂). Such a cycle exists because the 1-skeleton surjects on π₁. Euler characteristic gives f₂=r.

Any filling killing H₁(G;F₂) needs at least r cycles, and their images must span the nonzero H₁(RP²;F₂), so at least one has length ≥s. Thus a₂ ≥ 3(r−1)+s. Choose a shortest essential simple cycle C. Delete the interior of a triangular face. The remaining surface is a Möbius band. The curve C, lying in its 1-skeleton, is still embedded and has nonzero mod-2 class in RP². An embedded closed curve in a Möbius band with odd core winding represents a generator (the other essential embedded type is boundary-parallel with even winding). Therefore attaching one disk along C kills the fundamental group of the Möbius band. Filling the r−1 remaining triangular faces and then C proves aπ ≤ 3(r−1)+s. Together with a₂≤aπ,

**a₂(G) = aπ(G) = 3(r−1)+s.**

The embedded-curve fact can be seen by taking a regular neighborhood: a one-sided curve has a Möbius-band neighborhood; its complement in the ambient Möbius band is an annulus, whereas an essential two-sided curve is boundary-parallel and represents twice a generator. Contractible curves represent zero.

For an odd-characteristic field F, all r triangular boundaries instead form a homology basis, since RP² is F-acyclic, so a_F(G)=3r. Thus the projective-plane construction *can* separate aπ from a_F by s−3 when s>3. The primary report's p.84 display explicitly uses F₂. The preceding equality is an apparent coefficient-specific inconsistency with that display, pending independent review; it is not a criticism of the main open question or of the version with odd-characteristic coefficients.

**Outcome of Approach 2.** Additive separation is proved with a corrected odd-torsion example, while sums and uniform subdivisions are rigorously excluded as ratio amplifiers.

## Approach 3. Maximum-degree-three reduction

For each vertex v of G choose a finite tree T_v with maximum degree at most three and exactly deg_G(v) labeled leaf ports, one per incident edge. For degrees one or two use a singleton or a single edge; arbitrary larger degrees admit a binary tree. Internal vertices have degree at most three, while ports acquire at most one external edge. Let D be the maximum of the diameters of these finitely many trees. Replace every original edge uv by a fresh path of length L joining its corresponding ports in T_u and T_v, with pairwise disjoint new internal vertices. Call the resulting connected simple graph H_L. It has maximum degree at most three.

Collapse each T_v to a point and suppress the new subdivision vertices. This gives a homotopy equivalence q:|H_L|→|G|, because collapsing a finite forest is a homotopy equivalence of graphs and subdivision preserves the underlying topological graph. One may factor q into the forest collapse followed by the subdivision homeomorphism. It induces separate isomorphisms on π₁ and H₁.

### 3.1 Upper bounds, separately for the two invariants

Lift an original simple cycle C by traversing its length-L edge paths and the unique connecting tree path at each original vertex it visits. Since C visits no original vertex twice, the lift is simple: each vertex tree is used only once and external paths have disjoint interiors. Its length is between L|C| and (L+D)|C|. Its image under q is C.

If the original family spans H₁(G;F₂), the lifted classes span H₁(H_L;F₂) by q_*. If the original family normally generates π₁(G), the lifted conjugacy classes normally generate π₁(H_L), again by the isomorphism q_*; no homological argument is used for this implication. Therefore

a₂(H_L) ≤ (L+D)a₂(G),       aπ(H_L) ≤ (L+D)aπ(G).

### 3.2 Lower bounds and projected closed walks

Consider any simple cycle Z in H_L. It cannot lie entirely in the union of the vertex trees. If it contains an edge of a new length-L external path, it traverses that entire path, because each internal vertex has degree two; if the starting point lies there, rotate the cycle's parametrization first. Thus Z traverses k whole external paths for some k≥1. After collapsing trees its image is a closed edge walk W in G of length k, possibly with repeated original vertices. Its projected length obeys kL≤|Z|. If an original edge appears more than once after an arbitrary walk normalization, all appearances are counted; for a simple Z, no external path is used twice.

Decompose W into simple cycles by the normalization in §0. The total original length of the pieces is at most k≤|Z|/L. Perform this replacement for every cycle in a killing family in H_L.

For H₁: q_* takes the original span onto H₁(G;F₂). Each projected class is a sum of replacement classes. The replacement family therefore spans H₁(G;F₂). Its cost is at most the H_L family's cost divided by L.

For π₁: q_* takes the normal closure of the original relators onto π₁(G). Each projected relator is a product of conjugates of its replacement simple cycles. Hence the normal closure of all replacement cycles contains the normal closure of all projected relators, which is all π₁(G). They are a legitimate normal-generating family of the stated cost. Conjugating paths are used only to justify normal containment; they are not charged as extra attaching-cycle lengths.

Taking minima proves

**L aτ(G) ≤ aτ(H_L) ≤ (L+D)aτ(G), for τ=2,π.**

Because r(G)>0, its denominator is positive. The same is true for H_L by homotopy equivalence. Thus

L/(L+D) · aπ(G)/a₂(G) ≤ aπ(H_L)/a₂(H_L) ≤ (L+D)/L · aπ(G)/a₂(G).

In particular the ratio converges to the original ratio as L→∞. The supremum of ratios over finite connected simple graphs with a cycle equals the supremum over such graphs of maximum degree three, even as an extended real number. Therefore the two unboundedness questions are equivalent. No bound on the number of new vertices relative to the original graph is asserted. If multigraphs or loop edges are allowed in the original question, uniformly subdividing sufficiently first makes a simple graph and preserves both costs by the same cycle/walk argument.

**Outcome of Approach 3.** The bounded-degree clause introduces no additional obstruction when graph size and edge subdivision are unrestricted. This reduces, but does not settle, the main question.

## Approach 4. Field-dependent systoles and homology growth

Let X be a finite connected two-dimensional simplicial complex with graph G, cycle rank r>0, and H₁(X;F₂)=0. Its triangular boundaries span H₁(G;F₂), so selecting a basis of them proves a₂(G)=3r. Let ℓ be a prime for which d=dim H₁(X;F_ℓ)>0. Let s be the minimum length of a simple graph cycle having nonzero class in that group. This minimum exists: cycles of the graph generate H₁ of the complex.

Any π₁-killing family in G projects to a spanning family in H₁(X;F_ℓ). It therefore includes at least d cycles with nonzero images, each costing at least s. It contains at least r cycles in total, by its F₂ span. Since s≥3, its total cost is at least

**aπ(G) ≥ 3r + d(s−3),     aπ(G)/a₂(G) ≥ 1 + d(s−3)/(3r).**

This lower bound controls *every alternative family of relators*, not merely a chosen presentation. It yields a sufficient condition for a positive answer: complexes X_n with H₁(X_n;F₂)=0 and d_n(s_n−3)/r_n→∞. By Approach 3 their vertex degrees need not be bounded at the initial construction stage.

The Moore complexes above realize d=1, s=6 and r=54p, so this criterion is exact but the resulting ratio tends to one. Bridge sums of k copies have d=k, s=6 and r=54pk, hence cannot improve it. Uniform subdivision preserves the actual ratio by Approach 2; it cannot be mistaken for a way of raising s while keeping a₂=3r, since the subdivided relators are no longer triangles.

A concrete covering-space version would suffice. Suppose a fixed finite triangular complex admits finite connected covers X_n with (i) zero mod-2 H₁, (ii) dim H₁(X_n;F_ℓ) bounded below by a positive constant times the number of sheets, and (iii) mod-ℓ homological systole tending to infinity. The graph cycle ranks grow linearly in the sheets (r_n = N_n(r_0−1)+1), so the criterion applies. None of these three simultaneous properties is established here for a proposed tower. Large girth of a graph alone is insufficient: then a₂ itself costs at least r times the graph girth. A large fundamental group with trivial mod-2 abelianization also supplies neither a lower bound on the number of required long relators nor this homological growth condition.

More generally, a finite quotient Q of π₁(X) supplies the lower bound ν(Q)s_Q on aπ(G), where ν(Q) is the least size of a normal-generating set of Q and s_Q is the least graph-cycle length with nontrivial image in Q. The projected relators must normally generate Q, so at least ν(Q) of them are nontrivial and each costs at least s_Q. Large group order alone does not lower-bound ν(Q): for example a nonabelian simple quotient has ν=1. This blocks the naive strategy of using increasingly large perfect simple quotients without a metric-generation estimate.

**Outcome of Approach 4.** A rigorous sufficient construction criterion and a quotient lower-bound mechanism are obtained. The missing object is a family with quantitatively many independent long obstructions and cheap mod-2 filling. No such family is provided.

## Approach 5. Universal upper bounds through controlled cycle deletion

Write W(G) for the number of edges belonging to at least one cycle, excluding bridges. Every F₂ cycle-space basis covers every such edge. Indeed, if an edge e is in a cycle but absent from all basis elements, the e coordinate of every linear combination would be zero, a contradiction. Thus W(G)≤a₂(G).

A crude bound is aπ(G)≤rW(G). Delete bridges and handle the remaining connected components separately. A spanning-tree fundamental cycle in any component uses at most its cyclic-edge count. The union of these fundamental families normally generates the free product of the component groups. Summing r_i W_i ≤ r ΣW_i gives the claim. In particular bounded cycle rank cannot yield an unbounded ratio.

Here is an elementary logarithmic improvement. For r≥2 put

k(r) = 2 ceil(log₂(2r)) + 1.

**Claim. aπ(G) ≤ k(r) W(G), and consequently aπ(G)/a₂(G) ≤ k(r).**

We construct a weakly fundamental family. At each step discard bridges and isolated vertices from the current graph, and suppress maximal degree-two paths, assigning to each resulting edge the number of original edges in its represented path. The represented paths have disjoint interiors and pairwise disjoint edge sets. A connected component consisting solely of a cycle is handled by recording that entire cycle and retiring all its edges; its cost equals its retired weight.

Any other component after suppression is a weighted multigraph J of minimum degree at least three, allowing loops and parallel edges. Its cycle rank r' is at most r. If it has N vertices, the degree sum gives e≥3N/2, hence N≤2r'−2≤2r−2. Loops or parallel edges already give a combinatorial cycle of length at most two. Otherwise a standard breadth-first count gives a cycle of length at most 2 ceil(log₂(2r))+1: if every cycle were longer than 2t+1, the ball of radius t about a vertex would be a tree with at least 1+3(2^t−1) vertices; taking t=ceil(log₂(2r)) exceeds N. Edges within the ball or coincident search branches would produce a cycle of length at most 2t+1, which justifies the tree count.

Choose such a combinatorially short cycle C in J, and an edge e of maximum weight on C. Then weight(C)≤k(r)weight(e). Lift C to a simple cycle in the original current graph, record it, and retire the path P represented by e. Topologically, one may first delete a single edge of P after attaching the recorded disk: the disk and that edge are an elementary collapse pair. The remaining pieces of P are hanging paths with no other attachments at their internal vertices, so can be pruned. Deleting the first edge reduces cycle rank by exactly one; the pruning and suppression change no cycle rank. Then repeat.

Every recorded cycle contains a retired edge absent from all subsequently recorded cycles. In reverse order the recorded cycles are weakly fundamental. The process records exactly r cycles and leaves a forest, so §1.1 shows that they normally generate. All charged retired paths are edge-disjoint subsets of the original cyclic edges; extra pruned edges are not charged. The total cost is therefore at most k(r)W(G). The special pure-cycle steps obey the same bound since k(r)≥1. For r=1, the graph has a unique cycle and both costs equal its length.

This is a reconstruction of the standard Rizzi (2007) deletion argument, explicitly presented as Theorem 4.4 in the 2009 survey by Kavitha et al., with the cycle-rank and cyclic-edge bookkeeping made explicit. The survey credits its proof to T. Kavitha and R. Rizzi. Neither the deletion mechanism nor its logarithmic order is claimed as new. The explicit constant above is included for clarity. It leaves room for unbounded ratios growing logarithmically or more slowly.

For planar graphs an elementary stronger bound aπ≤2W≤2a₂ follows by filling the bounded facial boundary walks in a plane embedding, componentwise after deleting bridges. The resulting complex is simply connected: each bounded complementary disk has been filled, and any loop contracts in the resulting filled planar set, or equivalently use a dual spanning-tree elimination. The sum of all face-boundary lengths is 2W, so the bounded faces cost at most this; decompose boundary walks into simple cycles using §0 if necessary. In fact the established planar minimum-basis theorem gives the sharper equality aπ=a₂: Theorem 5.34 of the cited survey supplies a minimum rational cycle basis that is weakly fundamental. Every F₂ basis, with its cycles oriented, is rationally independent because its cycle-coordinate determinant is odd and hence nonzero. Thus the rational minimum is no larger than the F₂ minimum. The supplied weakly fundamental basis is itself an F₂ basis, yielding the reverse inequality. Apply §1.1. This sharper planar conclusion is credited existing work, not a new result. Thus a planar construction cannot prove unboundedness.

**Outcome of Approach 5.** The search is restricted to growing cycle rank and genuinely nonplanar families. A universal logarithmic upper bound is proved, but no universal constant and no matching unbounded lower bound are established.

## Remaining mathematical gap

There is no sequence G_n in this packet for which aπ(G_n)/a₂(G_n)→∞, and no absolute constant C proved to bound that ratio for all graphs. The odd-torsion examples have exact ratio 1+1/(54p); their replication produces only additive gaps. The subcubic reduction transfers any future construction but does not create one. The field-systole route isolates one sufficient missing family. The upper bounds do not decide boundedness.

No argument identifies an arbitrary F₂ basis with a free basis, normal basis, integral basis, or contractible filling. No undecidable group-triviality algorithm is asserted. The elementary Tietze reductions in the checker certify only the concrete small presentations on which they terminate.
