# Verification machinery: final integration review

The frozen runner/scanner tests passed: 63 tests, no failures. Actual Lean
validation is separate from these Python machinery tests. The clean build's
actual output contains all 1,852 expected axiom reports, and parsing that output
finds only `propext`, `Classical.choice`, and `Quot.sound`.

The incoming verification scripts also required repair. The final changes keep
the mathematical and diagnostic requirements strict:

1. A rejected control must exit with Lean's ordinary proof-error code and every
   error must be source-located inside that control's designated proof body.
   Unknown imports/names, malformed statements, crashes, resource exhaustion and
   unrelated error diagnostics invalidate a run. The four linarith-only failures
   and the aesop-depth failure were repaired in the controls rather than accepted
   by weakening this policy. All original 49 example statements remain.
2. The source inventory covers indentation, escaped identifiers, nested modules,
   namespace/section context, apostrophes and the root source file. Unsupported
   or anonymous declarations fail instead of silently escaping the query list.
3. Generated `AxiomAudit.lean` explicitly imports every inventoried source module.
   Thus newly added coverage theorems are actually available to the Lean queries;
   merely enumerating their names is insufficient. Root/self imports are excluded
   to prevent cycles. A focused generation test checks new submodule inclusion.
4. The import scanner recognizes all imports on a line. The trusted, exactly
   pinned `Mathlib` root is accepted alongside `Mathlib.*`; similarly named
   external packages remain rejected by a dedicated mutation test.
5. Because the axiom module now imports every source explicitly, removing one
   redundant settings import no longer removes that module from the build. The
   corresponding mutation test now removes all incoming edges and still requires
   the audit to reject omitted settings contracts. This tests actual coverage
   omission rather than an incidental import arrangement.

The general first-bound dependency checks remain in place: those upper-bound
modules cannot import concrete witness constructions. Claim-ledger names must
refer to real declarations in the stated files. Axiom parsing rejects missing,
duplicate, extra or unapproved reports. Static token checks supplement the actual
kernel dependency reports and are not presented as proof verification.

The standard runner executes the whole clean build, all controls, and then a
standalone repeat of the full axiom-query file. The latter is intentionally
retained in this verified workflow. The full axiom traversal is substantially
slower than an ordinary incremental build; this was not a reason to omit queries
or replace them with mocked/scanner output.

Evidence: `runner_tests.log`, `integration_static.json`,
`validation_actual/SUMMARY.json`, `validation_statement_preservation.json`,
`clean_build_axioms.json`, and the final frozen-run receipt when completed.
