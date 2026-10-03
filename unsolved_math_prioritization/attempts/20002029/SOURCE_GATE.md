# Source and prior-attempt audit

Checked 3 October 2026.

## Exact problem and scope

The catalogue identifier is 20002029 / AIM-GEOMETRY-0367. Its exact detail URL is https://www.unsolvedmath.com/problems/20002029. That live page returned a visible HTTP 403 block, so live page freshness is not claimed. The supplied catalogue record was checked against the original AIM source.

The original problem is Robin Graham's Problem 10 in the [2003 AIM conformal-structure problem list](https://aimath.org/WWN/confstruct/confstruct.pdf), PDF page 24. The [official HTML version](https://aimath.org/WWN/confstruct/articles/html/30a/) agrees. It asks, for even n>=4, whether a nonzero scalar conformal invariant of weight -n can be expressed by a linear combination of complete contractions of nabla^l P for l>=0. In scalar notation this means I(e^(2u)g)=e^(-nu)I(g) pointwise.

P is the Schouten tensor, whereas P_n in the source is the critical GJMS operator. The Q-curvature uniqueness consequence holds with that operator and transformation law fixed. The question is not restricted to locally conformally flat metrics, and it is not a classification modulo divergences or a statement about conformally invariant integrals. The source itself records n=4 as negative and gives Bach/ambient-obstruction norms as examples at more-negative weights.

The proposed formulas in this package use complete metric contractions, the standard orientation-even convention. No extra geometric structure, nonpolynomial expression, global integration, or field equation is inserted into the original claim. Ricci-flat metrics are used only as necessary test metrics.

## Prior work and status

A prior machine-generated report supplied elementary derivative-free and fully symmetric-jet reductions and the known n=4 case, while explicitly leaving the full problem unresolved. Those findings are background, not fresh proof attempts in this package.

Bounded repository searches for the exact ID and code found no matching earlier campaign commit or pull request. Negative indexed searches do not establish the absence of inaccessible or unindexed work.

Primary literature inspected includes:

- Graham's 2007 restatement in [Peterson, SIGMA 3, 081](https://arxiv.org/abs/0708.2170). It describes the Ricci-jet characterization as open at that time.
- [Fefferman–Graham, The Ambient Metric](https://arxiv.org/abs/0710.0919), including its conformal-normalization and invariant-classification theorems. The weight -6 classification is used in ATTEMPT_3; it is not asserted to prove the unrestricted all-dimensional intersection statement by itself.
- [Case et al., arXiv:2404.11319v4](https://arxiv.org/html/2404.11319v4), the final preprint version dated 20 April 2026, published in Advances in Mathematics 496 (2026), 110991. The exact dimension-eight formulas in (3.4) are the subject of ATTEMPT_4. Their being natural divergences alone has no implication that they are Schouten-only.
- [Case–Gover, The GJMS operators in geometry, analysis, and physics](https://arxiv.org/abs/2509.16047), Journal of the London Mathematical Society 113 (2026), e70375.

No primary source establishing the full all-even-dimensional answer was located in this search. This does not prove that no such source exists. No priority claim is made for the dimension-six consequence, the first-jet vanishing theorem, or the explicit exclusion certificates.

## Research accounting and current limit

ATTEMPT_1 through ATTEMPT_5 are five separate substantive mathematical attempts. Source retrieval, bibliographic review, exact re-runs, and packaging are not additional attempts. The full question remains unresolved here; dimension six and the stated sectors are the only positive nonexistence claims.

All mathematical claims in this author package await fresh independent review. No third-party PDF, screenshot, complete source corpus, private correspondence, or account credential is included in this package.
