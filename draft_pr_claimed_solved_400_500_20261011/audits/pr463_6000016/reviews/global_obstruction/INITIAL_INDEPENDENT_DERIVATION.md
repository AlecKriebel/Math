# Independent global obstruction: initial derivation

Recorded 2026-10-12 15:53 UTC. Completion estimate: 35% of this verification family.

This derivation follows a read of the frozen candidate PROOF.md, SOURCE_GATE.md and README.md, but precedes any old audit verdict or new peer verdict. No such verdict has been read. It treats the candidate as a hypothesis and makes no novelty claim.

Let M=R²/Z², X=∂x, Y=∂y and D=D⁰+t dx⊗dx⊗Y. The sole nonzero connection coefficient is Γʸₓₓ=t. For an arbitrary smooth symmetric tensor g=A dx²+2B dxdy+C dy²,

    (D_X g)(Y,X)=B_x−tC,
    (D_Y g)(X,X)=A_y,
    (D_X g)(Y,Y)=C_x,
    (D_Y g)(X,Y)=B_y.

Thus the necessary Hessian Codazzi condition gives B_x−A_y=tC and C_x=B_y. The first identity alone is enough: α=g(X,·)=A dx+B dy is a global one-form, so dα=t C dx∧dy. Since C=g(Y,Y)>0 for every positive-definite g, Stokes gives 0=t∫M C dxdy, hence t=0. The lower-index covariant tensor has two minus connection terms; dropping one of them or using the upper-index sign would corrupt this calculation.

No invariance, parallelism, diagonal form, proximity to g₀, global potential, or smooth choice of g in t is required. In quotient coordinates A,B,C are periodic, whereas they need not be periodic in developing coordinates. All real nonzero t, including negative and arbitrarily small values, are excluded analytically.

An averaging verification gives the same central zero-mode obstruction. Coordinate translations preserve D because its coefficients are constant; averaging a hypothetical positive Codazzi g over the compact translation group preserves positivity and Codazzi and gives a constant tensor. Its first Codazzi equation reduces to t C̄=0 with C̄>0. This is a useful independent implementation of the argument, but is equivalent to integrating the displayed equation, not a second independent central theorem.

Negative controls: t=0 admits dx²+dy². For t≠0, 2dxdy is a global nondegenerate indefinite Codazzi tensor with C=0; in affine developing coordinates u=x, v=y+t x²/2 it is Hess(uv−t u³/3). The positive developing Euclidean tensor pulls back to (1+t²x²)dx²+2tx dxdy+dy², which is Hessian on the cover and satisfies B_x−A_y=t, but is not x-periodic and therefore does not descend. These controls separate positivity and global descent from local integrability.

Next checks: all curvature and tensor components, exact developing/holonomy/geodesic formulae, full printed target and scope, and symbolic corruption controls. This is verification of an existing complete candidate, not an additional original proof attempt.
