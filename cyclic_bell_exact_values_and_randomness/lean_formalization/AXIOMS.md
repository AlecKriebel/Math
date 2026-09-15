# Executed axiom audit and reproduction

The received handoff had no compiler results. The repaired package obtains actual
Lean `#print axioms` output for every explicitly named declaration, including
proof-bearing definitions and named instances. The ordered names are generated
in `reference/expected_theorems.json`; the query module explicitly imports every
source module, including the added coverage constructions.

The only permitted foundational axioms are:

```text
propext
Classical.choice
Quot.sound
```

The runner rejects `sorryAx`, custom axioms, native proof-evaluation trust,
unexpected or missing reports, duplicate names and changed source fingerprints.
Static scans additionally reject admissions, unsafe replacements and unapproved
compiler options. These scans supplement actual elaboration and transitive axiom
reports; they cannot replace them.

Reproduce from this directory with Lean 4.19.0:

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

Omit `--bootstrap` when the exact locked dependencies and cache are installed.
The command verifies the compiler hash, manuscript SHA/blob and dependency commits,
removes the companion's build directory, builds the complete library, runs all
five acceptance and twenty rejection controls, and collects every axiom report.
Sources and dependencies must remain unchanged throughout that run.

`logs/latest_run.json` is the machine-readable outcome. Detailed retained evidence
and independent manuscript correspondence reviews are in
`repair_audit_2026-09-14/`. The automated runner deliberately does not claim
semantic correspondence from compiler success alone; its
`formal_endpoint_certified` field concerns what that automated process alone
can establish. Read the separate evaluation and `COVERAGE.md` for that review.

The negative controls must fail inside their designated proof bodies. Missing
imports, syntax errors, unknown names, crashes and resource exhaustion do not
count as successful rejection. Failed proof attempts alone do not prove the
negation of every test statement; these are strict regression controls.

The trust base includes the pinned Lean compiler/runtime, ordinary hardware and
filesystem, and exact upstream dependency artifacts. This is not a from-source
compiler bootstrap or an independent implementation of Lean's kernel.
