# Fresh whole-package adversarial review — round 1

**Verdict: CHANGES REQUIRED in publication workflow; mathematics, frozen package, attribution and four-page layout pass.** Two P2 safeguard defects were reproduced with fully offline stubs. No mathematical or PDF/archive repair is required by this review. The reviewed inputs were not changed.

Review completion: **100% of this assigned review scope**. This is a fresh candidate-aware whole-package review, independent of earlier whole-package verdicts. Archived candidate reports and their provenance claims were treated as objects to challenge. No outside sibling work, earlier whole-package review conclusion, Git/index/checkout mutation, external application mutation, publication operation, or communication with an external individual was used.

## Exact reviewed inputs

The note is 61,285 bytes, SHA256 `f066f56ee442078163b85c858bf180f484954b0bda56d3c686aa0c6b13a34853`. The verification ZIP is 257,172 bytes, SHA256 `17e8543dce0d41c829291c8840a749860159cff9fb48a8c6af8b3463dd4b895f`. The TeX SHA256 is `f2d3b59d95c813d07f4792d1781b29a09c7284255d3141a0ef3f7842f07204c2`.

`CHECKS/INPUT_BINDINGS.json` binds these plus BUILD/COMPILE/LAYOUT receipts, metadata, the standalone proof and all seven supplied workflow/replay scripts. `CHECKS/FINAL_INPUT_DRIFT.json` confirms all fifteen bound inputs were unchanged at the review's final checkpoint. The metadata SHA256 is `e04fff3fa5db7078bff504450eb1841000c8a339fbd8b328560fc617f1aa4d23`; the two affected script hashes are recorded in the findings below. A later repaired workflow requires its own updated binding/review.

## Required repair F1 — P2: rebind saved PR retries to the current reviewed operation

**Location:** `publication/update_pr_publication.py:40–49`, with saved operation data at line86.

The existing receipt fast path checks only that the PR head equals `old['commit']`, then returns the old receipt. The existing intent branch similarly trusts the recorded commit when the current head is either the original or that commit. Neither path compares the saved `review_gate_sha256`, DOI, expected paths or byte bindings to the current successfully checked package. Thus the top-of-function checks can authenticate today's artifacts/gate/publication, while the fast path accepts or completes yesterday's commit. The receipt can still contain the previous DOI and obsolete files. The original commit-parent/tree/path checks execute only in the new-intent branch and are skipped on recovery.

**Executed reproduction:** `CHECKS/stale_pr_retry.py` loads the actual script with isolated fixture files and replaces every Git/PR operation by local stubs. In both intent and receipt cases it supplies a current valid build/gate/publication fixture but a saved operation with a different review hash, DOI and obsolete file map. Both return successfully; the intent path writes `remote_readback_verified: true` for that obsolete operation. `CHECKS/stale_pr_retry.json` records the control-flow outcome. No real Git, gh, push or network operation occurred; this demonstrates a missing decision check, not an actual stale commit pushed to GitHub.

**Required repair:** before either fast return or retry push, recompute a current operation identity binding the full review gate, reviewed PDF/ZIP/metadata, confirmed deposit identity/DOI and relevant publication/tracker receipts, and the exact expected committed paths/bytes. Require equality with the saved intent/receipt. Independently read the recorded commit's parent and tree and verify the expected original parent, allowed exact path set and all blobs against those current bindings. Fail closed on any drift; do not silently reuse or overwrite an older operation. Ensure the tracker prerequisite belongs to the same deposit/DOI rather than accepting only its boolean `readback_verified`. Preserve the existing non-force push/readback and pinned branch/original-head checks.

Affected reviewed script SHA256: `fcb0688c6d885f9bc9dbf0cf1f024d25c9b6b72d6c9b092e7c65b8bc21ff8436`.

## Required repair F2 — P2: exact public metadata needs an actual comparison and gate

**Locations:** `publication/check_public_downloads.py:13–27`; resulting assurance in `publication/update_pr_publication.py:64`.

The public checker verifies record id, DOI and title, then the PDF/ZIP inventory and bytes. It never loads `zenodo-deposit.json` or compares the remaining metadata. A correct title and correct files therefore pass even when creators/ORCID, license, date, version, description/AI disclosure, keywords or related identifiers differ. Its own narrowly named `public_record_identity_verified` result is truthful, but this does not establish the generated PR statement that “exact metadata” was verified. The PR updater does not require a public-verification receipt at all.

**Executed reproduction:** `CHECKS/public_metadata_scope.py` loads the actual checker, provides exact reviewed artifact bytes, keeps id/DOI/title correct, and substitutes wrong creator, license, version, publication date and description. The checker succeeds. `CHECKS/public_metadata_scope.json` records accepted changed fields. All fetches are in-memory fixture lookups; no Zenodo request or mutation occurred.

**Required repair:** compare every supplied metadata field with the public record through an explicit legacy-deposit/public-record schema mapping, including creator name/affiliation/ORCID, publication type, description/disclosure, access/license, version/date, keywords and related identifiers. Normalize only documented representation differences, not substantive omissions. Bind the expected metadata hash, deposit identity and reviewed file hashes into a public-verification receipt, require that receipt before the PR's verification assurance, and reject missing/stale/inconsistent receipts. Add positive mapped-schema and one-field-at-a-time adverse fixtures. If a field is not publicly exposed, authenticate it through a separately recorded exact deposit response and describe that limit rather than claiming a public comparison.

Affected reviewed checker SHA256: `75d5f78ea32a7e8ca799a1b93478b47850350a2837782a93fd0edb63e4e0f960`.

## Mathematical and primary-source review

`CHECKS/ANALYTIC_REVIEW.md` contains the full independent derivation/falsification record. No mathematical gap was identified in:

- entire convergence from eventual logarithmic jets; complete relative X_M spaces; the M=0 unit-circle boundary; common factorial tails and the finite-coordinate topology;
- relative Baire/high-jet block density, including the zero polynomial, arbitrary huge fixed target coefficients, complex phases, retained low jets and the full shifted tail;
- highest-degree Leibniz dominance for every nonconstant complex p, including d=1, tiny leading/huge lower coefficients and polynomial-dependent onset; the all-p quantifier is deterministic after fixing f;
- full-orbit scalar nondensity including every finite initial evaluation; ambient density, meagreness and compatibility with Costakis's residual preservation family; universal polynomial preservers exactly the nonzero constants;
- the original stronger-locality fixed-p construction at a root of arbitrary multiplicity, triangular dependence only on prior corrections, uniform eta bounds, entire/null-orbit convergence and preservation of hypercyclicity near every prescribed HC input.

Fresh primary-source retrievals and source receipts are in `CHECKS/primary_sources.json`; bodies and rendered source pages are ignored and not distributed. Costakis's complete printed330/file34 page was visually inspected and matches Question5, Definition4 and Theorem6 exactly in operation and quantifiers. Nikula's complete v1 Theorem1 was visually inspected on pages2–3; Bayart–Matheron's relevant complete pages11–15 were visually inspected, with definitions and proof context cross-checked in text. Official version records and publisher-deposited DOI metadata were separately obtained. The source hashes agree with the archived decisive-source receipts.

The Gaussian estimates are summable at exponent3/4 and give one coefficient event for all p. Clipping is performed after applying the IID theorem; correction jets tend to zero, FHC survives a null derivative orbit, and the clipped law has full relative support including the collapsed annulus at coordinate0. The raw square-root lower floor would fail infinitely often, and the paper does not mistake it for an unmodified Gaussian property.

The Bayart–Matheron specialization uses a permitted separable complex Fréchet space, normalized Haar measure and the explicit eigenfield exp(lambda z). Its Fourier-basis images identify precisely the IID standard circular Gaussian jets; summability verifies gamma-radonifying convergence; monomials give spanning/full support; all L1 densities have Fourier decay; ergodicity and a countable basis give almost-sure FHC. No Banach-only assumption or unidentified Gaussian covariance is substituted.

The note correctly credits older implications without asserting that the sources explicitly printed the multiplier corollary or identifying its first recording. It distinguishes the served Nikula v1 PDF's later internal date of unauthenticated cause from official2012 repository and2013/2014 journal dates. It does not backdate a later explicit Bayart–Matheron remark. The no-firstness/no-new-existence/no-current-openness framing is appropriate. Full re-audit of all source proofs and an exhaustive priority census are not claimed.

## Frozen archive and reproducibility

A fresh, path-checked ZIP extraction contains104 unique regular-file members. The root manifest binds103 nonself members. Every extracted byte matches the staged verification tree and all build bindings. All six root/nested manifests were independently checked, including the later cross-freeze manifest beyond the special loops in verify.py. Submitted SHA256/size and Git-blob identities match the supplied snapshot; original and current editions remain separately bound. Current-document acceptance bindings and the source-question/analytic/priority freezes are coherent. This confirms internal original-object identities against the provided anchor, not a fresh read of the remote PR.

The extracted `verify.py` passed under normal, -O and -OO Python using only the standard library; each complete result equals the build receipt. Its two finite drivers actually replay in all three modes. The root driver's three altered recurrences are executed programs. The analytic driver's five controls are fixed-fixture false predicates, and current documentation/addenda accurately limit their scope. Historical missing execution bodies are not reauthenticated by current hashes. Input-boundary/independence statements are documented provenance claims; hashes bind their text but cannot retrospectively prove an agent's mental independence. No conflict between the current scoped provenance and archived records was found.

Eight deliberately altered extracted copies were actually rejected: changed payload, added member, removed member, duplicate manifest path, unsafe manifest path, original/current proof edits rebound only at root, and changed expected diagnostics rebound at root. The latter checks semantic replay rather than merely a frozen checksum. `CHECKS/corruption_controls.json` records each failure. External BUILD/artifact bindings remain essential because no manifest can authenticate its own rewritten root.

A separately authored exact rational-pair oracle, importing no candidate code, passed96 fixed-polynomial cases/1,344 recursion steps and80 radial boundary cases. It multiplies ordinary polynomials, expands both factors globally and directly differentiates at nonreal centers. Three actual altered recurrences fail the product barrier. These diagnostics corroborate algebra only; no finite computation establishes entire convergence, hypercyclicity, density, infinite escape, probability one or priority.

## Layout, metadata and remaining safeguard scope

All four rendered current PDF pages were individually inspected. No clipping, overlap, missing glyph, malformed formula/citation, broken paragraph or unreadable attribution was found. Title, author, ORCID and17October2026 date match the exact supplied metadata. The source/PDF/build/compile/layout bindings agree. The final page clearly discloses extensive AI use, unrefereed status and absence of external human peer review/formal certification. The intended two-file inventory, CC BY4.0, preprint type,1.0 version and cited identifiers are appropriate; no deposited DOI has been invented in the current inputs.

Seventeen offline guard/recovery cases in `CHECKS/workflow_guards.py` verify first append/exact-row recovery, refusal of uncertain unmatched intent, duplicate/mismatched rows, bad headers, unpublished state and bad readback, plus refusal of wrong branch, failed review, artifact/metadata/workflow drift, closed/unexpected PR and changed retry heads. Existing guards generally fail safely; F1/F2 are the specific remaining gaps. The append intent-before-write and exact-row reconciliation correctly avoid a blind sequential retry. Multi-process append concurrency was not exercised. The update script uses Git objects and a non-force pinned-branch push, preserving the shared index/checkout by construction. It does not itself implement Zenodo upload or merge; no future upload/merge result, public download or tracker mutation is certified by this review.

## Disposition

Repair F1/F2 in workflow code, run offline regressions including stale-operation and altered-metadata adverse cases, then bind and review the repaired workflow in the next fresh whole-package gate. Preserve this report and its exact input bindings. The existing PDF, source and ZIP may remain unchanged if the repair is confined to external workflow safeguards.
