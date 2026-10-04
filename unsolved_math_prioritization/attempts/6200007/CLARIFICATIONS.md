# Additive clarifications after independent review

The frozen author and independent-audit files remain unchanged. These points
implement the audit's nonblocking clarifications and sharpen the precise gap.

## Bowditch's infinite annulus system is already available

For a convergence action on a perfect metrizable compactum, Bowditch's
Proposition 8.2 already constructs a symmetric invariant annulus system,
possibly with infinitely many group orbits, satisfying:

- (A1): finite distinct-pair versus distinct-pair chain lengths
- (A2): at least two of the three quadruple chain lengths are zero
- (A4): every two distinct points are separated by an annulus

Thus no general existence gap for A1+A2+A4 is claimed. The missing hypothesis
in the sufficient route described in the author packet is (A3) at every
point: arbitrarily long annular chains separating a pair from a third point.
Bowditch's Lemma 8.3 provides this at conical points, and hence provides it
globally if every point is conical. It does not, by this argument, supply
(A3) at arbitrary nonconical points.

Source: [Bowditch, Section 8, Proposition 8.2 and Lemma 8.3](https://bhbowditch.com/papers/bhb-topchar.pdf#page=24).

The author packet's unrestricted all-annuli example and sum/maximum examples
refute those particular enlargement shortcuts. They do not refute Bowditch's
controlled construction. Likewise the finite-orbit modular obstruction
does not rule out infinite systems or other interior geometries.

## Norm and equal-ray conventions

In the determinant-one column-angle proof in `author/TURN_4.md`, the column
norms are Euclidean norms. The normalization of the matrices can use their
maximum-entry norm. Projective convergence away from the limiting kernel
follows because normalized output-vector norms have a positive lower bound
on each compact set there.

In the fixed-height proof in `author/TURN_3.md`, the difference of two
common-prefix lengths is asserted for distinct boundary rays. Equal rays
are handled separately: their lifted distance depends only on the heights,
so it is preserved. No subtraction of infinity from infinity is needed.

These are not changes to the theorem conclusions. The original universal
realization question remains unresolved, and PSL_2(Z) retains its ordinary
positive realization on H^2.
