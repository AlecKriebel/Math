# Additive expository notes

These clarifications follow the optional observations in the independent adversarial audit. They do not alter the original research files or enlarge any theorem's scope.

1. In Attempt 2's common-linear-factor case, Q(T) dividing ad−bc is only a necessary filter. For each resulting signed-divisor candidate T that is a nonnegative power of p, test the original condition C|Q(T)| dividing h(T). This final test is essential.
2. In Attempt 4, discard identically zero minors before taking a polynomial gcd. The generic-rank-zero case is treated separately, as in the original proof. Numerical zeros of nonzero pivot minors remain exceptional parameters to be checked directly.
3. Density one in Attempt 1 is relative to integer parameter cubes for the affine lattice. When applying it to exponential fibers, the density constants and the first successful cube may depend on the chosen exponent. No uniform radius or witness bound across those fibers is asserted or needed.
4. The exact regression script is a bounded control, not a general-purpose implementation of the decision procedures proved in the text. The independent audit's additional rectangular and rank-zero matrix controls strengthen those controls without changing their logical role.
