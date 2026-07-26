# Research log: cube-component geometry/reference audit

All times are UTC.

## 2026-07-26T06:42:00Z — Audit opened

Created a separate conceptual audit of the claim that every nonsingular
\(C+\ell^3+Q_2+L_1\) is a coordinate.  Scope set to the full rank atlas,
degree transfer, fibrewise injectivity, Ax--Grothendieck, exact plane
threshold, and prior-art collision search.

Best-guess completion: **10%**.

## 2026-07-26T07:05:00Z — Rank atlas reconstructed

Independently derived the rank-\(2/1/0\) transverse quadratic-form
classification.  Checked the rank-one null-vector pivot boundaries and
the rank-zero determinant and coordinate pivots.  Found no missing
boundary.  Confirmed that the only nonsingular charts have explicit
coordinate inverses of degree at most three.

Best-guess completion: **40%**.

## 2026-07-26T07:19:00Z — Degree corollary checked

Verified the exact target-linear-combination sequence
\(F\mapsto H=TF\mapsto G=H\circ\sigma^{-1}\), determinant transfer, and
\(\deg G_i\le3d\).  The Guccione et al. theorem leaves possible degree
pair \((72,108)\), so the safe range is strictly below \(108\).
Consequently \(d\le35\) passes and the uniform \(d=36\) boundary does
not.  Moh's exact older statement is inclusive through degree \(100\),
giving the fallback \(d\le33\).

Best-guess completion: **62%**.

## 2026-07-26T07:33:00Z — Fibrewise/Ax implication repaired

Verified fibrewise injectivity.  Audited the common shorthand that
Ax--Grothendieck directly gives a polynomial automorphism: Ax's primary
statement gives surjectivity.  Here the Keller condition makes the map
étale; pointwise injectivity kills the off-diagonal fibre product, hence
the map is universally injective and therefore an open immersion.
Surjectivity then makes it an isomorphism.

Best-guess completion: **74%**.

## 2026-07-26T07:49:00Z — Primary and adjacent references checked

Checked the precise statement of Guccione--Guccione--Horruitiner--Valqui,
Theorem 2.1, and the primary Ax paper.  Located and compared the closest
literature: Vistoli on full degree-three Keller maps; Blanc--van Santen
on degree-three automorphisms and affine-plane fibres; Kaliman on general
\(\mathbf C^2\)-fibres; Ribeiro on cubic singularities at infinity; and
Shpilrain--Yu on unimodular gradients/retracts.  No exact cube-leading
coordinate theorem was located.  Recorded that this does not establish
novelty.  No journal publication of arXiv:2204.14178 was located.

Best-guess completion: **90%**.

## 2026-07-26T08:01:10Z — Audit finalized

Wrote `AUDIT.md` with explicit PASS/conditional verdicts, exact
hypotheses, every pivot boundary, the target-linear-combination passage,
the \(d\le35\) threshold and \(d=36\) obstruction, the étale repair to
the Ax step, and a hypothesis-by-hypothesis prior-art collision audit.

Best-guess completion: **100%**.

No external contact or outreach was made.  No commit or push was made.
