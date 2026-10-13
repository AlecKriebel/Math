# Path-cost arborescence optimization is strongly NP-hard

**30003997 / OWR-16633-014. Complete proof candidate; independent review pending.** One reduction family. The proof uses destination-dependent costs in \(\{0,1\}\) on a four-layer directed acyclic graph. It also gives a strictly positive \(\{1,2\}\)-cost version. Historical priority is not established; no novelty claim is made.

## 1. Exact source and computational formulation

Volker Kaibel's *Arborescences and NP-hardness*, OWR50/2018, printed pp.3014–3015, distinguishes two questions. Problem2 on p.3015 is the present target: given a directed graph \(D=(V,A)\), a fixed root \(r\), and an arc-cost vector \(c^v\) for each \(v\ne r\), minimize
\[
 C(T)=\sum_{v\ne r}c^v(P_T^v)
 =\sum_{v\ne r}\sum_{e\in P_T^v}c^v_e, \tag{1}
\]
where \(T\) is a spanning out-arborescence rooted at \(r\), and \(P_T^v\) is its unique directed \(r\)-to-\(v\) path. The source allows real vectors. We use only integer entries0 and1, so there is no issue of encoding arbitrary real numbers.

For the decision version, the vectors and threshold are rational numbers encoded in binary, and the question is whether a feasible \(T\) has cost at most the threshold. A proposed arborescence and all its root paths can be checked and costed in polynomial time. Thus this rational decision problem is in NP.

**Theorem.** Deciding whether (1) has value zero is NP-complete even when:
- \(D\) is a simple directed acyclic graph with four layers;
- every arc goes from one layer to the next;
- every vertex is reachable from \(r\), so feasible arborescences always exist;
- every arc cost in every destination vector belongs to \(\{0,1\}\);
- every nonroot vertex has indegree at most three.

In particular the optimization problem is strongly NP-hard. It remains strongly NP-hard with all costs in \(\{1,2\}\), using a polynomially specified positive threshold.

## 2. Reduction from 3SAT

Use the classical NP-complete problem of satisfiability of a CNF formula with at most three literals per clause. Delete tautological clauses and repeated occurrences of the same literal. Each remaining clause is nonempty and contains distinct variables, with one sign per variable. This preprocessing preserves satisfiability. Trivial constant inputs can be mapped to fixed yes/no instances; they play no role in the hardness argument.

Let the variables be \(x_1,\ldots,x_n\), and the remaining clauses be \(C_1,\ldots,C_m\). Construct the following vertices:
\[
 V=\{r\}\cup\{t_i,f_i:1\le i\le n\}
       \cup\{v_i:1\le i\le n\}
       \cup\{z_j:1\le j\le m\}.
\]
The four displayed sets are layers0,1,2,3. Include exactly the arcs
\[
 r\to t_i,\quad r\to f_i,\quad
 t_i\to v_i,\quad f_i\to v_i
 \qquad(1\le i\le n), \tag{2}
\]
and
\[
 v_i\to z_j
 \quad\text{whenever }x_i\text{ or }\neg x_i\text{ occurs in }C_j. \tag{3}
\]
There are \(1+3n+m\) vertices and at most \(4n+3m\) arcs. The graph is simple and acyclic, and every vertex is reachable from \(r\).

For every destination \(t_i,f_i,v_i\), let its cost vector be identically zero. For a clause destination \(z_j\), set
\[
 c^{z_j}_{r\to t_i}=
 \begin{cases}1,&\neg x_i\in C_j,\\0,&\text{otherwise},\end{cases}
 \qquad
 c^{z_j}_{r\to f_i}=
 \begin{cases}1,&x_i\in C_j,\\0,&\text{otherwise}.\end{cases} \tag{4}
\]
Set every other entry of \(c^{z_j}\) to zero. All entries are binary. Even if the input format requires the full dense cost table, it has polynomial size.

## 3. All feasible trees and their costs

In every spanning out-arborescence:
1. Both \(r\to t_i\) and \(r\to f_i\) are present, since they are the only incoming arcs of their heads.
2. Exactly one of \(t_i\to v_i\) and \(f_i\to v_i\) is present.
3. Exactly one incoming arc \(v_i\to z_j\) is present for each clause vertex.

Conversely, any choices of the arcs in items2–3, together with the forced arcs in item1, form an arborescence. Every nonroot vertex has one incoming arc, and the layer order ensures both acyclicity and a path from \(r\).

Thus every feasible tree determines a truth assignment \(\sigma_T\):
\[
 \sigma_T(x_i)=
 \begin{cases}
 \text{true},&t_i\to v_i\in T,\\
 \text{false},&f_i\to v_i\in T.
 \end{cases} \tag{5}
\]
If \(v_i\to z_j\) is the chosen incoming arc of \(z_j\), its root path is exactly one of
\[
 r\to t_i\to v_i\to z_j,\qquad
 r\to f_i\to v_i\to z_j.
\]
By (4), its path cost is zero precisely when the literal of \(x_i\) in \(C_j\) is true under \(\sigma_T\); otherwise it is one. The paths to all non-clause vertices contribute zero. Therefore
\[
 C(T)=
 \#\{\text{clauses whose selected literal is false under }\sigma_T\}. \tag{6}
\]

If the formula is satisfiable, choose the variable parents according to a satisfying assignment and choose a true literal as parent for every clause. The resulting tree has cost zero.

Conversely, if a tree has cost zero, every clause has a selected literal that is true under the one globally consistent assignment in (5). Thus the formula is satisfiable. This is a polynomial many-one reduction with threshold zero.

A slightly stronger identity follows. For a fixed assignment, each clause can choose its parent independently. A satisfied clause can achieve cost zero; an unsatisfied clause must pay one. Hence
\[
 \min_T C(T)=\min_\sigma
 \#\{\text{clauses unsatisfied by }\sigma\}. \tag{7}
\]
The reduction proves the theorem. \(\square\)

## 4. Strictly positive costs without changing the choice of optimum

Add one to every entry of every destination cost vector. In this layered graph every path to a layer1 vertex has length1, every path to a variable vertex has length2, and every path to a clause vertex has length3. Thus for every feasible tree the objective increases by exactly
\[
 2n+2n+3m=4n+3m. \tag{8}
\]
The new costs lie in \(\{1,2\}\), and the formula is satisfiable exactly when the new optimum is at most \(4n+3m\). The graph and numerical values remain polynomially bounded. In particular the hardness does not depend on negative arc costs, long paths, cycles, or feasibility obstructions.

## 5. Scope, related targets and validation

This is not the ordinary minimum-arborescence problem with one common arc-cost vector. In (1), traversing the same early arc can be charged differently for different destinations. The variable parent shared by multiple clause paths is exactly the consistency mechanism that couples these choices.

The source motivates Problem2 via integer optimization over Wong's extended formulation. The proof addresses the graph optimization formulation as written; it does not rely on an unproved translation to a specific polyhedral encoding. Standard polynomial algorithms for ordinary minimum spanning trees or fixed common-cost shortest-path trees do not optimize the destination-dependent objective (1).

The adjacent record30003996 is the distinct all-roots undirected-tree question, source Problem1, motivated by Martin's formulation. Its research and this proof use the same general assignment/literal-selection mechanism; they should not be described as two unrelated conceptual discoveries. No equivalence of the two optimization models is claimed here. Record30003998 is a literal duplicate of the present source Problem2 and must not receive a separate proof budget or PR.

The classical input theorem is 3SAT's NP-completeness, credited to the standard Cook–Karp reduction framework. A bounded search of the exact source, title and destination-dependent path-cost terminology did not identify a prior proof of this precise restricted statement. That does not establish historical novelty.

The verifier builds the explicit graph and cost vectors, enumerates parent choices for small instances, evaluates every path using those costs, and compares the resulting optimum to exhaustive truth assignments. It also checks the positive-cost offset and the promised graph restrictions. These finite tests support the gadget; the proof of polynomial reduction and correctness for arbitrary formula size is given above.
