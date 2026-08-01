# A weakly reversible mass-action continuum without a common factor

This directory contains a complete exact construction:

- three species;
- ten complexes and twenty directed reactions;
- a connected reversible graph (one linkage class);
- positive integer rate constants;
- full stoichiometric rank;
- a positive algebraic ellipse of equilibria; and
- coordinate-polynomial gcd equal to `1`; and
- a radical steady-state ideal, exactly decomposed into the conic prime and a
  degree-15 maximal ideal.

The manuscript-ready proof is in `MANUSCRIPT.md`, the machine-readable reaction
list is in `network.csv`, the post-solution literature check is in
`PRIORITY_AUDIT.md`, and `verify_construction.py` independently reconstructs
and checks every exact claim.

Run the verifier from the repository root with

```text
.venv/bin/python weakly_reversible_continuum_no_common_factor/verify_construction.py
```
