# Independent candidate reconstruction

2026-10-12 16:04 UTC; completion estimate 25%; original proof-search attempts 0. This reconstruction precedes reading the frozen PROOF, historical audit, root claim ledger and current peer reports.

## Primary question and family

I independently downloaded the official three-page 1998 question article, rendered and visually inspected its printed p.126. Item 5(b), attributed to Satoru Shimizu, asks: “Does every small deformation of M admit a Hessian metric?” It requires compactness and deformation of affine structures. The hyperbolic case is identified as a separately known affirmative special case; the item does not impose hyperbolicity, fixed holonomy or a dimension lower bound.

I independently downloaded arXiv:math/0401257v2 and visually inspected printed p.20. Baues and Goldman explicitly give F_t(x,y)=(x,y+t x^2/2) as a differentiable one-parameter family of developing maps for complete marked affine tori. Their period coordinate is (0,-cube_root(t)); lack of differentiability of that coordinate at zero is explicitly contrasted with the differentiability of the affine family itself. The same family after t=s^3 is smooth even in this period coordinate.

## Global affine structure and completeness

Let X=partial_x and Y=partial_y be the global coordinate vector fields on the fixed torus, with the sole nonzero connection coefficient D_X X=tY. Torsion vanishes, and the only connection matrix sends X to tY and Y to zero; all curvature commutators and coefficient derivatives vanish. F_t is a polynomial diffeomorphism of R^2 with inverse F_-t and Jacobian determinant 1. Pulling back the standard affine connection gives precisely D_X X=tY.

F_t(x+m,y+n)=(u+m,v+n+tm u+t m^2/2) when (u,v)=F_t(x,y). Thus the integral translations in the source act by affine transformations in developing coordinates, with linear shear matrix [[1,0],[tm,1]]. Conjugacy by the developing diffeomorphism proves freeness, properness and compactness of the quotient and proves that F_t defines a developing map on the fixed marked torus. F_t need not descend to a diffeomorphism of the standard affine torus. It is a smooth compact-open-C-infinity family, and its polynomial inverse makes completeness immediate. Geodesics are globally defined: x=x0+as, y=y0+bs-(t a^2/2)s^2.

## All-metric obstruction

A locally Hessian positive metric is a smooth symmetric tensor g=A dx^2+2B dx dy+C dy^2 with periodic coefficients satisfying the Codazzi identity Dg in Sym^3. The connection terms give

(D_X g)(Y,X)=X(B)-g(D_XY,X)-g(Y,D_XX)=B_x-tC,
(D_Y g)(X,X)=A_y.

Hence B_x-A_y=tC. The global one-form alpha=g(X,.)=A dx+B dy satisfies d alpha=tC dx wedge dy. Stokes on the boundaryless compact torus gives t integral(C dx dy)=0. Positive definiteness implies C=g(Y,Y)>0 everywhere, so the integral is positive and t must be zero. The proof does not posit invariance, diagonal form, parallelness, proximity to the central metric or a family of metrics. It rules out every positive metric at every nonzero parameter.

At t=0, the standard Euclidean metric is locally Hessian with local quadratic potential. Requiring a global periodic potential would make the central example impossible, but is not the usual locally Hessian definition. On the universal cover, F_t^*(du^2+dv^2) exists but its B=tx component is not periodic. An indefinite metric 2 dx dy satisfies Codazzi for every t because C=0, and has the affine-coordinate potential uv-t u^3/3; it lies outside positive-definite Hessian geometry. D_t preserves dx wedge dy because its connection matrices have trace zero. Every affine gauge/diffeomorphism transports existence of a locally Hessian positive metric, so the result cannot be evaded by a new marking or atlas.

## Current result

The primary question and an all-metric counterexample appear compatible. No mathematical defect was found in this independent reconstruction. Whether this outcome had already followed from earlier theorems is separate and remains open in this reviewer record. The upcoming historical theorem-chain review must not replace the all-metric obstruction with a weaker nonexistence of parallel candidates.
