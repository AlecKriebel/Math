# Independent mathematical audit: KP-3.18 / 2816

Verdict: ACCEPT the four scoped propositions in the exact author freeze. No mathematical repair is required. The unrestricted existence question remains unsolved; retain 3/5 approaches. This is an independent AI audit, not human peer review or a novelty determination.

## The target and the regularity boundary

The K3 statement asks for a closed hyperbolic three-manifold foliated by surfaces minimal in that hyperbolic metric. It does not require compact leaves, a fibration, geometric normal velocity, a principal-curvature bound, or a global transverse coordinate. The author makes transverse smoothness an explicit additional hypothesis of the propositions rather than silently importing it into the source statement. The arguments differentiate a unit normal transversely and therefore are not automatically valid for merely continuous or leafwise-smooth foliations. A change of ambient metric would change the problem.

The proof consistently uses B(X)=nabla_X N, not its negative, and R(X,Y)Z=nabla_X nabla_Y Z-nabla_Y nabla_X Z-nabla_[X,Y] Z. With these choices the hyperbolic Ricci tensor is -2g. Changing the sign of the shape convention would not change its squared norm or determinant in leaf dimension two, but the divergence calculation must still use a coherent convention.

## Proposition 1: the equality case

Distinct eigenvalues +1 and -1 admit smooth local orthonormal principal frames on sufficiently small leaf patches. The ambient space-form Codazzi equation applies to the induced shape tensor. Its two sides in that frame are respectively 2 omega(e1)e1 and 2 omega(e2)e2; their equality forces both connection coefficients to vanish. A parallel orthonormal frame on that patch gives intrinsic curvature zero. Gauss instead gives -1+(1)(-1)=-2. This contradiction is local and excludes an open patch with those constant principal curvatures, without leaf compactness or any global choice of frame. The proposition's heading mentions constant nonzero opposite curvatures more generally; the stated assertion and supplied proof concern the needed +1,-1 case. The same argument works for +c,-c with fixed c nonzero, but that extension is not needed for acceptance.

## Proposition 2: divergence, integration, and strictness

At a point use a normal ambient frame and differentiate a^i=N^j nabla_j N^i. The first differentiated factor gives (nabla_i N^j)(nabla_j N^i)=tr(T^2), where T(X)=nabla_X N. Commuting the remaining derivatives contributes Ric(N,N), while the noncommuted term is N(div N). Therefore

    div a = tr(T^2) + N(div N) + Ric(N,N).

Unit length forces the normal row of T to vanish. Integrability makes the leaf block B symmetric, and the remaining column is a. Hence tr(T^2)=tr(B^2)=s. Replacing this by the Hilbert-Schmidt norm of T would introduce an erroneous |a|^2; the author does not make that mistake. Minimality gives div N=tr B=0, so the result is div a=s-2.

On an overlap, two local unit normals differ by a locally constant sign. Thus nabla_(-N)(-N)=nabla_N N and a is a well-defined smooth global vector field, even when the normal line bundle is nontrivial. The scalar s is invariant too. No global coorientation is needed. On a nonorientable manifold the density divergence theorem gives zero integral, or one can pull everything to the orientation double cover and divide both volume integrals by two. The same argument can be performed on every connected component separately. Closedness excludes boundary flux and ensures finite volume; it is not interchangeable with completeness alone.

It follows that integral s=2 Vol. If s were everywhere at most 2 on one component, the continuous nonpositive function s-2 with zero integral would vanish identically. Likewise for s at least 2. The resulting s=2 gives principal curvatures +1,-1 on every sufficiently small leaf patch and contradicts Proposition 1. There must therefore be points, and by continuity nonempty open sets, of both strict signs in each component. Since s=2 lambda^2, this is exactly crossing of principal-curvature magnitude 1. It is an ambient-component conclusion, not a conclusion about each noncompact leaf. The special case a=0 would force s=2 pointwise and is correctly excluded.

The integrated identity is classical. The author correctly attributes its second-mean-curvature form to the literature and claims no new integral formula.

## Proposition 3: what a compact product family adds

A smooth three-dimensional embedding F:(-epsilon,epsilon) x S -> M has nonsingular differential. Its time vector projects to a nowhere-zero normal vector along each leaf. Normalizing that projection constructs a global normal and a positive normal speed u on the leaf. This works even without orientability of the ambient manifold or of S: the product family itself supplies the trivial normal line. Positivity and connectedness remove any sign ambiguity.

Differentiating zero mean curvature gives Delta u+(|B|^2+Ric(N,N))u=0. With the author's Laplacian and Ricci conventions this is Delta u+(s-2)u=0, as in Wolf-Wu Proposition 3.1. Tangential variation terms vanish because the mean curvature is identically zero. Integration on the closed leaf yields integral (s-2)u=0. A one-signed potential then vanishes everywhere since u is strictly positive, leading to the prohibited equality case. This proves strict crossing on every member of this particular family.

Closedness of S is essential: it removes the boundary/infinity term in integrating Delta u. A compact leaf with holonomy need not have an embedded global product neighborhood, and local foliation coordinates do not provide a single-valued positive global lapse on that compact leaf. The author explicitly preserves this extra hypothesis. No claim of a general compact-leaf obstruction has slipped in.

## Proposition 4: vertical planes and compact descent

For the upper half-space metric and N=z partial_x, direct differentiation gives zero shape operator on the plane directions, a=z partial_z, and div a=-2. The plane normal speed u=1/z is positive and satisfies Delta_H2 u=2u; this verifies the Jacobi sign and demonstrates why noncompactness invalidates the preceding closed-leaf integration. Reflection across x=t is a hyperbolic isometry, so those planes are independently recognized as totally geodesic.

The ideal circles of any two distinct parallel vertical planes have intersection exactly the point at infinity. A group permuting all leaves preserves that common point. Every hyperbolic isometry fixing infinity, including orientation-reversing ones, has similarity form (v,z) -> (cQv+b,cz). The pushforward of z partial_z is exactly the same field at the image point. Thus it descends to a smooth quotient by a free properly discontinuous such group. A compact quotient would be boundaryless and have positive volume, contradicting integral div V=-2 Vol. The argument does not assume the group fixes individual leaves and does not mistakenly exclude all minimal-plane foliations of hyperbolic space.

## What remains open

Sign-changing s-2 is compatible with both integral constraints. There is no contradiction for arbitrary noncompact leaves and no reason for local lapse functions to glue to a globally defined transverse parameter. The explicit plane family is only one equivariance class. The paper offers neither a cocompact-lattice-invariant general construction nor an obstruction to all such constructions. All four propositions are accepted as scoped necessary conditions or exclusions, never as a full answer to KP-3.18.

## Role of finite checks

The author script checks 139 exact coordinate and algebra identities; the independent script checks 512 rational/algebraic controls, including nonminimal constant-direction normal fields to test the full divergence formula and distinguish trace-square from norm-square. These finite checks help catch algebra/sign and implementation mistakes. They do not certify smooth geometric existence, the divergence theorem, Codazzi, the Jacobi variation theorem, compactness, or general nonexistence. Those inferences were separately audited above.
