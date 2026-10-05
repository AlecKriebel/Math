# Equality of tropical and matroidal amoeba-dimension formulas

Problem 30005479 / OWR-12697711-015; queue rank 652.

**Outcome: already_solved.** A public preprint by Alper Ferudun dated 30 September 2026 supplies the full affirmative answer for arbitrary finite loopless matroids. This packet checks the argument and its published prerequisites; it does not claim a new solution. The preprint explicitly describes itself as unrefereed and AI-assisted. Independent checking here is not a claim of human peer review.

The exact equality also holds when the minimum ranges over every real subspace. Both minima equal the dimension of the Minkowski self-sum of the matroid fan. An optimal partition provides a rational minimizing subspace.

- `RESULT.md`: checkable mathematical verification and convention audit.
- `SOURCE_GATE.md`, `SOURCE_MANIFEST.json`: primary-source scope and provenance.
- `REPOSITORY_GATE.json`: live duplicate checks and selected-row metadata.
- `verify_dimensions.py`, `check_results.json`: separately written exact regression checks, using only the Python standard library.
- `RESEARCH_LOG.md`, `turns.jsonl`, `STATUS.json`: bounded investigation record.
- `verify_manifest.py`, `SHA256SUMS.json`: artifact integrity checks.

Run `python3 verify_dimensions.py` and `python3 verify_manifest.py` from this folder. The first must reproduce `check_results.json` exactly. Finite tests supplement the proof audit; they do not establish its universal quantifiers.

No third-party PDF, article text, dataset row, source archive, or copied implementation is included.

Prior resolution: [Ferudun, The Amoeba Dimension of an Arbitrary Loopless Matroid](https://eulersolve.org/papers/owr-12697711-015/).
