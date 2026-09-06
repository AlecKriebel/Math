# Independent full referee report

**Paper:** Maximally collective stable Turing patterns in binary-complex mass-action networks.

**Author:** Alec Kriebel, ORCID <https://orcid.org/0009-0001-9320-500X>.

**Audited version:** commit `6f68ad3e795c239e452206c84ce4ce331386a094`, preserved before testing.

**Date:** 2026-09-05 America/Los_Angeles / 2026-09-06 UTC.

**Recommendation:** **Minor revision; hold submission pending the corrections and checks below.**

I found no false central theorem or unresolved substantive gap in the all-dimensional algebraic and nonlinear PDE constructions. The main conclusions survived independent reaction-derived calculations, structural proof reconstruction, endpoint challenges, and cross-review. This is a substantially stronger conclusion than a successful run of the supplied tests alone.

The package is nevertheless **not ready to submit as it stands**. There is a reproducible certificate-reader defect, genuinely overlapping supplement table entries, two inaccurate sentences in a determinant proof, incomplete checkability of a true secondary example, and a literature-comparison row that understates prior numerical results. The manuscript also describes an uncreated version tag as already frozen. Author declarations remain pending. Finally, this audit could not finish fresh pinned TeX builds and the full portable replay because of local storage exhaustion. Prior successful builds do not count as fresh passes in this report.

No manuscript, mathematical certificate, supplied PDF, tag or release was changed by this audit. Its findings and independent evidence are separate research artifacts. This is author-requested pre-submission assistance, not an official SIAM journal referee decision.

## 1. Scope and independence

The root reviewer read the full canonical manuscript and supplement source, examined all 94 supplied PDF pages, inspected load-bearing verification code, checked current journal instructions and relevant primary literature, and integrated three independent review lines. Algebra and PDE reviewers reconstructed their assigned arguments before seeing earlier referee verdicts. The software reviewer executed preserved copies and challenged failure behavior. After their initial work, the algebra and PDE reviewers cross-checked each other's new findings; the algebra reviewer independently repeated the near-threshold calculation and visually confirmed the table defect.

Both referenced prior tasks were read for context: **Turing Referee** and **Revise Turing patterns manuscript**. Their pass statements were treated as historical claims requiring fresh evidence, not assumptions.

The snapshot came from `git archive` of the target commit's project subtree. Its archive SHA-256 is `98fbd863a4b953656d2c94efbcb3e723c918e20d11bb6d79d6c49bed2012da58`; [SOURCE_INVENTORY.json](SOURCE_INVENTORY.json) records every archived file. The tracked manifest contains 1,108 entries matching that 1,109-file archive, with the manifest itself excluded as designed. Later repository commits or this new audit folder do not retroactively belong to the target version.

Detailed evidence is preserved in the [algebra report](algebra/ALGEBRA_REPORT.md), [PDE report](pde/PDE_REPORT.md), [software report](software/SOFTWARE_REPORT.md), [adversarial cross-review](algebra/CROSS_REVIEW.md), [document review](documents/DOCUMENT_REVIEW.md), and [literature review](documents/LITERATURE_REVIEW.md). Finite regression checks and floating-point probes are explicitly distinguished from proofs for all dimensions and continuous parameters.

## 2. Corrections needed before submission

### R1 — Certificate reader accepts undeclared terms and order-dependent duplicates

**Priority:** substantive verifier repair; no counterexample to the shipped mathematical result.

**Location:** `independent_verifier/frontier_verify_mode_certificates.py:185–218`, particularly lines 193–201 and 210–218. A corresponding expected-key-only comparison occurs in the exposition verifier's spatial table logic.

The verifier converts declared terms to a dictionary and checks only the monomials it independently expects. It compares the declared `term_count` to the expected polynomial's term count, but does not require that the actual input terms have exactly that support or that their monomials are unique.

A counterexample appends a term with powers `[99,99]` and coefficient `-1` to the homogeneous certificate, and powers `[99,99,99]` and coefficient `-1` to the spatial certificate, leaving declared counts 22 and 84 unchanged. These polynomials differ from the intended certificates and become negative for sufficiently large positive variables. The direct verifier still exits zero with `VERIFY_MODE_CERTIFICATES_PASS`. Prepending an opposite-sign duplicate also passes because the later genuine row overwrites it; putting the duplicate last rejects. This is not harmless extra descriptive metadata: the mutation is inside the actual polynomial term lists.

The **minimal symbolic aggregate also accepts the added negative terms**, ending with `ALL_SYMBOLIC_CERTIFICATES_PASS`. In the full source tree, generated-table freshness detects the mutation when the printed table is left unchanged; the fixed portable manifest detects changed bytes before computation. These enclosing protections limit the defect but do not repair the standalone/minimal certificate reader. The unit-profile checker at `verify_mode_isolation.py:27–45` also accepts identical positive duplicate rows because its set comparison collapses them. The authentic shipped coefficients were independently regenerated and are correct.

**Required repair:** reject duplicate monomials; require exact equality of actual and expected monomial sets; check actual row count as well as declared count; retain exact coefficient comparisons. Add negative controls for added terms, missing terms, and duplicates in both orders. Apply this to each distributed copy through its generator/build process, and rerun the minimal aggregate as well as full-package checks. General rejection of unknown metadata fields is not requested.

**Evidence:** [certificate_containment.py](software/certificate_containment.py), the mutant JSONs under `software/mutation_artifacts/`, and recorded exit/output evidence in the software report and logs. The root reviewer separately reproduced direct/minimal false acceptance using [check_certificate_reader.py](check_certificate_reader.py); see [ROOT_CERTIFICATE_READER_WITNESS.json](ROOT_CERTIFICATE_READER_WITNESS.json).

### R2 — Certificate fractions visibly touch or overprint in the supplement

**Priority:** required presentation correction.

**Location:** generated `data/certificate_tables.tex`, especially the 77-term and 84-term tables; `computation/generate_tables.py:37–49` supplies ordinary unpadded rows.

The defect occurs in canonical supplement pp. 12–15 and journal supplement pp. 14–19. A precise witness is journal supplement p. 15: the denominator `91125` of `160888/91125` touches the following numerator `4420871` of `4420871/182250`. Their extracted text boxes overlap vertically by 1.512865 points and overlap horizontally. Enlarged raster inspection by two reviewers confirms actual loss of row separation, rather than a bounding-box artifact.

**Required repair:** increase table row height/spacing in the generator or a scoped table style, or use a legible single-line rational convention. Regenerate and rebuild both supplements, inspect all affected pages, and refresh dependent archives/hashes. No coefficient changes are needed. Passing semantic PDF text comparisons does not establish table legibility.

**Evidence:** [DOCUMENT_REVIEW.md](documents/DOCUMENT_REVIEW.md), [TABLE_SPACING_WITNESS.json](documents/TABLE_SPACING_WITNESS.json), and [check_table_spacing.py](documents/check_table_spacing.py).

### R3 — Correct two local determinant-proof sentences

**Priority:** minor mathematical exposition.

**Locations:** `manuscript/main.tex:485–490`; `manuscript/supplement.tex:188–190`.

First, the core determinant proof says “two surviving cycle covers.” At the included case m=3, a=b=1, all six permutation terms are nonzero: −10, +8, +5, −2, +2, −1, summing to 2. Replace the inaccurate count with a reference to the already valid Schur-complement calculation in Supplement S2, or give a correct explicit computation.

Second, the stated order of both retained chain fragments followed by the boundary triad is not block triangular for a general interior omission. For m=5, omitting X3 gives arrows X4 → triad → X2. Put the triad between the two fragments, or simply invoke an appropriate Frobenius permutation. The determinant factors and their signs remain unchanged.

These are two independently confirmed errors in the written argument, with existing local repairs. They do not invalidate the localization or diffusion-law theorems. Exact matrices and contributions are in [exposition_counterexamples.json](algebra/exposition_counterexamples.json).

### R4 — Expose the derivation and onset checks for the secondary subcritical example

**Priority:** minor checkability addition.

**Location:** Supplement S9, `supplement.tex:947–954`, and `independent_verifier/frontier_verify_near_threshold.py` (also reached through its wrapper).

The supplied verifier starts from a hardcoded rational cubic. Its checks do not derive that expression from the printed reaction system or establish the simple critical mode and stable complementary spectrum needed to call the example a primary subcritical bifurcation.

The claim itself is **true**. Two independently implemented reaction/Hessian calculations reproduce the exact cubic, including `6/1379 + (421985/11409846) epsilon + O(epsilon^2)`. Exact rational coefficient certificates establish positive diffusivities, a simple transverse zero at damping t=1, a Hurwitz complement, and stability for every t>1 throughout `0<epsilon<=1/1000`.

**Required addition:** incorporate a reaction-derived cubic reconstruction and a brief explanation/check of these linear hypotheses into the public verifier and supplement. The [PDE report](pde/PDE_REPORT.md) gives a concrete short paragraph. [near_threshold_independent.py](pde/near_threshold_independent.py) and [crosscheck_near_threshold.py](algebra/crosscheck_near_threshold.py) provide independently checkable implementations. This is a secondary-example evidence gap in the shipped presentation, not a missing central all-dimensional theorem.

### R5 — Make the final version reference and author declarations accurate

**Priority:** submission completion.

**Location:** `manuscript/main.tex:1250–1258`, supplementary index, and draft cover letter.

The source says the files “are frozen” at the v1.0.9 tag, but a live remote lookup finds no such tag or release. The previous v1.0.8 DOI is correctly identified as belonging to an earlier version; it does not identify the corrected current files.

Use a resolving immutable reference that actually contains the final corrected evidence. An existing exact commit permalink is one option; a deliberately created new release after validation is another. If a DOI is included, use only the DOI actually assigned. A new Zenodo DOI is not itself a SIADS submission requirement. No release should be made merely to give this review a positive checklist entry.

The human author must supply accurate funding, competing-interest and simultaneous-submission declarations and finalize the cover letter. This audit cannot infer these facts. The journal portal preview has not been checked.

### R6 — Credit prior numerical nonlinear and stable branches accurately

**Priority:** minor attribution correction.

**Location:** `literature/theorem_comparison.csv`, the Conradi–Mincheva–Uecker (2026) row.

The unqualified entries `Nonlinear branch=no` and `Stable branch=no` understate that paper's numerical continuation of nonlinear branches and stable segments. Its Section 4.3, Figure 3 discussion, explicitly reports a primary subcritical patterned branch that stabilizes after a fold. The underlying example also has binary-complex classical mass action. [Primary paper](https://arxiv.org/html/2605.16049v1).

**Required repair:** use entries such as “numerical continuation” and “numerically stable segments,” or explicitly define the columns as analytic existence/stability theorems and still acknowledge the numerical results. The main manuscript's narrower description is not false; it can usefully add this acknowledgment. The all-dimensional, all-realization localization theorem and exact stable contrast-scaling construction remain meaningful distinctions. See [NOVELTY_CROSSCHECK.md](pde/NOVELTY_CROSSCHECK.md).

## 3. Claim-by-claim mathematical assessment

| Claim in main source | Verified mechanism and conclusion | Boundary/scope retained |
|---|---|---|
| Propositions at lines 207 and 255: conservation, flux cone, complete realization | Reconstructed the polynomial field from reaction exponents, the semipositive conservation vector, rank m, the two positive flux parameters, and every Jacobian `J=A_m(a,b)H`. | Strictly positive rates and equilibria; m≥3 includes the empty chain. Semipositive conservation does not imply global boundedness. |
| Lemma 276 and Theorem 327: maximal all-spectrum localization | Exhaustive graph argument reduces every principal block below m to negative singletons, two stable long cycles, or stable boundary-triad principal blocks. Modulus bounds and exact triad Routh positivity prove Hurwitz stability. Core Schur elimination gives negative signed determinant and a positive real eigenvalue. | All positive a,b,H, including edge cancellation b=2a. The endpoint is m=n−1. R3 repairs literal proof wording. |
| Theorem 395: principal-minor diffusion ray | Principal-minor expansion gives `det(sD−J)=s q_D(s)` with all higher coefficients positive. Monotonicity gives the unique positive threshold exactly when the linear coefficient is negative; characteristic-polynomial monotonicity proves a simple zero and the exact positive-real-eigenvalue band. | The positive sum of order n−1 minors is used. Equality has no positive threshold. n=2 is included. This theorem alone does not exclude nonreal unstable eigenvalues at or away from the stationary threshold. |
| Proposition 461 and Theorem 519: omission minors and stationary law | Negative Z-omission, positive interior omissions and two zero omissions yield `d_Z > 8 h_Z sum_{j=2}^{m−1}(d_j/h_j)`. Homogeneous stability on c-perp makes the conservation zero simple and supplies the required coefficient sign. | Requires a homogeneously stable realization. The full stability region is not classified, and T(H)>1 is necessary rather than asserted sufficient. |
| Theorem 574: sharp contrasts | Exact fixed-H infimum T(H), unit-equilibrium infimum 8(m−2), and strict product bound `chi_D chi_H > 8(m−2)` follow from the stationary law. Explicit approaching profiles prove sharpness. | Infima are not attained. Sharp stationary onset does not by itself imply a stable patterned branch. |
| Theorem 643: unit-equilibrium stable design | A generic Schur identity connects the actual characteristic determinant to the modulus polynomials. Independently regenerated 35/77-term certificates and separate simplicity/transversality arguments control the full modal spectrum. The generic cubic recurrence and sign certificates give a negative cubic for every m. | Fixed m and a fixed Neumann interval; fixed integrated mass. Finite matrix checks only corroborate the all-dimensional identities. |
| Theorem 860: scaled stable trade-off | 22/84-term modulus certificates, the exceptional m=3 Routh calculation, the physically transformed mass gauge, and negative cubic prove the stated closed L interval. Exact contrast formulas yield exponent 1/2 and the within-family minimizer. | The corrected lower endpoint is essential; a broader cubic-sign interval is not a spectral interval. The square-root exponent is topology-specific. The global constant-optimal Pareto frontier remains open. |
| Local PDE stability in Sections 6–7 / S10–S11 | Fixed-mass Fourier Fredholm calculation gives index zero and the correct range condition. H1→L2 reaction smoothness in one dimension, sectoriality, compact resolvent, reflection symmetry, bounded multiplication perturbations and the high-frequency estimate justify the local reduction and exponential H1 stability. | Sufficiently small positive bifurcation parameter; positive nearby branches on the same affine mass class. No global attraction or dimension-uniform neighborhood. Nonconstant-branch modes need not remain decoupled. |
| Proposition 1109: robustness | Transport to a fixed interval and a simple-eigenvalue implicit-function argument retune one scalar diffusion multiplier. Cubic sign and complementary spectrum persist locally. | Fixed m,L and local perturbations within the positive-equilibrium realization manifold. Nearby unretuned points are not all critical. |
| S9: near-threshold subcritical control | Two independent exact reaction-derived calculations and entire-interval Routh certificates establish the printed claim. | m=3 and positive epsilon≤10^−3 only; no uniform epsilon→0 bifurcation neighborhood. Add the public derivation under R4. |

The nonlinear proof is not circular: the all-mode spectrum and simplicity are established before the harmonic inverses and Fredholm reduction; the cubic sign then determines the emerging center eigenvalue. High-frequency parabolic estimates plus finite spectral projection continuation justify complementary stability on the nonconstant branch.

## 4. Reproduction and falsification evidence

The algebra review independently checked 49 generic-parameter omission identities; 263,945 SCC classifications; 422 distinct SCC and 630 whole-subsystem exact Hurwitz cases; and 759 additional exact cases under extreme rational scaling. Reaction-derived identities, graph exhaustion and coefficient positivity carry the infinite quantifiers. These finite counts are not substituted for those proofs.

The PDE review regenerated all four principal modulus polynomials with 35, 77, 84 and 22 terms, including equality supports; reconstructed the generic boundary determinant and physical mass gauge; directly solved exact cubic contractions in selected dimensions; and ran 88 supplementary floating spectral probes. At a deliberately excluded older endpoint with m=149, a floating-point probe estimates a positive homogeneous spectral abscissa; the corresponding probe at the current certified endpoint passes. This supports retaining the present domain exactly.

Fresh execution of the unchanged shipped package produced:

| Check | This audit's outcome |
|---|---|
| Tracked manifest, public manifest and seven supplied bundle hashes/ZIP integrity | Pass. |
| All 39 ordinary verifier entrypoints | Pass. The count includes wrappers/overlapping checks, not 39 independent proofs. |
| All 39 optimized-Python rejection controls | Pass: reject optimization as intended. |
| Standalone test suite | **28 passed, 1 TeX-dependent test skipped.** Do not report 29 fresh passes. |
| Minimal verifier replay | Pass on the authentic package; R1 records false acceptance on malformed certificate terms. |
| Numerical/data regeneration | All 15 integrations, three Python figures, 13 baseline exact-artifact hashes and seven deterministic ZIP byte reconstructions passed. |
| Supplied canonical and journal PDF semantic audits | Pass; visual review nevertheless found R2. |
| Supplied PDF visual inspection | All 94 pages examined; R2 requires correction. |
| Actual pinned toolchain preflight | Eventually emitted `TOOLCHAIN_LOCK_PASS` and exited zero, with disk-exhaustion warnings during setup. This is not a document-build pass. |
| Fresh full portable replay including TeX; three detached source builds and their fresh rendered-text comparisons | **Not completed in this audit.** Host storage exhaustion prevented the complete build campaign. Controlled protocol stubs used for isolated lock/manifest negative controls are not actual TeX builds. |
| Historical top-level provenance replay | **Not completed.** Its five lineage archives were unavailable at the documented default location, and its base-host toolchain preflight failed. This does not affect the completed independent current-data reconstruction or the portable route, which does not require those archives. |

The [software report](software/SOFTWARE_REPORT.md) and command logs are authoritative for detailed exit codes, stage ordering and containment. The prior researcher's reported successful TeX campaign remains historical evidence. Repeat the missing fresh build stages on the corrected package with sufficient storage before claiming complete release reproducibility.

## 5. Novelty, positioning and journal presentation

The examined primary literature does not duplicate the combination of an explicit binary-complex classical mass-action family, maximum all-spectrum localization for every realization, exact topology-specific stationary contrast law, and all-dimensional stable nonlinear branches. The general relationship between unstable subsystems and Turing instability is established prior work and is appropriately treated as background. This is a focused novelty assessment, with access limits recorded in the [literature review](documents/LITERATURE_REVIEW.md), not a universal priority guarantee.

Three optional wording improvements would reduce avoidable ambiguity: make the homogeneous stability phrase at main lines 650–651 explicitly refer to the restricted Jacobian; state the fixed-interval stationary-bifurcation convention for “Turing,” without asserting intrinsic finite-wavelength selection; and replace “or equivalently” at line 1138 when relating an entire constant-optimal Pareto frontier to the scalar minimax infimum, since knowing one minimax value does not recover a whole frontier.

The 23-page SIADS main PDF uses the permitted alternative review layout, with 11-point type, a 6×8-inch text area, line numbers, keywords, MSC codes, embedded figures and a supplementary index. The current [SIADS author instructions](https://epubs.siam.org/journal/siads/instructions-for-authors) and [SIAM AI policy](https://epubs.siam.org/artificial-intelligence) were checked. The AI-use disclosure and single-author responsibility sentence are present. The supplied cover letter is explicitly still a draft. Apart from R2 and final version/declaration work, no new journal-format blocker was found in the supplied PDFs.

## 6. Readiness decision and closure conditions

My scientific recommendation is minor revision. I would not ask the author to change a theorem, topology, certified endpoint or numerical result on the basis of this review. I would ask for the concrete repairs R1–R6, preservation of the newly supplied S9 proof evidence, and a clean reproducibility run of the final corrected artifacts.

Submission readiness can be reassessed by checking the finite action list in [AUTHOR_ACTIONS.md](AUTHOR_ACTIONS.md). It does not require another open-ended rewrite. The unresolved validation gaps in this review are fresh pinned TeX/full portable/detached build completion and the separately documented historical lineage replay; the unresolved factual gap is the author's declarations. No claim of unconditional submission readiness is made.
