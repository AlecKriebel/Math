# Scaling profiles in addition–coagulation models

Problem **30000849 / OWR-1729-002**. Current disposition: **unsolved after five substantive author turns**, with independently reviewed scoped results.

## Start here

- [Final result and remaining gaps](RESULT.md)
- [Proof map and exact hypotheses](PROOF_COLLECTION.md)
- [Full independent review](final_review/REVIEW.md)
- [Machine-readable review verdict](final_review/VERDICT.json)
- [Publication integrity manifest](PUBLICATION_MANIFEST.json)

The original `README.md`, numbered turn files, author manifests, and first-turn review are preserved historical artifacts. This file is the current publication entry point. Review and packaging add no author research turn.

## What is established

The displayed normalization in the 2007 OWR conjecture has a counterexample at `p=1/4`, constant input, and zero initial data. Its actual infinite-system construction works for both the printed coefficient convention and the standard mass-conserving addition equations. A time-integrated fixed-ray argument excludes the displayed positive interior profile without assuming uniform convergence in the similarity variable.

For the standard physical model, with birth coefficient `(j-1)^p`, the packet establishes:

1. An exact exponential-sum transport representation and a conditional off-front scaling theorem for prescribed monomer-clock forcing, for every `p<1` and real forcing exponent
2. Nonlinear asymptotics for `alpha>0`, `omega>-1/2`, `0<p<1`, and `d=(omega+1)(1-p)<1/2`: the higher-cluster count tends to a finite positive limit, the size scale is asymptotic to `(alpha/[(omega+1)N_infinity])t^(omega+1)`, and leading mass converges weakly to a front atom
3. The critical constant-input case `p=1/2`, with logarithmic corrections: `N(t)~sqrt(2 alpha log t)` and `sigma(t)~sqrt(alpha/2)t/sqrt(log t)`, together with the stated off-front profile and weak count/mass front limits
4. Extensions of the proved physical regimes to nonnegative finite-support initial data and a precise obstruction to a single initial-data-independent strict-regime size coefficient

The proofs use explicit finite truncation estimates, nonexplosive pure-birth cohorts, comparison arguments, and moment limits. The finite checks supplement those analytic arguments.

## What remains unresolved

The general intended physical scaling question remains open within this work: the `d>1/2` region outside credited known cases, the remainder of `d=1/2`, and the full infinite polynomial-tail initial-data class are not settled. The prescribed-forcing transport theorem cannot substitute for the missing nonlinear monomer asymptotic. A pointwise front-layer description is not proved and is not required by the original off-front statement.

The singular bulk profiles are not integrated through the front to claim a leading mass density. The strict-regime scale depends on the limiting cluster count. No uniqueness theorem, explicit universal value of that count, historical novelty, or human peer-review certification is claimed.

## Verification and provenance

The immutable author checkpoint is `93c6f7ee463145541d359d9076546e727ac80039`. All 53 author files remain byte-identical. The aggregate freeze, four historical author freezes, and first-review manifest were checked. All four primary-source PDFs match their recorded hashes; the full PDFs and reading images are excluded from this publication package.

The final independent review passed without a mandatory correction. All five author scripts replay byte-for-byte, totaling 45,682 exact controls. The preserved first-turn review adds 16,585 replayed controls, and the final reviewer adds 32,588 independent exact rational/symbolic controls. These counts are not evidence of a general solution or substitutes for analytic proof review.

For sources, credit, and exact scope see [SOURCES.md](SOURCES.md) and [the final source audit](final_review/SOURCE_AUDIT.md). The literal normalization correction and the unresolved broader physical question have separate dispositions throughout the final result and review.
