# Attempt 5 of 5: the null-orbit boundary and realizable Jordan transitions

## Target and verdict

The final attempt tries to remove the nondegenerate-orbit hypothesis from Attempt 4 and to prohibit the algebraic transitions left by Attempts 1–2. Neither extension is completed. Two explicit calculations identify the surviving difficulty rather than hiding it: smooth Lorentz metrics on S³ genuinely can have degenerate principal tori, and smooth locally compatible pairs genuinely can pass through nontrivial Jordan collisions. A necessary matching condition at a nonstationary null torus is proved below.

## 1. A smooth global metric with degenerate principal tori

Let

h=dr²+sin²(r)dφ²+cos²(r)dψ²

be the round metric on S³, and let H=∂φ+∂ψ be the smooth unit Hopf field. On the principal interval put R=∂r. Choose a smooth function β(r) that is zero near both endpoints, equals π/2 on a nonempty interior interval, and crosses π/4 with nonzero derivative. Define

T=cos(β)H+sin(β)R,
g=h-2 h(T,·)⊗h(T,·).

The field sin(β)R vanishes near the coordinate singularities, so T and g extend smoothly to S³. Since T is h-unit, g has signature (-,+,+) everywhere. It is invariant under the standard torus action.

Set D=diag(sin²r,cos²r) and v=(sin²r,cos²r)^T. The orbit matrix is

G=D-2cos²(β) vv^T.

The matrix determinant lemma gives

det G=sin²r cos²r [1-2cos²β]=-sin²r cos²r cos(2β).

The full metric determinant in principal coordinates is always -sin²r cos²r. Hence when β=π/4, the orbit restriction degenerates but the ambient metric does not. The mixed radial-angular terms maintain nondegeneracy. Near the endpoints the orbits are Lorentzian; where β=π/2 they are spacelike.

This is not a projectively equivalent pair and is not an answer to the original question. It rigorously demonstrates why invertibility of G cannot be assumed or inferred just from compactness, torus symmetry, or smooth endpoint collapse.

## 2. A necessary matching condition at a null principal torus

Suppose g and gbar are T²-invariant and projectively equivalent near a principal torus r=r0. Let G_ab=g(Ka,Kb), where K1,K2 are the two invariant angular fields. Assume det G(r0)=0 and G'(r0) is not the zero matrix. Then the restrictions of g and gbar to this torus have the same one-dimensional radical.

Proof. Let W=grad_g r. At a degenerate orbit, W is a nonzero vector tangent to the orbit: it is perpendicular to the orbit and null, and the orbit has codimension one. In invariant coordinates, for angular indices a,b,

∇^g_(Ka) Kb = -(1/2)G'_ab W.

Indeed, all angular metric derivatives vanish, leaving only the radial derivative in the Christoffel formula. The projective one-form annihilates the angular fields, since the ratio of the metric volume densities depends only on r. Consequently the displayed covariant derivatives are the same for gbar.

Invariance of gbar gives Ka[gbar(Kb,Kc)]=0. Metric compatibility now implies

G'_ab ζc+G'_ac ζb=0,  ζc=gbar(W,Kc).

A nonzero row of G' forces ζ=0. Thus W belongs to the radical of gbar restricted to the orbit. In a nondegenerate Lorentz three-space, a degenerate two-plane has radical dimension one, so both radicals equal RW. ∎

In particular L preserves this null line and its g-orthogonal orbit plane: since g(W,·)=dr and gbar(W,·)=k dr for a nonzero k, the reconstruction formula makes W an eigenvector. This is a matching condition only. It does not give a nondegenerate complement or extend the inverse G^(-1) used in Attempt 4.

## 3. A genuine local compatible Jordan transition

Work in Minkowski three-space with constant metric η=diag(-1,1,1). Let x denote the position vector, q=η(x,x), and define

L=I+x⊗x^flat.

For any constant vector X,

∂_X L=X⊗x^flat+x⊗X^flat,
tr L=3+q,
d(tr L)=2x^flat.

These are exactly the compatibility equation. On q>-1, det L=1+q is nonzero, so

gbar=(1+q)^(-1)[η-(1+q)^(-1)x^flat⊗x^flat]

is a smooth metric projectively equivalent to η. In a neighborhood of the origin it is Lorentzian and nonproportional.

For q≠0, L is diagonalizable with eigenvalues 1,1,1+q. At a nonzero null point q=0, its nilpotent part N=x⊗x^flat has rank one and N²=0, giving Jordan type (2,1). At the origin L=I and d tr L=0, but L is not parallel on a neighborhood.

Thus an argument that treats real eigenvalue collisions or Jordan-type changes as intrinsically singular is false. Even vanishing of ∇L at a critical point does not by itself propagate affine equivalence. This example has neither compact S³ topology nor the required global extrema; it is a local consistency test, not a global construction.

## 4. Exact remaining problem

For arbitrary candidate metrics, one must still control global real-spectrum compatibility tensors across collision and Jordan-type transition sets. Even within standard torus symmetry, the remaining route passes through degenerate principal tori; the matching condition above is not a classification across them. No globally smooth nonproportional pair on S³ has been constructed, and no proof excluding every such pair has been obtained.

Five substantive attempts have now been written. The defensible outcome is partial progress with the original existence question unresolved, not solved and not already solved. The calculations here are elementary and fully reproducible; no historical novelty assertion is made.
