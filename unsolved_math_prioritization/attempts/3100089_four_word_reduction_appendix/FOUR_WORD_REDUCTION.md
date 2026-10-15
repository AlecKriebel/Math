# A scoped reduction for a hypothetical four-word disconnection

## Scope

This note gives necessary conditions for a pressing instance with exactly four successful words to have a disconnected four-deletion/four-insertion graph. It does not classify all four-word languages and does not produce a counterexample. It uses the accepted [trajectory-fiber theorem](../3100089_positive_connectivity_appendix/STRUCTURAL_LEMMAS.md) and the accepted [short-neighbor/two-word theorem](../3100089_short_neighbor_terminal_appendix/SHORT_NEIGHBOR_THEOREM.md). No further search is needed for the proofs below.

Delete all permanently zero rows and columns. Let N be the remaining coordinate set, m=|N|, r=rank(A), and Z the number of successful words. Put e=m-r. The zero-coordinate deletion changes no successful word or LCS. Assume the successful language is nonempty.

## 1. A component-size bound

For any exact trajectory, its disjoint nonempty layers have sizes l_1,...,l_r, with sum m. Its fiber consists of all independent choices of a letter in each layer, and has size

product_j l_j = product_j (1+(l_j-1)) >= 1+sum_j(l_j-1)=e+1.

All its words are connected by single-position substitutions. Hence every component of the original four-deletion/four-insertion graph has at least e+1 words. The accepted short-neighbor theorem additionally says that a nonunique instance has no singleton component. Therefore a disconnected instance must satisfy

Z >= 2 max(2,e+1).                                      (1)

In particular, a disconnected four-word instance must have e=0 or e=1. Cases with at least two extra nonzero coordinates are excluded, in arbitrary rank.

A second useful count: fix a selected coordinate basis B of size r. At most one word from any exact-trajectory fiber uses precisely B, since membership in the disjoint layers fixes its complete order. Different successful words on B therefore belong to different fibers. Consequently

Z(A) >= (e+1) Z(A[B]).                                  (2)

Here successful words on the nonsingular A[B] are also successful on the full A: their r legal full-matrix presses drop rank from r to zero. Conversely any full successful word using B is a successful word on A[B].

## 2. The exact omission multigraph in corank one

Suppose e=1, so m=r+1. In every trajectory partition exactly one layer has size two, and every other layer is a singleton. Thus every fiber has exactly two words. In particular Z is even.

Define a loopless multigraph H. Its vertices are the coordinate labels that are omitted by at least one successful word. Every exact trajectory gives one edge: its two words omit two different labels a and b, and the edge joins a to b. Distinct trajectories can give parallel edges. Each successful word corresponds to one incidence of an edge and one endpoint, namely its omitted label. Hence

|E(H)|=Z/2,
deg_H(v)=Z(A[N minus {v}]).                             (3)

For the degree identity, the words omitting v are precisely the successful words of that full-rank principal restriction, by the rank argument following (2).

Let h be the unique nonzero vector in ker(A), and let K be its support. Every vertex of H lies in K. Indeed, the coordinate images in the rank-r radical quotient have exactly the one linear relation given by h. Omitting v leaves a basis exactly when h_v=1. A successful word selects such a basis.

There is also a direct description of each edge. In a word omitting a in K, let b be the last selected label from K. The relation

x_a = sum_{v in K minus {a}} x_v

has, in the word's triangular Gram–Schmidt coordinates, highest nonzero coordinate at the position of b. Thus a lies in b's trajectory layer. The two words in that fiber omit a and b respectively. An edge of H is exactly the terminal pair from K in its trajectory; labels outside K are never omitted.

## 3. The remaining corank-one four-word configuration

If Z=4, H has exactly two edges. At every vertex, its degree is at most two. By the accepted two-word theorem, all words incident at a fixed vertex v are connected inside their nonsingular principal restriction A[N minus {v}], at the original deficit-four threshold. The two incidences of a single edge are connected by the trajectory's deficit-one replacement.

Therefore, if the two edges of H meet, these within-vertex and within-edge paths connect all four words. This includes parallel edges. A disconnected four-word pressing graph with e=1 must consequently have

H = two disjoint edges.                                (4)

Equivalently, its entire language must consist of exactly two trajectory fibers of size two, with disjoint omitted-label pairs. Each of the four selected coordinate bases then has a unique successful word.

Condition (4) is **necessary, not sufficient**, for a BFM disconnection. Even if H were disconnected, the full BFM graph could have an edge between words using different omitted labels and different trajectories. The omission multigraph retains only the guaranteed within-basis and within-fiber routes.

## 4. A further necessary one-column-union form

Assume the configuration (4), and select one of its two fibers, with omitted-label pair {a,b}. Write its word omitting a as S, and suppose b occupies position j. Let U be the unit-upper-triangular Cholesky root of the coordinate basis N minus {a}, in S's order.

The companion word replaces b by a at position j and has exactly the same Gram–Schmidt basis and full matrix trajectory. Its Cholesky root V therefore agrees with U in every column except j; column j is replaced by the coordinate vector x_a expressed in that common orthonormal basis. It still has its highest nonzero entry at j.

Because all four endpoint degrees in H are one, the principal restrictions omitting a and omitting b each have a unique successful word. The accepted Cooper–Whitlatch characterization therefore places both U and V in the unique-root class M_r, with its precise four interval/weight conditions as stated in the accepted [short-neighbor/two-word theorem](../3100089_short_neighbor_terminal_appendix/SHORT_NEIGHBOR_THEOREM.md).

The two differing columns must be genuinely distinct. If x_a=x_b, the unique radical relation would have support exactly {a,b}; every omittable label would then belong to {a,b}, contradicting the other disjoint edge in (4).

Thus a remaining corank-one four-word candidate must arise by taking a unique root U in M_r and adjoining one alternate column from another root V in M_r that differs from U at exactly that column. The resulting augmented configuration would need an additional exact trajectory whose omitted-label pair is disjoint from the original pair.

This is a rigorous reduction, but the following sufficient exclusion statement has **not** been proved here:

> If U,V in M_r differ in exactly one column, their combined coordinate configuration has only the common original trajectory.

It would rule out (4), and thereby settle all corank-one four-word instances. No assertion of this rigidity statement, or of full-rank four-word connectivity, is made.

## 5. What remains

The accepted [arbitrary-ambient rank-six theorem](../3100089_rank_six_overlap_appendix/RANK_SIX_CONNECTIVITY.md), together with the earlier lower-rank result, separately covers all of these configurations in ranks at most six. In arbitrary rank the remaining four-word cases are:

- m=r, a nonsingular full-coordinate matrix;
- m=r+1, exactly the necessary two-disjoint-edge omission configuration above.

The accepted [eight-vertex unique-overlap example](../3100089_rank_six_overlap_appendix/UNIQUE_OVERLAP_OBSTRUCTION.md) belongs to the first case but has a connected BFM four-cycle. It establishes a limitation of the restricted move system, not a counterexample in either remaining case.

The accepted short-neighbor theorem and the separate restricted-move obstruction remain unchanged. This note is an additional scoped reduction; no classification claim is inferred from a finite search.
