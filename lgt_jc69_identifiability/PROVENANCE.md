# Provenance and AI-assistance disclosure

**Version 0.2 — prepared for author audit — August 2026**

## Assistance and authorship workflow

- AI systems assisted with stochastic-model derivation, symbolic manipulation, proof drafting, interval-certificate implementation, document restructuring, and reproducibility packaging.
- Computational searches were used during discovery to locate the second preimage of the auxiliary map and to explore algebraic factorizations. Search output is not used as a theorem certificate.
- The final mathematical claims are presented as human-readable arguments in `main_manuscript.tex`; source attribution and immutable version metadata are separated into `SOURCE_SNAPSHOT.md`.

## Software-independent proof components

The following arguments can be checked directly from the manuscript without executing software:

- the omitted two-transfer movement example;
- the three-state occupancy-chain construction and its transition kernel;
- the exhaustive partition and topology probabilities;
- the JC69 Fourier reduction;
- the cube reparameterization and unknown-rate scale invariance;
- the fixed-`(D,M)` monotonicity reduction, feasible-interval crossing argument, Jacobian sign inequalities, and global injectivity conclusion;
- the matching-pair topology corollary;
- the inverse-function and population-likelihood Hessian lemmas.

## Exact symbolic verification

The scripts below independently reproduce displayed identities and integrations with exact rational/symbolic arithmetic:

- `verifier/exhaustive_measure_audit.py`
- `verifier/symbolic_audit.py`
- `verifier/jc_transition_audit.py`
- `verifier/analytic_identity_audit.py`
- `verifier/scope_topology_audit.py`
- `verifier/source_formula_audit.py`

They check algebra; they do not replace the manuscript's global sign arguments.

## Rigorous interval verification

- `verifier/verify_table_double_point.py` and `verifier/mpfr_interval.py` constitute the directed-rounding interval verifier.
- `verifier/certificate.json` contains the exact anchor, target, rational interval box, precision, and rational-decimal preconditioner.
- All elementary operations and transcendental functions are enclosed using MPFR-directed rounding.
- Strict Krawczyk inclusion proves existence and uniqueness of the second root in the recorded box; determinant intervals prove regularity at both preimages.

These files are logically independent of the numerical root search that first suggested the box.

## Numerical audit

`verifier/simulate_process_audit.py` is a fixed-seed Monte Carlo sanity check. It is separated under `make audit-simulation` and is not theorem-bearing.

## Independent checks recorded in the archive

The archived exact transcript covers normalization, direct integrations, all 64 JC69 leaf patterns, global-injectivity identities, topology and scale claims, source-formula diagnostics, and the Krawczyk proof. The clean-unpack transcript records fresh LaTeX compilation and all verifier targets. The per-file and per-archive SHA-256 manifests make the audited bytes explicit.
