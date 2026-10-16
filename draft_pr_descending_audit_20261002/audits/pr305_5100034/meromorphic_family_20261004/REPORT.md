# Independent meromorphic-family audit of PR305 / 5100034

Final audit UTC: 2026-10-04T23:12:34.158471+00:00
Submitted head named by ROOT: `cc083024dbd00de06ad444cd4070f51f60d209eb`.
Reviewed candidate input: `/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr305_5100034/snapshot/problems/5100034_focal_pedal_equality/TURN_1.md`.
Candidate byte SHA-256: `1abb4eaea5ef795f056ea89636defc99eb48f526cd20012b70d663cbeb2c4a34`.

## Verdict and strongest verified result

**PASS for the stated nondegenerate confocal elliptic-caustic theorem.** I found no central analytic gap after independently checking the canonical parameter, perpendicular-foot formulas, exhaustive poles, local orders, common lattice, anti-period, strict real positivity, and all divisions. The proof establishes the stronger intermediate statement that the outer-tangent focal pedal area is a fixed positive multiple of the original-chord focal pedal area, with the same multiplier for both foci. Consequently the source's displayed area-ratio equality holds at every real phase. Primitive signed star traversal, reversal, and positive integral repetitions are covered.

This verdict does **not** establish phase-constancy of the common ratio. That extra assertion is false, and an independently derived exact convex triangle below refutes it. This is a mathematical mechanism audit, with no novelty, priority, or firstness determination.

## Independence and source reconstruction

Criteria were frozen at `2026-10-04T22:59:18.950696+00:00`, before any source, candidate, check, or inherited-review access. SHA-256: `1bbb0dfd74e5aa48e1339e2e42df6c6171bf63743af68e64568b6c4401ae56f0`.

The source-only target and proposed independent route were frozen at `2026-10-04T23:01:46.117797+00:00`, before candidate access. SHA-256: `b0b5d98e05443397f201f65af114da317c2a6c78754fd989315480caf6c1632e`. The first independently authored exact-control program was simultaneously frozen with SHA-256 `a21268f510efcdb8b401c40333a1627b8a66adf56ac3b8ffd354351fd84b1cae`.

The full candidate was first read at `2026-10-04T23:02:07.274818+00:00`. Declarative source/dependency/document bindings were subsequently read. No inherited review, author checker source, or author checker output was read or run. A later independently derived local analytic analysis was frozen at `2026-10-04T23:05:32.004302+00:00`, SHA-256 `6ed7a345c069cf5a8297a6f0c874efecbc7bdc849cf3989e0d14559ff5533c3a`. Extended independent code was frozen at `2026-10-04T23:07:27.127046+00:00`, SHA-256 `a2d47853426ff8f61c31ba0987c1312238851a194ac76bb09aa53792060e1fe0`.

Both source PDFs were downloaded independently, converted, and their page-9 Table 7 tables visually inspected:

| Edition | Exact displayed target | Identifier | Printed page |
|---|---|---|---|
| [arXiv 2004.12497 v11](https://arxiv.org/abs/2004.12497v11), *Eighty New Invariants* | `bar(A1)/bar(A2) = bar(A1')/bar(A2')` | k606 | 9 |
| [Published 2021 paper](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), *Fifty New Invariants* | `A1/A2 = A1'/A2'` | k607 | 349 |

Both rows say all N, value unknown, detected 4/20, and proof unknown. Published k606 is instead a product; arXiv k607 instead concerns antipedals. The source setting is a pair of confocal ellipses with outer semiaxes a>b>0. Unprimed focal pedals use billiard side lines; primed pedals use the outer polygon's tangent side lines. Areas are signed cyclic shoelace areas, not sums of unsigned lobes. Primitive-period and star/repetition conventions are not spelled out in the row; the candidate specifies them and extends through repetition. These are the same geometric target, not a hyperbolic-caustic or arbitrary-polygon theorem.

The independently obtained arXiv/published PDF hashes exactly agree with the candidate's declarative source bindings: respectively `c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da` and `c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42`.

The snapshot excludes the raw `source_record.json` and local-only dependency-source files. Therefore I do not independently authenticate the stronger assertion's dataset wording or earlier review conclusions. The stronger mathematical assertion itself is independently refuted. The present analytic proof does not require accepting earlier review verdicts: its local mechanisms are reproduced and checked here.

## Canonical coordinates and geometry

[Stachel's published Theorem 4.3 and equation 4.9](https://link.springer.com/article/10.1007/s40879-021-00524-2) explicitly give the modulus as caustic eccentricity, vertex increment 2v, and outer semiaxes `a=dn(v)/cn(v)`, `b=k'/cn(v)` after normalizing the caustic major axis to 1. Here `v=2K tau/N`, with coprime primitive N,tau and `0<tau<N/2`. The published contact-coordinate discussion gives contacts at `u±v`. Thus the candidate's canonical parameter and chord-midpoint tangent line are source-supported with the correct modulus convention. An independently downloaded repository copy of that published article is retained; its hash differs from the absent local candidate copy, so no byte-identity claim is made for Stachel.

For a real line `n·X=1` and focus F, its foot is `F+(1−n·F)n/(n·n)`. Substituting the inner and outer tangent coefficients yields exactly the candidate's q and Q formulas. The functions become rational meromorphic expressions in sn and cn. Complexification uses the bilinear dot product and involves no conjugation or Hermitian continuation. On the real locus `1−k sn(u)>0` and `a−k sn(u)>0`; all side lines and consecutive tangent intersections are finite. Consecutive tangent normals have angle change in `(0,pi)`, so cannot be parallel.

All areas scale by the square of the geometric normalization factor. The multiplier C is dimensionless; restoring the original caustic scale preserves the proportionality.

## Complete local pole audit

The [DLMF shift and period table](https://dlmf.nist.gov/22.4) gives, for `r=K+iK'`,

`sn(r+z)=dn(z)/(k cn(z))`,
`cn(r+z)=−i k'/(k cn(z))`,
`dn(r+z)=i k' sn(z)/cn(z)`.

These identities also fix the imaginary cn sign, which is essential here. Let `d=1−k²`. Since `cn(z)−dn(z)=−d z²/2+O(z⁴)`, direct substitution gives the original pedal vertex germ

`q(r+z)=(2/k)(1,i) z^(−2)+O(1)`.

There is no order-one term in this even germ. The difference of the two neighboring vertices is

`q(r+z+delta)−q(r+z−delta)=2q'(r+delta)z+O(z³)`.

The two incident area terms therefore have at most a simple pole, with residue `(2/k) det((1,i),q'(r+delta))`. This explicitly eliminates the double principal part; it does not mistake matching residues for eliminating higher orders. Neighbors are regular because `0<delta<2K` and primitiveness gives distinct parameters modulo4K.

For the outer pedal, put `s=sn(v)>0`, `cv=cn(v)>0`, and `dv=dn(v)>0`. The only new denominator roots are `u±=r±v`. At both roots the numerator vector is

`V=(−a b²/k)(1,i)`.

The respective denominator derivatives are `∓b² s`, giving nonzero opposite residues

`R±=±a(1,i)/(k s)`.

Their separation is exactly delta. Thus the one edge with two singular endpoints has possible order-two coefficient `det(R−,R+)=0`; its order is at most one. Each other incident edge has only one singular endpoint. This argument works for N=3 as well as larger N: only the regular neighbor is then shared by the remaining two edges. N=2 is separately excluded.

Common Jacobi poles are removable in both maps, because the nonzero sn leading coefficient appears in each denominator and cancels the numerator pole. The sn elliptic function has degree2 on the lattice generated by4K and2iK'. Hence the double root `sn=1/k` at r and the two simple roots `sn=a/k` at r±v exhaust the possible new poles; no unenumerated finite denominator roots remain. Lifting to the maps'4iK' imaginary period duplicates these classes by2iK'.

## Lattice and residue argument

Each cyclic trace has real periods4K and delta=`4K tau/N`. Bezout gives their common real period L=`4K/N`, with coprimality explicitly needed. After reduction by L, both traces have only the two possible simple poles

`t+iK'`, `t+3iK'`, where `t=K−v`.

They are distinct on `C/(L Z+4iK' Z)`. Under a2iK' shift, sn is fixed and cn changes sign, so the vertex maps reflect across the x-axis and the signed areas negate. The compact torus and imaginary anti-period are therefore correct. For even primitive N,2K is an integral multiple of L; for odd N it is a half-real-period modulo L. No even-period lattice has been used for odd N.

Strict positive real areas make both traces nonzero. If one listed first pole were removable, the anti-period would make the second removable too. A holomorphic function on this compact torus is constant; the anti-period would force the constant0, contradicting positivity. Therefore each first residue is nonzero, and dividing their residues to define C is legitimate.

Subtracting `B−C A` removes the first pole; the anti-period removes the second. The independently verified order-one bound leaves no higher principal parts and no other poles. The remainder is holomorphic, hence constant, and its anti-period forces0. Evaluating on the real locus makes C positive real. Translating by2K exchanges foci, so the same C works at both. Complex zeros of area traces do not affect the argument: no division by an area meromorphic function is performed until returning to the nonzero real locus.

## Strict signed-area positivity

For tangent normal `n(u)=(-sn(u)/A,cn(u)/B)`,

`det(n,n')=dn(u)/(AB)>0` on the real locus.

The normal angle increases strictly and advances pi over2K. Since delta is in `(0,2K)`, the normal angle increment between consecutive sides lies in `(0,pi)`. The focus is strictly inside both ellipses, so every vector from focus to foot is a positive multiple of its outward normal. Each successive determinant is positive, including the cyclic closing edge using the lifted total angle `2pi tau`. The sum is strictly positive even for star traversal. Translation to the focus leaves the signed shoelace sum unchanged. This supplies all required real denominator nonvanishing and both trace nontriviality claims independently of the target equation.

## Exact controls, diagnostics, and boundary cases

The first frozen program independently used rational geometry of the (5,3) ellipse's axis diamond, with foci±4 and caustic squared semiaxes625/34,81/34. It found original focal areas `3375/289` at both foci and outer focal areas30 at both. All18 combinations of scales1,2,1/3, reversal, and1/2/3 repetitions give exact determinant0.

Independently deriving the reflection equation for an isosceles triangle with vertices `(a,0),(-at,b sqrt(1−t²)),(-at,-b sqrt(1−t²))` gives

`a²/b²=t(2−t)/(1−t²)`.

The independently chosen `t=2/3`, `a²=8`, `b²=5` yields caustic squared semiaxes32/9,5/9, with actual focus±sqrt3. Direct exact reflection, confocal tangency, tangent intersections, perpendicular feet, and shoelace evaluation give

`A±=(64sqrt2±8sqrt3)/81`,
`B±=(16sqrt2±2sqrt3)/3`,
`C=27/4`.

All four areas are positive. The common ratio is greater than1, while central inversion preserves orientation and interchanges foci, replacing it by its reciprocal. Thus separate phase-constancy is false. The candidate's t=3/5, axes²(21,16) triangle was also independently recomputed by the same geometry code. The exact controls include reversal and repetition for both triangles,12 cases total, without using either author checker.

The extended independent program also ran34 separate100-digit mpmath diagnostics: N=3–11; convex and primitive stars (including5/2,7/3,8/3,9/4,11/5); k=.05,.6,.95 and an extreme5/2 test at k=.9999. It independently formed actual chord feet and tangent-intersection polygons, compared the area maps, checked L periodicity and2iK' anti-periodicity, checked complex proportionality, and estimated local leading coefficients/residues at distances1e-8,1e-12,1e-16. Maximum reported errors were approximately3.14e-99 for real geometry/target equality,4.87e-99 for L period,4.71e-100 for the anti-period, and1.12e-95 for complex proportionality. These are **non-interval diagnostics**, not certified enclosures or a universal proof. The analytic proof above carries the universal result.

Boundary conclusions are explicit:

- Reversal negates all four signed areas; repetition multiplies all four by the count. Ratio equality and C survive. An even repetition of an odd primitive orbit need not have ratio1; the candidate appropriately applies primitiveness before the parity reasoning.
- In the circular limit k=0, both foci coincide. Independently, `q=(-sin u,cos u)` and `Q=sec(v) q`, so C=`sec²(v)` and both ratios1 for a regular circular periodic orbit. The compact elliptic torus degenerates in this limit; the circular statement is separately verified, not inferred from an invalid torus limit.
- At k=1 the caustic collapses and real denominators/strict positivity can fail. The proof does not extend there.
- A two-period diameter has zero original pedal signed areas; the two outer tangents are parallel. Its requested ratios and outer polygon are undefined. No value is assigned by this proof.
- Coincident conics, zero-length sides, hyperbolic caustics, and unsigned lobe-area sums lie outside the verified theorem.

## Reproducibility, gaps, and closure

The exact-plus-complex run used native argv

`["/Users/alec/Documents/Math/.venv/bin/python", "/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr305_5100034/meromorphic_family_20261004/independent_exact_complex_checks.py"]`

with cwd `/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr305_5100034/meromorphic_family_20261004`, Python3.9.6, SymPy1.14.0, and mpmath1.3.0. No package was installed. Full stdout, full stderr, exit code0, argv, cwd, and UTC start/end are preserved in `independent_exact_complex_checks.capture.json`. The stdout SHA-256 is `44afb7ddde837aa4a7704a388694287b5c91b340b8534a10bdb6118860a3f31d`; capture SHA-256 is `78dd868ec341fa9ce4cbc87231f69de6080d52d621bdb64fc2e70fbb9913c83f`. Exact rational control capture SHA-256 is `d0e11a7da4f4dd2e7ac4ce1e04c0122c8644c542b0508c0a17b7f2b5c1bfaddb`. Source extraction/render subprocesses also retain full stream captures.

**Remaining mathematical gap within the stated theorem: none identified by this audit.** Numerical coverage is finite and does not replace the local/global argument. Dataset-wording authentication and dependency review provenance are outside this mechanism verdict because those raw local-only files are absent from the supplied snapshot. Historical priority is deliberately unresolved. No blocked unsupported-equivalence route is used: the proposed pole uniqueness proof was independently verified to close the target equality.

All work remains in this dedicated new directory. No shared tracked files, Git index/refs, source candidate files, original inputs, PRs, or remote publication were changed. No outside individual or other chat was contacted. Coordination was only with ROOT via the collaboration channel. Final artifact bytes/modes and native seal execution are recorded by `ARTIFACT_SEAL.json` and `SEAL_RUN.json`, whose own final hashes are delivered to ROOT. After their read-only verification, this audit explicitly stops writing.
