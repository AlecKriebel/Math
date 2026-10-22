# Source and reproduction notes

## Primary inputs and exact use

The ten full PDFs are pinned by the author's `ALL_SOURCE_INPUTS.json`; their hashes are independently checked in `HASH_CHECK.json`.

1. Goldman, book chapter, printed p. 211/PDF p. 218, Problem 2.5; standalone chapter Problem 2.8: the exact closed-surface SU(2) character-space ergodicity target.
2. Saadi, [2505.08105v1](https://arxiv.org/abs/2505.08105v1): historical four-square conventions, Figures 3–4, the based lifts and Section 4 angle. The [live record](https://arxiv.org/abs/2505.08105) checked on 1 October 2026 says withdrawn in v2, 28 September 2026, because of a mistake in Theorem 3.1. No v2 PDF is supplied. The historical calculation is not framed as an accusation against a standing published theorem.
3. Saadi, [2404.00372v2](https://arxiv.org/abs/2404.00372v2), p. 2: explicitly credits Julien Marché for the no-polynomial-invariant observation from Charles–Marché. Its representation-variety/nonorientable-character statements are not substituted for the original orientable character-space target.
4. Goldman–Xia, full 2009 primary manuscript: smooth irreducible locus, connectedness/density and Goldman measure used in the extension argument.
5. Charles–Marché, original and [published full paper](https://ems.press/content/serial-article-files/43287), Theorem 1.1, printed p. 412, and Theorem 5.3/proof, pp. 426–427: SU(2) multicurve linear independence, including parallel components. The proof passages and actual scope were read; a complex-only invariant theorem is not substituted.
6. Forni–Goldman–Lawton–Matheus, [published 2024 article](https://ahl.centre-mersenne.org/item/10.5802/ahl.216.pdf), especially Theorem 4.8, printed p. 1112: the corrected analytic area-preserving Brjuno-elliptic stability input. Its two-dimensional relative setting is essential.
7. Ferreira–Ribas, [2602.23597v1](https://arxiv.org/abs/2602.23597), Theorem 1.1 and proof: Baker–Wüstholz yields a Diophantine argument for an algebraic unit-circle multiplier that is not a root of unity. This is a 2026 preprint input, not evidence that the angle itself is algebraic. The elementary non-root argument in the packet was also checked independently.
8. Bellamy–Schedler, full primary manuscript: the factoriality assertions used only to delimit an abandoned shortcut. No global UFD conclusion or vanished Picard group is assumed.

The source figures were visually inspected, in addition to the text and independently rebuilt cell identifications. Public artifacts omit downloaded PDFs, page renderings and private reading copies.

## Reproduction

With Python 3 and the installed SymPy, run from the review directory:

```
python3 independent_geometry.py
python3 independent_cohomology.py /path/to/author/TURN_5_COCHAIN_CERTIFICATE.json
```

Compare the resulting JSON byte-for-byte with `GEOMETRY_CHECKS.json` and `COHOMOLOGY_CHECKS.json`. Neither program imports an author checker. The second reads only the frozen exact matrix/word certificate for comparison; it independently reconstructs the mathematics using an actual kernel/mod-conjugation basis.

`AUTHOR_REPLAY.json` records the five separate exact author-output replays. `HASH_CHECK.json` records the original 39-entry freeze, corrected 42-entry freeze, preservation of every original entry, historical manifests and all ten PDF hashes. Its original `frozen_manifest_sha256` field deliberately preserves the earlier binding; `reviewed_corrected_manifest_sha256` is the final binding used for this verdict.

Finite grouped assertion counts are implementation controls. They are not a replacement for the continuous-parameter identities, multicurve theorem, foliation geometry, KAM hypothesis checks or ambient-measure arguments in the written review.
