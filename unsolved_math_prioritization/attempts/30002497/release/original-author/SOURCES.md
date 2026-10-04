# Source and scope check

Checked 2026-10-04 (UTC).

## Exact primary target

Michel Balazard, “Nyman's and Báez-Duarte's criteria for the Riemann
hypothesis: survey and open problems,” in *Dirichlet Series and Function
Theory in Polydiscs*, Oberwolfach Report 06/2014, printed pp. 348–351.
The target is **Question 2 on printed p. 350**; the definition immediately
preceding it integrates from zero to infinity.

- https://doi.org/10.4171/owr/2014/06
- Official report: https://publications.mfo.de/bitstream/handle/mfo/3396/OWR_2014_06.pdf?isAllowed=y&sequence=1

The question has only one existential part. It does not ask for all
maxima, for the normalized autocorrelation, or for differentiability.
It recalls an earlier question from Báez-Duarte and collaborators.

The starting catalogue URL, https://www.unsolvedmath.com/problems/30002497,
was unavailable (HTTP 403 from the local retrieval; web retrieval also
failed). The pinned catalogue row was checked against the primary report;
the primary source fixes the mathematical scope.

## Mathematical dependencies

**[BDBLS]** L. Báez-Duarte, M. Balazard, B. Landreau, and E. Saias,
*Sur l'autocorrélation multiplicative de la fonction « partie fractionnaire »*,
arXiv:math/0306251v1 (2003), detailed companion to the published study,
*Ramanujan Journal* 9 (2005), 215–240.

- https://arxiv.org/abs/math/0306251
- https://doi.org/10.1007/s11139-005-0834-4
- Companion §8: Hilbert-space dilation/autocorrelation framework.
- Proposition 87, p. 38: the value at 1.
- Proposition 88, p. 38: the relation involving the two Bernoulli series.
- Propositions 90–91, pp. 39–41: integral identities.
- Proposition 98, p. 44: rational-point expansion and its dependence on p,q.

**[BM]** M. Balazard and B. Martin,
*Sur l'autocorrélation multiplicative de la fonction « partie fractionnaire »
et une fonction définie par J. R. Wilton*, arXiv:1305.4395v1.

- https://arxiv.org/abs/1305.4395
- https://arxiv.org/html/1305.4395
- Theorem 1, p. 3, and Proposition 7: differentiability/Wilton criterion.
- Proposition 1, p. 4: A equals a differentiable remainder minus a scaled
  primitive of the Wilton function, on (0,1).
- Proposition 11 proof, pp. 17–19, especially (32)–(37): the secant sequence
  with parity-dependent sides. The estimates precede the final use of the
  divergence assumption.
- Proposition 12: Wilton points are Lebesgue points of W.
- Theorem 2 and Proposition 26: convergence and Lebesgue-point properties
  needed when differentiating the Bernoulli-series integral identity.
- Proposition 23, p. 31; Propositions 27–30, pp. 33–35: integral identities,
  the second Bernoulli series, and differentiability.

The 2013 arXiv record's downloaded PDF has a 27 February 2018 title-page
compilation date. The arXiv identifier/version, rather than that compilation
date, identifies the cited source. The proof packet derives a necessary
condition from these results; it does not attribute that deduction as an
explicit theorem of the source.

## Later primary literature checked

- S. B. Lee, S. Marmi, I. Petrykiewicz and T. I. Schindler, *Regularity
  properties of k-Brjuno and Wilton functions*, Aequationes Mathematicae 98
  (2024), 13–85; correction at 349–350.
  https://arxiv.org/abs/2106.07298 and
  https://doi.org/10.1007/s00010-023-00967-w
  The inspected publisher text concerns BMO/regularity and rational
  behavior. No full solution of the target was identified there.
- A. Bakhtawar, C. Carminati and S. B. Lee, *Regularity properties of the
  alpha-Wilton functions*, arXiv:2409.20401.
  https://arxiv.org/abs/2409.20401
  The inspected abstract concerns BMO ranges for generalized continued
  fractions; it does not assert the requested extrema result.
- C. Burrin, S. B. Lee and S. Marmi, *The Brjuno and Wilton functions*,
  Mathematika 72 (2026), e70068, first published 2026-01-08.
  https://arxiv.org/abs/2503.08206 and
  https://doi.org/10.1112/mtk.70068
  The available arXiv text was inspected, including Theorems 1.1–1.2 and
  Proposition 2.1. Its bounded-defect/regularity statements do not settle
  the two-sided remainder sign needed here. Its introductory displayed
  autocorrelation has upper endpoint 1 in the inspected arXiv rendering;
  the target definition is taken from OWR and [BM], not that display.

These are bounded source checks, not a claim of an exhaustive bibliography
or a proof that no recent resolution exists.

## Identity and duplication checks

- The live repository queue listed ID30002497 at rank 623, queued, 0/5.
- Searches for the numeric ID, “Fractional-Part,” and “OWR-12866-004” found
  no existing matching pull request. The ID branch search was empty; the
  target attempt README returned 404.
- The selected ID was absent from the inspected state and related-target
  records.
- Catalogue ID30002496 is a composite that includes this question together
  with the separate real-variable Nyman-criterion question. It is not a
  second independent target or discovery. This packet does not address its
  other component.
- No matching research-report key containing the source code, and no
  matching numeric-ID/title report, was present in the pinned report corpus.
  No unexamined prior AI proof is being accepted as evidence.

Only original author text, code, and generated control results belong to
this packet. Source PDFs, full texts, and raw catalogues are not included.
