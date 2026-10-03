# Planar p-capacity: partial bounds and local segment comparison

Problem [20001670](https://www.unsolvedmath.com/problems/20001670),
AIM-GEOMETRY-0008. Five substantive proof attempts, 3 October 2026.

**Original conjecture: unresolved.** For `1<p<2`, does a segment minimize
homogeneous variational p-capacity among convex planar compact sets with the
same generalized perimeter? A segment's perimeter is twice its length.

This is an AI-assisted, unrefereed research package. It is not a complete
resolution, and priority of its partial results is not established.

## Strongest partial results

1. Every compact convex planar `K` satisfies
   `C_p(K) >= rho^(2-p) C_p(I_{P(K)})`, where
   `rho=0.7472461733...` is the unique root in `(2/3,1)` of
   `rho^2=pi*(1-rho)*sqrt(2*rho-1)`. This improves the imported longest-side
   constant `2/3` by combining area and diameter comparisons.
2. An explicit elliptic-coordinate trial potential strengthens `rho` to the
   p-dependent `rho_p` in Attempt 2. For example, at `p=4/3` its defining
   equation is the exact quartic `rho^4=16*(1-rho)^2*(2*rho-1)`.
3. For each fixed `p`, all sufficiently thin nondegenerate triangles have
   strictly larger capacity than their same-perimeter segments. This includes
   degenerations in which the third vertex collides with a base endpoint.
   The threshold is qualitative, with no claim of uniformity in `p`.
4. The energy of a unit segment's capacitary potential has exact directional
   proportions `(p-1)/p` parallel and `1/p` perpendicular to the segment.

The remaining issue is global control of nonthin triangles. The known
Brunn--Minkowski reduction does not remove this issue. An exact sufficient
bulk-energy inequality is isolated, but unproved, in Attempt 5.

## Reading order

- `SOURCE_GATE.md`: statement normalization, primary references, access limits,
  and prior-attempt search.
- `ATTEMPT_1.md`: area--diameter bound and its geometric minimax.
- `ATTEMPT_2.md`: elliptic-coordinate trial bound and algebraic special case.
- `ATTEMPT_3.md`: energy defect and non-colliding thin triangles.
- `ATTEMPT_4.md`: slit-endpoint barrier and the uniform-in-shape local theorem.
- `ATTEMPT_5.md`: affine-squeezing identities and the exact remaining gap.
- `verify_constants.py`, `checks.json`: 6,145 rational Heron checks, a certified
  rational bracket for the basic constant, an exact quartic bracket, and a
  separately labeled illustrative floating-point table. No PDE computation is
  being certified by this script.
- `RESEARCH_LOG.md`: chronological checkpoints and explicitly subjective
  completion estimates.

No PDF, screenshot, imported corpus, or private conversation material is included.
The full fresh adversarial audit is included as `FRESH_ADVERSARIAL_AUDIT.md`.
It passed the stated partial results and requested two minor rigor
clarifications, now applied in Attempts 3 and 5. `CHANGE_MAP.md` records the
exact scope. These corrections await narrow review; they do not add a sixth
proof attempt or resolve the original conjecture.
