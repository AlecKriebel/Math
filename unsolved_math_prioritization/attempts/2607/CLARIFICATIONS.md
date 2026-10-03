# Post-audit clarifications

Date: 2026-10-03 UTC. These are wording clarifications only; the five frozen attempt files remain unchanged and no additional proof-search turn is recorded.

1. In Attempt 3, s means the number of distinct lines Qx for **nonzero actual word values** x in H tensor Q. The identity value does not introduce additional directions.
2. In Attempt 4, the derived-word convention is delta_0(x)=x and delta_(j+1)=[delta_j,delta_j], with disjoint formal variable sets. Thus c_0=h is a delta_0-value in the induction.

The independent mathematical audit found no blocking errors in the partial claims. Its verdict is PASS as an unresolved five-attempt package, not a solution or a novelty certificate. The remaining target is rank at most one for the free abelian verbal subgroup in the general soluble reduction.

## Reproducing both implementations

- Original controls: Python 3 standard library; run `python3 verify_controls.py`.
- Independent audit controls: Python 3 with SymPy 1.14.0 (the version tested); run `python3 independent_controls.py`. No candidate code is imported. The script uses paths relative to its own location and recreates `independent_control_results.json`.

The 2,210 matrix-power checks and 23,409 Heisenberg pairs are finite exact controls. Universal conclusions rely on the written proofs and their audit.
