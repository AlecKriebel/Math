# A guard-free shell resolvent for the hard H_b twelve

## 1. Scope and status

This note replaces the failed logarithmic-guard construction in
*hard333_hb12_killed_shell_transfer.md*.  It uses the same physical
rate-adjusted factorial potential but stops only at the first
lower-linkage reaction.  The top chain may visit a thin shell boundary
arbitrarily many times before that reaction.  Those visits are handled by
the exact polynomial size bias of the reversible shell law, not by a
pathwise avoidance event.

The result is a claim-neutral analytic target.  The exact sixteen
gap-versus-killing rows, dominant lower source sets, lower-dimensional
menu, and the countersequence to the old guard are executable.  All
analytic, recurrence, and global flags remain false until hostile replay.
The exact twelve-pair fingerprint is

~~~text
7fcbd17c5571534a7e1bd50d218cfc56389c73a136c2fe0a73d3478ac2cf14fb
~~~

## 2. Why a pathwise guard is impossible

Take any \(B\)-side incidence with descriptor weight \((3,1,5)\), and let

\[
 B=m,\qquad C=\lceil e^{m^2}\rceil,\qquad
 A^2/(BC)\longrightarrow1.                            \tag{2.1}
\]

After harmless integer adjustment, this realizes the same exact order

\[
 2C>AC>\{2A,BC\}>C>AB>A>2B>B>0.                      \tag{2.2}
\]

The smallest center coordinate is only \(\Theta(m)\), while the logarithm
of the largest is \(\Theta(m^2)\).  A guard whose entropy height is a fixed
multiple of \(\log C\) therefore contains the point \(B=0\); the shell
energy barrier to that boundary is only \(\Theta(m)\).  Moreover the
top relaxation-to-lower-killing ratio is exponentially large, so the top
chain has time to visit that boundary before the lower clock rings.

Thus frequent boundary visits are real.  The repair below does not stop at
one and does not require \(q_R\) to be nearly constant along a path.

## 3. Exact reversible shell and size bias

The common top support is

\[
                             2A\rightleftarrows B+C.   \tag{3.1}
\]

Choose \(\theta>0\) to satisfy top detailed balance, put
\(\ell_i=-\log\theta_i\), and choose one rate-dependent constant
\(K_\ell\), independent of the shell, so that the common physical
potential

\[
 \pi_Q(x)=Z_Q^{-1}{\theta^x\over x!},\qquad
 G_\ell(x)=K_\ell+\sum_i\log(x_i!)+\ell\mathbin\cdot x
            =-\log\pi_Q(x)+c_Q\ge1.                 \tag{3.2}
\]

on every finite shell with invariant vector \(Q\).  Only the additive
constant \(c_Q\) in the last expression depends on the shell.  Thus
\(G_\ell\), and hence \(W_\ell=G_\ell^4\), is one common state function
across all shells and all lower-dimensional handoffs.  In the
one-dimensional
shell coordinate \(k\), the rates are

\[
 \lambda_k=\kappa_+A_k(A_k-1),\qquad
 \mu_k=\kappa_-B_kC_k.                                \tag{3.3}
\]

Their difference is strictly decreasing through the mode.  If \(v_Q\) is
the shell variance and \(\alpha_Q\) the common modal top propensity, then

\[
 v_Q\asymp \min(A_*,B_*,C_*),\qquad
 \gamma_Q\asymp{\alpha_Q\over v_Q},                  \tag{3.4}
\]

where \(\gamma_Q\) is the relaxation gap.

For every lower source complex \(u\), falling-factorial multiplication has
the exact shift identity

\[
 x^{\underline u}\pi_Q(x)
 =c_{Q,u}\,\pi_{Q-Iu}(x-u),                           \tag{3.5}
\]

where \(Iu\) is the change in the two top invariants and the right side is
zero off its shifted shell.  Products needed for second moments satisfy

\[
 x^{\underline u}x^{\underline v}
 =\sum_{r\le u\wedge v}
   \left\{\prod_i {u_i\choose r_i}{v_i\choose r_i}r_i!\right\}
   x^{\underline{u+v-r}}.                            \tag{3.6}
\]

All shifts in (3.5)--(3.6) have bounded degree.  The neighboring modes
differ by a bounded number of standardized shell units.  Uniform
log-concavity of (3.3) therefore gives, for every fixed \(p\),

\[
\begin{split}
 \pi_Q(q_R^p)&\le C_p\{\pi_Qq_R\}^p,\\
 {\pi_Q\{q_R(1+D_Q)^p\}\over\pi_Qq_R}&\le C_p,
 \qquad D_Q=G_\ell-G_\ell(x_Q^*).
\end{split}                                           \tag{3.7}
\]

This is the key distinction between kill mass and visit probability.
Even in (2.1), the \(q_R\)-size-biased endpoint stays in bounded shell
energy with high probability.

## 4. Exact relaxation margin on all sixteen rows

At every \(B\)-side mode,

\[
 A_*^2\asymp B_*C_*,\qquad v_Q\asymp B_*,
 \qquad \gamma_Q\asymp C_*.                           \tag{4.1}
\]

The exact finite table splits as follows.

\[
\begin{array}{c|c|c|c}
\text{rows}&\text{descriptor}&\bar q=\pi_Qq_R&
                         \gamma_Q/\bar q\\ \hline
10\text{ mixed}&(3,1,5)&A_*B_*&A_*/B_*^2\\
\text{double-only}&(2,1,3)&A_*+B_*^2&B_*\\
\text{double-only}&(3,1,5)&A_*&A_*/B_*\\
\text{double-only}&(7,4,10)&B_*^2&A_*^2/B_*^3 .
\end{array}                                           \tag{4.2}
\]

The three double-only lines and their coordinate swaps account for six
incidences.  Each ratio in the last column tends to infinity in its exact
descriptor.  Equivalently,

\[
 \varepsilon_Q={\bar q\over\gamma_Q}\longrightarrow0. \tag{4.3}
\]

The executable obtains the same statement without asymptotic shorthand:
the relaxation-gap D-exponent exceeds the lower-hazard exponent by one on
twelve rows and by two on four rows.

## 5. Same-state Kac cycles

Fix an actual starting point \(x\) with
\(D_Q(x)\le K_0\).  Let \(T\) be the first positive return time of the top
birth--death chain to this same state.  Define

\[
\begin{split}
 A_t&=\int_0^tq_R(X_s)\,ds,\\
 H&=A_T,\\
 R&=\int_0^T{\cal L}_RG_\ell(X_s)\,ds.
\end{split}                                           \tag{5.1}
\]

Continuous-time Kac identities give

\[
 {\mathbb E}_xH={\mathbb E}_xT\,\pi_Qq_R,\qquad
 {\mathbb E}_xR={\mathbb E}_xT\,\pi_Q({\cal L}_RG_\ell).
                                                               \tag{5.2}
\]

The load-bearing pointwise estimate is a Dirichlet Green bound, not an
\(L^2(\pi)\) evaluation at \(x\).  For the top chain killed on returning to
\(x\), one-dimensional strong log-concavity gives

\[
 \left\|G_{Q,x}^{\rm D}\right\|\le {C\over\gamma_Q}   \tag{5.3}
\]

uniformly for \(D_Q(x)\le K_0\).  Consequently, for additive functions
\(f,g\),

\[
\begin{split}
 {\mathbb E}_x\left(\int_0^Tf(X_s)\,ds\right)^2
 &\le {C\,{\mathbb E}_xT\over\gamma_Q}\,\pi_Q(f^2),\\
 \left|{\mathbb E}_x
 \left\{\int_0^Tf(X_s)\,ds\int_0^Tg(X_s)\,ds\right\}\right|
 &\le {C\,{\mathbb E}_xT\over\gamma_Q}
       \{\pi_Q(f^2)\pi_Q(g^2)\}^{1/2}.
\end{split}                                           \tag{5.4}
\]

Write \(b_Q={\cal L}_RG_\ell\) and \(\bar q=\pi_Qq_R\).  The same
finite shift calculation as in (3.5)--(3.7), now applied to the
log-factorial increments on every lower edge, gives the two explicit
stationary \(L^2\) bounds

\[
 \{\pi_Q(q_R^2)\}^{1/2}\le C\bar q,
 \qquad
 \{\pi_Q(b_Q^2)\}^{1/2}\le C\bar q\,g_Q .            \tag{5.5}
\]

Here \(g_Q\) is the stationary lower factorial reward scale from
Section 7.  Using (4.3) and (5.5) in the polarized Green inequality
(5.4) yields

\[
\begin{split}
 {\mathbb E}_xH^2
 &\le C\varepsilon_Q\,{\mathbb E}_xH,\\
 {\mathbb E}_x\left[
 H\int_0^T|{\cal L}_RG_\ell(X_s)|\,ds\right]
 &\le C\varepsilon_Q\,{\mathbb E}_xH\,g_Q ,
\end{split}                                           \tag{5.6}
\]

where \(g_Q\to\infty\) is the stationary lower factorial reward scale.

## 6. Exact renewal quotient

Retain every top and lower clock and stop at the first lower reaction
\(\tau_R\).  One return cycle has exact survival factor \(e^{-H}\).  Put

\[
\begin{split}
 d&={\mathbb E}_x(1-e^{-H}),\\
 N&={\mathbb E}_x\int_0^T
       e^{-A_t}{\cal L}_RG_\ell(X_t)\,dt .
\end{split}                                           \tag{6.1}
\]

Regeneration at the same state \(x\) includes a kill during the initial
holding time and gives the exact lower-reward payoff

\[
 {\mathbb E}_x\{G_\ell(X_{\tau_R})-G_\ell(X_{\tau_R-})\}
 ={N\over d}.                                        \tag{6.2}
\]

Equations (5.6) and \(0\le H-(1-e^{-H})\le H^2/2\)
give

\[
\begin{split}
 d&={\mathbb E}_xH\{1+O(\varepsilon_Q)\},\\
 N&={\mathbb E}_xR+
     O(\varepsilon_Q{\mathbb E}_xH\,g_Q).
\end{split}                                           \tag{6.3}
\]

Therefore

\[
 {N\over d}
 ={\pi_Q({\cal L}_RG_\ell)\over\pi_Qq_R}+o(g_Q).
                                                               \tag{6.4}
\]

For a lower edge \(e\), let \(q_e\) be its source propensity and define

\[
 h_j(x)=\sum_e q_e(x)|\Delta_eG_\ell(x)|^j,
 \qquad
 L_Q=\max_i\log(1+x_{Q,i}^*).                        \tag{6.5}
\]

The factorial identity
\(\log((x_i+r)!/x_i!)=\sum_{a=1}^r\log(x_i+a)\), with its analogous
formula for negative \(r\), and the shifted laws (3.5) give, for every
fixed \(j\),

\[
 {\pi_Qh_j\over\pi_Qq_R}\le C_j(1+L_Q)^j.            \tag{6.6}
\]

Apply the exact quotient (6.1) to the nonnegative rewards
\(q_R(1+D_Q)^j\) and \(h_j\).  The corresponding shifted \(L^2\) bounds
and (5.4) control the renewal errors just as in (6.3).  Thus, uniformly
for a core start and every fixed \(j\le p\),

\[
 \begin{split}
 {\mathbb E}_x(1+D_Q(X_{\tau_R-}))^j&\le C_j,\\
 {\mathbb E}_x|G_\ell(X_{\tau_R})-G_\ell(X_{\tau_R-})|^j
     &\le C_j(1+L_Q)^j,\\
 {\mathbb E}_x|G_\ell(X_{\tau_R})-G_\ell(x)|^j
     &\le C_j(1+L_Q)^j.
 \end{split}                                          \tag{6.7}
\]

We take one integer \(p>8\).  These are moments of the actual lower jump
and of the full stopped increment, not merely moments of its source.

There is also a duration estimate.  Apply the higher-order Dirichlet
Green inequalities to the additive functions (q_R) and (1).  Since
\(\bar q/\gamma_Q\to0\), the return-cycle renewal transform is analytic
on a fixed interval after the rescaling \(z\mapsto z\bar q\).  Expanding
the exact denominator
\(1-{\mathbb E}_x\exp\{-H+z\bar qT\}\) at zero, with the same cycle
moment bounds used in (5.6), gives constants \(c,C>0\) such that

\[
 {\mathbb E}_x e^{c\bar q\tau_R}\le C,
 \qquad
 {\mathbb E}_x\tau_R^j\le {C_j\over\bar q^j},
 \quad 1\le j\le p.                                  \tag{6.8}
\]

This includes the first-cycle holding interval and does not replace any
physical clock by an independent exponential clock.

## 7. Stationary lower reward

The finite table has ten rows with unique dominant source \(AB\) or \(AC\).
Strong connectivity forces a dominant-source exit to a lower D-tier.  The
other six rows have dominant sets

\[
 A,\quad\{A,2B\},\quad2B
 \quad\text{and their }B/C\text{ swaps}.              \tag{7.1}
\]

Each set has the exact strong-cut descent recorded by the all-active
factorial theorem.  Applying the shift identity (3.5) changes its mode only
by bounded shell energy.  The usual \(ue^{-u}\) estimate removes positive
edges from lower source tiers.  Hence, uniformly over fixed positive rates,

\[
 {\pi_Q({\cal L}_RG_\ell)\over\pi_Qq_R}
 \le-g_Q,\qquad g_Q\longrightarrow\infty.             \tag{7.2}
\]

Combining (6.4) and (7.2), while separately charging the \(O(1)\) terminal
top-shell energy from (3.7), gives

\[
 {\mathbb E}_x\{G_\ell(X_{\tau_R})-G_\ell(x)\}
 \le-cg_Q.                                            \tag{7.3}
\]

No guard or boundary handoff occurs in this all-active episode.

## 8. Fourth-power lift and other dimensions

Let \(S_Q=\max_i x_{Q,i}^*\).  Properness of the single shifted physical
potential gives, uniformly on the fixed-energy core,

\[
 G_\ell(x)\ge cS_Q\log(1+S_Q),\qquad
 L_Q\le C\log(1+S_Q).                                 \tag{8.1}
\]

Together with \(g_Q\to\infty\), this proves the load-bearing remainder
comparison

\[
 {L_Q^2\over G_\ell(x)g_Q}\longrightarrow0,
 \qquad {L_Q\over G_\ell(x)}\longrightarrow0.        \tag{8.2}
\]

Expand \((G_\ell+J)^4-G_\ell^4\) exactly and use (6.7), (7.3), and
(8.2).  The leading term is at most \(-cG_\ell^3g_Q\), while the second,
third, and fourth binomial terms are respectively
\(O(G_\ell^2L_Q^2)\), \(O(G_\ell L_Q^3)\), and \(O(L_Q^4)\).  Equation
(6.8) absorbs the duration.  Hence the common \(W_\ell=G_\ell^4\) target is

\[
 {\mathbb E}_x\left[
 W_\ell(X_{\tau_R})-W_\ell(x)+\tau_R
 \right]
 \le-cG_\ell(x)^3g_Q.                                 \tag{8.3}
\]

Outside the fixed-energy core no mixing-times-reward comparison is used.
There are two separately negative pointwise branches.  Where the top-shell
flux imbalance is large, the reversible factorial shell estimate absorbs
its own carré and higher binomial terms.  On the complementary branch, the
lower factorial high-cut is itself negative; reverse positive terms are
suppressed by the usual (he^{-h}) bound, and that same lower gap absorbs
its fourth-power Taylor remainder.  In particular, the argument requires
only \(\gamma_Q/\bar q\to\infty\) in the core renewal calculation and does
**not** assert

\[
              {\gamma_Q\over \bar q\,g_Q}\longrightarrow\infty.       \tag{8.4}
\]

Because the top path may visit \(B=0\) or \(C=0\), a lower reaction can
end this episode in a lower-dimensional state.  Such an endpoint is
routed through the existing exhaustive common-\(W_\ell\) menu:

\[
\begin{array}{c|c|c}
\text{dimension}&\text{route}&\text{incidences}\\ \hline
\text{two-active}&\text{closed rank-one top}&36\\
                 &\text{dormant top}&12\\ \hline
\text{one-active}&\text{generalized Family II}&36\\
                 &\text{direct physical }C&2.
\end{array}                                           \tag{8.5}
\]

The \(q_R\)-size-biased energy and full-jump estimates (6.7) pay the
handoff toll.  Appending the corresponding common-\(W_\ell\) kernel does
not require a boundary-avoidance event and preserves (8.3).

## 9. Audit gate

Before any flag changes, an independent replay must verify:

1. the shifted-shell identity (3.5), product identity (3.6), and all
   uniform moment consequences in (3.7);
2. the one-dimensional Dirichlet Green inequality (5.3)--(5.4), uniformly
   for every extreme shell and every core start;
3. the stationary \(L^2\) bounds (5.5) and the cycle second and cross
   moments (5.6);
4. the exact renewal quotient (6.1)--(6.4), including kills in the first
   holding interval;
5. the full terminal-jump and duration moments (6.5)--(6.8) through one
   integer \(p>8\);
6. the stationary high-cut estimate (7.2) for all sixteen rows and every
   strong lower orientation;
7. the remainder comparison (8.2), fourth-power endpoint (8.3), and
   pointwise core complement; and
8. the independent top-shell/lower-high-cut core complement, with no
   \(\gamma_Q/(\bar qg_Q)\) hypothesis; and
9. the exact lower-dimensional endpoint menu (8.5), including its
   common-potential handoff.

Failure of any item leaves all twelve pairs unresolved.  Every flag in the
executable remains false.

## 10. Reproduction

~~~text
PYTHONPATH=src python3 -B src/hard333_hb12_global_shell_resolvent.py
PYTHONPATH=src python3 -B -m unittest \
  tests/test_hard333_hb12_global_shell_resolvent.py -v
~~~

The frozen row hash is

~~~text
3999b185f5626b0999d72e9c10d3cdf082054f70cd84af8cd43a52aa6f286c7a
~~~

and the frozen payload hash is

~~~text
f750d01ff8c0ea884df27cf8e4625f6d6ef020f8d335c6086f6c1147c0934417
~~~
