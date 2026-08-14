# Research log: Kac derivative versus endpoint pins

## 2026-08-13 19:45 PDT — exact bridge audit

- Identified the singleton Kac reward exactly as the derivative at zero of
  the root Schur complement of the diagonally tilted full subset generator:
  `Sigma_i'(0)=g_i+Q_iR(-Q_RR)^(-1)g_R=psi_i`.
- Derived the corresponding ordinary endpoint-action source and hard-pin
  derivatives.  They contain only the endpoint and inverse endpoint
  Hessian, not the full subset killed Green kernel.
- Proved a sharp rule-blind pin obstruction on complete regular modules.
  There `J_B=J_D` identically and every standard coordinate pin agrees,
  while `psi_B=1/r` and
  `psi_D=(s-r^(s-1))/(r(s-1))` are unequal.
- Hostile sign audit: the general dB reward is positive only when
  `r^(s-1)<s`.  The scoped active witness is `K_2`, where both rewards are
  positive for every `1<r<2`, including the full rational interval
  containing `R_hyb`.
- This closes only a rule-blind endpoint-pin interpretation.  It does not
  prove or refute the diagonal Kac inequality.
