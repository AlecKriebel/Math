# 30001321 current status after author turn 2/5

Unreviewed partial research; the original conjecture is unresolved. The initial
continuity.json and RESEARCH_LOG.md are frozen turn-1 historical snapshots.
BUDGET_TURN2.json is the current count. No source lookup is counted as a turn.

Turn 1: ordinary environmental L1 convergence for every diverging interval scale.
Turn 2: all-order conditional replica-occupation moments and a scalar concentration
argument prove the source-strength superpolynomial tail for all fixed polynomial
scales M >= N^gamma with gamma > 1/4. See TURN_2.md for all hypotheses and proof.
This does not settle the original every-diverging-scale statement.

Verification: python check_turn2.py, using Python's standard library only.
The exact finite controls check the conditional identities and deterministic
algebra, not the limiting theorem. The full analytic argument needs separate
review before any promotion. No PR or queue-status change is requested here.
