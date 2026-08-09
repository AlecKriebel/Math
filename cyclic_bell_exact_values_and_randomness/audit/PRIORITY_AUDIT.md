# Fresh priority audit

**Audit date:** 9 August 2026

**Claims frozen against:** the revised canonical `main.tex`

**Search cutoff:** public primary records discoverable on 9 August 2026

**Scope:** priority and attribution, not peer review or proof verification

## Executive finding

No priority conflict was found for the two lead results: the exact
all-dimensional value of the first reduced cyclic operator (including its
commuting-operator strengthening), and the family-specific construction of
nonuniform exact maximizers. This conclusion is necessarily qualified: the
originating and neighboring papers are recent, and a negative literature
search cannot exclude unpublished or not-yet-indexed work.

The originating paper already proved substantially more than a lower bound.
It proved the analytic upper bound
\(\beta_q(\mathcal I_d)\le d\sqrt2\), supplied an all-dimensional strategy
of value \(M_d=2\csc(\pi/(2d))\), conjectured equality, and reported NPA
agreement through \(d=6\). The present exact theorem must always be described
against that full benchmark.

| Contribution | Priority outcome | Publication-safe boundary |
|---|---|---|
| Definitions and normalizations of both cyclic Bell families | **ESTABLISHED PRIOR ART** | Credit Perito et al. |
| Canonical strategies and all-dimensional lower values | **ESTABLISHED PRIOR ART** | Credit Perito et al.; say they supplied the attaining candidates. |
| General first-family bound \(d\sqrt2\) and NPA evidence through \(d=6\) | **ESTABLISHED PRIOR ART** | Credit Proposition 3 and Table 1 of Perito et al.; do not describe the exact proof as replacing an absence of upper bounds. |
| Second-family value \(d\) and SOS certificate | **ESTABLISHED PRIOR ART** | Import the corrected source SOS with citation. |
| Scalar half-angle extremum, polar decomposition, functional calculus, and cosecant-square identities as abstract tools | **ESTABLISHED MATHEMATICAL TOOLS** | Make no stand-alone priority claim for these tools. |
| Exact first-family value \(M_d=2\csc(\pi/(2d))\) in every dimension | **PLAUSIBLY NEW** | “We prove the value conjectured by Perito et al.” |
| Equality \(\beta_q=\beta_{qa}=\beta_{qc}=M_d\) | **NEW STRENGTHENING OF A KNOWN/CONJECTURED RESULT** | State that the exact upper bound is strengthened to the commuting-operator model. |
| Sufficient conditional phase-permutation theorem for the polar-linear form | **PLAUSIBLY NEW** | Do not call it a complete maximizing-face classification. |
| First-family nonuniform exact maximizers for every \(d\ge4\) | **PLAUSIBLY NEW** | “To our knowledge, no previous work identified such maximizers.” |
| Second-family phase-permuted, nonuniform exact maximizers | **PLAUSIBLY NEW APPLICATION OF AN ESTABLISHED SOS** | Credit the SOS and claim only the new saturating strategies and consequence. |
| General distinction between one Bell value and complete-statistics conditioning | **ESTABLISHED PRIOR ART** | Cite the complete-statistics randomness literature. |
| Refutation, for \(d\ge4\), of the normalized scalar implication in source Conjecture 2 | **PLAUSIBLY NEW FAMILY-SPECIFIC COUNTEREXAMPLE** | Use the operator normalization \(\max\overline{\mathcal I}_d=M_d+1\); say explicitly that the fixed canonical behavior is untouched. |
| Behavior-level nonuniqueness modulo local output relabelings | **PLAUSIBLY NEW COROLLARY** | Do not promote it to a complete strategy-level self-testing classification. |
| Equal supported multiplicities and \(d\mid\dim K\) for finite-dimensional exact first-family maximizers | **RESTORED HISTORICAL/INTERNAL RESULT; NO LEAD PRIORITY CLAIM** | The result appeared in the preserved standalone randomness manuscript and is restored after replay. No external-priority claim or \(qa/qc\) extension is made. |
| One-input locality/private-randomness baseline | **ESTABLISHED PRIOR ART** | Present as a standard baseline. |
| Binary \(3\sqrt3\) privacy benchmark | **ESTABLISHED PRIOR ART** | Identify it, after an output flip, with the \(\delta=\pi/6\) Wooltorton--Brown--Colbeck family; the included derivation is expository verification. |
| Private-MUB composition lemma | **RESTORED HISTORICAL/INTERNAL DESIGN LEMMA; NO NOVELTY CLAIM** | State only a sufficient state-supported criterion; claim neither necessity nor existence of a Bell functional enforcing it. |
| Computational-MUB exposure obstruction | **NOVELTY UNCERTAIN** | Keep its operator-span and coefficientwise-bound hypotheses explicit; make no general low-setting no-go claim. |

## Originating record, version by version

The controlling primary source is Ignacio Perito, Raffaele D'Avino, Michał
Jung, Piotr Mironowicz, Antonio Acín, and Remigiusz Augusiak, *Bell
inequalities tailored to optimal global randomness certification*,
[arXiv:2606.21362](https://arxiv.org/abs/2606.21362). Its v1, v2, and v3 TeX
sources were inspected, not only the abstract.

- v1: 19 June 2026.
- v2: 24 June 2026.
- v3: 21 July 2026; latest public version found at the cutoff.
- Section III and Appendix A define the two cyclic families, give the
  canonical strategies, prove
  \(\beta_q(\mathcal I_d)\le d\sqrt2\), conjecture the sharper value
  \(M_d\), and report NPA/see-saw agreement through \(d=6\).
- Section IV proves the second reduced value \(d\) by SOS. Version 3 corrects
  the relevant prefactor to \(1/(2d)\).
- Conjecture 2 asserts maximal global randomness from maximal violation of
  the first augmented scalar functional. Its adjacent printed maximum has a
  localized normalization discrepancy. The operator definition, Eq. (17),
  and the reported \(d=3\) augmented value consistently give \(M_d+1\).
- The source's selected numerical randomness calculations condition on the
  complete canonical behavior. No source version inspected contains the
  present polar exact upper bound, conditional phase-permutation theorem, or
  nonuniform maximum-value behavior.
- No supplementary code archive was present in the arXiv source package; it
  contained TeX, bibliography, and figures.

The canonical manuscript therefore distinguishes three logically different
source statements: the proved \(d\sqrt2\) bound, the conjectured exact value,
and randomness evaluated or asserted under different conditioning data.

## Exact scope of the Conjecture 2 consequence

For the displayed first augmented operator, the authoritative normalized
maximum is
\[
 \max\overline{\mathcal I}_d=M_d+1,
 \qquad M_d=2\csc\!\left(\frac{\pi}{2d}\right).
\]
The merged construction gives, for every \(d\ge4\), a finite-dimensional
behavior attaining \(M_d+1\) with a nonuniform target table. Hence it refutes
the normalized scalar implication
\[
 \langle\overline{\mathcal I}_d\rangle=M_d+1
 \quad\Longrightarrow\quad
 G(AB\mid1,d,E)=\frac1{d^2}
\]
in those dimensions. This conclusion does not invalidate the source's
calculation after the entire canonical distribution is fixed, does not show
that the canonical strategy lacks maximal randomness, and does not determine
the exact worst-case guessing probability over the maximizing face.

## Restored results and non-lead material

The equal-supported-multiplicity theorem, reflection-rank lemma, and
private-MUB composition lemma were already present in preserved standalone
Kriebel manuscripts. Their restoration prevents mathematical content from
being silently lost in the merger; it does not reset their provenance or
turn them into new lead claims of this revision. The support theorem is
finite-dimensional, tensor-product, and exact-attainment only. The
private-MUB lemma is only a sufficient state-supported design criterion.

Likewise, the binary theorem is retained because it gives a useful exact
privacy calibration, but the result is established prior art: after
\(B_1\mapsto-B_1\), the score is the \(\delta=\pi/6\) member of the
Wooltorton--Brown--Colbeck family. The self-contained proof is not presented
as an independent priority claim.

## Closely related primary sources inspected

1. M. Farkas, P. Mironowicz, and R. Augusiak, *Maximal global
   device-independent randomness from projective measurements in every
   dimension*, [arXiv:2606.21369v2](https://arxiv.org/abs/2606.21369v2).
   It gives a different all-dimensional construction, not this exact cyclic
   bound or its phase-permutation maximizers.
2. R. D'Avino et al., *Noise robustness of three outcome Bell certified
   quantum randomness*, [arXiv:2606.21371v2](https://arxiv.org/abs/2606.21371v2).
   It concerns a different three-outcome robustness problem.
3. L. Coccia, M. Padovan, and G. Vallone, *Systematic derivation of Tsirelson
   bounds in arbitrary dimensions*,
   [arXiv:2606.21626v1](https://arxiv.org/abs/2606.21626v1). The official
   record confirms the initials L. Coccia and M. Padovan. Its general method
   does not state the present family-specific value or permutation orbit.
4. I. Klep, N. Leijenhorst, and V. Magron, *Robust self-testing with CHSH mod
   3*, [arXiv:2604.03700v1](https://arxiv.org/abs/2604.03700v1). It concerns
   a different modular operator.
5. V. Barizien, P. Sekatski, and J.-D. Bancal, *Custom Bell inequalities from
   formal sums of squares*, [Quantum 8, 1333
   (2024)](https://doi.org/10.22331/q-2024-05-02-1333). This is general SOS
   methodology, not the present family-specific result.
6. L. Wooltorton, P. Brown, and R. Colbeck, *Tight analytic bound on the
   trade-off between device-independent randomness and nonlocality*,
   [Physical Review Letters 129, 150403
   (2022)](https://doi.org/10.1103/PhysRevLett.129.150403). This contains the
   binary family used for the \(d=2\) calibration.
7. O. Nieto-Silleras, S. Pironio, and J. Silman, *Using complete measurement
   statistics for optimal device-independent randomness evaluation*,
   [New Journal of Physics 16, 013035
   (2014)](https://doi.org/10.1088/1367-2630/16/1/013035), and J.-D. Bancal,
   L. Sheridan, and V. Scarani, *More randomness from the same data*,
   [New Journal of Physics 16, 033011
   (2014)](https://doi.org/10.1088/1367-2630/16/3/033011). These establish
   the general complete-statistics principle.
8. M. Navascués, S. Pironio, and A. Acín, *Bounding the Set of Quantum
   Correlations*, [Physical Review Letters 98, 010401
   (2007)](https://doi.org/10.1103/PhysRevLett.98.010401). This is the primary
   NPA citation for the source's numerical hierarchy evidence.

The source-comparison table records the remaining family and low-setting
comparators checked during the audit.

## Search and update checks

The arXiv version history and source package, title/author searches, exact
formula searches, cited-by and related-work records, and public correction
or note searches were checked after the theorem set was frozen. No later
version of arXiv:2606.21362 and no primary paper containing the same exact
polar proof, weighted-shift permutation family, or biased exact maximizer was
found at the cutoff. This is evidence of due diligence, not proof of absence.

The source's \(d\sqrt2\) bound is of the same linear order as \(M_d\), but it
is not asymptotically tight:
\[
 \frac{d\sqrt2}{2\csc(\pi/(2d))}
 \longrightarrow \frac{\pi}{2\sqrt2}=1.110720\ldots .
\]

## Publication boundary and residual risk

The manuscript should continue to say:

- “we prove the value conjectured by Perito et al.”;
- “we strengthen the exact result to commuting operators”;
- “we identify a sufficient phase-permutation mechanism,” not a complete
  maximizing-face classification;
- “the scalar maximum alone is insufficient,” not that the canonical
  full-behavior calculation is invalid; and
- “to our knowledge” for absence-of-prior-work statements.

The principal residual priority risk is concurrent discovery in a rapidly
moving 2026 literature. The polar positive-factor identity may also have a
standard named antecedent deserving an additional citation even though no
family-specific application was located. Neither point changes the proved
theorems, but both require qualified novelty language.

**Priority verdict:** no conflict found. The exact all-dimensional value and
family-specific nonuniform maximizers are **plausibly new**; the
commuting-operator equality is a **new strengthening**; source bounds,
canonical strategies, the second-family SOS, the binary calibration, and the
general scalar/full-statistics distinction are **established prior art**.
