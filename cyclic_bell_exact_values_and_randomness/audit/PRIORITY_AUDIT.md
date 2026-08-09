# Fresh priority audit

**Audit date:** 2026-08-08

**Claims frozen against:** `main.tex` after the mathematical audit

**Cutoff:** public records discoverable on 2026-08-08

## Executive finding

No priority conflict was found for the paper's two central contributions:
the exact all-dimensional upper bound for the first reduced cyclic operator,
and the family-specific phase-permutation maximizers with nonuniform target
outputs. The safest classifications are nevertheless qualified because the
originating paper and several closely related papers appeared only weeks
before this audit.

| Contribution | Outcome | Publication wording |
|---|---|---|
| Definitions of both Bell families | **ESTABLISHED PRIOR ART** | Credit Perito et al. |
| Canonical strategies and matching lower bounds | **ESTABLISHED PRIOR ART** | Credit Perito et al. |
| Second-family SOS and value (d) | **ESTABLISHED PRIOR ART** | Import the corrected v3 SOS with citation |
| Scalar trigonometric extremum and abstract polar identity | **ESTABLISHED MATHEMATICAL TOOLS** | Make no stand-alone novelty claim |
| Exact upper bound (2\csc(\pi/(2d))) for the first family | **PLAUSIBLY NEW** | “We prove the value conjectured by Perito et al.” |
| First-family commuting-operator bound and (q=qa=qc) | **NEW STRENGTHENING OF A CONJECTURED RESULT** | “We strengthen the bound to commuting operators” |
| Sufficient phase-permutation theorem for this polar-linear form | **PLAUSIBLY NEW** | Avoid claiming a complete equality classification |
| Nonuniform exact maximizers for the first family, (d\ge4) | **PLAUSIBLY NEW** | “To our knowledge, no previous work identified…” |
| Same mechanism for the second augmented family | **PLAUSIBLY NEW** | Credit the source SOS; claim only the new saturating family |
| Bell-value versus fixed-full-behavior distinction in general | **ESTABLISHED PRINCIPLE** | Cite complete-statistics randomness literature |
| This distinction for the two exact cyclic families | **PLAUSIBLY NEW APPLICATION** | State the scalar-value scope prominently |
| One-input locality/private-randomness baseline | **ESTABLISHED PRIOR ART** | Present as a standard baseline, not novelty |
| Binary (d=2) calibration | **ESTABLISHED PRIOR ART** | Credit Wooltorton--Brown--Colbeck |
| Computational-MUB exposure obstruction | **NOVELTY UNCERTAIN** | Keep scoped in an appendix and make no priority claim |

## Originating record, version by version

The originating record is I. Perito, R. D'Avino, M. Jung, P. Mironowicz,
A. Acin, and R. Augusiak, *Bell inequalities tailored to optimal global
randomness certification*, [arXiv:2606.21362](https://arxiv.org/abs/2606.21362).
The raw source of v1, v2, and v3 was inspected, not only the abstract.

- v1: 19 June 2026.
- v2: 24 June 2026.
- v3: 21 July 2026; latest version found at the audit cutoff.
- All three versions define the two cyclic families, supply canonical
  strategies, conjecture the first reduced value, and prove the second
  reduced value by SOS.
- v3 corrects the second-family SOS prefactor to (1/(2d)) and adds selected
  fixed-full-behavior numerical data. It does not contain the polar upper
  bound, a phase-permutation construction, or a nonuniform maximum-value
  behavior.
- No supplementary code archive was included in the arXiv source package;
  the package contained the TeX source, bibliography, and figures.

The source has convention/normalization discrepancies that affect notation,
not priority: main equations use (B_y), an appendix uses (B_y^\dagger),
and the printed first augmented conjecture contains an extra denominator
factor inconsistent with the operator definition and its stated (d=3)
value. The merged paper follows the Hermitian main-text operator convention
and describes the discrepancy neutrally.

## Closely related primary sources inspected

1. M. Farkas, P. Mironowicz, and R. Augusiak, *Maximal global
   device-independent randomness from projective measurements in every
   dimension*, [arXiv:2606.21369v2](https://arxiv.org/abs/2606.21369v2).
   It gives a different all-dimensional randomness construction and does not
   supply the present exact cyclic bound or permutation maximizers.
2. R. D'Avino et al., *Noise robustness of three outcome Bell certified
   quantum randomness*, [arXiv:2606.21371v2](https://arxiv.org/abs/2606.21371v2).
   It concerns three-outcome robustness, not the present equality mechanism.
3. L. Coccia, M. Padovan, and G. Vallone, *Systematic derivation of Tsirelson
   bounds in arbitrary dimensions*,
   [arXiv:2606.21626v1](https://arxiv.org/abs/2606.21626v1). The general SOS
   framework does not specialize to the claimed first-family value or its
   maximizing permutations.
4. I. Klep, N. Leijenhorst, and V. Magron, *Robust self-testing with CHSH mod
   3*, [arXiv:2604.03700v1](https://arxiv.org/abs/2604.03700v1). Its modular
   self-testing results concern a different operator.
5. V. Barizien, P. Sekatski, and J.-D. Bancal, *Custom Bell inequalities from
   formal sums of squares*, [Quantum 8, 1333
   (2024)](https://doi.org/10.22331/q-2024-05-02-1333). This is relevant SOS
   methodology, not the family-specific claims.
6. S. Sarkar et al., *Self-testing quantum systems of arbitrary local
   dimension with minimal number of measurements*, [npj Quantum Information
   7, 151 (2021)](https://doi.org/10.1038/s41534-021-00490-3). It is the
   primary source for the two-input qudit strategy used in the scoped
   setting discussion.
7. O. Nieto-Silleras, S. Pironio, and J. Silman, *Using complete measurement
   statistics for optimal device-independent randomness evaluation*,
   [New Journal of Physics 16, 013035
   (2014)](https://doi.org/10.1088/1367-2630/16/1/013035), and J.-D. Bancal,
   L. Sheridan, and V. Scarani, *More randomness from the same data*,
   [New Journal of Physics 16, 033011
   (2014)](https://doi.org/10.1088/1367-2630/16/3/033011). These establish the
   general importance of full statistics; the present contribution is the
   explicit obstruction for these cyclic families.

The source-comparison table records additional high-dimensional Bell and MUB
sources checked during the audit.

## Citation and update checks

The arXiv API, title/author searches, formula searches, cited-by/related-work
records, and public correction/note searches were repeated after the theorem
set was frozen. No later version of arXiv:2606.21362 and no paper containing
the same polar proof, weighted-shift permutation family, or biased exact
maximizer was located. Semantic Scholar and OpenAlex showed no later citing
paper supplying those results at the cutoff. These negative searches are
evidence of due diligence, not proof of absence.

## Priority-safe manuscript boundary

The manuscript therefore says:

- “we prove the conjectured value,” rather than claiming discovery of the
  family or its lower bound;
- “we strengthen the upper bound to the commuting-operator model”;
- “we identify a sufficient phase-permutation mechanism,” not a complete
  maximizing-face classification;
- “the scalar maximum alone is insufficient,” not that the canonical
  full-behavior calculation is invalid;
- “to our knowledge” when discussing absence of prior exact nonuniform
  maximizers.

## Residual priority risk

The main residual risk is concurrent discovery: all three June 2026 papers
are recent, and unpublished or not-yet-indexed work cannot be excluded. A
specialist should also check whether the polar positive-factor identity has a
standard named antecedent that deserves an additional citation. Neither risk
changes the family-specific theorem, but both counsel qualified novelty
language.

**Priority verdict:** no conflict found; central results are **plausibly new**
or a **new strengthening**, with the qualifications above.
