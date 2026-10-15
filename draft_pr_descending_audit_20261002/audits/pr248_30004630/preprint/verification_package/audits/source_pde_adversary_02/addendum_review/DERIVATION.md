# Independent optional-strengthening derivation

PR 248 / 30004630, submitted head `e9c5d10978764db2cf25fa7d49cf4bd14a82d604`. This addendum challenges new hypotheses under the exact frozen example. It does not edit or replace the finalized source/PDE audit. Its original pins are verified in `ORIGINAL_PINS.json`.

## 1. Data, dependencies, and hypothesis

Use the unit ball, T=1, zero initial data, normalized first radial Dirichlet mode e, cap ∥u(t)∥_H≤ρ, and quintic defocusing wave of the frozen proof. Fix γ=β_1=1 and β_2=0. Write

\[
J_{d,\nu}(u)=\tfrac12\|y_u(1)-d\|_H^2
+\tfrac\nu2\|(y_u)_t(1)\|_{H^{-1}}^2
+\tfrac14\|y_u\|_{L^4L^{12}}^4+A,
\qquad A=\|u\|_{L^1H},\quad \nu\ge0.
\]

The finalized original audit independently established, with constants independent of u and ν,

\[
\|y_u-z_u\|_{C(H)}\le R A^5,
\quad \|y_u(1)\|_H\le E A,
\quad (e,z_u(1))=\frac1\pi\int_0^1\sin(\pi t)(e,u(t))dt.
\]

Here R≥0 and E>0 are finite constants fixed before choosing the cap; all admissible controls obey A≤ρ≤a_0, the small-input radius. These are actual full-space wave bounds, not a linear-model substitution. The original global estimate is

\[
G_\nu(u):=J_{\pi e,\nu}(u)-J_{\pi e,\nu}(0)
\ge\frac{A^3}{12\rho^2}.
\tag{1}
\]

These dependencies were already proved in the finalized `../INDEPENDENT_DERIVATION.md` (SHA256 `77f7a9e4f1631f071572ea54e6a76c7a4d8bc4a25dd71b0f15c68e6690d52eda`). They rely on the classical linear energy/Strichartz estimate and full nonlinear contraction, not an unproved equivalent coercivity claim. This addendum treats the proposed *quadratic* L^1 growth and improved perturbation rates as new hypotheses and derives them below.

## 2. The one-sided endpoint substitution is valid

Put x=(e,y_u(1))_H. Since ∥e∥_H=1 and sin(πt)≤1,

\[
x\le \frac A\pi+R A^5=:b(A).
\tag{2}
\]

This is an upper bound for all spatial signs and profiles of u. It is not an assertion that x≥0. Exact expansion of the tracking square, discarding nonnegative velocity/state terms and using ∥y_u(1)∥_H²≥x², gives

\[
G_\nu(u)\ge A-\pi x+\frac{x^2}{2}=:q_A(x).
\tag{3}
\]

For fixed A, q_A'(x)=x−π. Thus q_A is decreasing on the entire interval (−∞,π]. If b(A)<π, (2) implies

\[
q_A(x)\ge q_A(b(A)).
\tag{4}
\]

In particular negative x causes no problem. It would be invalid to replace x² by b(A)² separately merely from x≤b(A); the justified operation is substitution into the *composite decreasing function* q_A.

Take the explicit positive local radius

\[
\delta=\min\left\{
\rho,a_0,\frac{\pi^2}{4},
\left(\frac\pi{4(1+R)}\right)^{1/5},
\left(\frac1{4\pi^3(1+R)}\right)^{1/3}
\right\}.
\tag{5}
\]

For 0≤A≤δ, A/π≤π/4 and R A^5≤π/4, so b(A)≤π/2<π. Also R A³≤1/(4π³). Direct expansion yields

\[
q_A(b(A))
=\frac{A^2}{2\pi^2}-\pi R A^5
+\frac R\pi A^6+\frac{R^2}{2}A^{10}
\ge\frac{A^2}{2\pi^2}-\pi R A^5
\ge\frac{A^2}{4\pi^2}.
\tag{6}
\]

All non-displayed costs have nonnegative coefficients. Hence the proposed local growth statement is correct:

\[
J_{\pi e,\nu}(u)-J_{\pi e,\nu}(0)
\ge k\|u\|_{L^1H}^2,
\quad k=\frac1{4\pi^2},
\quad u\in U_{ad},\ \|u\|_{L^1H}\le\delta.
\tag{7}
\]

The constants k and δ are independent of ν≥0; the assertion holds simultaneously for all finite nonnegative ν. There is no need to change the frozen ρ. It is enough to localize at A≤δ, possibly with δ<ρ. The A=0 case is equality. The case R=0 is covered by the harmless 1+R choices in (5).

This does not imply L^2-squared growth: the concentrating pulses have A_h²=4h^4, while ∥u_h∥_2²=2h³. A positive L^1-squared lower bound is fully consistent with the original failure of an L^2-squared bound. It also entails a local L^2 fourth-power bound k∥u∥_2^4/ρ², since ∥u∥_2²≤ρA, but not a quadratic L^2 bound.

## 3. Uniform relative-to-zero target response

The argument actually permits any H-valued target perturbation w, not just w=εe. Write d=πe+w and ε=∥w∥_H. For each finite ν≥0, perturbed global minimizers exist by the finalized direct method. Let u_w be *any* such minimizer and A_w=∥u_w∥_{L^1H}. Since zero is feasible,

\[
J_{d,\nu}(u_w)\le J_{d,\nu}(0).
\]

The exact change-of-target identity is

\[
J_{d,\nu}(u)-J_{d,\nu}(0)
=G_\nu(u)-(w,y_u(1))_H.
\tag{8}
\]

The w² constant cancels. Combining (1), (8) and the endpoint bound gives

\[
\frac{A_w^3}{12\rho^2}
\le G_\nu(u_w)
\le (w,y_{u_w}(1))_H
\le E\epsilon A_w.
\tag{9}
\]

For A_w>0, A_w≤√(12ρ²Eε); for A_w=0 every claimed bound is immediate. Thus all global minimizers enter the L^1 growth neighborhood uniformly as ε→0. Set

\[
\epsilon_0=\min\left\{1,\frac{\delta^2}{12\rho^2E}\right\}>0.
\tag{10}
\]

For ε≤ε_0, apply (7) and cancel A_w when positive:

\[
k A_w^2\le E\epsilon A_w,
\qquad
A_w\le 4\pi^2E\epsilon.
\tag{11}
\]

The original pointwise cap yields

\[
\|u_w\|_{L^2H}^2
=\int\|u_w(t)\|_H^2dt
\le\rho\int\|u_w(t)\|_Hdt
=\rho A_w,
\]

and therefore

\[
\|u_w\|_{L^2H}\le 2\pi\sqrt{\rho E}\,\epsilon^{1/2}.
\tag{12}
\]

Equations (10)–(12) hold for every perturbed global optimizer, with the same constants and neighborhood radius for all ν≥0. The proof only drops or cancels its nonnegative velocity term, so neither its constant nor its localization threshold depends on ν. No optimizer selection needs to be singled out.

These are bounds relative to the fixed, unique zero optimizer at the fixed base target. They prove Lipschitz L^1 distance from zero and one-half Hölder L^2 distance from zero. They do *not* prove a Lipschitz selection map between arbitrary nearby target pairs, uniqueness of every perturbed optimizer, a bound between different optimizers of one perturbed problem, or L^∞ convergence of the optimizers. A pointwise-to-base estimate cannot be silently turned into any of those pairwise assertions.

## 4. Rough lower L^2 rate and its separate ν quantifier

For the radial perturbation w=εe, the finalized original proof supplies, for every fixed ν≥0 and all sufficiently small ε>0,

\[
J_{(\pi+\epsilon)e,\nu}(u_\epsilon)
-J_{(\pi+\epsilon)e,\nu}(0)\le-\frac{\epsilon^2}{4}
\tag{13}
\]

for every global optimizer, by comparing with its feasible fixed-amplitude pulse. The small-ε threshold in (13) may depend on ν: the pulse's true nonlinear terminal velocity is only estimated as O(ε^5), so its ν-cost is O(νε^{10}). The original proof establishes (13) for each fixed finite ν, or uniformly for bounded ν ranges; it has not established this comparison uniformly for all unbounded ν≥0 simultaneously. The L^1 growth and upper target bounds above do not need (13), and remain uniform in ν.

For r=∥u∥_2, the original lower estimate has

\[
J_{(\pi+\epsilon)e,\nu}(u)-J_{(\pi+\epsilon)e,\nu}(0)
\ge-C_g\epsilon^{5/4}r-C_2r^5,
\quad C_g=2^{1/4}\pi^{-5/4},
\tag{14}
\]

where C_2 can be fixed for 0<ε≤1 independently of ν≥0. Choose c=1/(8C_g). If an optimizer had r≤cε^{3/4}, (14) would give

\[
J_{(\pi+\epsilon)e,\nu}(u)-J_{(\pi+\epsilon)e,\nu}(0)
\ge-\frac{\epsilon^2}{8}-C_2c^5\epsilon^{15/4}.
\]

Choose ε small enough that C_2c^5ε^{7/4}≤1/16. The resulting bound is at least −3ε²/16, contradicting (13). Thus for each fixed ν≥0, for every global optimizer and all sufficiently small ε,

\[
c\epsilon^{3/4}\le\|u_\epsilon\|_{L^2H}
\le 2\pi\sqrt{\rho E}\,\epsilon^{1/2}.
\tag{15}
\]

The lower c can be chosen independently of ν, but its ε-neighborhood is only established per fixed ν, because of (13). One can alternatively use (12) to absorb the r^5 term as O(ε^{5/2}); the direct small-r contradiction above avoids requiring that extra step.

The two powers are compatible for 0<ε<1. The lower bound provides a quantitative non-Lipschitz conclusion r/ε≥cε^{-1/4}→∞, while (12) proves approach to zero. Neither bound is claimed sharp. No lower bound for arbitrary nonradial target perturbations is asserted; for some directions the zero optimizer can persist.

## 5. Disposition

All proposed upper assertions are valid under their stated locality, with a rigorously chosen radius. The optional rough lower radial bound is valid for each fixed ν≥0 with the quantifier in Section 4. Uniformity over all unbounded ν in its neighborhood would require additional evidence; the supplied pulse proof does not provide it.

This is an **optional enhancement**, not a mandatory repair of the frozen original L^2 counterexample. It adds a positive natural-space growth statement and sharper relative-to-base upper stability rates. The original strict-cone/L^2 failure theorem, its zero-cone mechanism and its scope remain unchanged. No claim about historical priority is made or investigated, and no external, Git, PR, publication, or spreadsheet action is taken.
