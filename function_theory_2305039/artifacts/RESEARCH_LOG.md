# Five substantive attempts

Problem: Hayman–Lingham 5.39; catalogue 2305039 / AMR-022-5039.
Research date: 3 October 2026.
Overall outcome: partial results, with the finite-exponent question for p>2 unresolved.

## Attempt 1: weighted coefficients and the known quadratic case

The primary statement and its update were checked, including the definition of subordination immediately before Problems 5.38–5.40. In particular, no univalence restriction is present in Problem 5.39. The classical coefficient route was reconstructed from the integral-mean contraction: truncate the outer function, compare the first N squared coefficients, then sum with the decreasing weights n²r^(2n−2). This proves the sharp p=2 radius 1/2. The complete relevant coefficient proofs in Reich's Lemmas 5 and 6 were inspected. The nearby 2025 weighted-coefficient work was checked to distinguish its quadratic framework from the arbitrary-p question.

Outcome: a self-contained proof of the known case and a precise weighted-composition formulation. Failure point for the general case: coefficient-square dominance directly controls p=2 only.

## Attempt 2: zero removal and downward extrapolation

The input derivative was factored into a finite radius-r Blaschke product and a zero-free factor. Fractional powers of the latter need only be holomorphic near the closed radius-r disk: approximation by Taylor polynomials extends the universal weighted inequality to that local class. Hölder then interpolates the derivative weight between exponent q and exponent 0, where the latter is ordinary integral-mean contraction.

Outcome: a complete proof that r_p is nonincreasing in p and that r_p=1/2 for every 0<p≤2. Boundary zeros are handled by radial approximation. Failure point: this interpolation is one-directional; for p>q its Hölder exponents are invalid, so it does not establish a half-radius beyond p=2.

## Attempt 3: perturb a degree-two Blaschke map

For f(z)=z and φ_a(z)=z(a+z)/(1+az), the derivative mean on the half-radius circle was expanded at a=0. Explicit Laurent averages give the second-order term p(p−16)a²/64. This was checked by rational arithmetic.

Outcome: for every p>16, a sufficiently small nonzero a gives a strict violation, and continuity moves it below radius 1/2. Thus a conjectural half-radius for all finite exponents is false. Failure point: the expansion gives neither a sharp radius nor an obstruction for every p>2. The vanishing coefficient at p=16 is not treated as a proof at that endpoint.

## Attempt 4: convert a finite-dimensional test into an exact counterexample

A modest numerical exploration of the degree-two Blaschke family and low-degree polynomial derivatives suggested a stronger obstruction. Floating-point quadrature and truncated operator eigenvalues were used solely to select a candidate, never as a certificate of an infinite-dimensional inequality. The selected functions were simplified to f(z)=z+z²/10 and φ(z)=z(2/3+z)/(1+2z/3).

At p=14 and r=99/200, Parseval applied to (g′)^7 turns the desired strict violation into a lower bound from only its first eleven coefficients. Every coefficient and the resulting positive difference were then recomputed with exact rational arithmetic, including a separate denominator-recurrence check. The omitted terms are nonnegative, so no numerical tail estimate is required.

Outcome: an explicit admissible example with a rigorously positive mean-power difference exceeding 1/200. Monotonicity gives r_p≤99/200 for every p≥14. Failure point: no extremality theorem for this pair or family is known here, and the bound is not asserted sharp. Numerical nonviolations at smaller exponents are not proofs.

## Attempt 5: optimize the pointwise derivative bound and pass to large p

Schwarz–Pick for φ(z)/z reduces the universal pointwise estimate to maximizing t+r(1−t²)/(1−r²), 0≤t≤1. Its threshold is √2−1. Above that threshold a disk automorphism realizes a derivative strictly larger than 1 at one point. The convergence of L^p means of a continuous circle function to its maximum then produces violations for all sufficiently large exponents.

Outcome: a complete proof of lim_{p→∞}r_p=√2−1 and of the sharp auxiliary maximum-modulus radius. Failure point: pointwise optimization does not control the distribution of derivative values needed for an exact finite-p optimum. Together, the five attempts do not determine any exact finite-p radius with p>2.

## Final boundary of the result

The original problem asks for an exact radius for every p>0. That request remains unmet for p>2. The package records precise partial theorems and a counterexample to a possible universal-half-radius guess; it does not reclassify the full problem as solved.
