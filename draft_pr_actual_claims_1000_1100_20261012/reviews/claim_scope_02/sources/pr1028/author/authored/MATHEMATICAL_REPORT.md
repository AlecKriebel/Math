# Greedy spanning-tree decomposition: partial results and unresolved general case

## Disposition

The general problem 30001934 / OWR-11451-007 is **unresolved by this work**. Five distinct substantive routes were used. No graph/integral point for which every spanning tree has a nonintegral maximal coefficient was found. This report proves the exact coefficient formula, a low-dilation theorem, the property for all connected graphs with at most four vertices, and the property for the complete graph K5. It also gives exact counterexamples to two tempting selection rules. None is a resolution of the all-graph question or of the other clauses in aggregate 30001932. No novelty claim is made for the partial results.

## 1. Statement and source interface

The source is Dion Gijswijt's contribution with Guus Regts, Question 3, OWR53/2011, printed p.3027, context pp.3025–3028: https://ems.press/content/serial-article-files/46369 . Work with a finite connected undirected graph G=(V,E), n=|V|>=1, and

P(G)=conv{1_T : T a spanning tree of G}.

Parallel edges are separate coordinates; loops belong to no spanning tree. For k a positive integer and integral w in kP(G), define

L(w,T)=max{lambda in [0,k] : w-lambda 1_T in (k-lambda)P(G)}.

Here 0P={0}. The question is whether some spanning tree T has L(w,T) integral. This formulation preserves the printed allowance of lambda=0: an integer maximum of zero counts. We do not silently replace it by a positive maximum. When w/k lies in the relative interior of P, every tree has positive feasible coefficient, so any integral maximum furnished by our results is then positive.

The source omits the upper bound lambda<=k. Our bound makes explicit the intended nonnegative remaining mass. Interpreting (k-lambda)P literally for negative scalars instead gives an unbounded feasible set when P is a singleton and w=k1_T, and would not express the intended decomposition problem. That omission is a model repair, not a mathematical counterexample to the intended question.

The n=1 case has the empty spanning tree, P={0}, and L=k. A disconnected graph has no spanning trees and supplies no input w; it is not replaced by its spanning-forest polytope.

The integer decomposition and integer Caratheodory properties are already known for matroid base polytopes. Gijswijt–Regts, JCTB102(2012),62–70, https://www.math.ucdavis.edu/~deloera/TEACHING/READINGSEMINAR/PAPERS/gijswijt%2Bregts.pdf , supplies those weaker facts. They do not directly control the maximal coefficient. Chaourar's fixed-basis greedy-pair condition has different quantifiers; see the separate readiness record. Neither minimum/maximum-weight spanning-tree optimization nor greedy tree-packing convergence answers the question.

## 2. Exact coefficient formula

For S subset V let E(S) contain all edges whose two endpoints lie in S, including loops. For nonempty proper S put

r_S=|S|-1,  d_T(S)=r_S-|T intersect E(S)|,
s_w(S)=k r_S-w(E(S)).

Then d_T(S)>=0, s_w(S)>=0, and

L(w,T)=min( {k} union {w_e:e in T} union {s_w(S)/d_T(S): nonempty proper S, d_T(S)>0} ).       (1)

All quantities on the right are exact rational numbers. In particular an individual fractional tree coefficient is not a counterexample: every tree must have a fractional maximum.

Proof. The spanning-tree polytope is described by z>=0, z(E)=n-1, and z(E(S))<=|S|-1 for nonempty proper S, with loops zero. For a nonnegative mass q its dilation is described by z>=0, z(E)=q(n-1), z(E(S))<=q(|S|-1), with loops zero; at q=0 the total equality and nonnegativity force z=0. Substituting z=w-lambda1_T and q=k-lambda gives the coordinate upper bounds lambda<=w_e for e in T, and

lambda d_T(S)<=s_w(S).

When d_T(S)=0 the inequality is automatic. Total mass is automatic because |T|=n-1. Include 0<=lambda<=k. This finite family describes exactly a closed interval starting at zero, and its endpoint is (1). This also proves feasibility at the minimum and impossibility beyond it.

For completeness, the standard polytope description can be reduced to the graphic matroid rank inequalities without an extra assumption. If F subset E has vertex components C_i, nonnegativity and the E(C_i) inequalities give z(F)<=sum_i(|C_i|-1)=rank(F). Conversely the rank inequalities imply the displayed induced-subgraph inequalities. The usual greedy support-function proof identifies the nonnegative rank-inequality polytope with the forest polytope: sort nonnegative edge weights, apply each prefix rank bound, and attain them simultaneously with a greedy forest. Its total-rank face is exactly the convex hull of spanning trees. Loops and parallel edges cause no change.

## 3. Low-dilation theorem

**Theorem A.** Let P be any nonempty 0–1 polytope with the integer decomposition property. For k=1,2,3,4 and integral w in kP, some integral x in P has a positive integral maximal coefficient under the nonnegative-mass convention. Consequently every spanning-tree polytope satisfies the question for k<=4.

Proof. Every integral point of a 0–1 polytope is a 0–1 vertex. Indeed, in any convex representation of an integral point, each coordinate equal to zero or one forces that same coordinate in every positively weighted vertex.

Take an integer decomposition w=x_1+...+x_k. If some coordinate w_e=1, choose a summand with x_e=1. Subtracting that summand once is feasible, whereas nonnegativity forces lambda<=1. Its maximum is 1. If w_e=k-1, choose a summand with x_e=0. The residual e-coordinate equals k-1; every point of (k-lambda)P has this coordinate at most k-lambda. Hence lambda<=1, and again equality is feasible.

For k<=3, either one of those two cases occurs, or all coordinates are zero or k. In the latter case all summands coincide with x=w/k and L=k.

For k=4, after excluding coordinates 1 and 3, all coordinates of w are in {0,2,4}. Thus v=w/2 is an integral point of 2P. Write v=x+y by integer decomposition. The coefficient 2 is feasible for x. If x=y then L=4. Otherwise choose a coordinate in which x and y differ. If x_e=1,y_e=0, nonnegativity forces lambda<=w_e=2. If x_e=0,y_e=1, the coordinate upper bound gives 2<=4-lambda, again lambda<=2. Thus L=2. This proof includes k=1 and singleton polytopes. QED.

A related immediate certificate is useful in searches: a nonconstant integral valid inequality a.x<=b with slack kb-a.w=1 yields a tree with L=1. In an integer decomposition, the nonnegative integral deficits b-a.x_i sum to 1; the unique positive deficit equals 1, and selecting that summand gives the bound lambda<=1. This does not prove the general case when all relevant slacks are larger.

## 4. At most four vertices and complete graph K5

**Theorem B.** Every finite connected undirected multigraph with at most four vertices has the requested property.

Proof first for simple graphs. For n<=3, any tree T and every nonempty proper S have d_T(S)<=1, so (1) is a minimum of integers. On four vertices, if G has a Hamiltonian path T, then every three-vertex induced subgraph T[S] contains an edge. Thus again d_T(S)<=1 for every proper nonempty S. If G has no Hamiltonian path, take any spanning tree. It must be a three-leaf star; any additional edge between its leaves creates a Hamiltonian path. Therefore G is that star, P is a singleton, and L=k.

For parallel edges, project to the simple underlying graph by summing weights within each parallel class. This sends the tree polytope onto the simple tree polytope. Choose a simple tree whose projected maximum is an integer, and choose one representative edge of each selected class. For the lifted tree, (1) shows that its maximum is the minimum of that projected maximum and the individual weights of its selected representative edges: all induced-subgraph sums and tree counts are unchanged, and the only additional restrictions are individual coordinate nonnegativity. This is a minimum of integers. Loops are fixed zero. QED.

The same parallel-extension argument applies to any graph already known to have the property.

**Theorem C.** The spanning-tree polytope of K5 admits greedy decomposition in the exact sense of the question, for every positive integer k and integral w in kP(K5). The result extends to graphs obtained from K5 by replacing its edges with nonempty parallel classes and adding loops.

Proof. We have w(E)=4k. For each of the ten three-vertex sets S, let

c(S)=min{w_e:e crosses between S and V\S}.

Each such cut has six edges. Every edge lies inside exactly three of the ten sets S and crosses exactly six of their cuts. Therefore

sum_{|S|=3} w(E(S))=3w(E)=12k,
sum_{|S|=3} c(S)<= (1/6) sum_{|S|=3} w(delta(S))=w(E)=4k.

It follows that

sum_{|S|=3} [w(E(S))+2c(S)]<=20k.

Hence some S has w(E(S))+2c(S)<=2k. Choose a crossing edge e attaining c(S). There is a Hamiltonian path T alternating between the three vertices of S and the two vertices of its complement, and containing e. Explicitly, relabel e=a_1b_1, S={a_1,a_2,a_3}, V\S={b_1,b_2}, and take the path a_1,b_1,a_2,b_2,a_3.

For this five-vertex path, d_T(U)<=1 for all proper nonempty U other than S. For |U|<=2 this is immediate; among three-vertex sets only the alternating set S is independent in T; for |U|=4, deleting one vertex from the path leaves at least two edges. Thus the only potentially noninteger bound in (1) is

s_w(S)/d_T(S)=(2k-w(E(S)))/2 >= c(S).

The edge e in T already gives the integer bound lambda<=w_e=c(S). All other bounds in (1) are integers, so the potentially noninteger bound cannot lower their minimum. Hence L(w,T) is an integer. Zero-valued coordinates are allowed and may give L=0, exactly as permitted in the printed question. The parallel-extension conclusion follows from Theorem B's projection argument. QED.

This proof uses completeness to build the alternating path through any chosen crossing edge. Adding zero weights to embed an arbitrary five-vertex graph in K5 does not establish the property for that graph, since the selected path could use a missing edge. Nor does a Hamiltonian path in K6 have only one subset denominator exceeding one. These are genuine boundaries of the proof, not omitted steps of an all-graph theorem.

## 5. Exact obstructions to proposed selection rules

List edges lexicographically.

1. On K4 with k=6 and all six weights equal to 3, the star at vertex 0 has L=3/2. Its leaf set has slack 3 and denominator 2. A Hamiltonian path has L=3. Thus neither one fractional tree nor the minimum over tree coefficients disproves the question, and an arbitrary tied ordinary greedy spanning tree need not work.

2. On K5 with k=10 and weights

(3,6,5,5,4,5,4,2,3,3)

on (01,02,03,04,12,13,14,23,24,34), exhaustive exact evaluation of all 125 spanning trees gives largest coefficient 9/2. Nevertheless 105 trees have an integer maximum. Thus the strategy of maximizing L globally does not force an integer optimum. The input's membership, every tree's coefficient, and each maximum endpoint are independently checked by the finite test suite. This example is a counterexample to the selection-rule conjecture only.

3. On K4, take k=20 and weights (11,13,11,8,8,9) on (01,02,03,12,13,23). The unique maximum-total-weight tree is the star (01,02,03), with total tree weight 35 and L=15/2. Its leaf triangle has weight 25, slack 40-25=15 and denominator 2; all other bounds are no smaller. A path is available with an integral maximum. Thus even a unique maximum-weight spanning tree can fail the requested coefficient test.

## 6. What remains

An all-graph proof must select a tree controlling all non-coordinate subset bounds simultaneously. A counterexample must certify w in kP and a nonintegral exact maximum for every spanning tree, including trees on the boundary with possible maximum zero. The tests below search finite regimes and reject tempting shortcuts; they do not bridge this remaining gap.
