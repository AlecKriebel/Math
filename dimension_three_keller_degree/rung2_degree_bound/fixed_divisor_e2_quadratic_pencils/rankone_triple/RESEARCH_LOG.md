# Research log

All timestamps are UTC.

## 2026-07-25

- **09:52:51** — Independently closed the \(A\ne0\) half of the branch
  ledger.  The separate PARI/GP reconstruction verifies the four forced
  \(E_5\) branches
  \[
  s=0,\qquad v=s,\qquad 4s=3,\qquad 4s=-3,
  \]
  and eliminates every leaf at \(E_4\), \(E_3\), or the constant-Jacobian
  condition.

- **10:12:00** — Opened a hostile external audit of the completed symbolic
  proof and both independent replays.  The audit was instructed to rebuild
  the equations from the map rather than trust recorded matrices or branch
  labels.

- **10:21:00** — The hostile audit independently reproduced the raw
  determinant expansion, the \(E_7\) linear system, the legal four-dimensional
  gauge quotient, and the top-level \(A=0\) branch cover.

- **10:27:00** — The audit found a genuine certificate gap in the
  \(A=0,\ w_3\ne0,\ D\ne0\) computation: the displayed \(E_4\) pivot on the
  \(a_3\ne0\) chart carried a factor \(a_3^4\), so it did not certify the
  hidden leaf \(a_3=0\).  The primary verifier and the independent PARI/GP
  verifier were both rebuilt on a fresh \(a_3=0\) chart.  They now certify,
  respectively, nonzero pivots
  \[
  \frac{2048}{81}s^8
  \quad\text{and}\quad
  \pm\frac{4096}{81}s^8,
  \]
  then obtain the same \(E_4\) solution
  \(b_1=b_4=b_5=0,\ b_2=C_1D+b_3\), the same \(E_3\) obstruction
  \(\frac43s^2\ell_4\), and the determinant obstruction
  \(D\ell_0\ell_4s\).  Fault-injection tests now mutate this new pivot and
  verify fail-closed behavior.

- **10:32:00** — Corrected the proof text for the legal reduction of a
  nonzero \(xz\)-component.  The source shear
  \[
  (x,y,z)\longmapsto
  (x,\ y+\alpha x,\ z-2\alpha y-\alpha^2x)
  \]
  preserves \(q=y^2+xz\); choosing
  \(\alpha=w_1/(2w_2)\) removes the \(xy\)-term.  The residual \(x^2\)-term is
  removed by an \(x\)-translation together with a relabeling of the free
  cubic tail, using the exact identity
  \[
  (4x^3/3,0,x^2)
  =\tfrac13(\partial_xP,\partial_xQ,\partial_xR)
   +(0,-2xy^2/3-x^2z,0).
  \]
  No unsupported target shear is used.

- **10:38:00** — The hostile audit independently reconstructed the
  \(w_3=0\) origin, \(xz\), and \(xy\) leaves and checked the stabilizer
  reductions and all recorded nonzero minors.

- **10:42:11** — Hostile audit verdict: **PASS**, after the two repairs above.
  It independently checked the full \(A=0\) and \(A\ne0\) coverage and
  confirmed that seven deliberate mutations are rejected.  The detailed
  report and replay scripts are in
  [`audit_hostile_external/`](audit_hostile_external/).

- **10:46:11** — Completed a targeted public priority sweep over arXiv,
  MathOverflow, Terence Tao's blog, the Secret Blogging Seminar, and public
  X/Twitter indexing.  No source located states this exact fixed-leading-form
  degree-four exclusion.  The source-by-source record and the required
  worldwide-priority caveat are in
  [`PRIORITY_AUDIT.md`](PRIORITY_AUDIT.md).

## Current certified result

There is no degree-four Keller map
\[
F=H_4+H_3+H_2+H_1+H_0:\mathbb A^3\to\mathbb A^3
\]
with
\[
H_4=(x^4,x^2(y^2+xz),0),
\qquad
(H_3)_3=x^3.
\]
The proof is an exhaustive exact branch calculation with two
methodologically independent replays and a separate hostile reconstruction.
It is a support-shape exclusion, not a lower bound for all dimension-three
Keller counterexamples.

## Verification and review status

This work is AI-assisted and is **not peer reviewed**.  Exact symbolic,
finite-branch, and computer-algebra checks are evidence about the encoded
algebra; they are not substitutes for peer review.  No external person was
contacted during this work.
