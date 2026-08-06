# Ill-conditioned frozen-phase false positive

An exploratory floating-point search over a five-state conserved defect shell
reported a positive asymptotic level drift.  The candidate used rate constants
spanning roughly nineteen orders of magnitude and evaluated a singularly
perturbed stationary system at `N=10^80` in double precision.

An independent exact matrix-tree calculation over `Q(N)` showed that the
stationary reward numerator has degree two with a **strictly negative** leading
coefficient.  The apparent limiting drift was a conditioning artifact.  The
exact numerator factors as a negative positive-rate prefactor times a quadratic
whose leading coefficient is positive.

This failure is retained because it is a useful warning: direct floating-point
stationary solves at enormous scale are not reliable for fast-slow reward
cycles.  Final sign checks use exact polynomial coefficients or lexicographic
Bellman certificates.
