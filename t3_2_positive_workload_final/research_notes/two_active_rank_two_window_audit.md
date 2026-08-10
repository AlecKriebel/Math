# Audit of the rank-two Riccati window

## 1. Verdict and scope

Proposition 5.1 of *two_active_promotion_phase.md* is valid as a **local
core-window lemma** for all fourteen certified lower supports and arbitrary
fixed strongly connected orientations and positive rates. Its conclusion
does not provide the missing return-to-core potential and therefore does
not close any support pair by itself.

The proof in that note is compressed at two points: it does not display the
lower-reaction terms in the exponential domination of \(C\), and the linear
Poisson corrector needs its \(N^{-1/2}\) scaling. The estimates below fill
those local omissions.

## 2. Exact lower-linkage decomposition

The fast support is

\[
 L_* = \{B,2A,B+C\},\qquad q=A+2B.
 \tag{2.1}
\]

Every one of the fourteen lower supports lies in

\[
 E_0\cup E_1,\qquad
 E_0=\{0,C,2C\},\quad E_1=\{A,A+C\},
 \tag{2.2}
\]

and meets both sets. A strongly connected directed graph has an edge from
\(E_1\) to \(E_0\). Aggregating all such edges by their source gives

\[
 d_A+d_{AC}>0.
 \tag{2.3}
\]

Since a reaction crossing from \(E_1\) to \(E_0\) decreases \(A\) by one,
one crossing in the reverse direction increases it by one, and within-set
edges do not change \(A\), stochastic mass action gives the exact identity

\[
 {\cal L}_{-}q
 =g_+(C)-A\{d_A+d_{AC}C\},
 \tag{2.4}
\]

where \(g_+\) is a nonnegative linear combination of \(1,C,(C)_2\).
This identity is valid on every boundary face.

## 3. Uniform \(C\)-moments with the full lower linkage present

Stop the accelerated window before

\[
 q\notin[N/2,2N]\quad\hbox{or}\quad A>K\sqrt N.
 \tag{3.1}
\]

Then \(B\ge N/8\) for all large \(N\). If \(y,r,d\) are the aggregate
fast-linkage rates used in the residual-pair calculation, the fast part of
the \(C\)-generator has birth rate at most \(K_0N\) and contains death rate

\[
 dBC\ge(d/8)NC.
 \tag{3.2}
\]

For any lower support in (2.2), every reaction which increases \(C\) has
source \(0,A,C\), or \(A+C\). A source \(2C\) cannot increase \(C\).
Consequently the additional \(C\)-birth intensity is bounded by

\[
 K_1\{1+\sqrt N+(1+\sqrt N)C\}.
 \tag{3.3}
\]

For large \(N\), the linear-in-\(C\) term in (3.3) is absorbed by half of
(3.2). Since a lower reaction can create two copies of \(C\) at once, the
precise comparison is an immigration--death chain with immigration batches
bounded by two, total immigration intensity \(K_2N\), and per-particle
death \(K_3N\). Equivalently, the exponential-generator inequality gives
the same bound directly. If the initial core has a uniform exponential
moment, then for some \(\theta>0\)

\[
 \sup_N\sup_{0\le \tau\le T}
 {\mathbb E}\exp\{\theta C(\tau/\sqrt N)\}<\infty.
 \tag{3.4}
\]

The lower linkage thus does not invalidate the transient domination used
by the Riccati argument.

## 4. Riccati and averaging errors

Let \(Z=A+\zeta C\), \(z_N=Z/\sqrt N\), and use accelerated time
\(\tau=\sqrt N\,t\). On (3.1), the lower-linkage contribution to the
drift of \(z_N\) is bounded in every fixed \(L^p\) by

\[
 {K\{1+A+C+(C)_2+AC\}\over N}
 =O(N^{-1/2}),
 \tag{4.1}
\]

using (3.4). Its martingale quadratic variation is \(O(N^{-1})\).
Thus the stopped limit remains

\[
 \dot z=\alpha-\beta z^2.
 \tag{4.2}
\]

For the fast linkage,

\[
 {\cal L}_*C=yB+r(A)_2-dBC.
 \tag{4.3}
\]

Put

\[
 m_N={yB+r(A)_2\over dB},
 \qquad
 h_N={2C\over d\sqrt N}.
 \tag{4.4}
\]

For the accelerated generator \(G_N={\cal L}/\sqrt N\),

\[
 G_Nh_N={2B\over N}(m_N-C)+R_N,
 \tag{4.5}
\]

where the lower-linkage bound (3.3) gives
\(\int_0^T{\mathbb E}|R_N|\,d\tau=o(1)\). The endpoint term
\(h_N(T)-h_N(0)\) tends to zero in \(L^1\), and its martingale has quadratic
variation \(O(N^{-1/2})\). Since \(2B/N\to1\) and

\[
 m_N\longrightarrow m(z)={y+2rz^2\over d},
 \tag{4.6}
\]

Dynkin's formula yields

\[
 \int_0^T\{C(\tau)-m(z(\tau))\}\,d\tau
 \longrightarrow0
 \quad\hbox{in }L^1.
 \tag{4.7}
\]

This is the scaled version of the “linear Poisson corrector” invoked in the
candidate proof.

## 5. Strict drift and counts

On accelerated time, (2.4), (3.4), and (4.7) give

\[
 {\mathbb E}[q(T/\sqrt N)-q(0)]
 \longrightarrow
 -\int_0^Tz(\tau)
       \{d_A+d_{AC}m(z(\tau))\}\,d\tau.
 \tag{5.1}
\]

The positive term \(g_+(C)/\sqrt N\) vanishes in \(L^1\). If \(d_A>0\),
the minimum over bounded nonnegative initial data is obtained from the
Riccati solution starting at zero and is strictly positive after time zero.
If \(d_A=0\), then \(d_{AC}>0\). Strong connectivity of the fast linkage
forces \(y>0\) or \(r>0\); in the latter case the Riccati solution and
\(m(z)=2rz^2/d\) are both positive for every positive time. Hence the
right side of (5.1) is bounded above by a strictly negative constant,
uniformly on the stated core.

Finally, the accelerated \(q\)-changing intensity is bounded by

\[
 K\{z(1+C)+N^{-1/2}(1+C+(C)_2)\}.
 \tag{5.2}
\]

The exponential bound (3.4) and standard counting-process inequalities
give every fixed moment of the number of \(q\)-changes on the window.
The stop in (3.1) is removable by the same high-moment argument used in
the exact residual-pair proof.

Therefore the local short-window assertion survives the adversarial check.
What remains open is exactly what the candidate note says remains open: a
proper return workload, with endpoint and duration estimates, for each of
the fourteen lower partners containing the additional \(2C\) and \(A+C\)
sources.
