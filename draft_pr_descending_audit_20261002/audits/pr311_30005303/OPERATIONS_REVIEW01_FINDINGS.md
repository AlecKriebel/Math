# PR311 publication operations: independent adversarial report

**Verdict: OPERATIONAL_REPAIRS_REQUIRED. Three concrete defects remain.** This is an operational verdict, not a mathematical, preprint, or priority finding. The already cleared scientific package was not reassessed or changed. Review completion: 100%; publication-operator clearance is withheld pending the repairs and a fresh review of their final sources.

## Independence, scope and evidence

The operational criteria were reasoned and frozen at **2026-10-04T20:05:54.057585+00:00**, before candidate access (`criteria_frozen.md`, SHA-256 `2aa6c6522233cf3473aff9ba634656002e62d535ebb8e71022d5515424aa7716`). All ten candidate sources were copied and pinned before simulations at **2026-10-04T20:06:37.860543+00:00**. Their absolute original/frozen paths, hashes, sizes and original modes are in `source_pins.json`. Final read-only source rechecks at 20:19:30 and 20:28:56 UTC found all ten original sources unchanged. All ten compile in memory.

Only new private files were written. No existing project file or mode was changed; no Git mutation, real network request, outside contact, other-chat message, release or publication occurred. The only collaboration messages went internally to ROOT. No other PR's mathematics was read or adjudicated. The two helpers were reviewed with ROOT's deployment clarification: reconciliation runs from its current private location; the checkpoint template is copied byte for byte into the descending-program folder under its final execution name. The checkpoint simulation used exactly that deployment arrangement.

`input_pins.json` freezes operational inputs, including the clearance, original and repaired manifests, queue repair receipt, initial branch refresh attempt, accepted body, merge body, publication metadata and shared-window state. The exact metadata input hash is `d34ee53b05b73bcb704ad43de2fba47ac1b0822597cf6788f20c730452e557d6`. It has all eleven keys, explicit creator affiliation and no description U+2019 normalization trigger. Scientific inputs were treated as already cleared; their contents were not independently adjudicated.

The authoritative counterexamples are in `simulation_artifacts_v04/`, driven by `simulations_v04.py` (SHA-256 `ba7590e421c1aa7c108717728528075c36dfb68bf42cdc1adb120add5236bbd8`). Trusted upstream clearance and all remote/Git interfaces were mocked. The exact candidate source bytes were executed without editing them. Mocked interface calls retain argv, UTC, complete returned stdout/stderr and explicit mock labels. Outer real process invocations retain actual argv, UTC, full stdout/stderr and stream hashes in `checks/*/invocation.json`, `stdout.bin`, and `stderr.bin`. Synthetic IDs 123, 777 and 999 are test inputs; no actual Zenodo ID has been assigned by this review.

## D1 — Public verification can inherit authentication and still pass

**Location:** `publication/verify_public_record.py:23–35`, especially the curl argv at lines 26–27. Candidate SHA-256 `f3708ef2b6e129989ac0869aee1a0f0f82e4014eda5f33f3b1133d095bc7b7fc`.

The command starts with `curl --fail ...` and does not disable curl's default configuration. An inherited `.curlrc` can supply an Authorization header, cookies, netrc configuration or client authentication. Consequently a successful complete download does not prove unauthenticated availability. The local curl primary manual states that default configuration is read unless disabled, and that `-q`/`--disable` must be the first parameter. The complete manual and a focused excerpt are retained under `checks/20261004T201148.368280Z_curl_manual/` and `checks/20261004T201930.849609Z_curl_config_primary_doc_excerpt/`.

**Counterexample:** `simulation_artifacts_v04/public_authenticated_only/` sets test-only `CURL_HOME` to its private directory containing a dummy Authorization configuration. The mock faithfully models that documented config-selection rule, and models a record and files accessible only with that authentication. All eleven metadata fields and both full file bytes match, and the unchanged verifier writes `PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES`. This proves the guarantee is unenforced; it does not claim that the user's actual curl configuration contains credentials.

**Required repair:** Make every purported public request explicitly unauthenticated. Use a trusted absolute curl executable with `-q` as its first option, no origin Authorization/Cookie/client-auth/netrc inputs, and explicit HTTPS protocol constraints, or an equivalently controlled unauthenticated HTTP implementation. Retain the effective command/configuration evidence. Re-test an authentication-only mock: it must fail, while an unauthenticated public record with complete matching files must pass. Preserve the paper, ZIP and all eleven metadata bytes.

## D2 — DOI, record ID and resolver landing target are not bound

**Locations:** kit `zenodo.py:69–97,359–388`; `run_zenodo_step.py:57–60`; `verify_public_record.py:37–48,67`; `append_tracker.py:22–25`; `root_record_publication_completion.py:17–26`.

The kit accepts any syntactically plausible DOI and calls any successful HTTPS landing response resolved. The public verifier checks agreement among the public API and local receipts, but does not require this manifest's version DOI to be `10.5281/zenodo.<record-id>`. Completion tests only `doi_resolution.http_status == 200`; it never verifies the final landing record. Thus internally consistent wrong identity can propagate to the tracker and completion announcement.

**Counterexamples:**

- `simulation_artifacts_v04/public_wrong_doi_record_id/`: record ID 123, DOI `10.5281/zenodo.999`, all eleven metadata fields and both complete file bytes otherwise correct. The exact verifier writes PASS.
- `simulation_artifacts_v04/kit_doi_wrong_landing/`: request `https://doi.org/10.5281/zenodo.123` ends at `https://zenodo.org/records/999` with HTTP 200. The exact kit returns `status: resolved`. The completion guard accepts that HTTP status.

**Required repair:** For this production manifest, require a positive integer record ID and its exact version DOI `10.5281/zenodo.<id>`, with that same identity bound through stage, inspected publication, unauthenticated public API, public verification, tracker and completion receipts. A concept DOI or an unrelated DOI is insufficient. Perform a fresh unauthenticated DOI resolution and require the final HTTPS Zenodo landing to identify that same record. Explicitly accept the canonical `/records/<id>` and legacy `/record/<id>` paths (optionally their trailing slash), with an approved Zenodo host and no userinfo, query or fragment; reject other record IDs, hosts, unsafe schemes and non-record pages. The generic kit can remain unchanged if the stricter PR311 checks are implemented locally. Test both approved path forms and the wrong-ID/wrong-host/HTTP200 counterexamples before clearing the revised operators.

## D3 — The checkpoint records allowlist pins but does not enforce them

**Location:** checkpoint template `root_checkpoint_311_completed_publication_031_preparation.py:29–35,39–48,57–71`. Candidate SHA-256 `6cd730fffb2616c707aa894c3089dc5d68d349f9001e02eaf78dc12e85e5f84c`.

The helper validates the intended QUEUE change and records file pins once, then stages and commits whole allowlisted paths. `foreign()` excludes the entire QUEUE file. Between stage and commit, it checks clearance and that excluded foreign snapshot, but never compares allowlisted bytes/modes with the recorded pins. Moreover `git commit --only -- <paths>` rereads the selected worktree paths. Its final comparison proves only that commit and current disk agree; it does not prove they match the intended pinned submission.

This `--only` behavior is independently supported by the local Git primary manual, retained in `checks/20261004T202740.559330Z_git_commit_primary_manual/` and its focused excerpt. It commits the worktree contents of specified paths rather than the previously staged contents.

**Counterexample:** `simulation_artifacts_v04/checkpoint_queue_race/` deploys the exact template at its intended path and uses the actual cleared target queue row, with its original 2/5 and the intended DOI insertion. All 29 original attempt files are separately modeled as unchanged. A completely synthetic foreign queue row changes after staging. The unchanged helper commits that foreign row edit, pushes in the model, and writes `PASS_PR311_PUBLICATION_COMPLETION_CHECKPOINT_PUSHED`. The intended QUEUE pin is `8539a7327590cce029dbbe03423020a5c02a35027f82340fcc1aec2f72f2c675`; the committed QUEUE hash is `677d441ae869872ee8d2d66f62686ecff256bab08a07bfcebcd544daa806761b`. The committed and intended full bytes are retained.

**Required repair:** Enforce the recorded contents and modes immediately around staging and before commit/push. Verify the staged tree's exact blobs/modes against the intended pins and exact path scope; commit that verified staged tree instead of permitting `--only` to reread newer worktree content. Use the shared exclusive-write discipline to close the final check-to-mutation interval, including shared-file edits as well as index writes. Independently verify the actual committed tree against the same pins before pushing. Treat another QUEUE-row edit as foreign shared-file work: stop and preserve it rather than including it or overwriting it. Re-run the after-stage row-edit counterexample and mode/content drift cases; the revised helper must stop without committing or pushing the altered file.

## Safety guards that passed and are not defects

`guard_checks.py` (SHA-256 `237420622aa8f38f617484eb727c886c1576fe75aaa1f3a2ae1bbb8401809fb7`) ran four private exact-source guard checks, with complete outer streams in `checks/20261004T201817.038275Z_uncertain_outcome_guards/` and detailed artifacts in `guard_artifacts/`:

- A prior uncertain merge marker stops integration before any subprocess invocation.
- A stage failure modeled after remote draft creation retains `stage_preexecution.json`, produces no successful stage receipt and blocks a second stage invocation. There is one subprocess call total.
- A publish response lost after remote success is recovered through GET of the same saved ID. A second kit invocation recognizes existing publication; there is one publish POST total in the model.
- A tracker append timeout modeled after one remote row insertion preserves the preexecution marker, produces no TRACKER_COMPLETE receipt and blocks a second append attempt. The wrapper launches one actual append CLI call in the model.

The wrapper's read-only `inspect_draft` route requires a successful stage receipt, so a failed partial stage needs direct read-only kit/account-state reconciliation. That is a safety-stopping recovery limitation, not false completeness or permission to restage. Missing actual merge, post-merge, publication and tracker receipts at this preparation stage are expected hard gates.

Static review also found the intended strong guards: main branch and empty initial index; exact head/API file set/blob checks; original snapshot byte hashes; exact 29 original attempt files; target-row preservation of original 2/5; merged-tree/parent checks; formal submission byte/mode pins; an immutable kit source pin; exactly eleven metadata comparisons and complete two-file readback; explicit tracker spreadsheet/tab/header/range checks; preexecution uncertainty evidence; and persisted foreign index/dirty-body/mode baselines. Neither helper creates a GitHub release. Reconciliation preserves the initial branch refresh receipt and writes a separate attempt/verification pair plus a saved prior repaired manifest.

## Exact limits and remaining gap

All remote behavior here was simulated. This review proves the listed enforcement failures and guard behavior, not the present Zenodo/GitHub/Google Workspace service state. The deployed gws launcher and local docs were inspected; its underlying binary's non-idempotent HTTP retry policy was not independently proved. The wrapper's no-retry claim means no wrapper rerun, not a proof of one underlying HTTP transmission. Preserve a known-safe CLI retry policy/version before the production append.

The source uses a shared-window status flag, not an atomic remote-main or cross-process lock. GitHub's head-match guard does not itself compare-and-swap the base ref. Maintain exclusive shared-main/index/shared-file ownership through the final merge and checkpoint intervals; unexpected advancement should retain its uncertain attempt and be reconciled. No alternate-base merge or concurrent tracker writer was cleared by this review. Strict unsupported API/schema variants are safety stops, not evidence of success.

The strongest verified result is that the exact prepared sources have the four tested uncertainty guards, but can falsely complete the three counterexamples above. The exact remaining gap is **repair D1–D3, pin final revised sources, and obtain fresh operational verification before promotion**. This requires no scientific/preprint/priority reopening or metadata/archive alteration.

## Retained evidence map

- `criteria_frozen.md`, `criteria_freeze.json`: independent pre-access criterion.
- `source_pins.json`, `frozen_sources/`: all ten candidate sources, original paths/modes and hashes.
- `input_pins.json`, `frozen_inputs/`, `documentation_pins.json`: exact operational inputs and local documentation. The optional gws-shared skill path was absent; nothing was installed or generated.
- `simulation_harness*_pins.json`, `guard_harness_pins.json`: harness pins before execution.
- `simulation_artifacts_v04/results.json`: authoritative four counterexamples for three defects.
- `guard_artifacts/results.json`: four successful safe-stop/recovery checks.
- `checks/`: actual outer argv/cwd/UTC/exit/full native stdout/stderr; scenario `mock_native/` directories clearly distinguish mocked calls and retain all returned bytes.
- Earlier v01–v03 artifacts are retained. The initial v01 run stopped correctly on a test label missing the required `public_readback_` prefix; this was a fixture error, not an operator defect. v03 improved the queue fixture; v04 made the curl configuration-selection environment explicit.
- `research_log.md`, `syntax_results.json`, `ARTIFACT_MANIFEST.json`, `SEALED_REPORT.json`: chronology/completion estimates, syntax verification and the final seal.
