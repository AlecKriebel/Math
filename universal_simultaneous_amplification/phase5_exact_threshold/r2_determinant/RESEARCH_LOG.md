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
  binomial coefficients.  A subsequent block elimination proves the exact
  determinant factorization and semisimple generalized spectrum for every
  `N>=2`.  The right eigenvectors form a Pascal system, but the transfer
  matrix in that basis still has mixed signs, so the variation theorem
  remains open.
- Recast the positive-quotient target as a consequence of discrete
  Schur-convexity of the fully word-symmetrized multinomial pin reward.  A
  two-label swap pairs every lower-binomial-tail term with the correct sign.
  Exact rational computation verifies 95,495 add-one comparisons through
  `(n,t)=(3,35),(4,14),(5,9)`; the all-order reflection theorem is open.

## 2026-08-08 — exact cubic and quartic optional-potential refutations

- Independently derived the monomial drift columns and the Farkas dual of
  the degree-bounded optional-potential LP.
- On the complete-support two-class graph of order seven with class sizes
  `(2,5)` and weights `w_AA=10000,w_BB=100,w_AB=1`, extracted a seven-state
  positive integer Farkas ray with exact negative objective
  `-16671847733465987326305780396702792`.  This exactly refutes the cubic
  lemma.
- Verified the entire 126-state labelled drift system against the
  `S_2 x S_5` quotient, so the obstruction is not a faulty lump.
- Exactified a strict quartic potential on that same graph and checked its
  expected drift directly on every labelled transient state.
- Enlarging the classes to `(2,8)` gives an order-ten graph with a ten-state
  exact Farkas ray against every degree-at-most-four potential; its objective
  is
  `-591738467543996669461667803880418671550252755178182911237183584`.
- Numerical two-class sweeps suggest the required degree continues to grow,
  but no unbounded-degree theorem is claimed.

## 2026-08-08 — rank-dependent additive Farkas refutation

- Derived the exact drift system for
  `G(S)=1+|S|/n+sum_(v in S)a_(|S|,v)` and its marked Farkas dual.
- Found and exactified a complete-support three-class graph of order 17,
  with class sizes `(2,5,10)` and integer class weights
  `((20000000,15,5),(15,9,4500),(5,4500,150))`.
- The 48-state dual support has a one-dimensional rational nullspace.  In
  normalization `z=-1`, all 48 state weights are strictly positive and the
  exact objective is `-0.34734270358231461111...`.
- The summed rank balances telescope to
  `[2(n-1)R_1-(2^(n-1)(n+1)-2n)A_(n-1)]/n`.  The witness exceeds the endpoint
  ratio threshold, showing precisely why a one-marked-vertex correction is
  insufficient.  A viable forest dual must retain a second marked
  vertex/collision statistic rather than merely raising a fixed polynomial
  degree.
- Independently solved the 196-state quotient fixation chain exactly over
  `QQ`.  The normalized dB fixation ratio is
  `0.87345507490368193387...<1`, so the graph supports the universal r=2
  inequality and refutes only the potential ansatz.

## 2026-08-08 — marked-cache refutation and stationary standard closure

- Exactified the first failure of the all-order marked-cache/PGF Schur
  strengthening.  At `n=8`, word length 26, the shuffled pin counts
  `(14,12)` versus `(13,13)` give a strictly negative `q=1` avoidance
  coefficient, while the true inverse-rank difference remains strictly
  positive.
- Integrated the Hausdorff atoms before attempting a renewal proof.  The
  resulting true inverse-rank reward admits the exact bad-channel debt
  `W_1=N^2`, `W_k=2N/[k(k-1)]`; its transformed reward is entrywise
  nonnegative, but a memoryless signed occupation still fails in small
  orders.
- Schur-eliminated complete bad excursions.  The exact stationary standard
  scalar is `s(I+A)^(-1)f_0`, where
  `A=(I-S)^(-1)C(I-Q)^(-1)D` is nonnegative.
- Proved an all-order phase contraction with the explicit radial majorant
  `V_1=N`, `V_k=4N/k^2+2/N`: `f_0<=v`,
  `f_0(R_k)>=V_k/3`, and
  `Av<=[12/(5(N+1))]v`.
- Summing the absolute re-entry tail proves strict positivity for every
  `N>=9`; seven exact Schur complements close `2<=N<=8`.  This proves the
  stationary standard irreducible Hessian sector in every population order.
  The stationary symmetric sector was still open at this checkpoint.

## 2026-08-08 — stationary symmetric closure

- Transposed the exact symmetric two-feature recurrence to the signed phase
  form `H=((S,C),(-D,Q))` and Schur-eliminated the bad channel.  The exact
  scalar is `ell(I+A)^(-1)f_0-s^bW`, with
  `A=(I-S)^(-1)C(I-Q)^(-1)D>=0`.
- Proved the radial identity
  `2/k-d_k=2^(2-N) sum_(r>=k)binom(N-1,r)/[(N-1)binom(N-2,k-1)]`
  and the uniform bounds `2(N-2)/(Nk)<=d_k<=2/k`.
- Found the sharp enough binomial debt majorant
  `Wbar=(7N/25)q`.  Its all-order sign reduces to a cubic with negative
  discriminant for `N>=25`; the isolated order `N=24` has exact minimum 24.
  This leaves the uniform first-phase reserve `f_0>=(11/25)v`.
- Proved the complete bad-phase contraction
  `Av<=c_Nv`, `c_N=(2N-5)/[2N(N-2)]`, using the explicit majorant
  `h_k=k omega_(k-1)/(N-2)` and an exact radial-ratio induction.
- Controlled the left occupation by
  `Y_k=2(k+1)/[3k(k-1)]`; the residual `(I-Q^T)Y-1/[k(k-1)]`
  is entrywise strictly positive.
- Reduced the remaining debt to one scalar rank recurrence.  Exact rational
  margins close `40<=N<=287`; for `N>=288`, a pure-birth lower barrier and a
  second negative-discriminant cubic give the uniform split
  `debt<=19/20` and `re-entry tail<=1/20`.  Direct exact solves close
  `3<=N<=39`.
- Therefore the stationary symmetric row-zero inverse-rank sector is
  strictly positive in every population order.  Together with the prior
  standard and antisymmetric theorems, every stationary nonradial Hessian
  sector is now closed.  Finite-time standard/symmetric signs, all forest
  orders at least three, and the global `F0` determinant sign remain open.

## 2026-08-08 — fixed-colour row mixtures and unicycle cancellation

- Derived the exact Bernstein root-vector recurrence
  `(d+1-j)t_j(I-K_0)+j t_(j-1)(I-K)=0` and its scalar colour-current form
  `t_(j-1) Delta h=n_(j-1)+(d+1-j)n_j/j`.
- Rewrote each degree-elevated control as the uniform sum of row-mixed
  determinants.  Each determinant equals a leave-one-root tree-weighted
  response `sum_x tau_x Delta h(x)`.
- Rewrote the same fixed-colour control as a sum of spanning functional-
  unicycle circulations, with an exact elementary-symmetric formula for
  every fixed skeleton.
- Exact hostile audit on the reversible triangle with weights `(1,10,3)`:
  the row set `{(2,0)}` gives determinant `-891/524288`, and a level-two
  spanning-unicycle packet gives `-4804/1859`.
- Therefore neither row locations nor unicycle skeletons can be treated
  pointwise.  The remaining global target is a simultaneous cancellation
  over all fixed-colour locations and all spanning-unicycle completions.
- Summed all attachment forests for each fixed directed cycle by the
  all-minors theorem.  This larger unit is still insufficient: on the same
  triangle, the cycle `(2,0)->(6,0)->(3,2)->(2,0)` has a strictly negative
  degree-eight Bernstein control at every nonzero level; its level-one
  value is `-783/11534336`.  The exact 362-cycle audit reconstructs the
  global determinant, so cancellation across distinct cycles is essential.
