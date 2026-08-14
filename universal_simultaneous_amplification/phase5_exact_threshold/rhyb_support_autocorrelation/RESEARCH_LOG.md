# Research log: endpoint support autocorrelation

## 2026-08-13

- Derived the exact centered balances
  `c E_p x+r E_p(xPx)=0` and
  `c E_p u+r E_p(u^2/h)=0`.
- Compressed the diffuse endpoint support to
  `T_r=r{E_p(xPx)+c^{-1}E_p(u^2/h)}`.
- Verified that this is an exact cancellation inside the stored
  ground-energy square, not an independent positivity theorem.
- Identified the correct self-adjoint autocorrelation operator under `p` as
  `(P+R)/2` and proved its canonical edgewise lower bound
  `E_p(xPx)>=-E_p((1+t)x^2)/2`.
- Used the existing exact positive symmetric singular family to prove that
  the resulting sufficient norm comparison is false throughout
  `3/2<=r<=151/100`, while the true support remains positive.
- The same family proves sharpness: the ratio
  `E_p(u^2/h)/(-E_p(xPx))` tends to `r-1`.  Hence no uniform strengthening
  of the desired coefficient can close the endpoint theorem.
- No graph, kernel, or parameter search was performed.
