# The unified dormant-interface priority and resolvent theorem

## 1. Scope and claim boundary

This note gives the analytic candidate for the two pieces of the hard
interface that were previously open:

1. the 407 dormant, no-wholly-top two-active incidences on 333 support
   pairs; and
2. the 951 generalized Family-II one-active incidences on the exact
   317-pair intersection.

The finite selectors, normalizations, and the exact one-active-to-two-active
promotion map are frozen in
src/two_active_dormant_407_certificate.py.  The finite certificate proves
only support identities and the premises of the graph argument.  It does not
infer a stochastic theorem from a finite box.

The candidate theorem is descriptor-local. It does not by itself certify
any support pair or T3-2. Independent audit found that the original uniform
form of Lemma 7.1 and the original pathwise argument in Section 8 were
false.  A first repair also incorrectly put the actual service endpoint
inside a uniformly negative entropy drift, and a second repair expanded
only through finitely many paid interruptions although their count is
unbounded.  Sections 6--8 now use a start-weighted Green estimate, a
logarithmic service-boundary majorant with a bounded compact corrector, a
full weighted Neumann sum over every paid-interruption order, and an
unweighted boundary charge.  This repair is pending independent re-audit.
Accordingly,
analytic_theorem_independently_audited,
pair_level_recurrence_certified, and global_t3_2_certified remain false.

## 2. Exact arithmetic

### 2.1 The two-active hard interface

There are

$$
407 \quad\text{incidences on}\quad 333 \quad\text{support pairs}. \tag{2.1}
$$

The incidence split is 369 positive-invariant and 38 signed rows.  The pair
union has 299 positive-invariant and 34 signed members.  The exact
fingerprints are

    incidences  ddd4c217b0236d7a44aa684873e6f6a9d5356c6741dea0d8575703e6263b7567
    pairs       d3c9dad6e8510a81efee6c56873de0f1f2cf6f24d3f50b46d4cf22abb2ad9484

Relabel the inactive species as $I$, the lower-weight active species as $U$,
and the higher-weight active species as $V$.  Every row has cap $I=0$,
one proper-top linkage $L_+$, and one linkage $L_0$ disjoint from the top.
Moreover,

$$
L_+\cap\mathcal T=\{V+I\}. \tag{2.2}
$$

The physical weight ratios are

$$
(1,2):37,\qquad (1,3):333,\qquad (4,5):37. \tag{2.3}
$$

Put

$$
\begin{aligned}
S_{12}=S_{45}&=\{0,U,I,2I,U+I\},\\
S_{13}&=S_{12}\cup\{2U\}.
\end{aligned} \tag{2.4}
$$

Every normalized row has

$$
L_+=\{V+I\}\cup P,\qquad L_0=Q,\qquad
P,Q\subseteq S_{pq},\qquad P\cap Q=\varnothing. \tag{2.5}
$$

There are 188 normalized ratio/support templates, split as
$17+154+17$.  After the ratio is forgotten there are 154 support templates.
The compact hashes are

    normalized physical rows
    dc15a6144dc604ef2e44e3b2da148281ce9a4f7dfc48f65818781cbf25373d04

    normalized templates
    fc0f8e9ced3824c5a6f8172e1f74775c61f1d001042a66c443ca8bae38611bcc

### 2.2 The complete one-active dimension on the 333 pairs

The same 333 pairs have 1,104 one-active failing incidences and 527 ordered
normalized profiles.  Their exact hashes are

    incidences
    a594c1f98a890ef17c255d90e765d655d45721c8dcf036be99651ea362a301fb

    classified rows
    ada26d0a37444e135bcab62dc97d9df116f0dec9c06f6bfd63c3244294b6dd0e

    profiles
    7b467db2167ac27b0420d6a1c8bba914fea0ff2379494a8f78bfd8fe1341584b

The exact classification is

| family | incidences |
|---|---:|
| generalized Family II | 951 |
| direct physical active-source service | 99 |
| exact Family II | 48 |
| open wholly-top | 6 |

The 951 generalized rows lie on exactly 317 pairs, with fingerprints

    generalized incidences
    8af9ed6aa8ba1661bacfe1390778b5677ee8d67cf1a606e042e5329e6ee86496

    generalized pair union
    0c8291a398cc981002c2164b643fbf75e1d107252beb9133fc3b4ad3af229c4a

The other 16 hard pairs are exactly the already classified exact-Family-II
pair union:

    3a552bf80f494f991e46ec3516d2a5c65a9de427f7d1a256eb2d918c12406879

Thus the exact pair arithmetic is

$$
333=317+16, \tag{2.6}
$$

with disjoint generalized-Family-II and exact-Family-II pair sets.  The 99
direct rows and six open-wholly-top rows occur on those same pairs and are
covered by their existing one-active graph predicates.

### 2.3 A common normalization and the exact promotion map

In a generalized one-active row, call the old active species $V$, the unique
inactive cofactor appearing in the sole top source $I$, and the other
inactive species $U$.  Thus $U$ is the spectator that can be promoted.  In
this normalization the supports are already of the form (2.5):

$$
L_+\cap\mathcal T=\{V+I\},\qquad I=0, \tag{2.7}
$$

and $L_0$ is lower-only.  The spectator cap is $0$, $1$, or $2$, with
exactly 317 rows at each cap.

There are 146 normalized support templates and 438
support-plus-spectator-cap templates.  Their hashes are

    normalized generalized rows
    725b014b571202c2970b333f865eee0762e83ce7a6d797d94f11f8f176536771

    support templates
    c2af132164aa2159478594a60378261d4d3956bbea1a61453b283995d27d2715

    support-plus-cap templates
    e16ecfc8c8f6300e21c5b58bfa813590c0c044eb5ced2eed85b1c3ff02e0cd49

Promote $U$ at relative weight one against weight three for $V$, while
retaining cap $I=0$.  Every one of the 951 rows maps to a hard
two-active $(1,3,0)$ incidence.  There are exactly 317 distinct targets,
one per pair and one for every three spectator caps.  The map and target
hashes are

    951-to-317 map
    2b34a3c828fa55a93a5595555f7dd5160e7a676338245bd0611809f399b4296f

    target incidences
    61be985100426fa5720254e5f95bb6ebce020b6f9198260a7e42596c41d047f4

    normalized target rows
    4fa439da6e1094cebfecf5d4042dc4cf5cd74a9ecaad7b7e01b8aa05c3568f59

The 317 targets have 146 normalized support templates, exactly the
generalized support menu above, and have resistance split

$$
m_-=0:305,\qquad m_-=1:10,\qquad m_-=2:2. \tag{2.8}
$$

The incidence identity is necessary for composition but is not the analytic
handoff.  Sections 7 and 8 prove that the boundary-causing physical macrojump
is included in the first stopped kernel, is charged by the same potential,
and ends at the state from which the mapped hard kernel starts.

## 3. Source-scale resistance for the hard rows

Fix one exact hard row.  Write its active weight as $(p,q)$ in the
$(U,V)$ order, where $p<q$, and let $x_n$ realize that tier.  After passing
to a subsequence there is a scale $s_n\to\infty$ such that

$$
x_{n,U}=s_n^{p+o(1)},\qquad x_{n,V}=s_n^{q+o(1)}. \tag{3.1}
$$

The $o(1)$ is retained throughout.  No claim of the form
$\log x_n=\lambda_nw+O(1)$ is used.

On $I=0$, the unique largest enabled source is

$$
M=U\quad\text{or}\quad M=2U. \tag{3.2}
$$

It is $U$ in 111 rows and $2U$ in 296 rows.  If $d_*$ is its $U$-degree,
then the base source clock has order $s_n^{pd_*+o(1)}$.  Once $I>0$, the
unique largest source is $V+I$, with clock
$s_n^{q+o(1)}I$.  The exact menu gives

$$
q-pd_*\ge 1. \tag{3.3}
$$

A reaction has zero resistance when it is sourced at $M$ on $I=0$, or at
$V+I$ on $I>0$.  Every other physical firing is a paid interruption.  Its
resistance is the loss of primitive source exponent from the largest
currently enabled source, and is at least one.

For a complex $y$, put

$$
h(y)=p\,u(y)+q\,v(y). \tag{3.4}
$$

Start an episode at $I=0$ with zero relative $h$-displacement.  Contract
only exact neutral returns.  Stop at:

- $D$, the first negative relative $h$-displacement;
- $U^\uparrow$, the first return to $I=0$ with positive displacement;
- $N$, a neutral return selected for regeneration; or
- $P$, the moving boundary of Section 6.

Let $m_-$ be the least aggregate resistance of $D$ after all neutral loops
are summed, and let $m_+$ be the corresponding least resistance of
$U^\uparrow$.

## 4. Arbitrary-orientation priority graph theorem

**Theorem 4.1 (hard dormant priority graph).**  For every one of the 407
incidences, every strongly connected orientation on each linkage support,
and every positive rate vector,

$$
0\le m_-\le 2,\qquad m_+\ge m_-+1. \tag{4.1}
$$

The physical incidence split is

$$
m_-=0:395,\qquad m_-=1:10,\qquad m_-=2:2, \tag{4.2}
$$

and the normalized-template split is $182+5+1$.

### 4.1 The 395 zero-resistance rows

The source $M$ is the unique maximal $I$-free complex in the network.  If
$M\in L_0$, every edge sourced at $M$ either descends strictly in $h$, or,
only for $M=U$, targets $U+I$ with equal $h$-weight.  The first case is
immediate service.  In the second case the next $V+I$ firing makes the
cumulative displacement negative.

If $M\in L_+$, the same argument applies unless the first edge is
$M\to V+I$.  A following $V+I$ edge either returns exactly to $M$, giving
an exact neutral block, or exits at weight at most $h(M)$.  A strict exit
is service.  The only equal exit is $U+I$ when $M=U$; it leaves $I>0$, so
the next $V+I$ firing is service.

Consequently the only service-free zero-resistance component is

$$
\{M,V+I\}. \tag{4.3}
$$

When (4.3) is a proper subset of $L_+$, strong connectivity supplies a cut
edge.  Outgoing reactions from one source have fixed positive relative
probabilities.  Exact neutral returns therefore have a geometric tail
before the cut is taken.  A zero-resistance return to $I=0$ is a
concatenation of exact reverse blocks and descending exits, so it cannot
have positive displacement.  The support certificate verifies that this
argument applies to exactly 395 rows.

### 4.2 The exceptional support

Equality in (4.3) occurs only for

$$
(p,q)=(1,3),\qquad L_+=\{2U,V+I\}. \tag{4.4}
$$

There are twelve physical rows, all positive-invariant, and their six other
supports are

$$
\begin{gathered}
\{0,U,I,2I\},\quad \{0,U,I,U+I\},\quad
\{0,U,2I,U+I\},\\
\{0,I,2I,U+I\},\quad \{U,I,2I,U+I\},\quad
\{0,U,I,2I,U+I\}.
\end{gathered} \tag{4.5}
$$

Strong connectivity forces both reactions in (4.4).  Before an $L_0$
reaction, the exact proper-chain identity is

$$
r(t)=I(t), \tag{4.6}
$$

where $r$ is relative $h$-displacement.  This follows because
$2U\to V+I$ changes both quantities by $+1$, and the reverse changes both
by $-1$.

If $U\in L_0$, every $U$-sourced exit is service, either immediately or
after the next proper death.  Its clock is one order below the $2U$ base
clock.  Hence $m_-=1$.  Through resistance one, proper births and deaths
cancel by (4.6), while every $U$ event is descending, so $m_+\ge2$.

If $U\notin L_0$, the support is forced to be

$$
L_0=\{0,I,2I,U+I\}. \tag{4.7}
$$

Strong connectivity forces a directed cut

$$
\{0,U+I\}\longrightarrow\{I,2I\}. \tag{4.8}
$$

If the cut is sourced at $0$, it fires at resistance two at the base.  If
it is sourced at $U+I$, first take a free proper excursion.  During that
excursion the $U+I$ clock has order $s_n^{1+o(1)}I$, while the proper death
clock has order $s_n^{3+o(1)}I$, again giving resistance two.  In either
case the following proper death is service.  Every other history through
resistance two is an exact proper cancellation or one of the two neutral
base macros.  Thus $m_-=2$ and $m_+\ge3$.

No Hamilton-cycle assumption is used anywhere in this proof.

## 5. All-reaction Green and killed-resolvent estimates

The graph theorem alone is not a probability estimate.  This section keeps
every reaction and sums every neutral loop.

### 5.1 Zero-order Green operators

For a nonexceptional row, before the first paid interruption the zero-order
phase has a finite state menu after exact neutral returns are contracted.
The cut argument gives a fixed positive service probability per visit.
Its killed Green operator is therefore geometrically bounded in every fixed
polynomial endpoint norm.

The exceptional phase (4.4) is different: it is countable, not a fixed
finite set.  At cofactor level $I=i$, the exact proper invariants give

$$
U=U_0-2i,\qquad V=V_0+i. \tag{5.1}
$$

The birth and death rates are

$$
\lambda_{n,i}=\kappa_+(U_0-2i)_{\underline{2}},\qquad
\mu_{n,i}=\kappa_-(V_0+i)i. \tag{5.2}
$$

This is an exact one-dimensional birth-death chain.  It is not literally
an immigration-death chain.  Until $i$ is a fixed fraction of $U_0$,

$$
\lambda_{n,i}\le s_n^{2+o(1)},\qquad
\mu_{n,i}\ge c\,s_n^{3+o(1)}i, \tag{5.3}
$$

and beyond that range the birth rate decreases.  Hence

$$
\frac{\lambda_{n,i}}{\mu_{n,i+1}}
\le \frac{C s_n^{-1+o(1)}}{i+1}. \tag{5.4}
$$

The explicit birth-death product gives, for every fixed $r$,

$$
\mathbb E[(1+I_{\max})^r]\le C_r,\qquad
\mathbb P(I_{\max}\ge k)
\le \frac{C^k s_n^{-(k-1)+o(1)}}{k!}. \tag{5.5}
$$

Polynomial size bias by any binary lower propensity preserves (5.5).
Thus the exceptional killed Green operator is bounded in factorially
weighted endpoint spaces, uniformly through every fixed moment order.  This
countable-state estimate replaces, rather than hides inside, the finite-menu
argument.  A union over the at most $s_n^{2+o(1)}$ regeneration attempts
preserves every fixed endpoint moment: the first finitely many cofactor
levels contribute constants, and the remaining product tail in (5.5)
beats the polynomial number of attempts.

### 5.2 Ordered physical expansion

Let $J$ count paid interruptions.  In a nonexceptional row, the states
reachable after $k\le2$ paid interruptions lie in a fixed finite menu after
neutral contraction.  In an exceptional row, retain the countable
birth-death coordinate and use (5.5).  Let $G^{(0)}_{n,k}$ denote the
corresponding zero-order killed Green operator.  In either case, for every
fixed endpoint order $r$,

$$
\lVert G^{(0)}_{n,k}\rVert_{r\to r}\le s_n^{o(1)},
\qquad k=0,1,2. \tag{5.6}
$$

If $B_{n,k}$ is the stopped multiplication operator for the next paid
source, source-scale separation and (5.5) give

$$
\lVert G^{(0)}_{n,k}B_{n,k}\rVert_{r\to r}
\le s_n^{-1+o(1)}. \tag{5.7}
$$

Write $A_{n,k}$ for termination before the next paid clock and $K_{n,k}$
for one paid physical firing followed by the zero-order resolvent.  The
strong Markov property gives the exact nonnegative expansion

$$
\begin{aligned}
\mathsf P_n={}&A_{n,0}+K_{n,0}A_{n,1}
+K_{n,0}K_{n,1}A_{n,2}\\
&+K_{n,0}K_{n,1}K_{n,2}\mathsf P_n^{[3]}.
\end{aligned} \tag{5.8}
$$

Every coefficient is a sum over physical histories.  Consequently an
up-history absent through resistance $m$ cannot be created by cancellation
or by neutral-loop resummation.  For every $\varepsilon>0$,

$$
\begin{aligned}
\mathbb P(D)&\ge c_\varepsilon
s_n^{-m_- -\varepsilon},\\
\mathbb P(U^\uparrow)&\le C_\varepsilon
s_n^{-(m_-+1)+\varepsilon}.
\end{aligned} \tag{5.9}
$$

On every nonboundary terminal $E\in\{D,U^\uparrow,N\}$, endpoint
multiplication in (5.8), together with (5.5), yields

$$
\mathbb E[(1+Z+R_E)^r;E]\le C_r\mathbb P(E) \tag{5.10}
$$

for every fixed $r$.  Here $Z$ is the inactive factorial cost and $R_E$ is
the active overshoot.  In particular, any fixed $r>8$ is available.

### 5.3 The only subpower-neutral macro pair

Only (4.7) has a nontrivial neutral base return at the same resistance as
service.  The two possible neutral macrojumps are

$$
\zeta=(3,-1,0),\qquad -\zeta=(-3,1,0) \tag{5.11}
$$

in $(U,V,I)$ coordinates.  For a fixed vector $\ell$, put

$$
g_n=\log\frac{x_{n,V}}{x_{n,U}^3}+c_\ell, \tag{5.12}
$$

where $c_\ell$ includes the two macro rate constants and
$\ell\cdot\zeta$.  The exact factorial identity gives

$$
\Delta_\zeta\mathcal F_\ell=-g_n+o(1),\qquad
\Delta_{-\zeta}\mathcal F_\ell=g_n+o(1), \tag{5.13}
$$

and the effective hazard ratio is

$$
\frac{\rho_{-\zeta,n}}{\rho_{\zeta,n}}
=C\frac{x_{n,U}^3}{x_{n,V}}\{1+o(1)\}
=\exp\{-g_n+O(1)\}. \tag{5.14}
$$

Indeed, proper excursions occur at rate $\Theta(U^2)$ and the integrated
chance that a $U+I$ clock beats the $V+I$ death clock is $\Theta(U/V)$.

If $g_n$ is bounded, the two macro hazards and the cut-service hazard are
comparable after passage to a subsequence.  The cut then gives a geometric
service time with moments of every order.  If $g_n\to+\infty$, the forward
macro has entropy reward $-g_n+o(g_n)$, while the positive reverse reward is
suppressed by $g_ne^{-g_n}=o(1)$.  If $g_n\to-\infty$, the reverse macro has
reward $-|g_n|+o(|g_n|)$, while the positive forward reward is suppressed by
$|g_n|e^{g_n}=o(1)$.  In the divergent cases, stop also on the
entropy-negative neutral direction.

This trichotomy supplies uniform endpoint moments in arbitrary subpower
gaps.  A fixed $\ell$ changes only the bounded threshold between the three
cases; it cannot reverse the conclusion.

### 5.4 Physical duration

For a nonexceptional row, a zero-order base wait has mean
$s_n^{-pd_*+o(1)}$, and the following $V+I$ wait is smaller.  The number of
neutral returns is geometric.  In an exceptional row, one proper
regeneration cycle has mean

$$
s_n^{-2+o(1)}. \tag{5.15}
$$

Repeating raw attempts until $D$, $U^\uparrow$, or $P$ takes
$s_n^{m_-+o(1)}$ cycles in expectation.  Hence

$$
\mathbb E\tau_n\le
\begin{cases}
s_n^{-pd_*+o(1)},&m_-=0,\\
s_n^{m_--2+o(1)},&m_-\in\{1,2\},
\end{cases}
\qquad \mathbb E\tau_n\le s_n^{o(1)}. \tag{5.16}
$$

The same argument with exponential holding-time moments gives every fixed
duration moment.  These are physical times, not embedded jump counts.

## 6. Hard-row moving boundary and common potential

For one arbitrary fixed $\ell\in\mathbb R^3$, choose $K_\ell$ so that

$$
G_\ell(x)=K_\ell+\sum_j\log(x_j!)+\ell\cdot x\ge1,
\qquad W_\ell(x)=G_\ell(x)^4. \tag{6.1}
$$

The same $\ell$ and the same $K_\ell$ are used in every adjacent descriptor.
For a hard row, set

$$
L_n=s_n^{1/8}. \tag{6.2}
$$

The reset convention is part of the stopping rule.  A raw block ends at
$D,U^\uparrow,P$, or an **exact physical-state** regeneration $N$.
Only at such an exact return are its paid-interruption count
$J^{\rm raw}$ and its local absolute-displacement mark $C^{\rm raw}$
reset.  Every nonexact neutral return remains in the same raw block.  The
only exception is the pair of macros $\pm\zeta$ in (5.11): those returns
are lifted to the macrochain of Section 5.3 and their absolute variation
$A$ is accumulated across the completed episode.  The mark $A$ is never
reset before $D,U^\uparrow$, or $P$.

Stop at $P$ when one of

$$
 I,\qquad J^{\rm raw},\qquad C^{\rm raw},\qquad A              \tag{6.2a}
$$

first reaches $L_n$.  Include the boundary-causing physical reaction in
the endpoint.  The support exhaustion in Section 4 shows that, through
resistance $m_-$, every neutral base return is an exact state return except
for (5.11).  A higher-resistance nonexact return is therefore retained in
the raw block and in $J^{\rm raw}$; it is not silently regenerated away.

With at most two paid interruptions the explicit phases in Sections 4 and
5 have bounded local displacement, apart from the exceptional
birth--death coordinate controlled by (5.5) and the macro pair controlled
by Section 5.3.  Their probabilities of reaching $L_n$ before a terminal
are superpolynomially small.  Below the marks in (6.2a), a binary lower
propensity, after its primitive source power has been factored out,
contributes at most $CL_n^2$.  Three stopped applications of (5.7), with
the continuation kernel bounded only by its total mass, therefore give the
valid **unweighted** estimate

$$
\mathbb P(P\text{ in one raw exact-regeneration block})
\le s_n^{-3+6/8+o(1)}.                              \tag{6.3}
$$

No all-$r$ endpoint-weighted version of (6.3) is asserted.  In particular,
three insertions alone would not justify multiplying its left side by an
arbitrary power of the cutoff.

The exact-regeneration block count has geometric moments and

$$
 \mathbb E N_{\rm raw}=s_n^{m_-+o(1)}.              \tag{6.3a}
$$

Thus a conditional union bound gives the contribution of (6.3) to the
completed episode.  Repetition of nonexact neutral blocks cannot evade
that union: it occurs only for (5.11), and the geometric-service/bounded-gap
case and the entropy-negative/divergent-gap case of Section 5.3 give a
superpolynomial bound for $A\ge L_n$.  Consequently

$$
\mathbb P(P\text{ in the completed episode})
\le s_n^{m_--3+6/8+o(1)}
\le s_n^{-1/4+o(1)}.                                \tag{6.4}
$$

At the base, $G_\ell=s_n^{q+o(1)}$.  A strict $h$-decrease gives

$$
\Delta\mathcal F_\ell\le-\log s_n+o(\log s_n). \tag{6.5}
$$

When the gap (5.12) is bounded, (5.9) and (5.10) yield

$$
\mathbb E[\Delta W_\ell;D]
\le -c\,s_n^{3q+o(1)}(\log s_n)^4. \tag{6.6}
$$

The completed upward probability is one primitive order smaller.  For the
boundary term no weighted Green assertion is needed.  Before the included
boundary jump, every paid vector contributes $O(J^{\rm raw})$, every
nonexact local return contributes $O(C^{\rm raw})$, and the exceptional
proper phase has active displacement $O(I)$.  The only displacement which
survives exact regeneration is the macro displacement recorded by $A$.
Bounded reaction vectors therefore give, pathwise at $P$,

$$
 |X_{P,U}-x_U|+|X_{P,V}-x_V|
 \le C(1+I+J^{\rm raw}+C^{\rm raw}+A)\le CL_n.      \tag{6.6a}
$$

Since $L_n=o(s_n^p)$, the factorial finite-difference identity and the
included boundary jump imply

$$
 |\Delta G_\ell|\le CL_n\log s_n,
 \qquad
 (\Delta W_\ell)^+
 \le C\{G_\ell^3L_n\log s_n+(L_n\log s_n)^4\}.     \tag{6.6b}
$$

Multiplying the deterministic bound (6.6b) by (6.4), and using
$m_-\le2$ and $L_n=s_n^{1/8}$, gives

$$
\begin{aligned}
\mathbb E[(\Delta W_\ell)^+;P]
&\le G_\ell^3\log s_n\,
 s_n^{m_--3+7/8+o(1)}+o(G_\ell^3\log s_n)\\
&\le s_n^{3q-1/8+o(1)}(\log s_n)^4,
\end{aligned}                                       \tag{6.7}
$$

which is strictly below (6.6).  The exponent $-1/8$ is the sum of the
worst completed boundary-probability exponent $-1/4$ and the deterministic
endpoint factor $+1/8$.

When $|g_n|\to\infty$, stop also on the entropy-negative macro from Section
5.3.  Its negative reward is

$$
-cG_\ell^3|g_n|, \tag{6.8}
$$

whereas the opposite positive reward is smaller by
$O(|g_n|e^{-|g_n|})$.  The probability of reaching the mark boundary before
the negative direction is exponentially small in $L_n\min(1,|g_n|)$.
This estimate treats even sublogarithmic divergent gaps and is stronger
than a polynomial boundary comparison.

Combining (5.16) with these estimates gives

$$
\mathbb E_x[
W_\ell(X_{\tau_n})-W_\ell(x)+\tau_n]\longrightarrow-\infty. \tag{6.9}
$$

## 7. Generalized Family-II all-reaction resolvent

Fix one of the 951 generalized rows in the common normalization of Section
2.3.  Let $n=x_V\to\infty$, initially $I=0$, and let $U$ be the spectator.
The only $V$-containing source is $V+I$.

### 7.1 Contracted no-fast phase

On $I=0$, every physical source is lower and has $U$-degree at most two.
A service-free zero-order history is either

1. a direct lower reaction between $I$-free complexes; or
2. a lower reaction into $V+I$, followed by exactly one $V+I$ reaction
   returning to $I=0$ with zero net $V$ displacement.

After these exact neutral macros are contracted, the remaining population
coordinate is a one-species mass-action chain on the complex menu

$$
\mathcal E=\{0,U,2U\}. \tag{7.1}
$$

Every other top excursion is service: after the first top firing, either
$I=0$, or a second $V+I$ firing lowers the old active workload.  A lower
reaction interrupting an uncleared top excursion is retained as a paid
physical event.

### 7.2 One-species Green lemma

Write $u$ for the spectator population at the initial no-fast base; it is
not replaced by its cap label.  In particular, cap $2$ permits $u$ to
diverge subpolynomially along a one-active tier.

**Lemma 7.1 (start-weighted killed one-species phase).**  Contract exact
zero-displacement macros in (7.1), and let $\sigma_0$ be the first workload
service.  For every historically consistent positive-debt base, every
fixed $r$, and constants depending on the fixed support, orientation, and
rates but not on $u$ or the old-active level,

$$
 \mathbb E_u\left[
   \sum_{k<\sigma_0}(1+U_k)^r+(1+U_{\sigma_0})^r
 \right]
 \le C_r(1+u)^{r+1}.                               \tag{7.2}
$$

For

$$
 H_\theta(u)=\exp\{\theta u\log(u+e)\},            \tag{7.3}
$$

and $0<\theta'<\theta<1/2$,

$$
 \mathbb E_u\left[
   \sum_{k<\sigma_0}H_{\theta'}(U_k)
   +H_{\theta'}(U_{\sigma_0})
 \right]
 \le C_{\theta',\theta}H_\theta(u).                \tag{7.4}
$$

Consequently, for $L>u+4$,

$$
 \mathbb P_u\{\max_{k\le\sigma_0}U_k\ge L\}
 \le C{H_\theta(u)\over H_{\theta'}(L-4)}.         \tag{7.5}
$$

The start weight is necessary.  For

$$
 L_+=\{U,I,V+I\},\qquad L_0=\{0,2U,U+I\},          \tag{7.6}
$$

with complete strong digraphs, the physical history

$$
 0\to U+I,\quad U\to V+I,\quad I\to U,\quad I\to U
                                                                    \tag{7.7}
$$

returns to $I=0$ with positive old-$V$ debt and $U=2$.  Repeating
$0\to2U$ gives historically consistent bases $U=2+2k$.  Thus the old
claim $\sup_n\mathbb E\sum(1+U_k)^r<\infty$ was false.  This is a
counterexample to that quantifier, not to recurrence.

To prove the corrected lemma, retain the actual service endpoint and
write every contracted base transition as

$$
 a\longrightarrow b\quad\hbox{at rate }c_{ab}(u)_{\underline a},
 \qquad a,b\in\{0,1,2\},                            \tag{7.8}
$$

or as a service mark at rate $c_{a\dagger}(u)_{\underline a}$.  Here a
proper macro $aU\to V+I\to bU$ is included in $c_{ab}$; the common
$V+I$ source makes its exit probabilities independent of the old-active
level.  Exact $a=b$ macros have already been contracted.

Let $d$ be the largest source degree among the remaining nontrivial macros
and service marks.  There is one $I$-free complex of degree $d$.  If it is
in $L_0$, strong connectivity forces a nonself edge either to a smaller
$I$-free degree or to an $I$-bearing state, which gives service at the next
fast firing.  If it is in $L_+$, apply the same cut argument to the safe
block $\{dU,V+I\}$.  A cut lowers the base population at source order $d$
or gives service.  If the block is the whole proper linkage, move to the
maximal $I$-free source of $L_0$.  The exact support exhaustion has
seventeen such proper pairs,

$$
 \{0,V+I\}:6,\qquad \{U,V+I\}:5,\qquad
 \{2U,V+I\}:6,                                      \tag{7.9}
$$

and every one has an $I$-free source in $L_0$.  Hence the second cut is
always available.

It follows that a negative or killed transition has source degree $d$,
while every positive transition has source degree at most $d-1$.  For a
bounded jump $j$,

$$
 {H_\theta(u+j)\over H_\theta(u)}=O(u^{\theta j}). \tag{7.10}
$$

After division by the total contracted rate, the negative/killed clock
has probability bounded below, whereas all positive contributions to the
$H_\theta$ drift are $O(u^{-1+2\theta})$.  Thus the embedded kernel
contracts $H_\theta$ outside a finite set when $\theta<1/2$.  Applied to
$(1+u)^{r+1}$, the same calculation gives drift at most
$-c(1+u)^r$.  This proves (7.2)--(7.5) once the finite set is killed
transiently.

There is no hidden singleton exception.  Any positive-debt no-fast return
ends at an $I$-free target $bU$ which is enabled at its endpoint.  A
directed path in its linkage from $bU$ to an $I$-bearing complex supplies
service.  If no such path exists, the interruption which allegedly
created positive old-active debt could not have returned to that class.
Thus an exact-zero singleton is either killed by a directed cut or is a
frozen/no-history class.  It is never an initial state of the lemma.  The
killed Green matrix on the remaining finite set is transient, uniformly
after first entrance, and completes the Foster proof for arbitrary strong
orientations.

The same calculation supplies the weaker entropy estimate actually needed
below.  For the arbitrary fixed common vector $\ell$, put

$$
 B_\ell(u)=\log(u!)+\ell_Uu.                        \tag{7.11}
$$

An $O(1)$ bound with the actual service endpoint inside the one-step drift
is false.  Indeed, take

$$
 L_+=\{2U,V+I\},\qquad L_0=\{0,I,2I,U+I\}.          \tag{7.11a}
$$

Orient the proper pair in both directions and orient the lower linkage by
the strong cycle $0\to I\to2I\to U+I\to0$.  After the exact proper
self-macro is contracted, the lower firing $0\to I$ followed by the fast
service $V+I\to2U$ sends the base coordinate $u$ to the actual service
endpoint $u+2$.  Consequently

$$
 B_\ell(u+2)-B_\ell(u)
 =\log((u+1)(u+2))+2\ell_U
 =2\log u+O(1).                                     \tag{7.11b}
$$

This refutes the previous assertion that the service-including drift is
negative outside a compact set.  It does not refute the killed Green
estimate: this transition is the terminal workload service itself.

Keep the actual endpoint and pay exactly this logarithmic loss.  Let $Q$
be the substochastic continuation kernel before service and let $S$ be the
terminal service kernel, including the actual spectator coordinate after
the service macro.  Put

$$
 L(u)=\log(u+e),\qquad h_C(u)=B_\ell(u)+C L(u).      \tag{7.12}
$$

For $C$ sufficiently large, the maximal-source cut used above gives

$$
 Qh_C(u)+SB_\ell(u)-h_C(u)<0                       \tag{7.13}
$$

outside a finite set.  Here is the complete large-$u$ comparison.  Every
contracted jump is bounded.  If a degree-$d$ service mark is present, its
actual endpoint contributes at most $j_*\log(u+e)+O(1)$ to $B_\ell$, while
the absence of the $CL$ term at the service boundary contributes
$-C\log(u+e)$.  Its normalized probability is bounded below, so choosing
$C>j_*$ dominates this endpoint cost.  If there is no degree-$d$ service
mark, the cut supplies a degree-$d$ descending continuation, whose
$B_\ell$ increment is $-c\log(u+e)+O(1)$.  Every positive continuation or
service mark then has source degree at most $d-1$, so its total normalized
contribution is only $O(u^{-1}\log(u+e))$.  Mixed maximal-degree service
and descent only strengthens the same inequality.  For $d=0$ there is no
positive lower-degree transition.  These alternatives are exhaustive by
the cut proof preceding (7.10).

Let

$$
 g(u)=\bigl[Qh_C(u)+SB_\ell(u)-h_C(u)\bigr]_+.
$$

By (7.13), $g$ has finite support.  The finite-set killed transience gives
the bounded resolvent corrector

$$
 \chi(u)=\mathbb E_u\sum_{k<\sigma_0}g(U_k),
 \qquad \chi=g+Q\chi,qquad \|\chi\|_\infty<\infty. \tag{7.14}
$$

Consequently

$$
 Q(h_C+\chi)+SB_\ell-(h_C+\chi)
 =Qh_C+SB_\ell-h_C-g\le0.                          \tag{7.14a}
$$

Iteration keeps the exact terminal payoff $B_\ell(U_{\sigma_0})$ and gives

$$
 \mathbb E_u[B_\ell(U_{\sigma_0})-B_\ell(u)]
 \le C\log(u+e)+\|\chi\|_\infty.                  \tag{7.14b}
$$

The logarithmic majorant and bounded function $\chi$ are only proof
correctors.  Neither is added to $G_\ell$ or $W_\ell$; the actual physical
endpoint, common potential, and exact seam telescoping are unchanged.

### 7.3 All-reaction perturbation and endpoint moments

During a top excursion with $I>0$, the dominant clock is
$\Theta(nI)$.  Along a one-active tier the initial spectator is

$$
 u=u_n=n^{o(1)};                                    \tag{7.15}
$$

this, rather than a uniform bound in $u$, is the exact tier input.  Set

$$
 L_n=\lfloor n^{1/3}\rfloor.                       \tag{7.15a}
$$

Let $J$ count **all** paid lower firings, not a fixed truncation.  Before
the first old-active service put

$$
 R=V-n.                                             \tag{7.15b0}
$$

This is a nonnegative reserve, not an abstract debt mark.  The only
$V$-bearing complex is $V+I$.  Consequently a lower firing whose source is
not $V+I$ cannot decrease $R$ and can raise it by at most one, whereas
every $V+I$ firing lowers $R$ by one.  If such a fast firing occurs at
$R=0$, it is the terminal old-active service.  At a service endpoint we
set the stopped proof mark $R_\sigma=0$; at an upward endpoint it is the
actual active overshoot $V_\sigma-n$.

Stop at the auxiliary boundary $B_n$ if $I$, $J$, or $R$ first reaches
$L_n$, or if $U$ reaches $L_n$ anywhere other than the exact service-free
base return used for the promotion boundary $P_n$ in Section 8.  Include
the boundary-causing physical firing.  Until $B_n\cup P_n$,

$$
 U,I,J,R\le L_n+O(1).                              \tag{7.15b}
$$

There is a useful exact clock bound which does not require a false
linear-source assertion.  The finite support menu has molecularity at most
two.  It actually contains quadratic $I$-increasing paid edges, for example
$2U\to2I$ in

$$
 L_+=\{U,I,V+I\},\qquad L_0=\{0,2U,2I\}.           \tag{7.15c}
$$

The lower strong cycle $0\to2U\to2I\to0$ contains the quadratic birth
explicitly.  Exhausting the 146 support templates gives 705 possible
ordered $I$-increasing lower edges, 253 of them with quadratic source.
Thus the claim that every $I$-increasing paid source has
molecularity at most one would be false.  The true uniform estimates are
sufficient.  If
$\lambda_f$ is the total $V+I$ clock, $\lambda_p$ the total paid lower
clock, and $\lambda_+$ its $I$-increasing part, then
$V=n+O(R)\ge n/2$ on the stopped region for all large $n$.  Hence, for
$I\ge1$,

$$
\begin{aligned}
 \lambda_f&\ge c nI,\\
 \lambda_p&\le C(1+U+I)^2,\\
 \lambda_+&\le C\{(1+U)^2+(1+U)I\}.
\end{aligned}                                                   \tag{7.15d}
$$

Consequently, throughout (7.15b),

$$
 {\lambda_p\over\lambda_f}\le Cn^{-1/3},\qquad
 {\lambda_+\over\lambda_f}
 \le {Cn^{-1/3}\over I}.                           \tag{7.15e}
$$

The second inequality uses $I\le L_n$: the extra $n^{-2/3}$ term from
$(1+U)I/(nI)$ is at most $n^{-1/3}/I$.  It gives a factorial cost for
successive cofactor increases even though quadratic birth edges exist.

We now sum the full ordered expansion.  Let $\tau_1$ be the first paid
firing and let $\sigma$ be the terminal or auxiliary stop.  Compensation
and (7.2), with a sufficiently high but fixed polynomial weight, give

$$
\begin{aligned}
 \mathbb P_u(\tau_1<\sigma)&\le {C(1+u)^a\over n},\\
 \mathbb E_u[(1+U_{\tau_1})^{r+1};\tau_1<\sigma]
 &\le {C_r(1+u)^{b_r}\over n}.
\end{aligned}                                                   \tag{7.16}
$$

This retains the decisive first-event factor $n^{-1+o(1)}$.  It is not
replaced by the weaker uniform bound in (7.15e).  Before $\tau_1$, a
zero-paid top excursion has uniformly bounded $I$ and $R$, and the first
paid reaction vector is bounded.  Thus the second line of (7.16) also
controls every fixed mark used below at the state just after $\tau_1$.

The continuation estimate is made on a hybrid skeleton; it is not a
pointwise clock estimate pasted onto a whole-phase kernel.  At
$(I,R)=(0,0)$, contract only the zero-paid neutral entry/cleanup macros of
Lemma 7.1.  As soon as $I>0$, expose every physical firing until service,
an exact neutral base return, or a boundary.  In particular, every
**nonterminal** fast firing has

$$
 \Delta R=-1,\qquad \Delta I\le1,                 \tag{7.16a}
$$

and a fast firing from $R=0$ belongs to the terminal kernel.

Here is the marked inequality on that skeleton.  Fix $r$ and let $j_*$
bound one physical $U$-jump.  Let $\kappa_r\ge0$ be the bounded resolvent
corrector supplied by the finite-set part of the base cut calculation and
put

$$
 \phi_r(u)=D_r+(1+u)^{r+1}+\kappa_r(u).           \tag{7.16b}
$$

Enlarge $D_r$ after the corrector is added.  Then

$$
 \sup_{u\ge0,\ |j|\le j_*}
 {\phi_r((u+j)^+)\over\phi_r(u)}\downarrow1
 \quad\hbox{as }D_r\uparrow\infty.               \tag{7.16c}
$$

Choose fixed numbers

$$
 1<z_0<z_1,\qquad 1<a_I<a_R,                      \tag{7.16d}
$$

all sufficiently close to one, and $D_r$ sufficiently large, so that for
some $\varepsilon>0$

$$
 {a_I\over a_R}
 \sup_{u,|j|\le j_*}{\phi_r((u+j)^+)\over\phi_r(u)}
 \le1-4\varepsilon.                               \tag{7.16e}
$$

The choices are made in this order: first make the jump ratio in
(7.16c) close to one, next choose $a_R/a_I$ across that ratio, and finally
take $a_I-1$ and $z_1-1$ still smaller.  Thus an opened zero-paid service
mark, which has a uniformly bounded cofactor, retains a fixed fraction of
the killed base drift, while every paid mark multiplier remains as close
to one as required below.

This asymmetric choice is essential.  For example, in the exact template
$L_+=\{0,I,2I,V+I\}$, $L_0=\{U,2U\}$, orient
$0\to I\to V+I\to2I\to0$ and $U\leftrightarrow2U$.  After $k$ paid
$I\to V+I$ firings, successive zero-paid $V+I\to2I$ firings send
$(I,R)=(1+t,k-t)$.  Thus the previously used symmetric mark
$a_0^{I+R}$ is constant for $k$ physical steps and has no strict drift.
It is withdrawn.

Let $\mathcal K_n$ denote one continuation step of the hybrid skeleton and
$\mathcal S_n$ its terminal kernel, including the boundary-causing
physical firing.  For a fixed large constant $A_r$, define the interior
mark and the **actual terminal reward** by

$$
\begin{aligned}
 \Psi_r(U,I,J,R)&=A_r z_1^J a_I^I a_R^R\phi_r(U),\\
 \Phi_r(U,I,J,R)&=z_0^J(1+U+I+R)^r.
\end{aligned}                                                   \tag{7.16f}
$$

The reward $\Phi_r$ is evaluated at the physical terminal endpoint, not
at the state before service.  Exponential gaps in $J,I,R$, the extra
power in $\phi_r$, and then $A_r$ make every bounded terminal jump satisfy
the required comparison with $\Psi_r$.

We verify the two pieces separately.  At $I>0$, (7.15e) says that the
next firing is paid with probability at most $Cn^{-1/3}$.  On a
nonterminal fast firing, (7.16a) and (7.16e) give a continuation-mark ratio
at most $1-4\varepsilon$.  The constant $A_r$ is chosen so that the actual
$\Phi_r$ reward of every fast terminal step is at most
$(1-4\varepsilon)\Psi_r$; this includes the service firing from $R=0$.
A paid firing has a fixed mark multiplier
$m_*$, because all reaction vectors are bounded.  Hence, for all large
$n$, the physical top-step kernel obeys

$$
 \mathcal K_n^{\rm top}\Psi_r+
 \mathcal S_n^{\rm top}\Phi_r
 \varepsilon\Psi_r\le\Psi_r.                     \tag{7.16g}
$$

At $(I,R)=(0,0)$ use the contracted kernel of Lemma 7.1.  A zero-paid
neutral entry creates one unit each of $I$ and $R$, and its fast cleanup
removes both; their asymmetric marks cancel exactly, leaving the same
contracted $U$-transition as in Lemma 7.1.  A zero-paid service mark is
opened one physical step early when necessary.  It enters with $R=0$ and
bounded $I$, so the ordered choice after (7.16e), followed by (7.16g),
retains the maximal-degree killing in the proof of (7.2).  During either
opened macro, the chance of a paid firing before the fast cleanup or
service is at most
$C(1+U)^2/n$.  Relative to the negative
$-c(1+U)^r$ base drift, its mark-only and bounded-$U$-jump errors are,
respectively,

$$
 C(m_*-1){(1+U)^3\over n}(1+U)^r,
 \qquad
 C{(1+U)^2\over n}(1+U)^r.                        \tag{7.16h}
$$

On $U\le L_n$, the two displayed ratios are at most
$C(m_*-1)$ and $Cn^{-1/3}$.  The parameters in (7.16d) can be chosen close
enough to one that the first is smaller than one quarter of the base
drift; the second is $o(1)$.  The bounded compact corrector already folded
into $\phi_r$ handles the remaining states.  This comparison also covers
the apparent loss of a killed macro.  On a neutral macro, the unmarked
continuation value is already present in the contracted kernel, so only
the mark excess and the bounded $U$-difference in (7.16h) are new.  On a
service macro, replacing the fast service by a paid continuation loses at
most $C(1+U)^2/n$ of a killing term of order $\phi_r(U)$; this is
$O(n^{-1/3})$ relative to that same maximal-degree killing.  Thus the
contracted base piece and (7.16g) combine to the genuine physical-step
Foster--Feynman--Kac inequality

$$
 \mathcal K_n\Psi_r+\mathcal S_n\Phi_r
 +c_r\!\left[
   {\bf1}_{\{I=0\}}z_1^J(1+U)^r
   +{\bf1}_{\{I>0\}}\Psi_r
 \right]
 \le\Psi_r.                                       \tag{7.16i}
$$

There is no cap on $J$ in (7.16i), and the actual service, upward, and
boundary endpoints all occur in $\mathcal S_n\Phi_r$.

For completeness, the exact ordered history expansion is

$$
 \mathsf P_n=A_{n,0}
 +K_{n,0}\sum_{k=0}^{\infty}K_n^kA_n.             \tag{7.16j}
$$

Here $K_{n,0}$ is the first paid operator, $K_n$ every subsequent paid
operator, and $A_{n,0},A_n$ terminate before the next paid clock.  No small
norm is asserted for an entire zero-paid return phase.  Instead, iterate
(7.16i) from the state immediately after $\tau_1$ and use (7.16).  This
justifies the series and gives

$$
 \sum_{k\ge1}z_0^{k-1}
 \mathbb E_u[(1+U_\sigma+I_\sigma+R_\sigma)^r;J=k]
 \le {C_r(1+u)^{b_r}\over n}.                      \tag{7.16k}
$$

Thus no remainder with $J\ge3$, or with any other fixed value of $J$, is
discarded.  In particular,

$$
\begin{aligned}
 \mathbb P_u(J\ge k)
 &\le {C(1+u)^a\over n}z_0^{-(k-1)},\\
 I_{\max}+R_{\max}
 &\le r_*(1+J)\quad\hbox{before termination}.
\end{aligned}                                                   \tag{7.16l}
$$

The deterministic inequality is exact: $R$ starts at zero, a zero-paid
entry creates at most one reserve unit, only a paid firing can create
another, and every nonterminal fast firing consumes one.  A paid firing
changes $I$ by a bounded amount, while every fast increase of $I$ consumes
one of those reserve units.  Thus total $I,J,R$ have exponential tails.
The sharper $1/I$ bound in (7.15e) additionally gives the factorial factor
$(Cn^{-1/3})^{(k-1)_+}/(k-1)_+!$ after the first paid event for histories
with $k$ record-setting **paid** cofactor births.  Fast cofactor increases
are instead charged to the reserve they consume.  That refinement is not needed
below.  Applying (7.16i) also before $\tau_1$ and using (7.16k) on
$\{J\ge1\}$ proves for every fixed $r$ that

$$
\begin{aligned}
 \mathbb E_u[(1+U_\sigma+I_\sigma+J+R_\sigma)^r]
   &\le C_r(1+u)^{a_r}=n^{o(1)},\\
 \mathbb E_u[(1+U_\sigma+I_\sigma+J+R_\sigma)^r;
                 U^\uparrow]
   &\le {C_r(1+u)^{a_r}\over n}=n^{-1+o(1)}.
\end{aligned}                                                   \tag{7.17}
$$

A zero-paid return cannot increase $V$: entry into $V+I$ adds one $V$,
and a return to $I=0$ uses a $V+I$ firing which removes it.  Hence an upward
old-active return contains $K_{n,0}$, and the all-order bound (7.16k)
preserves the first $n^{-1}$ in the second line of (7.17).

The same sum proves the physical-duration statement.  If $T_j$ is the
duration of the $j$th zero-paid block, its fixed moments satisfy the same
weighted Green bounds.  The inequality

$$
 \left(\sum_{j=0}^{J}T_j\right)^r
 \le (J+1)^{r-1}\sum_{j=0}^{J}T_j^r
$$

and the exponential $J$ moment in (7.16k)--(7.16l), together with the
occupation term in (7.16i), imply

$$
 \mathbb E_u\sigma^r\le C_r(1+u)^{a_r}=n^{o(1)}.   \tag{7.17a}
$$

Finally extend $h_C+\chi$ to each top phase by its zero-order
harmonic interpolation, using $B_\ell$ at an actual service boundary; call
the extension $\widehat h$.  A paid physical firing has positive
$\widehat h$ increment at most $C\log n$ before the boundary.  The first
insertion estimate and the full series, not a finite hierarchy, give

$$
\begin{aligned}
 \mathbb E_u\sum_{j\le J}(\Delta_j\widehat h)^+
 &\le {C(1+u)^a\log n\over n}
       \sum_{k\ge1}kz_0^{-(k-1)}\\
 &=n^{-1+o(1)}\log n=o(1).
\end{aligned}                                       \tag{7.18}
$$

Apply (7.14a) at every zero-paid block.  Since
$h_C+\chi\ge B_\ell$ at a nonservice stop and actual service uses the
terminal payoff $B_\ell$, (7.18) yields

$$
 \mathbb E_u[B_\ell(U_\sigma)-B_\ell(u)]
 \le C\log(u+e)+\|\chi\|_\infty+o(1),
 \qquad
 \mathbb P_u(U^\uparrow)=n^{-1+o(1)}.              \tag{7.19}
$$

No raw uniform $O(1)$ entropy-endpoint, polynomial-endpoint, or duration
claim is made for an unbounded spectator start.  Since $u=n^{o(1)}$,
$\log(u+e)=o(\log n)$; this is exactly the loss allowed in Section 8.

## 8. Moving spectator boundary and exact handoff

Keep $L_n$ from (7.15a).  Stop the one-active kernel on workload service
$D$, an upward return $U^\uparrow$, the first service-free neutral return
$P_n$ to $I=0$ with $U\ge L_n$, or the auxiliary boundary $B_n$ of
Section 7.3.  Every stopping rule includes its boundary-causing physical
firing.  Since all reaction vectors are bounded, each overshoot is $O(1)$.

For $u=u_n=n^{o(1)}$, use (7.17) with an arbitrarily large fixed
polynomial order $q$.  Because the boundary-causing firing is included,
$U_\sigma\ge L_n$ on $P_n$ and on the $U$-part of $B_n$.  Write their
union as $\partial_n^U$.  For every prescribed $M$, choose $q>3M$;
Markov's inequality gives

$$
 \mathbb P_u(\partial_n^U)
 \le {C_q(1+u)^{a_q}\over L_n^q}
 =n^{-q/3+o(1)}=O(n^{-M}).                         \tag{8.2}
$$

The same actual-terminal reward in (7.16f), rather than a pre-boundary
state, gives

$$
 \mathbb P_u(B_n\text{ through }I,J,\text{ or }R)
 \le {C_q(1+u)^{a_q}\over L_n^q}=O(n^{-M}).        \tag{8.2a}
$$

These are all-reaction estimates: paths with arbitrarily large finite $J$
have already been summed.  The exponential $J,I,R$ tails in (7.16l) are
stronger for those three marks, but are not needed for the fourth-power
boundary charge.

On the promotion boundary $P_n$,

$$
U=n^{1/3+o(1)},\qquad V=n^{1+o(1)},\qquad I=0. \tag{8.3}
$$

Writing $s=n^{1/3}$, this is exactly the two-active weight
$(1,3,0)$.  The boundary endpoint, including its entry macro, obeys

$$
(\Delta W_\ell)^+
\le C G_\ell(x)^3 L_n\log n
+C(L_n\log n)^4. \tag{8.4}
$$

The same deterministic bound holds on $B_n$, because every coordinate,
the reserve mark, and the paid-event count are at most $CL_n$ after the
included boundary jump.
Multiplying (8.4) by (8.2)--(8.2a) shows

$$
\mathbb E[(\Delta W_\ell)^+;P_n\cup B_n]
=o(G_\ell(x)^3\log n). \tag{8.5}
$$

Thus no part of the entry jump or of the accumulated spectator displacement
is deferred or omitted.  It is charged by the first kernel under the same
$W_\ell$.  Only $P_n$ is used for the exact hard-row handoff; $B_n$ is an
auxiliary event whose full positive cost is already negligible in (8.5).

There is no pathwise weighted-order descent at service.  In the support
pair (7.6), with complete strong digraphs, the service path

$$
 0\to2U,\qquad 0\to U+I,\qquad V+I\to U            \tag{8.5a}
$$

takes $(U,I,\Delta V)$ from $(0,0,0)$ to $(4,0,-1)$, and hence

$$
 \Delta(3V+U)=1.                                   \tag{8.5b}
$$

Longer neutral spectator excursions can also make the raw factorial
increment positive on an individual service path.  Thus neither
$3v+u$ nor $\mathcal F_\ell$ is used pathwise here.

Instead set

$$
 Y_n=G_\ell(X_{\sigma_n})-G_\ell(x).               \tag{8.5c}
$$

On a zero-interruption service, the first strict old-active descent has
$V=n-1$ and contributes $-\log n+O(1)$.  A positive old-active endpoint
contains a paid interruption and is controlled by the second line of
(7.17); a promotion endpoint is neutral in $V$.  Equations (7.14a),
(7.18), (7.19), and (8.2)--(8.5) control the entire spectator entropy in
expectation, including the actual service endpoint and starts
$u_n\to\infty$.  Its positive contribution is
$O(\log(u_n+e))=o(\log n)$.  The cofactor endpoint is bounded in the
zero-interruption phase and has event-weighted polynomial moments after an
interruption.  Therefore

$$
 \mathbb E Y_n
 \le-\mathbb P(D)\log n+O(\log(u_n+e))
       +n^{-1+o(1)}\log n
 \le-\tfrac12\log n,                               \tag{8.6}
$$

Indeed, the service probability follows explicitly from
$$
 \mathbb P(D)=1-\mathbb P(U^\uparrow)
                -\mathbb P(P_n)-\mathbb P(B_n)=1-o(1),          \tag{8.6a}
$$

where (7.17), (8.2), and (8.2a) bound the three subtracted terms.  For the
three remaining Taylor orders, on a nonboundary endpoint and $j\le4$,

$$
 |Y_n|^j\le C_j\left\{
 (1+I_\sigma+R_\sigma)^{2j}(\log n)^{2j}
 +(U_\sigma\log(U_\sigma+e))^j
 +(u\log(u+e))^j+1\right\}.                        \tag{8.6b}
$$

The endpoint estimate (7.17) is available with an exponent $r>8$, and
$(z\log(z+e))^j\le C_j(1+z)^{2j}$.  The boundary contribution is smaller
than every power by the deterministic bound (8.4) and the probabilities
(8.2)--(8.2a).  Therefore the full, untruncated
all-reaction kernel satisfies
$$
 \mathbb E|Y_n|^j=n^{o(1)},\qquad j=2,3,4.          \tag{8.6c}
$$

Since $u=n^{o(1)}$ and $I=0$ initially,
$G_\ell(x)=(1+o(1))n\log n$.  The exact fourth-power identity now gives

$$
\begin{aligned}
\mathbb E[W_\ell(X_{\sigma_n})-W_\ell(x)]
={}&4G_\ell(x)^3\mathbb EY_n
 +6G_\ell(x)^2\mathbb EY_n^2\\
&+4G_\ell(x)\mathbb EY_n^3+\mathbb EY_n^4\\
\le{}&-cG_\ell(x)^3\log n.
\end{aligned}                                       \tag{8.6d}
$$

The duration bound $n^{o(1)}$ from Section 7.3 is lower order.  Hence

$$
\mathbb E_x[
W_\ell(X_{\sigma_n})-W_\ell(x)+\sigma_n]
\longrightarrow-\infty. \tag{8.7}
$$

Finally, the exact map of Section 2.3 identifies the endpoint of $P_n$ with
one of the 317 hard dormant targets.  The second kernel starts at that same
physical state, with the same rate vector, $\ell$, $K_\ell$, and
$W_\ell$.  Consequently the two increments telescope exactly:

$$
\bigl(W_\ell(X_{\sigma_n})-W_\ell(x)\bigr)
+\bigl(W_\ell(X_{\tau_n})-W_\ell(X_{\sigma_n})\bigr)
=W_\ell(X_{\tau_n})-W_\ell(x). \tag{8.8}
$$

There is no change of potential, no finite-box inference, and no uncharged
boundary comparison at the one-active-to-two-active seam.

## 9. Candidate unified interface theorem

**Theorem 9.1 (candidate, pending independent analytic audit).**  For every
positive rate vector and every strongly connected orientation on the two
linkage supports:

1. each of the exact 407 dormant two-active incidences has aggregate service
   resistance $m_-\le2$ and upward resistance at least $m_-+1$;
2. its all-reaction killed resolvent has endpoint and physical-duration
   moments of every fixed order, including an arbitrary exponent $r>8$;
3. its moving-boundary remainder is lower order for the one common
   fourth-power factorial entropy $W_\ell$, for arbitrary fixed $\ell$;
4. each of the 951 generalized Family-II one-active rows has a
   start-weighted killed one-species resolvent, polynomial moments
   $n^{o(1)}$ along every one-active tier, a logarithmic service-boundary
   majorant with bounded compact corrector, an
   $O(\log(u+e))=o(\log n)$ actual endpoint charge, and a charged
   spectator-promotion boundary; all paid-interruption orders are summed by
   the physical-step inequality (7.16f)--(7.16i) and its iteration
   (7.16k); and
5. that boundary lands, including its entry macrojump, in the exact mapped
   hard $(1,3,0)$ row, so the two physical kernels compose under the same
   $W_\ell$.

The false uniform Green, service-including uniformly negative entropy
drift, finite-$J$ truncation, linear-only cofactor-birth premise, symmetric
$a_0^{I+R}$ strict drift, pathwise $3V+U$, and weighted all-$r$
three-insertion statements have all been withdrawn explicitly; none is a
premise of this repaired theorem.
Together with the existing
exact-Family-II, direct-service, and
open-wholly-top one-active predicates, item 4 covers the one-active
dimension on all 333 hard pairs.  This still does not set a pair-level or
global recurrence flag: an independent audit of Sections 4--8 and the
separate all-active/global composition are required.

## 10. Reproduction

Run

    PYTHONPATH=src python3 -B src/two_active_dormant_407_certificate.py

and

    PYTHONPATH=src python3 -B -m unittest \
      tests/test_two_active_dormant_407_certificate.py -v

The executable checks the exact selectors, all normalized support
identities, the resistance partition, the complete one-active arithmetic,
and the 951-to-317 promotion map.  It deliberately keeps all analytic,
pair-level, and global certification flags false pending independent audit.
