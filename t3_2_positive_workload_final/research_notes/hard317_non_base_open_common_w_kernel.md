# The non-base-open hard kernel: graph cuts and regenerative lower killing

**Proof-first, claim-neutral note (2026-08-11 PDT).  Audit status:
FAIL-as-written pending repair of (3.14).**  This note treats the
129 generalized Family-II support templates not covered by the exact
base-open cloud theorem.  They consist of 20 exact proper supports with no
cofactor-free proper source and 109 proper supports with at least three
complexes.  The argument is analytic.  A finite support table is used only
to verify the structural trichotomy in Section 2; no finite state box,
orientation list, or bounded reaction-word list is used to infer a
probability estimate.

All linkage orientations below are arbitrary strong orientations, and all
rate constants are arbitrary fixed positive numbers.  Constants may depend
on that fixed data, but not on the active population $n$, the spectator
population $u$, or the reflected debt carried into the episode.

This note changes no incidence, pair, or global certification flag.  Its
purpose is to state and prove the local common-potential stopped kernel for
this 129-template scope in a form suitable for independent audit.

## 1. Physical chart and stopping labels

Use coordinates

\[
 U=\hbox{spectator},\qquad V=\hbox{old active species},\qquad
 I=\hbox{cofactor}.
\]

The proper linkage $L_+$ contains $V+I$, no other complex contains
$V$, and the lower linkage $L_0$ is $V$-free.  Every complex belongs
to

\[
 \{0,U,2U,I,2I,U+I,V+I\}.                         \tag{1.1}
\]

Start from the no-fast base

\[
                         x=(u,n,0),                 \tag{1.2}
\]

where $u=n^{o(1)}$.  Put $R=V-n$.  A firing sourced at $V+I$
decreases $R$ by one.  Before strict service, $R\ge0$, and the first
firing with $R=0$ sourced at $V+I$ is the physical service event

\[
              D_n=\{\hbox{the first physical crossing }V<n\}.   \tag{1.3}
\]

Fix

\[
 L_n=\left\lfloor{n^{1/3}\over\log(n+e)}\right\rfloor.          \tag{1.4}
\]

Every boundary-causing reaction is included.  The two boundary labels are
path labels, not two names for the same endpoint:

* $P_n$ is a boundary-causing reaction which lands on
  $I=R=0, U\ge L_n$;
* $B_n$ is every other first hit of
  $U\vee I\vee R\ge L_n$, including a hit inside an open excursion.

Thus $P_n\cap B_n=\varnothing$.  An exact physical-population return may
be erased in an analytic renewal identity, but its elapsed physical time
and every boundary hit before that return are retained.

When one reaction satisfies more than one stopping condition, labels are
assigned in physical order: first $D_n$ if it crosses $V<n$, otherwise
$P_n$ or $B_n$ if it hits the cutoff, and otherwise $E_n$.  Thus the
terminal labels used below are disjoint and exhaustive.

Let $D_V>0$ be the incoming reflected old-active debt.  The stopping rule
below is mark-blind after this eligibility check.  Until (1.3), reflection
is inactive in the $V$-mark and

\[
                 D_V(t)=D_V(0)+V(t)-n.             \tag{1.5}
\]

Consequently every exact return to $V=n$ restores the incoming mark and
the crossing (1.3) reduces it by one.

## 2. The support trichotomy

Call $0,U,2U$ **base complexes** and $I,2I,U+I$ **cofactor
complexes**.  Delete $V+I$ when making this distinction.

### Lemma 2.1 (structural partition)

The 129 support templates split as follows.

\[
\begin{array}{c|rrr|r}
 &\text{mixed}&\text{no-history}&\text{separated}&\text{total}\\
\hline
\text{exact, no base proper source}&18&2&0&20\\
\text{larger proper support}&93&10&6&109\\
\hline
&111&12&6&129.
\end{array}                                                     \tag{2.1}
\]

Here:

1. **mixed** means that at least one linkage, after deleting $V+I$,
   contains both a base complex and a cofactor complex;
2. **no-history** means that every proper complex contains $I$, whereas
   every lower complex is a base complex; and
3. **separated** means that $L_+\setminus\{V+I\}$ consists only of base
   complexes and $L_0$ consists only of cofactor complexes.

The six separated supports are exactly

\[
\begin{array}{c|c}
L_+&L_0\\ \hline
\{0,2U,V+I\}&\{I,2I,U+I\}\\
\{0,U,2U,V+I\}&\{2I,U+I\}\\
\{0,U,2U,V+I\}&\{I,2I\}\\
\{0,U,2U,V+I\}&\{I,2I,U+I\}\\
\{0,U,V+I\}&\{I,2I,U+I\}\\
\{U,2U,V+I\}&\{I,2I,U+I\}.
\end{array}                                                     \tag{2.2}
\]

#### Proof

This is support bookkeeping.  The canonical support table has 37 exact
proper pairs: 17 have a base proper source and are outside the present
scope, leaving 20.  Splitting those 20 and the 109 larger supports by the
three mutually exclusive definitions above gives (2.1); direct comparison
of the support sets gives (2.2).  These are the only finite facts used in
the stochastic proof.  In particular, (2.1) says nothing about a strong
orientation or a long physical path.  $\square$

### Lemma 2.2 (the twelve no-history rows are vacuous)

On the reachable reflected lift of a closed irreducible physical class, a
no-history support has no state satisfying $I=0$ and $D_V>0$.

#### Proof

Every proper source contains $I$, so the proper linkage is disabled on
$I=0$.  Every lower complex is $I$-free and $V$-free, so lower
reactions preserve both $I=0$ and $V$.  The face is forward invariant
and cannot be entered from $I>0$, because every proper target also
contains $I$.  Starting the reachable lift with zero mark therefore
leaves $D_V=0$ on this face.  $\square$

It remains to prove a kernel on the 111 mixed and six separated supports.

## 3. Two physical resolvent lemmas

The proofs below use two elementary analytic resolvents.  They are stated
here so that neither a finite path search nor a formal resistance ledger is
mistaken for a stochastic estimate.

Put

\[
 \Psi_\theta(u)=\exp\{\theta u\log(u+e)\},
 \qquad 0<\theta<\tfrac12.                         \tag{3.1}
\]

### Lemma 3.1 (contracted base Green function)

Consider a physical trace on $I=R=0$ made from the following moves.

1. A reaction $y\to z$ between base complexes is retained as
   $u\mapsto u-c_y+c_z$.
2. A proper opening $y\to V+I$, followed by a $V+I$-sourced firing
   to a base complex $z$, is retained as the same base move.
3. A target containing $I$ while $R=0$, or a $V+I$-sourced target
   still containing $I$ after an opening, is killed at the ensuing
   strict service.
4. Exact physical self returns are contracted.  The first non-$V+I$
   firing during the one- or two-fast-step cleanup is put in a separate
   defect kernel $E$.

Suppose the base trace has access to the service killing set and is not a
static class.  Let $Q_n$ be its service-free, defect-free,
nonboundary kernel, after exact self-return contraction.  Then, for every
$0<\theta'<\theta<1/2$,

\[
 (I-Q_n)^{-1}\Psi_{\theta'}(u)
       \le C_{\theta',\theta}\Psi_\theta(u).         \tag{3.2}
\]

The same resolvent has every fixed macro-count moment and every polynomial
occupation moment.  Moreover, for each fixed $p$, the actual first-defect
kernel satisfies the sourcewise, endpoint-weighted bound

\[
 (I-Q_n)^{-1}E
  (1+U_E+I_E+|R_E|)^p
       \le {C_p(1+u)^{c_p}\over n}.                \tag{3.3}
\]

#### Proof

First ignore $E$.  Conditional on a proper cleanup clock, all outgoing
$V+I$ reactions share the factor $VI$; hence their relative
probabilities are fixed positive ratios of rate constants.  A clean
two-step move sourced at a base complex $y$ consequently has rate

\[
              a_{yz}(u)_{\underline{c_y}},          \tag{3.4}
\]

with $a_{yz}>0$.  Direct base reactions have the same form.  Thus the
contracted trace is a one-species mass-action trace on a subset of
$\{0,U,2U\}$, with service killing.

Let $dU$ be its unique maximal-degree enabled source outside a fixed
compact set.  A $dU$-sourced nonself move either is killed or decreases
$U$.  If $dU\to V+I\to dU$ is an exact return, contraction deletes it.
In a larger proper support, the strong cut out of
$\{dU,V+I\}$ is sourced at $dU$ or $V+I$; the cut therefore has a
fixed conditional probability and is again killing or decreasing.  The
exact-pair rows in the present scope have no base proper source, so this is
the only possible diagonal case.

Every positive continuation is sourced at degree at most $d-1$ and has
jump at most two.  Since

\[
 {\Psi_\theta(u+j)\over\Psi_\theta(u)}
        \le C_j u^{\theta j},\qquad |j|\le2,         \tag{3.5}
\]

its normalized positive contribution is
$O(u^{-1+2\theta})=o(1)$.  A maximal-source decreasing move has ratio
$O(u^{-\theta})$, and a maximal-source kill has ratio zero.  This gives a
strict multiplicative $Q_n$-drift outside a compact set.

On the compact set, strong connectivity gives a directed path from every
eligible base class to a cofactor target.  Following a path through base
complexes preserves the nonnegative residual $u-c_y$; a first cofactor
target is enabled.  A visit to $V+I$ is followed along a chosen outgoing
edge, whose conditional probability is a fixed rate ratio.  The only
compact classes without such a path are static $I=0,V$-constant classes;
on a closed irreducible reachable lift they have $D_V=0$.  Since the
compact set is finite, there are $M<\infty$ and $\eta>0$, independent
of large $n$, such that service or the outer drift region is reached in
at most $M$ contracted moves with probability at least $\eta$.  A
finite-state corrector joins this minorization to (3.5) and proves (3.2).
The standard binomial recursion for the occupied move count gives its
fixed moments; polynomial weights are dominated by a smaller
$\Psi$-weight.

It remains to restore the physical windows.  In an open state below the
boundary,

\[
 \lambda_f\ge c nI,qquad
 \lambda_{\rm nf}\le C(1+U+I)^2.                  \tag{3.6}
\]

The ideal cleanup uses at most two fast firings.  For a distinguished
clean edge insertion $J_e$, the two time orderings of one additional
nonfast insertion give

\[
 \mathbb E[J_eJ_{\rm nf}]
 \le {C(1+u)^{c}\over n}\,\mathbb E J_e.          \tag{3.7}
\]

To see (3.7), condition at the earlier insertion.  The future integral is
bounded using (3.6).  For the reverse ordering, reverse the finite fast
downcrossing: every unmatched cofactor contributes one factor $n^{-1}$,
and size bias by a binary propensity contributes only a fixed polynomial
in $1+u$.  Summing levels gives a factorial series.  Hence

\[
 0\le \mathbb E J_e-
 \mathbb E\!\left[J_e e^{-J_{\rm nf}}\right]
 \le\mathbb E[J_eJ_{\rm nf}]
 \le {C(1+u)^c\over n}\mathbb E J_e.             \tag{3.8}
\]

The same calculation after size bias by the endpoint polynomial proves
(3.3) once it is summed against (3.2).  This is a relative two-insertion
estimate; a bare cutoff bound $L_n^2/n$ is not used.  A fast-only hit of
the open boundary requires a factorial number of unmatched births and is
absorbed by the boundary estimate in Section 6.  $\square$

### Lemma 3.2 (regenerative occupation of a separated proper linkage)

Let

\[
                  L_+=S\cup\{V+I\},
 \qquad S\subseteq\{0,U,2U\},                    \tag{3.9}
\]

be one of the four proper supports in (2.2), with an arbitrary strong
orientation.  Delete all lower reactions temporarily.  Before service the
proper chain preserves

\[
                              R-I=0.                \tag{3.10}
\]

Each base communicating class has a bounded atom: $0$ for supports
containing $0,U$, $0$ or $1$ for $S=\{0,2U\}$, and $1$ for
$S=\{U,2U\}$.  Let $\tau_a^+$ be a full return cycle to its atom.
For every fixed $p$, uniformly for large $n$,

\[
 \mathbb E_a(\tau_a^+)^p\le C_p,
 \qquad
 \mathbb E_a\sup_{t\le\tau_a^+}\Psi_{\theta'}(U_t)
       \le C\Psi_\theta(a).                         \tag{3.11}
\]

For a lower source $y=c_yU+b_yI$, define its un-killed occupation in
one proper cycle by

\[
 A_y^{(n)}(a)=
 \mathbb E_a\int_0^{\tau_a^+}
        (U_t)_{\underline{c_y}}(I_t)_{\underline{b_y}}\,dt.
                                                               \tag{3.12}
\]

Then

\[
 A_y^{(n)}(a)=n^{-b_y}
       \{a_y(a)+O(n^{-1})\},                       \tag{3.13}
\]

with $a_y(a)>0$ exactly when the source is accessible in that proper
class.  The estimate remains valid after any fixed polynomial endpoint
size bias.  The frozen draft claimed, for two lower insertions,

\[
 \mathbb E_a[J_yJ_z]
       \le C_{y,z}n^{-b_y-b_z}.                    \tag{3.14}
\]

This is false when \(b_y=b_z=2\).  One nested opening has probability
\(\Theta(n^{-1})\); at carrier level two the holding time is
\(\Theta(n^{-1})\), and the conditional square of the \(2I\)-occupation
is \(\Theta(n^{-2})\).  Thus \(\mathbb E J_{2I}^2=\Theta(n^{-3})\),
not \(O(n^{-4})\).  A corrected ordered two-insertion bound, sufficient for
the later renewal, is being proved separately.  Until it is inserted and
independently replayed, Sections 5--9 are conditional and the scoped
theorem is not established.

#### Proof

At $I=0$, direct reactions between members of $S$, together with a
clean contraction $y\to V+I\to z$, have one-species rates of the form
(3.4).  The maximal-degree argument in Lemma 3.1, now without killing,
gives multiplicative return drift to the displayed atom.  Strong
connectivity supplies a decreasing path from the maximal complex, and the
reverse path supplies irreducibility in the appropriate residue class.
This proves the base part of (3.11).

During an open proper excursion, a $V+I$-sourced downcrossing has rate at
least $cnI$.  Every other proper clock is at most
$C(1+U+I)^2$.  Successive unmatched openings therefore have the
occupation product

\[
 {C^j(1+U)^{2j}\over n^j j!},                    \tag{3.15}
\]

after the direct same-level moves have been summed against the
one-species return Green function.  The maximal-degree drift makes every
polynomial moment of that Green function finite.  Hence (3.15) is summable
at every order, proves the open part of (3.11), and justifies dominated
termwise occupation summation.

Here is the sourcewise calculation behind that dominated expansion.  Put

\[
 \kappa_V=\sum_{V+I\to z}\kappa_{V+I,z},\qquad
 p_z={\kappa_{V+I,z}\over\kappa_V}.                \tag{3.16}
\]

After exact self moves are deleted, the limiting base generator is

\[
\begin{aligned}
 \overline{\mathcal L}f(u)={}&
 \sum_{y\to z;\ y,z\in S}\kappa_{yz}(u)_{\underline{c_y}}
       [f(u-c_y+c_z)-f(u)]\\
 &+\sum_{y\to V+I}\kappa_{y,V+I}(u)_{\underline{c_y}}
       \sum_{V+I\to z}p_z[f(u-c_y+c_z)-f(u)].       \tag{3.17}
\end{aligned}
\]

It is a recurrent one-species mass-action chain in the residue class of
the displayed atom.  If an opening $y\to V+I$ occurs at base population
$w$ and $q=w-c_y$, then, before any additional nonfast reaction,

\[
 \mathbb E_{q,1}\int_0^{\tau_0}
       (U_t)_{\underline c}I_t\,dt
 = {(q)_{\underline c}\over \kappa_V n}
       +O\!\left({(1+q)^{c+2}\over n^2}\right).     \tag{3.18}
\]

For the source $2I$, one further proper opening $s\to V+I$ at level
one gives

\[
 \mathbb E_{q,1}\int_0^{\tau_0}(I_t)_{\underline{2}}\,dt
 ={1\over \kappa_V^2n^2}
   \sum_{s\to V+I}\kappa_{s,V+I}(q)_{\underline{c_s}}
 +O\!\left({(1+q)^C\over n^3}\right).              \tag{3.19}
\]

Equations (3.18)--(3.19) follow by conditioning on the first clock at
level one: its fast holding mean is
$(\kappa_V(n+1)+O((1+q)^2))^{-1}$; after a nested opening, the level-two
holding mean is
$(2\kappa_V(n+2)+O((1+q)^2))^{-1}$, while
the order-two falling factorial at level two equals $2$.  Every omitted
term has at least one additional
nonfast insertion and is summed by (3.15).  Summing (3.18) or (3.19) over
the openings in one cycle of (3.17) gives the coefficient $a_y(a)$ in
(3.13).  Its finiteness follows from the factorial return Green function;
its strict positivity is exactly physical accessibility of the source.

To occupy a source with $b_y$ cofactors requires $b_y$ unmatched
openings and a final holding interval of order $n^{-1}$; equivalently,
the detailed downcrossing product has exactly one $n^{-1}$ factor for
each cofactor in the falling-factorial source.  This gives (3.13).  The
leading coefficient is a finite sum of positive occupation terms.  It is
positive precisely when a proper path reaches an open state enabling
$y$.  Repeating the ordered occupation calculation with two distinguished
insertions gives an $O(n^{-2})$ bound whenever at least one source has
cofactor degree one.  For two degree-two sources the raw square may instead
have the $n^{-3}$ scale recorded after (3.14).  The corrected uniform
ordered statement and its exact use in the Feynman--Kac quotient are the
remaining repair obligation.  Polynomial size bias only inserts polynomial
factors into (3.15), so it does not alter these primitive powers.

Finally, physical holding times at a base atom have all fixed moments, and
open holding times are $O(n^{-1})$.  The move-count return Green and the
binomial additive-functional recursion therefore give the first assertion
of (3.11) in physical, not embedded, time.  $\square$

Two cautions about the intended repaired form of Lemma 3.2 are important.
It treats the **full proper
process**.  Nested proper openings are not truncated or mislabeled as a
rare error.  Also, a corrected ordered version of (3.14), rather than a
bare probability estimate, must be the sourcewise Feynman--Kac input below.

## 4. The 111 mixed supports

For a mixed linkage, choose a directed path from a base complex to a
cofactor complex and stop it at its first cofactor target.  Every internal
source is a base complex.  If the first target is not $V+I$, then $R=0$
and the next $V+I$-sourced firing is strict service.  If the first target
is $V+I$, follow the chosen proper outgoing edge.  A cofactor target
leaves $I>0$ at $R=0$ and the next fast firing is service; a base target
is a contracted base move.

This construction uses a path only to prove positive accessibility on a
finite support graph.  The stochastic trace is the complete kernel of
Lemma 3.1 and retains every reaction.  In particular, the chosen path is
not assigned probability one.

Let $\sigma_n$ stop on $D_n,E_n,P_n$, or $B_n$, where $E_n$ is the
first nonfast firing inside an ideal fast cleanup.  Lemma 3.1 gives, for
every fixed $p$,

\[
\begin{aligned}
 \mathbb E(1+U_{\sigma_n}+I_{\sigma_n}+|R_{\sigma_n}|)^p
     &\le C_p(1+u)^{c_p},\\
 \mathbb E[(1+U_{\sigma_n}+I_{\sigma_n}+|R_{\sigma_n}|)^p;E_n]
     &\le {C_p(1+u)^{c_p}\over n},\\
 \mathbb P(D_n)&=1-n^{-1+o(1)},\\
 \mathbb E\sigma_n^p&\le C_p(1+u)^{c_p}.
\end{aligned}                                                   \tag{4.1}
\]

The duration statement includes every holding time in a contracted exact
return.  It follows by time-marking the kernel in Lemma 3.1 and applying
the same macro-count binomial recursion.  There is no $n$-long pure
renewal in this group: a safe two-node block is a proper subset of the
proper linkage, so its sourcewise strong cut has fixed conditional
probability.  The exact supports in this group have no base proper opening.

## 5. The six separated supports

Here zero-order proper motion alone preserves $V$, so calling a proper
cut "service" would be false.  Service is instead a regenerative lower
killing of the full proper environment.

Every lower support in (2.2) contains $2I$, and its minimum cofactor
source order is one.  More explicitly,

\[
\begin{array}{c|c|c}
L_0&\text{order-one sources}&\text{strict targets}\\ \hline
\{I,2I\}&\{I\}&\{2I\}\\
\{2I,U+I\}&\{U+I\}&\{2I\}\\
\{I,2I,U+I\}&\{I,U+I\}&\{2I\}.
\end{array}                                                     \tag{5.1}
\]

All sources in the middle column are accessible during a proper cycle in
every residue class.  For $I$ this is immediate.  For $U+I$, follow a
proper base path to a base with one spare $U$ and then open; the atoms in
Lemma 3.2 and the four sets $S$ in (2.2) show that this path exists in
both parity classes.

Run the lower-free proper process from $u$ until its bounded atom, unless
a lower reaction or a physical boundary occurs first.  The weighted chance
of a lower reaction during this burn-in is

\[
       {C_p(1+u)^{c_p}\over n}                    \tag{5.2}
\]

for an order-one source, and smaller for an order-two source, by
(3.11)--(3.13).  Put such an early reaction in $E_n$, retaining its
actual endpoint.

At the atom, expose successive complete proper cycles.  If $J$ is the
total lower integrated hazard in one cycle, the exact Feynman--Kac formula
and (3.13)--(3.14) give

\[
\begin{aligned}
 p_{1,n}&=\mathbb P\{\hbox{first lower source has order one in the cycle}\}
             ={a\over n}+O(n^{-2}),\qquad a>0,\\
 p_{2,n}&=O(n^{-2}),\\
 \mathbb P\{\hbox{two lower firings in one cycle}\}&=O(n^{-2}).
\end{aligned}                                                   \tag{5.3}
\]

For example, the relative error in the first line is bounded by

\[
 0\le\mathbb EJ_1-
 \mathbb E\!\left[J_1e^{-J}\right]
 \le\mathbb E[J_1J]=O(n^{-2}),                  \tag{5.4}
\]

not by conditioning on a prescribed finite reaction word.  The number of
proper cycles before an order-one lower firing consequently has all fixed
moments $O(n^p)$.  During those cycles, the chance that an order-two
source wins first is $O(n^{-1})$.

Suppose the leading lower edge is $y\to z$, with $b_y=1$.  Before it
fires, (3.10) holds.  The lower firing changes $I$, not $R$, and every
subsequent proper firing preserves their difference.  Hence

\[
                     R-I=b_y-b_z.                 \tag{5.5}
\]

If $b_z=2$, run the proper cleanup until the raw path crosses $V<n$.
Equation (5.5) forces that crossing before a no-fast return.  If $b_z=1$,
(5.5) is zero; run the proper cleanup to $I=R=0$, then regenerate at the
bounded atom of the new residue class.  In either case, a second lower
firing during cleanup or regeneration has endpoint-weighted probability
$O(n^{-1})$, by the two-insertion bound (3.14), and is assigned to $E_n$
instead of being deleted.

Let $\mathcal A_1$ be the order-one lower complexes.  It is a nonempty
proper subset of $L_0$, because $2I\notin\mathcal A_1$.  Strong
connectivity gives an edge from $\mathcal A_1$ to $2I$.  Its source is
accessible and its coefficient in (5.3) is strictly positive.  There are
only two proper residue atoms.  Therefore there is a fixed
$\delta>0$, independent of $n$, such that every leading lower episode
services with probability at least $\delta$.  The number of equality
episodes before service is geometric with all fixed moments.

Combining this geometric equality renewal with (5.2)--(5.4), for every
fixed $p$, gives

\[
\begin{aligned}
 \mathbb E(1+U_{\sigma_n}+I_{\sigma_n}+|R_{\sigma_n}|)^p
     &\le C_p(1+u)^{c_p},\\
 \mathbb E[(1+U_{\sigma_n}+I_{\sigma_n}+|R_{\sigma_n}|)^p;E_n]
     &\le {C_p(1+u)^{c_p}\over n},\\
 \mathbb P(D_n)&=1-n^{-1+o(1)},\\
 \mathbb E\sigma_n^p&\le C_p n^p(1+u)^{c_p}.
\end{aligned}                                                   \tag{5.6}
\]

This is the physical-time resolvent for the six separated supports.  The
$n$-scale is genuine: order-one lower clocks accumulate over order $n$
proper regeneration cycles.  They are not an $O(n^{-1})$ error after
that renewal.

## 6. Boundary endpoints and historical service

The maximal-degree supermartingale used in (3.2) and (3.11) gives, from a
subpower start,

\[
 \mathbb P\!\left\{\max U\ge k\right\}
     \le C\Psi_\theta(u)\exp\{-c k\log(k+e)\}.       \tag{6.1}
\]

For a mixed support only a polynomial number of physical windows is
occupied in the corresponding weighted sense.  For a separated support
there are $O(n^p)$ fixed moments of the number of proper cycles.  Thus
the union cost at $k=L_n$ remains superpolynomial.

At a fixed occupied $U$, successive unmatched proper openings have the
factorial product (3.15).  Before a lower firing $R=I$; after a leading
equality lower firing the same identity holds.  Hence the $I$- and
$R$-boundaries have the same factorial tail.  Since every reaction vector
is bounded and the boundary-causing reaction is included, for every fixed
$p,M$,

\[
\mathbb E[(1+U_\sigma+I_\sigma+|R_\sigma|)^p;
                 P_n\cup B_n]\le C_{p,M}n^{-M}.      \tag{6.2}
\]

Because $V=n+R$ and $W_\ell$ has only fourth-power factorial growth,
(6.2), with $p,M$ enlarged, also pays the actual common-$W_\ell$
boundary reward.  No preboundary surrogate is substituted for its included
endpoint.

Equations (1.5), (4.1), and (5.6) then show that the terminal $D_n$ is a
strict service of existing reflected debt, not merely a decrement of a
formal relative coordinate.

## 7. Actual entropy endpoint

Fix the same pair-wide vector $\ell$ used by every adjacent chart and put

\[
 G_\ell(x)=K_\ell+\sum_j\log(x_j!)+\ell\mathbin\cdot x,
 \qquad W_\ell(x)=G_\ell(x)^4,                   \tag{7.1}
\]

where $K_\ell$ is fixed and $G_\ell\ge1$.  Write

\[
                    B_\ell(u)=\log(u!)+\ell_Uu.    \tag{7.2}
\]

The killed base resolvent retains the actual spectator coordinate at
service.  More precisely,

\[
 \mathbb E[B_\ell(U_{D_n})-B_\ell(u);D_n]
       \le C\log(u+e)+C.                            \tag{7.3}
\]

For a mixed support, apply the base kernel to

\[
                 h_C(u)=B_\ell(u)+C\log(u+e).       \tag{7.4}
\]

At large $u$, a maximal-source service endpoint can raise $U$ by only
a bounded amount, costing at most $j_*\log u+O(1)$; termination deletes
the $C\log u$ boundary term.  Choose $C>j_*$.  A maximal-source
continuation decreases $U$ and hence pays $-\log u+O(1)$.  Every
positive continuation has a source-degree loss of at least one, so its
expected logarithmic cost is $O((\log u)/u)$.  The remaining positive
residual has finite support and is removed by the finite killed Green
corrector from Lemma 3.1.  Iterating the resulting inequality proves
(7.3).  This retains $B_\ell(U_{D_n})$; it does not replace the service
endpoint by a cemetery value.

For a separated support, first regeneration reaches a bounded atom with
the same maximal-degree estimate.  The lower-killed cycle endpoint and its
proper cleanup have factorial moments by Lemma 3.2, and the number of
leading equality episodes is geometric.  Applying (7.4) to the initial
burn-in and then the bounded-atom cycles proves (7.3) again.

At service $V_{D_n}=n-1$.  The frozen draft incorrectly wrote the
equalities

\[
 \mathbb E\!\left[
 G_\ell(X_{\sigma_n})-G_\ell(X_0)
       +\mathbf1_{D_n}\log n\right]=o(\log n),       \tag{7.5}
\]

and, in particular,

\[
 \mathbb E\Delta G_\ell
                       =-\log n+o(\log n).           \tag{7.6}
\]

Both equality signs are false in general.  A strong orientation may first
produce a much larger negative spectator factorial drift.  The correct
statements required by the fourth-power argument are

\[
 \mathbb E[\Delta G_\ell+\mathbf1_{D_n}\log n]\le o(\log n),
 \qquad
 \mathbb E\Delta G_\ell\le-\log n+o(\log n).          \tag{7.6a}
\]

They remain conditional here on the repaired form of Lemma 3.2.  Additional
spectator descent helps the fourth-power estimate.

The same factorial and endpoint estimates give, for every fixed $r$,

\[
                         \mathbb E|\Delta G_\ell|^r=n^{o(1)}.     \tag{7.7}
\]

## 8. Fourth power and physical duration

At the starting base, $G_\ell(X_0)=\Theta(n\log n)$.  The exact identity

\[
\begin{aligned}
 \Delta W_\ell={}&4G_\ell^3\Delta G_\ell
   +6G_\ell^2(\Delta G_\ell)^2\\
  &+4G_\ell(\Delta G_\ell)^3+(\Delta G_\ell)^4
\end{aligned}                                                   \tag{8.1}
\]

and the intended repaired bounds (7.6a)--(7.7) show that its last three terms are
$o(G_\ell^3\log n)$.  The duration bounds are $n^{o(1)}$ in the mixed
case and $n^{1+o(1)}$ in the separated case, so the physical-time reward
is smaller still.  Therefore, for all sufficiently large $n$,

\[
 \mathbb E_{(u,n,0)}\!\left[
 W_\ell(X_{\sigma_n})-W_\ell(X_0)+\sigma_n\right]
       \le-cG_\ell(X_0)^3\log n.                    \tag{8.2}
\]

All reactions and holding times are present in $\sigma_n$.  The proof
correctors $\Psi_\theta$ and $h_C$ are resolvent weights only; neither
is added to the physical population potential $W_\ell$.

## 9. Scoped theorem and audit boundary

Combining Sections 2--8 gives the following claim-neutral local statement.

> **Non-base-open hard-kernel theorem.**  For every historically reachable
> positive-$D_V$ start (1.2) in any of the 129 support templates, the
> twelve no-history templates are vacuous.  Each of the remaining 117
> templates has the raw physical stopping rule above.  It services one unit
> of old $V$-debt with probability $1-n^{-1+o(1)}$, has arbitrary fixed
> endpoint moments, has physical duration $n^{1+o(1)}$ or better, pays
> both path-labelled boundaries at their actual included endpoints, and
> satisfies the pair-wide common-$W_\ell$ drift (8.2).

This theorem is local.  It does not prove that the 129 templates exhaust a
global descriptor selector, and it does not perform a handoff at $P_n$.
Those are respectively finite atlas and marked strong-Markov composition
obligations.  It also does not certify the separate seventeen-template
exact base-open theorem.

The points requiring hostile independent replay are now precise:

1. the relative two-insertion estimate (3.7)--(3.8), including polynomial
   endpoint size bias;
2. the full-proper regenerative occupation asymptotic
   (3.13)--(3.14), especially the $U+I$ source in both parity classes;
3. the compact service minorization after exact physical self-return
   contraction;
4. the actual-endpoint logarithmic estimate (7.3), rather than a killed-to-
   cemetery surrogate; and
5. the time-marked geometric-cycle recursion in (5.6).

No counterexample to this 117-template local statement is presently known.
The rejected uniform pure-renewal estimate is not used anywhere in the
proof.
