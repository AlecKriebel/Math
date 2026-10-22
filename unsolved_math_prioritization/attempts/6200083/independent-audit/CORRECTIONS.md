# Nonblocking corrections and clarifications

The author packet is preserved byte-for-byte. The companion patch is an optional
editorial overlay, not a replacement freeze and not a new substantive approach.
No central theorem or status correction is required.

1. **Signed parabolic displacement.** In analysis.md Section 2, change
   `2 asinh(n/2)` to `2 asinh(|n|/2)`, or explicitly restrict that displayed
   equality to n >= 0. All subsequent powers n = 2^k are positive, so the
   obstruction and all 5,859 author controls remain valid.

2. **Proper/geodesic example scope.** In Section 1, restrict the blanket
   assertion about proper geodesic spaces and proper actions to the parabolic
   action of Section 2 and the surface-group action of Section 3. The general
   cone is only guaranteed roughly geodesic by the inspected source, and its
   hypothetical lifted symmetry action is not an established proper discrete
   action. Section 6 already explains this missing group-action condition.

3. **Make the uniqueness hypotheses explicit.** In Section 4, state that the
   surface subgroup is non-elementary and that its compact metrizable limit set
   carries a minimal non-elementary convergence action. Explain that endpoints
   of each infinite-order element lie in the limit set, so restriction preserves
   loxodromic behavior and excludes parabolic subgroups. Under the contradictory
   geometrical-finiteness hypothesis, both compacta are boundaries of the same
   pair (H, empty), which is the precise uniqueness application. Do not replace
   this with an unrestricted boundary-quotient assertion.

Retain “unsolved,” “no full proof or counterexample,” and the explicit statement
that failure of an equivariant boundary map does not establish non-local-
connectedness. A subjective 5% completion estimate is not an audited measure.
