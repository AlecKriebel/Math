# Sealed mathematical verdict before code and reported claims

Timestamp and exact hashes are in `MATHEMATICAL_SEAL.json`. Candidate code, check-output JSON, statuses, final documents, history, old reviews, and sibling/root findings remained unread at this seal.

**Verdict:** the inspected mathematics supports scoped partial results and scoped obstructions. I found no geometric/hypothesis defect in TURN_1 through TURN_5 that invalidates their stated scoped conclusions. It does **not** resolve original Problem 2.55, and the double-exponential test still lacks an unrestricted bounded-ambient-entire Liouville proof.

| Turn | Reconstructed result | Exact prerequisite and boundary check | Geometric verdict |
|---|---|---|---|
| 1 | Polynomial precomposition equivalence; three Laurent-exponential polynomial-phase inputs | Multiplicities handled by finite characteristic coefficients; normal connected regular loci; algebraic quotient is ultra-Liouville; regular abelian cover | Valid scoped partial |
| 2 | Two such inputs and arbitrary third input | Generic product monodromy; finite winding-lattice index away from extra constant level; local topological component labels; holomorphic finite symmetric coefficients; density at exceptional fibers | Valid scoped partial, subsumed by turn 3 |
| 3 | One such input and two arbitrary nonconstant entire inputs | Actual fixed-degree finite covering off a proper analytic subset, density, finite attained psh maximum; ultra-Liouville quotient; connected cyclic cover | Valid scoped partial |
| 4 | One input with finite excluded singular-value set and virtually nilpotent inverse monodromy | Normal closure, regular pullback subgroup, finite-index nilpotent core, ultra-Liouville intermediate cover; `Z wr Z` obstruction for `exp(exp z)` | Valid conditional family and valid route obstruction |
| 5 | Character and finite-dimensional deck-orbit rigidity on triple double-exponential surface | Smooth quotient, SNC coordinate divisors, strict subunit removal exponents, entire common-translation lines, finite-dimensional isometries | Valid scoped obstruction; infinite-dimensional orbit remains untreated |

No metric, cotangent positivity, jet differential, projective compactification, or hyperbolicity conclusion is actually asserted by these proofs. The general graph and quadratic-cone controls rule out importing such conclusions without new hypotheses. Singular points are isolated and are recovered by density, not by an assumed smooth global metric. Divisor crossings and exceptional levels are explicitly accounted for.

Primary prior coverage was checked independently. Demailly establishes the two-simple-exponential case; Lin-Zaidenberg establishes the covering mechanism with the required ultra-Liouville hypothesis. The quoted irreducibility theorem is credited as an established dependency, with Demailly's published primary statement corroborated and the original Annals proof not fetched. No novelty/historical-priority conclusion is made by this audit.

Audit completion estimate at mathematical checkpoint: 60%. Best-guess completion toward a full original-problem discovery: 30%, a qualitative estimate reflecting verified broad classes but no mechanism for three arbitrary inputs; not a proof that 30% of the quantifier space is covered. This number may fall as new obstructions are found. Mathematical reconstruction and exact remaining gap are in `GEOMETRIC_PROOF_RECONSTRUCTION.md`.
