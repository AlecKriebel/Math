# Attempt 1: sparse tight constraints, exact encoding, and a counterexample

Date: 20 October 2026. Target: row 1827 / 30002723. This attempt preserves rational sparse breakpoint/point/one-sided-limit data, the minimality promise, and unrestricted valid-function competitors.

## Source theorem inspected

Basu–Hildebrand–Köppe, Part I, Theorem 4.11, proves that a possibly discontinuous rational-breakpoint minimal valid function is extreme if and only if its complete point/interval-affine tight system (10) on the grid (1/(4q)) Z has a unique solution. This is stronger than the continuous finite-group oversampling theorem, and is the correct starting point for the discontinuous target. Theorem 3.2 turns a nonzero kernel vector into an effective piecewise-linear perturbation. The paper's introductory complexity conjecture is explicitly a question, not a hardness theorem.

Public source: https://arxiv.org/html/1206.2079v2, §§3–4. The cited primary source was inspected; its text is not reproduced in this authored report.

## Polynomial bit-size facts

Let L be the total binary encoding length and k the number of input intervals. Add f to the breakpoint list if needed. The common denominator q can be computed using gcd/lcm operations, and log q is at most the sum of input denominator bit lengths, hence O(L). Coordinates of the sparse two-dimensional arrangement are sums/differences of input breakpoints and have polynomial bit length. The arrangement has O(k^2) faces, vertices, and incidences, so its finite minimality test and its same-breakpoint tight system are polynomial-bit computations.

This does NOT establish extremality: restricting competitors to the original breakpoints is invalid.

## Exact counterexample to the same-grid shortcut

Take f=1/5. The continuous periodic interpolant with sparse breakpoint/value pairs

(0,0), (1/5,1), (2/5,1/3), (4/5,2/3), (1,0)

is minimal. Its values on the 1/5 grid are (0,1,1/3,1/2,2/3). The normalized tight system on those five points has rank 5, but the system on the 1/15 grid has rank 13 rather than 15.

An exact nonzero perturbation h on the 1/15 grid has h(8/15)=-1, h(10/15)=1, and all other grid values zero, with continuous linear interpolation. Both pi+(5/18)h and pi−(5/18)h satisfy every finite-group minimality inequality and symmetry equality on that grid, hence their continuous interpolants are minimal valid. Thus pi is not extreme despite same-grid rigidity.

Reproduce with `python checks/verify_counterexample.py`. The verifier uses rational arithmetic for every assertion. The discovery script used deterministic floating-point linear programming only to propose candidates; the displayed counterexample and epsilon were independently checked exactly.

## Outcome and next question

The naive sparse-rank approach is refuted. The exact 4q-grid theorem remains usable if its exponentially large linear system admits compressed rank determination. The next attempt studies the arithmetic orbit structure rather than expanding q.
