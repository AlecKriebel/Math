# Brownian first-visit cells on a circle

Research note, version 1.0, Alec Kriebel, 7 October 2026. ORCID: https://orcid.org/0009-0001-9320-500X.

The manuscript gives the complete joint law in an explicit Laplace-series format for every finite number of independent continuing Brownian walkers, including the two seed schemes in Georgakopoulos’s question. The proof, coefficient definitions, and outer-series remainder are in `brownian_first_visit.pdf` and its standalone LaTeX source. A named density, efficient evaluator, and certified inner numerical integration are not claimed.

The intended Zenodo upload is exactly the PDF plus `brownian_first_visit_support.zip`, using the unchanged `metadata.json` object inside `zenodo-deposit.json`. The support archive contains the standalone manuscript source, metadata, source provenance, five portable diagnostic families, their recorded reproduction, and bounded priority/source comparisons. Its complete member hashes are listed in `SUPPORT_MANIFEST.json`; the surrounding repository package manifest additionally pins the exported PDF and archive. Full third-party papers and private research caches are excluded.

Run the supporting checks on a POSIX system with an existing Python 3.11+ interpreter and an existing library environment providing mpmath 1.3.0 and SymPy 1.14.0:

```text
python verification/run_diagnostics.py --stdlib-python /path/to/python --library-python /path/to/library-python --output-directory ../my_brownian_checks
```

The runner creates a new output directory outside `verification`, checks the full verifier source manifest, runs every family normally and with optimization, compares complete scientific results to preserved baselines, and tests true/false diagnostic guards. Exact finite-state controls and high-precision scalar comparisons are supporting diagnostics, not a Brownian proof or uniform numerical-error certificate. The mathematical proof is the manuscript.

`verification/reference/JOINT_LAW.md` is byte-exact submitted history from September 30. Its then-pending-review/priority header is historical. The current manuscript and `priority_and_provenance.md` contain the updated attribution and bounded-audit conclusions. Initial mathematical reviews and the priority audit under `audits` are dated source records, not conventional human peer review. Full original diagnostic source copies and precise portability changes are under `source_history`.

AI tools were used extensively in solving, drafting, reproducing, and adversarially verifying the work. This preprint is unrefereed and has not undergone conventional human peer review. All authored package materials are offered under CC BY 4.0; cited third-party works retain their own rights.
