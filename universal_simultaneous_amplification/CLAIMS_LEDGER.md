# Claims ledger

Every substantive mathematical statement is assigned one of the required
statuses. The ledger is updated before each publication checkpoint.

The authoritative current asymptotic-threshold ledger is
`phase4_landmark_closure/CLAIMS_LEDGER.md`.  The table below retains the
fixed-graph program and has been updated only where the phase-4 theorem
superseded its former open status.

| Claim | Status | Basis | Inherited or new |
|---|---|---|---|
| Complete-graph Bd and dB baseline formulas | PROVED | Direct birth--death recurrence in `paper/main.tex` | Inherited |
| Incomplete-support undirected dB strong limit | PROVED | Limiting-chain argument and exact support-gap identity | Inherited |
| Complete-support undirected first `1/r` correction | PROVED | Differentiated first-step equations and exact SOS identity | Inherited, proof hardened |
| `q'_S(0)=0` for complete support and `|S|>=3` | PROVED | Analytic finite chain plus triangular derivative system | New proof hardening |
| No fixed finite undirected weighted graph amplifies dB for every `r>1` | PROVED | Exhaustive support dichotomy | Inherited |
| No family satisfies `exists N0 forall N>=N0 forall r>1` strict dB amplification | PROVED | Apply the fixed-graph theorem to each member | Clarified |
| A family satisfies `forall r in (1,R_hyb) exists N0(r) forall N>=N0(r)` simultaneous amplification | PROVED | Explicit dilute pair--leaf family; exact trace, post-establishment, diagonal, and sextic certificate | New phase-4 theorem |
| A family satisfies `forall r>1 exists N0(r) forall N>=N0(r)` simultaneous amplification | OPEN | The construction proves only `r<R_hyb`; no finite universal upper bound is known | Explicit limitation |
| Directed complete-support obstruction with columnwise SOS | PROVED | Differentiated first-step proof, exact column SOS, independent `QQ(r)` verifier | New theorem |
| Equality in the directed complete-support coefficient | PROVED | Exactly the column-uniform class; target-column scaling gives the baseline chain for all fitness | New theorem |
| Non-strong directed supports are eventually dB-suppressing | PROVED | Source-component reachability and first-gain bound | New theorem |
| Strongly connected noncomplete directed supports are eventually dB-suppressing | PROVED (PRIOR) | Tkadlec et al. Theorem 1; hypotheses audited after the new proof | Prior result |
| No fixed finite loopless directed weighting with positive incoming degrees amplifies dB for every `r>1` | PROVED | Exhaustive support/strong-connectivity trichotomy | New synthesis |
| Complete-support weighted-triangle suppression for every `r>1` | PROVED | Exact six-state rational formula, homogeneous SOS, independent no-import hostile replay | New theorem |
| `1+3` symmetric weighted `K_4` suppression for every `r>1` | PROVED | Exact six-orbit rational formula with coefficientwise-positive certificate and symbolic full-chain audit | New theorem |
| `2+2` symmetric weighted `K_4` suppression for every `r>1` | PROVED | Exact seven-orbit formula, positive determinant, `(g,d,t)` coefficient certificate, and symbolic full-chain audit | New theorem |
| Unrestricted six-edge weighted `K_4` suppression for every `r>1` | OPEN | 5,000 exact rational samples found no counterexample, but sampling is not a universal proof | New track |
| General complete-support beneficial-fitness suppression | OPEN | Strong-selection coefficient and low-dimensional certificates alone are insufficient | New track |
| Eventual dB amplification at every fixed fitness forces support degree to diverge in probability | PROVED | dB fitness monotonicity plus the exact strong-selection support bound | New theorem |
| Fixed-class positive-proportion dense equitable blow-ups with fixed irreducible kernel and unequal limiting degrees are asymptotically dB-suppressing | PROVED | Exact stopped-generator convergence, multitype branching process, stationarity, and strict Jensen inequality | New theorem |
| A fitness-independent family eventually amplifying Bd and dB at every fixed `r>1` exists or is universally impossible | OPEN | Diffuse asymptotically regular, mesoscopic, vanishing-class, and reducible-kernel regimes remain | New track |
| The optimal asymptotic simultaneous-amplification interval is known beyond the prior lower bound `(1,1.2)` | PROVED LOWER BOUND | `R_sim>=R_hyb=1.5028569127905696...>3/2`; the endpoint disjunction is exactly refuted | New phase-4 theorem |
| The exact value of `R_sim` is known | OPEN | No matching universal upper bound; the fitness-two collision target has an exact determinant form, while a stronger promotion sign is a sufficient route | New track |

Computational labels in detailed phase reports distinguish exact symbolic
outputs from numerical discovery observations. No numerical observation is
promoted to a theorem here.
