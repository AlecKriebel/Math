# Author packet: lattice-circle separations

Status: unsolved, five routes. The three-point subquestion is proved as a credited consequence. Larger sharp squarefree clusters remain unresolved.

Read REPORT.md for all proofs, dependencies and gaps; STATUS.json for the scope. Run `python -B exact_checks.py` for finite exact controls. Normal, -O and -OO all use explicit exceptions, with the same expected mathematical output. The expected output is CHECK_RESULTS.json. Tests do not replace universal proofs or the published squarefree-value theorem.

Run `python -B verify_packet.py --manifest-sha256 PIN` using the manifest SHA-256 supplied separately. The pin must come from the delivery receipt; trusting a replaced manifest alone is insufficient. The validator enforces the exact flat inventory and replays the mathematical controls without writing to the packet. No source PDFs, extracted source text, screenshots or raw datasets are present.

Independent audit pending. AI-assisted, unrefereed, no novelty or full-resolution claim.

Run `python -B test_packet.py --manifest-sha256 PIN` for all three interpreter modes, read-only relocated positive replays, and thirteen hostile controls per mode. PORTABILITY_RESULTS.json records the expected labels and counts.
