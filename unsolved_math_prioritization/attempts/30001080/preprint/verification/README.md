# PR284 main-theorem finite verification controls

This is a small, portable verification package accompanying Alec Kriebel's AI-assisted, unrefereed research note on measure-only preserving Markov transports and joint mass-stationarity. It contains three unchanged historical exact finite-control scripts, their **complete** expected JSON stdout, a standard-library verifier, and provenance. The manuscript source is included separately as `../paper.tex` in the full source archive. This package does not itself contain the analytical proof or a paper PDF.

The program checks byte consistency and reruns finite controls. A successful run is **not a proof of the general analytical theorem**, a formal machine proof, human peer review, a priority certificate, or a resolution of the stricter allocation-only Cox question. Read [CLAIM_SCOPE.md](CLAIM_SCOPE.md) before interpreting any result. Historical phrases inside unchanged scripts or expected stdout do not override that scope statement.

## Reproduce

Use Python 3.9 or newer with assertions enabled and **Sympy==1.14.0**. The development replay used Python 3.9.6 and Sympy 1.14.0. The verifier uses only the Python standard library; the three controls require Sympy. A Python without Sympy fails the dependency probe and cannot complete verification.

From the directory containing this package, create the environment **outside** the package, then run:

```sh
python3 -m venv verification-venv
verification-venv/bin/python -m pip install -r verification/requirements.txt
verification-venv/bin/python -E -B verification/verify_package.py
```

If the extracted folder has a different name, substitute that name for `verification`. On Windows, use the environment's `Scripts/python.exe` in the same commands. Paths with spaces must be quoted. The verifier resolves the package relative to its own file, so the current working directory is otherwise immaterial. Keep the environment and new files outside the package.

The expected final status is `PASS_FINITE_CONTROLS_AND_PACKAGE_HASHES`. The three assertion totals are 18,814, 75,172, and 186,869. Each complete stdout must match its stored expected file byte for byte, including whitespace and the final newline; stderr must be empty and each process must exit successfully. The verifier launches children through its own explicit interpreter with `-E -B`, ignoring Python environment settings and avoiding bytecode artifacts. It rejects an optimized parent interpreter (`-O`, `-OO`, or optimization inherited without `-E`) because the unchanged controls use Python assertions.

## Integrity and limits

`manifest.json` covers every public regular file except **itself**. That is the sole, explicit, nonrecursive self-hash exception. The checker also requires the exact declared file set, rejects symlinks, and checks its own source against the manifest. The project's separate closure record pins the manifest and deterministic ZIP; no self-contained manifest can authenticate itself against coordinated modification. These are consistency checks, not a cryptographic signature or a guarantee of mathematical correctness. Read-only file modes are set in the prepared payload but are not required by the portable verifier.

The controls are exact finite computations (rational arithmetic and symbolic matrix rank), not floating-point approximations. Their finite success does not establish arbitrary ambient measurability, sigma-finite measure arguments, infinite-group identities, or Haar-period analysis. Those require the accompanying analytical proof and independent mathematical scrutiny.

No publisher PDF, API receipt, native private execution receipt, or internal research file is redistributed here. Public metadata records source and output hashes without local private paths. No external publication action is performed by this package.
