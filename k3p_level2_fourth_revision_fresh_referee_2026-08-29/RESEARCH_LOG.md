# Research log

## 2026-08-29 19:28 PDT — audit opened

- Created a dedicated fourth-revision audit folder.
- Recorded the neutral referee brief and the third-revision findings as the
  review baseline, without accepting either package claims or stored PASS
  fields.
- Package contains 664 files and occupies approximately 170 MB.
- Package-manifest SHA-256:
  `c67c1c524ef59217a2327e7dd4016cd82a9b8be1e8f188e6cc61a4fe1fd6c725`.
- Outer checksum-list SHA-256:
  `5bf8045cf745754092f0eb7e1a00bd7842ba475dc70d74091b099e135b974fa4`.
- Article PDF SHA-256:
  `3d08a722ba1fa53f6e336ab285c1cd32d1307bac08e1d4dd2460da71df1816d6`.
- Supplement PDF SHA-256:
  `96508f4b4eddb89de99881172abee307b3fe86d236f48e17508bdd1ca9c30efa`.
- Three independent adversarial tracks opened: mathematical/certificate,
  release/seal, and source/literature.

Completion estimate: **5%**. Authentication and all substantive checks remain.

## 2026-08-29 19:38 PDT — source reading and first independent checks

- Read the 38-page article and 14-page reader supplement completely before
  relying on stored package conclusions.
- Rendered every page and inspected six contact sheets covering all 52 pages.
  No clipping, overlap, missing glyph, unresolved-reference artifact, or
  malformed figure/table was detected; `pdffonts` reports every font embedded.
- Independently restated the theorem, domain, quantifiers, reconstruction
  boundary, triangle ambiguity, and weak-class sharpness in
  `PRIMARY_SOURCE_CLAIMS.md` and updated the claim dependency map.
- Confirmed by Git comparison that mathematical manuscript sections 01--16
  are byte-identical to revision three; only reproducibility disclosure and
  supplement text changed.
- The copied sealed payload passed the initial package-integrity verifier:
  635 payload files, 597 inner proof members, 160,213,642 inner bytes, with
  bytes and modes bound. The expected 55-command plan reconstructed exactly.
- The supplied folder itself already contained 14 MB under unsealed
  `review_runs/`, despite `START_HERE.md` saying a clean delivery contains no
  such directory. These files were inventoried as untrusted author runtime
  evidence and excluded from the clean execution copy.
- Launched the package runner's combined `all` mode exactly once in the clean
  copy under a network-denying, credential-free macOS sandbox. It remains the
  sole fresh verification/regeneration process.
- Seven referee-owned check families passed in 39.613 seconds without
  importing package modules. Suite report SHA-256:
  `bf578631a4303afee4eb20c6a2d2fc05d624308c6d8de0e60072d110ebdd6327`.
- Independent cut-certificate red team: fresh evidence rebuilt
  byte-identically; 72/72 ordinary and 18/18 optimized resealed typed-claim
  mutants were rejected; both CLIs rejected an unbound evidence path in both
  modes. Prior finding F2 is closed.

Completion estimate: **55%**. The long official replay, release audit, source
reproduction/literature audit, and final synthesis remain.

## 2026-08-29 19:46 PDT — all bounded subaudits complete

- Prior F1 is closed on its active routes: the three implicated atomic writers
  preserve `0644`, and the new focused control passes.  A release red team
  independently matched the package to exact commit `10bd695c...`, rejected
  37/37 release attacks, and passed 12/12 controls.
- Prior F2 is closed: exact typed nine-row declarations are independently
  enforced; 72/72 ordinary and 18/18 optimized resealed claim mutations plus
  four unbound-path controls were rejected.
- Prior F3 is closed: 16/16 is now consistent and the local-versus-downstream
  resealing description is accurate.
- Prior F4 is closed: an independent checker matched all 24 Git-bound source
  members and reconstructed both ZIPs exactly; four completed offline Tectonic
  builds reproduced the two PDFs byte-for-byte; the exact 725-file cache and
  final reports/transcripts are bound.
- Bounded literature review found no identified primary result that subsumes
  the complete strong level-two K3P classification.  This is not an exhaustive
  priority guarantee.
- Two minor residuals were identified: an omitted fourth direct-report writer
  still produces mode `0600`, though no declared runner route uses it as a
  sealed output; and the historical release ledger still calls older hashes
  and counts “current.”  The pre-existing unsealed `review_runs/` directory is
  a separate delivery-hygiene inconsistency.

Completion estimate: **80%**.  The one already-running official 4+55 replay
and final evidence synthesis remain; no long command has been relaunched.

## 2026-08-29 19:48 PDT — disk-space safeguard

- Available workspace storage fell to approximately 505 MiB while the single
  official replay was healthy.  To avoid jeopardizing its later regeneration
  workspace, removed only three ignored, audit-created disposable copies after
  their reports and hashes were finalized: `tmp/math_cert_copy`, `tmp/pdfs`,
  and `execution/source_literature_reaudit` (about 391 MiB apparent size and
  roughly 325 MiB recovered on disk).
- The supplied package, clean running copy, official run, retained audit code,
  reports, hashes, and tracked logs were not changed.  The removed raw copies
  are reproducible from the retained commands but are not recoverable in place.
- Available storage after cleanup was approximately 830 MiB.

Completion estimate: **80%**.  This was an in-scope resource safeguard, not a
relaunch or modification of the proof package.

## 2026-08-29 20:19 PDT — verify phase passed; regeneration underway

- The original `all` process completed its fresh verification phase: 4/4
  commands passed.  The integrated independent replay took 2,961.961 seconds
  and the integrated mutation command took 13.374 seconds.
- The same process entered the 55-command regeneration and had passed its first
  27 commands at the checkpoint; it was not restarted.
- Storage fell to approximately 326 MiB because the runner deliberately
  retained both copied phase workspaces.  After `run_phase(verify)` had returned,
  source inspection at `run_active_verifiers.py:523-662,815-841` established
  that later logic uses the retained report/inventories/transcript and in-memory
  report summary, not the finished workspace.  Removed only
  `review_runs/20260830T023318.110748Z/verify/workspace` from the audit copy,
  preserving every verification evidence file.  This recovered about 154 MiB;
  the active regeneration workspace was untouched.

Completion estimate: **88%**.  The hour-scale regeneration tail and final
postflight remain.

## 2026-08-29 21:08 PDT — exact-once regeneration stopped by filesystem ENOSPC

- The same single process passed regeneration commands 1--38.  Their child
  timing sum was 2,138.644 seconds and included the full revised cut cone,
  405,216-presentation four-port producer, 133-anchor producer, 36,824-edge
  restoration producer/replay, and their mutations.
- Command 39, `probe_hour_scale_producer`, completed all 176 one-port anchors
  and reached two-port parent 600/2,107.  It then failed while flushing gzip
  ledgers with repeated `OSError: [Errno 28] No space left on device` and the
  runner exited 1.  No mathematical predicate or mutation failed.
- Commands 40--55 were not invoked.  In accordance with the user's explicit
  constraint, the process was not relaunched.
- Preserved the full partial transcript, verification report/transcript,
  detailed fresh report, and before inventories under
  `results/official_replay/`.  Machine-readable summary SHA-256:
  `437d8a6ab464e6c4cd7650342d386a0bc75c5a3cdbdfcba68711b7af46e90583`.
- A fresh postfailure integrity check again passed all 635 sealed payload files
  and 597 core members.  Independent inventory comparison found zero drift in
  the 6,635-entry virtual environment.
- The `probes`, `restoration`, `anchor_universe`, `four_port_atlas`, and
  `sharpness` directories are byte-identical to the third revision whose
  independent exact-once run passed every one of the 55 command bodies.  This
  corroboration is recorded as such; it is not relabelled a current full run.

Completion estimate: **95%**.  Evidence synthesis, report QA, and repository
checkpoint/push remain.

## 2026-08-29 — final referee synthesis

- Final recommendation: mathematically valid within the stated assumptions and
  finite-certificate boundary, subject to three localized release corrections.
- Verified all four prior repairs: official-route mode preservation, exact
  nine-row cut-certificate binding and mutation rejection, corrected mutation
  metadata, and the fully bound cached source/PDF build contract.
- Recorded three residual non-theorem issues: one untested direct-report writer
  still emits mode `0600`; a historical ledger retains stale “current” wording;
  and the delivered unsealed runtime tree should be removed or separately
  authenticated while its excluded control paths are hardened.
- Reconciled the exact-once replay without relaunching it: verification passed
  4/4; regeneration passed 38/55 before command 39 encountered filesystem
  `ENOSPC`; commands 40--55 were not invoked.  No fresh 55/55 fourth-revision
  PASS is claimed.
- Preserved the verification reports, complete partial regeneration transcript,
  pre-run inventories, postfailure seal result, environment check, independent
  mathematical checks, source-reproduction evidence, and PDF QA.  Removed only
  disposable copied workspaces after their evidence had been retained and
  hashed.
- Final adversarial mathematics, release, source/literature, runtime-hygiene,
  and evidence-reconciliation passes found no basis to downgrade the theorem
  verdict.

Completion estimate: **100%**.  The referee report and retained evidence are
final; the incomplete regeneration is a disclosed result, not unfinished
audit work.
