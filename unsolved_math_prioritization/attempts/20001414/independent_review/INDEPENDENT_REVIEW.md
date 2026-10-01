# Independent source-coverage review: AIM Problem29 / 20001414

## Verdict and classification

**PASS_CREDITED_TEMPORAL_W1_METHODS_WITH_EXPLICIT_SCOPE. No mandatory correction.**

The frozen assessment is a valid credited answer to the source's open-ended request for a method of bounding Wasserstein convergence rates, under its expressly stated finite-total-rate temporal-W1 interpretation and analytic hypotheses. I support **already_solved0/5 as a known-method source disposition**, with those qualifications preserved in the queue and PR. This does not mean every local system converges, an optimal rate is known for every model, or the entire possible infinite-volume/infinite-activity research program has been closed.

The original page asks how to bound rates; it does not specify a particular positive exponent or promise locality alone is sufficient. A directly applicable, generator-side transport criterion with explicit sufficient hypotheses answers that methods request. It would be inappropriate to relabel the result as an unconditional convergence theorem, an all-Wasserstein-orders theorem, or a solution for a specified infinite-volume model. If a separately clarified source interpretation were to require those stronger targets, they would remain new open work rather than follow from this assessment.

This review binds SOURCE_ASSESSMENT.md SHA-256648156aeb8d2afa800328e9bd358931a01bd9f9323ab621ea34c8a9d142f1546 and FROZEN_MANIFEST.json SHA-256af5925e0b24dc8bd0fc968ee202d21d9388650dbbea6e7045a36b2815048e57b. The reviewer did not contribute to the assessment. No author proof-search turn or novelty is claimed.

## 1. Original source and editions

I inspected the actual rendered Problem29 on p.3, read the full three-page AIM list and six-page workshop report, and checked the official source navigation. The displayed i is a summation subscript; the imported `> i` is a layout artifact. The imported rate-dictionary title is descriptive metadata, not the source title. The original is an open-ended local-generator question, without a prescribed state space, Wasserstein order or stationary/irreducibility assumptions.

The theorem and proof uses were audited against the complete accessible Villemonais2019v4 and Cheng–Li–Wu2019v1 primary texts. The revised2026 journal title/metadata is separately attributed. The final Cheng–Li–Wu PDF was not available; its zero-byte export is not a proof source. No identity between final theorem numbering and the pinned preprint was presumed, and no access restriction was bypassed.

## 2. Augmented-kernel criterion

The one-state-space criterion is exactly the N=1 case of Villemonais Theorem2.1. For finite jump measures J_x,J_y with rates r_x,r_y, the augmented measures

    J_x+r_y delta_x,     J_y+r_x delta_y

have equal mass r_x+r_y. Their optimal finite-mass transport cost minus (r_x+r_y)d(x,y) is the drift of the distance under the constructed coupling generator. The extra atoms contribute zero to their respective marginal generators. This retains state-dependent clock rates correctly; separately normalizing the two raw kernels would not.

Measurable optimal coupling selection is justified by the stated Polish/metric framework. The finite jump-moment conditions make the distance drift well-defined. Nonexplosion and localization support the exponential coupling estimate. Integrating the pointwise coupled transition bound against an initial coupling yields the probability-measure W1 inequality. The assessment explicitly assumes semigroup preservation of P1; it does not infer that property from a pointwise moment condition alone.

Zero jump mass is harmless: both augmented measures are zero and the cost/drift are zero. The construction also permits null-jump atoms already present in J; they do not change the marginal generator.

## 3. Stationarity and metric hypotheses

For kappa>0, P_(t0) is a strict contraction of the complete metric space P1(E) for every t0>0, under the explicitly assumed preservation of that space. Banach's theorem gives a unique fixed point there. Commutation with every P_s and uniqueness of the P_(t0) fixed point show that it is stationary for the full semigroup. The same contraction estimate gives convergence to it.

The uniqueness statement is correctly limited to P1 for an unbounded metric. No stationary measure with an infinite first moment is silently excluded by an argument performed only on P1. For finite E all probabilities are in P1. If kappa<=0, the asserted inequality may be a growth bound and does not itself prove mixing. The clock-scaling and frozen two-state examples correctly prevent an unconditional positive-rate conclusion.

## 4. Matching local and block generators

For finitely many local terms with finite total rates, the full configuration is one Polish state and J_x=sum_i omega_i(x,.) gives exactly the original generator. This includes state-dependent local block updates; it does not require y to mean one coordinate replacement.

The separate-local-coupling construction is valid: summing the local coupling generators preserves both full marginal generators and adds their distance drifts. It supplies a sufficient bound, with no false assertion that separate local optima equal the optimum for the combined generator. The single-coordinate averaged-product formula follows from Villemonais's actual particle theorem, with unchanged coordinates canceling from each distance drift.

The assessment excludes countably many sites with infinite total rate from this N=1 reduction. Infinite-activity jump kernels likewise do not meet the finite-measure hypotheses. Those exclusions are necessary. They are not silently treated as counterexamples to the stated finite-rate method, nor as solved by it.

## 5. Graph optimality claim

I checked the standing locally finite connected graph assumptions, positive edge rates, conservativity and invariant-probability/recurrence condition(H) in Cheng–Li–Wu v1. Theorem2.2 gives the metric contraction/coupling-generator equivalence in that framework. Theorem2.4 permits a common augmented mass at least the sum of the actual exit rates and realizes the minimum distance drift among coupling generators.

Thus the criterion identifies the best uniform **prefactor-one** contraction constant for a fixed metric in that stated graph setting. It does not identify the best large-time exponential rate with an arbitrary prefactor or after changing the metric. The graph result is extra optimality information; the sufficient Villemonais criterion and its block application do not depend on the restricted final journal text.

## 6. Reproducibility and limits

All eight frozen author files and all seven pinned reading inputs match their hashes. The6019-assertion author receipt replays byte-identically. A separate standard-library checker gives exact primal/dual transport certificates for486 rate-pair cases on a three-point metric that is not a line metric, verifies marginal generator identities and rate normalization, and exhibits32 cases where separate local optima are strictly worse than the combined optimum. Its29126 finite assertions are calibration, not a replacement for the general source/proof review.

The imported upstream machine synthesis is neither a primary theorem nor a previous Alec campaign attempt. This remains a zero-author-turn, credited-source assessment. Preserve the conditional finite-rate temporal-W1 reading, P1/nonexplosion assumptions, positive-kappa requirement for convergence, and final/preprint access distinction in any publication. No historical discovery or proposer acceptance is certified.
