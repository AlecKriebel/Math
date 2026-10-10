# Independent isolated-transversal audit

This package contains an independent mathematical audit, exact tests, public verification metadata, and a separate strict-inventory correction. The reviewed public author derivative is supplied separately. Its editorial metadata redaction leaves the mathematics, geometry, verifier code, and author results unchanged. Earlier archives remain unchanged.

Verdict: accept the `3d-3` minimal-pinning lower bound and the conditional `4d-4` theorem. The existence of an unrestricted finite `h(d)` remains unresolved here. The author's directory inventory checker has a confirmed `__pycache__` bypass; the reviewed ZIP itself is clean.

## Files

- `INDEPENDENT_AUDIT.md`: complete finding, proof review, source scope, and acceptance boundary
- `RESULTS.json`, `RESULTS_OPTIMIZED_RELOCATED.json`: independent normal/optimized replay
- `strict_inventory.py`: fail-closed unchanged-author archive/directory check
- `independent_test.py`: independent rational geometry and adversarial tests
- `verify_package_strict.patch`, `PATCH_REPLAY.json`: separate correction and tested outcomes
- `verify_corpora.py`, `CORPUS_REPLAY.json`: optional full-corpus identity replay, metadata only
- `SOURCES.json`: public primary-source metadata and inspection history
- `ACCEPTANCE.json`: structured final scope and status
- `AUDIT_MANIFEST.json`, `verify_audit_package.py`: exact audit-package inventory

## Replay

Disable local bytecode creation to preserve exact inventory:

    python -B verify_audit_package.py
    python -B strict_inventory.py --archive /path/to/ISOLATED_TRANSVERSAL_30001066_AUTHOR_PUBLIC_SAFE_DERIVATIVE.zip --expected-sha256 be4dabaf22028561681c76c353bd537d0b240cfd67d52aa7ed9531f435905034
    python -B independent_test.py --author-archive /path/to/ISOLATED_TRANSVERSAL_30001066_AUTHOR_PUBLIC_SAFE_DERIVATIVE.zip
    python -B -O independent_test.py --author-archive /path/to/ISOLATED_TRANSVERSAL_30001066_AUTHOR_PUBLIC_SAFE_DERIVATIVE.zip

Optional full-corpus replay requires the three separately held complete datasets:

    python -B verify_corpora.py --catalog /path/to/catalog.json --problems /path/to/problems.json --research-results /path/to/research_results.json

Do not write fresh result files into an already manifested packet unless producing a new identified version. Scripts need only Python's standard library. No network access is needed for mathematical or inventory replay. Source PDFs, extracts, screenshots, datasets, and private coordination are excluded.
