# Canonical Hochschild BV classification: 30005740

For every characteristic-zero field and nonzero polynomial h, the canonical Hochschild Gerstenhaber algebra of A_h admits a BV generator iff h is squarefree. Repeated factors exclude any degree-minus-one bracket generator; squarefree h admits Δ=0. See RESEARCH.md and AUDIT.md for the proof and exact scope. The actual embedded subalgebra at h=0 is k[x] and is outside the theorem.

Run from this directory:

    python -B verify.py
    python -B -O verify.py

Requires Python 3.9+ and SymPy. The verifier uses explicit RuntimeError checks, enforces the exact file inventory (including rejection of nested MANIFEST files and symlinks), checks hashes/sizes, reconstructs the exact assertion-to-runtime-check AST transformation with original conditions and control-flow provenance, compares complete JSON outputs in normal and optimized modes, and checks actual derivation-polynomial, bracket, and cup corruptions in both modes.

The manifest excludes only its own root file. A separately recorded manifest hash anchors the delivered package; the manifest is not a cryptographic signature. Finite symbolic tests are not a substitute for the general proof. No novelty, peer-review, or proof-assistant certification is claimed.

Only authored mathematical analysis, verification scripts/results, acceptance reports, and public verification metadata are included. No copied source PDFs/text or dataset contents are distributed. The original manuscript acceptance hash remains recorded; publication-only redactions and code hardening are documented in PUBLICATION_PROVENANCE.json. Source gate status is historical source-recovery status, not the mathematical verdict.
