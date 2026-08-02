# Stationary component-odds closure

This directory isolates the remaining stationary-mixture problem at
fitness `r=2`.

* `STATIONARY_ODDS_SPLIT.md` gives the proved direct stationary/resolvent
  formulation, the exact two-piece split, and exact route counterexamples.
* `verify_stationary_odds_split.py` is the standard-library exact
  certificate.
* `search_split_counterexamples.py` is a floating-point adversarial search
  used only for discovery.

The component-odds inequality and both halves of the stationary sandwich
remain open for connected undirected weighted graphs.
