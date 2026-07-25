# Hostile-audit research log

## 2026-07-25T08:52:17Z — independent reconstruction complete

Reconstructed both raw \(E_7\) systems in PARI/GP.  Confirmed rank
\(14\), nullity \(12\), the two fixed maximal minors, the twelve complete
kernel directions, and the five legal affine gauges.

Reconstructed both global \(E_6\) systems using constant pivot minors.
The residual generators are exactly \(Cw_3,Dw_5\) and
\(Dw_5,Cw_5+Dw_4\), so specialization cannot introduce a hidden
\(E_6\) rank-drop branch.

Rebuilt every lower-identity branch.  The only apparent audit hazard was
a PARI left-kernel basis containing \(1/(C-w_4)\) on the rank-one
\(D=0,C\ne0\) branch.  Cross-multiplication gives polynomial left
syzygies \(Cf\) and \(Cg\); direct reconstruction at \(w_4=C\) gives
nonzero right-hand sides \(2C^4\) and \(-6C^4\).  Hence the apparent
denominator is a basis artifact, not an omitted resonance.

Rebuilt the four \(C=D=0\) specialization charts, including separate
constant-pivot treatment of \(d=0\), and verified that the \(d\ne0\)
determinant is an exact linear combination of two \(E_4\) coefficients.

Added a strict runner and two fail-closed injections.  Verdict: **PASS**.
