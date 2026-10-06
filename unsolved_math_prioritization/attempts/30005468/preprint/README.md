# A fixed moment separator without a rational normalized sum-of-squares certificate

This archive supplements Alec Kriebel's research note dated 6 October 2026. It contains the manuscript source and exact data for an explicit instance of the phenomenon asked about in the fixed-polynomial question in Oberwolfach Report 14/2023, using rational polynomial square factors.

The example applies Scheiderer's classical quartic and a classical local leading-form obstruction. The claim concerns the fixed polynomial p=1+f on the three-variable unit ball at minimum one. The moment input is not positive semidefinite. Another polynomial q=1+x^4 certifies the same input rationally, p itself has a rational positivity certificate, and rational rescaling cp with c>1 removes the normalized obstruction. Read CLAIM_SCOPE.md and the manuscript for these essential limits.

## Reproduce the exact controls

Use Python 3.8 or later and its standard library, with no network connection or external packages:

```text
python3 verify_package.py
```

Run this from an unmodified extracted archive. The verifier first checks the exact file inventory and every SHA-256 digest in manifest.json, then starts verification/check_exact.py with isolated Python and bytecode writing disabled. Its complete standard output must equal verification/expected_result.json byte for byte, its error output must be empty, and its exit status must be zero. It also checks agreement among the exact data, manuscript title, source provenance, and publication metadata. The expected finite-check result is PASS with 2,059 exact assertions and no floating-point diagnostics.

These checks cover the quartic norm identity, finite-field factorizations, the explicit real-SOS identity modulo its cubic, the rational moments, and representative interpolation and leading-form controls. They do not prove an all-degree assertion by finite search, establish real positivity by sampled values, or replace the manuscript's Galois and local proofs. No proof-assistant certificate is supplied. The archive does not reproduce computations reported by authors of cited sources.

## Contents

- paper.tex: the standalone manuscript source; the rendered PDF is supplied separately with the preprint record.
- CLAIM_SCOPE.md: the exact claim, hypotheses, boundary cases, and excluded stronger conclusions.
- PRIORITY_NOTE.md: the dated bounded literature comparison and explicit access and version limits.
- data.json: all 35 rational moments and sparse coefficient data for f, g, p, and q.
- SOURCE_VERSIONS.json: cited primary versions, inspected scopes, and checker provenance.
- verification/check_exact.py and verification/expected_result.json: portable exact controls and their complete expected output.
- verify_package.py: file integrity, consistency, and child-checker verification.
- record_metadata.json: the publication metadata accompanying this note and archive.
- manifest.json: hashes for every archive file except itself. It is an integrity inventory, not a digital signature or independent mathematical certification.

Third-party articles, extracted article text, screenshots, private credentials, and repository execution receipts are not distributed. Sources are linked in the manuscript and priority note. The final manifest records the final manuscript's exact bytes; preliminary manuscript hashes are not substituted for it.

## Disclosure and license

AI tools were used extensively in developing the application, literature comparison, exact computation, writing, and adversarial checking. This is an unrefereed preprint without independent human peer review or formal proof-assistant certification. The bounded priority audit does not certify worldwide firstness, current openness, or the originating authors' unpublished intention or approval.

Author: Alec Kriebel, independent researcher. ORCID: https://orcid.org/0009-0001-9320-500X. Version 1.0. The note and the original supporting assets in this archive are released under Creative Commons Attribution 4.0 International (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/.
