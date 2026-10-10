# Five-approach research log

Problem 2303015, Function Theory 3.15. All times below are UTC on 2026-10-04.
Source triage was completed before the mathematical approaches. The five
approaches below constitute the entire substantive proof-search budget for
this attempt. None produced a complete candidate resolving the source target.
Completion estimates are subjective planning estimates, not probabilities or
fractions of a theorem proved.

1. **08:17, harmonic comparison and annular normalization.** Conformal
   normalization makes the boundary harmonic interpolant affine in log radius.
   Proved emptiness for A>0 under finite boundary limits, exact equality with
   the harmonic interpolant when A<=0 and h(z1)<=0, and reduced the genuinely
   constrained regime to A<=0<B, h(z1)>0. Gap: comparison alone is not sharp in
   that regime. Full-goal completion estimate: 10%.

2. **08:18, logarithmically convex radial extremals.** Derived and proved the
   optimal broken-line logarithmic profile, including the slope-jump formula
   h(z1)/(s(1-s)). This proves feasibility for all A<=0 and resolves the entire
   coincident-marked-point case. Gap: the radial restriction has no
   justification for the original free-curve problem. Estimate: 15%.

3. **08:20, Green-potential concentration and point-constraint relaxation.**
   Truncated Green kernels give continuous subharmonic competitors with a
   forced nonpositive value at z1 and values tending to the harmonic envelope
   at every other fixed point. This proves that an isolated-point relaxation
   cannot retain the desired curve information. Gap: its competitors generally
   have only a tiny constrained component around z1, without a path to alpha.
   Estimate: 15%.

4. **08:21, fixed-slit Dirichlet problems and harmonic measure.** For A=0,
   a radial slit gives a rigorous harmonic-measure solution of the fixed-path
   problem. Its extension is subharmonic and strictly improves the radial
   envelope at marked points inside the tip radius but away from the slit.
   This falsifies radial optimality. For A<0, imposing zero on the whole slit
   contradicts the boundary limit at its attachment. Literature on extremal
   wires and quadratic differentials is related, but no checked theorem
   settled this two-boundary-value annular problem. Gap: optimize the path;
   for A<0 first solve its nonconstant-obstacle envelope. Estimate: 15%.

5. **08:23, uniform path penalty by an explicit Green potential.** Constructed
   a probability measure on a subpath using first radial hitting points.
   Its linear ball-mass bound gives a uniform bound for its Green potential.
   Comparison then proves a positive gap below the harmonic envelope,
   independent of the admissible path, whenever h(z1)>0 and z0!=z1. The full
   analytic proof is in RESULTS.md, Section 5. Gap: this bound is not sharp
   and does not select a minimizing path or prove attainment. Estimate: 20%.

## Stopping verdict

The full source problem remains unresolved. Proposed literal queue status:
`unsolved`; substantive approaches: `5/5`. Exact special cases, a counterexample
to a tempting restricted ansatz, and a uniform quantitative upper bound have
been preserved. No more proof search is part of this frozen attempt. A later
review may test the saved claims without being counted as a new search phase.

## Reproducibility

Run `python3 verify.py` in this directory. Python 3.10 or newer and its standard
library suffice. The script checks exact radial identities and solves a small
periodic-cylinder Dirichlet graph using rational Gaussian elimination. See
RESULTS.md for the limits of these controls. The checked output is saved in
verification.json. The SHA-256 manifest binds every public artifact except
the manifest itself.
