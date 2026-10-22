# Exact algebraic fixtures for the complex fixed-camera residual

These are authored finite tests for the pass-1 arguments, not a proof of the general classification, a full source solution, or a novelty claim. No external source material is included. They use the adopted complex fixed-pinhole formulation.

## Reproduction and conventions

Run `python exact/certify_examples.py` from the package root, or use `python verify_package.py` for integrity checking and isolated clean-copy replay. Python 3.12 with SymPy 1.14.0 was used. All arithmetic is exact. The script writes `CERTIFICATE_RESULTS.json` and fails immediately if an asserted certificate does not check.

World coordinates are `[x:w:y:z]`. The cameras are

- `pi1([x:w:y:z])=[x:y:z]`, with center `c1=[0:1:0:0]`;
- `pi2([x:w:y:z])=[w:y:z]`, with center `c2=[1:0:0:0]`.

The baseline is `L=V(y,z)` and both image epipoles are `[1:0:0]` in their respective image planes. A generator `f(x,y,z)` or `g(w,y,z)` is the corresponding pulled-back image equation.

The script verifies ideal equalities by mutual Groebner reduction. It computes principal saturations by eliminating `u` from `(I,1-u*f)`, ideal intersections by eliminating `u` from `u*A+(1-u)*B`, and Hilbert series by inclusion-exclusion on the leading monomial ideal. Smoothness certificates use the component's own ideal plus all 2-by-2 Jacobian minors; the resulting ideal is the unit ideal on each of the four projective affine charts. Thus these certificates do not confuse a smooth component with a singular or nonreduced total cone intersection.

For generic baseline multiplicity, put `K=Q(x,w)` and regard the two equations in transverse coordinates `(y,z)`. Adding `(y,z)^N`, where `N` is a Bezout-safe bound equal to the product of their transverse total degrees, isolates the origin's local Artinian factor without changing its length. The exact standard monomial basis gives the length. Away from the origin, `(y,z)` is the unit ideal; at the origin, an Artinian local factor of length at most `N` has maximal ideal power `N` zero. These local lengths are scheme multiplicities, not products of image multiplicities guessed from incidence.

Absolute irreducibility in these explicit fixtures is independently visible: transformed twisted cubics are prime; the conics are smooth; the indicated plane cubics are primitive polynomials linear in one coordinate; and the quartic's irreducibility is proved below. The script is not an implementation of general absolute primary decomposition.

## E1. Distinct epipole tangents, centers retained

Take `f=xz-y^2` and `g=wy-z^2`. The exact decomposition is

`(f,g) = (f,g,xw-yz) intersection (y,z)`.

The first prime is the smooth twisted cubic

`[s:t] -> [s^3:t^3:s^2*t:s*t^2]`.

It has degree 3, and each projection has generic degree 1 onto a conic. It passes through both camera centers, smoothly and with multiplicity 1. The degree identities are

`3 = 1*2 + 1` for both cameras.

The complete intersection has degree 4, and the baseline has generic multiplicity 1. Baseline saturation must retain the two center points of the twisted cubic; it removes a whole baseline component, not every point lying on the baseline.

## E2. Same tangent: a doubled baseline and a false total-Jacobian alarm

Take `f=xz-y^2` and `g=wz-y^2`. The exact decomposition is

`(f,g) = (x-w,xz-y^2) intersection (z,y^2)`.

The residual prime is a smooth plane conic, parametrized by

`[s:t] -> [s^2:s^2:s*t:t^2]`.

Both image epipoles are smooth and have multiplicity 1, yet the baseline has scheme multiplicity 2. Accordingly, `4 = 2 + 2`, not a baseline contribution of `1*1`.

At the residual/baseline meeting point `[1:1:0:0]`, the two original cone gradients have rank 1. The Jacobian of the residual conic ideal has rank 2, and the residual is smooth on all four projective charts. A test of the unsaturated two-equation complete intersection would incorrectly reject this smooth world curve.

Both centers are absent. The projections have degree 1, so `2=1*2+0` for both cameras.

## E3. Cuspidal image, smooth lift, unequal epipole branch multiplicities

Take `f=y^3-xz^2` and `g=wz-y^2`. The unique nonbaseline prime is

`(w^2-xy, wy-xz, y^2-wz)`.

Its parametrization is the smooth twisted cubic

`[s:t] -> [s^3:s^2*t:s*t^2:t^3]`.

The first image is a cuspidal cubic with its cusp at the epipole; the second is a smooth conic through its epipole. At the common normalized epipole branch `t=0`, the two image branch multiplicities are 2 and 1. The world point is `c2`, with world multiplicity 1. The world does not contain `c1`.

The exact projection degrees are both 1:

- Camera 1: no common factor in `[s^3:s*t^2:t^3]`, so `3=1*3+0`.
- Camera 2: divide `[s^2*t:s*t^2:t^3]` by `t`, so `3=1*2+1`.

The cone intersection has degree 6, the residual has degree 3, and the baseline has local length 3. Indeed, over `Q(x,w)`, substitute `z=y^2/w`; the remaining equation is `y^3*(w^2-xy)/w^2`, whose second factor is a unit at `y=0`.

This fixture tests that a singular image can have a smooth embedded world lift, and that a center correction is a multiplicity, not only an incidence flag.

## E4 and E5. Identical normalized epipolar data can glue differently on the baseline

For `lambda` equal to 1 or 2, take

`f=y^3+z^3-xyz`,

`g=y^3+lambda*z^3-wyz`.

Both image curves are integral nodal cubics, with node at the epipole and epipolar map of degree 1. The unique nonbaseline world component has normalization map

`[s:t] -> [s^3+t^3:s^3+lambda*t^3:s^2*t:s*t^2]`.

For `lambda=2`, use the invertible change `A=2x-w`, `B=w-x`. The residual ideal is exactly the transformed twisted cubic ideal

`(Az-y^2, By-z^2, AB-yz)`.

It is smooth, degree 3 and avoids both centers. The two normalized node branches land at distinct baseline points `[1:1:0:0]` and `[1:2:0:0]`.

For `lambda=1`, the residual is the plane nodal cubic

`(x-w, y^3+z^3-xyz)`.

The same two normalized points land at `[1:1:0:0]`. Both branches are immersive: in the chart `x=1`, their tangent vectors in `(w,y,z)` coordinates are `(0,1,0)` and `(0,0,1)`. The resulting embedded world curve is nonetheless singular because the normalization identifies two distinct points.

For both parameter values, the total cone intersection has degree 9 and the residual degree 3; the baseline's exact local length is 6, despite the two image epipole multiplicities being 2 and 2. Thus neither normalization smoothness, immersion alone, nor a naive baseline multiplicity product decides the desired conclusion.

## E6 and E7. Cusp and node away from the epipoles

The plane ideals

- cusp: `(w-x, y^2*z-x^3)`;
- node: `(w-x, y^2*z-x^2*(x+z))`

are admissible degree-3 world components, with both projections generically one-to-one onto identical image curves avoiding the epipoles. Each is absolutely irreducible by the primitive-linear-polynomial observation.

For the cusp, the normalization in `z=1` is `(x,w,y)=(u^2,u^2,u^3)`; its differential vanishes at zero. The singular subscheme on this chart has ideal `(x-w,w^2,y,z-1)`, with support the cusp.

For the node, the normalization is `(u^2-1,u^2-1,u*(u^2-1))`. The distinct points `u=-1,1` both map to the node, and both derivatives are nonzero. The singular subscheme is the reduced node `(x,w,y,z-1)`.

These fixtures separate failure of immersion from failure of injectivity even when no epipole or camera-center complication is present. They establish the properties of the selected world components, not the claim that no other component can be smooth for the same pair of image curves.

## E8. Matching epipolar lines: all smooth-conic projection patterns

In the epipolar plane `z=0`, the four smooth conics below give all generic projection pairs `(r1,r2)` in `{1,2}^2`:

- `x^2+w^2+y^2=0`: center multiplicities `(0,0)`, degrees `(2,2)`.
- `xw-y^2=0`: center multiplicities `(1,1)`, degrees `(1,1)`.
- `xw+x^2-y^2=0`: center multiplicities `(1,0)`, degrees `(1,2)`.
- `xw+w^2-y^2=0`: center multiplicities `(0,1)`, degrees `(2,1)`.

Their Hilbert degree is 2; every projective Jacobian chart is certified smooth. Polynomial degree in the omitted coordinate also verifies the generic projection degrees directly.

## E9. Matching epipolar lines: an integral quartic with two center nodes

In `z=0`, take

`F=x^2*w^2+y^2*(x^2+w^2)+2*y^4`.

It has degree 4 and multiplicity 2 at both camera centers. The local quadratic terms are `x^2+y^2` at `c1` and `w^2+y^2` at `c2`; both are products of two distinct linear forms over C. Thus each center is an ordinary node. Each projection has generic degree 2, giving `4=2+2` for each camera and the boundary pattern `r1+r2=d`.

For absolute irreducibility, set `y=1` and solve

`w^2=-(x^2+2)/(x^2+1)`.

This rational function has simple zeros and poles over C, hence is not a square in `C(x)`. The quadratic in `w` is therefore irreducible over `C(x)` and primitive over `C[x]`. Homogenization is not divisible by `y`, so `F` is absolutely irreducible. A factorization test only over Q would not have been enough.

## E10 and E11. Empty exceptional cases and contracted components

For camera-1 line `y=0` and camera-2 line `z=0`, the two back-projection planes meet only in the baseline. Its projections are points, so no admissible world curve exists.

For camera-1 line `z=0` and camera-2 conic `wy-z^2=0`, the exact cone decomposition is

`(z,wy-z^2) = (z,w) intersection (z,y)`.

The first component projects onto the desired camera-1 line but is contracted by camera 2 to `[0:1:0]`. The second is the baseline. Neither projects onto the conic, so there is no admissible world curve. Existence of a one-dimensional cone intersection alone is insufficient.

## E12. Saturation by a product is not saturation by the baseline ideal

The line `W=V(z,x+w+y)` avoids both centers and projects onto the matching epipolar line `z=0` in both images. It is a valid degree-1 world curve.

Yet saturation of its prime by `z` (and hence by `y*z`) is the unit ideal, deleting the valid curve. In contrast,

`I(W):(y,z)^infinity = (I(W):y^infinity) intersection (I(W):z^infinity) = I(W)`.

The script verifies these identities. This warning concerns the general or matching-plane case; it is not a counterexample to product saturation within the neither-epipolar finite branch, where every admissible component meets both coordinate nonvanishing opens. Removing the baseline means ideal saturation by `(y,z)`, or explicitly deleting minimal primes supported there, not saturation by the coordinate product `y*z`.

## E13. Equal singular branch orders: the baseline ratio derivative

The supplementary report ../local/SHARPNESS_FAMILIES.md gives the global family

`[s:t] -> [s^(k+1):s^(k+1)+s^k*t:s*t^k:t^(k+1)]`, for `k>=2`.

The suite certifies `k=2` and `k=3`. Its two image equations are

`f=y^(k+1)-xz^k`,

`g=y^(k+1)+y^k*z-wz^k`.

Both image curves have a singular epipole branch of multiplicity `k`, and the normalized epipolar cover has degree 1. Nevertheless, the embedded world curve is smooth. In the chart `x=1`, its local form at the baseline is `[1:1+u:u^k:u^(k+1)]`. The derivative of `w/x` is 1 and supplies the world tangent direction along the baseline, even though both transverse derivatives vanish. Globally this ratio recovers `u` wherever `s` is nonzero, and the coordinate `y/z=s/t` covers the remaining point. Thus injectivity and immersion are transparent as well as Jacobian-certified.

The `k=2` world is a smooth twisted cubic and the `k=3` world is a smooth rational quartic. Their cone intersection degrees are 9 and 16; the exact baseline local lengths are respectively 6 and 12. Neither world contains a camera center.

For comparison, remove the `s^k*t` term in the second coordinate with `k=2`. The residual becomes the plane cusp `(x-w,y^3-xz^2)`, locally `[1:1:u^2:u^3]`. Both transverse derivatives and the baseline-ratio derivative vanish, and the component is singular. The two examples have the same branch-order pair `(2,2)` and different derivative behavior. Multiplicity data alone cannot decide the local smoothness at a noncenter baseline point.

## Acceptance limits

The exact fixture suite passes. It supplies adversarial checks for degree corrections, center retention, baseline scheme multiplicity, contracted components, exceptional planes, and the injective-plus-immersive distinction. General existence, absolute decomposition, all-degree exceptional-plane realization, and the general smoothness theorem require their own proofs and independent audit; these finite computations do not replace them.
