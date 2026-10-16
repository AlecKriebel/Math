# Fresh source, formulation, and adversarial audit

## Decision

The submitted elementary obstruction is correct for its explicitly stated target: a dimension-independent positive factor, all finite ground sets and normalized nonnegative monotone submodular inputs, and one ordinary matroid rank on the original ground set. The mathematical proof uses the source's actual two-sided comparison, including its left denominator. The submitted report also states the interpretive limitation that the source does not separately write a quantifier over ground sets. Keep that qualification wherever the result is summarized.

No mathematical defect or unsupported strengthening of the source's approximant class was found. The original question's conventional uniform interpretation is reasonably supported; it is not an explicitly printed `forall V` clause. The audit makes no conclusion about an unknown different intended formulation. It supplies no exhaustive priority, novelty, or current-open-status certification.

## Frozen input and independence

- Subject: PR 1047 / problem 30004909 / OWR-8415356-020.
- Head identifier: `56b3a35182e5cb04b05e41f5017e47caf50582c1`.
- All nine original submitted files and `SUBMITTED_PINS.json` were copied into `frozen/` at the first checkpoint, 2026-10-13T23:05:51.131182+00:00. Each byte count and SHA-256 matches the provided pins; see `FROZEN_VERIFICATION.json`.
- The head binding is through those provided submitted pins; this worker did not query Git or a PR service to independently reconstruct the remote commit.
- Read the complete frozen submitted `REPORT.md`, then retrieved and inspected primary sources independently.
- Saved the full [independent comparison](INDEPENDENT_PRIMARY_COMPARISON.md) and its immutable checkpoint hash at 2026-10-13T23:08:42.147292+00:00 before opening any old audit, acceptance, provenance, status, README, or manifest body.
- Only afterward read the remaining eight submitted bodies. No other worker, external individual, or external peer was consulted. No subagent was spawned and no Git index, PR, publication, release, branch, or queue operation was performed.

The actual source locators, displayed symbols, interpretation, independent derivations, and hostile boundary checks are recorded in the independent comparison. It is preserved unchanged after the checkpoint so the ordering can be checked against `PRECOMPARISON_CHECKPOINT.json`.

## Mathematical findings

The adversarial analysis did not assume a symmetric, representable, simple, or uniform approximating matroid. It tested a basis chosen from any proposed approximant and the entire same ground set. Singletons exclude loops and give both positive total rank and a factor at least one. Thus the crucial divisions are valid, and the universal-subset quantifier licenses testing a basis that depends on the approximant.

The square-root family's decreasing increments establish submodularity with all empty-sum cases. Its basis and full-set inequalities force `R <= alpha^2` and `sqrt(n) <= alpha R`, hence `alpha >= n^(1/6)`. An integer `n > alpha^6` contradicts every proposed fixed factor. This is a complete universal counterexample argument, not numerical evidence alone.

The rational family has increments `1, 1/m, 1/m, ...`; it therefore satisfies the same input conditions. On `m^2` elements the comparisons force `alpha^2 + alpha >= m`, the stated quadratic root bound, and `alpha >= n^(1/4)/sqrt(2)`. The derivation neither divides by `m-alpha` nor omits a sign case. The one-element and `m=1` boundaries are benign. The non-integer-only wording also permits the unbounded family by choosing `n >= 2` or `m >= 2`.

A general independent calculation checks the intermediate-set challenge: for any monotone normalized concave cardinality function `phi`, total rank `R` requires the factor `max(R/phi(R), phi(n)/R)`, and the uniform matroid attains it. This establishes the report's square-root-family optimum over all matroids, including integer-rank rounding and exact attainment on cube sizes. It does not establish an optimal exponent over the entire input class. Both submitted families belong to one basis/full-set mechanism.

## Comparison with actual submitted records

| Submitted record | Faithful comparison and outcome |
| --- | --- |
| `REPORT.md` | Full proof, normalization, lower bounds, exact square-root optimum, same-ground ordinary-rank scope, and missing explicit ground-set quantifier agree with the independent comparison. No novelty claim. PASS. |
| `SOURCE_AUDIT.md` | Correctly reports the original denominator, local rank-name inconsistency, full contribution boundary, single-rank class, and uniform-reading qualification. Its hostile proof checks are independently reproduced. Its official PDF size/hash equal the freshly retrieved source. PASS for present source/math claims. |
| `ACCEPTANCE.md` | Accepts precisely the explicit uniform target and limits sharpness to one input family. Explicitly distinguishes AI-assisted acceptance from human peer review and formal certification. Its 9 October acceptance events remain historical claims, not newly authenticated events. PASS for scope and mathematical content. |
| `PROVENANCE.md` | Correct source scope and appropriately bounded attribution. Its absence-of-source-redistribution claim is consistent with the nine submitted text/JSON members. Claims of byte preservation and private-history-only selection relative to earlier originals cannot be certified without those predecessors. No contradiction found. |
| `SOURCE_PROVENANCE.json` | Official source size/hash verified anew. Source correction, notation, quantifier, and output-class cautions agree. Its earlier GHIM inspection scope names Problem 1 and does not assert a whole-body reading; this worker's fresh whole-body reading extends the evidence without rewriting that historical metadata. Historical retrieval/search events are not re-certified. |
| `STATUS.json` | Correctly limits the negative result and all numerical bounds. One substantive mechanism with two families is accurate. Novelty, priority, and current-open-status claims are expressly false. PASS. |
| `README.md` | Scope, source qualification, optimal-family claim, and publication/verification limits agree with the proof and audit. PASS. |
| `MANIFEST.json` | All eight non-self entries match the frozen files, and membership enumerates the nine submitted members. PASS for internal integrity. |
| `ARTIFACT_MANIFEST.json` | All three listed member identities match. It labels its selected inventory and exclusions. PASS for internal integrity; preservation of omitted predecessor categories is outside this worker's evidence. |

The manuscript's corpus-denominator-error assertion is consistent across the edition. This worker freshly confirms the publisher formula, but did not inspect the corpus or its history. Accordingly the publication-source correction is verified, while the historical origin of the incorrect transcription is reported as a submitted-record assertion.

## Related-paper interpretation and priority boundary

The entire named ten-page author-hosted GHIM body, rather than merely its abstract, was read and its relevant formulas rendered. The independent comparison gives the precise Problem 1, Figure 1, and Section 4-6 locators. The existence obstruction cannot be inferred from a query-indistinguishability result on inputs that are already matroid ranks: those inputs themselves give an existential rank approximant with factor one. This is a checkable mathematical distinction, not a dismissal based on the abstract. The square-root input also belongs exactly to the square-root-of-modular approximant family, so its use is not asserted as a new submodular construction.

That establishes the difference between the named paper's argument and this submitted obstruction. It does not rule out every implicit antecedent in the literature. The submitted bounded search and lack-of-priority claim must remain bounded. Exhaustive priority work is a separate audit and does not determine whether this elementary proof is valid.

The original source's integer-valued observation was checked through the ordinary rank axioms: normalization and diminishing returns give `f(S) <= |S|`, while the other axioms are supplied by its stated hypotheses. Thus there is no hidden extension to weighted ranks or an integer polymatroid with larger singleton values.

## Checkable artifacts and numerical limits

`validate_scope.py` runs with the standard Python library and bytecode disabled. `VALIDATION_RESULTS.json` records:

- Exhaustive independent-set-system enumeration of all loopless matroids on one through four labeled elements, yielding counts `1, 2, 6, 27`.
- Exact rational comparison of the square-root factor squared with the claimed uniform optimum for all those matroids.
- Fifty-six normalized concave cardinality profiles, tested against all subset pairs and all enumerated matroids, with exact rational agreement with the general optimum.
- 47,905 cardinality triples for square-root submodularity at 80 decimal digits with tolerance `1e-75`.
- 1,496 exact rational total-rank cases for `m=1,...,16`, validating the rational lower bounds and positive-rank boundaries.

All checks passed. Decimal checks are finite-precision evidence, and all enumeration is finite. Neither is a premise of the universal written proof. This is not formal proof-assistant verification or external human peer review.

`EDITION_HASH_CROSSCHECK.json` also records the edition's internal identity checks. These establish packaging integrity, not mathematical correctness or historical preservation relative to unsupplied versions.

## Source handling and access failures

Fresh full-PDF retrievals succeeded for all three sources used as evidence; their URLs, retrieval times, headers, byte counts, and SHA-256 values are in `SOURCES_RETRIEVAL.json`. Third-party PDFs, full extracted text, and rendered images remain exclusively in ignored `sources/raw/`. They are excluded from the authored-output manifest. The authored comparison contains only the required mathematical display, primary-source locators, and bounded paraphrases.

The DOI opening failed through the web tool. Two initial exploratory lecture-note URL openings also failed; the search-located actual MIT lecture PDF was accessible. These failures did not interrupt any needed source inspection. Details are preserved in `ACCESS_FAILURES.json`. No failed mathematical check was observed.

## Final disposition and exact remaining gaps

Accept the mathematical obstruction and the faithful ordinary-rank display interpretation, retaining the report's explicit dimension-independence qualification. No change to the submitted mathematical argument is required by this audit. The notation inconsistency belongs to the original source and is handled correctly by the report.

The remaining gaps are exhaustive historical priority, historical open-status or correction status beyond this source inspection, predecessor-edition preservation, and authentication of earlier review/retrieval events. None is used as a proof premise. No result for an unknown differently intended formulation is asserted.

Audit completion estimate: 100% of this worker's assigned source/formulation review; this percentage is not a probability of novelty or a claim that the wider research program is complete.
