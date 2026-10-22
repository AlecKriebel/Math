# Independent analytic stress tests for the whole PR196 note

The mechanism challenge was frozen before favorable package reports were opened. These checks concern the actual manuscript, not just replay of an earlier favorable conclusion. Published source contracts were checked directly in OWR, AIF and the moduli author version; the earlier IHES duality/current statements and APDE rank discussion were also compared.

## 1. Geometry and the current across a positive-capacity slit

The proof deliberately selects the particular Proposition3.4 construction, not every self-touching flow. The source allows a genuine segment, T in(0,1), and a smooth immersed boundary resolved by a fixed universal cover. The chosen lifted open domain projects biholomorphically. Its closure need not project injectively. I visually checked the closure bars on printed15: punctures are outside the closure; this is consistent with resolving the two copies of a boundary segment. The source Theorem6.2 proof verifies the two local fluid pieces and nonzero limiting velocity. At a relative interior point of a segment, small B has B minus S contained in Omega. This statement is false for a generic isolated tangent point with an exterior cusp, which is correctly excluded.

D+=Omega union B adds zero area but removes a nonpolar boundary barrier. Positive smooth area of its complement remains1−T, so it is a proper Greenian domain on the sphere. Its boundary need not be smooth or simply connected.

The current identity is stronger than the heuristic zero-area removal argument. On D+, ddc(psi_T+rho)=T delta0. Hence the complete distributional Laplacian has no line measure on S. Weyl regularity, not arbitrary removability of arcs, gives harmonic continuation. For h>0, subtracting currents gives ddc v_h=delta0+h^{-1}1_{Omega_(T+h)^c}omega_phi; monotonicity actually kills the last term almost everywhere on D+. The quotient is nonpositive and has exactly one log-squared pole. It is therefore a valid competitor below the negative unit-pole Green function of D+. Exhaustion by smooth relatively compact domains verifies this sign without a smooth-boundary assumption for D+.

The comparison is strict. Green monotonicity gives G_D+<=G_Omega; equal-pole cancellation makes their difference harmonic through0. On either smooth lifted slit side the old Green value tends to0, whereas G_D+(q)<0 at the newly interior nonpole point. Thus the difference is nonzero and positive everywhere by the strong maximum principle. Point-only removal would not prove this.

## 2. Finite L and the hidden endpoint differentiability concern

A fixed nonpole point in Omega_T lies in all sufficiently late precontact domains. One can see this from strict obstacle inequality plus continuity in t, or from the smooth nested lifted family. Fix its lift and the lifted pole under the time-independent projection.

For t<T, psi_t−phi solves ddc u=t delta0−omega_phi with zero boundary data. Subtracting a fixed cut-off logarithmic singularity and pulling back by smooth domain diffeomorphisms gives a smooth uniformly elliptic Dirichlet family. Thus differentiation in t is justified; it is not an assumed derivative of an arbitrary envelope. Spatial C1,1 fit makes gradients of psi_t and phi agree on the free boundary. Moving-boundary differentiation therefore gives zero boundary value for partial_t psi_t, while its pole coefficient is1. Green uniqueness gives partial_t psi_t=G_Omega_t.

The endpoint T is handled on the cover. AIF Theorem2.15 explicitly provides a two-sided family and cites the precursor Theorem2.2 plus Remark7.1. I checked the latter directly: the changed permeability is smooth positive, agrees with the prior one outside, and allows a smooth increasing family indexed on both signs of time. A forward-only theorem would not justify the stated endpoint argument. Uniformization places the noncompact simply connected covering surface in C or D; a compact lifted domain and collar are contained in one such coordinate. AppendixA then applies on a compact time interval. No projected postcontact regularity follows or is used.

Remove the fixed singular part of G before differentiating. H=partial_t G atT is harmonic including at the pole and has boundary value −V partial_nG. Strict positive outward V and Hopf's positive outward derivative of negative G make H strictly negative. Compact smooth data give finiteness. Hence −infinity<L<0. This rules out both zero and infinite curvature mechanisms that could defeat the claimed quadratic coefficient.

A normalization sanity model is the standard round flow for phi=0: R(t)^2=t/(1−t), G_t(w)=log|w|^2−log(t/(1−t)), and partial_tG=−1/[t(1−t)]<0 for0<t<1. This independently checks the sign and area-time factor. It is not a model of contact and is not offered as a PDE proof for the contact example.

## 3. Global maximization, endpoints and actual Taylor failure

For finite concave a(t)=psi_t(w), concavity on an open interval containingT gives finite one-sided slopes and continuity. The IHES Proposition1.3 endpoint convention and explicit admissible lower logarithmic barriers also prevent endpoint values from exceeding concave support. The manuscript safely allows extended-real endpoints. No discontinuous upper endpoint can win.

For t<T, a(t)−a(T)<=k0(t−T). For t>T, a(t)−a(T)<=b(t−T), where a'_+(T)<=b<k0. Therefore b<k<k0 gives strict global support atT. For k>k0 near it, finite negative left curvature yields a unique t(k)<T with a'(t(k))=k. Its tangent supports the entire concave function. Two global maximizers would force an intervening affine interval, contradicted by strict local curvature. This excludes all distant and unknown postcontact branches.

Set delta=k−k0 and x=t(k)−T=delta/L+o(delta). The objective remainder on the precontact maximizing branch is (k0−k)x+Lx^2/2+o(x^2)=−delta^2/(2L)+o(delta^2). On the plateau side it is exactly0. Since L is finite negative, the coefficients differ. This proves no second-order real Taylor expansion at the point, which is stronger and more precise than claiming only a jump in limiting Hessians.

At k0 finite negative, tau*=exp(k0/2) is strictly between0and1. Direct substitution into the source Proposition4.2 gives the smooth additive correction log[(1+|w|^2)/(exp(k)+|w|^2)] along (z,tau)=(w exp(−k/2),exp(k/2)). If an ambient second-order Taylor expansion existed, composition with this smooth curve, whose derivative is nonzero, would have one quadratic coefficient. Smooth addition changes both coefficients equally. The contradiction therefore transfers to a genuine product interior point.

## 4. PDE, positivity and normalization

The smooth global phi comes from the credited theorem; no closed-form polynomial is promised. Circle rotations act smoothly on P1, preserve FS and pull the strictly positive form back, so f(z,tau)=phi(tau z) is jointly smooth and strictly positive on each boundary fibre. The source envelope/duality theorem identifies the bounded Bedford–Taylor weak solution, including boundary trace. Constant min(phi) is a lower envelope competitor and vertical subharmonic comparison gives upper max(phi). The weak product is therefore well defined.

With ordinary exterior derivative, dc=i/(4pi)(barpartial−partial) gives ddc=i/(2pi)partialbarpartial, unit log-squared Dirac and FSarea1. These are mutually consistent; the apparent prefactor error printed in AIF is independently visible on page7. The manuscript does not copy that inconsistent prefactor. Every Green value, area-time coefficient, current and tau*=exp(G/2) uses the same unit convention. The source inconsistency is described as apparent, not as an author-confirmed erratum.

## 5. Adversarial stopping point

No mathematical contradiction or unsupported central step remains in this source-specific proof. T=0,1; evaluation at the pole; isolated point contact; arbitrary terminal slit; zero/infinite curvature; and rank-loss-only arguments are excluded or explicitly disclaimed. The proof relies on the credited published flow theorem and classical potential/elliptic/convex facts. I have not independently reconstructed every foundational proof or performed a numerical PDE solve. None is claimed in the note or this audit.
