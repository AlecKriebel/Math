# Corrections and scope clarifications

No fatal mathematical error or change of disposition is required. Preserve the frozen packet. The following text is suitable for a later append-only correction or reviewed successor; it must not be read as a new proof attempt.

## C1. Dense prefixes versus the published sparse grid

**Location:** PROOF.md, Approach 3; README summary.

**Classification:** Important scope clarification, not a falsification of an existing claim.

**Suggested addition:** “This construction uses all prefix sizes in the specified range. It is not a counterexample to the manuscript's particular spaced-size Algorithm 2. For total n=k^2, validation k, and its square-root grid, the probability of any exceptional fit is at most (H_(k-2)-1)/k, which tends to zero, regardless of dependence between its sampled subsets.”

**Why:** Pointwise convergence fails to control arbitrary growing collections, but it may be enough for this learner on a sparse collection. The distinction is verified in the independent controls.

## C2. Specify the selector's information

**Location:** PROOF.md, Proposition 2.

**Classification:** Filtration precision.

**Suggested replacement for “Every measurable selector”:** “Every selector measurable with respect to training, independent validation, and independent auxiliary randomization, with the future test pair independent of that information, which returns one of the unchanged candidate predictors.”

**Why:** This makes the final conditional-risk interpretation exact and excludes illicit access to the future test label or subsequent refitting. The pathwise numerical inequality is already correct.

## C3. Clarify what is bounded

**Location:** README and PROOF.md, Approach 3.

**Classification:** Terminology precision.

**Suggested wording:** “A symmetric learner whose realized candidate losses are bounded by 4.”

**Why:** Squared loss is globally unbounded on real inputs; the displayed model and predictions give an almost-sure bound sufficient for all stated concentration arguments. If a globally bounded loss is desired, replace squared loss by min{(y-a)^2,4}; every calculation for this construction is unchanged.

## C4. Clarify the ridgeless reference's conditioning convention

**Location:** SOURCES.md, item 3.

**Classification:** Source-attribution precision.

**Suggested addition:** “Hastie et al. condition on the design and integrate training-response noise, whereas this packet conditions on the full training data. The packet's Gaussian concentration argument supplies the additional step, as well as restoring irreducible test noise.”

**Why:** The difference is more than adding the noise variance. The packet's proof successfully bridges it.

## C5. Preserve historical review metadata

**Location:** Frozen RESULT.json.

**Classification:** Workflow/provenance instruction.

The original `independent_review: not yet performed` correctly describes the freeze. Do not silently alter it. Record this audit separately, bound to the original SHA256SUMS digest. The audited disposition remains unsolved and the five-attempt budget remains exhausted.
