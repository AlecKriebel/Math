# Independent derivations — row 101 / Zenodo 23331258

These arguments were formulated from the actual four-page manuscript and complete controlling TeX before foreign primary bodies or current/historical review opinions. EARLY_LEDGER.md and EARLY_SEAL.json freeze that reconstruction. The details here expand it; they do not inherit the deposited historical audits.

## 1. The exact decision predicate

For finite simple undirected G, unit traversal lengths, distinct initially pairwise-connected r,s,t, a set F is feasible precisely when every original geodesic for each of the three unordered terminal pairs meets F. Indeed every surviving path is an original path and has length at least the old distance d. If all paths of length d disappear, any surviving shortest path has integral length at least d+1; if none survives, infinity satisfies the convention. Conversely a surviving old geodesic violates the inequality. This uses unit lengths and allowed disconnection, both explicit in the note. Deletion prices are unrelated to traversal lengths.

## 2. Two-subdivision for every cover

Replace each Q-edge uv by u-b-c-v using private b,c. All old vertices form A, all b form B and all c form C. Thus every edge joins distinct parts, and every gadget supplies AB,BC,CA edges.

Let S cover Q. If only u belongs to S, add c; if only v belongs, add b; if both, add either. These choices cover the three gadget edges and use exactly m additional vertices, so tau(H) <= tau(Q)+m.

For an arbitrary cover X of H put S=X intersect V(Q). The private middle edge bc requires at least one new vertex. Every original edge with neither endpoint in S requires both b and c, from the two outer gadget edges. If q counts these edges, disjointness of the private gadget vertices gives |X| >= |S|+m+q. Adding one endpoint for each uncovered original edge produces a Q-cover of size at most |S|+q <= |X|-m; repeats only reduce the size. Hence tau(H)=tau(Q)+m for arbitrary finite Q, including isolates and m=0. No assumption of minimum X or a consistently oriented Q is used.

## 3. Complete geodesic classification and arbitrary deletions

Add new terminals r,s,t, joining respectively all of A,B,C. The terminal neighborhoods are disjoint and there are no terminal-terminal edges, so distances are at least three. At least one cross-part edge of each type supplies a three-edge terminal path for each pair. For terminals a,b attached to parts U,V, every length-three terminal path has precisely the form a-u-v-b with u in U, v in V and uv an H-edge. Its two interior vertices cannot be another terminal: the first and last edges are spokes to H-vertices. This characterizes ALL shortest paths, not merely a selected family.

For an H-cover X delete the corresponding spokes e_w. Every such path contains a spoke indexed by an endpoint of its middle H-edge, so this is a blocker of size |X|.

For ANY blocker F, including ones deleting H-edges, choose w for each deleted spoke e_w and choose one arbitrary endpoint of each deleted H-edge. Let X be the resulting vertex set. Each deleted edge makes at most one contribution, so |X| <= |F|. For each H-edge uv its terminal geodesic e_u,uv,e_v must meet F. Whichever of those edges is deleted contributes u or v, independently of the arbitrary choices for other edges. Thus X covers EVERY H-edge. This proves tau(H) <= |F| and therefore opt(G_H)=tau(H). It does not assert that all minimum blockers contain only spokes.

## 4. All input sizes and binary encoding

For a Vertex Cover instance (Q,k), k>=0, m>=1, the chain is

tau(Q)<=k iff tau(H)<=m+k iff opt(G_H)<=m+k.

There are n+2m+3 vertices and 3m+(n+2m)=n+5m edges. Endpoint labels and the addition B=m+k have polynomial bit length. The graph has no dependence on the numerical magnitude of k. An isolated old vertex creates a degree-one spoke vertex and no new middle edge; it does not affect the reverse extraction. With m=1 all three cross-part types are already present. For m=0, k>=0 makes the source a YES-instance; a triangle H with one spoke per vertex and budget two is a fixed restricted YES-instance. Thus no missing nonnegative-budget source case remains. Invalid encodings or negative budgets are outside the stated source decision language and may be rejected before the reduction.

An edge-list certificate has polynomial length; three BFS runs before and after deletion verify the distances, connectivity conventions and the unit budget. For positive binary-encoded rational costs, use a common denominator formed by the product of denominators. Its bit length is at most their summed input bit lengths. The sum of the corresponding numerators and exact budget comparison also have polynomial bit length, so verification remains polynomial. Unit price one lies in this rational class, giving hardness without any unsupported weighted vertex-cover identity. An exact optimizer would decide the unit budget question by comparing its output value with B.

## 5. Finite and exact-distance variants, without protected edges

For each terminal pair add a four-edge path with three fresh internal vertices, disjoint from the other new paths internally and with no other incident edges. A simple terminal path entering a new internal vertex must continue along its degree-two chain until the opposite terminal: it traverses the whole four-edge added path. Therefore it cannot have length at most three. Since positive unit lengths permit shortest paths to be simple, no new terminal geodesic of old length three is created.

Any feasible deletion set in the augmented graph still must hit every old three-edge geodesic. Disregarding backup deletions, apply the extraction of section 3 to obtain an H-cover of size at most the total deletion count. This lower bound applies even when arbitrary backup edges are deleted. Conversely a cover's spoke deletions leave all three backup paths untouched, hit every old three-edge path, and leave a four-edge path for every pair. All three new distances are exactly four. Hence both strengthened optima equal tau(H), and the same budget equivalence and BFS certificate apply. There are nine new internal vertices and twelve new edges, a constant increase. No protected edge, large cost or global residual connectivity assumption is used.

## 6. What the finite diagnostics establish

check_controls.py was independently written and inspected before execution. It enumerates all eight nonempty labelled Q on two or three vertices. On their associated G_H it enumerates every edge-deletion subset (287,616 total), compares BFS feasibility with the explicit three-edge-path hitting predicate, and for each of 104,891 feasible masks constructs and checks the endpoint cover. It independently enumerates minimum Q/H covers and minimum blocker sizes, checking both identities. It checks all 234 H-covers on the augmented graphs yield distances (4,4,4), plus a fixed YES boundary and a one-spoke insufficient-deletion negative control. Removing all H-edges and no spokes is an explicit feasible control in every graph, preventing a false spoke-only assumption.

These are finite exact consistency checks. The arguments above establish the universal statements. No finite grid, solver output or historical verification certificate substitutes for them.

## 7. Strongest surviving original result and remaining gap

The complete original Lemmas 1–2, Theorem 3 and Corollary 4 survive this adversarial reconstruction under the exact stated model. No mathematical defect or substantive proof gap was found. External hardness is the classical NP-completeness of Vertex Cover, whose original Karp Node Cover interface was inspected. No planar, bounded-degree, arbitrary weighted-traversal, approximation or globally connected residual classification follows here. Bibliographic first priority remains unestablished; the note explicitly makes no such claim.
