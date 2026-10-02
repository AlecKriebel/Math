# Universal audit of the original conditional differential-geometric claims

The arguments here do not depend on the finite verification programs.

Let gamma be a regular smooth curve parametrized by arclength s. Let B be a C² unit field satisfying B·T=B·T′=0 for T=gamma′. Put N=B×T. The positive orthonormal frame (T,N,B) has T′=kN, where k is signed. Differentiating the six orthonormality identities shows B′ has no B or T component, so B′=−tau N and N′=−kT+tau B. No division by k is involved, so the equations survive k=0. With parameter t of speed v>0 these three derivatives all acquire the factor v.

The ribbon twist integrand in the convention (T×B)·B′ equals tau, since T×B=−N. Equivalently T·(B×B′)=tau. Thus Tw=(2pi)⁻¹∫tau ds. For a rotating normal V=cos(theta)N+sin(theta)B the twist density becomes tau+theta′ in arclength. These identities are orientation-consistent; B and N changing sign leaves tau and twist unchanged.

If B is regular, |B′|=|tau|>0 and continuous tau has constant sign on the connected parameter circle. Let sigma=sign(tau). The spherical unit tangent is U=−sigma N. Spherical arclength ell obeys d ell=|tau| ds. Thus

    dU/d ell = (k/tau)T−B,
    B×U = sigma T,
    k_g=(dU/d ell+B)·(B×U)=k/|tau|,
    k_g d ell=k ds.

This is the outward-sphere oriented geodesic-curvature convention. The original numerator B″·(B×B′)=tau² k gives the same formula, because dividing by |B′|³ gives k/|tau|. Replacing |tau| by tau would be wrong for negative torsion. Reversing the parameter reverses the signed curvature integral and leaves its absolute value unchanged.

A C² regular simple spherical B is a Jordan curve. Orient it as the boundary of one Jordan component of area A. That component is a disk and 0<A<4pi. Gauss–Bonnet gives ∫ k_g d ell=2pi−A, so the absolute value is strictly below2pi. If k never changes sign, then ∫|k| ds=|∫k ds|<2pi. But |k| is the ordinary curvature of gamma, and Fenchel's theorem for any smooth regular closed space curve, including an immersion, gives ∫|k| ds≥2pi. Hence a closed gamma with a regular injective compatible unit binormal must have signed-curvature changes and therefore inflections. This is a conditional obstruction, not a proof of linking≠0.

For a smooth embedded centerline and sufficiently small smooth nonzero normal push-off, Călugăreanu gives Lk=Wr+Tw. A nonzero Tw does not exclude Wr=−Tw. The original partial correctly leaves this cancellation unresolved under its regular-binormal restrictions. Its imported signed-crossing formula has the same limitation: the crossing sum is signed, and no bound preventing its cancellation is established.

Here is a derivation of that formula under the smooth embedded regular-B hypotheses, independently of the paper's textual typos. For a generic fixed u not parallel to a tangent set a=u·T, b=u·N, c=u·B. Then a′=kb, b′=−ka+tau c, c′=−tau b. The blackboard normal V=(u×T)/|u×T| has angle theta relative to (N,B) with cos(theta)=c/sqrt(b²+c²), sin(theta)=−b/sqrt(b²+c²). Differentiate atan2 to obtain

    theta′=−tau+kac/(b²+c²).

When c=0, b≠0 and c′≠0, while theta′=−tau. There are finitely many such zeros, each giving one of the two regular circle values pi/2 and3pi/2. Counting both values gives degree(V relative to B)=−#(c=0)sign(tau)/2. The blackboard framed linking is the signed projected crossing sum Cr(gamma_u), hence

    Lk(gamma,B)=Cr(gamma_u)+#(u·B=0)sign(tau)/2.

An angle lift is taken on an interval representing the parameter circle. It need not be a globally periodic real-valued function if the framing has nonzero winding. That minor bookkeeping point avoids mistaking a circle-valued angle for a globally real periodic angle.

For the ruled strip F(s,r)=gamma(s)+rN(s), its metric at r=0 is the identity and second fundamental matrix is [[0,tau],[tau,0]] relative to B; Gaussian curvature is −tau². Thus regular B implies negative curvature near the compact centerline, while B′=0 gives zero curvature on the centerline at that parameter. The explicit countermodel in COUNTERMODEL_DERIVATION.md consequently fails the 2025 negative-curvature hypothesis, as expected.

On a planar subarc with nonzero curvature, a continuous unit compatible binormal lies in the two-point set of plane normals and therefore is constant. Any smooth regular closed planar curve has a nonzero-curvature subarc: if its curvature vanished everywhere its tangent would be constant and it could not close. Thus its unit binormal cannot be injective. The narrower wording in the final original artifact is correct; an arbitrary planar arc with a straight interval allows its compatible normal direction to vary on that interval.

A continuous injective spherical map alone need not be differentiable or rectifiable; a smooth injective map need not be regular. The exact cos2t graph countermodel proves the last point within actual binormal compatibility and a smooth positive-curvature embedded centerline. No approximation preserving compatibility, closure, injectivity and linking simultaneously has been supplied by the original PR. The conditional Gauss–Bonnet proof cannot be extended by simply removing its regularity hypothesis.
