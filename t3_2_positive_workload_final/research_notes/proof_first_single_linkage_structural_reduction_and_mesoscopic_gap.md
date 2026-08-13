# Structural reduction for the three-species single-linkage branch

**Proof-first note, 2026-08-12 PDT.  Status: partial theorem; carrier lemma
open.**  This note gives a non-enumerative classification of every failure
of the Anderson--Cappelletti--Kim source/deterministic-tier inclusion in a
classwise reduced binary network with one weakly reversible linkage and at
most three dynamic species.  It also states the exact physical stopped
lemma which would finish the branch.  The classification proves that the
missing theorem cannot be reduced only to one-active faces: a full-rank,
two-active counterexample to that reduction is exhibited below.

This is not a counterexample to positive recurrence.  The exceptional
two-species face is already closed by
`proof_first_single_linkage_2d_exception_service_theorem.md`.  Section 5
closes the balanced three-species carrier, and Section 6 isolates the
remaining separated-scale carrier problem.  No atlas, pair, or global
certification flag is changed here.

## 1. Reduced classwise setting

Fix a closed irreducible population class and perform the exact reduction
used in `proof_first_global_t3_2_classwise_composition.md`: delete constant
coordinates, delete linkages with no enabled source on the class, and merge
projected linkages which share a projected complex.  Suppose that the
remaining network has one strongly connected linkage, positive fixed rate
constants, at most three dynamic species, and complexes of molecularity at
most two.

Let \(x_n\) be a proper tier sequence in this class.  Write

\[
 D^1=T^{D,1}_{\{x_n\}},\qquad
 S^1=T^{S,1}_{\{x_n\}},\qquad
 E=\{y:x_n\ge y\hbox{ eventually}\}.                         \tag{1.1}
\]

After taking a subsequence, every bounded integer coordinate is constant
and every source is either eventually enabled or eventually disabled.

## 2. The enabled-top criterion

> **Lemma 2.1.**  Let \(D^1,D^2,\ldots\) be the deterministic tiers in
> decreasing order and let
> \[
> j_* = \min\{j:D^j\cap E\ne\varnothing\}.
> \]
> Then
> \[
>                         S^1=D^{j_*}\cap E.                   \tag{2.1}
> \]
> In particular,
> \[
>        S^1\subseteq D^1\quad\Longleftrightarrow\quad
>                         D^1\cap E\ne\varnothing .            \tag{2.2}
> \]

### Proof

For an enabled complex \(y\), stochastic mass action gives

\[
 {\lambda_y(x_n)\over (x_n\vee1)^y}
   =\prod_i{(x_{n,i})_{\underline{y_i}}
          \over (x_{n,i}\vee1)^{y_i}}\longrightarrow c_y,
       \qquad 0<c_y<\infty.                                   \tag{2.3}
\]

For a disabled source the propensity is identically zero.  Thus the
stochastic order is precisely the deterministic order restricted to the
enabled complexes, which proves (2.1) and (2.2). \(\square\)

This elementary identity locates the entire gap in the published
single-linkage argument: its tier inclusion fails exactly when **every**
top deterministic complex is disabled.  No reaction orientation enters
Lemma 2.1.

The top deterministic tier is a proper subset of the complex set.  To see
this, suppose instead that all complexes were D-equivalent.  Put
\(\ell_n=\log(x_n\vee1)\), normalize by \(\|\ell_n\|\), and pass to a
nonzero limit \(w\ge0\).  D-equivalence gives
\(w\cdot(y-z)=0\) for every two complexes and hence for every reaction
vector.  Therefore \(w\cdot x\) is constant on the fixed stoichiometric
class.  But a positive component of \(w\) belongs to a divergent coordinate,
so \(w\cdot x_n\to\infty\), a contradiction.  Strong connectivity thus
always supplies an edge from the top D-tier to its complement; the issue is
whether an enabled top source can take such an edge.

## 3. Binary shape of every obstruction

Because the classwise reduction has deleted constant species, every
divergent dynamic coordinate occurs in a complex.  Consequently

\[
                  \max_y (x_n\vee1)^y\longrightarrow\infty .  \tag{3.1}
\]

If an unavailable binary complex has a divergent deterministic monomial,
it cannot be \(0,S_i\), or \(2S_i\): disabling a pure complex forces its
monomial, computed with \(x\vee1\), to equal one.  It must therefore be

\[
                            S_i+S_j,                             \tag{3.2}
\]

with exactly one of the two populations eventually zero and the other
divergent.  Lemma 2.1 proves the following theorem.

> **Theorem 3.1 (structural obstruction theorem).**  A proper tier sequence
> of a classwise reduced binary one-linkage network violates
> \(S^1\subseteq D^1\) if and only if every member of \(D^1\) is a disabled
> mixed complex of the form (3.2).  Each such top complex contains one
> zero-population cofactor and one divergent carrier species.

This recovers the pure-multiple premise in the published theorem.  If a
pure complex \(S_i\) or \(2S_i\) is present for each divergent species,
then a disabled \(S_i+S_j\) cannot be strictly above all enabled sources:
\(S_i\) ties its divergent factor or \(2S_i\) dominates it.

There is a useful orientation distinction.  For a fixed strong graph and
top set \(K=D^1\), the one-step descending-source criterion holds exactly
when the graph contains

\[
                    y\longrightarrow z,\qquad
                 y\in K\cap E,\quad z\notin K.                 \tag{3.3}
\]

If arbitrary strong orientations on a fixed vertex support are quantified,
(3.3) is forced for every orientation precisely when \(K\subseteq E\).
Sufficiency is the first exit from \(K\).  For necessity, order a directed
Hamiltonian cycle so that a chosen disabled top vertex is the sole exit
from the consecutive top block.  This comparison explains why the
orientation-uniform direct criterion is stricter than (2.2).

## 4. Exact three-species obstruction families

Relabel a failed tier so that the zero cofactor is \(C=0\).

### 4.1 One divergent species

If only \(A\to\infty\), then every top complex is among
\(A+B,A+C\), with the displayed cofactor equal to zero.  The pure complexes
\(A,2A\) are absent.  This is the one-active carrier boundary already
targeted by the stopped service theorems in the hard-family library.

### 4.2 Two divergent species

Let \(A,B\to\infty\) and \(C=0\).  Then

\[
             \varnothing\ne D^1\subseteq\{A+C,B+C\}.          \tag{4.1}
\]

There are three symbolic regimes.

1. If \(D^1=\{A+C,B+C\}\), then \(A/B\to c\in(0,\infty)\), and
   \[
          {\cal C}\subseteq\{0,C,2C,A+C,B+C\},               \tag{4.2}
   \]
   with both mixed complexes present.  Indeed, \(A\) or \(B\) would be an
   enabled top complex, while \(2A,A+B,2B\) would dominate.
2. If \(D^1=\{A+C\}\), then \(A/B\to\infty\) and
   \[
       {\cal C}\subseteq
       \{0,C,2C,B,2B,B+C,A+C\}.                                \tag{4.3}
   \]
   Any present \(2B\) satisfies \(B^2/A\to0\); equality would make it an
   enabled top complex and divergence would contradict the chosen top.
3. The case \(D^1=\{B+C\}\) is symmetric.

If all three populations diverge, every complex is enabled and Lemma 2.1
closes the tier.  Thus (4.2)--(4.3) are the only genuinely new qualitative
faces beyond the one-active obstruction.

### 4.3 A full-rank counterexample to one-active reduction

Take

\[
       {\cal C}=\{0,C,A+C,B+C\},qquad
       0\to A+C\to B+C\to C\to0.                              \tag{4.4}
\]

The support is binary, one-linkage, weakly reversible, and has
stoichiometric rank three.  The CTMC is irreducible on
\(\mathbb Z_{\ge0}^3\).  If the four reactions are \(r_1,\ldots,r_4\), the
following executable words have the indicated net effects:

\[
\begin{array}{c|c}
r_1r_4&+A\\
r_1r_2r_4&+B\\
r_1r_2r_3&+C\\
r_1r_2^2r_3^2r_4&-A\quad(A>0)\\
r_1r_2r_3^2r_4&-B\quad(B>0)\\
r_4&-C\quad(C>0).
\end{array}                                                     \tag{4.5}
\]

Thus \(x_n=(n,n,0)\) lies in a single closed irreducible class.  Its
deterministic monomials are \(1,1,n,n\), whereas only the zero source is
enabled, so

\[
          D^1=\{A+C,B+C\},\qquad S^1=\{0\}.                    \tag{4.6}
\]

The only D-descending edge in (4.4) is disabled.  Equations (4.4)--(4.6)
disprove the proposed claim that every tier obstruction has exactly one
divergent species.  They do not disprove recurrence.

## 5. The balanced mesoscopic carrier theorem

The balanced family (4.2) can be closed without enumerating its supports or
orientations.

For a fixed \(\ell\in\mathbb R^3\), choose \(K_\ell\) so that
\[
 G_\ell(z)=K_\ell+\sum_{i=A,B,C}\log(z_i!)+\ell\cdot z\ge1,
 \qquad W_\ell(z)=G_\ell(z)^4                              \tag{5.0}
\]
on the nonnegative lattice.  The stopping rule below is independent of
\(\ell\).

> **Theorem 5.1 (balanced all-clock carrier service).**  Fix a support
> \[
>  \{A+C,B+C\}\subseteq{\cal C}
>       \subseteq\{0,C,2C,A+C,B+C\}                            \tag{5.1}
> \]
> with an arbitrary strongly connected directed graph and arbitrary positive
> fixed rates, and fix one closed irreducible class \(\Gamma\).  Fix
> \(\epsilon>0\), and suppose \(\Gamma\) contains states
> \[
>       x=(a,b,0),\qquad N=a+b,\qquad
>       a\wedge b\ge\epsilon N,                                \tag{5.2}
> \]
> with arbitrarily large \(N\).  From every sufficiently large such state
> there is an included physical stopping time \(\tau\) such that, for every
> fixed \(p,M\),
> \[
> \begin{aligned}
> \mathbb P(D^c)&\le C/N+C_{M}N^{-M},\\
> \mathbb E[(1+\lvert X_\tau-x\rvert+\tau)^p;E]&\le C_p/N,\\
> \mathbb E[(1+\lvert X_\tau-x\rvert+\tau)^p;B]&\le C_{p,M}N^{-M},\\
> \mathbb E(1+\lvert X_\tau-x\rvert+\tau)^p&\le C_p.
> \end{aligned}
> \tag{5.3}
> \]
> Here \(D\) is a net service with
> \(A_\tau+B_\tau=N-1\), \(E\) is the included first pure-source
> competitor during an open carrier window, and \(B\) is an included
> localization boundary.  For every fixed \(\ell\), the actual endpoint
> obeys
> \[
> \mathbb E_x[G_\ell(X_\tau)-G_\ell(x)]
>       \le-\log N+O_{\epsilon,\ell}(1),                         \tag{5.4}
> \]
> and
> \[
> \mathbb E_x[W_\ell(X_\tau)-W_\ell(x)+\tau]
>       \le-cG_\ell(x)^3\log N.                                 \tag{5.5}
> \]
> All constants may depend on the fixed support, reaction graph, rate
> constants, \(\epsilon,p,M,\ell\), as applicable, but not on \(a,b,N\).

### Proof

If \(0\notin{\cal C}\), no source is enabled on \(C=0\), so such a state is
static and its irreducible class is a singleton, contrary to the hypothesis.
Suppose \(0\in{\cal C}\).  Put

\[
 {\cal K}=\{A+C,B+C\},\qquad
 {\cal P}={\cal C}\cap\{C,2C\}.                                \tag{5.6}
\]

If \({\cal P}=\varnothing\), every reaction preserves
\(A+B-C\), because that linear functional is zero on every complex in
\(\{0,A+C,B+C\}\).  On \(C=0\), \(A+B\) is therefore fixed by the
stoichiometric class, again excluding (5.2) along a divergent fixed-class
sequence.  Hence a relevant balanced face has \({\cal P}\ne\varnothing\).

Construct an auxiliary attempt as follows.  At \(C=0\), retain the actual
first \(0\)-sourced reaction.  While \(C>0\), retain only reactions sourced
in \({\cal K}\).  Stop the attempt when either \(C=0\) with no net loss of
\(A+B\), or \(A+B=N-1\).

During this auxiliary attempt an internal \({\cal K}\)-to-\({\cal K}\)
reaction preserves both \(C\) and \(A+B\).  A
\({\cal K}\)-to-\(\{0,C,2C\}\) exit lowers \(A+B\) by one.  The launch
raises \(A+B\) by zero or one.  Consequently a pure launch followed by one
mixed exit is a service.  A mixed launch followed by a positive-pure exit
and one further mixed exit is a service.  A mixed launch followed by an
exit to \(0\) is a neutral attempt and restarts at \(C=0\).  Before service
or neutral return there are at most two mixed exits and

\[
                              1\le C\le3.                        \tag{5.7}
\]

Localize when the total number of internal mixed reactions and neutral
attempts first reaches

\[
                         L_N=\lfloor N^{1/4}\rfloor,            \tag{5.8}
\]

including the causing reaction.  Before this cutoff,
\(A\wedge B\ge\epsilon N/2\) for all large \(N\).  At every open state the
aggregate mixed rate is therefore at least \(c_\epsilon NC\).
Strong connectivity supplies an edge from the proper block \({\cal K}\)
to its complement.  Since both mixed populations are at least
\(\epsilon N/2\), the conditional probability that the next mixed firing
leaves \({\cal K}\) is bounded below by a fixed
\(\delta_\epsilon>0\).  Thus the number of internal mixed firings has a
geometric tail.

There is also a fixed positive probability of a successful attempt.  If an
outgoing \(0\)-edge has target in \({\cal P}\), its fixed launch probability
already gives this.  Otherwise, strong connectivity of the full support
forces an edge from \({\cal K}\) to \({\cal P}\); its conditional
probability is bounded below by the same balanced-population comparison.
Hence the number of neutral attempts is geometric with a fixed parameter.
It follows that the auxiliary history length has an exponential tail and

\[
              \mathbb P\{\hbox{auxiliary length}\ge L_N\}
                       \le C e^{-cL_N}.                         \tag{5.9}
\]

Restore every physical clock.  By (5.7), the total propensity of sources
in \(\{0,C,2C\}\) during an open window is bounded above by a constant,
whereas the mixed propensity is at least \(c_\epsilon N\).  The exact
race probability of a pure-source competitor is therefore \(O(N^{-1})\)
per mixed race.  Stop at and include its actual firing.  Summing this bound
over the exponentially-tailed auxiliary history, with any fixed polynomial
bias in the history
length and centered endpoint displacement, proves the second line of
(5.3), while (5.9) proves the third.  At \(C=0\), each neutral attempt waits
an exponential time with the fixed aggregate \(0\)-source rate; open waits
are faster than an exponential clock of rate \(c_\epsilon N\).
Geometric-sum moment formulas prove the last line of (5.3).  The first line
then follows from the exhaustive clean-service/defect/boundary partition.
All estimates are for the actual post-jump endpoint.

For definiteness the event labels are applied in the order: included
pure-source competitor \(E\), localization boundary \(B\), then clean
service \(D\).  In fact the causing reactions make these events disjoint,
but this priority removes any convention at a simultaneous bookkeeping
threshold.

On \(D\), put \(\Delta_A=A_\tau-a\) and
\(\Delta_B=B_\tau-b\).  Then

\[
          \Delta_A+\Delta_B=-1,\qquad
          \mathbb E(1+|\Delta_A|+|\Delta_B|)^p\le C_p.          \tag{5.10}
\]

Because \(a,b\asymp_\epsilon N\), the factorial finite difference and
(5.10) give

\[
 \log{A_\tau!B_\tau!\over a!b!}
   =\Delta_A\log a+\Delta_B\log b+O_\epsilon(1+|\Delta|^2/N)
   \le-\log N+O_\epsilon(1+|\Delta|).                           \tag{5.11}
\]

The terminal \(C\)-population is bounded by three on the clean event.
The fixed linear correction has increment \(O_\ell(|\Delta|+1)\).
The defect contribution to every fixed moment of \(\Delta G_\ell\) is
\(O(N^{-1}(\log N)^p)\), and the boundary contribution is smaller than
every power by (5.9).  Equations (5.10)--(5.11) prove (5.4) and

\[
                     \mathbb E|\Delta G_\ell|^p
                             \le C_p(\log N)^p.                  \tag{5.12}
\]

Finally \(G_\ell(x)\asymp N\log N\).  Insert (5.4) and (5.12) in the exact
fourth-power identity.  Its quadratic, cubic, and quartic remainders are
lower order than \(G_\ell(x)^3\log N\), and the bounded duration moments
are lower order as well.  This proves (5.5). \(\square\)

The proof uses only the block structure in (5.6), strong connectivity, and
the balanced cone in (5.2).  It does not inspect an orientation list or
select one prescribed physical reaction word.

## 6. The exact missing stopped theorem

The structural theorem and Theorem 5.1 leave only the separated-scale
families (4.3) and its symmetric counterpart.  It is important not to
overstate the missing estimate.  In particular, requiring order \(a+b\)
clean services with probability \(1-O((a+b)^{-1})\) is neither needed for
Foster drift nor justified: an \(O(a^{-1})\) clock accumulated through
order \(a\) windows need not remain rare.

Here is the exact sufficient random-time contract.  It deliberately puts
all physical clocks into the stopped kernel rather than declaring a
``first defect'' to be negligible.

> **Separated-scale carrier contract (open).**  Fix a binary support in
> (4.3), an arbitrary strongly connected reaction graph, arbitrary positive
> fixed rates, and one closed irreducible class.  Let
> \[
> x_n=(a_n,b_n,0),\qquad a_n,b_n\to\infty,\qquad
> {b_n\over a_n}\to0,                                         \tag{6.1}
> \]
> be actual states in that one class.  If \(2B\) is a complex, also
> \[
>                         {b_n^2\over a_n}\longrightarrow0.   \tag{6.2}
> \]
> For every fixed \(\ell\in\mathbb R^3\), put
> \[
> G_\ell(x)=K_\ell+\sum_i\log(x_i!)+\ell\cdot x\ge1,
> \qquad W_\ell=G_\ell^4.                                    \tag{6.3}
> \]
> There must exist one statewise stopping rule \(x\mapsto\tau_x\) on this
> chart, independent of \(\ell\).  It is all-clock and finite almost surely,
> and its terminal state is the actual post-reaction state (every
> service, return, promotion, and localization cutoff includes the reaction
> which first crosses it).  Along every sequence (6.1)--(6.2) there is a
> function \(h_n\to\infty\) such that, with \(\tau_n=\tau_{x_n}\),
> \[
> \mathbb E_{x_n}
>   [W_\ell(X_{\tau_n})-W_\ell(x_n)+\tau_n]
>       \le-c_\ell G_\ell(x_n)^3h_n .                          \tag{6.4}
> \]
> The same physical rule for \(\tau_x\) must work for every fixed \(\ell\)
> (only the harmless constants may depend on \(\ell\)), and, for every
> fixed \(p\), it must have uniform polynomial endpoint and duration
> integrability
> \[
> \mathbb E_{x_n}
>   (1+|X_{\tau_n}-x_n|+\tau_n)^p
>       \le C_p(1+a_n+b_n)^{q_p}.                              \tag{6.5}
> \]
> A terminal cofactor-free promotion may instead be handed to an already
> proved drift chart, but only at its actual post-jump endpoint and with its
> elapsed time retained.  A cutoff crossed with \(C>0\) is an open boundary
> and must be estimated inside (6.4), not contracted to a fictitious return.
> If the cofactor-free trace cannot produce positive net old service, the
> alternative conclusion must be an exact class invariant/no-history
> statement or containment in the finite classwise target.

The service count in a prospective proof is canonical.  In (4.3) the only
complex containing \(A\) is \(q=A+C\).  If \(N_q^{\rm in}(t)\) and
\(N_q^{\rm out}(t)\) count actual reactions entering and leaving \(q\),
then
\[
 N_q^{\rm out}(t)-N_q^{\rm in}(t)=a-A_t.                     \tag{6.6}
\]
Thus a \(K\)-service boundary is the physical hitting time
\(A_t=a-K\), including the \(q\)-sourced firing which hits it; no marked or
virtual service is required.  A useful candidate kernel follows the exact
chain until this boundary, a physical landing at \(C=0\) where an enabled
base monomial becomes comparable to \(A_t\) (promotion), or an included
open localization boundary.  The theorem does **not** prescribe that
\(K\) grow with \(a\); a fixed or state-dependent \(K\) is admissible if
the direct drift (6.4) holds.

There is already an exact invariant/service dichotomy; the gap is not
service accessibility.  Put
\[
 {cal F}={\cal C}\cap\{0,B,2B\},\qquad
 {cal P}={\cal C}\cap\{C,2C,B+C\}.                           \tag{6.7}
\]
Every member of \({\cal F}\) is enabled for all large \(b\).  If
\({\cal F}=\varnothing\), the cofactor-free state has no enabled source and
its closed class is a singleton, so it cannot realize (6.1).

> **Lemma 6.1 (invariant or physical service).**  Suppose
> \({\cal F}\ne\varnothing\).  If
> \({\cal P}=\varnothing\), then \(A-C\) is an exact stoichiometric
> invariant, so a cofactor-free state in one fixed class has fixed \(A\)
> and cannot realize (6.1).  If \({\cal P}\ne\varnothing\), then from every
> sufficiently large cofactor-free state there is an executable physical
> reaction history of length at most \(|{cal C}|+1\), ending with its
> causing reaction, for which \(A\) has net change \(-1\).

Indeed, in the first case every complex is in \({\cal F}\cup\{q\}\), and
the functional \(A-C\) is zero on all of them.  In the second case choose
an enabled \(f\in{cal F}\) and a simple directed path from \(f\) to
\({\cal P}\).  A directed complex path is physically executable: after
each firing its target complex is present and enables the next source.
Stop the simple path at its first \({\cal P}\)-vertex.  Before that vertex
the path visits \(q\) at most once.  Entries to and exits from \(q\) cancel
in \(A\), while the terminal \({\cal P}\)-state contains a carrier but no
extra \(A\).  Fire a nonself outgoing \(q\)-reaction; it is enabled by the
old \(A\) and the carrier, and it lowers \(A\) by one.  This proves the second
alternative.  The lemma selects no orientation-specific word in the
theorem: it uses only a simple path in an arbitrary strong graph to prove a
uniform finite accessibility fact.

Two features prevent importing Theorem 5.1 or the existing one-active
theorem verbatim.

1. The second cloud coordinate need not be subpower relative to the first.
   The tier assumptions give only \(B/A\to0\), and, when \(2B\) is present,
   \(B^2/A\to0\).
2. The complexes \(B,2B,B+C\) can generate a quadratic countable base
   trace before an \(A+C\) service window.  A crude endpoint estimate loses
   several factors of \(\log B\).  Those losses cannot be paid merely from
   \(-\log A\) when, for example, \(B=A^{0.49}\).

The scale condition does pay every *individual* source-to-target entropy
gap.  For example an \(A+C\to 2B\) firing contributes
\(-\log(A/B^2)+O(1)\), which tends to \(-\infty\).  The unresolved point is
to retain this sourcewise payment through the killed base Green kernel.
A path such as
\[
                  0\longrightarrow B+C,qquad A+C\longrightarrow2B
                                                                    \tag{6.8}
\]
has raw endpoint change \((-1,+3,\ast)\); bounding only its endpoint would
charge \(3\log B\), although the initiating zero-source event is suppressed
relative to the quadratic base clock when that clock is present.  The
needed proof must preserve this propensity weight rather than take a
worst-case displacement.

Consequently the precise analytic obstruction is a sourcewise killed
Green/Feynman--Kac estimate, uniform in the full mesoscopic range (6.1)--
(6.2), which controls the positive factorial endpoint and physical duration
while preserving the logarithmic source/target ratios.  A direct
fluid-scale random-time estimate for the entire carrier trace would be an
equivalent replacement.  A selected reaction word or an
orientation-dependent finite population search cannot establish (6.4).

## 7. Conditional classwise composition

Assume the separated-scale carrier contract.  Every divergent proper tier
sequence is then treated as follows.

* If \(D^1\cap E\ne\varnothing\), use the published source/D-tier theorem
  or the direct generator estimate.
* If every top-D complex is disabled and only one species diverges, use the
  existing one-active carrier theorem (including its no-history
  alternative).
* If two species diverge, Theorem 3.1 and Section 4 put the sequence in
  (4.2) or (4.3).  Theorem 5.1 treats (4.2), while (6.4)--(6.5) treat
  (4.3).
* If all three diverge, every source is enabled and the first case applies.

All branches use the same physical factorial-linear fourth power.  Exact returns may be
contracted only analytically; their elapsed time, internal boundary hits,
and actual endpoint are retained in the stopped estimate.  Reclassification
therefore has zero comparison toll.  The compactness and random-time Foster
argument in Sections 5--7 of
`hard333_common_w_fixed_class_theorem.md` then gives finite mean hitting time
of a finite target and positive recurrence on the closed class.

Without (6.4)--(6.5), that composition is conditional.  The structural
classification and balanced carrier theorem are complete, but the
three-species one-linkage branch is not.
