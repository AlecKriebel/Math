# Research log: hostile audit of the exceptional power fibre

All timestamps are UTC.  This directory is isolated from the primary
certificate directory.

## 2026-07-26T07:37:13Z — audit opened

- Read `POWER_FIBRE_EXCLUSION_NOTE.md`, `V9_EXCLUSION_NOTE.md`, the hostile
  checklist, and every primary exploration and verification script in
  `power_fibre/`.
- Confirmed that the repository was already dirty with unrelated tracked and
  untracked work.  This audit will touch only `power_fibre/audit_hostile/`.
- Chose PARI/GP with a six-term Leibniz determinant expansion as the independent
  algebra engine, rather than importing or copying the primary SymPy
  determinant.
- Reconstructed the weight-seven identity before using any primary branch
  conclusion:
  \[
  E_7=2p^4q\bigl(4p\,\partial_r(H_2)_3
                   -3\,\partial_r(H_3)_1\bigr).
  \]
  Coefficient comparison in a completely general homogeneous cubic gives all
  six nonbinary coefficients of \((H_3)_1\); the four binary coefficients are
  free.  The other quadratic and cubic components do not enter \(E_7\), so
  their advertised generality is genuine.
- Began a direct stabilizer computation.  The distinguished cube \(p^3\)
  forces \(p\) to scale.  Writing a possible second binary coordinate as
  \(cp+dq\), preservation of
  \(\langle p^4,p^2q^2\rangle\) gives the coefficient
  \(2c d\,p^3q\), hence \(c=0\).  Thus the binary stabilizer is diagonal;
  the remaining source freedom is a nonzero scaling of \(r\) and a shear of
  \(r\) by \(p,q\).
