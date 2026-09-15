# Settings appendix and runner audit

This is a single-assistant source inspection. No independent agent, Lean
process, kernel check, or external referee participated. Uncompiled scripts may
require substantive mathematical and API repair.

## Existing proof routes inspected

Selected scalar-sector/equality, zero-safe functional-calculus, support-saturation
and rectangular reflection-rank arguments were inspected. The reflection proof
retains the actual amplitude column space and obtains its lower bounds from
intertwining powers, not from a full-space invertibility assumption. No new
mathematical defect in those selected old arguments was established. This was
not a comprehensive review of 1,090 incoming theorem candidates and does not
establish their correctness. Old mathematical source files are unchanged.

## Reproduced incoming runner defect and repair

The incoming runner could accept an expected-failure process as a mathematical
negative-control rejection whenever it printed a recognized proof diagnostic,
even if it was killed or also reported exhausted resources. With MOCKED process
outputs (no Lean invocation), all three cases were wrongly accepted:

* exit -9 plus `error: type mismatch`;
* exit 1 plus `unsolved goals` and maximum-heartbeat exhaustion;
* exit 1 plus `tactic failed` and deterministic timeout.

`logs/phase_incoming_runner_defects.json` preserves those reproductions. The
runner now rejects signal termination, any negative-control exit other than 1,
and diagnostic evidence of resource exhaustion, timeout, stack/memory failure,
or a process kill. These checks apply to ordinary runs as well; a zero exit does
not excuse a resource diagnostic. Normal exit-1 proof failures still pass the
reporting test. The prior unknown-import/identifier and unapproved-axiom checks
remain. All tests of compiler-output handling use clearly identified mocks.

This repair prevents these particular false positive receipts. It is not a
proof that the reporting program is immune to every possible malformed output.
The independent review must still inspect actual diagnostics and statements.

## New mathematical route

The standard strategy is explicit, with negative Alice and positive Bob Fourier
signs. Probabilities start with physical trace products. A finite geometric
identity is proved before dividing, so equal-offset matching is not lost to
Lean's convention 0/0=0. The denominator argument uses exact integer folding
and sine monotonicity. It cannot silently select the wrong lift of a-b.

Upper and attaining parts of each maximum are separate. Nonuniformity follows
from an entry above the average, not from a floating-point table. The standard
strict inequality covers d>=2; the anchor strict inequality covers d>=3 and a
separate theorem gives every d=2 cross entry exactly 1/4. Existing Bob inputs
are preserved literally when the new anchor input is added.

The scalar entropy statement is tied to the attained peak. It is not an
adversarial privacy assertion. The limiting proof is a filter-limit proof
script from the derivative of sine, not an inference from sampled dimensions.

## Exact tests and a corrected test-design mistake

New exact tests in Q[x]/Phi_(8*d), using rational coefficients, cover d=2..8:
7,794 distinct assertions and 48 negative controls. They compare projectors,
Gram inner products, normalization, trace/amplitude/sine expressions, marginals,
attaining entries, all anchor cases, and division-free resonances. A separate
full joint-index trace calculation is also used in d<=4. Comparisons used for
maximum locations are rational folded-angle distances, NOT an external ordered
algebraic-number prover. No finite test establishes the asymptotic theorem.

The first Bob-sign control accidentally used a=0 in the zero-phase Alice basis,
where complex conjugation preserves the modulus. The test correctly rejected
that ineffective control. It was replaced with a=1,b=0 for d>=3, comparing
5/4 against 3/4 displacement. The initial failure and repair are preserved in
`logs/phase_control_design_repair.json`. This was a test-design issue, not a
manuscript counterexample and not something silently counted as a passing test.

These scripts share the retained exact field engine and were written by the
same assistant. They are supplementary, not independent Lean certificates.

## Pinned API/source inspection and likely repair points

Inspected the exact pinned Mathlib implementations of the sine derivative,
`HasDerivAt.tendsto_slope_zero`, basic trigonometric bounds, and
`tendsto_const_div_atTop_nhds_zero_nat`. A nonexistent Sinc-module candidate was
not used. New code does not require a different Mathlib or Lean version.

Likely elaboration-sensitive points remain: rewriting finite sums through
ZMod representatives, real/complex casts and scalar action, infimum-filter
syntax, trigonometric rational-angle normalization, and positivity inference.
An integer r<q conversion was made explicit as r+1<=q during source inspection.
These are inspected candidates, not a claim that only syntax repairs remain.

The conservative project-reference scanner and default-import tests do not
parse Lean, check external library identifier resolution, or validate proof
terms. Every endpoint and axiom query still awaits an actual clean build.
