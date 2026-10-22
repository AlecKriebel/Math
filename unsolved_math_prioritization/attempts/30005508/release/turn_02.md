# Approach 2: exact reduction to involutions on a central quotient

## Proposition

Let H be a finite group, x a central 2-element, y²=x, and Z=⟨x⟩. Let b be a real nonprincipal 2-block of H with one simple module S and defect pair (P,Q), where Z≤P. Let bar b be its dominated block of bar H=H/Z, with simple module bar S. Set

C=C_H(y), K={h∈H:y^h∈yZ}, L=C/Z,
t=[K:C].

Then t∈{1,2}, and, writing bars for images modulo Z,

[k[y^H]:S] = t [k[bar y^{bar H}]:bar S],  (2)

|y^H∩(Q\P)| = t |bar y^{bar H}∩(bar Q\bar P)|.  (3)

If x≠1, bar y is an involution. Thus the desired formula for this root is equivalent to the involution formula for bar b and bar y.

## Central quotient and block facts

Every simple kH-module is trivial on the normal 2-subgroup Z. For a central 2-subgroup, quotienting induces the standard block correspondence; bar b has the same number of simple modules and is real and nonprincipal. Its defect pair is (P/Z,Q/Z). The corresponding extended-defect quotient fact is used explicitly in Sambale's proof of Theorem 13 in *Real characters in nilpotent blocks*, citing Murray's real-subpair quotient lemma.

These facts do not assert that ordinary projective characters can simply be inflated unchanged. Their degrees generally change. The proof below instead uses composition multiplicities of permutation modules, avoiding that potential error.

## Centralizer calculation

By definition K/Z=C_{bar H}(bar y). Since x=y² and x is central, any h∈K sends y to yx^j and fixes x. If x has order 2^n with n≥1, squaring gives x^{2j}=1. There are only two possible values of x^j, namely 1 and x^{2^{n-1}}. Conjugation on ⟨y⟩ therefore has kernel C and image of order at most 2. Thus C is normal in K and t∈{1,2}. For x=1, Z=1 and K=C, so t=1.

In particular,

L ◁ C_{bar H}(bar y),
C_{bar H}(bar y)/L ≅ K/C,

and this quotient is a 2-group. The equality of centralizers after quotienting is not automatic: it can fail by exactly this factor t.

## Proof of the multiplicity identity

Z acts trivially on y^H. As a bar H-set this orbit is bar H/L. Consequently its permutation module is

Ind_L^{bar H} k = Ind_{C_{bar H}(bar y)}^{bar H}(Ind_L^{C_{bar H}(bar y)} k).

The inner permutation module is inflated from the regular module of the group K/C of order t. In characteristic 2 every composition factor of that module is trivial, and there are exactly t of them. Induction is exact. Hence in the Grothendieck group of finite-dimensional k bar H-modules,

[k[y^H]] = t [k[bar y^{bar H}]].

Taking the coefficient of bar S proves (2). Approach 1 converts these coefficients to the relevant restricted projective-character multiplicities.

## Proof of the intersection identity

The natural map y^H→bar y^{bar H} is onto. Its fiber over bar y has size [K:C]=t; equivariance makes every fiber have the same size. Because Z≤P≤Q, if an image orbit element is in bar Q\bar P, all its lifts in y^H lie in Q\P. Conversely, any y^H element in Q\P maps there. Counting these complete fibers proves (3).

## Application to the original problem

Take H=C_G(x), P=C_D(x), and Q=C_E(x). A subsection has x∈D and x∈Z(H), so Z≤P. If b is nonreal, Approach 1 already proves the formula. If b is real, it is nonprincipal: a principal local block would induce the principal global block by Brauer's third main theorem. Thus the proposition applies.

For x≠1, the order of y is twice the order of x, and bar y has order 2. For x=1, the question already is the involution formula, apart from the identity root handled in Approach 1.

It follows that the universal local square-root conjecture is equivalent to the universal real-nonprincipal, one-simple-module involution-orbit conjecture. One direction is specialization to x=1; the other is the central-quotient reduction plus the known nonreal vanishing case. This equivalence does not prove either universal conjecture.

## Exact sanity checks and stopping point

For H=D₈=⟨r,s:r⁴=s²=1,srs=r⁻¹⟩, x=r² and y=r, the multiplier is 2. For H=C₈, x=r² and y=r, it is 1. The exact script verifies both orbit-fiber calculations. These examples validate the group-theoretic factor; they are not purported nonprincipal block examples.

The strategy ends at Sambale's still-conjectural involution-orbit statement. In particular, dropping t or identifying C_H(y)/Z with C_{H/Z}(yZ) would produce an invalid proof.
