# Research log: hostile W5 audit

All timestamps are UTC.

## 2026-07-25T11:00:00Z — audit opened

- Began an independent reconstruction of the candidate \(p=23,s=3\)
  deepest-branch certificate.
- Did not import the candidate W5 evaluator or W4 finite-algebra
  implementation.
- Chose a structurally different representation: elements are their full
  regular multiplication matrices, and each cubic root is a block companion
  matrix.

## 2026-07-25T11:12:00Z — matrix tower complete

- Re-derived the inverse parameter \(t=x/(1+xy)\), its cubic
  \(2aT^3-bT^2+2T-c\), and all three reconstruction formulas.
- Built ranks \(1,3,9,27,81\) from block companion matrices.
- At every level verified the cubic relation, forward evaluation under
  \(F\), inverse reconstruction, and recovery of the resolvent parameter.
- Reproduced exactly:
  \[
  (10,22,10,4,0),\quad(2,14,19,11,1),
  \]
  and all twelve requested guard norms.

## 2026-07-25T11:20:00Z — p-adic and sheet checks

- Recomputed the three norms modulo \(23^2\):
  \[
  (460,299,138),
  \]
  giving derivative \(16\).
- Verified the first Hensel lift \(s=371\pmod {529}\) directly.
- Exhausted rational root paths and found the unique vanishing path
  \((10,22,13,1)\), ending at \((22,2,21)\).
- Dual arithmetic gives path derivatives \((7,22,4,19)\) and deepest
  discriminant derivative \(18\).
- The final cubic has simple root \(1\) and double root \(22\).

## 2026-07-25T11:28:00Z — proof audit and fault suite

- Reconstructed the localization and Hensel argument.
- Checked that norm valuation one forces one residue-degree-one,
  order-one prime and cannot hide two sheets.
- Rebuilt the \(S_3^{81}\) kernel argument on 243 leaves.
- Strict replay: \(6.37\) seconds wall, peak RSS \(19{,}824{,}640\) bytes.
- Refactored fault runs so late lightweight mutations do not repeat the
  three heavy prime-square towers.  Full strict-plus-12-fault wrapper:
  \(30.78\) seconds.

## 2026-07-25T11:34:30Z — verdict

- All strict checks and twelve fail-closed mutations passed.
- Caught and reported one factual wording error: “degree-three” needed to
  distinguish total degree seven from generic degree three.  The candidate
  corrected it before promotion.
- Final verdict: **PASS**.
- Estimated completion of this bounded audit task: **100%**.
