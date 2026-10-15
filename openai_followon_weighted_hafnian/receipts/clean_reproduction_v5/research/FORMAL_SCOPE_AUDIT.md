# Family 113 Lean scope audit

Audit timestamp: 2026-10-07T05:12:34.625381+00:00. Upstream pin: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Every copied source byte was checked by SHA256 against `git cat-file` at the exact pinned commit, with zero mismatches. The upstream clone was read only. All copied sources, checks and outputs are under this project's `sources/lean_validation/`. This audit is source inspection and a reproducible failed dependency probe; **it is not a successful Lean kernel build or completed comparator verification**.

## Strongest verified finding and exact remaining gap

The actual solution declaration is `OAI.MatchingFPRAS.thm_main` in `lean/OAI/Combinatorics/MatchingCount/Main.lean`, not the `sorry` declaration in `ComparatorChallenges/MatchingFPRAS.lean`. Its final type is `MainStatement`; its proof assembles `LiteralPhysical.mainTime_bound`, `LiteralPhysical.mainProgram_outputs`, and `LiteralPhysical.mainProgram_success`. The real definitions in `MatchingCount/Model.lean` agree with the comparator definitions modulo whitespace. The theorem has no additional hypothesis parameter beyond the assumptions quantified within `MainStatement`.

The recursively discovered local import closure contains **415 modules, 3,091,883 bytes, all within `OAI.Combinatorics.MatchingCount`**, plus the external import `Mathlib`. A lexical scan of every module in this closure found no `sorry`, `admit`, `axiom`, `unsafe`, `native_decide`, `ofReduceBool`, `implemented_by`, `partial`, `opaque`, `run_tac`, or `run_cmd`. No local dependency imports `ComparatorChallenges`. These are useful reproducible static checks; they do not determine the compiled declaration's axiom closure and cannot exclude elaboration errors, nor certify the mathematical correctness of an unbuilt proof.

**Remaining verification gap:** compile this actual closure with the pinned Mathlib and toolchain, run `#print axioms OAI.MatchingFPRAS.thm_main`, and run the configured comparator. The local Lean 4.34.1 probe failed immediately at missing `Mathlib`. No upstream `.lake` directory exists, and `comparator`, `landrun`, and `lean4export` are unavailable. Only about 1.01 GB was free at the probe; the installed Lean 4.34.1 toolchain alone occupies about 2.7 GB. A brief search found seven existing Mathlib caches elsewhere in the workspace, but all use Lean 4.19.0 and Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b`, so they cannot supply the required pinned Lean 4.34.1 build. Their read-only metadata is recorded in `available_cache_audit.json`. We did not install a large dependency/cache tree or claim an unsuccessful check passed.

This limitation is **not evidence that the theorem is false**. The handwritten manuscript must be independently audited on its mathematical merits. The follow-on package must not describe this session as independently reproducing upstream formal verification, and must not claim its weighted theorem or gadget is formalized.

## Exact semantics of the actual theorem

`Model.lean` represents a graph by `n : Nat` and a finite set of pairs in `Fin n × Fin n`, with each edge's first endpoint strictly less than its second. Thus loops and repeated edges are excluded, and every finite simple undirected graph can be encoded. `Perfect G M` means `M` is a subset of the edge set and every vertex has exactly one incident selected edge. `Z G` is the cardinality of the finite set of these perfect matchings.

The input is an explicitly listed sparse graph followed by reduced rational parameters. Natural numbers use binary digits with a delimiter; signed integers have a sign symbol; rationals encode a numerator and positive denominator. The alphabet is `Fin 8`. The machine has a single finite transition table, and one nonhalting tick makes exactly one tape move, one symbol write, or detects halting. It reads a fresh fair Boolean input each tick, and a halted state is absorbing.

`MainStatement` asserts the existence of one machine `A` and natural constants `C,d`, with `C > 0`, such that for **every graph** and **rational** `0 < epsilon < 1`, `0 < delta < 1/2`, every Boolean tape of length

```
C * (length(encodeInput G epsilon delta)
     + ceil_N(epsilon^(-1)) + clog_2(ceil_N(delta^(-1))) + 1)^d
```

halts and writes a nonnegative rational. If `Z G = 0`, every tape writes encoded zero. At least a fraction `1-delta` of all these fair tapes writes `q` in `[(1-epsilon) Z G, (1+epsilon) Z G]`. This is a worst-case bit-operation bound, including unsuccessful tapes; no real-arithmetic oracle or expected-time convention appears in the final statement.

The final theorem's `delta < 1/2` range can be extended to the user's `delta < 1` by calling it with `min(delta,1/4)`, preserving the polynomial logarithmic dependence. Rational finite-input accuracy parameters are the formalized interface; treatment of unspecified exact real parameters should be expressed through finite rational requested bounds.

The graph quantifier includes the empty graph. `Algorithm/AlgorithmLaw.lean` invokes `count_empty_graph` and explicitly returns one for `n=0`. Odd order or `2 * edgeCount < n` returns zero. Other disconnected or infeasible graphs are covered by the quantifier and zero-output conclusion; there is no connectedness or existence hypothesis on `MainStatement`.

**Zero nuance:** `Z G = 0 -> output = 0 on every tape` is one direction. `MainStatement` does not state `output = 0 -> Z G = 0` on every tape for positive inputs. An exact zero/nonzero decision for the follow-on target must be supplied independently, for example by a polynomial deterministic perfect-matching existence algorithm on the positive support graph. Treating a lone zero randomized estimate as an exact infeasibility certificate would exceed the formal statement.

## Configuration and assumptions

`ComparatorChallenges/MatchingFPRAS.json` names the challenge module `ComparatorChallenges.MatchingFPRAS`, solution module `OAI.Combinatorics.MatchingCount.Main`, and theorem `OAI.MatchingFPRAS.thm_main`. Its permitted axioms are exactly `propext`, `Quot.sound`, and `Classical.choice`; `enable_nanoda` is false. This is a verification configuration, not a verification receipt. Until the actual declaration builds and its axiom list is checked, the present audit cannot assert that these are its only axioms.

`lean/docs/113.md` states precisely the finite-simple-graph FPRAS scope and the finite-alphabet worst-case bit-time claim. `lean/README.md` recommends compiling small portions and directs users to the Comparator README. That README requires installing comparator, landrun and lean4export, then `lake update`, `lake exe cache get`, and the chosen comparator JSON. The source toolchain is `leanprover/lean4:v4.34.1`; the Mathlib pin in both Lake config and manifest is `d13f23b723b8a846827a245b89c10fc7d3f11612`.

The source `formalization.yaml` contains the family's entropy and deterministic counting entries but **no MatchingFPRAS/MatchingCount.Main entry**. This metadata omission should be stated rather than silently using it as a verification certificate. The actual proof, explicit comparator JSON, and scope document do exist independently of that omission.

## Sampling scope

The top-level theorem returns a count estimate; it does **not** provide a sampler of the original graph's perfect matchings. Filenames containing `Sampling` are insufficient to infer that conclusion.

The local proof contains meaningful intermediate sampling results. `Sampling/LadderL.lean` proves `Transport.ideal_ladder_sampling`: TV mixing of an ideal ladder chain on a **bag graph** whose bags obey an acyclic color graph, positive controlled activities, local height-ratio constraints, global activity bounds, and an explicitly supplied initial perfect matching. Its ladder size is `(10^4 * N * D)^100`; this is polynomial in numerical `D`, not a standalone theorem of polynomial dependence on arbitrary binary compressed weights.

`Algorithm/FiniteStage.lean` proves `RationalSource.finiteSourceLaw_tv`, with TV bound `2*eta + 1/r`, where the source parameter named `m` in that theorem is a numerical sampling-budget parameter (denoted `r` here to distinguish it from half the input matrix order). The target is `sourceLaw` on `SourceMarked` of a transformed positively weighted graph. It assumes positive rational activities `w` everywhere, a bottleneck bound by `4^K`, `D >= 1`, at least two transformed vertices, `r > 1`, a supplied `BagPM`, and `eta > 0`. `Algorithm/OutputLengthBound.lean` defines `fixedSampler`, pads its fair-bit budget by `totalBitsPolynomial`, and proves `fixedSampler_law`; `Algorithm/Guard.lean` proves support positivity. The finite chain perturbation theorem `Variation.runSample_walk_tv` separately bounds cumulative one-step TV errors by `n*d`.

These are ingredients of the actual counting algorithm, not the user's claimed uniform weighted perfect-matching sampler on arbitrary nonnegative rational input. The follow-on note should derive its own fully specified counting self-reduction and cumulative-error guarantee or identify a suitable complete upstream sampler theorem. This audit recommends self-reduction so that no unproved pushforward or arbitrary-weight runtime interpretation is imported from these internal theorems.

## Reproduction and hashes

The original author-working-tree command was `python3 sources/lean_validation/audit_sources.py`; the third-party copied closure under that directory is excluded from the public archive. The archive now includes the small authored inspector at `research/lean_source_inspection/audit_sources.py` and the original receipt at `research/lean_source_inspection/STATIC_AUDIT_RECEIPT.json`. To reproduce source inspection after obtaining the exact pinned upstream Git repository, run `python3 research/lean_source_inspection/audit_sources.py --source /path/to/math/lean` in a fresh extracted copy, optionally adding `--lean /path/to/the/pinned/lean`. It reads the upstream clone, copies the selected closure into its own directory, checks every byte against the pin and writes a new `static_audit.json`. The helper was adjusted only to record an unavailable Lean version without a missing-key error; that adjustment supplies no new formal-verification result. It is not one of the three standard-library finite mathematical checks run by `reproduce.py`.

The saved receipt records every copied file's SHA256, the full module list, software version, exact failed probe command/output and metadata findings. The inspector's direct Lean probe is a dependency-availability check, not a complete kernel build: its isolated copied tree has no built dependency closure. A generated `pinned_lean/` tree is for local inspection only and is not by itself a complete Lake project or successful build artifact. Follow the complete-build instructions below to attempt actual kernel/comparator verification.

Key SHA256 values:

| Source | SHA256 |
| --- | --- |
| Actual Main | `5baa10d9bacd0be4ea26ae041a8600c9de9391abe8c0836c0ded10143054b100` |
| Actual Model | `357b41c991087fcdba5ef7f7170cdc0705d986d3bedd3ca0b4ce115df8611b90` |
| Scope document | `988234abb376528ffa180cd07778d5349ed15190b9d21c961117dd9d011c7e00` |
| Comparator configuration | `7f610f6ce6c7a87d1c1f190bdd5676b7f23bec79381c6acf787625a7ebe91fa9` |
| Lake manifest | `cf6105a25d9dca2f166b241d9191bd12c7e13305890dc9c4d0952351cccc0794` |

`pinned_lean/AxiomAudit.lean` is prepared to import only the real solution and print its theorem and axiom closure after a successful build. Do not import the comparator challenge to run the axiom check.

To reproduce the complete upstream prescribed check in a sufficiently provisioned **project-local full pinned source copy**, install the prescribed tools, preserve the exact dependency pins, and run `lake update`, `lake exe cache get`, `lake build OAI.Combinatorics.MatchingCount.Main`, then `lake env lean AxiomAudit.lean` and `lake env comparator ComparatorChallenges/MatchingFPRAS.json`. No such complete run succeeded in the present session. A full copy must include `patches/`, because the upstream Lake configuration applies pinned compatibility patches to several dependencies; the minimal inspection snapshot is not a complete Lake project ready for that command.

## Status

Source/theorem-scope audit: complete. Static local-closure and semantic comparison checks: reproduced. Kernel build, compiled axiom closure, and comparator check: unverified due to missing dependencies/tools and available storage. Exact detection and original-law approximate sampling must be established by the follow-on proof, rather than inferred from the formal FPRAS statement.
