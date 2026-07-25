# Research log

All timestamps are UTC.

- **2026-07-25T07:07Z:** opened the unmarked companion-at-infinity orbit
  \(H_4=((p-q)^2,(p+q)^2,0)\), \(R=xq\) as a separate branch.
- **2026-07-25T07:09Z:** reconstructed the raw \(E_7\) matrix: rank \(18\),
  nullity \(8\). Found the six algebraic directions and two independent
  translation jets; verified the exact relation eliminating the third jet.
- **2026-07-25T07:11Z:** used translations and target shears to obtain the
  complete gauge \(H_3=(Ax^3,Bx^3,xq)\),
  \((H_2)_3=w_0p+w_1q\).
- **2026-07-25T07:13Z:** found a parameter-free degree-six forcing minor
  \(4831838208\). The full solve forces both non-pencil quadratic parts and
  \(\ell_{32},\ell_{33}\) to zero.
- **2026-07-25T07:14Z:** four degree-five coefficients force
  \(\ell_{12},\ell_{22},\ell_{13},\ell_{23}\) to zero. Hence the last two
  columns of \(L\) vanish.
- **2026-07-25T07:16Z:** independent SymPy and PARI/GP certificates passed.
- **2026-07-25T07:18Z:** fail-closed harness and source-specific priority
  search completed; packaged the theorem.
- **2026-07-25T10:00Z:** a dependency-free hostile verifier rebuilt the
  full sparse determinant, raw rank sandwich, legal gauge quotient,
  constant \(E_6\) forcing/converse, and \(E_5\) determinant exit. All
  supplied and hostile strict/fail-closed checks pass. Verdict: PASS for
  this exact joint orbit.
