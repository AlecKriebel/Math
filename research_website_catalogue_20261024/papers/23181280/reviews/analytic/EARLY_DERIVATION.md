# Independent reduction reconstruction, before primary or review exposure

Checkpoint: 2026-10-25T07:08:00Z (rounded). Bounded analytic-review completion estimate: 45%. This is a scientific review artifact without publication authority. All 203 papers remain ongoing.

Read before this seal: the project policy; exact queue row 94; fresh actual Zenodo record/latest/versions and actual file-object transport receipts; complete actual four-page PDF, including all four renders; complete controlling source `published-source/source_preparation/root_dependent_spanning_trees.tex`. No archive audit, historical proof or verdict, root/sibling opinion, supplied verification program, or external primary body has been read. The original source packet has already been independently frozen in a 59-binding manifest and seal.

## Literal claim and computational model

Input: a finite connected simple undirected graph G=(V,E), N=|V|>=1; the full table c_r(a)>=0 of integer costs for every root r and both directions a of every undirected edge, explicitly encoded in binary; an integer threshold K. A certificate is one common undirected spanning tree T. For each root, every tree edge is oriented away from that root, and every resulting arc is charged. The decision predicate is F(T)=sum_r sum_{a in T^r} c_r(a)<=K. This is not a separate tree for each root and not merely the cost of root-to-terminal paths.

Theorem target: this decision problem is NP-complete with every table entry in {0,1,2}, hence strongly NP-complete, and its minimization version is NP-hard. The positive-cost corollary restricts entries to {1,2,3}. The equivalence to the inward convention requires transposing each root's arc table.

The primary-interface assertions about Kaibel's exact objective, Martin's extension, Karp's restricted satisfiability theorem, and historical novelty remain unchecked at this early seal. They are not assumptions used to validate the internal reduction except for the standard NP-completeness of at-most-three-literal CNF satisfiability, whose exact cited interface will be checked later.

## Polynomial normalization and construction

Remove repeated literals and tautological clauses. Repeated literals can be removed without changing clause truth, and a clause containing both signs is always true and may be discarded. If any empty clause remains, a fixed two-vertex one-edge instance with all four table entries equal to one and K=1 is a no-instance: each of two root orientations contributes one, total two. If no clauses remain, the same graph with all costs and K zero is a yes-instance. Delete unused declarations and densely relabel the variables appearing in literals. This prevents a large binary variable label from being interpreted as an exponentially large vertex count.

In the remaining case n>=1 and m>=1. The graph consists of distinct hubs t,f, variable vertices v_i, and clause vertices q_j. It has the hub edge tf, two hub-variable edges tv_i and fv_i per variable, and q_jv_i precisely for the variables occurring in clause j. There are no multiedges because the normalized clause contains no repeated variable or both signs. Each clause is nonempty, each variable has hub neighbours, and tf joins the hubs, so the graph is connected. N=n+m+2 and |E|<=1+2n+3m.

The table is explicitly filled as follows. At root t the cost is symmetric: zero on tf, one on every hub-variable edge, and two on every clause-variable edge. For root q_j the only possibly nonzero arcs are v_i->t and v_i->f for variables appearing in that clause. A positive literal gets costs (0,1), and a negative literal gets (1,0). Reverse arcs and every other arc cost zero there. Root f and all variable-root vectors are zero. These values depend only on the input formula, never on a prospective tree. Set K=n+2m. There are 2N|E|=O((n+m)^2) entries, all constant-sized, and K<=2N. Dense labels, the graph and the full table can be written in polynomial time in the original formula encoding.

## Universal structural bound

Partition the edges of an arbitrary spanning tree into p hub-variable edges, q clause-variable edges, and h copies of the hub edge, where h is either zero or one. Every clause vertex has positive tree degree, and only clause-variable edges are incident to it. Each such edge meets exactly one clause vertex. Thus q=sum_j deg_T(q_j)>=m. The tree edge count is p+q+h=N-1=n+m+1.

The symmetric root-t table charges p+2q, independently of its orientation. Eliminating p gives

`F_t(T) = p+2q = (n+2m) + (1-h) + (q-m)`.

Both last terms are nonnegative integers. All other root costs are nonnegative too. Therefore F(T)<=K forces h=1 and q=m. The sum of m positive clause degrees then equals m, so each clause is a leaf. Removing all clause leaves preserves a connected acyclic core on hubs and variables. A variable has no variable neighbours, so it must meet at least one hub in that core. It cannot meet both hubs, since tf plus both attachments would be a cycle. Hence every variable has exactly one hub attachment.

No comparison with the maximum possible literal penalty is necessary. The choice of two for clause edges already gives a strict unit penalty for every structural violation. More generally with clause-edge cost B, one has

`F_t(T) = (n+Bm) + (1-h) + (B-1)(q-m)`.

For every integer B>=2 the same forcing argument holds. At B=1 this specific bound no longer penalizes excess clause edges; no unproved claim about the entire B=1 decision problem is made.

## Literal-root identity on exactly the forced family

Call the preceding forced trees structured. Encode x_i=true if v_i attaches to t and false if it attaches to f. Each clause leaf has one selected variable, and normalization ensures exactly one associated literal in that clause.

Root a structured tree at q_j and let v_i be that leaf's neighbour. Its path into the core is q_j->v_i->h_i, so the selected variable's unique hub edge is directed v_i->h_i. Every other variable is a leaf of the two-hub core and is reached from its own hub, so its hub edge is directed hub->variable. Clause leaves attached to any variable do not alter this direction: they are terminal branches. The only arc with a potentially nonzero q_j-root cost is therefore the selected v_i->h_i. Its cost is one exactly when that selected literal is false and zero exactly when it is true.

Summing gives the exact identity, for every structured tree and only for that family,

`F(T)=K + number of false selected clause literals`.

Unselected variables of clause j contribute zero because their selected hub edges point in the reverse, zero-cost direction. Costs of hub edges and clause edges at clause roots vanish by construction. The t-root contributes K, and the f and variable roots contribute zero. No charge from another clause root is omitted.

## Both reduction directions and complexity consequence

If the formula is satisfiable, include tf, the n hub attachments representing a satisfying truth assignment, and one edge from each q_j to a true literal's variable. This is connected and has 1+n+m=N-1 edges; it is therefore a spanning tree and is structured. The identity gives F(T)=K.

Conversely, if a spanning tree has F(T)<=K, the nonnegative structural bound first forces it to be structured. The literal-root identity and nonnegativity of its false-literal count force every selected literal to be true. Each clause has one selected literal, so the encoded assignment satisfies every clause. This proves satisfiability iff the decision answer is yes. It also proves the exact separation: a no formula yields no tree at or below K, while a yes formula yields a tree of cost exactly K. An unrestricted optimum formula in terms of the minimum number of unsatisfied clauses is neither needed nor established.

A certificate is at most N-1 edges. Connectivity and edge count verify it is a tree in polynomial time. Breadth-first traversal from each of N roots generates all N(N-1) oriented tree arcs, whose costs are looked up in the explicit table and summed. For arbitrary binary costs of maximum bit length L, intermediate sums have O(L+log(N(N-1))) bits. The full verification is polynomial in the explicit input size. N=1 has the empty spanning tree and cost zero; negative K is simply a no-instance. This covers the general NP-membership claim.

NP-hardness follows from the satisfiability equivalence, provided the standard restricted-CNF source theorem is supplied. The reduction uses bounded costs and K<=2N, so it remains polynomial with unary numerical encoding and proves strong NP-hardness in the usual sense. Combining it with membership gives strong NP-completeness. A polynomial exact minimization algorithm would answer the threshold question and hence is NP-hard.

For the positive-cost corollary, add one to every entry of every root's table. Every tree has exactly N-1 arcs at each of N roots, so all objectives shift by the same N(N-1). Increasing K by that quantity preserves every decision answer. New costs lie in {1,2,3}, and the new threshold remains polynomially bounded. To reverse the orientation convention, transpose c'_r(u,v)=c_r(v,u); every inward arc matches the corresponding outward arc's old charge exactly.

## Independent auxiliary identity and falsifiable controls

For a tree edge {a,b}, delete it and let S_a,S_b be the two root sets on the respective endpoint sides. Away-from-root orientation is a->b precisely for roots in S_a and b->a precisely for roots in S_b. Consequently the full objective also equals

`sum_{ab in T} [sum_{r in S_a} c_r(a,b) + sum_{r in S_b} c_r(b,a)]`.

This provides an independent check against root-by-root traversal and detects root-path-only or reversed-orientation implementations. It does not make the edge weights tree-independent: S_a and S_b depend on the selected tree.

Necessary controls identified before any code inspection: exhaustively check small trees against both objective evaluators; test the unrestricted base identity and every structural-violation unit gap; check individual literal-root costs only on structured trees; include duplicate/tautological/empty clauses, no clauses, duplicate clauses, single literals, unused declarations and sparse labels; test inward transpose and uniform shift on all trees of chosen small instances. Such finite checks can falsify an implementation or a displayed identity but cannot prove NP-hardness.

## Early finding and remaining work

No central mathematical defect is found in the literal reduction. The same-tree and whole-orientation requirements are essential to this proof; arbitrary real input costs, negative costs, root-independent costs, separately optimized root trees, and root-to-terminal path objectives are not established by it. The required primary source theorem, exact Kaibel interface, classical-extension interpretation, bounded novelty/credit, supplied-code behavior and final preservation receipts remain unchecked. The early supported result is the complete conditional reduction and complexity proof above, not a novelty or publication verdict.
