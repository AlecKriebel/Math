# Research log: line-\((2,2)\) companion-at-infinity boundary

## 2026-07-25T06:46:00Z — boundary opened

- Work in the rank-two-restriction pencil
  \[
  p=x^2,\qquad q=yz,
  \]
  with cubic normal companion \(R_3=xq\).
- There are two outstanding joint-moduli families:
  \[
  H_4=((p-aq)^2,q^2,0)
  \]
  with \(a=0\) or \(a\ne0\), and
  \[
  H_4=((p-aq)^2,(p-bq)^2,0),\qquad a\ne b,
  \]
  with both outer critical points finite.
- First experiment: reconstruct the complete raw \(E_7\) kernels over
  symbolic moduli, quotient only by verified translation/shear directions,
  then test whether \(E_6\) and \(E_5\) force proportional columns of the
  linear part.  All specializations at maximal-minor zeros will be retained
  as separate strata.
- No theorem is claimed at this checkpoint.

## 2026-07-25T06:53:00Z — open and outer charts solved

- Exact raw \(E_7\) minors give rank \(18\) for every
  outer-critical-at-infinity parameter and for finite outer pairs away
  from \(t=-2,-1/2,1\).
- Eight complete kernel directions reduce by legal translations and
  target shears to
  \(H_3=(0,Cx^3,xq)\), \(W=w_0p+w_1q\).
- Full \(E_6\) and \(E_5\) minors force the last two columns of the linear
  part to vanish.  The only valid omitted finite orbit is the single
  unordered resonance \(t=-2\sim-1/2\).

## 2026-07-25T07:34:00Z — partial hostile audit passed

- A fresh auditor reconstructed the stabilizer, projective orbit coverage,
  raw kernels, affine gauges, special ranks, and all nonresonant/outer
  lower converses.
- An independent PARI/GP backend and exact-output fault tests were added.
  No defect was found in the claimed partial theorem.

## 2026-07-25T07:39:00Z — resonance closed symbolically

- At \(t=-2\), the raw \(E_7\) rank is \(14\).  Five legal gauges plus
  seven displayed normal directions have independence minor \(82944\).
- Exact \(E_6\) compatibility forces all four noninvariant coefficients
  of \(W\) to vanish.  The reduced \(E_6\) solve has minor \(5308416\).
- The full \(E_5\) pivot minor is \(576\), with residual
  \[
  36K(\ell_{32}y^3z^2-\ell_{33}y^2z^3).
  \]
  Both \(K\ne0\) and \(K=0\) make the last two columns of \(L\)
  dependent.
- The resonance theorem is exact but remains provisional pending a second
  backend and hostile reconstruction.

## 2026-07-25T10:07:13Z — resonance hostile audit passed

- A fresh PARI/GP backend reconstructed the projective orbit ledger and
  the full \(t=-2\) resonance without importing the SymPy matrices.
- A nonzero \(14\times14\) raw minor and the twelve-direction independence
  minor prove kernel completeness and validate the five legal gauges.
- Denominator-cleared polynomial \(E_6\) syzygies reproduce the square
  chain globally.  The reduced constant minor and direct substitution prove
  the full converse.
- The \(E_5\) pivot and residual reproduce both \(K=0\) and \(K\ne0\)
  determinant exits.
- Strict transcript checking and six injected mutations pass fail-closed.
  The theorem is promoted from provisional to independently audited exact
  status.
