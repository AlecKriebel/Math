# Dyadic compound activation for the four hard H_w switches

## 1. Scope and two withdrawn shortcuts

This note gives a second repair target for the exact four hard
\(H_w\)-switch pairs.  Two earlier shortcuts are explicitly withdrawn.

First, a resistance-two seed state does not satisfy a linear
Perron--Frobenius bound of order \(nR\).  On the exact cycle

\[
                         2C\to YC\to2Y\to XY\to2C     \tag{1.1}
\]

at \((X,Y,C)=(n-2,0,2)\), every fixed positive linear form has only
\(O(1)\) top drift.

Second, a bounded shortest reaction word does not give a one-level
comparison for raw transverse mass \(M=Y+C\).  In the sparse orientation

\[
 2Y\to2C,\quad2Y\to YC,\quad2C\to XY,\quad
 YC\to2Y,\quad XY\to2Y,                               \tag{1.2}
\]

the reaction \(2C\to XY\) has rate \(\Theta(M^2)\) near the all-\(C\)
axis and lowers \(M\).  Before the carrier propensity catches up,
\(\Theta(M^2/n)\) such mass dips can accumulate.

The replacement uses a different transverse coordinate on which every
one of those dips is exactly neutral, tracks the exact source balance across
the neutral two-complex class, and works on dyadic rather than one-unit
levels.

This is a claim-neutral target.  The exact supports and all 1,606 strong
four-node digraphs are executable, but every analytic, recurrence, and
global flag remains false.  The pair fingerprint is

~~~text
4b24d4d3437351daf8e1d9b0e84e3d38e5e77147141a44fd9b68f6e1bba68716
~~~

## 2. Universal weighted height

Let \(X\) be the dormant species and \(Y\) the other nonservice species.
After relabeling, each top support contains

\[
                              2Y,\quad2C,\quad YC      \tag{2.1}
\]

and one mixed carrier.

For the two resistance-two rows the carrier is \(XY\).  Put

\[
                         R_2=2Y+C.                    \tag{2.2}
\]

For the two resistance-one rows the carrier is \(XC\).  Put

\[
                         R_1=Y+2C.                    \tag{2.3}
\]

The complete height tables are

\[
\begin{array}{c|cccc|c|c}
&2Y&2C&YC&\text{mixed}&\text{minimum class}&
  \text{strictly higher}\\ \hline
R_2&4&2&3&2\ (XY)&\{2C,XY\}&\{YC,2Y\}\\
R_1&2&4&3&2\ (XC)&\{2Y,XC\}&\{YC,2C\}.
\end{array}                                           \tag{2.4}
\]

In both cases

\[
                            M\le R_i\le2M.             \tag{2.5}
\]

The problematic edge in (1.2) is \(2C\to XY\), and
\(\Delta R_2=0\) on it.  Its return edge \(XY\to2Y\) has
\(\Delta R_2=2\).  Thus raw-mass debt can accumulate only inside a
zero-height class; it is not a loss in the activation coordinate.

## 3. Exact finite minimum cut

There are twelve possible directed arcs on four labeled complexes.  The
executable enumerates all \(2^{12}\) simple digraphs and selects the 1,606
which are strongly connected.  From each of the two minimum-height nodes,
it computes the shortest directed path which remains in the minimum class
until its final strict-height edge.  The exact result is

\[
\begin{array}{c|c}
\text{minimum-cut profile}&\text{strong digraphs}\\ \hline
(1,1)&1234\\
(1,2)&372.
\end{array}                                           \tag{3.1}
\]

No strong orientation needs more than one zero-height transfer before a
strict cut.  The same enumeration covers \(R_1\) after swapping \(Y\) and
\(C\).

Writing \(A=2P\) for the pure minimum node and \(B=XU\) for the carrier
minimum node, the same masks give the sharper direct-source profile

\[
\begin{array}{c|c}
\text{direct strict-cut sources}&\text{strong digraphs}\\ \hline
A\text{ and }B&1234\\
A\text{ only}&186\\
B\text{ only}&186.
\end{array}                                           \tag{3.2}
\]

Whenever one minimum node lacks a direct cut, its zero-height edge to the
other minimum node is present.  These are finite graph equalities only;
they do not assert a physical-clock comparison.

The finite statement does not by itself compare physical clocks.  That is
the role of the next section.

## 4. Quadratic compound ascent

Fix an orientation and positive rates.  Constants below may depend on
them.  Localize at

\[
                         K\le R\le\varepsilon n,       \tag{4.1}
\]

where \(K\) is large and \(\varepsilon\) will be small.

There is one universal parametrization.  Put

\[
 A=2P,\qquad B=XU,\qquad H_1=PU,\qquad H_2=2U,
 \qquad R=P+2U,                                      \tag{4.2}
\]

where \((P,U)=(C,Y)\) for \(R_2\) and \((P,U)=(Y,C)\) for
\(R_1\).  Thus \(A,B\) have height two and \(H_1,H_2\) have heights
three and four.  A reaction sourced at \(A\) or \(B\) is either a
zero-height transfer between them or a strict cut of reward one or two.

Let \(a_A,a_B>0\) be the sums of outgoing rate constants from \(A,B\).
While \(r/2<R<2r\) and \(R\le\varepsilon n\),

\[
 \lambda_{\min}=a_AP(P-1)+a_BXU
       \ge c\{P(P-1)+nU\}\ge cr^2.                  \tag{4.3}
\]

Call every \(H_1,H_2\)-source reaction and the physical death *bad*, and
also include the favorable physical birth in the larger class
*exceptional*.  Since

\[
 \lambda_{\rm high}\le CUR,\qquad
 \lambda_{\rm death}\le CR,\qquad
 \lambda_{\rm birth}=O(1),                           \tag{4.4}
\]

the aggregate comparison is

\[
 {\lambda_{\rm exceptional}\over\lambda_{\min}}
 \le q_{\varepsilon,K}:=C(\varepsilon+K^{-1}).       \tag{4.5}
\]

If \(U>0\), the \(XU\) term bounds the high ratio by \(CR/n\); if
\(U=0\), the high propensity is zero.  A split at \(P=R/2\) handles the
death term.  This is a comparison with the *aggregate* minimum clock, not
with a currently available cut clock.

At successive reaction times, exceptional indicators are therefore
adaptively Bernoulli-dominated.  For any deterministic \(M,t\),

\[
 \Pr\{E_M\ge t\}\le\inf_{\theta>0}
 \exp\{-\theta t+M\log(1+q_{\varepsilon,K}(e^\theta-1))\}.            \tag{4.6}
\]

It remains to turn aggregate minimum firings into strict cuts.  The graph
distance in (3.1) is not treated as a bounded physical reaction word.

For any reaction prefix in the band, let \(m_A,m_B\) count \(A\)- and
\(B\)-source reactions and let \(e\) count exceptional reactions.  If
\(B\) has no direct cut, strong connectivity forces every \(B\)-reaction
to be \(B\to A\), which lowers \(U\) by one.  Since an \(A\)- or
exceptional reaction raises \(U\) by at most two,

\[
 m_B\le U_0+2m_A+2e\le2r+2m_A+2e,\qquad
 m_A\ge{m_A+m_B-2r-2e\over3}.                        \tag{4.7}
\]

If \(A\) has no direct cut, every \(A\)-reaction is \(A\to B\), lowering
\(P\) by two.  Nonnegativity of \(P\) gives

\[
 2m_A\le P_0+2m_B+2e\le2r+2m_B+2e,\qquad
 m_B\ge{m_A+m_B-r-e\over2}.                          \tag{4.8}
\]

If both nodes have direct cuts, every minimum firing is already a
direct-source opportunity.  Conditional on any direct-source firing, its
destination probabilities are its fixed outgoing rate ratios.  Hence its
strict-cut probability is a fixed \(q_*>0\), and adaptive Chernoff gives

\[
                 \Pr\{D_d\le q_*d/2\}\le e^{-c_*d}.  \tag{4.9}
\]

This exact source balance charges repeated high-source recreation of a
carrier-rich phase to \(e\); no Green corrector, bounded reaction word, or
pointwise cut-clock lower bound is used.

Choose \(L=L(q_*)\) large and inspect the deterministic prefix of
\(M=(L+2)r\) total reactions, padding exceptional indicators by zero after
an exit.  On the event that no exit occurs among the first \(M\) actual
reactions and \(E_M\le r\), all \(M\) reactions remain in the band and the
prefix contains at least \((L+1)r\) minimum-source firings.  Equations
(4.7)--(4.9) then give at least \(4r\) strict cuts, except with probability
\(Ce^{-cr}\).  After fixing \(L\), choose \(\varepsilon\) small and \(K\)
large so that (4.6) gives the same bound for \(E_M>r\) and for \(r/5\) bad
reactions.

Before a lower exit from \(R=r+O(1)\), at least \(r/5\) bad reactions must
occur because minimum reactions and births do not lower \(R\), whereas one
bad reaction lowers it by at most two.  On the complementary event, the
cuts contribute at least \(4r\) and all exceptional reactions cost at worst
\(-2r\), forcing the upper or activation exit by time \(M\).  Consequently

\[
 \Pr\{R\le r/2\text{ first}\}\le Ce^{-cr}.           \tag{4.10}
\]

Restarting the same argument after a rare nonexit prefix gives an
exponential tail for the reaction count \(J_r\) at scale \(r\).  Equation
(4.3) dominates every holding time by an exponential variable of rate
\(cr^2\), so

\[
 {\mathbb E}e^{crS_r}\le C,\qquad
 {\mathbb E}S_r^p\le C_pr^{-p}.                       \tag{4.11}
\]

This also covers a carrier-rich one-way zero phase: the proof never waits
for \(U\) to drain to zero.  Every top, birth, and death clock is retained.

Applying (4.10)--(4.11) at \(K,2K,4K,\ldots\) yields

\[
 {\mathbb P}\{R\text{ reaches }\varepsilon n
      \text{ before a failed dyadic block}\}
 \ge1-\sum_{j\ge0}Ce^{-c2^jK}>0,                     \tag{4.12}
\]

and the time moments sum because \(\sum_j(2^jK)^{-1}<\infty\).

## 5. Finite establishment and exact birth accounting

At the dormant vertex, one physical \(0\to C\) seed enables \(XC\) in a
resistance-one row.  In a resistance-two row, two seeds enable \(2C\).
The probability that the second resistance-two seed arrives before the
first dies is bounded below uniformly in \(n\).

Below fixed \(K\), only finitely many transverse count states occur, while
every enabled mixed-carrier clock has order \(n\).  Contract those fast
mixed clocks.  They are zero-height or strictly favorable; in particular,
they cannot create an activation debt.  The remaining pure, high-source,
birth, and death clocks are all explicit \(O_K(1)\) competitors.  If the
fast \(XU\) source has no direct cut, its only outgoing edge is the zero
edge to \(2P\), after which the pure source has a fixed positive direct-cut
branch.  If \(XU\) is direct, that branch itself has fixed positive
probability.  Thus the contracted finite chain has no closed unsuccessful
class.  Prescribing finitely many favorable branches while forbidding all
listed slow competitors gives

\[
 \inf_{n\ge n_K}{\mathbb P}\{R\text{ reaches }K
       \text{ in one localized trial}\}=p_K>0.        \tag{5.1}
\]

The finitely many populations below \(n_K\) belong to the global compact
exception.  Define a full activation attempt from every preactivated
strong-Markov endpoint as follows.  If \(R<K\), first run the finite
establishment kernel.  If \(R\ge K\), take the first dyadic scale
\(r=R+O(1)\) and apply Section 4, then double scales until activation.  The
sum in (4.12) gives every such attempt a conditional success probability at
least one fixed \(p>0\).  A lower-block failure starts a new full attempt at
its actual endpoint; it is not asserted to return to the finite phase.

Each attempt has a uniform exponential duration bound by (4.11) and the
finite establishment estimate.  Thus the number of attempts is
geometrically dominated.  The stopped birth counting-process exponential
martingale then gives, for some \(s_0>0\),

\[
 \sup_n{\mathbb E}e^{s_0K_{\rm birth}}<\infty,\qquad
 \sup_n{\mathbb E}e^{s_0\tau_{\rm act}}<\infty.       \tag{5.2}
\]

No conditional-Poisson assertion is used, and every preactivation death is
retained in the population identity.

## 6. Deterministic service

Every positive-population state belongs to one of two regions.  If
\(R<\varepsilon n\), then \(X>(1-\varepsilon)n\) and Sections 4--5 apply.
If \(R\ge\varepsilon n\), activation is skipped and the state enters the
same service block directly.  By (2.5), the normalized activated region is
compact and separated from the dormant \(X\)-vertex.

The largest top-ODE invariant subset of the face \(C=0\) is exactly that
dormant vertex.  Indeed, at \(C=0\) no enabled reaction can consume
\(C\).  From every enabled \(C\)-free complex, strong connectivity gives a
directed path to a complex containing \(C\); the first crossing edge has
strictly positive \(C\)-production.  If no \(C\)-free source is enabled,
then \(Y=0\), leaving only the dormant \(X\)-vertex.  The same first-crossing
argument for the other missing species shows that every non-dormant
boundary trajectory enters the relative interior.

The top network is weakly reversible with one linkage class.  The
permanence theorem of Boros and Hofbauer applies after that interior entry;
see
[*Permanence of Weakly Reversible Mass-Action Systems with a Single
Linkage Class*](https://doi.org/10.1137/19M1248431), SIAM Journal on
Applied Dynamical Systems 19 (2020), 352--365.

Consequently every activated top trajectory has

\[
                         \int_0^\infty C_z(t)\,dt=\infty.               \tag{6.1}
\]

Continuity and compactness imply that, for each prescribed \(D_0\), one
finite fluid time \(T(D_0)\) satisfies

\[
 \inf_{R(z)\ge\varepsilon}\int_0^{T(D_0)}C_z(t)\,dt>D_0.               \tag{6.2}
\]

Run the full stochastic chain for physical time \(T/n\).  Uniformity over
the compact activated set includes lattice endpoints on its boundary,
because the preceding first-crossing argument is part of the deterministic
flow.  The density-dependent limit and the exact death counting-process
compensator then give a service count with any prescribed fixed mean,
uniform exponential positive moments, and all lower clocks retained.

## 7. Macroincrements and fractional return

Choose the service threshold after the activation law.  Let \(B\) be all
births in one macroepisode, let \(D_{\rm pre}\) be its favorable
preactivation deaths, and let \(D_{\rm win}\) count only deaths in the fixed
service window.  Since every top reaction preserves population, pathwise

\[
 Z=B-D_{\rm pre}-D_{\rm win}
       \le B-D_{\rm win}=:\widetilde Z.              \tag{7.1}
\]

The activation martingale gives a uniform exponential moment for \(B\).
The bounded fixed-window compensator gives one for \(D_{\rm win}\), on both
sides of \(\widetilde Z\).  Choose the service integral so that
\({\mathbb E}(\widetilde Z\mid{\cal F}_0)\le-a\).  Uniform Taylor control,
not negative mean alone, then gives fixed \(\lambda,c>0\).  Together with
the duration \(S\), the exact bounds are

\[
 {\mathbb E}(e^{\theta(B+D_{\rm win})}\mid{\cal F}_0)\le C,\qquad
 {\mathbb E}(e^{\lambda Z}\mid{\cal F}_0)
   \le {\mathbb E}(e^{\lambda\widetilde Z}\mid{\cal F}_0)
   \le1-c\lambda,\qquad
 {\mathbb E}S^p\le C_p.                               \tag{7.2}
\]

Repeat macroepisodes and stop at the first endpoint with

\[
                         n_J\le\rho n_0
                    \qquad\hbox{or}\qquad n_J\ge2n_0. \tag{7.3}
\]

The conditional exponential supermartingale makes the upper exit
exponentially unlikely.  For one fixed integer \(p>8\), the stopped-sum
estimates give

\[
 \Pr\{n_J\ge2n_0\}\le Ce^{-cn_0},\qquad
 {\mathbb E}J^p+{\mathbb E}\tau^p\le C_p n_0^p,       \tag{7.4}
\]

and the positive population overshoot has a uniform exponential moment.
These are the endpoint and duration orders needed by the common-potential
gluing step.

For

\[
 G_\ell(x)=K_\ell+\sum_i\log(x_i!)+\ell\mathbin\cdot x\ge1,
 \qquad W_\ell=G_\ell^4,                              \tag{7.5}
\]

the deterministic factorial envelope

\[
 \log(n!)-n\log3\le\sum_i\log(x_i!)\le\log(n!)        \tag{7.6}
\]

and the \(O(n)\) linear term imply, after choosing any fixed
\(\rho<1\) sufficiently below one, that the fractional lower exit obeys

\[
 W_\ell(X_\tau)-W_\ell(x)
 \le-c(n_0\log n_0)^4.                                \tag{7.7}
\]

The upper exit and its random overshoot are event-weighted by the
exponential tail in (7.4); (7.4) also makes the duration negligible on the
scale of (7.7).  Consequently the appended stopped episode satisfies

\[
 {\mathbb E}_x\{W_\ell(X_\tau)-W_\ell(x)+\tau\}
 \le-c(n_0\log n_0)^4.                                \tag{7.8}
\]

This is one common physical factorial potential, applies whether the start
was activated or dormant, and uses no additive total-population power.

## 8. Audit gate

Before any flag changes, independent replay must verify:

1. the exact height relabeling, all 1,606 minimum-cut distances, and the
   direct-source profile (3.2);
2. the aggregate clock comparison, deterministic-prefix exceptional bound,
   and exact source balances (4.3)--(4.9);
3. the dyadic exit and duration estimates (4.10)--(4.12), with every lower
   clock and the carrier-rich one-way configuration;
4. uniform finite establishment (5.1), including every slow competitor and
   the no-closed-class contraction, and both exponential moments (5.2);
5. the exact service-zero invariant subset and boundary-to-interior step
   before invoking single-linkage permanence;
6. the lattice-uniform full-chain service window and compensator moments;
7. the conditional exponential comparator (7.1)--(7.2) and the stopped-sum
   endpoint estimates (7.4) through one integer order \(p>8\); and
8. the common shifted-factorial envelope (7.5)--(7.8) on both fractional
   stopping branches and both all-start regions.

Until all eight items pass, the four pairs remain unresolved and every
claim flag stays false.

## 9. Reproduction

~~~text
PYTHONPATH=src python3 -B src/hard333_hw4_dyadic_compound_activation.py
PYTHONPATH=src python3 -B -m unittest \
  tests/test_hard333_hw4_dyadic_compound_activation.py -v
~~~

The frozen geometry-row hash is

~~~text
e80426c2363dca89d51a7a7e7cf845f64c807a8df76971c35c15941311d1ec70
~~~

the exact minimum-cut profile hash is

~~~text
2f48ace8a269e1a8ab2c6eb7e770b7d69f9f20a8d396b9468368b1c1d3a5a54f
~~~

and the payload hash is

~~~text
57608cbc0912802e526b5555631ffcfcaacd8eba2c26852439971babf5ea4aa7
~~~
