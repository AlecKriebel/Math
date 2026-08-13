# Scoped audit of the global T3-2 classwise skeleton

**Proof-first audit, 2026-08-12 PDT.**  The exact target is

`proof_first_global_t3_2_classwise_composition.md`

at SHA-256

`37a8a395797dabb86659d877020c137554f1bb0b6c7b5f97bdd57a0d563e1edf`

(241 lines, 10891 bytes).  This audit covers only Sections 1, 2, 5, and
6: fixed-class projection and linkage merging, nonexplosion,
common-potential descriptor compactness, random-time Foster gluing, and
the marked-to-physical recurrence implication.  It assumes no unresolved
one-linkage or two-linkage coverage theorem and does not edit the target.
No support, orientation, or population enumeration is used.

## 1. Verdict

**Sections 1 and 2: STRICT PASS.**  Projection is an exact conjugacy on
the fixed class, projected linkage merging preserves the physical
generator, and the binary molecularity bound proves nonexplosion.

**Sections 5 and 6: CONDITIONALLY VALID, BUT NOT YET A STRICT STANDALONE
PASS AS WRITTEN.**  Their core gluing mechanism is correct after four
interfaces are stated literally:

1. one proper potential is fixed on the entire physical or reachable
   marked class;
2. the local theorem library supplies uniform, not merely statewise or
   descriptorwise, positive constants;
3. a visit to the finite target inside an episode is recorded immediately,
   while that one episode may be completed only for drift bookkeeping; and
4. in a reflected proof the mark is propagated through the first return
   cycle and the resulting finite marked occupation measure is projected to
   the physical chain.

Under the repaired abstract statement in Sections 5--7 below, the skeleton
earns a strict conditional PASS.  These are composition clarifications, not
new branch estimates.  The exact target should not be cited as a complete
global proof until they and the separately pending branch hypotheses are
pinned.

## 2. Exact fixed-class projection

Let (i) be a population coordinate which is constant, with value (m_i),
on the closed irreducible class \(\Gamma\).  If a reaction (y\to z) is
enabled at (x\in\Gamma), its endpoint (x-y+z) is reached at positive
rate and therefore belongs to \(\Gamma\).  Hence

\[
                         z_i-y_i=0.                          \tag{2.1}
\]

Now suppose one source (y_0) in a weakly reversible linkage is enabled
at (x).  Write (r=x-y_0\ge0).  Along any directed complex path

\[
 y_0\longrightarrow y_1\longrightarrow\cdots
             \longrightarrow y_k,                           \tag{2.2}
\]

the literal population history is

\[
                         r+y_0,r+y_1,\ldots,r+y_k.           \tag{2.3}
\]

Every next source is enabled because it is present as the preceding target.
Closure and (2.1) imply (r_i+(y_j)_i=m_i) for every (j).  Strong
connectivity therefore makes the (i)-stoichiometry constant across the
whole active linkage.  Its mass-action factor
((m_i)_{(y_j)_i}) is a single positive constant and is absorbed into the
labelled rate constants.

Deleting all constant coordinates is injective on \(\Gamma\), because the
deleted values are fixed.  It is surjective onto the projected class by
definition, and the preceding rate calculation intertwines the two
generators.  Thus it is a CTMC conjugacy, not merely a stoichiometric
comparison.

A linkage with no enabled source anywhere on \(\Gamma\) contributes zero
propensity and may be deleted.  Two projected strong linkage graphs which
share a projected complex have a strongly connected union.  Retaining
parallel labelled channels, or equivalently adding their propensities,
preserves every projected transition rate.  A projected zero-displacement
channel contributes zero to the state generator and may also be deleted.

It follows that recurrence and explosion properties of the full chain on
\(\Gamma\) are exactly those of the reduced dynamic-coordinate chain.  If
no projected linkage is active, every state is absorbing; irreducibility
then forces \(\Gamma\) to be a singleton.

## 3. Nonexplosion

Put (N(x)=1+|x|_1).  A reaction with a source of total degree two cannot
increase (N), since every target also has degree at most two.  Every
positive increment is therefore sourced at degree zero or one, has bounded
size, and has aggregate rate at most

\[
                         C N(x).                             \tag{3.1}
\]

Let \(\sigma_R\) be the first time (N\ge R).  Before \(\sigma_R\) the
state space is finite and every total rate is bounded, so the stopped chain
is nonexplosive and Dynkin's formula is legitimate.  Dropping all negative
increments gives

\[
 {cal L}N(x)\le C N(x),qquad
 \mathbb E_xN(X_{t\wedge\sigma_R})\le N(x)e^{Ct}.           \tag{3.2}
\]

Because reaction increments are bounded, (3.2) implies

\[
             \mathbb P_x\{\sigma_R\le t\}
                    \le {C_tN(x)\over R}.                   \tag{3.3}
\]

Letting (R\to\infty) shows that total population remains finite on every
bounded time interval.  Conditional on any fixed population cap there are
only finitely many states and a finite maximum total rate.  Hence the
quadratic population-preserving or population-decreasing clocks cannot
accumulate infinitely many jumps under that cap.  Equations (3.2)--(3.3)
prove nonexplosion.

This argument avoids a possible circularity in an informal Yule comparison:
the finite-sublevel localization is established before quadratic clocks are
discarded.

## 4. What descriptor compactness does and does not prove

For a fixed support pair, the availability sets, active-coordinate sets,
and weak orders of finitely many source monomials have only finitely many
combinatorial values.  Pairwise monomial ratios take values in the compact
extended half-line after normalization, so diagonal subsequence extraction
also fixes every limiting tier relation.  Thus every divergent sequence has
a subsequence with a stable descriptor of the kind used in Section 5 of the
target.

Properness then converts sequential coverage into a finite exceptional
set.  For example, if every divergent generator-good sequence has a
subsequence along which

\[
                         {\cal L}W(x_n)\longrightarrow-\infty, \tag{4.1}
\]

then \({\cal L}W\le-a\) outside a finite subset of the generator-good
region for any fixed (a>0).  Otherwise infinitely many violating states
would, by properness, contain a divergent descriptor subsequence
contradicting (4.1).

Compactness does **not**, by itself, turn unrelated pointwise inequalities

\[
 \mathbb E_x[W(Z_{\tau_x})-W(x)+\eta_x\tau_x]le-\delta_x,
 \qquad \delta_x>0,                                       \tag{4.2}
\]

into one inequality with \(\inf_x\delta_x>0\).  Positive margins can tend
to zero along a continuous normalized descriptor or along an infinite
state family.  The local library must instead provide one of the following
equivalent publication interfaces:

* finitely many episode types, each with constants
  \(\eta_j,\delta_j>0\) uniform over its full start domain; or
* a sequential coercivity assertion saying that every divergent sequence
  of episode starts has a subsequence on which one fixed positive margin
  applies.

With finitely many types, take

\[
              \eta=\min\{a,\eta_1,\ldots,\eta_J\}>0,
 \qquad       \delta=\min_j\delta_j>0.                     \tag{4.3}
\]

Decreasing \(\eta_j\) or \(\delta_j\) preserves each local inequality.
This is the exact uniformity hypothesis implicitly needed by the last
paragraph of target Section 5.  Endpoint and duration integrability must be
part of every local theorem; a finite descriptor partition does not prove
it.

The second indispensable hypothesis is a single potential.  The same
proper (W) must be used in the generator region, every episode estimate,
every boundary charge, and every actual endpoint handoff.  A finite menu of
potentials selected anew after an endpoint would introduce uncontrolled
comparison tolls.  The target correctly states the single-pair-potential
requirement; each eventual branch audit must verify it literally, including
on the reachable reflected state space for an augmented workload.

## 5. Repaired common-potential Foster lemma

The following statement is sufficient for the target's global composition.

> **Lemma 5.1 (physical-time state-selected Foster lemma).**  Let (Z) be
> a nonexplosive CTMC on a countable state space (E).  Let
> (W:E\to[0,\infty)) be proper and belong to the extended generator
> domain under finite-sublevel localization.  Suppose a finite set (K)
> and a partition
> 
> \[
>                         E\setminus K=G\mathbin{\dot\cup}B \tag{5.1}
> \]
> 
> satisfy
> 
> \[
>                         {\cal L}W\le-a\quad(G)             \tag{5.2}
> \]
> 
> for some (a>0).  For each (z\in B), suppose a state-selected
> strong-Markov stopping time \(\tau_z>0\), using the full physical clocks,
> satisfies, with constants independent of (z),
> 
> \[
> \mathbb E_z[W(Z_{\tau_z})+\tau_z]<\infty,
> \qquad
> \mathbb E_z[W(Z_{\tau_z})-W(z)+\eta\tau_z]
>                              \le-\delta,                   \tag{5.3}
> \]
> 
> where (0<\eta\le a) and \(\delta>0\).  Then
> 
> \[
>                         \mathbb E_zT_K<\infty
>                         \qquad(z\in E).                   \tag{5.4}
> \]

### Proof

From (z\in G), run until first entrance into (B\cup K).  Localized
Dynkin gives

\[
 \mathbb E_z[W(Z_\sigma)-W(z)+\eta\sigma]\le0.             \tag{5.5}
\]

Indeed, apply Dynkin before a finite (W)-sublevel exit and then use
nonexplosion and Fatou; the nonnegative endpoint potential and the
one-sided drift require no additional endpoint moment.  Equation (5.5)
also proves \(\mathbb E\sigma<\infty\), so the chain cannot remain in (G)
forever.

At an entrance (z\in B), append the actual physical episode
\(\tau_z\), then repeat from its actual endpoint.  If (K) is visited
inside that episode, record the physical hit immediately, but allow that
one episode to finish solely for inequality (5.3).  Its completed duration
upper-bounds the actual hitting time.  This convention is essential: an
episode endpoint can lie outside (K) even though its interior path has
already visited (K).

Let (S_m) be the accumulated accounting time after (m) completed
exceptional episodes and let (N) be the terminal episode index, with the
obvious zero-episode convention when a generator segment first hits (K).
Conditional iteration of (5.3) and (5.5), followed by (W\ge0), gives

\[
 \delta\,\mathbb E(N\wedge m)
   +\eta\,\mathbb E S_{N\wedge m}
                          \le W(z)+\delta.                  \tag{5.6}
\]

The harmless final \(\delta\) covers the zero-episode/off-by-one terminal
case.  Monotone convergence shows that the number of exceptional episodes
and their accumulated accounting time have finite expectation.  Failure to
hit (K) would require either infinitely many episodes or one final
generator segment which never exits; (5.6) and (5.5) exclude the two cases.
Since the physical (T_K) is no larger than the accounting time of its
successful segment, (5.4) follows. \(\square\)

The count term in (5.6), not a vague appeal to positive episode lengths, is
what excludes infinitely many zero-time or vanishing-time selections.
Nonexplosion is still required for the localized CTMC and the strong-Markov
concatenation.

## 6. Applying Lemma 5.1 to the descriptor cover

The publication-safe descriptor interface is now precise.  For each fixed
support pair one must verify:

1. the physical class or reachable reflected class is countable and
   nonexplosive;
2. one (W\ge0) is proper on that class and is used by every chart;
3. outside a finite set, the state space is partitioned by a statewise
   priority into generator-good states and finitely many genuine episode
   start domains;
4. the generator region has (5.2) with one (a>0);
5. every selected episode uses all physical clocks, includes its causing
   reaction and every cutoff endpoint, and satisfies (5.3) with the common
   \(\eta,\delta\); and
6. endpoint and time integrability are stated at the actual endpoint, with
   no post hoc cleanup or potential replacement.

Under these six clauses, descriptor extraction is used only to prove the
finite cover.  It is not used to infer a stochastic estimate.  Evaluation
at the identical (W) makes an outer handoff telescope with zero toll.
An internal moving boundary must either remain inside its original episode
theorem or be an actual endpoint whose complete (W)-charge is already
included in (5.3); calling it a descriptor boundary alone is insufficient.

The moment order greater than eight appearing in target Section 5 is a
convenient sufficient integrability interface for
(W=G_\ell^4\), since for fixed dimension

\[
                 G_\ell(x)^4\le C_\ell(1+|x|_1)^8.         \tag{6.1}
\]

For an augmented scalar, its own stated growth degree must be used instead.
The random-time lemma itself needs only the literal integrability in (5.3).

## 7. Marked-to-physical positive recurrence

The reflected update

\[
                    D_i^+=(D_i+\zeta_i)^+                   \tag{7.1}
\]

preserves (0\le D_i\le X_i): if (D_i\le X_i), then
(D_i+\zeta_i\le X_i+\zeta_i=X_i^+), and reflection at zero preserves the
upper bound.  It also makes

\[
             H_i^+=X_i^+-D_i^+\le X_i-D_i=H_i,             \tag{7.2}
\]

so (H_i\le x_i^\circ) on the marked class reachable from
((x^\circ,0)).  The marked transition rate depends only on (X), and
projection onto (X) is exactly the physical CTMC.

Suppose Lemma 5.1 gives finite mean hitting of a finite marked target
\(\widehat K\) from every state of the reachable marked class.  Its
physical projection is finite; conversely \(0\le D\le X\) gives only
finitely many marks above each point of that projection.  If a target
population has zero total rate, physical irreducibility forces the class to
be its absorbing singleton.  Otherwise, from each marked target state take
one ordinary physical reaction **and update (D) by (7.1)**.  There are
only finitely many such marked successors, and Lemma 5.1 gives a uniform
finite expected time back to \(\widehat K\).

The resulting return kernel on the finite marked target is stochastic.
Choose a stationary distribution on one of its recurrent classes and form
the usual cycle occupation measure.  Its total mass is finite because the
positive target-to-target cycle has finite mean duration.  Normalize it to
an invariant probability \(\widehat\pi\) for the reachable marked process.
For every finitely supported physical test function (f),

\[
 \widehat{\cal L}(f\circ\mathrm{pr}_X)(x,d)
                         =({\cal L}f)(x).                    \tag{7.3}
\]

Therefore

\[
                  \pi(x)=\sum_d\widehat\pi(x,d)            \tag{7.4}

is an invariant probability for the physical chain.  Irreducibility of
\(\Gamma\) makes every physical state positive recurrent and makes this
stationary probability unique.

Equivalently, one may deterministically reset the auxiliary mark whenever
the physical projection of \(\widehat K\) is hit and build the finite
physical return trace.  Such a reset changes only the proof device, never a
physical reaction rate.  The target's phrase “take one ordinary physical
jump” is valid only with one of these two literal constructions; finite
projection by itself is not a proof that an arbitrary unmarked successor
lies in the reachable marked class.

## 8. Final scoped disposition

No flaw was found in the fixed-class projection, linkage merging, or
nonexplosion arguments.  No counterexample was found to the repaired
common-potential gluing theorem.  The target's global skeleton becomes
publication-safe once it imports Lemma 5.1, requires branch-uniform
constants and integrability, records target hits inside episodes, and makes
the marked-cycle projection explicit.

This audit does not assert that the one-linkage and two-linkage analytic
families cover every reduced network.  It certifies only the composition
machinery that will apply after those independent coverage gates pass.
