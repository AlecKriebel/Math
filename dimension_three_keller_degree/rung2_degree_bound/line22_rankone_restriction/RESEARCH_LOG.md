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

## 2026-07-25T08:32:00Z — unmarked triple \(c=0\) excluded

- Raw rank \(16\) leaves a ten-dimensional kernel and a complete
  five-direction affine/target gauge.
- A literal degree-six compatibility row forces \(w_2=w_3\); an integer
  degree-five row syzygy then forces \(w_1=0\).
- A constant four-pivot solve gives
  \(\ell_{12}=\ell_{22}=\ell_{32}=0\), so the second column of \(L\)
  vanishes.
- Independent PARI reconstruction passed without hidden division or
  rank-drop specialization.

## 2026-07-25T08:38:00Z — both marked mixed orbits excluded

- For the marked critical pair \(H_4=(p^2,q^2,0)\), the two mixed
  companions are exactly \(R=xq\) and \(R=x(p-q)\).
- Both raw \(E_7\) matrices have rank \(18\) and complete
  five-gauge/three-normal kernels.
- Parameter-free \(E_6/E_5\) minors remain nonzero at
  \(d=w_2-w_3=0\), and both complete solves force the second column of
  \(L\) to vanish.
- A hostile PARI audit reconstructed the orbit ledger, all gauges,
  converses, and the collision specialization.  Verdict: PASS.

## 2026-07-25T09:19:25Z — marked triple orbit repaired and excluded

- For \(H_4=(p^2,q^2,0)\) and \((H_3)_3=x^3\), the raw \(E_7\)
  matrix has rank \(8\), with a complete five-gauge/thirteen-normal
  kernel.
- The degree-six compatibility ideal splits into the \(K\ne0\),
  \(K=0,A\ne0\), and \(K=A=0\) branches.  Fresh solves at every rank
  drop, including the free-\(\ell_{13}\) and exceptional \(V=Czq\)
  leaves, force a singular linear part.
- Hostile review found three specialization defects in the provisional
  proof.  The corrected SymPy certificate and an independent PARI/GP
  reconstruction now cover each leaf and pass targeted corruption tests.
  Verdict: PASS.
- The remaining genuine rank-one line-\((2,2)\) frontier is unmarked
  \(c^2=9\) and the unmarked companion at infinity.  The universal
  total-degree floor remains \(4\).

## 2026-07-25T09:55:40Z — unmarked \(c^2=9\) resonance audited

- An independent hostile PARI/GP reconstruction confirmed raw rank
  \(14\), the complete twelve-dimensional kernel and legal gauge, and a
  constant rank-eight \(E_6\) floor through every specialization.
- The successive augmented ranks certify exactly the four square
  compatibilities, while constant \(E_5\) pivots and two literal \(E_4\)
  coefficients exhaust the remaining resonance branch.
- The source/target conjugacy between \(c=3\) and \(c=-3\) was checked
  exactly, including its nonzero Jacobian scaling. Verdict: PASS.
- The unmarked companion at infinity is now the sole genuine
  rank-one-restriction line-\((2,2)\) frontier. The universal
  total-degree floor remains \(4\).
