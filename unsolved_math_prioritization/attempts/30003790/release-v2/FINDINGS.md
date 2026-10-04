# Findings

## Affirmative literal bounded-model result

For each fixed finite `D`, every Borel design law `P` on `R^D`, bounded continuous
`F` on `supp(P)`, iid regression pairs, and noise satisfying
`E[ε|X]=0` and `E[ε²|X]≤σ²<∞` almost surely with one common bound, the accepted
sample-split tangent-neighbor safeguard is consistent in expected integrated squared
error. Its sample-conditional integrated squared error tends to zero in probability.

An independently trained field is jointly measurable in training data and covariate
and has norm at most one. It can be inaccurate. All `n` regression covariates are
ranked by tangent-projection distance plus a positive Euclidean guard. Ties use
deterministic sample index, and neither field assignment nor selection uses regression
responses. The test point is independent of the joint observed training/regression
data. An unverified coarse-segment filter is not part of this construction.

Both a fixed guard `0<λ≤1` and the local choice
`λ_n(x)=min(1,sqrt(R_n(x)+1/n))`, where `R_n(x)` is the kth Euclidean-neighbor
radius among all `n` covariates, are accepted. Here `k_n→∞` and `k_n/n→0`.
The local guard vanishes in probability. No density, lower-mass, bounded-support or
covariate-moment assumption is required for this theorem.

This is an affirmative answer to literal noisy consistency under that explicit model.
The exact accepted theorem/proof is unchanged in `public/AUXILIARY_THEOREM.md`:
SHA256 `072aba944c908baf44bb86d6c9a3d1c87444b5f779c53a14b4a9648d9595351c`.
Acceptance is bound by the fresh audit SHA256
`954dedd9ec67d2819b211aa6cbb6f33cd578977175fb1478ede820aa3f4aab6f`.

## Remaining gap and queue disposition

The short OWR source does not fully specify target integrability, boundedness/domain
conditions or the noise-identification assumptions. Coverage of every distribution
allowed by that incomplete description has therefore not been verified. Conservative
queue disposition stays `unsolved`, 5/5. This status does not deny the affirmative
bounded-model result and does not impose an unstated dimension-efficiency condition.

Dimension-efficient geometric rates, accurate tangent/coordinate recovery,
almost-sure risk consistency, uniform consistency and unbounded/discontinuous target
extensions are not established by the accepted theorem. They must not be silently
added to its conclusions. The original quantitative theorem remains available under
its stronger lower-mass and Hölder assumptions.

## Attribution and verification

No novelty is claimed. Generic nearest-neighbor regression consistency is longstanding;
see C. J. Stone, *Consistent Nonparametric Regression*, Annals of Statistics 5(4),
595–620 (1977), https://doi.org/10.1214/aos/1176343886. This attribution does not
substitute for the independent check of the specific safeguarded ordering.

The first audit's moment, interior-projection/almost-everywhere, joint-measurability
and response-independent tie corrections are applied to the corrected author copy.
Original evidence is preserved byte-for-byte. The complete corrected release awaits
binding review before any publication authorization.
