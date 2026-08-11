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
any support pair or T3-2. Independent audit found that Lemma 7.1 is false as
stated for unbounded spectator starts, and consequently Section 8 does not
yet close. A start-weighted Green estimate and revised workload accounting
are required. Accordingly,
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

Stop at $P$ when $I$, the accumulated nontrivial base displacement, or the
paid-interruption count first reaches $L_n$.  Include the boundary-causing
physical reaction in the endpoint.

With at most two paid interruptions the explicit phases in Sections 4 and
5 have bounded displacement, apart from the exceptional birth-death
coordinate already controlled by (5.5).  Below $L_n$, a binary lower
propensity contributes at most $CL_n^2$.  Three applications of (5.7) give,
for every fixed $r$,

$$
\mathbb E[(1+J+I+\tau_n)^r;P\text{ in one raw attempt}]
\le s_n^{-3+6/8+o(1)}. \tag{6.3}
$$

There are at most $s_n^{m_-+o(1)}\le s_n^{2+o(1)}$ attempts, so

$$
\mathbb P(P\text{ in the completed episode})
\le s_n^{-1/4+o(1)}. \tag{6.4}
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

The completed upward probability is one primitive order smaller.  The
$r>8$ endpoint estimate in (6.3) charges the included boundary jump and
gives

$$
\mathbb E[(\Delta W_\ell)^+;P]
\le s_n^{3q-1/8+o(1)}(\log s_n)^4, \tag{6.7}
$$

which is strictly below (6.6).

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

**Lemma 7.1 (killed one-species phase).**  Contract exact neutral self-loops
in the chain (7.1) and kill it on workload service.  From every historically
consistent positive-debt base, its killed Green kernel satisfies, for each
fixed $r$,

$$
\sup_n
\mathbb E\left[
\sum_{k<\sigma}(1+U_k)^r
\right]<\infty. \tag{7.2}
$$

The same statement holds with the factorial Foster weight

$$
H_\theta(u)=\exp\{\theta u\log(u+e)\} \tag{7.3}
$$

for sufficiently small fixed $\theta>0$.

**Audit failure.** The uniform assertion (7.2) is false when the historically
consistent spectator start depends on $n$. For

$$
L_+=\{U,I,V+I\},\qquad L_0=\{0,2U,U+I\},
$$

with complete strong digraphs, the physical history

$$
0\to U+I,\quad U\to V+I,\quad I\to U,\quad I\to U
$$

returns to $I=0$ with positive old-$V$ debt and $U=2$. Repeating the neutral
move $0\to2U$ yields historically consistent positive-debt bases with
$U=2+2k$. Choosing $U_n\asymp\log n$ makes the summand in (7.2) diverge.
Thus the proof below establishes at most a start-weighted factorial Green
bound; it does not establish (7.2) uniformly. The subsequent use of (7.6)
and the pathwise service assertion (8.6) must be replaced by a conditional
start-weighted expectation estimate. No network recurrence counterexample
is implied by this audit example.

To prove the lemma, decompose the finite neutral complex graph on
$\mathcal E$ into strongly connected components.  Consider the largest
enabled $U$-degree $d$ in a linkage.  There is only one $I$-free complex of
degree $d$.  If it lies in $L_0$, every nontrivial outgoing edge either
lowers $U$ or enters an $I$-bearing state and is killed by the fast service
mechanism.  If it lies in $L_+$, an edge through $V+I$ is neutral only when
the following top edge returns to the same degree-$d$ complex.  Strong
connectivity then forces a cut from this exact reverse block unless the
block is the whole proper linkage.  The cut either lowers $U$ at the same
degree-$d$ source order or gives service.  In the whole-linkage exception,
apply the same argument to the maximal enabled source of $L_0$.

It follows that, in any nontrivial closed service-free neutral component,
a negative population clock has the maximal mass-action order, while every
positive population jump is sourced at a lower degree.  The generator
applied to (7.3) is therefore strictly negative outside a fixed set.  A
singleton component consists only of exact zero-displacement loops; either
a strong-connectivity cut kills it geometrically, or it is a
history-free/frozen class and no positive old-active debt episode is
started there.  Transient components reach one of these alternatives after
a geometrically bounded number of component changes.  This proves (7.2)
and the factorial tail without selecting a reaction word.

This is the point at which arbitrary orientations matter.  The argument
uses only the maximal source degree and the directed cut forced by strong
connectivity; it does not assume a preferred cycle.

### 7.3 All-reaction perturbation and endpoint moments

During a top excursion with $I>0$, the dominant clock is
$\Theta(nI)$.  On a stopped set $U\le L$, the total lower clock is at most
$C(1+U+I)^2$.  The weighted Green estimate (7.2) therefore gives

$$
\left\lVert
G_n^{\mathrm{nf}}B_n
\right\rVert_{r\to r}
\le n^{-1+o(1)} \tag{7.4}
$$

for the operator that inserts a lower interruption into an uncleared top
excursion.  Expanding at the first such interruption is an exact
all-reaction resolvent identity with nonnegative coefficients, just as in
(5.8).

A zero-interruption return cannot increase $V$: a lower entry into $V+I$
adds one $V$, and return to $I=0$ requires a $V+I$ firing that removes it.
Thus an upward old-active return contains at least one operator $B_n$.
Equations (7.2)--(7.4) give a fixed conditional service probability and

$$
\mathbb P(U^\uparrow)\le n^{-1+o(1)}. \tag{7.5}
$$

Endpoint multiplication in the same resolvent gives

$$
\mathbb E[(1+U_\sigma+I_\sigma+R_\sigma)^r;E]
\le C_r\mathbb P(E) \tag{7.6}
$$

for every fixed $r$, hence for arbitrary $r>8$.  Exponential holding-time
moments and (7.2) also give every fixed moment of the physical duration,
uniformly $O(1)$ in $n$; fast top holding times are $O(n^{-1})$.

## 8. Moving spectator boundary and exact handoff

Set

$$
L_n=\lfloor n^{1/3}\rfloor. \tag{8.1}
$$

Stop the one-active kernel on workload service, an upward return, or the
first service-free neutral return to $I=0$ with $U\ge L_n$.  The stopping
time includes every physical firing in the boundary-causing macro.  Since
all reaction vectors are bounded, the overshoot is $O(1)$.

The factorial Foster estimate (7.3) gives constants $c,C>0$ such that

$$
\mathbb P(P\text{ before service})
\le C\exp\{-cL_n\log L_n\}. \tag{8.2}
$$

At the boundary,

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

Multiplying (8.4) by (8.2) shows

$$
\mathbb E[(\Delta W_\ell)^+;P]
=o(G_\ell(x)^3\log n). \tag{8.5}
$$

Thus no part of the entry jump or of the accumulated spectator displacement
is deferred or omitted.  It is charged by the first kernel under the same
$W_\ell$.

On a strict workload-service terminal, the weighted source order
$3v+u$ decreases by at least one.  Therefore

$$
\Delta\mathcal F_\ell
\le -c\log n+O(1), \tag{8.6}
$$

and the negative fourth-power contribution is
$-cG_\ell^3\log n$.  Equations (7.5), (7.6), and (8.5) make every positive
terminal lower order.  The physical duration is also lower order.  Hence

$$
\mathbb E_x[
W_\ell(X_{\sigma_n})-W_\ell(x)+\sigma_n]
\longrightarrow-\infty. \tag{8.7}
$$

Finally, the exact map of Section 2.3 identifies the endpoint of $P$ with
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
4. each of the 951 generalized Family-II one-active rows has a killed
   one-species no-fast resolvent with factorial endpoint tails and a charged
   spectator-promotion boundary; and
5. that boundary lands, including its entry macrojump, in the exact mapped
   hard $(1,3,0)$ row, so the two physical kernels compose under the same
   $W_\ell$.

Together with the existing exact-Family-II, direct-service, and
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
