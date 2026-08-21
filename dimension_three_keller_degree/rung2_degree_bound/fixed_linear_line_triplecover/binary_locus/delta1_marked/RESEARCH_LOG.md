# Research log: fixed-linear binary \(\delta=1\), marked divisor

All timestamps are UTC.

## 2026-07-25T13:04:00Z — marked component opened

- In the fixed-linear row \(P=pA_3,Q=pB_3\), the universal factor \(p^2\)
  of \(J(P,Q)\) makes the exact-\(\delta=1\) divisor split naturally into
  a marked component \(g=p\) and an unmarked critical-point component.
- On \(g=p\), one has \(R=pS_2\).  The degree-one Hilbert--Burch tangent
  is the divided \(q\)-gradient
  \[
  N=(A_q,B_q,S_q).
  \]
- A target change at \(p=0\) normalizes the \(q^3\)-coefficients of
  \((A,B)\) to \((0,1)\).  Exact \(\delta=1\) then requires the
  \(q^2\)-coefficient of \(S\) to be nonzero, normalized here to \(1\).
- Opened an exact contact-minor calculation with all remaining coefficients
  retained.  No lower Keller conclusion is claimed yet.

## 2026-07-25T13:16:35Z — marked exact-\(\delta=1\) provisionally closed

- Reduced \(S_2\) to its double-root and squarefree orbits under source
  changes preserving \(p\).
- In the double-root orbit, the first contact coefficient makes a second
  linear divisor common to \(\alpha,\beta,\gamma\), so contact leaves
  exact \(\delta=1\).
- In the squarefree orbit, the \(a_2=0\) boundary is inconsistent.  On
  \(a_2\ne0\), legal target changes give \(a_2=1,b_2=0\); the complete
  contact solution has exactly two components.  Their literal common
  factors have total degrees four and three, so both again leave exact
  \(\delta=1\).
- Consequently any exact-\(\delta=1\) Keller map has zero contact
  parameter.  The injective lower syzygy block makes it all-binary, and
  the plane-plus-shear exit gives an automorphism.
- Added independent SymPy and PARI/GP certificates and a strict wrapper.
  Both pass.  Promotion awaits the hostile checklist.
