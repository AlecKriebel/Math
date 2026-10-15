# PR1052 bounded P3-01 package repair

The exact prospective notes-date correction is implemented in the three canonical metadata objects. The current local stage remains **PENDING_NEW_WHOLE_02**, dated 2026-10-14, with `publication_ready=false` and `all_issues_resolved=false`. This is a completed bounded administrative repair, not a new whole-package review, mathematical acceptance, global zero-issue verdict, or publication authorization. A NEW complete whole-package review 02, root adoption, the required fresh-review multiplicity, and the ascending publication hold after PR1032 remain.

Repair completion: 100%. Best-guess overall workflow completion: 90%. Checkpoint times and estimates are recorded in `RESEARCH_LOG.md`; execution times, commands, exit codes and complete authored stdout/stderr are in `REPRODUCTION_RECEIPTS.json`. `FINAL_PIN_VERIFICATION.json` records the final external-stage rehash and strict checks.

## Exact correction and scope

The final notes sentence in current `.zenodo.json`, `metadata.json.metadata`, and `zenodo-deposit.json.metadata` was replaced from:

> This metadata is prepared locally; no deposit or publication occurred.

to exactly:

> Prepared locally on 2026-10-14 before deposit or publication.

The three bibliographic metadata objects remain equal. Comparing the complete before and after objects proves that this exact sentence is their sole difference: no title, description, creator, ORCID, license, keywords, identifiers, publication date or other bibliographic field changed. The bibliographic assertion is now explicitly about local preparation before a future publication.

The wrapper, README, support history, preparation report, research log and new `verification/REPAIR_STAGE.json` consistently record the dated current pending stage. The current external `FINAL_VERIFICATION.json` is distinct from its preserved preparation snapshot. The original `OUTPUT_PINS.json` remains byte-identical historical preparation data; a distinct external `CURRENT_OUTPUT_PINS.json` binds current candidate files. The verifier adds only the exact dated notes and current preparation date/stage gates, using explicit guards that also execute under optimized Python. Both readiness flags continue to be required false. No optional-descriptor symlink policy or other security feature was added. `build_support.py`, the mathematical checkers, and the PDF builder remain unchanged.

## Baseline and immutable history

Before any repair mutation, all 1,136 pre-existing immediate PR1052 audit/candidate files were frozen in `INPUT_PINS.json`. Hashes were streamed without duplicating raw source trees. The 14 selected administrative before files, unchanged PDF, and old ZIP were copied to ignored local `private/before/preprint_v1_0/`. The old ZIP remains SHA-256 `34116a25f6632579fe8bf3494c50527a205560e55f511964350a71973e5b8625`; neither that baseline ZIP nor a duplicate PDF is included in the repaired support archive.

Before editing, all 348 preparation input pins, all 91 prior preparation output pins, all 23 first-review output pins, and all 59 original-to-support copies were independently rehashed or compared exactly. The complete first-review REPORT/VERDICT and root adoption were read. The original `REQUEST_NARROW_METADATA_REVISION` verdict with P0=0, P1=0, P2=0, P3=1 is unchanged.

Selected history now includes byte-exact copies of all 23 safe authored terminal files from `reviews/package_01`, that review's `OUTPUT_PINS.json` and `REVIEW_SEAL.json`, the root whole-review adoption, and 14 pre-repair administrative snapshots. `HISTORY_SELECTION.json` identifies each copy and confirms no authored terminal stream was omitted. Private/frozen raw trees, extracted text, environments, raw executable work trees, renders, third-party source bodies and duplicated binary archives were excluded. Historical manifests may identify excluded material; those identifiers are not a current archive inventory.

The prior 59 copy-map records remain exact in the same order, with their copied bytes untouched. Forty selected exact history copies were appended, producing 99 copy records. `support/history/preparation_01/OUTPUT_PIN_LOCATIONS.json` resolves every one of the 91 historical output pins to unchanged current bytes or preserved before bytes. Changed textual before bytes are distributed as clearly marked history; the old binary ZIP is resolvable only through ignored local custody. Historical notes, archive hashes and status snapshots were not silently rewritten.

`PROTECTED_UNCHANGED.json` rehashes all 1,122 protected pre-existing files. Exactly 14 pre-existing candidate files changed, all listed with before/after hashes and preserved-before locations in `CHANGE_INVENTORY.json`: the three canonical metadata surfaces, dated administration, allowlist/copy map/manifest, strict notes/date/stage verifier, current external final verification, ZIP and ZIP sidecar. All other prior bytes remain exact, including every mathematical/source claim, checker, eight-file original edition, 59 previous copied records, first-review terminal record and root adoption.

## Checkable final artifacts and reproduction

The final shipped PDF remains 58,570 bytes, SHA-256 `e2be83ab3c334c8352f1c6a256c6038b59ed834d3beaa50ed7602f3c24f292a6`. `paper.tex` remains 13,600 bytes, SHA-256 `ca8812d3e7d07193ecd0d7ff7f7cadcc04d078a3bab591b260b4fef39a5e7973`. Therefore the previously inspected four-page layout and prior standalone compilation receipts apply to the same source/PDF bytes. This repair did not compile, render, reinspect page pixels, create a PDF operation marker, or conduct a new mathematical review.

The final support ZIP is 892,512 bytes, SHA-256 `76f21bc611c39e7f45068ca325ae0fad796c2788b0206b6201137f814bcd0eb0`. It has exactly 125 sorted allowlisted members, regular 0644 file mode, fixed timestamp 2026-10-14T00:00:00, and stored compression. Every payload member is bound by the regenerated manifest; the manifest omits its own hash and is bound by the external archive hash. The current external descriptor is excluded from the ZIP and strictly binds both this archive and the unchanged PDF. The unchanged PDF sidecar and regenerated ZIP sidecar verify.

On both a wrapped exact payload copy and a fresh clean ZIP extraction, the following five README commands were actually executed verbatim and exited zero:

1. `python3 -I -B verify_support.py`
2. `python3 -I -B run_checks.py --output _runs/fresh.json`
3. `python3 -I -B test_integrity.py --output _runs/integrity.json`
4. `python3 -I -B build_support.py --output _runs/rebuilt.zip`
5. `python3 -I -B verify_support.py --archive _runs/rebuilt.zip`

Both rebuilt archives equal the final shipped ZIP bytes. A separate closed ZIP construction, importing neither shipped builder nor verifier, also equals those bytes. Each checker command runs the unchanged five authored family/mode checks and each integrity command rejects the unchanged 21 invalid controls. This is support reproduction; finite checks are not a new proof of asymptotic hardness or a fresh whole-package review.

Strict verification of the actual current candidate with its actual external descriptor succeeds in normal and optimized Python. The new repair controls also agree substantively in normal and optimized execution: two accepted current metadata/two-file-binding controls and 17 rejected controls per mode. They reject matching undated/wrong-date notes, wrong/missing stage, wrong preparation date, true readiness flags, mismatched metadata surfaces, altered PDF/ZIP byte-count or digest bindings, and three invalid-metadata build attempts after recomputing their manifests. Those three attempts demonstrate that a hash-consistent payload cannot bypass the current notes/stage gate or create an archive. Trace text and argv naturally distinguish optimized execution; the accepted/rejected outcomes and reasons agree.

The preliminary reproduction receipts are retained separately under `PRELIMINARY_REPRODUCTION/`; they refer to the earlier interim 124-member administrative payload. The final receipts and summary at this repair folder's top level refer to the final 125-member ZIP hash above. Final `CURRENT_OUTPUT_PINS.json` rehashes 134 current candidate outputs, and `FINAL_CURRENT_INPUT_PINS.json` rehashes 1,179 current immediate audit/candidate files, excluding this repair folder whose authored outputs are pinned separately.

## Remaining boundary

This repair supplies checkable implementation evidence for P3-01 and dependent administration. It does not relabel the first review as clean, clear issues globally, settle historical cyclic priority, add novelty, create human peer review or formal certification, alter the theorem or credited dependencies, or authorize publication. No new whole-package review was performed. No Git command, branch/index action, service write, release, deposit, other-shard coordination or outside individual communication occurred. The requested next step is root reading and pin checks followed by a fresh complete whole-package review 02; publication remains held after PR1032.
