# Research log: fixed-linear binary power fibre

All timestamps are UTC.

## 2026-07-25T12:38:00Z — general companion opened

- Normalized the power-fibre exception to
  \[
  H_4=(p^4,pB_3(p,q),0),\qquad (H_3)_3=p^3,
  \]
  where \(B_3\) is coprime to \(p^3\), so its \(q^3\)-coefficient is
  nonzero.
- The top multipliers satisfy
  \[
  \alpha=-3p^3(B_3)_q,\qquad
  \beta=0,\qquad
  \gamma=4p^4(B_3)_q,
  \]
  hence the complete \(E_7\) identity is again
  \(-3U_r+4pT_r=0\), while \(V_r\) remains free.
- Opened a full-coefficient determinant expansion to test whether the
  nonzero \(q^3\) coefficient of \(B_3\) eliminates the exception before
  any moduli classification.

## 2026-07-25T12:48:06Z — entire power fibre provisionally closed

- Depressed and scaled the arbitrary coprime cubic companion to
  \(d_0p^3+d_1p^2q+q^3\), retaining both moduli.
- On \(v_9\ne0\), exact \(E_6,E_5\) coefficients force all \(r\)-top
  parameters to zero; \(E_4\) then kills \(\ell_{33}\) and \(E_3\)
  kills \(\ell_{32}\), making the linear part singular.
- On \(v_9=0\) with nonzero
  \(\ell=v_7p+v_8q\), handled \(v_8\ne0\) and \(v_8=0,v_7\ne0\)
  without normalizing either coefficient.  Both branches end with
  \(\ell_{33}=\ell_{32}=0\) and a singular linear part.
- On \(\ell=0\), the identity
  \([r^2]E_5=-(4/9)pt_p^3(d_1p^2+3q^2)\) removes \(t_p\).
  The two remaining coordinate exits have plane degrees at most \(6\)
  and \(10\), so the unconditional plane bound and birational Keller
  theorem make every surviving Keller map an automorphism.
- Added `POWER_FIBRE_NOTE.md`, a full exact verifier, and a strict wrapper.
  The primary suite passes.  Promotion awaits an independent hostile
  reconstruction.

## 2026-07-25T13:02:27Z — independent CAS replay added

- A manual proof replay found that the exposition had omitted the necessary
  \(E_4\) relation
  \(\ell_{12}=\ell_{32}(u_0-8c_0/9)\) on the \(v_9\ne0\) branch.
  The SymPy substitutions already imposed it; the note now states it.
- Added a fresh PARI/GP construction of the full weighted determinant.
  It independently confirms the displayed \(E_6,E_5,E_4,E_3\)
  coefficients, retains \(d_0,d_1\), and recomputes the plane degree
  ceilings \(6\) and \(10\).
- The strict wrapper now requires both SymPy and PARI/GP.  The dual-engine
  suite passes.  This strengthens the algebraic evidence but does not
  replace the pending hostile normalization and theorem-scope audit.
