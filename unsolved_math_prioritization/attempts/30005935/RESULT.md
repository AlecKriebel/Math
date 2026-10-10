# Result: positivity and convergence of the splitting scheme

Problem30005935 / OWR-14298374-004. **Five substantive author turns completed.** The asserted superlinear mean-square half-order behavior has a negative proof candidate; the broader source weak-rate question is only partially answered. All claims below await independent review. Historical priority is unverified.

## Main findings

For the intended geometric-Brownian-then-Dirichlet-heat scheme, with D=(0,1), g(v)=v_+^(5/4), a nonzero nonnegative smooth compactly supported initial profile and fixed T>0:

1. Numerical iterates are finite and positive almost surely, and their first moments equal those of the deterministic heat equation
2. At every grid index at least two, every numerical moment above one is infinite
3. The exact nonnegative local mild solution exists globally and is bounded by a scalar inverse-six-dimensional-Bessel process, with finite fixed-time moments below3/2
4. Consequently the actual coupled mean-square error is infinite, including at fixed final time for every M≥2. No mean-square half-order bound is possible
5. A normalized principal-eigenfunction mass observable has a finite weak error bounded away from zero independently of M; expected L1-field convergence fails as well
6. Nevertheless the interpolated path laws converge in bounded-Lipschitz distance at least at rate O([log(eM)]^(-2)) in one spatial dimension. This uses a quantified cutoff argument and does not modify the original scheme

The finite and infinite weak-error conclusions concern different test classes. The linear mass test is unbounded. The bounded-Lipschitz theorem suppresses the rare extreme tails responsible for failure of uniform integrability. No positive algebraic weak order, optimality of the logarithmic rate, or higher-dimensional sup-norm weak theorem is claimed.

## Source scope

The complete source contribution is Cohen's report in [OWR26/2024, pp1495–1498](https://ems.press/content/serial-article-files/49484). It separately discusses the superlinear time-only-noise convergence question and a weak-SPDE question, and then a different space-time-white-noise problem. Only the first setting is used here.

A displayed formula in that report and its cited time-noise paper lacks the multiplicative old-value factor. The stated geometric-Brownian substeps explicitly include it; this packet uses that intended substep-defined scheme and records the discrepancy in SOURCE_SCOPE.md. It does not analyze the inconsistent factor-free formula as if it were the intended method.

## Verification and remaining scope

The checker scripts test exact algebra, Gaussian exponent identities, transforms, cutoff scaling and rate bookkeeping. They are not simulations and do not independently prove the continuum SPDE estimates. Those proofs appear in TURN_1.md through TURN_5.md and need adversarial review, particularly the localized comparison, clock stopping-time argument, maximal Sobolev estimates and dependence of constants on the cutoff.

The broader source question does not specify a unique weak-test class or restrict dimension. Its higher-dimensional and sharper bounded-test variants remain unresolved in this packet after5/5 turns. The reconstructed assertion of universal superlinear mean-square half-order is refuted already by the stated admissible one-dimensional case. These dispositions are kept separate.

Best-guess progress toward the broad source bundle:75%, low confidence. This is a planning estimate, not a correctness or novelty probability.
