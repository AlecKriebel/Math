# Research log

## 2026-07-23 22:10 PDT

Started an independent normalization audit.  Derived the ordered-base moment
block directly as an average of \([z;1][z;1]^T\).

## 2026-07-23 22:18 PDT

Exact D5 enumeration confirmed the \(\binom N4/N\) K4 factor, the
\(\alpha_q\) ordered-base normalization, and the \(\alpha_q/2\)
unordered-base normalization.  The first attempted unordered audit exposed
the endpoint-orientation loss: the two endpoint kernels merge into one
sum-kernel.

## 2026-07-23 22:33 PDT

Added the vertex flag, K2-to-K3 identities, all oriented K3-to-K4 centering
identities, and ordered-edge PSD blocks.  Exact relabeling reduced 609
apparent K3 rows to 116 distinct integer rows.  A high-accuracy Clarabel
iterate retained pair/triple margin \(0.9045\), with maximum linear and
kernel residual below \(2.7\cdot10^{-10}\).

## 2026-07-23 22:40 PDT

Repaired all 1,433 variables to positive exact rationals.  The 183-row
integral affine system has rank 171.  Exact substitution verified every
row.

## 2026-07-23 22:45 PDT

Completed exact rational PSD verification.  All seven ordered-edge blocks
are positive definite after quotienting by their two or three forced
kernels; the vertex block is positive definite after quotienting by its two
kernels.  All 203 ordered triangle types and all non-deduplicated extension
identities pass exactly.  Conclusion: the full centered ordered-flag K4
mechanism is an exact relaxation barrier, not an obstruction to 41 points.
