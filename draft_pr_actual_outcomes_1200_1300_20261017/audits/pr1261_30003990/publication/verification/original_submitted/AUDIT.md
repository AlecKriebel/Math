# Independent audit: convex-body SOS-density rate

Date: 2026-10-11. Source question: OWR-16633-006.

## Verdict and exact version

**PASS for the scoped mathematical claim.** The accepted final proof is `PROOF.md`, 8,867 bytes, SHA256 `a49d5c37e132810d22219271cd225f9519618b1eb8ae8b63ce424e5eaa00a03a`. The earlier 6,898-byte version, SHA256 `47f1eb8b49d38b6b041529ad65c42f17ffba71002158703fc6ad743986b34e6f`, was also fully reviewed. The final revision clarifies the C^2-neighborhood condition and adds source context; the proof mathematics is unchanged. Its construction proves the claimed O(r^-2) upper rate for every fixed compact convex body with nonempty interior, fixed real polynomial objective, and n-dimensional Lebesgue reference measure. No proof correction is required.

This is an independent mathematical audit, not a machine-checked formal proof or a certification of novelty. The proof improves on the rate stated in the inspected general-convex-body sources. The literature screen did not locate the same full theorem, but is bounded and cannot establish priority or current-open status.

## Exact accepted theorem

Let K be a compact convex subset of R^n, n>=1, with nonempty interior, and f a real polynomial. Define

    H_r = inf { integral_K f q dx : q is a global sum of squares,
                degree(q)<=2r, integral_K q dx=1 }.

For any minimizer a of f on K set

    gamma=1+(1/2) max_K ||Hess f||_op,
    g(x)=gradient f(a) dot (x-a)+gamma||x-a||^2,
    G=max_K g,   L=n+2,
    C_n=4L^2 (pi/2)^(2L) (1+2^(n+2)).

Then G>0 and, for every integer r>=1,

    0 <= H_r-min_K f <= C_n G/r^2.

If D=diam(K), B=max_K||gradient f|| and H=max_K||Hess f||_op, then

    G <= BD+(1+H/2)D^2.

Thus the constant can be bounded independently of the choice of minimizer. The result is an existence/rate statement: computing a, G, or the witness density efficiently is not asserted.

## Independent derivation

### 1. Proxy geometry

For every x in K, s -> f(a+s(x-a)) has a right minimum at zero on [0,1]. Its right derivative is nonnegative, so ell(x)=gradient f(a) dot (x-a)>=0. Taylor's integral remainder on the same segment is at most (H/2)||x-a||^2. Consequently 0<=f(x)-f(a)<=g(x), g(a)=0, and g(x)>0 on K outside a. Compactness gives finite positive G. The polynomial u=g/G has degree at most two and range [0,1] on K.

For 0<=alpha<=1,

    g(a+alpha(x-a))
      =alpha ell(x)+alpha^2 gamma||x-a||^2
      <=alpha g(x).

Let S_t={x in K:u(x)<=t} and F(t)=vol_n(S_t), for all t>0. For 0<s<=t, the injective homothety x -> a+(s/t)(x-a) maps S_t into S_s and has Jacobian (s/t)^n. Therefore

    F(s)>=(s/t)^n F(t), or F(t)<=(t/s)^n F(s).

The inequality holds for t>1 as well. In particular F(s)>=s^n vol(K)>0 for 0<s<=1. Its direction is exactly the direction needed to control shell mass relative to the kernel's core mass.

### 2. Algebraic endpoint kernel

For m>=1, N=2m+1, set

    A_m(t)=[1+2 sum_{j=1}^m T_j(1-2t)]/N.

This is a real polynomial of degree m, not a trigonometric function of the original variables. On 0<t<=1, put v=arcsin(sqrt(t)). The finite cosine-sum identity gives

    A_m(t)=sin(Nv)/(N sin v)=sin(Nv)/(N sqrt(t)).

The original cosine sum gives |A_m|<=1. The numerator in the sine ratio gives |A_m(t)|<=1/(N sqrt(t)). Put h=N^-2. For 0<t<=h, the convexity chord bound arcsin(z)<=pi z/2 gives Nv<=pi/2. Since sin(w)>=2w/pi on [0,pi/2] and v>=sqrt(t), A_m(t)>=2/pi. At t=0 this follows from A_m(0)=1. This bound does not require monotonicity of the oscillating kernel.

### 3. The full moment ratio

Take L=n+2 and Q=A_m(u)^(2L). The positive core gives

    Z=integral_K Q dx >= (2/pi)^(2L)F(h)>0.

On K, Q<=1 and Q<=(h/u)^L where u>0. The core contributes at most hF(h) to integral uQ. On the disjoint shells E_j={2^j h<u<=2^(j+1)h}, j>=0,

    integral_{E_j} uQ
      <=2^(j+1)h 2^(-jL) F(2^(j+1)h)
      <=hF(h) 2^(n+1) 2^(j(n+1-L)).

Only finitely many shells meet K. Extending their nonnegative upper bounds to an infinite sum is valid. Because L=n+2, the last geometric series has ratio 1/2 and sum 2. Thus

    integral_K uQ / integral_K Q
       <=(pi/2)^(2L)(1+2^(n+2))/(2m+1)^2.

The same F(h) appears on both sides and cancels. This is the decisive distinction from replacing F(h) by an absolute power bound while bounding the entire tail by vol(K). No logarithm remains.

### 4. Admissibility and degree

For r>=2L choose m=floor(r/(2L)). The polynomial A_m(u)^L has degree <=2mL<=r, so Q is one global square of degree <=2r. Since Z>0, q=Q/Z is also one global square, [A_m(u)^L/sqrt(Z)]^2, and has exactly unit integral on K. Positivity of g or u away from K is unnecessary.

The feasible witness gives H_r-f(a)<=G integral uQ/Z. Also 2floor(r/(2L))+1>=r/(2L), yielding the constant C_n above. For 1<=r<2L the constant density 1/vol(K) has error <=G, while C_n/r^2>1. This proves the displayed theorem for all its integer orders. Alternatively A_0=1 handles the small orders in the same family; the supplied proof's separate small-order argument is already correct.

## Adversarial checklist

- **Boundary minimizers:** The derivative is one-sided along segments in K. No interior first-order condition or vanishing gradient is presumed.
- **Nonconvex f:** Convexity is required of K and the chosen upper proxy, not of f.
- **Taylor regularity:** Polynomial f is C^2 on a neighborhood of K. The optional C^2 extension is valid for objectives C^2 on a neighborhood of K with bounded Hessian there along the segments. A merely Lipschitz objective is not covered by this extension.
- **Constant/affine f:** The added 1 in gamma ensures G>0 even when the Hessian and gradient vanish. Constant f has exact zero hierarchy error; the positive upper bound is harmless.
- **Thin or nonsmooth K:** No smoothness, curvature, semialgebraicity, or simplex decomposition is used. K may have nonsimple vertices or arbitrarily small fixed width; interior ensures positive volume.
- **Final shell:** F is defined above 1 and the homothety proof still works. Alternatively cap its upper endpoint at 1. Neither approach changes the estimate.
- **Level-set atoms:** No differentiation of F, density formula, or absolute continuity of its push-forward is used. The argument works as a measure estimate.
- **Zeros and sign changes of A_m:** The denominator uses only the positive core; the tails use absolute bounds and an even power. There is no division by A_m.
- **Fixed exponent:** L=n+2 is fixed as r grows. The degree cost is a dimension-dependent constant. Taking L=n+1 would leave a divergent geometric upper bound and would not justify this proof.
- **SOS category:** The actual witness is a global square. Merely nonnegative-on-K polynomials or weighted/preordering SOS representations are never substituted.
- **Reference measure:** The normalization and objective remain Lebesgue integrals over the original K. No Chebyshev reweighting or omission of mass outside a local model occurs.
- **Hierarchy order:** The objective's degree does not enter the density degree because the polynomial composed into A_m is the quadratic proxy. The proof establishes the ordinary multivariate SOS-density hierarchy, not generally the more restrictive hierarchy s(f(x)).
- **Uniformity:** K, f, n are fixed for the O(r^-2) assertion. No dimension-free or shape-free numerical bound, exact leading coefficient, or two-sided rate for every objective is asserted.

## Supplemental moment formulation

The supplemental `MOMENT_FORMULATION.md`, 3,099 bytes, SHA256 `b1988e13ab99ba0614d0695c67448bbf6538267ed75c271c5be48eb7c8f3cc37`, is also accepted. For the square pyramid 0<=z<=1, |x|<=z, |y|<=z, direct integration gives the stated rational moments and volume 4/3. The moment matrix is positive definite, and every SOS Rayleigh quotient is a weighted average of its constituent single-square quotients, proving the exact generalized-eigenvalue formulation. The witness A_m(z)^10 has degree 10m and is feasible at order 5m. Its full-pyramid objective ratio is exactly the ratio of integrals with weights z^3 and z^2. The apex cone has four extreme rays and is pointed; nonvertex cube/simplex boundary cones have lineality, while their vertex cones have three extreme rays. Thus the claimed local affine distinction is valid. This example supports category fidelity; it is not needed for the general analytic proof.

## Source matching and bounded prior-work check

The following are statements of the inspected sources, not an inference that no other work exists. Full retrieval and full proof inspection are different; the exact read scope is recorded separately.

1. **OWR 50/2018, Laurent contribution, PDF pp.23-25 / printed pp.2991-2993.** Item (2) specifies convex bodies and Lebesgue measure. The concluding question concerns the convergence regime. The normalization omission in equations (3)-(4) is visibly present in the printed PDF, not merely OCR: '=1' is missing. The theorem audited here explicitly restores probability normalization, consistent with the prose and later papers. [Public report](https://ems.press/journals/owr/articles/16633).

2. **Slot–Laurent, Improved convergence analysis, arXiv:1905.08142v2.** PDF p.2 defines global SOS degree <=2r and unit mass. Pages 5-6 already justify the constrained gradient and quadratic upper-proxy reductions. Theorem 11 on p.17 gives O(log^2(r)/r^2), and p.29 explicitly asks for removal of the logarithm. Lemma 20 and Corollary 5 on p.24 substantiate the final proof's comparison with the previous absolute-normalization/tail estimate. The audited proof uses the same target hierarchy and geometry. It does not discover the proxy reduction. [Paper](https://arxiv.org/abs/1905.08142).

3. **Laurent–Slot, final 2026 overview.** PDF p.10 equation (14) confirms the hierarchy, and p.11 Table 1 still reports the logarithmic general-convex-body rate. Pages 16-17 explain the weaker original-objective push-forward hierarchy. The final chapter's table is evidence about what that source states, not proof of present novelty. [Final chapter](https://ir.cwi.nl/pub/36052/36052.pdf).

4. **Slot–Laurent, Near-optimal analysis, DOI 10.1007/s10107-020-01586-y.** The retained publisher-formatted PDF obtained at arXiv:2001.11289 has its two hierarchies explicitly distinguished on pp.2-3. Its original-objective push-forward result is O(log^2(r)/r^2). The candidate uses s(g(x)); its proof does not settle the s(f(x)) rate for general nonconvex f. [Paper](https://arxiv.org/abs/2001.11289).

5. **de Klerk–Hess–Laurent, arXiv:1603.03329v2 / SIOPT 2017.** Theorem 1.5 concerns the hypercube with Chebyshev measure and Schmudgen-type densities. Section 2.2 explicitly uses Jackson kernels. These are established precursors to polynomial-kernel concentration, but that theorem does not give the present arbitrary-convex-body Lebesgue/global-square claim. The retained PDF's title page has an internal June 21, 2021 date despite its arXiv v2 banner and metadata dating the revision to 2017; this audit does not infer a different theorem version from that date alone. [Paper](https://arxiv.org/abs/1603.03329).

6. **Gribling–de Klerk–Vera, arXiv:2605.31496v1, May 2026.** Section 4.3, Proposition 14, gives a constructive O(r^-2) proof for the hypercube with product Chebyshev measure. Section 5 asks about extension of its kernel construction to more convex bodies. Its separate logarithm-cubed result concerns lower bounds/coefficient approximation and must not be confused with the density hierarchy audited here. The inspected statements do not subsume this theorem. [Paper](https://arxiv.org/abs/2605.31496).

7. **Totik–Varga, Non-symmetric fast decreasing polynomials and applications, JMAA 394 (2012), 378-390.** Section 3 develops endpoint Christoffel estimates for locally/globally doubling measures, and Section 4 discusses endpoint zero spacing. Such concentration and power-growth arguments are classical. Their hypotheses on interval-centered doubling are not automatically identical to the candidate's one-endpoint cumulative growth, and the inspected theorems do not state the full convex-body SOS consequence. This audit relies on its direct elementary derivation, not an unverified invocation of those theorems. [Author-hosted paper](https://www.math.u-szeged.hu/pot/5fdp.pdf).

**Priority conclusion:** the kernel idea is classical, the quadratic proxy is already in the cited SOS literature, and no originality is assigned to either ingredient. The relative-volume normalization argument provides a valid proof of the source-matched rate. Whether this exact consequence was previously proved, published, or circulated remains unverified.

## Verification limits and disposition

The mathematical acceptance rests on the full analytic derivation above. Exact-arithmetic example checks, degree-loop tests, SHA256 checks, and tamper controls are supplementary reproducibility checks, not a proof of the theorem for all K,f. The authored checker passes under normal Python, -O, and -OO: 1,677 rational kernel-grid cases, 20,000 degree/floor cases, 16 exact beta-moment examples, and three deliberately rejected invalid-exponent/degree controls per mode. No source-author code was run. No source was fully proof-audited, and no exhaustive literature search was performed. No publication, queue mutation, or outreach was performed by this auditor.

