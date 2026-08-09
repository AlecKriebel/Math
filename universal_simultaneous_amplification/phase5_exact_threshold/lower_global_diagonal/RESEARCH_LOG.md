# Global lower-diagonal research log

## 2026-08-08 — arbitrary adjoint-kernel stability target

- Began from the surviving catalyst criterion: a positive Bd response with
  little-oh dB cost at fitness two.  No separated-pair, rank-one, regular
  tangent, fixed-cell, or bounded gadget screen is being repeated.
- Isolated a genuinely global candidate obstruction for the exact diffuse
  adjoint branching normal form.  If `P` is any row-stochastic latent-type
  kernel, `p` is the uniform-start type law, `P*` is its `p`-adjoint, and
  `b,s` are the positive endpoint survival solutions, write

  ```text
  beta = E_p b,   sigma = E_p s.
  ```

  The candidate sharp inequality is

  ```text
  1/2 - sigma >= 2 (beta - 1/2).
  ```

  Unlike the proved regular quadratic tangent inequality, this statement is
  global and would include singular, nonregular, boundary, and growing-rank
  diagonals after the usual stopped-chain passage.
- Broad hostile floating tests have not refuted the inequality.  Nonregular
  deterministic period-two kernels attain equality exactly in the
  two-type calculation, so the factor two cannot be improved.  These are
  discovery facts only.  The active task is an edge-measure/SOS proof or an
  exact counterexample; no theorem is claimed yet.

## 2026-08-08 — singular period-two boundary closed exactly

- **PROVED COMPLETE NORMAL FORM:** for an arbitrary finite involution of
  latent types, arbitrary positive type law, arbitrary growing rank, and
  arbitrary mass imbalance, the deterministic period-two adjoint branching
  trace satisfies exactly

  ```text
  1/2 - sigma = 2 (beta - 1/2) >= 0.
  ```

- Each two-cycle solves in closed form.  If its mass ratio is `a`, then
  `b_i=3/[2(a+2)]`, `b_j=3a/[2(2a+1)]`, and the dB vector reverses the two Bd
  coordinates.  The orbit Bd gain is
  `(a-1)^2/[2(a+2)(2a+1)]`, while the dB cost is exactly twice that value.
- A stopped-chain passage retains uniform initialization and every
  post-establishment path.  Consequently trace-resolved connected clone
  completions whose off-boundary error is little-oh of the response cannot
  be catalyst rays.
- This is the global finite-amplitude version of the earlier local
  period-two tangent equality.  It closes arbitrary singular mass ratios
  and growing unions of two-cycles, but not same-scale non-period-two
  completion or order-one within-colony collisions.  The conjectural global
  inequality for every stochastic kernel remains open.
