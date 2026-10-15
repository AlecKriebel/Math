# Separate verification repair: PR 436 / 2569

The repaired verification copy fixes the reproduced optimization defect. Every frozen original byte is preserved. This is a validation repair with zero additional proof-search attempts; it changes no mathematical claim, input, formula or expected result.

`make_explicit_check_copy.py` parsed each frozen original and replaced its 82 `assert` nodes with explicit `if not test: raise AssertionError(...)` branches. Tests are evaluated once, and failure messages only on failure, preserving ordinary assertion behavior. An exception cannot be removed by Python optimization. The generated scripts are separate files under `repaired_verification`, and AST unparse reformats them and removes comments. The source and repaired hashes, all exact original test ASTs and source line locations are in `repaired_verification/REPAIR_PROVENANCE.json`.

`check_repair_equivalence.py` independently reparses each generated script and confirms that its full AST is exactly the source AST after the declared assertion transformation. All non-assert code, imports, mathematical expressions, iteration, output fields and input/output destinations are thereby preserved in the AST. There are zero remaining source `assert` statements. This mechanical equivalence check does not purport to formalize Python semantics or prove the mathematical theorem.

The same original `reproduce.py` harness and exact five original fault definitions were reused by `repair_replay.py`. Repair fixtures copied the frozen input package, overlaid only the four separately repaired scripts, and kept all original mathematical input bytes. The original coefficient fault, proof-byte fault, rank-function faults and contributor class-size fault were not weakened. The trace-based contributor injection locates its target assignment from the repaired AST, so formatting changes do not bypass the fault.

| Replay scope | Normal Python | Python `-O` |
|---|---:|---:|
| Four unchanged-data repaired entry points | 4/4 exit zero and byte-match frozen outputs | 4/4 exit zero and byte-match frozen outputs |
| Five original meaningful faults | 5/5 reject with explicit failures | 5/5 reject with explicit failures |

All mathematical fields match the frozen output, with the stronger result that all generated JSON files and stdout are byte-identical. The actual interpreter/dependencies are Python 3.12.14, SymPy 1.14.0 and mpmath 1.3.0. Both repaired modes now execute the validation expressions; optimized-mode byte equality is no longer being treated as a substitute for real checks.

The exact portable replay commands, run from the audit-case directory in a fresh case with no existing private fixtures, are:

```sh
python3.12 -m venv private_sources/reproduction_adversary/venv
private_sources/reproduction_adversary/venv/bin/python -m pip install -r reviews/reproduction_adversary/repaired_verification/requirements.txt
private_sources/reproduction_adversary/venv/bin/python -B reviews/reproduction_adversary/make_explicit_check_copy.py
private_sources/reproduction_adversary/venv/bin/python -B reviews/reproduction_adversary/check_repair_equivalence.py
private_sources/reproduction_adversary/venv/bin/python -B reviews/reproduction_adversary/repair_replay.py
```

The generator and checker use the bound frozen source snapshot in this audit case. `repaired_verification` contains the transformed scripts and their provenance, README and pinned requirements; it does not contain a copied proof or coefficient input and is not directly executable by itself. `repair_replay.py` supplies those unchanged frozen noncode inputs by copying the source package into private fixtures before overlaying repaired scripts. For direct execution outside the audit case, follow the isolated frozen-copy/overlay instructions in its README. Raw execution records preserve the actual interpreter path and command used on this machine.

`REPAIRED_EXECUTION_RESULTS.json` records actual statuses, hashes, timestamps, byte/field comparisons and private raw-record locations. All original failures and repaired failure records are preserved. No script executed in a frozen/public source directory, and all generated output, mutable input copies, wrappers, dependency packages and raw records remain private.

The original `REPORT.md` remains the original audit verdict and documents the unrepaired frozen package. The repaired copy is a distinct artifact, and must be described as such. It does not retroactively change the historical verifiers or historical reviews. The source receipt and historical manifest continue to bind the original bytes; repaired scripts have their own provenance.

Remaining gap: the general mathematical proof is still subject to the separately assigned theory/representation audits. This validation repair removes the reproduced code defect in the separate copy. Historical-priority review has not begun, and no external communication or remote action was performed.

Completion estimate: 100% of the explicitly requested verification repair and replay.
