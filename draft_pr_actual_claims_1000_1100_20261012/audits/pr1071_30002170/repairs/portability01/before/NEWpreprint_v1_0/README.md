# Version 1.0: attributed fractional iterated-area note

Alec Kriebel, Independent Researcher, ORCID 0009-0001-9320-500X. Prepared 14 October 2026 UTC. The primary artifact is paper.pdf with its standalone paper.tex. See SUPPLEMENT.md for scope, source versions, reproducibility limitations and custody. Newly authored content is CC BY 4.0; third-party publications are cited and excluded from the archive.

The analytic bound covers independent standard equal-H fBm, each fixed H in (1/4,1), the canonical iterated integral, both complete uniform grids, every T>0 and integer n>=1 and every L2 grid estimator. Brownian exact optimum and smooth asymptotic rate are prior. This is an attributed localized Gaussian-witness proof; full novelty, historical and method priority and worldwide current-open status are UNKNOWN. Source use is canonical existence plus sufficient L2 convergence; the pinned NTU v1 exact Euler coefficients are not endorsed. The fresh journal-formatted source has a different lag split; no journal-error claim follows from the specific v1 defect. See the current dated root addendum preserved in custody/.

Extensive AI assistance, unrefereed, and no formal certification. STATUS.json retains the original preparation state, and CURRENT_STATUS.json retains the dated bounded-repair stage. TERMINAL_STATUS.json and FINAL_ACCEPTANCE.md preserve the dated two-review terminal stage and its historical whole02 zero-finding result. CASE_ALIAS_REPAIR_STATUS.json now governs current workflow: the new CASE-1071 P3 support defect is bounded-repaired, but a NEW complete whole03 review and root repair/terminal adoption are required. The program support hold supersedes former readiness; publication_ready=false, issues_resolved=false and published=false. Ascending service operations remain held after PR1032. The note does not establish an endpoint, sharp constant, exact limit, H-uniform constant, adaptive/nonuniform, unequal-H or correlated-component result.

## Clean extraction and read-only verification

Python 3.9+ standard library is sufficient for integrity, archive building and finite-checker replay. Tectonic is optional for standalone PDF recompilation and may need its normal TeX cache/network resources. The commands below were executed against a clean extraction. Replace the two input paths with the downloaded archive and its containing directory. Generated outputs must be new and outside every descendant of the extracted frozen package. Their parent must already exist and have no symlink ancestors. Physical existing-ancestor identity is checked against the frozen root, including case aliases and ancestors above absent intermediate directories. Parent-traversal (..) components are rejected before normalization. Existing output files/directories are rejected, including symlinks, dangling links and hardlink aliases. Use a new directory/file for every run. This static local preflight covers the entire new checker/compiler directory, including subprocess files, logs and receipts; it does not promise safety under concurrent filesystem changes.

```sh
python3 -m zipfile -e /path/to/PR1071_preprint_v1_0_support.zip /path/to/pr1071-clean
cd /path/to/pr1071-clean
python3 scripts/verify_package.py
python3 scripts/check.py --out /path/to/pr1071-check-output
python3 -O scripts/check.py --out /path/to/pr1071-check-output-optimized
python3 scripts/build_archive.py --out /path/to/PR1071-rebuilt.zip
cmp /path/to/PR1071_preprint_v1_0_support.zip /path/to/PR1071-rebuilt.zip
python3 scripts/verify_package.py
python3 scripts/build_pdf.py --out /path/to/pr1071-pdf-output
cmp paper.pdf /path/to/pr1071-pdf-output/paper.pdf
```

The checker uses an unchanged isolated copy of the original standard-library program and compares all result mathematics with the frozen original, ignoring only utc. Explicit guards survive `python -O`; negative controls remove Fourier conjugation, remove the current journal lag-cutoff qualification, and change the exact area pairing to zero. Finite floating calculations are neither interval-validated nor universal analytic proof.

Default verification succeeds in a clean extraction with no external upload binding present. A binding file that is present is checked strictly; a missing archive or mismatched PDF/ZIP fails. To require external bindings explicitly:

```sh
python3 scripts/verify_package.py --require-bindings \
  --bindings /path/to/UPLOAD_BINDINGS.json \
  --archive /path/to/PR1071_preprint_v1_0_support.zip
```

The bare metadata.json object equals the metadata object in metadata_wrapped.json and deposit.json exactly. UPLOAD_BINDINGS.json and the archive sidecar are intentionally outside the ZIP to avoid self-reference. PACKAGE_MANIFEST.json excludes its own hash; the external binding pins it. A deterministic ZIP_STORED allowlist uses fixed UTC date 2026-10-14, lexicographic order and regular-file mode 0644. No ambient filesystem glob is packed. The builder never rewrites the manifest or other frozen content.

Selected original authored records remain byte-exact in custody/; their historical wording is governed by the current paper, SUPPLEMENT.md and dated source addendum. INPUT_COPY_MAP.json proves exact copy identity. FROZEN_INPUTS.json records all earlier audit bytes including omitted private sources; downloading those bodies or rerunning omitted programs is not claimed. Raw source PDFs/text/images/API captures, environment executables, Git full trees and upload/service actions are excluded.

## Repaired support interfaces and citation

CITATION.txt is a validated plain UTF-8 scholarly citation of the research note; the mathematical paper is not classified as software or a dataset. The invalid original CFF (root `type: unpublished`, outside CFF 1.2.0's software/dataset enum) is preserved exactly as history/preparation01/CITATION.cff.invalid.txt and is not an active citation file. The official schema is https://raw.githubusercontent.com/citation-file-format/citation-file-format/1.2.0/schema.json . The verifier parses the plain fields and requires their exact agreement with the reviewed author/title/ORCID/version/date and attribution.

Every manifest/member file is required to be present, regular, nonsymlink and reached only through real directory ancestors inside the package, including the self-hash-excluded manifest BEFORE JSON parsing. The default absent-binding path and strict present/required binding checks remain available. The original preparation's pin manifest and dated reports remain unchanged. history/preparation01/ resolves exact before bytes of changed outputs; WHOLE01_COPY_EXCLUSIONS.json names individually omitted raw streams/private/generated files. These historical artifacts retain their earlier meanings and are superseded first by the dated CURRENT_STATUS.json repair stage and then by the dated TERMINAL_STATUS.json/FINAL_ACCEPTANCE.md stage, and currently by CASE_ALIAS_REPAIR_STATUS.json for workflow accounting.

The local audit resolves all 92 original preparation output pins, including external receipts, the previous ZIP and its sidecar. The distribution preserves selected exact before-byte text/code/manifest/descriptor snapshots; it does not redistribute the previous ZIP, its sidecar, raw compiler streams or all external preparation receipts. Current UPLOAD_BINDINGS.json is outside the ZIP and binds the current PDF/archive/manifest.

## Current support hold and review accounting

Two prior NEW complete whole reviews are complete (minimum two); historical whole02 found zero actionable issues. A later program/root case-alias audit found the new CASE-1071 P3 support issue. This repair changes the shared output guard and accurate current accounting only. NEW complete whole03 and root repair/terminal adoption are required; this package remains unpublished with readiness/issues-resolved false and ordered services held after PR1032. Old terminal/ROOT seals remain exact dated history. See CASE_ALIAS_REPAIR_NOTES.md, CASE_ALIAS_REPAIR_STATUS.json and the explicitly scoped authored CASE_ALIAS_SOURCE_EVIDENCE.json.

The external native uploader input is publication/zenodo-deposit.json in the audit tree; its unchanged metadata equals the three unchanged reviewed bibliographic objects and it selects this unchanged paper.pdf and same-named repaired support ZIP. Included deposit.json remains a historical metadata wrapper. The first 116 exact copy-map rows remain unchanged and ordered; new before-byte authored history and individual omissions are recorded without old archive redistribution or claims of omitted historical replay. No mathematical/bibliographic content changed.
