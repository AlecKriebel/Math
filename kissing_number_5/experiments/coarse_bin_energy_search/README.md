# Coarse-bin energy search

This directory preserves a sequence of floating-point LP/conic searches that
combined finite inner-product grids with coarse integer degree facets, harmonic
blocks, and tentative eigenvalue cuts.

The outputs are **numerical evidence only**.  Several early attractive values
were invalid because normalized facet rows were divided by their scales twice;
the later `*_scalefix*` files record the corrected runs.  None of these finite
grids covers arbitrary continuous inner products, and no solver status or
stored JSON file proves infeasibility of a 41-point spherical code.

The code and result files are retained to make the failed mechanism
reproducible and to prevent the scaling bug from being rediscovered.  Resume
only if a boundary-safe continuous reduction or an exact dual certificate is
available.
