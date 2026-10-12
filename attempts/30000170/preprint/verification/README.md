# Nonunique nearest stable complex quadratics: verification materials

Author: Alec Kriebel, independent researcher, ORCID https://orcid.org/0009-0001-9320-500X.

This archive accompanies an unrefereed research note dated 11 October 2026. The manuscript source contains the complete proofs. It answers the historical complex coefficient stable-set projection question in degree two; it makes no firstness or present-openness guarantee. Stability includes roots on the imaginary axis. All coefficient metrics in the projection theorem are fixed positive-definite real inner products.

The proofs establish multiple attained global nearest stable coefficient polynomials arbitrarily close to z², in both monic and full exact-degree complex quadratic spaces. They also establish failure of whole-epigraph set prox-regularity. The separate monic quadratic function result is positive: function prox-regularity holds at the origin relative to each finite limiting subgradient. Its neighborhood and curvature bound can depend on that subgradient.

From the extracted archive directory, with Python 3.10 or later and no third-party packages:

```
python3 verify_exact.py
python3 verify_function_boundary.py
python3 check_archive_hashes.py
```

`verify_exact.py` checks 2,005 exact rational assertions about root factorization, all four monic and all six full-degree real derivatives, the cubic support and quartic distance, the limiting epigraph covector, and an explicitly mixed positive-definite metric. Its complete stdout should equal `expected_exact.json` byte for byte. `verify_function_boundary.py` uses the standard-library Decimal implementation at 90-digit precision with a fixed seed. Its stdout should equal `expected_function_boundary.json`; it checks 45 scalar boundary cases, 1,200 coefficient supports, six adverse-curvature zero-set cases, and eight horizontal epigraph-normal controls. These numerical controls are not interval-certified calculations and do not substitute for the exact proofs.

The finite scripts do not verify the entire analytic proof, infer a limit from sampled points, search all multiplier degrees, or compute a nonunique input and its minimizers. The limiting-normal argument, every-fixed-metric conclusion, projection equivalence and compact localization are written in the manuscript. The real monic quadratic orthant is a boundary control, not the domain of the complex counterexample. The positive finite-subgradient proposition is compatible with the negative whole-epigraph theorem.

The archive includes the LaTeX source, authored source/priority memorandum, publication metadata, both scripts and expected outputs, license notice, and a hash manifest. It contains no copyrighted source PDFs or full texts, credentials, imported problem-record dumps, or spreadsheet data. LaTeX dependencies are standard: article, geometry, amsmath, amssymb, amsthm, mathtools, microtype, fontenc, lmodern and hyperref. Compile the standalone source with an ordinary LaTeX engine or Tectonic. The published PDF is distributed separately alongside this archive.

AI tools were used extensively in research, exact checks, source auditing, writing and independent adversarial reviews. Those reviews are not human peer review, and no proof-assistant certification is claimed. The author is responsible for the work. No outside individual was contacted. Original paper and verification materials: CC BY 4.0.
