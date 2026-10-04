# AMR-026-0004: eternal compressible Euler flow

Rank 561, catalogue ID 2700004.

**Outcome:** a literature-known affirmative example for the unrestricted classical, non-isentropic full-Euler formulation. No novelty claim and no claimed resolution of isentropic or bounded-entropy variants.

- [PROOF.md](PROOF.md): complete direct and kinetic verifications, finite mass/energy calculations, arbitrary-\(\gamma\) affine extension, and the exact regularity limitation.
- [SOURCE_GATE.md](SOURCE_GATE.md): primary question, prior-publication mapping, earlier-report correction, repository duplicate checks.
- [ATTEMPT_LOG.md](ATTEMPT_LOG.md): one substantive source-driven reconstruction and stopping rationale.
- [verify.py](verify.py), [checks.json](checks.json): reproducible exact symbolic checks, supplementary to the written proof.
- [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json): public source URLs, locations, and hashes; no source documents are included.
- [STATUS.json](STATUS.json): scope-qualified status and audit gate.
- [FROZEN_MANIFEST.json](FROZEN_MANIFEST.json): SHA-256 author freeze.

Run:
\`\`\`sh
python3 verify.py
\`\`\`
Python 3 and SymPy are required; the freeze was checked with SymPy 1.14.0. The script writes a deterministic checks.json beside itself.

The decisive example is already explicit in Fellner–Schmeiser (2007), Section 5, pp.11–12 of the author manuscript. It is smooth with finite mass and energy but has spatially unbounded specific entropy. Independent review is pending. Nothing in this packet authorizes merging, releasing, external outreach, or calling the narrower variants solved.

