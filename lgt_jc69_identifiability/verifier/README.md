# Exact verifier

Run the complete deterministic suite from the package root:

```bash
make verify-exact
```

Expected final line:

```text
ALL EXACT CHECKS PASSED
```

## Scripts

- `environment_audit.py` — validates the locked SymPy/mpmath versions and MPFR discovery.
- `exhaustive_measure_audit.py` — exact process partition, CTMC kernel, absolute-time density, and topology probabilities.
- `symbolic_audit.py` — site/Fourier inversion, auxiliary-map normalization and integration, exhaustive-process integrations, and compact cube map.
- `jc_transition_audit.py` — direct transition-matrix comparison for all 64 leaf nucleotide patterns.
- `analytic_identity_audit.py` — positive minor, full determinant factorization, convexity identities, and fixed-`(D,M)` derivative formula.
- `scope_topology_audit.py` — cube inverse, common-scale ambiguity, matching-pair factorization, source-point conversion, and likelihood-Hessian cancellation.
- `source_formula_audit.py` — exact transcription, normalization, map difference, positivity, and inequality-reversal diagnostic for the frozen R function.
- `source_diagnostic.json` — machine-readable source identifiers, exact point, original-parameter conversion, and expected rational diagnostic values.
- `verify_table_double_point.py` — outward-rounded Krawczyk proof and Jacobian determinant enclosures for `F_table`.
- `mpfr_interval.py` — minimal MPFR interval arithmetic with directed rounding.
- `certificate.json` — exact target, rational box, precision, center, and rational-decimal preconditioner.

## Krawczyk certificate

The interval proof uses

```text
K(c,B) = c - R G(c) + (I - R DG(B))(B-c),
```

with `G = F_table - target`. Strict containment `K(c,B) ⊂ int(B)` proves that the second box contains exactly one root. Determinant intervals exclude zero throughout that box and at the exact first point. Decimal strings are parsed as exact finite decimals. The root-search trajectory that discovered the box is neither stored nor used.

## Numerical sanity check

Run separately from the package root:

```bash
make audit-simulation
```

This fixed-seed Monte Carlo calculation is not part of the proof.
