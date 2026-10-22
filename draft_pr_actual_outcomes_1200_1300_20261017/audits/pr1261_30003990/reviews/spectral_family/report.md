# Independent spectral-family mechanism review

Date: 2026-10-17 UTC. Problem: PR1261 / problem30003990. Author metadata supplied for the project: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. This report is an independent mathematical derivation, not a priority claim or a final publication review.

## 1. Exact claim, isolation, and verdict

Let K be any fixed compact convex body in R^n, n >= 1, with nonempty interior, and let mu be normalized n-dimensional Lebesgue measure on K. For a fixed real polynomial f, define

    H_r(f) = inf { integral_K f q dmu : q is a global SOS,
                  deg q <= 2r, integral_K q dmu = 1 }.

The target is: there exists C_(K,f) < infinity such that

    0 <= H_r(f) - min_K f <= C_(K,f)/r^2    for every integer r >= 1.

**Independent conclusion:** the specified upper-rate claim has a complete spectral route, using the inspected upper estimate in Totik–Varga Theorem 3.1 as a standard import. The geometric hypothesis of that theorem is proved below for a quadratic majorizer, for every convex body in the stated class. No unsupported endpoint-zero assertion is left as a substitute for the original difficulty.

The central mechanism is **quadratic majorization -> full local doubling of the quadratic push-forward -> Christoffel upper estimate -> extreme orthogonal zero -> compressed multiplication eigenvector**. It does not rely on an explicit hand-selected concentrating density. It also does not assert suitable regularity for the original push-forward f#mu.

Only the assigned question and specified primary sources were inspected. No candidate/submitted files, root derivations, or other family reports were read. No external contacts, subdelegation, Git/PR/Zenodo/GWS changes, or reference/index mutations were made. Candidate comparison is outside this report and must occur only after its immutable manifest is written.

## 2. Standard import and exact inspection scope

The primary import is the upper half of Theorem 3.1 of Totik and Varga, *Non-symmetric fast decreasing polynomials and applications*, JMAA 394 (2012), 378–390, author PDF https://www.math.u-szeged.hu/pot/5fdp.pdf.

For a finite positive compactly supported measure nu with global left endpoint 0, suppose nu is doubling on [0,beta]. With

    lambda_k(z,nu) = inf { integral p(t)^2 dnu(t) : deg p <= k, p(z)=1 },
    delta_k(z) = sqrt(z)/k + 1/k^2,

that theorem gives, uniformly for 0 <= z <= gamma < beta,

    lambda_k(z,nu) <= C nu([z-delta_k(z), z+delta_k(z)]).

Here doubling means nu(2I) <= L nu(I) for every interval with 2I contained in [0,beta]; it is not merely a statement about [0,t]. The PDF's definition (3.1), Theorem 3.1 and its proof, including its exterior-support cutoff, were inspected. Theorem 4.1, its proof, and Section 5 were also inspected. We derive the needed endpoint estimate below rather than importing an unexamined zero-spacing assertion. This is ordinary use of the stated primary theorem; its underlying older references were not separately re-proved.

The other assigned sources were inspected for the problem convention and context:

- OWR report https://ems.press/journals/owr/articles/16633 and its PDF, Laurent's contribution, printed pp. 2991–2993: the full SOS hierarchy and the historical question about general convex bodies.
- Slot–Laurent https://arxiv.org/abs/1905.08142, PDF definition (3) and introductory spectral discussion: degree 2r means global SOS degree 2r, with unit integral.
- Laurent–Slot overview https://ir.cwi.nl/pub/36052/36052.pdf, Table 1, Sections 2.1–2.4: quadratic majorization and compressed multiplication provide context; the original-objective push-forward is not assumed understood.

These establish historical context, not a present-day priority/open-status determination. No exhaustive literature or novelty clearance was attempted.

## 3. Reduction to an isolating quadratic

Choose a global minimizer x* in K, translate it to 0, and subtract f(x*). Put a = grad f(0). Convexity gives

    a dot x >= 0 for every x in K.                                      (3.1)

Indeed, the segment s x belongs to K for 0 <= s <= 1, and the right derivative of f(s x) at its minimum s=0 is nonnegative. This does not require a differentiable boundary or a unique minimizer.

The Hessian of f is bounded on K. Taylor's formula along each segment gives a finite b > 0 such that

    0 <= f(x) <= h(x) := a dot x + b ||x||^2    for x in K.              (3.2)

For example take b >= 1 and b >= one half of the maximum Hessian operator norm. The polynomial h has degree two, is nonnegative on K, and has its unique zero there at 0. Let nu = h#mu. It is a finite positive compactly supported measure, with global left endpoint 0 and positive mass arbitrarily close to 0. The latter follows from a scaled copy of an interior ball joined to 0. The support is an interval because K is connected, and every nonempty relative-open part of K meets its interior.

All constants below may depend on K, a, and b. A positive scalar rescaling of h can put its maximum at 1 when using the dimensionless spectral estimates; multiplying back only changes the final constant.

## 4. Geometric measure lemma

**Lemma.** Suppose K is as above, 0 in K, a dot x >= 0 on K, b > 0, and h(x)=a dot x+b||x||^2. Then h#(dx|K) has a positive density w(t) for sufficiently small t > 0, and is doubling on some [0,beta].

Normalization by vol(K) makes no difference to this assertion.

### 4.1. Nonzero gradient: central projection makes projected level domains nested

Assume a != 0. Choose e in int(K). Then A := a dot e > 0: a nonzero linear functional that is nonnegative on a full-dimensional convex body cannot vanish at an interior point. Set E = {z : a dot z = 0}, and use coordinates

    x = X(u,z) := (1-u) z + u e,     z in E, u < 1.                    (4.1)

This is the central projection from e onto E. Its inverse and Jacobian are

    u = (a dot x)/A,
    z = (x-u e)/(1-u),
    dx = (A/||a||) (1-u)^(n-1) du dz.                                (4.2)

For n=1, E has dimension zero and dz assigns mass 1 to its single point; the same formulas apply.

Write G(u,z)=h(X(u,z)). Then

    G(u,z) = A u + b ||(1-u)z+u e||^2,
    G_u(u,z) = A + 2b X(u,z) dot (e-z).                               (4.3)

For points in K with h(x) <= beta,

    ||x|| <= sqrt(beta/b),       0 <= u <= beta/A,
    ||z|| <= [sqrt(beta/b)+(beta/A)||e||]/[1-beta/A].                  (4.4)

These quantities tend to zero as beta decreases. Therefore choose beta > 0 sufficiently small that u <= 1/4 and, on the required coordinate neighborhood,

    A/2 <= G_u(u,z) <= 3A/2.                                         (4.5)

This choice is justified by continuity at (u,z)=(0,0), where G_u=A. It can be made uniformly for 0 <= u <= beta/A and every z occurring in (4.4), and also for ||z|| <= sqrt(beta/b).

For each t in (0,beta] and z with b||z||^2 <= t, there is a unique u=u(t,z) in [0,beta/A] solving G(u,z)=t. In fact G(0,z)=b||z||^2 and G(beta/A,z) >= beta, while (4.5) ensures strict increase. Every point of K on h=t is obtained this way: (4.4) places it in the monotonicity neighborhood, and then G(0,z) <= G(u,z)=t.

Define

    D_t = { z in E : b||z||^2 <= t,
                    X(u(t,z),z) belongs to K }.

**The key inclusion is D_s subset D_t for 0 < s <= t <= beta.** For z in D_s, monotonicity gives u(t,z) >= u(s,z). Both are less than 1. Thus X(u(t,z),z) lies on the segment from X(u(s,z),z) to e, and belongs to K by convexity. No regularity of the boundary of K or of D_t is used.

Changing variables first by (4.1), then from u to t, gives

    w(t) = integral_(D_t) J(t,z) dz,
    J(t,z) = (A/||a||) (1-u(t,z))^(n-1) / G_u(u(t,z),z).               (4.6)

These are ordinary measurable-domain/Fubini formulas. They hold as density versions; values at any exceptional individual t are immaterial. The bounds (4.5) imply

    [2/(3||a||)] (3/4)^(n-1) <= J(t,z) <= 2/||a||.                   (4.7)

Consequently, with c0=(1/3)(3/4)^(n-1),

    w(t) >= c0 w(s)     whenever 0 < s <= t <= beta.                  (4.8)

Positivity is not assumed: it follows because the ray from 0 through e meets the interior of K at every positive fraction of e; each sufficiently small level has an open surface patch in int(K), hence D_t has positive (n-1)-dimensional measure.

### 4.2. Origin-polar coordinates limit density growth

Independently, write K along rays from 0 as 0 <= r <= rho(theta). Every direction with rho(theta)>0 has alpha(theta):=a dot theta >= 0. Let R_t(theta)>0 solve

    alpha(theta) R_t + b R_t^2 = t.

Polar integration gives a second density formula,

    w(t) = integral_{R_t(theta)<rho(theta)}
               R_t(theta)^(n-1) / [alpha(theta)+2b R_t(theta)] dtheta. (4.9)

The distinction between strict/non-strict boundary inclusion affects only an irrelevant density version. For 0 < s <= t, the active directions at t are a subset of those at s. Also

    R_s/R_t >= s/t,
    [alpha+2b R_t]/[alpha+2b R_s] >= 1.

For n >= 1, each active integrand therefore satisfies

    integrand(s) >= (s/t)^(n-1) integrand(t).

Integration proves

    w(t) <= (t/s)^(n-1) w(s).                                        (4.10)

Together, (4.8) and (4.10) are genuine pointwise local control of the density. They are substantially stronger than an endpoint cumulative-volume estimate.

### 4.3. Full interval-centered doubling

Take I=[c-d,c+d] with 2I=[c-2d,c+2d] contained in [0,beta], so c>=2d. If t in 2I and s in I, then either t<=s and (4.8) gives w(t)<=c0^(-1)w(s), or t>=s and t/s<=4, so (4.10) gives w(t)<=4^(n-1)w(s). Hence

    integral_(2I) w <= 2 max(c0^(-1),4^(n-1)) integral_I w.             (4.11)

This proves exactly the local interval doubling hypothesis in the imported theorem, including intervals whose doubles approach the endpoint 0.

### 4.4. Zero gradient

If a=0, h=b||x||^2. Polar integration gives

    w(t) = [1/(2 b^(n/2))] t^(n/2-1) S(t),
    S(t) = surface_measure{theta : rho(theta)>sqrt(t/b)}.              (4.12)

A fixed interior ball, joined convexly to 0, supplies a truncated cone of positive solid angle. Therefore for some beta>0,

    0 < c <= S(t) <= surface_measure(S^(n-1)),   0<t<=beta.

Thus w(t) is comparable to t^alpha, alpha=n/2-1 > -1. Such power weights are interval doubling on [0,beta]. This includes n=1, where alpha=-1/2; no false monotonicity claim about w is needed in this case. This completes the geometric lemma.

## 5. Endpoint zero bound with the indexing exposed

Here is a short derivation of the needed endpoint conclusion from the inspected Christoffel upper bound. It avoids relying on adjacent-zero spacing to control an endpoint gap.

For either density class just established there is D<infinity such that, for small z>0 and 0<delta<=z/2,

    nu([z-delta,z+delta]) <= D (delta/z) nu([0,z]).                     (5.1)

For a!=0, compare almost every t in [z-delta,z+delta] with almost every s in [z/2,z]. If t<=s use (4.8); if t>=s then t/s<=3 and use (4.10). Integrating both variables gives (5.1) with D=4 max(c0^(-1),3^(n-1)). This avoids selecting a density value at any exceptional individual level. For a=0 the same statement follows by integrating the two-sided bounds c t^alpha <= w(t) <= C t^alpha. This uses a full shell estimate, not an unjustified inference from anchored doubling.

Let P_N be the degree-N orthogonal polynomial for nu, with smallest zero z_N. For completeness, the required standard spectral and quadrature facts have elementary checks:

1. Orthogonality's sign-change argument puts all N zeros simply inside the convex hull of the support. The compressed multiplication operator on polynomials of degree <=N-1 is symmetric and has characteristic polynomial proportional to P_N (the three-term recurrence proves this).
2. With Lagrange cardinal polynomials ell_i at those zeros, polynomial division by P_N proves Gaussian quadrature exact through degree 2N-1. Its weights omega_i are positive because omega_i=integral ell_i^2 dnu.
3. For any p of degree <=N-1 with p(z_N)=1, quadrature gives integral p^2 dnu>=omega_1. Equality is attained by ell_1. Therefore lambda_(N-1)(z_N,nu)=omega_1. On [0,z_N], every factor in ell_1(t)=product_(j>=2)(t-z_j)/(z_N-z_j) is at least 1, so

       nu([0,z_N]) <= integral ell_1^2 dnu
                    = lambda_(N-1)(z_N,nu).                          (5.2)

No off-by-one is being hidden here: the degree-N zero is coupled to lambda of degree N-1. The PDF's alternative convention using lambda_N at a zero gives the same value because the additional orthogonal polynomial vanishes there.

Also z_N tends to 0. The Rayleigh characterization of compressed multiplication gives

    z_N = min_{deg p<=N-1, p!=0} integral t p^2 dnu / integral p^2 dnu. (5.3)

After scaling the support to [0,1], testing p(t)=(1-t)^(N-1) proves convergence to the global left endpoint: for any epsilon>0, the part above epsilon is exponentially small compared to the positive mass below epsilon/2. This convergence argument asserts no rate and is used only to enter the local interval [0,gamma].

For sufficiently large N put k=N-1 and delta=delta_k(z_N). By the imported Christoffel bound,

    nu([0,z_N]) <= lambda_k(z_N)
                 <= C nu([z_N-delta,z_N+delta]).                      (5.4)

If delta>z_N/2 then z_N<2delta. Otherwise (5.1), (5.4), and positivity give z_N<=CD delta. In either case, for a fixed B,

    z_N <= B [sqrt(z_N)/k+1/k^2].                                    (5.5)

Writing y=k sqrt(z_N), this is y^2<=B(y+1), which bounds y independently of k. Consequently

    z_N <= C'/N^2                                                    (5.6)

for all large N, and for all N>=1 after enlarging C'. This is a checkable endpoint argument with a verified geometric hypothesis, not a restatement of an unsupported spacing conjecture.

## 6. Return to global SOS densities and every integer r

Let m=floor(r/2). Choose a real polynomial p_m of degree <=m attaining the Rayleigh minimum for multiplication by t under nu. The finite-dimensional symmetric eigenvalue problem ensures it exists. Define

    q_r(x) = p_m(h(x))^2 / integral_K p_m(h(x))^2 dmu(x).              (6.1)

The denominator is positive because nu has interval support and p_m is nonzero. This is one square times a positive constant, hence a **global SOS on all of R^n**, regardless of the sign of h away from K. Its degree is at most 4m<=2r, and its integral against normalized Lebesgue measure is exactly 1. Equations (3.2), (5.3), and (5.6) yield

    H_r(f)-min_K f <= integral_K h q_r dmu
                   = z_(m+1) <= C'/(m+1)^2 <= 4C'/r^2.              (6.2)

The last inequality uses m+1>=r/2. Enlarge the constant to cover the finitely many small degrees where the local endpoint estimate was not yet applied. In particular r=1 permits the constant density. The lower bound 0 follows from f>=min_K f and q>=0 on K.

Using dx rather than dx/vol(K) leaves H_r unchanged: divide a normalized-measure density by vol(K) to obtain its dx-normalized counterpart. Thus no volume factor is missing.

The construction is an existence argument using a minimizer and moment data. It does not give an efficient method to locate the minimizer or to integrate over an arbitrary convex body.

## 7. Adversarial checks and boundaries of the conclusion

- **Arbitrary boundary geometry:** central projection uses only one interior point and convex segments. Smoothness, tangent balls, semialgebraicity, a simplicial cone, and a unique supporting plane are not assumptions. A nonsimple cone is covered without triangulating it.
- **Stationary boundary minimizer:** a=0 is treated separately; the power weight can decrease when n=1, and Section 4.4 accounts for this.
- **Nonunique original minimizer:** b>0 isolates the chosen point for h, while preserving f<=h. A flat minimum face therefore causes no problem.
- **Small nonzero gradient:** the admissible beta can shrink as ||a|| shrinks. The conclusion permits a constant depending on the fixed objective, so no uniform-in-a assertion is needed.
- **Global support and endpoint:** h>=0 on all K and has unique zero 0. The global endpoint requirement is checked; a merely local support endpoint would not suffice for the same first-zero argument.
- **No substitution of f#mu:** the carefully chosen quadratic h is essential to the measure proof. The conclusion does not claim the same zero estimate for every original-objective push-forward or for arbitrary reference measures.
- **Full hierarchy fidelity:** only a feasible subfamily of global squares is used to upper bound the full hierarchy. This is legitimate; no equality between the full hierarchy and a restricted s(f) hierarchy is asserted.
- **No circular endpoint import:** the exact Christoffel theorem is imported; its full doubling hypothesis is proved. The endpoint zero bound is then derived from shell control and Gaussian quadrature.
- **Universal O versus Theta:** constant f has zero error at every degree, so a per-objective Theta(r^-2) claim is false. The universal upper rate can still be worst-case sharp: on an interval with Lebesgue measure and a nonconstant linear objective, the exact hierarchy is the smallest shifted-Legendre zero, which has two-sided order r^-2 (also covered by the inspected global-endpoint result). No lower bound is claimed for every objective.

An explicit cautionary example shows why one-end cumulative growth could not replace Section 4.3. On [0,1] take Lebesgue measure plus spikes supported on [a_j,a_j+epsilon_j], with a_j=2^-j, epsilon_j=2^(-j^2), and spike mass a_j, for j>=3. Its cumulative F(t) satisfies t<=F(t)<=3t, hence F(2t)<=6F(t). But I_j=[a_j-epsilon_j,a_j] has nu(I_j)=epsilon_j, while nu(2I_j)>=a_j/2, so the interval-doubling ratios diverge. This measure is not claimed to arise from the quadratic convex-body geometry; it falsifies the tempting general inference.

## 8. Checkable computation, status, and exact remaining work

`validate_spectral.py` and `numerical_results.json` provide reproducible floating-point stress checks, **not** rigorous interval numerics and **not** the proof. The analytic proof above is the validation artifact for the universal claim.

The script computes compressed multiplication spectra for K_phi={(x,y): |x|<=1, phi(|x|)<=y<=1}, h=y+x^2+y^2. Cases include a flat face, phi(x)=x, x^1.25, x^2, x^4, x^16, and the nonsemialgebraic convex phi(x)=x/log(e/x). The coarea density is integrated explicitly in x using the endpoint root of phi(x)+x^2+phi(x)^2=t. Numerical quadrature is repeated at two resolutions. Moment checks use an independent direct integration over K_phi rather than the push-forward formula. Full reorthogonalization avoids ill-conditioned monomial moment matrices.

For m=64, the observed m^2 times the first zero ranges from 6.803 to 9.898 across these cases. Maximum change when doubling quadrature resolution is below 6e-10; the maximum independent moment relative error at the finer resolution is below 3e-13. Five hundred central-projection nesting checks on a square pyramid with a nonsimple apex all retain positive membership slack; maximum level residual is below 9e-19. Exact Jacobi recurrence checks also cover zero-gradient radial measures in dimensions 1, 2, 3, and 7, including the decreasing t^(-1/2) density in dimension 1. All numerical sanity assertions pass. These data are consistent with the analytic route and do not establish asymptotics by themselves.

**Strongest verified statement:** the exact target upper bound follows from Sections 3–6 and the inspected primary Christoffel theorem. No mathematical gap in those deductions is identified by this family's internal adversarial check. **Remaining work before promotion:** independent adversarial verification by another family, review of proof presentation, and separate literature/priority clearance. Those are review tasks, not a newly asserted equivalent mathematical conjecture. The parent workflow is responsible for cross-family checks; this isolated family made no contact with other agents.

Mechanism status: successful, subject to the explicitly named standard import. Completion estimate for this family's assigned mathematical mechanism review: 100%. Completion estimate for a publication-ready, priority-cleared theorem: not assessed.
