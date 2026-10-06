# Independent period and parameter audit of PR104 /600008

Completed 2026-10-06 UTC. Scope: mathematical falsification and verification of the preserved `ANALYTIC_CRITERION.md`, especially its period identity and factors. This audit reconstructed the branch, real periods, metric, and parameter argument before consulting any old review or another agent's findings. No old review was read. The GKT primary text was consulted afterward to check its definition of the equator map and invariant density. No mathematical novelty or historical priority is decided here. Original attempt 1/5 is unchanged; this audit consumed zero fresh central proof-search turns.

**Verdict: the stated analytic criterion passes this bounded independent mathematical audit.** No counterexample or substantive mathematical error was found. The result is conditional only on the explicitly stated positive axes and alternating reflected null-chain convention. It gives a necessary and sufficient integral condition, including all positive values of `c`; it does not supply or validate a finite algebraic Cayley condition.

The exact tested claim is that, with

\[
F(t)=a\sin^2t+b\cos^2t,\qquad
L=\int_0^{2\pi}\sqrt{F(t)/(c+F(t))}\,dt,
\]

the actual positively advancing lift of the equator-to-North-to-equator map has advance `2H` and rotation number

\[
\rho={2H\over L}={\pi\over L}-{1\over2}
={1-\mathcal M\over2\mathcal M},\qquad \mathcal M=L/(2\pi).
\]

This number is a lift-dependent real rotation number, which may exceed one; its reduction modulo one is the conventional circle rotation number. The candidate explicitly fixes the lift by the null path, so there is no normalization ambiguity in its winding statements.

## Checkable independent derivation

Assume initially `a>b>0,c>0`. For real `alpha<beta`, define on the cut plane

\[
s_{\alpha,\beta}(z)=(z-\beta)
\sqrt{\frac{z-\alpha}{z-\beta}},
\]

using the principal square root. The ratio avoids the nonpositive real axis exactly off `[alpha,beta]`, and this defines the analytic square root of `(z-alpha)(z-beta)` with `s~z` at infinity. Thus

\[
R=s_{-a,-b}s_{0,c}
\]

is a globally defined, nonvanishing holomorphic branch on the twice-cut plane, with `R~z^2`. Simply connectedness of that plane is unnecessary; the paired construction settles existence and normalization.

For `alpha<x<beta`, the upper-bank value of `s` is `+i sqrt((x-alpha)(beta-x))`; for `x<alpha` it is negative real and for `x>beta` positive real. Consequently the upper-bank values of `R` are

\[
\begin{array}{c|c|c}
\text{interval}&R(x+i0)& x/R(x+i0)\\
(-a,-b)&-i\sqrt{-P(x)}&-i\sqrt{\frac{x}{(a+x)(b+x)(c-x)}}\\
(0,c)&+i\sqrt{-P(x)}&-i\sqrt{\frac{x}{(a+x)(b+x)(c-x)}}
\end{array}
\]

where `P=z(z+a)(z+b)(z-c)`. In the first row the negative numerator is essential: `R` has the opposite bank sign there, but `x/R` has the same `-i` sign. Lower-bank values have opposite signs.

The form `omega=z dz/R` is holomorphic off the cuts and

\[
\omega=(1/z+O(z^{-2}))\,dz
\]

at infinity. A large counterclockwise circle therefore has integral `2pi i`. A counterclockwise thin loop around either slit traverses its upper bank right to left and lower bank left to right, giving `2i` times its positive real integral. Deforming the large circle to these two counterclockwise loops gives

\[
\boxed{I_u+I_v=\pi}.
\]

The finite endpoint contributions vanish: the ordinary branch endpoints have `O(epsilon^(1/2))` loop contributions, while at zero the numerator cancels the branch singularity and the contribution is `O(epsilon^(3/2))`. There are no finite-point residues omitted in the deformation. On the compact two-sheeted curve, `omega` itself has residues `-1,+1` at its two infinities; the outer-contour coefficient, rather than a claim that this form is holomorphic, is what drives the identity.

On one quadrant, `u=-F(t)` runs from `-b` to `-a`, and direct substitution yields

\[
\sqrt{\frac{u}{(a+u)(b+u)(c-u)}}\,|du|
=2\sqrt{\frac{F(t)}{c+F(t)}}\,dt.
\]

The density has four equal quadrant integrals, so `Iu=L/2`, not `L` or `L/4`. Independently, `tau(v)=(1/2) integral_0^v sqrt(w/((a+w)(b+w)(c-w))) dw` gives `Iv=2H`. Hence `rho=Iv/L=(pi-L/2)/L` exactly as claimed.

For completeness, direct differentiation of the candidate's coordinates was independently checked algebraically. Setting `h=sin^2(t)` gives zero residuals for the ellipsoid equation and all three metric components:

\[
g_{tt}=(v+F)F/(c+F),\quad g_{tv}=0,\quad
g_{vv}=-\frac{(v+F)v}{4(a+v)(b+v)(c-v)}.
\]

The belt chart has no missing or duplicated points: its defining left side in equation (7) strictly decreases with `v`; at `v=c` it is `1-z^2/c<=1`; at `v=0` it is `1+c(x^2/a^2+y^2/b^2-z^2/c^2)>=1`. The signed trigonometric coordinates then determine `t`. The signed height is smooth across the equator because both height and `z` equal a positive analytic factor times `sqrt(c-v)`. At the tropics the continuous extension and order `v^(3/2)` are adequate for the reflected null-chain convention; a nonsingular Lorentz metric there is not assumed.

Thus `g=(v+F)(dS^2-dY^2)` on the open cylinder, null leaves have slopes `dS/dY=+/-1`, and reflection retaining positive `S` advance gives `2H` for both an equator return and one full tropic-to-tropic arc. The GKT definition in Section 5 agrees with the first path, and its Section 4 density agrees with `dS` up to a nonzero constant.

## Boundary cases, closure, and parameter control

If `a<b`, exchange the axes (or use the ordered cut `[-max(a,b),-min(a,b)]`); the density is carried into itself by a quarter-period shift. No ordering of `c` relative to either axis is required: the two negative branch points remain separate from `0<c`.

At `a=b=A`, one must not set the shrinking-cut integral to zero. Its limiting value is `pi sqrt(A/(A+c))`. The collapsed branch has

\[
R=(z+A)s_{0,c}(z),\qquad
\operatorname{res}_{z=-A}\frac{z\,dz}{R}
=\sqrt{A/(A+c)}.
\]

The former cut period has become a pole contribution. Direct real evaluation with `v=c sin^2(theta)` gives

\[
I_v=2\int_0^{\pi/2}\frac{c\sin^2\theta}{A+c\sin^2\theta}\,d\theta
=\pi\bigl(1-\sqrt{A/(A+c)}\bigr).
\]

This verifies the degeneration without a formal zero-length integral. The candidate's continuity passage is sound with this limiting interpretation; writing it explicitly would improve exposition.

For the equator map, `T^n` closes with actual winding `r` precisely when `n(2H)=rL`, hence `M=n/(n+2r)`. Full arcs additionally alternate the two distinct boundary circles, forcing even `n`. Rational `rho=p/q` has least return-map period `q`; full chains have least arc count `lcm(2,q)` and winding `p lcm(2,q)/q`. This checks the odd-denominator case and rules out an odd closed full-arc sequence. Positive advance makes zero winding impossible for a nontrivial finite chain.

Differentiation gives

\[
\partial_c M=-\frac1{4\pi}\int_0^{2\pi}
\frac{\sqrt F}{(c+F)^{3/2}}\,dt<0.
\]

For fixed positive axes the endpoint limits are `M->1` as `c->0+` and `M->0` as `c->infinity`. Thus each positive rational `r/n` has exactly one positive `c`. Local real analyticity and the implicit function theorem apply because `F` has a positive lower bound locally and this derivative never vanishes. Common scaling preserves `M` and `rho`. For unequal axes, with `m=min(a,b), B=max(a,b)` and `K=(1+2r/n)^2-1`, the strict density bounds yield `m K<c<B K`. Equal axes give equality `c=A K`. There is no hidden extra parity condition on the equator map or extra parameter exclusion.

## The imported elliptic translation error

For `p=(a+b)/2,q=(a-b)/2>0`, all four roots of

\[
y^2=(p-qw)(c+p-qw)(1-w^2)
\]

are distinct: `-1<1<p/q<(c+p)/q`. On its nonsingular genus-one compactification, `dS=-(p-qw)dw/(2y)` has no finite poles. In the local coordinate `xi=1/w`, put `eta=y xi^2`. Then

\[
dS=\frac{p\xi-q}{2\eta\xi}\,d\xi,
\qquad \eta(0)=\pm iq.
\]

The two residues are respectively `+i/2,-i/2`, validating the candidate's correction: it is third kind, not second kind or holomorphic.

A useful stronger falsification of the imported inference is available. Any ordinary elliptic-group translation that preserves this meromorphic form must preserve its poles and their residues. Because the residues are distinct, it must fix each of the two poles. A nonidentity group translation has no fixed point. Therefore **only the identity elliptic-group translation preserves this form**. If a proposed identification of the real return map with a group translation extended algebraically and preserved `dS`, the real invariance would imply complex invariance by analytic continuation and this obstruction would apply. The real invariant-coordinate conjugacy alone cannot establish that identification. This does not rule out a different algebraic construction or arithmetic criterion.

## Computational evidence and exact remaining gap

`independent_checks.py` was actually run as `/usr/bin/python3 -E -B independent_checks.py` (Python 3.9.6, SymPy 1.14.0, mpmath 1.3.0); the final subprocess exited zero and its raw stderr is empty. It verifies the metric residuals and residues symbolically. At 70 decimal digits it evaluates the two real periods independently after smooth endpoint substitutions, tests ten cases including axis order reversal, axis collision, aspect ratio `10^8`, and `c` from `10^-12` to `10^12`, checks common scaling down to `10^-20`, verifies upper-bank signs, and integrates a separate large complex circle. Period-sum errors round to zero at that precision; the complex-circle discrepancy is about `2.90e-70`. These are diagnostic calculations, not certified interval quadrature.

For example, at `(a,b,c)=(5,2,7)`, `Iu=1.78461747174397992485848505226`, `Iv=1.35697518184581331360415833102`, and `rho=0.380186567522433205443237508091`. Bisection for `(a,b,n,r)=(5,2,3,1)` gives `c=5.912121814712764919990341261730937156731` strictly between `32/9` and `80/9`, with target-density error about `1.54e-40`.

The first subprocess failed because this audit's own direct-differentiation checker mistakenly interchanged `sin^2(t)` and `cos^2(t)` in the two positive `gtt` terms. That checker transcription was corrected; the failed raw output is preserved separately. It exposed no defect in the candidate.

The strongest verified result is the complete analytic iff criterion for the defined map and reflected chains. The exact stronger gap is a finite algebraic Cayley-type characterization or a justified different algebraic period/torsion mechanism. The already imported automatic group-translation route is blocked by its missing and incompatible differential identification. Historical novelty and publishability require separate evaluation and are deliberately outside this verdict.
