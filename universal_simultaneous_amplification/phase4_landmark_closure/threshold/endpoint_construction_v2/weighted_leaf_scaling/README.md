# Weighted-leaf scaling audit

This folder classifies the leaf-weight regimes inside the dilute `K_2` plus
hub-leaf construction.

Main result: weighting the common-hub leaves cannot improve their correction
vector, and putting heavy leaves on distinct clique hubs also cannot improve
the hybrid once the far-field ordinary-singleton term is included.  The exact
class threshold remains

\[
1.5028569127905696\ldots .
\]

The tempting local-only distinct-hub calculation is explicitly corrected in
`WEIGHTED_LEAF_CLASSIFICATION.md`.  At `r=3/2,tau=5/2`, the true vector is

\[
(-2216/3535,-45/98),
\]

not the local pair of values obtained by ignoring all ordinary starts.

Run `replay.sh` for the exact algebra, exact labelled lumping, and finite
orbit-chain convergence diagnostic.

