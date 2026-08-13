# A proof-first regenerative kernel for the six separated hard supports

**Claim-neutral repair note (2026-08-12 PDT).** This note proves only the
local stochastic statement for the six separated supports isolated in
“The non-base-open hard kernel.” It changes no atlas, incidence, pair, or
global certification flag. The six support sets are finite input data, but
no orientation list and no search through a population box is used as a
probability proof.

The main correction is that the relevant object is the occupation of the
**entire physical proper return cycle**, not the occupation of a chosen
simple cycle in the complex graph. A proper path can create spare \(U\),
and the same graph path can then be replayed while carrying that spare
molecule. This slack-lifting mechanism is load-bearing for the source
\(U+I\). It also resolves the apparent even-residue obstruction in
Section 4.

All linkage orientations are arbitrary strongly connected directed graphs,
and all rate constants are arbitrary fixed positive numbers. Constants may
depend on this fixed graph and rate data, but not on \(n\), the subpower
spectator input, the residue class, or the incoming reflected mark.

## 1. Scope and assertion

Write

\[
 C=V+I,\qquad R=V-n.
\]

The six proper/lower support pairs are

\[
\begin{array}{c|c}
L_+&L_0\\ \hline
\{0,2U,C\}&\{I,2I,U+I\}\\
\{0,U,2U,C\}&\{2I,U+I\}\\
\{0,U,2U,C\}&\{I,2I\}\\
\{0,U,2U,C\}&\{I,2I,U+I\}\\
\{0,U,C\}&\{I,2I,U+I\}\\
\{U,2U,C\}&\{I,2I,U+I\}.
\end{array}                                                     \tag{1.1}
\]

Start at the no-fast base

\[
                         X_0=(U,V,I)=(u,n,0),                    \tag{1.2}
\]

where \(u=n^{o(1)}\). The statement is used only when the historically
reachable reflected lift has selected old-active debt \(D_V>0\). Until the
first crossing \(V<n\), reflection is inactive and

\[
                    D_V(t)=D_V(0)+V(t)-n.                       \tag{1.3}
\]

Thus the included reaction which first reaches \(V=n-1\) really services
one unit of the incoming mark.

Put

\[
 L_n=\left\lfloor {n^{1/3}\over\log(n+e)}\right\rfloor .        \tag{1.4}
\]

The stopping labels are physical and disjoint:

* \(D_n\) is the first included reaction with \(V<n\);
* \(P_n\) is a boundary-causing reaction landing on
  \(I=R=0,\ U\ge L_n\);
* \(B_n\) is every other first hit of \(U\vee I\vee |R|\ge L_n\);
* \(E_n\) is the defect label defined in Section 6.

If one physical reaction meets more than one condition, use the priority
\(D_n\) first, then \(P_n\) or \(B_n\), and only then \(E_n\). Thus a
defect reaction which itself services the incoming debt is labelled
\(D_n\), while a defect reaction which first crosses the cutoff is retained
at its included endpoint under \(P_n\) or \(B_n\). With this convention the
four labels are genuinely disjoint.

> **Theorem 1.1 (separated-six regenerative service).** For every support
> in (1.1), every strong orientation of both linkages, every fixed positive
> rate vector, every historically reachable positive-\(D_V\) start (1.2),
> and every fixed \(p\), there is a physical stopping time
> \(\sigma_n\in D_n\sqcup E_n\sqcup P_n\sqcup B_n\) such that
> \[
> \begin{aligned}
>  \mathbb P(D_n^c)&\le n^{-1+o(1)},\\
>  \mathbb E\!\left[(1+U_{\sigma_n}+I_{\sigma_n}
>                    +|R_{\sigma_n}|)^p;E_n\right]
>      &\le n^{-1+o(1)},\\
>  \mathbb E\!\left[(1+U_{\sigma_n}+I_{\sigma_n}
>                    +|R_{\sigma_n}|)^p;P_n\cup B_n\right]
>      &\le C_{p,M}n^{-M}\qquad(M<\infty),\\
>  \mathbb E(1+U_{\sigma_n}+I_{\sigma_n}
>                    +|R_{\sigma_n}|)^p&=n^{o(1)},\\
>  \mathbb E\sigma_n^p&\le n^{p+o(1)}.
>                                                               \tag{1.5}
> \end{aligned}
> \]
> In particular the duration exponent is \(1\), hence at most \(3\).
> For the pair-wide corrected factorial potential \(W_\ell=G_\ell^4\)
> defined in Section 8,
> \[
>  \mathbb E[W_\ell(X_{\sigma_n})-W_\ell(X_0)+\sigma_n]
>       \le -cG_\ell(X_0)^3\log n                              \tag{1.6}
> \]
> for all sufficiently large \(n\).

The first line of (1.5) comes from an exact Feynman–Kac expansion of a
recurrent proper environment, not a finite-word minorization.

## 2. The lower-free proper return process

Temporarily delete all lower reactions. Proper reactions preserve

\[
                              R-I=0.                             \tag{2.1}
\]

At a no-fast state, contract an opening \(y\to C\) and its first
\(C\)-sourced cleanup \(C\to z\), but retain the physical holding time. If

\[
 \kappa_C=\sum_{C\to z}\kappa_{Cz},
 \qquad p_z={\kappa_{Cz}\over\kappa_C},                         \tag{2.2}
\]

then the limiting no-fast generator on
\(S=L_+\setminus\{C\}\) is

\[
\begin{aligned}
 \overline{\mathcal L}f(w)={}&
 \sum_{y\to z;\ y,z\in S}\kappa_{yz}(w)_{\underline{c_y}}
       [f(w-c_y+c_z)-f(w)]\\
 &+\sum_{y\to C}\kappa_{yC}(w)_{\underline{c_y}}
       \sum_{C\to z}p_z[f(w-c_y+c_z)-f(w)].
                                                               \tag{2.3}
\end{aligned}
\]

Exact self returns in (2.3) are deleted. Eliminating \(C\) from a strong
directed graph leaves a strong directed graph on \(S\): replace each
subpath \(y\to C\to z\) by \(y\to z\). Thus (2.3) is a one-species
weakly reversible mass-action chain on a subset of \(\{0,U,2U\}\).

The recurrent residue atoms may be chosen as

\[
\begin{array}{c|c}
S&\text{atoms}\\ \hline
\{0,2U\}&0\text{ in the even class},\quad1\text{ in the odd class},\\
\{0,U\},\ \{0,U,2U\}&0,\\
\{U,2U\}&1.
\end{array}                                                     \tag{2.4}
\]

Only the first row has two residue classes. Equality lower reactions may
switch them, so all constants below are uniform over the finite set in
(2.4).

### Lemma 2.1 (uniform proper regeneration)

Let \(a\) be an atom in (2.4), and let \(\tau_a^+\) be the first
proper-only return to \((a,n,0)\) after at least one physical reaction.
For some \(0<\theta'<\theta<1/2\), and every fixed \(p\),

\[
\begin{aligned}
 \sup_n\mathbb E_a(1+\tau_a^+)^p&<\infty,\\
 \sup_n\mathbb E_a\sup_{t\le\tau_a^+}
       \exp\{\theta' U_t\log(U_t+e)\}&<\infty,\\
 \sup_n\mathbb E_a\sup_{t\le\tau_a^+}
       (1+I_t+|R_t|)^p&<\infty.                                \tag{2.5}
\end{aligned}
\]

From a general no-fast \(u\) in the same class, the first-hit quantities
are bounded by \(C_p(1+u)^{c_p}\), or by a slightly larger
factorial-exponential weight when a maximum is taken.

#### Proof

Let \(dU\) be the largest complex in \(S\). Outside a fixed compact set,
the first contracted edge which leaves \(dU\) decreases \(U\), while every
increasing edge is sourced at degree at most \(d-1\). For

\[
             \Phi_\theta(w)=\exp\{\theta w\log(w+e)\},           \tag{2.6}
\]

a bounded increase \(j\le2\) has

\[
 {\Phi_\theta(w+j)\over\Phi_\theta(w)}\le C_jw^{\theta j}.      \tag{2.7}
\]

The normalized positive contribution of every lower-degree source is
\(O(w^{-1+2\theta})=o(1)\); a maximal-source decrease has ratio
\(O(w^{-\theta})\). This gives a strict multiplicative drift for (2.3).
Strong connectivity gives a finite return minorization on the remaining
compact set. The stopped-drift and additive-functional recursions give all
return-count moments and the first two estimates in (2.5) for the
contracted trace.

To undo the contraction, note that at cofactor level \(i\ge1\) the total
\(C\)-sourced rate is

\[
                   \kappa_C(n+i)i,                              \tag{2.8}
\]

whereas all base-sourced proper clocks are at most \(C(1+U)^2\).
Conditional on the base trace, \(j\) unmatched extra openings before
cleanup have the ordered bound

\[
        {C^j(1+U)^{2j}\over n^j j!}.                            \tag{2.9}
\]

We now make explicit the finite-\(n\) resolvent step which transfers the
ideal-chain estimate to the full proper process. Stop on the first
included cutoff hit. For a return cycle from an atom, let \(Q_n\) be the
embedded ideal no-fast kernel obtained from (2.3), killed on its next hit
of that atom or the boundary; for a first-hit path from a general \(u\),
kill it on its first hit of the appropriate atom or the boundary. Exact
self returns are terminal returns, not continuation steps. Let
\(\widehat F_n\) be the **aggregate** continuation kernel of one physical
no-fast-to-no-fast macro containing at least one base-sourced firing during
an open cleanup. It sums arbitrarily many nested openings and same-level
base firings, together with every required fast cleanup, before retaining
the next no-fast continuation endpoint.
Service and boundary endpoints are terminal and therefore omitted from
both continuation kernels. For \(0<\theta<1/2\), the
maximal-degree drift and compact return minorization above give the
same-weight estimate

\[
 (I-Q_n)^{-1}\Phi_\theta\le C\Phi_\theta .                     \tag{2.10}
\]

At every pre-insertion open state below the cutoff, the insertion clock is
at most \(C(1+U+I)^2\), while the fast clock is at least \(cnI\).
A bounded insertion changes \(U\) by at most two, so its
\(\Phi_\theta\)-weight ratio is at most \(CL_n^{2\theta}\).
The ordered fast-downcrossing product supplies the same estimate at
higher carrier levels. Match the path to the ideal macro with the same
initiating edge and cleanup choices; that ideal endpoint weight is already
accounted for in \(Q_n\). More explicitly, pair each nested opening with the
extra \(C\)-cleanup it creates; every other base firing is already a
bounded one-species move. A service-free macro with \(j\ge1\) open-window
base firings therefore changes \(U\), relative to its matched ideal
endpoint, by at most \(2j\), and its ordered
probability has the corresponding \(j\)-fold fast denominator. Summing
all temporal orders and channels gives

\[
 \begin{aligned}
 \bigl\|(I-Q_n)^{-1}\widehat F_n\bigr\|_{\Phi_\theta}
 &\le C\sum_{j\ge1}
       \left({C L_n^{\,2+2\theta}\over n}\right)^j\\
 &=o(1).                                                       \tag{2.11}
 \end{aligned}
\]

Here \(\|K\|_{\Phi_\theta}:=
\sup_{w<L_n}K\Phi_\theta(w)/\Phi_\theta(w)\); the bounded initial
departure from an atom has a uniformly bounded norm and is placed in
front of the displayed resolvent.

The exact first-insertion decomposition now yields the positive-kernel
identity

\[
 (I-Q_n-\widehat F_n)^{-1}
   =\{I-(I-Q_n)^{-1}\widehat F_n\}^{-1}(I-Q_n)^{-1}.          \tag{2.12}
\]

Its Neumann series converges uniformly for all sufficiently large \(n\).
Adding fixed powers of the reaction count or elapsed time to the reward
in (2.11), and using the binomial additive-functional recursion, gives
the corresponding return-count and physical-duration moments. The same
stopped identity retains every included boundary endpoint. Thus the
ideal drift, return, boundary, and duration estimates used in (2.5) hold
for the full finite-\(n\) proper process.

A base-to-base reaction inserted while \(I>0\) does not raise the cofactor
level, but each such insertion still has an ordered factor
\(C(1+U)^2/n\). Summing any number of same-level insertions first gives a
geometric series on bounded \(U\); the complement is absorbed by the
\(\Phi_\theta\)-tail. The factorial denominator in (2.9), summed against
the resulting \(\Phi_\theta\)-Green function, remains finite with every
polynomial size bias. It proves the third estimate in (2.5), and open
holding times only improve the return-time estimate. Direct base holding
times at the bounded atoms have fixed positive total rates and all moments.
These are physical-time, not embedded-time, estimates. \(\square\)

## 3. Ordered occupation and slack accessibility

For a lower source \(y=cU+bI\), define its proper-cycle occupation

\[
 J_y=\int_0^{\tau_a^+}
          (U_t)_{\underline c}(I_t)_{\underline b}\,dt.          \tag{3.1}
\]

### Lemma 3.1 (sourcewise cycle asymptotics)

For every relevant atom \(a\),

\[
\begin{aligned}
 \mathbb E_aJ_y&={A_y(a)\over n}+O(n^{-2}),
       &&y=I\text{ or }U+I,\\
 \mathbb E_aJ_{2I}&=O(n^{-2}),\\
 \mathbb E_a[J_yJ_z]&\le
       C_{y,z}n^{-\{\max(b_y,b_z)+1\}}.                         \tag{3.2}
\end{aligned}
\]

Every coefficient \(A_y(a)\) needed as a source in the lower linkage is
strictly positive. The estimates remain true with any fixed polynomial of
the endpoint or cycle maximum inserted on the left.

#### Proof: upper bounds and the correct two-mark exponent

At level \(I=1\), (2.8) gives mean holding time
\((\kappa_Cn)^{-1}+O(n^{-2}(1+U)^2)\). Thus an \(I\)- or
\(U+I\)-occupation contributes one factor \(n^{-1}\). To occupy \(2I\),
one additional proper opening must beat a rate of order \(n\), after which
the level-two holding interval contributes the second \(n^{-1}\). Ordered
summation using (2.9) gives

\[
 \mathbb E_aJ_y=n^{-b_y}\{A_y(a)+O(n^{-1})\}.                    \tag{3.3}
\]

The coefficient in (3.3) is a convergent sum of nonnegative clean-path
occupation terms. For two marked intervals, expose the larger cofactor level first. Reaching
level \(m=\max(b_y,b_z)\) costs \(m-1\) unmatched openings, and the two
marked holding intervals contribute two more factors \(n^{-1}\). If both
marks lie in the same holding interval, its second moment is also
\(O(n^{-2})\). Hence

\[
            \mathbb E_a[J_yJ_z]
               \le Cn^{-\{\max(b_y,b_z)+1\}}.                   \tag{3.4}
\]

This exponent is sharp in general. Two \(2I\)-marks can share the same
single rare nested opening, giving
\(\mathbb EJ_{2I}^2=\Theta(n^{-3})\), not \(O(n^{-4})\).
Polynomial endpoint weights merely insert a polynomial into (2.9), which
is summable by Lemma 2.1.

#### Proof: positivity by slack lifting

It remains to prove that the coefficient for \(U+I\) does not vanish in a
singular residue.

Suppose first that \(0\in S\). Strong connectivity supplies a simple path
from \(0\) to a nonzero base complex \(hU\in S\), and another simple path
from \(0\) to \(C\), stopped at its first visit to \(C\). Follow the first
path physically to the state \(hU\). Then follow the second path while
carrying that \(hU\) as slack. At every step the state is

\[
                      hU+\{\text{current complex}\},             \tag{3.5}
\]

so each reaction is enabled. The last step reaches \(hU+C\), where
\(U+I\) is enabled. Every \(C\)-sourced choice along these bounded paths
has a fixed positive limiting conditional probability because all such
propensities share the factor \(VI\). Therefore this event has probability
bounded below independently of \(n\), and its final holding occupation is
\(c/n+O(n^{-2})\).

For the odd class of \(S=\{0,2U\}\), the atom itself is one \(U\) of
slack: apply the path \(0\leadsto C\) to \(U+0\). For the even class, the
preceding two-path construction creates \(2U\) of slack. Thus both parity
classes have \(A_{U+I}(a)>0\).

If \(0\notin S\), the only case in (1.1) is \(S=\{U,2U\}\). Starting at
the atom \(U\), follow a simple path \(U\leadsto2U\), and then follow a
simple path \(U\leadsto C\) while carrying the first \(U\) as slack. The
terminal open state contains \(U+C\), and the same holding calculation is
positive.

For the source \(I\), no newly created \(U\)-slack is required. If the
atom itself is a support complex, follow a simple path from that complex to
\(C\). In the odd residue of \(S=\{0,2U\}\), follow a simple
\(0\leadsto C\) path while carrying the atom's single \(U\) as inert
slack. In either case the terminal bounded state has \(I=1\). A simple path
is used only to exhibit one positive summand of the complete occupation
coefficient; the stochastic kernel still sums every physical path.
\(\square\)

### Corollary 3.2 (burn-in)

If \(\tau_a\) is the first proper hit of the appropriate atom from a
no-fast population \(u\), then

\[
\begin{aligned}
 \mathbb E_u\int_0^{\tau_a}\{I_t+U_tI_t\}\,dt
      &\le {C(1+u)^c\over n},\\
 \mathbb E_u\int_0^{\tau_a}(I_t)_{\underline2}\,dt
      &\le {C(1+u)^c\over n^2}.                                \tag{3.6}
\end{aligned}
\]

The bounds remain true with fixed polynomial endpoint weights. This is
the stopped Green-function version of Lemmas 2.1 and 3.1.

## 4. The apparent \(n^{-2}\) counter-witness

Consider the actual second support in (1.1), with the strong cycles

\[
 0\longrightarrow2U\longrightarrow C\longrightarrow U
   \longrightarrow0,
 \qquad 2I\rightleftarrows U+I.                                \tag{4.1}
\]

Start from the even atom \(U=0\). A traversal which insists on using the
proper complex cycle only once reaches its first \(C\) with no spare \(U\),
so it sees no \(U+I\)-clock. If that selected traversal is treated as the
whole regenerative cycle, one is led to an \(n^{-2}\) estimate. That
truncation is not the physical mass-action return cycle.

Indeed, the following legal event occurs before the first return to
\(U=0,I=R=0\):

\[
\begin{array}{c|c}
\text{reaction}&\text{relative state after the reaction}\\ \hline
0\to2U&U=2,\\
2U\to C&C,\\
C\to U&U=1,\\
0\to2U&U=3,\\
2U\to C&U+C,\\
U+I\to2I&2I.
\end{array}                                                     \tag{4.2}
\]

The first five choices have probability bounded below by a fixed positive
constant. At \(U+C\), the last lower clock has fixed positive rate, while
the total \(C\)-cleanup rate is \(\kappa_C(n+1)\). Its conditional
probability is

\[
             {\kappa_{U+I,2I}\over \kappa_C(n+1)+O(1)}
             ={c\over n}+O(n^{-2}),\qquad c>0.                  \tag{4.3}
\]

Thus the full return-cycle \(U+I\)-hazard is at least \(c'/n\), not merely
\(O(n^{-2})\). This is exactly the slack-lifting term in Lemma 3.1.

Even if one deletes \(U\) from the proper support and considers the parity
cycle \(0\to2U\to C\to0\), two legal zero-source births before the opening
reach \(U=4\); the opening then leaves \(2U+C\), again producing an
order-\(n^{-1}\) \(U+I\)-occupation in the even class. A formal
\(n^{-2}\) word is a genuine but nonleading contribution. It cannot be
used as the aggregate first-hazard exponent after neutral proper motion is
summed.

This calculation is not the proof for other orientations. It exposes why
the orientation-free slack lemma, rather than a chosen graph traversal, is
the correct proof object.

## 5. Feynman–Kac selection of the first lower reaction

For a proper return cycle set

\[
 H_1=\sum_{e:\ b_{s(e)}=1}\int_0^{\tau_a^+}\lambda_e(X_t)\,dt,
 \qquad
 H_2=\sum_{e:\ b_{s(e)}=2}\int_0^{\tau_a^+}\lambda_e(X_t)\,dt. \tag{5.1}
\]

Lemma 3.1 gives, uniformly over the finite residue set,

\[
 \mathbb EH_1={A_a\over n}+O(n^{-2}),\quad A_a>0,
 \qquad \mathbb EH_2=O(n^{-2}),
 \qquad \mathbb E(H_1+H_2)^2=O(n^{-2}).                         \tag{5.2}
\]

For an individual lower edge \(e\), the exact probability that it is the
first lower reaction in the cycle is

\[
 p_e(n)=\mathbb E\int_0^{\tau_a^+}
    \lambda_e(X_t)
    \exp\!\left\{-\int_0^t\lambda_0(X_s)\,ds\right\}dt,          \tag{5.3}
\]

where \(\lambda_0\) is the total lower propensity. The inequality
\(0\le1-e^{-x}\le x\), with (3.4), yields

\[
\begin{aligned}
 p_e(n)&={A_{e,a}\over n}+O(n^{-2})
          &&(b_{s(e)}=1),\\
 \sum_{e:\ b_{s(e)}=2}p_e(n)&=O(n^{-2}).                       \tag{5.4}
\end{aligned}
\]

Indeed, the error for an order-one mark against all other order-one marks
is \(O(n^{-2})\), and its error against an order-two mark is
\(O(n^{-3})\). The shared-opening correction
\(\mathbb EJ_{2I}^2=O(n^{-3})\) is therefore harmless and is not
incorrectly replaced by \(O(n^{-4})\).

The number of complete proper cycles before a lower firing consequently
has geometric tails on the \(n\)-scale and every fixed moment \(O(n^p)\).
Conditional on seeing a lower firing, its source has \(I\)-order two with
probability \(O(n^{-1})\).

Let

\[
                    \mathcal A_1=L_0\cap\{I,U+I\}.              \tag{5.5}
\]

It is nonempty in every row of (1.1), while \(2I\notin\mathcal A_1\).
Strong connectivity of the lower linkage gives an edge which first leaves
\(\mathcal A_1\) on a directed path to \(2I\). Its source lies in
\(\mathcal A_1\), its target is \(2I\), and its coefficient in (5.4) is
strictly positive by Lemma 3.1. Hence, for some \(\delta>0\), uniformly
over the finite proper residue set,

\[
 \mathbb P\{\text{leading order-one edge targets }2I
       \mid\text{an order-one edge occurs}\}\ge\delta.          \tag{5.6}
\]

This is a cut statement for exact aggregate coefficients, not a
Hamilton-cycle or reaction-word minorization.

## 6. Equality renewal, strict service, and defects

Immediately before a clean leading lower firing, \(R=I\). A lower edge
\(y\to z\) changes \(I\), but not \(R\), so throughout the following
proper cleanup

\[
                         R-I=b_y-b_z.                           \tag{6.1}
\]

There are two leading possibilities.

1. If \(b_y=1,b_z=2\), then \(R-I=-1\). The proper cleanup reaches
   \(I=0,R=-1\); its last included \(C\)-sourced firing is \(D_n\).
2. If \(b_y=b_z=1\), then \(R-I=0\). The cleanup returns to a no-fast
   base with \(V=n\). Regenerate to the atom of the new residue and repeat.

By (5.6), the number \(K\) of equality episodes before the first service
episode is dominated by a geometric random variable with parameter
\(\delta\). It has all fixed moments uniformly in \(n\).

The defect label \(E_n\) includes:

* a lower firing during the initial or a post-equality burn-in;
* a first lower firing sourced at \(2I\);
* an order-one lower firing occurring at level \(I\ge2\);
* any second lower firing, or any base-sourced proper firing, during the
  final one- or two-death fast cleanup.

The first item has weighted probability \(n^{-1+o(1)}\) by Corollary 3.2.
The second and third are \(O(n^{-1})\) relative to a leading lower episode
by (3.2) and (5.4). Starting from a clean order-one lower endpoint, the
cleanup has at most two \(C\)-deaths at rates at least \(cn\), while every
competing clock has a fixed polynomial rate in its factorial-tailed
spectator endpoint. The last item therefore has endpoint-weighted
probability \(O(n^{-1})\). Summing over the geometrically bounded number of
equality episodes gives

\[
 \mathbb E[(1+U_{\sigma_n}+I_{\sigma_n}+|R_{\sigma_n}|)^p;E_n]
       \le {C_p(1+u)^{c_p}\over n}.                             \tag{6.2}
\]

On the complement of \(E_n\) and the boundary labels, the equality renewal
must end at \(D_n\). Hence

\[
                           \mathbb P(D_n^c)\le n^{-1+o(1)}.      \tag{6.3}
\]

Each proper cycle has bounded physical-duration moments by Lemma 2.1. The
number of cycles in one lower episode has moments \(O(n^p)\), and the
number of equality episodes has bounded geometric moments. The random-sum
binomial recursion gives

\[
                  \mathbb E\sigma_n^p
                     \le C_p n^p(1+u)^{c_p}=n^{p+o(1)}.         \tag{6.4}
\]

No contraction has erased elapsed time. In particular, the weaker exponent
\(3\), sufficient for the fourth-power comparison, follows immediately.

Polynomial size bias in Lemma 3.1 and the same geometric recursion give

\[
 \mathbb E(1+U_{\sigma_n}+I_{\sigma_n}+|R_{\sigma_n}|)^p
       \le C_p(1+u)^{c_p}=n^{o(1)}.                             \tag{6.5}
\]

## 7. Boundary payment at the included endpoint

The multiplicative drift in Lemma 2.1 gives

\[
 \mathbb P_a\{\max_{t\le\tau_a^+}U_t\ge k\}
       \le C\exp\{-c k\log(k+e)\}.                              \tag{7.1}
\]

The ordered unmatched-opening bound (2.9) gives the same tail form for
\(I\) and \(R\). There are only polynomially many proper cycles in every
fixed-moment sense before service. Multiplying (7.1) by such a polynomial
at \(k=L_n\) remains superpolynomially small. Every reaction vector is
bounded, so a first included crossing lands a fixed distance beyond the
cutoff. Thus, for all fixed \(p,M\),

\[
 \mathbb E[(1+U_{\sigma_n}+I_{\sigma_n}+|R_{\sigma_n}|)^p;
                  P_n\cup B_n]\le C_{p,M}n^{-M}.                \tag{7.2}
\]

The path labels are retained: an open-phase \(U\)-boundary belongs to
\(B_n\), not to the no-fast handoff \(P_n\).

## 8. Actual entropy and the common fourth power

Fix the pair-wide vector \(\ell\), and choose \(K_\ell\) so that

\[
 G_\ell(x)=K_\ell+\sum_j\log(x_j!)+\ell\mathbin\cdot x\ge1,
 \qquad W_\ell(x)=G_\ell(x)^4.                                 \tag{8.1}
\]

Put \(B_\ell(w)=\log(w!)+\ell_Uw\). On a clean service endpoint,

\[
                 V=n-1,\qquad I=0.                             \tag{8.2}
\]

Its spectator population is an order-one-source occupation endpoint of a
cycle started from a bounded atom, followed by at most two clean deaths.
The size-biased form of Lemma 3.1 has a factorial-exponential tail. Hence

\[
 \mathbb E[B_\ell(U_{D_n});D_n]\le C.                           \tag{8.3}
\]

Since \(B_\ell\) has a finite lower bound on the nonnegative integers,
(8.3) retains the actual endpoint and implies

\[
 \mathbb E[B_\ell(U_{D_n})-B_\ell(u);D_n]\le C.                 \tag{8.4}
\]

On \(E_n\), (6.2) pays factorial entropy after increasing its polynomial
exponent; because \(u=n^{o(1)}\), the contribution is
\(n^{-1+o(1)}\log n=o(\log n)\). Equation (7.2) pays the actual included
boundary endpoint. Using

\[
                \log((n-1)!)-\log(n!)=-\log n,                 \tag{8.5}
\]

gives the one-sided entropy estimate needed for drift:

\[
 \mathbb E[ G_\ell(X_{\sigma_n})-G_\ell(X_0)]
       \le-\log n+o(\log n).                                   \tag{8.6}
\]

For every fixed \(r\), the same endpoint estimates give

\[
 \mathbb E|G_\ell(X_{\sigma_n})-G_\ell(X_0)|^r=n^{o(1)}.        \tag{8.7}
\]

At (1.2), \(G_\ell(X_0)=\Theta(n\log n)\). The exact identity

\[
\begin{aligned}
 \Delta W_\ell={}&4G_\ell^3\Delta G_\ell
       +6G_\ell^2(\Delta G_\ell)^2\\
      &+4G_\ell(\Delta G_\ell)^3+(\Delta G_\ell)^4              \tag{8.8}
\end{aligned}
\]

and (8.6)–(8.7) show that the last three terms are
\(o(G_\ell^3\log n)\), while the first is at most
\(-4G_\ell^3\log n+o(G_\ell^3\log n)\). The physical duration (6.4) is
smaller still. This proves (1.6).

## 9. Audit boundary

The local theorem rests on four orientation-free facts:

1. the contracted proper environment is a recurrent one-species
   mass-action chain with a factorial return Green function;
2. slack lifting makes every required order-one source accessible in every
   residue class;
3. ordered occupation gives an \(n^{-1}\) aggregate order-one hazard, an
   \(n^{-2}\) order-two hazard, and the sharp two-mark exponent
   \(n^{-(\max(b_y,b_z)+1)}\); and
4. the strong lower cut supplies fixed service probability per leading
   episode, so equality episodes form a bounded geometric renewal.

The note does not claim that a selected simple graph cycle has the same
hazard as the full return cycle; Section 4 shows why that is false. It also
does not prove that these six supports, the other non-base-open supports,
or the exact base-open supports form a complete global selector. Marked
handoff and atlas composition remain separate obligations.
