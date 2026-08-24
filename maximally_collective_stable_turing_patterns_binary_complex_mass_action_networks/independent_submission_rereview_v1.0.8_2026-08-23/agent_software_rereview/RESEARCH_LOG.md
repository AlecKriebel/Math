# Independent v1.0.8 software/reproducibility rereview log

## 2026-08-23 — opening checkpoint

- Scope: independently test the v1.0.8 repairs corresponding to prior defects D1–D4 and D6: PDF extraction/toolchain/producer consistency, optimized-Python guards on all 39 entrypoints, generic-recurrence evidentiary scope, fixed-baseline versus regenerated manifests, and output provenance including the stale `m=200` row.
- Preservation: `/source_snapshot` is read-only evidence. All commands capable of regeneration will run only in this agent's disposable copy.
- Additional target: investigate why `public/repository/sha256_manifest.txt` verifies while top-level `release/sha256_manifest.txt` names hundreds of absent v1.0.7 audit-copy files.
- Stored `PASS` outputs will be treated as provenance only.
- Completion estimate: **3%**.

## 2026-08-23 — preservation and manifest checkpoint

- Inventoried 1,064 files in the tagged snapshot and made a byte-identical disposable copy at `agent_software_rereview/disposable_source` (initial `diff -qr`: no differences).
- `public/repository/sha256_manifest.txt` passes all 210 entries. `release/BUNDLE_SHA256.txt` passes all seven bundles.
- Top-level `release/sha256_manifest.txt` fails: 1,063 current files verify, but 570 listed paths are absent. Every actual file except the manifest itself is listed and has the expected hash; the extra entries are all under the prior audit work directory, principally its duplicated `source_snapshot`, `working_packet`, and rendered-page trees.
- This is therefore not evidence of current-file tampering. It is a non-self-contained release-baseline manifest created against an unpruned local staging tree. Because `release/one_command_replay.sh:66` and `release/create_release_manifest.sh --check` fail on the tagged tree, it is nevertheless a real submission/release-integrity defect.
- Initial host lacks `pdflatex` and default-Python `pypdf`; the retained exact TinyTeX 2022.04 and disposable pypdf 6.10.0 environments will be used explicitly for the clean replay.
- Completion estimate: **22%**.

## 2026-08-23 — clean execution checkpoint

- Ran the exact recorded CPython 3.9.6 / TinyTeX 2022.04 / Biber 2.17 stack explicitly from retained disposable installations.
- A clean full public replay (not quick) passed all stages in 71.69 s, including 15 numerical illustrations, four figures, manuscript/supplement builds, exact-artifact comparison, PDF audit, and the distinct self-consistency manifest.
- Independently invoked all 39 direct verifier entrypoints: 39/39 passed normally in 87.392 s. The same 39 commands under `python -O` all rejected assertion-disabled execution in 0.959 s. All 25 tests/mutations passed in 9.23 s wall time.
- Byte comparison after replay found only the expected pytest runtime and provenance-scope differences plus the new self-consistency manifest. Exact data, simulations, figures, PDFs, integrated designs (including `m=200`), and stale-claim output were unchanged.
- Completion estimate: **70%**.

## 2026-08-23 — adversarial and submission checkpoint

- Independently repeated immutable-baseline controls. Changing `eta_3` from `143636/7451873` to `143637/7451873` made the shipped public manifest fail on exactly that file and stopped replay before stage 1. A one-unit generic-cubic coefficient mutation failed its final symbolic identity.
- Found an enforcement omission: impossible `FORMAT` and `LATEX` values in a disposable TeX lock still pass because `check_toolchain.sh:78-85` skips both rows. A simultaneous impossible `article.cls` row is correctly rejected, isolating the defect.
- Verified all seven ZIP hashes/integrity. The journal ZIP is byte-reproducible and matches its staged source. A clean two-pass supplement build has stale TOC page numbers; a third pass makes it byte-identical to the canonical supplement under deterministic settings.
- Exercised the top-level command with an empty `FROZEN_BASE`: it correctly reported all five missing historical-lineage archives, exited 2 before opening its log, and therefore did not check later stages. The full public replay remains the completed current-proof route.
- Completion estimate: **92%**.

## 2026-08-23 — final checkpoint

- Completed the 39-entry semantic inventory, separating exact symbolic work, finite exact regression, floating spectral regression, aggregate/provenance checks, duplicate layers, and typed-formula limitations.
- Finalized `SOFTWARE_REREVIEW.md` and the 26-row machine-readable `COMMAND_RESULTS.jsonl` ledger.
- Final software/reproducibility category: **VALID AFTER MINOR CORRECTIONS**. Three minor local corrections remain: regenerate the contaminated top-level manifest; enforce the FORMAT/LATEX lock rows; and add a third supplement pass to detached source-package validation. None changes a theorem hypothesis, conclusion, or headline claim.
- Confirmed the source snapshot has no tracked modification; all generated/mutated material remains under this agent's scratch directory.
- Completion estimate: **100%**.
