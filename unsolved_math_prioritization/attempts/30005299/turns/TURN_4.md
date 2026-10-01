# Substantive turn 4: singular extension and the rank-drop boundary

2026-10-01 06:05–06:08 UTC. Status: partial theorem for a larger intrinsic class, unreviewed. Full-target estimate: 60%. This turn does not assume smoothness, reducedness or normality, but it isolates an additional rank-one-presentation condition rather than pretending it holds for all Weddle quartics.

Let X be a quartic hypersurface scheme in P^3_C and H=O_X(1). Say a line bundle L has a linear quartic presentation if

    0 -> O_P3(-1)^4 --M--> O_P3^4 -> i_*L -> 0

is exact. For this turn that displayed condition is the definition used; no smooth-only theorem is silently applied to singular schemes. The determinant of M is a nonzero scalar multiple of the quartic equation. At every closed point of X, M has rank three, because its cokernel is the fiber of a line bundle, of dimension one. Conversely, rank three everywhere on X for a linear determinant representation ensures its cokernel is a line bundle: locally a 3-by-3 minor is invertible, reducing the presentation to diag(1,1,1,f).

## Intrinsic rank-one-presentation characterization

**Theorem.** The following conditions are equivalent.

A. X has a Weddle representation whose gradient matrix has rank three at every closed point of X.

B. X admits an involution sigma (fixed points now allowed) such that L=sigma^*H has a linear quartic presentation, and the canonical factor-exchange action of sigma on H^0(H tensor sigma^*H) has trace zero.

The involution and its action are intrinsic to the polarized scheme. It is not enough that some arbitrary determinant matrix pass a representation-dependent test.

### A implies B

The bilinear equations y^T A_j x=0 define the graph of a morphism X -> P^3, since their coefficient matrix has constant corank one. This is true scheme-theoretically: in the open set where a 3-by-3 minor is invertible, three coordinates of y are uniquely solved in terms of the fourth, and the remaining equation is the local defining equation f of X. The nonzero fourth coordinate gives the local graph chart. These charts cover X.

Symmetry of A_j makes the graph invariant under interchange of x and y. Therefore its two projections are isomorphisms to X and the resulting map sigma is an involution, even if X is singular or nonreduced. As in turn 3, the evaluation map of the cokernel line bundle L is this morphism, giving L=sigma^*H.

Twisting the linear presentation gives a surjective multiplication map from a 16-dimensional space onto H^0(H tensor L), with four-dimensional kernel K and no higher cohomology. Its kernel consists of the four symmetric bilinear equations. The domain has exchange eigenspace dimensions ten and six; the quotient therefore has dimensions six and six. Its trace is zero. This argument replaces the smooth fixed-point-free Lefschetz step and allows fixed points at singularities.

### B implies A

Use a basis of H^0(H) and its sigma-pullback as bases of the two factors. The linear presentation of L supplies the four-dimensional bilinear relation space K of the graph. Its multiplication quotient has dimension twelve. The stipulated trace zero gives quotient eigenspace dimensions six and six, hence K has plus dimension four and minus dimension zero. Every relation is symmetric. Writing them as y^T A_j x therefore gives four independent quadrics q_j=x^T A_j x/2 whose gradient determinant defines X. The presentation is a line-bundle presentation, so the matrix has rank three at every point of X. This proves the equivalence.

## Exact boundary obstruction: this still does not cover all source quartics

Take four independent quadrics

    q_0=x_0^2/2, q_1=x_0 x_1, q_2=x_0 x_2, q_3=x_0 x_3.

Their gradient matrix is

    [ x_0  x_1  x_2  x_3 ]
    [  0   x_0   0    0  ]
    [  0    0   x_0   0  ]
    [  0    0    0   x_0 ]

and its determinant is x_0^4. Thus the quadruple plane really occurs as a Weddle quartic scheme, with no dependence among the quadrics. Along its reduced support x_0=0 the matrix has rank one, so its polar incidence fiber is P^2 rather than a single point. The cokernel is not a line bundle. The source's unrestricted quartic wording does not allow this valid example to be discarded merely because the smooth argument fails there.

Similarly the four quadrics x_j^2/2 have Weddle determinant x_0 x_1 x_2 x_3. Along intersections of coordinate planes the rank drops by at least two. These are explicit reduced examples of the same obstruction. Smoothness of the determinant in turn 3 was a genuine hypothesis, not a generic convenience.

These examples show that a **given** valid Weddle presentation can fail the rank-one-presentation condition. They do not prove that the same hypersurface cannot possess a different everywhere-corank-one Weddle presentation. No such inference is made. Classifying possible alternative presentations remains part of the missing full argument.

## What remains

The graph/involution route now gives an exact characterization whenever an everywhere-corank-one Weddle presentation exists. For unrestricted quartics one must handle torsion-free or more general Cohen–Macaulay cokernels with higher-dimensional fibers in the polar incidence scheme. Merely replacing a graph by a symmetric bilinear correspondence recovers the starting tensor formulation and does not solve that classification. This route is blocked at that precise extension unless a new intrinsic condition on these singular sheaves/correspondences is proved.

The fifth turn will independently certify the size and generic finiteness of the actual Weddle locus and audit the possible confusion between its projective closure and its set of realized equations. Neither a dimension count nor a closure-membership test will be advertised as a full boundary classification.
