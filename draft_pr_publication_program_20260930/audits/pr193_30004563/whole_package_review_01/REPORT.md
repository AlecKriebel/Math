# Whole-publication-package adversarial review 01

**Verdict: CLEAN PASS for the entire frozen package in its expressly qualified scope.** No substantive mathematical, source-scope, reproducibility, archive-integrity, attribution, or metadata issue was found. There is no required repair. This is one new AI adversarial review, not conventional human peer review or a publication authorization.

Review target: PR193 / problem30004563, `publication_package_v2`, exactly15 allowlisted files; package-seal SHA256 `fe7b6c7abda9d04f35d6b07f5524e023320df9d8c399bc01cd4fb797c630301d`. The reviewed ZIP SHA256 is `c32415716b800aa38687d9882598ab4c8b9ae43a91e4805bc1ebfaa3572a299f`. Review completed15October2026 UTC.

## Independence and sequence

I read the primary published definitions2.1,2.4,2.5 and Remark4.8, and OWR35/2020 p1785, before any manuscript, support code, certificate or previous review. `SOURCE_FIRST_PLAN.md` was then sealed at SHA256 `a94fdb682702b776357dc3532c8eae2fd202f9caae789923d7ceb038e0b766ab`. The primary pages were subsequently rendered and visually compared, including Figure6's exact combinatorics.

I inspected the complete final verifier source before executing an owned copy. I wrote an independent exact checker without importing author code: three successive outward integer-isqrt square-root enclosures on a70-digit rational grid, a transformed odd boundary polynomial in z=1-2t with190 exact bisections, general vector trilateration, and symbolic coefficient-vector cancellation. The author uses direct integer eighth-power binary search and128 boundary bisections. The core independent assessment was recorded before reading any earlier audit report. Proposed refined outgoing s brackets are read as untrusted data from the author certificate; their strict signs are independently recomputed. The theorem's original six cutpoint signs and all boundary roots are reconstructed from the displayed constants, independent of those proposed refinements.

Only after the independent core passed did I read the earlier mathematical and priority reports, inspect all their executable code, and replay their mathematical scripts in extracted owned copies. No shared file, Git/index/ref/branch state, editor, remote artifact, PR, comment or publication was changed. No individual was contacted and no outreach was prepared.

## Primary claim and exact source correspondence

For finite nonzero alpha, the primary alpha-quad equation is |P-Q|^alpha+|R-S|^alpha=|P-S|^alpha+|Q-R|^alpha. Definition2.4 permits arbitrary realizations satisfying those face equations; crossing edges are allowed. Definition2.5 requires six distinct boundary vertices and noncollinear odd/even triples. Proper embeddings add independent geometric requirements.

Published Remark4.8, printed p811, explicitly expects at most three intersections of two construction curves sharing a focus for alpha>1. The expectation is simulation based. OWR p1785 expressly conjectures a maximum of three potential central points in its crossing-permitted setting. With A2=A, A4=B, A6=C, the two outgoing curves here are C3 (foci A,B through A3) and C1 (foci C,A through A1). Both meet the exact primary definition; they share A and have noncollinear other foci. The boundary completion and incoming certificate make this a cube-realization counterexample as well as a common-focus curve counterexample.

The strongest verified result is exactly the note's theorem: one fixed admissible six-point algebraic boundary at alpha16 has an incoming realization and at least five distinct nonboundary outgoing centers. No proper-embedding result, exact total root count, global maximum, or alpha<1 result follows. The package states these limits consistently.

## Independent mathematical checks

Write N(X,P)=|X-P|^16 and s=N(X,A). The nonnegative eighth roots u=s^(1/8), v=(s+lambda)^(1/8), w=(s+1)^(1/8) are the squared distances, not the distances. Subtracting squared-distance equations gives the displayed invertible linear system with determinant4bd>0. If G(s)=0, its coordinates give all three nonnegative squared distances, so taking eighth powers is reversible. Conversely every focus-system solution produces the same s and coordinates. Different s values therefore give different points. No branch, squaring, denominator or extraneous-root gap was found. G is continuous even at s=0; the proof brackets all lie at positive s.

The independent exact enclosures prove the alternating signs at

9/10000, 11/10000, 13/10000, 1/2, 1, 10^16,

inside respectively (0.38,0.39),(-0.28,-0.27),(0.51,0.52),(-0.91,-0.90),(9,10),(-4.766,-4.765). Each of the five disjoint open intervals has a zero by IVT; no uniqueness within an interval is used. All ten signs at the certificate's five refined bracket endpoints were also independently checked.

The final endpoint's concavity proof is sound: u=100 exactly, delta_v<=lambda/(8*10^14), delta_w<=1/(8*10^14). The stated positive-coordinate boxes follow from the linear system, and their squared endpoints prove the claimed G bound. The exact limiting coordinate is the circumcenter (2073/20000,1249057/128000), with squared norm39007985196121/409600000000<95.235. The differences of the radicals tend to zero, hence G tends to minus infinity. The fifth center remains a finite point. Independent iterated-isqrt arithmetic also directly verifies the10^16 sign without the concavity estimate.

For each boundary definition, g(t)=(t^2+h^2)^8 has g''(t)=16(t^2+h^2)^6(h^2+15t^2)>0 for the nonzero heights10,1,-10. Thus g(t-1)-g(t) is strictly decreasing. Its leading term is -16t^15, so it covers the real line once. Each boundary parameter is one fixed uniquely specified algebraic number. Interval boxes enclose these constants; they do not select different configurations at different roots. The independent transformed-polynomial isolation reproduces their coordinates.

The six edge powers are exactly (a,f,f+lambda,g,g+1-lambda,a+1), so both alternating sums equal a+f+g+1. For incoming constants L=g-f-lambda and M=a-f, the independent checker proves positivity and a nonzero odd determinant. For this one fixed boundary, H is continuous, and exact propagation gives H(1/100) in(0.00037,0.00038) and H(11/1000) in(-0.00081,-0.00080). This proves incoming existence without invoking a flip-existence theorem. Its whole retained box lies in(0.1677,0.1717)x(-0.0036,-0.0026).

All six ordered face equations cancel identically in an independent coefficient-vector computation. In particular the third incoming equation uses M-L=a-g+lambda, derived from the exact boundary identities. No equality is inferred from an interval merely enclosing zero.

The independent checker verifies all15 distinct boundary pairs and all20 noncollinear boundary triples, the required even determinant0.00132672 and odd determinant between6.37 and6.39. It independently verifies every selected outgoing center's separation from the boundary and from each other, and avoidance of all15 boundary-pair lines by each selected outgoing box and the whole incoming box. The strict orientation pattern(-,+,+,-) proves that[A1,A2] and[A3,A4] cross internally. Therefore no choice of center gives a proper embedding for this fixed boundary.

After reading the historical source/geometry report, a separate helper independently recomputed its additional polynomial-gradient determinants and face claims. Outgoing Jacobian signs are +,-,+,-,+, the incoming determinant is positive on its whole box, all tested face signed areas exclude zero, and the reported crossed-face table is reproduced. These extras corroborate nondegeneracy but are unnecessary for the basic existence theorem.

Limiting/edge checks: alpha2 gives two linear distance-difference equations with a unique solution for noncollinear foci, so the five-root argument is specific to the higher power. Collinear foci would invalidate the inversion and are explicitly excluded here. Zero radicands have a nonnegative branch; no used radicand or denominator approaches an uncontrolled sign boundary. The remote root's proximity to its circumcenter limit is not a collapsed face. Parameter-varying or universal statements were not inferred.

## Code, certificate and historical replay

The primary verifier uses only the standard library, embeds the geometric constants, and reads only its sibling certificate on default execution. Its grid-root proof is valid: the integer floor target and direct eighth-power comparisons imply lower^8<=q<=upper^8. Interval addition, negation, multiplication, square, nonnegative eighth power and reciprocal correctly enclose the fixed inputs; repeated dependencies merely widen bounds. Boundary and outgoing bisections retain strict opposite endpoint signs and reject unresolved midpoint signs. The divisions exclude zero and all asserted domain conditions hold.

The default owned run reproduces the full recorded JSON certificate and the outer stdout byte for byte. A profile independently counts17472 successful require returns, dominated by repeated interval/root implementation checks; it does not count independent mathematical propositions. A run from a read-only owned directory with read-only inputs, under Python -O, still passes and changes no file hashes. The final verifier uses explicit require exceptions, so optimization does not remove its checks.

After inspecting every historical script before execution, all three prior independent mathematical implementations replay successfully in private owned extraction. Algebra and exact-reproduction certificates match byte for byte; source/geometry data match exactly after excluding the intentionally fresh UTC field. The original submitted replay reproduces6987 successful verify calls. Its wrapper correctly requires ordinary Python with assertions enabled. Historical10^17 cutpoints remain explicit in the old records, while the final note, primary verifier and certificate consistently use10^16. The archive README explains the distinction and the algebra audit independently derived10^16.

The historical comparison helper's dependency on a sibling original_submission tree is expressly documented; the primary read-only verifier is fully self-contained with its sibling certificate and requires none of the historical dependencies or primary PDFs. Archived reports are supporting evidence, not premises of this review.

## Entire package and archive integrity

`INPUT_INTEGRITY.json` records all15 frozen-file identities. Exact allowed membership, every seal byte count and hash, and the prescribed package-seal hash pass. The ZIP contains64 unique safe relative filenames, no duplicate/path-traversal entries, and exactly matches all64 outer inventory records. Its internal self-excluded manifest authenticates all63 other members. All nested audit manifests and source-plan/source-target seals authenticate; all144 excluded-private-source hash references match the locally retained evidence.

The ZIP's paper PDF/TeX, primary verifier/certificate, README, license, reference metadata and verification stdout match the outer files byte for byte. Inner zenodo-metadata.json equals the exact metadata object in outer zenodo-deposit.json. LOCAL_DEPOSIT_CHECK's three file sizes/hashes match. All JSON parses, text members decode, and Python sources compile. Source inspection and archive enumeration show no primary-source PDF body, OCR/extracted body, render, raw API/service response, credentials or unrelated work in the ZIP.

All six final PDF pages were rendered and visually inspected: equations, rational sign table, scope, bibliography and disclosures are present and legible, without clipping or overlap. The PDF text agrees with the TeX's scientific content; TeX alone is not being treated as proof of its rendering.

The title, author, supplied ORCID, date, CC BY4.0 license, preprint resource type and three intended deposit files are mutually consistent. Extensive AI assistance and unrefereed/no conventional human peer review status appear in the note, README, archive explanation and intended metadata. Existing false publication-ready/review-complete flags correctly identify this as a frozen prepublication review target; they are not scientific defects or evidence that publication has occurred.

## Earlier families, bibliography and historical wording

I independently inspected and rendered Ash–Bolker's primary equations1.6–1.8 (pp209–210), pure t^4 discussion(p241), and separate t+k sin(t) example(pp241–242). The weighted family predates this construction; generic vertex valence does not count distinct intersections for one fixed triple, and a nonpower oscillatory cost does not establish a pure-power counterexample.

Bourne–Peletier–Roper's primary Definition4.12 in the author manuscript explicitly uses |X-x_i|^p-w_i. Bourne–Roper's primary manuscript Section5,p24 repeats it; its earlier arXiv manuscript independently confirms the reference metadata's Section1.7 locator: https://arxiv.org/pdf/1409.2786 . With p16 and weights(0,27/1250,1), equality of the three costs is exactly this note's two powered equations. No new curve-family claim survives or is made. Bibliographic titles/authors/years/pages agree with the inspected primary copies and the available Crossref DOI registrations. Two live Crossref requests were rate-limited; no absence inference is made from that.

I read the packaged priority report, source matrix, query matrix and access limitations. They support a bounded documented search, not a proof of no unknown literature. Saved public PR metadata and both candidate-body hashes match the dissemination record, while its caveats correctly withhold earliest-visibility, outside-awareness, human-review and firstness claims. The manuscript/README/metadata consistently say historical priority is unestablished. This is the authorized qualified-note route; proof of unknown-literature absence is neither possible nor required for it.

## Issues, remaining gaps and safe handoff

Substantive issue counts: critical0; major0; moderate0. No repair is required for the reviewed claims or package. No hidden math premise, circularity, fixed-versus-interval quantifier substitution, float sign decision, proper-embedding overclaim, mislabeled endpoint, package mismatch, or unconditional historical-priority assertion was found.

The exact total center count, a universal maximum, proper-embedding multiplicity, other alpha values and historical firstness remain unproved; the package already states these limits. This review does not independently rerun every historical search query or reverify every theorem in every cited paper. It independently checks the exact target, the three closest older families and the bounded-evidence interpretation needed by the published note. Future unindexed literature can alter priority without altering this exact mathematical witness.

Only SAFE_ALLOWLIST.json entries in this review folder may be integrated. SHA256_MANIFEST.json authenticates all other safe entries and excludes itself. All safe files are sealed read-only. private_work/**, all primary PDFs/text/OCR/renders, extracted ZIP working copies, raw API responses and rerun working products are excluded. To replay my checkers, copy the allowlisted files to a writable review folder beside a copy of publication_package_v2 and use ordinary Python with assertions enabled. The scripts write only their owned result files.

No publication or merge was performed. One new whole-package adversary has completed; any human-required further fresh review and final publication decision remain with the parent workflow.
