# Reproduce this independent audit

All scripts are standalone except the forensic diagnostic, which imports this folder's `geometric_audit.py`. Nothing imports the submitted checker or prior-review code.

Use the audit's dedicated runtime at `../reproduction_environment/bin/python` (mpmath 1.3.0, SymPy 1.14.0). From this folder:

```
../reproduction_environment/bin/python real_cartesian_certificate.py
../reproduction_environment/bin/python exact_star_audit.py
../reproduction_environment/bin/python geometric_audit.py
../reproduction_environment/bin/python reproduce_spurious_n4_diagnostic.py
```

The first command reproduces `CARTESIAN_CERTIFICATE.json`, an exact all-real polynomial certificate. The second recreates `EXACT_STAR_RESULTS.json` from a physical tangent/reflection construction. The third recreates `NUMERICAL_RESULTS.json`, the completed 110-digit finite controls. The fourth intentionally reproduces the documented initial diagnostic error and writes `SPURIOUS_N4_DIAGNOSTIC.json`; its `EXPECTED_DIAGNOSTIC_FAILURE` status is expected and is not a theorem counterexample.

`BASE_NUMERICAL_RESULTS.json` preserves the first completed 80-digit, 15-family checkpoint. The final program extends the same generator to 21 families at 110 digits. `ALL_REAL_CARTESIAN_PROOF.md` explains the general proof, while `GEOMETRIC_DOMAIN_REPORT.md` records source agreement, geometric deductions, the directly verified repaired N4 converse, exact singularity evidence, diagnostic history, and disposition.
