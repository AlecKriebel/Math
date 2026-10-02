# Turn 2: articulation reduction and cactus graphs

Status: a complete proof for a proper structural subclass, relying on the credited cycle theorem. The original arbitrary graph problem remains unresolved. Novelty is not certified.

## 1. Restriction at a one-vertex separation

Let V=V_1∪V_2, V_1∩V_2={v}, with both sides containing a vertex other than v, and suppose no arc joins V_1\{v} to V_2\{v} in either direction. Put a=|V_1|-1 and b=|V_2|-1, so there are a+b input colors. Each spanning out-arborescence restricts to a spanning out-arborescence on each V_j. This follows because the underlying tree's unique path between two vertices of V_j cannot leave through v and return through v. If the original root is outside V_j\{v}, the restriction's root is v; otherwise it is the original root.

Let c_j count colors whose root lies in V_j\{v}, and c_0 count those rooted at v. Thus c_0+c_1+c_2=a+b. At least one of

c_1≤b, or c_2≤a

holds. If both failed, c_1+c_2>a+b, a contradiction.

Suppose c_1≤b, exchanging indices if needed. There are at least a colors whose roots are outside V_1\{v}. Choose any a of them, call this color set I. Their restrictions to V_1 all have root v. A rainbow spanning arborescence B_1 on V_1 rooted at v can be constructed greedily: starting from v, use each selected color once and add a first arc exiting the current vertex set along that color's v-to-outside path. The a steps add all a other vertices.

There remain b colors. Restrict these to V_2. If this b-color instance has a rainbow spanning arborescence B_2 of any root, then B_1∪B_2 is a rainbow spanning arborescence on V. The underlying trees meet only at v. Every vertex except B_2's root has indegree one; in particular B_1 contributes no entering arc to v, whether or not v is B_2's root. Color sets are disjoint and together use all a+b colors.

**Articulation reduction.** A counterexample with a cut vertex yields a smaller counterexample on one side, with exactly the new vertex count minus one colors. The removed side is solved by a common-root construction; no prescribed root is imposed on the retained side. The choice of side is essential. Root counts must be recomputed after every restriction.

## 2. Structural consequences

A vertex-minimal counterexample to the full conjecture, if one exists, has no articulation vertex. Combined with Turn1, it has a strongly connected directed union and a two-vertex-connected underlying simple graph (small n=1,2 are immediate). Here the underlying simple graph ignores orientation and multiplicity; colored arcs themselves remain distinct.

More generally, let H be a connected simple scaffold containing all underlying edges. At every articulation of H, use the reduction above and recurse on the retained side. This terminates at one block of the original scaffold, perhaps with only a connected spanning subgraph of that block present. Thus it suffices that each original block support the conjecture for every colored instance whose underlying union is contained in that block. This formulation avoids assuming that deletion of colors preserves biconnectivity.

## 3. Cactus theorem

**Theorem.** Every instance of the original rainbow-arborescence problem whose underlying simple graph is a cactus has a rainbow spanning arborescence. A cactus is a connected graph in which each edge belongs to at most one simple cycle; its blocks are single edges or cycles. Arbitrarily many cycles and arbitrary root multiplicities are allowed.

Apply the scaffold reduction. A one-edge terminal block is immediate. If the terminal block is a cycle, the retained union is a connected spanning subgraph of that cycle. It is either the cycle itself or a path. The cycle case is exactly the credited Theorem4.9 of [Bérczi–Király–Yamaguchi–Yokoi, arXiv:2412.15457v2](https://arxiv.org/abs/2412.15457v2); the path case is their tree case, or follows by repeatedly removing a leaf. Lift the terminal witness through all recorded common-root pieces. This proves the claim for every finite cactus, not merely the tested sizes.

The imported cycle theorem is substantive. This packet does not claim a new proof of it. The primary paper states the cycle and pseudotree results; this deduction uses an articulation reduction to allow multiple cycle blocks. Targeted cactus/articulation searches located no prior statement, but that is not a novelty certificate.

The same reduction proves the conjecture when every block of the underlying graph has at most six vertices, by the credited all-instance n≤6 theorem. Replacing six by eight would rely additionally on the authors' reported exhaustive computation, which has not been reproduced here.

## 4. Constructivity and limits

The articulation step uses finite root counts, restrictions and greedy paths. For a cycle block, enumerate a possible root and a missing undirected edge, orient the remaining path away from that root, and test whether its arcs admit distinct available colors using bipartite matching. There are quadratically many candidates, and the credited existence theorem guarantees one succeeds. Consequently the cactus proof yields a polynomial-time construction, although the checker uses direct small-instance base searches in some controls rather than an optimized implementation.

A separator of two or more vertices does not have this proof: a restriction may be a forest with several entry points, and gluing can create a cycle or incompatible indegrees. No closure under two-vertex sums, series-parallel graphs, or general graphs is asserted.

## 5. Tests

`python verify_turn2.py` tests the exact reduction recursively, enumerates every four-color multiset of rooted spanning trees of a two-triangle cactus on five labeled vertices, and checks deterministic larger block-tree fixtures. Every returned arc must be an actual arc of its labeled color, each color occurs once, and global rooted connectivity/indegrees are checked independently. The algebraic side-choice inequality is also exhausted over bounded integer triples. These are finite controls, not a substitute for the unbounded proof or the imported cycle theorem.
