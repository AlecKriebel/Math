# Research log — unmarked-double \(\{2,0\}\)

## 2026-07-25T18:21:09Z

- Derived the full \(q^2\)-jet normal form and identified
  \(3b_1^2-8b_2=0\) as the exceptional \(\{2,0\}\) divisor.
- For \(b_1\ne0\), curvature removes the \(r\)-multiplier.  Every
  nonzero contact is the same \(nqN\) tangent, including the internal
  endpoint \(b^3c_0=256c_3\).
- Four top-only \(r^2E_5\) coefficients cannot vanish simultaneously.
- The sole zero-contact endpoint not covered by the plane-field exit has
  \(R=(p+q/4)^3\).  Solving its complete rank-six \(E_5\) system leaves
  the literal obstruction \((9/64)\eta^2rR\) in \(E_4\).
- Exact SymPy and independent PARI/GP suites pass.  The result remains
  candidate pending hostile normal-form and lower-pivot audits.

## 2026-07-25T18:40:21Z — \(b_1=0\) endpoint closed

- Exact gcd at \(b_1=0\) forces the normalized endpoint
  \((P,Q,R)=(pq^3,p^4,dp^3+q^3)\).
- The unrestricted \(E_7\) coefficient matrix has rank \(12\) on
  \(15\) variables.  Its full three-dimensional kernel is
  \(U_r=3pf,V_r=0,T_r=3f\), with
  \(f=mp+nq+\rho r\).
- In each of the three nonzero projective charts for
  \([m:n:\rho]\), the complete \(E_6,E_5,E_4\) chain forces columns two
  and three of the linear part to be proportional.
- At the zero contact, \(E_6\) leaves only
  \((A_r,B_r,\ell_{33})=\ell_{33}(p,0,1)\), which is covered by the
  unconditional plane-field exit.
- Both the exact SymPy rank/branch reconstruction and an independent
  raw PARI/GP weighted-determinant reconstruction pass.  The full
  exceptional unmarked-double \(\{2,0\}\) component is now provisionally
  excluded; hostile audit remains mandatory.
