# Research log: normalized cross-rule endpoint at fitness two

## 2026-08-13 09:53 PDT -- exact shared-arrow tree reduction

- Fixed the decisive sufficient endpoint target

  ```text
  m_L/b_n + m_D/d_n <= 2,
  b_n=n*2^(n-1)/(2^n-1),
  d_n=(n-1)*2^(n-2)/(2^(n-1)-1).
  ```

- Derived its exact common-denominator tree numerator

  ```text
  S_n=2*b_n*d_n*Z_L*Z_D-d_n*Y_L*Z_D-b_n*Z_L*Y_D
     =sum_(A,B) tau_L(A)tau_D(B)
        (2*b_n*d_n-d_n*|A|-b_n*|B|).
  ```

- Proved that the same sign is one root-cost sum for the independent product
  generator `L tensor I + I tensor D`: product-chain cofactors differ from
  `tau_L(A)tau_D(B)` by one positive root-independent factor.
- Specialized the weighted adjoint to fitness two.  Since the reference
  `mu(A)=(r-1)^|A|` is uniform, `L^T=C+V` has only a diagonal defect; hence
  `L(B,A)=C(A,B)` off diagonal.  Reversing a whole `L` in-tree gives a
  weight-preserving `C` out-tree.
- Combined this with the exact fair-geometric targetwise expansion

  ```text
  G_v=sum_(j>=0) 2^(-j-1) S_v^j N_v,
  (I-S_v/2)(G_v-I)=C_v/2.
  ```

  The minimal literal object is therefore a paired out-`C` tree and an
  in-tree made of target-locked histories of the same row arrows.
- Recorded the exact algebraic bridge through `m_C`, but did not assume the
  two pieces have separate signs.
- Reconciled this with the earlier r=2 tree-reflection route closures:
  complement rerooting, fixed-skeleton transport, and fixed-length labelled
  history injection are already exactly false on `K_3`.  A proof of the
  paired sign must use global cancellation between the two tree factors.
- Exact weighted three-path fingerprint:

  ```text
  b=12/7, d=4/3,
  m_L=584/341, m_C=118/75, m_D=6/5,
  2-m_L/b-m_D/d=1033/10230 > 0.
  ```

- **PROVED:** all reductions above.
- **OPEN:** the single all-graph paired-tree sign `SAPT_n`, equivalently the
  normalized cross-rule endpoint inequality.
