# Research log

Date: 2026-10-04 UTC. Exact full target: continuity on (1,infinity), and D(lambda) > D(nu) for every 1 < lambda < nu. Approximate percentages below are subjective progress toward a proof of this full target, not confidence levels or probabilities.

## Source/readiness checkpoint — 13:10 UTC

Read the supplied record and official Oberwolfach report, section 8, printed p. 390. The public catalogue fetch failed, but the official text confirmed the Hilbert space, generators, target, and both questions. The matched prior-report entry was absent from the supplied report corpus. Repository checks found the row queued at 0/5, no existing attempt directory for this ID, and no matching PR or branch; a Nyman keyword PR check also returned none. No target equivalence was inferred from nearby related records.

The Jousse 2005 paper initially looked like a resolution. Inspection established that it concerns fixed finite tuples and an integer number-of-terms parameter. It is not the same target. Full-target progress estimate: 5%.

## Approach 1 — Strong dilation continuity and Hilbert-space limits

Checkpoint: 13:11 UTC. Mechanism: dominated convergence for e_a and monotone projection limits. Outcome: rigorous left-continuity and the exact formula (1) for a possible downward right jump. Right-continuity requires the extra projection onto E_(lambda+) intersect E_lambda-perp to vanish. Norm-continuity of individual generators does not establish that assertion. Status: partial; full-target progress estimate 15%.

## Approach 2 — Local Möbius inversion and dual separation

Checkpoint: 13:15 UTC. Mechanism: recover the cumulative coefficient function by the finite sum (2). Outcome: every E_lambda vector has an eventually constant recovered function, while the target's recovered function has a jump at every prime. This proves finite-cutoff positivity and strict increase of the approximation spaces. Explicit dual witnesses give exact rational lower bounds and separate individual new generators.

The local necessary-condition space N_lambda is right-continuous, but equality E_lambda = N_lambda has not been proved. Approximating coefficient functions in local norms does not automatically approximate the original functions in the global weighted Hilbert norm. Status: partial; full-target progress estimate 20%.

## Approach 3 — Residual correlations and dilation variations

Checkpoint: 13:17 UTC. Mechanism: exact projection-gain identity and unitary shifts of the whole parameter interval. Outcome: (8)–(10) characterize a plateau precisely; (11) computes the gain for translated intervals. The variation would force improvement under 2B > Q, but no such inequality is established. When D(lambda) < sqrt(2)-1, its initial derivative is negative, showing that the proposed elementary variation cannot be a general proof. Strict subspace growth by itself is disproved as a sufficient argument by an elementary orthogonal-coordinate control. Status: blocked at a precise missing residual correlation; full-target progress estimate 15%.

## Approach 4 — Fixed-n compact optimization and limit exchange

Checkpoint: 13:18 UTC. Mechanism: apply Jousse's finite-tuple theorem through reciprocal coordinates, optimize over a compact cube, and inspect the limit over n. Outcome: each d_n(lambda) is continuous, but their decreasing infimum can jump. An explicit continuous scalar family demonstrates the invalid limit exchange. A hypothetical right jump must require both unbounded term count and unbounded coefficient total variation. A normalized difference of nearby generators shows that bounded Hilbert norms do not supply the latter bound. Status: partial reductions; full-target progress estimate 20%.

## Approach 5 — Mellin weighted exponential spans and exact controls

Checkpoint: 13:20 UTC. Mechanism: Mellin–Plancherel changes the problem to a weighted finite-frequency-interval approximation problem. Outcome: exact formulation (13), but no weighted endpoint-synthesis theorem or nonvanishing residual-correlation theorem was obtained. The zeta weight cannot be dropped. Direct single-generator integration establishes strict improvement from the endpoint 1, which is explicitly weaker than the requested strict decrease between arbitrary cutoffs.

`verify_controls.py` passed using exact rational arithmetic: five prime-centered witnesses, 701 rational generator annihilation checks in total, a noninteger-generator separation control with zero target pairing, and the finite-dimensional plateau and continuous-infimum negative controls. No sampling claim is used in place of the continuum proof. Status: unsolved after five approaches; full-target progress estimate 20%.

## Stopping conclusion — 13:21 UTC

Freeze the partial proof and exact controls. The missing steps are right-limit defect elimination and strict projection gain on every newly added parameter interval. No full resolution, counterexample, or verified prior resolution was obtained, so the only supported target status is `unsolved`.
