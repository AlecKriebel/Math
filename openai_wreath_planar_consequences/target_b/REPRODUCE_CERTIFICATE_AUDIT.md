# Reproducing the certificate audit

The decisive authored checkers are independent_validated_integrals.py and independent_scalar_checks.py. They contain the exact mathematical input tables, import no upstream verification implementation, and need Python 3.12 plus python-flint==0.9.0. Their receipts use complete Arb balls and reject an inequality unless its whole enclosure meets the threshold.

From a clean copy of these files, create a virtual environment, install requirements.txt, then run the two checkers with assertions enabled:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -B independent_validated_integrals.py
.venv/bin/python -B independent_scalar_checks.py
```

Do not use -O or -OO. The full validated-integral checker must report full_finite_gates="pass", with coverage of 51 finite nodes, two matrix signs, 102 residual pairs, 84 half-gap intervals and 2436 Bernstein inequalities. An earlier partial receipt, an interrupted run, or a success label with smaller coverage is insufficient. The scalar checker must report status="pass".

The full integral replay can take several minutes. It uses adaptive Arb integration of each analytic spectral piece; it therefore independently avoids the source's fixed Fejér rule and its quadrature-remainder assumption. Both algorithms still depend on correct Arb library ball arithmetic. This numerical verification cannot replace the written proofs in CERTIFICATE_AUDIT.md: the exact ℓ¹ inversion, Schwartz regularity, Fourier pairing, lower-jet cancellation, interpolation-node coverage and unbounded signs are analytic steps.

The supplied verifier's receipts are retained under computational_receipts/. They were produced from the immutable sources recorded in source_receipts.json. The full primary verifier's finite moment sums use Fejér quadrature with a manuscript-proved analytic error allowance. The optional supplied rational receipt covers only the initial 6×6 block.

independent_numeric_system.py is optional nonrigorous exploration. It requires NumPy 2.3.5 and uses different Gauss-Legendre quadratures to assemble and solve the finite system. Agreement of those floating-point computations is not a global sign proof and is not a publication gate.

The pinned manuscript and comparison-extracted text were inspected but are not included in the authored audit package. Their hashes, canonical upstream source and version-history query are in CERTIFICATE_AUDIT.md and source/version receipts. The imported claim remains credited to OpenAI. No formal proof or conventional human review is claimed.
