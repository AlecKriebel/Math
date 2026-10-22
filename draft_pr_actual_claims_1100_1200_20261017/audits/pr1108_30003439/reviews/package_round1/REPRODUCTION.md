# Reproduction for this audit

All commands run with the working directory set to:

`/Users/alec/Documents/Math/draft_pr_actual_claims_1100_1200_20261017/audits/pr1108_30003439`

1. `python3 -B reviews/package_round1/audit_distribution.py` validates and extracts the frozen source, runs both distributed verifiers, and checks mutations. Requires only the Python standard library.
2. `python3 -B reviews/package_round1/independent_controls.py` runs the fresh exact Taylor-jet/interpolation mechanism. The same checks also run under `python3 -B -O`.
3. Rebuild without modifying the parent's source or cache:

```sh
mkdir -p reviews/package_round1/tmp/compiled
cp -cR /Users/alec/Library/Caches/Tectonic reviews/package_round1/tmp/tectonic-cache
TECTONIC_CACHE_DIR="$PWD/reviews/package_round1/tmp/tectonic-cache" tectonic -C --untrusted --keep-logs --outdir reviews/package_round1/tmp/compiled reviews/package_round1/tmp/unpacked/main.tex
```

The existing resource cache was cloned for scoped writes. `-C` prohibits downloading uncached resources. The cache copy was removed after compilation to conserve disk. A future environment needs an already populated TeX resource bundle; no new large bundle is required or downloaded by these instructions.

4. Render and extract both PDFs:

```sh
mkdir -p reviews/package_round1/tmp/rendered-distributed reviews/package_round1/tmp/rendered-rebuilt
pdftoppm -r 110 -png reviews/package_round1/tmp/unpacked/output/pdf/negative-curvature-cone.pdf reviews/package_round1/tmp/rendered-distributed/page
pdftoppm -r 110 -png reviews/package_round1/tmp/compiled/main.pdf reviews/package_round1/tmp/rendered-rebuilt/page
pdftotext -layout reviews/package_round1/tmp/unpacked/output/pdf/negative-curvature-cone.pdf reviews/package_round1/distributed_extracted.txt
pdftotext -layout reviews/package_round1/tmp/compiled/main.pdf reviews/package_round1/rebuilt_extracted.txt
/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B reviews/package_round1/pdf_check.py
```

The last command compares all pixels, exact extracted text, PDF page count, metadata, and compiler diagnostics. Visual inspection is separate and was performed on all five actual page images. Creation timestamps can change on rebuilding; hashes of rebuilt PDF bytes therefore need not match. The original frozen PDF and ZIP hashes must continue to match.

Observed versions: Tectonic0.16.9; system Python3.14.6; bundled Python3.12.14; Poppler26.08.0.
