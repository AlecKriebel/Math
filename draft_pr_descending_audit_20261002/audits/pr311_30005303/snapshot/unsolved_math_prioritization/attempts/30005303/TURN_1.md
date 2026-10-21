# Turn 1: a binary MTP2 counterexample to Markov factorization

**Target:** 30005303 / OWR-11695865-001.  
**Date:** 2026-10-02. **Substantive author count:** 1/5.  
**Status:** Complete counterexample candidate to the second half of the bundled target; the first half remains open in this packet. No historical novelty claim.

## 1. Exact scope

The source is Steffen Lauritzen, *Two open problems in graphical models of algebraic nature*, Oberwolfach Report 55/2022, printed pp. 3125–3126, [official report](https://ems.press/content/serial-article-files/46992), DOI 10.4171/OWR/2022/55. Its state space is binary, the graph is finite, simple and undirected, and its Markov condition is the **global** separation property. Zeros in the mass function are allowed. Clique factorization uses finite real-valued functions; taking absolute values gives an equivalent nonnegative factorization for a nonnegative mass function.

The imported target bundles:

1. Is the intersection of edge-factorizing distributions and MTP2 Markov distributions closed under pointwise limits? (Source Conjecture 1.)
2. Does every MTP2 globally Markov distribution admit clique factorization? (Source Conjecture 2.)

The construction below answers question 2 negatively. Its support is a sublattice, so it also disproves the source's stronger, related Conjecture 3. It does **not** answer question 1: the constructed distribution is not even in the closure of clique-factorizing distributions.

## 2. Four-cycle construction

Let G have vertex set {1,2,3,4} and edges 12,23,34,41. Put

\[
p(a,a,b,c)=\frac{2^{abc}}9\quad(a,b,c\in\{0,1\}),
\qquad p(x)=0\quad\text{if }x_1\ne x_2.
\tag{1}
\]

Thus seven support atoms have mass 1/9 and the atom 1111 has mass 2/9. The eight weights sum to 1. Every individual coordinate takes both values with positive probability.

### Proposition

The distribution (1) is MTP2 and globally Markov with respect to G, but it does not factor over the cliques of G and is not a pointwise limit of such distributions.

### Proof: total positivity

The map (a,b,c)↦(a,a,b,c) preserves coordinatewise meet and join. Its image S is therefore a sublattice. On the three-dimensional Boolean cube, the function u(a,b,c)=abc, the indicator of the top element, is supermodular: if one input is the top, the supermodular inequality is an equality; if neither is the top, its right-hand side is zero and its left-hand side is nonnegative. Hence 2^u is log-supermodular. For inputs in S this proves

\[
p(x\wedge y)p(x\vee y)\ge p(x)p(y).
\]

If either input lies outside S, the right-hand side is zero, so the same inequality holds. This checks all pairs, including boundary zeros, rather than only adjacent-coordinate inequalities.

### Proof: the global Markov property

In a four-cycle, a nontrivial separation between nonempty disjoint A and B is possible only when the conditioning set C is one pair of opposite vertices, with A and B the two remaining singleton vertices. Indeed, deleting zero or one vertices leaves a connected graph; deleting two adjacent vertices also leaves a connected graph; and deleting three or more vertices cannot leave two nonempty disjoint sets.

Consequently the required nontrivial conditional independences, up to interchanging A and B, are precisely

\[
X_1\perp X_3\mid(X_2,X_4),\qquad
X_2\perp X_4\mid(X_1,X_3).
\]

Both hold because X_1=X_2 almost surely: in the first assertion X_1 is fixed by the conditioning variables, and in the second X_2 is fixed. Conditional independence imposes no additional restriction on null conditioning events. Empty A or B gives a tautology. Thus this is the global, not merely pairwise, Markov property.

### Proof: an invariant excluding factorization and its closure

Every clique of G has size at most two. For any clique-factorizing mass function r, necessarily

\[
r_{0000}r_{0011}r_{1101}r_{1110}
=
r_{0001}r_{0010}r_{1100}r_{1111}.
\tag{2}
\]

Here is a direct proof which also covers zero or signed potentials. For each edge 23,34,41, the four atoms on either side have the same multiset of restrictions to that edge: each pair 00,01,10,11 occurs once. For edge 12, each side has two restrictions 00 and two restrictions 11. Singleton and empty cliques likewise have equal restriction multisets on both sides. Substituting the product of clique factors in either side of (2) therefore gives exactly the same product of real numbers. No logarithm, division, positivity of a potential or cancellation is needed.

For (1), the left-hand side of (2) equals 1/9^4 and the right-hand side equals 2/9^4, a contradiction. Since (2) is a polynomial equality, it persists under pointwise limits on this finite state space. Thus (1) is outside even the closure of the factorizing model. ∎

## 3. Attribution and what is added

The invariant (2) is **not new**. It is exactly the polynomial denoted f_12^same in Geiger, Meek and Sturmfels, *On the toric algebra of graphical models*, Annals of Statistics 34 (2006), Proposition 1, equation (4.10), printed p. 1478, [author-hosted paper](https://math.berkeley.edu/~bernd/AOS0092.pdf), DOI 10.1214/009053606000000263. The direct balance proof is included so the argument is self-contained.

Their Example 8 uses a different four-atom support which is not a sublattice. Here the weight choice (1) supplies the needed MTP2 counterexample on an equality sublattice. A bounded literature check found no earlier explicit resolution of this source conjecture, but that is not proof of priority. The result is presented as a checkable counterexample to the exact printed formulation.

The 2021 paper by Lauritzen, Uhler and Zwiernik, *Total positivity in exponential families with application to binary variables*, §4.4, works with the intersection of MTP2 and the **extended** graphical model in the relevant compactness results. Its hypotheses do not include (1), which violates (2). There is therefore no conflict with those results. [Primary paper](https://par.nsf.gov/servlets/purl/10339054).

## 4. Six-cycle cross-check

The initial construction used the cycle C6 and atoms (a,a,b,b,c,c) with the same weights 2^(abc)/9. It has the same conclusion. The three internally connected equality blocks contract to a triangle. After deleting a separator, every untouched block remains connected to every other untouched block. Any block touched by the separator is fixed by conditioning. Thus two separated sets cannot both contain an unfixed coordinate, establishing the global Markov property. The same even-versus-odd cubic contrast is balanced on every original edge and is violated by the weights.

The smaller C4 construction is the principal proof; C6 is retained as a separately exhaustive exact control, not an additional research turn.

## 5. Reproduction, remaining gap and estimate

Run `python3 checks/verify_turn1.py` for C4: 332 exact assertions, including all 256 MTP2 pairs, all 64 conditional-independence equalities for its four ordered nontrivial separations, and all nine clique exponent balances.

Run `python3 checks/verify_c6.py` for C6: 13,520 exact assertions, including all 4,096 MTP2 pairs and all 9,408 conditional-independence equalities for 252 ordered separations. These finite exhaustive checks supplement the proof and use only the Python standard library.

**Sharp remaining gap:** prove or refute closure of the MTP2 edge-factorizing model for every finite graph, including boundary distributions. A proof only for strictly positive limiting distributions would not settle this. The convention for isolated vertices must also be made explicit: ordinary Ising models allow unary potentials; the source writes edge-only factors.

**Planning completion estimate:** 50% of the bundled two-question goal, conditional on independent review of the counterexample. This is a subjective progress estimate, not a probability of correctness or a claim that the remaining question has half the difficulty.
