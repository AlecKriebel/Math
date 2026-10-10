# KP-4.26: punctured homology 3-spheres in S⁴

**Unresolved after five substantive approaches.** No universal proof or counterexample is claimed.

The main useful reduction is Y₀ ↪ S⁴ if and only if Y # (−Y) ↪ S⁴. A diagonal-circle surgery gives an ambient homotopy 4-sphere for a weight-one group, but does not prove that ambient sphere is smoothly standard. Additional group-killing surgeries incur b₂ = 2r. Established cyclic-branched-cover examples are credited to Zeeman.

- PROOF.md: complete elementary reductions, exact surgery calculations, known-result boundaries, and remaining gaps
- ATTEMPT_LOG.md: five mathematical approaches and their outcomes
- SOURCE_GATE.md: exact primary question, proof-access boundaries, and bounded prior-work checks
- SOURCE_HASHES.json: fingerprints of locally inspected primary/reference PDFs, without redistributing those PDFs
- verify.py and verification.json: deterministic finite algebra controls
- STATUS.json: machine-readable outcome
- SHA256SUMS: frozen public-file manifest

Run from this directory with Python 3:

    python3 verify.py > replay.json
    cmp verification.json replay.json
    sha256sum -c SHA256SUMS

The checks use only the standard library and perform no network access. They are diagnostics, not a formal verification of smooth topology. No source PDF, corpus, or private research record belongs in this package. Any separate review should state its own scope; this author packet itself does not claim independent review or human peer review.
