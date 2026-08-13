# Certified global return theorem for the fourteen rank-two partners

## 1. Scope and audit status

This note treats

\[
 L_0=\{B,2A,B+C\}                                      \tag{1.1}
\]

and any of the fourteen compatible lower supports certified by
two_active_phase_gate.py. Each linkage has an arbitrary fixed strongly
connected orientation and arbitrary positive rates. Propensities are
stochastic mass-action propensities.

The construction uses no fixed box for \(C\), no stationary start, and no
raw-fast-jump recurrence:

1. a proper linear workload returns every large-\(q\) state to a moving
   core;
2. a physical-time regenerative block treats the four bounded-\(q\),
   \(C\to\infty\) faces not controlled pointwise by that workload; and
3. the audited transient Riccati window supplies strict core descent.

> **Theorem 1.1.** For every one of the fourteen supports and
> every strongly connected orientation with positive rates, the minimal
> CTMC is nonexplosive and every closed irreducible population class is
> positive recurrent.

The stopping-time composition in Sections 5--7 and all six obligations
listed in the prior candidate version have passed independent proof audit.
The theorem is certified at exactly this fourteen-support scope. It is not
a global T3-2 theorem.

## 2. A common outer workload

Use the fast-linkage rate notation

\[
\begin{array}{c|cccccc}
\text{edge}&B\to2A&B\to B+C&2A\to B&2A\to B+C&B+C\to B&B+C\to2A\\
\hline
\text{rate}&x&y&s&r&t&v .
\end{array}                                                \tag{2.1}
\]

Put \(d=t+v\). Strong connectivity makes

\[
 I_0=\left({r\over s+r},{d\over v}\right)                 \tag{2.2}
\]

nonempty and gives values in \(I_0\) arbitrarily close to one; a missing
denominator is interpreted as \(+\infty\).

For a lower complex \(z=(z_A,z_C)\), set

\[
 \ell_\rho(z)=\rho z_A+z_C,\qquad
 b_z(\rho)=\sum_{z\to z'}k_{zz'}
       \{\ell_\rho(z')-\ell_\rho(z)\}.                    \tag{2.3}
\]

The only quadratic lower complexes are \(2C\) and \(A+C\). At
\(\rho=1\), \(\ell_1\) is molecularity, so

\[
 b_{2C}(1)\le0,\qquad b_{AC}(1)\le0.                     \tag{2.4}
\]

There is a \(\rho>0\), arbitrarily close to one, for which every quadratic
complex present has a strictly negative coefficient. Equality in (2.4)
at one quadratic source means that all its outgoing edges target the other
quadratic complex. Both equalities would make \(\{2C,AC\}\) a closed
directed set. If only \(b_{2C}(1)=0\), take \(\rho<1\), because
\(2C\to AC\) has increment \(\rho-1\). If only \(b_{AC}(1)=0\), take
\(\rho>1\), because \(AC\to2C\) has increment \(1-\rho\). Existing strict
inequalities survive a sufficiently small perturbation. If only \(AC\) is
present, we may and do choose

\[
 0<\rho<1.                                                \tag{2.5}
\]

Choose \(\lambda\in I_0\), close enough to one that

\[
 p_B=2\rho-\lambda>0,                                    \tag{2.6}
\]

and put

\[
 U=\rho A+p_BB+C.                                        \tag{2.7}
\]

Direct substitution gives

\[
 {\cal L}_0U=c_BB-c_2(A)_2-c_{BC}BC,                     \tag{2.8}
\]

where

\[
 c_B=x\lambda+y,\quad
 c_2=(s+r)\lambda-r,\quad
 c_{BC}=d-v\lambda                                      \tag{2.9}
\]

are strictly positive. From (2.3)--(2.4),

\[
 {\cal L}_{-}U
 \le K_0+k_AA+k_CC-e_2(C)_2-e_{AC}AC,                    \tag{2.10}
\]

where \(K_0,k_A,k_C\ge0\), and \(e_h>0\) exactly when the quadratic
complex \(h\) is present. Every one of the fourteen supports contains
\(2C\) or \(AC\), so \(e_2+e_{AC}>0\).

Put

\[
\begin{split}
 P&=K_0+c_BB+k_AA+k_CC,\\
 D&=c_2(A)_2+c_{BC}BC+e_2(C)_2+e_{AC}AC,\\
 {\cal R}&=\{D\le2(P+1)\}.
\end{split}                                               \tag{2.11}
\]

Everywhere outside \({\cal R}\),

\[
 {\cal L}U\le-1-\tfrac12D.                              \tag{2.12}
\]

All jumps of \(U\) are bounded. Outside \({\cal R}\), every reaction
intensity is bounded by \(KD\). The point requiring care is that \(P\)
need not contain \(A\) or \(C\). The term \((A)_2\) controls \(A\) except
on the finite set \(A\le1\), and \(B\) occurs in \(P\). If \(2C\) is
present, \((C)_2\) controls \(C\). If only \(AC\) is present, then
\(A+B=0\) implies \(D=0\) and hence cannot occur in \({\cal R}^{\,c}\);
otherwise either \(AC\) or \(BC\) controls \(C\). Consequently, on
\({\cal R}^{\,c}\),

\[
 1+A+B+C\le K(1+P+D)\le K'D,                            \tag{2.13}
\]

and each actually present quadratic propensity is already one of the
terms in \(D\). Thus the full intensity is at most \(K''D\). After
enlarging a finite sublevel if necessary, the bounded-jump Taylor formula
gives, for every integer \(p\ge2\),

\[
 {\cal L}(1+U)^p
 \le C_p-c_pD(1+U)^{p-1}.                                \tag{2.14}
\]

For the finitely many powers used below, enlarge \({\cal R}\) by the
corresponding finite \(U\)-sublevels. This leaves Lemma 3.1 unchanged and
ensures, in particular,
\[
 {\cal L}(1+U)^2\le0\quad\hbox{on }{\cal R}^{\,c}.         \tag{2.15}
\]

The total-population generator is at most affine: a bimolecular source
cannot increase molecularity in a binary network. Localized Yule
comparison proves nonexplosion and finite-time population moments before
optional sampling is used.

## 3. Geometry and the first outer return

> **Lemma 3.1 (large-\(q\) core).** There are finite \(Q,K,C_*>0\) such
> that
> \[
> x\in{\cal R},\ q(x):=A+2B>Q
> \Longrightarrow A\le K\sqrt{q+1},\ C\le C_* .           \tag{3.1}
> \]

Indeed, (2.11) implies, after changing constants,

\[
 aA^2+bBC+eC^2+fAC\le K_1(1+q+C),                        \tag{3.2}
\]

where \(a,b>0\), \(e,f\ge0\), and \(e+f>0\). If \(e>0\),
first \(C=O(\sqrt q)\), then \(A=O(\sqrt q)\); hence
\(B\ge q/4\) for large \(q\), and the \(BC\) term gives \(C=O(1)\).
If \(e=0\), then \(f>0\). When
\(A\ge1+2K_1/f\), the \(AC\) term absorbs the linear \(C\) term, gives
\(A=O(\sqrt q)\), and then \(BC\) bounds \(C\). For bounded \(A\),
\(B\asymp q\) and \(BC\) bounds \(C\) directly. Enlarging the constants
covers the remaining finite range.

Define

\[
 {\cal K}=\{A\le K\sqrt{q+1},\ C\le C_*\},\qquad
 {\cal V}=\{q\le Q\},\qquad
 {\cal B}={\cal R}\cap{\cal V}.                           \tag{3.3}
\]

Then \({\cal R}\subset{\cal K}\cup{\cal B}\). For
\(\tau_{\cal R}=\inf\{t:X_t\in{\cal R}\}\), localized Dynkin estimates give

\[
\begin{split}
 \mathbb E_x\tau_{\cal R}+\tfrac12\mathbb E_x
       \int_0^{\tau_{\cal R}}D(X_t)\,dt&\le U(x),\\
 \mathbb E_xU(X_{\tau_{\cal R}})&\le U(x),\\
 \mathbb E_x[\tau_{\cal R}^p+U(X_{\tau_{\cal R}})^p]
 &\le C_p(1+U(x))^{r_p}.
\end{split}                                               \tag{3.4}
\]

No inactive coordinate is truncated: \({\cal B}\) is the exact
infinite bad-set portion to be treated on the vertical clock.

## 4. The four vertical strips

If \(2C\) is present, \(e_2(C)_2\) makes \({\cal B}\) finite. The only
supports needing another
argument are

\[
 \{0,A,AC\},\quad \{0,C,AC\},\quad
 \{A,C,AC\},\quad \{0,A,C,AC\}.                           \tag{4.1}
\]

Use \(0<\rho<1\). On \(q\le Q\), \(E=(A,B)\) is a genuinely finite
phase and \(C\) is the sole unbounded coordinate.

### 4.1 The three supports containing \(C\)

Aggregate lower rates as

\[
\begin{array}{c|ccc|ccc}
\text{edge}&C\to AC&C\to A&C\to0&AC\to C&AC\to A&AC\to0\\
\hline
\text{rate}&u&a&b&v_1&w&z .
\end{array}                                                \tag{4.2}
\]

On physical time \(t=\tau/n\), from \(C=n+O(1)\), the reactions with a
\(C\)-containing source converge to a linear phase process \(Y\). Its
first moments and its \(C\)-service intensity satisfy

\[
\begin{split}
 {d\over d\tau}\mathbb EY_B&=-v\mathbb EY_B,\\
 {d\over d\tau}\mathbb EY_A
 &=u+a-(v_1+z)\mathbb EY_A+2v\mathbb EY_B,\\
 s(\tau)&=a+b+(w+z)\mathbb EY_A+(t+v)\mathbb EY_B .
\end{split}                                               \tag{4.3}
\]

Here \(t,v\) are the rates \(BC\to B,2A\) from (2.1).
The expected leading-workload increment is exactly

\[
 F_T(a_0,b_0)
 =\rho\{\mathbb EY_A(T)-a_0\}
  +p_B\{\mathbb EY_B(T)-b_0\}
  -\int_0^Ts(\tau)\,d\tau.                               \tag{4.4}
\]

For every fixed \(Q\),

\[
 \max_{a_0+2b_0\le Q}F_T(a_0,b_0)\longrightarrow-\infty
 \quad(T\to\infty).                                      \tag{4.5}
\]

If \(v_1+z>0\), (4.3) has a finite limiting mean and the limiting
service rate is strictly positive. Otherwise
\(a=b=w=z=0\) would leave only the neutral pair
\(C\rightleftarrows AC\), a closed directed subset. If \(v_1+z=0\),
then \(w>0\). When \(u+a>0\), the mean of \(Y_A\) grows linearly and
\(\int w\mathbb EY_A\) grows quadratically; when \(u+a=0\), the source
\(C\) must have a direct edge to \(0\), so \(b>0\). If \(Y_B\) does not
decay because \(v=0\), strong connectivity of \(L_0\) gives \(t>0\), and
\(tY_B\) supplies service. These alternatives prove (4.5), uniformly on
the finite initial phase set.

Choose \(T,\epsilon>0\) so the maximum in (4.5) is at most
\(-4\epsilon\). Stop the \(T/n\) full-chain window if

\[
 C\notin[n/2,2n]\quad\hbox{or}\quad A+B>n^{1/4}.           \tag{4.6}
\]

The phase process is linear and has exponential moments on fixed
\(\tau\)-intervals. Non-\(C\)-source reactions have total physical rate
at most \(K(1+(A+B)^2)\), whose integral on \(T/n\) is \(o_{L^p}(1)\).
Random time changes and the Burkholder inequality therefore give,
uniformly over \(q\le Q\),

\[
 \mathbb E[U(X_{T/n})-U(X_0)]\le-3\epsilon.              \tag{4.7}
\]
\[
 \sup_n\mathbb E|U(X_{T/n})-U(X_0)|^p<\infty.            \tag{4.8}
\]

The stop is removable: the number of leading reactions has all fixed
moments, (4.6) has super-polynomially small probability, and the
total-population Yule bound charges its endpoint.

### 4.2 The sole dormant atom

For \(L_-=\{0,A,AC\}\), suppose first that \(A+B>0\). The enabled
\(C\)-order sources are \(AC\) and \(BC\). Every \(AC\)-edge targets
\(0\) or \(A\), and therefore has \(U\)-increment \(-(\rho+1)\) or
\(-1\). At source \(BC\), the rate-weighted mean increment is strictly
negative by \(c_{BC}>0\). Since \(q\le Q\), conditioning on the first
\(AC\)- or \(BC\)-reaction gives constants \(\epsilon_1,c_1>0\), uniform
over all nonzero phases, such that

\[
 \mathbb E\Delta U\le-4\epsilon_1,\qquad
 \mathbb E\sigma^p+\mathbb E|\Delta U|^p\le C_p           \tag{4.9}
\]

for the leading block, whose mean physical duration is at most \(c_1/C\).
The probability that a non-\(C\)-source reaction occurs first is
\(O(1/C)\), so the same bounds, with \(-3\epsilon_1\), hold for the full
chain at all large \(C\).

The only phase with no \(C\)-order source is

\[
 (A,B)=(0,0).                                             \tag{4.10}
\]

At (4.10), wait for the first reaction sourced at \(0\). Its mean time is
the reciprocal of the fixed positive total \(0\)-exit rate. A target
\(A\), followed by the first \(AC\)-reaction, has net \(U\)-increment at
most \(\rho-1<0\). A target \(AC\) followed by \(AC\to0\) is a neutral
trial. If instead \(AC\to A\) occurs, one more \(AC\)-reaction makes the
net increment at most \(\rho-1\). Strong connectivity says that either
\(0\to A\) or \(AC\to A\) has positive rate; otherwise
\(\{0,AC\}\) cannot reach \(A\).

Thus each trial has probability \(p_*>0\) of decreasing \(U\) by at least

\[
 \delta_*=1-\rho>0,                                      \tag{4.11}
\]

and otherwise returns with zero leading reward. The trial count is
geometrically dominated. During an \(AC\)-part, service has rate
\(\Theta(C)\), while all interfering reactions have bounded rate at the
bounded phase. Their probability is \(O(1/C)\), with the same conclusion
for fixed endpoint moments. Hence, for large \(C\), the complete dormant
block satisfies

\[
 \mathbb E\Delta U\le-3\epsilon_0,\qquad
 \mathbb E\sigma^p+\mathbb E|\Delta U|^p\le C_p.          \tag{4.12}
\]

This regeneration includes all excursions of the finite phase; it does
not stop at a fixed \(C\)-box boundary.

## 5. Global return to the core or a finite set

Choose \(M\) so that

\[
 F_V=\{x\in{\cal B}:U(x)\le M\}                           \tag{5.1}
\]

is finite and contains all finite-\(C\) exceptions in Section 4. For the
ten supports containing \(2C\), enlarge \(M\) so that
\({\cal B}\subset F_V\); no vertical episode is then required. Starting
from \({\cal B}\mathbin{\backslash} F_V\), run (4.7), (4.9), or (4.12), obtaining
\(Y\).
If \(Y\in{\cal R}\), stop; otherwise append \(\tau_{\cal R}\) from (3.4).
Call the result \(\sigma_V\).

The appendage has nonpositive expected \(U\)-increment by (3.4). Thus

\[
 \mathbb E_x[U(X_{\sigma_V})-U(x)]\le-\epsilon_V          \tag{5.2}
\]

for a common \(\epsilon_V>0\), and \(X_{\sigma_V}\in{\cal R}\).

The power estimate is equally important. By (2.15), optional sampling
makes the outer appendage nonincreasing for \((1+U)^2\).
Equations (4.8), (4.9), and (4.12) then yield

\[
 \mathbb E_x[(1+U(X_{\sigma_V}))^2-(1+U(x))^2]
 \le-c_V(1+U(x))+C_V.                                    \tag{5.3}
\]

Iterate (5.2) at endpoints in \({\cal B}\mathbin{\backslash} F_V\), and stop when
\({\cal K}\cup F_V\) is reached. Summing (5.2) and
(5.3), and using (3.4) for appended durations, gives

\[
\begin{split}
 \mathbb E_xN_V&\le {1+U(x)\over\epsilon_V},\\
 \mathbb E_x\sum_{j<N_V}(1+U_j)&\le C(1+U(x))^2,\\
 \mathbb E_x\tau_{{\cal K}\cup F_V}&\le C(1+U(x))^2.
\end{split}                                               \tag{5.4}
\]

Repeating the bounded-jump Taylor and counting-martingale estimates at
higher powers gives, for each fixed \(p\),

\[
 \mathbb E_x\!\left[
 \tau_{{\cal K}\cup F_V}^{\,p}
 +U(X_{\tau_{{\cal K}\cup F_V}})^p
 +|q(X_{\tau_{{\cal K}\cup F_V}})-q(x)|^p\right]
 \le C_p(1+U(x))^{r_p}.                                  \tag{5.5}
\]

This is a global physical-time return theorem with endpoint integrability,
not a tightness-to-finite-phase assertion. From an arbitrary initial state,
first run \(\tau_{\cal R}\). Its endpoint lies in
\({\cal K}\cup{\cal B}\); if it lies in \({\cal B}\mathbin{\backslash} F_V\), apply
the preceding vertical trace. Thus (5.4)--(5.5), with changed polynomial
constants, hold for the global hitting time of \({\cal K}\cup F_V\).

## 6. Core episode

Start at \(x\in{\cal K}\), put \(N=q(x)\), and run the full chain for

\[
 h_N={T\over\sqrt{N+1}}.                                 \tag{6.1}
\]

The audited Proposition 5.1 in two_active_promotion_phase.md, including
its exponential \(C\)-domination and scaled corrector
\(2C/(d\sqrt N)\), proves, uniformly on the core,

\[
 \mathbb E_x[q(X_{h_N})-N]\le-\epsilon_R                 \tag{6.2}
\]

for all large \(N\). It also gives all fixed moments of the \(q\)-change
count, a fixed Riccati margin below the \(A=K\sqrt q\) boundary, and a
uniform exponential moment for \(C\).

From \(Y=X_{h_N}\), append the global return of Section 5 until first
entrance into \({\cal K}\cup F_V\), stopping permanently at \(F_V\).
The needed all-fourteen \(C\)-tail estimate is as follows; it is not
inferred merely from the core-window proposition. On the typical
Riccati event,

\[
 q(Y)\in[N/2,2N],\qquad A(Y)\le K_0\sqrt N,\qquad
 C(Y)=c_0\le N^{1/8},                                    \tag{6.3}
\]

with a fixed margin below the \(A=K\sqrt q\) boundary. Stop the cleanup
when \(C\le C_*\) or one of the first two bounds in (6.3), with half its
margin, is violated. Throughout this stop,
\(B=(q-A)/2\ge cN\), so the fast \(BC\)-service rate is at least
\(c_1NC\). Fast \(C\)-immigration from \(B\) and \(2A\) is at most
\(C_1N\). The added lower sources can increase \(C\) at total rate at
most

\[
 C_2N+C_2\sqrt N\,C.                                    \tag{6.4}
\]

Here \(A\)-sourced births cost \(O(\sqrt N)\), and the only potentially
linear per-\(C\) addition, \(AC\to2C\), costs
\(O(\sqrt N\,C)\); it is absorbed by the \(c_1NC\) death for large
\(N\). A stopped comparison with an immigration--death chain of
immigration \(C_3N\) and per-particle death \(c_3N\) therefore gives

\[
 \begin{split}
 \mathbb E\sigma_C&\le {C(1+\log(1+c_0))\over N},\\
 \mathbb E\int_0^{\sigma_C}(1+C_t+C_t^2)\,dt
 &\le {C(\log N+c_0+c_0^2)\over N}=o(1).
 \end{split}                                             \tag{6.5}
\]

The same comparison gives every fixed polynomial moment of these
quantities. The only positive-\(q\) lower sources are \(0,C,2C\), whose
total propensity is at most \(C(1+C+C^2)\). Hence their expected count,
and their second-moment contribution, are \(o(1)\) by (6.5).
The \(AC\to2C\) channel is \(q\)-nonpositive and has already been
absorbed in (6.4). The fixed Riccati margin, the counting-martingale
bound, and (6.5) make the probability of hitting either other cleanup
stop smaller than every fixed power of \(N^{-1/2}\). Thus on the typical
event the cleanup duration, positive \(q\)-cost, and full \(q\)-increment
second moment are \(o(1)\).

The complementary event has probability smaller than every power of
\(N^{-1/2}\). The polynomial return estimate (5.5), Hölder's inequality,
and arbitrarily high moments make its duration, positive \(q\)-cost, and
endpoint second-moment contribution \(o(1)\). Thus the complete core
episode \(\sigma_K\) satisfies

\[
\begin{split}
 X_{\sigma_K}&\in{\cal K}\cup F_V,\\
 \mathbb E_x[q(X_{\sigma_K})-q(x)]&\le-\epsilon_K,\\
 \sup_{x\in{\cal K},q(x)>N_0}\mathbb E_x\sigma_K&<\infty,\\
 \sup_{x\in{\cal K},q(x)>N_0}
 \mathbb E_x|q(X_{\sigma_K})-q(x)|^2&<\infty
\end{split}                                               \tag{6.6}
\]

for some \(\epsilon_K>0,N_0<\infty\).

## 7. Random-time Foster composition

Let

\[
 F=F_V\cup({\cal K}\cap\{q\le N_0\}).                    \tag{7.1}
\]

It is finite. From an arbitrary state, Section 5 reaches
\({\cal K}\cup F_V\) in finite mean physical time. If \(F_V\) is reached,
stop. Otherwise run the core episodes until \(F_V\) is reached or the core
shell has \(q\le N_0\). For successive shell values \(Q_j\) and trace
hitting index \(\nu\), stopped telescoping of (6.6) gives

\[
 \epsilon_K\mathbb E_x(m\wedge\nu)\le q(x),\qquad
 \mathbb E_x\nu\le {q(x)\over\epsilon_K}.                 \tag{7.2}
\]

The duration and endpoint second-moment bounds in (6.6) justify the
telescoping and give finite mean physical hitting time of \(F\).

Fix a closed irreducible population class \(\Gamma\). The construction
stays in \(\Gamma\), so \(F\cap\Gamma\ne\varnothing\). From a state in
the finite set \(F\cap\Gamma\), take one ordinary jump and apply the
finite-mean hitting bound to its finitely many successors. The finite trace
has finite mean positive return time (an absorbing singleton is already
positive recurrent). Irreducibility gives positive recurrence of the
whole closed class. Together with nonexplosion after (2.14), this proves
Theorem 1.1.

## 8. Independent audit and branch arithmetic

The independent replay checked:

1. the one-sided \(\rho\) choice in every missing-edge strong orientation;
2. the exhaustive long-time alternatives in (4.5);
3. removal of (4.6), including slow-interference endpoint moments;
4. both first-target cases in the dormant block;
5. the squared-workload iteration (5.3)--(5.5); and
6. the exceptional-event use of (5.5) in the core appendage.

No orientation/rate counterexample or load-bearing gap was found. The
finite certificate identifies 42 descriptor incidences on exactly fourteen
ordered support pairs. The phase classifier is applied after the earlier
exact residual branch has been removed. Thus, although the family has the
same top support, it does not contain the already certified partner

\[
 \{B,2A,B+C\}\ /\ \{0,A,C\}.
\]

The prior-branch overlap is therefore zero, and the overlap-free table
contribution is

\[
 14-0=14
\]

new positive-invariant ordered support pairs and zero signed pairs. Relative
to the previously certified remainder, the exact update is

\[
 (2169,191)\longmapsto(2155,191).                        \tag{8.1}
\]

This arithmetic does not claim closure of any rank-one, one-active, or
all-active interface.

The scoped finite support certificate is reproduced by

    PYTHONPATH=src python3 -B src/rank_two_return_certificate.py
    PYTHONPATH=src python3 -B -m unittest \
      tests/test_rank_two_return_certificate.py -v

It freezes 42 incidences, 14 support pairs/lower supports, the split \(10+4\), the
vertical split \(3+1\), and support hash

    ec552cc5f008cbb881c52dfc054d4ea1034357bebe525c6be06b389dd019540c

The executable records analytic_theorem_certified as true to mirror the
independent proof audit; its finite checks do not substitute for that audit.
