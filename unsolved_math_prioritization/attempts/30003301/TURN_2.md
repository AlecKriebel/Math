# Substantive turn 2: a nonabelian smooth-section obstruction

**Partial, unreviewed. The original positive relation-lifting question remains unresolved.** Date: 2026-10-01. This turn produces an exact obstruction beyond the abelian lattice from turn 1 and a relative disk example showing why continuous extension is insufficient. It does not produce a positive relation of the identity on the closed surface.

## 1. Precise current input

The full preprint [Hillman–Pedrotti, arXiv:2604.10943v1](https://arxiv.org/pdf/2604.10943v1), dated 13 April 2026, was read, including the proofs of Theorems 3.12, 3.14 and 3.19 and the concatenation Lemmas 3.17–3.18. This is a preprint, not a claim of a peer-reviewed publication. Its one-critical-point result distinguishes two types of boundary extension:

- A continuous section can use any integer power of a based vanishing cycle, within its twisted-conjugacy class.
- A section avoiding the critical point uses one of the two smooth local types, corresponding to powers 0 and 1 in the paper's convention.

The relevant condition is existential over the allowable representations. A representation with an integer outside {0,1} does not itself prove nonsmoothability if another representation with an allowed integer exists. The construction below rules out *all* such alternative representations using an explicit quotient.

The overline on the last loop in the source formula denotes path reversal. It must not be dropped when reading extracted text. The relevant expression is

    alpha = zeta V^m phi^(-1)(zeta^(-1)),                 (1)

where phi is the vanishing-cycle twist's action on the based fundamental group. The inverse in phi reflects the paper's mapping-torus convention. Both twists and sections here are positive/chiral; no mixed-sign example is being imported.

## 2. Genus-two separating model and exact quotient

Let S be a closed genus-two surface, with

    pi_1(S,p) = <a,b,c,d | [a,b][c,d] = 1>.

Let V separate its two one-holed tori and take its based class to be v=[a,b], with orientation chosen to match the local convention. A Dehn twist about V fixes the first torus's generators and conjugates the other torus's generators by v or v^(-1), depending on the chosen positive-twist action convention. Either choice gives the same quotient computation below.

Use the integral Heisenberg group H of triples (x,y,z), with multiplication

    (x,y,z)(X,Y,Z) = (x+X, y+Y, z+Z+xY).

Put X=(1,0,0), Y=(0,1,0), Z=(0,0,1). Then [X,Y]=Z, and Z is central of infinite order. Define

    rho(a)=X,  rho(b)=Y,  rho(c)=Y,  rho(d)=X.

This descends to the surface group because [X,Y][Y,X]=1. Moreover rho(v)=Z. Since rho(v) is central, conjugating c and d by v or its inverse does not change their images. Hence

    rho composed with phi = rho,
    rho composed with phi^(-1) = rho.                    (2)

For every possible based loop zeta, (1) and (2) therefore imply

    rho(zeta v^m phi^(-1)(zeta^(-1))) = Z^m.              (3)

This is a universal group calculation, not an inference from finite testing.

## 3. Relative counterexample to the smooth-extension shortcut

Take the positive Lefschetz fibration over a disk with closed genus-two regular fiber and one separating vanishing cycle V. Consider the boundary section whose fiber component is alpha=v^2. Such a boundary section exists by the mapping-torus construction, and it extends continuously over the critical disk by the m=2 local model.

For an explicit local expression, write the Lefschetz map as q(x,y)=xy. Then

    s_m(r exp(i theta)) =
      (sqrt(r) exp(i m theta), sqrt(r) exp(i(1-m) theta))

satisfies q composed with s_m = identity for every integer m and extends continuously to the node at r=0. This is equivalent to the local construction in Hillman–Pedrotti's Theorem 3.12 after the linear change from the sum-of-squares model. Its prescribed boundary class is the one used in (1).

If this boundary section had a smooth extension, that extension could not pass through the critical point: differentiating q composed with s = identity would contradict dq=0 there. The local smooth-section classification, including either component of the singular fiber away from the node, would therefore express alpha as (1) with m=0 or m=1 and some zeta. Applying rho would give Z^2 equal to 1 or Z, an impossibility. This rules out every twisted-conjugate alternative and both separating-curve component choices.

Thus alpha=v^2 admits a continuous extension but no smooth extension relative to that boundary class. It also has zero ordinary homology class in H_1(S;Z), because v is separating. It lies in the normal closure of the vanishing cycle and becomes trivial after collapsing that cycle. Ordinary homology and this collapse therefore miss the smooth obstruction.

This example is a credited application of the preprint's local section classification with a concrete quotient certificate. No historical-first claim is made.

## 4. How to use this beyond the local example

For a fixed disk factorization with vanishing cycles V_i, let psi_i be the inverse twist actions, in the source's convention. Suppose a quotient rho of the fiber group satisfies rho composed with psi_i = rho and each z_i=rho(V_i) is central. Applying rho to the ordered criterion of Theorem 3.19 shows that a smooth extension of the prescribed boundary class alpha requires

    rho(alpha) in { product_i z_i^(epsilon_i) :
                    epsilon_i in {0,1} }.               (4)

In contrast, continuous extension only gives the corresponding condition with arbitrary integer exponents. Condition (4) is necessary; no sufficiency claim follows from passing to a quotient. For separating twists in the genus-two model, the Heisenberg quotient has exactly the required properties. More general factorizations need a separately constructed compatible quotient.

This suggests a sharper test than the turn-1 abelian obstruction for a genuine sphere-base candidate: compute the boundary class supplied by its trivial cap, then seek a quotient satisfying (4) in which that class is excluded. One cannot choose the boundary class arbitrarily. In the local example the total monodromy is a nontrivial Dehn twist, so it cannot be capped by a product fibration to obtain the original closed-surface identity relation. Consequently the local example is **not** a counterexample to Korkmaz's question.

## 5. Exact remaining gap and checkpoint

No positive identity relation with an excluded cap class has been exhibited. No general proof has been given that cap classes always belong to the allowed ordered twisted-conjugacy set. The newer September seminar announcement is still only a scoped announcement and has not been used as a theorem here.

`turn_2_check.py` records exact integral quotient controls. They corroborate the explicit homomorphism and central-coordinate calculation; the universal argument is (2)–(3), not the number of tested triples.

Substantive author turns: **2/5**. Estimated completion toward a full solution: **5%**. The attempt remains active. Next: construct or evaluate an actual positive identity factorization, including its cap class, rather than only arbitrary boundary data; alternatively derive a universal mechanism controlling those cap classes. Separate review is still required for the partial results.
