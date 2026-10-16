# Portable verification for the regular-ZAS weak Bianchi counterexample

Author: Alec Kriebel, [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). Problem 30004807 / OWR-8415343-010, PR464, original head `97b2ed225574ca61bd03cb8db021a533e04938dc`. This supplement supports the current research note; it is not a standalone historical-priority certificate.

The metric and tensor are the known Dadhich–Kar–Mukherjee–Visser family, with dictionary `(m, isotropic radius, kappa, lambda)=(-2a,rho,A,B)` and main `A=B=1/2`. The boundary-flux method is credited to BKTZ. The present application verifies regular-ZAS admissibility, all-vector-field absolute convergence, and a normalized radial defect `-8*pi`. Read [CURRENT_ATTRIBUTION_AND_SCOPE.md](CURRENT_ATTRIBUTION_AND_SCOPE.md) for primary references and the precise interpretation. The example violates NEC; arbitrary tilted slices, collapsed-point tests, independently smooth covector tests, and specified matter models are outside the claim. No new metric, new tensor, first historical priority, formal verification, or human peer review is claimed. AI tools were used extensively; the work is unrefereed.

## Run the complete package

Use Python 3.10 or newer. Create a disposable environment, install the two pinned dependencies, and run the entry point from this extracted folder:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_verification.py
.venv/bin/python -O run_verification.py
```

On Windows use `.venv\Scripts\python.exe` in place of `.venv/bin/python`. Installing the dependencies may use a network; verification itself uses no network. The supplied replay was executed with Python 3.14.6, SymPy 1.14.0, and mpmath 1.3.0. The independent symbolic output's Python-version field is the sole runtime-dependent field omitted from its expected-object comparison. All mathematical results and check names must match. Both historical JSON outputs match their frozen bytes exactly with the pinned dependencies.

For a useful dependency-free subset:

```sh
python3 run_verification.py --stdlib-only
python3 -O run_verification.py --stdlib-only
```

This subset explicitly reports `profile: stdlib_only`; it omits the historical and symbolic checks. A passing subset must not be described as a complete replay.

The entry point requires explicit integer counts and exact check names, actual Boolean `true` values, the `all_passed` flag, expected output, successful execution, and empty unexpected diagnostics. It uses conditional exceptions; Python optimization cannot disable its guards. Thirteen internal guard controls reject false/missing flags, false/non-Boolean checks, missing/substituted names, malformed counts, and duplicate JSON keys. The author's historical final `assert` is disabled by `-O`, so external explicit guards are essential.

## Evidence and limitations

- **Historical provenance:** thirteen files in `frozen_history/` match the original source receipt by SHA-256 and byte count, before and after execution. Six author-payload and five audit-payload manifest references are verified. The standalone author-manifest digest has no supplied path or bytes and remains **UNATTESTED**. No bytes are reconstructed to satisfy it.
- **Historical executions:** author17 and independent35 programs each run normally and with `-O` in fresh temporary working copies. Each produces byte-identical frozen JSON and stdout, with all checks explicitly inspected by the driver.
- **Independent geometry:** the exact rational second-order controls give 396 explicit checks over 18 cases per mode.
- **Independent curvature:** the full metric-derivative Christoffel/Ricci/Riemann controls give 1,557 exact equalities over 60 metric and 27 Cartesian cases per mode.
- **Independent Cartesian four-metric:** direct connection and Ricci contraction from exact rational second-order jets gives 2,916 explicit checks over 72 metric points per mode, including rotated directions and near-boundary cases.
- **Independent symbolic route:** the generic-lapse area-radius derivation gives 67 exact checks per mode. Sixteen false claim families are actually rejected in both modes, for 32 subprocess rejections. Exit code 4 and the exact intended `InvalidClaim` diagnostic are required; an accidental crash does not count.

All finite checks support the analytic arguments and do not prove their universal quantifiers by sampling. The analytic proof supplies the C1 approaching-surface area argument, all-test absolute integrability, causal interpretation, and source scope. The family reports preserve those distinctions. Literature and primary-source interpretation are separate reviews; no foreign full-text sources are redistributed.

`provenance/code_origins.json` records the four independent checker families, their original repository paths, and exact transferred code/report hashes. These programs are byte-for-byte copies with no imports from the historical checkers. The first three family reports are included here; the whole-candidate report is distributed separately by the publication package. Historical presentation and attribution omissions are superseded by the current attribution note; immutable source files retain their original bytes rather than silently rewriting history.

The driver reads the bundle and writes only to a temporary directory that is removed on completion. Deliberately false claim JSON inputs are generated privately during execution and never included in the supplement. `VERIFICATION_MANIFEST.json` contains the exact positive payload inventory and hashes, excluding its own hash. A separate delivery whitelist binds that manifest; neither sidecar authenticates a maliciously replaced entire package. They make received-byte checks reproducible.

`results/bundle_normal.json` and `results/bundle_optimized.json` contain the sanitized complete replay records. Their bytes are identical. No local absolute paths, credentials, foreign PDFs, private environments, invalid fixture files, or unrelated repository content are in the positive inventory.
