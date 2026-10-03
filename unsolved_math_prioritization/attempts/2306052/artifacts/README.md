# Rubel's bounded univalent perturbation question

**2306052 / AMR-022-6052 / Function Theory 6.52. Original problem unresolved; five substantive approaches recorded.**

For f_0(z)=2z(1+z)/(1−z)^2, this packet proves the exact classification:

- f_0+az is onto C when (2 Re a−1)^3 < 27(Im a)^2.
- Otherwise its range is C minus the single point −conj(a).

Thus every nonzero |a|<1/2 works, while a=1/2 fails. Separately, any bounded holomorphic perturbation of norm less than 3/64 preserves this particular f_0's surjectivity. General contour/inverse-branch criteria and an omitted-value selection obstruction are also proved. None settles the question for arbitrary surjective f.

- `PROOF.md`: complete stated proofs and the precise general gap.
- `SOURCE_GATE.md`: primary statement, theorem applicability, prior-work checks, and limits.
- `RESEARCH_LOG.md`: five substantive analytical attempts.
- `STATUS.json`: machine-readable scope.
- `verify.py`, `verification.json`: exact auxiliary algebra and reproducible output.

Run `python3 verify.py` using Python 3; no third-party package is needed. The recorded output passes 1,021 exact assertions. These checks are supplementary, not a formal proof of complex analysis or a solution to the original problem.

AI-assisted, unrefereed partial research. No novelty or priority claim. Historical problem source: [Hayman–Lingham, arXiv:1809.07200v2, Problem 6.52](https://arxiv.org/abs/1809.07200v2).
