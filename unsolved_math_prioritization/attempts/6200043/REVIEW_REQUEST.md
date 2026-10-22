# Independent review request

Please independently audit all five written proof attempts, source normalization, classical credit and exact scopes, plus the three small standard-library checkers. Challenge the critical assumptions rather than treating finite tests as proofs.

Highest-risk points:

- Use of Carrasco–Mackay Proposition 8.3 with a possibly nonregular self-image; its regularization theorem is the reason this is allowed. Distinguish ordinary from Ahlfors regular conformal dimension.
- Turn 2 finite coset envelope: convergence/subsequence passage, QS invariance of porosity, finite-union Assouad dimension, and the uniformly-perfect regularization step. Check that 'quasiconvex subset' is not promoted to 'subgroup'.
- Turn 3 mandatory additive correction, disjoint layers, inverse-Lipschitz Hausdorff measure estimate, Borel measurability, packing constants, and the attractor proof. No uniform bounds for arbitrary source iterates are claimed.
- Turn 4 p-modulus formula and the precise target regularity requirement. Cube example is not a source counterexample.
- Turn 5 metric cell-hole condition, scale choice and N bound; no implication from missing codewords to missing metric points without the explicitly required geometric certificate. A proper regular language need not have every-state escape.

All historical public files should be preserved. If a mandatory mathematical repair is needed, request an additive correction and re-review it. Original disposition is unsolved, five recovery turns, with historical turns unknown; do not initiate a sixth author search or create a PR. Return a written scoped verdict, exact artifact list/hashes, any source access limits, and independent controls if useful.
