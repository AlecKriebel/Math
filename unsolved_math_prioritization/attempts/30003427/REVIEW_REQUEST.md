# Independent review request

Please audit the exact source-model and algorithmic theorem in PROOF.md.
Original OWR source: printed p.697, report 13/2017; full PDF in ../../sources.
Published model: Gerhold–Gülüm Definitions 2.1, 2.2, 2.4, final article XML
from Europe PMC and full arXiv v2 reading copy; source_manifest.json pins both.

Particular attacks:

- Preserve the separate adapted reference and shadow prices, finite arbitrary
  filtration, strictly positive stock bid, reference lower bound R>=epsilon,
  deterministic bank discounting and initial spread requirement.
- Check deterministic-root reduction when the original initial sigma field
  is nontrivial. No physical probability law is part of the input.
- Verify conditional Carathéodory retains all q payoff expectations and every
  local martingale equation, with the claimed q+2 branching bound. Do not
  substitute ordinary global terminal-law compression, which could lose the
  martingale. Auxiliary reference values need not be functions of shadow history.
- Check full-tree positive-weight padding, every polynomial constraint and
  the positive-part equation. Verify both model-to-system and system-to-model.
- Distinguish exact quantifier elimination on rational/algebraic data from
  formal semialgebraic characterization at arbitrary real parameters. The
  code compiles and tests the formula; no general CAD solver run is claimed.
- Check the complete admissible epsilon set, emptiness, endpoint inclusion,
  attainment and the strict-positive two-date example. No monotonicity or
  closedness of the admissible set is assumed.
- Assess the literal source request: this is a finite algorithmic quote-only
  characterization, with classical credit, no efficient or short inequality
  formula. It does not settle a separate CVB sufficiency/arbitrage conjecture.
  If that is insufficient for the exact source target, state the remaining
  scope gap rather than promoting a broader full claim.

Author count is one substantive turn of five. The exact checker passes
16,697 finite assertions; it does not prove quantifier elimination or replace
mathematical review. No novelty claim. No queue promotion or PR yet.
