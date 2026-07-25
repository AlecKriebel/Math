# Research log

## 2026-07-25T10:59:30Z — hostile audit opened

- Began an independent reconstruction of the vertical fixed-linear cubic
  pencil package without modifying candidate files.
- Isolated the principal risks: the sign convention for
  \(\operatorname{ord}_\infty R\), nonreduced fibre components, possible
  finite poles in the \(m=3\) branch, completeness of the two companion
  orbits, source stabilizers, and the minimality boundary.

## 2026-07-25T11:07:00Z — divisor and orbit reconstruction

- Re-derived
  \[
  4v_f(G)-d(a+\mathbf1_{f=h})=a\,\operatorname{ord}_\infty R
  \]
  at every multiplicity-\(a\) component of \(p=0\).
- Confirmed the \(m=1\) congruence obstruction for both possible
  multiplicities in the quadratic cofactor and the immediate odd-parity
  obstruction for \(m=2\).
- In the \(m=3\) branch, explicitly ruled out finite poles and enumerated
  every cubic fibre multiplicity type.  Only one finite zero of order four
  survives, giving a cubic pencil member.
- Checked that \(q\mapsto aq+bp\) normalizes every nonvertical companion
  to \(q\), while divisibility by \(h\) separates it from the \(p=h^3\)
  companion.

## 2026-07-25T11:12:00Z — boundary attack and exact certificate

- Found the sharp nonminimal test
  \[
  p=z^3,\qquad q=x^3+x^2z+xz^2,
  \]
  whose cubic \(E_8\)-kernel is four-dimensional.  This lies exactly on
  the stated binary reclassification boundary and therefore does not
  contradict the theorem.
- Built a dependency-free exact verifier using dictionary polynomial
  arithmetic, rational row reduction, and integer divisor enumeration.
- Recomputed all marked degree-two and degree-three kernels, source rank
  pairs, stabilizers, two primitive kernels, and top-three witnesses.

## 2026-07-25T11:15:08Z — verdict

- Strict exact run passed.
- All eleven fail-closed mutations passed.
- Verdict: **PASS**, with one nonfatal request to spell out the finite-pole
  and total-zero-order steps in the \(m=3\) proof.
- Estimated completion of this bounded audit task: **100%**.
