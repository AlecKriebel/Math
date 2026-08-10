# One-active service requires the countable phase

## 1. Exact residual regression

Use \(A\) as the active species and \(B,C\) as the inactive species. Consider

\[
 L_0=\{A,A+C\},\qquad
 L_1=\{B,C,2B,A+B\}.
 \tag{1.1}
\]

Choose the strongly connected channels

\[
\begin{array}{c}
 A\rightleftarrows A+C,\\[1mm]
 A+B\longrightarrow C\longrightarrow B\longrightarrow A+B,
 \qquad B\rightleftarrows2B,
\end{array}
\tag{1.2}
\]

with arbitrary fixed positive rates on the displayed edges.

The ordered pair in (1.1) is a positive-shield residual pair. Its three
affine-feasible failed descriptors all have active weight \((1,0,0)\), with
\(C\)-caps \(0,1,\ge2\). It lies in the candidate
affine-plus-one-active branch.

While \(A=N\), the flat linkage gives

\[
 C\longrightarrow C+1\quad\hbox{at rate }\alpha N,
 \qquad
 C\longrightarrow C-1\quad\hbox{at rate }\beta NC.
 \tag{1.3}
\]

Thus \(C\) is an immigration--death chain run at speed \(N\), with
stationary mean \(\alpha/\beta\).

There is an actual unresolved-debt history. Starting with \(B=1\), two
occurrences of

\[
 B\longrightarrow A+B
 \tag{1.4}
\]

followed by one occurrence of

\[
 A+B\longrightarrow C
 \tag{1.5}
\]

change scalar debt by \(+1,+1,-1\). The resulting state has \(B=0\), at
least one \(C\), and one unresolved unit. This event is rare for large
\(A\), but every source is physically enabled and its probability is
positive.

Old-debt service is

\[
 C\longrightarrow B,\qquad A+B\longrightarrow C.
 \tag{1.6}
\]

After the first, slow reaction, the exit has rate of order \(A\) and beats
the competing \(B\)-source reactions with probability \(1-O(A^{-1})\).
The phase returns to \(C\), while \(A\) and debt both fall by one. Hence
(1.6) is a genuine reward \(-1\) cycle.

## 2. The fixed-box claim is false

Fix \(M\ge1\), and stop when \(C=M+1\). In fast time \(s=Nt\), let
\(\widehat C_s\) have generator

\[
 Qf(c)=\alpha\{f(c+1)-f(c)\}
       +\beta c\{f(c-1)-f(c)\},
 \tag{2.1}
\]

and put

\[
 T_M=\inf\{s:\widehat C_s=M+1\}.
 \tag{2.2}
\]

For fixed \(M\), both \(T_M\) and
\(\int_0^{T_M}\widehat C_s\,ds\) have finite expectation. Before the box
exit or \(C\to B\), the physical chain is exactly (2.1) under the time
change. If \(C\to B\) has rate \(d\), then

\[
\begin{aligned}
 {\mathbb P}(\hbox{service preparation before box exit})
 &=
 1-{\mathbb E}\exp\left\{
   -{d\over N}\int_0^{T_M}\widehat C_s\,ds
 \right\}\\
 &\le {d\over N}\,
 {\mathbb E}\int_0^{T_M}\widehat C_s\,ds
 ={K_M\over N}.
\end{aligned}
\tag{2.3}
\]

No \(p_M>0\), independent of the active level, can therefore satisfy the
service-before-box-exit assertion of Proposition 5.1 in
*one_active_physical_phase_theorem.md*. In particular,

\[
 \hbox{negative reward cycle}
 \ \not\Longrightarrow\
 \hbox{uniform service before leaving a fixed phase box}.
 \tag{2.4}
\]

The graph-theoretic coboundary statement is unaffected: weak-return paths
still turn a positive cycle in a terminal physical quotient component into
a negative reverse walk. The failure is kinetic. A positive recurrent fast
chain makes order \(N\) transitions in one unit of physical time and
eventually visits the tail outside every fixed box. Such a tail visit is not
promotion of \(C\) to an active coordinate.

## 3. Accelerated unimolecular hazards

The correct repair retains the recurrent phase.

> **Theorem 3.1 (countable accelerated hazard).** Let \(Q\) be the
> generator of a stable open unimolecular network on finitely many particle
> types, with irreducible product-Poisson law \(\pi\), and let \(Z^{(N)}\)
> have generator \(NQ\). Let
> \[
>  g(z)=\sum_j\kappa_j(z)_{y_j}\ge0,\qquad |y_j|\le2,
> \tag{3.1}
> \]
> with \(\pi(g)>0\), and let \(\tau_N\) be the first event of a Cox clock
> with intensity \(g(Z^{(N)}_t)\).
>
> There are \(T,p>0\), independent of \(N\ge N_0\) and the initial phase,
> such that
> \[
>  {\mathbb P}_z\{\tau_N\le T\}\ge p.
> \tag{3.2}
> \]
> Every moment of \(\tau_N\) is uniformly bounded. For every integer
> \(r\ge1\),
> \[
>  {\mathbb E}_z(1+|Z^{(N)}_{\tau_N-}|)^r
>  \le C_r(1+|z|)^{q_r}.
> \tag{3.3}
> \]
>
> The same conclusions hold for a conservative unimolecular network on
> classes with total molecule number bounded by a fixed constant, provided
> \(g\) is nonzero on each class.

### Proof

For the open network use its independent-particle construction. Initial
particles follow a finite transient type chain until absorption at \(0\);
immigrants arrive as independent Poisson processes. In every physical time
block, retain only particles descending from immigrants born in that
block. This fresh subsystem is independent of the past and is
coordinatewise dominated by the full population.

The finite particle chain has an exponential absorption tail. Every
factorial polynomial of degree at most two has uniformly bounded moments,
and the fresh process approaches \(\pi\) at rate \(e^{-cNt}\). From a
bounded initial set, or with a polynomial factor in the initial population,
the usual mixing calculation gives

\[
 \left|\operatorname{Cov}_z\{g(Z^{(N)}_s),g(Z^{(N)}_t)\}\right|
 \le C(1+|z|)^q e^{-cN|t-s|},
 \tag{3.4}
\]

and, for fixed \(T\),

\[
\begin{aligned}
 {\mathbb E}\int_0^T g(Z^{(N)}_t)\,dt
   &=T\pi(g)+O\{(1+|z|)^qN^{-1}\},\\
 \operatorname{Var}\left(\int_0^Tg(Z^{(N)}_t)\,dt\right)
   &\le {C_T(1+|z|)^q\over N}.
\end{aligned}
\tag{3.5}
\]

These estimates prove the assertion from a bounded initial set. Uniformity
over arbitrary \(z\) follows instead from the fresh-immigrant subsystem:
it is independent of the initial particles, is coordinatewise dominated by
the full population, and has the same positive limiting value of
\(\pi(g)\). Conditional on a phase path, the Cox clock rings with
probability \(1-\exp\{-\int g\,dt\}\). Using a new fresh-immigrant
subsystem in successive disjoint blocks gives a conditional success
probability bounded below independently of the past. Repetition gives a
geometric tail for \(\tau_N/T\), and hence every duration moment.

The open independent-particle system has an exponential Foster function
\(W(z)=\exp\{\theta\ell\cdot z\}\), where \(\ell>0\) comes from the
phase-type particle chain. For small \(\theta>0\),

\[
 QW\le-cW+C.
 \tag{3.6}
\]

Apply the localized stopped Dynkin formula to
\(Z^{(N)}_{t\wedge\tau_N}\), and then remove localization and let
\(t\to\infty\). This proves (3.3). A reaction target changes at most two
molecules, so the same bound holds after the slow event.

In the conservative case, a bounded number of marked particles evolves on
a finite type space. Uniform finite-state mixing at speed \(N\) gives
(3.4)--(3.5), while total molecule number is fixed. The same block proof
applies.
\(\square\)

There is an equivalent Poisson-equation proof. The space of polynomials of
degree at most two is invariant under \(Q\). On centered polynomials in the
stable open case, \(Q\) is invertible, so

\[
 Q\chi=g-\pi(g).
 \tag{3.7}
\]

Dynkin's formula for the full generator \(NQ+R\), where \(R\) contains the
slow reactions, gives

\[
 \int_0^T\{g(Z_s)-\pi(g)\}\,ds=O_{L^1}(N^{-1/2})
 \tag{3.8}
\]

from polynomial-moment-controlled starts. The \(R\chi/N\) term is
\(O(N^{-1})\), and the fast martingale divided by \(N\) is
\(O_{L^2}(N^{-1/2})\).

## 4. The regression model is completely repaired

For (1.3), take \(g(c)=dc\). An elementary transient proof is even sharper.
Ignore all initial particles. New \(C\)-particles immigrate at rate
\(N\alpha\). Each races fast death of rate \(N\beta\) against service
preparation of rate \(d\), so its success probability is

\[
 {d\over N\beta+d}.
 \tag{4.1}
\]

Successful candidates arrive at rate

\[
 r_N={N\alpha d\over N\beta+d}
 \ge {\alpha d\over\beta+d},\qquad N\ge1.
 \tag{4.2}
\]

The preparation time has all moments uniformly bounded, from every initial
\(C\). After \(C\to B\), the exit \(A+B\to C\) has probability
\(1-O(A^{-1})\), duration \(O(A^{-1})\), and competing-entry probability
\(O(A^{-1})\). Thus

\[
\begin{aligned}
 {\mathbb P}(\hbox{one old unit is cleared})&\ge p>0,\\
 {\mathbb E}(\hbox{new unresolved units})&\le {C\over A},\\
 {\mathbb E}\tau^r&\le C_r,
\end{aligned}
\tag{4.3}
\]

with polynomial endpoint moments. At debt zero, the same episode is a
surplus service.

For \(\Phi_A(a)=a(\log a-1)+1\),

\[
 \Phi_A(A-1)-\Phi_A(A)=-\log A+O(A^{-1}).
 \tag{4.4}
\]

The endpoint \(B,C\) moments are controlled by Theorem 3.1, while a rare
unresolved entry costs \(O(A^{-1}\log A)\). Hence the exact model obeys

\[
 {\mathbb E}\{\Phi(X_\tau)-\Phi(X_0)\}
 \le-p\log A+C.
 \tag{4.5}
\]

This proves the countable-phase repair, including old debt, surplus service,
and the entropy seam, for the regression network.

## 5. Exhaustion of the closed top-phase shapes

The top menu is \(\mathcal H_X=\{X,X+U,X+V\}\), and linkage supports are
disjoint.

> **Lemma 5.1 (support exhaustion).**  Suppose there is no \(2X\) complex.
> A closed nonkilled component of the stripped top graph is contained in a
> linkage lying wholly in \(\mathcal H_X\).  Up to exchanging \(U,V\), a
> nontrivial such support has one of the forms
> \[
>  \{X,X+U\},\qquad \{X+U,X+V\},\qquad
>  \{X,X+U,X+V\}.                                    \tag{5.1}
> \]
> The first is one-dimensional immigration--death, the second is
> conservative on every fixed \(U+V\) class, and the third leaves no top
> complex for the other linkage.  If every linkage is wholly top or wholly
> lower, then \(X\) is an exact reaction invariant.

### Proof

In a mixed linkage, strong connectivity gives a path from every top vertex
to a lower vertex.  The first top-to-lower edge on that path kills the
stripped component.  Thus a nonkilled top component belongs to a wholly top
linkage.  There are only three top vertices and linkage supports are
disjoint, giving (5.1).  Removing the common \(X\), their reaction vectors
are respectively multiples of \(U\), multiples of \(V-U\), and vectors of
the unimolecular menu \(\{0,U,V\}\).  The first two assertions follow.
If all three vertices are used, the other linkage is wholly lower.  More
generally, if no linkage is mixed, active degree is constant on every
reaction and \(X\) is invariant. \(\square\)

The exact support enumeration on the affine-feasible one-active candidate
branch makes this still sharper: the only wholly top pattern which occurs
is \(\{X,X+U\}\), up to relabelling.  The analytic result below is stated
for that sole countable pattern.  The conservative pattern can be handled
by a genuine finite class, and a mixed top component by the killed-carrier
estimate.

## 6. The one-dimensional physical service kernel

Assume henceforth that the two linkage supports are

\[
 F=\{X,X+U\},\qquad L=\{T=X+V\}\mathbin\cup K,        \tag{6.1}
\]

where every complex in \(K\) has active degree zero.  Aggregate parallel
channels in \(F\).  At active level \(X=N\), its generator is

\[
 NQf(u)=N\alpha\{f(u+1)-f(u)\}
       +N\beta u\{f(u-1)-f(u)\},                     \tag{6.2}
\]

with \(\alpha,\beta>0\) and stationary law
\(\pi=\operatorname{Pois}(\lambda)\),
\(\lambda=\alpha/\beta\).  The other linkage has the sole top complex
\(T\).

Put \(K_0=\{y\in K:y_V=0\}\).  If \(T\to z\) ranges over labelled outgoing
channels, define

\[
 q_+={\sum_{T\to z,\ z_V>0}\kappa_{Tz}
            \over\sum_{T\to z}\kappa_{Tz}}.          \tag{6.3}
\]

The denominator is positive by strong connectivity.  Define the
**base-to-service polynomial**

\[
\begin{aligned}
 g(u)={}&
 \sum_{\substack{y\to z,\ y,z\in K\\y_V=0,\ z_V>0}}
       \kappa_{yz}(u)_{y_U}\\
 &+q_+\sum_{\substack{y\to T\\y\in K_0}}
       \kappa_{yT}(u)_{y_U}.
\end{aligned}                                        \tag{6.4}
\]

It is a nonnegative falling-factorial polynomial of degree at most two.
Every term in the first line creates \(V>0\) without increasing \(X\), so
the next top exit is unpaired.  A term in the second line is an entry whose
first top exit is paired; with probability \(q_+\) its target still contains
\(V\), and the next top exit is unpaired.

> **Theorem 6.1 (Poisson-averaged service block).**  Retain every lower
> reaction.  Start a block with \(X=N\), \(V=0\), and with the moments of
> \(U\) bounded independently of \(N\).  If \(g\not\equiv0\), there are
> constants \(T,p,C,N_0\), depending only on the network and the stated
> moment bounds, and a stopping time \(\tau_N\le T\), such that
> \[
> \begin{aligned}
>  {\mathbb P}\{\hbox{an unpaired top exit occurs by }\tau_N\}&\ge p,\\
>  {\mathbb E}A_N&\le {C\over N},\\
>  \sup_N{\mathbb E}J_N^r&<\infty\qquad(r<\infty),   \tag{6.5}
> \end{aligned}
> \]
> where \(A_N\) is the number of entries left unresolved at the endpoint
> and \(J_N\) is the total number of lower reactions and raw entry carriers
> launched in the block.  The endpoint \(U,V\) populations have every fixed
> polynomial moment uniformly in \(N\).  From a deterministic arbitrary
> \(u\), the same bounds hold with a polynomial factor
> \(C(1+u)^q/N\) in the second line and polynomial endpoint bounds.
>
> If scalar debt \(D>0\), the unpaired exit in (6.5) services one old unit.
> If \(D=0\), it is a surplus service.

### Proof

Until service, the chain spends all but carrier intervals on the base face
\(V=0\).  Contract a base entry \(y\to T\) with the first top exit.  All
outgoing top clocks at \(T\) contain the same factor \((X)_1(V)_1\), so
their relative probabilities are exactly the constant ratios in (6.3).
The contracted jump has net active reward zero.  Flat \(U\)-reactions may
occur during the carrier, but they neither consume \(V\) nor alter the exit
ratios.

The carrier duration is \(O(N^{-1})\).  The total lower propensity is at
most \(C(1+U+V)^2\); hence the actual-target carrier estimate and the
polynomial occupation bounds give

\[
 {\mathbb E}(\hbox{interrupted or time-boundary carriers in }[0,T])
 \le {C\over N}.                                     \tag{6.6}
\]

This is a total bound, not a per-entry assertion: the compensator of the
raw-entry count is a degree-two polynomial of \(U\), its fixed-time
occupation moments are bounded, and multiplying that compensator by the
conditional carrier-interruption bound only raises the required polynomial
moment.  A carrier launched within its \(O(N^{-1})\) mean lifetime of the
deterministic endpoint \(T\) contributes the same compensator-times-lifetime
bound.  Such a carrier is included in \(A_N\), whether or not a lower
reaction interrupted it.  The same calculation gives all fixed moments of
\(J_N\).

After contraction, all remaining lower reactions are retained as the slow
bounded-jump part of the generator \(NQ+R\).  For completeness, solve
\(Q\chi=g-\pi(g)\) in the space of polynomials of degree at most two.
Dynkin's formula gives the centered occupation as an endpoint difference
divided by \(N\), a martingale whose quadratic variation is \(O(N)\)
divided by \(N\), and \(N^{-1}\int R\chi\).  Polynomial occupation moments
bound the first and third terms by \(O(N^{-1})\) and the martingale by
\(O_{L^1}(N^{-1/2})\).  Carrier intervals contribute another
\(O(N^{-1})\).  Hence

\[
 \int_0^T g(U_s)\,ds=T\pi(g)+O_{L^1}(N^{-1/2}).       \tag{6.7}
\]

Since \(\pi(U)_j=\lambda^j>0\) for \(j=0,1,2\),
\(g\not\equiv0\) implies \(\pi(g)>0\).  Choose \(T\) so that the Cox clock
with intensity \(g(U_s)\) rings with probability at least \(2p\).  Each
ring produces the unpaired exit described after (6.4), except on a carrier
interruption event.  Equation (6.6) therefore leaves probability at least
\(p\) for all large \(N\).

At the first unpaired exit, stop.  If none occurs, stop at \(T\), charging
every carrier still active at that boundary to \(A_N\).  Bounded
jumps, the moment bounds for \(NQ+R\), and (6.6) prove the remaining claims.
Paired carriers change debt by \(+1-1=0\).  An interrupted carrier accounts
for one of the units in \(A_N\), while an unpaired exit lowers positive debt
or is surplus at debt zero. \(\square\)

The moment hypothesis is the correct sequential one-active hypothesis.  If
the initial inactive population is bounded, it is automatic after taking a
subsequence.  If it grows, the polynomial version following (6.5) applies
until it ceases to be \(o(N^{1/q})\); beyond that point the state belongs to
a promoted two-active flag.  No visit of the recurrent Poisson tail is
called promotion.

## 7. Old debt and the zero-reward alternative

The apparent finite marked graph has only one slow base vertex after the
countable \(U\)-coordinate is averaged.  Its nonsurplus loops are lower
\(V=0\) jumps and paired entry--exit carriers, all of reward zero.  Its
service loops have reward \(-1\).  Thus its cycle/coboundary dichotomy is
exact rather than qualitative.

> **Lemma 7.1 (debt forces the service polynomial).**  If an entry carrier
> can be interrupted in a way which leaves positive unresolved \(X\)-debt
> on the face \(V=0\), then \(g\not\equiv0\).  Consequently Theorem 6.1
> services old debt with a uniform physical-time margin.  If
> \(g\equiv0\), unresolved \(X\)-debt cannot persist after all active
> carriers are drained.  On the singular one-carrier graph the active
> reward is a coboundary; one may take potential zero at the base and
> \(-1\) at the carrier.  This is not asserted to be a bounded potential on
> the raw physical state with arbitrarily many simultaneous carriers.

### Proof

Consider a carrier history which starts on \(V=0\), contains more entries
than top exits, and later returns to \(V=0\).  At its last transition to the
base, either a lower edge consumes positive \(V\), or a top exit lands at a
zero-\(V\) target while an earlier entry remains unmatched.  In the first
case there is an edge \(y\to y'\) with \(y_V>0,y'_V=0\).  In the second,
some intervening lower entry necessarily had a positive-\(V\) source; call
that source \(y\), and let \(y'\) be the zero-\(V\) target of the final top
exit.  (An entry with zero-\(V\) source adds a molecule of \(V\), so one top
exit cannot both return to the base and leave that entry unmatched.)

In either case strong connectivity supplies a directed path from the
zero-\(V\) complex \(y'\) to the positive-\(V\) complex \(y\).  Inspect the
first positive-\(V\) complex on this path.  If that complex is lower, its
incoming edge occurs in the first sum of (6.4).  If it is \(T\), inspect the
next path edge.  An exit to a positive-\(V\) lower complex makes \(q_+>0\)
and the entering edge contributes to the second sum.  An exit to the base
returns to \(V=0\); continuing along the finite path eventually gives one
of the preceding two cases.  Hence \(g\not\equiv0\).

Suppose \(g\equiv0\).  If \(K_0=\varnothing\), no source in the mixed
linkage is enabled on \(V=0\), so an entry and hence debt cannot be created
there; the assertion is immediate until \(V\) is promoted.  Assume
\(K_0\ne\varnothing\).  The first sum in (6.4) says that no lower edge from a
zero-\(V\) complex reaches a positive-\(V\) lower complex.  The second says
that every top exit lands at \(V=0\).  Strong connectivity then excludes
positive-\(V\) lower complexes altogether: a path from a zero-\(V\) top-exit
target to such a complex would have a first positive-\(V\) vertex and would
make one of the two sums nonzero.

Consequently \(V\) is exactly the number of unmatched physical entries.
Retain every reaction and stop at the actual first hit of \(V=0\).  When
\(V=m>0\), the aggregate top-exit rate is at least \(cNm\), while new
entries have a degree-two polynomial intensity in the countable
\(U\)-phase.  Immigration--death comparison and the polynomial occupation
bounds give

\[
 {\mathbb E}\tau_{\rm drain}^r\le {C_r(1+\log(1+m))^r\over N^r},
 \qquad
 {\mathbb E}(1+U_{\tau_{\rm drain}})^r
 \le C_r(1+U_0)^{q_r}.                                \tag{7.1}
\]

New entries during the drain are not suppressed; they merely add one to
the queue and are included in the same comparison.  At the physical hit
\(V=0\), every entry has an exit and unresolved debt is exactly zero.
After this all-reactions-retained drain, the entry reward \(+1\) and
paired-exit reward \(-1\) are cancelled by the bounded singular
one-carrier potential.  Thus every contracted cycle has reward zero unless
it contains a service. \(\square\)

For repeated blocks with \(D>0\), (6.5) gives the aggregate-debt inequality

\[
 {\mathbb E}(D_{k+1}-D_k\mid\mathcal F_k)
 \le-p+{C\over N}.                                   \tag{7.2}
\]

Taking \(N\) large makes the margin at least \(p/2\).  Since each block has
duration at most \(T\) and its event count has fixed moments, the expected
physical time and raw reaction count needed to clear any fixed initial debt
are finite.  This is precisely the old-debt estimate which the fixed-box
kernel failed to provide.

## 8. Entropy episode

Let \(h(n)=n(\log n-1)+1\), with the usual continuous convention at zero.
Write the active endpoint change as

\[
 X_{\tau_N}-N=A_N-S_N,                                \tag{8.1}
\]

after cancelling every completed entry--exit carrier, where
\({\mathbb E}S_N\ge p\), \({\mathbb E}A_N\le C/N\), and both counts have
fixed moments.  Taylor expansion on \(|A_N-S_N|\le N/2\), followed by a
moment bound on the complementary event, yields

\[
 {\mathbb E}\{h(X_{\tau_N})-h(N)\}
 \le -p\log N+C+{C\log N\over N}.                    \tag{8.2}
\]

The endpoint \(U,V\) entropy has bounded expectation by Theorem 6.1.
Therefore, whenever \(g\not\equiv0\), the full factorial entropy satisfies

\[
 {\mathbb E}\{\Phi(X_{\tau_N},U_{\tau_N},V_{\tau_N})
                 -\Phi(N,U_0,0)\}
 \le -{p\over2}\log N+C                              \tag{8.3}
\]

for all large \(N\), from bounded-moment one-active starts.  This covers
both old service and surplus service.  If \(g\equiv0\), Lemma 7.1 supplies
the bounded-coboundary alternative instead of a strict entropy episode.

## 9. Certification boundary

Lemmas 5.1 and 7.1 and Theorem 6.1 replace the false finite-box clause of
Proposition 5.1 in *one_active_physical_phase_theorem.md*.  They prove the
local countable regenerated-mode kernel, including the total entry bound,
old debt, surplus service, duration, endpoint moments, and entropy cost.

They do not by themselves promote the 1,227 support-pair count.  A global
argument must still glue this episode to the generator-good complement and
to promoted two-active tubes, and must exhibit one finite marked target for
the original irreducible class.  Those are tube-composition obligations,
not countable-phase or finite-mark obligations.

## 10. Regression command

    PYTHONPATH=src python3 -B -m unittest \
      tests/test_one_active_countable_phase_service.py -v
