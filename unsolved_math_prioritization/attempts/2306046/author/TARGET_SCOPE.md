# Exact target and scope controls

Let D={z in C: |z|<1}. Let S* consist of injective holomorphic maps f:D→C with f(0)=0, f'(0)=1 and the property that tw belongs to f(D) whenever w belongs to f(D) and 0≤t≤1. Write f(z)=sum_{n≥1} a_n z^n, a_1=1.

The target quantifies over every f in S* and every integer n≥1 and asks whether

    abs(abs(a_(n+1)) - abs(a_n)) ≤ 1.

Equivalently, both -1≤|a_(n+1)|-|a_n| and |a_(n+1)|-|a_n|≤1 must hold. An upper estimate alone is insufficient. This is an interior analytic class; no continuation across the unit circle or boundary regularity is assumed. Coefficients may be complex. The radial image condition is with respect to the origin. There is no growth-index hypothesis and no positive-order starlikeness restriction in the final target.

The class S normalization was checked in Hayman–Lingham Chapter 6, printed p. 114 (PDF p. 115). The target and its credited solution are on printed p. 135 (PDF p. 136). The original problem is attributed there to J. G. Clunie. The bibliography [510] on printed p. 234 (PDF p. 235) identifies Leung's 1978 article. The earlier growth-qualified and constant-two remarks on the target page are historical partial results, not extra hypotheses of the credited solution.

The target does not ask for |a_(n+1)-a_n|≤1. Rotation of the independent variable preserves all coefficient moduli but need not preserve raw coefficient differences. It also does not ask for the claim over all normalized univalent functions: starlikeness must be retained. Robertson's weighted close-to-convex coefficient problem, also discussed in the update, is a separate result and is not part of this target.

The explicit two-pole family in `PROOFS.md` is only a subclass of S*. Showing the estimate for that family, or finding no violation in finite atomic Herglotz tests, does not establish the assertion for all S*. No reduction of every starlike map to that family is asserted.

## Success criterion and evidence level

A new-solution claim would require a complete proof or admissible counterexample for the full quantified statement, followed by independent audit. This package instead meets the earlier stop condition: the source's own update names a published complete solution of precisely that statement, and another primary research paper restates it with the same quantifiers and attribution.

The remaining verification limit is the original proof: its steps and equality classification were not audited. We make no all-literature completeness or human-peer-review claim. Only the elementary controls are proved within this package.
