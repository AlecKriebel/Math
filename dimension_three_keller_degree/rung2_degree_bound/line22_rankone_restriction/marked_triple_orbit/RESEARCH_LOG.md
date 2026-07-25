# Research log: marked triple-companion orbit

All times are UTC.

## 2026-07-25T08:26:00Z — enlarged raw kernel normalized

- Reconstructed raw \(E_7\) rank \(8\), nullity \(18\).
- Separated five legal affine/target gauges and thirteen normal directions.
- Obtained the complete normal form with parameters
  \(A,w_1,\ldots,w_5,B_1,\ldots,B_7\).

## 2026-07-25T08:33:00Z — degree-six branch ideal

- Exact left-kernel compatibility forces \(w_4=w_5=0\).
- With \(K=4w_3-3A\), the remaining ideal is
  \(Aw_1=Ad=0\) and \(K\) times all transverse \(B\)-directions.
- Split the proof into \(K\ne0\), \(K=0,A\ne0\), and \(K=A=0\).

## 2026-07-25T08:42:00Z — every lower leaf closed

- The \(K\ne0\) branch reduces to
  \(H_3=(Axq,Czq,x^3)\), \(W=w_3q\); its \(C\ne0\) and \(C=0\)
  leaves both force \(\det L=0\).
- In the resonant \(A\ne0\) branch, degree five reduces \(V\) to three
  coefficients and degree three kills the remaining \(B_1,B_2\);
  the residual column vanishes.
- In the resonant \(A=0\) branch, degree-five cubes kill \(w_1,w_2\)
  and degree-four squares kill \(\ell_{32},\ell_{33}\).

## 2026-07-25T08:46:00Z — provisional package completed

- Added the full theorem and exact branch-tree verifier.
- The result awaits an independent hostile reconstruction before promotion.

## 2026-07-25T09:19:25Z — hostile repair and independent audit passed

- Hostile review found three real specialization defects in the
  provisional proof: a rank drop at \(A=0\) in the open branch, a fresh
  \(B_1=B_2=0\) leaf in the \(K=0,A\ne0\) branch, and the exceptional
  \(V=Czq\) shape when \(K=A=0\).
- Each leaf was recomputed without the invalid pivot.  The repaired
  primary SymPy certificate closes them, including the cases with free
  \(\ell_{13}\).
- An independently implemented PARI/GP reconstruction confirms the raw
  kernel, compatibility ideal, and every repaired determinant exit.
  Strict transcript checks and targeted corruption tests pass.
- Status promoted to exact audited theorem.  The work remains
  unreviewed.
