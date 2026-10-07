# Approach 4: implicit continuation beyond the symmetric class

## Objective and result

Rather than trying to force symmetry from sliding stationarity, perturb the normal directions of a known stationary polygon. For every fixed \(0<\alpha<2\), there exists a neighborhood of the square's four outward normals such that every ordered four-normal configuration in that neighborhood has a unique nearby, area-one, sliding-stationary quadrilateral, modulo translation.

In particular, there are non-parallelogram quadrilaterals whose Wulff shapes remain global minimizers at small γ. The result is local and implicit. It does not identify all such quadrilaterals or rule out additional stationary solutions far away.

## 1. A nondegenerate constrained Hessian at the square

Let \(R_\tau\) be the centered unit-area rectangle with horizontal side length \(a=e^\tau\) and vertical side length \(b=e^{-\tau}\). Let \(M_b(\tau),M_a(\tau)\) be the side averages from Approach 3. By the side-velocity first-variation formula,
\[
\frac d{d\tau}V_\alpha(R_\tau)=2(M_b(\tau)-M_a(\tau)).
\tag{1}
\]
Indeed, each vertical side moves outward with speed \(a/2\), while each horizontal side moves outward with speed \(-b/2\); the side integrals are \(bM_b\) and \(aM_a\), respectively, and \(ab=1\).

For perpendicular \(a,b\), formula (1) in Approach 3 reads
\[
M_b(\tau)-M_a(\tau)
=2\int_0^1\int_0^1(s-t)
(e^{2\tau}s^2+e^{-2\tau}t^2)^{-\alpha/2}\,ds\,dt.
\]
Differentiating at 0 is justified by integrability, or by the transport lemma of Approach 2. Thus
\[
\left.\frac{d^2}{d\tau^2}V_\alpha(R_\tau)\right|_{\tau=0}
=-4\alpha\int_0^1\int_0^1
\frac{(s-t)^2(s+t)}{(s^2+t^2)^{1+\alpha/2}}\,ds\,dt<0.
\tag{2}
\]
The integral is finite: the integrand has degree \(1-\alpha\) near the origin, hence its polar-area integral behaves as \(\int_0 r^{2-\alpha}\,dr\). It is strictly positive on a set of positive measure. The exact negativity holds throughout \(0<\alpha<2\); it is not based on numerics.

## 2. A genuine chart for the constrained quadrilaterals

Take normal angles
\[
\theta^0=(0,\pi/2,\pi,3\pi/2),\qquad
\nu_i(\theta_i)=(\cos\theta_i,\sin\theta_i).
\]
For \(\theta\) near \(\theta^0\), all successive supporting lines intersect transversely. Translation changes supports by \(h_i\mapsto h_i+\nu_i\cdot u\). Since \(\nu_1,\nu_2\) are independent, there is a unique translation imposing
\[
h_1=h_2=1/2.
\]
Set \(h_3=1/2+z\). At the square (z=0,h_4=1/2), the derivative of area with respect to \(h_4\) equals the fourth side length, which is 1. The implicit function theorem gives a smooth function
\[
h_4=H(\theta,z)
\]
making the area exactly 1. Near the basepoint all four side lengths remain positive, and the origin remains in the interior. Denote this polygon by \(Q(\theta,z)\).

This chart includes every sufficiently close area-one quadrilateral with the specified normals, modulo translations. Its only residual shape coordinate is \(z\).

## 3. Smoothness under changing normals

The vertices of \(Q(\theta,z)\) are smooth functions of (θ,z), obtained by solving nonsingular \(2\times2\) linear systems. Apply the fixed reference fan-triangulation construction from Approach 2. The resulting maps and all their required parameter derivatives are uniformly Lipschitz in space; differences of each derivative at \(x,y\) are \(O(|x-y|)\). The same dominating kernel \(C|x-y|^{-\alpha}\) therefore proves that
\[
f(\theta,z)=V_\alpha(Q(\theta,z))
\]
is \(C^2\).

At \(\theta=\theta^0\), the polygon has width \(a=1+z\) and height \(1/a\), up to translation. Thus \(\tau=\log(1+z)\). Since \(f_z(\theta^0,0)=0\), equation (2) gives
\[
f_{zz}(\theta^0,0)=
\left.\frac{d^2}{d\tau^2}V_\alpha(R_\tau)\right|_{\tau=0}<0.
\]

## 4. Implicit critical shapes

Apply the implicit function theorem to \(G(\theta,z)=f_z(\theta,z)\). There is a unique \(C^1\) function \(z=z(\theta)\), for θ sufficiently close to θ⁰ and z sufficiently close to zero, such that
\[
f_z(\theta,z(\theta))=0.
\]
Translation invariance and the completeness of the chart show that this is stationarity for **all** fixed-normal area-preserving variations, not just an arbitrarily selected direction. Equivalently the four side-average potentials are equal. Approach 2 then gives unique global minimality, modulo translations, for sufficiently small γ, with the threshold allowed to depend on the resulting polygon and on α.

For an explicit choice of nonsymmetric normal data, take
\[
\theta=(0,\pi/2,\pi+\varepsilon,3\pi/2),\qquad
0<|\varepsilon|\ll1.
\]
The resulting quadrilateral has one pair of opposite sides parallel and the other pair nonparallel. It is not a parallelogram and hence not a rhombus. Every side-transitive convex quadrilateral is equilateral and therefore a rhombus, so these examples lie outside the side-transitive class.

This is an existence proof for exact examples, not a claim that a floating-point quadrilateral is exactly stationary. The relevant shape is defined by the unique local zero \(z(\theta)\).

## What remains open

- No explicit formula is obtained for \(z(\theta)\).
- Uniqueness is only near the square and at the fixed nearby normal data.
- The proof does not control continuation through side collapse, distant branches, or arbitrary normal fans.
- For \(n\ge5\), there are \(n-3\) genuine constrained shape directions; extending this method requires a nondegenerate full Hessian, which is not proved here.
- The construction uses the source's permission of non-even anisotropies. It does not settle a separately imposed centrally symmetric classification.
