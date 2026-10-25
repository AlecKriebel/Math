# COMPLETE — adversarial review of actual published record 23440119

**Verdict:** no substantive mathematical defect found. The actual five-page paper supplies a checkable proof of Theorem 1 at precisely its stated one-sided, three-dimensional, third-derivative-curvature scope. No repair or scope weakening is required by this review. Follow-up recommendation: **null**. This is an independent AI review, not human peer review, a worldwide priority certificate, proof-assistant certification, or promotion clearance. The parent must read the complete actual paper and review reports before any promotion decision.

## Custody and independence

- Published record: DOI `10.5281/zenodo.23440119`; version `1.0.0`; 17 October 2026; title *A negative-curvature normal barrier on an algebraic cone that is not a hyperbolicity cone*.
- Actual fresh PDF: `sources/negative-curvature-cone.pdf`, 73,062 bytes, SHA256 `ad9864c08642737e4459673749c1db6d2e3dafb521f323fb1071f157f8110eb0`. Intake fetched the Zenodo content at 2026-10-25T05:22:37.446838Z; its checksum matches the API, queue, starting local PDF, and embedded supplement PDF. This review is bound to these fresh published bytes.
- Actual fresh support ZIP: `sources/negative-curvature-cone-source-and-verification.zip`, 134,250 bytes, SHA256 `d97ba7ed1057518e3bd499d88182c64767e912d589ed8574092c0ebc7a27c06e`; fetched at 2026-10-25T05:22:38.577532Z. All 26 extracted members were inventoried. Every one of the 25 entries in its internal source manifest matches its declared byte count and SHA256.
- Initial independence seal: `independent-seal.json`, 2026-10-25T05:24:49.339840Z. Before that timestamp I had read the entire actual paper, acquisition metadata, and workspace instructions, and had written and run only my own checker. No submitted supplement, checker, prior favorable audit/verdict, historical proof, or other current reviewer opinion was consulted. The sealed assessment SHA256 is `d450d799094be30170799b8d21f8a5970ab3f81032eb934b05392ccee2a74068`.
- The sealed independent artifacts remain unmodified. The later support and primary-source inspections are explicitly subsequent evidence; they do not retroactively constitute the independent first-pass reasoning.

## Claim and adversarial result

The hypothesis reviewed is the exact conjunction for

`K={(x,y,z)>=0: xy^2>=z^3}`, `F=-25 log(z(xy^2-z^3))`:

1. K is a closed, pointed, full-dimensional algebraic convex cone.
2. F on the complete interior of K is a parameter-100 normal barrier, meaning a logarithmically homogeneous self-concordant barrier, with the gradient bound also checked.
3. For all interior base points a, all h in the **closed** cone K, and all real u, `D^3F(a)[h,u,u]<=0`.
4. No homogeneous polynomial in the original R^3 has K as its hyperbolicity cone.

The independent mechanism starts from the raw polynomial tensor of `p=xy^2-z^3`; it reconstructs the curvature numerator and attacks its boundary cases with exact arithmetic. The universal sign reasoning uses discriminants of the two quadratic-in-s minor factors, a different algebraic presentation from the paper's square identities. The complete derivations and construction checks are in the sealed `independent-assessment.md`.

The original tensor verifies every printed matrix entry and leading-minor identity. The discriminants are

`disc_s P=-3(t-1)^2(8t^3+21t^2+6t-11)`,

`disc_s(R/(t+2))=-3(t-1)^3(8t^2+13t+3)`.

For t>1 both are negative, with positive quadratic leading coefficients; for 0<=t<1 the direct coefficients have the required nonnegative signs and positive constant term; at t=1 both factors equal `6s^2`. Thus the universal positivity is proved, rather than sampled. At t=1 the matrix has a positive definite lower block and kernel R e_x. At e_x it has the explicit positive semidefinite Gram form, with kernel R(1,1,1). h=0, t=0, the flat facet, h_y=0, and approaching an interior base toward every finite boundary stratum are accounted for. The fixed diagonal normalization and nonnegative direction decomposition are valid. s=0 and t<0 are outside the respective base and direction domains and introduce no missing case.

The self-concordance identities, mixed polarization, weighted Cauchy bound, factor 25, degree-four homogeneity, exact dual gradient norm 100, boundary blow-up, and extended closedness all check. The Hessian rank-one formula for the weighted geometric mean establishes cone convexity. No optimality of the barrier parameter is claimed or needed.

For the all-polynomial exclusion, the curved boundary is genuinely a topological boundary patch. Vanishing of any proposed H there forces `p|H` by the rational substitution identity and Gauss's lemma. Every possible interior hyperbolicity direction e gives the same nonreal-root obstruction: with `a=(e_x e_y^2)^(1/3)>b=e_z>0`, `p((0,0,1)+te)` has a quadratic factor of discriminant `-3a^2`. H(e)>0 makes the restricted product nonzero, so those roots cannot cancel. This excludes arbitrary degrees and polynomial factors. Reversing t changes no real-rootedness conclusion. No assertion about projections or higher-dimensional lifts is made.

The review also produced an exact falsification control for the tempting omission of `-log z`: at q=(5,1,1), h=(8,1,2), and u=(-10,-10,7), `D^3[-log p](q)[h,u,u]=13/8>0`. The actual barrier avoids that failure. The condition is third-derivative matrix negativity; neither the paper nor the verified conclusion asserts nonpositive sectional curvature of a Hessian Riemannian metric.

## Reproduction and submitted-code audit

The independent standard-library checker was authored before support inspection. It passed 1,591 assertions, including exact symbolic tensor/minor/discriminant identities, 80 rational normalized cases extending to s=10^-12 and 10^12 and either side of t=1, plus 500 generic exact base/direction and mixed-self-concordance cases. Its rational samples are supplemental to the universal proof.

After the initial seal I read **both complete submitted Python files** (176 and 149 lines) before running them. They import only standard-library arithmetic, iteration, JSON/runtime metadata, and time. Their inspected top-level behavior has no file, network, subprocess, deployment, or other external effect. I copied their exact bytes into this review's private `quarantine/`, verified SHA256 identity, and ran copies only, with Python `-I -B`, a private working directory, and captured output. No submitted code was patched or repaired.

- `check_geometry.py`: SHA256 `0300a189e13c87f3d295df9f8be375c919851f7243f9e8e3a11436bb9bd9d970`; normal and optimized runs each passed 791 explicit checks, including eight adverse controls, with empty stderr.
- `curvature_reproduction.py`: SHA256 `f2887da4e1f1821691d9d1a27ee21f7794e78eadea4ec5f41ee004d2b003cdc0`; normal run reproduced its identities, 45 rational cases, and 315 independent logarithm-series contractions. Optimized Python correctly failed at startup with zero stdout because its assertions would otherwise be disabled.
- Every stable result matches the published `expected_results.json` after omitting only the documented runtime timestamp/version/optimization fields. Full execution evidence is in `submitted-execution.json` and captured stdout/stderr files.

A submitted checker PASS is evidence of reproduction, **not a proof of the theorem**. The theorem is supported by the analytic argument and the independently checked identities and sign logic above.

## Full support read and historical deltas

After sealing I read the complete actual `main.tex` and README, provenance and manifest, all human mathematical/priority reports and ledgers in the published ZIP, and both complete verification programs. The remaining JSON metadata/results were parsed in full, their structure and counts inspected, and stable outputs compared. `support-read-manifest.json` records exact read extent and identity for each of the 26 members. The embedded PDF is byte-identical to the actual published PDF.

For the historical delta, I then read the complete locally frozen provenance proof and mathematical audit. The proof has the exact declared SHA256 `9577476ee2c0fd2e3d12ab1265201d8b99f6ef50a9060e245c46f872dd673302` at the pinned source head `148130ab93ab46a3459d7bc98a11a1ca79052d65`. The five-page paper retains the same cone/barrier, mixed self-concordance bridge, endpoint Gram form, minor identities, and arbitrary-polynomial obstruction. The published exposition adds explicit Roy–Xiao attribution, a sharper explanation of scope and definitions, the omission negative control, and newly distributed reproducible checkers/audits. The historical proof-only edition's statement that old executables were not distributed is not a defect of this new package. Its historical run claims were not used as current proof or current execution evidence. No historical acceptance verdict substitutes for this review.

## Primary dependencies, read extent, and limits

Fresh primary PDFs were obtained by intake from official/author sources. I checked their actual central statements, with relevant pages rendered and visually inspected. The authored `primary-read-ledger.json` preserves URLs, retrieval times, exact hashes and read extents; third-party full texts and extracts remain local and ignored.

- Official Oberwolfach report, printed 797–800: the target contribution, root convention, definition, and exact existential Open Problem 1 agree with the paper. Physical page 29 / printed 799 was visually read.
- Nesterov–Tunçel arXiv:1412.1857v1: scalar self-concordance and gradient bound near p3; regularity/normality and logarithmic homogeneity on p4; §6 negative curvature on pp17–18. The normality and sign conventions used in the manuscript match.
- Dahl–Tunçel–Vandenberghe arXiv:2509.10263v2: §2.2 matrix self-concordance, §3.1 Definition 3.1 directional-gradient concavity, and §6 broader existence question. The manuscript proves the mixed condition directly and correctly separates the universal question from the 2017 existential question. I used the PDF definitions; its known internal date difference from HTML is not mathematically consequential here.
- Hildebrand arXiv:1305.4814v1, Theorem 3.2 and family list on pp4–5: the exact cone is already family 5 with p=3, q=3/2 and coordinates (x,z,y), as credited. Hyperbolic affine-sphere terminology supplies no exception to the polynomial argument.
- Roy–Xiao, original 2018 PDF, introduction/definitions and Theorem 2 on pp1–3: the exact prior parameter-3 barrier and nonnegative cone formula agree with the attribution. That theorem is about self-concordance, and is not being used to infer the additional curvature property.

No central mathematical dependency gap remains in this bounded review. These sources were read at the stated central statements, not all cover-to-cover. This is not a new worldwide priority search; no exhaustive absence, first-ever, or present-day openness claim is made. The paper itself makes those limitations clear. No high-value follow-up clearing the requested very high bar was established: **null**.

## Preservation and completion

All writes are confined to `papers/23440119/reviews/adversarial`. The sealed core, actual fresh sources, existing proofs/audits, source code, shared scripts/configuration, catalogue, Sheet, main branch, remotes, website, GitHub releases and DOI record were preserved. No external individual was contacted and no outreach was prepared. No child agents, Git actions, releases, deployment or external mutations were performed. Submitted code was run only as byte-identical quarantined copies with the inspected behavior described above.

Assigned review completion: **100%**. That is task completion, not a probability of correctness. Strongest verified result: the complete Theorem 1 at the actual published scope. Exact remaining mathematical gap found: none. Remaining global limitations are ordinary non-formal-verification and bounded literature coverage; the parent retains the promotion decision after full reading.
