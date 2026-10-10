# Author self-check

This is an author-side check, not an independent audit, referee report, or formal verification.

- Proposition 1: checked the Li_2 lower-end constants, logarithm absorption, all-epsilon quantifier, and prime-power remainder. All integration steps are real.
- Proposition 2: checked the sign in mu*Lambda=-mu log and the subtraction of y-1 in R. Integer and noninteger endpoints obey the same finite sum formula. The bound O(x) is reported as a loss, not as the desired square-root estimate.
- Proposition 3: checked the weighted isometry, both exponential tails of the convolution kernel, truncation/Bochner approximation, the use of finite weighted measure on [1,infinity), real s>1 absolute multiplication, the dominated limit proving integral M/u^2=0, and the sign of the dilation difference. The actual Möbius H_2 moment is known to diverge; this route's endpoint condition is explicitly identified as nonviable.
- Proposition 4.1: checked integrability of C below zero in logarithmic coordinates, finite floor expansion, and the descending support argument ending at 1. The assertion is only for upper-bounded support, not arbitrary L2 annihilators.
- Proposition 4.2: checked both exponential constants, the negative-shift value 1/8, the tail ODE signs, and that exp(-s) cannot be in L2 of the whole real line. This auxiliary kernel is never identified with the Nyman kernel.
- Proposition 5.1: checked the finite/infinite sum separation, the sign of f, N>=R, the integer breakpoint convention, the real inverse-series bound A_epsilon<=epsilon, and the near-zero weighted norm. The enormous diagonal cutoffs are an existence choice, not a computation.
- Proposition 5.2: checked local-to-weak convergence using a uniform global bound, real closed-subspace weak closure, and the recursive convex-average norm estimate. Neither uniform boundedness nor its necessity for the chosen diagonal is asserted.

## Executed finite controls

`python3 check_controls.py` produces CONTROL_RESULTS.json, with 23,767 exact assertion groups. Arithmetic uses standard-library integers and fractions; logarithmic identities are checked as rational prime-exponent vectors. Covered groups include divisor cancellation, logarithmic convolution, the exact real Möbius integral equation at rational x, damped fractional-part identities, endpoint conventions, escaping-mass norms, compact-support tail expansions, and the two-exponential separation constants.

These controls validate only their finite identities and constants. They do not prove an asymptotic, a uniform infinite family bound, any density theorem, RH, or the methodological equivalence. The analytic arguments are supplied in full for external review.

The packet verifier enforces complete-file inventory, lengths and SHA-256 values and can replay the exact controls. Its mutation tests target integrity failures, not mathematical validity.
