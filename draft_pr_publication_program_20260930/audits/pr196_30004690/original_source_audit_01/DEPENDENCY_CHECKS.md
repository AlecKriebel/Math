# Independent dependency checks

These derivations were completed after the original-source freeze and before reading any other new family report. They verify applications of the source contracts, rather than reproving the cited construction theorem.

## 1. Contact geometry and Greenian enlargement

Use a point q strictly inside a contact segment in the particular Proposition3.4 construction. A small coordinate ball B misses the segment endpoints, the injection point, and other boundary components. Its two open sides belong to Omega_T, and B minus Omega_T is the local segment. Thus D_plus=Omega_T union B is open and connected and differs from Omega_T by a zero-area piece. Since area_omega_phi(Omega_T)=T<1 and omega_phi is smooth positive, the complement of D_plus retains positive area. It is nonpolar; D_plus is proper and Greenian. This argument uses genuine arc contact; it is not valid for a lone polar contact point.

At time T the current identity gives omega_FS+dd^c psi_T=T*delta_0 on D_plus. Consequently psi_T plus a local Fubini-Study potential is distributionally harmonic away from 0 across the segment. Weyl regularity applies. For h>0, subtracting currents gives, on D_plus,

    dd^c[(psi_(T+h)-psi_T)/h]
       = delta_0 + h^{-1}*1_(Omega_(T+h)^c)*omega_phi >= delta_0.

The difference quotient is nonpositive, because the admissible envelopes decrease with t. Its pole coefficient is one. It is therefore an admissible negative subharmonic competitor for G_D_plus, yielding v_h<=G_D_plus. In fact monotonicity Omega_(T+h) contains Omega_T implies that the added measure has zero area on D_plus, but the weaker displayed inequality is sufficient.

Negative Green functions decrease when a domain is enlarged: G_D_plus<=G_Omega_T. The difference G_Omega_T-G_D_plus is nonnegative harmonic on Omega_T and has a removable singularity at 0. At a smooth side of q, G_Omega_T tends to 0 while G_D_plus(q)<0. Therefore the difference is not identically zero and is strictly positive at every non-pole interior point. The inequality's direction and strictness in the candidate are correct.

## 2. Left Green derivative and time curvature

For t<T near T, a fixed w* in Omega_T lies in Omega_t. One way to justify this is continuity of psi_t(w*) in t and the strict obstacle inequality at T. The lifted domains Omega'_t form a smooth Jordan family through T on the cover. Choose a fixed conformal coordinate on that simply connected covering surface containing the compact closure of Omega'_T and a small neighboring family. Equivalently pull back a smooth conformal metric to a fixed disk. Compact time restriction makes ellipticity uniform. This supplies the precise extension from the planar AppendixA to this use.

The injection point lift and the lift of w* remain fixed. Conformal projection identifies negative unit-logarithmic Green functions on the open domains. Add local Fubini-Study potentials and subtract t*log of the fixed pole coordinate. The remaining harmonic Dirichlet problems have smooth coefficients/data, so the envelope has smooth pre-contact parameter dependence in the lifted family. Differentiate the boundary equality psi_t=phi along moving boundary points. Smooth fit gives grad(psi_t-phi)=0 there, hence the time derivative has boundary value zero. Its Laplacian vanishes away from the pole and its pole coefficient is one. Uniqueness yields

    d/dt psi_t(w*) = G_Omega_t(w*,0).

Let g_t be that Green function on the lifted domain, and H=d/dt g_t at T from the left. The log singularity is independent of t, so H is harmonic even at the pole. Differentiating g_t(x_t)=0 at the smooth boundary gives H=-V*partial_n g_T. Outward scalar velocity V is positive and smooth; Hopf gives partial_n g_T>0. H is smooth with strictly negative boundary values, so H(w*) is finite and strictly negative. Thus a''(T-)=L lies in (-infinity,0). No post-contact shape differentiability, globally injective boundary projection, or negative-curvature condition is needed.

The two-sided smooth family used for this endpoint argument comes from AIF Theorem2.15. Its cited precursor's Theorem2.2 alone is forward; Remark7.1 supplies the interior permeability modification and two-sided family. This distinction matters, but the published input used by the candidate includes it.

## 3. Global concave maximization and actual second differentiability

Set a(t)=psi_t(w*) and kappa_0=G_Omega_T(w*,0)<0. Concavity and the Green comparison give a'_+(T)<=b<kappa_0=a'_-(T), with b=G_D_plus(w*,0). For b<kappa<kappa_0, the supporting line inequality is strict for every t unequal to T: on the left, the limiting slope is larger than kappa; on the right, the limiting slope is smaller. Hence T is the unique global maximizer of a(t)-t*kappa. For kappa>kappa_0 sufficiently close, a''<0 locally gives a unique nearby t(kappa)<T, with a'(t(kappa))=kappa. Global concavity again makes it the unique global maximizer; a later unknown branch cannot win.

Consequently F(kappa)=kappa+sup_t(a(t)-t*kappa) is affine on the left of kappa_0, with slope 1-T. On the right F'=1-t(kappa), and

    t(kappa)-T=(kappa-kappa_0)/L+o(kappa-kappa_0).

Therefore the left derivative of F' at kappa_0 is 0 and its right derivative is -1/L>0. This proves failure of an actual second derivative, rather than merely unequal limiting values of a possibly undefined F''. The first derivative matches. Duality holds at this nonzero disc radius, and the smooth curve kappa -> (w*exp(-kappa/2),exp(kappa/2)) transfers the failure to Phi. The curve stays in P^1 x D near kappa_0, because kappa_0<0. Smooth additive correction terms cannot remove it.

## 4. Result and remaining limits

All candidate applications of the cited contracts pass these checks. The extra fixed-chart/compact-time explanation makes the AppendixA extension checkable; it requires no new conjecture. The proof establishes the stated existence result relative to the published construction and ordinary Green-function/elliptic facts. It is not an elementary closed-form formula for phi. It does not certify novelty, exclusivity of the mechanism, or present literature status.
