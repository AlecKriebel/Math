# Common catalyst with every residual lower support

**Proof-first standalone theorem, 2026-08-12 PDT.**  This note proves the
all-clock workload macro for the homogeneous common-catalyst top support

\[
                         T=\{X+Y,Y+Z,2Y\}              \tag{1.1}
\]

paired with every lower support occurring in the residual 336 family:

\[
 R=\{0\}\cup U,\qquad
 U\in\big\{\{X,Y\},\{X,Z\},\{Y,Z\},\{X,Y,Z\}\big\}. \tag{1.2}
\]

Both supports carry arbitrary strongly connected labelled directed graphs
and arbitrary fixed positive rates.  The argument is symbolic and retains
every clock.  In particular, order-\(H\) lower activity sourced at \(X\) is
not contracted, conditioned away globally, or treated as a bounded phase.

## 1. Exact workload theorem

Put \(H=X+Y+Z\).  Let \(B_t\) count all zero-source births and let
\(D_t\) count all labelled direct lower deaths \(u\to0\).  Every top
reaction and every nonzero lower transfer preserves \(H\), so pathwise

\[
                         H(X_t)-H(X_0)=B_t-D_t.         \tag{1.3}
\]

> **Theorem 1.1 (general common-catalyst macro).**  Fix a network with
> supports (1.1)--(1.2).  On every closed irreducible class which is not a
> catalyst-free invariant reduction, there are constants \(R,C<\infty\),
> \(a>0\), and \(\eta>0\) such that, from every state \(x\) with
> \(H(x)\ge R\), an all-clock stopping time \(\tau_x\) can be selected
> with an actual physical endpoint and at least one ordinary jump, satisfying
> \[
>       0<\mathbb E_x\tau_x\le C,\qquad
>       \mathbb E_x(D_{\tau_x}-B_{\tau_x})\ge a,       \tag{1.4}
> \]
> and therefore
> \[
>  \mathbb E_x\{H(X_{\tau_x})-H(x)+\eta\tau_x\}\le0. \tag{1.5}
> \]
> Moreover \(\mathbb E_xH(X_{\tau_x})<\infty\).  If \(Y\notin U\) and
> a class lies in \(Y=0\), that face is invariant, the top linkage is dead,
> and the class is an open-unary reduction; it is positive recurrent by a
> linear Foster function.

The theorem supplies exactly the occupation macro in the workload-only
physical-time Foster theorem.  It makes no bound on the number of neutral
top reactions.

## 2. Labelled top particles and protected paths

Assume \(Y\ge1\), remove one persistent catalyst, and set

\[
 z_{\mathsf X}=X,\qquad z_{\mathsf Z}=Z,
 \qquad z_{\mathsf Y}=Y-1.                            \tag{2.1}
\]

The three source propensities factor exactly:

\[
 (x)_{X+Y}=Yz_{\mathsf X},\qquad
 (x)_{Y+Z}=Yz_{\mathsf Z},\qquad
 (x)_{2Y}=Yz_{\mathsf Y}.                            \tag{2.2}
\]

After aggregating labelled top rates, let \(Q\) be the irreducible
three-state generator on \(\{\mathsf X,\mathsf Z,\mathsf Y\}\).  With

\[
                              A(t)=\int_0^tY(s)\,ds,  \tag{2.3}
\]

the \(H-1\) free labels move independently with generator \(Q\) in
operational time:

\[
                              {\cal L}_T=Y{\cal L}_Q. \tag{2.4}
\]

Fix an operational block length \(a_0>0\).  For each initial type
\(i\), choose a simple \(Q\)-path to \(\mathsf Y\), of length at most two.
For one initial free label define a protected event as follows.

1. In prescribed disjoint operational subintervals, its chosen top arrows
   occur and its competing top arrows do not.
2. Once it first reaches \(\mathsf Y\), every later top arrow out of
   \(\mathsf Y\) is absent through operational time \(a_0\).
3. Until that first \(\mathsf Y\)-hit, no lower unary clock sourced at
   \(X\) or \(Z\) acts on this label.

To realize the last requirement without conditioning on the block duration,
use the standard per-molecule graphical construction for unary mass action:
attach to each label an independent physical-time Poisson clock of rate
\(K_*\), where \(K_*\) dominates the total lower rate of one \(X\)- or
\(Z\)-molecule, and require no mark in the first \(a_0\) units of physical
time.  Thinning realizes every actual lower label clock.  The top and lower
graphical clocks are independent between distinct labels.  On the global
event of Section 3, \(Y\ge1\), so the physical block duration is at most
\(a_0\).  Hence there is a fixed

\[
 p_*\ge p_Qe^{-K_*a_0}>0                              \tag{2.5}
\]

such that every initial free label is protected with probability at least
\(p_*\), independently over labels.

The per-label lower-clock requirement prevents a protected \(X\)- or
\(Z\)-label from being transferred or killed before its terminal hit.  Once
it is at \(Y\), the global clean event in Section 3 suppresses its lower
\(Y\)-clock and the protected top event suppresses its top \(Y\)-out arrows.
Arbitrary lower events involving other labels remain active and do not
invalidate a protected success.  One could allow a helpful \(Z\to Y\)
transfer as an earlier terminal hit, but the stronger no-lower-mark event is
used here so that the protected indicators are literally independent.

Let \(S\) be the number of protected initial labels.  Uniform binomial
Chernoff gives constants \(c>0\) and \(n_0\) such that, for every initial
free-particle profile,

\[
             \mathbb P\{S\ge p_*(H-1)/2\}\ge1-e^{-cH}
             \qquad(H\ge n_0).                       \tag{2.6}
\]

## 3. The global clean event

Let \(K_Y^R\) be the total lower rate per \(Y\)-molecule, with
\(K_Y^R=0\) when \(Y\notin U\), and let \(\beta>0\) be the aggregate
zero-source birth rate.  From \(Y\ge1\), run every clock until the first of

* an increment \(a_0\) of \(A\);
* a lower event sourced at \(Y\);
* a zero-source birth; or
* the fractional-return stop defined in Section 5.

Call the block **unspoiled** when neither listed adverse clock occurs before
the earlier of the operational endpoint and the fractional-return stop.
Conditional on all top and all \(X/Z\)-sourced lower graphical histories,
the top linkage preserves at least one catalyst before a \(Y\)-sourced lower
event and lower \(X/Z\)-events cannot remove it.  Hence \(Y\ge1\), and an
operational interval of length \(a_0\) takes at most \(a_0\) physical time.
The integrated adverse hazards before the earlier endpoint are bounded by

\[
 K_Y^R\int Y(t)\,dt+\beta t
       \le(K_Y^R+\beta)a_0.                           \tag{3.1}
\]

Therefore the conditional probability of the global unspoiled event is at least

\[
                         q_0=e^{-(K_Y^R+\beta)a_0}>0. \tag{3.2}
\]

The conditioning order is important: first reveal the protected-label
events and every allowed lower history, and then suppress the disjoint birth
and \(Y\)-source clocks.  Combining (2.6) with (3.2) gives

\[
 \mathbb P\{F\text{ occurs, or the block reaches the shell}\}
                    \ge q_0(1-e^{-cH}).               \tag{3.3}
\]

On the fractional-return branch the macro has already succeeded.  Otherwise
the unspoiled block reaches its operational endpoint, and every protected
label is still at \(Y\).  No birth occurred, so
\(H_{\rm end}\le H_{\rm start}\).  With \(\rho=p_*/4\), for all large
block-start workloads,

\[
                  Y_{\rm end}\ge\rho H_{\rm start}
                               \ge\rho H_{\rm end}.    \tag{3.4}
\]

Thus one active block reaches a catalyst shell with a fixed probability,
uniformly over every allowed lower support and all large initial profiles.
All nonsuppressed lower deaths remain in \(D\) and are favorable.

## 4. Uniform seeding of the catalyst

Suppose \(Y=0\) and \(Y\in U\).  The top linkage is dead.  Choose a simple
directed lower path

\[
                         0=u_0\longrightarrow u_1
                           \longrightarrow\cdots\longrightarrow u_m=Y,
                                                               \tag{4.1}
\]

with \(m\le3\).  Wait for the selected constant label \(0\to u_1\), tag
that molecule, and require its successive selected unary labels.  Before the
final step, \(Y=0\), so no top clock can act.  The tagged molecule's total
unary rate is fixed, its selected branch probabilities are positive, and a
deviation simply starts a new trial from the actual endpoint.  Trials are
geometrically dominated.  Other molecules do not delay the selected
constant clock or the tagged unary lifetimes; if another event creates
\(Y\), stop successfully, and count every direct death as favorable.

Consequently the seed time \(\sigma_s\) and seed birth count have uniform
finite first moments:

\[
       \sup_{x:Y(x)=0}\mathbb E_x\sigma_s<\infty,
       \qquad
       \sup_{x:Y(x)=0}\mathbb E_xB_{\sigma_s}<\infty,
       \qquad Y(X_{\sigma_s})\ge1.                    \tag{4.2}
\]

If \(Y\notin U\), the coordinate face \(Y=0\) is invariant for the full
network.  On a class in this face the top linkage is dead and the remaining
system is an open unary linkage.  Killing its finite unary graph on reaching
zero gives a transient subgenerator \(Q_R\); the positive vector
\((-Q_R)^{-1}{\bf1}\) supplies a linear Foster function.  Such a class is
already positive recurrent.  On any other class, \(Y\ge1\) and no seed is
needed.

## 5. Geometric prelude

Fix a start \(x\) and put \(H_0=H(x)\).  If already
\(Y\ge\rho H\), stop the prelude at time zero and proceed to service.
Otherwise repeat complete attempts:

1. when \(Y=0\), use the seed of Section 4;
2. from \(Y\ge1\), use the active block of Section 3.

Stop the prelude immediately after any physical jump for which

\[
                              H\le H_0/2.              \tag{5.1}
\]

Also stop on the catalyst shell (3.4).  Until (5.1), every active block
starts above \(H_0/2\); after enlarging the fixed workload threshold, (3.3)
gives one conditional success probability at every attempt.  The number of
complete attempts is geometrically dominated.  Each active block has
physical duration at most \(a_0\) and stops at its first adverse birth, so it
adds at most one birth on failure.  Each seed has the uniform bounds (4.2).
Therefore constants independent of \(H_0\) satisfy

\[
             \mathbb E\tau_{\rm pre}\le C_{\rm pre},
             \qquad
             \mathbb E B_{\tau_{\rm pre}}\le C_B.     \tag{5.2}
\]

The endpoint alternatives are disjoint:

\[
 \begin{array}{ll}
 F:& H\le H_0/2,\qquad D_{\rm pre}-B_{\rm pre}\ge H_0/2;\\[2mm]
 I:& Y\ge\rho H,\qquad H>H_0/2.
 \end{array}                                          \tag{5.3}
\]

All deaths in failed attempts are retained.  No first-death restart or local
ledger threshold is used.

## 6. Uniform service on the catalyst shell

Let

\[
                  \delta_i=\sum_{i\to0}\kappa_{i0},
                  \qquad i\in\{X,Y,Z\}.              \tag{6.1}
\]

At least one \(\delta_i\) is positive by strong connectivity of \(R\).
On the unit simplex, the top ODE is exactly

\[
       \frac{dq}{ds}=q_{\mathsf Y}qQ,
       \qquad q(\theta)=q(0)e^{Q\theta},
       \qquad \frac{d\theta}{ds}=q_{\mathsf Y}.       \tag{6.2}
\]

Uniformly over \(q_{\mathsf Y}(0)\ge\rho\), bounded operational intervals
obey \(q_{\mathsf Y}(\theta)\ge\rho e^{-K\theta}\), so every fixed
operational time is reached in uniformly finite physical time.  Since \(Q\)
is irreducible, \(q(0)e^{Q\theta}\) converges uniformly over the simplex to
its strictly positive invariant vector.  Hence, after a uniform finite
physical time, every coordinate is bounded below by one fixed positive
constant.  For every prescribed \(D_0\), a finite physical fluid horizon
\(T(D_0)\) therefore satisfies

\[
 \inf_{q_{\mathsf Y}(0)\ge\rho}
 \int_0^{T(D_0)}\sum_i\delta_iq_i(s)\,ds\ge2D_0.      \tag{6.3}
\]

Start the full chain at a shell endpoint of workload \(n\), and run all
clocks for physical time \(T(D_0)/n\).  On the rescaled interval the top
density martingale has quadratic variation \(O(n^{-1})\), the top drift is
uniformly Lipschitz on the simplex, and lower unary and constant reactions
make only \(O(1)\) jumps and hence an \(o(1)\) density perturbation.
Localization and Gronwall give uniform \(L^1\) convergence to (6.2).  The
direct-death compensator and (6.3) imply, for all sufficiently large \(n\),

\[
              \inf_{\rm shell}\mathbb E D_{\rm serv}\ge D_0,
              \qquad
              \mathbb E B_{\rm serv}=\frac{\beta T(D_0)}n.          \tag{6.4}
\]

Append one final ordinary jump.  The total hazard is at least \(\beta>0\),
so its holding time has mean at most \(1/\beta\), and it adds at most one
birth.  This guarantees a genuine jump even when the macro starts on the
shell and the deterministic service window contains no reaction.

## 7. Expected ledger closure

Choose

\[
                              D_0=C_B+3.               \tag{7.1}
\]

Then enlarge \(R\) so that \(R/2\ge D_0\), the graphical block estimate is
uniform above \(R/2\), (6.4) holds, and the service-window expected birth
count is at most one.  On \(F\), (5.3) gives net ledger at least \(D_0\).
On \(I\), discard all favorable prelude deaths, use conditional service at
least \(D_0\), and subtract the prelude, service, and final-jump births.
Thus

\[
\begin{aligned}
 \mathbb E(D_\tau-B_\tau)
 &\ge D_0\mathbb P(F)+D_0\mathbb P(I)-(C_B+2)\\
 &\ge1.
\end{aligned}
\tag{7.2}
\]

This is an expectation-level ledger; no successful block is asked to repay
the realized births in preceding failures.  Equations (5.2), (6.4), and the
final holding bound give \(\mathbb E\tau\le C<\infty\).  Since
\(H(X_\tau)\le H(x)+B_\tau\), endpoint workload is integrable.  With
\(a=1\) and \(\eta=1/(2C)\), (1.3) and (7.2) prove (1.4)--(1.5).

## 8. Classwise conclusion and scope

Population-increasing channels have at most linear propensity; quadratic
top clocks preserve the proper workload and cannot accumulate in a finite
sublevel.  Thus the chain is nonexplosive.  Every failure restarts at its
actual endpoint by the strong Markov property, every clock remains active,
and the complete macro contains a physical jump.

The theorem covers all four relative lower-support patterns in (1.2).  It
therefore repairs precisely the scope restriction of the two-unary
\(R=\{0,Y,Z\}\) operational theorem while preserving its physical-time
ledger interface.  Combined with the workload-only physical-time Foster
theorem, it proves positive recurrence on every nonreduced fixed class; the
only excluded face is an exact catalyst-free open-unary reduction, which is
positive recurrent directly.
