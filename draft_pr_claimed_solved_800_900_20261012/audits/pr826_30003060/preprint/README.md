# A characteristic obstruction in higher Koszul homology

Alec Kriebel, independent researcher. ORCID 0009-0001-9320-500X. Version 1.0.0, October 14, 2026. Three-page unrefereed research note, extensively AI-assisted. No completed external human peer review or formal proof-assistant certification.

The literal unrestricted-field equivalence in Solotar's OWR 2016/10 contribution is false. The Koszul free algebra k<x,y> has nonzero fundamental-cocycle, coefficient-A higher homology in every positive characteristic. The characteristic-zero converse and the general vanishing-to-Koszulness implication remain unresolved here. The precise classical calculation is credited to Loday–Quillen, Goodwillie and the BLS definition. No new substantial mechanism, firstness or certificate of current worldwide openness is claimed. See CURRENT_PRIORITY.md and the bounded audit.

## Contents and boundaries

The archive includes note.pdf, editable note.tex, exact deposit metadata, this guide, current portable verifier and deterministic builder, all 65 original files in source/ (including four evidence archives with 55 members), current independent algebra and source-scope reports, priority reports/ledgers and root evidence. Raw scholarly PDFs/text/images and full imported source corpora are excluded. Source locators, versions and byte hashes identify what was inspected. Earlier assertions and superseded interface records remain explicitly labeled historical_v1; current executable checks use explicit guards.

The only promised complete portable verification entrypoint is verify_package.py. Files in root_evidence/ are dated audit evidence and may require the original audit-directory context. Optional source-provenance tools require the separately obtained complete input corpora/PDFs matching recorded hashes; the portable checker does not pretend to download or rehash absent inputs or repeat human-readable literature inspection.

## Trusted startup and complete portable checks

Obtain the external index SHA-256 and verifier SHA-256 from the final acceptance receipt in the repository, independently of the downloaded archive:

https://github.com/AlecKriebel/Math/blob/main/draft_pr_claimed_solved_800_900_20261012/audits/pr826_30003060/FINAL_PREPRINT_ACCEPTANCE.json

Verify the complete archive/member inventory and the verifier's bytes before running any downloaded program. The current verifier SHA-256 is ed19078665c832c52c405c29169cf621a6670499845b046ca970475bef40ceed. An executable cannot authenticate arbitrary replacement startup code by hashing itself. The final external acceptance receipt is the trust authority; it is not contained in the indexed archive, avoiding a circular digest.

From the extracted archive root, substitute the externally trusted index digest for PIN:

    python3 -I -S -B verify_package.py PIN --full
    python3 -I -S -B -O verify_package.py PIN --full

Python 3.10+ standard library and a compatible system patch command are required. The gate verifies a closed regular-file inventory against the external index pin before and after execution. It runs the original publication replay in a disposable canonical directory, verifies four archives / 55 members and three patches, and checks its 14 child runs. The original author and second-review children deliberately reject optimized startup; those rejections are fail-closed controls, not optimized mathematical passes. The historical root replay also includes eighteen startup/archive controls.

Fresh algebra diagnostics execute 2110 explicit checks in each requested mode, covering 234 matrix/necklace cases, 14 prime witnesses and 10 negative controls. A deliberately corrupted expected dimension must fail with no acceptance output. Separate integer word-operator controls cover 21 cases / 604 orbit blocks and distinguish Euler scalar d from Connes scalar n/d; a corrupted expected Euler scalar must also fail. These fresh current diagnostics genuinely run their checks with and without optimization. All write-producing historical and diagnostic programs execute only disposable copies; package inputs stay unchanged. Canonical temporary paths handle macOS's symlinked /var safely.

These bounded computations and integrity checks supplement the unlimited algebraic proof. They do not prove the theorem, establish historical priority, or replace the separately recorded primary-source reading.

## Rebuild the same archive

From the extracted archive root, use an output directory outside the intact input package, which must be new or empty:

    python3 -I -S -B build_verification.py --from-package . --trusted-index-sha256 PIN --output-root /absolute/new-output

From an assembled repository preprint directory, use --from-package ../verification_package instead. The builder rejects a nonregular input index before reading it, binds the index and verifier before execution, and reproduces package_index.json and verification.zip byte for byte. The default development assembly mode requires the original canonical audit layout; use the documented --from-package mode for a downloaded or assembled package. LaTex compilation is optional and not needed for verification; regenerating a PDF can alter its timestamp and bytes. The accepted PDF is the included one.

## Publication files and metadata

The repository preprint directory additionally holds zenodo-deposit.json with metadata identical to metadata.json, referring to output/pdf/note.pdf as higher-koszul-characteristic-note.pdf and verification.zip as higher-koszul-characteristic-verification.zip. The production upload is performed only from the canonical repository audit manifest after final independent package acceptance. The archive is for verification; it does not automatically create a deposit or update the tracker. The current kit, final external acceptance and publication receipts are preserved in the repository.

CC BY 4.0 applies to the authored note and supporting authored package. Underlying cited publications retain their own terms and are not redistributed.
