# Static scope, reproducibility, literature, and presentation audit

**Audit date:** 2026-08-27
**Package audited:** `k3p_level2_identifiability_final/release/dist/K3P_Level2_Independent_Referee_Package/`
**Method:** current sealed package only; the supplied edit summary was not used as evidence. I read the manifests, `START_HERE.md`, article and supplement sources and rendered PDFs, bibliography, portable-review code, release-building and verification code, source ZIP metadata, submission metadata, and stored reports. I independently enumerated files and symlinks and recomputed the supplied SHA-256 list with system tools. I did **not** execute any package Python, shell runner, verifier, producer, mutation test, TeX build, or regeneration.

## Bottom line

This sub-audit finds **one moderate reproducibility-documentation defect and two low editorial defects**. The theorem scope, distinction between the 24 mathematical and 32 packaging mutations, retired terminology, portable 53-command plan, internal literature positioning, and substantive AI disclosure are internally coherent in the current package. The moderate defect is that exact historical execution and PDF double-build claims cite a ledger that the package intentionally excludes; those claims therefore cannot be audited from the current sealed delivery. This is not by itself a mathematical-theorem defect, because the package supplies a fresh execution route and expressly requires the referee to run it.

## Findings

### SR-1 — Moderate: the cited historical execution ledger is absent from the sealed package

**Evidence.** `proof_package/README.md:64-75` asserts that, at proof snapshot `e4b13c571eb462d7ba02e39ffd0a7b368fa5fc9f`, the clean quick suite and complete 54-command regeneration passed, that the latter ran for 7,686 seconds and regenerated 405,216 four-port presentations and 574,535 probe rows, that 24/24 and 32/32 mutations were rejected, and that both PDFs were rebuilt twice byte-identically and visually inspected. The README identifies `release/FINAL_RELEASE_ENGINEERING_REPORT.md` as the post-run ledger at `proof_package/README.md:71-78`. That file is not present. Its absence is deliberate under the sealed fileset policy: `proof_package/release/RELEASE_FILESET.json:49-69` excludes runtime/transcript locations and specifically excludes `release/FINAL_RELEASE_ENGINEERING_REPORT.md` at line 66.

`proof_package/FINAL_CLAIM_LOCK.md:191-200` repeats the suite-pass and deterministic two-build claims, but it is another claim document rather than underlying execution evidence.

The included `proof_package/reproducibility/RELEASE_WORK_LOG.md` is not a substitute for the missing current ledger. Its final checkpoint reports an older 205.782-second run, 18/18 integrated mutations, a one-shot 45-command execution, and older source/archive hashes (`RELEASE_WORK_LOG.md:176-199`); it ends with an external-submission status note at `RELEASE_WORK_LOG.md:201-203`. These are intelligible as historical log entries, but they do not evidence the current 54-command, 24-mutation, 7,686-second claim. The active plan records component/reference runtimes and a 210-minute recommendation (`referee_tools/ACTIVE_VERIFIER_PLAN.json:111-115`), not a transcript or completed-run attestation.

**Impact and theorem dependency.** This affects computational reproducibility and provenance, not any handwritten theorem implication directly. The current package statically supplies the producer/verifier plan and stored component artifacts, but a reviewer cannot authenticate the claimed historical execution, exact elapsed time, or two-build PDF result from the sealed delivery alone. Those statements must remain unverified unless the referee performs the documented fresh runs or obtains independently sealed execution evidence.

**Repairability:** straightforward.

**Exact repair.** Either:

1. add a sealed, immutable execution-evidence directory containing the cited final ledger plus the exact commit, ordered 54-command plan, environment/tool hashes, complete transcript hashes, per-command timings, fourteen-child fresh-replay report, 24- and 32-mutation reports, PDF two-build hashes, archive two-build hashes, and before/after drift record; then update `proof_package/README.md:71-73` to its included path; or
2. narrow `proof_package/README.md:64-78` to say that these are historical author-reported results whose underlying ledger/transcripts are not included, and require fresh reviewer execution before repeating them as independently verified facts.

### SR-2 — Low: “post-submission review” contradicts the package's explicit no-submission status

**Evidence.** `START_HERE.md:3-6` calls the delivery an “independent post-submission review” package. In contrast, `proof_package/README.md:78-81` says journal packages are `NOT_READY` and that no submission is claimed. `proof_package/submission/VALIDATION_REPORT.json:18-49` records 26 release blockers and status `NOT_READY`.

**Impact and theorem dependency.** Editorial/provenance ambiguity only; no theorem or computation depends on it.

**Repairability:** immediate.

**Exact repair.** Replace “post-submission review” at `START_HERE.md:3` with “pre-submission independent external review” (or simply “independent external review”).

### SR-3 — Low: the rendered article repeats the generative-AI disclosure

**Evidence.** The reproducibility section gives a substantive AI-use and human-review disclosure at `proof_package/manuscript/sections/17_reproducibility.tex:68-73`. The article then repeats substantially the same disclosure in the formal “Use of generative AI” section at `proof_package/manuscript/main.tex:149-158`. Both appear in the rendered article (the duplication is visible on article page 35).

**Impact and theorem dependency.** Presentation only. The disclosure is appropriately broad and clear; this finding concerns duplication, not omission.

**Repairability:** immediate.

**Exact repair.** Keep the formal disclosure at `main.tex:149-158`; delete `sections/17_reproducibility.tex:68-73` or replace it with a one-sentence cross-reference to the formal statement.

## Claims checked and supported internally

### Package seal, file count, runtime exclusions, and symlinks — pass

- `PACKAGE_MANIFEST.json:3007-3009` declares 600 payload files, 158,848,430 payload bytes, and proof source commit `76a097fbc4ddadf23ba0119a371c5ac29f4802b1`. Independent filesystem enumeration found exactly 602 regular files: the 600 payload files plus `PACKAGE_MANIFEST.json` and `SHA256SUMS`. `SHA256SUMS` has 601 entries, as expected because it covers the payload and manifest but cannot cover itself; this convention is disclosed at `START_HERE.md:15-18`.
- The inner canonical manifest lists 573 core members (`proof_package/ARCHIVE_MANIFEST.json:2-10`). The delivered `proof_package/` contains those 573 members, the inner manifest, and 18 intentionally supplemental `WORK_LOG.md` files, matching `START_HERE.md:10-13`; this is not a 573-versus-600 count inconsistency.
- Independent static SHA-256 recomputation produced no mismatches. I did not run `referee_tools/verify_package_integrity.py`. Its source nevertheless agrees with the stated contract: runtime roots are excluded at `verify_package_integrity.py:44-49`, payload symlinks and nonregular objects are rejected at `verify_package_integrity.py:52-74`, exact manifest/file equality is required at `verify_package_integrity.py:99-118`, and the checksum path set and bytes are checked at `verify_package_integrity.py:120-133`.
- A full-depth filesystem scan found zero symlinks in the delivered package and no top-level `.venv/` or `review_runs/`, consistent with `START_HERE.md:44-48`. Runtime creation of a workspace-local `.venv` link is an explicit runner implementation detail (`referee_tools/run_active_verifiers.py:366-376`), not a delivered-payload symlink.

### Commit identities — internally coherent, with SR-1 limiting execution-history verification

- The current delivery identity is consistently `76a097fbc4ddadf23ba0119a371c5ac29f4802b1`: outer builder and proof-source fields are at `PACKAGE_MANIFEST.json:2-3,3007-3009`; the canonical inner archive records the same source commit at `proof_package/ARCHIVE_MANIFEST.json:3450-3461`; and `proof_package/source_archives/k3p_level2_article_source.zip!/SOURCE_BUILD.json:17-22` records that commit plus the pinned Tectonic identity.
- The article's availability statement deliberately points to the earlier immutable **certificate and replay snapshot** `e4b13c571eb462d7ba02e39ffd0a7b368fa5fc9f` (`proof_package/manuscript/main.tex:131-140`). `proof_package/README.md:64-70` explicitly labels that value the exact pushed proof snapshot and says the article points to it. Thus the two hashes are assigned different roles rather than silently conflated. The current package alone does not contain the missing run ledger or a commit-to-commit diff, so the historical execution claim remains subject to SR-1.
- A clarity-only improvement, not required to cure a contradiction, would be one sentence in `START_HERE.md` stating: “This delivery and its TeX source archives are built from `76a097…`; the article's availability link names the earlier `e4b13c…` proof-execution snapshot.”

### Portable plan and runtime prose — pass statically

- `START_HERE.md:66-71` promises a 53-command portable mathematical regeneration plan. The active plan declares an original 54 commands, excludes only `release_engineering_mutations` because it requires the live Git checkout, and retains 53 mathematical commands (`referee_tools/ACTIVE_VERIFIER_PLAN.json:46-55`). Its ordered list expressly contains the full four-port producer, structural verifier and mutations, restoration producer/replay/mutations/portability test, probe producer/independent replay/full semantic replay/mutations/seal, sharpness, global-infrastructure, hardened cleanroom, primary rebind, release-input gate, integrated fresh replay, and integrated mutations (`ACTIVE_VERIFIER_PLAN.json:56-109`).
- The runner derives the command list from `run_release_suite.py`, removes only the declared exclusion, and fail-closes unless all counts and the exact order match (`referee_tools/run_active_verifiers.py:220-263`). The underlying suite contains four full-gate commands including the Git-bound release-engineering suite (`proof_package/reproducibility/run_release_suite.py:93-113`) and includes the full four-port, restoration, probe, sharpness, global, primary, and final integrated stages in regeneration (`run_release_suite.py:221-281`). This supports `START_HERE.md:113-120`.
- The runner records runtime/environment metadata, command output hashes and timings (`run_active_verifiers.py:123-158,161-208`), requires and preserves the detailed fourteen-child fresh replay (`run_active_verifiers.py:336-363`), checks workspace drift (`run_active_verifiers.py:416-438`), and executes verify/regenerate in separate copied workspaces when `all` is selected (`run_active_verifiers.py:489-499`).
- Isolation wording is appropriately limited: `START_HERE.md:50-59` says active verifiers make no network requests but dependency installation may, and explicitly says the runner is not an OS sandbox or credential boundary. No claim of credential isolation is made.
- Runtime estimates are presented as estimates/reference-machine data, not guaranteed bounds (`START_HERE.md:79-96`; `ACTIVE_VERIFIER_PLAN.json:111-115`). Exact historical runtime claims remain affected by SR-1.

### The 24-versus-32 mutation language — pass

- The stored integrated **mathematical classification** mutation report records 24 rejected, zero survived, status `PASS` at `proof_package/reproducibility/K3P_SAME_CLASSIFICATION_MUTATION_REPORT.json:174-179`.
- The separate **release-engineering/packaging** mutation report records 32 rejected, zero survived, status `PASS` at `proof_package/reproducibility/RELEASE_ENGINEERING_MUTATION_REPORT.json:316-329`. Its driver visibly defines the 32 cases at `proof_package/reproducibility/test_release_engineering_mutations.py:893-960` and requires the full regeneration plan to contain 54 uniquely named commands at `test_release_engineering_mutations.py:747-765`.
- The reader supplement describes 24/24 fail-closed integrated mutations and keeps publication engineering separate (`proof_package/supplement/reader_supplement.tex:70-75`); later it distinguishes the 24-mutation theorem suite from the clean-checkout 54-command wrapper and disclaims a release-archive gate (`reader_supplement.tex:916-923`). The portable plan properly omits only the 32-case Git-bound packaging suite (`ACTIVE_VERIFIER_PLAN.json:46-55`). No 24/32 conflation was found.

### Archive and source reproducibility contract — pass statically, subject to SR-1

- The release fileset pins the archive roots, PDF epoch, Tectonic version/hash, and full/compact selection counts and hashes (`proof_package/release/RELEASE_FILESET.json:1-11`). The environment document states the exact Tectonic executable hash and two-build equality requirement while disclosing that the tool is not bundled or inferred (`proof_package/release/ENVIRONMENT.md:15-23`) and that exact compressed bytes are conditioned on the recorded Python/zlib and TeX toolchains (`ENVIRONMENT.md:25-27`). This is consistent with `START_HERE.md:127-130`.
- TAR/gzip and ZIP builders normalize gzip time, member order, ownership, modes, timestamps, and compression parameters (`proof_package/release/archive_tools.py:83-153`). Verification rejects symlinks/hardlinks and nonregular TAR members and enforces root, ordering, ownership, mode, timestamp, size, and hash (`archive_tools.py:196-262`). Git-selected archive inputs are restricted to regular blobs with mode `100644` or `100755` (`proof_package/reproducibility/release_common.py:202-225`).
- Full selection is locked to the committed tree (`proof_package/release/build_release.py:379-406`); source ZIPs are built from committed blobs with the pinned TeX command/environment (`build_release.py:498-538`); and the full archive builder adds both source ZIPs, constructs and structurally verifies the deterministic TAR, and runs an extracted replay (`build_release.py:640-705`).
- Static inspection of both included source ZIPs found only regular members. Their TeX/Bib source bytes match the corresponding current package source bytes, and each `SOURCE_BUILD.json` records commit `76a097…`, Tectonic 0.16.9, executable SHA-256 `38eff9…`, and `SOURCE_DATE_EPOCH=1787677101`. I did not run Tectonic or rebuild any archive. The historical two-build and exact-runtime claims therefore remain unverified as explained in SR-1.
- `PACKAGE_MANIFEST.json:2` records the expected canonical full-archive SHA-256, while the canonical `.tar.gz` itself is not a payload member (generated archives are excluded at `proof_package/release/RELEASE_FILESET.json:67-69`). The hash is therefore a provenance/rebuild target, not something the extracted handoff can self-verify without rebuilding or obtaining the archive. This is consistent with the explicit non-self-reference boundary at `proof_package/ARCHIVE_MANIFEST.json:3456-3459`, but it should not be reported as independently reproduced in this static audit.

### Mathematical scope and retired wording — pass

- The article explicitly limits the result to an exact infinite-data topology theorem, not full parameter identification (`proof_package/manuscript/sections/16_scope.tex:3-7`), and lists binary standard semi-directed networks, level at most two, strong tree-childness, positivity, fixed labels, and principal-positive/strict-continuous-time domains (`sections/16_scope.tex:9-22`). It expressly excludes the principal boundary cases, signed/nonpositive domains, larger model classes, pointwise-everywhere identification, full stochastic-image equality, and finite-sample guarantees (`sections/16_scope.tex:24-40`).
- The withdrawn universal pointwise cut-recovery claim is explicitly retired at `proof_package/manuscript/sections/17_reproducibility.tex:61-66` and is not used in the active prose. The old “same classification” phrase survives in compatibility filenames, sentinels, manifest paths, and an explanatory compatibility note (`proof_package/FINAL_CLAIM_LOCK.md:201-203`); `START_HERE.md:24-27` and `referee_tools/ACTIVE_VERIFIER_PLAN.json:117-121` expressly say it is not theorem terminology. No active theorem statement was found using that retired phrase.

### Google Drive — no active claim found

No active Google Drive or `drive.google` claim appears in the current package's article, supplement, availability statement, start guide, release metadata, or submission wrappers. The operative availability statement points to the immutable GitHub commit and expressly disclaims an unsupplied DOI/license (`proof_package/manuscript/main.tex:131-140`). A final report should not import or repeat any Google Drive assertion from an edit summary or omitted external ledger without separate evidence.

### Scholarly positioning — internally careful; external accuracy not assessed here

- The introduction distinguishes level-1 and level-2 results, model differences, finite-data work, and quartet-concordance work rather than presenting them as direct substitutes (`proof_package/manuscript/sections/01_introduction.tex:31-74`). Same-author JC/K2P companions and the tree--theta result are explicitly called unreviewed (`sections/01_introduction.tex:75-88`).
- The Kimura-family synthesis again says the JC/K2P manuscripts are unreviewed and not independent corroboration, limits the comparison to three named models, and disclaims independent consensus or arbitrary-group generality (`proof_package/manuscript/sections/15_kimura_perspective.tex:3-8,34-41`).
- Bibliography records for the three same-author companions repeat their unreviewed status and give immutable versions/commits or tags (`proof_package/manuscript/references.bib:241-283`). No material internal novelty overstatement or model conflation was found.
- Because this assignment was restricted to the current package, I did not browse publisher, arXiv, Crossref, Google Scholar, or repository pages. Publication status, bibliographic metadata, literature completeness, and priority/novelty claims therefore still require an independent external literature check before a final referee verdict.

### AI disclosure and rendered presentation — substantive pass, duplication noted in SR-3

- The formal disclosure names mathematical exploration, code generation, implementation, drafting, and adversarial review; explains the evidence policy; disclaims independent human specialist review; and assigns responsibility to the author (`proof_package/manuscript/main.tex:149-158`). Submission wrappers and cover letters contain corresponding disclosures, so there is no material omission.
- I visually inspected all 37 article pages and all 13 supplement pages from rendered page images. I found no clipping, overlap, missing-glyph boxes, unresolved template tokens, or illegible figure/table failures. The supplement is dense but legible. Article page 37 has substantial unused space after the last bibliography entries, but that is optional reflow polish rather than a defect.

## Unexecuted and unresolved checks

1. No package code, integrity script, portable runner, verifier, producer, mutation suite, or regeneration command was executed.
2. No TeX/PDF or TAR/ZIP artifact was rebuilt; exact byte reproducibility, peak memory, elapsed times, command sentinels, and before/after drift were not reproduced.
3. The absent execution ledger and transcripts leave the exact historical claims in `proof_package/README.md:64-78` unresolved (SR-1).
4. Literature facts and novelty were assessed only for internal wording and citation structure, not against external scholarly databases or the linked works.
5. Static integrity and source-code inspection establish identity/contract coherence, not mathematical truth or successful execution.
