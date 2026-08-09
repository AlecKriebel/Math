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

## 2026-08-08 — global factor-two conjecture exactly refuted

- **FALSIFIED:** the proposed global inequality
  `1/2-sigma >= 2(beta-1/2)`, even for a positive three-type kernel induced
  by a symmetric rational weight matrix.
- The exact family has masses
  `p=(1-gamma-epsilon,epsilon,gamma)` and symmetric weights
  `W_AA=epsilon`, `W_AB=(1-theta)/epsilon`, `W_AC=theta/gamma`,
  `W_BB=W_BC=1`, `W_CC=1/epsilon`.  As `epsilon -> 0`, its response at
  general fitness is

  ```text
  Bd gain = (1-gamma)(1-theta)/r,
  dB cost = (1-gamma)(r-1)/r.
  ```

- At `r=2`, every `theta<1/2` violates factor two.  The rational choice
  `(gamma,theta,epsilon)=(1/14,1/50,1/1000)` is enclosed by exact monotone
  rational boxes and satisfies
  `L-2G <= -182920163290948548677/700000000000000000000 < 0`.
- Scaling `gamma=1-c`, `theta->0`, and then taking `epsilon` sufficiently
  smaller produces the compact-uniform normalized branching ray
  `(1/r,-(r-1)/r)`.  This is the sharpest catalyst-like ray found, but its
  endpoint cost/gain tends to one, not zero.
- The active global boundary is now the sharper conjecture
  `beta+sigma<=1`, equivalently endpoint cost at least Bd gain.  All broad
  hostile optimizations approach equality from the allowed side; no proof
  or exact counterexample is yet known.
