# Finite-priority actual-target trace theorem

## 1. Terminal-chart data

Fix a terminal chart.  Its active coordinates are larger than a chart
threshold, its inactive coordinates lie in one finite padded box, its enabled
source set is fixed, and its physical source propensities have a complete
finite flag

\[
 \mathcal F_1\gg\mathcal F_2\gg\cdots\gg\mathcal F_m.
\]

A rational scalarization is multiplied by a common denominator so that

\[
 p(y)=h\cdot y\in\mathbb Z
\]

and the order of `p(y)` agrees with the source flag.  Every active coordinate
has positive coefficient.  The finite chart phase records the inactive
population, capped availability, the actual target of the last labelled
reaction, the linkage, the source-flag cell, and the finite correctors already
constructed at faster layers.

For a reaction `e:y->u`, put

\[
 d(e)=h\cdot(u-y)=p(u)-p(y).
\]

The target `u` is physically present after `e` and hence is an enabled source.
No future reaction is conditioned upon.

## 2. Faster return prefix

If `d(e)>0`, choose in the creator linkage a directed path

\[
 u=y_0\longrightarrow y_1\longrightarrow\cdots\longrightarrow y_r=y.
\]

Let `j` be the first index with `p(y_j)<=p(y)`.  Every source
`y_0,...,y_{j-1}` is strictly faster than `y`, and

\[
 d(e)+h\cdot(y_j-u)=h\cdot(y_j-y)\le0.       \tag{2.1}
\]

The lifted designated path is physical whenever it remains in the chart.  If
an inactive coordinate leaves its box, an active coordinate leaves the chart,
or source support changes, the event is retained as a structural exit.

## 3. The finite carrier phase

For one positive edge `e`, augment the chart phase by

* the creator edge type;
* the actual current target;
* the position of the chosen return prefix;
* the remaining integer workload credit, between `1` and
  `max_e d(e)`;
* the finite inactive-coordinate and zero-class data.

This phase is finite.  Active populations are not stored in it.  They enter
only through normalized tied-layer coefficients, which range over a compact
positive cell.

A faster reaction which leaves the designated source enabled is simply an
edge of this finite phase.  If it destroys the last required inactive
cofactor, its source contains that cofactor and its actual target is retained.
A source involving no active particle is a slower-layer interruption.  Thus a
bounded cofactor can be transferred only through finitely many physical
carrier complexes before either it is restored, a workload-decreasing edge
fires, or a declared chart exit occurs.

The following accessibility statement is load bearing.

### Lemma 3.1 — carrier accessibility

From every phase reached after the positive edge `e`, the faster carrier
graph has a physical path to one of:

1. accumulated workload loss at least `d(e)`;
2. a structural chart exit;
3. a closed zero component.

In a fully active chart the first alternative follows directly by the lifted
return prefix.  With two active coordinates, failure of the first two
alternatives makes every active linkage shielded for the chart workload; the
certified workload atlas then gives a common affine invariant, a
 deficiency-zero component, or one of the two service architectures.  With
one active coordinate, the corresponding zero component is the finite token
class of the one-active theorem.

**Proof.**  The first designated return channel is enabled at the actual
creator target.  Following designated channels reaches (1) or an exit.  Add
all faster physical deviations and their actual targets.  If the resulting
finite phase set has a closed class avoiding (1) and (2), no positive-flux
phase in it exposes a workload-decreasing faster source.  The creator linkage
is then shielded.  Applying the same argument to the second linkage shows
that every linkage represented in the closed class is shielded.  The
three-way independently verified atlas gives the stated alternatives in a
two-active chart.  With three active coordinates a shielded linkage is flat,
so the common chart workload is invariant.  With one active coordinate the
source-degree classification gives the token alternative.  \(\square\)

## 4. Uniform faster absorption

Remove the certified zero/exceptional alternatives.  The remaining finite
carrier graph is transient when killed at service or exit.  Normalize its
fastest outgoing rates.  Transition coefficients vary continuously over a
compact positive tied-rate cell.  From every phase a path of at most `L`
steps reaches absorption, and every edge on one selected path has conditional
probability at least `q>0`.  Therefore

\[
 \Pr\{\text{no absorption in }L\text{ carrier changes}\}\le1-q^L,
\]

and the number of carrier changes has a uniform geometric moment bound.

Let `rho_<k` be the aggregate rate of the current faster carrier source and
`rho_>=k` the aggregate rate of unprocessed layer-`k` and slower sources.
The complete flag gives, uniformly on the chart,

\[
 \frac{\rho_{\ge k}}{\rho_{<k}}\le\varepsilon_R,
 \qquad \varepsilon_R\to0.                    \tag{4.1}
\]

Compensator comparison and the geometric moment bound imply

\[
 \Pr\{\text{an unprocessed event occurs before service or exit}\}
 \le K\varepsilon_R.                           \tag{4.2}
\]

Physical duration has the same finite bound after multiplication by the
inverse current carrier rate.  Unrelated faster jumps are skipped and do not
delay the carrier clock.

## 5. The physical-credit busy period

Scale `h` to integer coordinates and let `delta>0` be the smallest positive
workload increment.  At the first positive unprocessed event, freeze the
pre-event workload `H_0=h\cdot X_0` and define the aggregate outstanding
credit

\[
 Q=\frac{(h\cdot X-H_0)_+}{\delta}.
\]

Only the integer ceiling is used if increments are not all multiples of the
minimal one.  This is a physical workload excess, not a genealogical label
or a component of the finite carrier phase.

A completed carrier service lowers `Q` by at least one.  Before service, one
unprocessed event can add at most

\[
 M=\max_e\left\lceil\frac{(h\cdot\zeta_e)_+}{\delta}\right\rceil
\]

units.  By (4.2), for a sufficiently large chart threshold the conditional
failure probability is at most `epsilon_R`, with

\[
 -(1-\varepsilon_R)+M\varepsilon_R\le-\tfrac12.  \tag{5.1}
\]

If `Q>0`, the finite carrier classification either supplies another service
trial, declares a structural exit, or enters a zero/invariant branch.  A
bounded inactive service token is part of the physical finite phase; more
than the chart cap is a promotion exit.  An active token leaves its service
source enabled.  Thus no unbounded obligation count is hidden in the phase.

At successive carrier trials, (5.1) and bounded-index optional stopping give

\[
 \mathbb E\tau_{Q=0}\le 2Q_0              \tag{5.2}
\]

in trial count.  The geometric carrier bound makes its physical duration
finite.  At clearing,

\[
 h\cdot X_\tau\le h\cdot X_0.             \tag{5.3}
\]

A strict service with `Q=0` gives strict descent.  The result permits complete
cancellation, rather than incorrectly claiming that every return prefix
overshoots below its pre-activation workload.

## 6. Source-layer elimination

Proceed inductively from the fastest source layer to the slowest.  Assume all
faster recurrent classes have already been replaced by finite-mean effective
transitions with pathwise nonpositive corrected workload reward, and their
zero classes have been contracted with finite Poisson correctors.

For a raw layer-`k` event:

* if its corrected reward is nonpositive, retain it;
* if it is positive, retain the event itself and run the physical-credit busy
  period above.

At clearing the complete transition has reward at most zero.  A structural
exit remains an exit.  Failed relaxations are included at their natural
probability inside the busy period; they are never assigned a favorable sign
or conditioned away.  Source layers too slow to enter (5.1) are retained for
the next lexicographic trace.

This operation is rate preserving.  The activation event belongs to the
preceding actual-current-target episode and simultaneously initializes the
physical credit; it is counted exactly once.

## 7. Recurrent classes and zero reward

Let `P_k` be a recurrent finite effective class at layer `k`.

* If one effective edge has strictly negative reward and positive limiting
  probability, the stationary corrected mean is strictly negative.  Compact
  tied-rate cells give a uniform strict margin.
* If the stationary mean is zero, every positive-probability effective edge
  has reward exactly zero.  Cycle sums vanish, so there is a bounded rational
  phase potential `psi_k` with

  \[
   h\cdot\Delta X+\psi_k(\phi')-\psi_k(\phi)=0
  \]

  on the class.

Transient elimination uses a nonnegative Green matrix and preserves
nonpositivity.  Source layers whose reaction counts vanish at one
normalization are passed to the next slower physical trace; they are never
deleted from the proof.

Because the source flag is finite, the induction terminates.  If every layer
is zero, the sum of the finitely many phase correctors gives an affine
invariant

\[
 W(X,\phi)=h\cdot X+\psi(\phi)                 \tag{6.1}
\]

on the terminal recurrent support.  The phase term is bounded and `h` is
positive on every active coordinate.  Hence (6.1) is incompatible with an
escaping occupation in one communicating class.

## 8. No hidden critical branch

The zero conclusion is edgewise zero **after complete faster relaxation**,
not merely zero stationary mean.  Therefore the corrected macroincrement has
zero variance.  Excursions removed at a faster normalization have uniform
geometric carrier moments; if their counts dominate, the lexicographic Green
construction selects that faster trace instead.  Thus an escaping critical
random walk cannot be hidden inside a zero effective class.

## 9. Conclusion

Every terminal chart has exactly one of:

1. strict negative corrected workload flux;
2. positive structural-exit flux;
3. a bounded-phase affine invariant positive on the escape cone;
4. one of the certified deficiency-zero or service alternatives.

This is the finite-priority actual-target trace theorem.
