# Bounded-variation solutions for hysteretic traffic systems

**Target:** 30005735 / OWR-14298011-006.  
**Disposition:** partial results; the general switching small-BV Cauchy problem is not solved here.  
**Substantive approaches:** five distinct routes, exhausted. Literature checks, source corrections, verification and packaging do not add a sixth route. No originality claim is made for the partial results.

## 1. Source, conventions, and a necessary qualification

The controlling workshop question is Corli's contribution, OWR 52/2023, printed pp. 2968–2969. It discusses HLWR and its HARZ extension, and asks for a rational Riemann selection and a general BV initial-value theory, possibly with small data. It does **not** specify a smallness norm, reference state, uniform hyperbolicity constant, or a theorem covering arbitrary switching. These must not be retroactively attributed to the report. [S1]

### 1.1 Equations and coefficient hypotheses

Use a Lagrangian vehicle label $x$, spacing $u=1/\rho>0$, driver marker $w$, and memory $h$. The HARZ equations are

\[
u_t-\partial_x V(u,w,h)=0,\qquad w_t=0,\qquad
h_t=\chi_A\partial_t h^A(u,w)+\chi_D\partial_t h^D(u,w).                 \tag{1}
\]

Here

\[
V(u,w,h)=\begin{cases}
v^D(u,w),&u\le u^D(w,h),\\
v^S(u,w,h),&u^D(w,h)<u<u^A(w,h),\\
v^A(u,w),&u\ge u^A(w,h).
\end{cases}                                                        \tag{2}
\]

Endpoint matching means $v^S(u^B(w,h),w,h)=v^B(u^B(w,h),w)$, $B=A,D$. The functions $h^B(\cdot,w)$ invert $u^B(w,\cdot)$. The physical state space is

\[
\Omega=\{w\in[w_{\min},w_{\max}],\ h\in[h_{\min}(w),h_{\max}(w)],
                \ u^D(w,h)\le u\le u^A(w,h)\}.                      \tag{3}
\]

In Lagrangian coordinates $A=\{V=v^A,V_t>0\}$, $D=\{V=v^D,V_t<0\}$; the complement is scanning. With strictly positive branch slopes, the velocity and spacing time-derivative signs agree on each active branch. At BV discontinuities these indicators and products require an additional path/graph convention; they are not defined by multiplying arbitrary representatives of distributions.

For HLWR omit $w_t=0$ and all $w$-dependence. Its original base assumptions permit $v^S_u=0$. HARZ's printed Assumptions 1–3 include:

- $v^A,v^D,v^S\in C^1$, with the second $u$-derivatives in Assumption 3;
- $v^A_u,v^D_u>0$, $v^S_u\ge0$, strengthened to $v^S_u>0$;
- $v^A_{uu},v^D_{uu},v^S_{uu}<0$ for the Riemann-wave analysis;
- $v^S_h>0$, $u^A_h,u^D_h>0$;
- $u^D\le u^A$, equality only at $h_{\mathrm{cr}}(w)$;
- a crossing $u_{\mathrm{cr}}(w)$, with $v^D>v^A$ below it and $v^A>v^D$ above it;
- common upper speed $v_{\max}$, with $v^A,v^D\to v_{\max}$ as $u\to\infty$, continuous endpoint bounds in $w$, and transverse scanning/end-curve intersections.

These are the source's assertions, not a newly certified globally consistent hypothesis package. In a theorem on a compact patch, positive lower slope bounds and Lipschitz constants must be explicitly extracted from that patch. Strict positivity on an unbounded domain alone gives no global positive lower bound.

### 1.2 Viscosity and paths

HARZ uses

\[
u_t-V_x=\varepsilon\partial_x(B(u,w,h)V_x),\qquad B\ge\mu>0,           \tag{4}
\]

with $w,h$ governed as in (1). The 2019 HLWR paper instead uses

\[
u_t-V_x=\varepsilon\partial_x(B(u)u_x),\qquad B\ge\mu>0.             \tag{5}
\]

They must not be silently identified. A moving HARZ profile with coordinate $\xi=(x-st)/\varepsilon$ satisfies

\[
B V'=-s(u-u_-)-(V-V_-),\quad w\equiv w_-,\quad
h'=\chi_A(h^A)' +\chi_D(h^D)',\quad
s=-\frac{V_+-V_-}{u_+-u_-}<0.                                     \tag{6}
\]

The physical path initially scans at fixed $h_-$, then, if necessary, follows the appropriate boundary monotonically. Stationary contacts have equal velocity and can change $w,h,u$. In (4), a constant-velocity stationary profile has zero diffusion. Fan–Shu's HLWR weak formulation uses monotone hysteresis paths and, for a nonzero temporal memory jump, the endpoint conditions

\[
[h]>0\ \Longrightarrow\ h_+=h^A(u_+),\qquad
[h]<0\ \Longrightarrow\ h_+=h^D(u_+).                              \tag{7}
\]

For their piecewise-$C^1$ class, the endpoint conditions (7), together with the smooth-part conditions $h_t>0\Rightarrow h=h^A(u)$ and $h_t<0\Rightarrow h=h^D(u)$ (and feasibility), characterize the memory equation. The jump conditions alone do not do so. A general BV extension must also specify the diffuse/Cantor part and convergence through unresolved thin layers. The mere phrase “DLM solution” does not supply these choices for a derivative-sign-dependent switching law. [S2–S4]

The Eulerian conservation equations are $\rho_t+(\rho V)_x=0$ and $(\rho w)_t+(\rho Vw)_x=0$, while the memory derivative is material: $D_t h=h_t+Vh_x$. Thus the coordinate-covariant switching tests are $D_tV\gtrless0$, not the Eulerian partial derivative $V_t\gtrless0$. The printed Eulerian indicator notation should be read with that correction explicitly identified. Nothing below uses the ambiguous Eulerian notation.

### 1.3 Coefficient-compatibility audit

The positive $v^S_h$ condition is printed both in the author PDF, p. 7, and in the publisher HTML. It is not an OCR error.

Fix $w$, and suppose a fixed-$u$ physical section contains both endpoints $a=h^A(u,w)$ and $d=h^D(u,w)$. Increasing endpoint maps and $u^D\le u^A$ imply $a\le d$. Endpoint matching gives the identity

\[
v^D(u,w)-v^A(u,w)
=\int_{a}^{d} v^S_h(u,w,r)\,dr\ \ge0,                              \tag{8}
\]

strictly if $a<d$. Therefore a fully represented free-zone section with $v^A>v^D$ cannot at the same time satisfy all these printed signs. In particular, if $h_{\mathrm{cr}}$ is interior to the represented memory interval, both inverse endpoints exist for nearby $u>u_{\mathrm{cr}}$, producing the conflict. A patch containing only a congested sector need not have this problem. A truncated domain that represents no free-zone sections is not a representation of the full two-zone diagram.

This is a scope/parameterization issue, not a nonexistence theorem for the intended traffic dynamics. We do not repair $v^S_h$'s sign globally by fiat, discard the free zone silently, or obtain a vacuous “solution” from incompatible assumptions. The proved statements below have their own coherent local hypotheses.

### 1.4 Known work and the success test

Corli–Fan 2024, Theorem 5 and Remarks 5–6, already give the velocity-monotone rational Riemann solver, including the HLWR uniqueness observation. Theorem 1 assumes a sufficiently regular viscous solution already exists; Remark 2 labels velocity TVD formal. Fan–Shu 2020, Theorem 6.1, assumes the numerical limit is piecewise $C^1$. Their TVD work is important prior progress, not a general-BV closure theorem. Fan 2024 concerns a different two-parameter hysteresis model. Goatin–Moreti 2026 treats $u_t+w_t+f(u)_x=0$ with a Play operator, not (1). No exact full-target resolution was established by these checks. [S2–S6]

A precise small-data formulation for further work could fix a coherent coefficient chart and an admissible reference state $\bar U$, and assume

\[
\|U_0-\bar U\|_{L^\infty}+\operatorname{TV}(U_0)\le\delta,
\qquad U_0-\bar U\in L^1,\quad U_0(x)\in\Omega.                    \tag{9}
\]

This norm is **our explicit test formulation**, not a norm specified by OWR. Success for the switching problem would require global approximants, uniform full-state BV bounds, compactness, proof of the source-compatible nonconservative limit, the initial trace, and shock admissibility. It must include arbitrary patterns of switching among the allowed states, rather than only a reference point strictly inside one scanning leaf. No result below satisfies this complete success test.

## 2. Approach 1: branch-preserving construction

### Restricted theorem

Let $z=(w,h)$ range over a compact convex set $Z$, and let $J=[c_-,c_+]$. Assume $V=v^S$ is $C^2$, with $V_{uu}<0$, on a neighborhood of

\[
K=\{(G(c,z),z):c\in J,z\in Z\},\qquad V(G(c,z),z)=c,
\]

with $0<m\le V_u\le L$, $G$ Lipschitz, and $K$ a positive distance from both switching boundaries. Let $z_0$ be BV, $v_0\in BV(\mathbb R;J)$, and set $u_0=G(v_0,z_0)$. Then there is a global BV solution of

\[
u_t-\partial_xV(u,z_0(x))=0,\qquad z(x,t)=z_0(x),                 \tag{10}
\]

remaining in $K$, with

\[
\operatorname{TV}v(t)\le\operatorname{TV}v_0,\qquad
\operatorname{TV}u(t)\le m^{-1}\operatorname{TV}v_0
                          +C_z\operatorname{TV}z_0.               \tag{11}
\]

Here $C_z$ is an inverse-map Lipschitz constant in $z$; coordinatewise variation can be used throughout. The solution has the adapted scalar entropy inequalities displayed below. For the HARZ path convention (4), its moving scanning shocks and stationary equal-velocity contacts have the corresponding admissibility. This theorem is conditional on a coherent scanning chart and makes no assertion for the inconsistent literal global hypothesis combination in §1.3.

### Proof

Approximate $v_0,z_0$ by BV piecewise-constant grid functions valued in $J,Z$, and set $u_j^0=G(v_j^0,z_j)$. Fix $z_j$ in time and use

\[
u_j^{n+1}=u_j^n+\lambda(v_{j+1}^n-v_j^n),\qquad
v_j^n=V(u_j^n,z_j),\qquad 0<\lambda L\le1.                        \tag{12}
\]

For fixed $z_j$, the map $r\mapsto r+\lambda(c-V(r,z_j))$ is increasing. Comparing with $G(c_-,z_j)$ and $G(c_+,z_j)$ proves that $u_j^{n+1}$ remains in the same interval, so the scheme never activates hysteresis. The mean-value theorem gives

\[
v_j^{n+1}=v_j^n+a_j^n(v_{j+1}^n-v_j^n),\qquad
0\le a_j^n=\lambda C_j^n\le1.                                    \tag{13}
\]

Put $d_j=v_{j+1}-v_j$. Then

\[
d_j^{n+1}=(1-a_j^n)d_j^n+a_{j+1}^n d_{j+1}^n.
\]

Summing absolute values gives $\sum_j|d_j^{n+1}|\le\sum_j|d_j^n|$. The maximum principle follows directly from (13). Applying the Lipschitz inverse map proves the grid form of (11). Also

\[
\Delta x\sum_j|u_j^{n+1}-u_j^n|
       \le\Delta t\operatorname{TV}v_0.                           \tag{14}
\]

Spatial BV and (14) give $L^1_{\rm loc}$ compactness on every finite time interval, using piecewise-constant time interpolation and a diagonal extraction. The limit has the initial trace; summation by parts in the conservative scheme gives (10). The bounds and the invariant set survive the limit. No claim of compactness on the whole line without appropriate integrable far-field assumptions is needed.

For completeness, fix $c\in J$ and $k_j=G(c,z_j)$. The update map in (12) is monotone in both $u_j,u_{j+1}$, and the sequence $k_j$ is an exact stationary grid solution. Comparing the coordinatewise maximum and minimum with (k) yields

\[
|u_j^{n+1}-k_j|\le|u_j^n-k_j|
       +\lambda\bigl(|v_{j+1}^n-c|-|v_j^n-c|\bigr).               \tag{15}
\]

Indeed, the difference of the two monotone updates is exactly the right-hand side, since $V(\cdot,z_j)$ is increasing. Passing to the limit gives

\[
\partial_t|u-G(c,z_0(x))|-\partial_x|v-c|\le0.                    \tag{16}
\]

All moving waves leave $z$ unchanged. For stationary jumps, (10) forces equal velocity. The path $z=z(\theta)\in Z, u=G(c,z(\theta))$ has constant $V=c$ and remains scanning, hence is compatible with (4). For a moving scanning shock, fix its common $z$. The flux $-V(\cdot,z)$ is strictly convex, so (16) selects $u_->u_+$. Let $\ell$ be the chord of $V$ between the endpoints. Strict concavity gives $\ell(u)-V(u,z)<0$ for $u_+<u<u_-$. The HARZ profile equation becomes

\[
B(u,z)V_u(u,z)u'=\ell(u)-V(u,z).
\]

Its positive left-hand coefficient and simple endpoint zeros give the decreasing heteroclinic profile, with limits at $\xi=\pm\infty$. Thus the moving-shock admissibility claimed above follows for this scanning chart. This completes the restricted construction.

**Exact gap:** a common scanning-only band excludes activation. An arbitrarily small perturbation of a reference state on a switching boundary need not have such a band. The result does not settle general small BV data near those states or data traversing a critical/degenerate region. It is a conventional scalar/frozen-parameter argument, not asserted to be new.

## 3. Approach 2: wave interactions and a first-order contact effect

### A bound that does follow from the prior rational solver

For any finite front configuration built from velocity-monotone Riemann fans, resolving an interaction with exterior velocities $v_L,v_R$ produces total outgoing velocity strength $|v_R-v_L|$. The incoming strength is at least that value by the triangle inequality. Stationary contacts have zero velocity strength. Thus, as long as the front construction exists,

\[
\operatorname{TV}v(t)\le\operatorname{TV}v(0).                     \tag{17}
\]

This does not bound the number of fronts, prevent accumulation of interactions, or control the full (u,h) variation.

### Exact local coefficients and states

On a compact neighborhood of the following states, take

\[
f(u)=u-\tfrac14(u-3)^2,\quad
v^S(u,w,h)=f(u)+h,\quad
h^A(u,w)=u-w,\quad h^D(u,w)=u-w+1.                                \tag{18}
\]

Consequently

\[
u^A(w,h)=w+h,\quad u^D(w,h)=w+h-1,\quad
v^A=f(u)+u-w,\quad v^D=f(u)+u-w+1.                               \tag{19}
\]

On, for example, the relevant $u$-range near ([2,3.1]), all branch slopes are positive, all branch second derivatives are (-1/2), $v^S_h=1$, and both endpoint $h$-derivatives are 1. This is a coherent **local congested patch**. We do not claim (18) is a globally bounded two-zone traffic law.

Let $0<\delta<1/8$, $\alpha=\delta/2$. Begin with the stationary contact

\[
U_L=(3,3,0),\quad U_R=(3,3+\delta,0),\qquad v_L=v_R=3.             \tag{20}
\]

The left trace is on its acceleration boundary; the right trace is strictly scanning. From the right send a scanning rarefaction raising the common transmitted velocity from (3) to $3+\alpha$. Its right state is

\[
U_{RR}=(r,3+\delta,0),\quad f(r)=3+\alpha,\quad
r=5-2\sqrt{1-\alpha}.                                            \tag{21}
\]

Because $\alpha<\delta-\delta^2/4=f(3+\delta)-3$, one has $r<3+\delta$; thus the incoming wave stays scanning and changes no $h$.

After that rarefaction has crossed the stationary contact, the rational solver on the left has an acceleration rarefaction ending at

\[
U_M=(3+H,3,H),\quad
2H-\tfrac14H^2=\alpha,\quad
H=4-2\sqrt{4-\alpha}.                                             \tag{22}
\]

It is followed by the new stationary contact $U_M\to U_{RR}$, whose two velocities are $3+\alpha$. The original contact had zero $h$-jump; the new one has magnitude $H$. The incoming moving wave had no $h$-jump. All states approach the same boundary state as $\delta\downarrow0$.

Exactly,

\[
H=\frac{2\alpha}{2+\sqrt{4-\alpha}},\qquad
\frac{\alpha}{2}<H<\alpha,\qquad
H=\frac\alpha2+\frac{\alpha^2}{32}+O(\alpha^3).                    \tag{23}
\]

Thus $H/(\alpha\delta)>1/(2\delta)\to\infty$. No uniform estimate of the form

\[
|\hbox{new memory-contact strength}-\hbox{old memory-contact strength}|
                  \le C\,|\hbox{incoming velocity strength}|\,|[w]|
\]

holds in these coordinates near switching. The change is first order, not a hidden numerical effect. In ordinary time a rarefaction crosses gradually; (22) is the final transmitted state. Using the whole small fan avoids falsely treating it as one entropy shock.

**Exact gap:** this rules out this particular smooth-system quadratic interaction estimate. It does not rule out a different wave-strength parametrization, a switching-aware functional, or a full BV theorem. A functional controlling the memory/driver contacts together with the moving waves remains unproved.

## 4. Approach 3: generalized play and the BV closure obstruction

At fixed $w$, feasibility is equivalently

\[
a(u,w):=h^A(u,w)\le h\le d(u,w):=h^D(u,w).                        \tag{24}
\]

For an absolutely continuous input (u(t)), the constitutive law is a one-dimensional sweeping rule: $h$ is constant in the interior, follows the lower endpoint when pushed upward and the upper endpoint when pushed downward. On a monotone input segment its update is

\[
h_{\rm new}=\operatorname{proj}_{[a(u_{\rm new},w),d(u_{\rm new},w)]}
                        (h_{\rm old}).                            \tag{25}
\]

Because both endpoints increase with $u$, repeated projections along a monotone segment reduce to this single projection. This suggests a Play/sweeping construction, but ordinary strong $L^1$ plus bounded variation does not close the constitutive graph.

### Explicit thin-pulse calculation

Use $a(u,w)=u-w, d(u,w)=u-w+1$, with fixed $w$, and choose $0<e<1$. Let $u_n=w+eP_n(t)$, where $P_n$ is a triangular pulse of height 1, supported in $[t_0-1/n,t_0+1/n]$, rising to its peak at $t_0$. Set $h_n=0$ initially and apply the exact sweeping rule. On the rising half $h_n=u_n-w$; on the falling half and afterward $h_n=e$, because the upper endpoint stays at least 1.

Every path is piecewise smooth and admissible, with

\[
\operatorname{TV}_t u_n=2e,\quad\operatorname{TV}_t h_n=e.
\]

Nevertheless,

\[
u_n\to w\text{ in }L^1_{\rm loc},\qquad
h_n\to e\,\mathbf1_{(t_0,\infty)}\text{ in }L^1_{\rm loc}.           \tag{26}
\]

The limiting positive $h$-jump ends at $h_+=e\ne a(w,w)=0$, violating the monotone-jump endpoint rule (7). The pulse amplitudes can be arbitrarily small. Hence the graph is not sequentially closed in this topology under these BV bounds.

This is a **constitutive counterexample**, not a sequence of solutions of the conservative PDE. Its time derivatives also do not satisfy a uniform Lipschitz-in-time bound. A spatially homogeneous realization has conservative residual $(u_n)_t\to0$ in distributions, but it is still not the actual upwind or viscous approximation. Stronger graph convergence, a no-hidden-excursion estimate, or the PDE's additional estimates might exclude it.

**Exact gap:** one must prove such exclusion for the chosen approximation, including its jump and Cantor parts. The scalar Play theorem cannot simply be imported: (1) has a state-dependent constitutive flux, a frozen heterogeneous marker, different dissipation structure and the profile convention (6).

## 5. Approach 4: a common convex-entropy obstruction

Here fix $w$ and work on a coherent $C^2$ positive-hysteresis scanning strip

\[
u^D(h)<u<u^A(h),\qquad V_u>0,\quad V_h>0,
\]

with increasing $h^A,h^D$. Suppose a $C^2$ local entropy–flux pair $(\eta(u,h),q(u,h))$, defined on a neighborhood of the closed strip, is valid for **every** smooth scanning, acceleration and deceleration solution, in the sense $\eta_t+q_x\le0$, and suppose $\eta_{uu}>0$.

In scanning, $h_t=0, u_t=V_u u_x+V_h h_x$. Since smooth scanning gradients can have either sign, the inequality forces

\[
q_u=-\eta_u V_u,\qquad q_h=-\eta_u V_h.                           \tag{27}
\]

Equality of mixed (q)-derivatives then gives

\[
V_u\eta_{uh}=V_h\eta_{uu},\qquad \eta_{uh}>0.                     \tag{28}
\]

On the acceleration boundary, differentiating the matching relation gives $v^A_u=V_u+V_h h^A_u$. Equations (27) therefore imply

\[
\eta_t+q_x=\eta_h h_t.
\]

Since $h_t>0$ is allowed there, dissipation requires

\[
\eta_h(u^A(h),h)\le0.                                             \tag{29}
\]

On the deceleration boundary $h_t<0$, so it requires

\[
\eta_h(u^D(h),h)\ge0.                                             \tag{30}
\]

But (28) yields

\[
\eta_h(u^A(h),h)-\eta_h(u^D(h),h)
=\int_{u^D(h)}^{u^A(h)}\frac{V_h}{V_u}\eta_{uu}\,du>0,             \tag{31}
\]

contradicting (29)–(30). Thus no such $C^2$, strictly-$u$-convex, common local dissipative entropy exists on the strip.

**Exact gap:** this closes the straightforward common-convex-entropy route in this class. It neither proves ill-posedness nor excludes nonsmooth, path-dependent, history-dependent or non-convex Lyapunov functionals. A different compactness mechanism would be needed.

## 6. Approach 5: flat-scanning resonance and nonuniform BV bounds

The base HLWR allowance $v^S_u=0$ cannot be confused with the stricter HARZ Riemann assumptions. The following exact local model tests what fails at zero scanning slope:

\[
u^D(h)=h,\quad u^A(h)=h+1,\quad
v^D(u)=f(u),\quad v^A(u)=f(u-1),\quad v^S(u,h)=f(h),               \tag{32}
\]

where $f(r)=r-r^2/20$ on the relevant compact range. The boundary curves are increasing and strictly concave there. The scanning slope is zero. This is a local positive-hysteresis patch; no globally crossing source coefficient family is asserted for (32).

Take the background $(u,h)=(5/2,2)$, and a pulse ((5/2,2+e)), $0<e\le1/64$. Put

\[
\Delta v=f(2+e)-f(2)=\tfrac45e-\tfrac1{20}e^2.
\]

At an increasing $h$-edge the rational scanning-to-acceleration shock connects

\[
(5/2,2)\ \longrightarrow\ (3+e,2+e),\qquad
s_\uparrow=-\frac{\Delta v}{1/2+e},                               \tag{33}
\]

followed by a stationary equal-velocity contact to ((5/2,2+e)). At the decreasing edge, the scanning-to-deceleration shock connects

\[
(5/2,2+e)\ \longrightarrow\ (2,2),\qquad
s_\downarrow=-2\Delta v,                                         \tag{34}
\]

followed by a stationary contact to ((5/2,2)).

These speeds satisfy $s[u]+[v]=0$. The increasing-edge chord lies strictly above the scanning/acceleration path: it is above the initial horizontal segment, and on the final acceleration segment its slope is smaller than (f'), making the positive chord gap decrease to zero only at the right endpoint. The decreasing-edge chord lies below the horizontal/concave deceleration path. Thus the moving shocks satisfy the corresponding profile chord tests for the $u_x$-viscosity (5). These equal-velocity contacts are inviscid stationary waves; a step in $u$ is not itself a smooth stationary profile for (5), and a constant-velocity nonconstant profile would force $u'=0$. This differs from (4). Here they do admit (5)-profiles with a small velocity excursion: choose $B=1$ and a sufficiently slow monotone spacing profile between the contact endpoints, then set $h=f^{-1}(v_0-u')$. For the high-spacing contact $u'<0$, so $h>2+e$; for the low-spacing contact $u'>0$, so $h<2$. Making $|u'|$ small keeps $u-1<h<u$ except at the limiting boundary endpoint and gives the required limits. The memory equation imposes no further profile restriction at speed zero. This is the distinction made in the HLWR stationary-wave construction, S3, Theorem 4.2.

For each pulse and each sufficiently small positive time before interactions, the spacing variation is

\[
2(1/2+e)+2(1/2)=2+2e,                                            \tag{35}
\]

although the initial full-state variation is (2e). Its spacing $L^1$ change is $2t\Delta v$. Place (N) pulses on ([3n,3n+1]), with $e_n=2^{-n-6}$, $0\le n<N$. All moving speeds have magnitude below (1/4), so no fronts from different edges meet for $0<t\le1$. Therefore

\[
\operatorname{TV}h_0=2\sum_{n<N}e_n<1/16,\qquad
\operatorname{TV}u(t)=2N+2\sum_{n<N}e_n.                          \tag{36}
\]

Multiplying all $e_n$ by an arbitrarily small positive factor makes the initial norm arbitrarily small without removing the order-one-per-pulse spacing variation. The countably infinite locally finite pulse pattern gives an explicit glued rational solution with infinite **global** spacing variation for every $0<t\le1$, while its spacing perturbation remains $L^1$. This is an example in the local degenerate coefficient model, not a proof that every possible weak solution lacks BV and not a full-source counterexample.

**Exact gap:** no conclusion against the strictly positive-slope, compact-patch problem follows. For $V_u\ge m>0$, the inverse estimate in (11) carries $m^{-1}$; the flat-scanning example explains why a lower-slope condition or a different norm matters. A complete global coefficient extension and an admissible uniqueness argument would be required to turn this local calculation into a counterexample to a fully specified source-level existence statement.

## 7. What is proved and what remains

Proved here, under the precisely stated scopes:

1. A global BV construction on a coherent uniformly scanning common velocity band, with (11), (14), and adapted entropy inequality (16).
2. Velocity TVD for any finite rational front construction, plus an exact first-order switching-contact effect obstructing the displayed quadratic estimate.
3. Failure of strong-$L^1$/BV closure for the constitutive sweeping graph without additional controls.
4. Nonexistence of a common $C^2$, strictly-$u$-convex local dissipative entropy for all three smooth modes on a positive-hysteresis strip.
5. Exact local flat-scanning rational waves showing nonuniform propagation of full-state BV near resonance.

The remaining central task is a coherent switching formulation together with a full-state BV estimate and convergence of the memory law through singular limits. A proof must cope with first-order activation at heterogeneous stationary contacts and control hidden path excursions. None of the five routes supplies these missing steps. There is no full rigorous candidate and no full-resolution or novelty claim.

## Sources and verification

- **S1.** Andrea Corli, “Hysteresis and string stability in traffic flows,” OWR 52/2023, printed pp. 2968–2969. [Official report](https://ems.press/content/serial-article-files/48173), DOI [10.4171/OWR/2023/52](https://doi.org/10.4171/OWR/2023/52).
- **S2.** Andrea Corli and Haitao Fan, “The hysteretic Aw–Rascle–Zhang model,” Studies in Applied Mathematics 153(4), e12769 (2024). [Publisher full text](https://onlinelibrary.wiley.com/doi/full/10.1111/sapm.12769), [author-hosted PDF](https://sfera.unife.it/retrieve/502a3b8a-a6fc-417a-814c-544d928b2ed1/2024_Corli-Fan-SAM.pdf). Equations (11)–(16), Assumptions 1–3, Remark 2, Section 6 and Theorem 5 checked. The printed p. 7 coefficient signs were visually inspected and independently matched to publisher HTML. Publication date: 9 October 2024.
- **S3.** Andrea Corli and Haitao Fan, “Hysteresis and stop-and-go waves in traffic flows,” M3AS 29 (2019), 2637–2678, DOI [10.1142/S0218202519500568](https://doi.org/10.1142/S0218202519500568). [Author preprint](https://iris.unife.it/retrieve/e309ade4-5dc1-3969-e053-3a05fe0a2c94/Corli-Fan_M3AS.pdf). Sections 2–4 and the viscosity distinction checked.
- **S4.** Haitao Fan and Chi-Wang Shu, “Existence and Computation of Solutions of a Model of Traffic Involving Hysteresis,” SIAM J. Appl. Math. 80(6) (2020), 2319–2337, DOI [10.1137/19M1269567](https://doi.org/10.1137/19M1269567). [NSF-hosted author manuscript](https://par.nsf.gov/servlets/purl/10226107). Definitions 3.1–3.2, Theorem 3.2, Theorems 5.1–5.2 and 6.1 inspected. Its conditional regularity hypothesis is retained.
- **S5.** Haitao Fan, “Conservation laws with hysteretic fluxes,” JDE 394 (2024), 1–30, DOI [10.1016/j.jde.2024.02.030](https://doi.org/10.1016/j.jde.2024.02.030). Publisher-indexed abstract/introduction inspected; a full-PDF proof audit was not completed. The two-parameter model was not substituted for HLWR/HARZ.
- **S6.** Paola Goatin and Stefan Moreti, “Well-posedness and Godunov approximation for nonlinear conservation laws with hysteresis,” NoDEA 33, 131 (2026), published 26 September 2026. [Publisher article](https://link.springer.com/article/10.1007/s00030-026-01271-7). The scalar Play equation and scope were checked, not its entire proof.

The accompanying calculation script uses only the Python standard library. Its rational root brackets, flat-scanning identities and bounds use exact rational arithmetic; explicitly labeled square-root illustrations use floating-point arithmetic. Runtime checks remain enabled under Python optimization. It supports the displayed calculations; the analytic proofs are given above. Original source bodies, private coordination and corpus contents are not included in this authored packet.
