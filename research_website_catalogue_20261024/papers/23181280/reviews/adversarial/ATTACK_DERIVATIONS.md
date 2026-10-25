# Universal reconstruction and adversarial witnesses

The theorem concerns one common undirected tree, evaluated using an independent entire oriented-tree cost vector at every vertex root. All costs are nonnegative integers explicitly listed. Only the classical NP-completeness of clause-width-at-most-three SAT is imported for hardness; the remainder is checked below for arbitrary sizes.

## 1. Preprocessing and polynomial output size

Removing duplicate literals preserves a clause's truth value. A clause containing both signs is always true and may be removed. An empty clause makes the conjunction unsatisfiable; the fixed two-vertex graph with both orientations costing1 at each root has aggregate2 and threshold1. If no clauses remain, its all-zero version with threshold0 is a yes-instance. Delete unused variable declarations and replace occurring labels by a dense indexing; the number of variables depends on occurrences, not on the largest binary label. Comparison/sorting of labels is polynomial in their encoded lengths.

For a remaining input with n occurring variables and m nonempty clauses, n≤3m and the output graph has N=n+m+2 and M≤1+2n+3m. It is simple: a clause has at most one literal on any variable, and distinct clauses have distinct vertices even if their text repeats. It is connected because every variable meets both hubs, the hubs meet each other and every clause meets a variable. Writing all2NM costs, including zeros, takes polynomial time and space. Every cost uses at most two bits, while K=n+2m≤2N.

## 2. Unrestricted accounting rules out all unintended trees

For an arbitrary spanning tree let p count hub–variable edges, q count clause–variable edges, and h∈{0,1} record the hub edge. These categories exhaust the graph. Because every clause vertex has degree at least1 and every such edge meets exactly one clause, q≥m. ExactlyN−1 edges are selected, so

    p+q+h=n+m+1.

The t-root vector is symmetric on each edge, so its value does not depend on how this tree happens to orient its edges. Therefore

    F_t=p+2q=n+2m+(1−h)+(q−m)=K+(1−h)+(q−m).

All other root costs are nonnegative. Consequently F≤K requires both h=1 and q=m, and also requires every other root's contribution to vanish. The sum of the m clause degrees is q=m, so each clause is a leaf. Deleting these leaves preserves connectedness and acyclicity on the remaining vertices. The remaining edges are only hub–variable edges and the hub edge. A variable cannot have degree0 there, and two hub attachments would form a triangle with the hub edge. Thus every variable has exactly one hub attachment.

This argument covers trees in which the hubs connect through a variable, variables connect through internal clause vertices, or variable vertices have no hub edge. Each such tree necessarily incurs a positive structural excess. It uses no typical-tree assumption, optimality exchange or enumeration of a restricted tree family.

## 3. Literal costs and both reduction directions

In a structured tree let x_i be true exactly when its unique hub is t. Each clause q_j is a leaf and selects a unique variable, hence a unique literal because preprocessing excluded repeated/complementary occurrences.

From root q_j the route starts q_j→v_i→h_i, where v_i is the selected variable and h_i its chosen hub. The two stars joined by the hub edge form the entire remaining core. Every other variable's hub edge is directed from its hub into that variable. All hub-to-variable arcs cost zero at q_j. Its only potentially charged selected arc is therefore v_i→h_i: cost0 when the selected literal is true and1 when false. Other clause edges and the hub edge have zero q_j-cost. The f-root and variable-root vectors vanish. Hence, for every structured tree,

    F=K+number of false selected literals.

For a satisfying assignment choose each variable's truth hub and one true literal per clause. The hub edge plus these attachments form a connected graph with exactlyN−1 edges, hence a tree. Its value isK. Conversely, any tree with value≤K is structured by section2, and the displayed equality forces all selected literals true. Every clause therefore has a true literal. This proves SAT iff a tree of value≤K, for every normalized formula, rather than just the finite controls.

## 4. NP membership, strong hardness and conventions

A certificate listsN−1 graph edges. Check membership/distinctness, connectedness and acyclicity, then traverse the tree from each root and sum itsN−1 directed costs. If input costs have at mostb bits, the total needs at mostb+ceil(log2(N(N−1)))+O(1) bits. Running time and intermediate bit lengths are polynomial in the explicit input length. For N=1 there is a unique empty tree with aggregate0, including when K is negative.

The reduction uses alphabet{0,1,2} and a threshold≤2N. Unary encoding of numerical data still has polynomial length, proving strong NP-hardness; with membership this gives strong NP-completeness. Adding1 to every directed cost at every root adds exactlyN(N−1), independent of which tree was selected. The shifted threshold remains polynomially bounded and all costs lie in{1,2,3}.

For inward orientations replace c_r(u,v) with c_r(v,u), with root indexr unchanged. Each inward arc is the reverse of the corresponding outward arc, so all root costs are preserved. This does not assert hardness for symmetric root vectors: only the t-vector is symmetric in the reduction. Nor does it charge merely the first edge of a rooted tree or permit different underlying trees at different roots.

## 5. Martin lift: why the source model agrees

The inspected Martin formulations project onto the spanning-tree polytope in x and impose nonnegative directed root variables with each edge's two directions summing to the same x_e. Each nonroot has indegree1, the root indegree0. For integral feasiblex, the projection describes a spanning-tree incidence vector. On that tree the root variables are unique: remove a nonroot leaf, whose incoming edge is forced to1, and continue, or use the unique path fromr to each vertex. Thus minimizing the sum of arbitrary linear objectives on all root orientations, over integral common x, gives exactlyF(T).

An integral projection describes optimization of objectives that depend only on x. It does not establish integrality of the full joint lift for objectives involving all root variables. No LP tractability assumption invalidates the reduction. The actual source's neighboring Problem2 charges root-to-vertex paths in a different directed model and is not used.

## 6. Constructed negative controls explain real boundaries

These are counterexamples to tempting stronger or corrupted claims, not to the submitted theorem.

For L≥1 let Φ_L consist of L copies of each of the four clauses on x_2,x_3,

    (x2∨x3), (x2∨¬x3), (¬x2∨x3), (¬x2∨¬x3),

plus the bridge clause(x1∨x2). Every assignment falsifies exactly one of the four sign clauses per copy. Taking x1=true satisfies the bridge, so the minimum number of false clauses isL and the formula is unsatisfiable.

Construct a tree with the hub edge, t–v1, the bridge clause joined to bothv1 andv2, one positive binary clause joined to bothv2 andv3, and every other binary clause joined only tov2. It is connected with N−1 edges. It has p=1,h=1,q=m+2. At every clause root all variable-to-hub arcs with potentially nonzero costs are absent: the only remaining variable-to-hub edge is v1→t, which is free at the positive bridge clause and irrelevant to every binary clause. Thus every clause-root contribution is0.

If the clause-edge base penalty wereB=1, this tree would have F=K_B=m+3 despite an unsatisfiable formula. Hence B≥2 is essential for the structural lemma. With the submittedB=2 and L=3, m=13,N=18,K=29 and this tree hasF=31, while K+minimum-unsatisfied-clauses=32. The unrestricted optimum is at most31, so the latter purported exact characterization would be false. The current manuscript expressly restricts the literal equality to structured trees and disclaims this stronger global identity. Both witnesses were checked by explicit full cost tables and whole-root orientations.
