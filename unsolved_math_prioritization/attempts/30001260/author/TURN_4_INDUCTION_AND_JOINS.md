# Turn 4: induction from S4 and stabilization by joins

## Attempt

Start with the smooth S4 rotation action on S(W)=S^2 from Turn 3 and enlarge the acting group to S5 by ordinary representation induction. Then try to repair isotropy by joins. Both steps can be evaluated exactly.

Let H=S4 fix the fifth letter and V=Ind_H^G W. Its dimension is 5*3=15. If f(g) is the number of fixed letters of g in the five-letter permutation action, then

    chi_V(g)=f(g)(f(g)-2) epsilon(g).

To derive this formula, identify G/H with the five letters. Each fixed coset contributes the W-character on the other four letters. This character is epsilon(g) times (f(g)-2). Summing over the f(g) fixed cosets proves the formula, including the value zero when there are no fixed cosets. The exact script also evaluates the defining induction sum over all 120 conjugators and verifies the formula independently.

It follows that chi_V(1)=15, chi_V(t)=-3, and chi_V(d)=-1. Hence

    dim V^E_A = (15-3)/4 = 3,
    dim V^E_B = (15-6-1)/4 = 2.

The induced sphere S^14 therefore contains an E_A-fixed S^2 and an E_B-fixed S^1. This is a concrete failure of the naive induction construction, not merely an appeal to the general obstruction.

## Why ordinary joins cannot repair it

For nonempty G-spaces X,Y with diagonal action on X*Y, each endpoint factor embeds equivariantly. Thus X^E embeds into (X*Y)^E regardless of whether Y^E is empty. At a point with join parameter strictly between 0 and 1, being fixed requires both coordinates to be E-fixed. Consequently

    (X*Y)^E is empty if and only if both X^E and Y^E are empty.

This endpoint issue matters: one must not incorrectly treat the join with an empty fixed set as automatically empty. A forbidden fixed set in the induced sphere survives every further join having that sphere as a factor. For representation spheres, the same fact is visible as S(V)*S(U) equivariantly homeomorphic to S(V direct_sum U), with fixed dimensions adding and never decreasing.

Joins of already rank-one-isotropy actions do preserve the isotropy condition. However a finite complex homotopy equivalent to a sphere is not thereby a manifold. An elementary nonequivariant test illustrates the missing implication: take a sphere with a closed whisker interval attached at one endpoint. The complex has the sphere's homotopy type. At the free endpoint its local homology vanishes. In a join with a sphere, a neighborhood of that endpoint is the product of this half-interval neighborhood with the cone on the sphere. The half-interval endpoint has zero local homology, so the product also has zero local homology. Thus the join is not a closed manifold at that point. Homotopy type plus joining does not provide the needed local manifold condition.

## Exact gap

These computations rule out induction and join stabilization as direct repairs of this linear S4 model. They do not rule out a nonlinear induced construction with subsequent controlled modifications, nor a special smooth realization of the known finite-CW example. Such modifications would need an additional theorem or explicit construction preserving rank-one isotropy and yielding a smooth sphere.
