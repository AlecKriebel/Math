# The post-rank-one one-active repair

## 1. Scope and status

This note treats only the 92 pairs left out of the 141-pair theorem in
*rank_one_no_promotion_pair_branch.md*. They have 272 affine-feasible
one-active failed flags. The finite classification, arbitrary-orientation
zero-contest lemma, corrected-factorial endpoint, and pair-level composition
below have passed independent audit. None uses the false uniform old-debt
lemma.

The mechanism is simpler than the universal reflected-debt proposal. On
these 92 pairs, every nonfrozen one-active face has a physical priority
episode with net active reward \(-1\). A lower-source clock is used only
when no active-source clock is enabled. Thus an unresolved positive reward
requires at least one slow-before-fast contest, whereas service requires no
such contest. Nested entries do not invalidate this ordering.

This is a scoped branch, not a theorem for T3-2. In particular, none of the
1,227-pair one-active flags outside this post-rank-one intersection is
included.

## 2. Exact support partition

Relabel the active species as \(X=C\), and quotient the exchange of the two
inactive species \(A,B\). The 272 rows have twelve top/cap profiles and
exactly two support forms.

### Family I: an inactive quadratic linkage (200 rows)

The first linkage is one of

\[
 \{2A,2B\},\quad \{2A,AB\},\quad \{2B,AB\},\quad
 \{2A,2B,AB\}.                                      \tag{2.1}
\]

It preserves \(M=A+B\). The other linkage has active-degree-one set

\[
 K=\{AC,BC\}\quad\hbox{or}\quad K=\{C,AC,BC\},       \tag{2.2}
\]

and its remaining vertices form a nonempty subset of \(\{0,A,B\}\). If
\(C\notin K\) and \(0\) is present, that same linkage also contains \(A\)
or \(B\).

### Family II: a mixed reversible kill (72 rows)

The first linkage is exactly

\[
 \{2A,AC\},                                           \tag{2.3}
\]

and is therefore reversible in every strong orientation. The second
linkage has active set \(\{BC\}\) or \(\{C,BC\}\), while its lower vertices
are a nonempty subset of

\[
 \{0,A,B,2B,AB\}.                                    \tag{2.4}
\]

If \(C\) is absent and \(0\) is present, (2.4) contains a nonzero vertex.

At the displayed capped face the split is

\[
\begin{array}{c|r}
\text{case}&\text{rows}\\ \hline
\text{an active source is already enabled}&230\\
\text{only the zero-source seed starts the priority word}&32\\
\text{no source is enabled}&10.
\end{array}                                           \tag{2.5}
\]

The executable certificate is *src/one_active_kinetic_depth.py*.

## 3. The arbitrary-orientation zero-contest lemma

Fix any strongly connected directed reaction graph on each displayed
linkage and positive rates. Call a finite physical word *zero-contest* if
it never fires a lower-source reaction while an active-source reaction is
enabled.

> **Lemma 3.1.** From every state on one of the 272 faces, exactly one of
> the following holds.
>
> 1. There is a zero-contest word with net active reward \(-1\).
> 2. No reaction is enabled; the state belongs to a singleton closed class
>    and \(X\) is classwise fixed.

### Proof

Suppose first that an active complex \(k\) is enabled. In its linkage,
strong connectivity gives a simple directed path from \(k\) to a lower
complex. Truncate at the first lower target. Every source before the last
edge is active. Starting from the actual physical copy of \(k\), the usual
residual-plus-current-complex lift enables the whole path. Its active
reward is \(-1\), so it is a zero-contest service word.

It remains to consider a state with no enabled active complex. In both
families the active set contains complexes with cofactors \(A\) and \(B\),
so this forces \(A=B=0\); pure \(C\) is absent. The quadratic linkage in
(2.1) and the reversible linkage (2.3) are then disabled.

If \(0\) is absent, every remaining source contains an inactive molecule.
No reaction is enabled, giving alternative 2. If \(0\) is present, the
support classification supplies a nonzero lower vertex \(j\) in the same
mixed linkage. Choose a simple directed path from \(0\) to \(j\). Follow
its lower part only while no active source is enabled. If a lower target
first creates a cofactor, the first paragraph supplies service. If the
path first enters the active set, follow its active segment to the first
lower target. The entry and exit cancel. Simplicity prevents that lower
target from being \(0\), so it retains a cofactor; the first paragraph then
supplies one surplus exit. All lower steps occurred with no active clock
enabled. This proves alternative 1. \(\square\)

The argument permits missing reaction edges and uses only strong
connectivity. In particular, it is not an inference from Hamilton-cycle
orientations.

## 4. Kinetic-depth consequence

Let \(N=X\), and assign a cost of one to a lower-source reaction fired while
an active-source clock is enabled, and cost zero to every other reaction.
For a prescribed finite word, this is its power of \(N^{-1}\), up to
subpower inactive cofactors.

> **Corollary 4.1.** On every nonfrozen row, old-debt service has minimum
> contest depth zero. Every finite word which starts with zero reflected
> debt, ends with positive reflected debt at a state with no active clock,
> and does not first decrease \(H=X-D\), has contest depth at least one.

Indeed, at zero contest depth every lower-to-active entry immediately
enables its active target. Before another lower edge can fire, an active
path must end at a lower complex; that exit cancels the entry or creates a
surplus negative reward. Lower-to-lower and active-to-active reactions
have zero active reward. Hence a zero-contest path cannot leave unresolved
positive debt at its next inactive base.

The finite regression additionally enumerates every failing directed
Hamilton-cycle orientation pair. There are 2,660 such orientation pairs.
Among the finite creation words in the certified box, all service depths
are zero and all creation depths lie in \(\{1,\ldots,8\}\); no row has
creation depth at most service depth. This numerical statement is only a
regression for Lemma 3.1, not its proof.

## 5. Corrected-factorial endpoint

Let

\[
 {\cal F}_*(x)=\sum_i\log(x_i!)+\ell_*\mathbin{\cdot}x       \tag{5.1}
\]

be the same rate-corrected potential selected by the unique rank-one top
linkage in *rank_one_corrected_factorial_endpoint.md*. Consider a
one-active source-rate sequence with \(X=N\to\infty\).

Section 8.1 of *global_atlas_interface_closure.md* proves that a coordinate
has positive weight in the refined rational flag exactly when its
population tends to infinity. Consequently a genuinely one-active
subsequence has both inactive coordinates bounded. Passing to a
subsequence fixes their two exact integer values. If an inactive coordinate
diverges, even subpower relative to \(N\), the sequence has at least two
active coordinates and belongs to the already audited rank-one
multi-active theorem. This deterministic subsequence split is not
tightness implying finite support.

> **Lemma 5.1 (priority endpoint).** On each of the 262 nonfrozen rows
> there is a physical stopping time \(\tau_N\), ending at the service word
> of Lemma 3.1 or at the first lower interruption of an enabled active
> phase, such that
> \[
>  {\mathbb P}\{\hbox{lower interruption}\}=O(N^{-1}),
>  \qquad \sup_N{\mathbb E}\tau_N<\infty,                \tag{5.2}
> \]
> and
> \[
>  {\mathbb E}\!\left[{\cal F}_*(X_{\tau_N})
>                    -{\cal F}_*(X_0)\right]
>       =-\log N+O(1).                                  \tag{5.3}
> \]

### The countable active phase

Strip the common active molecule from \(C,AC,BC\). Before the first active
exit, the phase is a unimolecular immigration/conversion chain on
\(\{0,A,B\}\), run on the \(N\)-clock. In Family II the additional vertex
\(AC\) has the direct active exit \(AC\to2A\). Every sink component of the
retained active graph has an edge to the killed lower set; otherwise the
original linkage would not be strongly connected.

Starting from the fixed inactive state selected above, this killed linear
chain has an \(N\)-independent law after the time change \(s=Nt\), finite
exponential endpoint moments, and an integrable killed duration. Here is a
direct proof which includes open phases. Retained reactions among
\(\{0,A,B\}\) are immigrations, deaths, and conversions; there is no
branching. Use the standard independent-particle construction: every
initial or immigrant particle follows a finite-state conversion/death
chain, and zero-source immigrations are independent Poisson processes.

If \(0\) is absent, total particle number is fixed and positive. Strong
connectivity gives every particle type a path with positive probability to
a killing edge in a fixed scaled-time block. Hence the first killed
particle has an exponential time tail. If \(0\) is present, either its
active edge is itself a killing edge or strong connectivity gives a
positive-rate immigration/conversion route to one. Every resulting
particle has a fixed positive probability to reach a killing edge before
it dies. Thinning the immigration process again gives an exponential tail,
including from the empty state. The number of immigrants before that
exponential time has an exponential moment. Thus the total population at
the killed endpoint has an exponential moment. This argument is uniform
from the fixed finite set of initial inactive states selected on the
subsequence.

The same construction, including the geometric number of seed trials,
gives for every fixed \(q\)

\[
 {\mathbb E}\int_0^{\widehat\tau}
 (1+|E_s|)^q\{1+\log(1+|E_s|)\}\,ds<\infty,            \tag{5.4a}
\]

where \(E_s\) is the stripped phase on scaled time and
\[
 \widehat\tau:=\sum_jN(\beta_j-\alpha_j)
\]
is the sum of the scaled lengths of the concatenated active windows
\([\alpha_j,\beta_j]\); lower-only waiting intervals are not included.
This occupation estimate, rather than endpoint moments alone, controls the
size-biased lower-interruption law.

It follows directly from (5.1) that

\[
 \sup_N {\mathbb E}\left[
  \left|\Delta{\cal F}_{*,\mathrm{inactive}}\right|
  \ ;\ \hbox{priority phase}\right]<\infty .            \tag{5.4}
\]

No finite phase box is asserted: the open unimolecular endpoint is
countable, and (5.4) follows from its exponential moment.

### Lower interruptions and the active reward

Every lower propensity is a polynomial of degree at most two in the
inactive phase. The occupation bound (5.4a) gives

\[
 {\mathbb E}\int_0^{\tau_N}
   \lambda_{\rm lower}(X_s)\,
   {\bf1}_{\{\text{an active clock is enabled}\}}\,ds
 \le {C\over N}.                                      \tag{5.5}
\]

Hence the first assertion of (5.2) follows from the compensator formula.
A lower interruption has one bounded population jump; (5.4) and the
factorial jump identity make its expected positive cost
\(O((\log N)/N)=o(1)\). On the complementary priority episode, the net
active change is exactly \(-1\), and hence

\[
 \log((N-1)!)-\log(N!)=-\log N.                        \tag{5.6}
\]

Equations (5.4)--(5.6) prove (5.3). The lower-only seed part has finite
geometric moments: a fixed simple path from \(0\) to its nonzero lower
vertex has positive rate-dependent probability, and every return to \(0\)
restarts the same trial. Waiting at a no-fast state is bounded by an
exponential clock with a fixed positive rate; retained active windows take
only \(O(N^{-1})\) mean physical time. A lower competitor which fires while
no active clock exists is part of the finite seed chain, rather than an
omitted interruption; a competitor which fires during an active phase is
charged by (5.5). Hence the full duration and endpoint are uniformly
integrable, proving (5.2) and Lemma 5.1.

## 6. Pair-level composition

The 92 pairs already have the following audited common-potential facts.

1. Every feasible failure with at least two active coordinates is handled
   by the common \({\cal F}_*\) theorem for the 233 no-promotion rank-one
   pairs.
2. Every passing source-rate sequence remains Anderson--Kim descending
   after the fixed linear correction.
3. The rank-one mask, hence \(\ell_*\), is the same in every multi-active
   phase of a fixed pair.

Lemma 5.1 supplies the missing one-active alternative with the same
potential. The ten frozen rows are singleton closed classes, not divergent
return obstructions. Every sequence with an unbounded inactive coordinate,
including subpower divergence, is a refined multi-active flag by (8.6) of
*global_atlas_interface_closure.md*. Thus every divergent sequence in a
fixed non-singleton closed class has either generator drift tending to
\(-\infty\) or a physical \({\cal F}_*\)-episode with expected drift tending
to \(-\infty\).

The common-potential gluing theorem then gives a finite exceptional set;
nonexplosion is the same affine pure-birth comparison used for the
141-pair branch. An independent replay checked the arbitrary strong-digraph
path contraction, the countable killed-linear endpoint and occupation
moments, the exact refined-weight split, the common correction, frozen
classes, and the classwise gluing. Consequently the argument extends that
branch from 141 to all 233 no-promotion rank-one pairs.

The executable certificates set the local analytic and exact 92-pair
recurrence flags true. Global T3-2 remains false.

## 7. Reproduction

Run

    PYTHONPATH=src python3 -B src/one_active_kinetic_depth.py
    PYTHONPATH=src python3 -B -m unittest \
      tests/test_one_active_kinetic_depth.py -v
