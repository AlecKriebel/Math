# Triangle rebasing, independent symmetry, and the AIM three-point program

**Status: partial result. The general equality with Cohn–Elkies and a universal optimizer conversion remain unresolved.**

## 1. The exact problem and normalization

This concerns David de Laat's Problem 1.32 in the AIM list *Discrete geometry and automorphic forms*, not the later lattice bound with an additional condition on `|x+y|`. For an integer `n >= 1`, put `A = {0} union [1,infinity)` and

\[
 C_\triangle=\{(x,y):|x|,|y|,|x-y|\in A\}\setminus\{(0,0)\}.
\]

For a closed set `C` separated from the origin define
\[
 P(C)=\inf\{f(0,0): f\in\mathcal S(\mathbb R^{2n};\mathbb R),\quad
 \widehat f(0,0)=1,\quad\widehat f\ge0,\quad f|_C\le0\},
\]
using `exp(-2 pi i <x,xi>)` for the Fourier kernel. The original question asks whether `sqrt(P(C_triangle))` equals the raw Cohn–Elkies bound
\[
 L_n=\inf\{g(0):g\in\mathcal S(\mathbb R^n;\mathbb R),\quad
 \widehat g(0)=1,\quad\widehat g\ge0,\quad g(x)\le0\ (|x|\ge1)\},
\]
and asks for an explanation of empirically observed independent rotational symmetry and constructions between the two problems. We do not assume either infimum is attained.

For a lattice `Lambda` of minimum vector length at least 1, its square is supported on `C_triangle union {0}`. Poisson summation therefore gives
\[
 \operatorname{covol}(\Lambda)^{-2}
 \le\sum_{x,y\in\Lambda}f(x,y)\le f(0,0).
\]
Thus `sqrt(f(0,0))` bounds the **number density**. With radius `1/2`, conventional center density is bounded by `2^{-n} sqrt(f(0,0))`, and packing density by `vol(B^n_{1/2}) sqrt(f(0,0))`. This explicitly states the convention behind the AIM wording.

## 2. Genuine triangle symmetries

Let
\[
 S(x,y)=(y,x),\qquad R(x,y)=(-x,y-x).
\]
Both preserve the three edge lengths as an unordered triple. They satisfy `S^2=R^2=(SR)^3=1` and generate a six-element rebasing group. Every element has determinant of absolute value 1, so pullback preserves Fourier nonnegativity, Fourier normalization, the objective, and feasibility. Averaging over this group and simultaneous orthogonal transformations is valid.

There is a small but important generator distinction: the alternative involution `T(x,y)=(x,x-y)` is also a valid symmetry, but `S,T` generate a twelve-element group; `(ST)^3=-I`. The six-element rebasing group above avoids confusing global negation with a vertex permutation.

Independent rotations are not symmetries of the sign set: for a unit vector `e`, `(2e,-3e/2)` belongs to `C_triangle`, whereas `(2e,3e/2)` does not.

### Theorem 1. The two symmetry requirements are incompatible

A continuous function vanishing at infinity that is invariant under both `R` and the separate reflection `J(x,y)=(-x,y)` is identically zero. Consequently, no nonzero Schwartz function is invariant under both triangle rebasing and `O(n) x O(n)`.

**Proof.** The composition is
\[
 JR(x,y)=(x,y-x).
\]
The hypotheses imply `f(x,y)=f(x,y-kx)` for every integer `k`. When `x != 0`, the argument escapes to infinity as `k` tends to infinity, so the value is zero. Continuity handles `x=0`. Independent rotational invariance includes `J`. QED.

### Corollary 2. Angularly dependent competitors at every feasible value

For every feasible `f`, its six-term triangle average is feasible, has the same objective, and is **not** independently rotationally invariant. In particular, angular dependence alone is not evidence of an improvement on Cohn–Elkies. If an independently invariant optimizer exists, there is also a non-independently-invariant optimizer with the same value; it cannot be the unique optimizer.

**Proof.** The average is rebasing invariant. Its Fourier transform at zero remains 1, so it is not the zero function. Theorem 1 excludes independent invariance. QED.

The theorem does not disprove the existence of an independently invariant optimum. It disproves a universal claim that all optima must have that symmetry, conditional on attainment, and rules out imposing both symmetry requirements in a decaying ansatz.

## 3. What the independently invariant subclass proves

Write
\[
 C_\square=\{(x,y):|x|,|y|\in A\}\setminus\{(0,0)\},\qquad
 C_\pm=\{(x,y):|x|,|y|,|x-y|,|x+y|\in A\}\setminus\{(0,0)\}.
\]
Then `C_pm subset C_triangle subset C_square`. The product theorem of Cohn–de Laat–Salmon, Proposition 4.7, together with their Schwartz/continuous comparison, gives `P(C_square)=L_n^2`. The factor is obtained by rescaling their minimum distance 2 to 1 and cancelling the ball-volume factors. Therefore
\[
 P(C_\pm)\le P(C_\triangle)\le L_n^2.
\]

If `f` is independently invariant and feasible on `C_triangle`, it is feasible on `C_square`: axes already lie in the triangle set; otherwise rotate `x,y` to opposite directions, for which `|x-y|=|x|+|y|>=2`, and use invariance. Conversely, independent averaging preserves square feasibility. Hence
\[
 P_{\mathrm{ind}}(C_\triangle)=P(C_\square)=L_n^2.
\]
This is the previously available partial observation, rechecked here rather than claimed as new. Any strict improvement must leave the independently invariant subclass. Section 2 shows that leaving it is nevertheless possible with no improvement at all.

In the already sharp dimensions `n=1,8,24`, a lattice of number density `L_n` and the Poisson inequality prove equality for the exact triangle program. The raw values are respectively `L_1=1`, `L_8=16`, and `L_24=2^24`; this is a consequence of existing sharp sphere-packing results, not a new solution.

## 4. Why the obvious dual tensor does not settle the triangle program

The general sign-constrained duality theorem describes certificates by tempered measures `nu=delta_0+mu`, with `mu>=0` supported on the sign set and `hat(nu)>=c delta_0`. Tensoring one-point certificates proves the lower bound for `C_square`.

### Proposition 3. Radial tensor support obstruction

For `n>=2`, let `mu` be a nonzero rotationally invariant nonnegative measure supported on `|x|>=1`. The measure `(delta_0+mu) tensor (delta_0+mu)` has support outside `C_triangle union {0}`.

**Proof.** Some point of radius `r>=1` belongs to `supp(mu)`. Rotation invariance puts the whole sphere of radius `r` in that support. On this sphere choose distinct `x,y` sufficiently close that `0<|x-y|<1`. Every product neighborhood has positive `mu tensor mu` mass. Thus `(x,y)` lies in the product support but not in the triangle sign set. QED.

A one-point dual certificate with positive `c` cannot have `mu=0`, since the Fourier transform of `delta_0` is Lebesgue measure and has no atom at zero. Consequently, independently radial one-point dual tensoring cannot supply the missing lower bound in dimensions at least 2. Nonradial lattice-comb certificates in sharp dimensions are not excluded. This is a support obstruction, not a proof of a strict gap.

## 5. Restriction maps exist but need not preserve the bound

The three edge restrictions
\[
 g_1(x)=f(x,0),\quad g_2(x)=f(0,x),\quad g_3(x)=f(x,x)
\]
are Schwartz and have nonnegative Fourier transforms
\[
 \widehat g_1(\xi)=\int\widehat f(\xi,\eta)\,d\eta,\quad
 \widehat g_2(\eta)=\int\widehat f(\xi,\eta)\,d\xi,\quad
 \widehat g_3(\zeta)=\int\widehat f(\xi,\zeta-\xi)\,d\xi.
\]
All are nonpositive at distances at least 1. Each mass `a_j=hat(g_j)(0)` is strictly positive: continuity and `hat(f)(0,0)=1` give a positive neighborhood on the corresponding integration subspace. Thus `g_j/a_j` is a genuine normalized Cohn–Elkies function. Its objective is `f(0,0)/a_j`.

### Theorem 4. All three edge maps can worsen the three-point objective

For every `n>=1`, there is a triangle-rebasing-invariant feasible Schwartz function for which
\[
 a_1=a_2=a_3<\sqrt{f(0,0)}.
\]
Thus no universal inequality `max_j a_j >= sqrt(f(0,0))` holds, even after all legitimate compact symmetrizations.

**Proof.** Put
\[
 q(x,y)=|x|^2+|y|^2-\langle x,y\rangle,\qquad
 f(x,y)=c(1-q(x,y))e^{-2nq(x,y)},\qquad
 c=2\,3^{n/2}(n/\pi)^n.
\]
The form `q` is positive definite and rebasing invariant. It is at least 1 on `C_triangle`: on axes or the diagonal this follows from the nonzero norm bound; when all three edges are nonzero, `2q=|x|^2+|y|^2+|x-y|^2>=3`.

For `M=[[1,-1/2],[-1/2,1]] tensor I_n`, let `u=z^T M^{-1}z>=0`. The Fourier transform of `exp(-beta q)` is
\[
 H_\beta(z)=\frac{(2\pi/\beta)^n}{3^{n/2}}
             e^{-\pi^2u/\beta}.
\]
Differentiation in `beta` yields
\[
 \widehat{(1-q)e^{-\beta q}}(z)
 =H_\beta(z)\left(1-\frac n\beta+\frac{\pi^2u}{\beta^2}\right).
\]
Taking `beta=2n` proves Fourier positivity and the stated normalization. The three restrictions all equal `c(1-|x|^2) exp(-2n|x|^2)`, and their common integral is
\[
 a=\frac34c\left(\frac\pi{2n}\right)^{n/2}.
\]
Consequently
\[
 \frac{a^2}{c}=\frac98\left(\frac{\sqrt3}{2}\right)^n
 \le\frac{9\sqrt3}{16}<1.
\]
The last strict inequality is equivalent to `243<256`. QED.

This example is also square-feasible: when both radii `r,s>=1`, `q>=(r-s)^2+rs>=1`. It does not establish an improved three-point value.

## 6. The primal tensor and an exactly optimized Gaussian family

If a normalized even one-point feasible function `g` is strictly negative at some `u` with `|u|>=1`, then `F(x,y)=g(x)g(y)` has nonnegative Fourier transform and the expected normalization, but
\[
 F(u,-u)=g(u)^2>0,
\]
although `(u,-u)` belongs to `C_triangle`. Thus the obvious primal tensor has the wrong sign. Concrete such `g` are normalized multiples of `(1-|x|^2) exp(-beta |x|^2)` for `beta>n/2`; their Fourier positivity follows from the same Gaussian derivative calculation.

For the triangle-symmetric degree-one family `(1-q) exp(-beta q)`, normalization is possible with Fourier positivity exactly when `beta>n`. Its objective is
\[
 c_\beta=3^{n/2}\left(\frac\beta{2\pi}\right)^n
               \frac1{1-n/\beta}.
\]
It tends to infinity at both ends of `(n,infinity)`, and
\[
 \frac{d}{d\beta}\log c_\beta
 =\frac{n(\beta-n-1)}{\beta(\beta-n)}.
\]
The unique optimum in this family is at `beta=n+1`, with
\[
 c_* = \frac{3^{n/2}(n+1)^{n+1}}{(2\pi)^n}.
\]
This is an analytic feasible family and an exact within-family optimization, not a full optimization of the AIM program. The family is square-feasible, so it cannot improve `L_n^2`.

## 7. Remaining problem

The unrestricted inequality `P(C_triangle)>=L_n^2` has not been proved here, nor has a counterexample been constructed. The explicit forward tensor fails, the radial dual tensor violates support, and the three restriction maps can all lose objective value. These obstructions exclude specific natural constructions, not all possible conversions.

The later `C_pm` results cannot be substituted for this target: shrinking the sign set relaxes the negativity requirement and can lower the infimum. An angular or semidefinite search for this exact problem must retain the triangle condition and must not impose both rebasing symmetry and separate reflections, by Theorem 1.

## References

1. David de Laat, Problem 1.32, [AIM: Discrete geometry and automorphic forms](http://aimpl.org/discreteaf/1/). Primary statement directly checked on 2026-10-03.
2. H. Cohn, D. de Laat, A. Salmon, [Three-point bounds for sphere packing](https://arxiv.org/abs/2206.15373), 2022, especially Theorem 3.1, Proposition 3.5, Definition 4.5, Proposition 4.7, and Remark 4.9. Theorem 1.4 uses `C_pm`.
3. H. Cohn and N. Elkies, [New upper bounds on sphere packings I](https://doi.org/10.4007/annals.2003.157.689), Annals of Mathematics 157 (2003), 689–714.
