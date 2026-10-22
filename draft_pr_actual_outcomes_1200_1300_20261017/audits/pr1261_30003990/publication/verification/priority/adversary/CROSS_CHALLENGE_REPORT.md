# Detached reverse cross-challenge: priority deduction and spectral framing

Review date: 2026-10-17 UTC. Assignment: PR1261 / problem30003990. This report was written only after both original priority families had sealed and the parent supplied their outside manifest anchors. It supplements, and does not modify, this family's original audit. The three CROSS_CHALLENGE files are a separate seal.

## Verdict and scope

**PASS for the other priority family's mathematical deduction and its qualified priority framing. PASS for the inspected spectral route as an additional deduction from the named standard Christoffel theorem. No material mathematical issue requiring correction of either sealed input was found.** These are validity and framing conclusions, not firstness, current-openness, or publication clearance.

The exact claim remains: for each fixed compact convex body K in R^n, n>=1, with nonempty interior, and fixed real polynomial f, the unit-mass global-SOS density hierarchy with degree at most 2r and normalized Lebesgue reference measure satisfies

    0 <= H_r(f)-min_K f <= C(K,f)/r^2,  every integer r>=1.

One real global square suffices. Replacing normalized Lebesgue by dx changes only the normalization of the density, not H_r. Neither proof establishes an arbitrary-reference-measure theorem, a restricted q=s(f) result, an efficient minimizer algorithm, or a positive Theta rate for every objective. Constant objectives have zero error.

The other priority family correctly labels its derivation a consequence assembled on 2026-10-17 from older ingredients. The inspected 2012 paper does not explicitly print this multivariate hierarchy theorem. A verified implication assembled now does not date recognition or disclosure of that implication to 2012. Both sealed priority audits retain this distinction. The spectral report expressly disclaims a priority determination; its field named `central_new_geometric_check` is intelligible as an additional check in that derivation, but must not be promoted as evidence of historical novelty. In a public exposition, call this the additional geometric lemma unless separately supported priority evidence permits stronger language.

## Authentication and immutable inputs

All four supplied outside manifest anchors matched. All 62 listed members also matched their manifest bytes and SHA256: 29 original members in this family, 15 in the other priority family, 9 in the spectral family, and 9 in its adversarial review. Byte authentication is not a claim to have read every member's content.

| Original outside anchor | Bytes | SHA256 |
|---|---:|---|
| priority/adversary/MANIFEST.json | 5094 | 4a9ab52c55cd2ed713e23ddf1846d13ea549ba94efac7012ab7ee5a43178dc89 |
| priority/independent/MANIFEST.json | 4592 | fd822340f036e804bb0c350cfe386fb35fa5db1439aa97b7e3670ae2bd522686 |
| reviews/spectral_family/manifest.json | 3363 | 048f4a88d185103dce529fb03197901bbd25f87c0be6946c23b60f201e5a2214 |
| reviews/spectral_adversary/MANIFEST.json | 4176 | f81be83ca58de26e0929424a4eba7e8cc23bf1903172660c9677d571cb6db563 |

The audit root for these relative paths is `/Users/alec/Documents/Math/draft_pr_actual_outcomes_1200_1300_20261017/audits/pr1261_30003990`. Exact paths, bytes, and hashes of all authenticated members and of the primary bodies used here are recorded in CROSS_CHALLENGE_MANIFEST.json. The original outside report/verdict anchors for this family remain REPORT.md SHA256 `a6880afc134d701d73d4365c5cbe92a383cc594bf49a05e98692d2dbe3489cff` and VERDICT.json SHA256 `b55433289d11a8e37b4ed13c8cf22bdd2c54ed7783d582854d0ec8bcd5663a59`. Its original DERIVATION.md remains SHA256 `81e7e4e4fba1350120bee7bcd0c08a630d42bc32e4b14779449e90db41fcf562`.

The content targets read were the other family's full REPORT.md, DERIVATION.md, CLAIM_MATRIX.md, and BIBLIOGRAPHY_QA.md; the spectral family's full report.md, adversarial_review.md, and verdict.json; and the separate spectral adversary's full REPORT.md and VERDICT.json. SOURCE_RECORDS.json was consulted selectively for the newly encountered Gaussian source S09. The numerical files were hash-authenticated only in this phase; no reported numerical values are newly certified.

## Cross-challenge of Totik–Varga 2.1

Primary source: V. Totik and T. Varga, *Non-symmetric fast decreasing polynomials and applications*, J. Math. Anal. Appl. 394 (2012), 378–390, DOI [10.1016/j.jmaa.2012.03.006](https://doi.org/10.1016/j.jmaa.2012.03.006), [author PDF](https://www.math.u-szeged.hu/pot/5fdp.pdf). The retained body is 285373 bytes, SHA256 `004361b85bbaef05716c7789a108b9b764e3e7789ba22724a029e9ee5429a7a9`.

Theorem 2.1 is printed p.379 / PDF p.2. Its hypotheses are that psi is nonnegative and increasing on [0,infinity), psi(0+)=0, psi(v)<=M_0 psi(v/2), and the integral from 1 to infinity of psi(v)/v^2 is finite. The other family's choice psi(v)=sqrt(v) satisfies every condition: M_0=sqrt(2), and the integral equals 2. The parameter a=0 is explicitly allowed by a in [0,1/2]. The positive-degree parameter m is independent of the ambient dimension and of all measure parameters.

The displayed argument of psi is m|t|/(sqrt(|t|)+sqrt(a)). Thus at a=0 and t>0 it becomes m sqrt(t), giving exactly

    P_m(0)=1, deg P_m<=m, |P_m|<=2 on [0,1],
    |P_m(t)|<=A exp[-c(m^2 t)^(1/4)].

The constants A,c do not vary with m. The point t=0 uses the separate normalization P_m(0)=1, so no 0/0 evaluation is needed. The theorem's proof constructs real polynomials; taking a real part would also retain the stated value and bounds. No Christoffel, zero-spacing, local interval-doubling, or measure hypothesis enters Theorem 2.1.

This family's initial audit read the full proof on printed pp.380–381 / PDF pp.3–4, as did the other family's recorded read scope. Its dependence on older symmetric fast-decreasing-polynomial results is disclosed. This cross-challenge rechecked the actual theorem and its endpoint specialization, rather than claiming that every older cited proof was independently reconstructed. Ordinary reliance on the named standard theorem is sufficient for the deduction; the earlier missing Ivanov–Totik body remains a historical/source-completeness limitation.

### Markov core and relative normalization

The exact interval Markov inequality is printed as Lemma 11 on PDF p.18 of Slot–Laurent arXiv:1905.08142v2:

    ||p'||_[a,b] <= 2m^2/(b-a) ||p||_[a,b].

Consequently ||P_m'||_[0,1]<=4m^2. For h=1/(8m^2), the normalization at zero implies P_m(t)>=1/2 on [0,h]. For any finite nonzero positive measure nu on [0,1] with

    F(t)<= (t/h)^s F(h),  0<h<=t,  F(t)=nu([0,t]),

one has F(h)>=h^s F(1)>0 when h<=1, including when s=0. Therefore Z=integral P_m^2 dnu >=F(h)/4. No absolute lower-volume estimate is inserted in place of this relative denominator.

The numerator on [0,h] is at most 4hF(h). On E_j=(2^j h,2^(j+1)h], the verified bound is

    integral_Ej t P_m(t)^2 dnu
      <= A^2 2^(s+1) h F(h) 2^(j(s+1))
                     exp[-2c(2^j/8)^(1/4)].

Here t<=2^(j+1)h supplies one power, the cumulative hypothesis supplies 2^((j+1)s), and m^2t>2^j/8 supplies the exponential. Extending through empty shells is harmless. The infinite series converges because its successive ratio tends to zero. With B=4+A^2 2^(s+1) times that series, the normalized first moment is at most 4Bh=B/(2m^2). Every factor of the small mass F(h) cancels. This verifies the normalization bridge; a bare Christoffel norm upper bound would not by itself supply this first-moment ratio.

### Proxy geometry and all integer orders

Choose a minimizer z of f on K. The constrained directional derivative gives ell(x)=grad f(z) dot (x-z)>=0 for every x in K. With H=max_K ||Hessian f|| and gamma=1+H/2, the quadratic

    g(x)=ell(x)+gamma||x-z||^2

obeys 0<=f(x)-f(z)<=g(x), and g>0 away from z. Compactness gives G=max_K g>0; u=g/G has degree at most two and range [0,1] on K. This quadratic upper-proxy reduction is prior work, not a novelty of this audit.

For alpha in [0,1], g(z+alpha(x-z))<=alpha g(x). The homothety with alpha=h/t injects the K-sublevel {u<=t} into {u<=h}, with Jacobian (h/t)^n. Thus the required cumulative condition holds with s=n. It also holds for t>1, because the same homothety applies to all of K when the larger sublevel has saturated. The proof uses only convexity and full dimension; it needs no smoothness, semialgebraicity, or density formula for u#dx.

For r>=2 choose m=floor(r/2). The square P_m(u)^2/Z has degree at most 4m<=2r, integrates to one, and is a global square on all of R^n even though u need not be nonnegative there. Since m>=r/3, the error is at most 9GB/(2r^2). For r=1 the constant density has error at most G. Enlarging C covers this order and also constant, affine, stationary, boundary, and nonunique-minimum cases. There is no order-dependent kernel power or hidden degree cost. The other family's calculation is correct.

## Spectral route: actual additional argument and method framing

The spectral family's proof imports the upper half of Totik–Varga Theorem 3.1, not an unsupported extreme-zero assertion. In the paper's exact convention lambda_k minimizes integral p^2 over deg p<=k and p(z)=1. Its hypothesis is full interval-centered doubling on [0,beta], not merely cumulative growth at zero. The source permits compact support outside this small interval; its proof controls that part. Evaluation is uniform on [0,gamma] for gamma<beta. The actual definition (3.1), Theorems 3.1–3.2, and the relevant upper-proof passages were checked in the retained primary body, in addition to the earlier full primary reading recorded by this family. Underlying cited approximation theory is a named standard dependency, not newly reproduced here.

The spectral measure h#mu, with h(x)=a dot x+b||x||^2 after translation, satisfies stronger regularity for a geometric reason. For a!=0 choose an interior e, A=a dot e>0, and E=a-perp. In central coordinates X(u,z)=(1-u)z+u e,

    dx=(A/||a||)(1-u)^(n-1) du dz,
    G_u=A+2b X(u,z) dot(e-z).

Small h forces 0<=u<=beta/A and uniformly small z. The preliminary rectangle bound, made before narrowing the root domain, ensures A/2<=G_u<=3A/2 and u<=1/4. Every small-level point is represented by the root G(u,z)=t. For a projected point admitted at level s, increasing to level t moves along its segment toward the same interior e; hence D_s is contained in D_t. This is an additional use of convex geometry absent from a cumulative-growth hypothesis alone. The full Jacobian gives

    w(t)>=c_0 w(s),  0<s<=t<=beta,
    c_0=(1/3)(3/4)^(n-1).

Independently, origin-polar integration gives a shrinking angular domain as t increases and R_s/R_t>=s/t for the roots of alpha R+bR^2=t, alpha>=0. Hence w(t)<=(t/s)^(n-1)w(s). The two formulas can be compared on one common full-measure set; no exceptional-level value is used as a premise. Combining them and integrating over pairs proves full centered doubling, including doubles touching zero. A positive level patch comes from an interior ball scaled toward zero. Dimension one uses the legitimate zero-dimensional measure on E.

For a=0 the separate formula is w(t) comparable to t^(n/2-1) near zero. An interior cone supplies the lower angular bound. The exponent exceeds -1, including -1/2 in dimension one, so the integral doubling argument remains valid for decreasing densities. Taking a limit of the nonzero-gradient constants is neither needed nor asserted.

The same comparisons yield the further shell estimate

    nu([z-delta,z+delta]) <= D(delta/z)F(z),  delta<=z/2,

for small z. This estimate is stronger than merely centered doubling and is explicitly proved, so it is legitimate in the next bridge. For the degree-N orthogonal polynomial's smallest zero z_1, Gaussian quadrature through degree 2N-1 gives lambda_(N-1)(z_1)=omega_1. Its first cardinal polynomial is at least one on [0,z_1], proving F(z_1)<=omega_1. The compression of multiplication by t on degrees <=N-1 has z_1 as its least eigenvalue and a real polynomial eigenvector. Degree N-1, rather than N, is essential and correct.

A separate trial (1-t)^(N-1), after scaling support to [0,1], proves z_1 tends to zero without assuming a rate. Thus for all sufficiently large N, k=N-1>=1 and the local Christoffel bound is available. Put delta=sqrt(z_1)/k+1/k^2. If delta>z_1/2 the desired comparison is immediate; otherwise the shell estimate and F(z_1)>0 give z_1<=CD delta. In both cases y=k sqrt(z_1) satisfies y^2<=B(y+1), hence z_1=O(N^-2). Compact support absorbs all finite earlier orders and N=1. Finally m=floor(r/2), N=m+1, and the squared polynomial eigenvector composed with h has degree <=4m<=2r and error O((m+1)^-2)=O(r^-2), including r=1.

I find no flaw in these bridges. The spectral review's exact one-dimensional controls are consistent with their signs and degree convention. No finite numerical experiment is needed for this conclusion. This phase did not execute the frozen scripts, run source-author code, or certify the floating-point results.

This does not overturn our original warning. A generic measure satisfying cumulative growth need not be interval-centered doubling; the spike/valley counterexamples concern generic measures, not measures proved to come from this special convex-quadratic construction. The spectral route supplies the previously missing additional hypothesis by an actual geometric proof. Totik–Varga Theorem 3.2 also allows doubling only at centers in a set, including the singleton endpoint; that weaker endpoint norm estimate remains a separate route and does not automatically replace the spectral shell/first-moment bridge.

The two methods are distinct presentations: the scalar argument uses an explicit endpoint kernel and relative shell/core mass; the spectral argument establishes additional density regularity and uses a Christoffel estimate, Gaussian quadrature, and a compression eigenvector. They share the known quadratic reduction and older approximation theory. Their successful independent reconstruction supports validity. It does not establish a new historical mechanism or priority for either presentation.

## Claim matrix and bibliography challenge

The other family's CLAIM_MATRIX preserves the necessary distinctions: global SOS versus weighted preordering; Lebesgue versus Chebyshev, Jacobi, Gaussian, or arbitrary measures; general convex bodies versus boxes, balls, and simplices; the original f-pushforward versus a chosen quadratic proxy; upper rate versus minimax sharpness; and fixed degree loss versus order-dependent degree loss. In particular its use of the classical interval linear objective as a worst-case lower example is appropriate and does not assert Theta for each f.

The OWR source's missing visible unit-mass equality is openly stated and resolved by the probability formulation and the full hierarchy papers. The Slot–Laurent log-squared bound and the 2026 overview are used as printed baselines, not as a present-openness proof. The bibliography distinguishes retained preprint numbering from final journal metadata, acknowledges banner/internal-date discrepancies, rejects an incorrectly guessed DOI, and does not infer line-by-line disclosure or transmission from dates. I found no material bibliography inconsistency in this targeted comparison. This is not a new independent audit of every metadata endpoint or every unread source proof.

One newly encountered source in the other family's audit was inspected directly here: Gribling–Klep–Kumar, arXiv:2610.22030v1, retained PDF 487208 bytes, SHA256 `f7cac4e7f2f7075c935b2c4ed8e09347cfbed4b37fdf985871f834ef8c2983cc`. Its banner is 15 Oct2026. PDF pp.1–4 show the Gaussian hierarchy on R^d, the attained-infimum O(1/r) theorem, and its p.2 report of the compact convex Lebesgue log-squared baseline. This corroborates the other family's narrow interface comparison; it does not resolve the present compact theorem, and its later proof was not newly audited here. I do not use its date to infer disclosure lineage.

The other family's missing Kroó 2015 needle-polynomial body remains a real bounded-search limitation, as does our initial missing older-body coverage. The author is András Kroó (Kroo without diacritics); the source record's title and DOI `10.1007/s10474-015-0507-8` identify the item. Neither an abstract, a failed PDF retrieval returning HTML, an EulerSolve screen, nor partial Zenodo metadata can exclude an exact earlier theorem or establish firstness. No positive same-scope printed theorem was newly located during this cross-challenge. No literature search was performed in this phase, so that statement is not an expanded absence claim.

## Read scope, phase ledger, and completion

Retained primary reads in this phase used local bodies and text; no new HTTP bodies, remote searches, or raw copies were created. New web-query invocations: 0; new literal queries: 0; new HTTP requests: 0. The original two families' literal-query and body-read ledgers remain unchanged and retain their own bounded scopes. Primary PDF hashing and extraction are our read-only tooling, not execution of source-author research code.

| Retained primary body | Cross-challenge scope | Bytes / SHA256 |
|---|---|---|
| Totik–Varga 2012 | Rechecked 2.1 endpoint statement, 3.1–3.2 and definition (3.1), relevant upper-proof passages; earlier full relevant proof reads remain in original audit | 285373 / 004361b85bbaef05716c7789a108b9b764e3e7789ba22724a029e9ee5429a7a9 |
| Slot–Laurent 1905.08142v2 | Rechecked precise Lemma 11 Markov interval form, PDF p.18 | 573575 / c8aebdfc6a1b6a65dbdebbea6b31edfcb4e4bd711d4fc80077a2485bd7e6764a |
| Gribling–Klep–Kumar 2610.22030v1 | PDF pp.1–4 extracted and read; later proof not audited | 487208 / f7cac4e7f2f7075c935b2c4ed8e09347cfbed4b37fdf985871f834ef8c2983cc |

Timestamped checkpoints, UTC:

- 2026-10-17 21:41:06 — Began detached phase after receiving the four outside anchors. Completion estimate: 5% of assigned cross-challenge.
- 2026-10-17 21:42:51 — Core priority derivation and primary interfaces checked; Gaussian source inspected. Completion estimate: 65%.
- 2026-10-17 21:43:36 — All four manifests and 62 listed members authenticated; both spectral reports and all critical geometric/spectral bridges checked. Completion estimate: 85%.
- Final seal timestamp recorded in CROSS_CHALLENGE_MANIFEST.json — Detached report, verdict, and end authentication complete. Completion estimate: 100% of this assigned review; publication/priority clearance remains unassessed.

Only the three requested new root-level files were authored in this phase. All sealed originals and raw inventories are preserved. No unrelated agent or individual was contacted; the only task report was to the assigning parent. No subdelegation, Git/index/ref/PR/Zenodo/GWS mutation, outreach, or final-paper/workflow review occurred. The detached manifest excludes itself and its final digest is delivered outside it. No edits follow the new seal.
