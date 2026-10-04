# 20001587: amenable clopen restrictions

**Unsolved after five substantive approaches.** This is an AI-assisted, unrefereed partial-results packet for AIM *Amenability of discrete groups*, Problem 2.1. No historical-novelty claim is made.

Start with [PROOF.md](PROOF.md). Its central exact reduction identifies the universal question with binary-amplification stability. It also proves local transport, the credited invariant-measure extension, amenable finite-partition stabilizers and their coamenability gap, and countable reduction. Two counterexamples only test the necessity of hypotheses; neither answers the original question.

[SOURCE_GATE.md](SOURCE_GATE.md) establishes the original scope and records prior-work checks. [ATTEMPT_LOG.md](ATTEMPT_LOG.md) records the five mechanisms and exact gaps. Independent review is pending at author freeze.

## Reproduce

Python 3.12, standard library only:

    python verify.py > /tmp/amenable-clopen-verification.json
    cmp verification.json /tmp/amenable-clopen-verification.json
    sha256sum -c SHA256SUMS

All 609,078 indexed finite checks pass. These are bounded permutation, partition and exact-rational controls; they do not certify any infinite amenability assertion. No network access or third-party source copy is needed to replay them.

The author-frozen allowlist is FROZEN_MANIFEST.json. Source PDFs, source HTML, extracted source text, screenshots, datasets and private working files are excluded. Publication requires a separate fresh review and is draft-only; this packet makes no assertion about later publication status.
