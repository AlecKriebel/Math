# Critical WARM on the infinite line: five-turn partial result

**Original full temporal convergence remains unsolved after 5/5 substantive author turns. Independent partial review pending.** No novelty or priority claim.

The model studied is alpha=1 WARM on the nearest-neighbor line, with independent rate-one vertex clocks and every initial edge tally equal to one. When a clock rings it reinforces one incident edge proportionally to its current tally. The target observable is the scaled **edge** count N_i(t)/t. This is not a reinforced walk or the trace-ant process. The OWR source leaves the initial-count convention unstated; this packet explicitly uses the standard unit initialization and does not exploit zero or engineered initial weights.

## Candidate partial theorems

1. Exact harmonic count martingales converge in L2 and almost surely. Every count diverges, and its logarithmic growth exponent is one.
2. Any actual full pointwise limit is necessarily an alternating profile, including possible zero endpoints. Under the unit-initialized iid-clock construction, existence of the full limit would force that profile to be identically one.
3. A finite local entropy-dissipation integral gives almost-sure asymptotic stationarity. A second exact harmonic-entropy identity proves that every adjacent normalized pair sum converges to two almost surely.
4. All fixed sites therefore track one time-dependent alternating phase. Its liminf and limsup are deterministic and complementary around one. Exact cooperative diffusion and conservative logarithmic-flux formulas isolate the missing temporal convergence condition.
5. There is a **deterministic sequence of times** increasing to infinity along which every fixed normalized edge weight converges to one, simultaneously almost surely. Growing-block martingale and boundary-flux estimates are summable along explicitly selected low-dissipation times; this is not an uncontrolled exchange of spatial and temporal limits.

The last theorem does not control the gaps between selected times. The packet does not prove convergence of the boundary-flux integral, a positive pathwise lower linear rate, uniform spatial ellipticity, or convergence of the full time-dependent phase. Ergodicity is used for actual limits or pathwise envelopes, never assigned to weak subsequential laws.

## Reading and reproduction

The five substantive turn files contain the complete arguments in order. `checks/verify_exact.py` is a standard-library exact finite checker, with saved output `checks/EXACT_CHECKS.json`. Its 77,754 rational algebra and count-bookkeeping assertions support the written proofs; they do not certify infinite-volume stochastic claims. No WARM simulation is offered as a proof.

`SOURCE_SCOPE.md` and `source_manifest.json` identify the exact original source, initial-condition limitation and existing subcritical results. The local source cache contains complete primary PDFs and the pinned imported record. Those reading copies and full imported records are intentionally excluded from publication. `FROZEN_MANIFEST.json` fixes the author proof package for an uninvolved reviewer.
