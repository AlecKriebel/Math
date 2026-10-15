# Independent source/PDE derivation

Audit of PR 248, problem 30004630 / OWR-4990378-001, pinned submitted head `e9c5d10978764db2cf25fa7d49cf4bd14a82d604`. Initial derivation recorded on 2026-10-14 UTC before reading the submitted independent-review verdict. This is an adversarial reconstruction, not an acceptance of its algebra receipts or earlier PASS labels.

## Exact proposition under test

Let B be the open unit ball in R^3, H=L^2(B), E=H_0^1(B)×H, T=1, zero initial data, homogeneous Dirichlet boundary, and

\[
y_{tt}-\Delta y+y^5=u,\qquad \|u(t)\|_H\leq\rho.
\]

For fixed ν≥0 define

\[
J_d(u)=\tfrac12\|y_u(1)-d\|_H^2
+\tfrac\nu2\|(y_u)_t(1)\|_{H^{-1}}^2
+\tfrac14\|y_u\|_{L^4L^{12}}^4+\|u\|_{L^1H}.
\]

The target is d=πe, where e is the H-normalized first radial Dirichlet mode. The candidate asserts that some fixed ρ>0 gives a unique global zero minimizer, C(0)={0}, no local L^2-squared growth, and a failure of Lipschitz L^2-control response to d_ε=(π+ε)e. None of these is assumed in the reconstruction below. The source estimates are classical inputs; mathematical novelty and literature priority are separate questions.

## 1. Geometry and the classical estimate actually needed

For r=|x|,

\[
e(x)=\frac{\sin(\pi r)}{\sqrt{2\pi}\,r},\quad
e(0)=\frac\pi{\sqrt{2\pi}}.
\]

The series of sin(πr)/r contains only even powers of r, hence is smooth as a function of x at the origin. It is smooth on the closed ball, vanishes on r=1, and belongs to H_0^1. Direct radial differentiation gives Δe=−π²e; moreover

\[
4\pi\int_0^1e(r)^2r^2\,dr
=2\int_0^1\sin^2(\pi r)\,dr=1.
\]

No invariant one-mode nonlinear ansatz is used: e^5 is generally not proportional to e. Only the *linear* endpoint is calculated in this mode; the nonlinear remainder is controlled in the full space.

Write X for the Banach space of zero-data positions whose pair (y,y_t) is continuous in E, with y∈L^4(0,1;L^{12}), norm

\[
\|y\|_X=\|(y,y_t)\|_{C(E)}+\|y\|_{L^4L^{12}}.
\]

The linear Duhamel map L satisfies

\[
\|Lf\|_X\le M\|f\|_{L^1H}.
\]

This is precisely the zero-data consequence of [Kunisch–Meinlschmidt, arXiv v1, Lemma 2.9, printed p.8](https://arxiv.org/pdf/1907.02744v1); the pinned author preprint has the same estimate. It applies on this smooth bounded ball over fixed T=1, with finite constants depending only on domain and interval. It makes no assumption that forcing is smooth, separated, or spread over a minimum interval.

For y∈X, spatial interpolation at each time gives

\[
\|y(t)\|_{10}\le \|y(t)\|_{12}^{4/5}\|y(t)\|_6^{1/5},
\quad \|y\|_{L^5L^{10}}^5
\le \|y\|_{L^4L^{12}}^4\|y\|_{L^\infty L^6}
\le D\|y\|_X^5.
\]

Thus N(y)=y^5 maps X to L^1H and is locally Lipschitz:

\[
\|y^5-w^5\|_{L^1H}
\le 5(\|y\|_{L^5L^{10}}+\|w\|_{L^5L^{10}})^4
\|y-w\|_{L^5L^{10}}
\le D_1(\|y\|_X+\|w\|_X)^4\|y-w\|_X.
\]

The first inequality follows from the real polynomial identity and Hölder with five factors in L^5 in time and L^{10} in space. The interpolation applies to differences as well.

For A=∥u∥_{L^1H}, use Φ(y)=L(u−y^5) on the closed X-ball of radius R=2MA. Choose a_0>0 so that for every A≤a_0 both MD R^5≤MA and MD_1(2R)^4<1/2. Then Φ maps the ball into itself and is a contraction. At A=0 the zero solution is immediate. There are constants C,C_5 independent of u, A, and ρ such that

\[
\|y_u\|_X\le CA,\qquad
\|y_u-z_u\|_X=\|L(-y_u^5)\|_X\le C_5A^5,
\quad z_u=Lu.
\]

The fixed point satisfies the full Duhamel equation and is therefore a mild solution in the source sense. It agrees with its unique mild/Shatah–Struwe solution; uniqueness can also be shown by subdividing time until each pair of L^5L^{10} norms is small and applying the difference estimate on each interval. This prevents substitution of a weak solution outside the dispersive class. The bound is uniform on *all* admissible controls once ρ≤a_0, because A≤ρ on [0,1]. Concentration does not break this estimate.

Continuous embeddings H_0^1→H and H→H^{-1} give endpoint versions of the same A^5 remainder. Under the gradient norm convention, ∥e∥_{H^{-1}}=1/π; the proof only needs a finite embedding constant, so alternative equivalent H^{-1} norms do not affect it.

## 2. Independent global optimality estimate

Self-adjointness of the wave propagator and −Δe=π²e give

\[
(e,z_u(1))_H=\frac1\pi\int_0^1\sin(\pi(1-t))(e,u(t))_H\,dt
=\frac1\pi\int_0^1\sin(\pi t)(e,u(t))_H\,dt.
\]

Let f(t)=∥u(t)∥_H, A=∫f. Expanding the square around zero and discarding three nonnegative costs yields

\[
J_{\pi e}(u)-J_{\pi e}(0)
\ge A-\pi(e,y_u(1))_H
\ge \int_0^1(1-\sin(\pi t))f(t)\,dt-C_0A^5.
\]

Here the projection estimate is valid for arbitrary sign and spatial profile of u, since 0≤sin(πt)≤1 and (e,u(t))≤f(t). C_0 can be fixed before choosing ρ.

For s=t−1/2, concavity of sin on [0,π/4] implies sin(π|s|/2)≥√2|s|, hence

\[
1-\cos(\pi s)=2\sin^2(\pi s/2)\ge2s^2\qquad(|s|\le1/2).
\]

For 0<A≤ρ put r=A/(2ρ). The density f_*(s)=ρ1_{|s|<r} has mass A. Pointwise,

\[
(s^2-r^2)(f(s+1/2)-f_*(s))\ge0.
\]

Integrating and cancelling the equal mass terms gives

\[
\int_{-1/2}^{1/2}s^2f(s+1/2)\,ds
\ge\frac{2\rho r^3}{3}=\frac{A^3}{12\rho^2}.
\]

The A=0 case is trivial. Thus

\[
J_{\pi e}(u)-J_{\pi e}(0)
\ge\frac{A^3}{6\rho^2}-C_0A^5
\ge\frac{A^3}{12\rho^2}>0\quad(A>0),
\]

provided ρ≤a_0 and C_0ρ^4≤1/12. Both requirements admit a fixed positive ρ. They require no certified numerical value of a classical constant. This establishes uniqueness over the whole U_ad. It uses the amplitude cap essentially; the uncapped problem has not been proved equivalent.

## 3. Cone, nonsmooth derivative, and second variation

At u=0 the tangent cone is all L^rH, including r=1 used for β_2=0 in the paper. This is not a claim that U_ad has an L^1 or L^2 interior. For an arbitrary v in either space, truncate its magnitude to obtain bounded v_n→v; for sufficiently small τ_n>0, τ_nv_n∈U_ad. This proves the closure-of-radial-directions assertion directly.

The smooth part has first derivative

\[
F'(0)v=-\int_0^1\sin(\pi t)(e,v(t))_H\,dt.
\]

The terminal velocity square and quartic state penalty have zero first derivative at the zero state. The source subgradient can be chosen λ(t)=sin(πt)e, with ∥λ(t)∥≤1, so p+λ=0 and the pointwise ball multiplier is zero. The complete directional derivative obeys

\[
J'(0;v)=\int_0^1[\|v(t)\|_H-\sin(\pi t)(e,v(t))_H]dt
\ge\int_0^1[1-\sin(\pi t)]\|v(t)\|_Hdt>0
\]

for every nonzero equivalence class v. A function supported only at t=1/2 is zero in every stated L^r space. Therefore C(0)={0} exactly. This also covers a formulation using r=2.

The source defines the substitute j'' to be zero at u=0. It is not the ordinary second derivative of j. The smooth part at zero has

\[
F''(0)[v,v]=\|z_v(1)\|_H^2+\nu\|(z_v)_t(1)\|_{H^{-1}}^2.
\]

The nonlinear state map has zero second derivative at zero, and the state norm fourth power has zero second derivative there. Thus the substitute is well-defined. The strict source condition on C(0)\{0} holds vacuously. No positivity on a nonzero direction or enlarged approximate cone has been established or implied.

## 4. Exact pulse calculation and nonlinear error orders

Take 0<h<min(ρ,1/2), u_h=h e1_{|t−1/2|<h}. It is feasible, ∥u_h∥_∞=h, A_h=2h², and ∥u_h∥_2²=2h³. The linear state remains in span(e), with

\[
z_{u_h}(1)=b_he,\quad b_h=\frac{2h\sin(\pi h)}{\pi^2},\quad
(z_{u_h})_t(1)=0.
\]

The velocity integral is odd about t=1/2. The linear first-order gap is

\[
D_h=h\int_{-h}^h(1-\cos(\pi s))ds
=2h^2-\frac{2h\sin(\pi h)}\pi
=\frac{\pi^2}{3}h^4+O(h^6).
\]

For the true nonlinear state r_h=y_{u_h}−z_{u_h}, ∥r_h∥_X=O(h^{10}). Expanding the terminal square gives

\[
\tfrac12\|y_{u_h}(1)\|^2-\pi(e,r_h(1))
=\tfrac12b_h^2+O(h^{10}).
\]

The quartic state cost is O(h^8). The velocity cost is O(h^{20}), because its linear velocity vanishes and its nonlinear velocity is O(h^{10}). For every fixed ν≥0,

\[
J_{\pi e}(u_h)-J_{\pi e}(0)
=\left(\frac{\pi^2}{3}+\frac{2}{\pi^2}\right)h^4+O(h^6),
\]

where the state penalty and remainder are of higher order than the displayed h^6 error. The prior global lower bound ensures nonnegativity. Consequently

\[
\frac{J_{\pi e}(u_h)-J_{\pi e}(0)}{\|u_h\|_2^2}
=\left(\frac{\pi^2}{6}+\frac1{\pi^2}\right)h+O(h^3)\to0.
\]

This is a genuine nonlinear PDE counterexample; the exact finite calculations alone would not prove it. Since both L^∞ and L^2 norms tend to zero, it contradicts growth under either localization.

There is an explicit loss of compact coercivity: w_h=u_h/∥u_h∥_2 has L^2 norm one but tends weakly to zero. For any φ∈L^2H,

\[
|(w_h,\phi)_{L^2H}|\le\|\phi1_{|t-1/2|<h}\|_{L^2H}\to0.
\]

Hence the normalized concentrating directions disappear in the critical-cone weak limit. This is the precise difficulty which the β_2>0 term controls in the source proof.

## 5. Direct method including the report's optional velocity term

Fix ε in a bounded interval and take a minimizing sequence u_n for target d_ε. U_ad is bounded in Hilbert L^2H, convex, and norm closed: under strong L^2 convergence select a subsequence converging in H almost everywhere, then pass the pointwise cap to the limit. Hence it is weakly compact and weakly closed. Pass to u_n⇀u in L^2H with u∈U_ad.

The uniform X bound gives y_n bounded in L^∞H_0^1 and (y_n)_t bounded in L^∞H. The equation gives a stronger equicontinuity bound than merely a bounded L^1 derivative:

\[
\|(y_n)_{tt}\|_{L^\infty H^{-1}}
\le C\left(\|y_n\|_{L^\infty H_0^1}
+\|y_n\|_{L^\infty L^6}^5+\rho\right)<C_*.
\]

This uses L^{6/5}→H^{-1}, H_0^1→L^6, and the pointwise L^∞H control cap. Thus y_n is uniformly Lipschitz into H, and (y_n)_t uniformly Lipschitz into H^{-1}. The compact embeddings H_0^1 compactly into H and H compactly into H^{-1}, followed by Banach-valued Arzelà–Ascoli, give a common subsequence with

\[
y_n\to y\quad\hbox{in }C([0,1];H),\qquad
(y_n)_t\to v\quad\hbox{in }C([0,1];H^{-1}).
\]

Weak-* subsequences retain the L^∞ energy bounds. Distributional differentiation yields v=y_t; endpoints give y(0)=0 and y_t(0)=0 in H and H^{-1}. A further subsequence has y_n→y almost everywhere in spacetime.

The sequence y_n^5 is bounded in L^∞L^{6/5}, hence in reflexive spacetime L^{6/5}. Its weak limit equals y^5: boundedness in L^p with p>1 plus almost-everywhere convergence identifies the weak limit by truncation/uniform integrability. This suffices to pass every compactly supported smooth test function in the weak wave equation. The weak L^4L^{12} limit is also y, by uniqueness of the distributional limit, so y retains that bound. Together with L^∞L^6, interpolation gives y^5∈L^1H.

To make the weak-to-mild step explicit, let \(\tilde y=L(u-y^5)\), which is a continuous-energy linear mild solution. The difference y−\(\tilde y\) solves the homogeneous Dirichlet wave equation distributionally with zero initial position and velocity and bounded energy. Expanding against the Dirichlet eigenbasis, each coefficient solves a zero-data scalar harmonic oscillator and is identically zero. Completeness gives y=\(\tilde y\). Thus y satisfies the nonlinear Duhamel equation, lies in X, and is the unique mild solution associated with u. This avoids assuming mere energy weak uniqueness at critical exponent.

Both endpoint costs are continuous under the two displayed strong convergences, including the ν-term for any fixed ν≥0. The L^4L^{12} norm fourth power is weakly lower semicontinuous. The control L^1H norm is convex and norm-continuous on L^2H (difference bounded by ∥u−w∥_2 on T=1), hence weakly lower semicontinuous there. The limiting control minimizes J_{d_ε}.

The cap being constant is decisive for the L^∞H^{-1} bound used here. No claim is made that an arbitrary merely integrable source radius would give the same Lipschitz equicontinuity. For ν=0 the source's existence theorem also applies, but it is not required as a black-box extension to ν>0.

## 6. Target perturbation: existence and every-optimizer quantifier

Set a=ρ/2 once and for all, h_ε=πε/(2a), and

\[
v_ε=a e1_{|t−1/2|<h_ε}.
\]

For sufficiently small ε>0 it is feasible and A=2ah_ε=πε. Its linear endpoint b_εe has b_ε=2a sin(πh_ε)/π²=ε+O(ε³), and zero velocity. Its baseline first-order gap is O(ε³), nonlinear endpoint error is O(ε^5), and quartic cost is O(ε^4). The identity

\[
J_{d_ε}(v_ε)-J_{d_ε}(0)
=J_{\pi e}(v_ε)-J_{\pi e}(0)-ε(e,y_{v_ε}(1))
=-\tfrac12ε^2+O(ε^3)
\]

therefore gives a feasible objective improvement at most −ε²/4.

For arbitrary feasible u, put r=∥u∥_2 and A≤r. As before, dropping nonnegative costs gives

\[
J_{d_ε}(u)-J_{d_ε}(0)
\ge-\int_0^1g_ε(t)\|u(t)\|_Hdt-C_2A^5
\ge-\|g_ε\|_2r-C_2r^5,
\]

where \(g_ε=[(1+ε/π)\sin(πt)-1]_+\). On |s|≤1/2,

\[
g_ε(s+1/2)\le(ε/π-2s^2)_+,
\quad\|g_ε\|_2\le2^{1/4}\pi^{-5/4}ε^{5/4}.
\]

For every fixed K, controls with r≤Kε therefore have objective difference at least −O_K(ε^{9/4})−O_K(ε^5)=o(ε²). They cannot be global minimizers for all sufficiently small ε. Existence was proved above. Consequently

\[
\inf\{\|u\|_2/ε:u\in\operatorname{argmin}J_{d_ε}\}\longrightarrow\infty.
\]

This is stronger than merely finding one badly chosen optimizer selection. It rules out Lipschitz L^2 response for global optimizers to this one-dimensional terminal-target perturbation. It does not prove that every local stationary branch fails, or that all weaker exponents/norms fail.

## 7. Falsification outcome and exact boundary

The submitted estimates survive the independent checks. The limiting point t=1/2 is null in the relevant spaces, finite-amplitude trial pulses are used only for perturbed-target comparisons, vanishing-amplitude pulses establish the L^∞ localization, arbitrary controls are covered by the global estimate, and every fixed ν≥0 is covered. Negative ν, unbounded ν(ε), no amplitude cap, Neumann or boundary controls, other time/domain spectra, and altered second-order criteria are outside the proved theorem.

Strongest verified result: the source model with β_2=0 admits a unique global minimizer satisfying the *unchanged* strict critical-cone substitute condition while failing strong L^2-squared growth, plus the stated every-global-optimizer non-Lipschitz target response. This is a negative answer to simply dropping β_2>0 from the displayed criterion. It does not settle existence of useful replacement conditions. No unsupported equivalent central claim remains in the reconstructed proof; no proof route is marked blocked. Source classification and later priority investigation must preserve this exact scope.

## 8. Subsequent comparison with the prior reviewer

This section was added only after the initial derivation (SHA256 `c9b0c04b85b1e7c4aceb091c3ce15abc8391e0e063a2db11e138f44c3b5a972a`, 14767 bytes) had been saved and timestamped in the log, and the prior verdict was then opened. Its core proof checks agree. Its recommendation to promote campaign status is a separate judgment, and its PASS label was not used as proof.

The prior reviewer also observes that all perturbed global minimizers converge to zero in L^2. Independently checking this observation: if u_ε is a minimizer, J_{d_ε}(u_ε)≤J_{d_ε}(0), so

\[
\frac{A_ε^3}{12\rho^2}
\le J_{\pi e}(u_ε)-J_{\pi e}(0)
\le ε(e,y_{u_ε}(1))\le CεA_ε.
\]

For A_ε>0 this implies A_ε=O(ε^{1/2}); if A_ε=0 the bound is immediate. The cap gives ∥u_ε∥_2²≤ρA_ε and hence ∥u_ε∥_2=O(ε^{1/4})→0, uniformly over global minimizers. Thus the non-Lipschitz theorem concerns optimizers actually approaching the base point in L^2. It still makes no claim about their L^∞ convergence or all local stationary branches.

The independent exact control script imports no submitted checker code and verifies 17 symbolic identities; its receipts are corroboration of the finite calculations only. The author's checker was also executed, and its JSON result exactly equals the submitted 3937-assertion receipt. All 19 original supplied files match SHA256, size and native Git-blob SHA1 pins.
