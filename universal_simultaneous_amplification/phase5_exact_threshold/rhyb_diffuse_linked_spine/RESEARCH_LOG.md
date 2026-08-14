# Research log: diffuse linked endpoint spine

## 2026-08-13 — full-state reversible-spine reduction

- Generalized the endpoint machinery to the correctly scaled first input
  `X=(r-1)q` and retained the two endpoint grounds `v=as`, `w=aX`.
- Used the `v`-ground Doob transform

  ```text
  K_ij=P_ij v_j/(V_v,i v_i),
  m_i=pi_i V_v,i v_i^2
  ```

  to obtain a stochastic kernel reversible under `m`.
- For the signed ratio `x=w/v=X/s`, proved the pointwise transport identity

  ```text
  F_r(X)-s = s h1 K(x-1).
  ```

- Therefore the full endpoint gap is exactly

  ```text
  G=<A,K(x-1)>_m
   =<A,x-1>_m
    -(1/2) sum_ij m_i K_ij(A_i-A_j)(x_i-x_j),
  A=r h h1/(a s).
  ```

  This is a full-state cross-Dirichlet reduction, not a sign proof.
- Derived the general-fitness temperature-adjoint residuals
  `d=(r-1)q-s` and `d*=(r-1)h-b`.  Their exact mismatch is
  `d-d*=(r-2)(q-h)`, so the shared-residual energy used at `r=2` does not
  extend to `R_hyb`.
- On one conceptual deterministic two-cycle, verified exactly that both
  orientation quadratic pairings are negative throughout
  `[3/2,151/100]`.  This refutes only their interpretation as nonnegative
  energies and does not refute the desired endpoint inequality.
- No graph or kernel search was performed.  The universal endpoint sign
  remains open.  The next viable target is a two-root Green/Schur comparison
  retaining the orientation-sensitive cross term.
