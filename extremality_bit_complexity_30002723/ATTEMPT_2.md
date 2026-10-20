# Attempt 2: interval-pairing compression and the continuous case

Date: 20 October 2026. This is a substantive structural reduction, not a polynomial-in-q bound relabeled as a bit bound.

## Arithmetic bottleneck

An additive horizontal/vertical edge sends equal-length grid intervals to one another by a translation. An additive diagonal edge sends intervals by a reflection. On cell indices these are integer interval pairings i -> i+t or i -> c-i-1. Thus the q-cell graph can be specified by polynomially many partial order-preserving/reversing interval bijections, each using O(log q) bits.

Agol–Hass–Thurston, *The Computational Complexity of Knot Genus and Spanning Area*, Theorems 12 and 16, provide basic and weighted orbit-counting algorithms polynomial in the number/encoding of pairings and log N. The weighted algorithm accepts a piecewise-constant vector weight and returns orbit-weight groups with multiplicities. It does not explicitly enumerate exponentially many orbits.

Primary source inspected: https://arxiv.org/html/math/0205057v2, §§4 and 6.

## Seed merging

The interval lemma on a two-dimensional additive face forces a single slope across each of its three entire projection intervals. Connecting adjacent cells within those intervals and connecting their representatives is therefore justified, unlike merging arbitrary cells with the same input slope.

If every orbit is seeded by a two-dimensional additive projection, there are only polynomially many slope variables. Weighted orbit counting with seed markers and prefix indicators gives the integral of each slope variable up to every sparse arrangement vertex coordinate. If an orbit is unseeded, Part I Lemma 4.8 supplies an effective perturbation, so the input is not extreme.

## Continuous subclass conclusion

For continuous input, unrestricted competitors are Lipschitz by Part I Theorem 2.9. Thus a perturbation is recovered by integrating its slope variables. Along an additive edge its derivative is zero after paired slopes are identified; across an additive two-face all three projections have one slope. Consequently the additivity equations reduce to finitely many sparse endpoint equations. This gives a polynomial-bit extremality test for the continuous subclass using weighted AHT.

A full derivation is in `structural/CONTINUOUS_AHT_REDUCTION.md`. Dense exact checks in `structural/` compare the compressed mathematical reduction with 4q-grid rank; they do not claim to implement AHT.

## Why this is not yet the full target

For a discontinuous input, perturbations need not be continuous at artificial grid points. Slope integrals alone miss jump and isolated point-value variables. The next attempt treats these variables explicitly instead of silently imposing regularity.
