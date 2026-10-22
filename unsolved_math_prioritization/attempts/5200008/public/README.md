# Reflection-only billiard density: partial results

Problem 5200008 / AMR-051-0008 remains **unsolved after five substantive attempts**.

PROOF.md proves a conditional one-inverse reduction, exact circle/concentric-family obstructions, and a bounded-word perturbation barrier. It also gives an exact abstract matrix control showing why a naive shear-sign obstruction does not survive arbitrary long symplectic products. These do not settle the question with arbitrary nearby reflecting hypersurfaces.

- PROOF.md: complete retained mathematical arguments and exact remaining gap
- SOURCE_GATE.md: source match, checked versions and scope limitations
- ATTEMPT_LOG.md: five approaches and outcomes
- verify_exact.py and verification.json: portable finite exact controls
- SOURCE_HASHES.json: hashes of inspected primary PDFs, which are not redistributed
- STATUS.json: machine-readable disposition
- SHA256SUMS: frozen author-file manifest, excluding itself

Run `python3 verify_exact.py` and compare its output with verification.json. Check the frozen packet with `sha256sum -c SHA256SUMS`. The verifier needs only Python's standard library. It does not settle the full density statement or certify optical realizability of the matrix example.

This packet makes no novelty, priority or human-peer-review claim. Independent review is pending at the time of this author freeze.
