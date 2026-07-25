# Research log: rank-one-restriction line-\((2,2)\) pencil

All timestamps are UTC.

## 2026-07-25T06:05:00Z — independent chart opened

Opened a new directory for the pencil
\[
p=x^2,\qquad q=y^2+xz.
\]
No simultaneous normal form from the \(\langle x^2,yz\rangle\) pencil was
assumed.

## 2026-07-25T06:13:00Z — full stabilizer recovered

Coefficient comparison proved that every source linear stabilizer has the
form
\[
x'=\alpha x,\quad y'=\gamma x+\beta y,\quad
z'=\delta x-\frac{2\beta\gamma}{\alpha}y+
\frac{\beta^2}{\alpha}z.
\]
The induced base action is the full Borel fixing the marked double-line
value.  This immediately reduced the apparent three-point moduli to the
marked/unmarked critical-pair taxonomy and one cross-ratio \(c\sim-c\) in
the unmarked family.

## 2026-07-25T06:20:00Z — raw \(E_7\) resonance found

Exact coefficient matrices gave the complete rank table.  On the
unmarked normal form the generic rank is \(18\), the triple has rank
\(16\), the companion at infinity has rank \(18\), and the unique finite
resonance \(c^2=9\) has rank \(14\).  Marked-pair ranks are \(8,18,18\)
for the triple, coincident mixed, and distinct mixed orbits.

The open \(18\times18\) minor factors exactly as
\[
-769482217582755840c^6(c-3)^4(c+3)^4.
\]
Eight explicit kernel directions were found, with a constant independence
minor \(-8\).  The \(z\)-translation jet was retained through an explicit
linear dependence rather than discarded.

## 2026-07-25T06:29:00Z — lower exit closed

After the complete affine/target orbit gauge, the open kernel gives
\[
H_3=(Axq,Bxq,x(p-cq)),\qquad (H_2)_3=w_0p+w_1q.
\]
The full \(E_6\) coefficient matrix depends on ten transverse variables
and has minor
\[
-10871635968c^2(c-3)^2(c+3)^2.
\]
Thus \(E_6\) forces the third row of the linear part to vanish off its
first entry and forces both first quadratic components into
\(\langle p,q\rangle\).  Four \(E_5\) coefficients then zero the second
and third entries of the first two rows.  Hence the linear part is
singular, excluding the open orbit.

## 2026-07-25T06:37:11Z — package recorded

Recorded the scoped theorem, exact frontier, SymPy certificate, independent
PARI/GP reconstruction, strict PARI wrapper, and fail-closed guard tests.
No global status file, commit, or branch was changed.

## 2026-07-25T06:38:38Z — priority sweep completed

Completed the source-specific web sweep recorded in `PRIORITY_AUDIT.md`.
No matching stabilizer taxonomy, raw rank stratification, or open-orbit
exclusion was found in the checked sources.  This negative search result
is not a guarantee of worldwide priority.

## 2026-07-25T07:02:00Z — hostile audit passed

- A clean-room reconstruction confirmed the full Borel stabilizer, all
  six joint-moduli rows, the residual equivalence \(c\sim-c\), every raw
  rank, the affine gauges, and the \(E_6/E_5\) singular-column exit.
- Alternate exact minors were found for the open \(E_7\) and \(E_6\)
  matrices, and direct \(E_5\) pair determinants confirmed that the only
  lower division is by the stated nonzero parameter \(c\).
- The mathematical theorem passed.  Before promotion, equation (12), the
  Borel transitivity wording, and the verification-independence
  disclosure were corrected.
- The strict PARI wrapper was strengthened from sentinel recognition to an
  exact transcript whitelist, with injected tests for extra output,
  missing output, diagnostics, and nonzero exits.
