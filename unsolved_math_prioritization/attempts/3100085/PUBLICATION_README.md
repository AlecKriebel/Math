# Publication guide: 3100085 / AMR-030-0085

**Current disposition: unsolved, 5/5. Independent technical review passes the scoped partials unchanged.** The original all-row, all-biased-probability existence question remains unresolved. Historical novelty is not certified.

## Read first

1. `RESULT.md`: frozen author summary; its pending-review wording records the author-freeze state
2. `final_review/REVIEW.md` and `VERDICT.json`: subsequent independent review and current verdict
3. `SOURCE_SCOPE.md` and `final_review/SOURCE_AUDIT.md`: precise probability-domain interpretation and source provenance
4. `TURN_4.md` and `TURN_5.md`: analytic all-n fixed-span reduction and complete span-twelve certificate
5. `TURN_1.md` through `TURN_3.md`: exact finite scan and other retained necessary conditions, with credited classical ingredients

The all-n span theorem, finite n<=80 scan, rational-only corollaries and unresolved arbitrary-span question are distinct. The root brackets' largest endpoint is an output, not a search cap on n.

## Integrity

- Author checkpoint: `b1bf2b1cb02bc8db4635f7f1bfe092c26cc215fd`
- Author manifest SHA-256: `e2ee0cd9986c128b7699ee8dd13001e3d156bda1f3116a2182b00308db5b309c`
- Review manifest SHA-256: `f3c233f3880e30d084a49c889ec0a32f27f944d4e57c4942d280106848357742`
- `PUBLICATION_MANIFEST.json` binds the retained author packet, portable review and publication prose. It excludes itself and QUEUE

All frozen author files and historical manifests remain unchanged. Raw downloaded papers, imported datasets and temporary probes are excluded from this public packet. Source URLs and hashes retain provenance.

## Reproduce

From this directory, run `python verify_turn1.py` through `python verify_turn5.py`; their deterministic JSON output must match the respective `TURN_n_CHECKS.json`. These use standard Python exact arithmetic. The optional certificate generator for Turn 2 uses SymPy; regenerating is unnecessary for checking the frozen formal identities.

Run `python final_review/independent_check.py` with Python and SymPy available. Its exact output must match `final_review/INDEPENDENT_CHECKS.json`. Alternatively pass this directory as the sole argument. The reviewer program imports no author checker. Review assertions support the full analytic audit, not a replacement of proof by finite sampling.

The five author replays total 760,234 assertions; the independent controls total 107,320. A complete resolution would still require an example at some larger span or an argument excluding all larger spans.
