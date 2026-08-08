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
