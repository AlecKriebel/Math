# Five mathematical attempts

All energies below use the factor \(1/(2\pi)\). These attempts concern different proof mechanisms; the source checks are not counted as mathematical attempts.

## Attempt 1: Hardy relaxation and integer finite differences

Factor the weight analytically as \(|(1-z)^\lambda|^2\). The first nonzero coefficient of \((1-z)^\lambda P\) is a nonzero integer, giving the universal lower bound 1. It is too weak: at \(\lambda=1\), the exact answer is 2. For integral \(\lambda=m\), multiplication by \((z-1)^m\) produces an integral polynomial, so the problem becomes a discrete squared norm subject to a high-order zero at 1. This identifies the arithmetic constraint that a real-coefficient relaxation would lose.

Outcome: rigorous universal baseline and exact discrete formulation, but no unrestricted extremizer or closed formula.

## Attempt 2: a fractional difference kernel

Derive the Fourier coefficient recurrence by integration by parts. For \(0<\lambda<1\), every off-diagonal coefficient is negative. Absolute convergence and the zero of the weight at 1 give the discrete energy identity (4). Every nonzero integer sequence has at least two nonzero differences in a residue-class chain for every step size. This proves the lower bound \(C(\lambda)\), attained by a monomial. Strict tail contributions classify equality.

Outcome: complete exact determination for \(0<\lambda\le1\).

## Attempt 3: opposite signs after one difference

Write \(Q=(1-z)P=A-B\). Because \(Q(1)=0\), both signs occur. The negative off-diagonal Fourier kernel makes the interaction between the two signs nonnegative; each sign part costs at least \(C(\lambda-1)\). Geometric sums yield the matching limit. Strict interaction proves nonattainment on the interior interval.

Outcome: complete exact determination for \(1\le\lambda\le2\), including the distinction between a minimum and a nonattained infimum.

## Attempt 4: Newton identities and sparse arithmetic witnesses

For integer \(m\), encode positive and negative coefficients as equal-cardinality exponent multisets. Vanishing through order \(m-1\) means equal power sums. If either mass were less than \(m\), Newton identities would force identical multisets. Hence the squared norm is at least \(2m\). Equality requires distinct elements and coefficients only \(0,\pm1\). Explicit products with factor exponent lists (10) attain this for \(m\le6\). Binary subset sums give a general \(2^m\) upper bound.

Outcome: exact integer cases and an exact equivalence with a classical distinct-term ideal equal-power-sum existence problem. The equivalence does not resolve all multiplicities.

## Attempt 5: higher fractional moments and clustered constructions

Apply level decomposition and the decreasing interaction kernel to show that nonnegative integer sequences with mass \(T\) cost at least the interval energy \(G_\alpha(T)\). Combine with the Newton mass bound to obtain (14), and with pointwise weight comparison for (15). For \(2<\lambda<3\), the family \(S_NS_{N+1}\) makes two opposite coefficients adjacent and separates the other interactions; it yields (16) and the upper bound (17).

Bounded exact coefficient controls at half-integer parameters were also used to check formulas and avoid confusing a finite-degree search with the true infimum. Such a search is misleading above 2: the needed geometric-product witnesses have coefficients larger than 1, and no degree cutoff is justified.

Outcome: rigorous higher-parameter bounds with an explicit nonzero gap. No proof that the cluster upper bound is optimal, and no full solution. The five-attempt result is partial, with the original problem unresolved.
