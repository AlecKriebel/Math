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

## 2026-08-13 10:18 PDT -- weaker decisive product and local obstruction

- Added the weaker target `m_L*m_D<=b_n*d_n`, which by itself rules out
  simultaneous strict amplification at fitness two.
- Derived both of its exact shared-arrow tree forms:

  ```text
  P_n=b_n*d_n*Z_L*Z_D-Y_L*Y_D
     =sum_(A,B) tau_L(A)tau_D(B)(b_n*d_n-|A||B|),
  ```

  and, for the dB event-tree cofactors `theta_D`,

  ```text
  P_n^event=b_n*d_n*Z_L*Phi_D-Y_L*Theta_D
           =sum_(A,B)tau_L(A)theta_D(B)
                    (b_n*d_n/|B|-|A|).
  ```

- Compared the arithmetic and product root costs exactly.  Their difference
  is `(b_n-|A|)(d_n-|B|)`; this is sign-indefinite in precisely the relevant
  amplifier--suppressor regime.
- Exactified the first local obstruction on unweighted `K_3`.  A supported
  `L` skeleton has conditional mean `b_3=12/7`, while the dB state-star
  centered at mask `001` forces its only supported in-root to mask `110`, of
  rank two.  Both the conditional arithmetic and product gaps equal `-1/2`.
  Therefore neither target can be signed one pair of tree skeletons at a
  time; a proof must exchange mass globally among skeletons.
- Weighted-P3 product fingerprint:

  ```text
  1-m_L*m_D/(b_3*d_3)=172/1705 > 0.
  ```

- **OPEN:** `PAPT_n`, the weaker decisive shared-arrow product-tree sign.
