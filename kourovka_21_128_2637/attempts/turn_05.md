# Turn 5 of 5: normalized L2 homology and the commensurator torsion obstruction

## Last two routes and verdict
Try a genuine multiplicative finite-index invariant, then the abstract commensurator mechanism that succeeds against D4. The L2 invariants reproduce the Euler ratio and do not contradict it. The commensurator route isolates a sufficient obstruction, but the required claim about Comm(G_F) is not established. KOU-21.128 remains unresolved after five substantive attempts.

## L2 homology: all entries computed, no missing lower-degree obstruction
The projective reflection complement for Q_F or Q_H is a deconed affine hyperplane complement of rank three. It is aspherical. Davis–Januszkiewicz–Leary, Theorem A / Theorem 6.2, proves that only the rank-degree L2 Betti number of an affine hyperplane complement can be nonzero. Its alternating sum is the Euler characteristic. Applying the theorem and the turn-1 Euler values gives

b_i^(2)(Q_F)=0 for i!=3, b_3^(2)(Q_F)=240;
b_i^(2)(Q_H)=0 for i!=3, b_3^(2)(Q_H)=5040.

The affine arrangements have rank three because the original central reflection arrangements have rank four and their decones are essential. Here topological L2 Betti numbers are group L2 Betti numbers precisely because of asphericity; that identification would not be valid for an arbitrary arrangement without a K(pi,1) theorem.

Finite-index multiplicativity then yields

b_3^(2)(G_F)=5/12, b_3^(2)(G_H)=7/10,
b_3^(2)(K_F)=5, b_3^(2)(K_H)=42,

with all other degrees zero. For relative common-subgroup indices (42s,5s), both top L2 Betti numbers equal 210s. Thus the entire L2 Betti vector supplies no additional contradiction beyond turn 1. This does not assert that every L2-related invariant agrees.

The original Artin groups have an infinite central Z and virtually split off that factor; their L2 Betti numbers all vanish. Discarding the central factor was therefore essential even to see the Euler obstruction.

## An exact sufficient commensurator criterion
Soroko's Theorem 4 supplies an injection G_H -> Comm(G_H), and commensurable groups have isomorphic abstract commensurators. G_H contains an element of order 15, hence one of order 5. Consequently,

If Comm(G_F) has no element of order 5, then A[F4] and A[H4] are not commensurable.

This implication is rigorous. The premise is not proved here. Soroko's classification says G_F itself has torsion orders 2,3,4,6; it is not a classification of torsion in Comm(G_F). Replacing the latter by the former would invalidate the argument. Likewise, knowing an ordinary automorphism group is insufficient without a theorem that every virtual automorphism extends in the necessary way.

A somewhat different sufficient premise would be that the natural embedded G_F has finite index d in Comm(G_F), with 5 not dividing d. If an order-five subgroup existed in the commensurator, it would act freely on those d cosets: a stabilizer would embed it into a conjugate of G_F, which has no element of order five. That would force 5|d, a contradiction. Neither finiteness of this index nor its coprimality with five is established.

## Concrete warning: torsion can appear only virtually
Let F2=<x,y>. Its subgroup L=ker(F2->C14), with x mapping to 1 and y to 0, has index 14 and the free basis

x^14, y, xyx^-1, x^2 yx^-2, ..., x^13 yx^-13.

This basis has fifteen elements. Cyclically permuting it defines an automorphism alpha of L of order fifteen, hence a class in Comm(F2). This class has order exactly fifteen. Indeed a nontrivial power alpha^k, 0<k<15, moves a basis element u to a different basis element v. If it fixed some finite-index subgroup of L pointwise, that subgroup would contain a positive power u^n, forcing v^n=u^n. Free groups have unique roots, so v=u, a contradiction. Thus the torsion-free ambient group F2 has abstract commensurator torsion of order fifteen.

This example is not evidence that Comm(G_F) contains order five. It proves that the absence of ambient torsion alone cannot exclude such virtual torsion.

## Final state
No proof or counterexample to the original commensurability question has been obtained. The reusable partial outputs are explicit torsion-free covers, exact first-homology calculations, rejection of one Euler-minimal candidate, virtual-quotient constructions, and a precise unproved commensurator premise. The outstanding task is to compare arbitrary finite-index subgroups or to establish a genuine rigidity theorem for a relevant abstract commensurator. The five-turn budget is exhausted; literature retrieval, controls, packaging and independent audit are not additional proof-attempt turns.

## Credited input for this turn
Davis, Januszkiewicz and Leary, The l2-cohomology of hyperplane complements, Groups Geom. Dyn. 1 (2007), 301–309, Theorem A / 6.2: https://arxiv.org/abs/math/0612404
