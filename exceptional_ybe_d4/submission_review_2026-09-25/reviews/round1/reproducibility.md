# Reproducibility and verification audit — round 1

Checkpoint: 2026-09-26T04:56:00.216031+00:00. Baseline execution/audit completion: **100%**. Submission-supplement preparation is a separate follow-up (about **40%** complete at this checkpoint); its manifest is intentionally pending the GHR source-comparison adjudication.

## Verdict and exact claim

The unchanged v1.2.0 release reproduces all five supported execution routes, all 32 original failure-mode tests, and all 43 package-local checksums in a fresh hash-locked environment. The complete five-route stdout is byte-for-byte identical to `verification_output.txt`; SHA-256 is `108233f563373cc2b3e3e9fb4012f7f8ea52fb1149f58c2f6795344bfc5f3064`. The release source and upload artifacts were unchanged throughout this audit.

This establishes reproducibility of the **encoded finite identities**, not correctness of every literature attribution or all-strand theorem. The independent algebra review identified a material exception to the code's source-description: `verify_exact.py` calls its common-prefactor GHR matrix a literal transcription of Eq. (5.2), whereas the inspected preprint display has a different prefactor on its second block. The present successful run does not validate the claim of literal transcription. The submission must distinguish the corrected/common-prefactor representative or remove that source comparison. The mathematical computations about the encoded representative remain reproducible. This source issue is the sole substantive defect identified within the combined code/source review relevant to this report; its source-side evidence is in `evidence/algebra_ghr_source.py` and `.txt`, owned by the independent algebra reviewer.

## Environment and results

- Fresh virtual environment: `tmp/repro_venv`; CPython 3.14.6, SymPy 1.14.0, mpmath 1.3.0, optimization 0; macOS 26.6.2 arm64. Dependencies were installed with `--require-hashes --only-binary=:all:` against unchanged `requirements.txt`.
- Baseline Git commit when execution began: `ab42133b38eca7ee8758b6566054c39e6b2d8d71`, branch `main`. Other efforts' workspace changes were neither consumed nor modified.
- Five-route runner: exit 0 in 81.56 s.
- Original 32-test suite: exit 0 in 157.45 s.
- Package-local checksum checker: exit 0, 43 digests.
- Review-only arithmetic, consistency and packaging audit: exit 0, 297 explicitly checked conditions.
- Archived source ZIP: 44 distinct members, exactly the 43-entry allowlist plus its manifest. Every archived member equals its bound original file; no review notes, local environment, cache or submission correspondence is present.
- arXiv ZIP: exactly `main.tex`, equal to the original source bytes.
- All three uploaded artifact hashes agree with the two submission manifests. Rebuilding in `tmp/baseline_package_copy` produced all five files in `submission/` byte-for-byte identically, including both hash manifests.

The audit did **not** rebuild the PDF from TeX. Byte equality of the pre-existing PDF and deterministic repackaging is not a PDF-build reproducibility claim.

## Exact arithmetic and implementation independence

The standard-library matrices use `Fraction` coefficients in the basis `(1, sqrt(2), sqrt(3), sqrt(6))`, with a separate real/imaginary pair. Arithmetic multiplication follows reduction by `sqrt(2)^2=2`, `sqrt(3)^2=3` and `i^2=-1`; equality tests every rational coefficient. No tolerances, floating-point evaluation or random sampling enter these verifiers. The fixed eight-element field basis is linearly independent over the rationals, so coefficient equality represents equality in the stated field. The review independently compared every ordered basis product and conjugation in both arithmetic implementations with SymPy, tested nontrivial rational combinations and cancellation, and checked both real and Hermitian Pauli multiplication tables against independent 2-by-2 matrices. It also checked the quarter-turn conjugation formula and that the dense and Pauli encodings of R and its inverse coincide. The five supported scripts contain no binary float/complex literals.

There are five routes, **not five independent implementations of all results**. `verify_exact.py` and `verify_concurrent_equivalence.py` use duplicated versions of the same Q23/CQ23 formulas, although one matrix implementation is sparse and the other dense. `verify_braid_link.py:18–25` imports the concurrent verifier's field and matrix helpers. The SymPy route supplies a materially different arithmetic/matrix implementation for the central construction; the polynomial Pauli-word route supplies a materially different representation for the generic circle certificate. The fifth route's new global checks use a Pauli-sum algorithm but share scalar arithmetic. Manuscript wording currently says five supported routes and is defensible; an explicit dependency sentence in the curated supplement will make the boundary easier to assess.

## Silent-pass and failure-path audit

All five supported scripts reject optimized Python, use explicit failures rather than disableable Python `assert` statements, and report success only after their checks. `run_all.sh` uses shell fail-fast behavior and rejects wrong dependency versions. The original assertion-based discovery checker is expressly unsupported and is outside the runner. In the fixed real witness the SymPy use of transpose/squared entries is valid because H, P and both obstruction matrices are real; this is not a generic verifier for arbitrary complex inputs.

All 32 original negative tests passed. Their mutation helper only requires a nonzero subprocess status; it does not verify the reason. This is a **bounded test-harness weakness**, not evidence that any original mathematical check falsely passed: ordinary baseline execution succeeded in the same environment, the mutation anchors are checked to occur once, and the alterations preserve Python syntax. In the curated supplement the helper additionally requires `AssertionError:` in stderr, excluding import, syntax and infrastructure failures from being counted as a successful scientific rejection. No new cosmetic mutation sweep is needed.

The braid verifier's current-directory import fallback is used by the temporary mutation harness. Normal package execution resolves the sibling module. The program is a trusted local scientific script, not a sandbox for untrusted Python or an authenticity mechanism; checksum verification separately binds the sibling's bytes.

The checksum checker rejects malformed/duplicate/noncanonical/absolute/parent-directory paths, resolves symlinks and rejects escape outside the package. The package builder uses the verified allowlist, rejects a symlink output directory and unexpected output files. No archive-contamination or package-boundary defect was found. A SHA manifest establishes consistency against the selected manifest, not authorship of an untrusted replacement manifest; no stronger authenticity claim is made.

## Computational coverage and limitations

The finite programs certify the printed five-word construction, projection traces/rank, 64-dimensional ordinary Yang–Baxter identities, both exact obstruction trace-square values, active generalized operator/far commutativity, the six-dimensional three-strand image, the 18-word generic polynomial residual, the encoded local-unitary/opposite comparison, enhancement and skein constants, selected two- and three-strand link values, local order, the eight-term standard-frame non-Clifford witness, and reversal/Garside checks for every generator at n=3,4. The algebra/source caveat above applies to the claimed GHR literal input.

They do not by themselves prove all-n tower faithfulness, the full classification-based dimension-three exclusion, all-n conjugacy, the external Family III finite-image/evaluation theorem, or the Lickorish–Millett branched-cover interpretation. Those need the manuscript's proofs and cited-source review. Fixed n=3,4 tests cannot be promoted to an all-n proof. Independently computing dimension-three obstruction norms in a faithful d=4 trace model is useful evidence only after the printed trace/kernel argument has identified the relevant trace.

The missing discovery search code/seeds are explicitly disclosed in manuscript lines 1462–1465, with no claim of exhaustive/reproducible search or uniqueness. Exact verification of the displayed witness does not require reproducing discovery. No reproducibility defect arises from those missing seeds within this stated scope.

## Checkable evidence

`evidence/baseline_environment.json`, `baseline_locked_environment.json`, `baseline_dependency_install.log`, `baseline_run_summary.json`, `baseline_run_all.log`, `baseline_failure_modes.log`, `baseline_checksums.log`, `baseline_hashes_before.json`, `baseline_hashes_after.json`, and `baseline_crosscheck_summary.json` record the baseline. `evidence/audit_reproducibility.py` is the rerunnable independent arithmetic/archive check; `baseline_independent_audit.log` and `baseline_package_rebuild.log` record its output. Original release files were not edited, committed or pushed by this reviewer. No external contact occurred.

## Curated supplement completion checkpoint

Timestamp: 2026-09-26T05:06:56.951922+00:00. **Completion: 100%** for the assigned baseline reproducibility audit and curated verification supplement.

The follow-up curated package in `supplement/` is complete: all five routes pass in 82.16 s; all 26 retained scientific tests pass in 155.27 s; the stronger mutation harness requires explicit scientific `AssertionError` diagnostics; and all 14 supplemental manifest entries verify. The 15-file distribution boundary (including its manifest) is explicit in `evidence/supplement_allowlist.json`, with all final hashes in `evidence/supplement_final_hashes.json`. Final manifest SHA-256: `1e92f0f734669a0c233f89a7cd32742e4358133dca0e63a7b884a3bccd246b2c`. Fresh curated verification-output SHA-256: `ec55b7bba29e10ef0e2ab94995bf923419b8fddae55f1df45a4a3009434b802a`.

The auxiliary common-prefactor block matrix is now explicitly defined independently, verified against a distinct Pauli encoding, and separated from the accessible preprint's mixed-prefactor display. Both have their respective residuals checked. No intended-correction claim is made. The independent algebra reviewer approved the implementation and documentation, then confirmed that silently equating the two prefactors and reversing the new Pauli encoding's ZZZ sign each fail with the intended exact check. That closure is recorded in `reviews/round2/algebra_and_supplement.md`. The revised manuscript's old-GHR numerical comparison is outside this reviewer’s file ownership and was removed by the parent editor.

README/coverage documentation identifies all shared dependencies and finite-check limits. All actual code carries the requested title, author, affiliation, contact, ORCID and journal metadata. `PROVENANCE.md` records the earlier public-release identifiers and distinguishes this revision from the unchanged archival DOI; the parent independently rechecked the public timestamp, local tag resolution and historical Git PDF hash. This documentation-only provenance update was followed by a refreshed manifest/checksum run; the scientific code was unchanged after its passing run, so no redundant full rerun was needed.

The original release's 49 hash-bound source/manifest/upload files still match the original pre-audit snapshot. No original release file was edited; no commit, push, release, submission or external communication was performed by this reviewer.
