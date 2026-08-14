# Independent verifier

This directory is a definition-level implementation written for Phase III.  It
does not import the inherited T-ALG code.  It reconstructs indexed reaction
matrices, mass-action fluxes and Jacobians, the PARTITION reduction, and the
fixed-species projected flux cone.

Run all tests from the Phase III root with:

```bash
python -m unittest discover -s independent_verifier/tests -v
```

The red-team scripts in `../red_team/` add exhaustive bounded-matrix tests,
random rational tests, global numerical searches, and mutation checks.
