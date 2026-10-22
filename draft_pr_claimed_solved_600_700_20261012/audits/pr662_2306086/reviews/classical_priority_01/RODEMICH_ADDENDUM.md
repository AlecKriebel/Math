# New-source addendum: the recovered Rodemich argument bound

UTC date: 2026-10-15. Same PR 662 head `e31701151c331a6eed9224fb37a75a374ea1043e`. This addendum supersedes ONLY the earlier report's Rodemich source-access/formula gap. It does not erase the fact that my direct publisher retrievals failed. The earlier verdict and source bindings are preserved as `*.before_rodemich_addendum.json` and bound by `ADDENDUM_PRIOR_REVIEW_BINDING.json`.

## 1. Exact primary evidence

The full January 1979 AMS Notices issue was recovered by a separate source-access effort using an actual dated archive snapshot. I independently hashed all 39,063,095 bytes, obtaining SHA-256 `04df2b98e61313f7afb1da73329dc536237ce6d8c0f7431a9409991f693a64a0`, and visually read the complete original printed A-68. The page image has SHA-256 `e34277d4568410e77050da1ad2291be073cb37638eccc7a3d8c4bcb685c08a68`.

Primary archive URL: https://web.archive.org/web/20220620050040id_/https://www.ams.org/journals/notices/197901/197901FullIssue.pdf

Rodemich's abstract 763-30-11, received 1978-10-20, concerns normalized real-coefficient univalent functions. Its announced inequality is

    |arg((1-z^2) f'(z))| <= B(q),
    q = |z-conjugate(z)|/(1-|z|^2),

    B(q) = 2 arctan(q),              0 <= q <= 1,
           pi/2 + log(q),            q > 1.

The recovered quantity is an argument of a first derivative times a factor. It is not the pre-Schwarzian or its modulus. The short announcement supplies no proof, sharpness statement, equality classification, or further pre-Schwarzian conclusion on that page. No other family reports were read for this addendum.

## 2. Correct coordinate and derivative relation

Set

    w = log((1+z)/(1-z)),  z = tanh(w/2),
    |Im w| < pi/2.

This is the conformal disk-to-horizontal-strip correspondence with w(0)=0. For w=x+iv the Cayley transform has argument v, and direct calculation of its real and imaginary parts gives

    q = tan(|v|).

For a real normalized locally univalent function choose the logarithm

    h(w) = log((1-z^2) f'(z)),  h(0)=0.

It is analytic on the strip. Rodemich's bound, in this stronger continuous-argument interpretation, is

    |Im h(x+iv)| <= b(|v|),
    b(v) = 2v,                         0 <= v <= pi/4,
           pi/2 + log(tan v),          pi/4 < v < pi/2.

At w=iv, let t=tan(v/2), so z=it. The logarithmic derivative identity is

    f''(z)/f'(z) = 2(h'(w)+z)/(1-z^2).

Therefore the target quantity satisfies the exact relation

    A_f(it) = 2 cos(v) h'(iv) + 2i sin(v).                 (A)

A bound on Im h is not a bound on h' obtained by differentiating the numerical envelope. In particular, equality/inequality information for an analytic function and its derivative has different content.

## 3. Exact countermodel to the naive implication

The following construction proves that the announced argument envelope, even together with normalization, reality, and a nonvanishing analytic derivative, does not imply even the universal bound |A|<=4. It does NOT belong to the globally univalent target class and is NOT a counterexample to PR 662.

Let

    a = 10 exp(-50 pi),
    h(w) = a sin(100 w),
    f'(z) = exp(h(log((1+z)/(1-z))))/(1-z^2),
    f(z) = integral_0^z f'(zeta) d zeta.

The derivative is analytic and never zero in the disk. The integral is path-independent there, f(0)=0, f'(0)=1, and the reflection identity holds; hence f has real Taylor coefficients and is locally univalent. The analytic logarithm of (1-z^2)f'(z), normalized at zero, is exactly h(w).

For any x real and 0<=v<pi/2,

    |Im h(x+iv)| <= a sinh(100v).

We prove a sinh(100v)<=b(v) over the full interval.

### Central part: 0<=v<=pi/4

The quotient sinh(100v)/v is increasing for v>0, as its power series has nonnegative coefficients. At the right endpoint,

    a sinh(25pi) < 5 exp(-25pi) < 1 < pi/2.

Dividing this endpoint inequality by pi/4 and using monotonicity gives a sinh(100v)<2v for 0<v<=pi/4. At v=0 both sides vanish.

### Outer part: pi/4<=v<pi/2

Put u=pi/2-v, with 0<u<=pi/4. Since cos u>=1/2 and sin u<=u,

    cot u >= 1/(2u),
    b(v) >= pi/2 + log(1/(2u)).

Also

    a sinh(100v) < 5 exp(-100u).

Three elementary intervals establish the comparison:

* If 0<u<=1/100, then b(v)>=pi/2+log50>5, while 5exp(-100u)<=5. Here pi>3 and log50>7/2 suffice: e<3 and sqrt3<7/4 give e^(7/2)<27sqrt3<189/4<50.
* If 1/100<=u<=1/10, then b(v)>=pi/2+log5>5/2, while 5exp(-100u)<=5/e<2, using e>5/2.
* If 1/10<=u<=pi/4, then b(v)>=pi/2>1, while 5exp(-100u)<=5/e^10<1.

Thus this f satisfies the full continuous-argument version of the recovered bound everywhere. If arg in the announcement is instead read as the principal argument, its absolute value is at most the absolute value of this continuous argument, so the construction still satisfies it.

### Failure of the pre-Schwarzian bound at an interior point

Choose

    v = pi/2 - 1/100,
    t = tan(v/2) in (0,1),
    z = it.

Then

    h'(iv) = 1000 exp(-50pi) cosh(50pi-1)
            = 500[exp(-1)+exp(1-100pi)] > 500/e.

Moreover cos v=sin(1/100)>99/10000 and e<11/4. Hence

    cos(v) h'(iv) > (99/10000)(500)/(11/4) = 9/5.

Also sin v=cos(1/100)>9/10. Since h'(iv) is real, equation (A) gives

    |A_f(it)|^2
       = 4[cos(v)^2 h'(iv)^2 + sin(v)^2]
       > 4[(9/5)^2 + (9/10)^2]
       = 81/5 > 16.

All inequalities here are exact. For example sin x>=x-x^3/6 and cos x>=1-x^2/2 at x=1/100 justify the rational trigonometric bounds, and elementary exponential-series estimates give 5/2<e<11/4. The accompanying controls check these rational margins; a floating-point value is illustrative only.

The construction cannot be globally univalent because it violates the universal coefficient-derived pre-Schwarzian inequality at this explicit point. Global univalence is precisely the extra hypothesis deliberately not asserted in this countermodel.

## 4. Implication and priority disposition

The exact functional is now identified, so Rodemich is an established related result, not an inaccessible mystery. It is appropriate context for a narrowly framed note on real-coefficient distortion.

The construction rules out the tempting claim that differentiating, or otherwise using only the displayed argument envelope with local analytic normalizations, already supplies the target derivative bound. It does not prove that no ingenious use of Rodemich together with global univalence could yield a target estimate. Such a universal impossibility claim is neither needed nor established.

With global univalence and the classical coefficient equality classification, the target is already rigorously obtainable by the real-symmetry/compactness application in `DERIVATION.md`. Adding Rodemich to those premises does not supply a separate earlier statement of that application. No quantitative improvement or pre-Schwarzian equality classification was extracted from the recovered announcement itself, and no such claim is attributed to it.

Accordingly the family verdict remains: **no positive prior target overlap verified; no historical-firstness or exhaustive-novelty certificate**. The Rodemich formula/access gap is closed, while Jenkins 1960 derivative-bound formulas remain an exact unresolved priority lead. All scope restrictions in the earlier verdict remain in force. No native repair, publication, closure, remote mutation, or external outreach was performed.
