# Turn 1: a reflection-self-dual wheel family

2026-10-02. Substantive author turn **1/5**. The original all-determinants problem remains unresolved. The result is an explicit infinite family in its nonsquare, non-rational part. The checkerboard correspondence and the rational-case obstruction are credited to the prior sources in SOURCE_SCOPE.md; no historical novelty is certified.

## Theorem

For every integer k≥0, there is a prime alternating achiral knot of determinant

    n_k = 9(52k²+28k+5) = 468k²+252k+45.

Every n_k is a nonsquare odd sum of two squares and has no coprime sum-of-two-squares representation. Consequently these examples are outside both the rational-knot realization case and the perfect-square realization case already established by Stoimenow. This last statement does not claim that these knots or determinants were previously unknown.

## 1. The plane graph and its duality

Let W be the four-spoke wheel, with hub o, rim vertices v_0,v_1,v_2,v_3 in cyclic order, spokes s_i=ov_i and rim edges r_i=v_iv_{i+1}, indices modulo 4. Write U for the outer face and F_i for the triangular face between s_i,s_{i+1},r_i. The plane dual has hub U and cyclic rim F_i. The identification

    o ↦ U,   v_i ↦ F_{−i}

sends s_i to the dual edge of r_{−i} and r_i to the dual edge of s_{−i}. It is an orientation-preserving plane duality, as can be checked from the rotation systems. Around o the cyclic order is (v_0,v_1,v_2,v_3), whereas around U it is (F_0,F_3,F_2,F_1). Around v_i the order is (o,v_{i−1},v_{i+1}); around F_j it is (U,F_{j+1},F_{j−1}). The displayed identification preserves each of these cyclic orders. A rotation-preserving isomorphism of these cellularly embedded graphs extends over edge ribbons and face disks to an orientation-preserving sphere homeomorphism. It exchanges the two specified edge families in pairs; no rigid Euclidean symmetry of a particular drawing is assumed.

For a positive integer a, form G_a by replacing s_0 with a parallel edges in its narrow ribbon and r_0 with a path of a edges. All other edges are unchanged. Parallel replacement and subdivision are dual operations. Because s_0 and r_0 are paired by the above involution, doing these replacements with equal multiplicity preserves plane self-duality. One can extend the base homeomorphism across the replacement ribbons, exchanging the parallel and series configurations. This is a duality of the embedded graph, not merely equality of its tree count with another graph.

For an explicit incidence check, label the a−1 new digon faces in order between F_3 and F_0 by D_1,…,D_{a−1}. In the dual, the parallel-spoke bundle becomes the path

    F_3, D_1,…,D_{a−1}, F_0,

while the subdivided r_0 becomes a parallel-edge bundle from U to F_0. Map the internal vertex in position j along the original v_0-to-v_1 path to D_{a−j}; the old vertex map above completes the isomorphism. The cyclic order is the one inherited from the ribbon substitutions. Thus it realizes the stated plane duality.

The graph G_a has no loops, no bridges, and no cut vertex. Indeed, the wheel has these properties; adding parallel copies cannot create a cut vertex or bridge, and subdividing an edge of a vertex-biconnected graph preserves vertex-biconnectivity. For the latter assertion directly: removal of an old vertex leaves the rest of the wheel connected, with any surviving path segment attached at its surviving endpoint; removal of an internal path vertex leaves two path segments attached at v_0 and v_1, which remain connected through the other three rim edges. It follows in particular that every edge lies on a cycle. This argument uses the ordinary explicit conditions and does not import the unusual terminology in the source's Definition 6.2.

## 2. Exact tree count

Eliminate the a−1 internal vertices in the subdivided rim edge, or equivalently use the series conductance rule with its spanning-tree factor a. The resulting weighted wheel has spoke weight a at s_0, weight 1 on the other spokes, rim weight 1/a at r_0 and weight 1 on the remaining rim edges. Deleting the hub row/column gives

        [a+1+1/a   −1/a       0       −1]
    M = [  −1/a    2+1/a     −1        0]
        [     0      −1       3       −1]
        [    −1       0      −1        3].

The matrix-tree theorem yields

    τ(G_a) = a det M = 13a² + 16a + 16.

Here is a direct combinatorial justification of the series factor, avoiding any unproved normalization convention. A tree of the base wheel either uses r_0, in which case its replacement must use the whole length-a path, or does not use r_0, in which case exactly one of the a path edges is omitted, with a choices. A used spoke s_0 has a choices of its parallel copy; an unused spoke has none to choose. Thus a base tree contributes a^{1+1_{s_0 used}−1_{r_0 used}}. Among the 45 base-wheel trees, 13 have exponent 2, 16 have exponent 1 and 16 have exponent 0. These small counts can also be obtained by expanding the displayed 4×4 determinant. The supplied checker independently enumerates the 70 four-edge subsets of the wheel and compares the resulting formula with determinants of the actual expanded integer graph.

The identity

    13a²+16a+16 = (3a)²+(2a+4)²

is immediate. For odd a this determinant is odd. The alternating medial diagram of the embedded G_a is therefore a knot: a link with μ components has determinant divisible by 2^{μ−1}, whereas a knot has odd determinant. Its diagram is reduced because G_a has neither loops nor bridges, and prime because G_a has no cut vertex. The standard prime alternating diagram theorem then makes the knot prime. Its plane self-duality exchanges the checkerboard colors and gives its mirror diagram by a sphere homeomorphism, proving achirality. These are the established checkerboard facts in Stoimenow's Section 6.1 and the cited prime-diagram theorem; no converse classification of all achiral diagrams is needed.

## 3. The nonprimitive nonsquare specialization

Take a=6k+1. Then

    n_k = [3(6k+1)]² + [3(4k+2)]²
        = 9(52k²+28k+5).

It is at least 45, so none of 1,9,49 occurs. The inner quadratic is 5 modulo 8 because 52k²+28k+5≡4k(k+1)+5≡5 mod8. Hence n_k≡5 mod8 and cannot be a square. It is also coprime to 3: modulo 3 it is (6k+1)²+(4k+2)²=1+(k+2)², which is 1 or 2. Therefore v_3(n_k)=2.

For any representation n_k=x²+y², divisibility by 3 forces x≡y≡0 mod3, since the only squares modulo 3 are 0 and 1. Thus no representation is coprime. Stoimenow's Theorem 4.2 rules out any achiral rational knot with this determinant, while the constructed non-rational prime alternating achiral knot realizes it. Distinct k give increasing determinants, so the family is infinite.

## 4. Exact remaining gap and credit

This covers a single quadratic family. It does not cover arbitrary odd sums of two squares with nontrivial common prime factors, and it gives no counterexample outside the family. General planar self-dual graph constructions, spanning-tree evaluation, rational-knot realizations and the perfect-square theorem are pre-existing tools/results. The displayed graph specialization was derived in this attempt; no search has established first priority for its family. The next research question is whether more paired edge replacements can cover the remaining arithmetic possibilities without losing embedded self-duality or primeness.
