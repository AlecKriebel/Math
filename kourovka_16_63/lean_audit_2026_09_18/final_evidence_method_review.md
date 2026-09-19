# Adversarial review of final evidence and publication claims

Timestamp: 2026-09-19T04:18:02.101634+00:00.

## Scope and present conclusion

Independent review of the proposed final evidence workflow, source README, draft webpage, and packaging logic. No heavy Lean compilation or full-package queries were run for this review. This bounded method review is complete (**100%**); it does not change the mathematical completion status.

The README and webpage accurately label the supplement **partial**, explicitly state that the final group theorem is absent, and enumerate the substantive missing bridges. They do not claim that compiling helpers supplies the full theorem. The published paper's computational/AI review is distinguished from complete proof-assistant verification and human peer review.

## Required evidence distinctions

1. Each accepted module was compiled separately with bounded resource use. A final root import and actual declaration queries must **not** be described as a successful unified `check.py --milestones` invocation unless that invocation actually ran.
2. Importing `.olean` objects does not re-elaborate their current source bodies. Final root/query success alone cannot show that the supplied source is the source from which every imported object was built. Keep the per-module acceptance records and freeze the source/object pairing.
3. Source/object hashes bind the shipped bytes for later comparison; they are not proof of mathematical correctness. Timestamp freshness is a conservative detection heuristic and does not provide cryptographic proof of source-to-object correspondence. A changed dependency object can invalidate a dependent object even when that dependent's own source was not edited.
4. `#print axioms` reports transitive assumptions of the queried constants. The source inventory covers ordinary public named roots, not all private, anonymous, generated, or macro-produced environment declarations. Do not describe that inventory as an exhaustive elaborated-environment inventory. Source review, actual module acceptance, and transitive roots provide complementary evidence.
5. `#check` with full pretty-printing exposes declaration types, but does not mechanically establish agreement with the paper or expose every assumption hidden in a supplied structure's fields. The independent statement/hypothesis review remains necessary.
6. This workflow uses the pinned upstream cached objects and Lean's own trusted kernel/compiler installation. It is not a dependency-stack rebuild, verified compiler bootstrap, or independent implementation of the kernel. Optional same-kernel replay should be reported only if actually completed.
7. The external JSON/witness checks are distinct from Lean proof acceptance. Their successful reruns help match source literals to the fixed mathematical data but cannot discharge the absent BCH/automorphism/Smith developments.

## Added final-object audit helper

`audit_accepted_objects.py` builds a manifest of every module in the full `Kourovka` import closure, source/object hashes and timestamps, protected input hashes, and explicit freshness problems. It rejects missing objects, newer own or transitive local sources, and direct imported objects newer than their importer. No freshness exceptions or silent bypass are implemented.

After source freeze and `check.py --prepare-audit`, run:

```sh
python3 ../lean_audit_2026_09_18/audit_accepted_objects.py
python3 ../lean_audit_2026_09_18/audit_accepted_objects.py --query
```

The second command checks pinned dependency cleanliness, imports the existing root object, queries the actual axioms and types of all statically inventoried named roots, and verifies that the final source/object/protected-input snapshot did not change during those queries. It never rebuilds a project module and always records `unified_milestones_run: false` and `complete_formalization: false`. Prior per-module acceptance and the limits of timestamp evidence are stated in every result.

The helper's negative controls passed for valid snapshots, missing objects, newer import objects, and transitive source mutation. No actual full-project query outcome is claimed by this review. See `accepted_object_controls.json`; actual final runs, if completed, appear separately under `accepted_object_audits/`.

## Static-status label repair

`audit_support.py` formerly labeled every source declaration `uncompiled` and set `lean_compiled: false`, even though these were static inventory records and some modules had compiled. Version 3 of the inventory instead records `not_determined_by_static_inventory` and `lean_compiled: null`. This repairs the misleading label while preserving the strict separation from real compiler/query evidence. Existing rejection/parser self-tests still pass. The inventory must be regenerated after the final source freeze.

## Packaging observations

The outer downloadable ZIP manifest hashes the actual included bytes and excludes compiler/dependency caches. The parent has preserved the original stale inner `SHA256SUMS` and progress record under `reference/` and will refresh the current records after freeze. This is necessary to avoid presenting historical hashes/statuses as current validation. The final verification report must explicitly identify any failed modules and exactly which module/object/query checks completed. Publication should not strengthen the current partial-formalization wording.
