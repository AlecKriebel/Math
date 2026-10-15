# Priority reconciliation: problem 30005897

**Accepted disposition:** `already_solved`, credited known-method corollary,
no new paper, DOI, or spreadsheet row. Fresh complete acceptance review passed with no mandatory issues.

The exact target is the second sentence of OWR 19/2024 Open Problem (1),
p. 1080: shadowing is equivalent to generalized hyperbolicity for bounded
invertible dissipative scalar composition operators, without bounded distortion.
The original record's historical open classification is evidence of its dated
triage, not a theorem asserting that no older equivalent mechanism applies.

## Positive certificate and provenance

The complete checkable translation is [EQUIVALENT_TRANSLATION.md](https://github.com/AlecKriebel/Math/blob/main/draft_pr_publication_program_20260930/audits/pr12_30005897/priority_equivalents/EQUIVALENT_TRANSLATION.md).
Its independent adversarial report is [FALSIFIER.md](https://github.com/AlecKriebel/Math/blob/main/draft_pr_publication_program_20260930/audits/pr12_30005897/priority_equivalents/kitover_translation_falsifier/FALSIFIER.md).
The source statement is [Kitover--Orhon 2020v2, Theorem 2.26](https://arxiv.org/html/2009.09303v2),
which explicitly attributes the scalar decomposition to Kitover 2011 Theorem
3.29. The 2020 version date is fixed by arXiv's submission history; its HTML
internal 2026 date is not the priority date. The inaccessible 2011 proof is
not described as inspected or literally compared.

1. Orbit-density coordinates give the normalized positive bounded invertible
   bilateral shift B on Lp(W x Z), with dual S on Lq, including q=infinity.
2. Shadowing's bounded forced solutions imply ||u|| <= K||(I-S)u|| by summing
   constant forcing over a finite block and sending its length to infinity.
3. If the central weighted operator on Linfinity=C(K) had approximate fixed
   vectors, a finite coordinate cutoff on a positive finite-measure fiber
   subset would give approximate fixed vectors in Lq. The explicit bound
   tends to zero for all q and does not use an older full-spectrum equality.
4. The complete measure algebra has a Stonean Stone space. Coordinate residue
   clopen partitions rule out all periodic Stone points, including free
   ultrafilters. The old scalar decomposition applies in the spectral case;
   its global tail closures give a clopen one-step split and uniform product
   decay. In the resolvent case, the coordinate gauge and multiplier-invariant
   Riesz spaces give a clopen invariant split directly.
5. Central forward products are rho(n-k)/rho(n) to the power 1/p, exactly the
   primal B^k norm factors. Inverse products similarly give rho(n+k)/rho(n).
   Thus the split is generalized hyperbolicity on complementary measurable
   bands. Complexification and real indicator projections cover real scalars.
6. Choose one large common integer d so both band norm bounds are less than
   one. The same norm identities give condition (1.5) almost everywhere on
   the two complementary supports, with a common eta<1 and null set.

The broader 2020 proof's equation (33) uses the wrong reversed cocycle
product. An exact stable periodic-weight countercheck is saved in the
falsifier report. The sufficient certificate avoids that equation, the
claimed full spectral equality, and the uninspected original point criterion.
The sole imported non-elementary decomposition is the explicitly printed
scalar Theorem 2.26; its translation and all hypothesis matches were falsified
independently without finding a remaining obstruction.

## Reconcile distinct search families

The [independent exact-question search](https://github.com/AlecKriebel/Math/blob/main/draft_pr_publication_program_20260930/audits/pr12_30005897/priority_exact/REPORT.md)
found no inspected primary fulltext explicitly printing the complete all-p
statement, and records inaccessible fulltext leads. That bounded absence
supports only a novelty hypothesis. It does not defeat the positive derived
corollary above. We do not assert that the old authors advertised this precise
composition-operator answer, nor claim worldwide first priority for any proof.

The elementary Sections 2--6 and exact regression checks are preserved as
verification and useful exposition. The aggregate-mass question has a prior
negative answer and is not conflated with this equivalence. No related
structural-stability problem or general Banach conjecture is resolved here.

This work used AI extensively and has independent AI audits. It has not been
human peer reviewed or formally certified. This acceptance package is a
repository research record, not a newly published preprint.

**Source-proof precision update:** the plain-shift cocycle countercheck in the historical falsifier report alone distinguishes operators, not their global norms. A broader allowed weighted-module example does falsify the printed norm identity, and a corrected operator relation can repair the growth estimate; the old spectral theorem is not refuted. See [the exact correction](https://github.com/AlecKriebel/Math/blob/main/draft_pr_publication_program_20260930/audits/pr12_30005897/ROOT_EQ33_PRECISION.md). The sufficient priority route remains independent of that identity.
