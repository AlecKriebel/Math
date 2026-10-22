# Spatially linked polytope skeletons: partial-results packet

Target 30001138 / OWR-3385-009, ranked queue entry 666.

**Outcome: no resolution after five distinct approaches.** There is no candidate full solution. The packet gives proved and exact-computational exclusions of several large classes, and a source-correct account of the unresolved step. No novelty claim is made.

Read `PROOF_AND_PARTIALS.md`, then `APPROACH_LOG.md` and `SOURCE_VERIFICATION.json`.

Run the exact offline controls with Python 3.10 or later:

    python verify.py > replay.json
    python verify_manifest.py

`verify.py` uses the standard library only, has no network calls and does not depend on external datasets or PDFs. Compare the parsed JSON output to `verification_results.json`; both key order and insignificant whitespace are immaterial. It checks three explicit forbidden-minor models, their construction from K6, exhaustive facet-cover certificates for three polygon products, arithmetic controls for six-vertex polytopes, and deliberately damaged negative controls. It does not automatically verify every mathematical argument in the paper.

The additional authored exploratory scripts and their finite outputs are in `exploration/`. Randomized negative searches there are labeled inconclusive and excluded from theorem claims. The search script's default long run is optional; the core verifier replays the final fixed certificates in under a second on the author environment.

This release contains authored mathematics/code and public-source verification metadata only. Third-party PDFs, source excerpts, imported corpus contents, and private coordination are excluded. A fresh independent review remains necessary.
