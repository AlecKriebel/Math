# Functorial maps between p-local finite-group classifying spaces

Problem 30001052 / OWR-2089-013, rank 966. **Unsolved, 5/5 approaches.**

The complete [authored proof](packet/PROOF.md) and [independent mathematical audit](independent_audit/AUDIT_REPORT.md) are preserved byte-for-byte. The audit accepts the scoped partial results without mathematical corrections. The unrestricted unstable extension question remains open in this work; no global-openness, novelty, priority, human-refereeing or formal-proof claim is made.

Accepted results cover nilpotent targets, coprime-action sources (including normal-Sylow models and abelian Sylow sources), every fusion-preserving map in the nine named D8/Sigma_4/A_6 pairs, a conditional centric-image criterion with vanishing lim^2 Z_phi, and the diagonal wreath nonretraction obstruction when p divides n. The last result obstructs a method, not the original extension question. The finite calculation is not a classification of all D8 systems.

## Portable offline verification

Use Python 3.9+ and SymPy 1.14.0 (requirements.txt). From this directory, run:

    python3 -B verify_publication.py
    python3 -O -B verify_publication.py
    PYTHONOPTIMIZE=2 python3 -B verify_publication.py
    python3 -B mutation_tests.py

The verifier checks the closed file inventory, hashes and sizes, fixed author/audit manifest anchors, all original frozen members, the author verifier, and both author and independent checker outputs byte-for-byte. Each child is explicitly run in the same optimization mode. An optional --manifest-sha256 argument checks a separately retained PUBLIC_MANIFEST.json digest. Results are emitted to stdout; redirect them outside this closed packet.

The corruption suite also tests rebound author-checker mutations that reach the mathematical checks and independent-checker mutations, including optimized child executions. All changes stay in temporary copies. It is an integrity/replay control, not a proof checker. A complete malicious rewrite of the verifier and all trusted anchors is outside this model.

## Preservation and source boundary

The 14 author files and all 11 independent-audit files are original frozen artifacts. Historical author labels saying audit pending remain unchanged; PUBLICATION_STATUS.json records subsequent acceptance. The two original ZIPs were checked against their frozen members and retained locally; their public hashes and sizes appear in the status file.

No scholarly PDF, extraction, source image, input dataset content or private coordination record is included. Public source fingerprints and inspection history remain in packet/SOURCE_METADATA.json and the complete audit. The preserved run_audit_checks.py is a historical full audit runner requiring excluded source PDFs and optionally the corpus. The portable runner does not invoke it and does not claim to repeat source inspection or corpus certification.

Puig arXiv:1605.06657 remains excluded as a theorem dependency because it was withdrawn for a fatal proof error. Full foundational proofs remain external. The blocked complete Castellana–Libman paper was not inspected; the 2026 Bova papers were checked at record/abstract level only; the local AKO download is incomplete. Preserve every limitation in the original proof, source ledger and audit.
