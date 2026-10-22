# Independent adversarial review: literal full tensegrity partitions

PR #1001; problem 6900004; pinned head `f333d06cc161b1b8ae8422bf413ed1ffae31e614`.

**Verdict: the complete literal theorem is proved.** I found no mathematical gap in the proof under its stated hypotheses. The proof does not establish a classification after arbitrary ambient homeomorphisms or an abstract equivalence of stratified spaces. This distinction is substantive: the explicit nonisomorphic-tree construction below shows that the literal classification cannot answer those alternative comparisons.

This review reconstructed the equations and topology independently from the pinned report and primary definitions. I did not read historical `AUDIT.md`, earlier reviewer conclusions, or other current reviewer findings. I did read the current PR status and acceptance to identify the actual theorem and retained interpretation hold. Those documents were not evidence for correctness. No original authored source, PR state, deposit, or external communication was changed.

## Exact hypothesis and success criteria

For each integer \(n\ge1\) and \(d\ge1\), let \(G,H\) be simple graphs on the same labeled vertex set \([n]\), including isolated vertices. For \(P=(p_1,\ldots,p_n)\in X=(\mathbb R^d)^n\), define

\[
A_G(P):\mathbb R^{E(G)}\longrightarrow (\mathbb R^d)^n,
\qquad (A_G(P)w)_i=\sum_{j:\{i,j\}\in E(G)}w_{ij}(p_j-p_i).
\]

The stress space is \(W_G(P)=\ker A_G(P)\). One scalar belongs to each unordered edge. Nonedges and diagonal entries are zero in the redundant symmetric-array convention.

Within each fixed graph, two configurations have equivalent fibers if there is a homeomorphism between their stress spaces preserving the sign of every labeled coordinate, with sign zero preserved as well. The partition \(\mathcal S_d(G)\) consists of the connected components of the resulting equivalence classes in the full Euclidean configuration space. Equality of partitions means identical collections of subsets of that same \(X\). All vertex collisions and every deficient affine span are allowed.

The claim to verify is
\[
\mathcal S_d(G)=\mathcal S_d(H)\iff E(G)=E(H).
\]
The hard direction must produce two configurations in a single connected \(H\)-equivalence component but in distinct \(G\)-equivalence classes whenever \(G\) has an edge absent from \(H\). Endpoint equivalence alone is insufficient. A valid proof must not assume semialgebraicity, generic rank, graph connectivity, full affine span, or a prior classification.

## Reconstruction of the decisive invariant

For an edge \(e=\{i,j\}\in E(G)\), let \(u_e\in\mathbb R^{E(G)}\) have coordinate \(1\) at \(e\) and zero everywhere else. Then
\[
A_G(P)u_e=(0,\ldots,p_j-p_i,\ldots,p_i-p_j,\ldots,0).
\]
Consequently \(u_e\in W_G(P)\) exactly when \(p_i=p_j\). More generally, the positive singleton-support sign vector is realized exactly at such a collision: if its nonzero edge coordinate is \(c>0\), equilibrium at \(i\) is \(c(p_j-p_i)=0\). This is the known degenerate-edge criterion in Panina, Section 3, Lemma 4; the derivation here needs no result about oriented matroids or their topology.

If a sign-preserving fiber homeomorphism existed from a collided edge placement to a noncollided one, its image of \(u_e\) would be a positive singleton-support stress at the latter placement, which the displayed equation rules out. The homeomorphism need not be linear, continuous in the configuration, or normalized: positivity and all other coordinates being zero suffice. Its inverse is also sign preserving because the map is bijective. Thus the collision diagonal
\[
\Delta_{ij}=\{P:p_i=p_j\}
\]
is a union of entire fiber-equivalence classes, and therefore of strata, whenever \(\{i,j\}\in E(G)\).

## Independent incidence-space derivation of transport

Fix any orientation for each edge of \(H\), and let \(B_H\) be the \(n\times |E(H)|\) incidence matrix with \(+1\) at the first endpoint and \(-1\) at the second endpoint. Take a nonzero \(a\in\mathbb R^d\), scalars \(x_k(t)\), and \(p_k(t)=x_k(t)a\). Put
\[
D_t=\operatorname{diag}(x_v(t)-x_u(t))_{(u,v)\in E(H)}.
\]
Then at each vertex the vector equilibrium sum is \(a\) times the corresponding coordinate of \(B_HD_tw\). Since \(a\ne0\),
\[
W_H(P(t))=\ker(B_HD_t).
\]
If no \(H\)-edge is collapsed on a connected time interval \(I\), each diagonal entry of \(D_t\) is continuous, nonzero, and of constant sign. In particular \(D_t\) is invertible and
\[
T_t=D_t^{-1}D_{t_0},\qquad B_HD_tT_t=B_HD_{t_0}.
\]
Every diagonal entry of \(T_t\) is positive. This gives an explicit ambient linear homeomorphism restricting to
\[
T_t:W_H(P(t_0))\longrightarrow W_H(P(t)).
\]
Surjectivity follows from the inverse \(D_{t_0}^{-1}D_t\), not merely from inclusion. Every coordinate sign, including zero, is preserved. Reversing any edge orientation negates the corresponding diagonal entry of both \(D_t\) and \(D_{t_0}\), leaving their quotient unchanged.

This factorization also shows that every such noncollapsed collinear fiber has dimension \(|E(H)|-n+c(H)\), where \(c(H)\) includes isolated vertices. A collision of nonadjacent vertices creates no extra equation: the nonzero edge scalings leave the incidence rank unchanged. The dimension formula is corroboration; it is not used to infer sign equivalence.

Because the same construction works for every \(t\in I\), the complete continuous image \(P(I)\) belongs to one fiber-equivalence class \(C\). The image of an interval is connected in \(X\), hence in the subspace \(C\). Every connected subset of a space lies in one connected component. Therefore all points of the path share one \(H\)-stratum. This uses no local triviality theorem. The continuous dependence of \(T_t\) is available as an additional check, but endpoint-by-endpoint sign equivalence plus a connected configuration path already establishes the required component claim.

For an edgeless graph, \(D_t\) and \(B_H\) have no columns, \(W_H(P)=\{0\}\) for every \(P\), and the whole connected \(X\) is a single stratum. The empty map is the appropriate isomorphism.

## Complete separation argument

Suppose \(E(G)\ne E(H)\). Swapping their names if necessary, choose \(e=\{i,j\}\in E(G)\setminus E(H)\). For \(-1/2\le t\le1/2\), choose
\[
x_i(t)=t,\quad x_j(t)=0,\quad x_k(t)=k+1\ (k\notin\{i,j\}),
\quad p_k(t)=x_k(t)a.
\]
All stationary values besides \(x_j=0\) are distinct and at least \(2\), while \(x_i\in[-1/2,1/2]\). Thus the only possible coincident pair is \(i,j\). That pair is not an \(H\)-edge. Every \(H\)-edge is noncollapsed throughout the closed interval, and the incidence derivation places \(P(0)\) and \(P(1/4)\) in the same connected \(H\)-stratum.

At \(P(0)\), \(e\) is collapsed; at \(P(1/4)\), it is not. The singleton-support invariant puts these two points in different \(G\)-fiber-equivalence classes, and hence in distinct \(G\)-strata. Identical partitions cannot give different same-stratum answers for one pair of points. Therefore the partitions differ.

If \(E(G)=E(H)\), the equilibrium matrices and fiber equivalence relations agree at every point, so their connected-component partitions agree. These two directions prove the stated theorem for all \(n,d\ge1\).

Equivalently, an intrinsic reconstruction rule is
\[
\{i,j\}\in E(G)
\iff \Delta_{ij}\text{ is a union of strata of }\mathcal S_d(G).
\]
The forward direction is the singleton-support argument. For a nonedge the constructed path crosses \(\Delta_{ij}\) within one stratum, proving that the diagonal is not a union of whole strata. This formulation confirms that the theorem reconstructs the graph from the full partition itself rather than from directly comparing stress coordinates across different graphs.

## Adversarial cases and scope boundaries

| Attempted failure | Outcome |
| --- | --- |
| \(n=1\) | The unique simple graph has no edges; there is no distinct graph pair to distinguish. The reverse implication is trivial. |
| \(n=2\), one edge versus no edges | At the collision the edge graph has fiber \(\mathbb R\), away from it fiber \(\{0\}\); the empty graph has \(\{0\}\) everywhere. For \(d=1\) the noncollision set has two components, whereas for \(d\ge2\) it has one; either way the partitions differ. |
| Disconnected graphs and isolated vertices | Incidence factorization remains valid. Isolated coordinates contribute zero equations. Connectedness of the configuration path does not require graph connectivity. |
| No stress in an \(H\)-fiber | The homeomorphism between zero-dimensional fibers is still valid. Nonzero stress in \(H\) is never assumed. |
| \(d>1\) but all chosen points lie on one line | The target base includes deficient affine span. The vector sums equal \(a\) times scalar sums and \(a\ne0\), so no transverse condition is lost. This is an admissible witness within the full base. |
| Endpoint at a nonedge collision | No denominator vanishes: denominators belong only to \(H\)-edges. Positive transport remains continuous and invertible at \(t=0\). |
| Equal stress dimensions on the two \(G\)-placements | The triangle example below has this feature. Coordinate support, rather than dimension, distinguishes them. |
| Fiber homeomorphism could change magnitudes | It may change magnitudes freely; positive singleton support remains singleton support, which is enough for the contradiction. |
| Only endpoint fiber equivalence proved | The full path is explicitly inside the equivalence class, and its connectedness proves the component assertion. |
| Redundant \(n\times n\) stress arrays | The edge-coordinate representation and symmetric zero-diagonal array representation are linearly homeomorphic and preserve all signs. The primary 2008 definitions explicitly impose symmetry and zero nonedge coordinates. |
| Vertex permutations | Literal equality fixes labels. A permutation carries the partition for \(G\) to the partition for the relabeled graph. Equality after that specified permutation is therefore equivalent to equality of the resulting edge sets. |
| Dimension \(d=0\) | The claim would fail: the base is a single point for every graph. The positive-dimension hypothesis is necessary. |
| Multigraph extension | False as a literal partition classification. On two vertices, one edge and two parallel edges each partition the full base into the collision diagonal and components of its complement. Their respective fibers differ in dimension, but their within-graph partition subsets agree. Simplicity is necessary for this classification. |
| Loops allowed | A loop contributes an unconstrained stress coordinate at every placement, and the empty graph and single-loop graph each induce a one-piece partition. Loops are excluded. |
| Base restricted to collision-free placements | The result does not extend. For example, distinct forests have zero stress at every placement with no collapsed graph edges, so the partition of the common all-distinct-point base consists just of its connected components. |
| Replace equality of subsets by ambient homeomorphism | The nonisomorphic tree construction below gives a direct counterexample to the resulting uniqueness statement. |

For \(K_3\), let \(p_1=t a\), \(p_2=0\), \(p_3=c a\) with \(c>1/2\). With edge order \(12,13,23\), the stresses for \(t\ne0\) are
\[
\lambda\left(1,\frac{t}{c-t},-\frac{t}{c}\right).
\]
At \(t=0\), only edge \(12\) is free, so the fiber is \(\mathbb R(1,0,0)\). Both fibers have dimension one. The source pair-collision claim of dimension two is inconsistent with its own equations, independently confirming the report's narrow arithmetic correction. This correction is not needed as a premise for the theorem.

### Concrete distinction from abstract or ambient equivalence

Let \(G\) be the four-vertex path \(12,23,34\), and \(H\) the four-vertex star \(12,13,14\). They are nonisomorphic because their degree multisets differ. A forest has exactly the stress vectors supported on collapsed edges: remove a leaf, use its unique equilibrium equation to force the coefficient to zero unless that edge is collapsed, and continue inductively. Collapsed-edge stresses contribute no forces anywhere and are independent.

Define the ambient linear map \(\Phi:X_{4,d}\to X_{4,d}\) by
\[
q_1=p_1,\quad q_2=p_2,\quad
q_3=p_1+p_3-p_2,\quad q_4=p_1+p_4-p_3.
\]
Its inverse is
\[
p_1=q_1,\quad p_2=q_2,\quad
p_3=q_2+q_3-q_1,\quad p_4=q_2+q_3+q_4-2q_1.
\]
The star edge differences \(q_2-q_1,q_3-q_1,q_4-q_1\) are exactly the path differences \(p_2-p_1,p_3-p_2,p_4-p_3\). Thus each collapsed-edge subset for the path corresponds to the same subset for the star under the natural edge correspondence. Their fibers are identical coordinate subspaces after that correspondence. The ambient homeomorphism maps the full fiber-equivalence classes bijectively, and therefore maps their connected components bijectively, for every \(d\ge1\).

Hence these nonisomorphic graphs define ambient-linearly equivalent stratified spaces, while the literal partitions differ by the proved theorem. The comparison convention cannot be suppressed in a publication claim. This construction does not assert which meaning the original source intended.

## Independent computation and evidentiary limits

`independent_exact_check.py` constructs the equilibrium matrices directly from the vertex equations using exact rational arithmetic. It imports no PR program. It enumerates every simple graph on \(n\le5\) and every missing vertex pair, checks both edge orientations and both witness label orders, and checks five rational times through the nonedge collision. For all graphs through \(n=4\) it additionally uses directions in dimensions two and three, including directions with zero and negative coordinates.

For every sampled path point it checks the exact matrix identity, positivity of the transport, inverse identity, direct membership of each transported kernel basis vector, independent basis rank, and nullity computed anew by exact elimination. It also checks the collapsed versus noncollapsed singleton stress for the graph with the missing edge added. Every arbitrary differing graph pair has the same mathematical support witness; the computation does not claim to enumerate all ordered graph pairs.

The final run covers **1,099 graphs, 5,325 missing-edge witnesses, and 71,280 exact transport or singleton case checks**, plus 24 path/star boundary checks. Formula reversal and an attempted transport through a collapsed graph edge are negative controls that are actually rejected. The equal-dimensional \(K_3\) support control demonstrates why dropping coordinate-zero preservation would invalidate that decisive test.

Finite checks corroborate arithmetic and the implementation. They do not establish continuous connectedness, universal quantifiers, author intent, novelty, or formal proof-assistant certification; those are separate. The continuous and universal claims are supplied by the written derivation above. Neither numerical conditioning nor floating-point tolerance enters these exact checks.

## Primary-source confirmation and remaining gap

- Karpenkov, *Open Problems on Configuration Spaces of Tensegrities*, Arnold Mathematical Journal 4 (2018), 19–25, [journal source](https://link.springer.com/article/10.1007/s40598-018-0080-7). Definitions 1.1–1.3 agree with the full-base, labeled, sign-preserving convention. Problem 4 does not provide a separate cross-graph equivalence definition. Its surrounding combinatorial discussion does not itself decide the intended comparison.
- Doray, Karpenkov and Schepers, *Geometry of configuration spaces of tensegrities*, [arXiv:0806.4976v2](https://arxiv.org/pdf/0806.4976v2), Definitions 2.1 and 2.6. These make symmetric stresses, zero nonedge coordinates, the complete Cartesian base, and connected strata explicit.
- Panina, *A universality theorem for stressable graphs in the plane*, [arXiv:1902.07212v4](https://arxiv.org/pdf/1902.07212v4), Section 3, Lemma 4. The singleton-support collision detector is already stated there. No novelty should be assigned to this detector. The present theorem does not rely on her stronger sign-set equivalence result or her framework quotient.

**Strongest verified result:** the stated theorem and collision-diagonal reconstruction criterion hold for every simple labeled graph and every positive ambient dimension, with full collision-inclusive connected partitions. **Mathematical gap in that result: none found.**

**Exact remaining publication gap:** this review establishes neither prior-art novelty nor that literal equality is the comparison intended by original Problem 4. It cannot support an unqualified claim to solve every interpretation of that open problem. A paper confined to the verified literal theorem must retain the comparison convention prominently and retain Panina attribution. Priority and the original-problem interpretation require their separate audits; contacting anyone is neither prepared nor initiated.
