# Two-level physical-state repair for the generalized hard-333 interface

**Status (2026-08-11 PDT).**  This is a new, claim-neutral replacement for
Sections 7--8 of *two_active_dormant_407_resolvent_theorem.md*.  The replaced
snapshot is frozen at

```text
theorem  d7e3ba1548b8b5a3396f9b9aa5de458fd792039b10f780e57623696337ce64c7
source   098969ceeef5589a5a17f000901f43f168583015ac435de8c025add5c412e6a2
tests    ee51167d4948b8fff00d1ce4ae990d61aada1692656b1495d1e1e456359f8804
```

The exact counterexample in
*two_active_dormant_407_asymmetric_return_audit.md* invalidates (7.16i) of
that snapshot.  The problem is the global artificial factor $z^J$: an
exact physical-state self return can increase $J$, and repeated neutral
returns make the next such marked return overwhelmingly likely.  Nothing in
this note uses that inequality, a finite cap on $J$, or any other global
paid-reaction counter.

The replacement has two genuinely different levels.

1. An opened top excursion is followed in the physical variables
   $(U,I,R)$, where $R=V-n$ is the actual reserve above the current old
   active level.  An optional local interruption mark exists only inside
   that one excursion.  It is projected away at the next included physical
   $I=R=0$ return.
2. Exact returns of the complete physical state are erased from the outer
   trace.  Every nonexact return retains its actual $(U,V)$ endpoint and
   enters a killed one-species base resolvent.  Time spent in erased loops is
   retained as a duration reward.

The finite calculation accompanying this note verifies the exact
146-template split used below.  A first independent audit of this replacement,
frozen at note/source/test hashes `96ec15ba...` / `cd33270c...` /
`25775c38...`, found three further proof defects: the historical
positive-debt hypothesis had been dropped, open-phase and no-fast boundaries
had been conflated, and the all-orders factorial estimate lacked its coupled
source/endpoint invariant.  A second operator audit also required a separate
contraction of interrupted exact returns after pure nested diagonals are
summed.  Sections 1, 2, 5, 6, and 8 below attempted those repairs.

A later proof-only audit found a decisive compact-spectator obstruction to
the attempted renewal bound (5.11).  For

\[
 L_+=\{0,V+I\},\qquad L_0=\{I,2U,2I,U+I\},
\]

historically reachable positive-debt bases with (U=0) have a pure-return
inverse of order (n), an order-one renewed upward probability, and a mean
raw duration of order (n).  Thus (5.11), (7.2), (8.2), and the candidate
theorem in Section 9 are false as written.  The exact derivation is frozen in
*two_active_dormant_407_two_level_proof_audit_a.md*.  A proof-first
replacement follows the full singular priority macro using the coboundary
(V+m(U)); it is developed separately in
*hard317_source_zero_priority_macro.md* and is not imported here pending
audit.  All certification flags therefore remain false.  This note promotes
no incidence or support pair and does not certify T3-2 or C3.

## 1. Normalization and physical stopping variables

Fix one closed irreducible physical class $\Gamma$, a reference population
$x^\circ\in\Gamma$, and the reachable all-species reflected-debt lift begun
at $(x^\circ,0)$.  Fix one of the 951 generalized Family-II rows from
Section 2.3 of the frozen note and use its common normalization

```text
U = spectator,       V = old active species,       I = top cofactor.
```

The proper linkage contains $V+I$, no other complex contains $V$, and
the lower linkage does not contain $V$.  Every complex has molecularity at
most two.  Rate constants and the two strong orientations are arbitrary but
fixed.  Constants below may depend on these fixed data and on a requested
moment order, but not on the state or on $n$.

The local theorem is invoked only at a **historically consistent** reachable
no-fast base whose selected old-active mark satisfies $D_V>0$.  Start at

\[
                 x=(u,n,0),\qquad n\longrightarrow\infty,\qquad u=n^{o(1)}. \tag{1.1}
\]

At each later no-fast base $x_b=(u_b,n,0)$, open a new local chart and
write the physical reserve

\[
                       R=V-n.                                        \tag{1.2}
\]

Before a strict service, $R\ge0$.  A reaction not sourced at
$V+I$ cannot lower $R$ and can raise it by at most one.  Every reaction
sourced at $V+I$ lowers $R$ by one.  Such a firing at $R=0$ is the
terminal strict service $D$.  Every nonterminal $V+I$ firing therefore
satisfies

\[
                         \Delta R=-1,\qquad \Delta I\le1.              \tag{1.3}
\]

If an excursion returns to $I=0$ and $R=0$ before $D$, its actual
endpoint $(u',n,0)$ becomes the next outer base; in particular its actual
spectator coordinate $u'$ is retained.  If it instead returns to $I=0$
with $R>0$, that is the upward terminal $U^\uparrow$, not a regenerated
base.  Thus every continuing outer state is genuinely one-species.  The
physical reserve $R$ is never replaced by a reaction counter.

The hypothesis $D_V>0$ is load-bearing and is not a restriction on the
global theorem.  If $D_V=0$ on the reachable marked lift, then

\[
                         V=H_V\le x_V^\circ.                         \tag{1.4}
\]

Thus such states form a finite class-dependent exception in a fixed-width
one-active tube.  Conversely, there are exactly twelve normalized
no-history supports (84 incidences on 28 pairs) for which every proper
source contains $I$ and every lower complex is $I$-free.  On their $I=0$
face the proper linkage is disabled forever and every enabled reaction has
$\Delta V=0$.  For example,

\[
             L_+=\{I,V+I\},\qquad L_0=\{0,U,2U\}.                  \tag{1.4a}
\]

Such a face can never carry reachable positive $D_V$.  The earlier
unqualified physical-start statement was false there: service has
probability zero.  These rows are therefore a vacuous branch of the local
positive-debt theorem, not recurrence counterexamples.

For definiteness use the logarithmically shrunken critical cutoff

\[
 L_n=\left\lfloor{n^{1/3}\over\log(n+e)}\right\rfloor.                \tag{1.5}
\]

Stop, including the boundary-causing physical reaction, when $U$, $I$,
or $R$ first reaches $L_n$.  This choice has the same tier exponent as
$n^{1/3}$: $L_n=n^{1/3+o(1)}$.  Its only purpose is to make

\[
                         {L_n^3\over n}=O((\log n)^{-3})=o(1),        \tag{1.6}
\]

which allows one stopping rule to handle every fixed polynomial order.  A
fixed cutoff $\rho n^{1/3}$ also works for any prescribed finite list of
orders after choosing $\rho$ sufficiently small.

## 2. Exact physical self loops and the correct trace

An **open excursion** begins when a reaction from a no-fast base has an
$I$-bearing target.  It ends at the first strict service, included return to
$I=0$, or physical boundary.  Direct reactions between $I$-free complexes
are already outer base moves.

At one raw base attempt split the exact-return subprobability kernel as

\[
                         Z_{x,x}=Z_x^{\rm pure}+Z_x^{\rm int}.       \tag{2.0}
\]

The pure part contains only repetitions of one safe $aU\to V+I$ opening
and its matching $V+I\to aU$ cleanup.  The interrupted part contains every
other exact physical return.  Both kernels include the probability of
selecting the opening reaction against every other base clock; neither is
conditional on having opened.  Decompose every nonself exit as follows:

- $Q_x^0,S_x^0,B_x^0$ are respectively the no-interruption continuing,
  strict-service, and included physical-boundary kernels.  Direct reactions
  between $I$-free complexes are in $Q_x^0$.
- $E_x^1,S_x^1,A_x^1,B_x^1$ are respectively the interrupted nonexact
  $I=R=0$ return, strict service, upward $I=0,R>0$ return, and physical
  boundary kernels.

The two exact diagonal parts and these seven exits are exhaustive.  In particular,
the future $Q_0$ base exit is present already at this raw renewal level.  At
the outer level first sum the pure class and put

\[
 R_x^{\rm int}=(I-Z_x^{\rm pure})^{-1}Z_x^{\rm int},\qquad
 R_x^K=(I-Z_x^{\rm pure})^{-1}K_x.                                 \tag{2.1a}
\]

Lemma 5.3 proves $\|R_x^{\rm int}\|=o(1)$ uniformly before the moving
boundary.  Only then sum the interrupted exact returns.  For every

\[
 K_x\in\{Q_x^0,S_x^0,B_x^0,E_x^1,S_x^1,A_x^1,B_x^1\},
\]

put

\[
 \widetilde K_x=(I-R_x^{\rm int})^{-1}R_x^K
                =(I-Z_{x,x})^{-1}K_x.                              \tag{2.1}
\]

This is ordinary renewal at one physical state.  It is not a quotient by an
auxiliary mark.  Equivalently, in the trace generator the diagonal rate is

\[
                         q(x,x){f(x)-f(x)}=0.                      \tag{2.2}
\]

Only exact equality of all physical populations is erased.  A return with a
different $U$ and $V=n$ remains in $\widetilde Q_x^0$ or
$\widetilde E_x^1$; a return with $V>n$ remains in $\widetilde A_x^1$ as
the upward terminal.  Strict service remains in $\widetilde S_x^0$ or
$\widetilde S_x^1$.  Every included boundary remains in
$\widetilde B_x^0$ or $\widetilde B_x^1$.  The
physical duration of every diagonal loop is accumulated; Section 7 treats
its moments.

The erasure in (2.1) is only a projection inside this descriptor-local
physical kernel.  It does **not** assert that a global reflected-debt lift
has returned to the same auxiliary mark: reflection may change such a mark
along a population-zero cycle.  No global mark is evolved through (2.1).
The local kernel stops or returns first in physical population space, and
only then is the adjacent global interface invoked.  This is compatible with
the common-potential gluing because $W_\ell$ depends only on physical
populations and is exactly unchanged by a completed physical self loop.
The physical stopping law and the $W_\ell$ increment are independent of the
incoming reflected-debt mark, so no mark corrector is inserted here.  The
all-debt lift uses finiteness of the reachable fiber over each fixed physical
population only for properness, not for a state-uniform constant.  Exact
cycles may therefore change the global mark without changing the same
physical $W_\ell$ increment or physical-time bound.

The two-stage form is analytically essential.  The algebraic last equality
in (2.1) alone would not control a diagonal kernel close to one.  The first
renewal sums the potentially dominant pure nested class, while the second
has norm $o(1)$ and is a genuine convergent perturbation.

This convention removes the frozen counterexample for the right reason.  In

\[
 L_+=\{2U,V+I\},\qquad L_0=\{0,I,2I,U+I\},                         \tag{2.3}
\]

any word made only of $2U\to V+I$ entries and $V+I\to2U$ cleanups, with
the same number of each, returns exactly to $(u,n,0)$.  Whether an entry was
the first or the hundredth has no physical meaning.  Formula (2.1) deletes
the completed pure word; an exact return containing a different slow edge
is retained in $Z^{\rm int}$ until its separate small-norm renewal is
performed.  Both stages retain elapsed time and every pre-return boundary
hit.  There is no multiplier $z$ at either endpoint.

## 3. The inner all-interruption estimate

We first control one open excursion, before any diagonal repetitions are
summed.  Call a firing **fast** when its source is $V+I$, and **slow**
otherwise.  Here “slow” includes a nested proper entry as well as a lower
linkage firing.  Let $N$ count slow firings after the excursion has opened;
$N$ is local and is discarded at its endpoint.

**Order of operations.**  The physical diagonal renewal (2.1) is performed
before any polynomial, factorial, entropy, or duration norm is taken.  The
inner calculation below is used to retain nonself, service, boundary, and
holding-time rewards; it never assigns a terminal weight to a completed
diagonal return.

### Lemma 3.1 (physical opened-excursion Feynman--Kac bound)

Fix $q\ge0$.  There are constants $z>1$, $1<a_I<a_R$, $D_q<\infty$,
$A_q\ge1$, $c_q>0$, and a bounded compact corrector $\kappa_q\ge0$ such
that, with

\[
 \phi_q(u)=D_q+(1+u)^q+\kappa_q(u),\qquad
 \Psi_q=A_qz^N a_I^I a_R^R\phi_q(U),                               \tag{3.1}
\]

the physical embedded chain of one open excursion satisfies, for all large
$n$,

\[
 K^{\rm in}_n\Psi_q+T^{\rm in}_nF_q+B^{\rm in}_nF_q
      +c_q K^{\rm in}_n\Psi_q\le\Psi_q.                            \tag{3.2}
\]

Here $K^{\rm in}_n$ is the nonterminal physical-step kernel,
$T^{\rm in}_n$ contains every included $I=0$ return (continuing or upward)
and every strict-service endpoint, which may have $I>0$;
$B^{\rm in}_n$ contains the included physical boundary endpoint, and

\[
                         F_q(U,I,R)=(1+U+I+R)^q.                    \tag{3.3}
\]

The same estimate with a standard holding-time augmentation gives every
fixed moment of the open-excursion duration from the bounded data used by
the outer construction.  Concretely, every base opening has $N=0$ and
$I+R\le2$; immediately after its first slow firing one has $N=1$ and
$I+R\le5$.  Uniformly for either of these admissible starting classes,

\[
 \begin{aligned}
 \mathbb E_{u,I,R}(1+U_T+I_T+R_T)^q
     &\le C_q(1+u)^q,\\
 \mathbb E_{u,I,R}T^q&\le C_q(1+u)^{c_q}.                          \tag{3.4}
 \end{aligned}
\]

No polynomial claim for an arbitrary initial $I,R<L_n$ is made; iteration
of (3.2) from such a state would retain the exponential proof mark in (3.1).

Moreover, if the excursion is opened from a base with bounded initial
$I,R$, the endpoint-weighted probability of at least one slow firing is

\[
 \mathbb E[ F_q(U_T,I_T,R_T);N\ge1]
       \le {C_q(1+u)^{q+2}\over n}.                                \tag{3.5}
\]

#### Proof

On the stopped region $V\ge n/2$ for all large $n$.  At $I\ge1$, the
sum of the outgoing $V+I$ clocks and the sum of all other clocks obey

\[
 \lambda_f\ge c nI,\qquad
 \lambda_s\le C(1+U+I)^2.                                          \tag{3.6}
\]

Choose $D_q$ so large that for the bounded physical $U$-jump $j$,

\[
 \beta_q:=\sup_{u,|j|\le2}{\phi_q((u+j)^+)\over\phi_q(u)}
       <{a_R\over a_I}.                                             \tag{3.7}
\]

Then choose $a_I,a_R,z$ close enough to one, in that order.  By (1.3), a
nonterminal fast step has mark ratio at most

\[
                         \beta_q{a_I\over a_R}=1-4\epsilon_q         \tag{3.8}
\]

for some $\epsilon_q>0$.  A slow step has a fixed maximum mark ratio
$M_q$, because every reaction vector is bounded.  From (1.5)--(3.6),

\[
 {\lambda_s\over\lambda_f}
 \le {C L_n^2\over nI}
 =O(n^{-1/3}(\log n)^{-2})/I=o(1).                                 \tag{3.9}
\]

Thus the slow contribution $M_q\lambda_s/(\lambda_f+\lambda_s)$ is
smaller than $\epsilon_q$ for all large $n$.  The ratio of the actual
bounded-jump terminal reward $F_q$ to
$z^Na_I^Ia_R^R\phi_q(U)$ is bounded by a constant $C_q^{\rm term}$.
Choose $A_q$ so that $C_q^{\rm term}/A_q\le\epsilon_q$ and then choose
$c_q>0$ so small that

\[
 (1+c_q)(1-3\epsilon_q)+\epsilon_q\le1.                            \tag{3.9a}
\]

Condition on the next reaction.  A nonterminal fast branch costs at most
$1-4\epsilon_q$, all slow branches together cost at most $\epsilon_q$, and
all terminal branches together cost at most $\epsilon_q$ after the choice
of $A_q$.  This convex branchwise comparison proves (3.2), including a fast
service at $R=0$.  Notice that $z^N$ is used only before $T$; the terminal
reward (3.3) contains no $N$.

Before the first slow firing, $R\le1$.  Hence there are at most two
nonterminal fast firings before an $I=0$ return or service.  At each such
state the slow/fast ratio is bounded by $C(1+u)^2/n$.  Stop at the first
slow firing and apply the same-order endpoint bound (3.2) from the
post-firing state, which has $N=1$ and $I+R\le5$.  This proves (3.5).
Iteration of (3.2) from either admissible class proves the endpoint part of
(3.4), because its initial $z^Na_I^Ia_R^R$ factor is then uniformly bounded.
Since the total clock in the open phase is at least (cn),
the same argument applied to the standard binomial expansion of accumulated
exponential holding times proves the duration statement.  No truncation of
$N$ occurs.  \(□\)

The asymmetry $a_I<a_R$ is load-bearing: it makes every nonterminal fast
step contract even when $I+R$ is constant.  The global $z^J$ which failed
in the frozen snapshot is absent.

## 4. The exceptional exact pair

The generic estimate (3.5), multiplied by a degree-two base opening rate,
looks like $O(U^4/n)$.  This is harmless for every fixed-cut proper support,
but not for (2.3), whose lower cut has degree zero.  Here the apparent leading
term is exactly diagonal and must be removed before comparison.

### Lemma 4.1 (first-defect estimate for (2.3))

For the exact pair (2.3), erase all completed histories made only of the
nested edge $2U\to V+I$ and the fast edge $V+I\to2U$.  Uniformly for
$u<L_n$, the remaining endpoint-weighted nonself rate is

\[
                         O((1+u)^3/n).                              \tag{4.1}
\]

The part which returns to a **continuing** (I=R=0) base with outer
spectator endpoint larger than (u) has rate

\[
                         O((1+u)^2/n).                              \tag{4.2}
\]

The probability that an erased attempt reaches the physical $I$- or
$R$-boundary before returning is superpolynomially small, even after all
degree-two base repetitions are summed.

#### Proof

After the first proper entry, and until a lower-linkage firing occurs, put
$k=I=R$.  A nested $2U\to V+I$ firing raises $k$ by one; a fast
$V+I\to2U$ firing lowers it by one.  Their rates are bounded above and below
by

\[
             \lambda_+(k)\le C(1+u)^2,\qquad
             \lambda_-(k)\ge cnk.                                  \tag{4.3}
\]

If the chain reaches $k=0$ without a lower-linkage firing, the complete
physical state is exactly the starting base.  Thus all of (4.3), including
arbitrarily many nested entries, belongs to the diagonal kernel in (2.1).

The lower support is $\{0,I,2I,U+I\}$.  At level $k\ge1$, the total
lower-linkage defect clock is at most

\[
                    C\{1+(1+u)k+k^2\}.                              \tag{4.4}
\]

The comparison birth--death chain from (4.3) visits level $k$ with weight
at most

\[
                  {1\over k!}\left({C(1+u)^2\over n}\right)^{k-1}.  \tag{4.5}
\]

Summing the defect/fast ratios from (4.4) against (4.5) gives

\[
 \mathbb P(\hbox{a lower defect before the exact return})
                       \le {C(1+u)\over n}.                          \tag{4.6}
\]

Multiplication by the degree-two base opening clock proves (4.1).  A
degree-one lower source is necessarily $U+I$, and every target in the
lower support has $U$-degree at most one.  Hence the **first defect edge**
cannot increase (U).  Every first defect edge which increases (U) is
sourced at (U)-degree zero; the same sum without the factor (1+u)
gives (4.2) for a one-defect continuing return.

There is a necessary terminal distinction.  The physical word

```text
2U -> V+I,   U+I -> 2I,   V+I -> 2U,   V+I -> 2U
```

sends

\[
(u,0,0)\to(u-2,1,1)\to(u-3,2,1)
\to(u-1,1,0)\to(u+1,0,-1).                        \tag{4.6a}
\]

Thus a leading degree-one defect can raise the terminal spectator by one,
but its last firing is strict service at (R=0); it is not an outward base
return and is never iterated by (E_n).  Its effective service rate can be
(O(U^3/n)).  If a degree-one first defect is instead to yield a positive
**continuing** base return, it needs at least one additional slow firing,
whose factor is (O((1+u)^2/n)=o(1)) on (1.5); this is covered by (4.2).
Finally,
(4.5) at $k=L_n$, multiplied by at most a polynomial number of
raw degree-two attempts, is smaller than $n^{-M}$ for every fixed $M$.
This retains, rather than erases, a boundary hit inside a would-be diagonal
loop.  \(□\)

This lemma identifies the exact missing factor in the frozen proof.  The
$O(U^4/n)$ event is not a marked outward transition: it is a completed
physical self loop.  A genuinely nonself event must contain a first lower
defect and has only the rate (4.1).

## 5. Structural cut lemma and analytic all-order bound

There are 146 generalized support templates.  Exactly 37 have a two-complex
proper linkage.  Twenty of those have no $I$-free proper source and hence
no proper self opening at a no-fast base.  The remaining seventeen are

| exact proper pair | number | maximal $I$-free lower-cut degree |
|---|---:|---|
| $\{0,V+I\}$ | 6 | five degree 2, one degree 1 |
| $\{U,V+I\}$ | 5 | five degree 2 |
| $\{2U,V+I\}$ | 6 | five degree 1, one degree 0 |

The last degree-zero row is exactly (2.3).  For each of the other five
${\{2U,V+I\}}$ rows, Lemma 4.1 with its lower support changed only improves
the estimate: nested degree-two entries are still exact self histories, a
nonself history has effective rate $O(U^3/n)$, and the lower cut has rate
of order $U$.  Its relative insertion probability is therefore

\[
                              O(U^2/n).                              \tag{5.1}
\]

For an exact $\{U,V+I\}$ or $\{0,V+I\}$ pair, the lower maximal cut has
degree at least one more than any dangerous repetition factor, and (5.1) is
again an upper bound.

There are 109 templates with a larger proper support.  For every enabled
${aU}$, the safe block $\{aU,V+I\}$ is then a proper subset of its linkage.
Strong connectivity forces a directed edge out of that block.  If its source
is $aU$, the cut edge and the self-opening edge have the same falling
factorial $(U)_{\underline a}$; if its source is $V+I$, the cut edge and
the cleanup edge have the same $VI$ propensity.  Consequently every safe
self attempt has a fixed positive probability of taking the cut, independent
of $u,v$.  There is no polynomial repetition factor.  Combining that cut
with (3.5) again gives (5.1).

These alternatives are exhaustive:

\[
 \begin{aligned}
 17\;\hbox{base-open exact}
 &+20\;\hbox{exact without a base proper source}\\
 &\quad+109\;\hbox{larger proper}=146.
 \end{aligned}                                                       \tag{5.2}
\]

The executable certificate checks (5.2), the three histograms in the table,
and uniqueness of (2.3).  The graph step itself is elementary: in a finite
strong digraph, every proper nonempty vertex set has an outgoing edge.

### Regression 5.1 (finite one-defect certificate; not a proof input)

The following frozen finite statement attacks the $k=1$ edge case of the
analytic Lemma 5.2 below.  It is retained for reproducibility but is not
used to infer any unbounded-order assertion.  After exact physical loops are
erased, every positive **continuing** base
return either loses at least one of the four possible $U$-source powers in
its opening/first-defect pair, or contains at least two post-opening slow
firings.  More precisely, consider a return with exactly one post-opening
slow firing.  Let $a,b\in\{0,1,2\}$ be the $U$-source degrees of the opening
and that firing, let $d$ be the maximal genuine outer cut/service degree
**after diagonal deletion**, and let $j>0$ be the returned spectator
increment.  For an exact pair $\{aU,V+I\}$, its degree-$a$ proper clock is
diagonal and $d$ is instead the maximal $I$-free degree in the lower
linkage; for every other support, $d$ is the maximal $I$-free degree over
both linkages.  Then

\[
 a+b\le3,\qquad j\le4,qquad
 \max\{a+b-d+\theta j\}=2+\theta<\tfrac52
       \quad(0<\theta<\tfrac12).                                  \tag{5.3}
\]

The maximum in (5.3) is over all such paths in all 146 support templates.
It is independent of the strong orientations.

#### Proof

Enlarge each linkage to the complete directed graph on its support.  Every
strong orientation is a subgraph, so it suffices to check this larger menu.
Starting just after an opening, allow exactly one further slow edge and only
$V+I$-source edges otherwise; stop at the first physical $I=0$ endpoint or
strict service.  The opening has $R\in\{0,1\}$, the slow edge can raise $R$
by at most one, and every fast edge lowers $R$ by one.  Hence there are at
most two fast edges and the primitive menu is finite.

The executable regression enumerates this menu directly in $(U,I,R)$,
including paths that would later be removed as exact loops, so it is an
overcount.  There are 1,308 positive continuing paths.  For
$r=a+b-d$, its exact $(r,j)$ histogram is

\[
\begin{aligned}
\begin{array}{c|rrrrrr}
(r,j)&(-2,1)&(-2,2)&(-2,3)&(-2,4)&(-1,1)&(-1,2)\\
\hline
\#&158&170&58&36&316&140
\end{array}\\[4pt]
\begin{array}{c|rrrrr}
(r,j)&(-1,3)&(0,1)&(0,2)&(1,1)&(2,1)\\
\hline
\#&20&238&98&73&1
\end{array}
\end{aligned}                                                       \tag{5.4}
\]

Its canonical path-ledger hash is

```text
07b3a03c77ce5d58c87130f6344e8dc6e36d92cf5f99a59b46603fd31144057f
```

The same regression freezes the denominator for all 37 exact pairs:

| exact proper pair | post-diagonal outer degree $d$ |
|---|---|
| $\{0,V+I\}$ | one $d=1$, five $d=2$ |
| $\{U,V+I\}$ | five $d=2$ |
| $\{2U,V+I\}$ | one $d=0$, five $d=1$ |
| $\{I,V+I\}$ | one $d=1$, six $d=2$ |
| $\{2I,V+I\}$ | one $d=1$, five $d=2$ |
| $\{U+I,V+I\}$ | one $d=1$, six $d=2$ |

For fixed positive rates, the embedded weight of one listed primitive is at
most $C(1+u)^r/n$: select its degree-$a$ opening against the degree-$d$
base clock, then select its degree-$b$ defect against the $nI$ fast clock.
The unique $(r,j)=(2,1)$ row is the exceptional word

```text
2U -> V+I,   I -> U+I,   V+I -> 2U,
```

whose denominator is the degree-zero lower cut, not the erased degree-two
diagonal opening.
Thus no positive one-defect path has $a=b=2$, and direct inspection of (5.4),
together with (7.10) of the frozen one-species lemma, gives the last equality
in (5.3).  A path outside this primitive menu has a second post-opening slow
firing.  Equation (4.6a) explains why the word ``continuing'' is essential:
positive terminal service endpoints are instead handled by the strict
three-weight gap below.  \(□\)

### Lemma 5.2 (coupled all-order ledger and interrupted diagonals)

Consider a service-free physical history from a no-fast base to its first
included no-fast return.  Write $e_0$ for the opening and
$e_1,\ldots,e_k$ for the post-opening slow firings.  If $s(e)$ is the
$U$-degree of the source of $e$, let

\[
                  r=\sum_{i=0}^k s(e_i)-d,                         \tag{5.5}
\]

where $d$ is the post-contraction outer escape degree from Section 5, and
let $j=U_{\rm end}-U_{\rm start}$.  Every nonpure service-free return obeys

\[
                       r+j\le2k+1.                                \tag{5.6}
\]

For a positive continuing return, $j\ge1$, and consequently

\[
        r\le2k,\qquad r+\theta j\le2k+\theta
                    \quad(0<\theta<1).                            \tag{5.7}
\]

Every interrupted exact return also obeys $r\le2k$.  No finite-depth path
list is used in any of these assertions.

No bound $r\le2k$ is asserted for a negative return.  It is false in the
exceptional support: the word

```text
2U -> V+I,   U+I -> I,   V+I -> 2U
```

has $k=1$, $r=3$, and $j=-1$.  It still satisfies (5.6), and because its
endpoint is smaller it belongs to the nonincreasing continuation kernel,
where no factorial endpoint penalty is paid.

#### Proof

Write $t(e)$ for the $U$-degree of a target.  Let $f_1,\ldots,f_h$ be the
fast firings.  Their source $V+I$ has $U$-degree zero.  Telescoping the
spectator increments gives the exact identity

\[
 r+j=\sum_{e\ {\mathrm{slow}}}t(e)
       +\sum_{e\ {\mathrm{fast}}}t(e)-d.                           \tag{5.8}
\]

Every slow firing whose target is $V+I$ creates one unit of reserve and has
$t(e)=0$.  At a continuing return it is paired with exactly one later fast
firing, whose target has $U$-degree at most two.  Every remaining slow
target is $V$-free and itself has $U$-degree at most two.  Thus the two sums
in (5.8) are at most $2(k+1)$.  If $d\ge1$, (5.6) follows immediately.  The
only $d=0$ support is (2.3).  A nonpure positive or interrupted-exact return
there must use a lower-linkage defect, and every lower target in
$\{0,I,2I,U+I\}$ has $U$-degree at most one.  This supplies the same strict
one-unit saving and proves (5.6).  If $j\ge1$, then

\[
 r+\theta j=(r+j)-(1-\theta)j
             \le2k+\theta,
\]

which proves (5.7) for positive returns.

It remains to prove the exact-return source bound.  If $d\ge2$, then
$s(e)\le2$ directly gives $r\le2(k+1)-d\le2k$.  If $d=1$ and every slow
source had degree two, every such source would be $2U$.  In a larger proper
support this would force post-contraction degree at least two.  In an exact
pair $\{2U,V+I\}$, every $2U$-sourced proper opening is pure, so an
interrupted return contains a lower slow source of degree at most one.
Again $r\le2k$.  Finally suppose $d=0$.  In (2.3), proper slow firings are
pure $2U\to V+I$ openings and lower slow sources have degree at most one.
An interrupted word contains a lower reaction.  It cannot contain exactly
one: after the pure openings and matching fast cleanups cancel
stoichiometrically, one nonzero lower edge cannot return the physical state
exactly.  Hence it has at least two lower firings, and replacing two
degree-two sources by degree-at-most-one sources gives $r\le2k$.  \(□\)

### Lemma 5.3 (all-orders physical race and diagonal renewal)

At every open state below the boundary,

\[
 \lambda_{\rm fast}\ge cnI,\qquad
 \lambda_{\rm slow}\le C(1+U+I)^2,
 \qquad q_n:=\sup{\lambda_{\rm slow}\over
              \lambda_{\rm fast}+\lambda_{\rm slow}}
       \le {CL_n^2\over n}.                                      \tag{5.9}
\]

Conditional on opening, if there are $k$ post-opening slow firings before a
service-free return, reserve conservation allows at most $k+1$ fast
firings.  There are at most $4^{k+1}$ binary slow/fast patterns.  Summing
the detailed reaction choices inside the total slow hazard therefore gives,
for a fixed constant $C_0$ and $C_0q_n<1$,

\[
 \mathbb P\{N\ge m\mid\hbox{opened}\}
       \le {C_0(C_0q_n)^m\over1-C_0q_n}.                           \tag{5.10}
\]

This sums every interruption order.  Now let $Z^{\rm pure}$ and
$Z^{\rm int}$ be the two diagonal kernels in (2.0).  The strong-cut
alternative preceding Regression 5.1 and finite compact transience give

\[
 {1\over1-Z^{\rm pure}(u)}\le
 \begin{cases}
 C,&\{aU,V+I\}\text{ is a proper subset of its linkage},\\
 C(1+u)^{2-d},&\text{the proper linkage is }\{aU,V+I\}.
 \end{cases}                                                       \tag{5.11}
\]

Indeed, in the first case a strong cut from the safe two-node block has a
fixed conditional probability per traversal.  In the second, the genuine
degree-$d$ base escape clock competes with a total base rate of order at
most $(1+u)^2$.  On the finitely many small bases, historical positive-debt
transience excludes a closed pure-only class and supplies the compact
constant.

Every interrupted exact return has $N\ge1$.  In the unique $d=0$ support
it has $N\ge2$, by the last paragraph of Lemma 5.2.  Combining (5.9)--(5.11)
requires the same occupation summation used for the factorial continuation
kernel; a bare binary race probability would omit residual $I$-source
factors.  With $x=1+u$, Lemma 5.2 and (6.8c1) below give, for $N=k$ and an
exact endpoint,

\[
 \begin{cases}
 C^kk^kx^{2k}/n^k,&k\le x,\\
 C^kk^{3k+2}/n^k,&x<k\le L_n.
 \end{cases}                                                       \tag{5.11a}
\]

The successive ratio in these finite-$k$ lines is at most
$CL_n^3/n=o(1)$.  For $k>L_n$, do not continue that occupation series;
use the raw all-orders race bound (5.10).  Since an exact-return kernel has
no endpoint weight and pure-renewal amplification is at most $CL_n^2$, its
tail is bounded by $CL_n^2(CL_n^2/n)^{L_n}$.  Consequently, in every
positive base weight (both diagonal kernels return the same base),

\[
 \begin{aligned}
 \left\|(I-Z^{\rm pure})^{-1}Z^{\rm int}\right\|
 &\le C\left\{{L_n^2/n\over1-CL_n^3/n}
             +n^{-1}+L_n^2(CL_n^2/n)^{L_n}\right\}\\
 &=O((\log n)^{-3})=o(1).                                       \tag{5.12}
 \end{aligned}
\]

Consequently the second inverse in (2.1) is a genuine Neumann series.  For
any nonnegative actual exit reward $F$,

\[
 \|(I-R^{\rm int})^{-1}R^KF\|
       \le {\|R^KF\|\over1-\|R^{\rm int}\|}.                     \tag{5.13}
\]

Thus actual service, upward, and included-boundary endpoints propagate
without alteration.  An internal boundary hit never enters a diagonal
kernel.  Additive first-moment rewards, including elapsed time, obey the
same renewal-reward identity.  Higher duration moments require the separate
pure-loop geometric holding-time estimate in Section 7 followed by the
binomial induction there; they are not inferred from (5.12).  \(□\)

## 6. The outer killed base resolvent

Let $Q_0$ be the no-interruption continuing base kernel after exact physical
diagonal returns are erased, stopped before $L_n$, and let $S_0,B_0$ be its
actual strict-service and included physical-boundary kernels.  This is the
stopped killed one-species kernel of Lemma 7.1 and (7.5) in the frozen note.
The no-interruption partition has no upward return: a proper entry followed
by its first fast cleanup has zero net $R$, while a fast firing after a lower
opening at $R=0$ is strict service.  The
counterexample to (7.16i) did not affect that lemma.  Here and below
$Q_0,S_0,B_0,E_n,T_n^1,B_n^1$ denote the renewed kernels from (2.1);
tildes are suppressed after diagonal deletion.  With $w_p(u)=(1+u)^p$,
the Green operator $G_0=(I-Q_0)^{-1}$ satisfies

\[
 \begin{aligned}
 G_0w_p(u)+G_0(S_0+B_0)w_p(u)&\le C_pw_{p+1}(u),\\
 G_0H_{\theta'}(u)+G_0(S_0+B_0)H_{\theta'}(u)&\le
                C_{\theta',\theta}H_\theta(u),\quad
        0<\theta'<\theta<\tfrac12,                                \tag{6.1}
 \end{aligned}
\]

where $H_\theta(u)=\exp\{\theta u\log(u+e)\}$.

Separating continuation occupation from the terminal payoff, the
maximal-source Foster calculation in the proof of the frozen Lemma 7.1 gives
the same-weight estimate

\[
                  G_0H_{\theta_0}(u)\le C_{\theta_0}H_{\theta_0}(u),
                  \qquad 0<\theta_0<\tfrac12.                     \tag{6.1a}
\]

Indeed, outside a compact set the degree-$d$ descending/killed cut has
probability bounded below, while every positive continuing contribution is
$O(u^{-1+2\theta_0})$; killed transience controls the compact set.  Only the
terminal kernel spends a weight gap, and (6.1) implies, for the fixed triple
in (6.8a),

\[
             G_0(S_0+B_0)H_{\theta_-}(u)\le C H_{\theta_0}(u).      \tag{6.1b}
\]

Its actual entropy endpoint also obeys

\[
 \mathbb E_u[B_\ell(U_D)-B_\ell(u)]
             \le C\log(u+e)+O(1).                                  \tag{6.2}
\]

Equation (6.2) uses the killed continuation $Q_0$, actual strict-service
kernel $S_0$, logarithmic boundary majorant, and bounded compact resolvent
corrector from (7.12)--(7.14b) of the frozen note.  No claim refuted by the
latest audit is imported.

Let $E_n$ be the positive kernel which records one **nonexact** interrupted
excursion and returns its actual physical endpoint to a continuing
$I=R=0$ no-fast base.  Its strict-service, upward-return, and
physical-boundary parts are retained separately in $S_n^1,A_n^1,B_n^1$;
put $T_n^1=S_n^1+A_n^1$.  Thus $E_n,T_n^1,B_n^1$ are an exhaustive
continuing/terminal/boundary partition after diagonal deletion.  The case
split of Sections 4--5 and Lemma 3.1 imply, for every fixed $p$,

\[
 (E_n+T_n^1+B_n^1)w_p(u)
       \le C_p e_n(u)w_p(u),                                        \tag{6.3}
\]

where, before the boundary,

\[
 e_n(u)\le
 \begin{cases}
 C(1+u)^3/n,&\text{the unique row (2.3)},\\
 C(1+u)^2/n,&\text{all other rows}.
 \end{cases}                                                       \tag{6.4}
\]

In the exceptional row $Q_0$ kills with probability bounded below at the
degree-zero cut, so it has a geometric Green bound with no extra $U$-power.
In every other row, the first line of (6.1), with $p$ raised by two, gives

\[
 \sup_{u<L_n}{G_0(e_nw_p)(u)\over w_p(u)}
       \le C_p{(1+L_n)^3\over n}
       =O_p((\log n)^{-3})=o(1).                                   \tag{6.5}
\]

The same display holds in the exceptional row by its geometric killing.
This is the missing outer perturbation estimate.  It is an estimate on
physical nonself endpoints, not on an artificial marked return.

With the usual action of kernels on endpoint functions, the complete killed
continuation resolvent is

\[
 \begin{aligned}
 G_n&=(I-Q_0-E_n)^{-1}\\
    &=\sum_{k\ge0}(G_0E_n)^kG_0 .                                  \tag{6.6}
 \end{aligned}
\]

Every actual continuing history occurs exactly once in this nonnegative
expansion: each factor $G_0E_n$ ends with one nonexact physical return, and
the following $G_0$ restarts at that return's actual spectator population.
By (6.5), (6.6) converges in every fixed polynomial endpoint norm.  It gives

\[
 \begin{aligned}
 \mathbb E_u(1+U_\sigma+I_\sigma+R_\sigma)^p
     &\le C_p(1+u)^{a_p},\\
 \mathbb E_u\sum_{b<\sigma}(1+U_b)^p
     &\le C_p(1+u)^{a_p}.                         \tag{6.7}
 \end{aligned}
\]

One may take $a_p=p+1$ after enlarging the finite-state corrector; its
precise value is irrelevant below.  More importantly, (6.6) sums every
finite number of interrupted excursions.  No remainder at “large $J$” is
present because $J$ is not a state variable.

For completeness, the factorial estimate also survives, but continuation
and terminal kernels must be separated.  Fix

\[
                  0<\theta_-<\theta_0<\theta_+<\tfrac12.             \tag{6.8a}
\]

First split the **continuing** kernel $E_n$ by whether its physical
$U$-endpoint is at most or greater than its start.  The nonincreasing part
has the same norm as (6.5).  For a one-defect increasing primitive, the
analytic $k=1$ case of Lemma 5.2 and

\[
              {H_{\theta_0}(u+j)\over H_{\theta_0}(u)}
                    \le C(1+u)^{\theta_0j},\qquad 0<j\le4,           \tag{6.8}
\]

give a weighted relative power at most $2+\theta_0$.  A history not in that
primitive menu contains at least two post-opening slow firings.  It is not
legitimate to charge an independent factor $L_n^{2\theta_0}$ for each one:
the intervening fast cleanup also changes the spectator.  Lemma 5.2 is the
needed coupled estimate.  Pairing each fast $V+I$ firing with the slow
firing that created its reserve unit gives, for every $k\ge1$ at once,

\[
        r+j\le2k+1,\qquad r+\theta_0j\le2k+\theta_0.               \tag{6.8b}
\]

Here $r$ already contains the single opening/outer-denominator factor and
all $k$ factors $n^{-1}$; no endpoint factor or fast cleanup is omitted.
More explicitly, comparison of each post-opening slow hazard with
$cnI$ gives a factor

\[
 {C(1+U)^{s(e)}(1+I)^{(i(e)-1)^+}\over n},                       \tag{6.8c}
\]

where $i(e)$ is the $I$-degree of its source.  The asymmetric inner
Feynman--Kac estimate sums the remaining $I$-powers and the finite reaction
branching.  It is not bounded merely by $C^k$: a $2I$-source contributes
one residual factor of $I$, and before the $m$-th slow firing reserve
$I$-source factors is bounded linearly, $I\le C(m+1)$: before that firing
there are only $O(m)$ slow and fast firings and every $I$-jump is bounded
by two.  Therefore the product of all residual
$I$-factors and the finite reaction branching is at most

\[
                         C^k k^k.                                 \tag{6.8c1}
\]

This is the exact all-order occupation cost; it is kept below rather than
silently absorbed into a constant.

The factorial ratio must be combined with the propensities at the actual
intermediate populations; replacing all of them independently by their
cutoff values would lose the outer denominator.  Split instead by $k$.
Put $x=1+u$.  Before a continuing return there are at most $k+1$ fast
firings, hence $U\le u+Ck$ throughout.  After the pure diagonal renewal, a
fixed reaction word has probability times endpoint weight at most

\[
 {C^k x^{s(e_0)-d}(x+Ck)^{\sum_{i=1}^ks(e_i)}k^k\over n^k}
 {H_{\theta_0}(u+j)\over H_{\theta_0}(u)}.                         \tag{6.8c2}
\]

This follows by applying (6.8c) at each slow firing; fast/slow patterns and
the finite channel choices are included in $C^k$.  If $x\ge Ck$, all
intermediate spectator populations are $O(x)$, and the bounded-reaction
factorial ratio plus (6.8b) turns (6.8c2) into

\[
                  {C^k k^k x^{2k+\theta_0}\over n^k}.             \tag{6.8d}
\]

If $x<Ck$, then $x+Ck=O(k)$.  Dropping the initial degree-$d$ denominator
costs at most $k^d$, where $d\le2$.  Equation (6.8b) bounds (6.8c2) by

\[
                 {C^k k^{3k+\theta_0+2}\over n^k}.                 \tag{6.8e}
\]

For $k\le L_n$, the successive-term ratio in either (6.8d) or (6.8e) is at
most a fixed multiple of $L_n^3/n=o(1)$.  Their sums are bounded by
$CL_n^{2+\theta_0}/n(1-CL_n^3/n)$ and $C/n$, respectively.  If
$k>L_n$, do not continue the occupation series (its successive ratio need
not remain small).  Instead, every continuing endpoint and every
preterminal state lies below $L_n$, so its factorial reward is at most
$H_{\theta_0}(L_n+C)$.  The raw all-orders race bound (5.10), multiplied by
the at-most-quadratic pure-renewal amplification, bounds this entire tail by
a polynomial multiple of

\[
 L_n^2(C L_n^2/n)^{L_n}H_{\theta_0}(L_n+C)
 =\exp\{-(1-\theta_0+o(1))L_n\log n/3\},                          \tag{6.8f}
\]

this tail is superpolynomial.  We have therefore proved, uniformly on
$U<L_n$, that the whole positive continuing kernel satisfies

\[
 \begin{aligned}
 {E_n^+H_{\theta_0}(u)\over H_{\theta_0}(u)}
 &\le {C L_n^{2+\theta_0}/n\over1-C L_n^3/n}
       +O(n^{-1})+O(n^{-M})                                      \tag{6.8g}
 \end{aligned}
\]

for every fixed $M$.  This is an all-orders analytic estimate.  The finite
ledger in Regression 5.1 is only a check of its $k=1$ boundary case.  Since
$L_n^3/n=o(1)$, (6.8g) tends to zero.  Applying the same-weight killed
Green estimate (6.1a) gives

\[
 \|G_0E_n^+\|_{H_{\theta_0}}
 \le {C L_n^{2+\theta_0}/n\over1-C L_n^3/n}
 =n^{-(1-\theta_0)/3+o(1)}=o(1).                                  \tag{6.9}
\]

Because $\theta_0<1/2$, the displayed exponent is strictly below
$-1/6+o(1)$.  Direct cofactor births have the additional $1/I$ factor from
(3.9), and Lemma 3.1 sums their level occupation factorially.  Consequently
every factor $G_0E_n$ in (6.6) acts on the same
$H_{\theta_0}$ space with norm $o(1)$; no $\theta$-gap is spent when the
number of interruptions increases.

The leading positive word (4.6a) belongs to the strict-service part $S_n^1$
of the terminal kernel, not to $E_n^+$.  It can have rate $O(U^3/n)$, so a
false same-weight bound must not be used.  Instead the strict terminal gap
for both strict service and upward return gives, after summing all local slow
orders by Lemma 3.1,

\[
 (T_n^1+B_n^1)H_{\theta_-}(u)
       \le C e_n(u)H_{\theta_0}(u).                                \tag{6.10}
\]

For completeness, reserve pairing at a terminal gives the analogue of
(6.8b) with at most one additional fast firing: for $j\ge0$,
$r+j\le2k+3$, while for $j<0$ the source bound is $r\le2k+2$.  Put
$x=1+u$ and $\Delta\theta=\theta_0-\theta_->0$.  In the region
$x\ge Ck$, the exact factorial ratio gives

\[
 {H_{\theta_-}(u+j)\over H_{\theta_0}(u)}
 \le C^k x^{\theta_-j}
       e^{-\Delta\theta\,u\log(u+e)}.                             \tag{6.10a}
\]

Together with $C^kk^k$ from (6.8c1), a fixed $k$ terminal contribution is
at most

\[
 {C^kk^kx^{2k+3}\over n^k}
 e^{-\Delta\theta\,u\log(u+e)}.                                  \tag{6.10b}
\]

The first term is $O(x^2/n)$ because
$x^3e^{-\Delta\theta u\log(u+e)}$ is bounded, and the successive ratio is
$CL_n^3/n=o(1)$.  If $x<Ck\le L_n$, the corresponding bound is
$C^kk^{3k+5}/n^k=O(n^{-1})$ after summation.  For $k>L_n$, use the same raw
race tail as (6.8f), with $H_{\theta_-}$; it is superpolynomial because
$\theta_-<1$.  These three estimates prove (6.10) for arbitrary terminal
jump accumulation, not only for a bounded one-defect word.  Thus service,
upward, and boundary pieces use the
three-weight gap and are never charged to the same-weight continuing norm.
The included physical boundary is treated at its last pre-boundary state.
Equations (6.6), (6.9), (6.10), and the unperturbed two-weight estimate then
give

\[
 G_n(S_0+B_0+T_n^1+B_n^1)H_{\theta_-}(u)
       \le C H_{\theta_+}(u).                                      \tag{6.11}
\]

This is the promised factorial, rather than finite-hierarchy, control.  The
three weights are fixed once; no gap is spent per interruption.

### Why (6.6) does not repeat the frozen error

The frozen series weighted every exact base return by $z$, so its diagonal
factor could approach one from above.  In (6.6), exact physical diagonals
have already been summed in (2.1) and contribute the identity endpoint.
Only a nonexact physical return appears in $E_n$, and its complete killed
Green norm tends to zero by (6.5).  Thus the Neumann parameter is a physical
nonself insertion probability, not a paid-reaction count.

## 7. Physical duration across erased loops

Erasing a diagonal endpoint does not erase elapsed time.  We now attach to
each term in (2.1) the sum of its physical holding times.  As in Section 6,
the exact diagonal kernel is summed first.  Only its accumulated physical
holding-time reward, never its reaction count or a marked endpoint, enters
the duration estimate.

Suppose the dominant exact-self opening at a base has source degree $a$
and the competing nonself/service cut has degree $d\le a$.  A raw base wait
has mean $O((1+u)^{-a})$, while the number of self attempts before the cut
has geometric moments of order $O((1+u)^{q(a-d)})$.  Their random sum has
all fixed moments bounded by a polynomial in $1+u$.  Each open cleanup has
mean $O(n^{-1})$; even in the exceptional row its expected accumulated
cleanup time is

\[
                         O((1+u)^2/n)=o(1)                           \tag{7.1}
\]

before the degree-zero cut.  Lemma 3.1 supplies the same assertion after a
nonexact interruption.

To pass from one macro to the whole outer episode, let $\eta$ be the elapsed
physical time of one fully renewed outer macro and let

\[
 M_jf(u)=\mathbb E_u[\eta^j f(U');\ \hbox{the macro continues}],
 \qquad b_j(u)=\mathbb E_u\eta^j.                                 \tag{7.1a}
\]

The pure-loop geometric calculation, Lemma 3.1, and the $o(1)$ interrupted
diagonal renewal give, for every fixed $j,p$,

\[
 M_jw_p(u)\le C_{j,p}w_{p+c_j}(u),\qquad
 b_j(u)\le C_jw_{c_j}(u),                                        \tag{7.1b}
\]

Here the second renewal is controlled with its time mark retained: augment
each term of the exact-return occupation series (5.11a) by its holding-time
moment of order at most $j$.  The physical open clock is at least $cn$ and
the base waits have the polynomial geometric bounds preceding (7.1a).
The multinomial convolution therefore changes only the polynomial exponent
and constant.  Induction through
$(I-R^{\rm int})^{-1}=\sum_{m\ge0}(R^{\rm int})^m$ proves (7.1b); an
unweighted $o(1)$ norm alone would not suffice.

With $w_p(u)=(1+u)^p$, let $K=Q_0+E_n$ be the full continuing base kernel,
$G_n=(I-K)^{-1}$, and $m_p(u)=\mathbb E_u\sigma^p$.  Expanding
$\sigma=\eta+\mathbf1_{\{\mathrm{continue}\}}\sigma'$ gives the exact
renewal recursion

\[
 m_p=G_n\left[b_p+\sum_{j=1}^{p-1}{p\choose j}M_jm_{p-j}\right].  \tag{7.1c}
\]

The convention $b_p=\mathbb E\eta^p$ is unconditional; it already includes
the $j=p$ contribution on continuing macros, which is why the sum in
(7.1c) stops at $p-1$.  Induction on $p$, using (6.5)--(6.7) and (7.1b),
yields for every fixed
$p$

\[
                         \mathbb E_u\sigma^p
                         \le C_p(1+u)^{b_p}.                         \tag{7.2}
\]

This additive-functional recursion is necessary: conditional Minkowski for
one geometric pure block alone would not control the total duration across
arbitrarily many nonexact outer returns.  The calculation uses competing
physical hazards and holding times and does not attempt to bound the number
of physical reactions in erased self loops; that count can be large near
the moving boundary.

## 8. Subpower starts, entropy, and the (1/3) boundary

At a historically consistent reachable positive-debt start
$u=n^{o(1)}$, (6.1), (6.4), and the
exceptional geometric cut give

\[
 \mathbb P_u\{\mathcal A_n\}
                  \le {C(1+u)^c\over n}=n^{-1+o(1)}.                 \tag{8.1}
\]

Here $\mathcal A_n$ means that at least one renewed interrupted kernel
$E_n$, $T_n^1$, or $B_n^1$ occurs before absorption; it includes interrupted
strict service, upward return, and boundary, not only a continuing return.

An exact diagonal return cannot change $V$.  A zero-interruption base
return also has zero net $V$-change.  Hence every service-free endpoint
with increased old-active population contains the nonexact insertion in
(8.1), and

\[
                         \mathbb P_u(U^\uparrow)\le n^{-1+o(1)}.    \tag{8.2}
\]

The killed base Green operator is transient, and the perturbed Neumann norm
in (6.5) is strictly below one.  Hence absorption in service,
$U^\uparrow$, or the included physical boundary has probability one.
Together with (8.2) and (8.4) below this gives

\[
                         \mathbb P_u(D)=1-o(1).                      \tag{8.2a}
\]

For every fixed $p$, the weighted versions of (6.3), followed through
(6.6), give the same-order rare-event bound

\[
 \mathbb E_u[(1+U_\sigma+I_\sigma+R_\sigma^+)^p;\mathcal A_n]
                         \le n^{-1+o(1)}.                           \tag{8.2b}
\]

This weighted statement, not a bare unconditioned polynomial moment, pays
the entropy.  Since $y\log(y+e)\le C_p(1+y)^p$ and
$R^+\log(n+L_n)$ bounds the positive reserve contribution to
$\log(V!)-\log(n!)$, (8.2b) makes the total positive $U$-, $I$-, and
reserve-entropy charge on $\mathcal A_n$ equal to
$n^{-1+o(1)}\log n=o(1)$.  The superpolynomial boundary event is handled
separately by (8.4) with $M$ enlarged.

On a zero-slow strict service, $V_\sigma=n-1$, while $I_\sigma$ and the
$U$-jump are uniformly bounded.  Its non-$V$ entropy cost is therefore
$O(\log(u+e))=o(\log n)$.  Combining these two cases with the actual
unperturbed spectator endpoint estimate (6.2) yields

\[
 \mathbb E_u[B_\ell(U_\sigma)-B_\ell(u)]
             \le C\log(u+e)+O(1)+o(1)=o(\log n).                    \tag{8.3}
\]

Here $B_\ell$ is only the spectator component.  For the full physical
$G_\ell$ in (8.6), the preceding split also gives

\[
 \mathbb E_u\!\left[G_\ell(X_\sigma)-G_\ell(x)
                    +\mathbf1_D\log n\right]=o(\log n).             \tag{8.3a}
\]

Indeed, strict service contributes
$\log((n-1)!)-\log(n!)=-\log n$ in the old-active coordinate; all remaining
$U,I,R$ terms were charged above.  This is the full entropy input to (8.7),
not a false pathwise weighted service inequality.

For any prescribed $M$, take a fixed polynomial order $p>3M$ in
(6.7).  Since the boundary-causing reaction is included and
$L_n=n^{1/3+o(1)}$,

\[
 \mathbb P_u\{U\vee I\vee R\ge L_n\}
       \le {C_p(1+u)^{a_p}\over L_n^p}
       =n^{-p/3+o(1)}=O(n^{-M}).                                  \tag{8.4}
\]

There is no $J$-boundary.  Split the included boundary path into two
disjoint events.  The **promotion event** $\mathcal P_n$ is path-labelled:
the cutoff is crossed by a direct outer-base reaction while no excursion is
open, and its included endpoint has $I=R=0$.  If the cutoff is first crossed
after an excursion has opened, that path belongs to $\mathcal B_n$ even if
a later cleanup would return to $I=R=0$.  Since the boundary-causing
reaction is included and reaction vectors are bounded,

\[
 L_n\le U\le L_n+C,\qquad V=n,\qquad I=R=0
                   \quad\hbox{on }\mathcal P_n.                    \tag{8.5}
\]

This, and only this, is the exact two-active weight $(1,3,0)$ handoff.
Let $\mathcal B_n$ contain every other included $U$-, $I$-, or $R$-boundary
endpoint.  Such an endpoint may occur inside an open excursion; for
example an opening $0\to U+I$ from $U=L_n-1$ reaches
$(U,I,R)=(L_n,1,0)$.  It is therefore false to identify all spectator
boundaries with (8.5).  The full $W_\ell$ cost of $\mathcal B_n$, including
the boundary-causing reaction, is already charged.  At a first included
boundary all of $U,I,R$ are at most $L_n+C$ and $V\le n+L_n+C$, so
$W_\ell(X_\sigma)\le Cn^4\log^4n$.  Choose the moment order in (8.4) so
that its probability is $O(n^{-M})$ with $M>5$; its expected positive
$W_\ell$ cost is then $o(1)$.  The global selector restarts from its actual
physical endpoint; no uncharged potential switch or fictitious return to
$I=0$ is used.

### 8.1 Compatibility with the hard-row proof

Sections 3--6 of the frozen hard-row theorem use only resistance exponents,
subpower multiplicative gaps, and the strict inequalities in their
$s_n^{1/8}$ boundary arithmetic.  At the promotion endpoint (8.5), put
$s_n=L_n$.
Then

\[
             V=n=s_n^{3+o(1)},\qquad U=s_n^{1+o(1)},\qquad I=0.       \tag{8.5a}
\]

The factor $(\log n)^3$ between $n$ and $L_n^3$ is $s_n^{o(1)}$.
Consequently every resistance class, the $m_-\le2$ bound, the raw
three-insertion exponent, the $s_n^{-1/4+o(1)}$ completed boundary bound,
and the final strict $-1/8$ comparison in Sections 3--6 are unchanged.
Their constants are uniform after this logarithmic refinement because all
rate comparisons there already allow arbitrary $s_n^{o(1)}$ factors.  No
statement or proof step in hard Sections 3--6 is replaced here; only the
incoming one-active scale is refined by a subpower factor.

Let

\[
 G_\ell(x)=K_\ell+\sum_j\log(x_j!)+\ell\cdot x,\qquad
 W_\ell=G_\ell^4.                                                     \tag{8.6}
\]

At strict service the $V$-factor contributes $-\log n+O(1)$.  The full
compensated estimate (8.3a) and $\mathbb P_u(D)=1-o(1)$ therefore give a
first-order mean decrement $-\log n+o(\log n)$, including all $U,I,R$
charges.  Equations (6.7), (7.2), (8.2b), and (8.4) give every fixed Taylor
remainder moment at the included endpoint, with rare large $I,R$ endpoints
kept on their endpoint-weighted event.  Thus the conditional fourth-power
calculation from the frozen Section 8 now has its missing hypotheses:

\[
 \mathbb E_x[W_\ell(X_\sigma)-W_\ell(x)+\sigma]
        \le -cG_\ell(x)^3\log n+o(G_\ell(x)^3\log n).                \tag{8.7}
\]

The same fixed $\ell$, $K_\ell$, and physical $W_\ell$ are used at the
one-active start and at the two-active handoff.  Neither the logarithmic
majorant in (6.2) nor any inner proof mark is added to $W_\ell$.

## 9. Rejected descriptor-local statement and claim boundary

The following was the intended replacement target.  The compact-spectator
counterexample stated in the status paragraph disproves it, so it is retained
only to identify the failed claim boundary.

> **Rejected candidate two-level generalized Family-II theorem.**  For every one of
> the 951 generalized one-active incidences, every pair of strong
> orientations, every positive fixed rate vector, and every historically
> consistent reachable marked one-active start (1.1) with $D_V>0$, the
> stopped physical kernel defined in Sections 1--2 has arbitrary fixed
> endpoint and duration moments, upward probability at most
> $n^{-1+o(1)}$, spectator entropy cost $o(\log n)$,
> superpolynomially small physical boundary probability at exponent $1/3$,
> and the common fourth-power drift (8.7).  On $\mathcal P_n$ its outer
> no-fast spectator boundary is the exact $(1,3,0)$ physical handoff; every
> open-excursion boundary is included, charged, and returned to the global
> common-$W_\ell$ selector at its actual endpoint.  If $D_V=0$, the state is
> in the finite class-dependent target alternative (1.4), so no service
> assertion is made or needed.

The quantifiers excluded from the statement are equally important.

- No global $J$ exists, and no finite $J$-cap is used.
- No exact physical self return is assigned a multiplier greater than one.
- No pathwise weighted-order descent at service is claimed.
- No uniform (O(1)) entropy endpoint is claimed for an unbounded spectator.
- No unweighted reaction-count bound is inferred from the physical-duration
  estimate.
- Sections 3--6 of the frozen hard-row theorem are not altered by this note.

Until an independent audit reproduces the operator construction, all of the
following remain false:

```text
analytic_theorem_independently_audited = false
descriptor_local_recurrence_certified  = false
pair_level_recurrence_certified        = false
global_t3_2_certified                  = false
pair_counts_promoted                   = 0
```

### 9.1 Required independent audit obligations

A passing audit must check the following load-bearing points separately;
replaying only the finite menu is insufficient.

1. Reconstruct the renewal (2.1) from raw physical histories.  Verify that
   only complete population-state diagonals are erased, while every internal
   $I$- or $R$-boundary hit and every physical holding time is retained.
   Verify separately that no equality of reflected-debt proof marks is used.
2. Prove Lemma 3.1 for every permitted reaction vector, including a nested
   proper entry counted as a slow firing, the actual service/upward/boundary
   endpoint, and all local interruption orders.  In particular, confirm that
   the inner endpoint estimate preserves polynomial order $q$, not $q+1$,
   from the bounded opening/post-first-slow classes stated before (3.4); no
   arbitrary-initial-$I,R$ polynomial conclusion may be imported.
3. Replay the exceptional birth--death comparison (4.3)--(4.6) with arbitrary
   positive fixed rates.  Check that the whole degree-two nested class is
   diagonal, that any nonself endpoint needs a first lower defect, and that a
   positive endpoint following a degree-one defect pays a second slow factor.
4. Prove the strong-cut alternative in Section 5 and the bounds
   (6.3)--(6.5) on the **contracted nonself** kernel.  Then check the
   placement of the operators in the nonnegative expansion (6.6), including
   all continuing, strict-service, upward-return, and physical-boundary
   kernels.  The finite support table may check the hypotheses but may not
   replace this argument.
5. Prove the coupled source/endpoint identity (5.7) and the all-$k$ bounds
   (5.5)--(5.6) directly from reserve pairing; the finite one-defect ledger
   is only a regression check and is not admissible as the proof.  Use that
   analytic invariant to verify both stages of diagonal renewal, the
   same-weight estimate (6.9), and the strict three-weight terminal estimate
   (6.10)--(6.11) for arbitrarily many slow firings.
6. Derive duration moments from competing physical hazards after diagonal
   renewal, not from reaction counts.  Recheck the $n^{-1+o(1)}$ first
   nonself insertion, endpoint-weighted full $U,I,R$ entropy split
   (8.2b)--(8.3a), $L_n=n^{1/3+o(1)}$ Markov bound, the split between exact
   no-fast promotion and charged open-excursion boundaries, and uniformity
   of frozen hard Sections 3--6 under the logarithmic scale refinement.

Any failure of one item leaves the analytic, pair, and global flags false.

## 10. Reproduction

Run the exact finite certificate and focused tests with

```bash
PYTHONPATH=src python3 -B src/two_active_dormant_407_two_level_repair.py
PYTHONPATH=src python3 -B -m unittest \
  tests/test_two_active_dormant_407_two_level_repair.py -v
```

The certificate rechecks the frozen failed hashes, the hostile exact return,
the complete support split (5.2), uniqueness of the exceptional template,
the complete positive-continuation path ledger (5.4), the absence of a
global paid mark, and all false certification flags.  These finite checks
support the analytic proof; they are not a substitute for its requested
independent audit.
