# Version 1.0: attributed fractional iterated-area note

Alec Kriebel, Independent Researcher, ORCID 0009-0001-9320-500X. Prepared 14 October 2026 UTC. The primary artifact is paper.pdf with its standalone paper.tex. See SUPPLEMENT.md for scope, source versions, reproducibility limitations and custody. Newly authored content is CC BY 4.0; third-party publications are cited and excluded from the archive.

The analytic bound covers independent standard equal-H fBm, each fixed H in (1/4,1), the canonical iterated integral, both complete uniform grids, every T>0 and integer n>=1 and every L2 grid estimator. Brownian exact optimum and smooth asymptotic rate are prior. This is an attributed localized Gaussian-witness proof; full novelty, historical and method priority and worldwide current-open status are UNKNOWN. Source use is canonical existence plus sufficient L2 convergence; the pinned NTU v1 exact Euler coefficients are not endorsed. The fresh journal-formatted source has a different lag split; no journal-error claim follows from the specific v1 defect. See the current dated root addendum preserved in custody/.

Extensive AI assistance, unrefereed, and no formal certification. STATUS.json retains the original preparation state, and CURRENT_STATUS.json retains the dated bounded-repair stage. TERMINAL_STATUS.json and FINAL_ACCEPTANCE.md preserve the dated two-review terminal stage and its historical whole02 zero-finding result. CASE_ALIAS_REPAIR_STATUS.json preserves the dated case repair stage. PORTABILITY_REPAIR_STATUS.json preserves the dated portability stage. HISTORY_ORDER_REPAIR_STATUS.json preserves the dated history-order repair stage. TERMINAL_AFTER_WHOLE05_STATUS.json now governs current workflow: five complete whole reviews (minimum two), latest whole05 zero actionable findings and root-adopted, no further complete whole review currently required; terminal administration complete but NEW external ROOT final integrity REQUIRED and UNADOPTED. The program support hold supersedes former readiness; publication_ready=false, issues_resolved=false and published=false. Ascending service operations remain held after PR1032. The note does not establish an endpoint, sharp constant, exact limit, H-uniform constant, adaptive/nonuniform, unequal-H or correlated-component result.

## Clean extraction and read-only verification

The standard-library integrity, archive-building and finite-checker commands are validated on installed CPython 3.11.8 and 3.14.6 with IEEE754 binary64 floats. Other runtime versions/platforms are unvalidated; no blanket Python 3.9+ support claim remains. Tectonic is optional for standalone PDF recompilation and may need its normal TeX cache/network resources. The commands below were executed against a clean extraction. Replace the two input paths with the downloaded archive and its containing directory. Generated outputs must be new and outside every descendant of the extracted frozen package. Their parent must already exist and have no symlink ancestors. Physical existing-ancestor identity is checked against the frozen root, including case aliases and ancestors above absent intermediate directories. Parent-traversal (..) components are rejected before normalization. Existing output files/directories are rejected, including symlinks, dangling links and hardlink aliases. Use a new directory/file for every run. This static local preflight covers the entire new checker/compiler directory, including subprocess files, logs and receipts; it does not promise safety under concurrent filesystem changes.

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

The checker uses an unchanged isolated copy of the original standard-library program and checks every non-utc container, type and field against the frozen baseline. Exact identities/normalization and sample inputs stay exact; only derived floats use the explicit finite tolerances in PORTABILITY_REPAIR_NOTES.md (covariance absolute 2^-49; other derived values relative 2^-47). Nonfinite values reject; covariance residual consistency and positivity are checked. Same-runtime normal/optimized non-utc JSON must also agree exactly. Original assertions run only in normal mode; the optimized pass relies on the explicit wrapper contract. Explicit guards survive `python -O`; negative controls remove Fourier conjugation, remove the current journal lag-cutoff qualification, and change the exact area pairing to zero. Finite floating calculations are neither interval-validated nor universal analytic proof.

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

Every manifest/member file is required to be present, regular, nonsymlink and reached only through real directory ancestors inside the package, including the self-hash-excluded manifest BEFORE JSON parsing. The default absent-binding path and strict present/required binding checks remain available. The original preparation's pin manifest and dated reports remain unchanged. history/preparation01/ resolves exact before bytes of changed outputs; WHOLE01_COPY_EXCLUSIONS.json names individually omitted raw streams/private/generated files. These historical artifacts retain their earlier meanings and are superseded first by the dated CURRENT_STATUS.json repair stage and then by the dated TERMINAL_STATUS.json/FINAL_ACCEPTANCE.md stage, then by CASE_ALIAS_REPAIR_STATUS.json, then by PORTABILITY_REPAIR_STATUS.json, by HISTORY_ORDER_REPAIR_STATUS.json at that dated stage, and currently by TERMINAL_AFTER_WHOLE05_STATUS.json for workflow accounting.

The local audit resolves all 92 original preparation output pins, including external receipts, the previous ZIP and its sidecar. The distribution preserves selected exact before-byte text/code/manifest/descriptor snapshots; it does not redistribute the previous ZIP, its sidecar, raw compiler streams or all external preparation receipts. Current UPLOAD_BINDINGS.json is outside the ZIP and binds the current PDF/archive/manifest.

## Current support hold and review accounting

Five NEW complete whole reviews are complete (minimum two). Latest whole05 found zero actionable P0–P3 issues and is root-adopted. No further complete whole review is currently required. TERMINAL_AFTER_WHOLE05_STATUS.json governs current workflow: terminal administration is complete, but NEW external ROOT final integrity is REQUIRED and UNADOPTED. Readiness/issues-resolved/published remain false; services held after PR1032. Only a later external ROOT final seal can override readiness. All earlier statuses/counters/FINAL seals retain dated meanings.

HISTORY_ORDER_QUALIFICATION.json remains unchanged: the old global-order claim is false because intact633-row audit and306-row candidate blocks were swapped within1558 later references, changing939 global positions. The exact row multiset, each stage's internal order, first2788 global rows and all4346 byte identities are preserved. The raw false assertion remains sealed dated history and explicitly superseded. PORTABILITY_REPAIR_NOTES.md still defines the unchanged finite runtime contract.

The external native uploader input remains publication/zenodo-deposit.json with metadata/files in the audit tree; included deposit.json remains a historical metadata wrapper. All prior153 ordered copy rows and50/83/116/128/140 prefixes remain exact; six before-interface snapshots and16 complete safe authored whole05/root records are appended. WHOLE05_DISTRIBUTION_DECISIONS.json decides every903 regular inventory row and3 fixture link targets individually. Inventories pin omitted raw programs/streams/bodies/images/fixtures without claiming new replay or redistribution. Old ZIP/sidecar remain durably retained outside the distribution. The mathematical paper/PDF, native bibliographic objects, citation, source boundaries and UNKNOWN priority/novelty/current-open qualifications are unchanged. See TERMINAL_AFTER_WHOLE05_NOTES.md for actual historical execution/failure scopes and final adoption requirements.
