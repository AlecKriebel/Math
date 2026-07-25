# Research log

All times are UTC.

## 2026-07-25T05:58:00Z — chart opened

- Opened the finite-companion part of the omitted
  outer-critical-at-infinity chart
  \[
  H_4=((p-aq)^2,q^2,0),\qquad R_3=x(p-cq),
  \quad p=x^2,\ q=yz.
  \]
- Preserved the common-scaling modulus \([a:c]\).  Kept separate the
  generic orbit, both raw-rank resonances, the \(c=0\) endpoint, and the
  \(a=0\) endpoint.  The already banked fixed point \((0,0)\) was not
  rederived.

## 2026-07-25T06:06:00Z — complete raw kernels

- Reconstructed the raw \(E_7\) matrices and obtained ranks
  \(18,14,14,16,18\) on the generic, \(c=3a\), \(2c=3a\), \(c=0\), and
  \(a=0\) strata.
- Used only the two target-shear gauges removing the \(x^3\) terms in
  the first two cubic components.
- Recorded explicit maximal minors.  The symbolic generic minor factors
  as
  \[
  -782757789696\,t^4(t-3)^4(2t-3)^6,
  \]
  independently recovering all three exceptional ratios.

## 2026-07-25T06:18:00Z — generic and endpoints closed

- On the generic stratum, solved the complete \(E_6\) and \(E_5\)
  systems.  The last two columns of the linear matrix became
  \(w_1v,w_2v\).
- At \(c=0\), degree-six squares killed the two noninvariant
  coefficients of \(W\); the remaining cubic parameters
  \(r_1,r_2\) led to columns \(r_1v,r_2v\).
- At \(a=0\), the direct \(E_6/E_5\) solve again produced columns
  \(w_1v,w_2v\).
- All zero specializations were retained; no division by \(w_i\) or
  \(r_i\) was used.

## 2026-07-25T06:29:00Z — resonances closed

- On \(c=3a\), \(E_6\) squares first reduced the enlarged raw kernel to
  a two-parameter exceptional \(E_5\) branch
  \(K_1s_1=K_1s_2=0\), with \(K_1=-3A+6B+8w_0\).
- Split on \(K_1\) without cancellation.  On \(K_1=0\), exact
  \(E_4\) coefficients \(-8s_1^2/27,8s_2^2/27\) killed the branch.
- Repeated the argument independently at \(2c=3a\), with
  \(K_2=-3A+6B+8w_0+4w_4\) and \(E_4\) coefficients
  \(8s_1^2/27,-8s_2^2/27\).
- No normal form survived.

## 2026-07-25T06:41:00Z — package assembled

- Wrote the self-contained theorem and corrected frontier: after
  combining this theorem with the already banked \((0,0)\) theorem,
  only the companion-at-infinity form \(R_3=xq\) remains within this
  outer chart.
- Added an exact SymPy rank/kernel/lower-equation certificate and an
  independent direct PARI/GP determinant certificate.
- Added optimized-Python and strict-PARI fail-closed tests.
- Did not edit global registries and did not commit.

## 2026-07-25T07:01:00Z — hostile audit passed

- A fresh audit independently reconstructed simultaneous-scaling orbits,
  all five raw \(E_7\) ranks and maximal minors, the complete gauge-fixed
  kernels, every \(E_6/E_5\) converse, both \(K=0\) resonance square
  exits, and all proportional-column conclusions.
- The audit corrected one orbit-ledger label: the generic normalized
  \((1,t)\) row must explicitly assume \(a\ne0\), so it is disjoint from
  the separately computed endpoint \((a,c)=(0,1)\).
- No mathematical defect or surviving specialization was found.
- Supplied SymPy/PARI checks and the strengthened diagnostic, sentinel,
  extra-output, and nonzero-exit fault tests all pass.  Verdict: PASS.
