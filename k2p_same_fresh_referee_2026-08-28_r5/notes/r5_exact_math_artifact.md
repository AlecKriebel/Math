# R5 independent exact-mathematics artifact

Date: 2026-08-29 (America/Los_Angeles)

Status: **PASS**.

This is a fresh, review-owned spot check. It imports no submitted code,
classifier, graph generator, certificate ledger, or expected-output file. All
comparisons use `fractions.Fraction` or exact SymPy expressions; floating-point
samples are not used as proof.

The check independently reproduced:

- completion subtotals and `C(4,1)=831`, `C(4,0)=C(5,1)=1983`,
  `C(5,0)=4155`, plus the 405,216, 2,946,240, and 13,440 raw totals;
- strict `D_plus` margins at four rational boundary-near points, all sixteen
  paired products, the symbolic nonautomatic product-gap identity, and a
  four-factor marginal section at the continuous-time boundary-near target;
- the ordinary-triangle common tensor coordinates and exact block
  determinants `-1/2`, `-1/4`, with product `1/8`; and
- both representative weak-sharpness tensors, their exact named 9-by-9
  determinants, and the cherry determinant with witness value `2464/675`.

Command:

```text
/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-28_r5/execution/k2p_principal_d_plus_submission_referee/.venv/bin/python -B independent_checks/math/r5_exact_math_checks.py
```

The command ran once from the R5 review root. Exit status was 0, wall time was
0.510515 seconds, user time was 0.382427 seconds, system time was 0.043886
seconds, and peak RSS was 66,895,872 bytes. Standard error was empty. The
result's canonical semantic payload SHA-256 is
`cd4fc393575618cdd4ca627413d140408d48dd75d6047b98b3d45f9fde9a9a87`.

Artifact SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| `independent_checks/math/r5_exact_math_checks.py` | `03b1582a865e661a81dd886e7b50fc5b4bc502ffbbf813c7b0a6f64f2c861b18` |
| `independent_checks/math/r5_exact_math_checks_result.json` | `5cf3cecf911e6464821b6417f3a04313cbd7feb635e5c82b051b7ddcf5842ca6` |
| `evidence/math/r5_exact_math_checks.execution.json` | `f6304dfaf3b20c43ff728a1b916c652356e7c4164c6c3c0e498da29414e84023` |
| `evidence/math/r5_exact_math_checks.stdout` | `7784bfc8bd30f393794acbe9c588c5f1b060807bc6dc4c1356869823e010b68d` |
| `evidence/math/r5_exact_math_checks.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

This artifact independently tests representative exact identities. It does not
claim to replace the separate exhaustive finite-universe replays.
