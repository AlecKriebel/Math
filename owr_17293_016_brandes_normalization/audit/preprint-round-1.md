# Fresh preprint-readiness review, round 1

Checkpoint: 2026-09-23 13:34 UTC. Best-guess completion: **100% of this bounded review**. This percentage describes completion of the assigned checks, not certainty of correctness or probability of novelty.

## Verdict and independence

**No actionable findings.** No correction to the manuscript, proof, verifier, or reviewed public descriptions is requested. No counterexample or unsupported step in the stated theorem was found. This is an internal AI-assisted review, not external peer review or a guarantee of correctness, originality, or acceptance.

The first substantive file read was `manuscript/paper.tex`. The sphere-minimum calculation, Taylor coefficient, common-parameter step, normalization, and boundary cases were independently checked before consulting any previous audit report. A provisional clean mathematical verdict was sent to the parent reviewer before reading `audit/independent-geometry.md`; that later read checked the package's claim that it contains a second proof. No previous adversarial verdict, final manuscript review, source-match report, verification report, or priority audit was consulted. Public README and website descriptions were examined only after the independent mathematical derivation.

Scope: readiness to circulate this precisely stated result as an unrefereed preprint. A fresh exhaustive priority search, journal suitability, and new results beyond the theorem were outside the assignment. Only this report was written; no manuscript edits, publication actions, commits, pushes, or communications with other individuals were performed.

## Claim and independent proof checks

The reviewed claim is for a real homogeneous polynomial of positive degree on R^m, with m >= 1 and strict positivity away from zero. The requested matrix is any element of GL_m(R). The entries are those of the unique symmetric multilinear polarization, with the ordinary monomial coefficient divided by its multinomial multiplicity.

1. **Degree and minimum.** Homogeneity gives p(-x)=(-1)^d p(x); strict positivity forces d even. The stated positive-degree hypothesis therefore gives d >= 2. Compactness of the unit sphere gives a positive attained minimum c. After dividing by c, homogeneity supplies p(x) >= ||x||^d globally, including x=0. No convexity assumption is needed.
2. **Derivatives at the minimizing direction.** For tangent u, comparison with (1+t^2||u||^2)^(d/2) gives first derivative zero and second derivative nonnegative at t=0. Direct differentiation yields d A(v^(d-1),u)=0 and d(d-1)Q(u,u)-d||u||^2 >= 0. Thus the tangent slice is strictly positive on every nonzero tangent vector, even when the sphere minimum is not isolated.
3. **Independent leading-sign calculation.** Write a_r=w_(j_r), and, near zero where the numerator is positive, define R_J=N_J/(product_r p(v+epsilon a_r))^(1/d). Expansion of its logarithm gives

   log R_J = epsilon^2 [sum_(r<s) Q(a_r,a_s) - (d-1)/2 sum_r Q(a_r,a_r)] + O(epsilon^3)

   = -(epsilon^2/2) sum_(r<s) Q(a_r-a_s,a_r-a_s) + O(epsilon^3).

   This independently checks the manuscript's sign and factor in F_J: its quadratic coefficient is (d/2) times the same pair-difference sum. Distinct basis labels have distinct w_i, including w_m=0, so every mixed tuple has a strictly positive sum. For pure tuples the polynomial gap is identically zero.
4. **Remainders and one epsilon.** The displayed quantities are finite-degree polynomials. For each mixed J the remainder divided by epsilon^2 tends to zero, so strict positivity holds throughout a punctured interval. Intersecting these finitely many intervals gives one positive epsilon. A second finite intersection ensures N_J>0, since N_J(0)=1. There is no demand for an estimate uniform over all dimensions, degrees, or forms, nor an interchange of infinite limits.
5. **Basis and scaling.** Tangential projection proves independence for every nonzero epsilon. Restoring p and A multiplies both sides of the unnormalized inequality by c: the product contains exactly d factors, each raised to 1/d. Positive column rescaling by p(x_i)^(-1/d) then gives diagonal one and preserves the determinant's nonvanishing. The columns of S implement p(St), so the coefficient transformation uses the correct orientation.
6. **Boundary cases.** For m=1 the tangent basis is empty, x_1=v is nonzero, and all mixed assertions are vacuous. For d=2, Q=A and the omitted higher-order terms in individual expansions may vanish; the gap argument and positivity still work. An even d allows the powered inequality to recover the absolute-value bound; the separately established numerator positivity yields the stronger positive-entry statement.
7. **Rational-density remark.** For the unnormalized matrix, nonzero determinant, positive entries, and strict mixed upper inequalities form a finite intersection of open conditions. Pure equality is an identity, not an extra closed condition that obstructs density. A nearby rational matrix therefore works. The text correctly declines to assert rationality after unit-diagonal rescaling.

The fixed-coordinate example has ordinary x^2 y^2 coefficient 12 and ordered entry 12/6=2, so it correctly illustrates failure before changing coordinates. The proof does not purport to handle degree zero, merely nonnegative forms, or integral unimodular transformations.

## Authentication and antecedent

Independently opened the [EMS publisher report](https://ems.press/content/serial-article-files/46829) and located Brandes's Problem 11 at printed page 3182, PDF page 42. Its displayed polynomial is indexed by tuples (j_1,...,j_d), and its inequality places absolute values around both the mixed entry and the diagonal product. The cached page image was inspected visually, and its text agrees with the publisher extraction. The report imposes no orthogonality, determinant-size, conditioning, or integrality restriction on the linear change.

The report does not separately spell out permutation symmetry. The manuscript supplies the canonical symmetric ordered convention explicitly; it does not silently substitute ordinary monomial coefficients. This qualification is essential and is already present in the statement and public result section.

The [2015 antecedent, arXiv version 2](https://arxiv.org/pdf/1506.05343), was checked at its introduction and Lemma 2.1. The lemma proves the quadratic matrix-entry inequality by testing a positive definite matrix on vectors supported on two coordinates. Its earlier discussion indexes polynomial terms disregarding order, so its notation must not be imported without tracking multiplicities. The manuscript avoids that problem: it credits the earlier pseudo-diagonal discussion and quadratic lemma while defining its own coefficient convention. No unsupported claim of a general earlier result is made.

## Verification, second proof, and circulation artifacts

- Read `verification/verify.py` and `verification/adversarial_checks.py`. Matrix substitution, division by multinomial multiplicity, enumeration of every coefficient class (including missing coefficients), determinant calculation, and exact powered inequalities are consistent with the theorem. The polarization cross-check uses inclusion-exclusion rather than the substitution routine.
- Ran both scripts successfully. The first produced 12 certificates, 120 coefficient classes, 110 polarization cross-checks, identity checks in degrees 2 through 24, and two expected rejections. The second produced 500 independent determinant comparisons and 20 direct-polarization comparisons. Parsed outputs equal their respective checked-in result JSON files.
- The supplied nonconvex quartic is positive because it is (x^2-y^2)^2+x^2 y^2, with simultaneous vanishing only at the origin; its Hessian at (1,0) has a negative y-direction entry, confirming the nonconvex label. The radial examples and the positive-coefficient quartic have the stated elementary positivity certificates.
- After the independent verdict, checked the separate geometric proof's positive definite slice, joint-continuity cone argument, Cauchy-Schwarz inequality, and finite maximum propagation. Choosing a maximizing multiplicity vector with maximal sum of squares correctly forces a pure tuple. Strict Cauchy-Schwarz handles a nonproportional pair. No circular use of the target inequality was found.
- Extracted text from all three current PDF pages and inspected all three existing final-page images. The statement, formulas, citations, and disclosure are legible, with no missing symbols or clipped content observed. The parent reviewer separately reported that a fresh compilation's extracted text matches the published PDF.
- Read the README, local website, citation file, license text, Zenodo metadata and instructions, and package builder. They distinguish finite computations from the analytic proof, identify the work as unrefereed and AI-assisted, and limit the priority claim to a bounded search. The exact scope is discoverable alongside the headline summary.
- Tested the existing source ZIP for corruption: none found. Its core manuscript, PDF, scripts, result files, README, website source, and builder agree byte-for-byte with the reviewed live files. The parent is updating the research log and rebuilding manifests as part of the active review cycle; that expected ongoing change is not a finding against the reviewed paper.

The web tool could not fetch the public project-page URL, so this review does not independently certify live deployment availability. The DOI endpoint for the 2015 paper returned a tool-visible 403; the accessible author preprint supplied the relevant antecedent text. These retrieval limitations do not affect the mathematical checks. The bounded priority-search claim was checked for appropriate qualification, not independently re-proved by a new comprehensive literature search.

## Reviewed SHA-256 identifiers

Hashes were taken from the reviewed bytes on 2026-09-23; the manuscript and PDF remained unchanged throughout this review.

| File | SHA-256 |
| --- | --- |
| manuscript/paper.tex | 317ab083bdfc4e986921e517b368de8e1501c7f9a24b4faef5b047fe1d504f43 |
| output/pdf/paper.pdf | a84cfe9347d3d0ce05ef0fb22e8648ee64fd77992825729d24991cf0fc1d627d |
| sources/owr-2019-50.pdf | 549b3c1ecb3abb2a970f622e499b1b5aac23a02f4c73567408dfd8c457aff021 |
| verification/verify.py | f1d0b9755c3dab689878c0e8af758ea3f5e58ebcc86eb36afaed5f67b67dc82f |
| verification/adversarial_checks.py | 57bb78a8dfed31f909b28c94ffa5f118cd73df8e01e1214cf1c47a2d3f56d9e9 |
| verification/README.md | 1abf57ba6855ab17c0b2d08f399a8b1f82bf3121f36c9221ca321c76a395e4c0 |
| verification/results.json | c11f125a269e89d271a14e3680314bbf8d0095c57a83e5881e4b1ea42532bafa |
| verification/adversarial_results.json | 6b71e0e9e98b58d7dc5f4e11dd59c8bdcfab3984b73c5c327705e785124b18f3 |
| audit/independent-geometry.md | a9d13998e41de80c3197dd019a78906244dc74b243c9feeb73e0ea8d8896b6e3 |
| README.md | 9188a012ef709de177923c2991dde4ea8a42399f34ef0856c550559b82227d6b |
| site/index.html | 24bd01d199cc47d81970b0039d87ee2abd045318a086732aca30f6ba356fc24b |
| CITATION.cff | c48c92dfd64fe85e4e123578782af095300cd55f3b8ae26056daa3c5d0f144bf |
| LICENSES.md | 0680b059b3c8a6613f51a718ac6b3f48bbd6401f948ad3db461d1515b57f4d59 |
| zenodo/metadata.json | f116e7acd26ca0afe0d49df7d804d4877a9f2b310bde3b747f992121b1648519 |
| zenodo/UPLOAD.md | f6c70b27761b31fbc60ebd3773b47ba191c9694cf8f051fb728f177197b093b9 |
| build_package.py | 3f0a2f609d9314390a1e2fb2a3aeff70c0db71cd62b722cf399953117da92ae0 |
| zenodo/source-and-verification.zip | 9068952327aa9f695d750c477334f6fbdcdb1f192a8bc480c13b03c5fc8ea3c8 |

Strongest checked result: the stated basis-existence theorem, including positive strict mixed bounds, under its explicit hypotheses. Exact remaining mathematical gap identified by this review: **none**. Actionable findings by severity: **none**. Proposed minimal fixes: **none**.
