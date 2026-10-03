# Approach 1: orbit modules, aggregate indicators, and zero cases

## Aim

Translate the character formula to a modular multiplicity question, then test whether the established Frobenius–Schur identities already determine that multiplicity.

## Exact translation

Work over an algebraically closed field k of characteristic 2. Put H=C_G(x), P=C_D(x), Q=C_E(x), and IBr(b)={φ}. For a root y²=x, let M_y=k[y^H] be its conjugation-orbit permutation module. Its ordinary permutation character is

π_y = Ind_{C_H(y)}^H 1 = Ind_{C_G(y)}^H 1.

Projective/Brauer character duality and ordinary Frobenius reciprocity give

[M_y:φ] = ⟨Φ,π_y⟩_H = ⟨Res_{C_G(y)} Φ,1⟩_{C_G(y)}.

Here [M_y:φ] is composition-factor multiplicity, not the number of direct summands isomorphic to a simple or projective module. The equality holds because Φ is the projective character dual to φ and vanishes on 2-singular elements. In particular each term is a nonnegative integer.

Since every conjugate of y inside H still squares to x,

|y^H∩(E\D)| = |y^H∩(Q\P)|.

Thus the exact problem is

[k[y^H]:φ] = |y^H∩(Q\P)|.  (1)

## What the aggregate theory gives

Let Ω_x={y∈G:y²=x}; this is a disjoint union of H-orbits. By Sambale's published Lemma 4.1 in the dihedral paper,

[kΩ_x:φ] = Σ_{χ∈Irr(B)} ε(χ)d^x_{χφ}.

Therefore the left side of the aggregate square-root identity is the sum of the left sides of (1). Its right side is the sum of the right sides of (1). The scalar identity only fixes a total; it cannot determine an individual orbit. Even nonnegative integral vectors (2,0) and (1,1) have equal total. This numerical observation is an obstruction to this proof strategy, not a group-theoretic counterexample.

In particular, the known aggregate nilpotent abelian result in Proposition 4.2 cannot simply be relabelled a proof of the local orbit assertion. The same warning applies to the scalar solvable/nilpotent result.

## Complete zero cases

If no element of E\D squares to x, the final assertion of the cited Lemma 4.1 gives [kΩ_x:φ]=0. Every orbit multiplicity is nonnegative, so each is zero. All right sides in (1) are zero too. This proves the desired formula in this case.

If b is nonreal, its given defect pair satisfies Q=P. Any e∈E with e²=x centralizes x, hence lies in Q. Consequently there is no root in E\D and the preceding vanishing argument applies. This includes the nonreal local-block case without assuming b is real inadvertently.

For y=1, x=1 and b=B. Since the block is nonprincipal, Φ has no trivial ordinary constituent. Both sides are zero. More generally, when y is central in H and b is real nonprincipal, the left side is zero; a central element cannot lie outside P in a defect pair (P,Q), because such elements invert a nontrivial odd-order real-defect-class representative. Hence the right side is also zero.

## Outcome

Known zero cases are settled. The remaining case has b real and at least one root in Q\P. The obstacle is genuinely orbit-by-orbit, not a missing sign in the scalar indicator formula. The next approach reduces higher-order roots to involutions without losing this orbit information.
