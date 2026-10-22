# Independent adversarial review of the spectral route

Review date: 2026-10-17 UTC. Assigned effort: PR1261 / problem30003990. Reviewer scope: the frozen spectral-family inputs and the actual cited Totik–Varga primary PDF. This is a mathematical validity review, not a novelty or priority opinion.

## Verdict and exact claim

**PASS, relative to the named, inspected standard import: the upper half of Totik–Varga (2012), Theorem 3.1.** I find no unsupported central transfer and no remaining mathematical gap in this spectral route to the assigned upper bound. The conclusion is conditional in the ordinary sense of using that standard theorem; this review does not independently reconstruct all approximation theory behind it.

The verified claim is the following. Fix a compact convex body K in R^n, n >= 1, with nonempty interior, normalized Lebesgue measure mu on K, and a real polynomial f. For every integer r >= 1, there is a real polynomial v_r with degree at most r such that q_r=v_r^2 has integral 1 and

    0 <= integral_K f q_r dmu - min_K f <= C(K,f)/r^2.

Consequently the same upper bound holds for the infimum over all global SOS densities of degree at most 2r. The construction is one global square, with its positive normalizing constant absorbed into v_r. No statement for arbitrary measures, arbitrary original-objective push-forwards, a restricted s(f) hierarchy, a per-objective two-sided rate, or an efficient minimizer algorithm is established here.

The input anchor SHA256 is cfc71287c393cc15ca591f1488b7d8761f9217e327212a3d5c345ba471019db1. All ten listed files were authenticated at the start and again before sealing. The input report's conclusion, internal self-audit, and floating-point examples were not used as premises. The critical bridges are rederived below.

## 1. Primary import checked against the actual body

I independently downloaded [Totik and Varga, Non-symmetric fast decreasing polynomials and applications](https://www.math.u-szeged.hu/pot/5fdp.pdf). The downloaded body has 285373 bytes and SHA256 004361b85bbaef05716c7789a108b9b764e3e7789ba22724a029e9ee5429a7a9, matching the frozen source inventory. Printed pages 382–386 (PDF pages 5–9) were read in full as extraction and visually inspected. This includes the definition preceding (3.1), Theorem 3.1, and its complete proof. Theorem 4.1's statement was inspected incidentally; its zero-spacing result is not imported.

The imported consequence is:

    lambda_k(z,nu) <= C nu([z-delta_k(z),z+delta_k(z)]),
    lambda_k(z,nu) = inf_{deg p <= k, p(z)=1} integral p^2 dnu,
    delta_k(z) = sqrt(z)/k + 1/k^2.

It applies to a finite positive compactly supported measure, at a left support endpoint 0, when the measure is doubling on [0,beta]; the constant is uniform for z in [0,gamma], gamma<beta, and positive integer k. The paper's endpoint definition allows a local left endpoint. The measure here satisfies the stronger global condition. Its definition (3.1) concerns every interval I whose centered double 2I is contained in [0,beta]. Anchored cumulative doubling alone does not supply this hypothesis. The Christoffel index allows degree <= k, rather than degree < k. Thus the later application at a degree-N zero uses k=N-1.

The body also explicitly controls support outside the local interval in the upper-estimate proof. The application therefore does not require support to be only [0,beta], or global doubling across the entire support. Detailed body-inspection metadata are in PRIMARY_BODY_INSPECTION.json. No appeal to a zero-spacing theorem is needed to bridge an unproved endpoint gap.

## 2. Quadratic reduction and measure support

Translate a chosen minimizer of f to 0 and subtract its value. Let a=gradient f(0). For any x in K, the function s -> f(sx) has a right minimum at s=0 on [0,1]. Therefore a dot x >= 0. Taylor's integral formula on the segment [0,x], and a bound on the Hessian over compact K, give b>0 such that

    0 <= f(x) <= h(x)=a dot x+b||x||^2   (x in K).

One can take b at least 1 and at least half the maximum Hessian operator norm. This uses neither smoothness of the boundary nor uniqueness of the original minimizer. The function h has exactly one zero on K, at 0, and h>=b||x||^2 there.

Let nu=h#mu and H=max_K h. Since K has full dimension, H>0. The support is [0,H], not just a subset with a left accumulation point. Indeed continuous h maps connected K onto [0,H]. For any x in K and any ambient neighborhood of x, a small mixture of x with an interior ball gives a positive-volume subset of K in that neighborhood. The inverse image of a neighborhood of h(x) therefore has positive volume. Every image value belongs to the support of the push-forward. In particular 0 is the genuine global left endpoint and every interval (0,epsilon) has positive mass.

There are no atoms. Every level set of the nonconstant polynomial h has n-dimensional Lebesgue measure zero. This also prevents a mass at 0 from contaminating either the density analysis or the Gaussian endpoint inequality. Compact support gives all moments, and interval support makes the moment inner product positive definite on every finite polynomial space.

## 3. Nonzero a: central projection without a hidden geometric hypothesis

Assume a != 0. Choose e in int(K), put A=a dot e, and E=a-perp. The supporting inequality and full-dimensional interior imply A>0. With dz the Euclidean (n-1)-dimensional measure on E, set

    X(u,z)=(1-u)z+ue,       z in E, u<1.

The inverse is

    u=(a dot x)/A,   z=(x-ue)/(1-u).

Choose an orthonormal basis on E and append its normal a/||a||. The z columns of DX are (1-u) times that basis, and the normal component of the u column e-z is A/||a||. Thus the absolute volume Jacobian is

    (A/||a||)(1-u)^(n-1).

This formula also applies to n=1, with E a single point carrying zero-dimensional measure 1. No positive-dimensional cross-section is silently required in that case.

Put G(u,z)=h(X(u,z)). Then

    G(u,z)=Au+b||(1-u)z+ue||^2,
    G_u=A+2b X(u,z) dot (e-z).

For any x in K with h(x)<=beta, the supporting inequality and quadratic term imply

    0<=u<=beta/A,
    ||x||<=sqrt(beta/b),
    ||z||<=R_beta:=(sqrt(beta/b)+(beta/A)||e||)/(1-beta/A).

The rectangular coordinate region 0<=u<=beta/A, ||z||<=R_beta shrinks to (0,0) as beta decreases. Since G_u(0,0)=A, choose beta>0 so small that beta/A<=1/4 and

    A/2 <= G_u(u,z) <= 3A/2

on this entire region. This is an independent preliminary bound, not an inference that assumes the desired root already lies in a smaller ball.

For any 0<t<=beta and z with b||z||^2<=t, G(0,z)<=t and G(beta/A,z)>=beta>=t. The derivative bound gives existence and uniqueness of a root u(t,z) in [0,beta/A]. Every point in K with h=t is represented: the preliminary R_beta estimate includes its coordinates, and monotonicity from 0 to its u shows b||z||^2<=t. Thus there is no omitted part of a small level set.

Define

    D_t={z in E: b||z||^2<=t, X(u(t,z),z) in K}.

The root is a continuous, locally smooth implicit function because G_u>0, and K is closed, so these are measurable domains. For z in D_s and s<=t, u_t>=u_s and u_t<1. More explicitly,

    X(u_t,z)=((1-u_t)/(1-u_s)) X(u_s,z)
             +((u_t-u_s)/(1-u_s))e.

The displayed coefficients are nonnegative and sum to 1. Convexity proves D_s subset D_t. This is the decisive geometric fact: changing the level while holding z fixed moves along an actual segment to the same interior point e.

Changing variables first by X and then by t=G(u,z) gives a density version

    w_c(t)=integral_{D_t} J(t,z) dz,
    J(t,z)=(A/||a||)(1-u(t,z))^(n-1)/G_u(u(t,z),z).

The formula includes the full change-of-variable factor. The bounds are

    j_min=(2/(3||a||))(3/4)^(n-1) <= J <= 2/||a||=j_max.

Hence for 0<s<=t<=beta,

    w_c(t)>=c0 w_c(s),    c0=j_min/j_max=(1/3)(3/4)^(n-1)>0.

Positivity of the cross-section is also provable, not an assumption. For 0<tau<1, tau e is interior: if B(e,epsilon) is contained in K then B(tau e,tau epsilon) is contained in K by convexity with 0. The strictly increasing function tau -> h(tau e) takes all sufficiently small positive values. At the corresponding interior point on a level t, the positive u derivative supplies an open E-patch of level points in K. Its projection has positive dz measure. For n=1, this means D_t contains its single point and its zero-dimensional measure is 1.

## 4. Independent polar formula and the direction of the inequality

For a direction theta, let rho(theta)=sup{r>=0:r theta in K}. Convexity and 0 in K make its radial fiber [0,rho(theta)]. This is a measurable radial function, since its superlevel sets are closed. Directions with rho>0 have alpha(theta)=a dot theta>=0; other directions contribute zero volume. For such an active direction, define the positive solution R_t of

    alpha R_t+bR_t^2=t.

Polar integration, followed by a one-variable change of variable on each ray, gives a density version

    w_p(t)=integral_{R_t<rho(theta)}
              R_t^(n-1)/(alpha+2bR_t) dtheta.

For s<=t, the active angular set at t is a subset of the set at s. On a direction active at t,

    s/t=(R_s/R_t)(alpha+bR_s)/(alpha+bR_t)<=R_s/R_t,
    (alpha+2bR_t)/(alpha+2bR_s)>=1.

Consequently the ratio of the s integrand to the t integrand is at least (s/t)^(n-1), and

    w_p(t)<=(t/s)^(n-1) w_p(s).

In dimension 1 the exponent is zero, and the angular measure on S^0 is counting measure; the same argument is valid. Negative alpha is never used on a ray of positive length in K.

The distinction between < and <= at r=rho(theta), and intersections with the boundary of K in central coordinates, can alter a density version at exceptional levels. It cannot alter the measure. Both formulas are obtained by Fubini from the original volume integral, so they agree on one common full-measure subset T of (0,beta). All subsequent comparisons can and should be made for s,t in T. This avoids any claim about a chosen exceptional level value. There are no atoms from such levels, as verified above.

Combining the two density versions on T gives both

    w(t)>=c0w(s),
    w(t)<=(t/s)^(n-1)w(s),      0<s<=t<=beta, s,t in T.

Neither comparison alone would suffice for the application. Their joint use is the substantive difference from an anchored-only volume estimate.

## 5. Full centered doubling and shell control

Let I=[c-d,c+d] and 2I=[c-2d,c+2d] subset [0,beta], with d>0. Thus c>=2d. For almost every t in 2I and s in I:

- If t<=s, the first comparison gives w(t)<=c0^(-1)w(s).
- If t>=s, then t/s<=4, and the second gives w(t)<=4^(n-1)w(s).

With M=max(c0^(-1),4^(n-1)), integration over both variables yields

    nu(2I)<=2M nu(I).

All endpoints have measure zero, so this verifies precisely the paper's (3.1), including doubles that touch 0. It is stronger than F(2t)<=C F(t) for F(t)=nu([0,t]).

A further estimate needed for the endpoint-zero bridge follows without sampling any single density value. For 0<z<=beta/2 and 0<delta<=z/2, compare almost every t in [z-delta,z+delta] with almost every s in [z/2,z]. Both are in the local range. Either the first comparison applies, or t/s<=3. Hence with M_3=max(c0^(-1),3^(n-1)),

    (z/2) nu([z-delta,z+delta])
       <=2delta M_3 nu([z/2,z])
       <=2delta M_3 nu([0,z]).

Equivalently,

    nu([z-delta,z+delta]) <= D(delta/z)nu([0,z]),  D=4M_3.       (*)

This shell estimate is not deduced from anchored doubling; it is independently supported by the pairwise density bounds.

## 6. Stationary case, including dimension 1

If a=0, central projection is unnecessary and its argument must not be applied by a limit in a. Here h=b||x||^2 and polar integration gives

    w(t)=(1/(2b^(n/2))) t^(n/2-1) S(t),
    S(t)=surface_measure{theta:rho(theta)>sqrt(t/b)}.

An interior ball B(e,epsilon) and its convex hull with 0 give a truncated cone of positive solid angle. Choose the cone slightly inside the ball's angular shadow. Its radial length is then bounded below uniformly by a positive constant. Thus for some beta>0 and constants 0<c<=C,

    c t^alpha <= w(t) <= C t^alpha,    alpha=n/2-1>-1,
    0<t<=beta.

This is valid even when 0 is on the boundary. If 0 is interior, a small full ball gives it immediately. In n=1, a cone means one or both points of S^0, and alpha=-1/2. The density is permitted to decrease.

Power weights obey centered doubling even when alpha is negative; a pairwise bound down to t=0 would be false in that case. To verify the integral statement, write I=[c-d,c+d], with 0<d/c=eta<=1/2. After scaling t by c, the ratio of power-weight masses is

    R_alpha(eta)=integral_{1-2eta}^{1+2eta} u^alpha du
                  / integral_{1-eta}^{1+eta} u^alpha du.

This ratio is continuous on (0,1/2], finite at eta=1/2 since alpha>-1, and tends to 2 as eta tends to 0. It is therefore uniformly bounded. The two-sided density comparison transfers this centered-doubling bound to w. This integral argument includes doubles that touch 0 and the singular exponent alpha=-1/2.

The shell estimate (*) also holds. On [z/2,3z/2], w(t)<=C C_alpha z^alpha, where C_alpha=max(2^(-alpha),(3/2)^alpha), and

    nu([0,z])>=c z^(alpha+1)/(alpha+1).

Thus (*) follows with D=2(C/c)C_alpha(alpha+1). Both full interval doubling and the shell comparison have now been checked separately for the stationary case.

## 7. Orthogonal zeros, Gaussian weights, and the exact degree

Let P_N be the monic degree-N orthogonal polynomial for nu, and let z_1<...<z_N be its zeros. These are distinct and lie in (0,H). A direct sign-change proof is available: if fewer than N distinct sign-changing roots lay in the support interval, multiplication by the product of those factors would give a polynomial of fixed nonzero sign on the interval with degree of the multiplier <N, contradicting orthogonality and positive interval mass. This forces all N roots to be simple and internal.

Write z_N^*=z_1 for the smallest zero; the superscript avoids confusing the size N with the last ordered root. Let ell_i be the cardinal polynomial of degree N-1 at these roots. Polynomial division by P_N proves Gaussian quadrature for every polynomial of degree <=2N-1:

    integral g dnu = sum_i omega_i g(z_i),
    omega_i=integral ell_i dnu=integral ell_i^2 dnu>0.

Indeed the quotient has degree <=N-1 and integrates to zero after multiplication by P_N; the remainder is interpolated by the ell_i. Applying the formula to ell_i^2 gives the second equality and positivity.

For every p of degree <=N-1 with p(z_1)=1, exact quadrature of p^2 gives integral p^2 dnu>=omega_1. Equality is attained by ell_1. Hence, in the exact convention of the inspected paper,

    lambda_(N-1)(z_N^*,nu)=omega_1.

For t in [0,z_1], every factor (t-z_j)/(z_1-z_j), j>=2, is at least 1. The empty product when N=1 is 1. Therefore ell_1(t)>=1 and

    F(z_N^*)=nu([0,z_N^*])<=integral ell_1^2 dnu
             =lambda_(N-1)(z_N^*,nu).                         (**)

There is no missing endpoint term, incorrect direction, or use of degree N in place of degree N-1.

The compressed multiplication operator M_N on polynomials of degree <=N-1 has these same eigenvalues. In fact (t-z_i)ell_i is a multiple of P_N, hence orthogonal to that space. Projection gives M_N ell_i=z_i ell_i. The cardinal polynomials form a basis, so all eigenvalues have been accounted for. The finite-dimensional spectral theorem gives

    z_N^*=min_{0!=p, deg p<=N-1} integral t p^2 dnu/integral p^2 dnu.

This also explicitly exhibits a real eigenvector polynomial attaining the minimum.

## 8. Entering the local regime without assuming a rate

The smallest zero tends to 0 by a separate argument. Scale t by H for this argument only, obtaining support [0,1], and test the Rayleigh quotient with p(t)=(1-t)^(N-1). For 0<epsilon<1, the denominator is at least

    nu([0,epsilon/2]) (1-epsilon/2)^(2N-2)>0.

The part of the numerator on [0,epsilon] is at most epsilon times the full denominator. The part above epsilon is at most nu([0,1])(1-epsilon)^(2N-2). Thus the quotient is at most epsilon plus a constant times

    ((1-epsilon)/(1-epsilon/2))^(2N-2),

which tends to zero. This proves z_N^*->0 after returning to the original scale. No rate or doubling statement was used, so there is no circularity in entering the range of the imported theorem.

Fix gamma=beta/2. For all sufficiently large N, z=z_N^* lies in (0,gamma] and k=N-1>=1. The inspected uniform Christoffel upper estimate and (**) give

    F(z)<=lambda_k(z,nu)<=C nu([z-delta,z+delta]),
    delta=sqrt(z)/k+1/k^2.

If delta>z/2 then z<2delta. Otherwise (*) applies and F(z)>0 permits cancellation, giving z<=CD delta. Both cases imply, for a fixed B,

    z<=B(sqrt(z)/k+1/k^2).

Put y=k sqrt(z). Then y^2<=B(y+1), so

    0<=y<=(B+sqrt(B^2+4B))/2.

Therefore z<=C_0/k^2<=4C_0/N^2 for N>=2. Enlarge the constant to include the finitely many orders before the local regime and N=1; compact support bounds each such zero by H. This establishes z_N^*=O(N^-2) for all positive integer N.

## 9. Return to exactly the assigned SOS category

For r>=1 put m=floor(r/2) and N=m+1. Let p_m be a real Rayleigh eigenvector of degree <=m. Define

    q_r(x)=p_m(h(x))^2/integral_K p_m(h(x))^2 dmu.

Interval support makes the denominator strictly positive. Its square root can be absorbed into the polynomial, so this is one global square on all of R^n. Its degree is at most 4m<=2r, its integral is 1, and

    integral_K f q_r dmu <= integral_K h q_r dmu
       =z_(m+1)^*<=C_1/(m+1)^2<=4C_1/r^2.

The original minimum was subtracted at the start. Restoring it gives the claimed error bound. For r=1, m=0 gives the constant density, already included by enlarging the same finite constant. The nonnegative lower bound uses q_r>=0 and f>=min f. Normalized versus unnormalized volume only rescales the density normalization and does not change the optimization value.

The argument provides a feasible subfamily for the full hierarchy. It needs no equality between that hierarchy and any push-forward-restricted hierarchy. Existence of a minimizer and moments is sufficient; computational efficiency and an algorithm for finding the minimizer are outside the claim.

## 10. Adversarial controls and residual issues

The route was tested against materially different failure modes analytically:

| Potential failure | Independent resolution | Status |
|---|---|---|
| Root graph misses small levels | Preliminary R_beta rectangle, followed by monotonicity and intermediate value theorem | Verified |
| Projection expands out of K | Explicit convex coefficients on the segment from the old level point to e | Verified |
| Vanishing cross-section | Interior ball scaled toward 0 supplies an open level patch; zero-dimensional convention handles n=1 | Verified |
| Missing curvature/Jacobian term | Determinant of X followed by division by G_u | Verified |
| Angular domain grows in the wrong direction | R_t increases, so the active set shrinks; ratio is calculated explicitly | Verified |
| Boundary or exceptional-level values | Common full-measure density set and integration over pairs; nonatomic push-forward | Verified |
| Only endpoint cumulative doubling | Both density comparisons prove centered doubling directly | Verified |
| Stationary one-dimensional density | Separate t^(-1/2) power case | Verified |
| Endpoint or degree mismatch in source | Actual (3.1) and Theorem 3.1 checked; k=N-1>=1 in the eventual regime | Verified |
| A first-zero rate smuggled in through spacing | Gaussian cardinal inequality plus shell control; no spacing theorem imported | Verified |
| Convergence argument secretly assumes the desired rate | Fixed-epsilon exponential trial proves convergence only, independently | Verified |
| Global positivity or all-small-orders failure | A normalized square and explicit finite-order constant enlargement | Verified |

Two exact controls help expose direction and indexing errors, without substituting finite experiments for the proof. On K=[0,1], h=x+x^2 has normalized density w(t)=1/sqrt(1+4t) on [0,2]; in n=1 the polar upper comparison indeed says w(t)<=w(s) for s<=t, while the central comparison supplies the bounded reverse loss locally. On K=[-1,1], h=x^2 has w(t)=1/(2sqrt(t)) on [0,1]. Its degree-2 monic orthogonal polynomial is t^2-(6/7)t+3/35, with roots (15+-2sqrt(30))/35. Orthogonality follows exactly from moments integral t^j dnu=1/(2j+1). The two Gaussian masses are (18+-sqrt(30))/36, with the plus sign at the smaller root. These are positive and sum to 1, and the first mass exceeds sqrt(z_1)=F(z_1), consistent with (**). The control includes a decreasing density and the precise N=2 versus degree-1 Rayleigh convention.

The report's spike example is valid as a counterexample to a general inference only. With a_j=2^-j, epsilon_j=2^(-j^2), j>=3, add uniform spike mass a_j on [a_j,a_j+epsilon_j] to Lebesgue measure. Then t<=F(t)<=3t, while I_j=[a_j-epsilon_j,a_j] has mass epsilon_j and 2I_j captures at least half the spike mass a_j. Thus centered-doubling ratios diverge. This does not produce a quadratic push-forward from a convex body, and it contradicts none of the geometric arguments above.

I inspected the frozen numerical script and the result structure. Its labels correctly describe floating-point stress evidence. I did not execute that script, because its entry point writes into the frozen spectral-family folder, and no numerical result is needed for the proof. I do not certify the reported numbers or treat convergence of those finite experiments as proof. No test code was authored or run in this review; the exact controls above are direct algebraic checks.

There are presentation points worth retaining in a polished proof: state density comparisons on one common full-measure set; expose the preliminary R_beta neighborhood before deducing b||z||^2<=t; include the n=1 zero-dimensional convention; choose gamma small enough for the shell comparison; and use the exact Christoffel degree N-1. The frozen report already contains the mathematical content needed for these points. They do not constitute an unsupported lemma or a failed transfer.

**Strongest verified result:** the assigned universal O(r^-2) upper bound for each fixed full-dimensional compact convex body, fixed polynomial, normalized Lebesgue measure, every integer r>=1, using one global square of degree <=2r, follows relative to the inspected upper estimate of Totik–Varga Theorem 3.1. **Exact remaining mathematical gap in this route:** none identified. The validity of the standard import is an explicit dependency, not a newly transferred research problem. No novelty, historical open-status, or priority conclusion is made. If another route or the original candidate fails, that fact would be logically independent of this route's verification; no candidate was inspected here.

## 11. Isolation and sealing

All authored outputs are in this review root. Third-party primary bodies, extracted source text, and rendered source-page images are in ignored_local/ and inventoried separately. No candidate/submitted proof, parent derivation, other family, priority report, or external correspondence was accessed. No individual or other agent was contacted, no subdelegation occurred, and no Git/index/reference, PR, Zenodo, or GWS mutation was performed. This review creates a local sealed review only.

Completion estimate for the assigned adversarial mathematical review: 100%. Authored-output hashes are frozen in MANIFEST.json; its own digest is delivered outside that manifest. Input authentication at both boundaries is recorded separately. No authored file will be edited after sealing.
