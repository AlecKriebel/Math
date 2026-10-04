# Different exceptional values at two Julia rays

## Claim, scope, and credit

The concrete existence question in Hayman–Lingham Problem 2.4 has an
**affirmative** answer. This was already recorded as solved by Toppila
(1970), with a later treatment by Barth and Schneider (1972); see
`SOURCE_GATE.md` for the verified attribution and its retrieval limits.
No new resolution or priority claim is made here.

This note gives a complete, directly checkable verification using the
classical error function. It does not claim that this is the construction
in either historical paper. The witness satisfies precisely the
whole-plane entire-function question; it does not settle a general
classification of exceptional values and directions.

For a nonconstant entire function F, call a finite value c exceptional at
angle theta if some open angular neighborhood of theta contains only
finitely many c-points. A Julia ray has the property that every open
angular neighborhood contains infinitely many points of every finite
value, with at most one finite exception. Infinity is automatically the
other exception in the meromorphic version of the definition. A point at
zero has no argument and never affects the infinite-preimage property.

**Theorem.** The function

\[
 f(z)=\operatorname{erf}z=\frac{2}{\sqrt\pi}\int_0^z e^{-t^2}\,dt
\]

has a Julia ray at angle pi/4 whose unique finite exceptional value is 1,
and a Julia ray at angle 3pi/4 whose unique finite exceptional value is -1.
Consequently, any prescribed distinct finite values a and b can occur at
these respective rays, using

\[
 F(z)=\frac{a+b}{2}+\frac{a-b}{2}f(z).
\]

The integral is path-independent because its integrand is entire. Its
primitive is entire, is odd, and satisfies

\[
 f(\overline z)=\overline{f(z)},\qquad
 f'(z)=\frac2{\sqrt\pi}e^{-z^2}.
\]

It is transcendental: its derivative is not a polynomial.

## 1. A uniform tail estimate proved directly

Define

\[
 I(z)=\int_0^\infty e^{-t^2-2zt}\,dt.
\]

This is entire in z. Indeed, on any compact set |z|<=M, the integrand and
each z-derivative are dominated by a constant times a polynomial in t
multiplied by exp(-t^2+2Mt), an integrable function. For real z>=0, the
usual real Gaussian integral and the substitution u=z+t give

\[
 1-f(z)=\frac2{\sqrt\pi}e^{-z^2}I(z).
\]

Both sides are entire, so the identity theorem extends this formula to
every complex z.

Let x=Re z>0. Integration by parts is legitimate on the positive real
integration path and its boundary term at infinity vanishes. It gives

\[
 I(z)=\frac1{2z}-\frac1z\int_0^\infty t e^{-t^2-2zt}\,dt.
\]

Thus, with

\[
 \delta(z)=-2\int_0^\infty t e^{-t^2-2zt}\,dt,
\]

we obtain the **exact** formula and error bound

\[
 1-f(z)=\frac{e^{-z^2}}{\sqrt\pi\,z}(1+\delta(z)),
 \qquad
 |\delta(z)|\le2\int_0^\infty t e^{-2xt}\,dt
 =\frac1{2x^2}.                                      \tag{1}
\]

No asymptotic expansion is being used outside its domain, and the bound
is uniform wherever x is bounded below by a positive multiple of |z|.

In the sector |arg z-pi/4|<pi/12, we have x>|z|/2. For |z|>2, (1) gives
|delta(z)|<1/2. The other factors in (1) are nonzero, so f(z) is not 1 in
this sector outside the disk of radius 2. There are only finitely many
1-points in the disk, because f-1 is a nonzero entire function and its
zeros are isolated. This proves that 1 really is exceptional at pi/4;
it is not merely an asymptotic value along one path.

Write omega=exp(i pi/4). At z=r omega, equation (1) implies

\[
 |1-f(r\omega)|\le\frac{1+r^{-2}}{\sqrt\pi\,r}
 \longrightarrow0.                                  \tag{2}
\]

Here Re z=r/sqrt(2) and |exp(-z^2)|=|exp(-i r^2)|=1.
At the same points the derivative has constant modulus

\[
 |f'(r\omega)|=\frac2{\sqrt\pi}.                       \tag{3}
\]

## 2. Every other finite value occurs infinitely often in every angle

Fix an arbitrary finite w different from 1. Suppose, toward a
contradiction, that there is an epsilon>0 such that the sector
|arg z-pi/4|<epsilon contains only finitely many w-points.

Shrink epsilon to a positive eta<min(epsilon,pi/12). By the preceding
paragraph, this smaller sector also contains only finitely many 1-points.
Choose R0 large enough that the tail sector

\[
 |\arg z-\pi/4|<\eta,\qquad |z|>R_0
\]

omits both values 1 and w.

Choose 0<d<min(1/2,eta/4). For |s|<d,

\[
 |1+s|>1-d>1/2,\qquad
 |\arg(1+s)|\le\arctan\frac{d}{1-d}<2d<\eta.
\]

Consequently, for every real R>2R0 the holomorphic function

\[
 h_R(s)=f(R\omega(1+s)),\qquad |s|<d,
\]

omits 1 and w throughout the fixed disk |s|<d. Montel's theorem for
holomorphic functions omitting two distinct finite values says that this
family is normal in the spherical metric. This standard foundational
normal-family theorem is the only non-elementary analytic theorem used
here; no entire-approximation theorem or numerical experiment is needed.

Take any sequence R_j tending to infinity. By normality it has a
subsequence for which h_(R_j) converges spherically on compact subsets to
a meromorphic function or identically infinity. Equation (2) shows that
the limit at s=0 is 1. The limit is therefore finite and holomorphic in
some neighborhood of zero. On a sufficiently small closed disk about
zero it is bounded. Uniform spherical convergence to a bounded finite
limit on that disk gives uniform Euclidean convergence there: the
images stay a positive spherical distance from infinity. Cauchy's
integral formula then implies that the derivatives at zero are bounded
(and converge) along this subsequence.

On the other hand, the chain rule and (3) give

\[
 |h_R'(0)|=R\,|f'(R\omega)|=\frac{2R}{\sqrt\pi}
 \longrightarrow\infty.                              \tag{4}
\]

This contradiction proves that the assumed sector cannot exist. Since w
was arbitrary, every w other than 1 has infinitely many distinct
preimages in every angular neighborhood of pi/4. Those preimages have
unbounded moduli by isolation of zeros on compact disks. This proves the
Julia property, including its full quantifiers and its unique finite
exceptional value.

Notice that this argument does not infer a Julia ray from an asymptotic
value alone: the simultaneous derivative growth (4) is essential.

## 3. The second ray and arbitrary exceptional values

The real Taylor coefficients and oddness give

\[
 f(-\overline z)=-\overline{f(z)}.                    \tag{5}
\]

The map z -> -conjugate(z) preserves modulus and sends angular
neighborhoods of pi/4 bijectively to the corresponding neighborhoods of
3pi/4. By (5), w-points in the latter correspond bijectively to
(-conjugate(w))-points in the former. The unique exceptional value at
3pi/4 is therefore -1; every other finite value occurs infinitely often
in each such neighborhood. These two rays are distinct even as
unoriented lines.

Finally, if a is different from b, the affine map
u -> (a+b)/2+(a-b)u/2 is bijective. It sends 1 to a and -1 to b and
preserves all finite-versus-infinite preimage statements. This establishes
the announced generalization and completes the proof.

## 4. What is and is not verified

The proof above is an explicit mathematical witness for the terminal
existence question. All estimates needed for this witness are derived
above. Montel's theorem, the Gaussian integral, the identity theorem,
and Cauchy's formula are standard external foundational results.

The historical Toppila and Barth–Schneider papers were identified but
their full texts were not recovered in this investigation. We therefore
do not claim to have checked their constructions. The prior-resolution
attribution is explicitly reported in Hayman–Lingham's update and in
Hwang's original 1977 follow-up, whose full two pages were read. Hwang's
asymptotic-values theorem is not used as if it were an exceptional-values
theorem. Gol'dberg's 1968 article and neighboring Problem 2.5 have different
quantifiers and are not substituted for the present claim.

The accompanying finite controls are supplementary algebra and numerical
sanity checks. They neither establish infinitely many preimages nor
certify the normal-family theorem. The analytic proof does those jobs.
The preparation was AI-assisted and is not human peer review or formal
proof-assistant certification.
