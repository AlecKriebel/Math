# Attempt 5 of 5: continuum witnesses and the endpoint barrier

3 October 2026. Mechanism: turn numerical evidence into a rigorous witness.
Estimated full-target completion: 20%; final verdict unresolved, 5/5 exhausted.

## A sufficient witness

For a measurable multiplication operator T, compactly supported tests g,h
with disjoint supports and lying in the operator/form domain satisfy

    ⟨g,Th⟩=0.                                                (5.1)

Therefore one certified nonzero continuum pairing disproves multiplication.
For mass independence, one certified difference

    ⟨g,(M_−(m₁)−M_−(m₂))h⟩≠0                               (5.2)

in a justified common realization suffices. These are one-sided witness tests;
failing to find such tests does not prove multiplication or independence.
In particular, a local differential operator also satisfies disjoint-support
pairing tests, so their vanishing alone is not a characterization without
additional order/boundedness hypotheses.

In n=3, a global rotation-invariant multiplier is radial. With spherical
harmonics normalized in L²(S²), it acts by the same radial multiplication on
every angular-momentum sector. Thus a certified difference of two radial
sector pairings for the same radial tests would also refute global
multiplication. Merely seeing different finite matrices in those sectors is
not such a certificate.

## Why convergence cannot be asserted from stability of plots

For a scalar ε>0,

    arcoth(1+ε)=(1/2)log((2+ε)/ε).

The two scalar matrices B_ε=1+ε and C_ε=1+2ε differ by ε→0, but

    arcoth(B_ε)−arcoth(C_ε)
      =(1/2)log(2(2+ε)/(2+2ε)) → (1/2)log2 ≠0.             (5.3)

Using 1+exp(−N) gives arcoth values growing like N/2. The numerical precision
problem is structural: an absolute error small for B need not be small after
arcoth near ±1. Higher precision solves roundoff, not the continuum limit.

There is a useful bound when a uniform gap does exist. If selfadjoint bounded
B,C both have spectra in (−∞,−a]∪[a,∞), a>1, then the resolvent identity and
the integral representation from Attempt 1 give

    ||arcoth B−arcoth C||
      ≤ ||B−C|| ∫₀¹ (a−t)^−2 dt
      = ||B−C||/[a(a−1)].                                  (5.4)

This bound does not require B and C to commute or to have the same sign.
The sharper scalar derivative bound 1/(a²−1) cannot simply be substituted
for general two-sided operator spectra in this argument. The estimate blows
up as a↓1, exactly where the field numerics place eigenvalues.

## What would complete a numerical certificate

Suppose a verified finite interval [L,U] contains a discretized pairing, and
one separately proves an error bound η covering basis truncation, spatial
cutoff, and the singular functional calculus for those fixed test functions.
Then L>η or U<−η proves the corresponding continuum pairing is nonzero.
For a difference of two masses/sectors, the two independent certified error
bounds add. A ball-specific bound of this type was not found or proved.

A possible alternative is a resolvent construction based on Fröb's restricted
two-point-function formula; this changes the representation but leaves an
unevaluated spectral problem. Substituting that formula is not a solution.

**Final outcome:** rigorous witness criteria and conditioning obstruction;
no certified nonzero continuum witness. Five substantive attempts are complete.
Further unbounded-operator analysis would be a new research budget, not an
independent audit of a completed solution.

