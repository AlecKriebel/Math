# Result and unresolved boundary

## Original question

For every minimal convergence action G on a compact metrizable Z, can one
find a hyperbolic space X with boundary equivariantly homeomorphic to Z and
a uniform quasi-action inducing the given action?

**This packet does not answer that universal question.** The recommended
disposition is `unsolved`, with five substantive author attempts.

## Strongest scoped theorem

For the standard action PSL_2(Z) on RP^1, no hyperbolic graph obtained from
a symmetric invariant annulus system with finitely many group orbits, via
the Bowditch triple quasimetric and its equivariant graph realization, has
boundary equivariantly homeomorphic to RP^1.

The proof has four steps, all detailed in TURN_4.md:

1. Finite-orbit annulus systems cannot contain infinitely many annuli
   separating a fixed pair from a nonconical point.
2. Canonical triples approaching such a point stay bounded. A parabolic
   element fixing it has a bounded orbit in the resulting triple metric.
3. In PSL_2(Z), infinity is nonconical. A conical sequence would have
   determinant-one integer matrices whose two projective columns approach
   distinct limits, while the determinant and column-norm estimate force
   those limits to agree.
4. The translation x->x+1 therefore has bounded graph orbits. Isometries
   with bounded base-point orbits act equicontinuously on a compact
   hyperbolic boundary; the parabolic circle action does not. An equivariant
   boundary homeomorphism is impossible.

PSL_2(Z) nevertheless acts isometrically on H^2 with precisely the prescribed
circle boundary. The theorem is consequently an obstruction to a specified
construction family, not a negative answer to Kapovich's problem.

## Other proved deductions

- Every finite Z has an explicit star-tree realization. In the infinite
  case, Z is perfect, G is countable and infinite, and the action kernel
  is finite (TURN_1.md).
- Bowditch's established annulus conditions (A1)-(A3), together with the
  explicit equivariant graph bounds supplied here, give a sufficient route
  to an exact isometric realization. The general hypotheses do not supply
  the missing condition in this work (TURN_2.md).
- Uniformly equicontinuous boundary remetrization is impossible in the
  nonelementary setting. On an explicit tree-comparable metric space,
  fixed-height free-group lifts individually have additive error 2|g|,
  but no uniform quasi-isometry constants work for the family (TURN_3.md).
- Taking all annuli makes distinct-quadruple crossratios infinite; sums or
  maxima of individually hyperbolic pseudometrics can acquire arbitrarily
  large four-point defects (TURN_5.md).

## Limits

The annulus construction and finite-boundary mechanism are credited to
Bowditch, Sun and Azemar. The modest scoped deductions carry no priority
claim. An invariant controlled infinite annulus system, or an alternative
universal interior construction, is still missing. No genuine example
without any uniform hyperbolic realization has been found here.

The 59,002 exact finite assertions replay deterministically. They check
identities, finite geometry, and explicit witness formulas. They do not
prove the compactness arguments, unbounded limits, or topological boundary
claims and are not a substitute for the written proofs.
