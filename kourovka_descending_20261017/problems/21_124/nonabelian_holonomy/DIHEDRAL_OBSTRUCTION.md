# Pell candidate: all finite dihedral holonomy is excluded

UTC: 2026-10-24T22:38:46Z. **Proposed partial theorem, awaiting a fresh adversarial audit.** No original-solution or priority claim is made for Kourovka 21.124. Estimated discovery completion remains **4%**.

Let

\[
G=\langle a,b,t,s_1,s_2,s_3\mid[a,t]=[b,t]=1,\quad
s_i(a^{p_i}t)s_i^{-1}=b^{q_i}t\rangle,
\]

where \((p_i,q_i)=(3,2),(20,14),(119,84)\). The distinct preceding reviews verify that this group is CAT(0) and F5-by-Z. This note uses only its presentation and the already reviewed abelian-holonomy lemma.

## Exact new claim

There is no homomorphism \(G\to\mathbb R^N\rtimes Q\), injective on either displayed rank-two vertex group, when the finite orthogonal linear action of \(Q\) decomposes into invariant real summands of dimensions at most two. In particular, this excludes **every finite dihedral group, of arbitrarily large order**, in arbitrary Euclidean dimension and with arbitrary original affine cocycles and vertex rotational parts.

It does not exclude a representation having an irreducible real summand of dimension at least three. It therefore does not establish a counterexample to 21.124.

## Powers and orthogonal summands

Choose a positive common multiple M of the orders of the linear parts of a,b,t. Their Mth powers are translations; let their vectors be A,B,T. The commuting vertex generators give

\[
(a^{p_i}t)^M=a^{Mp_i}t^M,\qquad
(b^{q_i}t)^M=b^{Mq_i}t^M.
\]

Conjugation of a translation by an affine isometry acts on its vector by the linear part. Consequently

\[
 S_i(p_iA+T)=q_iB+T.\tag{1}
\]

This argument does not assume that the original images of a,b,t are translations. After averaging an inner product over Q, orthogonal projection onto any invariant summand commutes with the S_i, so (1) holds on each summand.

One-dimensional summands are covered by the reviewed abelian-holonomy result. Consider a two-dimensional invariant real plane, identified isometrically with C. Every finite subgroup of O(2) is cyclic or dihedral: its determinant-one subgroup consists of rotations, is finite cyclic, and any reflection multiplies that subgroup to the determinant-minus-one coset. If the S_i on this plane all preserve orientation, they commute and are already excluded by the reviewed abelian result. Otherwise, each acts either as z↦lambda_i z (rotation) or z↦lambda_i conjugate(z) (reflection).

Change the complex coordinate by a unit scalar so that the first reflection has phase 1. The other reflection phases become their ratios with this phase, while the rotation phases remain unchanged. Each resulting phase is a root of unity: rotations have finite order, and products of two reflections are finite-order rotations. Thus the other two phases x,y are roots of unity. This normalization does not assume that an unnormalized reflection phase was a root of unity.

## The seven exact determinants

Use complex coordinates ordered A,conjugate(A),B,conjugate(B),T,conjugate(T). A rotation with phase lambda contributes

\[
 p\lambda A-qB+(\lambda-1)T=0,
\quad p\lambda^{-1}\bar A-q\bar B+(\lambda^{-1}-1)\bar T=0.
\]

A reflection contributes

\[
 p\lambda\bar A-qB+\lambda\bar T-T=0,
\quad p\lambda^{-1}A-q\bar B+\lambda^{-1}T-\bar T=0.
\]

These give a 6-by-6 Laurent-polynomial matrix for each of seven patterns epsilon in {0,1}^3 other than (0,0,0), where 1 denotes reflection. The first reflection has phase 1 and the remaining indices, in increasing order, have phases x,y. `dihedral_determinant.py` constructs these equations and expands all 720 determinant permutations using exact integer polynomial arithmetic. Every complete coefficient list is in `dihedral_determinants.json`.

For example, for three reflections the determinant is

\[
5712\{4(x+x^{-1}+x/y+y/x)-3(y+y^{-1})-10\}.
\]

The determinant has seven nonzero monomials for patterns 001,010,100,111, and nine for 011,101,110. This is not a numerical determinant calculation.

## A finite certificate bounds every torsion order

Suppose one of these determinants vanishes at a root-of-unity pair (x,y). Partition its 7 or 9 nonzero rational-coefficient terms into minimal vanishing subsums. For each block, Mann's bound states that all ratios of its root-of-unity monomials have orders dividing the product of the primes at most the number of terms in that block. This product always divides 2·3·5·7=210. The earlier abelian-holonomy note gives a self-contained proof of precisely this rational-coefficient minimal-relation bound. Primary reference: H. B. Mann, *On linear relations between roots of unity*, Mathematika 12 (1965), 107–117, [DOI](https://doi.org/10.1112/S0025579300005210).

The following necessary tests discard impossible blocks:

* a singleton cannot vanish;
* the maximum coefficient magnitude cannot exceed the sum of the others;
* in a two-term block the magnitudes must agree;
* in a three-term block the magnitudes must either all agree or one must be the sum of the other two.

The final test follows from Mann's relative-order-six bound for three terms: after rotation they lie in the six sixth-root directions. Resolving along the rational basis 1,zeta_6 shows that a noncollinear three-term relation has equal magnitudes; a collinear one has one magnitude equal to the sum of the others.

`dihedral_partition_bounds.py` visits **every set partition** of the actual monomial indices and keeps every partition whose blocks pass these necessary tests. It does not presume the tests sufficient, so it may keep extraneous partitions. For each kept partition it forms the integer lattice generated by all exponent differences within each block. It computes the gcd of all its 2-by-2 minors, and verifies **rank two and lattice index one for every kept partition**:

| Reflection pattern | Terms | Kept partitions | Rank/index for every kept partition |
|---|---:|---:|---|
|001|7|12|2 / 1|
|010|7|4|2 / 1|
|011|9|131|2 / 1|
|100|7|4|2 / 1|
|101|9|131|2 / 1|
|110|9|111|2 / 1|
|111|7|12|2 / 1|

The standard lattice-index formula used here is elementary: for a rank-two integer column span, its index in Z² is the gcd of its maximal minors, equivalently the product of the Smith invariants. Thus the exponent differences span Z². Mann says that the 210th power of the monomial corresponding to every such difference is 1. Integer combinations giving (1,0),(0,1) then show

\[
 x^{210}=y^{210}=1.\tag{2}
\]

This rank/index step excludes positive-dimensional torsion families and is essential. A bounded root search alone would not prove (2).

## Exact cyclotomic zeros and conclusion

`check_dihedral_torsion.py` constructs Phi_210 by exact polynomial division of X^n-1 by previously constructed divisor cyclotomic polynomials. It represents all powers of zeta_210 by their 48 integer coordinates. For each determinant it checks all 210² pairs, screening modulo 421 via the primitive-order-210 element 4, and evaluates every modular survivor exactly in Z[zeta_210]. It verifies the polynomial relation at 4, so nonzero modular values rigorously exclude a complex zero. The complete exact output is `dihedral_torsion_results.json`.

For **each of the seven patterns**, the only zero is x=y=1. At that pair all three matrices on this plane are either the identity or ordinary complex conjugation; they commute. The previously reviewed abelian-holonomy argument therefore gives A=B=0 on this plane, including the determinant's singular case. The argument applies on all invariant summands, so A=B=0 globally. Thus the images of a^M and b^M are identity; no injectivity on either vertex group is possible.

For an abstract finite dihedral group, every real irreducible representation has dimension one or two: decompose the finite cyclic rotation subgroup into complex characters, pair each character with its inverse under a reflection, and take the resulting real lines or planes. Hence the stated all-dihedral consequence follows in every dimension.

## Reproduction and exact outstanding gap

Run with any standard-library Python3:

    python3 dihedral_determinant.py
    python3 dihedral_partition_bounds.py
    python3 check_dihedral_torsion.py

The signed permutation searches in this folder are a separate bounded family, not premises of this theorem. Neither the dihedral proof nor those searches control arbitrary higher-dimensional irreducible finite-group representations. The exact remaining unsupported assertion would be that no such higher-dimensional representation has a horizontal solution of (1). No proof of that assertion is claimed; no paper, Zenodo upload, solved_verified status, or tracker entry is justified by this note.
