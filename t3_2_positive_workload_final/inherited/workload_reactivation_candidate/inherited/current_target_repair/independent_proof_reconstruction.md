# Independent proof reconstruction

## Theorem

Every finite bimolecular weakly reversible stochastic mass-action network
with at most three dynamically active species and at most two active linkage
classes is positive recurrent on every closed communicating class, for every
positive rate vector.

The proof below uses the certified single-linkage target theorem only for
actual carried targets, the certified reaction-count Green theorem, and the
certified finite two-active atlas.  It never conditions on a future reaction.

## 1. Reduction to an escaping embedded occupation

Fix an infinite closed irreducible population class \(\Gamma\), and mark the
target of every actual labelled reaction.  If the embedded chain had infinite
mean positive return to a state \(o\), the certified reaction-count Green
theorem would give finite-volume stopping times \(\tau_M\), diverging means
\(T_M=\mathbb E_o\tau_M\), and probability transition occupations

\[
 \nu_M(x,e)=T_M^{-1}\mathbb E_o
 \sum_{n<\tau_M}\mathbf1\{X_n=x,E_{n+1}=e\}.
\]

They escape every finite population set and satisfy exact transition balance.
For every nonnegative physical workload \(h\), after subsequence extraction,

\[
 \sum_{x,e}\nu_M(x,e)h\cdot\zeta_e\longrightarrow h\cdot q,
 \qquad q\ge0.                                  \tag{1.1}
\]

No continuous-time intensity is normalized.

## 2. Terminal chart

Push \(\nu_M\) to the compact descriptor of
`terminal_chart_localization.md`.  Finite flow decomposition gives a
positive-mass terminal chart with:

* fixed active coordinate set;
* a finite inactive-coordinate box up to arbitrarily small exit flux;
* fixed capped availability and enabled source set;
* a complete finite physical source flag and compact tied-rate cells;
* a rational integer-scaled workload \(h\), positive on every active
  coordinate;
* zero normalized structural-exit flux.

The local workload balance is

\[
 \sum_{x,e}\nu(x,e)h\cdot\zeta_e\ge0.          \tag{2.1}
\]

A distributed occupation near different coordinate faces splits before this
selection; no mixed source is declared enabled merely because different
parts of the occupation make its different species large.

## 3. Source-layer count trace

Let \(\mathcal F_1\gg\cdots\gg\mathcal F_m\) be the chart source flag.  For
layers \(i<j\), the pointwise physical rate ratio tends uniformly to zero:

\[
 \Lambda_j(x)\le\varepsilon_{ij}(R)\Lambda_i(x),
 \qquad \varepsilon_{ij}(R)\to0.               \tag{3.1}
\]

Summing embedded source probabilities gives the same inequality for expected
labelled reaction counts.  Tied source and labelled-channel counts have
uniform positive ratios on the compact cell.

Starting with the fastest layer, contract recurrent zero-workload classes by
exact finite Poisson correctors.  If a layer count is bounded, its bounded
jumps have bounded endpoint displacement.  If it diverges, normalize by that
count.  Strictly slower layers disappear by (3.1), while faster layers have
already been made complete-workload neutral.  Some changing layer must have
diverging count: neutral reactions alone remain in a finite \(h\)-shell.
The source flag is finite, so this procedure reaches a first occupied
changing trace.

## 4. Return-prefix charging

Let a reaction \(s\to u\) in source layer \(k\) increase \(h\).  A directed
return path from \(u\) to \(s\) exists in the same linkage.  Truncate at the
first target \(v\) with \(h\cdot v\le h\cdot s\).  Every retained source has
strictly greater workload than \(s\), hence belongs to a faster source layer,
and

\[
 h\cdot(u-s)+h\cdot(v-u)=h\cdot(v-s)\le0.       \tag{4.1}
\]

The reaction \(s\to u\) is not conditioned upon.  Once it actually fires,
\(u\) is the physically present current target that initializes the carrier
trace.

## 5. Finite carrier phase and service race

The carrier trace observes only actual target changes, genuine destruction of
target availability, service, source-layer interruption, and chart exit.
Unrelated reactions that leave the current target enabled are skipped.  They
do not delay its physical clock.

The carrier phase is finite:

* active-only unary or binary targets remain enabled until a declared lower
  shell/support exit;
* a target \(I_i+D\) with bounded cofactor \(D\) can lose its last \(D\) at
  active order only through another source \(I_j+D\); the actual target of
  that reaction is another finite carrier phase;
* bounded-source theft is a strictly slower interruption.

At every carrier phase, the retained carrier source is faster than layer
\(k\).  The ratio of all layer-\(k\) and slower hazards to its hazard is at
most \(\varepsilon_R\to0\).  Exact exponential-race compensation is
unchanged by skipped unrelated jumps.

After successive faster tied classes are contracted, the finite carrier
kernel has one of:

1. return of the physical workload to its pre-activation level, or chart
   exit, in uniformly finite mean carrier time;
2. a closed class with no clearing edge.

The second possibility is completely classified in
`carrier_classification.md` and
`certified_components/actual_target_episode_elimination.md`.  The second possibility is classified by the active-set geometry.  It is
impossible with all coordinates active; in a two-active chart it is a
shielded atlas class; in a one-active chart it is the exact service-token
invariant class.  With three active coordinates it is impossible.
With two active coordinates it is a shielded assignment and hence a common
invariant, deficiency-zero system, or certified service system.  With one
active coordinate it is the explicit service-token invariant.

Outside those terminal alternatives there is a finite \(K\) such that

\[
 \mathbb P\{\text{layer-}k\text{ interruption before service/exit}\}
 \le K\varepsilon_R.                            \tag{5.1}
\]

This is finite M-matrix absorption, not an assumed mixing estimate.

## 6. High-credit return without an obligation phase

Scale \(h\) to integer values.  Let \(\delta\) be its least positive reaction
increment and \(D\) its largest positive reaction increment.  Relative to
the level immediately before a positive layer-\(k\) reaction, use the
physical scalar

\[
 Q=(h\cdot X-h\cdot X_0)_+.
\]

Service lowers \(Q\) by at least \(\delta\).  A layer-\(k\) interruption can
increase it by at most \(D\).  From (5.1), one trial has drift

\[
 \mathbb E\Delta Q
 \le-(1-K\varepsilon_R)\delta+K\varepsilon_RD
 \le-\delta/2                                  \tag{6.1}
\]

for all sufficiently large chart thresholds.  The additive drift theorem,
proved by bounded stopping and monotone convergence, gives finite mean return
to \(Q=0\).  Every trial has finite mean physical duration by the carrier
Green bound.  Thus repeated same-layer positive reactions are included at
their natural probabilities and cannot create a critical branching tail.
The mean unfinished credit at a killed boundary is uniformly bounded and
vanishes after division by the diverging source-layer count.

At the clearing endpoint the complete effective physical workload reward is
nonpositive.  An unpaired service gives a strict negative effective edge.

## 7. Finite source-layer induction

At the fastest occupied changing layer, the first-changing-source theorem
makes every changing edge nonpositive and at least one strict.  Contract its
zero recurrent classes.  Inductively, Section 6 replaces every positive edge
of the next layer by a finite-mean nonpositive clearing transition.  Hence
all effective transitions at every layer are nonpositive.

On a finite recurrent effective phase:

* if a negative transition occurs, strict positivity of the stationary phase
  measure gives negative mean workload reward, uniformly on the compact tied
  cell;
* if the mean is zero, every positive-probability transition has zero
  workload reward.

Zero classes are passed to the next slower physical trace.  If all layers are
zero, the endpoint process remains in one finite physical \(h\)-shell after
finite-mean clearing excursions.  Its finite endpoint trace is positive
recurrent and cannot support an escaping Green occupation.  An affine phase
invariant may also be recorded, but is not required for this conclusion.

The conditional activation counterexamples are harmless in this induction.
Their positive activation is retained at its natural layer, and its faster
return-prefix service is charged before the layer is contracted.  No sign is
assigned to “activation plus one selected target block.”

## 8. Active-set cases

### 8.1 Three active coordinates

Every possible bimolecular source is physically enabled.  The first occupied
changing layer therefore contains a strict negative channel with positive
normalized tied-layer flux.  Equation (2.1) is contradicted directly.

### 8.2 Two active coordinates

Use the certified atlas without alteration.

* If a linkage is available, Sections 4--7 give strict current-target
  charging or a structural exit.
* If both are shielded, the exact atlas gives 382 common-invariant
  assignments, 60 deficiency-zero assignments, and four ordered service
  assignments, with none unclassified.
* The common-invariant branch contradicts escape inside one communicating
  class.
* The deficiency-zero branch has a summable product-Poisson stationary
  probability.
* In the two service architectures, the mixed linkage preserves \(W=B-C\)
  and the other linkage supplies a finite-mean trial with
  \(W_\tau\le W_0-1\), or a declared promotion/exit.

### 8.3 One active coordinate

Apply `one_active_current_target_theorem.md`: quadratic descent from `2A`,
Poisson-corrected linear descent, creator-service descent, box/support exit,
or the exact affine token invariant.

### 8.4 No active coordinate

The chart is finite and cannot carry escaping occupation.

Every terminal chart therefore contradicts (2.1) or already supplies a
stationary probability.

## 9. Embedded and continuous time

No escaping reaction-count occupation exists, so the embedded chain has
finite expected positive return count.  At every nonabsorbing state one
enabled falling factorial is a positive integer; hence the total rate is at
least the smallest positive channel rate.  Embedded finite mean return gives
finite mean physical return.

Population-increasing channels have source molecularity at most one, so the
aggregate upward rate is at most linear in total population.  Between upward
jumps, neutral and decreasing reactions stay in a finite total-population
shell.  Comparison with a linear pure-birth process proves nonexplosion.
Therefore every closed irreducible CTMC class is positive recurrent and has a
unique stationary probability.
