# Verification design and limitations

## Exact vanishing

For each N, the script reduces each x^a modulo the integer cyclotomic polynomial Phi_N. A multiset sum vanishes at a primitive N-th root precisely when its integer remainder vector is zero. This is an exact algebraic test, independent of approximate complex arithmetic.

Every root multiset can be rotated by one of its entries to contain 1; sorting its remaining exponents gives one of the enumerated tuples. Thus normalization loses no possible modulus, although different tuples can represent the same rotational orbit. Repetitions are retained.

## Certified real intervals

The script constructs rational lower and upper bounds on arctan(1/5) and arctan(1/239) by the alternating series, then uses Machin's identity pi=16 arctan(1/5)-4 arctan(1/239). For completeness: tan(2 arctan(1/5))=5/12; tan(4 arctan(1/5))=120/119. Subtracting arctan(1/239) gives tangent exactly 1. The difference is in (0,pi/2), so it equals pi/4.

A root difference angle is reduced to [0,pi]. At the rational midpoint of the angle enclosure, the cosine Taylor polynomial through degree 60 is evaluated exactly as a Fraction. View this as degree 61 with zero odd coefficient: the order-62 remainder is at most 4^62/62!, because the angle is smaller than pi<4 and every real derivative of cosine has modulus at most 1. The extra angle uncertainty is bounded using the same derivative bound. The final interval is rounded outward to integers divided by 10^30.

For S=sum zeta_N^{a_j}, |S|^2=m+2 sum_{i<j}cos(2pi(a_i-a_j)/N). Interval addition therefore certifies a squared-modulus enclosure. Exact zeros must enclose 0. Every exact nonzero in the finite range must have strictly positive lower endpoint. The small-m analytic lower bounds are checked by comparing the squared rational bound to that lower endpoint.

For each pair (m,N), the minimum of lower endpoints and minimum of upper endpoints enclose the true finite minimum squared modulus. The reported tuple supplies the upper bound; it is not asserted to be the unique minimizer. Square roots are not numerically approximated or used as certificates.

## Algebraic identities

For 21 prime-order examples, with repeated coefficients included, the script separately computes integer cyclic convolution counts, a cyclotomic resultant, and the polynomial inverse of P(x)P(x^{-1}) modulo Phi_p. Taking its exact trace uses Trace(zeta_p^a)=-1 for 1<=a<=p-2 and Trace(1)=p-1. It checks both Fourier-count identities and the trace ratio, rather than merely comparing two floating evaluations.

Twelve sparse-polynomial cases verify the factorization at x=1, the multiplicity-versus-support inequality, and the quotient coefficient bound. Their infinite justification is the proof in PROOF.md; the finite examples do not establish it by themselves.

## Negative controls and runtime

Eight exact semantic controls rule out dropping the nonzero restriction, forbidding repetition, absorbing signs without adjusting an odd conductor, confusing support size and coefficient mass, extending prime nonvanishing to composite conductors, using subsum bounds to forbid total cancellation, assuming rotation forces a short exponent interval, and assigning exponent 2 to the eight-term case.

Checks raise explicit exceptions and do not use Python assert, so Python -O does not disable them. The integrity checker separately rejects changed bytes, removed files, extra files, duplicated paths, traversal paths, absolute paths, symlinks, nested-manifest extra files, and a symlinked manifest. These controls protect reproducibility, not mathematical truth beyond the statements actually checked.

No independent audit is included in the author's package. An independently written checker and line-by-line mathematical/source review are still needed before promoting any scoped conclusion.
