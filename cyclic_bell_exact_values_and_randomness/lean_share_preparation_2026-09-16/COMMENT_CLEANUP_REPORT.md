# Lean comment cleanup and preservation check

2026-09-16. Completion: 100% of the assigned comment cleanup.

Reviewed 130 Lean files: production `CyclicBell/*.lean`, the root `CyclicBell.lean`, and `validation/*.lean`, excluding generated `CyclicBell/AxiomAudit.lean`. Changed comments in 81 files. Removed obsolete uncompiled/candidate/offline-status wording and internal handoff narrative, and replaced affected headers with descriptions of their mathematical content. The source-polar headers now reference the completed constructions rather than work pending. The correlation-value header distinguishes its independent value argument from the separately established closure containment.

All edits are strictly within existing comment spans. No declarations, imports, proof terms, formal statements, string literals, or whitespace outside comments changed. No Lean/Lake commands, commits, or pushes were run. `git diff --check` passes for the owned Lean paths.

## Preservation evidence

`comment_token_preservation.json` records SHA-256 hashes before and after for all 130 files. For every file:

- The ordered list of all noncomment segments is exactly equal before and after, byte for byte. This includes string literals, all code whitespace, and the boundaries around each comment.
- The existing `strip_comments_strings` scanner gives identical content after whitespace normalization. Separate before/after hashes are recorded.
- A second, independently written contextual delimiter scanner rechecked exact noncomment segment equality and all 130 final source hashes.

The existing scanner masks every character of a comment with whitespace and preserves its newlines. Its raw outputs therefore change length when prose is shortened; literal raw-mask equality is recorded but is not the preservation criterion. The exact noncomment-segment check is stronger than token equality and detects changes to string literals that the existing masking scanner would hide. This interpretation was agreed with the integration owner before editing.

`comment_cleanup_before.json` preserves the original text of all changed files, outside the external-review folder. `clean_lean_comments.py` records the editorial transformations and preservation checks. These are editorial audit records, not Lean proof receipts.

## Mathematical scope retained

The cleaned comments retain the relevant boundaries: finite-Eve binary privacy; finite-dimensional support rigidity; no assertion on unused support complements; supplied defining polar-decomposition equations rather than a general existence construction; the alternate constant-diagonal MUB proof rather than verification of each Toeplitz/SVD intermediate step; explicit-realization rather than self-testing/no-go claims for settings tables; conditional scalar-cap hypotheses for permutation theorems; and guessing lower bounds rather than an asserted globally optimal adversary.

No new mathematical scope ambiguity was found. Existing d=4-only comments remain explicitly local to their modules and are not presented as limits on the separate all-dimensional results. Intentional validation-failure descriptions remain intact; only the stale offline wording in `AcceptGeneral.lean` changed.
