# Research log: marked-critical mixed companions

All times are UTC.

## 2026-07-25T08:10:00Z — raw kernels separated

- For \(H_4=(p^2,q^2,0)\), reconstructed both mixed companion rows
  \(R=xq\) and \(R=x(p-q)\).
- Each raw \(E_7\) matrix has rank \(18\) and nullity \(8\).
- In each row, separated five legal affine/target directions from three
  normal directions without division.

## 2026-07-25T08:14:00Z — identical lower mechanism found

- Both \(E_6\) systems have constant rank ten and complete affine solves.
- In both rows \(\ell_{32}=0\) before any specialization of
  \(d=w_2-w_3\).
- Exact \(E_5\) row reduction forces
  \(\ell_{12}=\ell_{22}=0\), so the second column of \(L\) vanishes.

## 2026-07-25T08:18:00Z — provisional package completed

- Added the combined theorem and a single exact SymPy reconstruction for
  both orbits.
- The triple marked companion \(R=x^3\) is explicitly left open.
- Promotion awaits an independent hostile audit.

## 2026-07-25T08:38:00Z — hostile audit passed

- Independent PARI/GP reconstructions confirmed both raw kernels, five
  legal gauges, quotient normal forms, constant \(E_6/E_5\) pivots, and
  complete converses.
- Both systems were rerun at \(d=w_2-w_3=0\); their ranks and solutions
  remain exact.
- The residual marked-pair orbit ledger contains precisely the triple
  marked companion, correctly outside this theorem.
- Verdict: PASS with no correction.
