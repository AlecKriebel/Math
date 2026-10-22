# Direct Euclidean audit: independent exact results

Independent continuation at 2026-10-16T07:36:00.472125+00:00. This text precedes original-proof intake.

## 1. Central pairing without elliptic parametrization

Fix the branch of the Poncelet step T on the outer ellipse that advances with the chosen caustic orientation. For a proper nested smooth strictly convex caustic, T is an orientation-preserving circle homeomorphism. One direct explanation: parameterize oriented tangent lines to the caustic by their normal angle. Each intersects the outer ellipse transversely in its entry and exit points. Each endpoint map is a degree-one circle homeomorphism because each boundary point has exactly one tangent of the chosen entry/exit branch. Their composition is T. Center inversion C(P)=-P preserves the centered ellipse pair and this branch, so CT=TC, C^2=id, and C has no fixed boundary point.

The given Poncelet family of primitive least period N has T^N=id and T has order exactly N. This uses the ordinary Poncelet porism for the fixed conic pair, not the desired pedal invariant. If N is even, H=T^(N/2) is a nonidentity orientation-preserving involution. H and C commute. If H != C, they generate a four-element Klein group of orientation-preserving circle homeomorphisms. Every finite subgroup of orientation-preserving circle homeomorphisms is cyclic: a finite-order orientation-preserving map fixing a point is the identity (otherwise iterating a point strictly moves it in one interval); therefore the action on any orbit is faithful and its cyclic order embeds the group into the cyclic rotations of that orbit. A Klein group is impossible. Hence C=H and P_(i+N/2)=-P_i.

This also explains why a nominal even-length list obtained by repeating an odd primitive orbit need not have antipodal pairing. The period in this argument must be the map's least period. For primitive winding p/N with N even, p is odd and the half-period maps to the antipode regardless of the star winding.

Combined with INDEPENDENT_DERIVATION_FREEZE.md this proves, universally for the target setting,

B_M=B_0+C|M|^2, C=(1/8)sum sin(2delta_i).

The target is exactly equivalent to the two scalar invariants A B_0 and AC. Central pairing alone does not prove either.

## 2. Complete elementary four-bounce proof

Put s=a^2+b^2 and lambda=a^2 b^2/s. The proper confocal caustic has axes squared a_c^2=a^4/s, b_c^2=b^4/s. An arbitrary positive-orientation primitive 4-orbit is a central parallelogram with vertices P,Q,-P,-Q. Write

P=(a cos(eta-xi),b sin(eta-xi)),
Q=(a cos(eta+xi),b sin(eta+xi)), 0<xi<pi/2.

Its consecutive line equations, with unnormalized normals, are

x cos eta/a+y sin eta/b=cos xi,
-x sin eta/a+y cos eta/b=sin xi.

Tangency to a confocal caustic of parameter lambda requires

sin^2 xi=lambda(cos^2 eta/a^2+sin^2 eta/b^2),
cos^2 xi=lambda(sin^2 eta/a^2+cos^2 eta/b^2).

Adding proves lambda=a^2 b^2/s, so the condition is forced for any such orbit. Define

U=a^2 sin^2 eta+b^2 cos^2 eta,
V=a^2 cos^2 eta+b^2 sin^2 eta.

Then sin^2 xi=U/s, cos^2 xi=V/s. Adjacent side lengths are u=2U/sqrt(s), v=2V/sqrt(s), while signed positive area is A=4ab sqrt(UV)/s. In particular A^2/(uv)=4a^2 b^2/s.

For ANY central parallelogram the side normal turns occur as delta,pi-delta,delta,pi-delta, giving C=0. Its centered pedal is the parallelogram with vertices h_1 n_1,h_2 n_2,-h_1 n_1,-h_2 n_2. The distances are |h_1|=A/(2u), |h_2|=A/(2v), and the sine between the normals is A/(uv), so B_0=A^3/(2u^2v^2). Therefore for every fixed finite real M,

A B_M=A B_0=A^4/(2u^2v^2)=8a^4 b^4/(a^2+b^2)^2.

All displayed area signs reverse with reversal; the product formula is unchanged. There is no division by B_M. Since 4-periodic trajectories on an elliptical caustic have primitive winding 1 or its reversal, this covers the full primitive N=4 case. Its units are length^4 as required. The parameter identities describe genuine confocal tangential polygons; the physical reflection law is independently checked below from equal focal sums.

## 3. Physical reflection from confocal tangency

A line segment of a confocal elliptical caustic joining two boundary points has the billiard reflection property under the ordinary conic Poncelet step. This well-known statement can be checked locally without invariant assumptions. Let outer quadratic matrix D=diag(a^2,b^2), P^T D^-1 P=1, and n a unit side normal with h=n dot P. Tangency to D-lambda I is h^2=n^T D n-lambda. Rearrangement shows

(n dot P)^2-n^T D n=-lambda.

At fixed P the two unit normals n to the two tangent lines solve the same quadratic on the unit circle. In the tangent-normal frame of the outer ellipse, the mixed term of P P^T-D vanishes, since for outer tangent t and normal N parallel D^-1 P,
t^T(P P^T-D)N=(t dot P)(P dot N)-t^T D N=0:
D N=P/k, P dot N=1/k, where k=|D^-1 P|.

Thus the quadratic is diagonal in that frame. Its two relevant solutions are mirror images across the outer normal/tangent axes, proving equal incidence and reflection angles. Proper lambda and transverse tangency exclude zero-length and glancing degeneracies. This is a local physical-law check, not a new scalar invariant.

## 4. A false nonconfocal extension, exact

Take the outer ellipse x^2/4+y^2=1 and homothetic inner ellipse x^2/2+2y^2=1. The affine images of a rotating square are a genuine tangent 4-Poncelet family for this nested nonconfocal pair. At phase 0 use (2,0),(0,1),(-2,0),(0,-1): A=4, B_0=32/25, A B_0=128/25. At phase pi/4 use (sqrt(2),1/sqrt(2)),(-sqrt(2),1/sqrt(2)),(-sqrt(2),-1/sqrt(2)),(sqrt(2),-1/sqrt(2)): A=4, B_0=2, A B_0=8. Both have C=0, so this counterexample holds for every M. The second polygon fails the physical billiard reflection law on the outer ellipse; merely being a Poncelet pair is insufficient.

## 5. Exact remaining gap and route status

For primitive least N=0 mod 4 larger than 4, no independent elementary proof of phase invariance of either A B_0 or AC has been obtained. The universal all-M reduction and central pairing remove point dependence but do not finish the main invariant. This direct-geometry route is PARTIAL/BLOCKED at the two-scalar stage unless a new mechanism supplies those identities. Completion toward a universal direct proof is 35%; the complete N=4 theorem and exact nonconfocal counterexample are verified results, not evidence establishing all N.
