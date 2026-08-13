# Research log: cross-rule orbital midpoint

## 2026-08-13 -- exact refutation and odd-sector obstruction

- Tested the proposed fitness-two conductance-transposition inequality for
  `log(rho_Bd rho_dB)` first on the two previously frozen nonregular dB
  midpoint witnesses.  Their cross-rule products improve, so neither is a
  counterexample.
- A targeted order-three rational audit found a counterexample immediately.
  Shrinking it gave the path `(w01,w02,w12)=(0,3,1)` under `(0 2)`, with
  exact midpoint-minus-endpoint product gap
  `-94973014/82395955215`.
- Found a strictly positive triangle witness `(1,10,2)`, so the failure is
  not a boundary effect.
- Derived the exact even--odd block equations and Schur complement for each
  rule, followed by one exact cross-rule product identity.
- On the minimal path, the combined source and even-rate terms are positive;
  the transposition-odd Green feedback is negative and dominates them.
- Derived the full one-parameter path orbit.  The log product has negative
  second derivative at the midpoint, so the desired inequality holds
  locally and reverses only at finite amplitude.
- **CLOSED:** permutation-orbit midpoint symmetrization of the cross-rule
  product cannot prove PAPT.  The original PAPT inequality remains open.
- Best-guess completion: **100% for deciding this orbital-midpoint claim**;
  **0% additional progress toward proving PAPT**, because the result is a
  route refutation rather than a substitute global inequality.
