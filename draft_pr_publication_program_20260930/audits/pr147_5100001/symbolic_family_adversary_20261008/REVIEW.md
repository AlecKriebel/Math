# Independent symbolic-family adversarial review of PR147

Status: PASS for the submitted geometric family and literal period-four counterexample. No mandatory mathematical correction found in this scope. This is an independent preparatory review, not a final package review or historical-priority clearance.

Reviewer scope and independence: read only `original_submitted_attempt/COUNTEREXAMPLE.md` and `source_record.json`, then derived the identities below before creating a separate symbolic check. Did not read the submitted verifier or any prior review. The exact target is the stated product `(A'/A) product sin(theta_i/2)` with interior angles of the orbit and the outer tangent polygon. This report checks the mathematical implication of that supplied statement; it does not independently certify that a journal or preprint prints that statement or establish novelty.

## 1. Exact assumptions and success criterion

Let `a>b>0`, `A=a²`, `B=b²`, `S=A+B`, `c²+d²=1`,

```
δ² = A²d²+B²c²,  δ>0,
U = Ad²+Bc²,
u = (c,d),
v = (-Ad,Bc)/δ,
P = (ac,bd), Q = (a v_x,b v_y).
```

The outer ellipse has semiaxes `a,b`; the fixed inner ellipse has squared semiaxes `A²/S,B²/S`. The target fails if two primitive, convex, nondegenerate four-period billiard orbits with this same fixed caustic have different values of the target quantity. Proving a period-four failure is sufficient to refute a universal assertion for all periods divisible by four. No result about all other periods is implied.

All denominators used below are strictly safe: `δ≥B>0`, `U≥B>0`, `S>0`, `AB>0`. The caustic offset is `λ=AB/S`, satisfying `0<λ<B`; thus the caustic is strictly inside the outer ellipse and is nondegenerate.

## 2. Independent verification of the complete oriented family

The map `T(u)=v` is induced by the invertible linear map with matrix `[[0,-A],[B,0]]` followed by positive radial normalization. Its determinant is `AB>0`. Therefore it preserves orientation on the unit circle; explicitly its angular derivative is `AB/δ²>0`.

Direct calculation gives

```
|v|²=1,
det(u,v)=U/δ>0,
u·v=(B-A)cd/δ,
δ(Tu)=AB/δ,
T²u=-u.
```

The final equality uses the positive square root for the next normalization; this sign is justified by `A,B,δ>0`. Consequently `P,Q,-P,-Q` is a continuous family of counterclockwise convex parallelograms. It has four distinct vertices: `det(P,Q)=abU/δ>0`. Returning after one or two steps is impossible because the first two vertices are linearly independent and `T²u=-u≠u`; period three would imply period one for this four-step map. Thus each orbit has primitive period four. No repeated traversal or phase endpoint degeneration is being used.

The chord `PQ` has a normal and support-line value

```
n = (b(d-Bc/δ), -a(c+Ad/δ)),
n·P = -abU/δ ≠0.
```

Using `δ²+AB=SU`, independently expanding the support square yields

```
(A²/S)n_x²+(B²/S)n_y² = (n·P)².
```

Indeed the inner bracket after removing the common factor is

```
A(δd-Bc)²+B(δc+Ad)² = U(δ²+AB)=SU².
```

The mixed terms cancel exactly. This is the support criterion for tangency to the fixed caustic. Applying the same identity at successive iterates of `T` verifies every side. The contact lies strictly inside the chord: it belongs to the inner ellipse, which is strictly inside the outer ellipse, and the intersection of the supporting line with the outer filled ellipse is precisely the segment joining its two distinct chord endpoints. Thus the polygon uses actual tangent segments, not an extraneous extension of a chord.

### Billiard reflection, with signs checked

For an arbitrary unit line direction `w=(w_x,w_y)` through a point `P=(x,y)` of the outer ellipse, tangency to the caustic is equivalent to

```
(P×w)²=(A-λ)w_y²+(B-λ)w_x².
```

Expanding this equation with `x²/A+y²/B=1` and `|w|=1` gives exactly

```
(xw_x/A+yw_y/B)² = λ/(AB) = 1/S.
```

Let `m=(x/A,y/B)` be the outward normal. Any direction from `P` toward a distinct point of the outer ellipse has `m·w<0`: in normalized coordinates this is the strict inequality `u·v-1<0`, divided by the positive chord length. Both inward directions along the two tangent chords therefore satisfy `m·w=-1/√S`. After resolving each unit direction along the normalized normal and tangent, they have the same negative normal component and opposite tangent components. The tangent components are nonzero because `S|m|²>1`, equivalently `δ²>0`. The two inward rays are reflected in the normal line. The actual incoming velocity is the reverse of one inward ray; reflecting it in the tangent line gives the other outgoing velocity. This establishes the ordinary billiard law and avoids confusing normal-line ray symmetry with reflection of the incoming velocity.

This also confirms that the common caustic family is one oriented continuous billiard family. At `(c,d)=(1,0)` it is the axis diamond; at `(c,d)=(a/√S,b/√S)` it is the stated rectangle. The two representatives are connected by phases in the same family.

## 3. Complete area and angle formula, derived independently

This formula checks the whole claimed family, including phases away from the two symmetric representatives. It is an additional consistency result, with no historical-priority or novelty assertion.

Set `e=u·v`, `k=det(u,v)=U/δ`. Then `e²+k²=1` and `k>0`, so `|e|<1`. There are no parallel consecutive outer tangents. In normalized coordinates their successive intersections are

```
w1=(u+v)/(1+e),  w2=(v-u)/(1-e),  -w1, -w2.
```

The first point satisfies `u·w1=v·w1=1`, and the second satisfies `v·w2=(-u)·w2=1`. Their determinant is `2/k>0`; hence the signed outer area and orbit area are both positive. Scaling back by `diag(a,b)` gives

```
A_orbit = 2ab U/δ,
A_outer = 4ab δ/U,
A_outer/A_orbit = 2δ²/U²,
A_orbit A_outer = 8a²b².
```

At `P`, `|m|²=U/(AB)`. If the angle between the two inward rays is the interior angle `θ_P`, its bisector is the inward normal and its half-angle sine satisfies

```
sin²(θ_P/2) = 1-1/(S|m|²) = δ²/(SU).
```

At `Q`, `|m_Q|²=U/δ²`, so

```
sin²(θ_Q/2)=AB/(SU).
```

The angles lie strictly in `(0,π)`, and opposite angles agree. Thus all square-root signs and the product are unambiguous:

```
H := product sin(θ_i/2) = AB δ²/(S²U²),
K := (A_outer/A_orbit) H = 2AB δ⁴/(S²U⁴).
```

These formulas give exactly

```
K_diamond = 2AB/S²,
K_rectangle = S²/(8AB).
```

For `a>b`, `S²>4AB`, so the first is strictly below `1/2` and the second is strictly above `1/2`. For `a=4,b=3`, the values are `288/625` and `625/1152` and their difference is `58849/720000>0`. These exact values match the submission.

The complete quotient formula is

```
(A_outer/A_orbit)/H = 2S²/(AB).
```

It therefore is constant throughout this period-four family. This supports a possible source-table product/quotient diagnosis; it does not identify the intended all-period replacement or prove a general invariant for other even periods.

### Exact range as a falsification check

The two decompositions

```
δ²-U²=(A-B)²c²d² ≥0,
S²U²-4ABδ²=(A-B)²(Ad²-Bc²)² ≥0
```

give `1≤δ²/U²≤S²/(4AB)`. The bounds are attained at the axis and rectangle phases, respectively. Continuity then gives the complete range

```
2AB/S² ≤ K ≤ S²/(8AB).
```

This excludes an accidental equality at a nongeneric chosen pair. The quantity genuinely varies over one fixed period-four family.

As a separate geometric consistency check, with the two alternating side lengths `l_-`, `l_+`, their product is `S U²/δ²` and their sum is `2√S`; the perimeter is therefore `4√S` throughout the family. Neither this perimeter identity nor a prior area-product theorem is a proof dependency of the refutation.

## 4. Boundary and limiting cases

Axis phases `c=0` or `d=0` are regular members: all positive denominators remain nonzero, all vertices remain distinct, and consecutive tangent intersections are finite. Negative phases are handled without selecting a quadrant; all decisive quantities use squares and the positive determinant remains positive. The phase parametrization has no boundary gap at `2π`.

As `a→b>0`, the map tends to a quarter-turn, the caustic becomes the concentric circle of radius `a/√2`, and all orbits become squares. The complete range of `K` collapses to `1/2`. Hence the circular limit correctly loses the counterexample rather than contradicting the proof, whose strict separation uses `a>b`.

As `b→0` with `a` fixed, the inner ellipse and billiard table degenerate, so this limiting object is outside the hypotheses. Within every nondegenerate ellipse all inequalities are valid. The two symmetric values behave differently: `K_diamond→0` and `K_rectangle→+∞`; the rectangle phase depends on `b` and approaches an axis phase. For a fixed phase with `d≠0`, `K→0`. Thus this limit is nonuniform in phase, as expected, and is not evidence of a hidden finite-parameter pole. At `b=0` the normalization can vanish at an axis; that excluded endpoint cannot be substituted into the family formula.

## 5. Reproduction and negative controls

`independent_symbolic_check.py` contains 28 independently formulated exact polynomial identities checked with SymPy 1.14.0; every remainder is zero modulo the two defining constraints. A separate Gröbner calculation verifies the general unit-direction reflection identity. These are algebra diagnostics supporting the geometric proof above, not numerical evidence substituting for the proof. Execution succeeded normally and with Python optimization enabled, and the script uses explicit failures instead of optimized-away assertions.

The exact negative controls reject constancy of the printed product (`58849/720000`) and reject an incorrectly swapped-axis support line (residual `49/144`). A convention-sensitivity control shows that replacing the specified area ratio by its reciprocal makes both symmetric representatives agree (`72/625`); the paper therefore must keep the supplied `A'/A` convention clear. No source convention has been silently changed in this review.

No mandatory mathematical finding remains in this assigned scope. Historical priority, authoritative source/version matching, the full verification package, and the final paper remain responsibilities of the root audit and its fresh whole-package reviews.
