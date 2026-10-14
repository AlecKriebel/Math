# Proof 27  An exact exterior ellipse barrier and stability bound

Included dependencies: [Exact one phase integration of the entropy kernel](14_one_phase_entropy.md); [Dominant endpoint entropy and nearby power comparisons](17_dominant_endpoint_entropy.md).

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

## 1. Exact nonnegative remainder outside the root ellipse

Let `a>0`, let `b` be real with `|b|<=a`, and let `Z` be uniform on the unit circle. Define

`F_ab(w)=E K(aZ+b/Z+w)`, `K(z)=|z|^2 log|z|`, `K(0)=0`,

and the quadratic polynomial

`Q_ab(w)=(a^2+b^2+|w|^2)log a+|w|^2+b^2+(b/(2a)) Re(w^2)`.

Then

`F_ab(w)=Q_ab(w)+B_ab(w)`, with `B_ab(w)>=0`.                         (1)

If both roots of `az^2+wz+b` lie in the closed unit disk, `B_ab(w)=0`. Otherwise exactly one root has modulus greater than one. Write that root as

`lambda=R exp(it)`, `R>1`, `x=R^2`, `q=b/a`.

The other root is `q/lambda`, and

`B_ab(w)=a^2 [(1+q^2/x) f(x)-q cos(2t) g(x)]`,                       (2)

where, for `x>=1`,

`f(x)=((x+1)/2)log x+1-x`,

`g(x)=(x-x^(-1))/2-log x`.

This includes the degenerate choices `b=0` and `|b|=a`. At a unit-circle transition the formula joins continuously to zero.

### Derivation

The product of the two roots is `q`, so at most one root has modulus greater than one. When there is none, the one-phase formula in [Proof 14](14_one_phase_entropy.md) is exactly `Q_ab`.

When an exterior root `lambda` exists, the accepted formula uses

`L0=log a+log R`,

`T1=q/lambda+1/conjugate(lambda)`,

`T2=q^2/lambda^2+1/conjugate(lambda)^2`,

and `w=-a(lambda+q/lambda)`. Substitute these quantities into

`F_ab(w)=(a^2+b^2+|w|^2)L0-Re[(a conjugate(w)+b w)T1]-(ab/2)Re(T2)`.

After subtracting `Q_ab`, the result divided by `a^2` is

`[(1+x)+q^2(1+x^(-1))+2q cos(2t)](log x)/2`

`+(1-x)(1+q^2/x)-(q/2)(x-x^(-1))cos(2t)`,

which is (2). Thus the reduction is algebraic and keeps root transitions explicit.

### Nonnegativity

For `x>=1`,

`f(1)=f'(1)=0`, `f''(x)=(x-1)/(2x^2)>=0`,

`g(1)=0`, `g'(x)=(x-1)^2/(2x^2)>=0`.

Also

`(1+x^(-1)) f(x)-g(x)>=0`.                                         (3)

To check (3), put `u=log x>=0`; its left side is

`u(cosh u+2)-3 sinh u`.

Its power series is

`sum_(n>=2) (2n-2) u^(2n+1)/(2n+1)!>=0`.

Let `q0=|q|<=1`. Since `|cos(2t)|<=1`, (2) is bounded below by

`a^2 [(1+q0^2/x)f(x)-q0 g(x)]`

`=a^2 [(1-q0)(1-q0/x)f(x)+q0((1+x^(-1))f(x)-g(x))]>=0`.

This proves (1). Nonnegativity of the individual barriers does **not** imply nonnegativity of their difference under sign changes.

## 2. Uniform cubic bound for the exterior remainder

Suppose `|w|<=M`. An exterior root obeys

`a R^2=|w lambda+b|<=M R+|b|`,

and therefore

`R<=L=(M+sqrt(M^2+4a|b|))/(2a)`.

For `x>=1`, the preceding derivative formulas give the elementary bounds

`0<=f(x)<= (x-1)^3/12`,

`0<=g(x)<= (x-1)^3/6`.

Consequently

`0<=B_ab(w)<=((a+|b|)^2/12) [(L^2-1)_+]^3`,                       (4)

where `t_+=max(t,0)`. If `L<=1`, no exterior root exists and the right side is zero. If `L>1`, use `1+q^2/x<=1+q^2`, `|q cos(2t)|<=|q|`, and (2) to obtain (4). This bound is deliberately elementary, rather than an assertion that the worst angle or largest permitted root is attained by a given coefficient array.

A convenient rational version avoids the square root: if `L0>=1` and

`M<=a L0-|b|/L0`,

then the right side of (4) may be replaced by

`((a+|b|)^2/12)(L0^2-1)^3`.                                       (5)

Indeed the positive root of `aR^2-MR-|b|=0` is then at most `L0`.

## 3. General centered-cross residual identity and sufficient comparison

Let

`U=c+sum_(j=0)^(n-1)(a_j Z_j+b_j/Z_j)`,

`V=c+sum_(j=0)^(n-1)(a_j Z_j+s_j b_j/Z_j)`,

with nonnegative coefficients, independent uniform `Z_j`, and `s_j in {-1,+1}`. Let `Y` be independent bounded radial noise, `|Y|<=rho`. Choose one pair with `a=a_0>=b=b_0>=0` and `a>0`; phase reversal permits this ordering. Put

`M=c+sum_(j>=1)(a_j+b_j)+rho`,

`Delta=(b/(2a))[(1-s_0)c^2+2 sum_(j>=1)(1-s_0 s_j)a_j b_j]`.

The same orthogonality calculation as in the accepted dominant-endpoint theorem now gives the **unconditional exact residual identity**

`E K(U+Y)-E K(V+Y)`

`=Delta+E B_(a,b)(w_+)-E B_(a,s_0 b)(w_s)`,                        (6)

where

`w_+=c+sum_(j>=1)(a_j Z_j+b_j/Z_j)+Y`,

`w_s=c+sum_(j>=1)(a_j Z_j+s_j b_j/Z_j)+Y`.

Unlike the previous contained-root identity, (6) requires no dominance hypothesis. Its unresolved part is precisely the difference of the two exterior barriers.

Dropping the nonnegative first barrier and applying (4) to the second gives the rigorous lower bound

`E K(U+Y)-E K(V+Y)`

`>=Delta-((a+b)^2/12)[(L^2-1)_+]^3`,                             (7)

where `L=(M+sqrt(M^2+4ab))/(2a)`.

In particular, a nonnegative right side is a sufficient entropy/Green comparison certificate, and a strictly positive right side certifies a strict entropy gap. The rational condition (5) can be used instead. This applies to every centered-cross dimension and every sign pattern, uniformly over all radial noise laws with the prescribed support bound.

When `M<=a-b`, both exterior barriers vanish and (6) recovers the exact prior dominant-endpoint gap `Delta`. When `M>a-b` but the escape is small, (7) controls the possible adverse contribution by a cubic error. It does not assert that the true gap is monotone in `M`, `c`, or any coefficient.

## 4. Exact genuinely mixed example beyond root containment

Take

`a_0=4`, `b_0=1`, `a_1=1`, `b_1=1/2`, `c=1`,

and flip only pair zero. Both pairs have genuinely unequal nonzero endpoints. Then `Delta=1/2` and

`M=5/2+rho`.

Choose `L0=6/5`. Since

`a L0-b/L0=24/5-5/6=119/30`,

the rational bound applies for every radial noise law bounded by

`rho<=119/30-5/2=22/15`.

Its cubic error is

`((a+b)^2/12)(L0^2-1)^3=(25/12)(11/25)^3=1331/7500`.

Therefore the exact certified lower bound is

`E K(U+Y)-E K(V+Y)>=1/2-1331/7500=2419/7500>0`                    (8)

uniformly for `rho<=22/15`. The previous contained-root criterion only guaranteed `rho<=1/2` for this same coefficient array. Thus (8) genuinely enters the exterior-root regime. It still covers only a bounded noise-radius range, so it is not the full radial-bisubharmonic comparison.

The accepted Taylor argument converts any positive lower bound `eta` for the entropy gap into a prescribed near-two power interval. If `R_*` bounds both compared moduli, put `delta=eta/R_*^2`; then

`E|U+Y|^p>E|V+Y|^p` for `2<p<2+e^2 delta`.

For example, in (8), `R_*=1+5+3/2+22/15=269/30` is a common support bound, and one may take `delta=(2419/7500)/(269/30)^2`. No claim at every `2<p<3` follows from this quantitative interval.
