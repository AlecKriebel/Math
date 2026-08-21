# Research log: exceptional power fibre

All timestamps are UTC.

## 2026-07-25T11:42:00Z — lower-identity solve opened

- Isolated the constant-dependent Hilbert--Burch exception
  \[
  H_4=(p^4,p^2q^2,0),\qquad (H_3)_3=p^3.
  \]
- This orbit is disjoint from the \(\delta=0,\ldots,4\) table and has
  \(E_7\) block ranks \((1,2,3)\).
- The exact \(E_7\) identity is
  \[
  -3U_r+4pT_r=0;
  \]
  \(V_r\) is initially free.
- Opened a full-coefficient \(E_6\) expansion without choosing a lower
  gauge.  The objective is either a specialization-safe singular-linear
  contradiction or a complete list of lower survivor leaves.

## 2026-07-25T11:58:42Z — \(v_9\ne0\) branch exactly excluded

- Retained all coefficients in \(H_2,H_3\) and reconstructed
  \(E_7,\ldots,E_3\) from the full weighted determinant.
- On the branch where \(v_9=[r^3](H_3)_2\ne0\), exact coefficient
  comparison splits into \(t_p\ne0\) and \(t_p=0\).
- A legal source shear on the first branch reduces the full
  \(E_6,E_5\) solution to the unavoidable obstruction
  \([r^3]E_4=-(8/27)qt_p^4\).
- On \(t_p=0,c_1\ne0\), the obstruction is
  \([q^2r^2]E_4=(4/3)c_1^3v_9\).
- The sole remaining leaf either makes two rows of \(L\) collinear or
  has a nonzero \(q\)-coefficient in the necessary \(E_3\) factor.
- Strengthened `verify_power_fibre_v9_sympy.py` to check not only the
  final substitutions but also the forcing coefficients that establish
  branch completeness.  The strict exact run passes.
- Wrote `V9_EXCLUSION_NOTE.md`.  Promotion is withheld pending an
  independent hostile audit.

## 2026-07-25T12:29:43Z — entire exceptional power fibre provisionally closed

- Split \(v_9=0\) by the stabilizer orbit of
  \(\ell=v_7p+v_8q\): \(0,p,q,p+q\).
- Exactly excluded the \(q\) and \(p+q\) orbits.  The \(q\) orbit has a
  final \((8/9)\ell_{33}^3\) obstruction on its nonsingular branch; the
  \(p+q\) orbit forces a singular linear part.
- Exactly excluded the \(p\) orbit.  Its \(t_p\ne0\) branch combines
  \([r]E_5\) with \([r^3]E_4\) to give
  \(-20t_p^4/81\); both \(t_p=0\) leaves force either a nonzero
  coefficient or \(\det L=0\).
- On the zero orbit, \(E_6,E_5\) force
  \(t_p=t_q=t_t=a_a=0\).  If \(\ell_{33}\ne0\), the coordinate
  \(w=F_3\) leaves a plane Keller map of degree at most \(6\).  If
  \(\ell_{33}=0\), the binary cubic submersion classification forces a
  triangular coordinate and a plane degree ceiling of \(9\).  The
  unconditional plane bound and birational Keller theorem make both exits
  automorphisms.
- Added three exact \(v_9=0\) verifiers and the strict aggregate wrapper.
  The full primary suite passes, including optimized-Python rejection.
- Wrote `POWER_FIBRE_EXCLUSION_NOTE.md`.  Together with the already audited
  abstract Hilbert--Burch step, this removes the last exceptional fibre
  outside the \(\delta\)-stratified binary fixed-quadratic table.
- Promotion is withheld pending an independent hostile reconstruction.
