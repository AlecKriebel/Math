# Axiom audit — requests generated, output not yet available

**Actual Lean axiom reports for this version: none. No Lean command was run.**
`CyclicBell/AxiomAudit.lean` contains 443 generated `#print axioms` requests,
not 443 dependency reports. It is imported by the standard `CyclicBell` target.
The inventory includes every named source theorem, definition, abbreviation,
and structure; proof-bearing PVM and state constructors are therefore included.

The principal requests include:

```lean
#print axioms CyclicBell.first_universal_upper
#print axioms CyclicBell.second_universal_upper
#print axioms CyclicBell.first_physical_sos
#print axioms CyclicBell.second_physical_sos
#print axioms CyclicBell.D4.first_counterexample
#print axioms CyclicBell.D4.second_counterexample
#print axioms CyclicBell.D4.main_d4_counterexamples
#print axioms CyclicBell.D4.trivialEve_purification
```

After a successful pinned clean build, the runner executes the query file and
parses every report. The only permitted axioms are some subset of:

```text
propext
Classical.choice
Quot.sound
```

These are the permitted foundations, NOT observed output. A missing or duplicate
report, `sorryAx`, a custom mathematical axiom, or a compiler-trust reduction
axiom stops the audit. The source scanner also rejects proof placeholders,
`native_decide`, unsafe or external proof code, custom elaboration commands,
and unapproved compiler options. Only ordinary recursion/heartbeat budgets
are allowed in production source.

The static scanner passed. This does not prove absence of unapproved transitive
axioms; only actual Lean output can establish the requested dependency result.
The synthetic `Foo.a` strings in `scripts/test_runner.py` are parser fixtures,
not mathematical receipts. The test that rejects `Lean.ofReduceBool` is likewise
a reporting-tool negative control, not evidence about an executed theorem.

## How to obtain the reports

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

The runner cleans this project's build directory, builds the default target,
runs positive and deliberately false physical controls, executes the axiom
queries, and verifies protected source and dependency fingerprints. Successful
receipts will appear in `logs/runs/<timestamp>/run.json`; the current package
contains no such successful receipt. `formal_endpoint_certified` remains false
until independent source correspondence is reviewed, even if the kernel passes.

## Trust boundary

Normal trust remains in the pinned Lean kernel/compiler binary and runtime,
the machine/filesystem, and the producer of the pinned Mathlib cache. This
command is a clean rebuild of the companion, not a bootstrap rebuild of Lean
or every third-party dependency. Exact Python checks are outside the proof
chain. They supply no trusted facts to Lean and cannot make an axiom audit pass.

Historic failure logs are under `history/pilot/` and refer to the smaller pilot,
not to this source revision. No independent agent reviewed this continuation.
