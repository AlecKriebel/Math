# Evaluated reverse arrow for the finite four-shift ratios functional

## Result and scope

The prescribed Conrey–Keating Ramanujan profile differentiates to the **evaluated Hardy–Littlewood singular series**, with density `S(h) x^(-2r)`. A uniform holomorphic error bounded by `epsilon(T,N)` on the closed radius-`rho` four-shift polydisc gives prime-power second-moment error at most `epsilon(T,N)/rho^2`. Consequently the gate's forward error `O(N^phi)` gives `O(N^phi (log N)^2/c^2)=o(T)` when `lambda phi<1`.

This reverse theorem requires no RH or GRH by itself: all Dirichlet polynomials are finite and all analytic continuation used below is local at the pole of zeta at 1. It does not remove the GRH qualification from any separate use of CK's arithmetic one-swap identity. It proves an aggregate prime-power statement, not inversion of the ratios average to individual fixed-shift correlations.

Notation and all fixed parameters are those of the adopted formulation gate, subject to the explicit pass-1 correction in `CONTRACT.md`: the combined two-arrow witness uses `0<psi<=phi<1`, in addition to the strict length restrictions. The general reverse theorem below starts only from (11), and does not itself need a correlation exponent `psi`. In particular `w` is real Schwartz, `supp(w_hat) subset [-A,A]`, `0<=r<=a0/log N`, and `rho=c/log N`. Put

\[
 b_T=2\pi A/T,\qquad d_T=e^{b_T}-1,\qquad
 H_T=\lfloor N(1-e^{-b_T})\rfloor,
\]
\[
 u_h(x)=\frac{T}{2\pi}\log(1+h/x),\qquad
 K_h^\pm(x)=\frac{\widehat w(\pm u_h(x))}{\sqrt{x(x+h)}}.
\]

All the assertions below hold once `T` exceeds a threshold depending only on the fixed parameters. Empty `h` sums are zero. No assertion of relative error to a possibly vanishing main term is needed: the concluding error is absolute `o(T)`.

## 1. Normal convergence and collision holomorphy of the prescribed profile

Write

\[
 g(v)=\frac1{\zeta(1+v)},\qquad
 \mathfrak S_{\boldsymbol z}(h)=
 \sum_{q\ge1}\frac{c_q(h)F_{\alpha,\gamma}(q)F_{\beta,\delta}(q)}{q^2}.
\]

Here `F` is exactly the gate's multiplicative function:

\[
 F_{\alpha,\gamma}(p)
 =-\frac{p^{\alpha-\gamma}}{1-p^{-1+\alpha-\gamma}},
 \qquad F_{\alpha,\gamma}(p^j)=0\quad(j\ge2).
\]

There is a fixed `eta>0` such that all the following hold on the fixed open neighborhood

\[
 U=\{\boldsymbol z:\max(|\alpha|,|\beta|,|\gamma|,|\delta|)<\eta\}.
\]

Choose `eta<1/8`, sufficiently small that `g` is holomorphic for `|v|<2 eta`; such an `eta` exists because `v zeta(1+v)` is holomorphic and equals 1 at zero. Shrinking `eta` if necessary gives `|alpha+beta|<1/2` on `U`. Every microscopic closed polydisc in the gate is contained in `U` for all sufficiently large `T`, uniformly in `a`.

For compact subsets of `U`,

\[
 |F_{\alpha,\gamma}(p)F_{\beta,\delta}(p)|/p^2
 \le C_\eta p^{-2+4\eta},
\]

because `|1-p^(-1+alpha-gamma)|>=1-2^(-1+2 eta)>0`. Also

\[
 c_p(h)=\begin{cases}p-1,&p\mid h,\\-1,&p\nmid h.\end{cases}
\]

For each fixed positive integer `h`, the finitely many primes dividing `h` cause no convergence problem, and the remaining prime majorant is summable because `2-4 eta>1`. Thus the `q` series is absolutely and normally convergent on `U`, and it equals the normally convergent Euler product

\[
 \mathfrak S_{\boldsymbol z}(h)
 =\prod_p\left(1+
 \frac{c_p(h)p^{\alpha-\gamma+\beta-\delta}}
 {p^2(1-p^{-1+\alpha-\gamma})(1-p^{-1+\beta-\delta})}\right).
 \tag{1}
\]

Normal convergence proves joint holomorphy and legitimizes shift differentiation. It remains valid when a local factor vanishes; no logarithm or division by that local factor is being used. All four-shift collisions in the small neighborhood are therefore harmless for this expression.

A useful stronger estimate is uniform in the number of gaps:

\[
 \sum_{1\le h\le H}|\mathfrak S_{\boldsymbol z}(h)|\le C_\eta H
 \qquad(\boldsymbol z\in U),
 \tag{2}
\]

with a slightly smaller fixed `U` if needed to make all constants uniform on its closure. Indeed only squarefree `q` occur, and

\[
 |c_q(h)|=\prod_{p\mid q}\bigl(1+(p-2)\mathbf1_{p\mid h}\bigr),
\]
\[
 \sum_{h\le H}|c_q(h)|
 \le H\prod_{p\mid q}(2-2/p).
\]

Expanding this finite divisor product and using `floor(H/d)<=H/d` proves the second line. Summing the nonnegative majorants over squarefree `q` produces the convergent Euler product

\[
 \prod_p\left(1+(2-2/p)
 \frac{|F_{\alpha,\gamma}(p)F_{\beta,\delta}(p)|}{p^2}\right),
\]

which is uniformly bounded on the fixed neighborhood. This proves (2) without an `H^epsilon` loss.

The cumulative profile is consequently the jointly holomorphic function

\[
 m_{\boldsymbol z}(x,h)
 =\frac{x^{1-\alpha-\beta}}{1-\alpha-\beta}
   g(\gamma-\alpha)g(\delta-\beta)
   \mathfrak S_{\boldsymbol z}(h),\qquad x>0.
 \tag{3}
\]

Its two oriented versions agree, since swapping the two coefficient pairs leaves (3) unchanged. Its classical density is

\[
 \frac{\partial m_{\boldsymbol z}}{\partial x}
 =x^{-\alpha-\beta}g(\gamma-\alpha)g(\delta-\beta)
   \mathfrak S_{\boldsymbol z}(h).
 \tag{4}
\]

The local analytic arguments here use no zero-free-region theorem and no GRH.

## 2. Exact evaluation at the collision

At `Delta_r=(r,r,r,r)`,

\[
 F_{r,r}(p)=-\frac{p}{p-1},\qquad
 \frac{F_{r,r}(q)^2}{q^2}=\frac{\mu(q)^2}{\varphi(q)^2}.
\]

Therefore

\[
 \mathfrak S_{\Delta_r}(h)
 =\sum_{q\ge1}\frac{\mu(q)^2 c_q(h)}{\varphi(q)^2}
 =\prod_p\left(1+\frac{c_p(h)}{(p-1)^2}\right)
 =\mathfrak S(h).
 \tag{5}
\]

The last equality is exactly the gate's singular series. If `p|h`, its local factor is

\[
 1+\frac1{p-1}=\frac{1-1/p}{(1-1/p)^2}.
\]

If `p` does not divide `h`, the factor is

\[
 1-\frac1{(p-1)^2}=\frac{1-2/p}{(1-1/p)^2}.
\]

This includes `p=2`: the product is zero for every odd gap. For even gaps it is the usual positive twin-prime singular series. Prime powers in `h` cause no ambiguity: the series depends only on which primes divide `h`, exactly as the local obstruction count does.

Since

\[
 g(v)=v+O(v^2),
\]

both `g` factors in (3) vanish at the collision. Any term in a mixed derivative in which one of the two `g` factors was not differentiated vanishes. Derivatives of the `x` factor and of `mathfrak S_z` therefore make no contribution to these particular mixed derivatives. With

\[
 D_{++}=\partial_\alpha\partial_\beta,\quad
 D_{+-}=\partial_\alpha\partial_\delta,\quad
 D_{-+}=\partial_\gamma\partial_\beta,\quad
 D_{--}=\partial_\gamma\partial_\delta,
\]

one obtains the exact signs

\[
 (D_{++},D_{+-},D_{-+},D_{--})m\big|_{\Delta_r}
 =(1,-1,-1,1)\,
 \mathfrak S(h)\frac{x^{1-2r}}{1-2r},
 \tag{6}
\]
\[
 (D_{++},D_{+-},D_{-+},D_{--})\,dm\big|_{\Delta_r}
 =(1,-1,-1,1)\,\mathfrak S(h)x^{-2r}\,dx.
 \tag{7}
\]

In (6), `r<1/2` for all sufficiently large `T`. Equation (7), which is the needed assertion, can also be read directly from (4). This derivation evaluates the main term; it does not leave a formal derivative of an unspecified profile.

### The lower endpoint `1^-`

For the cumulative arithmetic sum, `1^-` includes any atom at `n=1`. The profile (3) can either be continued smoothly through 1 or set to zero below 1, creating an atom `m(1,h)` at 1. These conventions give the same functional here. Indeed

\[
 T>2\pi A/\log2\quad\Longrightarrow\quad K_h^\pm(1)=0
 \quad\hbox{for every }h\ge1.
\]

In fact the kernel vanishes identically for `x<=h/d_T`, with all derivatives vanishing at the boundary, because `w_hat` is smooth and supported in `[-A,A]`. Thus no endpoint atom, differentiated or otherwise, survives. At the upper endpoint `N-h`, a sharp integer pair is retained exactly when its kernel is nonzero; no smoothing of the coefficient cutoff has been made.

## 3. Finite coefficient derivative identities

Dirichlet inversion gives the exact identities

\[
 I_{r,r}(n)=n^{-r}\mathbf1_{n=1},
\]
\[
 \partial_\alpha I_{\alpha,\gamma}(n)\big|_{\alpha=\gamma=r}
 =-n^{-r}\sum_{de=n}\mu(e)\log d=-n^{-r}\Lambda(n),
 \tag{8}
\]
\[
 \partial_\gamma I_{\alpha,\gamma}(n)\big|_{\alpha=\gamma=r}
 =-n^{-r}\sum_{de=n}\mu(e)\log e=+n^{-r}\Lambda(n).
 \tag{9}
\]

Here `Lambda(1)=0`. The identity `mu * log = Lambda` proves (8). For (9), use `log e=log n-log d` and `sum_{e|n}mu(e)=1_{n=1}`; the leftover `log n` term is always zero. The same formulas apply to the second coefficient pair.

Because all polynomial sums are finite, their shift derivatives can be taken inside the `t` integral. Since `r` is real, the two resulting Mangoldt polynomials at `t` and `-t` are complex conjugates. Hence

\[
 (D_{++},D_{+-},D_{-+},D_{--})\mathcal R_{T,N}\big|_{\Delta_r}
 =(1,-1,-1,1)V_{\Lambda,r}(T,N;w).
 \tag{10}
\]

Reality of `w` makes `V` real, but positivity of `w` is neither assumed nor needed.

## 4. Cauchy transfer with its precise loss

Suppose, independently of how it was proved,

\[
 \mathcal R_{T,N}(\boldsymbol z)=\mathcal Q_{T,N}(\boldsymbol z)
                              +E_{T,N}(\boldsymbol z)
\]

on the closed four-variable radius-`rho` polydisc about `Delta_r`, where `Q` is the **specific gate functional with profile (3)**, and

\[
 \sup_{\boldsymbol z\in D}|E_{T,N}(\boldsymbol z)|\le\epsilon(T,N).
 \tag{11}
\]

The preceding sections show that this `Q` is holomorphic on a neighborhood of `D` for all sufficiently large `T`. The exact diagonal is entire; the off-diagonal has finitely many `h` integrals on compact intervals of a normally convergent holomorphic function. Thus `E` is holomorphic there too.

Freeze `gamma=delta=r`. The two-variable Cauchy formula gives

\[
 \partial_\alpha\partial_\beta E(\Delta_r)
 =\frac1{(2\pi i)^2}
   \int_{|z_1-r|=\rho}\int_{|z_2-r|=\rho}
   \frac{E(z_1,z_2,r,r)}{(z_1-r)^2(z_2-r)^2}\,dz_2\,dz_1,
\]

and consequently

\[
 |\partial_\alpha\partial_\beta E(\Delta_r)|
 \le\epsilon(T,N)\rho^{-2}.
 \tag{12}
\]

The constant in (12) is exactly 1. The other three mixed derivatives satisfy the same bound. There is no extra factorial, because the multi-index is `(1,1)`. The loss cannot in general be improved: `E=epsilon (alpha-r)(beta-r)/rho^2` saturates (12). A real-slice estimate or pointwise-in-shifts estimate does not suffice for this argument.

## 5. Evaluated prime-power second-moment theorem

Define the fully explicit main term

\[
 \mathcal B_r(T,N;w)=
 T\widehat w(0)\sum_{n\le N}\frac{\Lambda(n)^2}{n^{1+2r}}
 +T\sum_{h=1}^{H_T}\mathfrak S(h)
   \int_1^{N-h}x^{-2r}\bigl(K_h^+(x)+K_h^-(x)\bigr)\,dx.
 \tag{13}
\]

The integral is zero if its support is empty. Equations (7)–(10) show

\[
 (D_{++},D_{+-},D_{-+},D_{--})\mathcal Q_{T,N}\big|_{\Delta_r}
 =(1,-1,-1,1)\mathcal B_r(T,N;w).
 \tag{14}
\]

In particular the diagonal in (13) is exact, including every prime power; no prime-number-theorem replacement or asymptotic truncation is involved.

Combining (10), (12), and (14) proves

\[
 \boxed{\big|V_{\Lambda,r}(T,N;w)-\mathcal B_r(T,N;w)\big|
 \le\epsilon(T,N)\rho^{-2}.}
 \tag{15}
\]

Under the proposed forward estimate `epsilon(T,N)<=C N^phi`, this becomes

\[
 V_{\Lambda,r}(T,N;w)=\mathcal B_r(T,N;w)
       +O\left(c^{-2}N^\phi(\log N)^2\right)
       =\mathcal B_r(T,N;w)+o(T),
 \tag{16}
\]

uniformly in `0<=a<=a0`, because `lambda phi<1`. Nothing in this reverse step uses `psi`; its restriction is part of proving the forward estimate.

For clarity, the exact Fourier expansion of the left side is

\[
 V_{\Lambda,r}=
 T\widehat w(0)\sum_{n\le N}\frac{\Lambda(n)^2}{n^{1+2r}}
 +T\sum_{h=1}^{H_T}\sum_{n\le N-h}
 \Lambda(n)\Lambda(n+h)[n(n+h)]^{-r}
       \bigl(K_h^+(n)+K_h^-(n)\bigr).
 \tag{17}
\]

The finite support cutoff is exact: if a pair with gap `h` contributes, then `h<=n d_T` and `n+h<=N`, whence `h<=N(1-e^(-b_T))`. Endpoint equality has zero Fourier kernel, so retaining it in `H_T` is harmless. Since `w` is real, `K_h^-` is the complex conjugate of `K_h^+`. The formulas remain valid without assuming `w` even.

Thus (15) is an evaluated, smoothed aggregate of the actual correlations in (17). It is not an unproved claim about a separate fixed gap.

## 6. Quantified density-convention comparison

Let `B_tilde_r` be (13) with the off-diagonal density `x^(-2r)` replaced by `x^(-r)(x+h)^(-r)`, leaving its exact diagonal unchanged. Put `W=||w_hat||_infinity`. Then

\[
 \boxed{\big|\mathcal B_r-\widetilde{\mathcal B}_r\big|
 \le 2T W r\,d_T H_T.}
 \tag{18}
\]

The claim is exact for all sufficiently large `T`; when `r=0`, both sides are zero.

First, the classical singular series has the elementary bound

\[
 \sum_{h\le H}\mathfrak S(h)\le H\quad(H\ge0).
 \tag{19}
\]

To prove it, set

\[
 C_2=\prod_{p>2}\left(1-\frac1{(p-1)^2}\right),\qquad
 a(d)=\begin{cases}\prod_{p\mid d}(p-2)^{-1},&d\text{ odd squarefree},\\0,&\text{otherwise}.\end{cases}
\]

Then `S(2k)=2 C2 sum_{d|k}a(d)` and `S(2k+1)=0`. All terms are nonnegative, so

\[
 \sum_{h\le H}\mathfrak S(h)
 =2C_2\sum_d a(d)\left\lfloor\frac{H}{2d}\right\rfloor
 \le C_2H\prod_{p>2}\left(1+\frac1{p(p-2)}\right)=H.
\]

The last equality follows prime by prime; both products converge absolutely.

For `r>=0` and `x>=1`,

\[
 0\le x^{-2r}-x^{-r}(x+h)^{-r}
 =x^{-2r}\bigl(1-e^{-r\log(1+h/x)}\bigr)
 \le r h/x.
\]

The kernel bound `|K_h^pm(x)|<=W/x` and its support `x>=h/d_T` give, for each orientation,

\[
 \int_1^{N-h}|K_h^\pm(x)|
 \big|x^{-2r}-x^{-r}(x+h)^{-r}\big|\,dx
 \le Wrh\int_{h/d_T}^{\infty}x^{-2}\,dx=Wr d_T.
\]

Summing and applying (19) proves (18). Since `T d_T=O_A(1)`, `H_T=O_A(N/T)`, and `r<=a0/log N`,

\[
 |\mathcal B_r-\widetilde{\mathcal B}_r|
 =O_{A,w,a_0}\left(\frac{N}{T\log N}\right)=o(T)
 \qquad(1<\lambda<2).
 \tag{20}
\]

If `a0=0`, the difference is identically zero. The alternative density convention therefore preserves the requested absolute `o(T)` prime endpoint, but its error has been explicitly paid rather than silently suppressed.

## Attribution and limitations

The coefficient family, its prime derivative, the prescribed arithmetic profile, and the ratios/correlation strategy come from Conrey–Keating, *Pair correlation and twin primes revisited* (2016), especially Sections 1, 3, and 4: https://arxiv.org/pdf/1604.06124v2 . The use of uniform shift differentiation is established ratios-method prior art, including Conrey–Snaith, *Applications of the L-functions ratios conjectures*: https://arxiv.org/pdf/math/0509480 . The local convergence proof, evaluated aggregate, precise Cauchy bookkeeping, endpoint discussion, and density comparison above are supplied as an audit of this declared finite-polynomial witness. No novelty claim is made.

This file proves the reverse component conditional on the explicit uniform finite-ratios estimate. It does not prove the arithmetic correlation hypothesis, the forward error, or the CK zero/one-swap identification. Those are separate components of the combined theorem. In particular it does not certify the full adopted gate on its own.
