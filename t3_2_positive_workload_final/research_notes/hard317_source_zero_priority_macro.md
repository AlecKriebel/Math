# Exact-proper priority trace and the cofactor-envelope coboundary

**Proof-first repair note, 2026-08-11 PDT.**  This note treats the singular
exact-proper bases

\[
                 L_+=\{aU,V+I\},\qquad a\in\{0,1\},                \tag{1.1}
\]

which are missed by the degree-only pure-renewal estimate in the current
hard-317 candidate.  The main family has \(a=0\) and six possible lower
supports.  The last section treats the singular \(a=1,u=1\) base in
\(\{U,V+I\}/\{I,2U,2I,U+I\}\).

The proof does not enumerate orientations.  It gives one coboundary identity
for every strong orientation and every fixed positive rate vector.  The
finite support table is used only to show that its equality set is proper.

The result is claim-neutral.  It does not certify the full hard kernel, a
support pair, T3-2, or C3.  Uniform endpoint, boundary, and common-potential
estimates still require an independent audit.

## 1. The exact proper cloud

Write a lower complex as

\[
                         y=(c_y,b_y),                              \tag{1.2}
\]

where \(c_y\) and \(b_y\) are its \(U\)- and \(I\)-degrees.  Put

\[
                         w_a(y)=c_y+a b_y.                         \tag{1.3}
\]

Before a lower reaction, the proper pair \(aU\leftrightarrow V+I\)
preserves \(U+aI\).  Starting at the no-fast base \((u,n,0)\), its level
\(i=I\) has

\[
                         U=u-ai,\qquad V=n+i.                      \tag{1.4}
\]

If the proper forward and reverse rates are \(\alpha,\beta>0\), the level
birth and death rates are

\[
 \lambda_i=\alpha(u-ai)_{\underline a},\qquad
 \mu_i=\beta(n+i)i.                                                \tag{1.5}
\]

For \(a=0\), this is an immigration--death cloud with factorial tail.  For
\(a=1\), it is a finite birth--death cloud on \(0\le i\le u\).  In either
case, for every fixed \(u\) and lower edge \(y\to z\), the integrated lower
hazard before a regenerated visit to \(I=0\) has the asymptotic form

\[
 q_{yz}^{(n)}(u)
   =n^{-b_y}\{\gamma_{yz}(u)+O_u(n^{-1})\},                        \tag{1.6}
\]

where

\[
 \gamma_{yz}(u)>0\quad\Longleftrightarrow\quad w_a(y)\le u.        \tag{1.7}
\]

Indeed, a source with \(b_y\) cofactors needs at least \(b_y\) unmatched
proper births.  The birth--death product contributes exactly one factor
\(n^{-1}\) per unmatched cofactor, while its \(U\)-falling factorial is
positive exactly when \(c_y\le u-a b_y\), which is (1.7).  The product tail
sums all higher proper levels and gives the relative \(O_u(n^{-1})\) error.
Thus (1.6) is an analytic occupation calculation, not a bounded path list.

At a fixed \(u\), define the first surviving cofactor order

\[
 m_a(u)=\min\{b_y:y\in L_0,\ w_a(y)\le u\}.                        \tag{1.8}
\]

Only sources with \(b_y=m_a(u)\) survive on the leading slow time scale
\(n^{m_a(u)}\).  Sources of higher cofactor order have total relative
probability \(O_u(n^{-1})\) before the next leading lower macro.

## 2. Exact clean macro and its coboundary

Suppose \(y\to z\) is the first lower reaction and the proper deaths then
clear the cofactor before another lower reaction.  Extra proper
birth--death pairs cancel.  The exact no-fast endpoint satisfies

\[
 \begin{aligned}
 u'&=u-w_a(y)+w_a(z),\\
 \Delta V&=b_y-b_z.                                                \tag{2.1}
 \end{aligned}
\]

For the first line, the lower firing changes \(U\) by \(c_z-c_y\), while
the \(b_z-b_y\) extra proper deaths change \(U\) by \(a(b_z-b_y)\).
The second line follows because clearing the final cofactor uses
\(i-b_y+b_z\) proper deaths after the pre-lower cloud has raised \(V\) by
\(i\).

Define the bounded integer proof corrector

\[
                         H_a(U,V)=V+m_a(U).                        \tag{2.2}
\]

### Lemma 2.1 (cofactor-envelope coboundary)

Every leading clean lower macro obeys

\[
                         \Delta H_a=m_a(u')-b_z\le0.               \tag{2.3}
\]

Equality holds if and only if the target \(z\) is itself a leading source
at the endpoint \(u'\).

#### Proof

For a leading source \(b_y=m_a(u)\).  Substituting (2.1) into (2.2) gives

\[
 \Delta H_a=b_y-b_z+m_a(u')-m_a(u)=m_a(u')-b_z.                   \tag{2.4}
\]

Moreover \(u'=u-w_a(y)+w_a(z)\ge w_a(z)\), so \(z\) is one of the
complexes over which the minimum defining \(m_a(u')\) is taken.  Hence
\(m_a(u')\le b_z\).  This proves (2.3) and the equality criterion. \(\square\)

The clean-macro restriction costs only \(O_u(n^{-1})\).  After the first
lower reaction, the cofactor is at most a fixed number plus the factorially
tailed proper level.  A further lower clock is \(O_u(1)\), while every
nonterminal proper death is \(\Theta(nI)\).  The same birth--death product
therefore bounds a lower interruption during cleanup by \(O_u(n^{-1})\).

## 3. Equality trace and strict killing

Let \(Q_a\) be the leading clean-macro kernel restricted to
\(\Delta H_a=0\), and let \(S_a\) contain the leading macros with
\(\Delta H_a\le-1\).  These are physical no-fast kernels; the corrector in
(2.2) is not added to the common population potential.

There is a useful orientation-free description of equality paths.  If
\(y\to z\) is an equality macro, put

\[
                         r=u-w_a(y)\ge0.                           \tag{3.1}
\]

Then (2.1) gives \(u'=r+w_a(z)\), and \(z\) is leading at that endpoint.
If the next lower macro is sourced at \(z\), the same residual \(r\) is
preserved.  Thus a directed equality path can remain inside

\[
 {\cal M}_{a,r}
   =\{y\in L_0:b_y=m_a(r+w_a(y))\}.                               \tag{3.2}
\]

If \({\cal M}_{a,r}\) is a proper subset of the lower support, strong
connectivity gives a directed edge leaving it.  Following a shortest
directed path to its complement gives a positive-probability leading path
whose first exit lies in \(S_a\).  No orientation list is needed.

## 4. The six source-zero supports

For \(a=0\), \(w_0(y)=c_y\).  The six supports and their equality sets are
as follows:

| lower support \(L_0\) | \({\cal M}_{0,0}\) | \({\cal M}_{0,1}\) | \({\cal M}_{0,r},\,r\ge2\) |
|---|---|---|---|
| \(\{I,2U,2I,U+I\}\) | \(\{I,2U,U+I\}\) | \(\{I,2U\}\) | \(\{2U\}\) |
| \(\{U,2U,2I,U+I\}\) | \(\{U,2U,2I\}\) | \(\{U,2U\}\) | \(\{U,2U\}\) |
| \(\{U,I,2I,U+I\}\) | \(\{U,I\}\) | \(\{U\}\) | \(\{U\}\) |
| \(\{U,I,2U,2I\}\) | \(\{U,I,2U\}\) | \(\{U,2U\}\) | \(\{U,2U\}\) |
| \(\{U,I,2U,2I,U+I\}\) | \(\{U,I,2U\}\) | \(\{U,2U\}\) | \(\{U,2U\}\) |
| \(\{U,I,2U,U+I\}\) | \(\{U,I,2U\}\) | \(\{U,2U\}\) | \(\{U,2U\}\) |

Each entry follows directly from (1.8): once \(U\) or \(2U\) is enabled,
the minimum cofactor order is zero; below that threshold it is one, except
for the second row at \(u=0\), where it is two.  Every displayed equality
set is nonempty and proper.  Therefore the strong-cut argument after (3.2)
gives a strict \(H_0\)-drop from every compact equality phase.

The large-\(U\) part is killed with factorial occupation control.  If
\(2U\) is present, every \(2U\)-sourced edge either enters \(S_0\) or lowers
\(U\) by at least one, whereas every positive \(U\)-move has source degree
at most one.  The quadratic negative/killed clock dominates the linear
positive clocks.  If \(2U\) is absent, the maximal source is \(U\), and
every nonkilled \(U\)-sourced edge is nonincreasing.  Consequently, for

\[
             F_\theta(u)=\exp\{\theta u\log(u+e)\},
             \qquad 0<\theta<\tfrac12,                            \tag{4.1}
\]

the normalized \(Q_0\)-drift is strictly negative outside a compact set.
The positive contribution is \(O(u^{-1+2\theta})\), while a descending or
killed maximal-source transition has probability bounded below.  The
compact strong-cut argument then supplies a bounded killed resolvent
corrector.  Hence

\[
  (I-Q_0)^{-1}F_{\theta'}(u)\le C_{\theta',\theta}F_\theta(u),
  \qquad 0<\theta'<\theta<\tfrac12.                               \tag{4.2}
\]

This proves an analytic killed Markov-additive trace for all six supports.
It also shows that no equality-only recurrent class exists.

### Proposition 4.1 (strict regenerative reward)

For every strong orientation of any of the six source-zero supports and
every fixed positive rate vector, the leading trace reaches \(S_0\) in
finite mean macro count with factorial spectator occupation.  Its mean
\(H_0\)-reward before that hit is strictly negative.

Continue the trace until

\[
                         q=m_0(U_{\rm start})+1\le3                \tag{4.3}
\]

strict \(H_0\)-drops have occurred.  Since \(0\le m_0\le2\),

\[
 \Delta V
   =\Delta H_0-\{m_0(U_{\rm end})-m_0(U_{\rm start})\}
   \le-q+m_0(U_{\rm start})\le-1.                                \tag{4.4}
\]

Thus the completed regenerative block gives a genuine physical old-active
service even though an intermediate no-fast return may have \(\Delta V>0\).

## 5. Subdominant probability and physical duration

At the finite traps, (1.6) shows that all subdominant-source macros and all
cleanup interruptions have probability \(O(n^{-1})\) per leading macro.
Equation (4.2) gives a finite expected number of leading macros and all
fixed spectator occupation moments.  Therefore the probability of any
subdominant or dirty macro before the completed block is

\[
                           O(n^{-1})                              \tag{5.1}
\]

from a bounded trap, and \(n^{-1+o(1)}\) from a subpower initial spectator.
The estimate is obtained by compensating the rare clocks against the killed
occupation measure, not by truncating the number of macros.

The slowest leading source has \(b_y=2\).  Its waiting scale is \(O(n^2)\);
orders zero and one cost \(O(1)\) and \(O(n)\), respectively.  Combining
these holding times with (4.2) and the finite number (4.3) of strict drops
gives, for every fixed duration moment \(p\),

\[
 \mathbb E_u\tau^p
       \le C_p n^{2p}(1+u)^{c_p}.                                 \tag{5.2}
\]

In particular, a bounded-trap block has mean duration \(O(n^2)\), and a
subpower start has duration \(n^{2+o(1)}\).  This replaces the false
\(n\)-uniform duration assertion in the rejected theorem.

On the source-zero active axis,
\(G_\ell(u,n,0)=\Theta(n\log n)\).  A physical decrement of one \(V\)
particle therefore changes \(W_\ell=G_\ell^4\) at leading order by
\(-\Theta(n^3\log^4n)\), while the time reward in (5.2) is only
\(O(n^2)\).  Hence the corrected time scale is compatible with a
fourth-power Foster block.

## 6. The singular source-\(U\) base

Now take

\[
 L_+=\{U,V+I\},\qquad L_0=\{I,2U,2I,U+I\}.                         \tag{6.1}
\]

At the singular base \(u=1\), a pure opening consumes the only \(U\), so
the only leading lower source in the open state is \(I\).  The same
construction applies with \(a=1\) and

\[
 w_1(I)=1,\qquad
 w_1(2U)=w_1(2I)=w_1(U+I)=2.                                     \tag{6.2}
\]

Here

\[
 m_1(1)=1,\qquad m_1(u)=0\quad(u\ge2),                             \tag{6.3}
\]

and the equality sets are

\[
 {\cal M}_{1,0}=\{I,2U\},\qquad
 {\cal M}_{1,r}=\{2U\}\quad(r\ge1).                               \tag{6.4}
\]

They are proper.  Strong connectivity therefore forces a strict
\(H_1=V+m_1(U)\) drop.  Concretely, the apparently dangerous macro
\(I\to2U\) sends \(u=1\) to \(u'=2\) and raises \(V\) by one, but
\(m_1\) simultaneously falls from one to zero, so its \(H_1\)-increment is
exactly zero.  The now-enabled \(2U\) phase supplies the later strict drop.

The maximal-source Foster argument is identical to Section 4.  Thus the
source-\(U\) singular base admits the same killed priority trace, with
subdominant probability \(O(n^{-1})\) and duration at most \(O(n^2)\)
(in fact its first singular holding scale is only \(O(n)\)).

## 7. The all-reaction stopped priority block

Fix

\[
 L_n=\left\lfloor {n^{1/3}\over\log(n+e)}\right\rfloor.           \tag{7.1}
\]

Start at a historically reachable marked base \((u,n,0)\), where
\(u=n^{o(1)}\) and \(D_V>0\).  Run the raw physical chain and use the
following exhaustive labels.

1. A lower macro is **leading clean** if its first lower source has
   \(b_y=m_a(u_b)\), where \(u_b\) is the preceding no-fast base, and no
   second lower reaction occurs before the next no-fast return.
2. Stop at \(E_n\) on the first nonleading lower source or the first second
   lower reaction inside a macro.  Include that reaction and retain its
   actual endpoint.
3. Stop at \(B_n\), including the boundary-causing reaction, when
   \(U\), \(I\), or the physical reserve above the initial active level
   first reaches \(L_n\).
4. On the leading clean trace, count strict \(H_a\)-drops.  Stop at the
   first physical firing that takes \(V\) below its initial value \(n\).

If neither \(E_n\) nor \(B_n\) occurs, Proposition 4.1 and its source-\(U\)
analogue force the last stop.  Indeed, after
\(m_a(u)+1\le3\) strict no-fast drops, the hypothetical completed clean
endpoint would have \(V\le n-1\) by (4.4).  Since \(V\) changes by unit
steps under the proper deaths, the raw path must first cross from \(n\) to
\(n-1\) during or before that final cleanup.  This crossing is the physical
strict service \(D_n\).

Before \(D_n\), the base values obey

\[
             V+m_a(U)\le n+m_a(u)\le n+2.                          \tag{7.2}
\]

Thus the no-fast reserve is at most two.  During a proper cloud, reserve
and cofactor grow together, and the product estimate from (1.5) controls
both.  At \(D_n\), the physical reserve is exactly \(-1\).  By the reflected
mark identity, the selected mark changes from \(D_V=d>0\) to \(d-1\).

### Lemma 7.1 (weighted rare-event estimate)

For every fixed polynomial order \(p\), the stopped block satisfies

\[
 \begin{aligned}
 \mathbb E[(1+U_E+I_E+|V_E-n|)^p;E_n]
       &\le {C_p(1+u)^{c_p}\over n},\\
 \mathbb P(B_n)&=O(n^{-M})\qquad\text{for every fixed }M.          \tag{7.3}
 \end{aligned}
\]

Consequently

\[
                  \mathbb P(D_n)=1-n^{-1+o(1)}.                   \tag{7.4}
\]

#### Proof

At a fixed no-fast base, the birth--death occupation formula (1.6) gives a
factor \(n^{-1}\) for every source order above \(m_a(u_b)\).  Size-biasing
the proper level by a binary lower propensity preserves all fixed moments
because the product tail has a factorial denominator.  After the first
lower reaction, compensation of a possible second lower clock against the
\(\Theta(nI)\) proper-death clock gives the same factor \(n^{-1}\), again
with all fixed endpoint moments.

Integrate these bounds against the killed equality occupation measure.
Equation (4.2) supplies every polynomial spectator moment, so

\[
 \mathbb E\sum_{k<\tau_S}
 {C_p(1+U_k)^{c_p}\over n}
 \le {C_p(1+u)^{c'_p}\over n}.                                   \tag{7.5}
\]

Repeating this at most three times proves the first line of (7.3).  This is
an infinite killed-resolvent sum; no macro-count truncation is used.

For the boundary, (4.2) gives a factorial tail for \(U\).  Conditional on
each occupied base, (1.4)--(1.5) give a factorial tail for \(I\), and (7.2)
identifies the reserve excess with that same proper level up to two.
Therefore, for fixed \(0<\theta'<\theta<1/2\),

\[
 \mathbb P(B_n)
 \le C\,{F_\theta(u)\over F_{\theta'}(L_n-C)}
      +C\sum_{j\ge L_n-C}{(C/n)^j\over j!}.                        \tag{7.6}
\]

Because \(u=n^{o(1)}\) and \(L_n=n^{1/3+o(1)}\), the right side is
superpolynomially small.  The events \(D_n,E_n,B_n\) exhaust the stopped
block, so (7.4) follows. \(\square\)

### Lemma 7.2 (endpoint and duration moments)

For every fixed \(p\),

\[
 \begin{aligned}
 \mathbb E(1+U_\sigma+I_\sigma+|V_\sigma-n|)^p
      &\le C_p(1+u)^{c_p},\\
 \mathbb E\sigma^p
      &\le C_p n^{2p}(1+u)^{c_p}.                                 \tag{7.7}
 \end{aligned}
\]

#### Proof

The endpoint estimate on leading paths follows from (4.2) and the
size-biased factorial proper-level bound.  The \(E_n\) part is (7.3), and
the included \(B_n\) endpoint differs from its preboundary state by one
bounded reaction vector.

For time, augment each leading macro kernel by its physical holding-time
reward.  Conditional on a base, an order-\(b\) leading lower macro has
geometric trial count with all fixed moments \(O(n^{bp})\); the base waits
have polynomial moments and every open wait is \(O(n^{-1})\).  Since
\(b\le2\), its \(p\)-th time reward is at most
\(C_p n^{2p}(1+u)^{c_p}\).  Apply the binomial recursion for an additive
functional through \((I-Q_a)^{-1}\), then repeat for at most three strict
drops.  Equation (4.2) absorbs every polynomial cross term and proves the
second line of (7.7). \(\square\)

## 8. Entropy and common fourth-power drift

Put

\[
 G_\ell(x)=K_\ell+\sum_j\log(x_j!)+\ell\cdot x,\qquad
 W_\ell(x)=G_\ell(x)^4,                                           \tag{8.1}
\]

with the same fixed \(\ell,K_\ell\) as the adjacent charts.  The
maximal-source calculation proving (4.2) also gives the actual killed
spectator endpoint estimate

\[
 \mathbb E[B_\ell(U_{\tau_S})-B_\ell(u)]
       \le C\log(u+e)+C,                                          \tag{8.2}
\]

where \(B_\ell(v)=\log(v!)+\ell_Uv\).  To see this directly, add
\(C\log(u+e)\) to \(B_\ell\).  A maximal-degree killed or descending edge
then pays the bounded logarithmic cost of its actual endpoint, while every
positive edge is one source degree lower.  The positive drift residue has
finite support and is removed by the bounded killed Green corrector.  The
same estimate may be iterated the fixed number of times in (4.3).

On \(D_n\), the active coordinate is exactly \(n-1\).  The cofactor endpoint
has factorial moments, and (8.2) pays the spectator.  Hence

\[
 \mathbb E\!\left[
   G_\ell(X_\sigma)-G_\ell(X_0)+\mathbf1_{D_n}\log n
 \right]=o(\log n).                                                \tag{8.3}
\]

The \(E_n\) contribution follows from the endpoint-weighted first line of
(7.3): its positive entropy is \(n^{-1+o(1)}\log n=o(1)\).  The \(B_n\)
contribution is negligible by (7.6), after multiplying its actual included
endpoint by any fixed polynomial.  Since (7.4) holds,

\[
                 \mathbb E\Delta G_\ell
                    =-\log n+o(\log n).                            \tag{8.4}
\]

Moreover, (7.3), (7.7), the factorial occupation bound, and (8.2) give for
every fixed \(r\)

\[
                         \mathbb E|\Delta G_\ell|^r=n^{o(1)}.       \tag{8.5}
\]

At the starting base \(G_\ell=\Theta(n\log n)\).  Expanding exactly,

\[
 \Delta W_\ell
 =4G_\ell^3\Delta G_\ell+6G_\ell^2(\Delta G_\ell)^2
   +4G_\ell(\Delta G_\ell)^3+(\Delta G_\ell)^4.                    \tag{8.6}
\]

Equations (8.4)--(8.5) show that the last three terms are
\(o(G_\ell^3\log n)\).  The duration reward in (7.7) is
\(n^{2+o(1)}=o(G_\ell^3\log n)\).  Therefore

\[
 \mathbb E_{(u,n,0)}
 [W_\ell(X_\sigma)-W_\ell(X_0)+\sigma]
 \le-c\,G_\ell(X_0)^3\log n                                      \tag{8.7}
\]

for all sufficiently large \(n\).

### Candidate exact-proper priority theorem

For each of the six source-zero supports and the source-\(U\) singular
support (6.1), every strong orientation, every fixed positive rate vector,
and every historically reachable positive-debt start with
\(u=n^{o(1)}\), the all-reaction stopping rule of Section 7 has:

- strict physical old-active service with probability \(1-n^{-1+o(1)}\);
- arbitrary fixed endpoint moments and duration \(n^{2+o(1)}\);
- superpolynomial moving-boundary probability;
- the full entropy estimate (8.3); and
- the common fourth-power drift (8.7).

The theorem replaces the false first-upward-terminal rule only on these
singular exact-proper bases.  Its bounded corrector \(m_a\) is used in the
proof trace and is not added to \(W_\ell\).

## 9. Remaining audit obligations

Before this priority block can be promoted, an independent audit must:

- reconstruct the occupation asymptotic (1.6) and its time augmentation
  from the raw physical chain;
- verify the killed equality resolvent (4.2) for the six explicit supports
  without replacing the strong-cut proof by orientation enumeration;
- replay the endpoint-weighted compensation in (7.3), including dirty
  cleanup paths;
- check the first physical \(V<n\) stopping convention and reflected mark;
  and
- verify the common-\(W_\ell\) Taylor estimate (8.3)--(8.7).

No finite orientation or path enumeration can replace these obligations.
All hard-family and global certification flags remain false.
