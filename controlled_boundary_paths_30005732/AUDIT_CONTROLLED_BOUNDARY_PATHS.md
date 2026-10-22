# Independent adversarial audit: controlled boundary paths

Audited 2026-10-21. Original Q1 remains unresolved at its general intended regularity/trajectory scope. The initial RESEARCH.md checkpoint correctly distinguishes optimal motions from arbitrary admissible motions. This audit supplies a stronger optimal special case and precise limitations.

## 1. Source anchors and class distinction

- Official OWR 52/2023, printed p.2959, OP and Q1: fixed terminal-area objective, inward speed beta >= -1, effort integral <= M; prose writes the speed/budget at every time. https://ems.press/content/serial-article-files/48173
- Bressan–Chiri–Salehi, arXiv:2201.01723, section 2, equations (2.1)–(2.13): bounded finite-perimeter space-time sets, inward normal nu, L1 one-sided traces, projected effort measure; these support the weak formulation below. https://arxiv.org/abs/2201.01723
- Bianchini–Bressan–Chiri, arXiv:2307.03599, Definition 1.1 and OP (1.4), printed pp.1–2: M>0, L1-Lipschitz motion, a.e. effort bound, nonnegative running/terminal area weights. https://arxiv.org/abs/2307.03599
- Bressan survey arXiv:2502.06050, section 5, printed pp.15–17: A5 requires a jointly C1,1 regular, nondegenerate parametrization and continuous normal speed; Problem 2 asks to justify orthogonal trajectories. https://arxiv.org/abs/2502.06050

The foundational paper's general effort-cost objective is not identical to a hard-budget area-only objective. Optimality conclusions below apply to the latter, not arbitrarily to quadratic effort penalties or other effort functions. Standard finite-perimeter slicing and the planar isoperimetric inequality are used in the derivation, not claimed as a verbatim theorem in these papers.

## 2. Weak area inequality, including singular pieces

Let Q be a bounded finite-perimeter space-time set, with inward reduced-boundary normal nu=(nu_0,nu_x). Put A(t)=|Q_t|. For the effort E(beta)=max(1+beta,0), its continuous positively homogeneous extension is

L(nu)=max(|nu_x|-nu_0,0).

This extension also specifies horizontal pieces, where beta itself is undefined. Let mu=L(nu) H2|boundary*Q and let mu_t be its time projection. Assume mu_t <= M dt and use initial/terminal L1 traces. Then, as measures on the time interval,

DA = projection(nu_0 H2|boundary*Q),
P(Q_t) dt = projection(|nu_x| H2|boundary*Q),
DA >= P(Q_t) dt - mu_t >= (2 sqrt(pi A)-M) dt.

The first two identities follow from distributional differentiation and BV slicing. The pointwise inequality L >= |nu_x|-nu_0 proves the third. The perimeter is reduced perimeter, not the topological-boundary length of an arbitrary null-set representative. In the L1-Lipschitz class, A is Lipschitz and this is an a.e. derivative inequality. In the larger BV class, singular increases can remain, but singular decreases cannot occur under this budget. Do not silently replace BV by AC or assert equality without saturation and exclusion of free faster-than-unit expansion.

Comparison is valid with a positive scalar solution a'=2 sqrt(pi a)-M, a(0)=A(0). On any interval a>=delta>0, set w=A-a and k=2 sqrt(pi)/(sqrt(A)+sqrt(a)). Then Dw>=k w dt, with k bounded. An integrating factor shows w>=0, including its nonnegative singular part. Let delta decrease to zero to reach extinction by traces. After extinction, the lower bound zero is automatic. No global Lipschitz assumption for sqrt at zero is needed.

## 3. Stronger positive-budget optimal example: moving critical disk

Fix R>0 and M=2 pi R. Let c:[0,T]->R2 be any Lipschitz center with c(0)=0 and |c'|<=1 a.e. Then Q_t=B_R(c(t)) is L1-Lipschitz, has smooth spatial boundary, and inward speed beta=-c' dot e at x=c+R e. Consequently beta>=-1 and

integral_boundary (1+beta) = 2 pi R = M.

Its area stays A0=pi R^2. The comparison in section 2, with the equilibrium solution a=A0, proves every admissible competitor starting from B_R(0) has A(t)>=A0. Therefore this translated disk is globally optimal for the terminal-area OP and for any nonnegative weighted running/terminal area cost. This is not only an arbitrary admissible example. It has a strictly positive budget and remains nonempty throughout. It does not establish optimality for a general penalized-effort functional.

### 3a. Interior kink, weak a.e. formulation

Take c' equal to v before an interior time t0 and -v afterward, with 0<|v|<1. Any C1 curve x(t) lying on the moving boundary at t0 would have to satisfy both

(x'(t0)-v) dot e0=0 and (x'(t0)+v) dot e0=0,

so v dot e0=0. Thus C1 boundary curves cannot cover the boundary at t0: only its two equatorial points pass this necessary condition. In particular there is no global C1, hence no A5, boundary parametrization. This example uses the a.e. admissible formulation; its classical normal speed is undefined at the kink time, so it must not be advertised as satisfying literal everywhere differentiability in the OWR prose.

Nevertheless AC/Lipschitz orthogonal trajectories do exist uniquely for initial labels: writing e(theta)=(cos theta,sin theta), solve

theta' = -(c' dot e_theta)/R.

The right side is measurable in time and uniformly Lipschitz in theta. Then x=c+R e(theta) has x'=(c' dot e)e a.e. The kink disproves universal C1 parametrizations of weak minimizers, not universal AC normal trajectories or existence of a smoother optimizer (the stationary disk is also optimal).

### 3b. Continuous-speed example satisfying the literal speed convention

Take c(t)=epsilon (|t-t0|^(3/2)-|t0|^(3/2)) e1, with epsilon small enough that max|c'|<1. This center is C1, and beta is continuous and defined at every time. The same optimality proof applies.

There cannot be an A5 parametrization. If x(t,xi) were jointly C1,1 and normal, then at t0, c'=0 implies x_t=0. Thus for each label x_t(t0+h)=O(|h|). At a label with e0 dot e1 !=0, the boundary identity requires x_t dot e = c' dot e, whose leading size is a nonzero constant times sign(h)|h|^(1/2), a contradiction. Here e(t)=(x(t)-c(t))/R converges to e0 and is Lipschitz near t0. This is an interior obstruction to joint C1,1 even with continuous speeds and smooth convex slices. Classical C1 orthogonal trajectories still exist, so this does not settle Q1 negatively at all possible interpretations.

## 4. Subcritical shrinking disk and extinction

For 0<R0<M/(2 pi), let k=M/(2 pi), R'=1-k/R and R(0)=R0. This saturates effort and solves the scalar lower-bound equation for area. It is globally area-optimal by section 2 until extinction, and stays area-optimal with the empty set afterward. Extinction time is

T*=k log(k/(k-R0))-R0.

As t increases to T*, R(t) is asymptotic to sqrt(2k(T*-t)); area decreases to zero with derivative tending to -M. Thus the set motion is L1-Lipschitz, although boundary-point speed diverges. Radial trajectories have total variation R0, extend absolutely continuously to the limiting origin, and are not Lipschitz near extinction. Their derivatives are integrable. Therefore divergent speed does not imply failure of AC trajectories.

There is no path valued in the boundary of the empty set at or after extinction. If a singleton representative is retained exactly at extinction, its topological boundary contains the origin, but that is a representative convention and does not permit continuation after the set is empty. Fixed-label nondegenerate parametrizations necessarily fail as the radius vanishes. These are endpoint/extinction phenomena, not evidence of interior irregularity before extinction.

## 5. Other candidate checks

- Zero-control expanding annulus B_(R0+t) minus closure(B_(r0-t)), until the hole vanishes, is admissible for every positive budget because effort is zero. Inner-boundary trajectories approach the origin while the surviving outer boundary stays a positive distance away. A full continuous labelled-boundary continuation through hole filling fails. Optimality is not established, so this cannot answer the original optimal-motion question.
- Two expanding disks meeting with M=0 are outside the stated M>0 convention; labeling this only a scope edge case is correct.
- Smooth normal reparametrization: for a regular embedding F(t,u), solve u'=-<F_t,F_u>/|F_u|^2. This cancels tangential velocity and proves normal curves under adequate joint regularity. Merely Lipschitz coefficients yield a bi-Lipschitz label flow, not automatically C1,1. A safe sufficient hypothesis for a jointly C1,1 reparametrization is F jointly C2,1 (or C3 on a compact cylinder), with |F_u| bounded away from zero. Under weaker hypotheses state exactly the flow regularity actually proved.

## Disposition

Source scope and optimality comparison pass subject to the explicitly stated BV budget class. The critical translated-disk examples are rigorous optimal special cases showing why a blanket claim that every optimizer satisfies A5 is too strong, even in convex geometry and away from extinction. They neither exclude smooth optimizers nor prove absence of AC orthogonal flows. Preserve the original problem's open disposition unless its precise quantifiers and trajectory regularity are resolved separately. This is a mathematical audit, not a resolution of the general question.

## 6. Second pass against the completed RESEARCH.md

The completed five-approach research file was read after the initial audit. Its exact graph nonuniqueness calculation passes: Y_s=(1,-sgn(s)sqrt(|s|)), so its displayed F is correct; integrating q' = sqrt(q)/(1+q) gives precisely t-a=2 sqrt(q)+(2/3)q^(3/2). Both signs and arbitrary waiting times are valid. A regular compact C1 Jordan curve can contain the patch and have finite perimeter; translating it at unit speed gives beta in [-1,1] and integral beta=0 by the divergence theorem, hence effort P. This example is admissible, not proved optimal, and the research correctly limits it accordingly.

Theorem 5.1 in arXiv:2307.03599, printed pp.36–38, explicitly asserts area domination over every other admissible strategy for the constructed convex motion. Its Remark 5.1 also expressly notes distinct translated optimal selections. For a disk, its scalar area ODE reduces to a'=2 sqrt(pi a)-M; the critical equilibrium and subcritical shrinking cases used in RESEARCH.md are therefore supported within that paper's stated admissible class. This theorem citation and the direct BV inequality in section 2 above are alternative routes, with their classes kept explicit, not an assertion that every null-set representative or every imaginable weak model is automatically covered.

The completed research's fixed-outer-radius annulus variant also passes: outer beta=0 costs 2 pi R, inner beta=-1 costs zero, and the positive-budget motion is L1-Lipschitz. Its component-loss conclusion is correct and expressly nonoptimal.

Final verdict: PASS for the stated partial results, with the continuous-speed example in section 3b recommended for inclusion. Universal A5 regularity of every area-optimal motion is disproved in the stated hard-budget class; the weaker general optimal AC-trajectory question, or existence of a regular optimal selection, remains unresolved. Do not relabel the original general question solved.
