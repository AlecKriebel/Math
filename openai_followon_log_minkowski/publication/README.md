# Publication and verification package

**Title:** Even Minkowski uniqueness as a consequence of logarithmic Brunn–Minkowski  
**Author:** Alec Kriebel — ORCID https://orcid.org/0009-0001-9320-500X  
**Manuscript/deposit date:** 2026-10-06  
**License:** CC BY 4.0 for the owned contribution  
**Type:** research preprint

This package records a newly available consequence of OpenAI's released origin-symmetric logarithmic Brunn–Minkowski inequality and established transfers. It covers smooth positive even support-function existence and uniqueness in every ambient dimension `n >= 2` for `0 <= p < 1`, and general-body uniqueness for identical `Lp` surface-area measures when `0 < p < 1`. The body must be origin symmetric. The smooth solution has a positive-definite spherical curvature-radius matrix. No assertion of arbitrary-measure uniqueness is made at `p=0`: equal-volume coordinate boxes are explicit counterexamples.

The base inequality and known reductions remain attributed to their original sources. The note makes no claim of first public announcement or of an independent proof of logarithmic Brunn–Minkowski. The priority audit discusses the 2018 Stancu announcement and records an exact access limitation. AI tools were used extensively in the research, drafting and verification. This preprint has not undergone conventional human peer review or refereeing at publication. Automated reviews are not human peer review.

## Exact intended uploads

The project-local `zenodo-deposit.json` lists only these three files:

1. `publication/upload-kit/paper.pdf`: the exported, inspected manuscript.
2. `publication/upload-kit/source-and-verification.zip`: standalone TeX source, proofs/audits, dependency and priority records, source-hash inventories, reproducibility checks and exact reviewed-version evidence.
3. `publication/upload-kit/README.md`: this publication README.

The archive has an explicit `PACKAGE_CONTENTS.json`, containing byte sizes and SHA-256/MD5 checksums of every payload entry. `publication/package-inventory.json` records the upload checksums, archive entry list and build environment. Fixed entry timestamps, permissions, order and compression settings make repeat archive construction deterministic in the recorded Python/zlib environment. A PDF rebuilt with a different engine or environment need not be byte-identical.

The package excludes downloaded third-party articles, upstream source copies, dependency clones, caches, credentials, preview images, build intermediates and unrelated operational incident records. It includes references and inspected-source hash identifiers rather than redistributing the external inputs. The manuscript's bibliography is embedded in `main.tex`; no external bibliography processing is required.

## Checks before deposit

The final archive is assembled only after the manuscript is stable. Run the builder with the explicit review/response file list. A final build requires at least two distinct complete-package review records and the lead's confirmation that the latest exact package has no known substantive unresolved concern; the program does not substitute for that judgment.

```sh
python3 publication/build_package.py --review reviews/REVIEW_1.md --review reviews/REVIEW_2.md
python3 verification/reproduce.py
```

The builder supports `--check` to verify exact correspondence without replacing any file. It supports `--final` only when the required complete reviews have actually passed. The concrete final command and review hashes are retained in `package-inventory.json`. Testing the extracted archive from a fresh project-local temporary directory checks its internal checksums and reruns the exact arithmetic checks. Clean manuscript compilation and visual PDF inspection are documented in the verification records.

The independent upstream formal audit did **not** complete the Lean kernel rebuild, axiom extraction or Comparator checks. The source-scope inspection and successful installation of the exact toolchain do not establish formal certification. The follow-on theorem is not formalized. See the analytic audits and `verification/REPRODUCIBILITY.md` for the positive evidence and its limits.

## Authorized production workflow

The repository's `zenodo_deposit_tool/zenodo.py` is the sole upload/publication path. From the repository root, its documented sequence is:

```sh
python3 zenodo_deposit_tool/zenodo.py check openai_followon_log_minkowski/zenodo-deposit.json
python3 zenodo_deposit_tool/zenodo.py stage openai_followon_log_minkowski/zenodo-deposit.json
python3 zenodo_deposit_tool/zenodo.py inspect openai_followon_log_minkowski/zenodo-deposit.json
python3 zenodo_deposit_tool/zenodo.py publish openai_followon_log_minkowski/zenodo-deposit.json --confirm-id ACTUAL_VERIFIED_DRAFT_ID
python3 zenodo_deposit_tool/zenodo.py inspect openai_followon_log_minkowski/zenodo-deposit.json --check-doi
```

The draft ID must come from this deposit's verified stage/inspect response. Before publishing, match remote metadata, exact filenames, byte sizes and MD5 checksums to the reviewed local upload kit. Existing deposit state must be reconciled before creating another draft. A timeout or DOI propagation delay is handled by inspecting the same deposit; it must not cause a duplicate deposit. Credentials remain in the repository's supported secret locations and are never part of this package. No GitHub release is used.

## Publication and tracker receipt

The Zenodo record metadata supplies the assigned public identifiers after confirmed publication. This package document alone does not certify publication. Local nonsecret receipts record the submitted/public production state, DOI and metadata/file read-back. The DOI resolver state is checked separately from the verified publication state.

After publication, the authorized tracker operation targets spreadsheet `1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20`, numeric tab ID `1254632077`. The actual title and column order must be fetched before appending. Duplicate DOI/deposit/title checks precede the append; the exact inserted range and values must be read back and retained in a nonsecret receipt. Tracker failure is repaired without republishing.

## Verified publication and tracker receipt

Verified 2026-10-06 21:45 PDT. Production [Zenodo record 23203081](https://zenodo.org/records/23203081), DOI [10.5281/zenodo.23203081](https://doi.org/10.5281/zenodo.23203081). The DOI resolves HTTP200 to the public record. All 3 anonymous downloads match the reviewed byte sizes, SHA256 and MD5 hashes. Author Alec Kriebel, ORCID 0009-0001-9320-500X; publication date 2026-10-06; license CC BY 4.0. Exact metadata and public-file evidence are retained in ZENODO_INSPECT_PUBLISHED.json and ZENODO_PUBLIC_DOWNLOADS.json.

Three complete-package reviews were performed; fresh review 03 passes the exact final ZIP. The original regularity explanation was repaired with explicit global BBC(i) and CW hypotheses. The exact reviewed upload kit remains frozen and unchanged. This local README appends post-publication receipts; its uploaded copy and the ZIP retain the reviewed prepublication version. For the frozen source/reproduction package use the deposited ZIP; do not rebuild the kit from later live operational notes. Source-state checkpoint before publication:097cb1821f9d3a36c3f1aa57b1bdbd278cabd627.

The target sheet 1254632077 resolves to **Math Puzzles**. One RAW entry was appended and read back at **'Math Puzzles'!A37:D37**, DOI in C37. Headers were inspected in actual order. Duplicate search found no prior match; afterward there is exactly one match, and prior 36 rows/formulas remain unchanged. TRACKER_READBACK.json retains the exact values, and TRACKER_VERIFIED.json retains the range/integrity result. No public chat URL was supplied; that optional field is blank.
