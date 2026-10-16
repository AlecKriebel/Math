# Invariant finite energy percolation with internal critical probability one

Problem 10000036 / AMR-099-0036. Author manuscript, 6 October 2026.

**Status:** Complete candidate proof for the ordinary, nonuniform finite-energy convention. Independent mathematical review is pending. No priority or novelty claim is made. The argument uses established existence theorems for one-ended invariant spanning trees, with all subsequent probabilistic and graph-theoretic steps supplied below.

## 1. The precise claim

For every integer d >= 2, there is a bond-percolation law on the nearest-neighbor edges E of Z^d with the following properties:

1. Its distribution is invariant under every graph automorphism of Z^d.
2. It is mixing, hence ergodic, under translations.
3. For every e in E, conditional on the states of all other edges, the probabilities of both states of e are strictly positive almost surely.
4. The resulting graph X = (Z^d, E_X) almost surely has exactly one infinite connected component C.
5. For almost every realized X, every independent Bernoulli bond thinning with retention parameter p < 1 has no infinite component almost surely. In particular p_c(X) = p_c(C) = 1, with p_c understood in the quenched sense.

The finite-energy assertion is condition 3, not a uniform lower bound over configurations. No uniform finite-energy conclusion is asserted. The external percolation is a bond law; no conversion of a site law is used. The vertices of X remain all of Z^d, so finite components are allowed. The claim does not say that every vertex percolates.

For a countable, locally finite deterministic graph H which has an infinite component, set

p_c(H) = inf {p in [0,1] : Bernoulli-p bond percolation on H has an infinite component with positive probability}.

The construction will produce a graph property that proves the conclusion separately for every p < 1 after X has been fixed. No annealed-to-quenched inference at an uncountable family of parameters is needed.

## 2. A deterministic one-ended tree lemma

Let G = (V,E) be a countably infinite connected simple graph of maximum degree at most a finite constant Delta. Let T be a spanning tree of G with exactly one end.

For each tree edge t, deleting t divides T into two components. Exactly one is finite. Indeed, both cannot be finite because T is infinite; if both were infinite, local finiteness would give an infinite simple ray in each, contradicting one-endedness. Write S_T(t) for the finite vertex set and s_T(t) = |S_T(t)|. Thus s_T(t) is a positive finite integer and

partial_T S_T(t) = {t},

where partial denotes the edges with exactly one endpoint in the indicated vertex set.

Fix v in V. There is a unique infinite simple T-ray from v, written v = v_0, v_1, v_2, ... . Existence follows from local finiteness and infinitude of T; two different rays starting at v in a tree would create two different ends. Let t_n = {v_n,v_{n+1}} for n >= 0, and abbreviate S_n = S_T(t_n), s_n = |S_n|. Then

v in S_0 subsetneq S_1 subsetneq S_2 subsetneq ...,

and s_n >= n+1. To see strict inclusion, S_n lies on the finite side of the next ray edge and v_{n+1} belongs to S_{n+1} but not S_n. Thus the s_n are distinct positive integers. Consequently, for every nonnegative sequence a_m,

sum_(n>=0) a_(s_n) <= sum_(m>=1) a_m.                 (2.1)

For an edge e = {x,y} outside T, let P_T(e) be the unique finite T-path from x to y. Define

M_T(e) = max {s_T(t) : t belongs to P_T(e)}.

This maximum is a finite positive integer. If e crosses the cut S_T(t), then the T-path between its endpoints crosses that cut too, and the only tree edge crossing is t. Hence

e in partial_G S_T(t), e not in T  ==>  t in P_T(e)  ==>  M_T(e) >= s_T(t).       (2.2)

Also |partial_G S_T(t)| <= Delta s_T(t), by summing degrees of the vertices in S_T(t). These facts require neither independence nor a geometric estimate on T.

## 3. The perturbation kernel

Given T, take mutually independent uniform [0,1] random variables U_e, one for each e in E. Set

r_T(e) = 1 - 2^(-s_T(e))                       if e is in T,
r_T(e) = 2^(-M_T(e))                           if e is outside T,

and declare e open in X exactly when U_e < r_T(e).

Thus every tree edge has a positive deletion probability and every non-tree edge has a positive insertion probability. For every e,

0 < r_T(e) < 1.                                (3.1)

The probabilities are not constant in the environment. In particular, the noise is not an independent Bernoulli process of a fixed positive density added to an everywhere-percolating graph.

The construction is measurable. For a prescribed finite vertex set, the event that it is the component of an endpoint after removing a prescribed tree edge can be specified using finitely many edge statuses, since G is locally finite. Finite component sizes are therefore measurable. The tree path between two fixed vertices is measurable by taking the countable disjoint union over finite candidate paths. The displayed finite maximum is consequently measurable as well. On the null set where a random input is not a one-ended spanning tree, all r_T(e) can be set to 1/2. This gives a measurable kernel on the entire input space.

For every automorphism g of G,

S_(gT)(gt) = g S_T(t),   s_(gT)(gt) = s_T(t),   P_(gT)(ge) = g P_T(e),

so r_(gT)(ge) = r_T(e). The perturbation kernel is fully automorphism-equivariant.

## 4. Simultaneously retained rays and unbypassed cuts

Fix a deterministic one-ended T and a vertex v, with t_n, S_n, s_n as in Section 2. Let D_n be the event that t_n is deleted. Let A_n be the event that some non-tree edge crossing S_n is open in X. Conditional on T,

P(D_n | T) = 2^(-s_n),

and, using (2.2) and the union bound,

P(A_n | T)
 <= sum_{e in partial_G S_n, e not in T} 2^(-M_T(e))
 <= Delta s_n 2^(-s_n).

It follows from (2.1) that

sum_(n>=0) P(D_n union A_n | T)
 <= sum_(m>=1) (1 + Delta m) 2^(-m)
 = 1 + 2 Delta < infinity.                     (4.1)

The first Borel-Cantelli lemma applies. No independence between the events A_n or D_n is required. With conditional probability one there is a finite random N_v such that, for every n >= N_v, the edge t_n is retained and no open non-tree edge crosses S_n. Since t_n was the only tree edge crossing this cut before any deletions, after the perturbation we have the exact identity

partial_X S_n = {t_n},                         (4.2)

and every edge in the tail t_(N_v), t_(N_v+1), ... is open.

There are only countably many vertices. Intersecting these conditional probability-one events over all v gives a single conditional probability-one event on which the conclusion holds simultaneously for every vertex. Integrating over any random one-ended T preserves probability one. Hence, on one event of full joint (T,U)-probability, all vertices have eventually retained rays and infinitely many distinct singleton cut boundaries in the final graph X.

## 5. Percolation and uniqueness

Let R = (V, T intersect E_X) be the subgraph of retained tree edges. Section 4 supplies an infinite R-ray tail, so R and therefore X percolate.

In fact R has exactly one infinite component. Any two rays of the one-ended tree T eventually coalesce: otherwise the finite path joining their starting points together with noncoalescing ray tails would give two ends. The eventually retained tails from any two vertices therefore meet in a common retained tail. Every infinite component of R contains a ray by local finiteness, and this ray must be the unique T-ray from any one of its vertices. It therefore meets the same retained-tail component. Denote this unique infinite R-component by C_R.

Suppose v belongs to an infinite X-component. Choose n >= N_v in (4.2). Because S_n is finite and contains v, an infinite X-path from v must leave S_n. It can only do so across t_n. Both endpoints of t_n lie on the retained ray tail and therefore belong to C_R. Thus v is X-connected to C_R. Every infinite X-component contains C_R, so X has exactly one infinite component C.

This argument establishes uniqueness directly; it does not require an ergodic-decomposition argument or an appeal to a uniqueness theorem for finite-energy percolation.

## 6. Quenched critical probability

Fix any pair (T,X) in the full-probability event from Section 4. Fix a vertex v and a retention parameter p < 1. Let H be independent Bernoulli-p bond percolation on this already fixed X.

Every H-path from v to infinity is an X-path and must cross each finite set S_n, n >= N_v. By (4.2), it must therefore use every one of the distinct edges t_n, n >= N_v. For any k >= 1,

P_p^X(v is in an infinite H-component)
 <= P_p^X(t_(N_v), ..., t_(N_v+k-1) are all retained)
 = p^k.

Letting k tend to infinity proves that this probability is zero. A countable union over v proves that H has no infinite component almost surely.

The proof works for every p < 1 for this fixed good X. At p = 1, X has the infinite component established in Section 5. Thus p_c(X) = 1. The same cuts, restricted to C, prove p_c(C) = 1: whenever v is in C, t_n lies in C and is the only C-edge through the finite set S_n intersect C. Possible deletions in the finite side of a cut do not create a bypass and do not invalidate its separating property.

The tree T is a witness for these graph properties, not part of the subsequent thinning randomness. Once (T,X) is fixed, all the relevant cut edges are fixed. The conclusion is a property of X alone, so the marginal law of X assigns probability one to graphs having it.

For completeness, the same construction also gives internal Bernoulli site critical probability one. An infinite site-open path from v would have to traverse every t_n and hence retain all the distinct vertices v_(N_v), v_(N_v+1), ... . The same p^k bound applies. This is an internal-thinning observation about the graph X; the external finite-energy process constructed here remains a bond process.

## 7. Finite energy after forgetting the tree

Let the law of the random tree be arbitrary, supported on one-ended spanning trees, and take the marks independently of T. For an edge e, set

F_e = sigma(X_f : f in E, f != e).

Conditional on T and F_e, the coordinate U_e is still uniform and independent, because all other X_f are functions of T and marks U_f with f != e. Therefore

P(X_e = 1 | T, F_e) = r_T(e),

and the conditional-expectation tower property gives

P(X_e = 1 | F_e) = E[r_T(e) | F_e],
P(X_e = 0 | F_e) = E[1 - r_T(e) | F_e].         (7.1)

Both conditional expectations are strictly positive almost surely. Here is the measure-theoretic detail: if Y > 0 almost surely and B = {E[Y | F_e] = 0}, then B is F_e-measurable and E[1_B Y] = E[1_B E[Y | F_e]] = 0, forcing P(B) = 0. Apply this separately to Y = r_T(e) and Y = 1-r_T(e), which are strictly positive by (3.1).

Thus 0 < P(X_e=1 | F_e) < 1 almost surely. Countability of E permits simultaneous versions off one null set. The standard almost-sure definition of finite energy follows. If a formulation requests a version defined with values in (0,1) also on configurations of zero conditioning probability, set that version to 1/2 on the exceptional null conditioning set.

No uniform lower bound was used or obtained in (7.1). Strictly positive random variables can have conditional expectations with essential infimum zero; conversely, the small conditional probabilities given T alone do not by themselves prove that the marginal law fails uniform finite energy. We make neither unsupported assertion.

## 8. Invariant inputs on every lattice dimension at least two

It remains to choose T.

For d = 2, a classical option is the uniform spanning tree on Z^2. Pemantle's theorem supplies its existence and one-endedness [P, Theorems 2.3 and 4.3]; the exhaustion-independent limiting law is invariant under all lattice automorphisms. In the same way this option works in dimensions 3 and 4. The corresponding forest in higher dimensions is not a spanning tree, so it must not be substituted into our formulas: edges between different forest components would have no finite tree path.

To cover every d >= 2, use Timar's established theorem [T, Theorem 1 and Corollary 2 in the cited arXiv version]. It provides a one-ended spanning tree as an isomorphism-equivariant measurable factor of independent vertex labels on an amenable one-ended unimodular graph. The nearest-neighbor graph Z^d satisfies these assumptions: it is a unimodular Cayley graph, boxes have boundary-to-volume ratio tending to zero, and the complement of a box is connected for d >= 2. The deterministic rooted lattice is an ergodic unimodular random graph.

Use this factor construction as the law of T, with an independent family of edge marks U_e. Equivariance of T and of the perturbation in Section 3 proves full automorphism invariance of X, including rotations and reflections.

The joint field of independent vertex labels and independent edge marks is mixing under translations. To verify this directly, approximate two events in that product space in probability by events depending on finitely many labels and marks. Sufficiently separated translates of the finite supports are disjoint and hence independent; then let the approximation errors tend to zero. Every measurable translation-equivariant factor inherits this mixing property by taking preimages of events. The graph X is such a factor. This proves assertion 2 in Section 1 without an extra assumption on an arbitrary mixture of invariant tree laws.

All five assertions are now established, subject only to the quoted established existence theorem for the input tree. The d = 2 affirmative construction can alternatively be based solely on the older uniform-spanning-tree theorem.

## 9. What this does and does not settle

Benjamini's Saint-Flour item 8.15 points to the earlier question of Benjamini, Haggstrom and Schramm. In [BHS, Section 1], finite energy is explicitly described as strict positivity of both single-edge conditional probabilities. Benjamini and Tassion repeat that convention beside Question 1 in [BT]. Sections 1-8 give an affirmative construction with exactly that weak finite-energy convention.

The published sprinkling theorem in [BT] assumes an everywhere-percolating subgraph to which independent fixed-density Bernoulli edges are added. Our tree edges can be deleted, and insertion rates depend on the entire tree. Thus that theorem does not apply to this perturbation.

The summable deletion idea is related to the one-ended-tree perturbation in Haggstrom and Mester's site construction [HM, Section 2]. The additional rule here suppresses every potential non-tree bypass according to the largest finite-side size along its tree path. We do not claim that this rule or its consequence is new. A bounded literature search found no exact prior resolution, which cannot establish priority.

No result for the stronger uniform finite-energy variant is claimed. No simulation, finite computation, or proof-assistant certificate is being used as an infinite-volume proof.

## References

[BHS] I. Benjamini, O. Haggstrom and O. Schramm, On the effect of adding epsilon-Bernoulli percolation to everywhere percolating subgraphs of Z^d, Journal of Mathematical Physics 41 (2000), 1294-1297. https://arxiv.org/abs/math/9906002

[BT] I. Benjamini and V. Tassion, Homogenization via sprinkling, Annales de l'Institut Henri Poincare, Probabilites et Statistiques 53 (2017), 997-1005. https://doi.org/10.1214/16-AIHP746 and https://arxiv.org/abs/1505.06069

[HM] O. Haggstrom and P. Mester, Some two-dimensional finite energy percolation processes, Electronic Communications in Probability 14 (2009), 42-54. https://doi.org/10.1214/ECP.v14-1446 and https://arxiv.org/abs/1011.2872

[P] R. Pemantle, Choosing a spanning tree for the integer lattice uniformly, Annals of Probability 19 (1991), 1559-1574. https://arxiv.org/abs/math/0404043

[T] A. Timar, One-ended spanning trees in amenable unimodular graphs, Electronic Communications in Probability 24 (2019), paper 72. https://doi.org/10.1214/19-ECP274 and https://arxiv.org/abs/1805.10690

[S] I. Benjamini, Coarse Geometry and Randomness, Saint-Flour notes, Open problem 8.15, printed and PDF page 61. https://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf#page=61
