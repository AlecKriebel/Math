# One-active physical phase: certified local lemmas and the remaining kernel

## 1. Scope and status

This note isolates the countable-phase gap at a **one-active tier**, without
replacing the inactive populations by a fixed finite phase and without
deleting lower-layer reactions.  Sections 2--4 prove the exact structural
reduction, the local actual-target carrier estimate, and the elementary
return-prefix identity.  Section 5 states the additional stopped-kernel
estimate still needed for a recurrence theorem.  That estimate is not yet
proved, so the support counts in Section 8 are candidate scope, not certified
closures.

The species are denoted by \(X,U,V\), with \(X\) the active species.  Complexes
have molecularity at most two, there are at most two linkage classes, the
directed graph of each nontrivial linkage is strongly connected, and every
rate constant is strictly positive.  The two linkage supports are disjoint.
Mass-action propensities use falling factorials.

A one-active tier sequence means

\[
 X_n\longrightarrow\infty,
 \qquad U_n=u,\qquad V_n=v
 \tag{1.1}
\]

after passage to a subsequence.  The constants \(u,v\) may be arbitrary.
The caps \(0,1,2\) in the finite atlas mean respectively \(0,1,\geq2\);
an integer coordinate which is bounded along a tier sequence is eventually
constant.  If \(U_n\) or \(V_n\) is not bounded, it is promoted to the active
set and belongs to a different descriptor.  Thus (1.1), rather than an
assumed finite support for a limiting distribution, is the exact use of a
one-active descriptor.

The intended interface result is the following.

**Candidate Theorem 1.1 (one-active physical-phase interface).**  Fix a
support pair and arbitrary strongly connected orientations and positive
rates.  Suppose that every **affine-stoichiometrically feasible** failed tier
descriptor for the pair has exactly one active coordinate.  Then every
closed irreducible class of the physical CTMC is positive recurrent.

The candidate theorem follows from the stopped-kernel hypotheses stated in
Proposition 5.1 and the gluing hypothesis in Section 6.  The present note
does not prove those hypotheses from weak reversibility alone.

More locally, for each one-active failed descriptor exactly one of the
following occurs.

1. The active coordinate is an exact affine invariant.
2. A mixed linkage supplies a physical service episode.  Its top part is a
   killed unimolecular process on the two inactive species.  Every positive
   \(X\)-arrival is either cleared on the \(X\)-clock or recorded as scalar
   unresolved debt.  Weak-reversibility return prefixes clear that debt with
   a uniform physical-time margin.
3. An inactive population or its polynomial occupation is not uniformly
   controlled.  It is retained as a promotion to a descriptor with at least
   two active coordinates.

In alternative 2 the episode duration and endpoint have all polynomial
moments required by random-time Foster.  Alternative 3 is not a truncation
error: the promoted state and every reaction used to reach it remain in the
physical chain.

The hypothesis that all failed descriptors are one-active is load-bearing.
This note does not claim to close a pair which also has an unresolved
two- or three-active descriptor.

## 2. Exact active-degree decomposition

Write \(a(y)=y_X\).  At a one-active tier, a complex with \(a(y)=2\) is the
unique highest \(X\)-degree complex.  It is enabled.  Strong connectivity of
its linkage forces an edge from it to a complex of smaller \(X\)-degree, so
the source is a top-S descending source.  Consequently a failed one-active
descriptor contains no \(2X\) complex.

It follows that

\[
 a(y)\in\{0,1\}
 \quad\hbox{for every network complex},
 \tag{2.1}
\]

and the complete active-degree-one menu is

\[
 \mathcal H_X=\{X,\,X+U,\,X+V\}
              =X+\{0,U,V\}.
 \tag{2.2}
\]

Every reaction is therefore of exactly one of four types:

\[
\begin{array}{c|c|c}
\text{source degree}&\text{target degree}&\Delta X\\ \hline
1&1&0\\
1&0&-1\\
0&1&+1\\
0&0&0.
\end{array}
\tag{2.3}
\]

Call the second type an **exit**, the third an **entry**, and the other two
internal.  This terminology is exact; in particular there is no reaction
which raises \(X\) at active order.

If, for each linkage \(L\), either \(L\subseteq\mathcal H_X\) or
\(L\cap\mathcal H_X=\varnothing\), then \(a(y)\) is constant on every
linkage.  Hence

\[
 X(t)=X(0)
 \tag{2.4}
\]

reaction by reaction.  This is the flat-top invariant alternative.

Otherwise a linkage is **mixed**: it contains both active-degree-one and
active-degree-zero complexes.  Strong connectivity gives, from every
 \(y\in L\cap\mathcal H_X\), a directed path to \(L\setminus\mathcal H_X\).
The first edge of that path leaving \(\mathcal H_X\) is an exit.  Also every
entry belongs to a mixed linkage, and its actual target is an enabled member
of \(\mathcal H_X\).  No future activation is conditioned upon.

## 3. The killed unimolecular carrier

Factor \(X\) from (2.2).  Before the first exit, \(X=N\) is constant and all
top reactions have the form

\[
 0\longrightarrow U,\quad 0\longrightarrow V,\quad
 U\longrightarrow0,\quad V\longrightarrow0,\quad
 U\longleftrightarrow V,
 \tag{3.1}
\]

with every propensity multiplied by \(N\).  Edges from a top complex to a
lower complex are killing edges.  Thus the top process is a possibly killed
unimolecular process on \(\{0,U,V\}\), run on the fast clock \(s=Nt\).

The following estimate is the analytic core.

**Lemma 3.1 (actual-target carrier estimate).**  Let an entry have just
produced an actual target in a mixed linkage, or let an already enabled top
complex of a mixed linkage be marked.  Put \(M=U+V\).  There are constants
\(C_p,q_p<\infty\), depending only on the network and \(p\), and a stopping
time \(\sigma\), such that, until the first lower-source interruption,

\[
 \mathbb P(\hbox{no exit by }\sigma)
 \le {C_1(1+M_0)^{q_1}\over N},
 \tag{3.2}
\]

\[
 \mathbb E\sigma^p
 \le {C_p(1+M_0)^{q_p}\over N^p},
 \qquad
 \mathbb E(1+M_\sigma)^p
 \le C_p(1+M_0)^p.
 \tag{3.3}
\]

The event on the left of (3.2) includes every lower-layer reaction, rather
than silently suppressing it.

**Proof.**  Tag the zero cofactor, or one \(U\)- or \(V\)-molecule supplied
by the actual target.  Assign to the tagged molecule its ordinary
per-particle mass-action clocks.  At the stripped state \(0\), the next
top reaction sourced at \(X\) moves the tag.  At \(U\) or \(V\), a top
reaction consuming the tagged molecule moves it to its top target or kills
it at a lower target.  A physical source complex belongs to only one
linkage, so another linkage has no second copy of that source with which to
steal the tag at order \(N\).

The directed top graph, with lower targets made absorbing, is finite.  From
every one of its vertices an absorbing vertex is reachable, because the
linkage is mixed and strongly connected.  The tag's absorption time \(S\)
on the fast clock is therefore phase type.  In particular

\[
 \mathbb E S^p<\infty
 \quad\hbox{for every }p.
 \tag{3.4}
\]

Unimolecular top conversions preserve \(M\), top deaths lower it, and only
the finitely many stripped \(0\)-sources can raise it.  Consequently, up to
time \(S\),

\[
 M_s\le M_0+P_s,
 \tag{3.5}
\]

where, after increasing one network-dependent rate if necessary, \(P\) is
a Poisson process independent of \(N\).  This proves the endpoint and time
estimates in (3.3).

A lower-source propensity contains no factor \(N\).  Bimolecularity gives

\[
 \lambda_{\rm low}(U,V)\le K(1+M)^2.
 \tag{3.6}
\]

Changing variables \(s=Nt\), (3.4)--(3.6) give

\[
 \mathbb P(\hbox{a lower interruption before tag killing})
 \le {K\over N}\,
 \mathbb E\int_0^S(1+M_s)^2\,ds
 \le {C(1+M_0)^q\over N}.
 \tag{3.7}
\]

Stopping at the interruption, rather than erasing it, proves (3.2).  A
terminal lower target changes \(M\) by at most two and preserves (3.3).
\(\square\)

Along (1.1), the right side of (3.2) tends to zero.  More generally it tends
to zero along every genuine one-active flag, because a bounded inactive
coordinate is fixed after taking a subsequence.  If \(M\) is not bounded,
that is a promotion, not a failure of (3.2).

## 4. Closed, killed, or promoted countable phase

The top trace in Lemma 3.1 is countable because stripped \(0\)-sources may
immigrate cofactors.  Its recurrence properties are nevertheless exact.

**Lemma 4.1 (unimolecular trichotomy).**  For a finite reaction set on
\(\{0,U,V\}\), with killing edges retained, every communicating component
reachable from a finite initial state has one of the following forms.

1. Killing is reachable.  The tagged killing time has all moments as in
   (3.4).
2. The component is nonkilled and closed.  If it contains \(0\) and every
   immigrated species has a path back to \(0\), it has a product-Poisson law
   and exponential moments.  If it excludes \(0\), total molecule number is
   conserved and each irreducible class is finite.
3. Immigration feeds a closed species class having no path to \(0\) or to
   killing.  Then \(U+V\to\infty\) in probability along the fast trace.  In
   the atlas argument this is promotion of \(U\) or \(V\).

**Proof.**  Collapse the directed graph on the species vertices and \(0\)
into strongly connected components.  A closed component not fed by \(0\)
is conservative.  A component fed by \(0\) is stable precisely when every
fed closed species component drains to \(0\); the standard independent-
particle construction then gives the product of Poisson laws, with means
given by the finite linear traffic equations.  If a fed closed component
does not drain, immigrants accumulate there.  Killing reachable from a
tagged particle is phase type; killing from \(0\) has an exponential clock.
These alternatives exhaust the finite condensation graph. \(\square\)

This trichotomy also controls lower-layer sampling.  In a product-Poisson
class every polynomial source propensity is integrable to all orders.  In a
conservative class the state space is finite.  If neither statement applies,
the phase grows and is promoted.  Thus no conclusion here uses

\[
 \text{tightness}\quad\Longrightarrow\quad\text{finite support},
 \tag{4.1}
\]

which is false.

We next record why a lower interruption cannot create an orphaned permanent
arrival.

**Lemma 4.2 (physical return prefix).**  For every reaction \(r:y\to y'\)
in a strongly connected linkage, choose a directed path in that linkage
from \(y'\) back to \(y\).  Starting immediately after \(r\), the consecutive
targets on that path make its first source, and then every subsequent
source, physically enabled.  The combined stoichiometric increment of the
return prefix is \(y-y'\), exactly cancelling \(r\).

If a prescribed source is disturbed before its return edge fires, the
disturbing reaction and its actual target must be retained.  Iterating the
identity suggests a physical return attempt, but the identity alone does not
give an \(N\)-uniform absorption probability or a finite-moment completion
time.  Those are the stopped-kernel requirements in Proposition 5.1.

**Proof.**  If the chosen path is
\(y'=z_0\to z_1\to\cdots\to z_k=y\), then immediately after \(r\) the state
has the form \(x-y+z_0\), so \(z_0\) is enabled.  After the first return edge
it has the form \(x-y+z_1\), and induction proves the assertion.  The path
sum telescopes to \(y-y'\).

This proves the exact pathwise identity. \(\square\)

The missing inference is worth making explicit.  A closed top component has
a conservative or product-Poisson law by Lemma 4.1, but positive stationary
occupation of a lower source does not by itself supply a uniform completion
bound after arbitrary fast/slow interruptions.  One must first stop on a
finite bad cross-section, classify every closed service-free singular limit
class, and bound the number of raw entries made during one old-debt attempt.
Merely saying “there are finitely many complexes and path positions” does
not prove those facts.

The distinction in Lemma 4.2 is important.  We do not demand that a
precoloured arbitrary active particle be cleared.  A debt is created only by
an actual physical entry, and every failed attempt is continued from an
actual physical target.

## 5. Scalar unresolved debt

At the level of individual reactions, let \(D\) count entries not yet
matched by exits:

\[
 D^+=\begin{cases}
 D+1,&\Delta X=+1,\\
 (D-1)^+,&\Delta X=-1,\\
 D,&\Delta X=0.
 \end{cases}
 \tag{5.1}
\]

Start with \(D_0=0\), and set

\[
 H=X-D.
 \tag{5.2}
\]

Then, pathwise,

\[
 0\le D\le X,\qquad H\ge0,\qquad H(t)\le H(0)=X(0).
 \tag{5.3}
\]

Indeed an entry raises both \(X,D\), a matched exit lowers both, and an exit
at \(D=0\) lowers \(H\) by one.  This also proves that surplus services cannot
make the bookkeeping inconsistent.

For drift estimates one would contract a successful entry followed by its
fast exit to a zero-reward macroedge.  Only an interrupted carrier remains as
**unresolved debt**.  Lemma 3.1 proves the per-entry estimate

\[
 \mathbb P(\text{new unresolved unit}\mid\text{one entry})
 \le {C(1+m)^q\over N}
 \tag{5.4}
\]

while the inactive population is bounded by \(m\).  It does **not** by itself
bound the total number of such units produced during an old-debt return
attempt.

The exact missing statement is the following.

**Proposition 5.1 (required stopped-kernel estimate).**  Let \(E\) be a finite
inactive phase set, enlarged by the actual target and return-path position.
There should exist stopping times

\[
 \tau_0=0<\tau_1<\cdots
 \tag{5.5}
\]

which stop immediately when \(X<N_E\), when the inactive phase leaves \(E\),
or when one complete old-debt attempt ends, and constants
\(p_E>0,C_E<\infty\), such that:

1. if \(D_{\tau_k}>0\), an exit clearing one old unit occurs before
   \(\tau_{k+1}\) with conditional probability at least \(p_E\);
2. if \(J_k\) is the number of raw entries in the block, then
   \(\mathbb E[J_k\mid\mathcal F_{\tau_k}]\le C_E\), with enough higher
   moments to control nested carrier trials;
3. the expected number \(A_k\) of *new unresolved* units obeys

   \[
   \mathbb E[A_k\mid\mathcal F_{\tau_k}]
   \le {C_E\over X_{\tau_k}};
   \tag{5.6}
   \]

4. the duration and the entropy endpoint at both exits
   \(X<N_E\) and \((U,V)\notin E\) are uniformly integrable.

The constants may depend on \(E\) and the rate vector, but not on the active
level.

If Proposition 5.1 holds, choose \(N_E\) larger if necessary so that
\(C_E/N_E\le p_E/2\).  The scalar aggregate-debt inequality then gives at
successive stopped blocks

\[
 \mathbb E[D_{\tau_{k+1}}-D_{\tau_k}\mid\mathcal F_{\tau_k}]
 \le -{p_E\over2}\mathbf 1_{\{D_{\tau_k}>0\}}.
 \tag{5.7}
\]

Together with (5.3), the duration and endpoint bounds would rule out a
critical reflected-random-walk branch.

Proposition 5.1 is stronger than the local carrier Lemma 3.1.  In
particular, (5.6) requires the factor
\(\mathbb E J_k\), a bound on recursively interrupted carriers, and a proof
that an old debt created by a \(\Delta X=0\) cofactor theft can be serviced
without relying on a new net entry.  Lemma 4.2 supplies the exact reverse
path, but the present note does not yet prove the uniform probability and
moment estimates after fast/slow elimination.

## 6. Composition with the other descriptors

Let

\[
 \Phi(x)=\sum_i\bigl[x_i(\log x_i-1)+1\bigr]
 \tag{6.1}
\]

be the Anderson--Kim entropy function.

**Lemma 6.1 (finite bad cross-section).**  Fix one affine stoichiometric
class.  Suppose every affine-stoichiometrically feasible descriptor with at
least two active coordinates passes the top-S descending-source condition.
Then there is a class-dependent \(M<\infty\) such that

\[
 \mathcal L\Phi(x)\le-1
 \tag{6.2}
\]

whenever at least two coordinates of \(x\) exceed \(M\), apart from a finite
set.

**Proof.**  Otherwise choose \(x_n\) with at least two coordinates exceeding
\(n\) and \(\mathcal L\Phi(x_n)>-1\).  Pass to a tier subsequence.  At least
two coordinates are active.  Because the sequence lies in one affine
stoichiometric class, its descriptor is affine feasible.  The exact
descriptor enumeration therefore supplies a top-S descending source, and
the Anderson--Kim generator estimate gives \(\mathcal L\Phi(x_n)\le-1\) for
all sufficiently large \(n\), a contradiction. \(\square\)

Thus the generator-bad region is contained in three one-active tubes having
finite inactive cross-sections.  This finite set is obtained from a
statewise generator contradiction, not from tightness of an occupation law.
Stopping a one-active kernel at its first tube exit makes the endpoint jump
bounded.  Outside the tubes, (6.2) controls physical duration rather than
the number of fast neutral jumps.

There is also an exact marked finite-target reduction across tube switches.
Let \(I\) be the set of species occurring as the active coordinate of a
one-active failed descriptor.  For every \(i\in I\), the argument of Section
2 excludes the complex \(2i\) globally.  Define \(D_i\) by (5.1), using the
sign of the \(i\)-th reaction increment, for the entire physical path, and
put \(H_i=X_i-D_i\).  Then

\[
 0\le D_i\le X_i,\qquad H_i(t)\le X_i(0),
 \qquad i\in I,
\tag{6.3}
\]

even when the chain changes tubes.  On a return to any bad tube with every
\(D_i=0\), its active coordinate is bounded by the corresponding initial
coordinate and its other coordinates are bounded by \(M\).  These original
population states form a genuinely finite target.  This removes a possible
ambiguity in the gluing target; it does not prove simultaneous negative
drift of the debt vector.

What remains is an explicit gluing inequality.  Starting at a tube state,
one must run the stopped kernel of Proposition 5.1; after a tube exit, run
the physical chain under (6.2) until it returns to a tube or hits a finite
set.  Dynkin's formula controls the latter segment.  To invoke random-time
Foster, however, one still must prove a single inequality of the form

\[
 \mathbb E_z\!\left[
   \Phi(Z_\tau)-\Phi(z)+\eta\tau
 \right]\le-\delta
 \tag{6.4}
\]

outside a finite set, with the marked target and debt included at the tube
stopping times.  Proposition 5.1(4) is exactly the endpoint hypothesis
needed to justify this composition.  In addition one needs a vector-debt
drift estimate which remains valid under tube switching.  The local carrier
estimate and the qualitative word “promotion” do not prove (6.4).

If Propositions 5.1 and (6.4) are established, the remaining conclusion is
standard.  The chain is nonexplosive because every reaction increasing total
population has source molecularity at most one, so the total increasing
rate is affine.  Stopped Dynkin summation gives finite expected hitting time
of a finite subset of each closed irreducible class; the finite-set trace
then gives an invariant probability and positive recurrence.  Until those
two estimates are proved, Candidate Theorem 1.1 remains open.

## 7. Adversarial checks and limits

### 7.1 A closed top phase need not descend the active coordinate

If an entire linkage lies in \(\mathcal H_X\), its stripped network can be a
closed strongly connected unimolecular system.  It may have a
product-Poisson phase while preserving \(X\) exactly.  The proof therefore
does not assert strict \(X\)-descent in every phase.  It uses (2.4), or the
fact that all positive \(X\)-changes in a mixed linkage are charged to debt.

### 7.2 Fast neutral jump count is irrelevant

A conservative \(U\leftrightarrow V\) trace can make order \(N(U+V)\) jumps
per unit physical time.  Lemma 3.1 controls its physical absorption time and
the endpoint total \(U+V\); it never asks for a finite expected number of
neutral jumps.

### 7.3 Cofactor theft is not ignored

For example, after \(0\to X+U\), a lower reaction can consume \(U\) before
\(X+U\) exits.  This is exactly the event in (3.7).  Its actual target starts
Lemma 4.2.  The return-prefix identity says how restoration would occur.
The uniform old-debt completion estimate after arbitrary competing
reactions is the unproved part of Proposition 5.1.  The failed entry remains
in \(D\) until a physical exit occurs; it may not be declared cleared merely
because a later entry obtained service.

### 7.4 Why arbitrary supersets are allowed here

Every lower reaction of either linkage is included in the aggregate bound
(3.6), in the return-prefix construction, or in the good-region generator
(6.2).  Any future proof must preserve this property; recurrence of a
minimal support cannot be extended to a superset by deletion monotonicity.

### 7.5 What is not proved

The present note does not yet prove Candidate Theorem 1.1, even when all
failed descriptors are one-active.  Proposition 5.1 and the marked
random-time inequality (6.4) remain open.  The intended conclusion is
classwise positive recurrence of the physical CTMC, not recurrence of the
raw embedded jump chain.

## 8. Exact atlas interface

Let \(G(P)\) be the set of **affine-feasible** failed descriptors of a
residual ordered support pair \(P\).  Let \(\mathcal O_1\) be the 27
descriptors having exactly one positive weight coordinate.  After first
removing the 151 pairs with \(G(P)=\varnothing\), the exact candidate
selection predicate is

\[
 \varnothing\ne G(P)\subseteq\mathcal O_1.
 \tag{8.1}
\]

The exact ordered branch arithmetic is:

\[
\begin{array}{c|r|r|r|r}
\text{family}&\text{tier failures}&G(P)=\varnothing&
\varnothing\ne G(P)\subseteq\mathcal O_1&\text{remaining}\\ \hline
\text{positive invariant shield}&2312&143&1076&1093\\
\text{signed shield}&199&8&151&40\\ \hline
\text{total}&2511&151&1227&1133.
\end{array}
\tag{8.2}
\]

The 67 raw flat-top invariant pairs are contained in the first,
affine-infeasible branch: a descriptor along an exactly invariant active
axis is not affine feasible.  Therefore the unproved physical carrier/debt
kernel is needed for all 1,227 pairs in the third column of (8.2).  If
Propositions 5.1 and (6.4) are proved, the ordered affine-plus-one-active
union would contain 1,378 pairs and leave 1,133.

The fingerprints of the candidate new branch, ordered union, and remainder
are respectively

\[
\begin{array}{c|c}
\text{set}&\text{SHA-256}\\ \hline
\text{candidate one-active branch}&
\mathtt{3ab28358663c45a089a5bdf4144c28573718b0c4f8b05472a0af208ca919fcf8}\\
\text{affine plus candidate one-active}&
\mathtt{c0ed5e98dfb08bbb1fb9f48861867a8bff5b1140a78e8610f12b1d16f42366fa}\\
\text{remaining}&
\mathtt{5e5a2e8d33f98332741ce760087047c063f67c0518e698239b9de48dfac4353b}.
\end{array}
 \tag{8.3}
\]

For comparison, the earlier zero-cap-only selector was

\[
 F(P)\subseteq
 \left\{
 ((1,0,0),(2,0,0)),
 ((0,1,0),(0,2,0)),
 ((0,0,1),(0,0,2))
 \right\}.
\tag{8.4}
\]

It selects 596 positive and 151 signed pairs.  The local carrier lemma
extends unchanged to fixed inactive caps \(1\) and \(\ge2\), but the same
stopped-kernel and gluing gaps remain even at zero cap.  None of these 747
pairs is promoted to a certified recurrence branch by this note.

The zero-cap fingerprints are

\[
\begin{array}{c|c|c}
&\text{selected}&\text{remaining}\\ \hline
\text{positive}&
\mathtt{73de3c2e5cbef71de1a003b75a0c593fe7eef8e18a9d34b88c3816f0a98512e6}&
\mathtt{2c42243075a701647009d7cb9595e4ec6f4fce4e0b273be5a70649f1a13004f1}\\
\text{signed}&
\mathtt{748bce431e84296b43e9fca18982d7e6ad353ee78efbeba01570dcd9325173d4}&
\mathtt{9a3892cf865ef93a3242d20642de7dada2230f5a27737c31c976d2c9219aa68a}.
\end{array}
\tag{8.5}
\]

The 596 zero-cap positive pairs are disjoint from the 67 flat-invariant
pairs.  Their union has fingerprint

\[
 \mathtt{197d225f6354883b650ab8269adf822e2b0e34d0ff6f06197a9ce39ef488f87b}.
\tag{8.6}
\]

The arithmetic in (8.2) is the maximal candidate scope of the proposed
one-active theorem.  The smaller zero-cap arithmetic in (8.4) is useful for regression
tests only; it is not a presently certified closure count.
