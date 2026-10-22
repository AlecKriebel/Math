# Global Hessian realizations: verification evidence

This standalone package accompanies the PR946 / problem 6000001 construction note. The mathematical result is a proper global realization of a smooth positive, boundaryless statistical manifold and its specified ordered torsion-free dual connections in one positive Hessian domain. For dimension n >= 1 the stated construction uses N = binomial(2n+4, 3). The domain may be nonconvex and incomplete. There is no finite-probability-model, optimal-dimension, global-gradient-injectivity, or firstness claim.

The accompanying manuscript and the written reconstruction in `root_receipts/ROOT_INDEPENDENT_RECONSTRUCTION.md` contain the proof. Finite computations cannot establish arbitrary-manifold existence. Extensive AI assistance was used in research, verification, packaging, and writing. These are unrefereed research materials; no independent human peer review or formal proof-assistant certification is claimed.

## Contents and temporal interpretation

- `original/unsolved_math_prioritization/attempts/6000001/` contains exactly the original 33 files, unchanged from PR head `7d3adb0e500b0414a49a449e7981d34ade329427`. Historical acceptance or priority language inside those preserved files is historical evidence.
- `reviews/` contains only the explicit sealed allowlists from five mathematical/reproducibility families (87 payloads), three priority families (35 payloads), and the separate reproducibility repair v2 (16 payloads), together with their nine original manifests. Source bodies, extracts, rendered pages, local runtimes, and private scratch are excluded.
- `tools/` contains byte-identical copies of the four current v2 tools. Historical v1 tools remain under `reviews/reproducibility/` for provenance; the current entry point never selects them.
- `root_receipts/` contains selected point-in-time root reconstructions and verification/disposition receipts. Their original timestamps and historical pending-work statements are retained. The current priority disposition permits preparation of a fully credited construction note, without certifying historical novelty, firstness, or current openness.
- `SOURCE_COPY_MAP.json` records every copied source path and hash. `PACKAGE_MANIFEST.json` is the authoritative closed inventory. Its own hash, and the entry-point hash, must be obtained from a trusted separate publication or review record.

The actual authorized AJLS 2017 preview statements, Theorems 4.10 (p. 222) and 4.11 (p. 238), were read later in the audit: finite target for compact inputs, countable target in the noncompact branch. Earlier sealed reports that could not access these statements are preserved as dated history. Full proof-page and other final-version access gaps remain qualified in the current priority disposition. The absence of an established full predecessor in this bounded audit is not a novelty certificate.

The original PR declared four proof-search responses out of five. Its corresponding historical native per-response events were unavailable. The audit added zero target proof-search responses; it does not authenticate or invent the missing historical events.

## Run the current checker

Authenticate `verify_package.py` and `PACKAGE_MANIFEST.json` against trusted external SHA-256 pins before executing. Replace `PIN` below with the externally authenticated package-manifest hash. Use Python >=3.11 with SymPy 1.14.0 and NumPy 2.3.5; the recorded build used Python 3.14.6. Use a trusted startup environment without `PYTHONPATH` or `PYTHONHOME` overrides. The checker does not install dependencies. Pass absolute paths.

```sh
python -P -B /absolute/path/package/verify_package.py \
  --package /absolute/path/package --manifest-sha256 PIN
```

Use `--integrity-only` to authenticate the closed inventory without running diagnostics. The entry point imports builtin `sys` first and explicitly requires safe-path startup (`-P` or `-I`) before importing other modules; an extra module beside the script cannot shadow a standard-library dependency before inventory checking. The default mode first captures and authenticates every package file, including the unchanged original inventory and current tool pins. It then materializes those captured bytes in a fresh temporary directory. All proof diagnostics run in explicitly isolated children at optimization level zero, with bytecode disabled and Python environment variables removed. The v2 launcher is executed from captured authenticated bytes; it authenticates the gate, worker, and comparator before execution. The independent programs also execute captured authenticated source. Programs that write beside their source write only beside temporary copies. The caller's package is reauthenticated after replay.

The outer checker supports `-O`, `-OO`, and `PYTHONOPTIMIZE=2`; it reports the *actual* outer optimization level. For the environment test, use `-P -B` and omit `-I` from the outer invocation so that Python observes that variable. Its diagnostic children still run at level zero. A normal run under `-I` ignores `PYTHONOPTIMIZE`; the historical v2 environment probe therefore actually observed outer zero, and is not represented as an observed two.

`package_selftests.py`, itself externally authenticated through the package manifest, runs ten selected rejection controls with `python -I -B`: an unsafe standard-library-shadow startup fixture, changed original proof, extra file, payload symlink, actual FIFO, archive traversal, duplicate member, archive symlink, archive control-character path, and an intentional false worker assertion. It is a supplement to the larger preserved historical control suites.

```sh
python -I -B /absolute/path/package/package_selftests.py \
  --package /absolute/path/package --manifest-sha256 PIN
```

The optional `verify_package.py --archive PACKAGE_ONLY.zip --archive-sha256 ZIP_PIN --manifest-sha256 PIN` accepts only a separately authenticated ZIP containing precisely this package's files at archive root, without directory entries or a prefix. It checks canonical paths, unique members, regular Unix file type and mode 0644, exact sizes, hashes, and the closed inventory before execution. A combined preprint archive containing `package/` plus manuscript files must first be authenticated and safely extracted against its separate complete archive allowlist; then run this checker on the extracted `package/` subdirectory. This checker does not claim to validate unrelated members of a combined archive.

## Exact checks and the numerical exception

The current v2 replay runs the three original inventory checkers and three original finite mathematics programs, then selected independent exact controls for nonaffine scalar-jet transformation, full third-jet feature rank/right inverse, conormal differentiation, ordered connection projection, mixed Hessian blocks, invariant Schur completion, degenerate/unbounded regimes, compact/noncompact examples, and dual flatness. These corroborate formulas, not the global theorem.

The original strict frozen-result wrapper **fails** on the tested Python 3.14.6 runtime because nine of twelve numerical sample fields differ, together with a runtime-version string. It has not been changed or described as passing. The largest observed absolute numerical difference was approximately 2.1032064978498966e-12. This separate portable policy compares exactly twelve named floating fields: `lambda`, `minimum_eigenvalue`, and `H_df_minus_dphi_max_abs` in each of four fixed `positive_hessian_completion_samples`.

- Lambda: float, finite, at least 1; absolute and relative tolerance 1e-13.
- Minimum eigenvalue: float, finite, strictly positive; absolute tolerance 1e-12 and relative tolerance 1e-10.
- Residual: float, finite, nonnegative and less than 1e-6; absolute tolerance 1e-10 and zero relative tolerance.

Every other mathematical field, key, type, integer, sample coordinate, and ordering is exact. The author diagnostic permits only its three top-level version strings to vary; the two historical audit diagnostics remove their explicitly identified version metadata before exact recursive comparison. The numerical tolerances are a bounded consistency criterion, **not a proved roundoff bound or byte-identical numerical reproduction**.

The checker's stdout is deterministic mathematical evidence for its given manifest and actual outer mode. It excludes child-output hashes and precisely identified provenance fields: global-Hessian `utc`; global-adversary `utc` and `python`; independent-exact `python` and `sympy`. No mathematical fields are removed. The complete raw diagnostic records and runtime provenance can be written with `--runtime-receipt /absolute/path/OUTSIDE_PACKAGE.json`. Canonical per-mode receipts containing this final manifest hash are stored outside the closed package to avoid a self-referential hash cycle.

## Trust boundary

The entry script and interpreter must already be trusted regular files. Python opens a directly supplied script before that script can validate itself; an internal checksum cannot protect that earlier open. The external pins must come from a separate trusted record. This tool rejects symbolic links and special inputs, extra or missing members, noncanonical paths, unexpected modes, and bounded-read changes, but supplies no OS sandbox. The trusted interpreter, startup environment, installed mathematical packages, process, and local filesystem are assumptions. Safe-path startup removes implicit script-directory and current-directory imports; it does not authenticate arbitrary configured Python import paths. Cryptographic integrity and finite diagnostic PASS do not certify the mathematical proof, sources, priority, human review, or publication readiness.
