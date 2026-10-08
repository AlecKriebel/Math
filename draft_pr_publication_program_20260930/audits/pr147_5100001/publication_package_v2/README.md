# Exact correction to the printed k107 product

Research note version1.0, Alec Kriebel, 7 October2026. ORCID https://orcid.org/0009-0001-9320-500X.

The manuscript decisively refutes the literal product in the unproved Table2 entry at primitive N=4. Both exact convex trajectories belong to one continuous fixed-confocal-caustic family. This is a source-specific correction; no quotient replacement or corrected all-period invariant is proved.

The four-period construction and area identities are prior work of Garcia–Reznik. Ferudun DOI10.5281/zenodo.23075934 supplies the same contemporary correction. The original PR's September30 provider chronology precedes that retrieved October1 record, but establishes neither exclusive priority nor independence. See priority_and_provenance.md for sources and search/access limits.

Upload exactly k107_counterexample.pdf and k107_counterexample_support.zip with the unchanged metadata.json object in zenodo-deposit.json. SUPPORT_MANIFEST.json inventories every support member; the outer repository package manifest also pins the final PDF and ZIP. Third-party full texts, screenshots, ZIPs, private caches and operational staging files are excluded.

On POSIX, with existing Python3.11+ and a separate existing Python environment containing SymPy1.14.0, run:

```text
python verification/run_diagnostics.py --stdlib-python /absolute/path/to/python --library-python /absolute/path/to/sympy-python --output-directory ../my_k107_checks
```

The runner creates a fresh output directory outside this package, validates all diagnostic source pins, copies sources before execution, reproduces all five families normally and under optimization, compares complete scientific results with recorded baselines, and checks that real false-value guards fail under optimization. It installs nothing.

verification/source/author/COUNTEREXAMPLE.md and its inherited replay are byte-exact historical submission text from September30, including then-pending review/priority language. They are not the current publication status. Original calculation code differs only by documented explicit failure-guard repairs. Current attribution and proof are in the manuscript and priority_and_provenance.md. Dated preparatory AI reports are source records, not later whole-package acceptance or human peer review.

AI tools were used extensively in solving, drafting, reproducing and adversarial verification. This is an unrefereed preprint without conventional human peer review. Authored materials are CC BY4.0; cited third-party works retain their own rights.

