# A free-quotient filter for the residual spherical types

This is an elementary derived partial result and a filter on candidate invariants, not a solution or novelty claim for21.129.

Let T be one of F4,H4,D6,E6,D7,E7,D8,E8. Let P_T be its pure Artin group and Q_T=P_T/Z(P_T). Then Q_T surjects onto the rank-two free group F2. Consequently for every positive integer m, Q_T has an index-m subgroup with first rational Betti number at least m+1. Thus its virtual first Betti number is infinite. The same virtual conclusion holds for the original Artin group.

## Proof

Use the established reflection-arrangement description P_T=pi_1(M(A_T)), with M(A_T) the complement in complexified reflection space of all reflecting hyperplanes. This identification and the pure/central notation are recalled in Cumplido–Paris2022, Section3 (DOI10.4171/RMI/1282). Every listed Coxeter diagram has an edge labelled3. The two corresponding reflections generate a rank-two A2 reflection subgroup, whose three hyperplanes form a subarrangement B. Their defining forms span a two-dimensional subspace. Thus, after a linear change of complex coordinates,

M(B) = {(x,y): x y (x-y) is nonzero} x C^(rank(T)-2)
      is isomorphic to C* x (C minus {0,1}) x C^(rank(T)-2).

The inclusion M(A_T)→M(B) is surjective on fundamental groups. To see this directly, represent a based loop in M(B) by a smooth loop. Perturb it relative to the base point to be transverse to each of the finitely many additional complex hyperplanes. Each has real codimension2, while the domain loop has dimension1, so a transverse loop avoids all of them. The perturbation is a homotopy inside M(B). Hence every pi_1 class has a representative in M(A_T).

It follows that P_T surjects onto pi_1(M(B))=Z x F2 and therefore onto F2. Under any surjective homomorphism, the image of the source center lies in the target center. Since Z(F2)=1, this epimorphism kills Z(P_T) and induces Q_T→F2.

Let U_m be the kernel of the epimorphism F2→Z/m sending one free generator to1 and the other to0. The covering rose or Nielsen–Schreier formula gives rank(U_m)=m+1. Its inverse image V_m in Q_T has indexm and surjects onto U_m. Abelianizing over Q gives b_1(V_m)≥m+1. Because P_T has finite index in the Artin group and P_T surjects onto Q_T, the same inverse-image construction proves unbounded virtual b_1 for the Artin group.

## What this excludes, and what it does not prove

All eight residual types have this property; merely establishing largeness or infinite virtual b_1 cannot separate one member of any of the four candidate pairs. This statement does not make virtual b_1 a general quasi-isometry invariant. The finite-index subgroups used here contain the kernel of Q_T→F2; they are not asserted to form a chain with trivial intersection. Thus the argument does not imply a positive L2-Betti number by a residual-chain approximation theorem.

The elementary distinction from rank-one spherical factors is essential: Q_(A1)=1 and has no such epimorphism. An all-Euclidean product of A1factors must be treated separately. The argument extends to any irreducible spherical type whose arrangement contains a rank-two localization with at least three hyperplanes; only the eight explicitly listed types are needed for the current filter.

No explicit quasi-isometry or noncommensurability proof for a residual pair is supplied. The exact missing task remains the four residual implications. It could be met by a valid large-scale distinguishing invariant, a shared geometric model combined with a commensurability decision, or a direct positive commensurability theorem.
