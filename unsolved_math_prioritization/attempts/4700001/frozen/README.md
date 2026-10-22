# Low degree rigid systems: audited-scope research attempt

- Numeric target: 4700001 / AMR-046-0001; queue rank at inspection: 635.
- Status: **unsolved**.
- Date: 2026-10-04.
- Full target: determine whether two is the maximum number of isolated finite planar periodic orbits of
  x' = -y + x(a+bx+cy+dx^2+exy),
  y' = x + y(a+bx+cy+dx^2+exy),
  over real a,b,c,d,e.

No stability, hyperbolicity, smallness, boundedness of all trajectories, or genericity condition is imposed on the target. Centers' nonisolated periodic orbits do not count as limit cycles. Orbits on a compactification's circle at infinity are not finite planar limit cycles.

## Outcome

The global upper bound remains unproved. This packet gives self-contained, checkable partial results:

1. An at-most-one, hyperbolic-cycle proof when e=0 and d is nonzero, using the return map's Schwarzian derivative; the degree-two degeneration d=e=0 has no limit cycles.
2. A complete existence and stability criterion when b=c=0: for a nonzero, there is one cycle exactly when -d/a>0 and |d|>|ae|. Its multiplier is exp(-4*pi*a). The boundary equality is excluded. The a=0 cases are handled separately.
3. An independent small-parameter derivation of at least two hyperbolic cycles for a=-epsilon^4/2, b=c=e=1, d=2*epsilon^2, for every sufficiently small positive epsilon. The inner cycle is unstable and the outer cycle stable.
4. Exact general periodic-orbit and pairwise identities, together with the unresolved sign-changing obstruction.
5. Reproducible floating-point probes, with center, one-cycle, and two-cycle controls. These are not validated numerics and do not exclude missed or nonhyperbolic cycles.

These reproduce and clarify known mechanisms. No novelty or full resolution is claimed. The 2024 primary survey expressly retains the full upper-bound problem as open; the literature check is bounded, not a guarantee that no later result exists.

## Files and reproduction

- `PROOF.md`: exact hypotheses, partial proofs, and remaining gap.
- `SOURCE_GATE.md`: source identity, inspection scope, and relevant current-literature distinctions.
- `ATTEMPT_LOG.md`: five distinct approaches and heuristic progress estimates.
- `check_symbolic.py`: exact symbolic identities; run with Python and SymPy.
- `check_numeric.py`: SciPy exploratory controls and bounded scan; run with Python, NumPy, and SciPy.
- `numerical-results.json`: the recorded full numeric outputs and parameters.
- `verification-metadata.json`: public-source hash and retrieval metadata only.

Run `python check_symbolic.py`, then `python check_numeric.py > numerical-results-rerun.json`. Numerical values may vary slightly with platform or library version. The analytic proofs do not depend on the numerical scan. No third-party full texts, datasets, or source PDFs are part of this packet.
