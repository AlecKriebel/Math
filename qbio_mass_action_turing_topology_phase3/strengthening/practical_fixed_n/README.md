# Route E - practical fixed-n implementation reconnaissance

**Status:** useful preprocessing, not a strengthening theorem.

The independent implementation enumerates positive circuits of the flux cone in two different ways, projects them to Jacobian-factor generators, tests strict positive-flux feasibility, and exactly decomposes sampled cone points. It therefore implements the load-bearing finite-dimensional reduction.

A complete practical solver for arbitrary `n<=3` would additionally require a reliable exact relative-facet engine and quantifier-elimination backend with certificate export. Those components are not bundled. The software is honestly described as an independent preprocessor and verifier rather than a complete practical CAD solver.
