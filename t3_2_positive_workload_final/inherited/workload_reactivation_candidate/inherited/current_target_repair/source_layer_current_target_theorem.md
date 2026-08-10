# Rate-weighted current-target priority theorem

## 1. Scope

Fix a terminal chart of a finite bimolecular network with at most three
active species and at most two linkage classes.  The chart fixes the active
coordinate set, a finite box for inactive coordinates, the enabled source
set, a complete physical source-rate flag

\[
  \mathcal F_1\gg\mathcal F_2\gg\cdots\gg\mathcal F_m,
\]

and a compact positive cell for the ratios inside every tied layer.  Let
\(h\in\mathbb Q^3_{\ge0}\) be an integer-scaled scalarization of the complete
flag, positive on every active coordinate.  The order of \(h\cdot y\) agrees
with the flag order of every enabled source complex.

All stopping rules below use the actual current target of the last labelled
physical reaction.  No future reaction is conditioned upon.

## 2. Return prefixes

Let \(e:s\to u\) satisfy

\[
 d_e=h\cdot(u-s)>0.
\]

Because \(u\) lies in the same strongly connected linkage class as \(s\),
choose a directed path from \(u\) back to \(s\).  Stop it on first reaching a
complex \(v\) with \(h\cdot v\le h\cdot s\).  Every source on the retained
prefix has workload strictly larger than \(h\cdot s\).  Hence every retained
source belongs to a strictly faster source layer.  Moreover

\[
 h\cdot(u-s)+h\cdot(v-u)=h\cdot(v-s)\le0.       \tag{2.1}
\]

This is a graph identity, but the first complex \(u\) is also the actual
physical target produced by \(e\).

## 3. The finite carrier phase

While a return-prefix obligation is outstanding, retain only:

* the actual carried target complex;
* the bounded inactive-coordinate values and capped availability;
* the tied source-ratio cell;
* the linkage and return-prefix position;
* the finite zero-class correctors already produced at faster layers.

Unrelated reactions that leave the required target source enabled are skipped
by the carrier trace.  They cannot delay its physical reaction clock.  A
reaction that genuinely destroys availability of the carrier is retained;
its actual target becomes the next carrier.  In the terminal chart this gives
one finite carrier graph.

The finiteness assertion uses bimolecularity.

1. A unary active carrier stays enabled until the corresponding active
   coordinate leaves the chart.
2. A binary carrier containing two active particles stays enabled under
   bounded jumps until a lower-shell or active-support exit.
3. A carrier \(I_i+D\), with \(D\) inactive and bounded, can lose its last
   \(D\) at active order only through another source containing \(D\).  Such
   a source is one of finitely many complexes \(I_j+D\), and its actual target
   is again a finite carrier phase.  A source containing no active particle
   is a strictly slower interruption.

Thus no unbounded population count is stored in the carrier phase.

## 4. Carrier-clock estimate

At a carrier phase whose current source belongs to a layer strictly faster
than \(\mathcal F_k\), let \(\lambda_c\) be the aggregate rate of the
current-target source and \(\lambda_{\ge k}\) the aggregate rate of all
unprocessed layer-\(k\) or slower sources.  Uniformly on the compact chart,

\[
 \frac{\lambda_{\ge k}}{\lambda_c}\le\varepsilon_R,
 \qquad \varepsilon_R\longrightarrow0             \tag{4.1}
\]

as the chart workload threshold \(R\to\infty\).

Until the carrier is fired or genuinely disabled, unrelated reactions do not
alter either clock.  Exponential-race compensation therefore gives

\[
 \mathbb P\{\hbox{a layer-}k\hbox{ interruption occurs first}\}
 \le\varepsilon_R.                                \tag{4.2}
\]

After a genuine carrier transfer the same estimate holds at the new finite
phase.  Contract faster tied recurrent classes in their lexicographic order.
On a finite carrier graph, either:

* the physical workload returns to its pre-activation level (or below) in a
  uniformly bounded mean number of carrier changes;
* positive chart-exit flux occurs; or
* a closed no-clearing carrier class remains.

A closed no-clearing carrier class has no executable faster return-prefix
exit.  In the fully active chart this is impossible.  In a two-active chart
it is one of the shielded finite atlas classes; in a one-active chart it is
the service-token invariant class.  With three
species and two linkages, the certified atlas classifies it as a common
workload invariant, a deficiency-zero class, or one of the two service
architectures.  The one-active version is the service-token alternative of
`one_active_current_target_theorem.md`.

Outside those terminal alternatives, there is a finite constant \(K\),
uniform on the compact tied-rate cell, such that

\[
 \mathbb P\{\hbox{layer-}k\hbox{ interruption before service}\}
 \le K\varepsilon_R.                             \tag{4.3}
\]

No mixing estimate for the full fast population process is used.

## 5. Physical workload credit, not an obligation phase

Scale \(h\) to have integer coordinates and let \(\delta>0\) be the smallest
strict positive workload increment.  Start immediately before a positive
layer-\(k\) reaction and put

\[
 Q_n=\bigl(h\cdot X_n-h\cdot X_0\bigr)_+.
\]

This is a physical scalar level, not a count of labelled obligations and not
a component of the finite phase.  Let \(D\) be the largest positive workload
jump of any bimolecular reaction.

A carrier service lowers \(Q\) by at least \(\delta\).  A layer-\(k\)
interruption increases it by at most \(D\).  Therefore one carrier trial has
conditional drift

\[
 \mathbb E[\Delta Q\mid\mathcal F]
 \le -(1-K\varepsilon_R)\delta+K\varepsilon_R D. \tag{5.1}
\]

For sufficiently large \(R\), the right side is at most \(-\delta/2\).
Optional stopping of \(Q_{n\wedge\tau}\) gives finite mean return to
\(Q=0\), with

\[
 \mathbb E\tau\le 2Q_0/\delta                    \tag{5.2}
\]

in carrier trials.  Every trial has finite mean physical duration by the
carrier-clock estimate.  Repeated positive layer-\(k\) reactions are thus
included at their natural probabilities; no activation is conditioned upon.
At the clearing endpoint,

\[
 h\cdot X_\tau\le h\cdot X_0.                   \tag{5.3}
\]

If a strict service occurs with no outstanding positive credit, the
inequality is strict.

## 6. Induction over source layers

Proceed from the fastest source layer to the slowest.

* At the fastest occupied changing layer, the first-changing-source theorem
  makes every changing reaction nonpositive and at least one strictly
  negative.
* Suppose all faster positive reactions have been replaced by the clearing
  episodes above.  Their effective workload rewards are nonpositive; faster
  zero recurrent classes are contracted with exact finite Poisson
  correctors.
* A positive reaction in the next layer has the faster return prefix (2.1),
  so Sections 3--5 replace it by a finite-mean nonpositive effective
  transition, or by a certified exit/invariant/exceptional branch.

Hence every effective transition at every processed layer is nonpositive.
On each finite recurrent effective class, either a negative transition has
positive stationary mass, giving strict negative mean, or every transition
has zero reward.  In the latter case the endpoint workload is constant.  The
endpoint process remains in one finite physical workload shell; its clearing
excursions have finite mean.  It therefore cannot support an escaping
reaction-count occupation.  A finite coboundary or affine invariant may be
recorded, but is not needed to infer this finite-shell recurrence.

Because the physical source flag is finite, the induction terminates.  If no
strict layer occurs, the zero coboundaries either:

1. glue to an affine workload invariant positive on the chart escape cone;
2. return the physical workload to the same finite shell after every
   finite-mean clearing excursion; or
3. fall in the certified deficiency-zero or service alternatives.

There is no infinite hierarchy and no discarded rare linkage.  A linkage
whose count vanishes at one normalization appears at the next slower source
trace.

## 7. Current-target interpretation

Every physical reaction is charged once.

* Its residual-factorial increment belongs to the episode that was already
  running from the previously carried actual target.
* Its actual target is the initial carrier of the next source-layer service
  routine.
* An available same-linkage target episode begins only from that actual
  target.

The false operation “condition on this reaction and append its target
episode” never occurs.  The mandatory cycles

\[
0\to2A\to A\to0
\]

and

\[
A\rightleftarrows2A,
\qquad0\to A+B\to B\to0
\]

are classified correctly: their conditioned activation blocks are positive,
but the faster physical return-prefix layer has strict negative service and
the complete unconditioned source-layer trace is nonpositive with an
unpaired strict death at high population.

## 8. Theorem

In a terminal three-species, two-linkage chart, the source-layer trace has
exactly one of:

1. a finite-mean episode with strictly negative corrected workload reward;
2. positive lower-shell, active-support, source-flag or structural-exit flux;
3. a common affine invariant positive on the escape cone;
4. a deficiency-zero product-form branch;
5. one of the two certified service branches.

This is the rate-weighted current-target charging theorem.
