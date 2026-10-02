# Source report: Exceptional Strata, Problem 21

Problem11000228 / AMR-109-0228. **Source-verification hold; proposed queue state remains queued, 0/5.** This is a credited theorem report with an unresolved dependency-verification issue, not an independently verified solution or a new proof.

## Original request and reported answer

Hubert–Masur–Schmidt–Zorich, in Farb's edited volume, Problem21, printed p.257 (PDF p.264), asks for a geometric invariant distinguishing the components of Q(−1,9), Q(−1,3,6), Q(−1,3,3,3), and Q(12). The contrast is with the combinatorial extended Rauzy class. [Original source](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf).

Chen–Möller, *Quadratic differentials in low genus: exceptional and non-varying strata*, Ann. Sci. ENS47(2014),309–369, Theorems1.1/1.2 and6.1/7.1, report that the intrinsic dimension h⁰(X,O_X(D)), with D one third of the positive zero divisor, is1 on the regular component and2 on the irregular component. [Published paper](https://doi.org/10.24033/asens.2216).

Explicitly, the four divisors are3z; 2z₁+z₂ (z₁ the order6 zero); z₁+z₂+z₃; and4z. The simple pole is excluded from D. The first three signatures have genus3, and Q(12) has genus4. The cited Q strata exclude global squares of Abelian differentials; Lanneau's definitions and Chen–Möller Section2.1 make that convention explicit.

## Two separate limitations

1. A calculation in published Appendix B.5 has not passed this audit. Its stated h⁰(F₂,O(e+2f))=2 disagrees with the section formula yielding4. That value is used in a strict dimension inequality needed for Lemma7.7 and the proof of Theorem7.1. No silent correction or completed replacement argument is supplied. See PRIOR_PROOF_AUDIT.md
2. The invariant above is algebro-geometric. A purely flat-geometric formula is explicitly left open in Chen–Möller p.311 and again in Chen–Yu's January2026 survey, §3.5/Problem3.2. The source question has no explicit flat-only restriction, but this stronger remaining problem must not be described as solved

The 2026 survey supports continued attribution of the published classification. It does not repair the identified dependency calculation. This report therefore recommends retaining the source-verification hold until independent review establishes what can safely be certified. No mathematical author turn was used, no new theorem is claimed, and no external contact has been made.
