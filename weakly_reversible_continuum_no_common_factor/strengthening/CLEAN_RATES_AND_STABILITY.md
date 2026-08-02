# Clean integer rates and transverse stability

This note records two independent exact strengthenings.  It does not modify
the original construction or its verifier.  Every claim below is replayed by
`clean_rates_stability_verifier.py` using rational arithmetic.

## 1. A much smaller primitive integer rate vector

Rates are ordered by the ten reversible pairs in `network.csv`, forward then
reverse.  The following positive integer vector preserves the same conic:

```text
(1160, 10296, 976, 23, 560, 5977, 1800, 25, 1629, 1237,
 1, 9152, 653, 1214, 5368, 1, 5368, 70, 6039, 915).
```

It is primitive, has maximum entry `10296`, and has sum `52464`.  The original
vector has maximum entry `7732494` and sum `39165070`.

The resulting field is

\[
\begin{aligned}
F_1={}&-4697x^3+6039x^2y-9177xyz-5977xy+10736xz\\
 &+1960z^3+1800z+560,\\
F_2={}&915x^3-6039x^2y-9177xyz-5977xy-3782y^3\\
 &+10736yz+4888z^3+1800z+3488,\\
F_3={}&3712x^3+18304xyz-5368xz+3712y^3-5368yz\\
 &-6848z^3-10296z+1160.
\end{aligned}
\]

Exact checks prove

- every rate is positive;
- each coordinate belongs to the original conic ideal \((L,Q)\);
- \(\gcd(F_1,F_2,F_3)=1\) over \(\mathbb Q[x,y,z]\);
- the Jacobian has rank two at \((3/2,1/2,1)\); and
- the steady ideal is again radical and is the intersection of the conic
  prime with a disjoint degree-15 maximal ideal over \(\mathbb Q\).  Over an
  algebraic closure the latter contributes fifteen reduced points.

### Exact fixed-support optimality

Let \(k_0,\ldots,k_{19}\) denote the directed rates in the ordering above.
The conic-preservation matrix has rank 16 and nullity 4.  Taking

\[
  (a,b,c,d)=(k_{12},k_{15},k_{17},k_{19}),
\]

all its solutions are

\[
\begin{split}
k={}&(-5c/16+31d/24,
-297c/32+957d/80,
16d/15,
-b/3+c/3,\\
&-221c/224+11d/16,
-221c/98+704d/105,
-9945c/3136+495d/224,
5c/14,\\
&a+16d/15,
-b/3-c/3+62d/45,
-3a-221c/64+77d/32,
-33c/4+319d/30,\\
&a,
-2c/3+62d/45,
88d/15,
b,
88d/15,
c,
33d/5,
d).
\end{split}
\]

The clean vector is obtained from \((a,b,c,d)=(653,1,70,915)\).

There is also a bounded exact optimality certificate: among all positive
integral vectors in this fixed-support family, this vector simultaneously
attains the smallest possible maximum entry and the smallest possible sum.
Indeed, integrality forces \(15\mid d\) and \(14\mid c\).  A competitor with
maximum below 10296 must have \(d<1755\), because \(k_{14}=88d/15\).  A
competitor with sum below 52464 must have \(d<2714\), because

\[
  k_{14}+k_{16}+k_{18}+k_{19}=58d/3.
\]

The verifier exhausts these two finite ranges using the displayed exact
formulas.  This is fixed-support integer-height optimality, not a claim of
global network minimality.  Multiplying all rational rates by a common scalar
only rescales time, which is why the primitive integer normalization is used.

## 2. Transverse stability of the original ellipse

This section concerns the original published rates.  Put

\[
d(t)=t^2-t+1,
\qquad
(x(t),y(t),z(t))=
\left(\frac{t^2+3}{2d},\frac{3t^2+1}{2d},
\frac{t^2+t+1}{d}\right).
\]

The Jacobian has one zero eigenvalue tangent to the equilibrium curve.  If
\(\lambda_1,\lambda_2\) are the two transverse eigenvalues, exact calculation
gives

\[
\lambda_1+\lambda_2=
-\frac{8T(t)}{d(t)^2},
\]

where

\[
T(t)=5399367t^4+1602005t^3+11579010t^2+1602005t+6979911,
\]

and

\[
\lambda_1\lambda_2=-\frac{6272N(t)}{d(t)^4},
\]

where

\[
\begin{aligned}
N(t)={}&5730530769t^8+20026244073t^7+29613209084t^6\\
&+118245415239t^5-38238695578t^4+127692520263t^3\\
&-127590858244t^2+10579139049t-79465564719.
\end{aligned}
\]

Sturm counts prove that \(T\) is positive on the real line.  The transverse
discriminant is

\[
(\lambda_1-\lambda_2)^2=\frac{64E(t)}{d(t)^4},
\]

with

\[
\begin{aligned}
E(t)={}&31399532062137t^8+25149913538286t^7
+139213446954293t^6\\
&+100751092465458t^5+199590946186248t^4
+109518436416306t^3\\
&+114191722124597t^2+26510727150318t+17568656198073,
\end{aligned}
\]

and a second Sturm count proves \(E(t)>0\) for every real \(t\).  Thus the
transverse eigenvalues are always real and distinct.

The polynomial \(N\) has exactly two real roots.  Define them exactly by

\[
  \alpha\in(-4,-3),\qquad \beta\in(9/10,1),
\]

with \(N(\alpha)=N(\beta)=0\).  Numerically, only for orientation,
\(\alpha\approx-3.8135049145\) and \(\beta\approx0.9130496953\).  Since the
trace is strictly negative, the full classification is:

- for \(\alpha<t<\beta\), both transverse eigenvalues are negative, so the
  ellipse is normally attracting;
- for \(t<\alpha\) or \(t>\beta\), their product is negative, so the ellipse
  is transversely saddle-type;
- at \(t=\alpha,\beta\), one transverse eigenvalue vanishes and normal
  hyperbolicity is lost.

The rational parametrization covers the ellipse except for its limit point at
\(t=\infty\), which is also saddle-type.  On the interval \((-1,1)\) used in
the original theorem, the normally attracting part is \((-1,\beta)\), the
point \(\beta\) is nonhyperbolic, and \((\beta,1)\) is saddle-type.

## Reproduction

From the repository root, run:

```sh
.venv/bin/python weakly_reversible_continuum_no_common_factor/strengthening/clean_rates_stability_verifier.py
```
