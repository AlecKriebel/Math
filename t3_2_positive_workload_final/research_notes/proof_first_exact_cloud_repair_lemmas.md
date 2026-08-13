# Four uniform lemmas for the exact proper-cloud trace

**Proof-first repair supplement, 2026-08-11 PDT.  Rejected draft.**  This
note attempted to supply the four analytic details isolated by the hostile audit of
*hard317_exact_pair_cloud_averaging.md*.  It is claim-neutral.  It does not
change an analytic, pair, or global certification flag.

An immediate independent audit found a units mismatch in Lemma 1.1:
\(A_e\) in (1.1) is an occupation hazard per unit level-zero local time and
includes direct level-zero clocks, whereas the displayed \(J_e\) was defined
on an opened excursion beginning at level one.  Thus the sourcewise
two-insertion estimate is not proved as written.  Direct base clocks and
opened-excursion occupation must be separated before this supplement can be
used.  Everything below is retained only as a rejected proof draft pending
that repair.

Throughout, the proper linkage is

\[
             \{aU,V+I\},\qquad a\in\{0,1,2\},
\]

the old-active coordinate satisfies \(v\ge n/2\), and

\[
 L_n=\left\lfloor {n^{1/3}\over\log(n+e)}\right\rfloor,
 \qquad 0\le u<L_n .
\]

All orientations and positive rate constants are fixed.  Constants may
depend on these fixed data and on a requested moment order, but not on
\(n,u,v\).

## 1. Sourcewise two-insertion estimate

Let \(Y_t\) be the proper birth--death carrier, killed on its return to
level zero after an opening.  For a lower edge \(e\), put

\[
 J_e=\int_0^{\tau_0}\lambda_e(Y_s)\,ds,
 \qquad J=\sum_fJ_f .
\]

The exact occupation formula gives, for a source \(cU+bI\),

\[
 A_e(u,v)=\mathbb E J_e
 = {\kappa_e\rho^b(u)_{\underline{ab+c}}
       \over(v+1)^{\overline b}}
   Z_a(u-ab-c,v+b),                                      \tag{1.1}
\]

where

\[
 Z_a(s,N)=\sum_{j\ge0}{\rho^j(s)_{\underline{aj}}
          \over j!(N+1)^{\overline j}},
 \qquad 1\le Z_a(s,N)\le e^{C(1+s)^a/N}.               \tag{1.2}
\]

### Lemma 1.1

For every feasible distinguished edge \(e\),

\[
 \mathbb E[J_eJ]
 \le {C(1+u)^3\over n}\,\mathbb EJ_e .                \tag{1.3}
\]

The same estimate, with a larger polynomial constant, holds after size
biasing the endpoint by any fixed power of \(1+U+I\).

### Proof

Expand \(J_eJ\) as a sum over an ordered pair \((e,f)\) and split the
double time integral into \(s<t\) and \(t<s\).  In the first ordering,
condition at the \(e\)-insertion.  The remaining proper Green kernel starts
from a carrier level shifted by at most two.  Formula (1.1), applied to the
future \(f\)-insertion, shows that its total hazard relative to the
distinguished insertion is bounded by

\[
 C\left\{{(1+u)^2\over n}
          +{(1+u)^{a+1}\over n}
          +{(1+u)^{2a}\over n^2}\right\}.              \tag{1.4}
\]

The three terms correspond respectively to an \(I\)-free source during an
open level, a one-\(I\) source, and a two-\(I\) source.  Since \(a\le2\)
and \(u<L_n\), (1.4) is at most \(C(1+u)^3/n\).  For the reverse ordering,
use detailed balance of the proper carrier to interchange the two marked
levels, and repeat the same calculation.  The factorial denominator in
\(Z_a\) absorbs every carrier level and every fixed polynomial size bias.
Summing the finitely many lower edges proves (1.3). \(\square\)

If \(\widehat A_e\) denotes the exact first-lower hazard, Feynman--Kac and
\(1-e^{-J}\le J\) now give the **relative**, sourcewise estimate

\[
 0\le A_e-\widehat A_e
 \le\mathbb E[J_eJ]
 \le {C(1+u)^3\over n}A_e .                           \tag{1.5}
\]

The identical two-insertion argument beginning immediately after the first
lower firing proves the endpoint-weighted dirty-cleanup bound.

## 2. Precise killed kernel and compact minorization

Contract completed proper excursions in level-zero local time.  At a base
with at least one feasible lower source, select the first lower edge with
probability

\[
                    {\widehat A_e\over\sum_f\widehat A_f}.       \tag{2.1}
\]

After the firing, expose proper cleanup to the next no-fast state.  Let
\(Q_n\) retain exactly the paths for which the selected source is leading,
cleanup is clean, and the cofactor-envelope reward
\(\Delta\{V+m_a(U)\}\) is zero.  Kill on a strict drop, a nonleading
source, dirty cleanup, or the included physical boundary.

For every compact set of bases, the rescaled leading weights in (2.1)
converge, by (1.1) and (1.5), to finite strictly positive weights.  The
proper equality set in every actual exact-pair support is a proper subset
of its strong lower linkage.  Hence a directed equality path reaches a
strict edge in at most \(|L_0|\) steps.  Since the compact base set and the
path-edge set are finite, there exist \(M<\infty\), \(\eta>0\), and
\(n_0\) such that

\[
 \inf_{n\ge n_0}\inf_{u\le u_*}
 \mathbb P_u\{Q_n\hbox{ is killed in at most }M\hbox{ steps}\}
 \ge\eta .                                                       \tag{2.2}
\]

Outside a compact set, let \(dU\) be the maximal feasible \(I\)-free lower
complex.  Every equality edge from \(dU\) descends in \(U\), while every
positive equality jump has source degree at most \(d-1\) and size at most
two.  Therefore, for
\(F_\theta(u)=e^{\theta u\log(u+e)}\), \(0<\theta<1/2\),

\[
 {Q_nF_\theta(u)\over F_\theta(u)}
 \le Cu^{-\theta}+Cu^{-1+2\theta}+o(1).                         \tag{2.3}
\]

Equations (2.2)--(2.3), with a finite-state corrector, prove

\[
 (I-Q_n)^{-1}F_\theta\le C_\theta F_\theta,
 \qquad
 (I-Q_n)^{-1}(1+U)^p\le C_p(1+u)^{p+c_p}.                       \tag{2.4}
\]

They also give all fixed moments of the killed macro count.

## 3. Physical duration as an additive functional

In level-zero local time the next lower macro is an exponential clock of
rate \(\sum_e\widehat A_e\).  At every nonstatic base, (1.1) yields

\[
 \mathbb E_u T_{\rm macro}^p
 \le C_p n^{2p}(1+u)^{c_p}.                                     \tag{3.1}
\]

The real-time overhead is a compound sum of proper excursions.  Each open
excursion has fixed moments \(O(n^{-p})\), and its intensity per unit base
local time is at most \(C(1+u)^a\); hence (3.1) remains true in physical
time after increasing \(c_p\).

If \(N\) is the killed macro count and \(T_j\) the successive physical
macro times, then

\[
 \left(\sum_{j<N}T_j\right)^p
 \le N^{p-1}\sum_{j<N}T_j^p .                                  \tag{3.2}
\]

Apply the polynomial Green bound (2.4) to the right-hand side.  Repeating
the argument for the at most three strict-drop episodes gives

\[
                      \mathbb E_uT^p
 \le C_p n^{2p}(1+u)^{c_p}.                                    \tag{3.3}
\]

This estimates physical time, not reaction count.

## 4. Static faces and historical debt

If no lower source is feasible, \(m_a(u)\) is not defined and the trace is
not invoked.  In the actual supports, every such base also has no proper
opening.  Every reaction source contains \(U\) or \(I\), so the face is
static and isolated.  Starting the reflected lift from a fixed-class
reference on that face leaves \(V\) unchanged; consequently reachable
\(D_V=0\).  Such a face is outside the local historically reachable
positive-\(D_V\) hypothesis and belongs to the finite classwise target
alternative.

## 5. Consequences and claim boundary

The pointwise defect estimate (1.5), integrated against (2.4), gives

\[
 \mathbb E[(1+U_E+I_E+|V_E-v|)^p;E]
 \le {C_p(1+u)^{c_p}\over n}.                                  \tag{5.1}
\]

The proper carrier product and (2.4), with the worst \(n^2\) singular
trial amplification retained, give the included-boundary bound

\[
 \mathbb P(B)
 \le C{F_\theta(u)\over F_{\theta'}(L_n-C)}
 +Cn^2(1+u)^C
   \sum_{j\ge L_n-C}{[C(1+L_n)^a/n]^j\over j!},                 \tag{5.2}
\]

which is superpolynomial for \(u=n^{o(1)}\).

Together with the cofactor-envelope service identity, (5.1)--(5.2) and
(3.3) supply the endpoint and duration inputs missing from the cloud note.
The entropy, fourth-power Taylor estimate, and global path-labelled
boundary gluing are deliberately not claimed here; they remain separate
proof obligations.  No certification flag changes.
