# Direct unbased obstruction from the folded cores

Problem 30003527, shared pass 3, 13 October 2026. Supplement to COLLARED_QUOTIENT_OBSTRUCTION.md; that report remains unchanged. This supplies a second, elementary proof of the key unbased nonmovability step and removes the need for the Takahasi-Higman theorem in this particular example. It is an authored candidate pending independent audit.

Let G be the two-loop rose, F=pi_1(G,v), and f(a)=a, f(b)=b a b^(-1) a^(-1) b. Put alpha=f_* and H_n=alpha^n(F).

## 1. Every iterate is an immersion

At the rose vertex the images of the four oriented directions a, a^(-1), b, b^(-1) start with those four distinct directions. At each interior subdivision point of the b-edge, the adjacent letters of b a b^(-1) a^(-1) b do not cancel. Thus f is locally injective at the vertex, at the four interior turns, and in the interiors of the edge segments. It is a graph immersion after subdivision.

Compositions of locally injective maps are locally injective. Consequently every iterate f^n is a graph immersion. In particular its word w_n=f^n(b) is freely reduced, starts with b, ends with b, and no fold occurs when the rose domain is subdivided according to w_n. One can also check the reduced length explicitly: w_n has 3^n occurrences of b or b^(-1) and length 2 times 3^n minus 1.

Let Gamma_n consist of one a-labeled edge-loop at its basepoint and a second subdivided circle spelling w_n. Its map to G is folded. Its fundamental group maps injectively onto H_n. Every edge belongs to a reduced closed path based at the basepoint, so Gamma_n is the entire based core graph for H_n. Its only a-labeled edge-loop is the original one at the basepoint: the other a-labeled edges join consecutive distinct vertices of the subdivided w_n-circle. For n=0 the second circle is simply the b-loop, and the same assertion holds.

## 2. Conjugation cannot relocate a subgroup containing a

Complete Gamma_n to the connected covering graph of G representing H_n by attaching labeled trees to the missing directions. This completion adds no cycles. Equivalently, the complement of the finite core in the covering graph is a union of trees attached to the core. Therefore the entire covering graph has exactly one vertex supporting an a-labeled edge-loop, namely its basepoint.

Suppose a belongs to g H_n g^(-1). Then g^(-1) a g belongs to H_n. In the covering graph, the path with label g^(-1) from the basepoint reaches a vertex at which the a-edge is a loop: lifting the whole word g^(-1) a g closes exactly when that a-edge fixes this intermediate vertex. Since the a-loop occurs only at the basepoint, the path g^(-1) must itself be closed. Hence g belongs to H_n and g H_n g^(-1)=H_n.

This can also be phrased using the right action of F on the coset vertices H_n h: the intermediate vertex H_n g^(-1) is fixed by a precisely when g^(-1) a g belongs to H_n. Uniqueness of the a-loop forces H_n g^(-1)=H_n.

## 3. Apply the unbased movability condition

The strict containments H_(n+1) properly contained in H_n were proved in the main report by the folded five-edge core: alpha is injective and b is absent from alpha(F).

If the inverse limit X were movable, the finite-graph expansion at stage zero would yield some j such that for every k>j there were a map r:G_j to G_k and an unbased homotopy between f^j and f^k composed with r. On fundamental groups this entails H_j contained in g H_k g^(-1) for some g in F. Since a belongs to H_j, Section 2 makes that conjugate equal to H_k. We obtain H_j contained in H_k, contrary to H_k being properly contained in H_j.

Thus X is nonmovable with the unbased homotopy quantifiers, independently of the Takahasi-Higman input. The collar, quotient, and stable-tail constructions of the main report then apply unchanged. No flow realization or invariant-enlargement counterexample is asserted.
