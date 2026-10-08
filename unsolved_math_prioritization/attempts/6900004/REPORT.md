# Full labeled tensegrity partitions determine the graph

**Status, 8 October 2026:** accepted after independent mathematical and source-scope review for equality of full partitions of the fixed labeled configuration space, with explicit attribution to Panina's Lemma 4. The unqualified original-problem interpretation hold remains. The phrase “same stratifications” in the source is not separately defined across graphs; this note does not settle a potentially intended weaker equivalence of abstract stratified spaces.

## 1. The precise claim

Fix integers \(n\geq 1\) and \(d\geq 1\). All graphs below are simple graphs on the **same labeled vertex set** \([n]\); missing vertices of a subgraph of \(K_n\) are treated as isolated vertices. For a configuration
\[
P=(p_1,\ldots,p_n)\in X_{n,d}:=(\mathbb R^d)^n,
\]
let
\[
W_G(P)=\left\{w\in\mathbb R^{E(G)}:
\sum_{j:\{i,j\}\in E(G)}w_{ij}(p_j-p_i)=0\quad\text{for every }i\right\}.
\]
There is one scalar per **unoriented** edge, so \(w_{ij}=w_{ji}\). These coordinates can equivalently be embedded in the symmetric zero-diagonal \(n\times n\) arrays, with nonedge coordinates zero. This redundancy does not change sign-preserving equivalence.

Two fibers for the **same** graph are equivalent when a homeomorphism between them preserves the sign of every labeled edge coordinate, including zero. Let \(\mathcal S_d(G)\) be the partition of \(X_{n,d}\) into connected components of these equivalence classes. No quotient by affine transformations, Euclidean transformations, vertex permutations, or ambient homeomorphisms is taken. Configurations with coincident points, collapsed edges, crossings, or deficient affine span are retained.

Here equality \(\mathcal S_d(G)=\mathcal S_d(H)\) means equality as collections of subsets of the **same** space \(X_{n,d}\). Stress spaces of different graphs are not directly compared.

**Theorem.** For every \(n\geq 1\), \(d\geq 1\), and pair of simple labeled graphs \(G,H\) on \([n]\),
\[
\boxed{\quad \mathcal S_d(G)=\mathcal S_d(H)\quad\Longleftrightarrow\quad E(G)=E(H).\quad}
\]

Thus, on the literal full-partition interpretation, each equivalence class of subgraphs consists of a single labeled graph. The criterion covers all dimensions allowed in the source and all strata, including high-codimension degeneracies.

## 2. Two elementary observations

**Observation A: a collapsed edge is detected by its coordinate support.** This is the degenerate-edge criterion in Panina, Section 3, Lemma 4 ([preprint v4, p.8](https://arxiv.org/pdf/1902.07212v4)); it is reproved here for completeness. Suppose \(e=\{i,j\}\in E(G)\). A stress whose only nonzero coordinate is \(w_e=1\) belongs to \(W_G(P)\) if and only if \(p_i=p_j\). Indeed, all equilibrium equations are zero except possibly those at \(i,j\), where the forces are \(p_j-p_i\) and \(p_i-p_j\). Consequently, a collapsed and a noncollapsed realization of this edge cannot have sign-preservingly equivalent \(G\)-fibers: a homeomorphism preserving every coordinate sign would have to preserve the existence of this singleton-support positive stress.

**Observation B: collinear motion with no collapsed graph edge gives explicit sign equivalences.** Let \(a\in\mathbb R^d\) be nonzero and write \(p_k(t)=x_k(t)a\), with \(t\) ranging over an interval \(I\). Suppose each scalar difference \(x_v(t)-x_u(t)\), for \(\{u,v\}\in E(H)\), is continuous and never zero on \(I\). Fix \(t_0\in I\). Define, for each edge,
\[
(T_t w)_{uv}
=\frac{x_v(t_0)-x_u(t_0)}{x_v(t)-x_u(t)}\,w_{uv}.
\tag{1}
\]
The quotient is independent of the orientation chosen for the edge and is strictly positive. The map is diagonal and invertible. For either endpoint of an edge,
\[
(T_t w)_{uv}\bigl(p_v(t)-p_u(t)\bigr)
=w_{uv}\bigl(p_v(t_0)-p_u(t_0)\bigr).
\tag{2}
\]
Therefore every vertex equilibrium sum is preserved term by term. The inverse transformation proves
\(T_t(W_H(P(t_0)))=W_H(P(t))\). It is a linear homeomorphism preserving every coordinate sign. Hence the entire continuous configuration path \(P(I)\) lies in one fiber-equivalence class. As it is connected, it lies in one stratum of \(\mathcal S_d(H)\).

This argument also applies when \(H\) has no edges: its stress fiber is the zero vector space and the empty diagonal map is its unique linear isomorphism.

## 3. Proof of the theorem

Identical edge sets clearly give identical fibers and partitions.

Conversely, assume \(E(G)\neq E(H)\). Interchange the names of the graphs, if needed, and choose
\[
e=\{i,j\}\in E(G)\setminus E(H).
\]
Choose \(a\neq 0\) in \(\mathbb R^d\), and for \(-1/2\leq t\leq 1/2\) set
\[
x_i(t)=t,\qquad x_j(t)=0,\qquad
x_k(t)=k+1\ \ (k\notin\{i,j\}),\qquad p_k(t)=x_k(t)a.
\tag{3}
\]
All stationary values other than \(x_j\) are distinct and at least 2. The only pair of vertices that can coincide along this path is \(i,j\), and that pair is not an edge of \(H\). Thus no \(H\)-edge collapses. Observation B shows that \(P(0)\) and \(P(1/4)\) belong to the same \(H\)-stratum.

For \(G\), the edge \(e\) is collapsed at \(P(0)\) and noncollapsed at \(P(1/4)\). Observation A shows that these two \(G\)-fibers are inequivalent, so the two configurations belong to different \(G\)-strata.

The two partitions therefore assign this pair of points differently and cannot be equal. This proves the contrapositive and completes the proof. \(\square\)

The proof uses a collinear path **inside the full configuration space to distinguish full partitions**. It does not replace the target by a classification restricted to collinear configurations or to a codimension-one locus.

## 4. Source scope and the unresolved interpretation issue

The relevant source is O. Karpenkov, *Open Problems on Configuration Spaces of Tensegrities*, Arnold Mathematical Journal **4** (2018), 19–25, [DOI 10.1007/s40598-018-0080-7](https://doi.org/10.1007/s40598-018-0080-7). Definitions 1.1–1.3 on p.20 specify positive ambient dimension, labeled vertices, the full Cartesian base, and coordinate-sign-preserving homeomorphisms. Examples 1.4–1.5 on p.21 explicitly retain collisions. Problem 5's example on p.22 again retains a collapsed edge. Problem 4 on p.22 asks: “Which subgraphs of K_n define the same stratifications?”

The source does **not** give a separate equivalence relation between stratifications of different graphs. Section 2 also discusses dimensions and adjacency, so its context leaves open whether an abstract combinatorial comparison was intended. The theorem above supplies a complete answer for literal equality of the defined partitions; it must not be advertised as resolving every possible intended meaning of Problem 4.

Distinguish these alternatives:

- **Literal equality of full fixed-label partitions:** proved above.
- **Equality after a specified permutation of vertex labels:** reduce to the theorem after relabeling. Direct substitution in the equilibrium equations shows that a vertex permutation carries \(\mathcal S_d(G)\) to \(\mathcal S_d(\sigma G)\). Thus such equality holds exactly when \(\sigma G=H\).
- **An arbitrary ambient homeomorphism or an abstract adjacency-poset isomorphism:** no classification is claimed here.
- **Only generic configurations, only noncollapsed edges, only some strata, or only codimension-one loci:** these change the comparison. The collision witness does not establish their classification.

The source's observation that some individual strata coincide is consistent with the theorem: equality of some pieces does not imply equality of the entire partitions. No external interpretation has been obtained from the author.

## 5. Relation to earlier literature and novelty limits

Doray, Karpenkov and Schepers introduced the sign-preserving equivalence and proved semialgebraicity: *Geometry of configuration spaces of tensegrities*, Discrete & Computational Geometry **43** (2010), 436–466, [DOI 10.1007/s00454-009-9229-4](https://doi.org/10.1007/s00454-009-9229-4), [author preprint](https://arxiv.org/abs/0806.4976). Its Definitions 2.1–2.6 and Theorem 2.8 establish the foundational setting. The present proof needs neither semialgebraic triviality nor a classification of those strata.

Observation A is already Panina's Lemma 4; no novelty is claimed for that criterion, the sign-set formulation, or the equivalence reduction. The argument specific to this note combines the known collision criterion with the explicit collinear transport to compare full fixed-label partitions.

Panina's *A universality theorem for stressable graphs in the plane*, Ars Mathematica Contemporanea **18** (2020), 137–148, [DOI 10.26493/1855-3974.641.e06](https://doi.org/10.26493/1855-3974.641.e06), [preprint v4](https://arxiv.org/abs/1902.07212v4), proves equivalence of stress-sign-set equality and sign-preserving homeomorphism in her setting. Her framework convention excludes collapsed graph edges and her realization spaces use an affine quotient. Neither that convention nor that quotient replaces Karpenkov's full base in the theorem here. The proof above constructs its homeomorphisms directly rather than claiming the oriented-matroid reduction as new.

A bounded primary-source search on 8 October 2026 located no prior full-graph classification under the exact equality convention above. That is not a guarantee of novelty or a certification of the author's intended open problem. Later generic-tensegrity, bounded-valence, and semi-discrete-framework results located in that search do not by their stated scopes classify these full labeled partitions.

### Source arithmetic note

The numerical fiber-dimension statement for exactly two coincident vertices of \(K_3\) in Karpenkov Example 1.4 (journal p.21) and Doray--Karpenkov--Schepers Example 2.7 (preprint p.5) is inconsistent with their displayed equilibrium equations: each states dimension 2, whereas the dimension is 1. For \(p_1=p_2=0\) and \(p_3=a\neq0\), equilibrium at vertices 1 and 2 forces \(w_{13}=w_{23}=0\), leaving only \(w_{12}\) free. This narrow arithmetic discrepancy does not change the cited full-space definitions, the explicit allowance of collisions, or the proof here; no conclusion about other results in those papers is drawn.

## 6. Reproducible checks and their limits

`check_collision_witness.py` is a standard-library, exact-rational checker. It checks the explicit matrix identity behind (2), positivity and invertibility of the diagonal map, the singleton-support witness, every distinct graph pair through four vertices, and selected denser and disconnected examples. Guards use explicit exceptions, not Python assertions, so they remain active under `-O` and `-OO`.

These finite checks are regression evidence for the formulas, not a substitute for the universal proof. They do not resolve the source-interpretation issue, establish publication novelty, or constitute independent review. The delivered independent audit is `AUDIT.md`. Fresh exact execution details, complete output references, and source metadata are recorded in `CHECK_RUNS.json`, `SOURCE_MANIFEST.json`, and `SOURCE_AUDIT.json`. The finite checks do not constitute a formal proof-assistant verification.
