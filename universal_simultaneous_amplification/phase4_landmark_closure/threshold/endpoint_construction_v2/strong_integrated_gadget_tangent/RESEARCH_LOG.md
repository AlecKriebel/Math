# Research log

## 2026-08-08 07:34 PDT — bounded strong-gadget cycle frozen

- Chose the strong integrated scaling `C*a_ij` internally and `x_i` from each
  gadget vertex to every core vertex.
- Derived the finite local Bd/dB chains directly from the update rules.
- Reinserted the ordinary-core singleton perturbation.  Its exact residuals
  are

  ```text
  s_B = r sum_i x_i u_B(i) - (r-1) sum_i x_i/d_i,
  s_D = r sum_i x_i u_D(i)/d_i - (r-1)(sum_i x_i+r-1).
  ```

- Verified the orbit transition rows against the fully labelled chain for a
  rational 7-vertex test graph, every state, and both rules.
- Proved the arbitrary-order portal-clone boundary identity
  `B_H=0`, `D_H=-sum_i (x_i-1)^2/(1+(r-1)x_i)`.
- Searched weighted complete gadgets of orders 3--7 at `r=1.51,1.55,2`.
  No strict positive balanced tangent survived the far-field correction.
  Runs converged to portal-clone equality or the inherited rare-K2 boundary.
- A final order-3 smoke replay at the three requested fitnesses returned
  balanced coefficients between `-1.01e-6` and `-1.13e-6`, approaching the
  portal-clone boundary at the finite logarithmic cutoff.

Status distinction:

- **PROVED / EXACTLY COMPUTED:** local-chain formula, far-field residual,
  labelled lumping audit, portal-clone obstruction and equality class.
- **NUMERICALLY OBSERVED:** no improvement among the searched genuinely
  interacting gadgets of orders 3--7.
- **OPEN:** a universal sign theorem for arbitrary positive internal matrices.
