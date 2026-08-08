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

## 2026-08-08 — transient baseline floor and grouped histories

- Isolated the weaker sufficient conjecture
  `nu_0 K_P^t H >= nu_0 H` for every finite time.  Cesaro convergence would
  prove the true collision target without stationary promotion.
- Recast it exactly as a quenched-versus-annealed comparison under a random
  fixed vertex labelling versus independently refreshed labellings.
- Derived the rank/transverse block expansions at times two and three.
  Individual packets are not positive: the reversible triangle `(1,10,10)`
  has an exact negative `BDC` packet, and `(1,2,2)` has a negative isolated
  two-colour word.  Their fixed-length grouped sums remain positive.
- Proved for every directed triangle that
  `a_2-a_0=(X^2+Y^2+Z^2)/12` and
  `a_3-a_2=((y+z)X^2+(1+x-z)Y^2+(2-x-y)Z^2)/16`.
- Exact boundary screens cover all deterministic row maps at orders three
  and four and all equal two-neighbour row supports at order four through
  time fifty.  Exact complete-ray Bernstein coefficients are nonnegative on
  a seeded reversible/directed corpus through order five and time thirty.
- Derived the exact fixed-count-word recurrence for complete-ray Bernstein
  control vectors.  It makes each coefficient the uniform average of all
  histories with a prescribed number of actual versus complete updates and
  avoids unstable polynomial interpolation.
- The finite evidence does not prove the all-time statement.  The live target
  is a grouped two-replica or tree-homomorphism certificate; termwise
  excursions are closed.
- Proved strict complete-ray convexity at time three for every directed
  triangle using the cubic bound
  `(X+Y)(X-Z)(Y+Z) >= -(X^2+Y^2+Z^2)/2`.
- Exactified two stronger-route failures.  Raw product-simplex Bernstein
  control coefficients are negative at order four and time three.  A
  reversible order-five kernel has negative complete-ray curvature at time
  eighteen, even though all its complete-ray Bernstein coefficients remain
  nonnegative.  Thus convexity is closed but the more flexible ray-history
  grouping survives.
- Exactified a third stronger-route failure.  The deterministic directed
  order-five map `(1,0,0,4,3)` has every time-28 complete-ray control
  positive, but `b_(28,28)<b_(28,27)`.  Positivity cannot be reduced to
  monotonicity in the number of actual-coloured updates.

## 2026-08-08 — fixed-count two-replica sectors

- Derived the exact triangular identity
  `binom(t,2)b_(t,2)=sum_(ell+m<=t-2) nu Delta K0^ell Delta R^m H`.
- Proved every antisymmetric packet positive for every order and both lags:
  the radial difference cone and the antisymmetric feature cone are both
  positive and decreasing, making the second perturbation a sum of four
  nonnegative sampling terms.
- Derived exact two-feature rank recurrences and one weighted output
  functional for each of the standard and symmetric balanced sectors.
- Proved the entire directed three-vertex two-colour coefficient positive
  at every time.  The exceptional standard cumulative generating function
  has a three-term residual recurrence contracting in an exact weighted
  maximum norm.
- Proved every four-vertex standard fixed-total-lag diagonal positive at
  every time by isolating its dominant `(2/3)^m` term and certifying an
  exact 21-step companion contraction.
- Exactified the failure of packetwise positivity: a symmetric balanced
  four-vertex direction has `Q_(1,0)=-1/36`.
- A first proposed local cone was rejected after a hostile boundary audit:
  it had silently set the physical standard `k=N` mode to zero.  The
  corrected upper-boundary mode is retained in the canonical recurrence.
- Exact finite screens find every unresolved standard and symmetric
  diagonal nonnegative for `4<=n<=31` and total lag at most 100.  Their
  universal signs remain open.

## 2026-08-08 — common-pin variation and exact convexity failure

- Represented the complete replacement kernel as the uniform mixture of
  vertex-pin kernels and identified the canonical standard direction with
  one distinguished pin minus that mixture, including the exact scale
  `(N-1)/N`.
- Recast the standard two-replica coefficient as the covariance of terminal
  inverse cache rank with the centered collision count of an iid pin
  history.
- Lumped the distinguished-pin line to the exact `3N-1` categories
  `X_k,I_k,O_k`; an independent implementation matches every labelled row
  through order five.
- Exactified the first failure of coefficientwise convexity:
  `(n,t,c)=(5,21,19)` has negative second difference, although the required
  binomially weighted curvature remains strictly positive.
- Isolated three surviving sufficient statements: first-difference
  one-crossing, curvature one-crossing plus positive terminal slope, and
  coefficientwise positivity after factoring the symmetry root from
  `Phi_t'`.  All survive exact rational checks for `3<=n<=8,t<=50`.
- Found a simple generalized spectrum for the quotient pencil in exact
  symbolic orders `2<=N<=7`, with nontrivial eigenvectors given by complement
  binomial coefficients.  An all-order oscillatory-pencil theorem remains
  open because the two pin operators do not commute.
