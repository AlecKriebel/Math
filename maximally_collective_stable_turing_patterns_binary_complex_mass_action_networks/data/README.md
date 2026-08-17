# Data dictionary

- `network_instances/`: exact JSON instances for selected values of `m`.
- `simulations/`: cosine-Galerkin method-of-lines outputs reproducible within the recorded solver and refinement tolerances. Profile CSV files contain position and concentrations; amplitude CSV files contain time, adjoint-projected first-mode amplitude, and minimum concentration.
- `branch_amplitudes.csv`: normal-form predictions and measured amplitudes for the base, spatial-refinement, and temporal-tolerance runs.
- `refinement_checks.csv`: 16/32-mode spatial comparisons and base/tight-tolerance temporal comparisons.
- `simulation_parameters.json`: every simulation configuration.
- `current_profile_exact.json` and `contrast_table.tex`: exact source and
  generated finite-dimensional table used in the manuscript.
- `certificate_tables.tex`, `sign_certificate_tables.tex`, and
  `triad_routh_gap.tex`: generated human-readable exact certificate displays.

The quadratic reaction products are evaluated by exact cosine convolution before Galerkin truncation. Numerical data illustrate, but do not prove, the exact theorems.
