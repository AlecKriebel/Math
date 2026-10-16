# Primary sources for the inverse-class and closure analysis

16 October 2026. This is a targeted hypothesis check supporting the authored class analysis, not a renewed general regularity survey. The exact equivalence and finite-energy closure are proved in the companion reports rather than attributed to a theorem for a different energy.

## Applicable inverse and area results

Bresciani–Davoli–Kružík, *Existence results in large-strain magnetoelasticity*, AIHP ANL 40 (2023), 557–592, Proposition 2.5, pp.566–567, and Remark 2.6, p.567, give the Sobolev inverse and inverse area formula under the standing three-dimensional p>3 assumption, positive Jacobian and a.e. injectivity. This supplies the primal-to-dual direction previously verified in pass 2. It cannot simply be applied backwards to a generic v∈W^{1,9/5}.

https://ems.press/content/serial-article-files/28047?nt=1

Barchiesi–Henao–Mora-Corral–Rodiac, *A relaxation approach to the minimisation of the neo-Hookean energy in 3D*, arXiv:2311.02952v2 (20 May 2024), Proposition 2.1 and Definition 2.2, p.5, provide the approximately differentiable area formula and good-set construction used in the reduced characterization. The rendered page was checked.
https://arxiv.org/pdf/2311.02952v2

## A related global divergence-identity class has a different exponent threshold

Mora-Corral–Mur-Callizo, *Invertibility of Sobolev maps through approximate invertibility at the boundary and tangential polyconvexity*, arXiv:2503.01795v1 (3 March 2025), equation (3.2), Definition 3.1, and Theorem 4.1, p.5, impose divergence identities up to the boundary and Sobolev regularity of the boundary trace. The injectivity theorem assumes p>d−1. Proposition 10.1, p.19, gives sequential compactness with that same strict exponent threshold, bounded bulk and boundary W^{1,p} norms, and equiintegrable determinants.

In dimension three, the inverse exponent 9/5 does not satisfy p>2. Thus these theorems cannot be used to infer inverse injectivity or closure merely from its finite energy and smooth trace. The companion characterization instead proves the needed assertion directly, using its separately imposed global Piola identity and the high integrability of the recovered primal derivative.

https://arxiv.org/pdf/2503.01795v1

## What the neo-Hookean relaxation theorem actually proves

The same paper's §1.2, pp.2–3, concerns |Du|²+H(det Du), thick boundary data, and an enlarged class with BV inverses and potentially negative Jacobians. Its modified energy penalizes the singular inverse derivative. Theorem 1.1, p.3, proves compactness and lower semicontinuity for that modified problem. The following discussion, pp.3–4, leaves equality with the full sequentially relaxed energy unproved.
Those conclusions do not identify arbitrary finite-V maps with E-6322 inverses or authorize substituting a weak closure of homeomorphisms for the frozen full primal class. In our exact class, bounded dual energy lifts to primal W^{1,6} compactness, and the singular-inverse limit mechanism is excluded by the separate inverse W^{1,9/5} bound. The exact lower-semicontinuity proof therefore does not require a neo-Hookean relaxation theorem or an inverse singular-part penalty.

## Approximation status and precise limitations

No approximation by diffeomorphisms is needed anywhere in the proved exact transfer. No verified source in this targeted check shows that every original finite-energy competitor has an energy-recovery sequence of diffeomorphisms, or that every finite-dual-energy map with trace G⁻¹ satisfies the full-boundary transported Piola identities. Neither assertion is made.

The transport characterization is deliberately stronger than a bulk distributional Jacobian equality or an ordinary inverse trace alone. Full boundary flux prevents losing the prescribed degree information at the boundary. The reduced characterization shows exactly what must be checked; the additive-comparison lemma verifies it for smooth compact additions whenever the resulting dual energy is finite.
