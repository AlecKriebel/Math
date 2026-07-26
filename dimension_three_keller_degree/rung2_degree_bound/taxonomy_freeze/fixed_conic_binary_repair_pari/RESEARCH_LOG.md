# Research log: independent PARI repair of the binary fixed-conic bridge

## 2026-07-26

- Began from the frozen taxonomy and the post-freeze audit report only, as
  required.
- Confirmed the audit target: the legacy PARI calculation evaluates the
  degree-six obstruction on one specialized tuple and does not retain the
  full degree-seven affine fibre.
- Fixed scope: binary fixed divisor \(h=pq\) and \(h=p^2\), with the complete
  degree-eight cubic normal, 12 arbitrary coefficients of \(V\), 18 arbitrary
  coefficients of \(H_2\), and 9 arbitrary entries of the linear part.
- Chosen independent method: PARI/GP 2.17.4, using coefficient matrices over
  \(\mathbb Q\), constant-pivot Gaussian elimination, and direct polynomial
  identities. No SymPy computation will be used.

### 2026-07-26T10:14:10Z checkpoint

- Verified independently that the general 30-coefficient ternary cubic
  \(E_8\) matrix has rank 12 for both \(h=pq\) and \(h=p^2\). The displayed
  18-parameter normal has coefficient rank 18 and lies in the kernel, so it
  is complete.
- Computed the full raw \(E_7\) coefficient matrices. Both have rank 7 in
  the 18 \(H_2\) variables. A common constant pivot minor is
  \(-524288=-2^{19}\), leaving an 11-dimensional affine fibre with no
  parameter-dependent division.
- Retained all 15 nonzero split-root and 13 nonzero double-root left-null
  compatibility generators in `verify_universal_e7_e6.gp`.
- Reduced the set-theoretic compatibility loci to
  \[
  \sqrt{I_{7,pq}}=\langle e,f,b,c,(a-3d)v_4,(3a-d)v_9\rangle
  \]
  and
  \[
  \sqrt{I_{7,p^2}}=\langle e,f,b,(a-2d)v_4,
  (a-4d)v_3-6cv_4-6(a-2d)v_8\rangle.
  \]
- Substituted the complete 11-parameter fibres into \(E_6\), with all 12
  coefficients of \(V\) and all 9 entries of \(L\) retained. Exact equality
  gives
  \(12p^2q^2(a-d)^2(a+d)\) and
  \(24dp^2(cp+(d-a)q)^2\). No free lower coefficient remains.
- Exhausted the factor components and their intersections. They give exactly
  the three split-root and four double-root tangent orbits in legacy (9),
  including the zero field. Found no omitted parameter branch and no
  counterexample to (7)--(9).
- Added `verify_strict.sh`. It guards against GP's recovered-error/zero-exit
  behavior and requires exact rank, pivot determinant, free-variable,
  universal-factor, and final pass markers.
- Scope decision: mark the disputed \(E_7\to E_6\) bridge repaired. Do not
  infer promotion of the whole binary/global row from this package because
  the later branch endgames were not re-audited here from complete fibres.
