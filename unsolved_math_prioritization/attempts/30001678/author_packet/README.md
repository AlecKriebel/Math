# 30001678 — Smoothness on Products of Perfect Sets

**Outcome: unresolved after five distinct approaches.** This is a restricted-results investigation, not a proof, counterexample, or verified prior resolution of the general source question. No novelty or global-openness claim is made.

The source is Zapletal's Question 2, printed page 100 of OWR 02/2011, in his report on joint work with Kanovei and Sabok. The question asks for Borel smoothness on a countable product, not analytic differentiability.

Contents:
- `PROOF.md`: full restricted proofs and exact obstructions
- `APPROACH_LOG.md`: five mathematical routes, outcomes and remaining obligations
- `SOURCE_STATUS.md`: exact source scope, prior-work checks and literature limits
- `source_verification.json`: public-source identities, byte counts, SHA-256 hashes and inspection history
- `verify_examples.py` and `example_results.json`: exact finite/symbolic example controls; not a proof of infinite results
- `verify_packet.py` and `MANIFEST.json`: strict packet integrity check and adversarial file-boundary tests

Run with Python 3.11+ and its standard library:

    python3 -B verify_examples.py
    python3 -B verify_packet.py --self-test

Compare the first command's complete output with `example_results.json`. The second also performs that comparison. The manifest does not hash itself; its SHA-256 must be recorded by the independent reviewer or other external receipt. Mathematical review remains separate from these checks.

No source PDFs, source text extracts, screenshots, corpus rows, or private coordination records are included. The exact live unsolvedmath page could not be inspected; the primary OWR formulation was read and its page visually checked. An independent mathematical audit and final release decision are still required.
