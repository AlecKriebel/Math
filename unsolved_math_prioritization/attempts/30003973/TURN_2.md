# Turn 2: a mixed-color transfer criterion and its obstruction

Problem30003973. Original unresolved; this is the second substantive turn. The attempt is to turn2-color equivalence into3-color equivalence by recoloring unions of color classes. It yields a sufficient condition in terms of an asymmetric Ramsey problem and a necessary configuration for any counterexample. A finite independence-system example proves that the extra condition cannot simply be inferred from an abstract equality of squares. No novelty claim is made.

## 1. A precise algebra for color partitions

Fix a finite vertex set V and its possible edge set E=binom(V,2). For a target H let A_H be the downward-closed family of edge subsets whose corresponding spanning graph on V contains no ordinary copy of H. Retaining all vertices is important if the target has isolated vertices. Turn1 permits us to restrict future target searching to isolate-free targets, but the present family definition is valid in either case.

For downward-closed families A,B⊆2^E, define

    A·B = {a∪b : a∈A, b∈B}.

This is itself downward closed, associative and commutative. Allowing overlap causes no ambiguity: replace b by b\a, which still belongs to B. Thus A_H^q is exactly the family of hosts on V that admit a q-edge-coloring with no monochromatic H. Equality of q-Ramsey classes is the equality of these q-th powers for every finite V.

For H≡_2 H', put A=A_H, B=A_H' and D=A²=B². Then A^(2k)=B^(2k) for every positive k. This is the known even-color transfer, in the language of edge-set families; it is not a new result. The challenge is the odd power A³ versus B³.

## 2. A sufficient asymmetric condition

**Algebraic lemma.** If A²=B²=D and A·B⊆D, then A³=B³. Consequently A^q=B^q for every q≥2.

Indeed,

    A³=A·B²=(A·B)·B⊆D·B=B³,
    B³=B·A²=(A·B)·A⊆D·A=A³.

This proves equality at3. Even powers follow from the common square, and any odd q≥3 equals3 plus an even nonnegative number, giving all remaining powers. The proof needs only associativity and commutativity plus the stated mixed inclusion; it does not assume a square-root cancellation law.

Write G→(H,H') when every red-blue coloring of G has a red H or a blue H'. The mixed product A_H·A_H' is exactly the class of hosts which fail this asymmetric arrow property. We therefore obtain:

**Conditional transfer theorem.** Suppose H≡_2 H'. If every2-Ramsey host for H is also Ramsey for the asymmetric pair(H,H'), then H≡_q H' for all q≥2.

The extra hypothesis says precisely A_H·A_H'⊆A_H² on every finite vertex set. Apply the algebraic lemma. Color reversal makes the order of the two entries immaterial here.

The nested-target situation is one familiar case where this mixed condition holds. If H⊆H', a coloring with red H absent and blue H' absent has H' absent in both colors. Hence a symmetric2-Ramsey host for H' cannot have that coloring. Since the symmetric host classes of H and H' agree, the mixed condition follows. This recovers, and credits, the known nested-target transfer cited by Clemens–Liebenau–Reding. It does not remove the nesting assumption without a new argument for the mixed condition.

## 3. Necessary crossed witnesses for a genuine counterexample

Suppose H≡_2 H' but some G satisfies G→_3 H and G↛_3 H'. Fix an H'-free3-coloring of G, with disjoint color edge sets B_1,B_2,B_3. Every B_i lies in B=A_H'.

Since B_1∪B_2∈B²=A², there is a partition

    B_1∪B_2=A_1⊔A_2

with both A_i H-free. For either i, the host F_i with edge set A_i∪B_3 **must** be2-Ramsey for H. Otherwise splitting F_i into two H-free classes and keeping the other A_j as a third class would give an H-free3-coloring of G. By2-equivalence, F_i is also2-Ramsey for H'. But its displayed partition into A_i and B_3 avoids a red H and a blue H'. Thus each F_i is a symmetric Ramsey host for both targets that fails the mixed asymmetric Ramsey condition.

More is forced:

- Each original B_i contains a copy of H. If B_3, for example, were H-free, the above A_1,A_2,B_3 would already be an H-free3-coloring. The same argument applies after permuting the three colors.
- Each recolored A_i contains H'. Otherwise A_i and B_3 would both be H'-free, contradicting the2-Ramsey property of F_i for H'. This holds for **every** H-free2-coloring of B_1∪B_2, not just a favorable choice.
- Neither target is a subgraph of the other. H⊆H' would contradict an H-free A_i containing H'; H'⊆H would contradict an H'-free B_i containing H.
- With e=|E(H)| and e'=|E(H')|, the host satisfies

      |E(G)|≥max{3e, e+2e'}.

  The first bound uses the three edge-disjoint B_i, each containing H. The second uses A_1,A_2,B_3, with the first two containing H' and the last containing H. Target copies may share vertices, so no unsupported vertex-disjointness bound is inferred.

This necessary configuration is stronger than finding one graph Ramsey for both symmetric targets but not the mixed pair: it requires two such crossed hosts with a common H'-free edge part, inside a3-Ramsey host for H. Producing an isolated mixed witness alone would not solve the original question.

## 4. Why the mixed condition is an extra hypothesis

Take a five-element abstract ground set {0,1,2,3,4}. Define two downward-closed families by their maximal members:

    A: {1}, {0,3}, {0,4}, {2,3,4}
    B: {0}, {1,3}, {1,4}, {2,3,4}.

Both contain every singleton. Direct union calculation gives the same square, with maximal members

    D: {0,1,3}, {0,1,4}, {0,2,3,4}, {1,2,3,4}.

However {0,3}∈A and {1,4}∈B have union {0,1,3,4}∉D. Thus A²=B² does not, by itself, imply A·B⊆D.

Both cubes in this example are the full power set: A has the three members {1},{0,3},{2,3,4} whose union is the entire ground set, and B has the analogous triple. Downward closure then yields every subset. Hence this example is **not** a counterexample to equality of cubes, and certainly not a pair of graphs resolving the source problem. It only blocks the unsupported inference that the mixed condition follows formally from equal squares.

No claim is made that these abstract families arise as the H-free and H'-free edge sets for a fixed pair of graph targets simultaneously on every host order. That graph-realizability and uniformity requirement is an additional, essential constraint.

## 5. Exact finite exploration and the remaining gap

The checker independently constructs products as all unions and verifies the explicit families above. It then enumerates all downward-closed families containing every singleton on ground sets of sizes1 through5. Families with the same square also have the same cube in this finite scan. This covers7,020 families in total, with exact counts recorded in TURN_2_CHECKS.json; it is not evidence of a general square-root theorem beyond the checked orders.

The author also explored pair-generated systems on a six-element set during this turn without finding a full-set cube distinction. That exploratory negative result is not promoted to a universal claim or part of the final theorem. The portable checker certifies only the explicitly stated size1–5 range and the finite mixed-condition obstruction.

The full target remains open in this work. A possible counterexample must survive Turn1's isolate removal, have incomparable targets, and exhibit the forced crossed recoloring configuration above. A positive solution by this approach still requires proving the mixed Ramsey condition for every2-equivalent pair, or some weaker argument that directly controls the cubes. The five-element example prevents treating that condition as a purely formal consequence of equal squares. Completion estimate:15%; three substantive author turns remain after this checkpoint.
