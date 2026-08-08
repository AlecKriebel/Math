# Fitness-two determinant branch: research log

## 2026-08-08 — exact target audit

- Reconstructed the marked and active chains from the phase-4 exact
  verifier.
- Confirmed that the true collision target is `sum g>=|Y|`.
- Confirmed that the named promotion statement is
  `sum g>=sum T_P^2 1`, whose right side is at least `|Y|` by the proved
  two-step SOS.
- Therefore promotion implies the collision theorem, while no converse is
  proved.  The previous use of “equivalent” was an exact logical overclaim.
- Separated the two active-tree coefficients `F_0` and `F_2`; their exact
  difference is the positive two-step defect times the total tree weight.

## 2026-08-08 — first coefficientwise forest calculation

- Built the nine-state active chain for a symbolic weighted triangle.
- Expanded all nine directed in-tree cofactors independently.
- The raw cleared collision numerator has negative monomial coefficients,
  ruling out naive positive coefficients in the original edge-weight basis.
- Found and verified the exact centered decomposition

  ```text
  F(a,b,c) = sum_cyclic (a-b)^2 q(a,b,c),
  q(x,y,z) = 16 x^2 y^2 + 20xy(x+y)z + 19xyz^2 + 12(x+y)z^3.
  ```

- This proves the true active-tree sign at order three, strictly away from
  the complete kernel.  It is a model for the required all-order grouping,
  not a universal proof.

## 2026-08-08 — subset-root polynomial audit

- Transferred the exact target to the smaller subset determinant
  `m_K Z_P(1)-Z_P'(1)>=0`, using `Z_P'/Z_P=m`.
- Real-rootedness already fails for the complete order-four root polynomial
  `t(t^2+3t+3)`.
- Ultra-log-concavity fails exactly on the unweighted order-four star.
- Ordinary log-concavity fails exactly on the order-five weighted tree with
  edges `02=1000,03=7,14=7,24=7`.
- Direct level-tail domination fails on the frozen order-six rank-tail
  witness even though its mean remains strictly below the complete mean.
- Therefore a root-polynomial proof must address the derivative at one
  globally; stability, log-concavity, and coefficientwise domination do not
  provide the missing sign.

## 2026-08-08 — factorial-moment recurrence and hostile audit

- Exactified the full falling-factorial stationarity recurrence in terms of
  labelled burst-coverage tensors.
- Derived the positive Laplace-product representation
  `c_p(T)=2 integral exp(-s) product_(i in T)(1-exp(-s p_i)) ds`.
- All factorial-moment inequalities survive the exact 54/624/48 graph
  corpus and both frozen order-six witnesses, including the rank-tail
  counterexample.
- The recurrence is triangular but not closed: its base member is already
  the unknown mean inequality and every higher member contains
  state-correlated labelled coverage tensors.
- On `P4`, the state `{0,2,3}` updated at endpoint `0` has every conditional
  factorial moment strictly larger than the corresponding complete update.
  Thus one-step total positivity cannot supply a pointwise comparison; a
  proof would need a new stationary correlation inequality.

## 2026-08-08 — complete-refresh forest interpolation

- Introduced the affine active-kernel interpolation
  `K_alpha=K_0+alpha(K(P)-K_0)` and the exact determinant
  `det[I-K_alpha+(H-c_0 1)nu_0]`.
- Proved `S Delta S=0` for rank averaging `S`; consequently its constant and
  linear coefficients vanish for every loopless row-stochastic kernel.
- For a symbolic weighted triangle, reconstructed the determinant and found
  positive centered Bernstein certificates for every nonzero coefficient.
  This proves the true collision sign along the entire complete-to-actual
  interpolation in order three.
- Exact hostile screens found every nonzero Bernstein coefficient positive on
  reversible and directed rational kernels through order five.  This is
  evidence only; higher-coefficient positivity remains open.

## 2026-08-08 — all-order antisymmetric Hessian sector

- Decomposed the quadratic coefficient into the standard, symmetric
  balanced, and antisymmetric balanced row-kernel sectors.
- Reduced the antisymmetric sector to a one-dimensional complete-rank
  resolvent.  A monotone heat-bath coupling proves the required rank
  potential differences strictly decrease.
- Derived an explicit positive two-tree expression after the second
  perturbation.  It proves strict Hessian positivity on every nonzero
  antisymmetric row-balanced perturbation for every population order.
- Independently checked the recurrence through order 40, against the full
  active chain through order seven, and against a separate stabilizer-orbit
  computation through order twelve.
- The standard and symmetric sectors are exactly positive through order
  twelve but do not yet have all-order sign proofs.
