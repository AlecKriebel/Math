# Jet Spanning by Nef Toric Vector Bundles

**Proposed disposition: already_solved, 1/5 substantive author turns.** The primary conjecture is false by a published counterexample of Di Rocco–Jabbusch–Smith. This is a prior-result verification, not a new counterexample or an unresolved five-approach packet. Independent review is still required before acceptance or publication of this packet.

Their rank-three toric bundle on P²_C has invariant-curve splitting types (4,3,1), (5,2,1), (6,1,1), so the report's τ equals one. It is nef but its value evaluation has rank two at one fixed point. Hence it cannot span first jets there, contradicting the conjectured implication at k=1. The exact first-jet rank is seven out of nine.

- PROOF.md: full attributed construction, proof, numerical certificate and scope.
- SOURCE_GATE.md and SOURCES.json: primary-source inspection, provenance, site-access and source-comparison limits.
- APPROACH_LOG.md: early stopping upon prior resolution; no invented extra attempts.
- VERIFY.py and RESULTS.json: reproducible exact checks using Python 3's standard library only.
- CHECK_PACKET.py and MANIFEST.json: strict file integrity and byte-for-byte replay.
- STATUS.json: machine-readable scoped disposition.

Run `python3 CHECK_PACKET.py` from this directory. It checks every frozen file, exact output reproduction, and three destructive-change controls in temporary copies. Run `python3 VERIFY.py` separately to see the mathematical check result. No network is used by either script, and the frozen directory is never modified.

The journal and arXiv v3 polygon coordinates agree with the filtration-derived construction. The verifier rejects a deliberately sign-flipped coordinate as a synthetic negative control.

No downloaded source PDFs, full text extracts, source images, full catalogue, raw selected records, or private coordination materials are included. The packet contains original verification prose, exact arithmetic code and public verification metadata only. No repository, branch, PR, queue, merge or release was changed during its preparation.
