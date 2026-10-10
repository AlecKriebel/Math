# Exact clique pinning in the plane: two tractable regimes

Problem: AMR-029-0001 / 3000001. This is an authored partial-result note, dated 10 October 2026. It does **not** solve the arbitrary-input problem, prove hardness, or assert that the consequences below are new to the literature. This AI-assisted manuscript is unrefereed. Acceptance refers to the separate mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

## 1. Objective and prior results

For a finite simple graph G=(V,E), let

    gamma(G) = min{|S| : S subset V and G+K_S is generically globally rigid in R^2}.

The added edges are exactly the missing edges of the clique on the chosen vertex set. The objective is vertex cardinality. No absolute-coordinate anchoring convention is imposed.

Király and Mihálykó, *Globally Rigid Augmentation of Rigid Graphs*, SIAM Journal on Discrete Mathematics 36(4), 2022, DOI https://doi.org/10.1137/21M1432417, already give exact polynomial-time clique-pinning optimization for rigid input graphs, and a deterministic polynomial-time factor-two approximation for arbitrary inputs. Their concluding section also gives exact completion when some vertices are already pinned and the graph after their clique is added is rigid. Author manuscript: https://real.mtak.hu/151592/1/Globally_Rigid_Augmentation.pdf, actual PDF pages 22–23, lines 904–934. These results are used, not claimed as new here. The inspected repository copy is labeled submitted and bears a review-manuscript footer; it is not represented as the final publisher PDF. The revised dissertation cited in Section 3 retains the needed planar theorem for simple rigid graphs of order at least six; the algorithm handles n<=5 by direct checks.

Jordán, *Rigid and Globally Rigid Graphs with Pinned Vertices*, EGRES TR-2009-05, https://egres.elte.hu/tr/egres-09-05.pdf, Lemma 4.4 (printed page 7, actual PDF page 8), supplies the sparse-graph rank formula used below. His Lemmas 7.6–7.8 already give a hypergraphic-matroid-parity formulation of the M-connected relaxation. Consequently that reformulation is also not new. Global rigidity for n>=4 is equivalent to 3-connectivity and redundant generic rigidity (Connelly; Jackson–Jordán; stated as Theorem 6.2 in this report).

## 2. Degenerate cases

Every already globally rigid graph has gamma(G)=0. A one-vertex clique adds no edge, so gamma(G) is never 1. For n=0 or 1 the optimum is 0. For n=2 the optimum is 0 if the edge is present and 2 otherwise. For n=3 global rigidity is equivalent to completeness; when G is incomplete the optimum is the number of distinct endpoints of all missing edges, either 2 or 3. Indeed all endpoints of every missing edge must be selected, and selecting their union suffices.

All subsequent rank statements concern n>=4. Write r(G) for the generic planar rigidity-matroid rank and

    delta(G) = 2n - 3 - r(G).

## 3. A sharp small rigidifying-seed lemma

**Lemma 1.** Suppose delta(G)>0 and G+K_S is rigid (in particular, S may be any globally rigidifying pin set). There is T subset S with |T|<=delta(G)+1 such that G+K_T is rigid.

**Proof.** Let delta=delta(G). Since r(G+K_S)>r(G), at least one edge ab of K_S increases rank when added to G. The graph F on S with edges ab and av,bv for each v in S\{a,b} is a Laman graph: start with the edge ab and add each remaining vertex with two incident edges. Thus F is a basis of the rigidity matroid of K_S. In the planar rigidity matroid on the complete graph on V, F and K_S have the same closure. Therefore G+F is rigid.

Start from G+ab, whose deficiency is delta-1. Process the pairs {av,bv}, adding a pair only if it increases the current rigidity rank. A skipped pair lies in the current closure and remains there as more edges are added, so at termination the graph has the same rank as G+F and is rigid. Each accepted pair increases rank by at least one; at most delta-1 pairs are accepted. Let T consist of a,b and the vertices indexing the accepted pairs. Then |T|<=delta+1, and G+K_T contains the rigid graph just constructed. QED.

The bound is sharp for arbitrarily large delta. For G=K_{1,m}, m>=3, r(G)=m and delta=m-1. Any vertex not selected retains its original degree. An unselected leaf has degree one, so G+K_T cannot be rigid. Every leaf must therefore belong to a rigidifying T. All m leaves suffice, as their clique together with the centre is K_{m+1}. Thus the smallest rigidifying seed has size m=delta+1.

**Corollary 2 (fixed-deficiency exact optimization).** Assuming the established exact rigid-input completion algorithm with already-pinned vertices, gamma(G) can be computed exactly in n^{delta(G)+O(1)} time. In particular it is polynomial-time computable on every class with bounded planar rigidity deficiency.

**Algorithm and proof.** Handle n<=5 by a constant-size direct check. The case delta=0 is the established rigid-input algorithm. For delta>0 enumerate T subset V of size at most min(n,delta+1). Discard T unless H=G+K_T is rigid. For every retained T, use the established constrained completion algorithm to find a smallest additional P subset V\T for which H+K_{T union P} is globally rigid, and minimize |T|+|P|. Every output is feasible for the original problem because H+K_{T union P}=G+K_{T union P}. Conversely, if S is an optimal original solution, Lemma 1 supplies an enumerated T subset S. For that T, S\T is a feasible completion; the exact completion is no larger. This proves equality with gamma(G). The number of enumerated seeds is at most sum_{j<=min(n,delta+1)} binomial(n,j)=n^{delta+O(1)}, and each subproblem is polynomial.

This is an XP algorithm in delta, not an FPT claim and not an arbitrary-input polynomial algorithm. It uses bounded-size rigidity seeds and an exact completion optimizer, rather than advertising full subset enumeration plus recognition as a resolution. The prior constrained-completion routine must include the already globally rigid and single-edge-completion cases; a bare atom-count formula cannot silently replace it.

For clarity, a safe implementation first tests completions by zero, one, or two additional vertices. If none succeeds, H cannot be globally rigidified by a single edge, since selecting that edge's endpoints in addition to T would have succeeded. In the remaining case the prior rigid-input atoms are disjoint, every completion must meet every atom, and a clique containing one vertex from each atom suffices. Choose one vertex in every atom missed by T. This is exactly the constrained optimum. Mihálykó's thesis, https://real-phd.mtak.hu/2172/1/Mihalyko_Andras_PhD_updated.pdf, Section 8.5, actual PDF pages 127–128, explicitly separates the partially pinned single-edge-completion case and gives a polynomial algorithm for it. No weighted pinning theorem is assumed here.

## 4. A sparse-graph redundancy criterion

Call G sparse when i_G(X)<=2|X|-3 for every X subset V with |X|>=2. For X subset V let e_G(X) count the edges with at least one endpoint in X.

**Lemma 3 (consequence of Jordán's rank formula).** Let G be sparse, n>=4, and |S|>=4. Then H=G+K_S is redundantly rigid if and only if

    e_G(X) >= 2|X|+1 for every nonempty X subset V\S.                 (1)

**Proof.** For necessity, fix such an X. The complement contains S and hence at least four vertices. If no edge touches X, H is not rigid. Otherwise choose an edge f touching X. All edges of H touching X belong to G. The rank of H-f is at most 2|V\X|-3+e_G(X)-1, since the edges inside the complement have at most the first rank and all other rows number at most the second term. Redundant rigidity requires this bound to be at least 2n-3, giving (1).

For sufficiency, Jordán's Lemma 4.4 states

    r(G+K_S) = min_{S subset Z subset V} [2|Z|-3+e_G(V\Z)].

Thus (1) first implies H is rigid. If f touches V\S, the graph G-f is still sparse and its incident-edge counts fall by at most one, so the same rank formula proves H-f rigid. If f has both endpoints in S, the graph K_S-f is rigid because |S|>=4. Consequently its rigidity-matroid closure contains K_S, and H-f has the same rank as H. All edge deletions leave a rigid graph. QED.

The criterion is not asserted to be a new recognition theorem: it is also the sparse-input specialization of Jordán's M-connected pinning inequalities. The proof is included to make exactly what is used in the following corollaries transparent.

## 5. Cubic 3-connected graphs and feedback vertex sets

Let tau(G) be the minimum number of vertices whose deletion leaves a forest.

**Theorem 4.** If G is a finite simple 3-connected cubic graph on n>=12 vertices, then

    gamma(G) = tau(G).

More strongly, for every S subset V with |S|>=4,

    G+K_S is generically globally rigid in R^2 iff G[V\S] is a forest.

**Proof.** A connected cubic graph other than K4 is sparse. For a vertex set of size two or three the sparsity inequalities are immediate. Four vertices span at most five edges, because a K4 in a cubic graph is a whole connected component. Five vertices span at most floor(15/2)=7 edges. For |X|>=6, i_G(X)<=3|X|/2<=2|X|-3.

As G is already 3-connected, so is G+K_S. The planar global-rigidity characterization and Lemma 3 therefore reduce feasibility to (1). Cubicity gives

    e_G(X)=3|X|-i_G(X).

Thus (1) is equivalent to i_G(X)<=|X|-1 for every nonempty X subset V\S, exactly the statement that G[V\S] is a forest.

It remains to ensure that the cutoff |S|>=4 does not change either optimum. For |S|<=3, H has at most 3n/2+3 edges. When n>=12 this is less than 2n-2, the necessary edge count for redundant rigidity. Hence gamma(G)>=4. If S is a feedback vertex set of size k<n and G-S has c>=1 components, then

    3n/2 - 3k + i_G(S) = i_G(V\S) <= n-k-c.

This implies k>=(n+2i_G(S)+2c)/4 >= (n+2)/4, and hence k>=4 for n>=12. If k=n, the same lower bound is automatic. Thus tau(G)>=4. The two feasible families agree throughout the range containing both optima, proving equality. QED.

**Algorithmic consequence.** Ueno, Kajitani and Gotoh proved that minimum feedback vertex set in graphs of maximum degree three is polynomial-time solvable by reduction to matroid parity: *On the nonseparating independent set problem and feedback set problem for graphs with no vertex degree exceeding three*, Discrete Mathematics 72 (1988), 355–360, DOI https://doi.org/10.1016/0012-365X(88)90226-9. Thus Theorem 4 yields exact polynomial-time clique pinning on all 3-connected cubic graphs of order at least twelve. These inputs are genuinely nonrigid: 3n/2<2n-3 for n>6. For the remaining cubic 3-connected orders 4,6,8,10, one may handle K4 by optimum zero and directly check all subsets of size at most three, comparing with a feedback vertex set enlarged if necessary to size four. This is a fixed-degree polynomial check, so the whole 3-connected subcubic class is tractable.

**Important limitation.** Dropping 3-connectivity is invalid. Let G be a diamond with edge set {01,02,03,12,13}, together with isolated vertices 4 and 5. Set S={2,3,4,5}. Every degree-at-most-two vertex is in S and G[V\S] is the single edge 01. Nevertheless G+K_S has the two-vertex separator {2,3}. Its true pinning optimum is five: all four low-degree vertices are forced, at least one of 0,1 is also needed, and selecting 0 in addition gives a K5 with the last vertex joined to three clique vertices. This example also rules out deducing vertex connectivity merely from an edge-boundary count.

## 6. Forest inputs, with arbitrary maximum degree

**Theorem 5.** If G is a forest on n>=4 vertices and L={v:deg_G(v)<=2}, then gamma(G)=|L|.

**Proof.** In a globally rigid graph on at least four vertices every degree is at least three. A vertex outside S receives no new incident edges; hence every feasible S contains L.

Suppose first |L|>=4 and put S=L, U=V\L. For every nonempty X subset U, the induced graph is a forest, so

    e_G(X)=sum_{v in X}deg_G(v)-i_G(X)
          >=3|X|-(|X|-1)=2|X|+1.

The forest G is sparse, so Lemma 3 proves redundant rigidity of H=G+K_L. We prove 3-connectivity. Delete an arbitrary set W of at most two vertices. The nonempty clique L\W lies in one component of H-W. If another component C exists, it is disjoint from L and is a connected subtree of G. All its external G-neighbors belong to W. As G is a forest, each vertex outside C has at most one neighbor in C, since two would make a cycle. Thus at most two G-edges leave C. On the other hand each vertex of C has G-degree at least three, so at least 3|C|-2(|C|-1)=|C|+2>=3 edges leave C, a contradiction. Hence H is 3-connected and globally rigid.

For n>=4, a forest with |L|<4 can only be the claw K_{1,3}, with |L|=3: if there are at least two vertices of degree at least three, the standard leaf count for forests gives at least four leaves; if there is exactly one such vertex, fewer than four low-degree vertices forces n=4; and if there is none, L=V. Pinning the claw's three leaves produces K4. This completes the proof. QED.

## 7. What remains

The arbitrary nonrigid-input optimum remains unresolved by this work. The fixed-deficiency algorithm has an exponent depending on delta; the cubic theorem relies essentially on original 3-connectivity; and the forest formula does not cover cycles and interacting higher-degree components. No NP-hardness reduction has been established. In particular, reducing the cubic case to feedback vertex set cannot establish hardness, because subcubic feedback vertex set is polynomial-time solvable.

Recorded literature searches retrieved the 2022 exact rigid-input/factor-two results and Jordán's earlier relaxation, but no verified exact arbitrary-input resolution. This is bounded negative evidence, not a proof of current openness. Recorded source identities, inspection history and limits appear in [SOURCE_METADATA.json](SOURCE_METADATA.json) and the [mathematical audit](MATHEMATICAL_AUDIT.md).
