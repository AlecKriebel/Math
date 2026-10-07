# Family-129 formal-source and reproduction audit

Checkpoint: 2026-10-06T21:18:06.614635-07:00. Mathematical-validation contribution estimate: 45%; local audit/reporting package: 100%. These percentages are planning estimates, not evidence; the uniform binary follow-on is not formalized here.

## Outcome

**The pinned family-129 Lean build was not reproduced.** Lean 4.34.1 is installed. A byte-identical minimal source closure has been preserved and scanned, and the real theorem signatures agree with the Comparator statement templates. Dependency acquisition hit disk exhaustion before cache retrieval or proof compilation. No `#print axioms` result or Comparator verdict is claimed. This limitation must be disclosed if the paper cites upstream formalizations.

## Exact scope and pins

- Read-only upstream clone `/Users/alec/Desktop/math`, commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
- Toolchain `leanprover/lean4:v4.34.1`; installed compiler reports commit `5045d0056413266e57c625dcd7c365b10e377c52`, arm64 Apple Darwin.
- Mathlib pin `d13f23b723b8a846827a245b89c10fc7d3f11612`; shallow checkout succeeded and its toolchain agrees.
- Entry points: `OAI.Combinatorics.Automata.Main`, `OAI.Combinatorics.TwoWayAutomata.Main`, `OAI.Combinatorics.TwoWayAutomata.ExplicitFamily`.
- Recursive local imports total **41 modules and 8,477 lines**. Each preserved byte sequence matches the pinned upstream Git blob; see `sources/lean_check/source_manifest.json` and `receipts/pinned_source_verification.json`.
- The two local base Model modules import the aggregate `Mathlib`. The upstream full Lake configuration also declares many unrelated dependencies. The local adapted `lakefile.lean` retains package options (`autoImplicit=false`, fixed toolchain), the exact Mathlib pin, and only the three actual entry points plus Comparator statement roots. The resolved root manifest retains the nine packages needed by Mathlib at the original exact pins. Original full Lake configuration is preserved as `original_lakefile.lean.txt`.

## Real declarations and assumptions

`OAI.OneWayLiveness.main_theorem` is a proved theorem in `Automata/Main.lean`, importing `Recognition` and `PathNFA`. For every integer `h≥2` it produces a one-way nondeterministic `NMachine` over `BRel (Fin h)` with `h+3` states, no left moves, recognizing `OWL h` under both finite-run conventions. Every equivalent `s`-state deterministic machine satisfies

`2^((h−2)/31) ≤ 4 (s + (if positive then 2 else 1))²`.

`OAI.TwoWayComplementation.complementation_lower_bound` is a proved theorem in `TwoWayAutomata/Main.lean`. For every `n≥4` it produces an `n`-state `TwoNFA` over `SetRel (Fin(n−2)) (Fin(n−2))`; every `s`-state `TwoNFA` recognizing its word-language complement satisfies

`2^((n−4)/127) ≤ 2(s+1)`.

`complementation_lower_bound_finite` converts this to `½ 2^((n−4)/127)−1 ≤ card Q`. `explicit_complementation_family` identifies the source language as the nonempty relation-product language; `explicit_family_main` additionally gives same-source determinization bounds. The recognition lower bounds depend on actual local rank/diagram transport and amplification proofs, not on the Comparator templates. Separate handwritten audits by the upstream-determinization and upstream-complementation agents address those central mechanisms; this report does not replace them.

## Semantic agreement checked at source level

- `OWL h` means existence of a pair in the ordered product of a word's relations. `BRel` identity is equality, so the empty input has the identity relation. `sourceLanguage` is nonempty `foldr SetRel.comp SetRel.id`; the multiplication direction and identity conventions agree after translating relation representations.
- `DMachine` starts on the distinct left marker with a partial `Option` transition; its structure forbids outward moves on either marker. It supports left, right and stay moves. `NMachine` has transition sets and the analogous marker restrictions.
- `FiniteRun false` is reflexive transitive closure, allowing length zero. `FiniteRun true` is transitive closure, requiring at least one step. Acceptance is occurrence of an accepting state on a finite run, at any head position. No acceptance follows from an infinite nonaccepting run.
- `TwoNFA` uses marker codes 0 and 1 and move codes 0, 1, 2 for left, stay, right. It starts on the left marker and uses reflexive finite-run acceptance. Head positions are `Fin(word.length+2)`; transition entries proposing an outward move cannot realize a legal step. No totality or global halting assumption is imposed.
- Complements are relative to all lists over the source alphabet, not to a restricted nonempty-word universe. The empty product is identity; for the family range `h≥2` the empty word belongs to liveness.
- The three advertised Comparator theorem signatures match the real signatures **exactly modulo whitespace/comments**, recorded in `receipts/comparator_signature_check.json`. The defining Model structures and operational definitions were inspected for semantic correspondence.

## Comparator versus proof code

The files in `ComparatorChallenges/` reproduce definitions and end with intentional `sorry` theorem placeholders. The real `OAI/` files have substantive proof bodies. Each relevant Comparator JSON permits only `propext`, `Classical.choice`, `Quot.sound`; `definition_names` is empty and `enable_nanoda` is false. This is intended policy, **not a reproduced axiom check**. Comparator, landrun and lean4export are absent from PATH and no Comparator invocation completed.

## Source trust scan

A lexical scanner removing nested block comments, line comments and double-quoted strings found **no** `sorry`, `admit`, `axiom` or `constant` candidates in the complete 41-module OAI import closure. This improves on a raw keyword scan (which only hits “admits” in a comment) but is not an elaborated dependency check.

The same scan of **8,529 Mathlib source modules** found eight `sorry` candidate tokens across five files, with no `axiom`, `constant` or `admit` declaration candidates. All eight were classified by inspecting the pinned source:

- `Tactic/TFAE.lean`: three `q(sorry : ...)` terms supplied only to editor hover metadata (`Term.addTermInfo'`).
- `Tactic/ITauto.lean`: inductive constructor `Proof.sorry`; reconstruction handles it by throwing a failure, not by assigning an admitted theorem.
- `MeasureTheory/Function/ConditionalLExpectation.lean` and `ConditionalExpectation/Basic.lean`: `#check` display tests with a `sorry` argument, not theorem declarations.
- `Tactic/Widget/Calc.lean`: syntax quotations/evaluation for an editor command that creates an unfinished calculation. The 41 family-129 OAI files do not invoke this command. The source is not globally “sorry-free”; the relevant claim is that no OAI proof placeholder was found.

Pinned candidate files and their source excerpts are preserved in `receipts/mathlib_scan_candidates/`. These are secondary source checks; they do not determine the actual axiom set of a compiled theorem, and do not scan every imported tactic dependency's compiled implementation.

## Failure evidence and recovery

The first shallow Mathlib fetch succeeded. An attempted `lake update` tried fetching all Mathlib tags; it was stopped to avoid unnecessary history acquisition. A manually preserved pinned manifest then guided shallow dependency fetches. `plausible` and `LeanSearchClient` succeeded; other fetches failed with `No space left on device` or invalid `index-pack` output. The exact command outputs are in `receipts/dependency_fetch.json`.

The volume showed 102 MiB free at the failure checkpoint, with our own `.lake` occupying 277 MiB, including an aborted 127 MiB temporary pack. Only that owned cache was deleted, after recording pins/source-scan evidence; the proof source copy and receipts remain. The volume subsequently reported 1.3 GiB available. No unrelated cache, upstream file, root index, branch or commit was altered by this subagent.

## Reproduction handoff

`bootstrap_and_build.py` verifies the copied OAI hashes, shallow-fetches the exact resolved dependency pins into the project-local cache, obtains the linked Mathlib cache, builds only the three entry points, and runs `AuditAxioms.lean`. It has **not** completed; its presence is an instruction artifact, not a successful reproduction receipt. It directs generated artifacts and Mathlib's download cache to the project-local `.lake` directory and never invokes the upstream clone.

From this directory with sufficient free storage and the pinned Lean toolchain available:

```sh
python3 bootstrap_and_build.py
```

The final axiom-print script targets 13 key declarations, including all three advertised main theorems, both pivotal lower bounds, `rankLoss_all`, `sourceLanguage_state_bound`, and `order_reversing_image_bound`. A future successful run must retain actual output and verify only the three conventional axioms are present, with no `sorryAx`; the present audit cannot claim that result.
