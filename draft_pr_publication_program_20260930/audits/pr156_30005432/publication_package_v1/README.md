# A counterexample to ideal closure of property-(s) elements in skew braces

Alec Kriebel, independent researcher. ORCID 0009-0001-9320-500X.
Formal preprint version 1.0.0, 12 October 2026. CC BY 4.0.

The manuscript proves a negative answer to Colazzo's unrestricted OWR Question 1. Its additive group is Z×Z/4Z, multiplication is (n,c)∘(m,d)=(n+epsilon(c)m,c+d+2cd mod4), and epsilon=(1,1,-1,-1). The exact property-(s) set is Z×{0,1}. The element (0,1) has both original indices2; its additive double has both infinite. The infinite-coset proof in the manuscript establishes infinitude for all integers. Finite quotients cannot establish the failure: every finite brace has property(s) globally.

The finite brace, standard semidirect construction and high-bit character are old. This is an explicit elementary application, not a new construction method or characterization. The manuscript credits the relevant antecedents and Alper Ferudun's exact matching October11 preprint (DOI10.5281/zenodo.23292254). GitHub records PR156 createdSeptember30 at12:24:37UTC, with the preserved proof already present. Original commit dates are author-supplied and distinct from the provider PR date; current public repository visibility was verified, historical visibility was not independently archived. The formal preprint date is not backdated.

“Contemporaneous separate discoveries” means separate disclosures in the same period. Mutual independence and a literally simultaneous release are not established. Historical novelty, first priority and exclusive resolution are not certified. The bounded audit found no explicit earlier negative answer in the full bodies read. Material publisher-body gaps and exact available versions appear in the manuscript and priority reviews. The reviewers' own infinite-module deductions from older finite constructions are distinguished from explicit prior publication of the target answer.

## Files and reproduction

- property_s_counterexample.tex: standalone manuscript and universal proof.
- verify.py: exact finite-factor and integer-coefficient controls, plus bounded checks in the actual infinite brace; all checks raise errors explicitly.
- verify_controls.py: runs ordinary and optimized modes and tests deliberately broken sign/index controls in isolated temporary folders.
- verification.normal.json and verification.optimized.json: recorded33512 controls in each mode.
- negative_controls.json: both deliberate mutations rejected in both modes.
- metadata.json: exact intended Zenodo metadata.
- TIMELINE_RECEIPT.json: source-authenticated disclosure chronology, with stated evidentiary limits.
- priority_reviews/: three independently sealed family reviews and their checkable implications, plus ROOT's full August-paper scope screening.
- SOURCE_LOCATORS.json: primary source versions, locators and access limits.
- MANIFEST.json: byte sizes and SHA256 hashes of archive contents, excluding itself.

Python3.11+ and its standard library are sufficient:

    python3 -E -S -B -P verify.py
    python3 -E -S -B -P -O verify.py
    python3 -E -S -B -P verify_controls.py

The last command writes the three diagnostic JSON outputs in the current package directory. Use a copy to preserve the deposited bytes. The controls reproduce the stated operations, indices and symbolic coefficients. They do not replace the universal proof, certify literature absence, or independently recertify unrelated imported source theorems. The source hash in each output identifies the manuscript bytes tested alongside the checker; it is not a formal proof checker for the LaTeX prose.

The original September30 proof is preserved in the repository audit. Its mathematical construction did not need essential repair. The original assert-based checker was unsafe under optimization; the distributed checker uses raised checks. A subsidiary source-map discussion was qualified separately; this note does not claim to refute the full source theorem.

AI tools were used extensively in solving, drafting, source comparison, reproduction and adversarial verification. The work is unrefereed and has not undergone conventional human peer review. The author is responsible for its contents. No outside individual was contacted on behalf of the project. Third-party source bodies and private retrieval headers are excluded.

