# Nonlinear gradient instability of the peaked reduced Ostrovsky wave

**Target:** 30004186 / OWR-17128-002.  
**Status:** complete candidate for the explicitly stated strong-norm result below; independent review pending. This is **not** a claim of nonlinear orbital instability in $L^2$ or $H^1$. Historical novelty is unconfirmed.  
**Date:** 30 September 2026. **Model and effort:** gpt-6-astra, xhigh. **Substantive response:** 1/5.

## 1. Claim and source boundary

On the circle $\mathbb T=\mathbb R/(2\pi\mathbb Z)$, consider the mean-zero reduced Ostrovsky equation

$$u_t+uu_x=\partial_x^{-1}u. \tag{1}$$

The inverse derivative denotes the periodic primitive with zero mean. Put $L=2\pi$, $\kappa=\pi/3$, $c=\kappa^2$, and place the crest at zero by writing

$$\phi(x)=\frac{(x-\pi)^2}{6}-\frac{\pi^2}{18},\qquad 0\le x\le L,$$

periodically continued. This is a translate of the source profile $U_*(z)=(3z^2-\pi^2)/18$. Its traveling solution is $u_*(t,x)=\phi(x-ct)$, its right crest slope is $-\kappa$, and $\|\phi'\|_\infty=\kappa$.

**Theorem (candidate, strong-norm orbital instability).** There is a fixed $\varepsilon_*>0$ and a family of continuous, mean-zero, periodic initial data $u_{0,\delta}$, smooth away from the crest, such that

$$\|u_{0,\delta}-\phi\|_{W^{1,\infty}(\mathbb T)}\longrightarrow0\quad(\delta\downarrow0),$$

but their local characteristic solutions to (1) have times $t_\delta$ within their intervals of existence for which

$$\inf_{\theta\in\mathbb T}\|u_\delta(t_\delta,\cdot)-\phi(\cdot-\theta)\|_{W^{1,\infty}(\mathbb T)}\ge\varepsilon_*.$$

Moreover $t_\delta=O(\log(1/\delta))$. The solutions used here are continuous and Lipschitz in space, are $C^1$ away from a single transported corner, and are obtained from the locally unique Banach-space characteristic system constructed below. The departure happens while the solution is still Lipschitz; it is not inferred merely from a possible later breakdown.

The [original OWR contribution](https://ems.press/content/serial-article-files/46811), pp. 1940–1942, leaves nonlinear instability open after proving linear and spectral results, and emphasizes the mismatch between the linearized domain and low-regularity nonlinear evolution. It does not state a nonlinear stability topology in its final question. The theorem above provides one precise strong-norm answer with an explicit solution class. It does not establish orbital instability in the weaker $L^2$ or $H^1$ norms discussed around the linear theory, and must not be represented as doing so.

## 2. Local characteristic evolution containing the peaked profile

We give the local construction because importing only smooth Sobolev well-posedness would exclude $\phi$.

Let

$$\mathcal B=\{f\in C^1([0,L]):f(0)=f(L)\},$$

with its usual $C^1$ Banach norm. Endpoint derivatives need not agree. Write the characteristic lift as $X(\xi)=\xi+Y(\xi)$, with $Y\in\mathcal B$, and take $V\in\mathcal B$. Work on the open set

$$\inf_{\xi\in[0,L]}X_\xi>0.$$

For any such $(X,V)$, define

$$m(X,V)=\frac1L\int_0^L V(\eta)X_\eta(\eta)\,d\eta,$$

$$K(\xi)=\int_0^\xi (V(\eta)-m)X_\eta(\eta)\,d\eta,$$

$$H(X,V)(\xi)=K(\xi)-\frac1L\int_0^L K(\eta)X_\eta(\eta)\,d\eta.$$

Since $\int_0^L X_\eta=L$, we have $K(0)=K(L)=0$ and $H\in\mathcal B$. Also

$$H_\xi=(V-m)X_\xi,\qquad \int_0^L H X_\xi=0. \tag{2}$$

Consider the ODE on $\mathcal B\times\mathcal B$

$$Y_t=V,\qquad V_t=H(X,V),\qquad X=\xi+Y. \tag{3}$$

The integral formulas involve only continuous bilinear products, integrations, and scalar multiplications of $C^1$ functions and their first derivatives. They define a locally Lipschitz vector field from $\mathcal B\times\mathcal B$ to itself, uniformly Lipschitz on each bounded set. The Banach-space Picard theorem therefore gives a unique local solution for initial $Y=0$ and any $V=u_0\in\mathcal B$. For the family constructed in Section 4, the initial $C^1$ norms are uniformly bounded and $X_\xi=1$, so one common positive local existence time works for every sufficiently small $\delta$. Large second derivatives of the narrow perturbation do not enter this $C^1$ system.

The physical mean is preserved. Differentiating $M=\int_0^L V X_\xi$ along (3) gives

$$M_t=\int_0^L H X_\xi+\int_0^L V V_\xi=0,$$

where the endpoint values of $V$ agree. Thus $m=0$ for mean-zero initial data. While $X_\xi>0$, define $u$ by

$$u(t,X(t,\xi))=V(t,\xi).$$

The function $H$ is exactly $(\partial_x^{-1}u)(X)$: (2) supplies its spatial derivative and zero mean. Equation (3) is therefore equivalent to (1), classically away from the transported endpoint $q(t)=X(t,0)$ and distributionally everywhere. The function $u$ is continuous across that endpoint; only its derivative can jump.

Set

$$w(t,\xi)=\frac{V_\xi(t,\xi)}{X_\xi(t,\xi)}.$$

Differentiating (3) in $\xi$ gives the exact identities, including one-sided endpoint values,

$$(X_\xi)_t=wX_\xi,\qquad w_t=V-w^2. \tag{4}$$

Thus the right crest slope $w_+(t)=w(t,0)$ satisfies

$$w_+'=u(t,q(t))-w_+^2,\qquad q'=u(t,q(t)). \tag{5}$$

There is no assumption that the crest value or its velocity remains equal to $c$. The difference of the two endpoint slopes satisfies $J_t=-(w_-+w_+)J$, so an initial nonzero corner persists while the slopes remain bounded. Profiles viewed in the moving coordinate $x-q(t)$ are continuous in $C^1([0,L])$. No assertion that translation is strongly continuous on periodic $W^{1,\infty}$ is needed.

### Continuation criterion

If $\|u_x(t)\|_\infty\le M$ on a finite time interval, (4) bounds $X_\xi$ above and below by $e^{Mt}$ and $e^{-Mt}$. The zero-mean primitive satisfies

$$\|\partial_x^{-1}h\|_\infty\le\frac{\pi}{2}\|h\|_\infty. \tag{6}$$

For example, its periodic convolution kernel on $(0,L)$ is $1/2-x/L$, whose $L^1$ norm is $L/4=\pi/2$. Hence (3) bounds $\|V\|_\infty$ on every finite interval. Since $V_\xi=wX_\xi$, it also bounds $\|V\|_{C^1}$; integrating $Y_t=V$ bounds $\|Y\|_{C^1}$. The vector field in (3) is uniformly locally Lipschitz on these bounded sets. The positive lower bound on $X_\xi$ permits continuation past the end of the interval.

In particular, the solution cannot cease to exist at a finite time while its spatial slope remains bounded. The slope norm is continuous in time, since it equals the supremum of the continuous function $w(t,\cdot)$ on the fixed closed parameter interval.

For the smooth-away-from-crest data used below, the same integral system preserves that local smoothness while $X_\xi>0$. Alternatively only its $C^1$ regularity and endpoint slopes are needed in the proof.

## 3. Uniform amplitude and crest-forcing estimates

Let $b(t,x)=\phi(x-ct)$ and $a_0=\|u_0-\phi\|_\infty$. For every characteristic solution just constructed, as long as it exists,

$$\|u(t,\cdot)-b(t,\cdot)\|_\infty\le a_0e^{At},\qquad
A:=\kappa+\frac\pi2=\frac52\kappa. \tag{7}$$

To verify this without differentiating the corner, follow a nonlinear characteristic $X(t,\xi)$ and set $h=V-b(t,X)$. The Lipschitz function $b$ is absolutely continuous along that characteristic. Almost everywhere in time its equation yields

$$h_t=(\partial_x^{-1}(u-b))(t,X)-b_x(t,X)h.$$

The chain rule holds off the crest. If a characteristic coincides with the crest on a time set of positive measure, its relative velocity there is zero almost everywhere on that set; the same identity follows with any bounded representative for $b_x$. Equivalently, one may use the standard Lipschitz chain rule and the traveling-wave identity $(\phi-c)\phi'=\partial_x^{-1}\phi$, whose two sides vanish at the crest. Integrating the absolute-value bound, using $|b_x|\le\kappa$ and (6), and taking the supremum over $\xi$ proves (7) by Gronwall's inequality.

Assume the transported corner starts at $q(0)=0$, and write $\zeta(t)=q(t)-ct$ as a continuous lift. Since $\phi(0)=c$ and $\phi$ is globally $\kappa$-Lipschitz on the periodic lift,

$$|\zeta'(t)|\le\kappa|\zeta(t)|+a_0e^{At}.$$

Consequently,

$$|\zeta(t)|\le\frac{a_0}{A-\kappa}(e^{At}-e^{\kappa t}),$$

and the true crest forcing obeys

$$|u(t,q(t))-c|\le\frac53a_0e^{At}. \tag{8}$$

These estimates need no smallness assumption on the spatial slope beyond its boundedness on the existing solution interval.

## 4. Narrow initial perturbations and fixed orbital departure

Choose a fixed smooth cutoff $\rho$ on $[0,\infty)$ with $\rho=1$ near zero, $0\le\rho\le1$, and $\rho=0$ for arguments at least one. Choose a fixed smooth function $\beta$, supported strictly inside $(L/3,2L/3)$, with $\int_0^L\beta=1$.

For small $\delta>0$, set $\eta=\delta^2$ and

$$v_\delta^0(x)=-\delta x\rho(x/\eta),\qquad
v_\delta=v_\delta^0-\left(\int_0^L v_\delta^0\right)\beta,\qquad
u_{0,\delta}=\phi+v_\delta.$$

The correction enforces zero mean and is supported away from the crest. The initial data agree continuously at the endpoints, and

$$u_{0,\delta}(0)=c,\quad u_{0,\delta}'(0^+)=-\kappa-\delta,\quad
u_{0,\delta}'(L^-)=\kappa.$$

There are constants $C_0,C_1$, independent of small $\delta$, for which

$$\|v_\delta\|_\infty\le C_0\delta^3,\qquad
\|v_\delta\|_{W^{1,\infty}}\le C_1\delta. \tag{9}$$

Indeed, the first term has amplitude at most $\delta\eta$, derivative bounded by a fixed multiple of $\delta$, and integral bounded by $\delta\eta^2/2$. The mean correction has still smaller amplitude and derivative. Notice that small second derivatives are neither claimed nor required.

Let $y=w_++\kappa$. Equations (5) and $c=\kappa^2$ give

$$y'=2\kappa y-y^2+[u(t,q(t))-c],\qquad y(0)=-\delta.$$

Dropping the nonpositive term $-y^2$ and applying (8)–(9) yields, throughout the interval of existence,

$$e^{-2\kappa t}y(t)
\le-\delta+\frac{5C_0\delta^3}{3(A-2\kappa)}
\bigl(e^{(A-2\kappa)t}-1\bigr). \tag{10}$$

Fix any small constant $\varepsilon_*>0$, for example $\varepsilon_*=\kappa/10$, and put

$$T_\delta=\frac{1}{2\kappa}\log\frac{2\varepsilon_*}{\delta}.$$

For sufficiently small $\delta$, this is positive. Since $A-2\kappa=\kappa/2$, the positive error on the right of (10), at every $t\le T_\delta$, is bounded by a constant times

$$\delta^3(2\varepsilon_*/\delta)^{1/4}=O(\delta^{11/4})=o(\delta).$$

In particular it is at most $\delta/2$. If the solution exists through $T_\delta$, then

$$y(T_\delta)\le-\frac\delta2e^{2\kappa T_\delta}=-\varepsilon_*,$$

so its right crest slope is at most $-\kappa-\varepsilon_*$.

If the slope norm reaches $\kappa+\varepsilon_*$ earlier, use its first hitting time. Otherwise it remains bounded by that constant, and the continuation criterion forces existence through $T_\delta$, when the preceding estimate supplies a hitting time. Thus in all cases there is a time $t_\delta\le T_\delta$, still within the solution's existence interval, with

$$\|u_x(t_\delta)\|_\infty\ge\kappa+\varepsilon_*.$$

For every translate of the traveling profile,

$$\|u_x(t_\delta)-\phi'(\cdot-\theta)\|_\infty
\ge\|u_x(t_\delta)\|_\infty-\|\phi'\|_\infty\ge\varepsilon_*.$$

This is uniform in $\theta$, proves the theorem, and avoids an assumption that the optimal orbital phase has to align the two corners. $\square$

## 5. What this result does and does not establish

The argument gives nonlinear **gradient** instability in a solution class that contains the peaked wave and arbitrarily small strong-norm perturbations. It proves local existence and the needed continuation statement directly, rather than applying a smooth Sobolev theorem outside its domain. It does not deduce nonlinear instability merely from linear or spectral instability.

It leaves open whether the orbit is nonlinearly stable or unstable in $L^2$ or $H^1$, for a specified global solution concept. The very narrow perturbations in (9) explain the gap: a fixed slope departure on a shrinking spatial region need not produce a fixed weaker-norm departure. Nor does the proof show finite-time blow-up, uniqueness of arbitrary weak continuations after breakdown, or instability under a strictly smoother norm excluding the peak.

The [2019 linear paper](https://pelinovsky.mcmaster.ca/PaperBank/PeakedWaveOstrov.pdf) and [2020 spectral paper](https://pelinovsky.mcmaster.ca/PaperBank/PeakedSpectralUnstable.pdf) are credited for the established background, not claimed as proof of this nonlinear result. The [2025 Natali–Pelinovsky–Wang paper](https://arxiv.org/abs/2503.15071) proves gradient instability for a different Hunter–Saxton-related model; it is relevant methodological prior work, but its theorem cannot be substituted for (1).

A bounded current-source search did not locate this exact strong-norm reduced-Ostrovsky theorem. That negative search does not establish novelty or priority. The appropriate disposition is a **candidate for the explicitly scoped nonlinear strong-norm theorem, with the weaker-norm source question not declared solved**.
