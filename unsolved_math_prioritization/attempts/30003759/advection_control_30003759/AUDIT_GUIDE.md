# Fresh independent audit guide

Status requested: audit of a prior-literature source match and elementary retained proofs, not certification of a new original threshold proof.

1. Open the public original OWR PDF, printed pp. 951–952 (PDF pages 11–12). Check the PDE, domain, sign convention, controlled endpoint and homogeneous endpoint. Check that the actual cost in equation (3) uses L² initial normalization, despite the H⁻¹ well-posedness setup.
2. Open arXiv:2609.35355v1. Check equation (1), the cost definition, the infimum definition, Theorems 1.3–1.4 and the sentence following Theorem 1.3. Confirm positive critical endpoint is left open; negative endpoint is included.
3. Confirm preprint/publication status from the arXiv record. A title, abstract, theorem statement and PDF verification do not certify the full mathematical proof. The paper's Sections 3–7 have not all been independently audited here.
4. Read all of `proofs/elementary_controls.md`. Pay particular attention to the control-norm scaling factor |M|^(-1/2), adjoint drift sign, boundary-flux factor ε, terminal state versus initial state in the observability ratio, and exact exponent at T=2.
5. Run both normal and optimized Python checks. They must agree byte-for-byte. Check that the single-mode lower bound is never called a bound from above on the true cost. Single modes and fixed finite discretizations cannot establish a uniform theorem for all data.
6. Check the endpoint countermodels and ensure the final disposition distinguishes a known infimum value from boundedness at the infimum.
7. Verify every manifest entry and the closed file list. This payload contains only authored explanations/proofs/code/check output and public source-verification metadata. Source PDFs, extracts and dataset records must not enter a publication payload.
8. Do not interpret the queued main row or empty search results as a proof of no previous attempt. Do not claim journal acceptance, complete literature absence, or a new solution by this campaign.

Recommended disposition if the checks pass: `prior_resolution_preprint`, with explicit `positive_critical_endpoint_open` qualification and no first-resolution claim. If the catalog requires literal boundedness at an attained minimum rather than its infimum, classify that endpoint part separately as unresolved.
