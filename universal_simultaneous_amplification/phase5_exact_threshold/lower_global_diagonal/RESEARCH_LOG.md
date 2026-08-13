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

## 2026-08-08 — exact first Bd-to-dB orbit step

- **PROVED:** for every finite row-stochastic `P`, every positive start law
  `p`, and every endpoint Bd extinction vector `q`, the first iterate of the
  endpoint dB survival map satisfies

  ```text
  E_p F(q) <= E_p q,       F(y)=2Ry/(1+2Ry).
  ```

  No reversibility or bounded-temperature hypothesis is used.
- The proof writes the gap as `E_p phi(Rq)` for the convex function
  `phi(z)=z(2z-1)/(1+2z)`, takes labelled tangent lines at `q_i`, and adds an
  exact Bd-flow null Lagrangian with

  ```text
  lambda(x)=-(2x-3)(12x^2-12x+11)/(16(2x+1)).
  ```

  The resulting two-label edge slack is nonnegative on the unit square.
  Its numerator is certified by exact Bernstein coefficients on 26 outer
  rational boxes and exact Hessian convexity on `[7/16,9/16]^2`.
- This closes only the first orbit step.  Pointwise and temporal monotonicity
  fail, so no endpoint claim is inferred.  The stronger active target

  ```text
  W = E[b(1-b)] - E[b^2 s/(1-s)] >= 0
    = E(q-s) - E[(q-s)^2/(1-s)]
  ```

  would prove `beta+sigma<=1` with a quantitative square deficit and remains
  open.

## 2026-08-08 — temporal and parity orbit monotonicity refuted exactly

- **FALSIFIED:** the Bd-started dB survival orbit is not monotone in
  `p`-average after its first step, and neither parity subsequence is
  monotone.  A positive rational symmetric-W three-type kernel has

  ```text
  E_p(y_10-y_9)  > 1.437e-7,
  E_p(y_15-y_13) > 4e-8.
  ```

- The Bd extinction vector is enclosed in an exact rational invariant box
  of radii `10^-60(2,16,3)`.  Fifteen dB iterates are propagated with exact
  outward rounding on a `10^-45` grid, so both strict signs are rigorous and
  independent of floating conditioning.
- Consequently the exact first-step theorem cannot be iterated directly,
  even after grouping updates in pairs.  This is a proof-route
  counterexample only; `beta+sigma<=1` and the special ground-state energy
  `K` remain open.

## 2026-08-13 — exact coupled three-ground Picone reduction

- Recast the two endpoint systems as four positive ground states
  `1,a,b,v=as` of the same self-adjoint kernel, with potentials
  `1`, `V_a=t`, `V_b=t/(2q)`, and `V_v=1/(2h)`.  The constant ground adds
  three ratio orders omitted from the pre-crash three-ground route.
- **PROVED:** for any two positive grounds `f,g`, the signed potential
  difference has the exact lower-ratio-cut formula

  ```text
  sum_{g_i/f_i <= z} pi_i f_i g_i (V_g-V_f)_i
    = sum_{g_i/f_i <= z < g_j/f_j}
        pi_i P_ij f_i f_j (g_j/f_j-g_i/f_i) >= 0.
  ```

  This is the cut form of the discrete Picone identity.
- **PROVED:** factor one follows if increasing label potentials on the six
  ground-pair ratio sets pointwise dominate `d=a(q-s)` by the corresponding
  signed potential differences.  The three-pair version on `b/a`, `s`, and
  `as/b` is an immediate subcertificate.
- **PROVED EXACT THEOREM OF ALTERNATIVES:** such coupled potentials fail to
  exist if and only if a nonnegative node measure has nonnegative lower
  prefixes and zero total for all six signed ratio orders, but has
  negative `d`-average.  This turns the remaining proof into a finite
  ordered four-ground lemma and specifies an exact counterexample to the
  route, rather than another floating kernel search.
- The factor-one inequality itself remains open.  If the ordered lemma is
  proved, diffuse adjoint branching cannot produce positive Bd gain with
  little-oh dB cost at fitness two, forcing any sharp lower construction to
  preserve a genuinely non-diffuse interaction.
