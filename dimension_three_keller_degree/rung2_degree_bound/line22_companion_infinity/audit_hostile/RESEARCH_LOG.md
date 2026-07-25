# Hostile-audit log

All times are UTC.

## 2026-07-25T07:14:00Z

Reconstructed the source-pencil stabilizer.  Confirmed that its base
action is scaling only, so the outer moduli split into the
\(\{a,\infty\}\) and \(\{t,1\}\) families.

## 2026-07-25T07:20:00Z

Checked the unordered quotient \(t\sim1/t\), the fixed \(t=0\) orbit,
and the \(t=\infty\) boundary.  Confirmed that the latter is the \(a=1\)
outer chart and that \(-2,-1/2\) form one resonance orbit.

## 2026-07-25T07:26:00Z

Reconstructed the eight-dimensional raw kernels and the full
translation/shear ledger.  No normalization divides by \(a,t,C\), or a
lower coefficient.

## 2026-07-25T07:31:00Z

Rebuilt the raw, \(E_6\), and \(E_5\) matrices independently in PARI/GP,
including special ranks and full converses.  Added a strict exact-output
wrapper and four fault modes plus a valid control.

## 2026-07-25T07:34:00Z

No theorem defect or surviving branch found.  Recorded PASS.

## 2026-07-25T10:07:13Z

Reconstructed the exceptional orbit \(t=-2\sim-1/2\) in a fresh PARI/GP
backend.  Certified the raw rank-\(14\) kernel and all five legal gauges,
the denominator-cleared polynomial \(E_6\) compatibility identities and
constant-rank converse, and both \(K=0\) and \(K\ne0\) degree-five exits.
The strict wrapper accepted the exact transcript, while six independent
mutations were rejected fail-closed.  Promoted the scoped audit to PASS
for every valid companion-at-infinity orbit.
