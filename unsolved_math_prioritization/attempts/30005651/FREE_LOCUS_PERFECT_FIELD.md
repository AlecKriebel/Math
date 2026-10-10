# Free-locus connectivity over a perfect field: detailed reduction

Date: 2026-10-10. This is an authored formal reduction for independent checking; no novelty claim. All topology below is ordinary equivariant Nisnevich topology. The result does not assert connectivity on nonfree germs, and does not prove the original general nonabelian theorem.

## Statement

Let k be an infinite perfect field and G a finite constant group of order prime to char(k). Let E be a connective spectral sheaf on the usual smooth admissible G-site over k. Then L_mot E is connective at every ordinary equivariant Nisnevich point represented by a free G-scheme. Equivalently, the negative homotopy sheaves of L_mot E restrict to zero on the free subsite.

More locally, perfectness can be weakened: the argument applies to a free orbit germ whose image in its smooth quotient has residue field separably generated over k.

This is stronger than testing only G x U, and it does NOT assert that every free torsor is Nisnevich-locally split.

## 1. A coefficient-field presentation with an essentially smooth model

Let Q be a smooth k-scheme, y a point, A=O_{Q,y}, and F=k(y). Suppose F/k is separably generated. Let r=trdeg_k F and choose a separating transcendence basis bar(t_1),...,bar(t_r). Choose lifts t_i in A. Every nonzero polynomial in the t_i has nonzero residue, hence is a unit in A. Thus

K0=k(t_1,...,t_r) is a subfield of A,

identified under the residue map with k(bar(t_1),...,bar(t_r)) inside F. The extension F/K0 is finite separable.

Claim: A is essentially smooth over K0. Indeed, work in a smooth affine neighborhood in Q on which the t_i are functions. The classes of dt_i in Omega_{Q/k} tensor F are linearly independent: their images form a basis of Omega_{F/k}, because F/K0 is finite separable. The differential criterion for a map between smooth k-schemes now makes (t_1,...,t_r):Q -> A_k^r smooth near y. Passing to the generic point of A_k^r and then localizing gives the claim.

Form B=A tensor_{K0} F. This is finite etale over A. Reduction followed by multiplication gives

B -> F tensor_{K0} F -> F.

Let n be its kernel. Then B_n is an essentially smooth local F-algebra with residue field F. The local map A -> B_n is essentially etale and induces an isomorphism on residue fields, so their henselizations are canonically isomorphic over A:

S=A^h = (B_n)^h.

The right side supplies the desired compatible coefficient field F -> S, and at the same time proves that S is the henselization of an essentially smooth local F-algebra. There is no appeal here to a merely formal coefficient field, completion, or Popescu approximation.

For perfect k, every finitely generated residue extension F/k is separably generated, so this construction applies to every point of a smooth k-scheme.

## 2. The free torsor becomes constant over that coefficient field

Let X be free, and work equivariantly Nisnevich locally so the quotient Q=X/G is a scheme. It is smooth over k, since X -> Q is finite etale and smoothness descends. Fix y in Q and put S=O^h_{Q,y}. The corresponding equivariant henselian orbit scheme is

T=X x_Q Spec(S).

It is a finite etale G-torsor over S. Its closed fiber P_F=T x_S Spec(F) is a finite etale G-torsor over F. Use the coefficient field F -> S from Section 1. Finite etale algebras over a henselian local ring are equivalent to finite etale algebras over its residue field. That equivalence is fully faithful, hence also respects the G-action and the torsor isomorphism. It follows that

T = P_F x_F Spec(S)

as G-schemes over S.

This is a constant-torsor description over F, not a split-torsor description. P_F need not be G x Spec(F).

## 3. Restriction along the essentially smooth field extension

For separably generated F/k, extend E to essentially smooth objects by filtered-colimit evaluation and define E_F on smooth G-schemes over F by this evaluation. This agrees with restriction through finite-type smooth k-models: a smooth finite-presentation F-scheme and its finite G-action descend, after shrinking, to a smooth finitely generated k-subalgebra of F.

Nisnevich covers, their finite-presentation maps, and the equivariant residue-orbit splitting data likewise descend. Covers of a smooth F-object stay in the F-site. Therefore this restriction commutes with homotopy-sheafification and is t-exact; in particular E_F is connective.

For spectral Nisnevich sheaves the explicit formula

L_mot E(U) = realization_n E(U x Delta^n)

commutes with the same filtered-colimit extension and with restriction. Consequently

(L_mot^k E)_F = L_mot^F(E_F).

This is the localization/evaluation comparison needed here. It does not infer connectivity by evaluation at a field and does not assume equivariant stable connectivity.

## 4. Fixed-torsor restriction and Morel

For the fixed torsor P_F let

R_{P_F}(A)(U)=A(P_F x_F U)

on ordinary smooth F-schemes U. Every equivariant etale map V -> P_F x U descends to an etale map V/G -> U and is the pullback of that map. Equivariant Nisnevich covers correspond precisely to ordinary Nisnevich covers downstairs. Thus R_{P_F} commutes with sheafification of homotopy presheaves and is t-exact.

It also commutes with the singular construction, because products with Delta^n carry trivial G-action. Hence

R_{P_F} L_mot^F(E_F) = L_mot R_{P_F}(E_F).

This direct argument only needs quotient representability for etale maps over P_F x U; it does not need a global twist functor on every smooth G-scheme. On the admissible/quasi-projective site one can alternatively use the adjunction with X -> (P_F x X)/G.

By ordinary Morel over F, the right side is a connective ordinary Nisnevich spectral sheaf. Evaluate at Spec(S), the henselization of an essentially smooth local F-algebra from Section 1. A henselian local test is a point of the ordinary Nisnevich topos, so this evaluation is connective. Section 2 and the restriction comparison identify it with

(L_mot^k E)(T).

Thus every free equivariant Nisnevich stalk under consideration is connective, as claimed.

## 5. Limits of the conclusion

- This proof covers all free germs when k is perfect. It covers the indicated separably generated quotient-residue germs without perfectness.
- It does not handle all free germs over a general imperfect k: a smooth k-scheme may have inseparable residue extensions, and the coefficient-field construction above then need not exist.
- It does not address a germ with nontrivial geometric inertia. The general-G question remains open in this work.
- It does not use closed-point conservativity. The counterexample in APPROACH_1.md, Section 4.3 proves that closed-point tests are not conservative for arbitrary ordinary Nisnevich sheaves.
- The localization comparison rests on the spectral singular-construction argument spelled out in APPROACH_1.md, Section 2; no fixed-point or isovariant topology is substituted.

## Standard references used

- Morel, The Stable A1-Connectivity Theorems, Theorem 3 / 6.1.8: https://fangzhoujin.github.io/Morel_The%20stable%20A1-connectivity%20theorems.pdf
- Bachmann, A C2-equivariant Gabber presentation lemma, Proposition 3.2 and footnote 5 for the spectral singular mechanism: https://arxiv.org/abs/2310.08125
- Heller--Krishna--Ostvaer, Proposition 2.17 (cover criterion), Proposition 2.22 (points), and Proposition 6.10 (quotient henselization): https://arxiv.org/abs/1408.2348
- Stacks Project, finite etale categories over a henselian local ring, Lemma 10.153.7, Tag 04GK: https://stacks.math.columbia.edu/tag/04GK
- Stacks Project, henselization and its uniqueness/functoriality, Section 10.155, Tag 0BSK: https://stacks.math.columbia.edu/tag/0BSK

## 6. Application: punctured standard S3-representation over C

Let V be the two-dimensional standard representation of S3 over C, and let E be any connective ordinary equivariant Nisnevich spectral sheaf. The above free-germ result and the known C2 theorem together imply that the negative homotopy sheaves of L_mot E restrict to zero on V minus the origin.

Here is the pointwise argument on the full small equivariant Nisnevich site, including NONCLOSED scheme points. Take any equivariant etale U -> V minus the origin and any x in U. Let H=S_x be its set-theoretic stabilizer and let J be geometric inertia, equivalently the kernel of H -> Aut_C(k(x)). A geometric point above x maps equivariantly to a nonzero vector over an algebraically closed extension of C, so J is a subgroup of that vector's stabilizer. Indeed a 3-cycle has no eigenvalue 1 in the standard representation, and the fixed lines of two distinct transpositions intersect only at the origin. Thus J is either 1 or C2.

- If J=1, x lies in the scheme-theoretically free open subset. Section 4 proves connectivity at its equivariant Nisnevich henselian stalk.
- If J=C2, normality of J in H implies H is contained in N_{S3}(J). But a transposition subgroup of S3 is self-normalizing. Hence H=J=C2. The subgroup induction/restriction comparison from APPROACH_1.md, Section 3 then identifies this stalk with a stalk of an H-spectrum obtained from E. Bachmann's C2 connectivity theorem proves it connective.

These cases exhaust the points of EVERY equivariant etale object over the punctured representation. The resulting orbit-henselian points form a conservative family for its small equivariant Nisnevich site and detect the claimed vanishing. Points of the base representation alone are not asserted to form such a family. Every small-site germ not covered by this argument lies over the origin. This is a localization of the possible failure locus, not a proof that a failure occurs at the origin and not a proof of general S3 stable connectivity.
