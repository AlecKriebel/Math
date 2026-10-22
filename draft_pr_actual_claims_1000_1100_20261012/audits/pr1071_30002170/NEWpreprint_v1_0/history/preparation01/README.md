# Version 1.0: attributed fractional iterated-area note

Alec Kriebel, Independent Researcher, ORCID 0009-0001-9320-500X. Prepared 14 October 2026 UTC. The primary artifact is paper.pdf with its standalone paper.tex. See SUPPLEMENT.md for scope, source versions, reproducibility limitations and custody. Newly authored content is CC BY 4.0; third-party publications are cited and excluded from the archive.

The analytic bound covers independent standard equal-H fBm, each fixed H in (1/4,1), the canonical iterated integral, both complete uniform grids, every T>0 and integer n>=1 and every L2 grid estimator. Brownian exact optimum and smooth asymptotic rate are prior. This is an attributed localized Gaussian-witness proof; full novelty, historical and method priority and worldwide current-open status are UNKNOWN. Source use is canonical existence plus sufficient L2 convergence; the pinned NTU v1 exact Euler coefficients are not endorsed. The fresh journal-formatted source has a different lag split; no journal-error claim follows from the specific v1 defect. See the current dated root addendum preserved in custody/.

Extensive AI assistance, unrefereed, and no formal certification. STATUS.json records the dated preparation state. This frozen version awaits at least two fresh whole-package reviews; publication_ready=false and issues_resolved=false. Ascending service operations are held at PR1032. The note does not establish an endpoint, sharp constant, exact limit, H-uniform constant, adaptive/nonuniform, unequal-H or correlated-component result.

## Clean extraction and read-only verification

Python 3.9+ standard library is sufficient for integrity, archive building and finite-checker replay. Tectonic is optional for standalone PDF recompilation and may need its normal TeX cache/network resources. The commands below were executed against a clean extraction. Replace the two input paths with the downloaded archive and its containing directory. Generated outputs are deliberately outside the extracted frozen package.

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
