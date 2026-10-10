# Loss of total-space positivity for the normalized relative Kähler–Ricci flow

## Scope and result

This note concerns problem 30003571 / OWR-15582-005. The source distinction matters. The catalogue asks whether a relative flow can be defined on \(\mathcal O_E(r)\). Naumann already defines such a flow in the 2017 Oberwolfach report, equation (2), and in the published paper [N], equation (13). The remaining question in the report, printed page 2443, and [N], Section 3.3, printed page 1521, is whether that flow preserves positivity in **all** directions on the total space. Merely writing the flow does not resolve this question.

We give a counterexample to this preservation assertion. The initial metric is smooth and strictly positive on the compact total space of a projective-space fibration of an ample bundle. The evolved metric is still positive on each fiber, but has negative horizontal curvature at an explicitly specified positive time. This does not disprove the Griffiths conjecture or rule out other flow normalizations or other choices of initial metrics. No historical priority claim is made.

### Theorem

Let \(S=\mathbf P^1\), \(E=\mathcal O_S(1)\oplus\mathcal O_S(1)\), and let \(f:X=\mathbf P(E^*)\to S\) use the convention \(f_*\mathcal O_E(1)=E\). Then \(X\cong\mathbf P^1_s\times\mathbf P^1_z\) and

\[
L:=\mathcal O_E(2)\cong\mathcal O_{\mathbf P^1_s\times\mathbf P^1_z}(2,2).
\]

There is a smooth Hermitian metric \(e^{-\phi_0}\) on \(L\), with strictly positive curvature on \(X\), whose solution of Naumann's normalized flow

\[
\partial_t\phi_t=\log\frac{\operatorname{MA}(\phi_t)}{\mu_{\phi_t}}
\tag{1}
\]

has

\[
(\phi_t)_{s\bar s}(0,0)
=\frac1{96}-\frac1{24}(1-e^{-2t}).
\tag{2}
\]

Here \(s,z\) are standard affine coordinates, and \(\operatorname{MA}\) is the fiberwise curvature volume divided by its total mass. In particular, at \(t_*=(\log 2)/2\), the coefficient in (2) equals \(-1/96\). The positive square root metric on \(\mathcal O_E(1)\) supplies exactly an initial metric of the kind requested in the source.

## 1. The precise flow and its normalization

Fix a local nonvanishing holomorphic frame of \(\det E\). Via

\[
K_{X/S}^{-1}=L\otimes f^*(\det E)^{-1},
\]

the restriction of a metric on \(L\) gives on each fiber the relative anticanonical volume density. In compatible affine coordinates and frames, write this density as \(e^{-\phi}\,dA_z\), where the positive constant in \(dA_z\) is irrelevant. Put

\[
I(s)=\int_{\mathbf P^1_z}e^{-\phi(s,z)}dA_z,
\qquad
\mu_\phi=\frac{e^{-\phi}dA_z}{I(s)}.
\tag{3}
\]

The density is understood across the second coordinate chart using the anticanonical transformation rule. Changing the frame of \(\det E\) multiplies numerator and denominator by the same positive base factor, so (3) is intrinsic. Likewise adding any function of the base to \(\phi\) does not change either probability measure on a fiber.

For fiber dimension one, let \(g=\phi_{z\bar z}>0\). The mass of the curvature form on \(\mathcal O_{\mathbf P^1}(2)\) is independent of \(s\) and \(t\). Thus (1), in these frames, is

\[
\partial_t\phi=\log g+\phi+\log I+C,
\tag{4}
\]

where \(C\) is constant in \(s,z,t\). Changing the fixed convention for \(dd^c\) changes only \(C\). The coefficient of \(\phi\) in (4) is **one**. All subsequent evolution calculations follow directly from (4), rather than from a general geodesic-curvature formula with potentially different metric-scaling conventions.

The probability-volume convention in (1) is [N], equations (8), (10), and (13). If instead one uses the report's unnormalized fiber volume in the numerator, the right side differs by the constant logarithm of that volume. Adding the corresponding function of time to the solution changes no curvature coefficients, so the counterexample is the same.

We use the established existence fact stated in [N], Theorem 5, printed page 1519: for smooth fiberwise positive initial metrics, this flow exists smoothly on \(X\times[0,\infty)\). Its proof identifies the fiberwise flow with the normalized anticanonical Kähler–Ricci flow. Our argument needs only this finite-time smoothness, uniqueness, and preservation of fiberwise positivity; it does not use convergence or horizontal regularity of a limiting metric. These are classical parabolic existence inputs, not conclusions of the symbolic verification below.

For clarity, uniqueness and the symmetries needed here can also be seen directly. If two fiberwise solutions have difference \(v\), then
\[
|\log I(\phi)-\log I(\widetilde\phi)|\leq\|v\|_{C^0}
\]
on each fiber. At a spatial maximum of \(v\), the difference of the logarithmic Hessian terms is nonpositive. Applying the scalar maximum principle to \(v\) and \(-v\), followed by Grönwall's inequality, gives uniqueness for common initial data. The flow therefore respects any lifted holomorphic symmetry of that data. Smooth dependence on the base at finite times is included in the cited existence theorem; only derivatives of order two in the base will be used.

## 2. A globally defined strictly positive initial metric

Set

\[
\epsilon=\frac1{96},\qquad\delta=\frac14,\qquad
u=|s|^2,\quad v=|z|^2,\quad
p=\frac{u}{1+u},\quad x=\frac{v}{1+v}.
\]

On the finite affine chart define

\[
\phi_0(s,z)=2\log(1+u)+\frac{2-\epsilon}{1+u}
             +2\log(1+v)+\delta\frac{u}{1+u}
                         \left(\frac{v}{1+v}\right)^2.
\tag{5}
\]

### 2.1. Bundle identification and all charts

Writing \(A=\mathcal O_S(1)\), we have \(E=A\otimes\mathbf C^2\). Projectivizing cancels the scalar factor \(A^*\), giving the product description. The tautological quotient line is \(A\boxtimes\mathcal O_{\mathbf P^1}(1)\), so its square is \(L=\mathcal O(2,2)\). In particular \(E\) is ample: \(\mathcal O_E(1)=\mathcal O(1,1)\) is ample.

The first and third terms of (5) are the usual metric weights on \(\mathcal O(2,2)\). The other terms are globally smooth real functions: \(p\), \(1-p\), and \(x\) extend smoothly over their respective projective lines.

Explicitly, with \(w=1/s\), subtract the transition weight \(2\log|s|^2\). The first two terms become

\[
2\log(1+|w|^2)+(2-\epsilon)\frac{|w|^2}{1+|w|^2},
\]

and \(p\) becomes \((1+|w|^2)^{-1}\). With \(\zeta=1/z\), subtract \(2\log|z|^2\); the fiber term becomes \(2\log(1+|\zeta|^2)\), and \(x^2\) becomes \((1+|\zeta|^2)^{-2}\). These formulas are smooth also in the joint infinity chart. Thus (5) defines a genuine smooth Hermitian metric everywhere, not merely an affine-chart potential.

### 2.2. Positivity in every tangent direction

Normalize the complex Hessian by the product Fubini–Study frame. Its diagonal coefficients and squared off-diagonal modulus are

\[
\begin{aligned}
A&=(1+u)^2(\phi_0)_{s\bar s}
  =4p+(\epsilon+\delta x^2)(1-2p),\\
B&=(1+v)^2(\phi_0)_{z\bar z}
  =2+2\delta p x(2-3x),\\
Q&=(1+u)^2(1+v)^2|(\phi_0)_{s\bar z}|^2
  =4\delta^2p(1-p)x^3(1-x).
\end{aligned}
\tag{6}
\]

These expressions follow by differentiating (5). They are also intrinsic diagonal coefficients and an intrinsic modulus in local unit frames for the product reference metric; consequently their continuous expressions at \(p=1\) or \(x=1\) cover the infinity charts.

For \(p,x\in[0,1]\), elementary inequalities give

\[
A\geq\epsilon+(4-2\epsilon-2\delta)p
       =\epsilon+\frac{167}{48}p,
\qquad B\geq2-2\delta=\frac32,
\qquad Q\leq4\delta^2p=\frac p4.
\]

For the middle inequality, \(x(2-3x)\geq-1\) on \([0,1]\). For the first, expand \(A\) and use \(\delta x^2\geq0\) and \(x^2\leq1\). Therefore

\[
AB-Q\geq\frac32\epsilon+\frac{159}{32}p
          =\frac1{64}+\frac{159}{32}p>0.
\tag{7}
\]

Since \(B>0\) and the determinant is strictly positive, the Hessian is positive definite. The bounds hold on the closed square, so no degeneracy has been hidden at an infinity point. Dividing (5) by two supplies a smooth positive weight on \(\mathcal O_E(1)\), whose squared metric is precisely the metric in (5).

## 3. Exact horizontal second-variation equation

The initial metric and the equation are invariant under \(s\mapsto e^{i\theta}s\), using the natural lifted rotation action on the base line bundle. Uniqueness implies the same invariance at each finite time. In the fixed affine frames this gives, on the entire fiber \(s=0\),

\[
(\phi_t)_s=(\phi_t)_{\bar s}=(\phi_t)_{s\bar z}=0.
\tag{8}
\]

By (5), the central-fiber weight initially is

\[
\phi_0(0,z)=2\log(1+|z|^2)+2-\epsilon.
\]

Its normalized curvature volume and its normalized anticanonical volume are both the Fubini–Study probability measure. Thus its right side in (1) is zero. Fiberwise uniqueness yields

\[
\phi_t(0,z)=2\log(1+|z|^2)+2-\epsilon
\quad(t\geq0).
\tag{9}
\]

Write

\[
w(z,t)=(\phi_t)_{s\bar s}(0,z),\qquad
g_F=\frac{2}{(1+|z|^2)^2},\qquad
\Delta_F=\frac{(1+|z|^2)^2}{2}\partial_z\partial_{\bar z}.
\]

Differentiate (4) by \(\partial_s\partial_{\bar s}\) and restrict to \(s=0\). By (8), \(g_s=g_{\bar s}=0\), hence

\[
\partial_s\partial_{\bar s}\log g=g_F^{-1}w_{z\bar z}=\Delta_F w.
\]

Differentiating the integral (3), justified by smoothness and compactness of the fiber, gives

\[
I_s=0,\qquad
I_{s\bar s}=\int\bigl(|\phi_s|^2-\phi_{s\bar s}\bigr)e^{-\phi}dA_z
          =-I\int w\,\mu_F.
\]

Consequently

\[
\partial_s\partial_{\bar s}\log I=-\int w\,\mu_F,
\]

and the exact, closed evolution is

\[
\partial_t w=\Delta_F w+w-\int_{\mathbf P^1}w\,\mu_F,
\qquad w(z,0)=\epsilon+\delta x^2.
\tag{10}
\]

This is an identity for the second derivative of the actual nonlinear solution. It is not a first-order-in-time approximation or a numerical linearization. The closure holds because the central fiber is exactly stationary and all first base derivatives vanish identically there.

For the usual geodesic curvature (Schur complement),

\[
c(\phi_t)=(\phi_t)_{s\bar s}
 -\frac{|(\phi_t)_{s\bar z}|^2}{(\phi_t)_{z\bar z}},
\]

equation (8) shows that \(c(\phi_t)=w\) on this central fiber. In particular, a negative value of \(w\) is a negative value of the curvature on the actual vector \(\partial/\partial s\).

## 4. Solution of the closed equation

The pushforward of \(\mu_F\) by \(x=|z|^2/(1+|z|^2)\) is ordinary Lebesgue measure on \([0,1]\). Indeed radial integration reduces, after angular normalization, to \(dv/(1+v)^2=dx\). For a smooth function \(F(x)\), direct differentiation gives

\[
\Delta_F F=\frac12\left[x(1-x)F''+(1-2x)F'\right].
\tag{11}
\]

Put

\[
P_1(x)=2x-1,\qquad P_2(x)=6x^2-6x+1.
\]

Then

\[
\int_0^1P_1dx=\int_0^1P_2dx=0,\quad
\Delta_FP_1=-P_1,\quad\Delta_FP_2=-3P_2,
\]

and

\[
x^2=\frac13+\frac12P_1(x)+\frac16P_2(x).
\tag{12}
\]

It follows that the solution of (10) is

\[
w(x,t)=\epsilon+\frac\delta3
       +\frac\delta2 P_1(x)
       +\frac\delta6 e^{-2t}P_2(x).
\tag{13}
\]

For completeness, uniqueness of (10) follows by integrating the equation for the difference of two solutions. Its mean has zero derivative, so zero initial difference has zero mean for all times. The difference then solves \(v_t=\Delta_Fv+v\) with zero initial data; the maximum principle applied to \(e^{-t}v\) gives \(v=0\). Thus checking (13) in the equation and at time zero establishes it for the actual curvature coefficient.

At \(z=0\), \(x=0\), \(P_1=-1\), and \(P_2=1\), which gives (2). Taking \(t_*=(\log2)/2\),

\[
c(\phi_{t_*})(0,0)=w(0,t_*)
=\frac1{96}-\frac{1/4}{12}=-\frac1{96}<0.
\]

All initial data were strictly positive, the time is finite, and the underlying bundle and base are compact. This proves the theorem. In fact the coefficient becomes negative whenever \(t>\frac12\log(4/3)\).

## 5. What has and has not been established

* The normalized flow on \(\mathcal O_E(r)\) was already constructed in the cited sources. The catalogue's literal existence question is therefore not a new open assertion.
* The positivity-preservation question explicitly left open in those sources has the negative answer exhibited above for the exact probability-normalized flow (1).
* The example starts with a positive metric on \(\mathcal O_E(1)\) and uses its square, so it does not evade the source's initial-data requirement.
* No argument about a limit as \(t\to\infty\), no singular-fiber phenomenon, no noncompact base, and no zero-curvature initial tangent direction is used.
* The example does not address whether some other initial metric or a changed horizontal normalization could be useful for Griffiths positivity. The bundle used here already admits Griffiths-positive metrics.

## References

[O] P. Naumann, **An approach to the Griffiths conjecture**, contribution to *Komplexe Analysis*, Oberwolfach Reports 14 (2017), no. 3, especially pp. 2440–2443. DOI: [10.4171/OWR/2017/39](https://doi.org/10.4171/OWR/2017/39). [Publisher report](https://ems.press/content/serial-article-files/46702?nt=1).

[N] P. Naumann, **An approach to the Griffiths conjecture**, Mathematical Research Letters 28 (2021), no. 5, 1505–1523. DOI: [10.4310/MRL.2021.v28.n5.a10](https://doi.org/10.4310/MRL.2021.v28.n5.a10). Relevant parts: Section 3.1, Theorems 3–4; Section 3.2, equation (13), Theorem 5 and its proof; Section 3.3. [Publisher full text](https://intlpress.com/api/bgcloud-front/resource/pdf/volume/1806601940286992386-1806601940286992386-fb415fcde747f9c588db3e8aababba9d.pdf). Earlier version: [arXiv:1710.10034](https://arxiv.org/abs/1710.10034).

[B] R. J. Berman, **Relative Kähler–Ricci flows and their quantization**, Analysis & PDE 6 (2013), no. 1, 131–180. DOI: [10.2140/apde.2013.6.131](https://doi.org/10.2140/apde.2013.6.131). [arXiv:1002.3717](https://arxiv.org/abs/1002.3717). This supplies background for [N]; the counterexample does not invoke Berman's positivity results for other normalizations.
