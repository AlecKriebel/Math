# 30001182: ambient invariance fails

**Candidate disposition: claimed_solved; 1/5 substantive author turns. Independent audit pending.**

Liebscher's extremal-exchangeable independence can change under a state-preserving ambient inclusion. In the four-point algebra C({0,1}²), the coordinate algebras with the perfectly correlated fair joint state have no extreme exchangeable witness. After diagonal embedding into M₄, a pure vector-state extension gives a pure, exchangeable witness by folding all copies onto M₄.

The subalgebras are distinct and proper with scalar intersection. A separate polynomial/Laurent-polynomial example also demonstrates the source's literal non-lifting concern for unrestricted algebraic *-algebras. The C* distinction and changes to the extremality convention are stated explicitly.

Read [PROOF.md](PROOF.md) for the complete argument, [SOURCE_GATE.md](SOURCE_GATE.md) for exact source scope and prior-work checks, and [ATTEMPT_LOG.md](ATTEMPT_LOG.md) for the single substantive attempt. The established pure-folding construction is credited to Dykema–Köstler–Williams; no historical novelty is claimed.

Run the standard-library-only auxiliary verifier:

    python3 verify.py

Its deterministic output must agree with [checks.json](checks.json): 14,944 exact rational controls. These finite controls supplement the proof; they do not establish the all-state or infinite-copy assertions on their own. [FROZEN_MANIFEST.json](FROZEN_MANIFEST.json) pins the author files. No third-party papers or datasets are redistributed.

This is AI-assisted research, not formal certification or human peer review. The packet awaits independent adversarial review before repository publication.
