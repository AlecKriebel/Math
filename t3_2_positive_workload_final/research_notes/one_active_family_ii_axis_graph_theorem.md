# The exact one-active Family-II axis lemma

## 1. Claim boundary

This note closes one graph-theoretic part of the candidate one-active
repair.  It proves the relative first-debt-reduction versus same-base
arrival-resistance inequality for the exact lower-only/single-top-cofactor
family, for every strongly connected orientation and every positive rate
vector.  It does not prove the aggregate killed-kernel estimates, a
promotion-return estimate, pair recurrence, or T3-2.

The finite support selector is
`src/one_active_relative_debt_cegar.py`, function
`family_ii_axis_certificate`.  It finds exactly 30 physical
pair--descriptor incidences on ten support pairs, collapsing after active
species and inactive-species relabelling to fifteen cap profiles and five
support types.  Its frozen hashes are

```text
rows   3642fb37f7dde46a5e0204f39851d38c167516678b4a1aae92529ec211d29d25
pairs  45a1df2a3462af42aed88753720c5b20b569238b08f7b6a2ba3d1811931e4a75
```

All recurrence and global flags remain false.

## 2. Relative resistance

Relabel the active species as $C$.  In this family the sole
active-degree-one source is $B+C$, so the no-fast set is the apparent
spectator axis $B=0$.  Start at a historically consistent marked state

\[
 (A,B,D_C)=(a_\Gamma,0,d),\qquad d>0,
\tag{2.1}
\]

and put the relative active displacement $r(0)=0$.  Before the first
time $r<0$, reflection is inactive and

\[
D_C(t)=d+r(t).
\tag{2.2}
\]

On a fixed closed irreducible class \(\Gamma\), the value in (2.1) is an
exact conserved spectator population; write it as \(a_\Gamma\).  The
atlas cap is only its availability representative

\[
 \bar a=\min\{a_\Gamma,2\}\in\{0,1,2\}.             \tag{2.2a}
\]

Thus \(\bar a=2\) means \(a_\Gamma\ge2\), not
\(a_\Gamma=2\).

A degree-zero reaction has resistance one precisely when it fires while
$B>0$; every active-source reaction has resistance zero.  Let
$m_-(a_\Gamma)$ be the minimum resistance to $r<0$, and let
$m_+(a_\Gamma)$ be the
minimum resistance of a return to $B=0$ with $r>0$.

> **Theorem 2.1 (Family-II axis resistance).**  For every one of the 30
> selected incidences, every strongly connected orientation of both
> linkage supports, every fixed class \(\Gamma\), and every historically
> consistent base (2.1),
> \[
>   m_-(a_\Gamma)=0,\qquad m_+(a_\Gamma)\ge1.
> \tag{2.3}
> \]
> In particular, the first strict old-debt reduction has one full kinetic
> order over every unresolved same-base arrival.  No population cutoff is
> used.

## 3. Exact support classification

Up to linkage order and the inactive $A/B$ exchange, the fifteen
profiles are the three normalized caps $\bar a=0,1,2$ on each of the following five
supports:

\[
\begin{array}{c|c}
L_0&L_1\\ \hline
\{A,A+B\}&\{0,2B,B+C\}\\
\{A,A+B\}&\{0,B,2B,B+C\}\\
\{A,A+B\}&\{0,B,B+C\}\\
\{A,A+B\}&\{B,2B,B+C\}\\
\{A,B+C\}&\{2A,A+B,2B\}.
\end{array}
\tag{3.1}
\]

There are no descriptor-forbidden directed edges in these rows.  Thus the
proof below quantifies over every strong directed graph on each displayed
support, not only the obstruction Hamilton cycle or the maximal graph.

The apparent unbounded spectator is not unbounded in (3.1).  In the first
four rows $A$ is an exact population invariant: both directions
$A\leftrightarrow A+B$ preserve it and the second linkage contains no
$A$.  In the last row $A+B$ is an exact population invariant.  Hence a
no-fast base has the exact classwise value \(a_\Gamma\), whose availability
type is the displayed cap \(\bar a=\min\{a_\Gamma,2\}\).  No one-counter
pumping or bounded-box inference is involved; constants may depend on the
fixed invariant \(a_\Gamma\).

## 4. Zero-resistance debt reduction

### 4.1 The first four supports

Strong connectivity of the two-node first linkage forces both

\[
 A\longrightarrow A+B,qquad A+B\longrightarrow A.
\tag{4.1}
\]

If $a_\Gamma\ge1$, fire $A\to A+B$ from $B=0$.  This is a free
degree-zero reaction and leaves $B=1$.  Strong connectivity of the mixed
linkage gives at least one outgoing edge $B+C\to z$.  Fire it.  It is an
active-source reaction, has resistance zero, and changes $r$ by $-1$.
Thus $m_-(a_\Gamma)=0$.

Suppose $a_\Gamma=0$.  For the first three mixed supports in (3.1), choose a
simple directed path from $0$ to a nonzero lower complex $q\in\{B,2B\}$.
If the path reaches a lower $B$-complex before $B+C$, then it has done
so while the fast clock was disabled; immediately firing any outgoing
$B+C$-edge lowers $r$.  If the path first enters $B+C$, that entry
raises $r$ by one.  Simplicity prevents the next vertex on the path from
being $0$, so the next edge is an active exit to a nonzero lower
complex.  The resulting $B>0$ enables one further active exit, which
lowers $r$ below zero.  Every reaction used has resistance zero.

The fourth mixed support contains no $0$.  At $a_\Gamma=B=0$ no reaction is
enabled, so this face cannot be a historically consistent positive-debt
base.  This exhausts the first four rows.

### 4.2 The last support

Strong connectivity of $\{A,B+C\}$ forces both directions and the second
linkage preserves $A+B$.  If $a_\Gamma=0$, the base is frozen.  If
$a_\Gamma=1$,
the quadratic linkage is disabled and the only excursion is

\[
 A\longrightarrow B+C\longrightarrow A,
\tag{4.2}
\]

whose reflected debt returns to zero.  Hence neither base is historically
consistent with $d>0$.

If $a_\Gamma\ge2$, strong connectivity of
$\{2A,A+B,2B\}$ supplies an outgoing edge
$2A\to z$, where $z=A+B$ or $2B$.  Fire it at $B=0$; it costs zero
and creates $B>0$ without increasing $C$.  Then fire the forced active
exit $B+C\to A$.  This lowers $r$ to $-1$, again at total resistance
zero.

## 5. No zero-resistance unresolved return

It remains to show $m_+(a_\Gamma)\ge1$.  Consider a primitive word from a
no-fast base $B=0$ back to $B=0$ with no intermediate no-fast return.
If its resistance is zero, its first reaction which makes $B>0$ fires
while the fast clock is disabled.  That launch increases $C$ by at most
one: it either enters $B+C$, or it is a lower-to-lower reaction and does
not change $C$.

After the launch, $B>0$.  A resistance-zero continuation can therefore
use only active-source reactions until it returns to $B=0$.  Since
$B+C$ is the sole top complex, every such reaction is an active exit and
decreases $r$ by one.  At least one exit is needed to reach $B=0$.
Consequently the net relative displacement of the primitive word is at
most zero.  Decomposing a general base-to-base word at its intermediate
no-fast returns gives the same conclusion for every zero-resistance word.
Thus a return with $r>0$ has resistance at least one, proving (2.3).

## 6. What this does and does not remove

The theorem eliminates the small-witness concern for the only exact
single-top-cofactor/lower-only profiles: their spectator is fixed at the
classwise invariant \(a_\Gamma\), and the required paths use populations
at most two above that base.  It also proves the arbitrary-orientation graph inequality directly,
so the bounded CEGAR is unnecessary for these 30 incidences.

It does not show that one selected word determines the aggregate stopped
kernel.  Neutral regeneration, countable-phase occupation, powered
factorial endpoint bounds, and promotion continuations still have to be
proved before these local rows can enter a common physical-time Foster
composition.
