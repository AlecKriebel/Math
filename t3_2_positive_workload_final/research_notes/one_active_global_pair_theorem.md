# Global one-active pair theorem

## 1. Scope and audit status

Let a binary reaction network have at most three species and at most two
linkage classes. Linkage supports are disjoint, every nontrivial linkage is
strongly connected, and every labelled rate is positive. Propensities are
stochastic mass-action propensities.

For an ordered support pair \(P\), let \(G(P)\) be its nonempty set of
affine-stoichiometrically feasible failed tier descriptors. The exact
certificate identifies 1,227 residual pairs satisfying

\[
 G(P)\ne\varnothing,\qquad
 \hbox{every descriptor in }G(P)\hbox{ has one active coordinate}. \tag{1.1}
\]

The finite selector and the analytic theorem are logically separate.

> **Audit-pending Theorem 1.1 (one-active pair theorem).** Every support
> pair satisfying (1.1), in every strongly connected orientation and for
> every positive rate vector, is classwise positive recurrent in physical
> time.

This note proves the stopping-time composition from the two local kernels:

- *one_active_countable_phase_service.md* for the 222 wholly top
  incidences, whose sole shape is one-dimensional immigration--death; and
- *one_active_killed_carrier_service.md* for the other 3,075 incidences.

The theorem remains labelled audit-pending until the complete composition
below receives an independent review. It makes no assertion about positive
recurrence of the raw embedded jump chain.

## 2. The statewise bad tubes

Use the factorial entropy

\[
 \Phi(x)=\sum_{i=1}^d\{x_i(\log x_i-1)+1\}.             \tag{2.1}
\]

Fix a closed irreducible population class \(\Gamma\). The standard
Anderson--Kim tier estimate and (1.1) give constants \(M,N_0<\infty\) and
a finite set \(F_0\subset\Gamma\) such that

\[
 {\cal L}\Phi(x)\le-1                                  \tag{2.2}
\]

outside \(F_0\) unless, for one coordinate \(i\),

\[
 x_i>N_0,\qquad x_j\le M\quad(j\ne i),                 \tag{2.3}
\]

and the resulting one-active descriptor is failed. Increase \(N_0\) so
that \(N_0>M\); the tubes in (2.3) are then disjoint.

Indeed, failure of this assertion gives a sequence in \(\Gamma\) with
\({\cal L}\Phi>-1\). Pass to a tier subsequence. If at least two
coordinates are active, its affine-feasible descriptor would be a failed
multi-active descriptor, contradicting (1.1). If one coordinate is active
but the descriptor passes, its top-S descending source makes
\({\cal L}\Phi\to-\infty\), another contradiction. This is a statewise
generator argument, not a tightness-to-finite-phase reduction.

Let \(I\) be the finite set of coordinates occurring as the active axis of
a failed descriptor on \(\Gamma\). For \(i\in I\), the complex \(2X_i\) is
absent. Otherwise it is an enabled unique highest-degree source and strong
connectivity supplies a top-S descending path. Hence every reaction changes
\(X_i\) by \(-1,0\), or \(1\).

## 3. Global debt marks and the finite neutral target

Choose a reference state \(x^\circ\in\Gamma\). For every \(i\in I\), start
\(D_i(0)=0\) and update it along the entire physical path by

\[
 D_i^+=\begin{cases}
 D_i+1,&\Delta X_i=1,\\
 (D_i-1)^+,&\Delta X_i=-1,\\
 D_i,&\Delta X_i=0.
 \end{cases}                                           \tag{3.1}
\]

Put \(H_i=X_i-D_i\). Pathwise,

\[
 0\le D_i\le X_i,\qquad H_i(t)\le x_i^\circ.           \tag{3.2}
\]

The augmented process consisting of population and these finitely many
marks is Markov on the subset \(\widehat\Gamma\) reachable from
\((x^\circ,0)\). No genealogical ledger is used. Moreover \(\Phi\), though
it ignores the marks, is proper on \(\widehat\Gamma\): above each finite
population set there are only finitely many choices \(0\le D_i\le X_i\).

At a bad-tube state, first finish any currently enabled **mixed** top
carrier by the physical fast drain in the appropriate local theorem. If
\(D_i>0\), its first top exit services debt; if \(D_i=0\), that exit is
surplus. Its duration is \(O(X_i^{-1})\), and every competing lower
reaction is retained. A wholly top flat component is not called a carrier
and is left in the countable averaging dynamics. Thus the local theorems
apply from an arbitrary tube state, not only from a displayed base
representative. After that normalization the alternatives, in priority
order, are as follows.

1. If \(D_i>0\) and the top component is mixed, the actual-target theorem
   makes an unpaired exit reachable and supplies an old-debt service block.
2. If \(D_i=0\) and surplus service is reachable, use the same block.
3. In the one-dimensional wholly top case, a nonzero service polynomial
   gives the Poisson-averaged service block.
4. Suppose that polynomial is zero. If \(K_0=\varnothing\), the only
   neutral state is on the drained base \(V=0\); there no entry is enabled,
   and consistency forces \(D_i=0\). States with \(V>0\) fall under 1 or
   2. If \(K_0\ne\varnothing\), vanishing of the polynomial implies that
   all lower vertices have \(V=0\) and every top exit lands at \(V=0\).
   Along the whole physical path,
   \[
      D_i\le V,
   \]
   because every positive \(X_i\)-jump adds one \(V\), every negative
   \(X_i\)-jump removes one \(V\), and reflection can only reduce debt.
   Hence every queue state in the tube has \(D_i\le V\le M\).
5. In a mixed service-free component, the singular reward is zero. A marked
   state with \(D_i>0\) belongs to case 1, so a genuinely neutral marked
   state has \(D_i=0\).

Call the remaining states in cases 4--5 **neutral**. Their populations and
marks form a finite class-dependent set. In case 5, (3.2) gives
\(X_i\le x_i^\circ\). In the nonempty-\(K_0\) part of case 4,

\[
 X_i=H_i+D_i\le x_i^\circ+M.                           \tag{3.3}
\]

All other coordinates are at most \(M\), and all other debts are bounded
by those coordinates. Define \(\widehat F_\Gamma\subset\widehat\Gamma\)
to contain these neutral marked states, every lift of \(F_0\), the
reference mark, and every marked state whose population lies in the finite
box in which all coordinates are at most the final active threshold chosen
below. It is finite. Write \(F_\Gamma\) for its finite projection to
original population states.

## 4. Uniform local entropy blocks

There are only finitely many active axes and finitely many bounded starting
cross-sections. (The recurrent immigration--death coordinate is retained
as a countable phase during its episode.) The two local theorems therefore
give common constants \(p,C,T,N_1\) and stopping times \(\kappa\) for every
nonneutral bad-tube mark with active population \(N\ge N_1\):

\[
\begin{aligned}
 {\mathbb P}(\hbox{one unpaired active exit in the block})&\ge p,\\
 {\mathbb E}(\hbox{new unresolved active entries})&\le C/N,\\
 {\mathbb E}\kappa^r+{\mathbb E}J^r&\le C_r
 \qquad(r<\infty),                                    \tag{4.1}\\
 {\mathbb E}\{\Phi(X_\kappa)-\Phi(X_0)\}
 &\le-c\log N+C.
\end{aligned}
\]

Here \(c>0\) is uniform after taking the minimum over the finite phase set.
The variable \(J\) counts the controlled nonflat reactions and launched
carriers, not the order-\(N\) neutral jumps of the retained Poisson phase.
Every lower reaction is retained. Completed entry--exit carriers are
endpoint-neutral in the active coordinate; lower-interrupted and
deterministic-boundary carriers contribute the total \(O(N^{-1})\) term.
The full countable Poisson phase is retained where it occurs.

Choose \(0<\eta\le1\), \(\delta>0\), and enlarge \(N_1\) so that, from every
nonneutral bad-tube state outside \(\widehat F_\Gamma\),

\[
 {\mathbb E}\{\Phi(X_\kappa)-\Phi(X_0)+\eta\kappa\}
 \le-2\delta.                                         \tag{4.2}
\]

If the local endpoint is neutral, its augmented state lies in
\(\widehat F_\Gamma\). Otherwise it is either another service-type tube
mark or a generator-good state. No tube switch potential is introduced:
the same \(\Phi\) is used everywhere.

## 5. Appending the generator-good excursion

Let \({\cal S}\) be the reachable augmented states which are nonneutral bad
tube marks outside \(\widehat F_\Gamma\). Starting from the endpoint of a
local block, if it is not in \(\widehat F_\Gamma\cup{\cal S}\), run the
original physical chain until

\[
 \gamma=\inf\{t\ge0:(X_t,D_t)\in\widehat F_\Gamma
                 \hbox{ or }(X_t,D_t)\in{\cal S}\}.     \tag{5.1}
\]

Before \(\gamma\), (2.2) holds. Localized Dynkin formula and nonexplosion
give

\[
 {\mathbb E}\{\Phi(X_\gamma)-\Phi(X_0)+\eta\gamma\}
 \le0.                                                 \tag{5.2}
\]

In particular, \(\gamma\) has finite mean. Properness of \(\Phi\), stopped
localization, and the endpoint moments in (4.1) give the uniform
integrability needed to remove the localization. A tube exit is therefore
not renamed promotion or discarded: its physical endpoint starts exactly
the excursion (5.1), and its entropy and duration are paid by (5.2).

Equations (4.2) and (5.2) are exactly the hypotheses of the
common-entropy physical-time gluing lemma on the augmented chain, with
\(K=\widehat F_\Gamma\), \(B={\cal S}\), and the complement as the
generator-good region. Consequently

\[
 {\mathbb E}_{\widehat x}\tau_{\widehat F_\Gamma}<\infty
 \qquad(\widehat x\in\widehat\Gamma).                 \tag{5.3}
\]

For clarity, its stopped macroepisode calculation is

\[
 \delta\,{\mathbb E}(m\wedge N_*)
 +\eta\,{\mathbb E}S_{m\wedge N_*}
 \le \Phi(x)+\delta,                                  \tag{5.4}
\]

where \(S_k\) is the end of the \(k\)-th appended local-plus-good episode
and \(N_*\) is the first terminal episode. Thus \(N_*<\infty\) almost
surely and the physical hitting time has finite mean. For any
\(x\in\Gamma\), choose once and for all a finite physical reaction path
from \(x^\circ\) to \(x\) and update (3.1) along it. This gives a
consistent lift \(\widehat x\in\widehat\Gamma\). Since the population
marginal of the augmented chain is the original chain, (5.3) implies

\[
 {\mathbb E}_x\tau_{F_\Gamma}<\infty
 \qquad(x\in\Gamma).                                  \tag{5.5}
\]

This is a physical-time estimate. It never sums the number of fast neutral
jumps.

## 6. From the finite hit to classwise positive recurrence

A bimolecular source cannot increase total population in a binary network.
Every population-increasing reaction therefore has source molecularity zero
or one, and the total increasing rate is affine. Localized Yule comparison
gives nonexplosion and the finite-time moments used above.

The construction remains inside \(\Gamma\), so \(F_\Gamma\cap\Gamma\ne
\varnothing\). Start from any consistent lift in the finite set
\(\widehat F_\Gamma\), take one ordinary jump, and apply (5.3) to each of
its finitely many augmented successors. An absorbing singleton is already
positive recurrent; otherwise the projection \(F_\Gamma\) has finite mean
positive return time. The finite-set trace therefore has an invariant
probability, whose cycle occupation measure is an invariant probability
for the original chain. Irreducibility gives positive recurrence of the
entire closed class.

Thus Theorem 1.1 follows, subject to independent audit of the composition
in Sections 3--5.

## 7. Exact certification boundary

The proof uses three distinct certified inputs and does not conflate them:

1. the finite selector: 1,227 pairs and 3,297 one-active incidences;
2. the local physical kernels: 222 countable and 3,075 mixed incidences;
3. the classwise global composition (5.3)--(5.5).

No count should be promoted until item 3 is independently accepted and the
release tables are updated consistently. The 151 no-affine-feasible-failure
pairs form an earlier disjoint branch and are not counted again here.
