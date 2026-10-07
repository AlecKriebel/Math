# Proposed publication kit and local deposit-state audit

Checkpoint: October 6, 2026, Pacific daylight time. Assigned kit-preparation completion estimate: 95%. This is a plan and proposed metadata, not a mathematical acceptance, a built final payload, or a publication action. No Zenodo account request, credential read, stage, publish, DOI creation, tracker change, Git mutation, or people contact was performed for this preparation.

The proposed title is **Metric rigidity at the boundary of cubic compactifications**. The creator is Alec Kriebel, ORCID 0009-0001-9320-500X, with no inferred affiliation. The metadata class is publication/preprint, open access, CC BY 4.0, version 1.0, language English, and manuscript date 2026-10-06. The local clock read 2026-10-06 22:51:03 PDT when this date was checked; UTC was already October 7. Recheck the intended manuscript date when freezing; a later actual upload date need not silently replace the manuscript date.

`metadata_proposed.json` describes the singular high-index criterion and metric-boundary application while making the pinned gap input explicit and crediting the complex comparison, its established transfer, splitting, smooth precursors, and conjugation convention. It discloses extensive AI use and absence of conventional human peer review. It makes no first-priority claim. The project lead must reconcile the exact final wording against the final manuscript and reviews and freeze it as `publication/metadata.json`. Add an immutable owned-source checkpoint related identifier before that freeze if desired; do not alter already reviewed metadata afterwards without renewed review.

## Actual downloadable payloads

1. `paper.pdf`: exact bytes copied from the verified project `paper.pdf`; a separate PDF download.
2. `source-and-verification.zip`: original standalone `main.tex`, static deposit README and `THEOREMS_AND_DEPENDENCIES.md`, selected proof notes, clean-build and verification scripts, original hash records, final licensing, final metadata and explicit selection, and `SOURCE_SHA256SUMS.txt`.

The helper writes these under `publication/upload-kit/` and writes the project-root `zenodo-deposit.json` with exactly `metadata` and `files` top-level keys. Its two file entries point to these actual payloads and name them individually. The outer `upload-kit.zip`, metadata JSON, licenses, checksum file, and package manifest are convenience and verification materials; they are not extra deposit file entries. This matches the documented Brandes publication convention, which uploaded the PDF and source archive separately.

The source archive contains a static `README.md` generated from `publication/README_FOR_DEPOSIT.md` and a static `publication/THEOREMS_AND_DEPENDENCIES.md`. The live repository README, theorem/status files, dependency ledger, approach table, and research log remain separate repository evidence and may change after publication without changing the frozen payload. The explicit proposed selection excludes those live files, `FINAL_STATUS.json`, the original pasted request, `checkpoint_push.py`, Git/publication operational receipts, hidden files, secrets, temporary/cache directories, all third-party PDFs and extracted text, and the read-only upstream clone. It also excludes unrelated KSZZ and Chen–Lai source-conflict investigations. The publication proof extracts preserve the relevant authored arguments without those investigations. Third-party sources are linked and pinned, not redistributed. `LICENSES_proposed.md` follows the repository's CC BY 4.0 prose / MIT original-code convention and must be finalized as `publication/LICENSES.md`; `source_provenance_proposed.json` must become `publication/SOURCE_PROVENANCE.json` after reconciliation.

The two forthcoming full-package review reports must stay outside the deposit archive. They inspect the exact frozen payload and current external review ledger and produce acceptance receipts referencing that snapshot. This avoids requiring a review report to include and hash itself. The source archive may include completed scoped proof audits or extracts chosen before the freeze. Any later changes to manuscript, PDF, metadata, selection, or selected source files invalidate the input freeze and require a new package and review snapshot.

## Deterministic helper and freeze procedure

`reproducibility/build_publication_package.py` uses only Python's standard library and performs local file reads and explicit packaging writes. It does not compile LaTeX, use credentials, run Git, contact Zenodo, or publish. Default mode is read-only. Run it from the project folder:

```text
python3 reproducibility/build_publication_package.py --selection publication/package_selection_proposed.json --metadata publication/metadata_proposed.json --plan
```

At this preparation checkpoint the final license and provenance filenames are deliberately absent, and selection status is proposed, so no final build is authorized or produced. The project lead should finalize the exact chosen files, current manuscript/PDF, static docs, metadata, and original scoped proof notes; then create `publication/package_selection.json` with the same documented schema, status `frozen`, and an initially empty `input_sha256`. Run a read-only final plan, copy its complete `input_sha256` mapping into that final selection, and run the plan again. The key `@metadata` hashes the canonical UTF-8 JSON bytes actually included in the package, rather than whitespace in the input metadata file. All other keys hash original selected file bytes, including `paper.pdf`. The selection itself is generated into the archive and is not an input hash, avoiding a circular digest.

Once `build_ready` is true and the mathematical gate allows packaging:

```text
python3 reproducibility/build_publication_package.py --selection publication/package_selection.json --metadata publication/metadata.json --build
python3 ../zenodo_deposit_tool/zenodo.py check zenodo-deposit.json
```

The first command produces actual payloads; the second is the documented local manifest/size/hash preflight and performs no network request. The final payloads then receive the required fresh complete-package reviews. This preparation has not run either command against a final kit.

Archive members use sorted names, `ZIP_STORED`, fixed 1980-01-01 timestamps, regular-file mode 0644, and no directory entries. This avoids dependence on source modification times and compression-library versions. The helper snapshots selected bytes before writing; it verifies every expected input hash and copies the PDF unchanged. A generated source hash manifest covers every other archive member, and `PACKAGE_MANIFEST.json` records all member and payload hashes. Building twice from the same inputs should yield byte-identical archives. Freeze plus exact-payload review is still required; these mechanical checks do not establish mathematics or novelty.

## Source and license provenance

The repository tool instructions read were `../zenodo_deposit_tool/README.md`, current `--help` and `check --help`, `deposit.example.json`, and the local manifest/state-path implementation. The reference convention was `../owr_17293_016_brandes_normalization/publication/README.md`, `zenodo/metadata.json`, `zenodo/LICENSES.md`, `zenodo/UPLOAD.md`, `build_package.py`, and `zenodo-deposit.json`. The documented example's affiliation was not copied. Only original material is licensed here. The final provenance JSON should be reconciled with the manuscript's inline bibliography; it deliberately contains no credential or absolute personal cache paths.

`initial_deposit_state_audit.json` records only nonsecret filenames and manifest-path-safe local observations. The chosen stable manifest is project-root `zenodo-deposit.json`. At the audit checkpoint this manifest did not exist, no matching local production or sandbox state file existed, and no project-local stage/publish receipt filename was found. No account or remote query was made. These observations do not prove absence of a remote record under another manifest path or lost state.

The tool hashes the absolute manifest path into its state filename, so preserve this path for stage/resume. The project lead handles any eventual `stage`, `inspect`, and confirmed `publish` sequentially after all gates. An ambiguous outcome must be reconciled using that same state and remote inspection before creating anything again. A returned published record and verified files establish publication; DOI resolver availability is a separate observation and must not trigger a duplicate deposit. No GitHub release is part of this plan.
