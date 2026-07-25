# Research log: fixed-quadratic line double cover

## 2026-07-25T04:43Z — logarithmic reduction opened

- Selected the uncovered taxonomy row
  \((e,a,b,\delta,\nu)=(2,1,2,1,2)\).
- Normalized the outer degree-two cover to
  \((p^2,q^2)\).
- Found
  \[
  \operatorname{adj}J\!\left(h(p^2,q^2,0)^T\right)
  =-2hpq\,k e_3^T,\qquad
  k=(ph_r,qh_r,rh_r-4h)^T.
  \]
- The resulting factor residues kill the third cubic component for every
  nonbinary \(h\), and kill the third quadratic component except when
  \(h\) is a square.

## 2026-07-25T04:59:28Z — both square-factor orbits closed

- The exceptional square normalizes to \(h=r^2\), whose quadratic
  invariant space is \(r\langle p,q\rangle\).
- Diagonal source changes and the swap reduce nonzero invariants to \(pr\)
  and \((p+q)r\).
- In the \(pr\) orbit, \(K=2bc-e=0\) immediately makes two rows of \(L_0\)
  proportional.  For \(K\ne0\), degrees four through two give a complete
  parameterization whose linear determinant vanishes identically.
- In the \((p+q)r\) orbit, four degree-four coefficients form a
  specialization-safe two-variable recurrence.  Its sole resonance is
  killed by the degree-three squares \(-2X^2\) and \(-2Y^2\).  Outside that
  resonance, degree three has one common factor dividing \(\det L_0\); at
  the resonance, one degree-two coefficient and one degree-one coefficient
  differ by the square of the remaining factor.
- Independent SymPy and PARI/GP regressions pass.  The GP check is
  fail-closed behind a diagnostic-rejecting wrapper.
- The theorem remains provisional pending an adversarial scope audit and a
  current source-specific priority sweep.  The binary fixed quadratic
  remains open.

## 2026-07-25T05:38:33Z — hostile audit passed and theorem promoted

- An independent reconstruction proved that the square over
  \(\mathbb C(t)[s]\) rehomogenizes globally as
  \(h=c(r+uq+vp)^2\).
- The full stabilizer preserves the doubled fixed line, reduced-pencil base
  point, and the two ramification lines.  Its nonzero quadratic-normal
  orbits are exactly \(pr\) and \((p+q)r\).
- The audit obtained constant raw ranks \(10,14\) in degree six and \(4,6\)
  in degree five, with the full displayed nullities and converses.
- It independently verified the \(K=0/K\ne0\) split, the rank-\(4\) and
  rank-\(3\) lower solves, the literal divisibilities by \(M,M_*\), and the
  division-free identity
  \(a[pr]E_2-[p]E_1=M_*^2\).
- Optimized-Python and GP-diagnostic fault injection both fail closed.
- Verdict: PASS.  The nonbinary subrow is promoted; the binary locus
  remains open.
