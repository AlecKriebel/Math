# Verification of the independent audit

The mathematical acceptance rests on the field, cohomology, valuation, and square-field arguments in the audit report. The submitted proof was read independently; the author's algebra program was not used as a theorem prover or as the basis for acceptance.

A separate standard-library-only implementation of characteristic-two polynomial and rational-function arithmetic checks 25 finite identities and adverse controls. All 25 pass under ordinary Python, Python `-O`, and Python `-OO`. Checks include the two Artin–Schreier changes, logarithmic differentiation, inverse-root and norm identities, the generic rank-one coefficient determinant, wrong powers, wrong differentiation, wrong norm inversion, the exponent-one degeneration, and the absorbing Pfister slot. A finite valuation grid is only a regression check; the audit proves the relevant parity inequalities for all valuations.

An intentionally incorrect expectation makes the program fail with nonzero exit status under all three Python modes. No correctness decision is implemented with a Python assertion.

Artifact hashes and exact inventories verify integrity only. They are logically separate from mathematical acceptance. Source PDFs and extracted third-party text, executable code, raw test output, and private coordination are excluded from the public authored material. Public source-identification hashes do not establish mathematical truth or novelty.
