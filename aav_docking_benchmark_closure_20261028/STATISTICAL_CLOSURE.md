# Statistical closure assessment

Assessment date: 2026-10-28. Upstream frozen at `e9d39e3ef1c58647c2bf9dea7dfc90f823198791`. Independent statistical assessment of `snapshot/PROTOCOL.md` and `snapshot/BIBLIOGRAPHY.md`; no new docking or biological results were generated. Assessment complete; confirmatory research remains unperformed.

## What can be concluded

The broad question is not a single identifiable yes/no hypothesis. A finite benchmark can establish measured performance of named, frozen workflows on a defined distribution of structures, ligands, information regimes, assay contexts, and compute budgets. It cannot establish universal reliability of molecular docking. A single validated failure refutes an assertion of perfect reliability, but does not establish low average performance or failure of all algorithms.

The defensible finish line is a bounded claim: “For the prespecified eligible cohort and information regime, workflow M achieved family-macro site recovery S, pose recovery P, and, where experimentally labeled data existed, specificity discrimination D, with uncertainty intervals and documented unsupported chemistry/preparation failures.” A biological-recognition claim requires specificity evidence in addition to structural recovery. If no admissible specificity labels exist, finishing the site/pose benchmark leaves that portion of the motivating question open.

## Separate estimands

1. **Site discovery:** Top-1/Top-5 recovery of a prespecified experimental site class, merging symmetry copies. Native-ligand-derived boxes are ineligible for this endpoint.
2. **Pose recovery:** Top-1/Top-5 near-native recovery after the prespecified receptor alignment, valid chemical atom mapping and symmetry handling. Report oracle-site and predicted-site regimes separately.
3. **Specificity:** Ranking tested binders against tested nonbinders, or ranking comparable quantitative measurements, within a single assay/protein context. A nonnative geometric pose is not automatically a biologically nonbinding site. An unoccupied surface patch in one structure is not a tested negative.
4. **Practical coverage:** Fraction of all prospectively eligible cases yielding valid output. Retain chemical parameterization/preparation/search failures in a workflow-level endpoint; report conditional algorithm accuracy separately. Quiet exclusion can turn a difficult chemistry class into an apparent success.

For complex j in family g and seed r, let Y(g,j,r,m) be a binary success for workflow m. Average over seeds, then complexes within each family, then families, to estimate a family-macro score. For a comparison, calculate within-family paired differences before averaging. Seeds, poses, and 60 symmetry-related capsid copies are not independent biological observations. Family-macro weighting is an explicit target-population choice; also show per-complex results so readers can inspect that choice.

## Sampling versus ranking: the identifiable part

For a fixed retained candidate pool define C = “at least one near-native candidate is retained” and T = “a near-native candidate appears in the final Top-k.” Because T implies C,

    P(T) = P(C) × P(T | C).

This is a useful exact decomposition of *retained-pool coverage* and *ranking conditional on that pool*. It says nothing by itself about candidates generated internally and discarded before export. If no near-native candidate is returned, sampling failure and pre-export score filtering are observationally confounded. Label that outcome “no near-native pose in returned pool,” rather than claiming a proven sampling failure.

To isolate scoring, rescore the same frozen pool with each scoring method, preserve candidate identities, and compare ranking conditional on near-native coverage. Report which generator supplied each pose and pool composition; a scorer cannot recover a pose absent from the pool. To separate internal sampling from internal filtering, retain candidates before selection or instrument the search. Native-pose injection/scoring is an additional scorer diagnostic, not a docking success.

## The proposed sample size is a pilot-scale target

The protocol correctly describes 24–36 complexes across at least 12 families as a feasibility target rather than a power calculation. Twelve independent families generally give wide uncertainty for population-level reliability and few units for subgroup/interaction claims. Adding more structures from the same families improves within-family measurement but does not create the same information as new independent families.

Checkable illustrations below assume independent identically distributed Bernoulli observations from a target population. Those assumptions do not automatically hold for fractional family-macro outcomes or a curated convenience cohort. The calculations illustrate why a small successful benchmark cannot certify a high population reliability floor.

If all n observations succeed, the two-sided 95% Clopper–Pearson lower bound is `0.025^(1/n)` (the lower-tail inversion is p^n = 0.025). The one-sided 95% lower bound is `0.05^(1/n)`.

| Independent observations, all successful | Two-sided 95% lower bound | One-sided 95% lower bound |
|---:|---:|---:|
| 12 | 0.73535 | 0.77908 |
| 24 | 0.85753 | 0.88265 |
| 36 | 0.90261 | 0.92015 |

Even 12/12 successes cannot certify an 80% reliability floor at one-sided 95% confidence under this favorable binomial model. With no failures, at least 29 independent observations are needed for a one-sided lower bound exceeding 90%; at least 36 for a two-sided interval whose lower bound exceeds 90%. These are *best-case all-success requirements*, not adequate sample-size plans under realistic failure rates. Counting 36 complexes as 36 independent units despite only 12 families would invalidate that reasoning.

For a rough independent-binomial precision calculation at worst-case p = 0.5, a normal 95% half-width is `1.96 sqrt(0.25/n)`: approximately 0.283 at n = 12 and 0.163 at n = 36. Target half-widths 0.15 and 0.10 give nominal n = 43 and 97, respectively, before clustering/design complications. Near boundaries, use valid interval procedures rather than these normal approximations. Paired contrasts may be more precise; their precision depends on the distribution of family-level paired differences, which must be estimated, not assumed.

The proposed cluster bootstrap preserves pairing and is directionally appropriate, but 10,000 resamples do not create more than 12 independent families. A bootstrap of all-success observations can produce a degenerate [1,1] interval; it must not be presented as proof of certainty. Show family scores and a suitable small-sample/model sensitivity analysis, and distinguish uncertainty for this fixed cohort from transport to unseen families. A paired family-level model or randomization/permutation analysis requires its own stated assumptions; none is an automatic cure for a small cohort.

## Prevent specificity from collapsing into size/charge prediction

Use tested positives and negatives with provenance, concentration/detection limits, and assay conditions. Keep “not tested” separate. Predeclare handling of nondetects/censoring and conflicting labels; do not recode every nondetect as an exact zero affinity. Array signal, affinity, and cellular transduction measure different quantities and should not be pooled into one response variable.

Compare within each target against prespecified simple size/charge baselines. Report raw discrimination and matched or adjusted discrimination. Matching changes the estimand to discrimination among similar-size/charge glycans; it does not reveal a universal “deconfounded” binding truth, and charge can be part of the real mechanism. Matched groups may shrink the admissible cohort and need adequate positives and negatives. Report AUROC and AUPRC with prevalence, per-target results, and family-aware uncertainty; assess whether a pooled score is merely recognizing target or assay identity. For quantitative rankings use comparable measurements and uncertainty/censoring-aware comparisons.

If the goal is an operational binder classifier, ranking quality alone is insufficient. Freeze a score threshold on development data, then evaluate held-out sensitivity, specificity, predictive value at a stated prevalence, and calibration if binding probabilities are claimed. Do not infer experimental affinity or a dissociation constant directly from a docking score.

## Prespecified stop rules

Choose a scoped primary claim, endpoint, and practically useful floor q or improvement margin delta before scoring the confirmatory test set. A threshold can depend on the intended scientific use; this audit supplies no arbitrary biological utility threshold.

- **Adequate evidence of reliability:** the prespecified lower confidence bound exceeds q, and structural/chemical quality, coverage, and leakage gates pass. Scope the conclusion to the tested conditions.
- **Evidence below the required reliability:** the upper confidence bound is below q. This answers the operational question negatively for that workflow and scope.
- **Inconclusive:** the interval crosses q. Failure to reject a null is not proof of equality or unreliability.
- **Meaningful improvement:** the lower bound on a prespecified paired difference exceeds delta. A positive point estimate alone is insufficient.
- **Practical equivalence:** the entire appropriate interval lies inside prespecified equivalence margins. A nonsignificant difference is insufficient.
- **Specificity unavailable:** finish a site/pose paper with specificity explicitly unresolved; do not replace missing experimental negatives with generated decoys.

If no defensible utility floor is chosen, report a descriptive benchmark and uncertainty rather than inventing a yes/no reliability verdict afterward. Declare a limited primary comparison and a multiplicity strategy for separate confirmatory claims; treat the remaining cross-products of algorithms, regimes, receptor states, chemistries, and waters as secondary/exploratory unless sample size supports them. Do not fit a large interaction model to 12 families.

Define an enlargement rule or sequential inferential procedure before collecting more confirmatory outcomes. “Keep adding until the interval is favorable” is not a valid fixed-sample design. If development outcomes cause changes in parameters, metrics, exclusions, or the primary endpoint, use a later untouched test cohort for the revised procedure.

## Adversarial checks and remaining gap

Before promotion, independently rerun native-coordinate metric controls; inspect site-definition leakage, family/fold and training overlap, valid atom permutations, reference uncertainty, symmetry equivalence, missing ligand atoms and denominator exclusions. Test sensitivity to threshold, receptor alignment, input chemistry, complete assembly, family weighting, and compute budget. Keep an accessible per-case audit trail linking raw outputs to every aggregate number.

The strongest result of this assessment is a falsifiable, finite-scope decision framework. The exact remaining gap is empirical: a frozen eligible cohort, independently validated references/labels, complete reproducible workflow outputs, and uncertainty estimates adequate for the chosen claim. No population performance estimate or mechanistic conclusion follows from the protocol alone.
