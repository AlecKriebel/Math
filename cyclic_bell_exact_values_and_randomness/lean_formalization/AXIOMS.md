# Axiom audit — prepared, never executed

**Actual Lean axiom reports: zero.** No Lean compiler or kernel was invoked in
this continuation. `#print axioms` lines and a static declaration inventory are
not axiom reports and are not evidence of formal correctness.

The generated `CyclicBell/AxiomAudit.lean` imports the entire statement umbrella
and contains **1,538 pending queries**, one for every explicitly named source
declaration found by the scanner, including proof-bearing constructors and named
instances. Its ordered name list is `reference/expected_theorems.json`.
All 81 source/audit files are reached by the default `CyclicBell` build target.

The permitted foundational axioms are any subset of:

```text
propext
Classical.choice
Quot.sound
```

A report containing `sorryAx`, a custom axiom, native proof-evaluation trust or
any other axiom must fail. Missing, duplicate and unexpected named reports also
fail. The parser and its rejection controls were exercised with mocked output,
not a real Lean executable.

The static scanner rejects source-level admission, custom mathematical axioms,
`native_decide`, unsafe/evaluator replacements and unapproved compiler options.
The control registry also scans all separate validation sources. Static absence
of forbidden tokens is weaker than checking all elaborated transitive proof
dependencies; imported library names and tactic success have not been tested.

Run the complete offline command:

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

It checks compiler and manuscript identities, locked dependencies, a clean
project rebuild, actual positive/negative Lean controls, every axiom report and
protected source hashes. Only then can actual reports be inspected. The usual
trust in the pinned Lean binary/runtime, filesystem, hardware and upstream
compiled dependency cache remains. This is not a from-source compiler bootstrap.

After a real pass, an independent statement-correspondence review is still
required. Until then, all endpoints—including the new model-value, adversarial
guessing/finite-POVM-maximum and appendix candidates—remain uncertified.

The current five positive and twenty negative controls remain unexecuted in Lean.
The runner rejects resource-exhaustion and abnormal-process diagnostics even
when a recognized proof-error message is also present. Its tests use mocks.
