# Problem 30005453: subcritical reinforcement on infinite graphs

## Result submitted for review

A complete **candidate proof** is supplied for strictly positive equilibrium
uniqueness and almost-sure coordinatewise convergence for the standard WARM
with 0 <= alpha < 1, a countable simple bounded-degree graph, bounded above
strictly positive vertex rates, and unit initial edge counts. No uniform
positive lower bound on the firing rates is imposed. The positive-integer
initial-count extension is explained in the proof.

The argument uses an exact reciprocal-power transform, vertex variables,
coordinatewise trajectory compactness, and a space-time maximum principle.
It does not extrapolate finite-volume concavity to infinite-graph uniqueness,
and it does not assume spatially uniform stochastic convergence.

The source's word “unique” needs a positive-equilibrium qualifier. On the
infinite path, alternating 2/0 arrays are boundary fixed points even below
criticality. This package distinguishes the false literal nonnegative-uniqueness
statement from an explicitly corrected positive-equilibrium convergence question.
Calling the latter the source's intended question is an interpretation; the report
does not explicitly state that restriction.

Status: author-level candidate; independent adversarial review is pending.
No novelty, editorial, or priority claim is made. The public-source search did
not locate a previous complete resolution, but is not exhaustive.

## Files and reproduction

- PROOF.md: complete candidate theorem and proof, including infinite-volume,
  martingale, and complete-trajectory steps
- SOURCE_REVIEW.md: source scope, hypotheses, known results, and search limits
- SOURCE_METADATA.json: public bibliographic and source-verification metadata
- PRIOR_ATTEMPT_CHECK.json: bounded repository checks for actual earlier work
- RESEARCH_LOG.md: mathematical approach outcomes and remaining validation step
- code/verify_algebra.py: exact finite rational diagnostics
- results/algebra_checks.json: deterministic diagnostic output
- code/verify_manifest.py and MANIFEST.json: file-integrity verification

From this directory run:

    python3 code/verify_algebra.py
    python3 code/verify_manifest.py

The diagnostics use only the Python standard library. They verify finite
algebraic identities and boundary examples; they do not computationally certify
the infinite stochastic theorem. The analytic proof is the substantive claim.

This bundle contains only authored work and verification metadata. It does
not contain scholarly PDFs, source extracts, images, raw datasets, or private
coordination material.
