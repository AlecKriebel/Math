# One-active mixed-top killed carriers (uniform old-debt claim withdrawn)

> **Refuted statement.** Lemma 4.1 and the old-debt part of Theorem 6.1
> below are false as uniform physical-time assertions. The exact network
> and vanishing nested-entry race are recorded in
> *one_active_nested_entry_obstruction.md*. The surplus-service and
> finite-carrier estimates remain useful locally, but this note must not be
> cited as a certified old-debt or 3,075-incidence theorem.

## 1. Scope and status

Fix an active species \(X\) and write the other species as \(U,V\).
Complexes have molecularity at most two, linkage supports are disjoint, and
every nontrivial linkage is strongly connected with fixed positive labelled
rates. At a failed one-active descriptor there is no \(2X\) complex, so the
complete top menu is

\[
 {\cal H}_X=\{X,X+U,X+V\}.                              \tag{1.1}
\]

The exact affine-filtered candidate table has 3,297 one-active incidences.
The support certificate in *src/one_active_phase_shape.py* finds 222
incidences with a wholly top linkage; their sole countable shape is treated
in *one_active_countable_phase_service.md*. This note treats the remaining
3,075 incidences, in which every linkage meeting \({\cal H}_X\) is mixed.

The intended result below is local. Its claimed killed-carrier
service/coboundary and direct factorial-entropy episode on a finite
generator-bad cross-section is now known to fail for consistent old debt
created by nested slow entries. It does not promote a support-pair count.
Global gluing to the generator-good region is a separate stopping-time
statement.

## 2. Base states and marked carriers

Put \(X=N\). Reactions have active increments in \(\{-1,0,1\}\). Call a
lower-to-top reaction an **entry**, a top-to-lower reaction an **exit**, and
a top-to-top reaction internal. At a state whose inactive population is
\(e=(u,v)\), a top source has rate \(N\) times a falling factorial in \(e\).
Every lower source has rate bounded by a quadratic polynomial in \(e\).

A **base state** has no enabled top source. If a top source is enabled with
no pending entry, its first exit is an unpaired service. If an entry has
just fired, mark one pending allowance. The first top exit consumes that
allowance and has net active reward zero; any further top exit is unpaired
and has reward \(-1\).

> **Lemma 2.1 (mixed carriers drain on the \(X\)-clock).** Suppose every
> linkage containing a top complex is mixed. From a bounded inactive start,
> a marked top carrier reaches an exit in a time \(\sigma_N\) satisfying,
> for every fixed \(r\),
> \[
>  {\mathbb E}\sigma_N^r\le {C_r\over N^r},\qquad
>  {\mathbb E}(1+U_{\sigma_N}+V_{\sigma_N})^r\le C_r.   \tag{2.1}
> \]
> The number of internal top reactions before that exit has every fixed
> moment. With every lower reaction retained,
> \[
>  {\mathbb P}(\hbox{a lower reaction interrupts the carrier})
>  \le {C\over N}.                                     \tag{2.2}
> \]

### Proof

Strip the common \(X\) from the at most three top complexes. In each mixed
linkage, strong connectivity gives a directed path from every top vertex to
a lower vertex. Make lower targets absorbing and tag the zero cofactor or
one cofactor molecule supplied by the actual target. The tag moves on a
finite transient graph and its absorption time on the fast clock is phase
type. Other top reactions form a finite-type linear particle system during
that phase-type interval. Its event count and endpoint therefore have all
polynomial moments. Rescaling fast time by \(N\) proves (2.1).

The total lower propensity is at most
\(C(1+U+V)^2\). Integrating it over the carrier and using the preceding
moments gives (2.2). A competing top exit is already a service or consumes
the single pending allowance, so it is not erased. A competing lower event
and its actual target are retained. \(\square\)

Sequential base entries can launch \(O(1)\) primary carriers on a fixed
physical interval. More than one carrier can be simultaneously pending only
if a lower entry occurs during an existing carrier. Primary base entries
have bounded compensator on a bounded base phase. By (2.2), each carrier
produces a further interrupted or nested carrier with conditional mean at
most \(C/N\). For large \(N\), the descendant family of each primary
carrier is dominated by a subcritical Galton--Watson family. Thus

\[
 \sup_N{\mathbb E}J_N^r<\infty,\qquad
 {\mathbb E}A_N\le {C\over N},                          \tag{2.3}
\]

where \(J_N\) is the total raw carrier count and \(A_N\) is the number left
unresolved by lower interruption or at a deterministic time boundary. The
boundary term is also \(O(N^{-1})\): it is bounded by launch intensity times
mean carrier lifetime. This is a total-carrier bound, not a per-entry
shortcut.

## 3. The finite contracted kernel

Let \(E_0\) be any finite set of inactive populations. It will be the
statewise generator-bad cross-section supplied by the tier contradiction.
Run the following ideal dynamics from a base point of \(E_0\).

1. Retain every lower reaction and its actual target.
2. If it is an entry, launch one marked carrier and contract its first exit.
3. If it is not an entry but enables a top source, the first exit is
   unpaired service.
4. After a paired exit, any still-enabled top source supplies unpaired
   service.

Completed entry--exit carriers have active reward zero. Every other ideal
active reward is nonpositive. A prescribed finite carrier outcome has a
strictly positive limiting probability because all relevant top clocks
carry the same factor \(N\), while lower interference has probability
\(O(N^{-1})\).

Before fixing the padding, inspect the full projected population graph. For
each point of \(E_0\) from which surplus service is reachable, select one
finite shortest service path. Lemma 4.1 below supplies the analogous paths
for consistent old-debt marks. Carrier endpoints have infinite support in
principle, but Lemma 2.1 gives uniform integrability. Given
\(\varepsilon>0\), choose one finite padding \(E\supset E_0\) containing
all selected paths and making the inactive entropy cost of any remaining
carrier tail outside \(E\) at most \(\varepsilon\) in expectation. Stop a
slow base excursion on leaving \(E\). If the exiting slow edge is an entry,
finish its first carrier physically before stopping; it is not charged as
unresolved merely because it crossed the padding. Only a genuine lower
interruption or a carrier active at the deterministic time boundary is
charged to \(A_N\). Inside \(E\), the contracted base kernel is finite. Add
two absorbing marks, **service** and **out**.

On this finite kernel every internal macroedge has reward zero and every
service edge has reward \(-1\). Consequently a terminal component either
reaches service or has zero reward on every cycle. In the latter case the
raw entry reward \(+1\) and its first-exit reward \(-1\) are a coboundary on
the singular one-carrier graph. This bounded singular potential is not a
bounded potential for an arbitrary number of simultaneous raw carriers;
those carriers are instead controlled by (2.3).

## 4. Consistent old debt reaches service

Define scalar debt reaction by reaction:

\[
 D^+=\begin{cases}
 D+1,&\Delta X=1,\\
 (D-1)^+,&\Delta X=-1,\\
 D,&\Delta X=0.
 \end{cases}                                           \tag{4.1}
\]

Only marks obtained from a physical path begun with \(D=0\) are called
**consistent**.

> **Withdrawn Lemma 4.1 (actual-target service reachability).** From every
> consistent base state with \(D>0\), an unpaired top exit is reachable by a
> finite physical reaction path. For a finite starting set \(E_0\), one may
> choose these paths and one finite padding \(E\) uniformly. Hence there
> are \(T,p>0\) such that the full chain, with all competing reactions
> retained, has probability at least \(p\) of servicing one old unit during
> a block of duration at most \(T\), apart from the \(O(N^{-1})\) unresolved
> correction in (2.3).

### Proof

For every fired reaction \(y\to y'\), strong connectivity supplies a
directed return path from the actual target \(y'\) to its source \(y\). The
return-prefix identity makes every successive source physically enabled and
telescopes to \(y-y'\). Concatenating these prefixes shows that every
physical population path can be reversed. This statement concerns
population states only; it does not falsely assert that a reflected debt
mark is reversed.

Because the current consistent mark has \(D>0\), its history has a last
time \(s\) at which \(D=0\). After \(s\), reflection is inactive and
\(H=X-D\) is constant. Hence the population segment from \(s\) to the
current state has active displacement exactly \(+D\). Reverse that segment,
in reverse chronological order, using the actual-target return prefixes
above. The resulting finite physical path has total active displacement
\(-D<0\).

Contract, chronologically along this reversed path, each positive-\(X\)
entry with the first later negative-\(X\) exit available to it. Since the
total reward is negative, at least one exit remains unpaired. Truncate the
path at the first such exit. Before it, completed carriers have reward zero
and no pending allowance remains; the terminal exit therefore lowers the
debt present at the start rather than merely cancelling a new entry.

This proves service reachability without conditioning on a future
activation and without requiring a return to the reference *mark*: every
edge starts from the actual target of the preceding edge. The historical
time \(s\) is used only to prove that some finite population path exists.
The stopping rule below chooses a shortest such path from the present
projected state and carries no history stack.

Before that first service, completed carriers have net active increment zero
and uncompleted entries only increase \(X\). Hence, for all sufficiently
large \(X\), feasibility of the truncated path depends only on inactive
population, the binary flag \(D>0\), and one pending-carrier allowance, not
on the numerical active level. Project to those data and choose a shortest
service witness. Its length and maximal inactive population are finite.
There are finitely many starting points in \(E_0\), so the selected witnesses
have a common finite length and lie in one finite padding \(E\).

At a base vertex, the probability that a prescribed lower edge is the next
lower edge and fires within a fixed time is positive. At a carrier vertex,
the probability of the prescribed finite top outcome is bounded below
independently of \(N\), and lower interference costs only \(O(N^{-1})\).
The product over the finitely many selected paths has a positive minimum.
Choose \(T\) larger than their slow waiting-time quantile. \(\square\)

The lemma removes the apparent unbounded return stack. A stack proves that
a path exists; the finite projected population graph supplies a shortest
path, so no genealogical stack enters the stopping kernel.

## 5. Surplus service or zero reward

Start at a base state with \(D=0\). If service is reachable in the full
projected graph, the selected finite path gives a uniform probability of a
surplus exit. If it is not reachable, every ideal contracted macroedge has
reward zero. A physical interruption may nevertheless create rare debt
through a transition omitted from the singular graph. Equation (2.3)
charges that arrival at rate \(O(N^{-1})\). Whenever that debt next lies in
the finite bad cross-section, Lemma 4.1 supplies its old-debt service block.
If its carrier endpoint lies outside the padding, it is passed to the
generator-good excursion with the debt mark retained.

Thus, after transient carriers and interruption debt are eventually
drained, \(D=0\) and \(X\) is exactly unchanged on a service-free terminal
component.
During one singular carrier it differs by the bounded one-carrier potential.
Multiple physical carriers and deterministic-boundary carriers are the
\(O(N^{-1})\) correction in (2.3), not part of the bounded coboundary claim.

For a classwise construction begun at a reference state, put \(H=X-D\).
Then \(H\) is pathwise nonincreasing. On a drained service-free return,
\(D=0\), so \(X\le X(0)\). Combined with the finite inactive
cross-section, these zero-reward returns lie in a genuinely finite set of
original population states. Finite-mean return to that set uses the global
generator-good/debt gluing; it is not asserted by the local kernel alone.

## 6. Direct factorial-entropy episode

Let

\[
 h(n)=n(\log n-1)+1,\qquad
 \Phi(x)=h(x_X)+h(x_U)+h(x_V).                          \tag{6.1}
\]

> **Withdrawn Theorem 6.1 (mixed-top entropy block).** Fix a finite base set \(E_0\).
> For every service-reachable base mark, and for every consistent mark with
> old debt, there are \(T,p,C,N_0\) and stopping times \(\tau_N\) such that
> \[
> \begin{aligned}
>  {\mathbb P}(S_N\ge1)&\ge p,\\
>  {\mathbb E}A_N&\le C/N,\\
>  {\mathbb E}\tau_N^r+{\mathbb E}J_N^r&\le C_r,
>       \qquad r<\infty,                               \tag{6.2}
> \end{aligned}
> \]
> and the inactive endpoint has every fixed polynomial moment. Here \(S_N\)
> is the unpaired-exit count and \(A_N\) the unresolved entry count. For all
> large \(N\),
> \[
>  {\mathbb E}\{\Phi(X_{\tau_N})-\Phi(X_0)\}
>  \le -{p\over2}\log N+C.                             \tag{6.3}
> \]
> If a base component is not service reachable, Section 5 gives the drained
> zero-reward alternative instead.

### Proof

Use Lemma 4.1's finite prescribed path, or a shortest surplus-service path,
and stop at service, at a deterministic slow-time horizon \(T\), or after a
slow base exit from the padded set \(E\). Finish the carrier launched by an
exiting entry; its additional duration is \(O(N^{-1})\). Charge only a
genuinely lower-interrupted carrier or one still active at the deterministic
boundary. Exact-path probability gives the first line of (6.2). Lemma 2.1,
the bounded lower propensities on \(E\), and the subcritical carrier-family
bound give its other lines. No lower channel is suppressed.

Cancel each completed entry with its first exit. The active endpoint is

\[
 X_{\tau_N}-N=A_N-S_N.                                 \tag{6.4}
\]

The counts in (6.2) have all fixed moments. Taylor expansion on
\(|A_N-S_N|\le N/2\), with a high-moment estimate on the complement, gives

\[
 {\mathbb E}\{h(X_{\tau_N})-h(N)\}
 \le- p\log N+C+{C\log N\over N}.                     \tag{6.5}
\]

Every slow base jump is bounded. A completed carrier has a
phase-type/linear endpoint with all polynomial moments, and the padding was
chosen by uniform integrability. Since \(h(m)\le C(1+m)^2\), the inactive
entropy endpoint contributes only \(C\). Equations (6.5) and (2.3) prove
(6.3). \(\square\)

The proof controls factorial entropy directly. A scalar workload decrease
would not be enough under subpower separation of inactive coordinates.

## 7. Exact boundary of the result

Theorem 6.1 supplies the local physical episode proposed for the 3,075
mixed/lower-top incidences:

- every lower reaction remains in the dynamics;
- completed carriers are endpoint-neutral in the active coordinate;
- total, not per-entry, unresolved reward is \(O(N^{-1})\);
- old debt is handled from actual targets without an unbounded mark stack;
- surplus service gives a direct \(-p\log N\) factorial-entropy margin; and
- a drained service-free terminal component has a finite classwise target.

The remaining obligations are an independent audit of Lemma 4.1 and global
gluing: append the Anderson--Kim generator-good excursion to each local
endpoint and prove one random-time Foster inequality on a closed
irreducible class. Until those checks are complete, the 3,075 incidences and
1,227 candidate support pairs remain unpromoted.
