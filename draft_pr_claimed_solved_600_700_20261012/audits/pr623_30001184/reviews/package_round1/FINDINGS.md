# Whole-package adversarial review — round 1

**Verdict: PASS for the exact current package and final helper hashes. No mandatory corrections or optional findings.** This is an independent AI review, not human peer review and not authorization for remote actions. A fresh sequential whole-package review remains required by the parent's publication gate.

Scope is only claimed_solved PR623, problem 30001184 / OWR-3392-012, at original PR head `947442c091ae617804c6a0d07b98ff2c50368798`. No other target, shard or person was contacted. Every output and disposable test artifact was written inside this review folder. The paper, archive, original native snapshot, shared checkout and helpers were not edited. No remote mutation, Git index update, commit, push, merge, release, publication or tracker append occurred.

## Mandatory findings

None. No mathematical gap, source-category mismatch, unsupported promoted priority assertion, rendering defect, archive-replay failure, incorrect author/ORCID metadata or unsafe operational retry behavior was found within the reviewed scope.

## Optional findings

None. The ordinary underfull-box warnings and reference-only fifth page do not impede readability and do not require repair.

## Mathematical result and claim scope

The exact universal theorem is verified analytically: the actual forward-generated algebra is unital and separable; its restricted cocycle dynamics is injective and point-norm continuous; the evaluation/diagonal map is a conditional expectation; the compression is the two-state exponential Markov semigroup at all real nonnegative times. The concrete expectation-GNS correspondence is M2 over C2 with the column inner product, and its entire left representation kernel is exactly the evaluation kernel. Its adjointable algebra is M2 direct-sum M2.

For every s>0 the paper's element a_s belongs to that actual algebra, is globally positive and nonzero, evaluates to zero at x=0 and leaves the representation kernel after theta_s. The coefficient is

    d_s=(1-exp(-2s))/(2(sqrt(1+exp(-2s))+exp(-s)))>0.

The monotone-derivative integral argument handles x>0, while x<=0 and both endpoints are checked separately. Zero time, the square-root cusp, s decreasing to zero, and s increasing without bound introduce no gap. Failure is of the representation kernel, not just a chosen vector-null space. No map can intertwine the same pi and theta_s at a positive time, so the first step of the source's two-step proposal already fails.

The finite-image proposition is also correct. Kernel invariance gives a norm-continuous semigroup on the finite-dimensional represented algebra; the invertible-integral argument gives a bounded derivation generator, and the descended expectation's bimodule property forces the compressed generator to be a derivation. The paper separately excludes strong, weak/corner, faithful-expectation, normal W*, different-dilation and stronger/incomparable-minimality claims. Conditional extension after separately imposed kernel invariance and the source's future-algebra problem remain unresolved here.

The independently written analytic audit is `INDEPENDENT_DEDUCTIONS.md`; `INDEPENDENT_MATH_RESULTS.json` records 14 new symbolic diagnostics, including the parametric projection and Markov identities, all-time witness factorization, cusp derivative, limiting coefficients, literal BFH bath compression and generator obstruction. These diagnostics do not replace the continuum proof.

## Primary sources and priority

The [OWR primary report](https://ems.press/content/serial-article-files/46209), printed pp.497–498 and 542–543, was read directly and visually inspected. Its general dilation requires p theta_t i=T_t and i p a conditional expectation. The problem's reversed expectation arrow is reconciled with its definition and diagrams. It offers generation by the observed algebra and time shifts as the concrete size condition, so the stated negative answer has the correct category and scope.

The authors of [BFH v2](https://arxiv.org/abs/2010.00279v2) are Daniel Burgarth, Paolo Facchi and Robin Hillier, confirmed against the arXiv version record and [publisher record](https://link.springer.com/article/10.1007/s00023-022-01211-y). Sections 2 and 4, Definition 4.1, Step 2 and equation (11) support the established clock/evaluation/translated-unitary mechanism. The explicit amplitude-damping angle has finite endpoint limits; compactification and forward-generated restriction therefore provide precisely the point-norm continuous category required for the elementary finite-GNS derivation obstruction. This negative phenomenon is already a short corollary of their earlier explicit model. The manuscript correctly presents that as a deduction, not a theorem stated by BFH.

[DMB v3](https://arxiv.org/abs/1503.01010v3), Appendix B, and [vom Ende v3](https://arxiv.org/abs/2211.08351v3), Theorem 1, were directly inspected and accurately credited as finite-unitary/initial-derivative antecedents. Shalit–Skeide Appendix B(i) and Skeide–Sumesh Section 5 were also checked for category and fixed-action boundaries. Source URLs, exact raw-input hashes and inspected locations are preserved in `SOURCE_RECEIPTS.json`; raw full texts were read from existing ignored source storage and were not copied into public artifacts.

The paper, abstract, notice, README, deposit description and operation templates consistently frame the result as the formulation-specific corollary, small M2/C2 realization and exact positive witnesses. They make no new general-method, literature-first, exhaustive-priority, independent historical-development, plagiarism or human-review assertion. A supplemental four-query search recovered the primary formulation and related papers but no explicitly matching earlier negative statement; that negative search result does not certify priority. Existing bounded search ledgers likewise carry appropriate limits. Historical frozen status/priority prose is expressly superseded by the current notice.

## Paper rendering and metadata

The current five-page PDF was independently rendered and all five pages visually inspected. Equations, theorem statements, author line, ORCID, scope exclusions and six bibliographic entries are readable and unclipped. Tectonic independently compiled the source into this review's temporary build directory with no errors or overfull boxes. The extracted text and all five rendered PNGs are byte-identical to the current PDF's text and page images. All fonts are embedded. The PDF SHA is `d9cccada38421d088969a34458d5d7f48f0affd812184b5fe85ec689438806f6`; TeX SHA is `1c91a3423e4727b401e51f61630c0a2df90da7a3b870bac49ef47fde25ec475c`.

The deposit intent has the exact paper title, Alec Kriebel as sole creator, independent-researcher affiliation, ORCID `0009-0001-9320-500X`, preprint classification, date 2026-10-13, version 1.0, CC BY 4.0, open access, and exactly the PDF/verification-ZIP upload names. The description states the precise result, antecedent credit and AI/unrefereed disclosure. No live publication record or DOI is represented as already existing. `PDF_AND_METADATA_RESULTS.json` preserves the rendering and metadata checks.

## Archive, code and reproducibility

ZIP SHA `1c854a2b6c752e22d1e494076f1134136f18d11cec1d17321cff932a18ef2090` has exactly 88 safe regular members: 87 manifested files plus the self manifest. Every size, hash and inventory name matches. Manifest SHA is `91d2e4fd528baa01e3cddf2ca3d1dede5c3b0e659c9c13795f128823cf82d33f`. All 29 original candidate files match the unchanged native snapshot exactly; packet13 and audit11 include their pinned inner manifests. Source TeX, PDF, current notice, README, verifier and pinned requirements agree byte-for-byte with the public archive. The builder reproduced the identical ZIP in an independently reconstructed disposable source tree.

Portable full replays passed both normally and under -O, with inherited PYTHONOPTIMIZE=2: original author76 and audit237, fresh operator22, priority7 and classical14 diagnostics; scope sanity checks use the declared numerical tolerance. The original 12 integrity controls pass both modes. Fourteen additional independent package-inventory corruptions are rejected in normal and optimized modes, including duplicate JSON/path, unsafe paths, missing/extra/changed files, invalid count/size/hash, symlink and empty-directory cases. Original and extracted packet bytes remain unchanged after replay. `PACKAGE_CHECK_RESULTS.json` and the recorded stdout/stderr files provide checkable results.

The actual environment is Python3.12.14, SymPy1.14.0, mpmath1.3.0, matching the declared dependencies. The archive has only its own five-page PDF and no raw third-party full text, private source directory, operational helper, upload receipt or credential file. A pattern scan of 87 textual members found no private-key, GitHub-token, AWS-key or bearer-credential pattern. This complements the allowlisted content inspection; it is not a general guarantee against arbitrary encoded secrets.

## Final operation helpers

Final handover was received and these exact inputs were reread and tested:

- `prepare_integration.py`: `b1729250dce32ac4d28fe807bf1f9464169900b4e3a05e649fc04d79868b1472`.
- `record_tracker.py`: `9dde2c212bc0066baf8da0c7d8f141f71290600b2244ec8e7d79523d91262b48`.
- `reviews/operations_01/check_helpers.py`: `7ff31da444143f9e31dc7f2051ab9bd1d6dc6b993f9c743510ac633604a890f5`.

The selected-head gate accepts only the original reviewed head or this helper's exact successfully pushed commit for the same DOI, then verifies the latter's parents, full attempt inventory, changed-path scope, queue digest and frozen manifests. It precedes candidate/publication reads. The live selected row must be exactly claimed_solved at 1/5. The remote main target must still be queued at 0/5 and absent from the attempt subtree. Only the selected row's Status/Turns/Findings change, retaining all other queue bytes and line endings.

The helper builds a two-parent integration commit using an alternate index, checks the exact changed paths, replays the extended outer wrapper, and retains all packet13/audit11 bytes. A rehashed frozen-proof modification still fails integrity-only mode. Local main/index are compared before push; PR-head and remote-main drift are checked again immediately before an explicit non-force push. Unknown or ambiguous push outcomes are not automatically retried. No merge or branch deletion is implemented.

Both publication receipts must attest a production published record with matching title, DOI/record identity, DOI resolution and exact two-file SHA-256 digests. The upload ZIP, all original29, source TeX/PDF and current source notice are bound to local bytes. Mutable deposit metadata is hashed as reviewed intent; actual production metadata remains the publishing tool's verification responsibility. Missing receipts currently prevent live preparation.

The tracker pins spreadsheet ID, gid1254632077, title Math Puzzles and exact A:D headers. It prepares the verified source DOI, leaves solution-chat blank, uses exact DOI duplicate checks, and requires exact existing-row equality. The append guard refreshes immediately before dispatch, persists an unconfirmed marker first, checks one exact A:D append range, reads back the entire exact row, and checks global DOI uniqueness and the returned row number. Uncertain outcomes block blind retry. The current wording uses Burgarth–Facchi–Hillier and the credited corollary framing throughout.

All 14 supplied local/mock fixtures passed both normal and -O after relocation into this review folder. A further 24 independent edge checks passed in both modes: wrong selected status/turns abort before candidate reads; wrong gid/title/header, DOI prefix collision, wrong append tab/header row/two-row range/count/readback, missing notice, symlink ZIP member and rehashed frozen proof are handled; ambiguous append failures retain their marker and block another append. Results are in `OPERATION_EDGE_RESULTS.json`.

Residual operational boundaries are accurately recorded in the helper notes: mock tests do not prove live authentication/API availability, live publication or remote outcomes; the append API does not provide atomic uniqueness against an external simultaneous writer. The immediate pre-push checks and non-force push are guards, not a transaction across separate remotes. These are deployment limitations, not missing mathematical evidence or reasons to mutate services during review.

## Final identity and remaining work

`INPUT_SHA256.json` records all 14 selected package/helper/note inputs; `FINAL_INPUT_RECHECK.json` confirms no drift. Original proof SHA remains `f2a1b3b4233c2850d8dd79ba17b464d74343aa66e7d22d12104d17fc5470e8a3`. The strongest verified result is precisely the current continuous generation-only counterexample with global positive witnesses at every positive time, plus the proved finite-image obstruction and correctly credited prior implication.

This round is complete. A clean fresh sequential package review and the parent's subsequent exact production-record/file checks remain outside this review and necessary before remote operations. Broader minimality/normal/conditional-extension questions and exhaustive priority remain outside the mathematical result. Review completion estimate: 100%.
