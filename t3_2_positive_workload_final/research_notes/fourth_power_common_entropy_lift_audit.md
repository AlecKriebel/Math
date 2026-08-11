# Audit of the fourth-power common-entropy lift

## 1. Scope and verdict

Let

\[
 {\cal F}_\ell(x)=K+\sum_{i=1}^3\log(x_i!)+\ell\cdot x\ge1,
 \qquad
 W(x)=(1+{\cal F}_\ell(x))^4.                         \tag{1.1}
\]

This note isolates what the fourth-power proposal proves and what it does
not prove for the 1,227 all-one-active candidate pairs.

1. On every affine-feasible descriptor with at least two active
   coordinates, the Anderson--Kim passing-cone estimate lifts from
   \({\cal F}_\ell\) to \(W\). The powered carré du champ cannot reverse
   the sign.
2. A resistance gap for a *raw attempt* is insufficient. If a failed
   attempt changes a bounded inactive coordinate with order-one
   probability, its positive \(W\)-cost can dominate a rare service.
3. A completed neutral-base trace repairs that problem. If the first
   nonzero relative active return is down with probability
   \(1-N^{-1+o(1)}\), has mean duration \(N^{m+o(1)}\) with \(m\le2\),
   and its inactive endpoint has \({\cal F}\)-cost \(o(\log N)\), then it
   gives a strict \(W+\)time Foster episode.

The third item is an abstract theorem below. The exact arbitrary-orientation
base-regeneration theorem needed to apply it to all 23 analytic templates
is still open. No pair count or recurrence flag is promoted here.

## 2. Powered drift on a passing cone

Put \(U=1+{\cal F}_\ell\). For a reaction \(r\), write
\(\Delta_r={\cal F}_\ell(x+\zeta_r)-{\cal F}_\ell(x)\) and
\(\lambda_r=\lambda_r(x)\). The fourth-power identity is exact:

\[
\begin{split}
 {\cal L}W
 ={}&4U^3{\cal L}{\cal F}_\ell
   +6U^2\sum_r\lambda_r\Delta_r^2\\
  &+4U\sum_r\lambda_r\Delta_r^3
   +\sum_r\lambda_r\Delta_r^4.                        \tag{2.1}
\end{split}
\]

Along any divergent population sequence, with
\(n=1+\lvert x\rvert_1\),

\[
 U\asymp n\log(n+1),\qquad
 \max_r|\Delta_r|\le C\log(n+1).                      \tag{2.2}
\]

Let \(\beta(x)=\max_r\lambda_r(x)\) over enabled reactions. There are
finitely many channels, so

\[
 \sum_r\lambda_r|\Delta_r|^k
 \le C\beta(x)\log^k(n+1),\qquad k=2,3,4.             \tag{2.3}
\]

The discrete corrected-factorial version of the Anderson--Kim estimate on
a passing descriptor is

\[
 {\cal L}{\cal F}_\ell(x_j)
 \le-\beta(x_j)a_j,\qquad a_j\longrightarrow\infty.  \tag{2.4}
\]

Combining (2.1)--(2.4), the ratio of the whole convexity remainder to the
absolute first term is at most

\[
 C\left\{
 { \log^2(n+1)\over Ua_j}
 +{ \log^3(n+1)\over U^2a_j}
 +{ \log^4(n+1)\over U^3a_j}
 \right\}\longrightarrow0.                           \tag{2.5}
\]

Consequently

\[
 {\cal L}W(x_j)
 \le-2U(x_j)^3\beta(x_j)a_j\longrightarrow-\infty.   \tag{2.6}
\]

This proves the proposed lift on every feasible multi-active descriptor
which already passes the one-step tier test. It also shows why a crude
\(O(n^2\log^2n)\) carré estimate is harmless: it must be compared after
the common factor \(U^2\), not directly with
\({\cal L}{\cal F}_\ell\).

## 3. Why raw rare attempts do not compose

At a one-active shell \(X=N\), one active service has

\[
 \Delta{\cal F}_\ell=-\log N+O(1),\qquad
 \Delta W=-\Theta\{N^3(\log N)^4\}.                  \tag{3.1}
\]

If that service occurs in one raw attempt with probability \(N^{-m}\),
its expected powered gain is only

\[
 -\Theta\{N^{3-m}(\log N)^4\}.                       \tag{3.2}
\]

By contrast, an order-one change of a bounded inactive population has
\(\Delta{\cal F}_\ell=O(1)\), and hence

\[
 (\Delta W)^+=O\{N^3(\log N)^3\}.                    \tag{3.3}
\]

For \(m\ge1\), (3.3) is larger than (3.2). Thus it is invalid to charge an
inactive endpoint separately after every raw attempt. A resistance
inequality by itself does not establish a powered Foster inequality.

The cure is to continue through every zero-relative-reward base return.
Intermediate inactive changes then telescope. They are charged only once,
at the first nonzero active return, a finite target, or a genuine promoted
boundary.

## 4. A completed-trace lemma

Let \(X\) be the active coordinate, let \(N=X_0\), and start with positive
old reflected debt. Let \(\sigma_N\) be an all-reactions-retained stopping
time which ends at one of:

1. a **down return**, with \(X_{\sigma_N}=N-1\);
2. an **up return**, with \(X_{\sigma_N}\ge N+1\);
3. a finite marked target; or
4. a promoted state, followed by the original process in a region where
   (2.6) holds, until it returns to the base region, hits the finite
   target, or reaches a \(W\)-localization boundary.

Assume, uniformly along the one-active sequence, that for some
\(m\in\{0,1,2\}\):

\[
\begin{aligned}
 \mathbb P(\text{down return})&=1-N^{-1+o(1)},\\
 \mathbb P(\text{up return})&\le N^{-1+o(1)},         \tag{4.1}\\
 \mathbb E\sigma_N&\le N^{m+o(1)}.
\end{aligned}
\]

Assume also that, off the promoted continuation,

\[
 \left|
 {\cal F}_{\ell,\mathrm{inactive}}(X_{\sigma_N})
 -{\cal F}_{\ell,\mathrm{inactive}}(X_0)
 \right|=o_{L^1}(\log N),                             \tag{4.2}
\]

with sufficiently high positive endpoint moments to Taylor-expand \(W\).
On an up return, allow a relative active increment \(N^{o(1)}\) and impose
the corresponding \(L^4\) bound. The promoted continuation is stopped and
localized so that Dynkin's formula for (2.6) is uniformly integrable.

> **Lemma 4.1 (completed one-active fourth-power trace).** Under these
> hypotheses there are \(c,\eta>0\) such that, for all sufficiently large
> \(N\),
> \[
>  \mathbb E\!\left[
>    W(X_{\sigma_N})-W(X_0)+\eta\sigma_N
>  \right]\le-cN^3(\log N)^4.                         \tag{4.3}
> \]

### Proof

On a down return, (4.2) and the factorial first difference give

\[
 {\cal F}_\ell(X_{\sigma_N})-{\cal F}_\ell(X_0)
 =-\log N+o_{L^1}(\log N).                            \tag{4.4}
\]

Taylor expansion of \(U^4\), with the stated endpoint moments, gives

\[
 \mathbb E[\Delta W;\text{down}]
 \le-c_1N^3(\log N)^4.                                \tag{4.5}
\]

The up-return contribution is at most

\[
 N^{-1+o(1)}\,O\{N^{3+o(1)}(\log N)^4\}
 =o\{N^3(\log N)^4\}.                                 \tag{4.6}
\]

Equation (4.2) makes every remaining nonpromoted endpoint contribution
one logarithmic order smaller than (4.5). On a promoted segment, stopped
Dynkin applied to (2.6) makes the expected \(W+\eta\)time change
nonpositive. Localization boundary terms are included before the limit;
they are not renamed promotion or discarded. Finally

\[
 \eta\mathbb E\sigma_N
 \le N^{2+o(1)}
 =o\{N^3(\log N)^4\}.                                 \tag{4.7}
\]

Combining (4.5)--(4.7) proves (4.3). \(\square\)

The lemma is deliberately about the *completed* trace. Applying it to a
single rare trial would violate (4.2) and reproduce the scale error in
Section 3.

## 5. A moving finite phase is legitimate

The false terminal-chart argument inferred a fixed finite inactive box
from tightness. Lemma 4.1 needs no such inference. Choose a deterministic
cutoff \(M_N\uparrow\infty\) so slowly that

\[
 M_N\log(M_N+1)=o(\log N).                            \tag{5.1}
\]

Within the box, every propensity coefficient and every finite-state
resolvent constant is \(N^{o(1)}\), after slowing \(M_N\) further if
necessary. A degree-zero reaction which competes with an enabled
degree-one reaction costs one factor \(N^{-1+o(1)}\). Standard finite
singular-perturbation first-step equations then convert a graph resistance
\(m\) into

\[
 \mathbb E\sigma_N\le N^{m+o(1)}.                    \tag{5.2}
\]

The boundary \(M_N\) is retained. Along any sequence which reaches it, an
inactive coordinate diverges and refines to a multi-active descriptor.
For the 1,227 selector that descriptor passes, so the continuation uses
(2.6). Equation (5.1) makes the one-time boundary factorial cost
\(o(\log N)\), as required by (4.2).

This is a diagonal moving-box argument, not tightness-to-finite-support.
Its missing input is an orientation-uniform graph theorem: every
historically consistent positive-debt base must reach a down return or a
promoted boundary, and the first up return must have strictly larger
resistance.

## 6. Reduction of the 23 phase templates

The active-degree-one sources are a subset of

\[
 \{X,X+U,X+V\}.                                      \tag{6.1}
\]

At a no-fast base, every cofactor which occurs in a top source is zero.
Therefore:

1. if \(X\) itself is a top source, there is no no-fast base;
2. if both \(X+U\) and \(X+V\) occur, the only no-fast base is
   \(U=V=0\);
3. if only \(X+V\) occurs, a no-fast base has \(V=0\), with only \(U\)
   potentially unbounded; and
4. the sole wholly-top phase in the exact selector is the already isolated
   open pair \(\{X,X+U\}\), whose stripped process is
   immigration--death.

Thus the 23 templates do not hide an arbitrary two-dimensional no-fast
environment. Their unresolved regenerative cores are either finite,
one-dimensional, or the known open Poisson phase. In the one-dimensional
case, contracting each fast top excursion leaves a bounded-jump chain in
the unused cofactor. Strong connectivity forces a highest-degree return
path; a transient outward alternative reaches \(M_N\) and is promoted.

The recurrence part of that last statement can be made exact.

> **Proposition 6.1 (one-dimensional no-fast phase).** Suppose the sole
> top cofactor is \(V\), so the only top complex is \(X+V\), and work on
> the no-fast face \(V=0\). Every closed service-free zero-resistance
> component is either a finite singleton or an exponentially recurrent
> one-species mass-action chain on a subset of \(\{0,U,2U\}\). From a
> fixed regenerative atom, all return times, polynomial occupation
> integrals, and polynomially size-biased killed endpoints have finite
> exponential/polynomial moments. In fact its return maximum has a
> factorial-scale tail. The finite-\(N\) fast-window perturbation admits a
> stopped compensation expansion through resistance two with an
> endpoint-weighted \(O(N^{-3})\) remainder while it remains in regenerated
> closed components, and an \(N^{-3+o(1)}=o(N^{-2})\) remainder when an
> intermediate transient component is stopped at a subpolynomial moving
> boundary. A moving boundary reached
> from a non-regenerated start may nevertheless have order-one
> probability and is a retained promotion, not a tail error.

### Proof

A zero-resistance neutral transition is exactly one of:

1. a direct lower reaction between \(U\)-only complexes; or
2. a paired contraction
   \[
    y\longrightarrow X+V\longrightarrow z,
    \qquad y,z\in\{0,U,2U\}.                          \tag{6.2}
   \]

Indeed, a direct lower target containing \(V\) enables an immediate
unpaired top exit. In (6.2), if the first top-exit target still contains
\(V\), the next top exit is unpaired. Thus a neutral endpoint must again
have \(V=0\).

It follows that every closed service-free singular component is a
strongly connected one-species mass-action graph on a subset of
\(\{0,U,2U\}\). A singleton is finite. Otherwise put

\[
 \Psi_\theta(u)
 =\exp\{\theta u\log(u+e)\},\qquad 0<\theta<1.       \tag{6.3}
\]

For every fixed nonzero jump \(j\),

\[
 {\Psi_\theta(u+j)\over\Psi_\theta(u)}
 =u^{\theta j}e^{O(1)}.                              \tag{6.4}
\]

If the maximal complex degree is one, strong connectivity supplies a
strict \(U\to0\) edge of linear rate, whereas every upward edge has
constant rate. If the maximal degree is two, every edge sourced at
\(2U\) is nonincreasing and strong connectivity supplies a strictly
decreasing one of quadratic rate; every increasing edge has source degree
at most one. Equation (6.4), with \(\theta<1\), therefore gives

\[
 {\cal L}_{\rm neutral}\Psi_\theta(U)
 \le C-c(1+U)^p\Psi_\theta(U),
 \qquad p\in\{1,2\}.                                \tag{6.5}
\]

The contracted rate in (6.2) is the lower entry propensity multiplied by
a positive constant top-exit probability, because all outgoing clocks at
\(X+V\) share the same factor \(XV\). Therefore it has exactly the
one-species mass-action form used in (6.5).

Stopped Dynkin and the multiplicative drift in (6.5) give an exponential
moment for the hit of a fixed finite set. Irreducibility inside that set
and a geometric trial give an exponential return moment to a fixed atom.
The stopped supermartingale also gives

\[
 \mathbb P_{u_*}\!\left\{
   \max_{t\le\tau_{u_*}^+}U_t\ge M
 \right\}\le C\exp\{-cM\log(M+e)\}.                 \tag{6.6}
\]

Polynomial occupation moments follow from the same drift hierarchy. If a
killing intensity has degree at most two, compensation merely
polynomially size-biases those bounds, so the killed endpoint still has
every fixed polynomial moment.

Finite-\(N\) lower interference during a top window has active-clock
intensity at most \(C(1+U)^2/N\). Let \(\tau_*\) be one regenerated
neutral cycle and put

\[
 A=\int_0^{\tau_*}(1+U_s)^2\,ds.                    \tag{6.7}
\]

Equation (6.5) gives \(\mathbb E A^q<\infty\) for every fixed \(q\).
As long as the marked path remains in regenerated closed components, the
ordered compensation formula therefore bounds the contribution of three
or more interference clocks by

\[
 {C\over N^3}\mathbb E A^3=O(N^{-3}),               \tag{6.8}
\]

and the same estimate holds after any fixed polynomial endpoint weight.
After either of the first two bounded interference jumps, the estimate is
restarted if the new marked component is closed and recurrent; service and
promotion outcomes are stopped. If an intermediate component is transient,
stop it at a boundary \(M_N=N^{o(1)}\). Its polynomial occupation cost is
then \(N^{o(1)}\), so three interferences contribute
\(N^{-3+o(1)}=o(N^{-2})\), and the boundary outcome is retained. Thus the
aggregate killed kernel has its ordinary expansion through resistance two
with the endpoint-weighted remainder required here. This is a weighted
compensation argument; an unqualified finite-box operator norm would not
be uniform as the box grows.

For comparison, one may localize a cycle begun at the fixed atom at
\(M_N=N^\delta\), \(0<\delta<1/6\). Below that boundary the instantaneous
perturbation is \(O(N^{2\delta-1})\), and (6.6) makes the boundary event
superpolynomially small. This is only an alternative localization of the
compensation proof, not a fixed-phase reduction.

The tail assertion in (6.6) is not uniform over starts
\(U_0\asymp M_N\). Such a start, or a transient component which reaches
\(M_N\) before regeneration with order-one probability, is a genuine
promotion outcome. Its endpoint obeys
\[
 {\cal F}_{\ell,U}(M_N)=O(M_N\log M_N).               \tag{6.9}
\]
and must be charged by the same-\(W\) promotion contract; it is not
discarded using (6.6). If the moving boundary is instead chosen
diagonally so slowly that \(M_N\log M_N=o(\log N)\), its one-time
factorial endpoint cost is smaller than one active decrement. This fact
alone does **not** prove the repeated promotion bound. If the boundary is
accessed at resistance \(k\) while service has resistance \(m\), its
unconditional powered cost is of order

\[
 N^{-k}N^3(\log N)^3M_N\log M_N.                    \tag{6.10}
\]

When \(k<m\), that quantity can dominate the service contribution even
though \(M_N\log M_N=o(\log N)\). Such an early boundary must be included
inside the completed neutral trace, shown to have favorable signed
\(W\)-drift, or supplied with a stronger access estimate. It cannot be
renamed promotion merely because \(M_N\to\infty\).

Consequently the one-dimensional neutral phase cannot be null recurrent:
it regenerates with exponential endpoint moments, takes a resistance
edge/service, or reaches the retained promoted boundary. This proves the
proposition. \(\square\)

There is also an exact small-interference consequence for the finite mixed
templates.

> **Proposition 6.2 (two-interference boundary dichotomy).** Exclude the
> direct-\(X\) rows and the wholly-top open pair, which have their own
> kernels. Start a no-fast mixed episode from a bounded inactive mark, stop
> at the first down/up return, and let \(J\) count degree-zero reactions
> fired while a degree-one source is enabled. Conditional on \(J\le2\),
> the probability that an inactive population reaches
> \(L_N=N^\delta\) is superpolynomially small. On \(J\ge3\), the ordered
> compensation estimate, stopped below \(L_N\), is
> \[
>  \mathbb E[(1+J)^q;J\ge3]
>  \le C_qN^{-3+6\delta}                              \tag{6.11}
> \]
> for every fixed \(q\), provided the corresponding regenerated
> occupation moments are used. Moreover the positive relative active
> displacement satisfies \(r^+\le1+J\).

To see the dichotomy, while a fast source is enabled, stripping \(X\)
from an active complex leaves only \(0,U,V\). Top-to-top reactions do not
branch inactive particles. Before the first down return, the free launch
and \(J\le2\) paid entries allow at most three top exits; every top-exit
target and every paid lower reaction has molecularity at most two. Thus a
large inactive population cannot be made by this finite carrier segment.
If no fast source is enabled, the exact binary support classification
leaves either a finite base or the one-dimensional phase of Proposition
6.1. The latter has the factorial maximum tail (6.6). This proves the
first assertion.

For the exact 1,227-pair architecture the routing is even sharper. The
mixed-\(X\)-source rows have an immediately enabled killed top phase;
Families I and III have no-fast base only at the origin, because every
nonzero inactive molecule enables one of \(X+U,X+V\); and the Family II
spectator axis is fixed by an exact linkage invariant. The only unbounded
wholly-top phase is the stripped open pair \(\{0,U\}\), an
immigration--death chain with the factorial tail above. Hence none of the
3,297 exact incidences has a nonfactorial promotion route after at most two
suppressed entries.

Below \(L_N\), each suppressed-clock coefficient is at most
\(CL_N^2/N\). The endpoint-weighted ordered compensation formula and the
occupation hierarchy give (6.11). Every positive active increment after
the free launch is one of those suppressed lower-to-top entries, whereas
top-to-top reactions have active increment zero and exits have increment
minus one. Hence \(r^+\le1+J\).

The last bound is deliberately moment-based. A deterministic estimate
\(r^+\le CL_N\) is false: alternating nested entries such as
\(U\to X+V\) and \(V\to X+U\) can keep one inactive molecule while
accumulating active carriers. Each nesting is, however, another counted
suppressed entry, so (6.11) is the estimate needed by the fourth-power
endpoint calculation.

The generator-good continuation itself has no hidden localization/UI
problem. The following elementary lemma is useful.

> **Lemma 6.3 (stopped good excursion).** Let \(G\) be a set on which
> \({\cal L}W\le-a<0\), let the physical chain be nonexplosive, and let
> \(\rho\) be the first hit of \(G^c\). For every \(y\in G\),
> \[
>  \mathbb E_y[W(X_\rho)-W(y)+a\rho]\le0,
>  \qquad \mathbb E_y\rho\le W(y)/a.                 \tag{6.12}
> \]
> In particular \(\rho<\infty\) almost surely.

Indeed, stop additionally at time \(R\) and at a finite population
sublevel. Dynkin's formula gives (6.12) for the localized stop. Monotone
convergence applies to the elapsed time and Fatou applies to the
nonnegative endpoint \(W\). The duration bound forces \(\rho<\infty\);
nonexplosion then makes the localized endpoints converge to \(X_\rho\).
No positive-endpoint uniform integrability is needed for this signed
inequality.

Lemma 6.3 pays the whole good excursion after a tube exit, but it does not
classify the state at reentry. A same-axis return at the same active level
and with a finite phase mark is neutral and may be telescoped. A return
which lowers the old active coordinate reduces old debt. A same-axis
return at a substantially higher active level, or a switch to a higher
scale on another axis, still needs either an aggregate upward-resistance
bound or a signed scale-stopped argument. All-species reflected debt makes
an axis switch visible--the formerly large coordinate has lost debt--but
does not by itself bound the powered cost of the newly large coordinate.

This closes the countable-phase recurrence issue for the unbounded no-fast
template. A separate arbitrary-orientation graph theorem now supplies the
wordwise bounds \(m_-\le2<m_+\) for the mixed templates. That graph theorem
does not by itself supply aggregate stopped probabilities; the phase and
endpoint conversion below remains analytic.

## 7. A completed-service Dirichlet corrector is too large

A finite-tube Green corrector can be useful for the neutral phase, but it
does not replace the completed stopping argument. The obstruction is
already visible in a one-state model. Let a tube state \(b_N\) jump to a
service boundary at rate \(\varepsilon_N=N^{-m}\), and suppose that jump
changes \(W\) by

\[
 -H_N,
 \qquad H_N=N^3(\log N)^4.                           \tag{7.1}
\]

Impose \(\chi=0\) at the service boundary and ask for
\({\cal L}(W+\chi)=-1\) at \(b_N\). The Dirichlet equation is

\[
 -\varepsilon_NH_N-\varepsilon_N\chi(b_N)=-1,
 \qquad
 \chi(b_N)=\varepsilon_N^{-1}-H_N.                  \tag{7.2}
\]

For \(m\le2\), \(|\chi(b_N)|\sim H_N\), not
\(O(N^3(\log N)^3)\). Thus a value corrector for the kernel completed all
the way to service carries the full terminal service reward. Setting it to
zero at a promotion boundary creates a seam toll of the same order as the
desired descent.

An \(O(N^3(\log N)^3)\) corrector may still solve the finite neutral-phase
Poisson equation after the terminal active reward is left explicitly in
the generator, or on an augmented raw-attempt mark. That smaller statement
does not itself prove service or promotion access. In particular, one may
not infer the claimed corrector bound by multiplying a per-attempt phase
oscillation by a Green kernel and overlooking the terminal condition.

## 8. Exact remaining gate

To promote the 1,227-pair branch, one still needs an arbitrary-orientation
stopped-kernel theorem with the following precise content.

1. The wordwise arbitrary-orientation bounds \(m_-\le2<m_+\) must lift to
   aggregate completed-return probabilities with the endpoint-weighted
   remainder in Proposition 6.2.
2. Every zero-resistance closed component must be either a genuine regenerative
   component with the finite resolvent estimates used in (5.2), or reaches
   the promoted boundary with the fourth-power endpoint moments.
3. The wholly-top open phase must satisfy the same completed-return statement
   after its Poisson regeneration.
4. Moving-cutoff endpoints must use the weighted carrier/interference
   estimate, not the false deterministic active-overshoot bound discussed
   after (6.11).

Once these four graph/phase statements hold, Lemmas 2.1 and 4.1 give the
common-\(W\) physical-time Foster inequality and the all-species reflected
marks give a finite classwise target. Until then, resistance separation
alone is not a recurrence proof, and all universal one-active counts must
remain false.
