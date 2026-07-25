# Research log: unmarked triple-companion \(c=0\)

All times are UTC.

## 2026-07-25T07:53:00Z — raw kernel normalized

- Reconstructed the raw \(E_7\) matrix at \(c=0\): rank \(16\), nullity
  \(10\).
- Separated its kernel into five legal affine/target gauge directions and
  five normal directions.
- Obtained the complete five-parameter normal form in `NOTE.md`.

## 2026-07-25T07:57:00Z — degree-six compatibility

- Found a parameter-free rank-ten lower minor \(7925422620672\).
- Exact left-kernel compatibility gives
  \(w_1(w_2-w_3)=0\) and \((w_2-w_3)^2=0\), hence \(w_2=w_3\).
- Solved the complete \(E_6\) system and checked the full converse.

## 2026-07-25T08:02:00Z — zero-column exit

- Degree-five compatibility forces \(w_1^3=0\).
- The remaining constant four-variable minor \(20736\) makes
  \(\ell_{12}=\ell_{22}=0\).
- Since the degree-six solve already gives \(\ell_{32}=0\), the second
  column of the linear part vanishes.
- Added the exact SymPy reconstruction.  The theorem remains provisional
  until an independent hostile audit passes.

## 2026-07-25T08:32:00Z — hostile reconstruction passed

- A fresh PARI/GP implementation rebuilt the raw determinant and complete
  five-direction gauge.
- It found a literal degree-six square row
  \(-32(w_2-w_3)^2/3\) and the integer degree-five row syzygy giving
  \(8w_1^3/9\).
- Both complete lower solves, converses, and the zero-second-column exit
  pass.  Verdict: PASS with no scope correction.
