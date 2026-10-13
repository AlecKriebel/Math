# Strong path convergence for bounded nonlinear EKI, and a moment-estimate obstruction

**30003935 / OWR-16413-006. Scoped partial result; the original general nonlinear problem remains unresolved. Two substantive approaches. Separate review pending; no historical-priority or human-peer-review claim.**

For a bounded, locally Lipschitz forward map in finite-dimensional parameter space, the exact stochastic ensemble Kalman inversion scheme converges in the strong path norm
\[
\mathbb E\sup_{0\le t\le T}\|Y_h(t)-U(t)\|^q\longrightarrow0
\]
for every \(q\ge2\) for which the common initial ensemble has a finite \(q\)-th moment. The bounded-forward restriction is essential to the argument given here. A smooth globally Lipschitz, unbounded forward map exhibits quartic positive growth of the standard quadratic Lyapunov function, so the same uniform linear-growth proof does not extend automatically.

## 1. Original model, norm distinction and prior results

Schillings's contribution in [OWR 38/2018, printed pp.2341–2343](https://ems.press/content/serial-article-files/46760), joint with Blömker, Stuart, Wacker and Weissmann, uses a fixed finite ensemble, a separable-Hilbert parameter space, finite-dimensional Gaussian observation noise, and independent Brownian observation perturbations. It asks about the time-step limit to the covariance-driven stochastic system. It does not specify an \(L^q\) exponent or the position of the time supremum. The present theorem explicitly uses finite-dimensional parameter space and the norm displayed above. It concerns \(h\to0\) on a fixed interval, not \(J\to\infty\), long-time optimization, or posterior consistency.

The published [Blömker–Schillings–Wacker–Weissmann paper, SIAM J. Numer. Anal. 60 (2022), 3181–3215](https://doi.org/10.1137/21M1437561), was read in its [full institutional copy](https://d-nb.info/1290144702/34). Theorem 3.2 gives path convergence in probability for globally Lipschitz forward maps. Theorem 3.5 supplies a conditional moment theorem, and the linear cases establish the required moments in specified ranges. Their strong-moment statements place \(\sup_t\) outside expectation; Remark 2.13 discusses exchanging it. Remark 3.4 discusses cutoff forward maps. These results and the localization/moment method are prior work, not discoveries of this attempt.

The earlier [2018 scalar-model paper](https://doi.org/10.1137/17M1132367) is identified for historical scope only; its title does not prove the general nonlinear claim. A bounded current-primary-source search did not establish a full later solution of the exact target. No claim of an exhaustive literature search is made.

## 2. Exact stochastic scheme and bounded-forward theorem

Let \(J\ge2\) be fixed, with parameters in \(\mathbb R^p\), observations in \(\mathbb R^K\), fixed data \(y\), and positive-definite observation covariance \(\Gamma\). Assume
\[
G:\mathbb R^p\to\mathbb R^K
\quad\text{is locally Lipschitz and bounded.}
\]
Whiten observations by setting \(H=\Gamma^{-1/2}G\), \(z=\Gamma^{-1/2}y\), and choose \(M<\infty\) with \(\|H(x)\|\le M\). For \(U=(u^1,\ldots,u^J)\), put
\[
\bar u=J^{-1}\sum_j u^j,\qquad \bar H=J^{-1}\sum_jH(u^j),
\]
\[
C(U)=J^{-1}\sum_j(u^j-\bar u)(H(u^j)-\bar H)^T,\qquad
S(U)=J^{-1}\sum_j(H(u^j)-\bar H)(H(u^j)-\bar H)^T .
\tag{1}
\]
Let \(W^1,\ldots,W^J\) be independent \(K\)-dimensional Brownian motions, independent of the initial ensemble \(U_0\). Use their actual increments to couple all step sizes.

The continuous system is
\[
du^j=C(U)(z-H(u^j))\,dt+C(U)\,dW^j.
\tag{2}
\]
For \(h>0\), the exact discrete EKI update is
\[
u^j_{n+1}=u^j_n+hC(U_n)R_h(U_n)(z-H(u^j_n))
                 +C(U_n)R_h(U_n)\Delta W^j_n,
\quad R_h(U)=(I+hS(U))^{-1}.
\tag{3}
\]
This is the original update with observation perturbation covariance \(h^{-1}\Gamma\): \(\Delta W_n^j\sim N(0,hI)\). Whitening the gain is an exact identity, not a different numerical method.

Write \(f,g\) for the stacked drift and block-diagonal diffusion in (2), and \(f_h,g_h\) for those in (3). The interpolation is
\[
Y_h(t)=U_0+\int_0^t f_h(Y_h(\eta_h(s)))\,ds
             +\int_0^t g_h(Y_h(\eta_h(s)))\,dW(s),
\quad \eta_h(s)=h\lfloor s/h\rfloor .
\tag{4}
\]
It agrees with (3) at grid times. The norm on the ensemble is
\(\|U\|^2=\sum_j\|u^j\|^2\).

**Theorem 1.** For every fixed \(T<\infty\) and \(q\ge2\), if
\(\mathbb E\|U_0\|^q<\infty\), then (2) has a unique global strong solution and
\[
\lim_{h\downarrow0}\mathbb E\sup_{t\in[0,T]}
                 \|Y_h(t)-U(t)\|^q=0.
\tag{5}
\]
No convergence rate is asserted. Constants may depend on \(T,J,p,K,\Gamma,M,y,q\) and the local Lipschitz bounds. They are uniform in the step size. The theorem covers bounded nonlinear maps without compact support, for example componentwise hyperbolic tangents.

## 3. Uniform bounds and proof

The empirical variance identities and Cauchy–Schwarz give
\[
\sum_j\|u^j-\bar u\|^2\le\|U\|^2,\qquad
\sum_j\|H(u^j)-\bar H\|^2\le JM^2,
\]
and hence
\[
\|C(U)\|_{\rm HS}\le M\|U\|/\sqrt J,\qquad
0\preceq S(U),\quad\|S(U)\|\le M^2.
\tag{6}
\]
Thus \(\|R_h\|\le1\) and \(\|R_h-I\|\le hM^2\). In stacked form,
\[
\|f_h(U)\|\le M(\|z\|+M)\|U\|,
\qquad
\|g_h(U)\|_{\rm HS}\le M\|U\|,
\tag{7}
\]
with the same bounds for \(f,g\). Moreover
\[
\|f_h(U)-f(U)\|+\|g_h(U)-g(U)\|_{\rm HS}
 \le Ch\|U\|.
\tag{8}
\]
All coefficients are locally Lipschitz, uniformly on each bounded set for \(0<h\le1\). In particular \(f(0)=g(0)=f_h(0)=g_h(0)=0\).

**Moment bounds.** Local Lipschitz continuity and the linear-growth bounds give a unique nonexplosive strong solution to (2). Applying the usual localized Itô/BDG estimates and Gronwall, for every \(r\ge2\),
\[
\mathbb E\sup_{t\le T}\|U(t)\|^r
+\sup_{0<h\le1}\mathbb E\sup_{t\le T}\|Y_h(t)\|^r
 \le C_{r,T}\mathbb E\|U_0\|^r
\tag{9}
\]
whenever the right side is finite.

For completeness, (4), the inequality for the \(r\)-th power of a sum, Hölder's inequality for the drift integral, and BDG for the stochastic integral bound the left running maximum by
\[
C\mathbb E\|U_0\|^r+
C_{r,T}\int_0^t\mathbb E\sup_{v\le s}\|Y_h(v)\|^r\,ds.
\]
Here the grid value at \(\eta_h(s)\) is bounded by that running maximum; (7) is uniform in \(h\). Gronwall proves the discrete-interpolation part. The same estimate with no grid rounding gives the continuous part, first stopped and then with stopping removed by monotone convergence. For \(r=2\), the stopped estimate also bounds exit probabilities by \(C/R^2\), proving nonexplosion. No bounded-state or invariant-box assertion is used.

**Stopped error.** Let
\[
\sigma_R=\inf\{t:\|U(t)\|\vee\|Y_h(t)\|\ge R\}\wedge T .
\]
On this interval all local Lipschitz constants are finite. From (7) and Itô isometry, the stopped within-step increments satisfy
\[
\int_0^T
 \mathbb E\!\left[
 1_{\{s\le\sigma_R\}}\|Y_h(s)-Y_h(\eta_h(s))\|^2
 \right]ds\le C_{R,T}h.
\tag{10}
\]
Indeed on \(\{s\le\sigma_R\}\) the increment equals the stopped drift and stochastic integrals over that grid interval; their bounded integrands give \(O(h^2)+O(h)\). Removing the indicator by using those stopped integrals only increases the bound.

Subtract (2) from (4), add and subtract the coefficients at \(Y_h(s)\), and use (8), (10), the local Lipschitz estimate, BDG and Gronwall. This gives
\[
\mathbb E\sup_{t\le T}
 \|U(t\wedge\sigma_R)-Y_h(t\wedge\sigma_R)\|^2
 \le C_{R,T}h
\tag{11}
\]
for \(0<h\le1\). The initial values coincide. Formula (9) bounds the probability of exiting radius \(R\), uniformly in \(h\). Taking \(h\to0\) first and then \(R\to\infty\) proves
\[
\sup_{t\le T}\|Y_h(t)-U(t)\|\longrightarrow0
\quad\text{in probability}.
\tag{12}
\]

**Strong moments, including the initial-moment endpoint.** If \(U_0\) has a finite \(r\)-th moment with \(r>q\), (9) makes the \(q\)-th powers of the path errors uniformly integrable. Equation (12) then gives (5).

To remove the extra moment assumption, let
\(A_L=\{\|U_0\|\le L\}\) and \(U_0^L=1_{A_L}U_0\). The truncated initial value has every finite moment. Because the coefficients vanish at the zero ensemble, uniqueness and the common driving Brownian motion imply
\[
U^L=1_{A_L}U,\qquad Y_h^L=1_{A_L}Y_h.
\]
The same statement holds for the complementary initial value \(1_{A_L^c}U_0\). Applying (9) to that complementary system gives
\[
\sup_h\mathbb E\!\left[
1_{A_L^c}\sup_{t\le T}\|Y_h(t)-U(t)\|^q\right]
 \le C_{q,T}\mathbb E[1_{A_L^c}\|U_0\|^q]\longrightarrow0.
\tag{13}
\]
On \(A_L\), the already-proved higher-moment case applies. First let \(h\to0\), then \(L\to\infty\), to obtain (5) under exactly the claimed initial moment. This completes the proof. \(\square\)

## 4. Compact forward support does not create an invariant state box

The cutoff discussion in the 2022 paper must not be interpreted as a deterministic bound on all particle paths. The theorem above instead proves moment bounds.

Here is an exact one-step diagnostic. Take scalar parameters and observations, \(J=2\), \(\Gamma=1\), \(y=0\), initial values \((0,1/2)\), and
\[
G(x)=
\begin{cases}
\exp\!\left(1-\dfrac1{1-4x^2}\right),&|x|<1/2,\\
0,&|x|\ge1/2.
\end{cases}
\]
This is smooth and compactly supported. Its two initial values are \(1,0\), giving
\(C=-1/8\) and \(S=1/4\). The first updated particle has law
\[
u_1^1=\frac{h}{8(1+h/4)}
       -\frac{\sqrt h}{8(1+h/4)}\,\xi,\qquad \xi\sim N(0,1).
\tag{14}
\]
Its variance is positive for every \(h>0\), so its support is unbounded even though both initial particles lie in a fixed bounded interval and \(G\) vanishes outside one. This is fully compatible with Theorem 1 and its finite moments. It is not a counterexample to strong convergence or a claim about what the source intended by informal boundedness language.

## 5. The quadratic-moment route fails for general globally Lipschitz maps

A standard route to extend Theorem 1 would seek a quadratic Lyapunov bound
\(\mathcal LV\le C(1+V)\), or the matching uniform one-step estimate. Those estimates need not hold even for a smooth globally Lipschitz scalar forward map.

Choose a smooth \(G\) with \(G(x)=0\) for \(x\le0\), \(G(x)=x\) for \(x\ge1\), and bounded derivative in between. Such a map is obtained as \(G(x)=x\chi(x)\) with a smooth cutoff \(\chi\) from zero to one on \([0,1]\). Take \(J=2,\Gamma=1,y=0\), and
\[
U_R=(R,-aR),\qquad R\ge1,\quad a>3.
\]
Then \(G(U_R)=(R,0)\), and
\[
C(U_R)=\frac{1+a}{4}R^2,\qquad S(U_R)=\frac14R^2.
\]
For \(V(u^1,u^2)=(u^1)^2+(u^2)^2\), direct evaluation of the generator of (2) gives
\[
\mathcal LV(U_R)
=-2R^2C(U_R)+2C(U_R)^2
=\frac{(1+a)(a-3)}8R^4.
\tag{15}
\]
Since \(V(U_R)=(1+a^2)R^2\), there is no uniform constant in the proposed quadratic generator bound.

The exact discrete conditional energy change is
\[
\mathbb E[V(U_{n+1})-V(U_n)\mid U_n=U_R]
=
\frac{hR^4}{
 (1+hR^2/4)^2}
\left[
\frac{(1+a)(a-3)}8
+hR^2\frac{(1+a)(a-1)}{16}
\right].
\tag{16}
\]
For example \(a=5\) makes both coefficients \(3/2\). Choosing \(h=R^{-4}\) shows that no estimate
\[
\mathbb E[V(U_{n+1})\mid U_n=U]\le
V(U)+Ch(1+V(U))
\]
can hold with a single \(C\) for all states and all sufficiently small steps.

This map falls in the globally Lipschitz setting of the published probability-convergence result. Equations (15)–(16) do not prove moment divergence, explosion or failure of strong convergence. They identify the precise failure of the elementary quadratic-moment extension attempted here. A different Lyapunov function or additional structure may still control the true dynamics.

## 6. Exact remaining gap and classification

The two routes were: (1) bounded-forward linear-growth estimates, yielding Theorem 1; (2) extension of the quadratic-moment proof to general globally Lipschitz forward maps, blocked by (15)–(16). The second route is not relabeled as a counterexample to the original convergence question.

The unrestricted nonlinear source target, including meaningful assumptions for its Hilbert-space version and the intended strong norm, remains unresolved by this attempt. Published probability convergence and conditional moment theorems are retained as prior results. Recommended campaign status: **unsolved, 2/5**.

The exact verifier checks covariance normalization, gain whitening, moment-expansion algebra, the compact-support Gaussian diagnostic and the Lyapunov obstruction. It cannot certify stochastic convergence by finite sampling; the qualitative path-norm theorem rests on the proof above and the stated Itô, BDG, localization and Gronwall arguments.

