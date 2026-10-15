# Independent spectral and exact-reproduction report

Problem 30000999 / PR466. Completed independently on 2026-10-12 UTC. Scope: the frozen release proof's stated equator-averaging convention, its explicit harmonic family, radial moments, gradient estimates, and finite checker reproducibility. This report does not independently establish bibliographic priority or correspondence with every external formulation of the problem.

**Disposition:** no mathematical fault found in the stated spectral/moment argument or its finite-real-p conclusion. The unrestricted negative result follows from antipodal point masses. The stronger even-density result follows for every fixed n >= 3, a in (0,1), and finite real p >= 1. The finite computations below support transcription and falsification only; the all-parameter conclusion depends on the analytic derivation given here. No discretized optimal-transport value is used as proof.

## Independence and starting scope

I read only release/PROOF.md first and wrote INITIAL_HYPOTHESIS.md at 06:32:43 UTC before opening either checker, historical audit results, or peer reports. I did not read historical AUDIT.md or its verdict prose. After recording the hypothesis, I inspected the two checker sources for safe replay and authored wick_controls.py without importing either source module. Its mechanism is covariance-based colored Gaussian contractions, not the original rational equator-frame computation or the historical Gegenbauer recurrence.

All authored files and diagnostics are confined to this review folder. No source, root, Git index, branch, cloud artifact, or external communication was modified or used. The private directories contain no publication candidates. PUBLICATION_MANIFEST.json is a positive, explicit file whitelist; it does not discover candidates recursively.

## Target claims and boundaries

The metric is intrinsic geodesic distance on the unit sphere S^(n-1). The transform averages over the normalized equator perpendicular to its argument, including its two-point interpretation at n = 2. The measure transform is dual to that function transform. The target inequality is a same-order global Lipschitz inverse bound for probability measures.

The point-mass result requires only n >= 2: both antipodes have the same equator measure and their Wasserstein distance is pi, for every finite p >= 1. The strengthened result uses k even, H_k = Re(x_1+i x_2)^k, and rho_k = 1+aH_k. It assumes no uniform derivative bound. An inverse modulus on all probabilities is impossible, but the argument does not settle derivative-bounded, finite-bandwidth, Hölder-modulus, support-restricted, or even-density W_infinity questions. For even measures on the circle, the transform is a quarter-turn isometry; dimension two is an essential boundary.

## Independent all-parameter spectral reconstruction

Put P = I-u u^T and w = e_1+i e_2. A standard Gaussian G in R^n has projected covariance P. Its real projected coordinate factors A = e_1 dot PG and B = e_2 dot PG have

    C00 = 1-u_1^2,  C01 = -u_1 u_2,  C11 = 1-u_2^2.

The Gaussian generating function is exp((C00 t^2+2 C01 ts+C11 s^2)/2). Differentiating it gives the colored contraction recurrence

    W(r,s) = (r-1) C00 W(r-2,s) + s C01 W(r-1,s-1),
    W(0,s) = (s-1) C11 W(0,s-2),  W(0,0)=1,

with odd total degree zero. This is an exact covariance mechanism and does not require a rational equator frame. Substitution of s=i t is a formal polynomial substitution in the generating function, so

    E(A+iB)^(2m) = (2m-1)!! (C00-C11+2i C01)^m.

The crucial contraction is

    C00-C11+2i C01 = -(u_1+i u_2)^2 = (Pw) dot (Pw).

It is bilinear. The Hermitian norm would instead produce C00+C11; that is a different quantity and fails already at u=e_1, degree two.

The Gaussian PG is an isotropic Gaussian on the d=n-1 dimensional equator space. Its radius R and unit direction X are independent; the direction is uniform on that sphere. The radial chi-square integral gives

    E R^(2m) = 2^m Gamma(m+d/2)/Gamma(d/2)
               = product_{j=0}^{m-1}(d+2j).

Divide the Gaussian homogeneous moment by this radial moment and take real parts. For every u, n >= 2, and m >= 0,

    F H_(2m) = lambda_(2m) H_(2m),
    lambda_(2m) = (-1)^m product_{j=0}^{m-1}(2j+1)/(n-1+2j).

Odd modes vanish. Each displayed even eigenvalue is nonzero. It has modulus at most one, strictly less than one for n >= 3 and m >= 1. Dimension two gives exactly (-1)^m. No irreducibility or representation-theoretic extension is needed: the argument establishes this particular harmonic family directly.

Gamma recurrence independently converts the product to

    |lambda_(2m)| = Gamma((n-1)/2) Gamma(m+1/2)
                       / (sqrt(pi) Gamma(m+(n-1)/2)).

For alpha=(n-2)/2 > 0, the Gamma ratio has order m^(-alpha), hence order k^(-alpha) for k=2m. The change from m to k contributes a positive factor 2^alpha; omitting that factor affects the constant, not the exponent. The supplied proof states its asymptotic in m correctly.

## Independent radial distribution and energy reconstruction

For a uniform direction in R^n, let U=G_1^2+G_2^2 and V=sum_{j=3}^n G_j^2. They are independent chi-square variables with two and n-2 degrees of freedom. Transforming their gamma densities to T=U/(U+V), S=U+V gives T the density alpha(1-T)^(alpha-1) on (0,1). Thus for every real q >= 0,

    M(q) = E r^q = alpha integral_0^1 t^(q/2)(1-t)^(alpha-1) dt
         = Gamma(alpha+1) Gamma(q/2+1)/Gamma(q/2+alpha+1).

This uses Beta(1,alpha), where alpha=(n-2)/2, not (n-1)/2. The first two coordinate angle is uniform and independent of r by planar rotational invariance. Therefore E H_k^2 = M(2k)/2 for every integer k >= 1.

Direct differentiation gives

    partial_1 H_k = k Re z^(k-1),
    partial_2 H_k = -k Im z^(k-1),
    |grad_Rn H_k|^2 = k^2 r^(2k-2),
    x dot grad_Rn H_k = k H_k.

The Euclidean Laplacian is zero because the two second derivatives multiply 1+i^2. Orthogonal projection to the tangent plane consequently gives the sharper identity

    |grad_S H_k|^2 = k^2 [r^(2k-2)-H_k^2].

The gradient bound k r^(k-1) follows without approximation. Its p-th-power integral is at most k^p M(p(k-1)) for every finite real p >= 1. The homogeneous harmonic identity gives -Delta_S H_k=k(k+n-2)H_k. Independently, the integrated gradient energy is

    E |grad_S H_k|^2 = k^2 [M(2k-2)-M(2k)/2]
                     = k(k+n-2) M(2k)/2.

The second equality follows from M(2k)/M(2k-2)=k/(k+alpha). It agrees with integration by parts, and checks both the tangential correction and the Laplace eigenvalue without using the latter as its input.

The mean of H_k is zero by a planar rotation through pi/k. Even k gives H_k(-x)=H_k(x), while |H_k| <= 1. Hence rho_k is a smooth even probability density with 1-a <= rho_k <= 1+a.

## Distance argument and real-p limiting exponent

The invariant probability on ordered orthogonal pairs is unique under the transitive O(n) action. Swapping coordinates preserves that invariant probability. Consequently F is self-adjoint and R(rho sigma)=(F rho)sigma, including R sigma=sigma.

Since |grad_S(H_k/k)| <= 1, the intrinsic Lipschitz test against any coupling gives

    W_p(rho_k sigma,sigma) >= W_1(rho_k sigma,sigma)
                              >= a M(2k)/(2k).

The first inequality uses the L^p-versus-L^1 inequality on a probability coupling. It needs no dual attainment theorem.

For b=a lambda_k and L=k(k+n-2), take eta_t=1+t bH_k and

    v_t=b grad_S H_k/(L eta_t).

Its denominator is at least 1-a. The continuity residual is bH_k+(b/L)Delta_S H_k=0 with the displayed positive sign in v_t. The smooth compact-manifold flow exists on [0,1]; its Jacobian identity pushes sigma to eta_t sigma. Thus it provides an actual coupling. The path-length bound, Jensen inequality for every real p >= 1, and change of variables yield

    W_p(R mu_k,sigma)^p <= |b|^p L^(-p)(1-a)^(1-p)
                            integral |grad_S H_k|^p d sigma.

Taking a p-th root and using the radial majorant gives the supplied output upper bound. The output differs from sigma because its nonzero eigenvalue multiplies a nonzero H_k, so the ratio denominator is strictly positive.

For every fixed finite real p >= 1, Gamma ratio asymptotics give

    M(2k) ~ Gamma(alpha+1) k^(-alpha),
    |lambda_k| ~ [2^alpha Gamma(alpha+1/2)/sqrt(pi)] k^(-alpha),
    M(p(k-1))^(1/p) ~ Gamma(alpha+1)^(1/p)
                            (p/2)^(-alpha/p) k^(-alpha/p).

Accordingly the ratio lower bound is asymptotic to D k^(alpha/p), with the independently reconstructed positive constant

    D = sqrt(pi) (1-a)^(1-1/p) Gamma(alpha+1)^(1-1/p)
           (p/2)^(alpha/p) / [2^(alpha+1) Gamma(alpha+1/2)].

The exponent is -alpha-(-alpha-alpha/p)=alpha/p, including p=1 and noninteger p. As an exact cross-check, n=4 and p=1 give D=1/4, agreeing with the rational specialization's leading term. The inference is for each fixed finite p; it does not interchange p-to-infinity and k-to-infinity limits. At p=infinity the displayed exponent would be zero, so this divergence proof supplies no even-density conclusion. At n=2 alpha is zero and the positive-decay hypothesis fails, consistent with the exact circle isometry. At n=1 the normalized equator transform is undefined.

## Reproduction and falsification evidence

The original author checker reports 591 finite checks, and the historical independent checker reports 3812. Both reproduced their own frozen expected JSON byte-for-byte in normal Python and Python -O, exit zero. Their counts are bounded tests, not coverage of all parameters. The original sources contain ancillary assert preconditions, removed by optimization; their explicit check functions still raise on failed tested conditions. The fresh checker uses explicit exceptions throughout, including preconditions.

The new checker reports 4844 successful finite exact checks, with identical normal and optimized JSON. The count includes scope/unit-vector checks and exact simplifications inside a negative trial; it should not be read as 4844 independent discoveries. Its main eigenvalue family tests dimensions 2..10, three rational directions each, and even degrees 0..24; the radial/energy family tests dimensions 3..12 and degrees 1..16. The circle family reaches degree 100. Real-p controls sample seven rational orders, including nonintegers and 1,000,000. The proof for all real p is analytic above.

Nine deliberately false alternatives were also executed separately. Each exited 1 with an explicit InvalidClaim exception in both normal and optimized modes, for 18 observed rejection runs. Concrete separating values include:

| False alternative | Exact separating value |
| --- | --- |
| Hermitian projection contraction | n=4, u=e_1, k=2: actual -1/3, false +1/3 |
| Ambient dimension in equator denominator | Same actual -1/3, false -1/4 |
| Beta(1,(n-1)/2) radial parameter | n=3: E r^2=2/3, false 1/2 |
| Ambient gradient energy without projection | n=3, k=2: true 8/5, false 8/3 |
| Exponent alpha(1-1/p) | n=3, p=1: true 1/2, false 0 |
| Shifted Gamma denominator | n=3, k=2: actual -1/2, false -1/3 |
| Reversed transport flow | b=1/5, H=1 gives residual 2/5 rather than zero |
| Strict spectral decay on the circle | n=2, k=20: modulus exactly 1 |
| Applying the equator theorem in dimension one | Explicit scope rejection before forming an undefined equator moment |

The rejection evidence is diagnostics/reproduction_summary.json and the per-control stderr files. These are valid test diagnostics generated by the authored checker; no invalid mutated source was selected for publication. The actual false alternatives are parameters of a valid falsification test, not proposed mathematical results.

All three frozen manifests were checked field by field: 30 reference records, including the audit's author-manifest hash reference. Every declared byte count, SHA-256, and supplied Git blob SHA matched. The blob hashes were computed directly as SHA-1 of the Git blob header plus bytes; no Git command or index operation was used. Inventories before and after all runs agree on all 17 frozen source files.

## Strongest verified result and remaining gap

Under the exact convention and hypotheses in the frozen proof, the unrestricted inverse inequality is false, and for n >= 3 the proposed same-order inverse bound also fails on smooth even densities with fixed positive upper/lower density bounds at every fixed finite real p >= 1. The spectral and moment calculations have both an independent analytic derivation and finite exact controls with demonstrated sensitivity to errors.

No unresolved mathematical gap was identified within that stated scope. This is an independent AI-assisted audit, not human peer review, a novelty certification, or evidence of optimality of the displayed exponent. The exact remaining limitations are the external-source correspondence/priority questions, the unclaimed restricted classes, and the unproved optimal actual Wasserstein ratio or even-density W_infinity behavior. The original proof itself labels these limitations appropriately.
