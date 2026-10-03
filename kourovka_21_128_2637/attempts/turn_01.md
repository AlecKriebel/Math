# Turn 1 of 5: quotient by the centre, Euler indices, and explicit torsion-free covers

## Target and verdict
Try to contradict commensurability by the centre, rational Euler characteristic, or finite-order elements. No contradiction is obtained. The calculation instead supplies necessary index ratios and two small, explicit torsion-free comparison groups. These are deductions from credited standard spherical-Artin/arrangement facts, not a novelty claim.

Write G_F=A[F4]/Z(A[F4]) and G_H=A[H4]/Z(A[H4]). Write Q_X=P_X/Z(P_X), where P_X is the pure Artin group. Cumplido–Paris Proposition 3.1 and Soroko Theorem 4 establish that the original question is equivalent to commensurability of G_F and G_H. Soroko Proposition 3 identifies Q_X as a finite-index subgroup of G_X and gives P_X=Q_X x Z. Thus quotienting the original centres is justified here; it is not an arbitrary cancellation of direct factors.

## Euler arithmetic
The reflection-arrangement Poincare polynomials are products (1+e_i t), where the exponents are (1,5,7,11) for F4 and (1,11,19,29) for H4. Deconing removes the factor (1+t). The projectivized arrangement complements are finite aspherical complexes for Q_X. Consequently

- P_QF(t)=(1+5t)(1+7t)(1+11t)=1+23t+167t^2+385t^3;
- P_QH(t)=(1+11t)(1+19t)(1+29t)=1+59t+1079t^2+6061t^3;
- chi(Q_F)=-240 and chi(Q_H)=-5040.

The Coxeter groups have orders 1152 and 14400 and centres of order two. The image of the pure group in the central quotient therefore has index 576 and 7200, respectively. Indeed the central generator Delta maps to -I, and the quotient G_X/Q_X is W_X/{+I,-I}. The rational Euler characteristics are

chi(G_F)=-240/576=-5/12,   chi(G_H)=-5040/7200=-7/10.

If isomorphic finite-index subgroups have indices i_F and i_H, multiplicativity gives 25 i_F=42 i_H. Thus i_F=42t and i_H=25t for a positive integer t. An unequal nonzero Euler characteristic is not a noncommensurability proof because the indices need not agree.

If those common subgroups are torsion-free, Soroko's torsion classification imposes 12|i_F and 30|i_H: a finite cyclic subgroup acts freely on cosets of a torsion-free subgroup, so its order divides the index. The orders 4,6 occur in G_F, and 6,10,15 in G_H. Hence 6|t, giving

(i_F,i_H)=(252k,150k),  k>=1.

This is necessary, not sufficient. No existence of an index-252 or index-150 subgroup is claimed.

## Explicit normal torsion-free covers
Use generators s1,s2,s3,s4 in the order of the path diagrams 3-4-3 and 5-3-3. The central words are Delta_F=(s1 s2 s3 s4)^6 and Delta_H=(s1 s2 s3 s4)^15.

For F4, send s1,s2 to 1 and s3,s4 to 0 in C12. Odd braid relations preserve these weights; the even middle braid relation has equal totals on both sides. Delta_F has weight 12, so this is a surjection alpha_F:G_F -> C12. Soroko's two basic torsion representatives are epsilon_6=s1 s2 s3 s4 and epsilon_4=s1 s2 s3 s4 s2 s3. Their weights 2 and 3 have orders 6 and 4 in C12. Every nonidentity torsion element is conjugate to a nonidentity power of one of these representatives. Hence ker(alpha_F)=K_F is torsion-free. Its index is 12 and chi(K_F)=-5.

For H4, send every generator to 1 in C60. The central word has length 60. The basic representatives epsilon_15, epsilon_10, epsilon_6 have lengths 4,6,10; their images have precisely orders 15,10,6 in C60. The same torsion classification shows K_H=ker(alpha_H) is torsion-free, has index 60, and chi(K_H)=-42.

The original question is now equivalently whether K_F and K_H have isomorphic finite-index subgroups. Such subgroups must have respective indices (42s,5s), by -5a=-42b. Intersecting a proposed commensurability witness with these two kernels can require refinement; these indices must not be confused with the universal torsion-free index bound above.

## What failed; next test
Centres and element orders distinguish the full groups but are deliberately removed by the explicit covers. Euler characteristic fixes a ratio rather than ruling it out. Next calculate H_1 of K_F and K_H exactly, and test whether any homological difference survives passage to arbitrary finite index.

## Credited inputs
- Cumplido–Paris, Commensurability in Artin groups of spherical type (2021), Proposition 3.1: https://ems.press/content/serial-article-files/39000?nt=1
- Soroko, Artin groups of types F4 and H4 are not commensurable with that of type D4 (2021; author corrected-reference file dated 12 June 2024), Proposition 3, Theorem 4, Theorem 7 and Table 1: https://sites.math.unt.edu/~soroko/ArtinFHD4.pdf
- Classical reflection-arrangement Poincare theorem and Coxeter exponent data. These numerical inputs are separately identified in SOURCES.md; the verification script checks the arithmetic, not these external theorems.
