# Priority macrochain for the sixteen dormant promotion rows

## 1. Scope and verdict

This note audits the load-bearing restart claim in Section 4.2 of
*two_active_promotion_36_pair_theorem.md*. The original wording incorrectly
said that all top and whole-shell clocks have the same scale. That is false
for the whole linkage \(\{B,2A\}\): on its exact rank-one shell,

\[
 A\asymp N,\qquad B\asymp N^2,
\tag{1.1}
\]

so a \(BC\)-source clock and the fastest shell clocks have order \(N^2\),
whereas \(A\)- and \(AC\)-source clocks have order \(N\).

The mismatch does not produce a counterexample. The faster \(BC\) reactions
are stabilizing. After contracting the conservative whole-shell motion, the
proper linkage has a finite priority macrochain whose only mark is reflected
workload debt. No nontrivial closed macroclass can avoid a surplus
workload-lowering exit.

The argument below is valid for arbitrary strongly connected directed graphs
and arbitrary positive rates. It uses the already audited shell-interior and
corrected-factorial endpoint estimates as inputs; it does not reprove those
inputs.

## 2. Reflected workload debt

Let

\[
 h(y)=w\mathbin{\cdot}y
\tag{2.1}
\]

be the descriptor workload of a proper-linkage complex. Along the physical
proper-linkage reactions define

\[
 D_{k+1}=\bigl(D_k+h(z_k)-h(y_k)\bigr)^+,\qquad D_0=0.
\tag{2.2}
\]

A negative increment which is larger than the current \(D_k\) is called a
*surplus exit*. Before the first surplus exit, the cumulative proper-linkage
workload increment equals \(D_k\). Thus a stopped path with no surplus has
nonnegative endpoint increment, while a surplus path has endpoint increment
at most \(-1\).

Whole-linkage reactions preserve \(h\), so they do not change \(D\). They are
retained physically and are contracted only for this workload bookkeeping.

## 3. The equal-scale shell \(\{A,B\}\)

Here \(w=(1,1,0)\). The proper support is a strongly connected subset of

\[
 \{0,C,2C,AC,BC\}
\tag{3.1}
\]

which contains \(2C\) and at least one of \(AC,BC\). In the non-disabled
rows it also contains \(0\). At \(C=0\), the only enabled proper source is
\(0\).

On the shell interior \(A,B\asymp N\). Whenever \(C>0\), every present
\(AC\)- and \(BC\)-source channel has order \(N\). Let \(K\) denote the
present set of these top vertices. Because \(K\) is a nonempty proper subset
of a strongly connected linkage, at least one directed edge leaves \(K\).
Every source in \(K\) is physically enabled when \(C>0\), so the aggregate
top-to-lower exit hazard is at least \(cN\). Internal top edges and the whole
shell are retained; the first top exit nevertheless has an exponential
tail on the \(N\)-clock.

Every lower-to-top entry raises \(D\) by one and every top exit lowers it by
one. Hence only the following transient macrostates are needed:

\[
 R=(C=0,D=0),\qquad
 P=(C>0,D=1),\qquad
 Q=(C>0,D=0),
\tag{3.2}
\]

together with the absorbing surplus state \(\dagger\). From \(Q\), the next
top exit reaches \(\dagger\). From \(P\), the first top exit either

1. consumes the only \(C\) and returns to \(R\); or
2. leaves \(C>0\), reaches \(Q\), and is followed by a surplus exit.

At \(R\), a \(0\)-source edge either creates a \(C\)-only target and enters
\(Q\), or creates a top target and enters \(P\). Suppose every trial from
\(R\) returned to \(R\) with no positive probability of reaching \(Q\) or
\(\dagger\). Then the complex set consisting of \(0\) and all reachable top
vertices would be closed under the directed proper-linkage graph. It omits
\(2C\), contradicting strong connectivity. Since the graph and rate vector
are finite, each visit to \(R\) therefore has a fixed positive probability
of reaching \(Q\) or \(\dagger\) before the next return.

Consequently the number of neutral \(R\)-returns before surplus service has
a geometric tail.

## 4. The unequal-scale shell \(\{B,2A\}\)

Here \(w=(1,2,0)\). The proper support is a strongly connected subset of

\[
 \{0,A,C,2C,AC,BC\}
\tag{4.1}
\]

which contains \(2C\) and \(BC\). The vertex \(BC\) is the unique
proper-linkage vertex of workload two. At \(C=0\), the leading enabled proper
source is \(A\), when \(A\) is present, and otherwise is \(0\). The two rows
with neither source are the disabled finite-class rows.

This choice is mandatory: one must not wait for a \(0\)-source clock while
an \(A\)-source clock of order \(N\) is enabled. In the exact enabled-source
histogram, a row labelled \(\{0\}\) has no \(A\)-vertex in the proper
linkage. In rows labelled \(\{0,A\}\) or \(\{A\}\), the macrochain always
takes the next \(A\)-source reaction and treats the \(0\)-source clock as a
lower-order interruption.

Whenever \(C>0\), every \(BC\)-source channel has order \(N^2\). Every target
of such a channel has workload at most one, and therefore

\[
 h(z)-h(BC)\le-1.
\tag{4.2}
\]

An entry from \(0\) can create at most two units of debt, and an entry from
\(A\) can create at most one. Thus

\[
 D\in\{0,1,2\}
\tag{4.3}
\]

throughout the priority macrochain.

If a \(BC\) reaction leaves \(C>0\), another \(BC\) clock is immediately
enabled. After at most two such reactions all old debt is cleared, and the
next one is a surplus exit. If a \(BC\) reaction consumes the last \(C\),
its target is either \(0\), with workload drop two, or \(A\), with workload
drop one. The former clears every possible debt and returns to
\((C=0,D=0)\). The latter can leave only
\((C=0,D=1)\), at which the \(A\)-source clock is leading.

It remains to exclude two possible neutral base traps. When \(A\) is
present, at \((C=0,D=1)\) an \(A\to BC\) edge can raise the debt to two,
followed by a \(BC\to A\) edge which returns it to one. When \(A\) is absent,
\(0\to BC\) followed by \(BC\to0\) can return
\((C=0,D=0)\) to itself. If every priority transition remained in one of
these two-vertex macrocycles, the complex subset
\(\{b,BC\}\), \(b\in\{0,A\}\), would be closed in the proper-linkage
digraph. Strong connectivity and the presence of \(2C\) rule this out. Any
edge leaving \(A\) has the same order-\(N\) scale as the other
\(A\)-source edges, every edge leaving \(0\) has the same order-one scale
as the other \(0\)-source edges, and any edge leaving \(BC\) has the same
order-\(N^2\) scale as the other \(BC\)-source edges. Thus the probability
of escaping either neutral macrocycle at each visit is bounded below
independently of \(N\).

Equivalently, allow a putative reset component
\(S\subseteq\{0,A,BC\}\), so mixed \(0/A\) targets are not omitted.
If \(A\) is a proper-linkage vertex, its source remains enabled by the
interior shell even after a reaction targets \(0\); the leading base source
is still \(A\), and the \(0\)-source clock is lower order. Moreover
\(A\to0\) itself lowers \(H_w\) by one: it can clear the single unit in
\(R_1\), but a further such exit is surplus. If \(A\) is absent, \(0\) is
the leading base source. Thus any service-free dominant reset component
contains one of the source pairs \(\{A,BC\}\) or \(\{0,BC\}\). An edge
from that pair to the third base vertex is already a same-source-scale
escape (and a negative-workload edge when sourced at \(A\) or \(BC\)).
If no such edge exists, the pair itself is closed. In either formulation,
strong connectivity to \(2C\) excludes a neutral closed \(S\).

All repeated \(A\)-source reactions are explicit macrotransitions; they are
not folded into the reversible whole shell. If an \(A\)-source reaction
targets \(0\), it lowers \(H_w\) by one, so it can clear at most the single
unit in \(R_1\) and the next such reaction is surplus. If its target carries
\(C\), the \(BC\)-priority block starts immediately. Hence there is no
order-one \(0\)-clock wait containing unaccounted order-\(N\) proper
reactions.

The minimal nonabsorbing state set can therefore be taken as

\[
\begin{split}
 R_0&=(C=0,D=0),\\
 R_1&=(C=0,D=1)\quad\text{(only when \(A\) is a vertex)},\\
 P_d&=(C>0,D=d),\qquad d=0,1,2.
\end{split}
\tag{4.4}
\]

The state \(P_0\) has an immediate surplus \(BC\) exit. Repeated (4.2)
drives \(P_2\) or \(P_1\) either to \(P_0\), to a surplus exit, or to
\(R_0,R_1\). The only possible neutral base cycles are the two just
excluded. Hence this finite macrochain has no closed class disjoint from
\(\dagger\).

Lower-order \(A\)- or \(AC\)-source reactions while \(BC\) is enabled have
probability \(O(N^{-1})\) before the next \(BC\) reaction. They are retained
as physical interruptions and are not used to establish service.

## 5. Uniform stopping block

The finite macrochains in Sections 3--4 have an absorbing state accessible
from every non-disabled starting macrostate and no other closed class. For
the fixed network and rates, there are constants \(C<\infty\) and
\(q\in(0,1)\) such that

\[
 {\mathbb P}\{\text{no surplus in the first \(K\) macrotransitions}\}
 \le Cq^K+O(N^{-1}).
\tag{5.1}
\]

Choose \(K\) so that \(Cq^K\) is smaller than one quarter of the resulting
surplus probability, and stop after service, physical interruption, or
\(K\) macrotransitions. Before service, the endpoint workload increase is
the reflected debt and is at most two. It follows that, for some
\(\delta>0\),

\[
 {\mathbb E}\Delta H_w\le-\delta
\tag{5.2}
\]

for all sufficiently large \(N\).

All reactions remain present. The contractions only invoke the strong
Markov property at physical reaction times:

1. \(0\)-source waits have fixed exponential moments;
2. \(A\)-source waits are killed occupation windows of order \(N^{-1}\);
3. equal-shell top exits have order-\(N^{-1}\) duration;
4. \(BC\) priority exits have order-\(N^{-2}\) duration; and
5. the conservative shell evolves throughout every wait.

Item 1 occurs only in supports with no proper \(A\)-source. When \(A\) is
present, item 2 replaces item 1 and every resulting proper reaction is
recorded in the macrochain.

With \(K\) fixed, physical duration has moments of every fixed order.
In the equal-scale shell, one top-exit macrotransition can contain a random
number of \(AC\leftrightarrow BC\) internal proper reactions. This number
is not pathwise bounded by \(K\). On the shell interior, however, the total
internal top rate is at most \(CN\) and the aggregate top-to-lower exit
rate is at least \(cN\). Its tail is therefore geometrically bounded,
uniformly in \(N\), and it has moments of every fixed order. Internal top
reactions preserve both \(C\) and \(H_w\). Thus the total proper-reaction
count has fixed-order moments, while the carried \(C\)-population remains
bounded by the \(K\) base/exit macrotransitions. The audited whole-shell
estimates then give the required scaled endpoint moments, and localization
can be removed.

## 6. Corrected-factorial lift

On the shell-interior event,

\[
\begin{array}{c|cc}
L_*&\log A&\log B\\ \hline
\{A,B\}&\log N+O(1)&\log N+O(1),\\
\{B,2A\}&\log N+O(1)&2\log N+O(1).
\end{array}
\tag{6.1}
\]

For each proper-linkage jump, whose inactive coordinate remains bounded,
the factorial increment therefore satisfies

\[
 \Delta{\cal F}_\ell
   =\Delta H_w\log N+O(1).
\tag{6.2}
\]

Summing over at most \(K\) proper-linkage macrotransitions and the
geometrically bounded internal top reactions, using the audited \(O(1)\)
expected corrected-factorial cost of the intervening whole shell, and
applying (5.2), gives

\[
 {\mathbb E}\Delta{\cal F}_\ell
 \le-\delta\log N+O(1).
\tag{6.3}
\]

The shell-interior failure probability is super-polynomial, while the
factorial oscillation on the finite shell is polynomial times \(\log N\);
its contribution is \(o(1)\). The \(O(N^{-1})\) priority-interruption event
has bounded workload jump and contributes \(O(\log N/N)\).

Thus the scale-corrected priority block supplies exactly the common-potential
episode required by the physical entropy gluing lemma.

## 7. Regression boundary

As a finite check, all 300 directed Hamilton-cycle orientations of the
sixteen dormant proper supports were tested in the singular priority
macrochain. The only twelve orientation rows with a closed nonservice state
are the Hamilton cycles on the two disabled supports

\[
 \{C,2C,AC,BC\}
\tag{7.1}
\]

at \(C=0\), where no proper source is physically enabled. Every non-disabled
orientation has no reachable closed service-free macroclass.

This enumeration is only a regression. The arbitrary-strong-orientation
proof is the closed-subset argument in Sections 3--4.
