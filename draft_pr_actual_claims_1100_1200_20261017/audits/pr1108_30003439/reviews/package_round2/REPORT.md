# Second successive fresh adversarial review of final publication package

Completed 2026-10-17T17:42:48.742303+00:00; bounded review completion estimate: 100%.

**Disposition: PASS — no actionable mathematical, reproducibility, provenance, packaging, metadata, or rendering defect found in the frozen package reviewed.**

This is the second fresh review requested by the parent auditor. I reconstructed the proof from the final `main.tex` and developed independent checks before consulting the bundled older mathematical/priority materials. I did not read the first fresh package review. The parent supplied its PASS status, but no prior reasoning or findings were used. No frozen package, parent report, Git state, PR, publication, or external communication was changed. Review files are confined to `reviews/package_round2/`.

## Exact package and target

- Problem 30003439 / OWR-15219-008; source PR 1108, frozen head `148130ab93ab46a3459d7bc98a11a1ca79052d65`.
- Original proof input SHA256 `9577476ee2c0fd2e3d12ab1265201d8b99f6ef50a9060e245c46f872dd673302`.
- Final TeX SHA256 `03f685e09a10a140915acfcaa1e4fcda9197a9a8a6f8800f2a3330c9532a101b`.
- Five-page PDF SHA256 `ad9864c08642737e4459673749c1db6d2e3dafb521f323fb1071f157f8110eb0`.
- Source/verification ZIP SHA256 `d97ba7ed1057518e3bd499d88182c64767e912d589ed8574092c0ebc7a27c06e`.
- Upload kit ZIP SHA256 `0f52fdfc42cc83e4739ca5de9cabda5120565c3d48cbb4457a0da9ab7ce1bd76`.

The exact assertion is that K={x,y,z≥0:xy²≥z³} is regular, algebraic and convex; F=25f, f=−log(xy²−z³)−log z, is a parameter-100 normal barrier; D³F(a)[h,u,u]≤0 for all a∈int K, h∈K, u∈R³; and no homogeneous polynomial has K as its hyperbolicity cone in the original R³. Success does not require the parameter to be optimal, novelty of the underlying cone or of self-concordant barriers on it, a projected/lifted obstruction, an answer for every regular cone, or worldwide priority certification.

## Independent analytic reconstruction and adversarial attacks

**Geometry/interior/boundary.** The displayed homogeneous inequalities imply closedness and conicity, the orthant pointedness, and the strict point (2,1,1) nonempty interior. The Hessian of m=x^(1/3)y^(2/3) is the printed negative scalar times a rank-one Gram matrix. Continuous extension preserves concavity on the closed orthant; its hypograph intersected with z≥0 is convex. Every interior point has x,y,z>0 and p>0. Conversely those strict inequalities give an open neighborhood. If x=0 or y=0, feasibility forces z=0, and coordinate/p equality points cannot be interior. Therefore every finite boundary point has z=0 or p=0; the quartic q=zp tends to zero from above along every convergent interior sequence. No missing boundary component prevents barrier blowup. Smoothness holds on the entire stated interior. Positive-definite Hessian and this boundary behavior justify the closed convex extended function.

**Derivatives, polarization and normality.** Independently differentiating a single logarithm of the quartic q=x y² z−z⁴ yields f_i=−q_i/q, f_ij=q_iq_j/q²−q_ij/q, and

D³f_ijk=−2q_iq_jq_k/q³+(q_ijq_k+q_ikq_j+q_jkq_i)/q²−q_ijk/q.

This does not reuse the distributed checkers' separate p and −log z tensor construction. It reproduces the manuscript identities. The δ,w,v,b,c decomposition is well-defined because g,δ,y,z>0. The Hessian vanishes only when b=c=w=0, hence only for the zero vector. Cubic polarization has the printed 1/3 factors. Weighted Cauchy–Schwarz gives |c−4b|≤3√(2b²+c²). Grouping the cubic mixed terms gives the claimed constants 2,3,3,2; summing them gives 10. For example the v/w group is bounded by |w_h|v_u²+2|w_u||v_h||v_u|≤3||h||f||u||f², and the ell group has the same bound. The final b,c group is bounded by 2||h||f||u||f² as printed. Multiplication by 25 changes the mixed constant to 10/√25=2, with ||u||F=5||u||f. The quartic degree gives logarithmic homogeneity 4×25=100. Euler differentiation and positive-definite Hessian give the exact squared dual gradient norm 100, so the gradient barrier bound is also established. No assumption of hyperbolicity is used in normality.

**Global curvature reduction.** The normalization uses an automorphism D fixed at the base point; differentiating a point-dependent D would be invalid, but that is explicitly avoided in the text. Its inverse also preserves K, and congruence covers arbitrary test vectors. The cone-direction decomposition has nonnegative coefficients and includes t=0, h=0, and the separate h_y=0⇒h_z=0 endpoint. Thus testing h(t) and e_x is exhaustive, not a sample of extreme directions.

**Exact matrix/positivity.** Formal differentiation of the single quartic log reproduces all nine matrix entries, the 2×2 leading minor and the determinant as polynomials in s,t. I additionally checked both printed square identities and used a different universal sign argument. Regarding P and R/(t+2) as quadratics in s, their discriminants are respectively

−3(t−1)²(8t³+21t²+6t−11),

−3(t−1)³(8t²+13t+3).

For t>1 both are strictly negative and both leading coefficients positive. The first remainder at t=1+v has positive coefficients (8,45,72,24). For 0≤t<1 the coefficients of the quadratics are nonnegative and their constant terms strictly positive; t=0 is included even though the second leading coefficient vanishes. At t=1 direct substitution gives P=R=6s². Hence the first three leading minors establish positive definiteness precisely when t≠1. At t=1 the zero first row/column requires the separate lower block argument; its determinant is s(2r+7)>0. The e_x Gram identity has rank two and kernel span{(1,1,1)}. Neither endpoint is incorrectly promoted to strict definiteness. All divisors used in the proof are positive on the region where they are invoked; s=0 is an excluded boundary base. Large t and r and near-degenerate s,t were also checked exactly as supplementary evidence.

**All-polynomial hyperbolicity obstruction.** For any putative H,e defining K, e lies in int K. Boundary containment in {H=0} follows from continuity of real roots with fixed nonzero leading coefficient; it is not assumed just from the displayed cubic. The curved open boundary patch implies H(z³/y²,y,z)=0 as a rational-polynomial identity. Clearing denominators is justified on y,z>0, an open set. In R(y,z)[x], x−z³/y² divides H; y²x−z³ is primitive because gcd(y²,z³)=1. Gauss's lemma therefore gives p|H in R[x,y,z]. For every possible interior e, a=(e_xe_y²)^(1/3)>b=e_z>0, and the line v=(0,0,1) produces the printed linear times quadratic factorization with discriminant −3a²<0. H(e)>0 ensures its restriction is a nonzero polynomial; multiplication cannot cancel complex roots. This argument handles every homogeneous degree and every possible hyperbolicity direction. It neither assumes H=p nor makes a claim about projections or lifts.

## Independent code and adverse controls

`independent_exact.py` is a separately authored standard-library exact rational implementation. It differentiates the quartic as a single log in a five-variable formal polynomial ring, proves the discriminant identities coefficientwise, and compares with two-variable affine logarithm jets of q(a+A h+B u). Its completed optimized-Python run passed **1,797 checks**, including **240** arbitrary-base mixed contractions and all printed Hessian/polarization identities at those cases. Exact cases include s=10⁻⁶, s≈10⁶, t=0, t=10⁻⁶, t=1±10⁻⁶, t=1, t=2 and t=10⁴, with non-normalized bases, fixed-D covariance, and mixed self-concordance bounds. These rational cases supplement the analytic argument; they do not replace universal sign reasoning.

Eight independently implemented adverse controls succeeded: strict-definiteness fails at t=1; omission of −log z gives determinant −24576 at r=5,t=2; reversing e_x to an off-cone direction violates the sign; a false parameter/scaling claim is rejected; a corrupted off-diagonal is detected; a missing factor of t−1 is detected; the wrong sign of the hyperbolicity discriminant is detected; and the e_x determinant correctly vanishes. The check mechanism uses explicit exceptions, so optimization cannot disable it. The pre-extension normal run passed 1,317 checks; the final 1,797-check run used `python3 -B -O independent_exact.py`. Results are in `independent_exact_results.json`.

The actual scripts extracted from the final distributed source ZIP were executed, rather than relying on old reported results:

| Archived verifier | Result |
| --- | --- |
| Geometry, ordinary Python | PASS, all 791 checks, eight negative controls |
| Geometry, optimized Python | PASS, all 791 checks; stable result equal to expectation |
| Curvature, ordinary Python | PASS, exact identities, 45 rational grid cases, 315 independent log-series contractions |
| Curvature, optimized Python | Nonzero startup rejection with the specified enabled-assertions message |

Stable outputs equal archived `verification/expected_results.json` exactly after removing only declared runtime/version fields. Outputs and stderr are preserved under this review's `tmp/`; `package_integrity_results.json` records the executions.

## Package, metadata and provenance

`package_integrity.py` passed **261 checks**. All receipt file sizes/hashes match, including the three task-pinned final hashes. The source archive has exactly **26** members and the upload kit exactly **five**. Names have no duplicates, case collisions, traversal, absolute paths or backslashes; entries are unencrypted regular files, and all ZIP CRCs pass. `SOURCE_MANIFEST.json` covers exactly every other source member, with exact size/hash equality to actual bytes and `PACKAGE_RECEIPT.json`. Every distributed main/readme/license/PDF/verifier member equals the corresponding publication file; every bundled audit equals its frozen repository source. No third-party PDF or copied primary-source document is redistributed in the source archive.

The kit's PDF, nested source ZIP, metadata and README are byte-identical to their frozen counterparts. Its portable deposit differs only in the intended local upload paths. The metadata, repository deposit metadata and portable deposit metadata are equal. Both deposit paths name the exact files intended for upload. Source provenance matches problem ID, alias, PR, frozen head and original proof input; all original manifest entries and the retrieved-input receipt match their frozen bytes.

Title, author Alec Kriebel, independent-researcher affiliation, ORCID 0009-0001-9320-500X, open CC-BY-4.0 licensing, preprint status, date and version are consistent. The theorem scope, credit to Hildebrand and Roy–Xiao, nonoptimal parameter, bounded priority status, extensive AI usage, unrefereed status, absence of external human peer review and absence of proof-assistant certification are explicit in both note and metadata. The source ZIP deliberately excludes later fresh-review receipts to avoid a self-referential archive manifest; this is disclosed in the README and does not affect source reproducibility.

## Independent PDF rebuild and complete visual review

I extracted the actual source ZIP into this review's `tmp/`, used an APFS clone of the existing TeX cache, and ran Tectonic **0.16.9** with cached-only (`-C`) and untrusted-input mode. The build succeeded with five pages, no overfull/underfull box or undefined-reference warnings, and no downloads. The isolated cloned cache has been removed; the shared cache was untouched.

Rebuilt PDF SHA256 is `25ceb4ed3f411c9f94e33b3b79ce6f8302d08ed6499fd1bc77b1d3c32a068bc4`. The PDF CreationDate changes from 17:20:04 to 17:37:59 UTC. Every page has identical extracted text, dimensions and uncompressed drawing stream bytes. Rendering both PDFs at 150 dpi yields **zero differing pixels on all five pages**. I visually inspected each rebuilt 1275×1650 page: title/theorem, attribution/normality, curvature formulas, positivity/nonhyperbolicity, and status/references are complete, legible and clear of clipping or overlaps. The pixel equality transfers this visual check to the frozen PDF. Link rectangles lie within their pages; PDF author/title metadata agree. Evidence is in `pdf_rebuild_results.json` and the five page images under `tmp/rendered_rebuilt/`.

## Primary-source and bounded priority scope

Fresh primary-source reads agree with the stated scope:

- [Tunçel's full OWR report](https://ems.press/content/serial-article-files/46677?nt=1), printed p.799, contains the existential algebraic-cone question and the same directional third-derivative definition; the [author contribution](https://www.math.uwaterloo.ca/~ltuncel/publications/OWR-2017-14.pdf) supplies a second locator. The separate generalized-Lax question is not being answered.
- [Nesterov–Tunçel](https://arxiv.org/pdf/1412.1857), definitions and §6, use the same normal-barrier and curvature conventions. The duality discussion supplies no free transfer of curvature to an arbitrary dual cone.
- [Hildebrand's Theorem 3.2, family 5](https://arxiv.org/html/1305.4814v1) contains this cone under (x1,x2,x3)=(x,z,y), p=3,q=3/2. The manuscript explicitly credits this prior cone. Affine-sphere hyperbolicity is a different property.
- [Roy–Xiao, Theorem 2, PDF p.3](https://optimization-online.org/wp-content/uploads/2018/01/6441.pdf) gives the stated parameter-3 self-concordant barrier for exactly this nonnegative power-cone family; the manuscript credits it and does not claim an improved parameter. Its theorem establishes self-concordance and does not itself supply this mixed-sign certificate.
- [DTV's PDF](https://arxiv.org/pdf/2509.10263v2), §2.2, Definition 3.1 and §6, matches the definitions and retains a broader universal question. Its internal date is June16,2026; the separate [HTML](https://arxiv.org/html/2509.10263v2) says August24,2026; the [arXiv version record](https://arxiv.org/abs/2509.10263) lists v2 June12,2026. These distinct representations are explicitly distinguished. Their date discrepancy's cause is not established.

After my independent mathematical reconstruction, I checked the bundled priority ledger. It contains exactly **65** independent-track query strings, with three additional root queries explicitly separated. The audit states bounded relevant-source findings, not exhaustive or first-ever priority. It expressly records uninspected/inaccessible leads: Hildebrand's habilitation URL returned 404; the 2026 publisher full text is subscription content; the OpenReview prepublication endpoint returned 403/verification; and Güler1997/Hildebrand2014 were inspected only at primary-record/abstract scope. The final note/metadata preserve these limits. I did not repeat all 65 searches or infer worldwide novelty from them. Fresh in-memory retrievals succeeded for all eight primary items in `source_scope_results.json`. OWR, NT, Hildebrand and both DTV PDFs match their pinned source identities exactly. The arXiv and author DTV PDFs are byte-identical, while the separately hashed HTML carries its different internal date. No full third-party source body is retained on disk; phrase absence is a navigational observation, not a substitute for examining theorem scope.

## Strongest result and exact remaining gap

The complete stated theorem survives this adversarial review, including all interior bases, all cone directions, the two semidefinite degeneracies, the mixed self-concordance normalization, and the all-degree/all-direction homogeneous hyperbolicity obstruction. No unsupported mathematical step or package inconsistency was found. Finite computations are supplements to the independently reconstructed analytic proof.

There is **no identified remaining gap in this theorem**. Limits remain: this is an AI-assisted adversarial audit rather than external human peer review or formal proof certification; literature coverage is bounded and certain primary leads remain uninspected; parameter100 is not claimed optimal; and neither the universal every-regular-cone question nor hyperbolic projections/lifts is settled. These are already correctly disclosed and are not blockers to the precise package claim. No outreach was prepared or initiated.
