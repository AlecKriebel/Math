# Independent reconstruction from the original problem

## Scope, independence, and source

This report was derived without reading the submitted proof, current edition,
candidate summaries, or other reviewers' work. The only mathematical inputs were
the original-problem JSON and Hayman--Lingham, arXiv:1809.07200v2. The source PDF
has SHA-256 `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`
and 1,706,228 bytes. I inspected PDF page 184 visually; its printed page is 183.
PDF page 185, printed 184, is not the location of Problem 7.72.

The exact relevant conventions are area measure, the kernel with coefficient
minus `1/pi`, and the **bilinear** pairing `integral(v phi)`: there is no
complex conjugate on the analytic test function. The tests include every
integrable holomorphic function on the disc. The target asks both essential
boundedness on this annihilator and one uniform norm estimate; the polynomial
subquestion retains that uniformity. No priority search was performed in this
source-only stage, and this report makes no claim of novelty or current openness.

## Result

Both proposed uniform bounds fail. In fact, a single bounded annihilator element
has an essentially unbounded transform. There is also an explicit unit-norm
polynomial sequence whose transform norms are exactly the harmonic numbers.
The proof below uses elementary angular integration and the Cauchy potential,
rather than any estimate whose conclusion presupposes the disputed bound.

Write `U={|z|<1}`, `dA=dx dy`, and extend every input by zero outside `U` when
considering it on the plane. Define, with an arbitrary value at the origin,

    v(re^{i theta}) = e^{2i theta},  0<r<1.

For each integer `m>=1`, define the genuine polynomial in `z` and `bar z`

    v_m(z) = z^2 sum_{j=0}^{m-1} (1-z bar z)^j.

Equivalently, away from zero, putting `t=r^2`,

    v_m(re^{i theta}) = e^{2i theta} F_m(t),
    F_m(t) = 1-(1-t)^m.

Then

    ||v||_infinity = ||v_m||_infinity = 1,
    v,v_m belong to N,
    Bv(re^{i theta}) = 1+2 log r       (0<r<1),
    ||Bv_m||_infinity = H_m = sum_{j=1}^m 1/j.

The transform norms can be read on the disc or on the plane with zero-extended
inputs: outside the closed disc the transforms vanish, and the boundary circle
has area zero. Thus the conclusion does not depend on this possible ambiguity.

## Annihilation of all integrable holomorphic tests

More generally, let `a` be any bounded measurable radial function on `(0,1)` and
put `w(re^{i theta})=e^{2i theta}a(r)`. For every radius `r<1` and holomorphic
`phi` on `U`, its Taylor series is uniformly convergent on that circle. Every
term in `e^{2i theta}phi(re^{i theta})` has a strictly positive angular frequency.
Consequently its angular integral is zero. If `phi` is integrable on `U`, then
`|w phi| <= ||a||_infinity |phi|` is integrable, so Fubini's theorem applies to
the polar-coordinate integral and proves `integral_U w phi dA=0`.

This checks the original full analytic-L1 condition directly. It is not an
argument that merely checks monomials and leaves density in analytic L1
unsupported. It also explains why accidentally replacing the bilinear pairing
by a Hermitian pairing would change the problem and invalidate this example.
Taking `a=1` and `a(r)=F_m(r^2)` gives the required membership statements.

On `0<t<1`, `0<F_m(t)<1`, and it increases to 1 as `t` tends to 1. Annuli of
positive area therefore show that the essential input norm is exactly 1, even
though the supremum 1 need not be attained at an interior point.

## Angular computation of the Cauchy potential

For bounded `a`, set

    Cw(z) = (1/pi) integral_U w(zeta)/(z-zeta) dA(zeta).

This integral is absolutely convergent for each `z`: the local singularity has
order `|z-zeta|^{-1}`, which is area-integrable. Fix `0<|z|=r<1`. On circles
`rho<r`, expand the denominator in powers of `rho e^{i theta}/z`; all angular
integrals vanish after multiplication by `e^{2i theta}`. On circles `rho>r`,

    1/(z-rho e^{i theta})
      = -sum_{k>=0} z^k rho^{-k-1} e^{-i(k+1)theta}.

Exactly the term `k=1` survives. Each expansion is used at a fixed radius away
from `rho=r`, where it converges uniformly in angle. The omitted single radius
has radial measure zero, and absolute integrability of the original two-variable
integral justifies Fubini. It follows that

    Cw(z) = -2 z integral_r^1 a(rho)/rho d rho.             (1)

For `|z|>1`, expanding in `zeta/z` instead gives zero. At zero direct angular
integration gives zero as well. For the two present families the expression in
(1) tends to zero at the unit circle, consistently with the exterior expression.

If `a` is continuously differentiable near a fixed positive radius, Wirtinger
differentiation of (1) gives

    partial Cw(z)
       = a(r) - 2 integral_r^1 a(rho)/rho d rho,           (2)
    barpartial Cw(z) = e^{2i theta} a(r).

Here `partial=(partial_x-i partial_y)/2` and
`barpartial=(partial_x+i partial_y)/2`; in particular `partial r=bar z/(2r)`.
These identities independently fix both the sign and the factor of two.

## Principal values and exceptional sets

For completeness, differentiating the Cauchy potential in the sense of
distributions uses

    partial[1/(pi z)] = -(1/pi) PV(1/z^2).

This identity follows by integration by parts on `|z|>epsilon`: the inner
boundary's order-zero term has angular frequency two and integrates to zero;
the remaining boundary terms tend to zero for a smooth compactly supported
test function after its first-order Taylor subtraction. Equivalently, local
subtraction of a constant from the numerator leaves an absolutely integrable
kernel when the input is continuously differentiable near the evaluation point.
It therefore identifies (2) with the **circular Cauchy principal value** in the
original problem at every point where the input is locally continuously
differentiable. For `v`, this includes all `0<|z|<1`; for `v_m`, it includes the
entire open disc.

There is no hidden distribution supported at the origin or unit circle in the
potential formula. For `v`, `Cv(z)=2z log|z|` inside, which tends to zero at zero
and has locally integrable logarithmic first derivatives. Its boundary term on
a circle of radius `epsilon` is bounded by a constant times
`epsilon^2 |log epsilon|`, tending to zero. At the unit circle the inside and
outside potential traces both vanish, so its first distributional derivative
has no jump measure. Polynomial inputs have no origin singularity at all.

Taking `a=1` in (2) proves `Bv=1+2log r` on the punctured disc. At zero the
truncated transform is `-2 log(1/epsilon)`, so that particular principal value
does not exist finitely. This is one point only. The negative answer does not
rest on it: for every `M>0`, sufficiently small punctured discs, each of positive
area, have `Bv<-M`. Thus the transform is not essentially bounded even on `U`.

The same mechanism can be confined away from the boundary: fix `0<R<1` and
replace `a` by the indicator of `(0,R)`. The resulting unit-norm element of `N`
is supported in `|z|<=R`, its transform is `1+2log(r/R)` on `0<r<R`, and its
transform vanishes on `R<r`. The circle `r=R` and the origin are irrelevant null
sets for this conclusion. Thus boundary discontinuity of the unit-disc zero
extension is not the cause of the essential unboundedness near the origin.

## Polynomial subquestion and exact norm

Changing variables `t=r^2`, equation (2) becomes

    Bv_m(z) = F_m(t) - integral_t^1 F_m(u)/u du.          (3)

Since `F_m(0)=0`, its quotient by `u` is a polynomial; (3) is a polynomial in
`t=z bar z`, hence is continuous at zero. Direct integration at zero agrees:

    Bv_m(0)
      = -integral_0^1 [1-(1-u)^m]/u du
      = -integral_0^1 sum_{j=0}^{m-1}(1-u)^j du
      = -H_m.                                         (4)

The original singular integrand at zero is actually nonsingular for these
inputs, because `v_m(zeta)/zeta^2=sum_{j=0}^{m-1}(1-|zeta|^2)^j`.
For `0<t<1`, differentiating the real radial output in (3) gives

    d(Bv_m)/dt = m(1-t)^{m-1} + F_m(t)/t > 0.

Its endpoint limits are `-H_m` at zero and 1 at one. It follows that the
essential supremum of its absolute value is exactly `H_m` (also for `m=1`).
Continuity on small discs, rather than the value at a single point alone,
ensures this is an essential-norm lower bound. Since `H_m>=log(m+1)` diverges,
no finite constant works uniformly on the polynomial subclass.

Each individual polynomial in this displayed sequence has a bounded transform.
The sequence disproves the polynomial *uniform estimate*, which is the weaker
question asked in context; it does not claim an individual polynomial has an
unbounded transform. The nonpolynomial `v` separately disproves the stronger
membership statement. For every fixed `0<r<1`, (3) also tends to `1+2log r`,
consistent with the singular example, but this limiting observation is not
needed to prove either failure.

## Verification and limits

`check_polynomials.py` uses exact rational arithmetic, independently constructs
`v_m`, integrates its radial polynomial, verifies (3)--(4), verifies the
polynomial Cauchy-potential derivatives coefficient by coefficient, checks the
moment/angular mechanism, and tests that a genuinely false certificate is
rejected under normal Python, `-O`, and `-OO`. The checks are finite corroboration;
the proofs above cover every integer `m>=1` and every analytic-L1 test function.

No unresolved mathematical gap was found for these counterexamples under the
original stated conventions. This source-only result does **not** certify any
unread candidate's files, publication artifacts, historical priority, or novelty.
