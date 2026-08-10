# The exact-flat rank-one carrier with every lower channel present

## 1. Scope

This note upgrades the one-clock occupation estimate in Proposition 4.2
of two_active_promotion_phase.md to the **full** lower linkage. It applies
to exactly

\[
 893+2=895                                                \tag{1.1}
\]

rank-one flat two-active incidences: 893 have an enabled maximal lower
source at the displayed cap, and two first obtain that source through the
top phase. The 25 strictly lower activation incidences and the ten finite
zero-boundary incidences are kept separate in Section 6.

The result is sequence-local, as a tier argument must be: constants may
depend on the exact within-tier limiting ratios after passage to a
subsequence. No uniformity over ratios approaching a refined D-tier is
claimed.

## 2. Exact tier notation

Let \(L_*\) be the rank-one linkage wholly contained in the network top
D-tier, and \(L_-\) the other linkage. Let

\[
 m(y)=w\cdot y,\qquad
 m_*=\max_{y\in L_-}m(y),\qquad
 {\cal M}=\{y\in L_-:m(y)=m_*\}.                          \tag{2.1}
\]

The finite certificate checks that \(m_*=1\) in all 930 rank-one
incidences and that \({\cal M}\) is a proper nonempty subset of \(L_-\).
For a realizing sequence \(x_n\), put

\[
 a_n=\max_{y\in L_-}(x_n\vee1)^y.                         \tag{2.2}
\]

Exact D-tier realization means

\[
 {(x_n\vee1)^y\over a_n}\longrightarrow c_y\in(0,\infty)
 \quad(y\in{\cal M}),\qquad
 {(x_n\vee1)^z\over a_n}\longrightarrow0
 \quad(z\in L_-\setminus{\cal M}).                        \tag{2.3}
\]

This is stronger than equality of normalized logarithmic weights. In
particular, it retains arbitrarily slow subpower separation between the
two lines in (2.3).

The top linkage preserves

\[
 H_w(x)=w\cdot x                                          \tag{2.4}
\]

pathwise. A lower reaction sourced in \({\cal M}\) cannot increase
\(H_w\); it is neutral if its target is in \({\cal M}\), and decreases
\(H_w\) by at least one otherwise.

## 3. Integrated all-channel bounds

Run only \(L_*\), starting from \(x_n\), and denote that chain by
\(\widehat X^{(n)}\). Proposition 4.2 gives, for every enabled
\(y\in{\cal M}\), after passage to a subsequence, constants
\(T_y,\eta_y,p_y>0\) such that

\[
 {\mathbb P}_{x_n}\left\{
   \int_0^{T_y/a_n}(\widehat X_t^{(n)})_y\,dt\ge\eta_y
 \right\}\ge p_y.                                        \tag{3.1}
\]

The transient estimates used in that proposition give the companion
upper bound which is needed when other clocks are restored. If

\[
\begin{split}
 \Lambda_{\cal M}(x)
 &=\sum_{\substack{e\in E_-:\ {\rm src}(e)\in{\cal M}}}
      \kappa_e(x)_{{\rm src}(e)},\\
 \Lambda_{<}(x)
 &=\sum_{\substack{e\in E_-:\ {\rm src}(e)\notin{\cal M}}}
      \kappa_e(x)_{{\rm src}(e)},
\end{split}                                               \tag{3.2}
\]

where \(E_-\) is the directed edge set of \(L_-\); top-linkage clocks
are part of the conditioned path and are not included in these hazards.

then for every fixed \(T\) and integer \(r\ge1\),

\[
\begin{split}
 \sup_n\mathbb E\left[
   \int_0^{T/a_n}\Lambda_{\cal M}(\widehat X_t^{(n)})dt
 \right]^r&<\infty,                                      \tag{3.3}\\
 \mathbb E\int_0^{T/a_n}
   \Lambda_<(\widehat X_t^{(n)})dt&\longrightarrow0.      \tag{3.4}
\end{split}
\]

Here is the required uniform-integrability argument; endpoint moments
alone would not suffice.  For a lower complex \(z\), write

\[
 d_{z,n}=(x_n\vee1)^z,
 \qquad r_{z,n}={d_{z,n}\over a_n}.                       \tag{3.5}
\]

After passage to the exact-D-tier subsequence, each of the three top
templates has the following *pointwise path-moment* estimate: for every
fixed \(T,r\),

\[
 \sup_n\sup_{0\le t\le T/a_n}
 {\mathbb E[(\widehat X_t^{(n)}\vee1)^{rz}]
       \over d_{z,n}^{\,r}}\le C_{T,r,z}.                 \tag{3.6}
\]

The proof of (3.6) is elementary in each template.

1. On a homogeneous quadratic shell, the active total is conserved and
   is comparable to \(a_n\).  Exact top-tier equivalence keeps every
   active coordinate which occurs in \(z\) comparable to that total at
   time zero.  The inactive coordinate is constant.  Thus (3.6) is a
   deterministic shell bound.

2. For \(L_*=\{B,2A\}\), put \(N_n=A_n\vee1\) and
   \(q=A+2B\).  Exact top-tier equivalence gives
   \(cN_n^2\le q\le CN_n^2\) and \(a_n\asymp N_n\).  On the
   interval \([0,T/N_n]\), the number of positive jumps of \(A\) is
   stochastically dominated by
   \[
      Y_n\sim {\rm Poisson}(C N_n^2T/N_n)
             ={\rm Poisson}(CTN_n).
   \]
   Consequently
   \[
      \sup_{t\le T/N_n}{A_t\over N_n}
      \le {A_0+2Y_n\over N_n},
      \qquad
      \sup_n\mathbb E\left[\sup_{t\le T/N_n}
           (1+A_t/N_n)^r\right]<\infty.                 \tag{3.7}
   \]
   The inactive coordinate is constant.  Since every lower source has
   active weight at most one, it contains no \(B\), and (3.7) proves
   (3.6).  Notice that (3.7), rather than convergence of the Riccati
   endpoint alone, also controls rare upward excursions.

3. For \(L_*=\{2A,B+C\}\), set \(N_n=A_n\vee1\). Let \(I\) be
   the bounded cofactor and \(R\) the other member of \(B+C\). Thus
   \(I=C,R=B\) for \(w=(1,2,0)\), and \(I=B,R=C\) for the
   relabelled \(w=(1,0,2)\) case. The two top invariants are
   \[
      J=A+2I,\qquad K=R-I.                               \tag{3.8}
   \]
   Exact top-tier equivalence and the fixed displayed cap give
   \(J\le CN_n\), \(K\ge cN_n^2\), and \(a_n\asymp N_n\).
   The exact birth and death rates of the one-dimensional top chain
   satisfy
   \[
      b_I\le C_1N_n^2,\qquad d_I\ge c_1N_n^2 I.          \tag{3.9}
   \]
   Hence, for a fixed sufficiently small \(\theta>0\), the generator
   applied to \(V(I)=e^{\theta I}\) obeys
   \[
      {\cal L}_*V(I)
      \le N_n^2\{C_2-c_2V(I)\}.                          \tag{3.10}
   \]
   To see this directly, divide by \(V(I)\): the birth term is at most
   \(C_1N_n^2(e^\theta-1)\), whereas the death term is at most
   \(-c_1N_n^2I(1-e^{-\theta})\); enlarge the constant on the finite
   set of smaller \(I\).  Dynkin's formula and Gronwall therefore give
   \[
      \sup_n\sup_{t\ge0}\mathbb E e^{\theta I_t}<\infty.\tag{3.11}
   \]
   Also \(A_t\le J\le CN_n\) pathwise.  A lower source of active weight
   at most one is one of an inactive-only source or \(A\) times at most
   one inactive molecule.  Thus (3.11) proves (3.6), including the two
   cases started with \(I=0\). No assertion about the path supremum of
   \(I\) is needed.

The falling-factorial propensity is bounded by the corresponding
surrogate monomial.  Jensen's inequality and (3.6), with
\(h_n=T/a_n\), now give for every lower edge sourced at \(z\)

\[
 \begin{split}
 \mathbb E\left[\int_0^{h_n}\kappa_e
              (\widehat X_t^{(n)})_z\,dt\right]^r
 &\le h_n^{r-1}\kappa_e^r
       \int_0^{h_n}\mathbb E(\widehat X_t^{(n)})_z^r\,dt\\
 &\le C_{T,r,z}\,r_{z,n}^{\,r}.                          \tag{3.12}
 \end{split}
\]

For \(z\in{\cal M}\), the ratios \(r_{z,n}\) converge to finite
positive constants, so summing (3.12) over the finite edge set proves
(3.3).  For \(z\notin{\cal M}\), (2.3) gives
\(r_{z,n}\to0\); (3.12) with \(r=1\), followed by the same finite sum,
proves (3.4).  This is the promised uniform-integrability factorization:
it remains valid however slowly the submaximal ratio tends to zero.

The same estimates remain valid after any bounded number of lower
top-to-top reactions. Such reactions change populations by \(O(1)\),
preserve \(H_w\), and change the inactive cap only within a fixed finite
set (caps at least two are equivalent for binary source availability).
In (3.6)--(3.12) this only enlarges the constants by a finite maximum.

## 4. Restoring all lower clocks

Fix an enabled \(y\in{\cal M}\) and a particular outgoing lower edge
\(e:y\to y'\) of rate \(\kappa_e>0\). Conditional on a top-only path,
attach the independent lower reaction clocks by the standard random
time-change construction. Let

\[
 I_e=\int_0^{T_y/a_n}\kappa_e
          (\widehat X_t^{(n)})_y\,dt,\qquad
 I_{\rm all}=\int_0^{T_y/a_n}
          \{\Lambda_{\cal M}+\Lambda_<\}(\widehat X_t^{(n)})dt. \tag{4.1}
\]

Choose \(M\) so large that (3.3) and Markov's inequality give

\[
 {\mathbb P}\{I_{\rm all}>M\}\le p_y/2.                   \tag{4.2}
\]

On the intersection of the event in (3.1) and
\(\{I_{\rm all}\le M\}\), the conditional probability that edge \(e\)
rings before every competing lower clock, and before the end of the
window, is at least

\[
 e^{-M}(1-e^{-\kappa_e\eta_y}).                           \tag{4.3}
\]

Consequently the **physical** full chain, with every lower channel
present, follows \(e\) before any competing lower reaction with
probability at least

\[
 \pi_e={p_y\over2}e^{-M}(1-e^{-\kappa_e\eta_y})>0.         \tag{4.4}
\]

No independence between population coordinates is used; only the
conditional Poisson construction of the reaction clocks is used.

## 5. A finite actual-target carrier

Give \(L_-\) its arbitrary strongly connected orientation. From any
\(y_0\in{\cal M}\), choose a directed path to
\(L_-\setminus{\cal M}\), stopped at its first exit:

\[
 y_0\to y_1\to\cdots\to y_\ell,\qquad
 y_0,\ldots,y_{\ell-1}\in{\cal M},\quad
 y_\ell\notin{\cal M}.                                   \tag{5.1}
\]

One may take \(\ell\le |L_-|-1\le4\). Whenever a prescribed edge in
(5.1) occurs, its target is an actual physical population target and is
therefore enabled for the next step. Apply (4.4) successively, using the
strong Markov property. There are only finitely many path vertices and
bounded cap changes. At each restart, restrict the scaled active endpoint
to a fixed compact set. The endpoint moment bounds in Section 3 make the
discarded probability arbitrarily small, while the three transient proofs
of Proposition 4.2 are uniform on such compact sets. Thus conditioning on
an earlier clock race cannot silently force the next stage to a shell
boundary. After this restriction, the finitely many constants have a
positive minimum. Thus
the full chain follows (5.1), with no competing lower reaction, with
probability

\[
 \pi_*=\prod_{j<\ell}\pi_{y_jy_{j+1}}>0.                  \tag{5.2}
\]

Top-linkage reactions are not declared interruptions: they are already
included in each top-only occupation window. This is why a top reaction
which temporarily consumes the produced cofactor does not invalidate the
argument.

Define one macro-attempt as follows. At each path vertex, run its
\(T_j/a_n\) window and stop immediately if a competing lower reaction
occurs; stop at the window endpoint if the prescribed reaction has not
occurred; otherwise continue to the next vertex. The total physical
duration is deterministically at most

\[
 {T_{\rm tot}\over a_n},\qquad
 T_{\rm tot}=\sum_{j<\ell}T_j.                            \tag{5.3}
\]

On the event (5.2), the final edge decreases \(H_w\) by at least one.
If a competing reaction has a source in \({\cal M}\), it cannot increase
\(H_w\). A competing reaction from a submaximal source can increase
\(H_w\), but (3.4) says that the probability of any such reaction in the
finitely many windows is \(o(1)\). All reaction jumps of \(H_w\) are
bounded. Therefore

\[
 \mathbb E_{x_n}\{H_w(X_{\tau_n})-H_w(x_n)\}
 \le-\pi_*+o(1)\le-\tfrac12\pi_*                         \tag{5.4}
\]

for all large \(n\). Moreover

\[
 |H_w(X_{\tau_n})-H_w(x_n)|\le C                         \tag{5.5}
\]

pathwise, because top reactions are \(H_w\)-neutral and at most four
lower reactions occur. The transient estimates in Section 3 give fixed
moments of every endpoint coordinate. Thus (5.3)--(5.5) supply physical
duration, full endpoint integrability, and strict scalar descent without
a genealogical ledger.

The two top-activation incidences use the cap-zero activation clause of
Proposition 4.2 for their first path vertex. In both, the activating top
reaction has rate at least \(cN_n^2\) until it fires, while every enabled
lower source at cap zero is inactive-only and has total rate \(O(1)\).
Thus the activation time is dominated by an exponential variable of mean
\(C/N_n^2\), and the probability that a lower clock wins this initial
race is \(O(N_n^{-2})\). Once the top reaction creates the missing
cofactor, (3.9)--(3.12) apply with cofactor population one and the
identical all-channel argument applies.

## 6. Exact conclusion and the lower activation block

> **Theorem 6.1.** Along every exact-flat realizing
> sequence belonging to the 893 seeded or two top-activation rank-one
> incidences, the full CTMC admits a bounded-step physical stopping time
> satisfying (5.3)--(5.5). In particular, competing lower channels do not
> destroy the rank-one service margin.

This closes the multi-channel carrier obligation for those 895 incidences.
It does **not** by itself promote a support pair to recurrence: the result
must be composed with the surrounding tier Foster theorem.

The ten zero-boundary incidences are already finite on their fixed
communication classes, as proved in Proposition 4.1. The remaining 25
incidences have no enabled maximal lower source at cap zero, but their
support geometry is rigid enough to supply a separate activation block.

### 6.1 The 25 cap-zero activations

The certificate checks the following statements in every one of the 25
incidences.

1. The inactive coordinate is \(C\), with cap zero.
2. The lower support contains \(0\), at least one of \(C,2C\), and at
   least one of \(AC,BC\), but no complex outside
   \(\{0,C,2C,AC,BC\}\).
3. The unique enabled lower source at cap zero is \(0\).
4. The maximal lower tier is a nonempty subset of \(\{AC,BC\}\).

Fix a \(C\)-only vertex \(c_*\in L_-\cap\{C,2C\}\). Strong connectivity
gives a simple directed path from \(0\) to \(c_*\). Stop it at its first
\(C\)-only target:

\[
 0=z_0\to z_1\to\cdots\to z_j=c_*,\qquad
 z_1,\ldots,z_{j-1}\in{\cal M}.                           \tag{6.1}
\]

Before the first edge, every lower clock except the clocks sourced at
\(0\) is off. The waiting time is exponential with fixed positive rate.
Whichever \(0\)-edge occurs, its target is either \(C\)-only or maximal.
If it is maximal, use the all-channel race bound (4.4), restarting from
each actual maximal target, until the first exit from \({\cal M}\).
Each restart has a fixed probability of following a path of length at
most four to the complement, so the restart count is geometrically
dominated.

There is no hidden moving-phase estimate in the constant-time wait at
cap zero. The certificate checks that the only top supports occurring in
these 25 incidences are

\[
 \{2A,2B\},\quad\{2A,A+B\},\quad\{2B,A+B\},\quad
 \{2A,2B,A+B\},\quad\{B,2A\}.                            \tag{6.2}
\]

For the first four, the active total is pathwise constant. For
\(\{B,2A\}\), let \(N\asymp\sqrt q\), \(q=A+2B\), and
\(W_r(A)=(1+A/N)^r\). The two elementary finite differences, together
with the rates \(B\to2A\) of order at most \(N^2\) and
\(2A\to B\) of order \((A)_2\), give constants independent of the shell
such that

\[
 {\cal L}_*W_r\le C_rN-c_rN W_r^{\,1+1/r}.               \tag{6.3}
\]

Indeed, the positive finite difference is at most
\(C_rN^{-1}(1+A/N)^{r-1}\). For \(A\ge2\), the negative finite
difference is at most
\(-c_rN^{-1}(1+A/N)^{r-1}\). After multiplication by
the respective rates, the negative term absorbs the positive term for
large \(A/N\), and the remaining compact range costs \(C_rN\).
Dynkin's formula, Jensen's inequality, and scalar comparison imply

\[
 \sup_n\sup_{t\ge0}\mathbb E(1+A_t/N)^r<\infty           \tag{6.4}
\]

from every exact-tier compact initial ratio. Thus the endpoint at an
independent constant-rate \(0\)-clock has every fixed scaled moment. A
path supremum does not follow from (6.4); the separate barrier estimate
below supplies precisely the lower-tail control that service requires.

For service one also needs a lower-tail estimate, which does not follow
from (6.4). Let \(N\) be the conserved active total in the homogeneous
cases and \(N\asymp\sqrt q\) for \(\{B,2A\}\). Exact-flat realization
puts the initial scaled active coordinates in a compact interior set.
There are nested compact interior sets
\({\cal I}_0\Subset{\cal I}_1\), depending on the limiting exact-tier
ratios and the rates, such that for every fixed \(L,m\),

\[
 {\mathbb P}\left\{
   Z_N(t)\notin{\cal I}_1\hbox{ for some }0\le t\le L\log N
 \right\}\le C_{L,m}N^{-m},                              \tag{6.5}
\]

whenever \(Z_N(0)\in{\cal I}_0\), even after a fixed number of bounded
lower-reaction perturbations. Here \(Z_N\) denotes the active fraction
in a homogeneous shell and \(A/N\) in the \(\{B,2A\}\) shell.

For completeness, (6.5) is a one-dimensional exponential-barrier
estimate. In a homogeneous shell the density drift is a quadratic
polynomial which is strictly inward in strips next to both accessible
endpoints; strong connectivity supplies the strict signs. In the
\(\{B,2A\}\) shell, uniformly for the exact-tier compact range of
\(q/N^2\), the scaled drift is strictly positive below a small
\(\delta>0\) and strictly negative above a large \(R<\infty\).
Across either boundary strip, apply the generator to
\(\exp(\pm\theta N Z_N)\), with the sign pointing out of the strip and
\(\theta>0\) small. The inward first-order term dominates the
bounded-jump quadratic remainder, so the probability of crossing the
whole strip in one excursion is at most \(e^{-cN}\). Before the stopped
exit, the total top intensity is \(O(N^2)\); hence at most
\(O(N^2\log N)\) excursion starts occur in expectation on the displayed
horizon. The strong Markov property and a union bound give (6.5).
A fixed number of \(O(1)\) population jumps cannot cross the
\(\Theta(N)\) gap between \({\cal I}_0\) and
\({\cal I}_1^c\).

The sum of any fixed number of independent constant-rate \(0\)-clock
waits exceeds \(L\log N\) with probability \(O(N^{-m})\) after choosing
\(L\). Consequently, throughout any fixed, preassigned number of
activation trials and carrier windows, every required \(AC\) or \(BC\)
source has propensity at least \(cN\), outside an \(o(1)\) event. This
is the required interior-at-activation statement.

We now cap every repetition deterministically. On the interior event
(6.5), Section 5 has a common lower bound \(p>0\), over the finitely many
maximal vertices, for one carrier attempt to reach
\(L_-\setminus{\cal M}\). Choose integers \(K_e,K_a,K_s\) as follows.
Within one activation trial allow at most \(K_e\) carrier attempts to
resolve an actual maximal target. Allow at most \(K_a\) completed
activation trials, and, after activation, at most \(K_s\) attempts for
the additional unpaired service.

An exit to \(0\) clears the possible unit activation debt and returns to
cap zero. Strong connectivity and the fixed path (6.1) give a prescribed
finite event, of probability at least \(a>0\), on which one activation
trial reaches \(C\) or \(2C\). Enlarge \(K_e\), if needed, so this path
fits within its attempt cap. Along such a trial, an initial
\(0\to{\cal M}\) edge raises \(H_w\) by one and the first
\({\cal M}\)-exit lowers it by one; intermediate maximal edges are
neutral. A direct \(0\to\{C,2C\}\) edge is neutral. Thus every completed
trial has zero net reward, and a successful one ends with

\[
 \Delta H_w=0,\qquad C\ge1.                              \tag{6.6}
\]

Choose \(K_a\) so that
\(s_a:=1-(1-a)^{K_a}>0\), and choose \(K_s\) so that
\(s_s:=1-(1-p)^{K_s}>0\). Once (6.6) holds, (6.5) makes every maximal
\(AC\) or \(BC\) source uniformly order \(N\). Hence the additional
service succeeds with probability at least \(s_s\), and on success

\[
 \Delta H_w\le-1.                                        \tag{6.7}
\]

The only positive reward before a completed activation is the unresolved
unit debt. Conditional on the interior event, its probability in at most
\(K_a\) trials is at most
\(\eta:=K_a(1-p)^{K_e}\). Consequently the probability of completing
activation before the attempt cap is at least \(s_a-\eta\). Choose
\(K_e\) last, so that

\[
 \eta(1+s_s)\le\tfrac14s_as_s.                           \tag{6.8}
\]

All three integers are fixed constants, independent of \(n\). Therefore
the total number of fast windows is deterministically bounded. If
\(\varepsilon_n\) is the largest conditional probability of a
submaximal firing in one such window, (3.4) and (3.12), uniformly over
\({\cal I}_1\), give

\[
 {\mathbb P}\{\hbox{some submaximal interference}\}
 \le (K_aK_e+K_s)\varepsilon_n=o(1).                     \tag{6.9}
\]

The boundary event in (6.5), the gamma tail of the finitely many
constant-rate waits, and (6.9) together have probability \(o(1)\).
Every one of these exceptional stops has bounded \(H_w\)-increment,
because only a fixed number of lower reactions has occurred. On the
complement, (6.6)--(6.8) give

\[
 \begin{split}
 \mathbb E\Delta H_w
 &\le-(s_a-\eta)s_s+\eta+o(1)
 \le-\tfrac12s_as_s,                                    \tag{6.10}\\
 \sup_n\mathbb E\tau^r&<\infty,\qquad
 |\Delta H_w|\le C .
 \end{split}
\]

The duration bound follows because there are at most \(K_a\)
constant-rate waits and a fixed number of \(O(a_n^{-1})\) windows.
Equations (3.6), (6.4), and (6.5) give all fixed **scaled** active
endpoint moments. This construction uses an actual \(C\)-only target and
then an additional unpaired maximal-source exit; it does not count the
first debt-cancelling return as strict descent.

> **Theorem 6.2.** The physical carrier theorem extends to
> all 25 lower-activation incidences via (6.1)--(6.10).

Combining Theorems 6.1 and 6.2 with the ten finite zero-boundary
incidences treats all 930 rank-one flat incidences at descriptor level.
This still does not promote any support pair to recurrence until the
descriptor episodes are composed with the global tier Foster theorem.

The independent audit checked:

1. the integrated upper moment (3.3);
2. the submaximal \(o(1)\) estimate (3.4) under subpower tier separation;
3. the conditional race bound (4.3); and
4. bounded-cap uniformity across the finite actual-target path;
5. the exact support assertions preceding (6.1); and
6. the second, unpaired service in the cap-zero activation episode.

All six checks passed at the local carrier scope. A second independent
replay of *rank_one_corrected_factorial_endpoint.md* then verified that the
same episodes have strictly negative expected drift for the actual
rate-corrected factorial potential, including arbitrarily slow subpower
tier gaps. Neither audit is a pair-level recurrence claim.

The scoped finite certificate is reproduced by

    PYTHONPATH=src python3 -B src/rank_one_carrier_certificate.py
    PYTHONPATH=src python3 -B -m unittest \
      tests/test_rank_one_carrier_certificate.py -v

It freezes the partition \(893+2+25+10=930\), verifies that every maximal
lower layer is proper and has weight one, and records dormant-geometry hash

    e645359a8ec1432f7093a703bccf4f309601d86ee5600582803677262f5ad5b2

The executable records the audited local corrected-factorial endpoint in a
narrowly named flag. Its broader analytic and pair-level recurrence flags
remain false; global T3-2 remains uncertified.
