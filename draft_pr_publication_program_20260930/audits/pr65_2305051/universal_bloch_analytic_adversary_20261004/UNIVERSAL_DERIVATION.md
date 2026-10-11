# Independent all-point analytic reconstruction

Exact submitted head: `5cc1602c05d79502defb07cec7027963149494d2`.
Input: authenticated original `CANDIDATE.md`, 13,491 bytes, git blob `7802cf06a9daa4b19e894e3b7a276740948bc37d`.
This is an audit of the submitted mechanism, not a new search for a replacement construction.

## Claim and assumptions

Let the candidate's four-adic recursion define the nonnegative integer lists `v^(n)` and consistent cell masses `mu(I_(n,j))=4^(-n)v_j^(n)`. Define

\[
F(z)=\int_0^1\frac{e^{2\pi i x}+z}{e^{2\pi i x}-z}\,d\mu(x).
\]

The claim under audit is that this particular transform exists holomorphically and satisfies a bound on `(1-|z|^2)|F'(z)|` at **every** disk point. The argument below provides the deliberately loose explicit bound

\[
\boxed{\sup_{z\in\mathbb D}(1-|z|^2)|F'(z)|\le 240\pi(\pi^2+1)<8196.}
\tag{A}
\]

No assertion that the atomic approximants have a uniformly bounded Bloch seminorm is made or needed. No lower bound independent of `z` on `|1-B(z)|` is assumed.

## 1. All-stage combinatorial estimates

For a positive parent the endpoint increments belong to `{−1,+1}`. Their sum belongs to `{−2,0,+2}`, so an oppositely summing middle pair always exists. Exactly two of the four increments are `+1`, and two are `−1`; the first admissible ordered pair makes the rule deterministic. A zero parent produces four zero children.

Consequently every generation has total sum `4^n`, all values lie between `0` and `n+1`, and child averages equal the parent. At each positive parent every child differs from the parent by exactly one. The pointwise increment bound is at most one including the absorbed case.

For completeness, write two neighboring parent values as `a,b`, with `|a-b|<=2`:

- If `a,b>0` and `a<b`, the facing children are `a+1,b-1`, with difference `b-a-2`, of absolute value at most one or zero.
- If `a,b>0` and `a>b`, the facing children are `a-1,b+1`, with difference `a-b-2`, likewise bounded.
- If `a=b>0`, the facing children are `a-1,b+1`, with difference two.
- If one parent is zero, the other is at most two, and its facing child is one less. Its absolute difference from zero is at most one.
- Two zero parents produce facing zeros. Inside any parent all child values differ by at most two.

This proves the circular neighbor bound for all generations, including the last-to-first boundary. This is a proof by induction, not an inference from the finite diagnostics.

## 2. Measure existence, endpoint control, and the Zygmund constant

The positive measures `f_n dx` have mass one on the compact circle. Consider any weakly convergent subsequence. For fixed generation `n`, every finer density gives the same mass to each `n`-cell, bounded by `(n+1)4^(-n)`. Every sufficiently short open arc is contained in at most two such cells. Portmanteau applied to an open neighborhood of any point bounds its limiting mass by `2(n+1)4^(-n)`. Letting `n` tend to infinity excludes every atom, including grid endpoints. Interval masses of every weak limit therefore equal the consistent specified masses. They determine a unique measure, so the full sequence converges weakly.

Let

\[
H_n(x)=\int_0^x(f_n(t)-1)\,dt.
\]

The increment has integral zero on each old cell and absolute value at most one. Hence `||H_(n+1)-H_n||_infty <=4^(-n)`, and summing the geometric tail gives

\[
\|H-H_n\|_\infty\le\frac43 4^{-n},\qquad \|H\|_\infty\le\frac43.
\]

All `H_n` and their uniform limit are continuous periodic functions. For a smooth periodic test function, integration by parts and weak convergence show distributionally `dH=dmu-dx`.

For `0<h<=1/4`, select `n>=1` with `ell=4^(-n)<=h<4ell`. A segment of length `2h<8ell` meets at most nine consecutive mesh cells, and the neighbor bound makes their range at most 16; the candidate's estimate 18 is therefore safe. Integrating the difference of opposite slopes yields

\[
|H_n(x+h)+H_n(x-h)-2H_n(x)|\le18h.
\]

The error is at most four times the uniform tail, hence at most `(16/3)ell`. Since `ell<=h`, the sum is at most `(70/3)h<24h`. For `h>1/4`, the second difference is at most `4||H||<=16/3<24h`. Thus, for every real `x,h`,

\[
|H(x+h)+H(x-h)-2H(x)|\le24|h|.
\tag{B}
\]

Periodic lifting covers intervals crossing the origin; atomlessness makes half-open, open and closed endpoint choices immaterial. This confirms the candidate's global adjacent-arc inequality with the stated constant 24.

## 3. Direct proof of the Bloch estimate

This part independently proves the required sufficiency direction of the classical criterion, with constants. Put `nu` for the angular pushforward of `mu` to `R/(2pi Z)`, `h(theta)=H(theta/(2pi))`, and

\[
p_r(t)=\frac{1-r^2}{1-2r\cos t+r^2},\qquad u(re^{i\theta})=\operatorname{Re}F(re^{i\theta}).
\]

The normalization matters: `dh=dnu-dtheta/(2pi)` and `int p_r dtheta/(2pi)=1`. Stieltjes integration by parts on the circle gives

\[
u(re^{i\theta})=1+\int_{-\pi}^{\pi}h(\theta-t)p_r'(t)\,dt,
\]

Differentiation may be performed before the change of variable, since the kernel is smooth for fixed `r<1`. This gives

\[
u_\theta(re^{i\theta})=\int_{-\pi}^{\pi}h(\theta-t)p_r''(t)\,dt.
\tag{C}
\]

Since `p_r''` is even and has integral zero, (B) implies

\[
|u_\theta(re^{i\theta})|\le\frac{6}{\pi}\int_{-\pi}^{\pi}|p_r''(t)|\,|t|\,dt.
\tag{D}
\]

For `r>=1/2`, put `delta=1-r` and `a=2/pi^2`. With `D(t)=delta^2+4r sin^2(t/2)`, the inequality `sin(|t|/2)>=|t|/pi` on `|t|<=pi` gives `D>=delta^2+a t^2`. Also `|D'|<=2|t|`, `|D''|<=2`, and `1-r^2<=2delta`. Differentiating `p_r=(1-r^2)/D` gives

\[
|p_r''(t)|\le\frac{16\delta t^2}{(\delta^2+a t^2)^3}
                 +\frac{4\delta}{(\delta^2+a t^2)^2}.
\]

Extending the positive integrals to the real line and evaluating them exactly,

\[
\begin{aligned}
\int_{-\pi}^{\pi}|p_r''(t)|\,|t|\,dt
&\le32\delta\int_0^\infty\frac{t^3}{(\delta^2+a t^2)^3}\,dt
  +8\delta\int_0^\infty\frac{t}{(\delta^2+a t^2)^2}\,dt\\
&=\frac{8/a^2+4/a}{\delta}
 =\frac{2\pi^4+2\pi^2}{\delta}.
\end{aligned}
\]

Consequently `|u_theta|<=K/(1-r)`, where `K=12pi(pi^2+1)`. For `r<=1/2`, the probability-measure kernel estimate `|F'(z)|<=2/(1-r)^2<=8` gives `|u_theta|=|Im(zF')|<=4`, so the same `K/(1-r)` bound holds on the entire disk.

Set `J(z)=zF'(z)=w(z)+iv(z)`. It is holomorphic, `J(0)=0`, and `v=-u_theta`. Thus `|v(z)|<=K/(1-|z|)` everywhere. For a point of radius `r`, the disk of radius `rho=(1-r)/2` about it lies inside the unit disk and has `|v|<=2K/(1-r)`. The center gradient formula for a harmonic function on a disk gives `|grad v|<=2 sup|v|/rho`, hence

\[
|\nabla v(z)|\le\frac{8K}{(1-|z|)^2}.
\]

The Cauchy–Riemann equations give the same gradient bound for `w`. Integrating on the radius from `0`, where `w(0)=0`, gives

\[
|w(re^{i\theta})|\le8K\int_0^r\frac{dt}{(1-t)^2}
 =\frac{8Kr}{1-r}.
\]

For `r>=1/2`,

\[
|F'(re^{i\theta})|=\frac{|J(re^{i\theta})|}{r}
\le\frac{(8+1/r)K}{1-r}\le\frac{10K}{1-r}.
\]

Multiplying by `1-r^2` proves (A). On `r<=1/2` the earlier bound gives a seminorm at most 8, which is also below `20K`. The proof controls both real and imaginary derivatives and holds uniformly in angle; it does not omit tangential approaches or exceptional boundary points.

## 4. Holomorphic convergence and denominators

On each compact disk `|z|<=r<1`, the Herglotz kernel and its `z` derivatives are continuous and uniformly bounded on the circle. Differentiation under the finite measure integral is justified there, so `F` is holomorphic, `F(0)=1`, and

\[
\operatorname{Re}F(z)=\int\frac{1-|z|^2}{|\zeta-z|^2}\,d\mu(\zeta)>0.
\]

Moving each cell's mass to its midpoint incurs angular-coordinate distance at most `ell/2`. Direct differentiation yields

\[
|\partial_x[(\zeta+z)/(\zeta-z)]|\le\frac{4\pi r}{(1-r)^2},
\qquad
|\partial_x[2\zeta/(\zeta-z)^2]|\le\frac{4\pi(1+r)}{(1-r)^3}.
\]

Therefore the candidate's function error is valid, and derivative convergence has the additional explicit audit bound

\[
\sup_{|z|\le r}|F-F_n|\le\frac{2\pi r}{(1-r)^2}4^{-n},
\qquad
\sup_{|z|\le r}|F'-F_n'|\le\frac{2\pi(1+r)}{(1-r)^3}4^{-n}.
\tag{E}
\]

Every `F_n` also has strictly positive real part and value one at zero. Hence `|F+1|,|F_n+1|>=1`; the stated identity for `B-B_n` proves the candidate's `4pi r/(1-r)^2` error. The Cayley transform is holomorphic, maps into the disk, and vanishes at zero.

The denominator `1-B` is never zero in the disk. A useful compact lower bound is `|1-B(z)|>=1-r` for `|z|<=r`, because `|F(z)+1|<=2/(1-r)` and `1-B=2/(F+1)`. This bound is allowed to approach zero at the boundary. The exact identity

\[
\frac{2B'(z)}{(1-B(z))^2}=F'(z)
\]

together with (A), rather than a nonexistent fixed lower bound on `1-B`, supplies the required small-denominator control.

## 5. Negative control and scope boundary

At generation zero the atom is at `zeta=-1`, so `F_0(z)=(-1+z)/(-1-z)`. At `z=-r`,

\[
(1-r^2)|F_0'(-r)|=\frac{2(1+r)}{1-r}\longrightarrow\infty.
\]

The same local pole mechanism occurs at every positive-weight atom in any fixed finite `F_n`. This is consistent with (E), which is compact convergence with constants depending on `r`; it shows why finite-stage boundary tests cannot prove a uniform Bloch estimate. The candidate does not make that inference.

This audit's all-point result concerns the Herglotz transform and its Cayley transform. Elimination of a singular inner factor and interpretation of the word “explicit” belong to distinct audit families; no overall purity, novelty, human-review, or publication certificate is implied.
