# Necessary conditions and the unresolved existence question

## Scope and notation

Let `(M,g)` be a nonempty closed three-dimensional Riemannian manifold of constant sectional curvature `-1`. The target asks whether some such manifold admits a foliation by surfaces minimal for **that hyperbolic metric**. A different ambient metric does not answer it.

The results below assume a smooth nonsingular codimension-one foliation. This is an explicit regularity hypothesis of these results, not a recovered regularity clause in the one-sentence K3 question. Leaves need not be compact except in Proposition 3. No global fibration, geometric-flow rule, or pointwise principal-curvature bound is assumed in Proposition 2.

Locally choose a unit normal `N`. Put `B(X)=nabla_X N` for leaf-tangent `X`, `s=tr(B^2)=|B|^2`, and `a=nabla_N N`. Integrability makes `B` self-adjoint. Minimality means `tr B=0`, so its eigenvalues are `lambda,-lambda` and `s=2 lambda^2`. Both `s` and `a` are unchanged by replacing `N` with `-N`; in particular `a` is globally defined even without coorientation. We use `Delta=div grad`, and the curvature convention `R(X,Y)Z=nabla_X nabla_Y Z-nabla_Y nabla_X Z-nabla_[X,Y] Z`.

## Proposition 1 Constant nonzero opposite principal curvatures are impossible

A minimal surface in a hyperbolic three-manifold cannot have principal curvatures `+1,-1` on a nonempty open set.

Proof. Choose a local orthonormal principal frame `e1,e2` on a sufficiently small patch, with `B e1=e1` and `B e2=-e2`. Write `nabla^L_X e1=omega(X)e2` and `nabla^L_X e2=-omega(X)e1`, where `nabla^L` is the induced connection. The Codazzi equation in a space form gives

`(nabla^L_e1 B)e2 = (nabla^L_e2 B)e1`.

The left side is `2 omega(e1)e1`, and the right side is `2 omega(e2)e2`. Hence both coefficients vanish. The frame is parallel on the patch and its intrinsic Gaussian curvature is zero. The Gauss equation instead gives `K_L=-1+det B=-2`, a contradiction. This is local and requires no compactness. QED.

## Proposition 2 Global curvature balance and strict threshold crossing

For a smooth minimal foliation of a closed hyperbolic three-manifold,

`div_M a = s-2`, and `integral_M s dV = 2 Vol(M)`.

On every connected component, there are points with `s<2` and points with `s>2`. Each of those inequalities holds on a nonempty open set. Consequently such a foliation cannot have `|lambda|<=1` everywhere, cannot have `|lambda|>=1` everywhere, and cannot have geodesic normal trajectories everywhere.

Proof of the divergence identity. Set `T(X)=nabla_X N`. In a normal orthonormal frame at a point, covariantly differentiate `a^i=N^j nabla_j N^i` and commute derivatives. This gives the tensor identity

`div a = tr(T^2) + N(div N) + Ric(N,N)`.

Equivalently, in indices the derivative commutator is `nabla_i nabla_j N^i = nabla_j nabla_i N^i + Ric_kj N^k`. Since `N` has unit length, `T` has block matrix `[[B,a],[0,0]]` relative to `T L plus span(N)`. Thus `tr(T^2)=tr(B^2)=s`; importantly, the quantity is the trace of the square, not the full squared norm of `T`, which would also contain `|a|^2`. Minimality gives `div N=0`, and hyperbolicity gives `Ric(N,N)=-2`. Therefore `div a=s-2`.

The calculation is valid in local normal choices, and its two sides are independent of that choice. Integration of the global vector field `a` on a closed manifold gives the integral identity by the divergence theorem, including for a nonorientable manifold using its Riemannian density (or its orientable double cover).

Suppose on one connected component `s<=2`. Since `s-2` is continuous, nonpositive, and has zero integral, it is identically zero. This contradicts Proposition 1 on any leaf patch. The same argument excludes `s>=2`. Continuity supplies the asserted open sets. If `a=0`, the pointwise identity forces `s=2` and gives the same contradiction. QED.

Attribution. The integrated identity is a specialization of the classical second-mean-curvature formula `integral(2 sigma_2-Ric(N,N))=0`, since `sigma_2=det B=-s/2`. Rovenski and Walczak [RW17, introduction, equation (2)] explicitly state that formula and its earlier attribution. The argument above is supplied for transparent signs and hypotheses, not as a new integral formula.

## Proposition 3 A compact leaf with a product family must cross the threshold

Let `S` be a closed connected surface, and suppose `F:(-epsilon,epsilon) times S -> M` is a smooth embedding into a hyperbolic three-manifold, with every `F_t(S)` minimal. The ambient manifold need not be closed. For each leaf in this family, `s` takes values both below and above `2`.

Proof. Choose its unit normal so that the normal speed `u=<partial_t F,N>` is positive. This is possible because the differential of the three-dimensional embedding is nonsingular, its time derivative is transverse, and `S` is connected. Tangential reparametrization does not affect the linearization of zero mean curvature. The minimal-surface variation equation is

`Delta_S u + (s-2)u=0`.

This equation is the usual Jacobi equation, also recorded in [WW20, Proposition 3.1]. Integrating on the closed leaf yields `integral_S (s-2)u dA=0`. If `s-2` has one sign, positivity of `u` forces `s=2` identically. Proposition 1 excludes that. Thus there are points of both signs. QED.

The assumption of an actual product family is essential to this argument. A compact leaf of an arbitrary foliation need not have such a global product neighborhood; local foliation charts alone do not provide a globally defined positive `u` on it. We do not silently remove that hypothesis.

## Proposition 4 A standard hyperbolic-space foliation cannot descend compactly

In the upper half-space model `H^3={(x,y,z):z>0}`, with metric `z^(-2)(dx^2+dy^2+dz^2)`, the planes `P_t={x=t}` give a smooth foliation by totally geodesic minimal surfaces. No group of hyperbolic isometries permuting all these planes acts freely and properly discontinuously with compact quotient.

Proof. The unit normal is `N=z partial_x`. Direct covariant differentiation gives `B=0`, `a=z partial_z`, and `div a=-2`, agreeing with Proposition 2 before integration. The leaves are also totally geodesic because reflection in each vertical Euclidean plane is a hyperbolic isometry fixing it.

For completeness, the foliation admits positive normal speed `u=1/z`, and on each plane `Delta_P u=2u`. Thus its local Jacobi equation with `s=0` is satisfied. Compactness of the leaf is genuinely absent from Proposition 3.

The ideal boundaries of any two distinct `P_t` intersect only at the point at infinity. Any isometry permuting all the planes therefore fixes that ideal point. An isometry fixing infinity has half-space form `(v,z) -> (c Q v+b,c z)` with `c>0`, `Q` orthogonal, and `v=(x,y)`. Consequently the vector field `V=z partial_z` is invariant under every such isometry. It would descend to any smooth quotient. Its divergence is

`div V = z^3 partial_z(z^(-3) z) = -2`.

On a nonempty closed quotient its integral would be both zero and `-2 Vol`, a contradiction. QED.

This only rejects this explicit family and its isometric images. It does not reject every minimal-plane foliation of hyperbolic space, and does not provide a general equivariance obstruction.

## Exact remaining gap

The curvature-balance identity permits sign-changing `s-2`; nothing proved here eliminates that case. The compact-family argument gives another necessary sign change, not a contradiction. General foliations can have noncompact leaves and need not be fibrations. Their local positive Jacobi functions need not assemble into a globally defined function or a closed transverse coordinate. A construction would need a foliation invariant under a cocompact lattice, not merely a local family in hyperbolic space. Conversely, a complete negative answer must exclude those possibilities without adding compact-leaf, geometric-speed, geodesic-normal, or curvature-pinning assumptions. No such construction or exclusion has been established in this investigation.
