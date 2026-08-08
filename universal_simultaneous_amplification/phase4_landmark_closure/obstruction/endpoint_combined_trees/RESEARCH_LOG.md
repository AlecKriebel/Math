# Research log: endpoint combined trees

## 2026-08-08 -- combined event-Palm identity

- [PROVED] With `b=m_B^K`, `d=m_D^K`, and `f(A)=1/|A|`, the normalized
  actual endpoint gap satisfies

  \[
  {1\over m_D}-{m_L\over bd}
  =(\alpha_Df-\beta_Cf)
   +(\beta_Cf-(b/d)\alpha_Cf)
   +{b^2-m_Lm_C\over bd\,m_C}.
  \]

- [PROVED] The multiplicative orientation term equals the midpoint term
  minus the exact cross correction

  \[
  {b^2-m_Lm_C\over bd\,m_C}
  ={2b-m_L-m_C\over d\,m_C}
   -{(b-m_L)(b-m_C)\over bd\,m_C}.
  \]

- [EXACTLY COMPUTED] The persistence term is negative on the frozen `n=4`
  witness; the timing term is negative on the frozen `n=5` witness and the
  `n=7` windmill.  The full combined gap is positive on all three.

## 2026-08-08 -- paired tree determinant

- [PROVED] If `tau_L` are continuous Bd-dual rooted-tree cofactors and
  `theta_D` are locked-dB event-arborescence cofactors, then the actual
  product inequality is exactly

  \[
  \sum_{A,B}\tau_L(A)\theta_D(B)
  \left({bd\over|B|}-|A|\right)\ge0.
  \]

- [PROVED] An equivalent continuous-tree form is

  \[
  \sum_{A,B}\tau_L(A)\tau_D(B)(bd-|A||B|)\ge0.
  \]

- [EXACTLY VERIFIED] Both event root laws were independently reconstructed
  from directed-tree cofactors, and all identities replay on `K4`, weighted
  `P3` with ratio `1:17`, both batching sign-failure graphs, and the frozen
  seven-vertex dB windmill.

- [OPEN] The global paired-tree sign for arbitrary connected undirected
  weighted graphs.

## 2026-08-08 -- forward forest surgery audit

- [PROVED] Direct forward generators give the paired absorbing-forest
  determinant exactly equivalent to the actual normalized product.

- [EXACTLY VERIFIED] Every outgoing two-root forest was enumerated on the
  weighted `P3`; the sums equal the determinant and linear-solve formulas.

- [PROVED] For an adjacent edge `(S,S+v)` and
  `S*=V\(S union {v})`, each Bd and dB bias product equals `r^2` across the
  complementary pair.  The cross-orientation factor `Xi` and the
  complete-normalized bias product `Pi` obey

  \[
  \Xi(S^*,v)=\Xi(S,v)^{-1},\qquad
  \Pi(S^*,v)=\Pi(S,v)^{-1}.
  \]

- [FALSIFIED] Any one-sided state-edge domination used before summing the
  forests.  On weighted `P3`, the exact factors are `Xi=17,1/17` and
  `Pi=1/17,17`.  Exact reciprocal failures also occur on both batching
  witnesses and the windmill.

- [PRECISE GLOBAL OBSTRUCTION] Complement pairing produces reciprocal
  local factors and loses the dB timing denominator from the path bias,
  while that denominator remains on side branches.  A valid tree surgery
  must transport mass across multiple roots/side branches; local
  reverse/complement path replacement cannot prove the endpoint sign.

## 2026-08-08 -- hidden-target conjugation audit

- [PROVED] For a fixed target, the conditional labelled reversed-arrow and
  dB source laws have ratio `d_v/(t_v d_u)`.  A history of `k` selective
  samples and one neutral sample therefore carries an exact endpoint degree
  potential, a target clock, and a residual source-collision factor.

- [EXACTLY COMPUTED] On weighted `P3` with degrees `(1,17,18)`, the neutral
  event has a common endpoint clock `1/2`.  After one selective sample the
  endpoint clocks are `9/2,9/34,9/2`; the middle value is the predicted
  target clock times the collision factor `1/17`.

- [FALSIFIED] Cancellation of this defect by the full `r=3/2` geometric
  mixture.  The exact post-mixture endpoint clocks are
  `53/90,37/90,1961/450`, hence no target-only row clock and endpoint
  diagonal `D(A)=product_i d_i` can conjugate the two kernels.

- [PRECISE REMAINING POSSIBILITY] A source-history or multiplicity-labelled
  Feynman--Kac representation retains the collision factor exactly.  Its
  projection requires a new global collision-weight inequality; target
  marking alone is insufficient.
