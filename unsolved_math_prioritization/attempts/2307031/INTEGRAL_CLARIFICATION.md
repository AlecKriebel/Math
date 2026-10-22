# Controlling integral clarification (C1)

This paragraph controls the integral-equivalence wording in Corollary 3 of
`author/PROOFS.md`. The frozen authored text and the complete independent
audit are retained unchanged as the review record.

For a nonnegative, locally bounded function f on [1,infinity) that tends to
zero and is eventually nonincreasing, choose A>=2 such that f is
nonincreasing on [A,infinity). The discrete sufficient condition

    sum_{k>=1} (k+1) 2^(k/2) f(2^k) < infinity

is equivalent to

    integral_A^infinity f(t)(1+log t)/sqrt(t) dt < infinity.

The integral is a Lebesgue integral on the monotone tail. If f is also
measurable on [2,A], local boundedness makes this equivalent to the
integral beginning at 2. Without that measurability assumption, the
integral beginning at 2 need not be defined. Eventual monotonicity alone
does not supply measurability on the entire initial interval.

To verify the equivalence, choose an integer K with 2^K>=A. Monotonicity
sandwiches f on each [2^k,2^(k+1)] between its endpoint values. The weight
integral over that shell is bounded above and below by positive constant
multiples of (k+1)2^(k/2). Shifting k by one changes these weights by bounded
factors, so the tail integral and discrete tail converge together. The
finite portion from A to 2^K is measurable and bounded. The finitely many
initial discrete terms are finite by local boundedness. Measurability on
[2,A], if separately imposed, similarly controls the remaining interval.

This resolves exactly the audit's C1 formulation issue. It does not alter
the counterexample, counting bound, discrete criterion, extremal count,
or continuous logarithmic examples. It neither establishes necessity nor
settles the broad classification, the additional shape condition, or the
logarithmic range 1<p<=2. No novelty or priority is claimed.
