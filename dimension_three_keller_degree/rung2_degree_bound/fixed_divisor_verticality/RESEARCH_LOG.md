# Research log: fixed-divisor verticality principle

## 2026-07-25T06:18:12Z — horizontal locus opened

- Isolated the taxonomy row
  \[
  (e,a,b,\delta,\nu)=(2,2,1,1,1),\qquad H_4=h(p,q,0).
  \]
- For a homogeneous normal first integral \(G\) of degree \(d\), scaling
  descent and minimality give
  \[
  G^4/(hp)^d=R(q/p).
  \]
- At any horizontal prime factor \(f^m\mid h\), the exact valuation is
  \(4v_f(G)=dm\), with \(m=1\) or \(2\).
- For \(d=3\), neither \(3\) nor \(6\) is divisible by four.  Thus one
  horizontal prime component already makes the degree-eight identity kill
  the cubic normal component.
- The surviving third component has degree at most two, so the banked
  quadratic-component theorem makes the map an automorphism.
- The vertical datum
  \(h=p=z^2,q=x^2+y^2,G_3=z^3\) is a minimal sharpness witness for the top
  identity, not a Keller map.
- Classified the complete surviving frontier: \(p=h\); or
  \(h=\ell^2,p=\ell m\); or
  \(h=\ell_1\ell_2,p=\ell_1m_1,q=\ell_2m_2\), up to pencil change.
- Exact SymPy and PARI/GP checks are being packaged.  Promotion is withheld
  pending hostile audit.

## 2026-07-25T06:33:00Z — unified fixed-divisor principle

- The valuation argument does not depend on \(e=a=2\).  It applies to
  every quartic line-pencil leading form
  \[
  H_4=h(p,q,0),\qquad \deg h=e,\quad\deg p=\deg q=4-e,
  \quad 1\le e\le3.
  \]
- For any horizontal prime \(f\mid h\), its multiplicity satisfies
  \(1\le m\le e\le3\).  The cubic normal identity would require
  \(4v_f(G_3)=3m\), impossible for all three possible multiplicities.
- This unifies three earlier-looking statements:
  the fixed line in the cubic-pencil row must be vertical; the fixed
  conic in the quadratic-pencil row is restricted to its all-vertical
  frontier; and the fixed cubic in the line-pencil row must be binary.
- Added exact horizontal kernel samples for all three rows to both
  verification backends.  The mathematical proof remains provisional
  until hostile audit.

## 2026-07-25T06:54:01Z — hostile audit passed

- A fresh auditor independently reconstructed the minimal-pair field
  closure, scaling descent, all finite and infinite divisor valuations,
  the \(E_8\) orientation, and the quadratic-component exit.
- A dependency-free modular checker confirmed all three quartic
  line-pencil rows and a mixed degeneration in which a different factor
  of \(h\) is shared with a pencil member.
- The mathematical theorem and the complete \(e=2\) all-vertical frontier
  passed.
- The audit found one packaging defect: the PARI wrapper was not executable
  and could accept an explicit `FAIL` line followed by the correct
  sentinel.  The wrapper and injected-failure tests were corrected.
- All supplied, independent, and fault-injection tests now pass.  The
  theorem is banked as an audited structural result; it remains unreviewed
  and does not by itself exclude every quartic counterexample.
