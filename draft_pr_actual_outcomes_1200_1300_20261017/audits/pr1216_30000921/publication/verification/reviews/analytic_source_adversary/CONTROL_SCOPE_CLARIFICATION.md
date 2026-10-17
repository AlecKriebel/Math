# Control-scope clarification

This addendum clarifies the frozen original review. It does not amend its proof, report, verdict, receipts, log, or evidence manifest. The original verdict remains confined to the fixed-polynomial claim and its explicitly stated monomial and constant-multiplier extensions. It provides no review of a separately developed stronger theorem and makes no novelty or priority claim.

## What the five controls do

`exact_checks.py` function `controls()` evaluates **five deliberately false diagnostic predicates on fixed exact algebra fixtures**. These are fault-model controls. It does **not** create and execute five separately mutated implementations of the coefficient-replacement or polynomial-recursion algorithms.

| Label in the frozen receipt | Actual diagnostic predicate |
|---|---|
| `omit_z_replacement` | The squared norm of zero is at least one. |
| `drop_z_factor_n` | The ordinary-convolution value for the second derivative of a fixed z-product equals the fixture coefficient with the factor two omitted. |
| `drop_fixed_polynomial_cross_term` | A fixed quadratic-product derivative equals the expression retaining only the linear-polynomial contribution. |
| `reverse_factorial_tail_inequality` | The later factorial ratio 1/2 is at least the earlier ratio 1. |
| `use_open_disk_at_zero_ignoring_n0` | The squared norm of the zeroth orbit evaluation zero is at least 1/16. |

The routine raises an error if any of these false predicates unexpectedly evaluates true and reports `REJECTED` otherwise. The first and fifth controls are elementary fixed-value predicates; the second and third compare an independent convolution result against a deliberately wrong fixed-fixture expression. They do not measure end-to-end mutation coverage of the constructive algorithms. A separate m=0 diagnostic records that the factorial ratio does not decay; it is not one of the five rejected predicates.

Accordingly, the frozen VERDICT.json field `invalid_variants_rejected_each_mode: 5`, the receipt key `mutation_controls`, and the original report's invalid-variant wording must be read in this limited sense. They mean five false fixed-fixture predicates were rejected, not five altered algorithm implementations were executed. The substantive positive diagnostics still execute the coefficient constructions and independently compare finite coefficient identities; the infinite analytic claims continue to rest on the written proof review.

The parent separately reports that `root_diagnostics.py` executes three actual algorithm variants. This family has not read or replayed that separate work, and it is not part of the original family's five-control evidence. Likewise, the parent's later stronger-theorem review and older Gaussian implication are separate developments, not claims independently established by this addendum.

## Fresh replay and preservation

A fresh replay ran the currently sealed `exact_checks.py` in normal, -O, and -OO modes, capturing output in memory. All exited successfully with empty stderr. Their outputs are byte-identical to one another and to all three existing sealed receipts: 1,671 bytes, SHA256 `6784d07d8a101b67172134cd11725f2f082af733635a70f32e188b463b0e9e35`. The program SHA256 remains `f1b9faee5fa6dbd27fa0abe7b5c9d5a6a5d1373c9f28718b372dbcb6d3a5cbd1`.

All thirteen members bound by the original EVIDENCE.json matched their sealed byte counts and hashes before and after replay. EVIDENCE.json itself stayed at SHA256 `0d87f851d7afe235de6985386c18573e3b73ba784e0869fe20c226c69230336a`. Existing receipts were not overwritten. The two clarification files are new addenda and are deliberately outside that frozen manifest. No new source retrieval, Git operation, external contact, or app mutation occurred.

The machine-readable details and replay timestamp are in CONTROL_SCOPE_CLARIFICATION.json. This is a completed clarification checkpoint, 100% of this follow-up scope; no original review bytes were changed.
