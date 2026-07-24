# Research log: weighted common-source attack

## 2026-07-24T07:51:49Z

- Started an independent audit of the conditional weighted-isotropy
  branch for a hypothetical 41-point code.
- Fixed assumptions:
  \(G\succeq0\), \(\operatorname{rank}G\leq5\), \(G_{ii}=1\),
  \(G_{ij}\leq1/2\), \(p\geq0\), \({\bf1}^{\mathsf T}p=1\),
  \(Gp=0\), and \(G\operatorname{diag}(p)G=G/5\).
- First objective: separate consequences that genuinely use all of these
  hypotheses from consequences of the projection or one-dimensional
  moment relaxations alone.
- Existing exact nonuniform and zero-support \(D_5\) weights were imported
  only as adversarial test instances; no uniformity or full-support
  assumption will be used.

## 2026-07-24T08:48:00Z

- Proved that the full quadratic identity itself recovers
  \(\operatorname{rank}G=5\), including when \(p\) has zeros.
- Derived the distance common-source identities
  \(Dp=2{\bf1}\) and \(DPD=(24/5)J-(2/5)D\), with exact
  reversible-chain spectrum \(\{1,(-1/5)^5,0\}\).
- Derived the Naimark stress
  \(P-pp^{\mathsf T}-5PGP\succeq0\), its all-subset inequality, and its
  two-point weight/inner-product inequality.
- Found an exact \(D_5\) weighted design supported on only 12 of the 40
  roots.  This leaves 28 exact zero-weight extensions and is a strong
  counterexample to sparse-support arguments that do not couple the
  extensions.
- Converted a numerical local-energy stress test into a 25-point exact
  rational kissing code whose anchored row-square energy is strictly
  greater than \(41/5\).
- Proved strict-boundary-safe negative and positive support-mass bounds for
  every zero-weight vertex.  At threshold \(1/50\), the exact masses are
  at least \(19/147\) below and \(1/4\) above.
