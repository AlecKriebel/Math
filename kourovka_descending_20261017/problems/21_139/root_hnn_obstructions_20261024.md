# Rational coefficients and the partial-HNN completion barriers

Checkpoint 2026-10-24T16:38:30.666969+00:00. Full21.139 discovery estimate **12%**; no complete resolution or novelty claim.

## A checked coefficient-change diagnostic

Use the independently verified atoroidal example from approach_counterexamples.md, with free-fiber monodromy a↦b,b↦c,c↦ab. Its integral H1 matrix is

    M = [[0,0,1],[1,0,1],[0,1,0]],   det(M)=1,   M³=M+I.

A direct polynomial calculation gives M⁷−I=2M⁴. Therefore M⁷−I is injective over Z and Q, and its cokernel is (Z/2)³ because M⁴ is unimodular. For the degree-seven cyclic mapping-torus cover G7, the integral Wang sequence gives

    H2(G7;Z)=0,    H1(G7;Z)=Z⊕(Z/2)³.

The universal coefficient theorem, or the field Wang sequence, gives b2(G7;Q)=0 and b2(G7;F2)=3. The small exact reproduction is root_artifacts/verify_coefficient_change.py. A fresh independent reviewer derived the same unimodular identity.

This example retains hyperbolicity and virtual compact specialness, but does not satisfy bounded rational b2 over ALL covers; indeed the previously verified degree16 and112 covers have rational b2=1 and7. It refutes only a local change-of-coefficients shortcut from rational vanishing in a cover. It does not refute a possible implication using the entire global hypothesis of21.139.

For a finite two-dimensional K(H,1), integral H2 is a subgroup of the finite-rank free cellular C2 and is free abelian. If rational H2 vanishes, integral H2 is zero, and UCT identifies mod-p H2 with H1 p-torsion. Thus the rational all-cover hypothesis cannot be upgraded to mod-p all-cover vanishing by UCT alone; an additional torsion-control theorem would need proof. No such theorem is established here.

## Completing a partial automorphism is not the needed embedding

In a finite free-base HNN presentation with associated free factors A,B of equal rank k<r, their isomorphism can be extended to an automorphism of the free base F_r. Adding the missing conjugacy relations produces the complete mapping torus, hence a quotient of the partial HNN group. Britton normal form detects the omitted conjugacy relations as nontrivial before they are imposed. This naive completion is consequently not an injective construction. Linton's genuine embedding theorem uses a controlled enlarged free group instead.

Even a genuine quasiconvex retract embedding into a hyperbolic finite-rank-free-by-cyclic group provides only vb2(retract)≤vb2(overgroup). The overgroup's unbounded virtual b2 does not settle the retract's value. A new finite-cover mechanism is needed to force a class inside the original zero-vb2 group.

## Nonconjugate doubles remain possible

The companion retract_double_obstruction.md excludes only two distinct conjugates of one retract inside its retraction host. The genus-two surface double

    〈a,b,c,d | [a,b]=[d,c]〉

retracts onto 〈a,b〉 by c↦b,d↦a, while its two handle groups share their boundary commutator and are not conjugate copies. Its second homology is nonzero. This verified boundary example prevents extending the malnormality lemma into a ban on arbitrary abstract doubles.
