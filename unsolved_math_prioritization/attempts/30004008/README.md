# Rainbow arborescences: reviewed partial results

**Original problem 30004008 / OWR-16633-026: unsolved after five substantive research turns.**

[Result and remaining gap](RESULT.md) · [Independent review](final_review/ADVERSARIAL_REVIEW.md) · [Source scope](SOURCE_SCOPE.md)

The strongest structural partial is an all-cactus existence theorem, obtained by an articulation root-count argument combined with the credited cycle theorem of Bérczi–Király–Yamaguchi–Yokoi, arXiv:2412.15457v2. The cycle theorem is an explicit external dependency; its full long proof has not been independently re-audited in this packet. Historical priority is unverified.

Other proofs give source-component localization, exact core color quotas, a two-vertex interface characterization, and explicit obstructions to two algebraic shortcuts. The general strongly connected, biconnected arbitrary-root problem remains unresolved. Finite checks do not prove that general target.

## Verification

The independent mathematical review is a scoped PASS with no mandatory correction. It is AI-assisted review, not formal certification or human peer review. All five author replays match byte-for-byte, totaling 6,147,292 assertions; separate independent controls pass 857,762 assertions. See [replay metadata](FINAL_REPLAYS.json) and [review output](final_review/independent_output.json).

Run `python verify_turn1.py` through `python verify_turn5.py` in this directory, and compare stdout with the corresponding TURN_N_CHECKS.json. Run `python final_review/independent_checks.py` and compare with final_review/independent_output.json. Python's standard library suffices.

The frozen author and review manifests retain their original hashes. PUBLICATION_MANIFEST.json binds this assembled packet, excluding itself. No source PDF is republished.
