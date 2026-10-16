# Weak Bianchi identities across regular timelike ZAS

Problem 30004807 / OWR-8415343-010.

Candidate complete counterexample to the universal geometric conjecture in Oberwolfach Report 40/2021, pp. 2232–2233, using the primary paper's smooth boundary-reaching test fields. Pending fresh independent adversarial audit; no historical-priority claim.

For any (a>0), take
\[
g=-(1-a/\rho)^{-2}dt^2+(1-a/\rho)^4(d\rho^2+\rho^2d\Omega^2),\qquad \rho>a.
\]
Every static spacelike slice has the standard regular negative-mass Schwarzschild ZAS, of mass (-2a). Nevertheless a smooth compactly supported radial test, normalized in time and equal to the radial unit-coordinate field near the inner boundary, has
\[
\int_M G^\mu{}_{\nu}\nabla_\mu\psi^\nu\,dV_g=-8\pi.
\]
The full contracted density is absolutely integrable. This is not a principal value or an undefined product of distributions.

The metric has the borderline curvature growth excluded by BKTZ's sufficient theorem. It violates the null energy condition, so stronger matter-restricted questions remain outside the claim.

## Contents

- `PROOF.md`: analytic proof, geometric and test-space checks, and exact lapse-family boundary defect.
- `SOURCE_GATE.md`: primary-source provenance and claim boundary, including the page-break conjecture.
- `RESEARCH_LOG.md`: first-attempt construction, cross-checks and exclusions.
- `checks/verify_bianchi_counterexample.py`: exact symbolic checks from the coordinate metric.
- `checks/verification_results.json`: generated results.

Run the checks with Python 3 and SymPy:

    python checks/verify_bianchi_counterexample.py

No source PDFs, full extracted source texts, private catalogue material, or large search corpus are included.
