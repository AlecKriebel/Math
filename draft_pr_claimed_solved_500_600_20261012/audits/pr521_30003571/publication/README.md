# Loss of total-space positivity for the normalized relative Kähler–Ricci flow

Author: Alec Kriebel, independent researcher. ORCID: https://orcid.org/0009-0001-9320-500X.

Version 1.0, 12 October 2026. Unrefereed; no human peer review. AI tools were used extensively in development, writing, reproduction, and adversarial review.

## Exact result

For the source's defining probability-normalized flow on O_E(2), with E = O(1) ⊕ O(1) over P¹, the paper exhibits a globally smooth strictly positive initial metric and an exact negative horizontal curvature coefficient −1/96 at time log(2)/2. This answers the total-space positivity-preservation question explicitly stated in Naumann's original report p2443 and published article §3.3. Construction of the flow was already known. No resolution of the Griffiths conjecture or historical first-priority claim is made.

The four-page paper contains the proof, the universal initial positivity certificate, all coordinate transitions, the exact second-variation evolution, and the normalization calibration. The analytic input is the cited smooth finite-time existence theorem. Symbolic checks verify algebra and do not prove that analytic theorem.

## Files and reproducibility

The deposit contains the paper PDF and a verification/source archive. Within the archive, `paper/` contains the standalone LaTeX source and this README; `original/` preserves the PR's authored mathematical and verification materials; `reviews/` contains new independent audit reports and exact checks; `root_reproduction/` preserves rerun results; `MANIFEST.json` records file sizes and SHA-256 hashes. No downloaded source papers, full extracted copyrighted texts, credentials, or private coordination files are included.

Extract the archive and run from its top directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_all.py
```

Run Python without optimization (`-O` or `PYTHONOPTIMIZE`), because the archived original checks use assertions. The wrapper refuses optimized execution. Python 3.9 or later is sufficient. The exact symbolic dependency is SymPy 1.14.0 with mpmath 1.3.0. Verification runs without network access once dependencies are installed. Passing output is evidence for the recorded identities and integrity checks, subject to the analytic and source-scope limitations stated above.

To rebuild the PDF, use a LaTeX installation with AMS packages, `geometry`, `lmodern`, and `hyperref`, or run `tectonic paper/positivity_loss.tex`. PDF binary hashes can vary with build timestamps and engine versions; the published PDF has its own verified hash.

## License and provenance

The authored paper and package are distributed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/. The archive preserves original draft PR #521 at head `91385a9ba0d445a2fae4629cd60b70026584e24b`; historical frozen manifests refer to those preserved originals. The current package manifest describes the delivered source archive. Original material was audited against the primary sources linked in the paper; the bounded priority audit and its access limits are included.

The fresh source audit recorded 76 searches and independently retrieved 19 primary PDFs. A relevant 2025 Naumann habilitation was identified through an institutional page, but its full text was not obtained. That specific lead remains unresolved; publication asserts the proved theorem, without certifying historical first priority. Its text, if available, could help settle the priority limitation. No outside contact or outreach was prepared.
