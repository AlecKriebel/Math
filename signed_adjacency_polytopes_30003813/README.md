# Signed adjacent-sum h-star certificate

This packet gives a complete independently audited answer to the literal combinatorial
interpretation requested by UnsolvedMath 30003813 / OWR-16164-005.

Reflect the even coordinates to obtain an oriented-path order polytope.
Its h-star polynomial counts naturally labeled linear-extension words by
descents. `PROOF.md` gives an explicit equivalent formula on a fixed descent
class of ordinary permutations, a self-contained all-dimensions proof, and
the exact source scope.

This is an application of classical results of Stanley, with no novelty
claim. No located paper was verified to close the exact OWR question
explicitly. A cyclic-order-specific refinement is outside this certificate.

## Files

- `PROOF.md`: theorem, complete proof, examples, and primary references
- `SOURCE_GATE.md`: source and prior-attempt checks
- `RESEARCH_LOG.md`: the one substantive author attempt and validation history
- `verify.py`: exact standard-library regression checker
- `verification.json`: its reproducible output
- `review/AUDIT.md`: independent full-proof audit
- `RELEASE_CHANGES.md`: explicit release-only changes
- `status.json`: machine-readable scope and review status
- `MANIFEST.sha256`: frozen file digests

## Reproduction

Run from this directory:

```sh
python3 verify.py --max-n 8 --output verification_replay.json
cmp verification.json verification_replay.json
sha256sum -c MANIFEST.sha256
```

The proof applies to every positive dimension and every sign word. The
finite regression tests cover all 255 sign words in dimensions 1 through 8.

Independent mathematical audit: PASS. Status: claimed_solved, 1/5 author attempts.
The complete review and its additional controls are in `review/`.

Run the independent checks with `python3 review/independent_controls.py`; this
regenerates `review/independent_results.json`. See `RELEASE_CHANGES.md` for the
editorial changes from the audited frozen packet.
