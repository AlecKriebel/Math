# Independent adversarial review:10000043

**Verdict: PASS for the partial conclusions, with the general problem unresolved.** No mandatory mathematical correction was found. This review does not certify novelty, external peer review, or a solution of the finite-but-unbounded fiber case.

Frozen artifact: `PARTIAL.md`, SHA256 `2a716868a8d7e2462adf14045212a8e3d8d502312743b7c1d8aa80575b1b479f`. A byte-identical snapshot is retained as `reviewed_partial.md`. Reviewed2026-09-30 by a separate gpt-6-astra agent at xhigh. The author’s source files were not edited.

## 1. Exact problem and graph conventions

The requested problem-page lookup was unavailable. I independently read the recovered original [Benjamini notes](https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf), including the rendered p76, Open Problem9.49. The standing conventions are simple, countable, locally finite graphs on p5; independent Bernoulli bond percolation on p32; and infinite connected graphs and the Cartesian product on p33. Thus the artifact uses the correct model. There is no standing bounded-degree hypothesis.

The original asks whether infinite clusters have infinite vertical-fiber intersections under \(p_c(G)=1\). The artifact does not exploit empty fibers as a negative answer. Its propagation lemma shows that any infinite fiber intersection is shared by all base fibers. Hence an infinite cluster that fails the intended property has only finite intersections, including zero, on every fiber. The capped proposition excludes a uniform finite upper bound, leaving the stated residual case intact.

All assertions are for each fixed percolation parameter. No simultaneous assertion over uncountably many\(p\) is needed or certified.

## 2. Propagation of infinite intersections

The deletion-of-one-fiber proof is correct and avoids conditioning on a completed cluster, which would bias its boundary edges.

Fix adjacent base vertices\(u,w\), and let\(\mathcal F\) reveal precisely the edges with both endpoints outside\(F_w\). Enumerate all product vertices by natural numbers; each cluster of this revealed graph can be measurably indexed by its least-numbered vertex. Conditional on\(\mathcal F\), a cluster\(D\) with infinitely many vertices in\(F_u\) has infinitely many distinct horizontal edges into\(F_w\). None belongs to\(\mathcal F\). Their conditional states remain independent Bernoulli\((p)\). For\(p>0\), infinitely many are open almost surely. The countable union over the measurable cluster enumeration preserves this conditional probability-one statement.

Suppose now an original cluster\(C\) has infinitely many vertices in\(F_u\) but only finitely many in\(F_w\). Delete\(S=C\cap F_w\). If\(S\) is nonempty, the number of components of\(C\setminus S\) is at most the total number of edges incident to\(S\); this is finite by local finiteness. If\(S\) is empty, the remainder is connected. Therefore one remainder component meets\(F_u\) infinitely. It is a complete cluster of the revealed graph: any further revealed open connection would belong to the original cluster and would connect components without using\(F_w\). The conditional argument then forces infinitely many vertices of\(F_w\) into\(C\), a contradiction.

There are only countably many oriented base edges. Intersecting their probability-one events, then following a finite base path, proves the global dichotomy simultaneously for all clusters. A uniform degree bound was never used; finiteness of the sum of the finitely many degrees in\(S\) is enough.

## 3. Nonanticipating capped exploration

### 3.1 Fairness and the deterministic trial bound

For fixed\(M\) and root\(x\), the capped breadth-first search only queries edges incident to already accepted vertices. Every such vertex has finitely many incident edges. Thus there is a sequential, nonanticipating implementation with one fresh query at each step. Breadth-first order is fair even if degrees are unbounded globally: the graph ball of any fixed radius in a locally finite connected graph is finite, and each queued vertex has only finitely many predecessors and incident edges to process.

For a fixed base edge\(e=\{u,v\}\), every queried edge above\(e\) has a height already accepted in\(F_u\) or\(F_v\). Each of these two height sets has cardinality at most\(M\), and a product edge above\(e\) is uniquely determined by its height. Consequently there are at most\(2M\) distinct queries above\(e\), regardless of their interleaving with other queries. The rule forbidding repeat queries is essential and is present in both proof and implementation.

The factor2 is genuinely relevant: an independent finite triangle-base example with cap2 accepts heights\(\{-1,0\}\) in one fiber and\(\{1,2\}\) in another, and queries all four edges between them. Thus replacing\(2M\) by\(M\) would not be justified by this argument.

### 3.2 Why reservoirs preserve the product law

Generate independent reservoirs\((X_{e,j})_{1\le j\le2M}\) for all base edges, independent of the vertical-edge variables. At any query, the next reservoir entry used has not previously been revealed. Its label is selected using only past revealed outcomes, so its conditional distribution is Bernoulli\((p)\), independently of the past. Induction gives the same law for every finite exploration transcript as querying a pre-existing independent product-edge configuration.

This argument is valid even though the queried heights depend on outcomes from other reservoirs. It is independence of *unread input variables*, rather than independence of adaptively selected output locations, that is used. No reservoir is selected using an unread value.

Completing unqueried product edges independently is also legitimate. In the ordinary product model, conditional on a finite adaptive transcript, the as-yet-unqueried edge states have their original independent law. Passing to the increasing transcript sigma-fields preserves this deferred-decision description for the countable exploration. Equivalently, one can realize the original product model first and expose it by the identical adaptive query rule. The finite transcript laws agree, and the completion has the required product distribution. This is not conditioning on the global event of bounded fiber intersections.

### 3.3 Independent base domination

The base variables
\[
Y_e=\max_{1\le j\le2M}X_{e,j}
\]
are functions of disjoint independent reservoirs. Hence they are independent, each with parameter\(q_M=1-(1-p)^{2M}\). This statement includes unused reservoir entries and does not assert that the actually queried edges form an independent selected family.

Every accepted vertex has an exploration ancestry path from\(x\). Each horizontal step on that path used an open reservoir entry, so its projected base edge is\(Y\)-open; vertical steps do not change the projection. Thus the accepted projection is contained in the\(Y\)-cluster of the base root. For finite\(M\) and\(p<1\),\(q_M<1\) exactly. The assumption\(p_c(G)=1\) therefore makes this base cluster finite almost surely. With at most\(M\) accepted vertices above each base vertex, the capped exploration is finite almost surely.

On the event that the actual root cluster has at most\(M\) vertices in every fiber, no new vertex of that cluster can be rejected because a fiber is full. Indeed, the\(M\) vertices already accepted there are distinct vertices of that same cluster; an additional distinct neighbor would violate the assumed bound. Induction along finite open paths and fairness therefore recovers the entire actual cluster on this event. It must consequently be finite almost surely.

Finally, there are countably many roots and integer caps. Their null-event union excludes every infinite cluster with a finite global fiber bound, including when the bound would otherwise be chosen randomly after seeing the configuration. No union over arbitrary functions\(v\mapsto M_v\) is taken.

## 4. Known uniqueness cases and source attribution

The unique-infinite-cluster observation is correct. Vertical translation acts mixingly on the independent edge process: finite cylinder events have disjoint supports after a sufficiently large shift, and approximation extends the result. Existence is therefore a zero-one event. If an infinite cluster exists, countability gives a vertex with positive infinite-cluster probability. FKG with a fixed finite connecting path propagates positivity to every vertex. The vertical ergodic theorem then gives a positive density of infinite-cluster vertices along each fixed fiber. Under uniqueness, they all belong to the same cluster. Countably many fibers give the simultaneous conclusion. Without uniqueness this last identification would fail, and the artifact does not make it.

I independently inspected [Benjamini–Kozma, *Uniqueness of percolation on products with Z*](https://alea.math.cnrs.fr/articles/v10/10-02.pdf), Theorem2 and published Lemma7, especially pp16 and22–23. Their assumption is a single uniform bound on edge cuts separating arbitrary finite base sets from infinity. Theorem2 excludes infinitely many infinite clusters; the paper’s initial zero-one/\(0,1,\infty\) classification supplies the stated at-most-one consequence. Lemma7 directly proves the fiber property under the stronger hypothesis. Theorem1’s counterexample contains copies of high-dimensional integer lattices, so its base has critical probability below1 and cannot refute the present target.

The cited [Hutchcroft–Pan relative Burton–Keane statements](https://arxiv.org/html/2409.12283v1), Theorems1.7 and3.1, bound the number of clusters with infinite intersection with a marked set under their hypotheses. They do not by themselves force every infinite cluster to have such an intersection. The source audit’s limited use of that paper is accurate.

## 5. Stretched tree and the unbounded-capacity obstruction

For the binary tree with level-\(n\) edge lengths\(2^n\), each root-to-original-level-\(n\) path has length\(2^{n+1}-2\), and there are\(2^n\) such paths. The union bound gives exactly the displayed estimate tending to zero for each\(p<1\). The portion preceding a fixed original level is finite, so an infinite root cluster would reach every level. Positivity of an infinite-cluster event at any other vertex would, by FKG and opening a fixed finite path, imply positivity at the root. Thus no vertex percolates below1 and\(p_c(T_*)=1\).

For the finite set containing the full subdivided tree through original level\(n\), each of its\(2^n\) boundary branch vertices has two distinct outgoing subtrees. Choose one infinite ray through each outgoing edge. These\(2^{n+1}\) rays are edge-disjoint, although paired rays may share their initial vertex. Any edge cut making *every* vertex of the finite set lie in a finite component must meet all these rays. Cutting edges inside the finite set cannot evade this requirement, since the rays themselves start at its boundary vertices. Therefore the claimed lower bound on cutset size and failure of uniform\(K\) are correct. The example does not assert anything negative about the original product-fiber question.

For the inhomogeneous ray, the sum of edge-failure probabilities is\(1/2\). The finite union bound, followed by continuity from above, gives positive probability of an entirely open ray. This correctly demonstrates why individual edge parameters below1 are not controlled merely by the homogeneous statement\(p_c(G)=1\). Replacing a fixed cap by unbounded deterministic capacities is therefore not a valid completion of the proof. Random capacities would additionally create dependence issues.

## 6. Independent computation and verdict

The original checker was copied into an isolated review subdirectory and rerun without altering the author’s files. All4,996 original assertions reproduce.

The separately written `independent_checks.py` adds multiple interacting base-edge reservoirs. On a three-vertex base path with three heights, it compares complete accepted-set laws for caps1 and2 at the exact parameters\(1/2,1/3,2/3\), using4,096 direct configurations and up to16,384 reservoir configurations. It verifies the *joint* law of the two dominating base variables, including their independence. A further test verifies the entire completed product-edge law on128 configurations, not only the exploration output. It also checks a configuration attaining\(2M\) queries, increasing finite-degree controls, and80 exact ray-product inequalities. All90,170 elementary assertions pass.

These finite checks do not replace the infinite exploration, conditional-independence, ergodicity or countability arguments; those were audited above. No defect requiring a source revision was found. The exact frozen package passes for publication as an unresolved partial result. The remaining possibility is an infinite cluster with finite intersection with every fiber and unbounded intersection sizes across base vertices. That possibility is neither excluded nor constructed here.
