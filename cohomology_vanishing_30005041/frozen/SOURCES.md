# Sources, provenance, prior-attempt and status checks

Checked 2026-10-03. A bounded search found no later resolution; that is not a proof that none exists and no priority is asserted.

## Primary sources

1. [Official OWR report landing page](https://ems.press/journals/owr/articles/9790362), DOI [10.4171/OWR/2022/11](https://doi.org/10.4171/OWR/2022/11). The report PDF was read locally. Question 1, printed p.568 (PDF page52), exactly matches the fixed-family question. The neighboring theorem solves the group-wide spectrum by changing the action; the report explicitly distinguishes the two problems.
2. Marrakchi–de la Salle, [arXiv:2001.02490v3](https://arxiv.org/abs/2001.02490v3), especially §5.2, Theorem5.4 and Question5.5. The formal-coboundary theorem is stated for `1<=p<q`. Question5.5 asks the stronger downward-vanishing analogue for full cohomology. The full interval question is explicitly left unsettled before Theorem5.4. The peer-reviewed article is [Compositio Mathematica 159 (2023), 1300–1313](https://doi.org/10.1112/S0010437X23007121); the theorem numbering used in these notes refers to the inspected arXiv version, not an assumed identical journal numbering.
3. Lavy–Olivier, [Fixed-point spectrum for group actions by affine isometries on Lp-spaces](https://aif.centre-mersenne.org/articles/10.5802/aif.3348/), Ann. Inst. Fourier71(2021),1–26; [arXiv:1410.0227v3](https://arxiv.org/abs/1410.0227v3). Theorem3/Proposition28 treat the fixed-family finite-measure-preserving ergodic case; atomic fixed-family results are also discussed. Their group-wide exceptional Hilbert-exponent phenomenon cannot be imported into a fixed Lamperti family.

## Recovery and history

The catalogue webpage [problem30005041](https://www.unsolvedmath.com/problems/30005041) returned HTTP403. The target was recovered from the supplied pinned corpus and independently verified against source1. The malformed corpus `original_statement` was not used as a mathematical statement. The supplied literature-review corpus did not yield a matching record under the problem's OWR key, so it was not treated as independent evidence.

The live repository `unsolved_math_prioritization/QUEUE.md` on main showed rank482 as queued,0/5. Exact repository commit search for30005041 found no prior commit; code searches for30005041 and Lamperti found no match. Broader cohomology history concerned mathematically different group-ring and tiling problems. The coordinator's exact conversation-history searches also found no prior target attempt. No duplicate-attempt skip was justified. Search indexing may be incomplete.

## Cautions

- This checkpoint does not assert the entire problem is already solved.
- The cited formal theorem alone is insufficient, even for the one-point trivial Z-action: formal cohomology is zero whereas ordinary H1 is nonzero.
- We do not extrapolate the cited theorem below p=1. The atomic-Z calculation and the no-measurable-invariants lemma are separately proved for all p>0.
- Only the specifically stated elementary propositions are proved here. Novelty has not been established.
- Scholarly PDFs, full catalogue corpora, and private working context are excluded from the publication directory.
