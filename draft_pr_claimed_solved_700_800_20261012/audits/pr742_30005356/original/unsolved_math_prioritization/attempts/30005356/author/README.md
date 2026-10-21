# Inverse Frobenius and definable multiplicative endomorphisms

Problem 30005356, OWR-12697685-001. Research date: 5 October 2026.

## Result

The literal assertion covering every characteristic has a negative answer. In every positive-characteristic model `(K, theta)` of ACFH, the inverse Frobenius map is a parameter-free definable multiplicative endomorphism outside `Z[theta]`. It is even a field automorphism commuting with `theta`.

`PROOF.md` gives the argument, including an elementary proof that polynomial evaluation at the generic multiplicative operator is faithful. This is a complete candidate counterexample to the unrestricted assertion. Independent review is pending. No novelty, priority, human-review, or editorial-acceptance claim is made.

The characteristic-zero classification and the positive-characteristic classification with `Z[1/p][theta]` in place of `Z[theta]` are not settled here. No change of coefficient ring is silently made in the target.

## Contents and checks

- `PROOF.md`: exact setup, counterexample, supporting lemmas, and limitations
- `LITERATURE.md`: primary-source interpretation and bounded current-literature check
- `SOURCE_VERIFICATION.json`: public hashes, byte counts, match results, source locations, and retrieval limits
- `RESEARCH_LOG.md`: one substantive approach and stopping reason
- `verify_math.py` and `CHECK_RESULTS.json`: reproducible finite sanity controls
- `verify_manifest.py` and `MANIFEST.json`: file-integrity checks

Run `python3 verify_math.py --check CHECK_RESULTS.json` and `python3 verify_manifest.py` from this directory. The finite controls do not prove the theorem or simulate an ACFH model. The mathematical proof is in `PROOF.md`.

This packet contains authored mathematics and programs, their outputs, and public verification metadata. It does not contain source PDFs, source-page images, extracted scholarly text, raw source datasets, selected dataset records, or private coordination material.
