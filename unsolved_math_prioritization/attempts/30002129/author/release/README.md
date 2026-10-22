# 30002129 — Refined slippery bounds

**Unresolved, 5/5 approaches. Independent review pending.**

Read RESULT.md for the exact target, proofs of scoped partials, countercontrols and remaining gap. APPROACH_LOG.md distinguishes the five routes. SOURCE_VERIFICATION.json records only public bibliographic, retrieval and inspection metadata. REPOSITORY_CHECK.json records bounded read-only repository checks.

Chowdhury's 2018 Proposition 6.2.2 already proves the matching-input/output-denominator case. The broader refined conjecture is not solved here. No novelty, exhaustive current-openness, human-peer-review, or formal-proof-assistant claim is made.

Reproduce the arithmetic controls with:

    python3 -B verify_math.py

The frozen output is MATH_CHECKS.json. Python 3.10+ standard library only. These finite controls do not replace the written proofs or the credited positive-word model theorem.

For strict byte inventory verification, supply the manifest SHA-256 obtained independently from the review handoff:

    python3 -B verify_bundle.py --expected-manifest SHA256 --replay --self-test

The verifier rejects extra paths, missing/changed files, directories and symlinks, and pins the manifest through the supplied hash. No self-contained package authenticates a substituted verifier plus substituted external hash; the review handoff or eventual reviewed Git commit is the trust anchor.

Only authored analysis, code, result logs and public verification metadata are included. Source PDFs, extracted texts, images, raw corpus records, private sources and private coordination are excluded. No remote write was made for this investigation.
