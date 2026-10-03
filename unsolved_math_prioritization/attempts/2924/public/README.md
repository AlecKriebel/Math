# KP-4.48: contractibility of relative homeomorphisms

This packet investigates UnsolvedMath ID 2924 / K3 Problem 4.48. The general question remains unresolved after five substantive attempts. It contains no claimed new proof or counterexample.

- `PROOF.md`: exact target, proofs of the elementary reductions/special case, five routes and their gaps
- `SOURCE_GATE.md`: original-source identity, corrected references, prior-attempt checks, and theorem-scope boundaries
- `ATTEMPT_LOG.md`: five substantive attempts and the surviving obstructions
- `STATUS.json`: machine-readable outcome
- `verify.py`, `verification.json`: deterministic exact-arithmetic consistency tests
- `SOURCE_HASHES.json`: URLs and SHA-256 hashes of inspected source PDFs; the papers themselves are not included
- `SHA256SUMS`: hashes of the authored public packet

To reproduce the checks with Python 3.10 or newer:

```sh
python3 verify.py > /tmp/kp448-verification.json
cmp verification.json /tmp/kp448-verification.json
sha256sum -c SHA256SUMS
```

The code uses only the Python standard library. It checks an explicit rational family of boundary-fixing cube homeomorphisms, its Alexander deformations and inverses, and the dimension inequalities in a cited theorem. It does not verify deep topology results, compute the unknown homotopy groups, or settle the general question. No source PDFs, page images, extracted articles, or catalogue corpora are redistributed.
