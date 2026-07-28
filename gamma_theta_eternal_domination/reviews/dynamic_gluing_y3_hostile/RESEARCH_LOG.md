# Research log: hostile audit of dynamic \(Y_3\) gluing

## 2026-07-28 PDT

- Froze and read the candidate note, checker, manifest, and research log.
- Re-read the accepted C-067, C-070, and C-072 proof sources, their hostile
  reviews, and the arbitrary-state restoration and ridge-response covariance
  inputs.
- Reconstructed the distinction between static dominating-swap lists and
  retained family-response lists.  Checked that family membership implies
  both the omitted-anchor graph edge and domination when the reference state
  is independent.
- Replayed every attack in the analytic static-to-family rigidity proof.
  Verified unoccupied attacks, exactly one moving guard, the required graph
  edge, each restoration rejection, both reflections, and the final missing
  color.
- Audited the defect-ridge argument, including nonemptiness, the
  \(\alpha=3\) clique step, independent-state forcing, singleton response
  lists, and the two transported middle-color incidences.
- Derived all 28 adjacency decisions on the eight-vertex double-defect core.
  Confirmed that exactly four pairs remain free and hence that the 16 local
  completions are exhaustive.
- Proved separately why no external vertex or external family state can
  repair a failed attack in the local greatest-fixed-point deletion.
- Wrote `independent_check.py` from scratch using adjacency dictionaries and
  `frozenset` states.  It imports no candidate or campaign game code.
- Independently reproduced 576 rigidity subpatterns, all 16 double-defect
  kernels, the `FDzro` 21-state family and all 84 obligations, and the
  ten-vertex control's complete four-round triple-family deletion.
- Checked ordinary graph6 byte order against `Ch`, round-tripped all three
  supplied graph6 records, and verified the ten-vertex \(G/H\) complement
  identity.
- Recomputed \(\gamma,\alpha,\gamma^\infty,\theta\) for both controls using
  exhaustive subsets, a clean one-guard kernel, and direct complement
  coloring.
- Reconstructed every collision exclusion used in the \(7+5+2=14\) count.
  Rechecked the exact C-072 five-witness separation at its accepted frozen
  source.

## Verdict and boundary

Verdict: **PASS**.

The accepted result is conditional on one embedded exact static \(Y_3\):
its family lists are dynamically rigid, its two endpoint static defects
cannot share a witness, and under parameter-three equality it requires at
least fourteen vertices.  No arbitrary-order exclusion, complete \(k=3\)
theorem, universal counterexample-order floor, or conjecture resolution is
claimed.
