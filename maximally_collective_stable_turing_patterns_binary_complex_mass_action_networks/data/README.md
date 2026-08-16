# Data dictionary

- `network_instances/`: exact JSON instances for selected values of `m`.
- `simulations/`: deterministic cosine-Galerkin method-of-lines outputs. Profile CSV files contain position and concentrations; amplitude CSV files contain time, adjoint-projected first-mode amplitude, and minimum concentration.
- `branch_amplitudes.csv`: normal-form predictions and measured amplitudes for the base, spatial-refinement, and temporal-tolerance runs.
- `refinement_checks.csv`: 16/32-mode spatial comparisons and base/tight-tolerance temporal comparisons.
- `simulation_parameters.json`: every simulation configuration.
- `figure_source_data/`: compact CSV files consumed by the plotting scripts.

The quadratic reaction products are evaluated by exact cosine convolution before Galerkin truncation. Numerical data illustrate, but do not prove, the exact theorems.
