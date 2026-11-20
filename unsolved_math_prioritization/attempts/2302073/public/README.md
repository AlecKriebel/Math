# Problem 2302073: known affirmative resolution

Rubel's two-parameter normal-family question, Hayman–Lingham Problem 2.73 / AMR-022-2073, has an affirmative answer in the prior work of [He, Tang and Zhang (21 March 2026)](https://arxiv.org/abs/2603.20883v1).

This packet verifies that construction. It supplies a self-contained attracting-basin parametrization, the normality proof and the obstruction to every entire one-parameter factorization. With the explicit normalization used here, the differential obstruction is identically 1/625. The construction and result are credited to the prior authors; no novelty or priority is claimed.

- PROOF.md: complete attributed proof reconstruction
- SOURCE_GATE.md and SOURCE_MANIFEST.json: exact source, prior-work and access checks
- ATTEMPT_LOG.md and STATUS.json: one-turn investigation and scoped disposition
- verify.py and verification.json: 35 exact supplementary controls
- SHA256SUMS and FROZEN_MANIFEST.json: frozen public-file bindings

Reproduce with Python 3.10+ and SymPy 1.14.0:

    python3 verify.py
    sha256sum -c SHA256SUMS

The output of verify.py should agree exactly with verification.json. Finite algebra checks supplement the analytic proof; no formal proof-assistant verification is claimed. Independent adversarial review is pending at this author freeze. Review files, if later added, must be separately bound without rewriting these frozen artifacts.

Disposition: already_solved, 1/5. This is an AI-assisted, unrefereed verification note. OpenAI tools were used extensively. The packet contains no downloaded scholarly sources or dataset copies. No merge, release, DOI deposit or outside outreach is requested.
