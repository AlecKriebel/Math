# PR104 / 600008: geometry and literal-source adversarial review

Audit completed 2026-10-06 UTC. This review verifies the preserved submitted proof; it performs no new central proof search. Original research accounting remains **1/5**. It does not establish novelty, publication clearance, or the truth of any imported torsion claim.

## Target and verdict

The exact mathematical target is the candidate theorem for **every real `a,b,c>0`**. With `f²=a sin²t+b cos²t`, let

\[
M=\frac1{2\pi}\int_0^{2\pi}\sqrt{\frac{f^2}{c+f^2}}\,dt.
\]

For the positively advancing, actual-path lift of GKT's equator/North/equator map, the assertion is `rho=(1-M)/(2M)`. For positive integers `n,r`, returning after `n` map iterations with winding `r` is equivalent to `M=n/(n+2r)`. A literal chain of `n` full tropic-to-tropic arcs requires that equation **and even `n`**. Least versus iterated closure must be separated.

**Verdict: PASS for the complete analytic theorem and the literal parameter-condition question under these stated conventions.** I found no substantive mathematical gap in the global conformal coordinates, equator seam, degenerate boundaries, geodesic classification, winding, or parity/minimality assertions. The stronger request for a finite algebraic Cayley condition remains unproved here. Historical priority and publication clearance remain outside this verdict.

I derived the coverage and seam arguments before reading the primary problem wording. I did not read or use the old author's review or `prior_imported_report.json` as verification evidence. The original author's checker was inspected only after the initial independent derivations; the independent control script uses a separate standard-library polynomial expansion, ordinary ellipsoid coordinates, and endpoint-regular quadrature.

## Literal source scope

The inspected [Tabachnikov 2015 article](https://amj.math.stonybrook.edu/pdf-Springer-final/014-0001-3.pdf), §7, printed p62, describes alternating left and right null geodesics going from tropic to tropic; it asks for conditions on `a,b,c` ensuring `(n,r)`-chains. It cites Cayley's formula for the classical Poncelet porism as the motivating precedent. Neither the problem sentence nor the following classical analogy explicitly restricts the answer to polynomial equations, determinants, or finite algebraic operations. Its section title supplies a Cayley motivation, which must be acknowledged, but does not change the literal parameter-condition request into an explicit algebraicity requirement.

The inspected [GKT 2007 primary preprint](https://arxiv.org/pdf/0705.0188v1), §5, pp17–18, defines `T` using an equator point, the right family up to the Northern tropic, and the left family back to the equator. Problem 5.2 asks for a necessary and sufficient relation on the parameters for closure after `k` iterations and `r` turns. The theorem uses `T^k(P)=P`, without requiring `k` to be the least period. GKT assumes `a>b` in its setup; the candidate's direct coordinates separately cover `a=b` and interchange of axes.

The source conventions therefore warrant two distinct statements. In GKT's return-map count, odd `n` is permitted. In Tabachnikov's literal full-arc reading, odd `n` cannot close because an arc exchanges the two disjoint tropics. The submitted theorem states both correctly. The source wording alone does not reconcile these counting conventions; identifying them without the parity qualification would be a real error. The analytic integral criterion is already a parameter-only necessary and sufficient relation. It is not just an unknown rotation number or unspecified endpoint shift.

The [Wüstholz 2017 slides](https://viasm.edu.vn/Cms_Data/Contents/viasm/Media/file/billards_halong2017.pdf) announce an arithmetic result for ellipsoids defined over a number field, using additional Jacobian/period conditions. The inspected null-geodesic slides do not provide a complete proof or a finite explicit formula for every `n,r`. This review draws no priority or equivalence conclusion from that announcement.

## Whole-belt coverage and tangent geometry

Write `Q=x²/a²+y²/b²-z²/c²`; the Lorentz belt is `Q>0` and its tropics are `Q=0`. For a given point of its closure, set

\[
F_0(v)=\frac{(a+c)x^2}{a(a+v)}+\frac{(b+c)y^2}{b(b+v)}.
\]

The ellipsoid identity gives `F_0(c)=1-z²/c<=1`, and `F_0(0)=1+cQ>=1`. The derivative is strictly negative: `x,y` cannot both vanish on this belt. There is exactly one root `F_0(v)=1`, with `0<=v<=c`. The normalized signed `x,y` coordinates then have cosine and sine squares summing to one and determine one `t modulo 2pi`. The sign of `z` specifies the half, except at the common equator. This is a single covering; the signs eliminate the ambiguities present in confocal **squared** coordinates.

The map and its inverse are smooth in each half away from the equator. The root derivative stays nonzero even at coordinate-axis points and at a tropic. Thus the coordinate axes do not create missing charts. Exact direct polynomial expansion verifies the ellipsoid identity, the normal identity

\[
Q=\frac{vf^2}{abc},
\]

the zero metric cross term, and both metric coefficients in equation (8) of the submission. All positive denominators are legitimate in the open half-belt. The resulting metric is `g=(v+f²)(dS²-dY²)` with strictly positive conformal factor. This is a universal rational-algebra check, not a finite parameter sample.

At a tropic the physical surface chart `(t,v)` remains regular. `g_tt=f⁴/(c+f²)>0`, `g_tv=0`, and `g_vv=0`; the nonzero vector `R_v` is the common null direction. It is transverse to the tropic tangent `R_t`, because if it were a multiple of `R_t`, its zero norm and `g_tt>0` would force it to vanish. Thus null arcs reach a tropic transversely in the physical surface; the tropic itself is not a null geodesic accidentally omitted by the classification.

## Equator seam and degenerate-boundary extension

For the equator introduce the **signed smooth physical normal variable** `q=sign(z)sqrt(c-v)`. The submitted map becomes

\[
x=\sqrt{\frac{a(a+c-q^2)}{a+c}}\cos t,\quad
y=\sqrt{\frac{b(b+c-q^2)}{b+c}}\sin t,\quad
z=q\sqrt{\frac{c(c+f^2)}{(a+c)(b+c)}}.
\]

These functions are analytic near `q=0`, and the positive coefficient of `q` in `z` makes this a valid local surface chart. Meanwhile

\[
Y(q)=\operatorname{sign}(q)[H-\tau(c-q^2)],\qquad
\frac{dY}{dq}=\sqrt{\frac{c-q^2}{(a+c-q^2)(b+c-q^2)}}.
\]

The derivative at zero is `sqrt(c/((a+c)(b+c)))>0`. Hence `Y` is analytic odd and the Northern/Southern definitions glue smoothly. The singular coefficient of `dv²` at `v=c` was a chart singularity; it does not persist in the signed `q` chart. This argument also works exactly at `a=b`.

Near a tropic,

\[
\tau(v)=\frac{v^{3/2}}{3\sqrt{abc}}+O(v^{5/2}).
\]

The conformal coordinates extend to a continuous bijection of the **closed** belt and the closed cylinder; the inverse is continuous by compactness. They do not give a smooth Lorentz chart at the boundary. The submission explicitly respects this limitation. An arc has tangential displacement of order `v^(3/2)` and physical normal displacement of order `v`; the other-family continuation produces the familiar cusp. No Levi-Civita connection at the degenerate tropic, continuation into a polar cap, or future-directed spacetime interpretation is needed or asserted.

## Null curves, paths, and ordinary winding

In the open belt, the null line fields of the conformal metric are exactly `dS/dY=+1` and `-1`. Their integral curves are unparameterized geodesics: for a null tangent `X`, metric compatibility gives `g(nabla_X X,X)=0`, and in a two-dimensional Lorentz plane `X-perp` is precisely the span of `X`. Reparameterization therefore makes the acceleration zero. Conversely every null geodesic is in one of these line fields. Their finite vertical interval `(-H,H)` implies that each maximal null arc has one endpoint on each tropic.

Choosing positive `S` advance fixes the direction throughout a chain. On an upward arc `dS/dY=+1`; on the following downward arc of the other family, `dS/dY=-1`. At a boundary the opposite-family arc entering the belt is unique. It cannot be chosen to reverse the winding while still alternating the two prescribed families. A North-return passage and a full boundary-to-boundary arc each advance `S` by `2H`; a two-arc North-to-North passage advances it by `4H`.

Since `S(t+2pi)=S(t)+L`, its lift counts turns in `t`. This agrees with the ordinary winding about the `z` axis: `(x,y)=(A(v)cos t,B(v)sin t)` has positive `A,B`, never meets the origin, and the diagonal positive scaling is homotopic to the unit circle parametrization. Equivalently, the belt's deformation retraction to its equator holds `t` fixed. Winding is an ordinary topological integer, not a redefined index.

The actual-path lift is important for large `c`, when a single arc can turn many times. Reducing its shift modulo one discards exactly the winding information that the problem asks for. The submitted normalization preserves it.

## Integral identity and closure bookkeeping

I independently checked the branch signs in the supplied contour proof. For the branch `R(z)=sqrt(z(z+a)(z+b)(z-c))~z²` at infinity and `a>b`, the upper-bank value is `+i sqrt(abs(product))` on `(0,c)` and `-i sqrt(abs(product))` on `(-a,-b)`. The numerator `z` is negative on the latter interval. Thus `z/R` is **minus i times the positive real integrand on both cuts**. A counterclockwise small loop traverses its upper bank from right to left, giving `2i Iv` and `2i Iu`. The large-circle coefficient is `1/z`; endpoint detours vanish. Consequently `Iu+Iv=pi`, with `Iu=L/2` and `Iv=2H`. The sign and factor in `rho=Iv/L=pi/L-1/2` are correct. Continuity of `Iv` is immediate after `v=c sin²phi`; the integrand is smooth on a compact interval with positive axes. This supports the equal-axis limit. Interchanging `a,b` handles the other ordering.

For `rho=p/q` reduced, the equator map first returns in `q` iterations. The full-arc process returns to its starting boundary precisely when the arc count is even, so its least count is `lcm(2,q)` and its winding is `p*lcm(2,q)/q`. The condition `gcd(n,r)=1` applies to a least-period equator pair; it is not generally the least-period condition for a full chain.

The following exact rotational controls expose the counting distinction rather than refute the submitted theorem:

| `a=b=1`, `c` | `rho` | least `T` iterations | least full arcs | full-chain winding |
|---:|---:|---:|---:|---:|
| `8` | `1` | `1` | `2` | `2` |
| `3` | `1/2` | `2` | `2` | `1` |
| `16/9` | `1/3` | `3` | `6` | `2` |
| `40/9` | `2/3` | `3` | `6` | `4` |
| `21/4` | `3/4` | `4` | `4` | `3` |

All strictly positive axes are allowed. `c=0`, zero transverse axes, and infinite axes are excluded boundary parameters, not counterexamples. As diagnostic controls the script also checks very small/large `c`, strong anisotropy, near-equal axes, swapped axes, equator points, both tropics, and axis crossings. Its ten quadrature cases obey the period identity to within `4.2e-11`; these floating checks are not interval-certified proofs. Its independently generated 810 physical belt points reconstruct within `1.8e-8` after scaling; this is diagnostic coverage evidence, while the monotone-root argument proves globality.

## Strongest verified result and exact remaining gap

The submitted integral gives a complete analytic parameter criterion for the literal full-arc source question, with the explicitly stated parity and optional minimality conditions, and for the separately defined GKT return-map question. The global mechanism and the period evaluation are checkable and do not transfer the central task to an unsupported elliptic torsion assertion. No repair to the central theorem is required by this audit.

A finite algebraic Cayley formula, equivalence with an arithmetic/Jacobian announcement, and historical novelty are **not** established. The former would require a materially new algebraic argument rather than treating a real invariant-coordinate translation as an ordinary elliptic-curve group translation. This audit does not reopen that route. Any promotion must preserve these limitations and must not treat this mathematical pass as publication clearance.

Reproduce the independent controls with `python3 geometry_controls.py`; compare stdout with `controls_result.json`. `MANIFEST.json` pins the exact read inputs and review outputs.
