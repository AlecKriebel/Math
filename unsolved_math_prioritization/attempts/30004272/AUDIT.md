# Audit of quantum confinement for the degenerate polynomial family

This AI-assisted, unrefereed edition records an internal AI audit of the specifically stated results below. It is not blanket acceptance of the external manuscript, external human peer review, formal proof-assistant certification, or a novelty or priority claim. Historical algebra and regression checks are corroboration only. This is a complete written proof and audit edition, not a computational reproduction package. Full proof inspection and source retrieval belong to the preceding audit on 11 October 2026. This editorial preparation authenticated the retained bytes and consulted retained first-page text for bibliographic title, author and date metadata, including visible abstract text; it performed no fresh source retrieval or new proof audit.

11 October 2026 UTC. Target: 30004272 / OWR-17290-002.

## Disposition

The following specific conclusions from Alper Ferudun's 29 September 2026 manuscript are supported by the complete arguments reconstructed here, with the corrected higher-dimensional effective-potential comparison in Section 7. Acceptance is restricted to these exact conclusions and hypotheses.

1. On the literal regular region of the entire polynomial plane, the minimal Laplace–Beltrami operator is **not essentially self-adjoint for any integer ell >= 1**, including ell = 1. The proof exhibits a nonzero adjoint boundary form at infinity. Incompleteness by itself is not used to infer this conclusion.
2. The specified complete extensions with coefficient c(z)x(x^(2ell)+rho(z)) are **essentially self-adjoint for every integer ell >= 0** under the manuscript's stated smoothness, positivity and boundedness assumptions. Both torus families in Prandi–Rizzi–Seri Examples 7.7 and 7.8 are covered for all ell and n.
3. This does **not** prove essential self-adjointness for every complete structure agreeing with the polynomial formula only near its exceptional point. No such localization theorem is established. The complete real-analytic no-tangency conjecture remains undecided by these results.
4. Ferudun's statement on PDF p. 6 that the older effective-potential criterion applies exactly for ell <= n/2 is incorrect in higher dimensions. Section 7 below supplies the correction. It does not damage the all-ell Hardy proof, the dimension-two comparison, or the negative literal-plane result.

The conclusion is a scoped mathematical audit of an unrefereed external manuscript, not external peer review, formal verification, or a priority certificate. Its author-supplied verification report is evidence of the author's assertions, not independent evidence for their correctness. No author programs were executed.

## 1 The three questions must remain distinct

The original OWR 2019/47 discussion assumes completeness of the ambient almost-Riemannian metric in Section 3.1, on printed p. 2919 / PDF p. 9. Section 3.2, printed p. 2920 / PDF p. 10, then displays

    X1 = partial_x,
    X2 = x(x^(2ell) + z^2) partial_z,     ell >= 1.

It refers to the ell = 1 case of PRS Example 7.7, asks about all ell, and then proposes the broader analytic no-tangency conjecture. PRS Example 7.7 is a model on R times a torus, not the literal whole plane. These are different global domains.

This edition treats the literal polynomial formula on all of R^2 separately from the complete-setting question recorded in OWR 2019/47. The broader real-analytic no-tangency conjecture is a distinct question and is not resolved by these results.

The OWR's simultaneous whole-plane formula and standing completeness premise are incompatible as global assumptions. It is therefore essential to describe two separate conclusions: a negative answer to the literal entire-plane formulation, and an affirmative result for a precisely specified class of complete realizations of the local degeneracy. It would be misleading to advertise the former as a counterexample to the source-complete conjecture, or the latter as a theorem about arbitrary complete extensions.

## 2 Domain measure and sign conventions

Let f be smooth, vanish exactly at x = 0, and let the frame be (partial_x, f partial_z). On Omega = {x != 0}, put

    g = dx^2 + f^(-2) dz^2,
    dmu = dx dz / |f|,
    Delta = |f| partial_x(|f|^(-1) partial_x)
            + |f| partial_z(|f| partial_z).

Equivalently,

    Delta u = u_xx - (f_x/f) u_x + f^2 u_zz + f f_z u_z.

This expression works on either sign component. The measure is the Riemannian volume, not Lebesgue measure or an arbitrarily chosen smooth ambient measure. The minimal operator always has initial domain C_c^infinity(Omega), with no imposed boundary condition at x = 0 or at infinity. Delta is symmetric and nonpositive in L^2(Omega,mu); H = -Delta is nonnegative. Essential self-adjointness is unaffected by changing this overall sign.

For every compactly supported smooth u,

    <Hu,u> = integral (|u_x|^2 + f^2 |u_z|^2) dmu.

The distance to S = {x=0} in the ambient almost-Riemannian metric is |x|: any admissible curve has length at least its change in x, and a horizontal x-segment realizes the bound. In an incomplete whole-plane model this is not necessarily the distance to the entire metric boundary: infinity adds boundary points. The distinction is crucial.

## 3 The weighted identity and the global product criterion

This section reconstructs Ferudun Lemmas 2.1 and 2.3 and Theorem 3.2, rather than relying on the abstract or a numerical Hardy test.

For a positive C^1 weight m on an interval avoiding zero and a real C^1 function b, let a = -t m'/m. For a compactly supported complex W^{1,2} function w, expansion and integration by parts give

    integral m |w'|^2
      = integral m |w' - b w/t|^2
        + integral [b(1+a-b) - t b'] m |w|^2/t^2.

Indeed, the cross term in the square is -(mb/t)(|w|^2)', and (mb/t)' = m(-ab + tb' - b)/t^2. This proves the identity also on a negative interval. Taking b = 1 yields the lower bound with coefficient a.

Now let Omega = (R minus {0}) times N, where N is a smooth manifold without boundary with positive smooth reference density nu. Let

    g = dx^2 + h_x,
    dmu = m(x,z) dx dnu(z),
    a = -x partial_x log m >= 1.

Assume that for each fixed R > 0 there are compactly supported Lipschitz fibre cutoffs eta_k, valued in [0,1], converging pointwise to 1 and satisfying

    epsilon_k(R) = sup_{0<|x|<=2R,z in N} |gradient eta_k|_g^2 --> 0.

A compact fibre satisfies this with eta_k = 1. Fubini and the identity above imply, for every compactly supported Lipschitz v,

    integral |gradient v|^2 dmu >= integral |v|^2/x^2 dmu.       (H)

There is no prior integrability assertion for a maximal-domain function divided by x.

Suppose psi is in L^2 and solves Delta psi = lambda psi, lambda > 0, distributionally. Local elliptic regularity makes psi smooth on Omega. Testing against h^2 psi, for real compactly supported Lipschitz h, gives

    integral |gradient(h psi)|^2 + lambda integral h^2 |psi|^2
       = integral |gradient h|^2 |psi|^2.                     (E)

All integrals here use dmu. The test is justified by ordinary local Sobolev approximation on its compact support.

Fix 0 < r1 < r0 < 1 <= R. Set G(r) equal to 0 up to r1/2, to (2r-r1)/r0 on [r1/2,r1], to r/r0 on [r1,r0], and to 1 thereafter. Let xi_R(x)=xi(x/R), where xi is a smooth compact cutoff equal to 1 on [-1,1], zero outside [-2,2], and between 0 and 1. Use

    h_k(x,z) = G(|x|) xi_R(x) eta_k(z).

These are genuinely compactly supported away from x=0. The x and fibre gradients are orthogonal; the derivatives of G and xi_R have disjoint support. In (E), subtract (H) applied to h_k psi. The quantity G'^2 - G^2/r^2 vanishes on [r1,r0], is at most 4/r0^2 on [r1/2,r1], and is nonpositive elsewhere. Consequently,

    lambda integral_{r0<=|x|<=R} eta_k^2 |psi|^2
      <= (4/r0^2) integral_{r1/2<=|x|<=r1} |psi|^2
         + (||xi'||_infinity^2/R^2 + epsilon_k(R)) ||psi||^2.

First let k tend to infinity for fixed R,r0,r1, then R tend to infinity, then r1 tend to zero while r0 stays fixed. Dominated convergence controls the fibre limit and the shrinking shell; monotone convergence controls the expanding x-region. The right side vanishes. Thus psi vanishes on {|x|>=r0} for every r0>0 and hence on Omega.

For completeness, the semibounded deficiency criterion used here has a short functional-analytic justification. For a densely defined nonnegative symmetric H, closure of Ran(H+lambda) is all the Hilbert space precisely when ker(H*+lambda)=0. The lower bound ||(H+lambda)u|| >= lambda||u|| makes the range of the closed operator closed. If that range is onto, the inverse is bounded, everywhere defined and symmetric, hence self-adjoint; it follows that the closed H is self-adjoint. Conversely a nonnegative self-adjoint operator has no kernel at -lambda. This proves the criterion needed above. The same cutoff proof on either half-product proves the separate component statements.

**Audit result:** the signs, critical constant 1, support conditions, order of limits, and infinity control in this proof are correct.

## 4 Verification of the complete families

Take N = R or R/LZ, ell a nonnegative integer, and smooth c,rho on N with

    c > 0,    rho >= 0,    sup c < infinity,    sup(c rho) < infinity.

Set f = c(z)x(x^(2ell)+rho(z)). Then

    a = x partial_x log|f|
      = 1 + 2ell x^(2ell)/(x^(2ell)+rho) >= 1.

For ell = 0 the numerator is zero and a = 1. There are no other zeros of f. For ell >= 1, the (2ell+1)st x-derivative of f at x=0 is (2ell+1)! c(z), so iterated brackets with partial_x generate partial_z. For ell=0, f_x(0,z)=c(z)(1+rho(z))>0. Thus the frame is bracket-generating throughout the ambient manifold, and S is transverse to X1.

For |x| <= R,

    |f(x,z)| <= R^(2ell+1) sup c + R sup(c rho) =: Lambda_R < infinity.

This proves both required controls. A finite-length controlled curve keeps x bounded and then has bounded z-speed by Lambda_R; on a circle the fibre is already compact. Since the bracket-generating metric induces the manifold topology, closed distance balls lie in compact coordinate rectangles (or in a bounded x-interval times the circle) and are compact. The ambient metric is complete. On R, eta_k(z)=eta(z/k) satisfies |gradient eta_k|^2 <= Lambda_(2R)^2 ||eta'||^2/k^2; on a circle use eta_k=1. The product criterion therefore applies.

It is not necessary that c have a positive uniform lower bound. Positivity at each point, smoothness, and the stated upper bounds suffice. An unbounded rho is allowed when c rho stays bounded. This includes c=(1+z^2)^(-1), rho=z^2. It also includes c=1 and bounded rho equal to z^2 on [-1,1], giving agreement with the polynomial formula on an entire strip. These are specified complete realizations, not a localization theorem.

For PRS Example 7.7, write k=n-1, F=t(t^(2ell)+f_0(q)), with smooth f_0>=0 on T^k. The frame is partial_t and F partial_qi. Its determinant is F^k, so the density is |F|^(-k) and

    a = k[1 + 2ell t^(2ell)/(t^(2ell)+f_0)] >= k >= 1.

The fibre is compact and t has unit speed. Hence the ambient metric is complete and the product theorem applies for every n>=2 and ell>=1.

In Example 7.8, the additional fields are partial_yi+t partial_qi. Relative to (q,y), the frame matrix has diagonal blocks F I_k and I_k. Its determinant is still F^k. The metric still splits as dt^2+h_t because partial_t is a unit vector orthogonal to all fibre fields. The same density, a, and compact-fibre argument work. The replacement k by 2k stated in PRS's discussion of Example 7.8 does not match its displayed frame. Ferudun's footnote correctly identifies this discrepancy; the all-ell result is independent of the erroneous factor.

## 5 The literal plane and a genuine adjoint obstruction

Fix ell>=1 and work in the positive half-plane. Write F=x(x^(2ell)+z^2)>0. The curve z -> (1,z), z>=0, has finite total length integral_0^infinity dz/(1+z^2)=pi/2, so the ambient plane is incomplete. The following additional operator argument is indispensable.

Choose nonzero real phi in C_c^infinity((1,2)) and real smooth chi with chi=0 for z<=1 and chi=1 for z>=2. Define

    U = phi(x) chi(z),
    W = phi(x) chi(z)/z,

with W extended by zero where chi vanishes. Both are globally smooth in Omega after extension by zero outside the indicated x-strip, and supported away from S. For z>=2,

    Delta U = phi'' - (F_x/F) phi',
    Delta W = [phi''-(F_x/F)phi']/z
              + phi 2 x^(2ell+2)(x^(2ell)+z^2)/z^3.

On this strip F_x/F is bounded. Since dmu=F^(-1) dx dz and F^(-1)<=z^(-2), U, W, Delta U and Delta W are all in L^2. Their transition-region contributions have compact support. Formal integration by parts against C_c^infinity test functions therefore puts U and W in the adjoint domain, with the adjoint acting as Delta. No boundary condition may be imposed on these functions merely because they are in the maximal domain.

The divergence identity is

    F^(-1) Delta u = partial_x(F^(-1)u_x) + partial_z(F u_z).

Integrate W Delta U - U Delta W over z<Z. The x-boundary terms vanish because phi is compactly supported, and the lower z terms vanish because chi=0. At Z>=2 the remaining term is

    integral_1^2 F(x,Z)[W U_z-U W_z](x,Z) dx
      = integral_1^2 phi(x)^2 F(x,Z)/Z^2 dx
      --> integral_1^2 x phi(x)^2 dx > 0.

The volume integrand is absolutely integrable by Cauchy–Schwarz, so this passage to the full inner products is valid. Thus the adjoint of the minimal Delta is not symmetric. If the minimal Delta were essentially self-adjoint, its adjoint would equal its self-adjoint closure and would be symmetric. This contradiction proves failure of essential self-adjointness.

This also gives a true deficiency statement, not just a geometric heuristic. Let H=-Delta and H_F be its Friedrichs extension. At least one v in {U,W} is not in D(H_F), since otherwise the nonzero boundary form would contradict symmetry of H_F. Then

    psi = v - (H_F+1)^(-1)(H*+1)v

lies in D(H*), satisfies (H*+1)psi=0, and is nonzero. This follows from H_F being a restriction of H* and from v not being in D(H_F). Thus the real negative-energy defect space is nontrivial; standard conjugation also makes the usual two complex deficiency indices equal and nonzero. No value for their dimension is needed or asserted.

As a geometric cross-check, the substitution y=1/z transforms the end z=+infinity, for x in (1,2), into the finite boundary y=0 with smooth nondegenerate metric

    g = dx^2 + dy^2/[x^2(1+x^(2ell)y^2)^2].

The two adjoint functions have respectively nonzero boundary value and nonzero normal derivative there. All of this occurs far from x=0. Extension by zero to the other x-component gives the same obstruction for the full regular region. Reflection gives the corresponding half-plane conclusion if needed.

## 6 The first-order criterion and the limit of the method

Ferudun Theorem 5.1 replaces the effective-potential inequality by

    -Delta_mu delta >= 1/delta - kappa

on a uniform smooth collar of the relevant metric boundary or singular set. All the other hypotheses of the cited theorem must remain in force. For the general Riemannian version this means the hypotheses of PRS Theorem 3.1 with V=0 and nu=0, including C^2 regularity of distance on a uniform collar. For its ARS specialization and the FPR sub-Riemannian version, completeness of the ambient structure and a compact embedded noncharacteristic hypersurface are retained. Positive uniform normal injectivity radius is the separately stated alternative in FPR, not an automatic consequence of having no tangencies on a noncompact set.

In collar coordinates t=delta, the density is m(t,q) dt dnu(q) with partial_t log m=Delta_mu delta and |gradient u|>=|partial_t u|. The b=1 identity gives, for compact collar support,

    integral |gradient u|^2 dmu
       >= integral (delta^(-2)-kappa delta^(-1)) |u|^2 dmu.

A two-function IMS partition in delta extends this to

    Q(u) >= integral_{delta<eta}(delta^(-2)-kappa delta^(-1))|u|^2
             + C ||u||^2,

for sufficiently small eta. The remaining Agmon proof only needs this inequality: away from zero use a profile G satisfying G'/G=sqrt(1/t^2-kappa/t), normalized at eta; set it to zero below epsilon and interpolate linearly up to 2epsilon. Since G(t) is asymptotic to a positive constant times t, the interpolation slope is bounded independently of epsilon. The shrinking-shell L^2 mass vanishes. The compact exhaustion at infinity is supplied by the corresponding PRS/FPR geometric setting. This is exactly the usage checked in the full relevant proofs, not an inference from their theorem statements alone.

In the sub-Riemannian case, the cited regularity and integration-by-parts input is FPR Lemmas 4.2 and 4.4, and the collar construction is FPR Proposition 3.1. The lower regularity claims rely on established local subelliptic regularity. The main product theorem above is Riemannian off S and needs only ordinary elliptic regularity.

Compact-resolvent inheritance, under the extra compactness assumptions of the cited results, also follows directly: the weak Hardy estimate bounds the L^2 mass of a bounded form-norm family in {delta<eta} by O(eta^2), and local Rellich compactness applies on the relatively compact complement. A diagonal subsequence gives compact embedding of the form domain into L^2 and hence compact resolvent. This avoids two immaterial slips in the source compactness calculations: a negative z times ||phi u||^2 must be bounded above by max(z,0)||u||^2, not by z||u||^2; and a resolvent below the lower bound is taken at z<C strictly. These do not affect the criterion or the replacement argument.

The two first-order/effective-potential criteria are not ordered. For density t^alpha, the first-order condition requires alpha<=-1; the effective potential alpha(alpha-2)/(4t^2) also works for alpha>=3. Conversely the dimension-two polynomial family has the first-order inequality for all ell even when the effective-potential bound fails.

The manuscript's Proposition 7.2 correctly demonstrates failure of this entire weak-Hardy route for another complete analytic no-tangency model. For

    f=x(sin^2(z-x)+x^4) on R times (R/pi Z),

the singular set is compact, the frame is bracket-generating (f_x(0,z)=sin^2 z and f_xxx(0,z)=6cos(2z) do not vanish together), the metric is complete by strip boundedness, and X1 is transverse. For the local model f=x(sigma(z-x)+x^4), with c1 y^2<=sigma(y)<=y^2, choose the paper's plateau-ramp cutoffs w=W(x/z)E(z/z0). Their support is compact in 0<x,z<1/2 when 0<z0<1/8.

Writing A=integral |w_x|^2/f, B=integral f|w_z|^2, D=integral |w|^2/(x^2 f), and N=integral |w|^2/f, the proof gives

    D > z0^(-4)/45,
    A <= 21 c1^(-1) z0^(-3),
    B <= 12096 z0^3,
    N <= 16 z0^2 D.

These estimates have been checked term by term. On the inner ridge |x-z|<=z^2 the plateau equals 1 and x^2 f <= (110125/16384) z^7. The integral coefficient 32768*113664/(110125*1500625) is strictly greater than 1/45. On the x-ramps the lower bounds on f yield the coefficient 182/(9c1)<21/c1. The z derivative is bounded by 12/z0; f<=32z0^3 and the support area is 21z0^2/8, giving the stated B bound. Thus (A+B)/D tends to zero while N/D does too. No positive uniform coefficient of delta^(-2)-kappa delta^(-1), even after an arbitrary L^2 remainder, can hold.

This is a failure of a sufficient method. It is not a non-essential-self-adjointness proof and supplies no counterexample to the analytic conjecture.

## 7 Required correction to the effective-potential comparison

The dimension-two expression in Ferudun equation (3) is correct. The higher-dimensional claim immediately following Corollary 4.3 is not.

For the PRS torus family set k=n-1 and u=t^(2ell)/(t^(2ell)+f_0). Since a=k(1+2ell u) and t partial_t u=2ell u(1-u), direct differentiation gives

    t^2 V_eff = (a^2+2a-2t partial_t a)/4
              = k(k+2)/4 + k ell(k+1-2ell)u
                + k(k+2)ell^2 u^2.                         (P)

This identity also covers f_0=0 by u=1. Its minimum over 0<=u<=1 is

    k(k+2)/4,                                              if ell<=n/2;
    k(k+2)/4 - k(2ell-n)^2/[4(n+1)],                       if ell>n/2.

The second minimum occurs at u=(2ell-n)/[2ell(n+1)]. In particular:

    n=3, ell=2: minimum 15/8;
    n=3, ell=3: minimum 7/8.

Both exceed 3/4 although ell>n/2. Thus the older criterion does apply in these cases with kappa=0.

For integer ell>=1, the exact range of this criterion, for the original PRS assumption that f_0 has both zero and positive values on the connected torus, is:

    n=2: ell=1;
    n>=3: 1<=ell<=n.

For n>=3 the minimum at ell=n equals (n-1)(2n+1)/[4(n+1)]>=3/4; it decreases with ell beyond n/2. At ell=n+1 it is -(n-1)(2n+3)/[4(n+1)]<0. This proves the integer cutoff. If the minimum is below 3/4, every fixed interior u-value near its minimizer can be realized along t_j->0 because the image of f_0 contains [0,a] for some a>0. The resulting negative constant times t_j^(-2) cannot be absorbed by -kappa/t_j for any fixed kappa. This establishes necessity as well as sufficiency for the stated criterion and family. Constant or strictly positive f_0 without zero is not covered by that necessity claim.

There is also an error in the particular negative-remainder path written in PRS Example 7.7(2), present in both the journal version and arXiv v3. Substituting f_0=t^(2ell) into its own displayed remainder gives

    t^2 R = ell(n-1)[ell(n-3)+2n]/4.

For n=2,ell=2 it is +1, and for every n>=3 it is positive. It therefore does not produce the asserted negative divergence. The correct ratio for testing a negative minimum is the minimizer of (P), when that minimum is actually below the threshold.

These corrections change the comparison with the reach of prior techniques, not the all-ell theorem proved through the alternative Hardy identity. They also do not change the dimension-two statement: for n=2 the minimum is 3/4-(ell-1)^2/3, so ell>=2 really does fail the effective-potential bound. No priority conclusion is inferred from the corrected comparison.

## 8 Acceptance boundaries and sources

Acceptance covers the literal-plane non-essential-self-adjointness theorem, the stated product criterion, the specified complete-family and PRS torus results, and the exact ancillary criterion and method-limit arguments reconstructed above, with the correction in Section 7. The all-ell complete-family theorem does not resolve arbitrary complete local extensions or the source's broader analytic conjecture. The literal-plane negative theorem addresses the completeness-dropped formulation. No conclusion about uninspected or unspecified manuscript claims follows.

The external 11-page manuscript was retrieved from Zenodo's public record and public PDF link, with 167534 bytes and SHA-256 2be8cb5173e4d620299d0083c967e4dbaa70eae650b9a231d10a66d402371701. Its MD5 also agrees with the record's displayed MD5. The PDF's SHA prefix agrees with the version string in the publisher's public PDF link; no byte identity to an inaccessible publisher-hosted download is asserted.

The earlier publisher HTML HTTP 403 was preserved as a denial. It was not bypassed. The publisher's web-reader PDF returned a cache-miss error; DOI and Zenodo web-reader attempts were unavailable. A normal, unauthenticated request to the independently advertised public Zenodo record returned HTTP 200, followed by its publicly linked PDF and verification report. This resolved the full-text blocker without authentication, a hidden endpoint, or author contact.

Primary sources:

- [Ferudun manuscript and record](https://zenodo.org/records/23041946), [full PDF](https://zenodo.org/records/23041946/files/OWR-17290-002-paper.pdf), DOI 10.5281/zenodo.23041946. Unrefereed, dated 29 September 2026; all 11 PDF pages read, mathematical pages 2–9 visually checked.
- [OWR 2019/47](https://ems.press/content/serial-article-files/46828), PDF pp. 8–11 / printed pp. 2918–2921, especially Section 3.1 and Problem 1. The model and completeness premise were checked against the retained original pages.
- [Prandi–Rizzi–Seri journal paper](https://ems.press/content/serial-article-files/33671), Journal of Spectral Theory 8 (2018), 1221–1280; [arXiv v3](https://arxiv.org/pdf/1609.01724v3). The cited numbering in Ferudun follows arXiv v3. The complete relevant collar, Hardy, Agmon, compactness and ARS-normal-form proofs were inspected in v3 pp. 9–21 and 31–38; the journal's Example 7.7–7.8 pages were also checked.
- [Franceschi–Prandi–Rizzi arXiv v3](https://arxiv.org/pdf/1708.09626v3), later Potential Analysis 53 (2020), 89–112. The statements and complete relevant collar, regularity, Hardy, Agmon and compactness proofs were inspected on pp. 1–3 and 7–18.

Basic functional-analytic and local regularity input is stated explicitly in this audit; it is not formalized. The background monographs cited inside PRS/FPR were not all independently retrieved. Neither the remainder of the literature bibliography nor the author's literature-search logs were independently exhausted. This audit makes no novelty claim, no claim that the general conjecture is globally known to be open today, and no claim that author-reported computational or internal-referee checks were reproduced. It establishes what the inspected proof does and does not prove.

## Appendix: complete authored correction patch

The following complete correction is retained verbatim from the accepted authored correction. It is an authored mathematical patch, not a copy of the external manuscript.

# Correction to the effective potential comparison

This is an authored correction for the comparison following Corollary 4.3 on PDF p. 6 of Ferudun's manuscript, DOI 10.5281/zenodo.23041946. It is not a modification of the author's original document.

## Replacement paragraph

For PRS Example 7.7, put k=n-1 and u=t^(2ell)/(t^(2ell)+f). The effective potential satisfies

    t^2 V_eff = k(k+2)/4 + k ell(k+1-2ell)u + k(k+2)ell^2 u^2.

When ell<=n/2, its minimum over u in [0,1] is k(k+2)/4. When ell>n/2, the minimum is

    k(k+2)/4 - k(2ell-n)^2/[4(n+1)].

For n=2 this recovers equation (3), so the effective-potential criterion applies only for ell=1 among positive integers. For n>=3 it applies for every positive integer ell<=n, a larger range than ell<=n/2. Under PRS's assumption that f has both zero and positive values on the connected torus, it fails for ell>=n+1. The Hardy argument of Corollary 4.3 establishes essential self-adjointness for all ell without this restriction.

## Verification and effect

The minimum follows by completing the square. For ell>n/2 the minimizing ratio is

    u_*=(2ell-n)/(2ell(n+1)).

For example, n=3 and ell=2 yield a minimum of 15/8; n=3 and ell=3 yield 7/8. Both are above the critical 3/4. At ell=n the minimum is (n-1)(2n+1)/(4(n+1)), which is at least 3/4 for n>=3. At ell=n+1 it is negative. Monotonicity of the displayed minimum in ell finishes the integer-range check. Ratios near u_* are realized along t->0 by continuity of f and its having both zero and positive values, proving failure of any fixed -kappa/t remainder outside the stated range.

PRS Example 7.7(2)'s particular path f=t^(2ell) does not produce its asserted negative remainder: substitution into its own equation gives

    t^2 R=ell(n-1)[ell(n-3)+2n]/4.

The expression equals 1 at n=2,ell=2 and is positive for all n>=3. A path with ratio u_* is the appropriate negative-threshold test when the minimum is below 3/4.

For the displayed frame of PRS Example 7.8 the determinant is F^(n-1), not F^(2(n-1)); Ferudun's existing footnote correctly identifies this separate issue.

No change is required to the all-ell product criterion, the complete-extension theorem, or the literal-plane boundary-form proof. The comparison correction does not establish novelty or priority.

Sources: [Ferudun PDF](https://zenodo.org/records/23041946/files/OWR-17290-002-paper.pdf); [PRS arXiv v3](https://arxiv.org/pdf/1609.01724v3), pp. 37–38; [PRS journal PDF](https://ems.press/content/serial-article-files/33671), pp. 55–56.
