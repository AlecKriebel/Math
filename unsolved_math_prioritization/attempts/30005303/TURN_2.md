# Turn 2: closure of the binary MTP2 edge-factorizing model

**Target:** 30005303 / OWR-11695865-001.  
**Date:** 2026-10-02. **Substantive author count:** 2/5.  
**Status:** Complete candidate for the remaining closure question, awaiting independent adversarial review. Together with the frozen TURN_1 counterexample, this answers both questions in the exact source: Conjecture 1 is true and Conjecture 2 is false. No historical novelty claim.

## 1. Definitions and theorem

For a finite simple undirected graph G=(V,E), let F(G) be the probability mass functions on {0,1}^V admitting a nonnegative unary-and-edge factorization

\[
p(x)=Z^{-1}\prod_{i\in V}\phi_i(x_i)\prod_{ij\in E}\psi_{ij}(x_i,x_j),
\qquad 0<Z<\infty.
\tag{1}
\]

Zeros in the factors are allowed. Real-valued source factors cause no difficulty: their absolute values have the same product whenever the original product is a nonnegative mass function. Let F_2(G) consist of the MTP2 elements of F(G). Let A(G) be the strictly positive ferromagnetic binary models

\[
p(x)=Z^{-1}\exp\!\left(\sum_i h_i x_i+\sum_{ij\in E}J_{ij}x_ix_j\right),
\qquad h_i\in\mathbb R,\quad J_{ij}\ge0.
\tag{2}
\]

**Theorem.** For every finite G,

\[
F_2(G)=\overline{A(G)}.
\tag{3}
\]

In particular F_2(G) is closed. The same closure conclusion holds for the literal edge-only convention in the source, including isolated vertices; this is checked in §6 rather than assumed.

The proof has two parts: a support reduction proves F_2(G)⊆closure A(G), and a bounded factor reparameterization proves closure A(G)⊆F_2(G). Compactness of unconstrained factorizing models is **not** assumed.

## 2. Support reduction to a finite partially ordered set

Fix p∈F_2(G), and let S={x:p(x)>0}. It is nonempty and closed under coordinatewise meet and join. Write

\[
m=\bigwedge_{x\in S}x,\qquad M=\bigvee_{x\in S}x.
\]

Both belong to S. Coordinates with m_i=M_i are fixed. On the active coordinates I={i:m_i=0,M_i=1}, the restrictions of m and M are the all-zero and all-one vectors.

For a coordinate set B, let S_B be the projection of S onto B. Factorization (1) gives the exact support identity

\[
S=\{x:x_i\in S_i\ (i\in V),\ (x_i,x_j)\in S_{ij}\ (ij\in E)\}.
\tag{4}
\]

One direction is immediate. Conversely, every locally projected pattern in (4) occurs in an atom where p is positive, so its corresponding original factor is positive; thus every factor at x is positive and x∈S.

Projection preserves the sublattice property. For an edge between active coordinates, S_ij contains 00 and 11 and hence is exactly one of

\[
\{00,11\},\quad\{00,01,11\},\quad
\{00,10,11\},\quad\{00,01,10,11\}.
\tag{5}
\]

These impose equality, one directed inequality, or no restriction. For each missing pattern 10, impose x_i≤x_j; for each missing pattern 01, impose x_j≤x_i. Add all such directed arcs on I. Collapse their strongly connected components. Inside each component all coordinates are equal. The resulting components form a finite partially ordered set P under directed reachability. Write y_A for the common coordinate in component A, with order convention A≤B meaning y_A≤y_B.

Equation (4) now says exactly that S is the set of fixed coordinates together with the increasing {0,1}-valued maps on P. Equivalently, {A:y_A=1} ranges over all upper sets of P. There are no additional constraints: edges meeting a fixed coordinate merely enforce that fixed value, and (5) lists all active-edge restrictions.

The case I empty gives a single atom and is included below with no active terms.

## 3. On that support, only nonnegative interactions are needed

The logarithms of all factors in (1) are finite on their projected support. Sum those logarithms, including the normalizing constant, to express log p on S. Each term can be reduced on the coordinates y_A as follows.

- A term involving only fixed coordinates is constant.
- A unary term, a fixed-active edge term, or an edge within one equality component is constant plus a unary term.
- If an edge joins comparable components A<B, its allowed patterns are 00,01,11. Every real function f on these three patterns is affine there: set c=f(00), b=f(01)−f(00), a=f(11)−f(01), and use c+a y_A+b y_B. Reverse the roles if B<A.
- If an edge joins incomparable components A,B, all four patterns occur. Expand its log factor uniquely as c+a y_A+b y_B+J y_Ay_B.

After summing and combining terms belonging to the same pair of components, obtain

\[
\log p(x)=c+\sum_{A\in P}h_Ay_A+
\sum_{\{A,B\}\text{ incomparable}}K_{AB}y_Ay_B
\quad(x\in S).
\tag{6}
\]

Here K_AB=0 unless at least one original edge joins A to B. Individual original edge coefficients need not be nonnegative; aggregation across equality components is essential.

**Claim:** every K_AB≥0. Fix incomparable A,B. The set

\[
U=(\{D:A<D\}\cup\{D:B<D\})
\]

is an upper set containing neither A nor B. So U, U∪{A}, U∪{B}, U∪{A,B} are four upper sets, hence four support atoms by §2. Their meet/join form a square. Applying MTP2, taking logarithms, and substituting (6), every term cancels except the mixed coefficient K_AB. Thus K_AB≥0.

Choose one original vertex in each component to carry h_A. For each nonzero K_AB choose one original edge joining those components to carry that coefficient. Define the resulting quadratic polynomial L(x) on the entire original Boolean cube. All its edge interaction coefficients are nonnegative, and on S it equals log p(x)−c.

Finally define the nonnegative integer-valued violation count

\[
D(x)=\sum_{i\text{ fixed}}\mathbf1\{x_i\ne m_i\}
+\sum_{i\to j}\!x_i(1-x_j),
\tag{7}
\]

where the second sum contains each directed active-edge implication from §2. Equality contributes both directions. By (4), D(x)=0 exactly on S. For t>0 set

\[
p_t(x)=\frac{\exp(L(x)-tD(x))}
{\sum_z\exp(L(z)-tD(z))}.
\tag{8}
\]

This is strictly positive. Each penalty −t x_i(1−x_j)=−t x_i+t x_ix_j adds a **nonnegative** coupling on an original edge; each fixed-coordinate penalty is unary. Consequently p_t∈A(G). On S the unnormalized weight is e^(−c)p(x), and off S it tends to zero. Since the state space is finite, p_t→p pointwise. This proves

\[
F_2(G)\subseteq\overline{A(G)}.
\tag{9}
\]

## 4. A bounded factor representation for every positive model

We prove that every q∈A(G) has a factor representation by finitely many numbers in [0,1], with its unnormalized weights summing to at least 1. This prevents normalization from degenerating in a limit.

Let the negative log weight in (2) be

\[
E(x)=-\sum_i h_ix_i-\sum_{ij\in E}J_{ij}x_ix_j.
\]

Orient each edge arbitrarily, say i→j. Since

\[
-J_{ij}x_ix_j=J_{ij}x_i(1-x_j)-J_{ij}x_i,
\]

we may write

\[
E(x)=\sum_{i\to j}J_{ij}x_i(1-x_j)+\sum_i b_ix_i.
\tag{10}
\]

Construct a finite capacitated directed network on {s,t}∪V. For each oriented edge i→j put capacity J_ij. If b_i≥0 put capacity b_i on i→t; if b_i<0 put capacity −b_i on s→i. All other capacities are zero. For a configuration x, take the cut whose source side is {s}∪{i:x_i=1}. Its capacity C(x) satisfies

\[
C(x)=E(x)+\kappa,\qquad
\kappa=\sum_{i:b_i<0}(-b_i).
\tag{11}
\]

Let f be a maximum flow, of value v. Define combined residual capacities

\[
r_{uv}=c_{uv}-f_{uv}+f_{vu}\ge0.
\]

Here 0≤f_uv≤c_uv and flow conservation holds at every nonterminal vertex. For every source/sink cut, summing conservation on its source side gives net flow across the cut equal to v. Thus

\[
\sum_{u\in S_x,v\notin S_x}r_{uv}=C(x)-v.
\tag{12}
\]

For completeness, such a flow exists because the bounded feasible flow polytope is compact. Its residual network has no positive-capacity s-to-t path, since augmenting on such a path would increase its value. The vertices reachable from s therefore form a cut with zero residual capacity. Equation (12) shows that this is a minimum cut and v=min_x C(x). No algorithmic termination claim for arbitrary real capacities is required.

Combining (11)–(12),

\[
E(x)-\min_zE(z)=\sum_{u\in S_x,v\notin S_x}r_{uv}.
\tag{13}
\]

Residual nonterminal arcs only connect endpoints of original edges. Residual arcs into s or out of t never cross a source/sink cut and can be ignored. Put

\[
a_i=e^{-r_{si}},\quad b'_i=e^{-r_{it}},\quad
c_{ij}=e^{-r_{ij}}\quad(ij\in E\text{ oriented both ways}).
\]

All these numbers belong to (0,1]. Equation (13) yields

\[
W(x):=e^{-E(x)+\min E}
=\prod_i a_i^{1-x_i}(b'_i)^{x_i}
 \prod_{ij\in E}c_{ij}^{x_i(1-x_j)}c_{ji}^{x_j(1-x_i)}.
\tag{14}
\]

Every local factor is at most 1, and at any minimum-energy configuration every factor in (14) equals 1. In particular

\[
1\le\sum_xW(x)\le2^{|V|},\qquad
q(x)=\frac{W(x)}{\sum_zW(z)}.
\tag{15}
\]

This is the required bounded representation. The underlying graph-cut and residual reparameterization mechanism is classical; §7 gives attribution. The details are provided to make the compactness deduction checkable.

## 5. Taking limits without losing factorization

Let q_n∈A(G) converge pointwise to q. Use (14) for each q_n. There are only 2|V|+2|E| scalar parameters in a fixed compact cube [0,1]^(2|V|+2|E|). Pass to a subsequence along which all parameters converge. Formula (14), interpreted as selecting a factor 1 or its parameter rather than taking an ambiguous 0^0, is polynomial and hence continuous in these parameters for each x. Thus W_n(x)→W(x) for every x. By (15), its limiting sum Z lies in [1,2^|V|]. It follows that q=W/Z still has unary-and-edge factorization.

The MTP2 inequalities are polynomial inequalities in the finitely many probabilities, so they persist in the pointwise limit. Each q_n is MTP2 because log q_n is a sum of modular unary functions and nonnegative multiples of x_ix_j, which are supermodular. Hence q∈F_2(G). Together with (9), this proves (3) and closure.

Equivalently, for a direct sequence p_n∈F_2(G), use (8) to select positive q_n∈A(G) with max_x|q_n(x)−p_n(x)|≤1/n and apply the preceding argument to any pointwise limit of p_n. This avoids any implicit assumption that a limiting distribution is strictly positive.

Every nonnegative edge-factorizing mass function is globally Markov. Indeed, after fixing a positive-probability conditioning assignment x_C, the product separates over the connected components of G\C; its finite normalizing sum separates as well. Components carrying separated A and B are therefore conditionally independent. Null conditioning assignments impose no condition. Thus the closure just proved is precisely the source's intersection with M_2, rather than an unrelated class lacking its Markov condition.

## 6. Literal edge-only factors and isolated vertices

If G has no isolated vertices, every unary factor and the positive normalization constant can be absorbed into incident edge factors, so F(G) is exactly the source's edge-factorizing class.

More generally let I_0 be the isolated vertices and H the subgraph on the other vertices. A mass function given literally by a product over E cannot depend on x_I0. Therefore it has the form

\[
p(x)=2^{-|I_0|}p_H(x_H).
\]

If E is nonempty, the factor 2^(-|I_0|) and all nonisolated unaries can be absorbed into edge factors. The source class is consequently the product of its model on H with the fixed uniform distribution on I_0. MTP2 is equivalent to MTP2 of p_H, and closure follows from the theorem for H. The same conclusion holds if one instead follows the conventional Ising definition allowing arbitrary unary factors at isolated vertices, because the theorem already covers those.

Under the strictly literal empty-product formula, an edgeless nonempty graph admits no normalized edge-only mass function (its empty product is identically 1); that empty class is closed. If V is empty, the one-state probability model is closed. If the source tacitly includes a scalar normalizer for an edgeless graph, its edge-only model is the singleton uniform distribution, again closed. Thus no convention on this harmless boundary changes the affirmative answer.

## 7. Attribution, controls and final scope

The source question is [Lauritzen, OWR55/2022, printed p.3125](https://ems.press/content/serial-article-files/46992). Its MTP2 inequalities, zero-permitting factorization definition, and global Markov scope were checked directly. TURN_1 settles its other requested question negatively by an eight-atom four-cycle example.

The graph-cut representation of attractive binary energies and flow reparameterization are established tools, not claimed discoveries of this packet. See Kolmogorov and Rother, *Minimizing nonsubmodular functions with graph cuts—a review*, IEEE TPAMI29 (2007), [author-hosted paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2007/01/PAMI07-QPBO.pdf), and the finite max-flow/min-cut theorem proved directly in §4 for the particular need here. The proposed contribution is the support/equality-block reduction together with the nondegenerate compactness deduction for the exact source closure question. No priority claim is inferred from a bounded literature search.

`checks/verify_turn2.py` checks finite examples of the support representation, comparable-component reductions, aggregated coupling signs, lifted penalties, and residual-cut identities using exact integer arithmetic. The proof above, rather than the finite range of those tests, supplies the all-graph quantifiers.

**Original full-target conclusion, conditional on independent review:** Conjecture 1 holds for every finite binary graph; Conjecture 2 fails even for C4; the companion lattice-support Conjecture 3 also fails. Both bundled questions have complete candidate answers after 2 substantive author turns. The author search is frozen for adversarial review; no extra turns are used to extend the scope.
