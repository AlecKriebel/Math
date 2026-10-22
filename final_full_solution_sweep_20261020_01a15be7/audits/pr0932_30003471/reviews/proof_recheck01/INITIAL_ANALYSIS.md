# Independent initial analysis

Timestamp: 2026-10-21T20:03:31.871400+00:00

This note precedes all historical audit conclusions.

Exact proposed strengthening: compact full-dimensional Euclidean convex 3-polytopes with a fixed face-lattice isomorphism and weak interior-dihedral dominance on every corresponding edge have equal complete facet-normal Gram matrices. It does not assert support-number or edge-length rigidity.

Initial attack families:

1. **Geometric counterexample / strength.** A prism reduction turns edge-angle dominance into a polygon turning-angle comparison, where the 2pi angle sum prevents strict dominance; support changes can preserve normals, so equal-normal examples are not counterexamples. For general polytopes a spherical normal fan has all edge lengths weakly contracted. A naïve piecewise extension on spherical vertex polygons can fail; the proof avoids that issue by deleting vertex neighborhoods of critical boundary capacity. Need check degree-one compatibility rather than assume a 1-Lipschitz global map exists. Nonsimple vertices specifically require the hemisphere margin to hold for every incident target normal.

2. **Analytic black box.** Primary dependency is the exact positive index and matrix/spinor convention in Brendle v4. This is central: if positive index needs pointwise angle matching, strict convexity, an orientation convention opposite to degree one, or a different boundary relation, the proof may fail. Must recover propositions, signs, norm coefficient and the equivalence of a spinor tuple and a 2x2 matrix.

3. **Uniform geometry.** Radial maps between fixed-inner/outer-ball convex bodies appear uniformly bi-Lipschitz; one must verify their boundary measure and H1 transport constants. Active-facet localization should be a Hoffman/error-bound property. Need test the proof's normal-cone argument with nonsimple vertices and disconnected nonadjacent facet pairs.

4. **Critical cutoff.** For dimension three the boundary is two-dimensional; a logarithmic radial cutoff has L2 gradient tending to zero. This succeeds only when the interpolation is nonexpanding in the zeta argument, so it does not multiply the large edge curvature by a factor greater than one. On a hemisphere, spherical interpolation toward a fixed q has singular values t and sin(t theta)/sin(theta), both <=1. Uniform bounds on q derivatives add only O(1) error. Must verify the actual smoothed boundary radial pullback down to the inner scale lambda^-1/2.

5. **Limit and final algebra.** H1 extension plus Rellich appears enough to prevent mass loss. A fixed flat patch gives strong H1 convergence and hence boundary relation. A nonzero intertwining matrix has C*C commuting with a spanning Clifford family; this forces invertibility and Gram equality. The normal vectors of a bounded full-dimensional polytope span R3. Need independently check adjoint signs and representation multiplicities.

No flaw or counterexample found at this initial stage. No conclusion yet: specialized index and boundary estimate require primary verification, and geometric details require independent derivations.
