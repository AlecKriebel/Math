# Independent control receipt

Executed UTC: 2026-10-16T04:17:25.043459+00:00

The audit authored and ran check_quantifiers.py without reading or importing the submitted verify.py or any family-authored code. Shared thirdparty runtime packages mpmath 1.3.0 and SymPy 1.14.0 were imported after root supplied their location. Mathematical/source approach independence does not claim independent implementations of those thirdparty numerical libraries.

Python: 3.14.6 (main, Jun 10 2026, 10:03:53) [Clang 21.0.0 (clang-2100.0.123.102)]

Checker SHA256: `807d540ae9de0b26cc4e38e3e6df675964c8dcd704334189db3ebc934d602371`.

The exact successful command, from any directory, was:

```sh
python3 -E -B -P -S /Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr200_5100007/math_source_family_01/check_quantifiers.py --packages /Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr200_5100007/math_algebra_family_01/runtime_packages --output /Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr200_5100007/math_source_family_01/check_results.json
```

For use elsewhere, provide any installation directory containing mpmath 1.3.0 and SymPy 1.14.0 through --packages, or omit that argument when both packages are importable. The program itself requires no network or Git operations and writes only its requested JSON output.

Result: process exit 0. Exact symbolic residual zero. 51 primitive families, 3 phases per family, 65 decimal digits; all asserted diagnostic thresholds passed. Max relative product spread 5.1869538811212900658072585897482191e-64. Negative control's nominal 12-cover relative variation -0.001248176836349520260262414234984091. Full observations and versions are recorded in check_results.json.

Exact proof versus diagnostics: DERIVATIONS.md proves the all-N theorem and cover nonconstancy analytically. Numeric values are not interval-certified. Rational-orbit tests are exact but bounded to N<=100; the unbounded parity argument is written separately. No finite check is promoted as proof of all N.
