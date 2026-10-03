# Attempt 1 of 5: compare the two resolutions through common coefficients

**Verdict: NO RESOLUTION.** The argument proves equality for fields of the same characteristic and for groups admitting one common finite free resolution whose base changes resolve both trivial modules. It does not compare unrelated resolutions in different characteristics. These are standard reductions, not a novelty claim.

## Exact question and attempted strategy

Kourovka 21.71 asks for a group G of type FL(F1) and FL(F2) with different ordinary homological Euler characteristics. Type FL(F) means a finite resolution of the trivial FG-module F by finitely generated free FG-modules. The hoped-for negative proof is to compare the alternating free ranks of the two resolutions.

Let P be such a resolution, with P_i=(FG)^{n_i}. Tensoring over FG with the trivial right module F gives a finite chain complex of vector spaces with chain dimensions n_i and homology H_i(G;F). Rank-nullity, telescoped across the finite complex, gives

    chi_F(G) = sum_i (-1)^i dim_F H_i(G;F)
             = sum_i (-1)^i n_i.

Thus the characteristic is an integer and is independent of the chosen F-resolution. The issue is that this argument compares resolutions over a fixed ring only.

## Proposition 1: fields of the same characteristic cannot witness the problem

Let k be the common prime field of F1 and F2. The bar complex B_*(G;k), even when its chain spaces are infinite-dimensional, is a complex of k-vector spaces. Scalar extension is exact, so

    H_i(G;Fj) = Fj tensor_k H_i(G;k).

Dimensions over Fj equal dimensions over k, including infinite dimensions. The given FL conditions ensure that these dimensions are finite and vanish beyond finite degree. Consequently every Betti number, and therefore the Euler characteristic, is equal over F1 and F2.

This proof does NOT assert descent of FL from Fj to k. Homology descends in this sense; finite free resolutions need not descend. Leary's 2002 paper constructs groups FL over C but not over Q, so replacing the original problem by the assertion that the group is FL over both prime fields would be unjustified.

## Proposition 2: a common finite free complex forces equality

Suppose A is a commutative ring with homomorphisms to F1,F2 and there is a finite complex of finite free AG-modules P_i=(AG)^{n_i} whose scalar extensions are resolutions of Fj for j=1,2. Then both Euler characteristics equal sum (-1)^i n_i.

In particular, if G is FL(Z), the integral resolution can be base-changed to every field. Why is exactness preserved even at positive characteristic? The augmented integral resolution is exact as a complex of abelian groups, and all its successive kernels are subgroups of free abelian groups, hence free abelian. Each short exact sequence of successive cycles and free modules therefore splits over Z. Tensoring with any field preserves these exact sequences. A finite classifying space is a familiar sufficient condition, through the cellular chains of its universal cover.

The condition is weaker than requiring a finite classifying space: any free, cocompact, finite-dimensional G-CW complex which is acyclic over both fields also supplies one common cellular complex and forces equality. Thus a construction by a single finite-orbit complex that is simultaneously acyclic in the two characteristics cannot solve the problem.

## Attempted cross-characteristic transport and its failure

One might lift entries of an FpG-resolution to ZG and reduce the lifted complex modulo q. There are two separate unsupported steps:

1. Products of lifted differential matrices need not be zero integrally, although they vanish modulo p.
2. Even a genuine integral lift need not remain exact in the second field.

Neither finite generation nor the existence of a second, independent FqG-resolution supplies a chain homotopy equivalence over a common coefficient ring. The comparison theorem for projective resolutions only compares complexes over the same ring resolving the same module; applying it across characteristics begs the question.

## Torsion obstruction that really is available

If char(F)=p>0 and G is FL(F), then G has no element of order p. Restrict a finite projective resolution to a subgroup C_p. The group algebra FG is free over FC_p (possibly of infinite rank), so the restriction is still a finite projective resolution of the trivial FC_p-module F. But the standard alternating periodic resolution of C_p gives H^n(C_p;F)=F for every n>=0, contradicting finite projective dimension. This does not exclude torsion of orders invertible in F and does not prove that G is torsion-free.

## Remaining problem after this attempt

Only distinct characteristics need to be compared, and any positive example must escape all common finite-rank cellular/resolution models above. Excluding p-torsion from G does not exclude p-torsion or non-finite-generation phenomena in integral group homology. The next attempt studies exactly what universal coefficients do and do not force.
