# Independent source/scope review — Zenodo 22929857

The complete published theorem passes this source/scope review. The explicit deformation preserves the specified Lipschitz sublevel, has the stated quantitative factor, fixes all constants, is continuous in the full input map and works in the original finite U(N). The primary Gromov pages support the paper's stated literal question. No substantive mathematical defect or unresolved proof gap was found within the expressly stated metrics and domain assumptions. This lane's conclusion is an independent review contribution for root/adversarial integration; it is not external peer review or a claim of first priority.

## Exact published edition and custody

Title: A Lipschitz-nonincreasing deformation of small unitary-valued maps. Author: Alec Kriebel, ORCID 0009-0001-9320-500X. Exact record 22929857, DOI 10.5281/zenodo.22929857, version 1.1. Declared publication date is September 23, 2026; the record was created September 24, 2026 at 04:08:19.697044 UTC and updated October 10, 2026 at 21:41:29.296237 UTC. These distinct timestamps are preserved. The PDF itself states September 23, 2026 and version 1.1. Latest and all-versions endpoints identify only this record; no later or mixed-concept paper was substituted.

The native assets occur in this order:

| Native asset | Bytes | Native MD5 | SHA256 |
|---|---:|---|---|
| reproducibility.zip | 133556 | 2c8122b5e0edaaa2d84771abb1a3c616 | 7692e3dbed4e43647721b3c007e567debcdcef0f43cab3700c129433dbd4a930 |
| paper.pdf | 69229 | 5ae67a95127ae05323cc76645ffee931 | 3e8c052065110ec412a3e01e80f0c789f663ce6a9eb74c31aa8fdd99915fc02b |

All record/latest/versions/files responses and both asset transports returned HTTP 200; response headers and native raw JSON objects/order/schemas were retained. Every ZIP member was checked for safe paths, uniqueness, encryption and regular-file type; all 30 payloads passed CRC32 and SHA256 checks. No nested archive format was detected by actual magic. All 29 native MANIFEST.sha256 entries match. The standalone four-page PDF is byte-identical to ZIP member paper/main.pdf. It is searchable, unencrypted and includes no JavaScript. The sole controlling TeX is paper/main.tex, 11,262 bytes and 150 lines, SHA256 954d45001560d29f3286383a40ff9c477a257d9359e02ada7477eac67a0cda4e.

Frozen SOURCE_READY SHA256: b9a6b2f5d848fd924682faf33ad39c74f80d6d849e1a0081abbc5d5bfdc0bf4d. Its manifest SHA256 is 6c0e7a2de9e057d850fc61addd2c493c6f2feacc6c5aa57bd0875df41fbd2924. Sources are read-only. The native CFF still says no DOI was assigned when packaged; that predeposit metadata is preserved. Public citation should use the verified published Zenodo DOI above. This is a metadata housekeeping limitation, not a mathematical defect.

## Independence and actual reading

The scope folder did not previously exist. After custody work, I personally read the entire actual four-page reader, all controlling TeX and every actual rendered page. I then wrote and sealed a substantive independent claim/proof/boundary reconstruction before foreign mathematical bodies, verification code/data, archived audits, priority notes, triage or current reviewer/root opinions. Native API descriptions had necessarily been encountered during metadata acquisition and were explicitly recorded as exposure; they supplied no proof authority. The INITIAL_SEAL SHA256 is ebcd02a2478cbc7cbbf2d9f7e842437b9ba39716c96c95ac6bc25f3c60f8cec1. No native archived audit body or other current lane/root scientific assessment was subsequently read.

## Exact mathematical claim

For n>=2 and N>=1, the domain is the unit-round S^(n-1) with geodesic distance. The target metric is the induced length metric of either the unnormalized Hilbert–Schmidt norm or the operator norm. On all maps Phi with Lipschitz constant <=1/2, equipped with uniform topology, choose one fixed domain point p and put A=Phi(p), W=A*Phi. The claimed deformation is A(W+tI)(I+tW)^(-1), 0<=t<=1. Its Lipschitz constant is at most q_t times the input constant, q_t=(1-t^2)/(1+t^2).

The endpoint is the input-dependent constant Phi(p). All constant maps remain fixed at every time, so the conclusion is a strong deformation retraction onto the constant-map copy of U(N), and the based subspace contracts to I. It preserves the strict sublevel, needs no stabilization in N, works for nonsmooth Lipschitz maps, extends to continuous families on any product parameter space Y x S^(n-1), and is equivariant under constant left/right target frames. The separate S0 extension uses assigned angular distance pi, rather than a disconnected intrinsic path metric.

## Independent proof verification

The unit-round diameter and the 1/2 bound place every normalized value within intrinsic pi/2 of I. Acting a unitary path on an eigenvector bounds each principal angle by its path length, so all normalized values have nonnegative real part. On this closed semicircle domain, (I+tW)*(I+tW)>=(1+t^2)I. Uniform invertibility therefore persists at t=1. Equality of the numerator and denominator Gram matrices proves unitarity.

The noncommutative resolvent difference identity and its differential keep the correct ordered inverse factors. Combined with the ideal norm inequality, they give q_t for both stated norms without assuming commuting perturbations. The decisive intrinsic step uses the image of a minimizing domain geodesic: that image stays inside the semicircle domain and is absolutely continuous; the differential estimate contracts its norm-speed integral. Its transformed image is an admissible target path. Thus the proof does not infer intrinsic contraction from a chordal endpoint inequality and does not require target-geodesic convexity of the semicircle set.

The input-map continuity estimate retains anchor variation as well as normalized-map variation, giving a uniform 3-delta bound in matrix norm. Compactness and uniform invertibility supply joint time continuity; the compact target identifies intrinsic and chordal uniform topologies. Endpoint, fixed-constant and based-space assertions follow directly. Explicit rational conjugation proves frame equivariance. All-dimensional analytic reasoning is independent of the finite diagnostic checks.

The S0 statement uses the principal-angle distance formulas: maximum angle for op, Euclidean angle norm for unnormalized HS. The former follows from the eigenvector lower bound and explicit exponential path; the latter follows from the complete bi-invariant trace metric's exponential minimizing geodesics. The scalar transformed angle derivative is (1-t^2)/(1+t^2+2t cos theta)<=q_t for |theta|<=pi/2, proving both S0 norm estimates. Detailed derivations, including the standard curve-length interface, are in DERIVATIONS.md.

The actual formula also confirms ordinary monotonicity of the Lipschitz constant along time: F_u composed with F_s equals F_((s+u)/(1+su)), and the anchor remains A. For s<=t, applying the proved estimate with u=(t-s)/(1-st) compares the two intermediate maps. This checks the title's interpretation and is not a novelty claim.

## Primary question and classical attribution

Gromov's exact October 1, 2017 author-hosted PDF was read and visually checked on printed pages 35–36, including neighboring context. The standard bi-invariant metric normalization appears on page 35; question [?24](i) on page 36 asks about continuous-in-input deformation of Lip<1/2 sphere maps to constants in all dimensions. The paper proves that assertion for its explicitly defined HS and op length metrics, with sublevel preservation as a stronger property. The nearby Lip<1 discussion and nontrivial-sphere-fibration question are separate. [Gromov primary PDF](https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf)

Neretin's cited Cayley section and Theorem 7.5 were read at printed page 42, actual page 54. The classical chart matches C(W)=(I-W)(I+W)^(-1); direct substitution scales it by (1-t)/(1+t). Its chart denominator is safe on the manuscript's domain. This confirms appropriate attribution of the transformation and does not establish priority for the quantitative map-space theorem. [Neretin primary book](https://www.mat.univie.ac.at/~neretin/lectures/ems.pdf)

The primary caches have SHA256 1478b4025eb55e7237ab3f066e8924938a1de4cd407d74893b49f2b9007d9645 and b0d03b03adb0fe863b3a73a56d4937df19e5e1e1e09fd172c5e9fc71c0553354. Only the relevant cited pages were scientifically read; no claim to have read the entire 572-page book is made. A bounded new search did not establish priority or independently resolve the AMR catalog mapping. The mathematical assertion was checked directly against Gromov, so that catalog identifier should remain bookkeeping rather than proof authority.

## Reproducibility and boundary attacks

Both deposited verification programs were inspected before execution. They support an explicit output argument, which redirected all results to this review folder; no builder/finalizer or archived audit was executed. The native exact checker passed 10/10 rational ordered-word checks. The optional seeded numerical checker completed 7,679 checks on 101 matrix pairs, with zero failures; these are ordinary double-precision diagnostics, not interval-certified proof.

The new independent checker imports neither deposited code nor stored results. It uses actual exact noncommuting rational-complex matrices and inverses, verifies unitarity, ordered difference and differential identities, endpoint behavior, scalar-angle factor, Cayley scaling, frame equivariance and the temporal composition law. It rejects an intentionally wrong inverse order. At the closed semicircle boundary its HS-squared differential factor is exact. Its times include 0, 1/7, 1/2, 999/1000 and 1. Source checksums were reverified after all runs.

Boundary falsification explicitly covered t=0, t=1, approach to 1, eigenangles +/-pi/2, scalar N=1 behavior, noncommuting N=2 matrices, constant maps, changing anchors, strict and closed sublevels, S0 and arbitrary parameter-family continuity. The scalar outside-domain example W=-I expands angular derivatives by 3 at t=1/2 and is singular at t=1; it confirms the semicircle hypothesis is essential to the displayed factor. Some algebraic semicircle-envelope examples lie outside the smaller eligible HS radial ball, so they are not represented as admissible normalized map examples. The scalar sphere map exp(i d(p,x)/2) is admissible and approaches the stated q_t factor near its antipode.

## Limits and disposition

The result concerns exactly the stated unit-round domain, two explicit target length metrics and Lip<=1/2 (with the separate angular S0 convention). Shortest closed-geodesic normalization alone does not define every bi-invariant metric. The deformation depends on a fixed domain basepoint; no nontrivial sphere-fibration or domain-rotation-equivariant theorem is supplied. There is no contraction of the constant-map copy to one prescribed constant, no broad scalar-curvature programme resolution, and no first-publication claim. The principal-log comparison supplies an ordinary deformation for Lip<1 without asserting sublevel preservation.

No substantive defect was found in these complete stated claims, and no repair or narrowed substitute theorem was used. No follow-up research question is proposed. The paper and package accurately identify an unrefereed, AI-assisted preprint and internal AI-assisted audits; those audits are not external human peer review. No outside communication, source edit, website, spreadsheet, Git branch, release or public promotion was performed by this lane.

## Review artifact verification

The read-only verify_review.py checks the sealed review artifacts, original source manifest/CRC/MD5 bindings, initial reconstruction seal and final exact/numeric outcomes. Its --recompute option reruns only the new independent exact diagnostics. Renderings and the full third-party primary cache are retained locally and ignored for repository publication; the cited public URLs and SHA256 pins allow independent reacquisition. No native source package was modified.
