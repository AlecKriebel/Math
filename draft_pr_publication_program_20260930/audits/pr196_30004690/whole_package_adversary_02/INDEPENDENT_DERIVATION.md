# Independent analytic check and falsification controls

This derivation records the reviewer’s own checks of the fixed manuscript. The mechanism challenges were frozen before reading archived favorable findings. All ingredients imported from Ross–Witt Nyström remain credited. No new construction, historical priority, or present worldwide openness is claimed.

## 1. Exact target and normalization

The claim is existence of a smooth global potential phi on P1 with omega_phi=omega_FS+ddc phi strictly positive, such that the bounded Bedford–Taylor homogeneous complex Monge–Ampere Dirichlet solution with f(z,tau)=phi(tau z) on the outer circle lacks a real quadratic Taylor expansion at a point with 0<|tau|<1. Failure of maximal rank or only boundary nonsmoothness would not suffice.

Use d^c=i/(4 pi)(barpartial-partial). Then ddc=i/(2 pi)partial barpartial, ddc log|z|^2=delta_0, and omega_FS=dx dy/[pi(1+|z|^2)^2] has total area one. Direct radial integration gives integral_0^infinity 2r/(1+r^2)^2 dr=1. AIF printed p.7 displays a doubled d^c prefactor while also imposing the unit-pole/area-one identities. I visually checked that printed inconsistency. The manuscript’s coherent convention agrees with the IHES normalization and does not import the doubled prefactor. This is an apparent source inconsistency, not an author-confirmed erratum.

## 2. Credited geometric input, including the cover

AIF Proposition 3.4 permits a genuine curve segment S and gives phi smooth and strictly positive. Definition 1.2 fixes a contact time 0<T<1 and simple connectivity through the limiting open domain. The proof chooses punctures outside the closure of the limiting domain; its closure bars were visually checked on printed p.15. The selected component U_T of the inverse image projects biholomorphically to Omega_T because the latter is simply connected. Distinct lifted boundary points may identify, while open interior points do not. The two distinct boundary arcs above an interior contact point give the two fluid sides of the physical slit. Choosing q away from endpoints and other contacts and shrinking B gives B minus S contained in Omega_T.

AIF Theorem 2.15 supplies a smooth lifted strong family on a two-sided interval. The precursor arXiv:1212.2337v2, section 7 through Remark 7.1, explicitly gives the modification of permeability and the two-sided family; its nonzero tangent along the disc boundary yields a nonvanishing outward boundary velocity. AIF Theorem 6.2’s proof independently records the limiting nonvanishing velocity for this particular construction. The universal cover of this punctured sphere is C or the disc; the compact smooth lifted closure and a small collar fit in a fixed conformal chart. Thus the planar smooth Dirichlet-dependence proof of Appendix A applies after restricting the time interval compactly. No regularity of the projected post-contact boundary is needed.

## 3. Current removal and the negative Green inequality

Let Omega=Omega_T and D=Omega union B. D is open and connected, and D minus Omega is an arc piece of zero area. Its complement has positive omega_phi area 1-T. A positive-area compact subset of the sphere is nonpolar, so the domain is Greenian. Omega is Greenian as well, also by its conformal smooth lift.

The exact current identity is

    omega_FS+ddc psi_t = 1_(Omega_t^c) omega_phi + t delta_0.

On D this says omega_FS+ddc psi_T=T delta_0. There is no unlisted line measure: the identity supplies the entire current. Distributional harmonicity away from the pole followed by Weyl regularity gives continuation across the arc. This does not assert that positive-capacity sets are generally removable.

For h>0 with T+h<1, v_h=(psi_(T+h)-psi_T)/h is nonpositive. Subtracting the current identities on D gives

    ddc v_h=delta_0+h^(-1)1_(Omega_(T+h)^c)omega_phi=delta_0.

The last equality uses Omega contained in Omega_(T+h), so any remaining support in D lies on the zero-area added arc. In particular v_h has exactly the unit fixed logarithmic pole and is harmonic off it. It is a negative Green competitor with the correct sign.

For rigor without assuming a regular boundary for D, exhaust D by connected smooth relatively compact D_j containing the pole and the evaluation point. The pole cancels in v_h-G_(D_j); its boundary upper limits are nonpositive. The maximum principle yields v_h<=G_(D_j), and monotone exhaustion yields v_h<=G_D. Enlargement similarly yields G_D<=G_Omega. At a slit interior point q, each lifted smooth boundary side gives G_Omega->0. In contrast G_D(q)<0 because q is interior. The nonnegative harmonic difference G_Omega-G_D, with its pole removable, is nonzero. The strong maximum principle yields strict positivity throughout Omega. Thus at every fixed w in Omega minus {0},

    a'_+(T)<=G_D(w,0)<G_Omega(w,0).

A point-only contact would not establish B minus S contained in Omega or this strict comparison. No post-contact filling rate enters.

## 4. Finite negative left curvature

For w fixed in Omega minus {0}, continuity of the envelopes, or the increasing smooth lifted family, puts w in Omega_t for all t<T sufficiently close to T. On the lifted smooth family, psi_t-phi solves the Dirichlet problem ddc(psi_t-phi)=t delta_0-omega_phi with zero boundary value. Subtracting its fixed logarithmic singular part and pulling to a fixed disc gives a smooth elliptic parameter problem. This justifies differentiating it.

Differentiating psi_t=phi along its smooth moving boundary gives a zero time derivative there, since spatial C1 smooth fit cancels the velocity term. The derivative is harmonic off the pole and has pole coefficient one. Green uniqueness therefore gives a'(t)=G_(Omega_t)(w,0). The covering map is fixed; the lifts of w and 0 remain fixed, so there is no moving-evaluation-point term.

Smooth lifted Green dependence through T yields k0=a'_-(T)=G_Omega(w,0) in (-infinity,0). Let H be the time derivative of that Green function on U_T. Its time-independent log pole differentiates to zero, so H is harmonic even at the pole. Differentiating its zero boundary value gives H=-V partial_n G. V>0 by the increasing nonvanishing strong flow, and partial_n G>0 by Hopf for the negative Green function. Smoothness on the compact boundary makes H finite and strictly negative. The maximum principle gives

    L=a''_-(T)=H(w) in (-infinity,0).

This establishes the required nonzero finite curvature on the lift, rather than transferring the main problem to an unsupported smoothness assertion at the physical contact boundary.

## 5. Global support and unequal Taylor coefficients

For w not the pole, the envelopes are finite on [0,1]: a uniform lower competitor is t log(|w|^2/(1+|w|^2))+C with C chosen below the obstacle, and phi bounds them above. The endpoints preserve concavity. Put b=G_D(w,0)<k0. Concavity gives

    a(t)-a(T)<=k0(t-T), t<T;
    a(t)-a(T)<=b(t-T), t>T.

For b<k<k0, subtract k(t-T). On either side the resulting objective difference is strictly negative. Thus T is the unique global optimizer, including endpoints. For k>k0 near k0, local L<0 gives a unique t_k<T with a'(t_k)=k. Concavity makes its tangent supporting line global. A second optimizer would force linearity between the two optimizers and contradict strict local curvature near t_k.

Consequently F(k)=k+sup_t(a(t)-kt) is affine to the left of k0. With d=k-k0>0 and x=t_k-T,

    x=d/L+o(d),
    a(T+x)=a(T)+k0*x+L*x^2/2+o(x^2),
    F(k0+d)-F(k0)-(1-T)d=-d^2/(2L)+o(d^2).

The left residual is identically zero, whereas the right quadratic coefficient is positive. This directly excludes a second-order Taylor/Peano expansion; it does not rely only on unequal limiting Hessians.

The independent rational control script optimizes both quadratic branches and endpoints across 972 parameter/step cases with 5,832 exact optimizer/residual checks. Normal and optimized execution match, using explicit exceptions. A no-gap smooth quadratic control has equal two-sided coefficient 3/14. For the infinite-left-curvature model a(T+x)=k0*x-(-x)^(3/2), x<0, the right conjugate gain is 4*d^3/27, whose quadratic coefficient tends to zero. Thus a gap alone would not force the manuscript’s conclusion without finite nonzero L. These controls corroborate scalar algebra only.

## 6. Actual weak PDE and interior transfer

The original IHES Definition 2.1 and Proposition 2.3/Theorem 2.7, and AIF Section 4, identify the actual boundary envelope and its Bedford–Taylor equation, not just a formal transform. Min phi is an admissible constant lower bound, while comparison on each vertical subharmonic disc bounds the envelope by max phi. This gives a bounded weak solution with the prescribed smooth boundary trace.

Take tau*=exp(k0/2), z*=w/tau*. The finite strictly negative k0 gives 0<tau*<1. The exact twist along c(k)=(w exp(-k/2),exp(k/2)) simplifies to

    Phi(c(k))=F(k)+log[(1+|w|^2)/(exp(k)+|w|^2)].

The correction is smooth. c is a smooth curve through a genuine interior point with a nonzero tangent. Any ambient second-order Taylor expansion restricts to one on this curve: its linear term evaluated on c'' adds the same quadratic coefficient from either side, and the o(|h|^2) remainder is o(d^2). A smooth correction also changes both coefficients equally. The mismatch therefore proves the exact claimed defect.

On |tau|=1 the map z->tau z is a smooth circle action on P1 preserving omega_FS. The boundary trace is jointly smooth and its fibre form is the pullback of omega_phi>0. This checks the global strict-data requirement, including the infinity chart. The argument freely chooses a finite affine w to avoid unnecessary coordinate complications.

No empirical/model assumptions are present. The strongest result verified is this attributed existence deduction from the published contact-arc construction and standard potential/elliptic foundations. No mathematical gap remains in that deduction within the checked assumptions. Its historical firstness remains unestablished.
