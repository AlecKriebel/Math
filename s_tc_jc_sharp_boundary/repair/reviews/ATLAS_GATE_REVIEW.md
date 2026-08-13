# Finite-atlas release-gate review

Audit date: 2026-08-09  
Scope: primitive decorated `k=5`, `k=6`, cut, cycle/theta seven-port, and the later Gate 2 nonroot closure  
Disposition: **OUTCOME B IS CORRECT; THE POSITIVE STANDARD-CLASS THEOREM REMAINS WITHHELD**

## Executive verdict

The available artifacts contain substantial exact finite algebra, and the audited direction and sign logic is correct. In particular:

- the three large end-to-end assignment tables are internally coherent;
- every referenced `k=5` and `k=6` strict-sign polynomial was independently recomputed;
- every cut-table sign certificate, including the partial Bernstein certificates in the inheritance variable, was independently recomputed;
- the directed containment filter has the correct orientation.

Those facts do **not** close the finite-atlas theorem. The missing step is provenance and exhaustiveness: the release cannot regenerate the large decorated assignment tables from primitive networks, and the seven-port chain does not bind the `4,368` primitive equalities to the `192` residual rows and then to source-target decorated completion certificates. The old `1,686` and proposed `1,152` counts are both target-only quotients, not counts of decorated directed pairs.

The later self-contained script `audit_gate2_nonroot_full_closure.py` materially improves the finite computation, but it does not cure the release gate. It computes displayed-tree descriptor decks and exact pullbacks in memory, yet:

1. successful strict directions are not emitted as topology-indexed pair-to-polynomial records;
2. each source signature is checked through one representative descriptor deck, while targets are checked through all distinct decks;
3. its primitive support universe is loaded from frozen encodings rather than regenerated inside the implementation; and
4. its arbitrary-subdivision conclusion is promoted from finitely constructed word tests plus prose, not from an executable or independently formalized all-subdivision proof.

Its separate adversarial replay ended `UNRESOLVED` after `BrokenPipeError`. Therefore, even if the user's current primary replay eventually emits `VERIFIED`, that status alone is not an admissible proof of topology binding, primitive-universe exhaustiveness, or arbitrary-subdivision promotion.

No exact algebraic counterexample to the intended theorem was found in this audit. The correct release status is:

> **UNRESOLVED:** the finite evidence supports the conjectured classification, but the end-to-end atlas assignment theorem and arbitrary-subdivision promotion are not independently certified.

## 1. Audit boundary and independent diagnostics

Publication files were not modified. New bounded diagnostics are confined to `repair/independent/atlas/`:

| Diagnostic | Purpose | Result |
|---|---|---|
| `audit_assignment_bindings.py` | Stream and cross-check the 189 MB/265 MB `k=5` and `k=6` assignment tables against graphs, signature bytes, pair TSVs, and sign libraries | Exact internal agreement |
| `audit_cut_assignment_table.py` | Recompute cut-table endpoint/single-blob classifications and sign certificates | Exact internal agreement |
| `direction_sign_logic.py` | Derive containment orientation and recompute strict signs | Direction correct; all signs replay |
| `seven_port_census_sensitivity.py` | Delete all nonresidual rows from the inherited `4,368` census and rerun the old scripts' effective selection predicates | Mutation escapes both old checks |
| `audit_gate2_script_structure.py` | Inspect topology/pullback bindings and arbitrary-subdivision promotion in the later Gate 2 script | Both release gates unresolved |
| `inventory_dependencies.py` | Search ordinary files and ZIP members across all supplied trees | Nine required inputs absent everywhere |
| `certificate_contract.py` | Prototype a content-addressed pair-level certificate/reviewer contract and mutate it | Baseline accepted; all nine mutations rejected |

Machine-readable results are in:

- `repair/independent/atlas/k5_binding_audit.json`
- `repair/independent/atlas/k6_binding_audit.json`
- `repair/independent/atlas/cut_binding_audit.json`
- `repair/independent/atlas/direction_sign_audit.json`
- `repair/independent/atlas/seven_port_census_sensitivity.json`
- `repair/independent/atlas/gate2_script_structure_audit.json`
- `repair/independent/atlas/dependency_inventory.json`
- `repair/independent/atlas/certificate_contract_mutation_test.json`

## 2. Reconstructed dependency chain

### 2.1 Compact nonroot release path

The current reproducibility driver regenerates topology data, `k=5`/`k=6` signature arrays, and directed pair TSVs in this order:

1. `regenerate_nonroot_topology_atlases.py`;
2. `regenerate_nonroot_algebra.py --k 5` and `--k 6`;
3. `regenerate_directed_pair_universe.cpp`;
4. `review_directed_pair_universe.cpp`.

Evidence: [`verify_regenerate_all.sh`](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_sharp_boundary/reproducibility/verify_regenerate_all.sh:13) invokes the generators at lines 13–24 and the reviewer at lines 65–73.

`regenerate_nonroot_algebra.py` really does rebuild descriptor/signature decks from the structural and core enumerators ([lines 39–68](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_sharp_boundary/reproducibility/publication/src/regenerate_nonroot_algebra.py:39)). It also associates each selected-strong signature with a graph code in memory ([lines 382–404](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_sharp_boundary/reproducibility/publication/src/regenerate_nonroot_algebra.py:382)). But its durable output is only sorted signature bytes and summary counts ([lines 403–420](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_sharp_boundary/reproducibility/publication/src/regenerate_nonroot_algebra.py:403)). The graph-to-signature map and the invariant pullbacks that generated each bit are discarded.

The C++ pair generator then treats the byte arrays as the complete universe and writes only `(source_index, target_index, relation)` ([lines 47–86](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_sharp_boundary/reproducibility/publication/src/regenerate_directed_pair_universe.cpp:47)). The reviewer independently recomputes the same bytewise relation, but it does not return to graphs or displayed-tree pullbacks ([lines 20–37](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_sharp_boundary/reproducibility/publication/review/review_directed_pair_universe.cpp:20)).

Thus the compact chain certifies:

`primitive generator -> signature multiset -> bytewise relation`,

but not the stronger release theorem:

`canonical source graph + canonical target graph + direction -> exact displayed-tree pullbacks -> exact separator/equality certificate`.

### 2.2 Large repaired assignment path

The three large JSONs add many of the missing bindings after the fact:

| Universe | SHA-256 | Exact replay |
|---|---|---:|
| `directed_k5_end_to_end_assignments.json` | `946bbf80935613edb0941940cf2bc0023ae56343b3b9a4336ca9b055e8004f67` | 27,000 directions |
| `directed_k6_end_to_end_assignments.json` | `f1c68860a3f84c5ab8c7af3bc870ba3a2b8741f2cf196ac2e74fc12bc3cf3c0d` | 32,940 directions |
| `cut_end_to_end_assignments.json` | `676b0bc16d00c03f700e39413d9c30160d22bc4425a4984b2617fc2e2aa743e3` | 630 classified cut records |

However, no located source writes either directed assignment filename. The located cut writer imports missing primitive/compiler/sign-library inputs. Consequently these JSONs are strong exact **table-consistency certificates**, but not reproducible primitive-to-certificate derivations.

### 2.3 Cycle/theta seven-port path

The intended repaired path is:

`48 labelled cycle sources × primitive weak-theta presentations`

`-> 4,368 primitive equality presentations`

`-> 192 missing-three-support residual presentations`

`-> 4,608 raw minimum-support completions`

`-> 1,152 canonical completed target graphs`.

This is visible in the proposed compiler at:

- primitive equality selection and the `4,368` assertion: [`compile_cycle_theta_atlas_v2.py:137`](/Users/alec/Downloads/STC_JC_AUDITOR_PACKAGE_RETRY/02_END_TO_END_REPAIR_WORK/src/compile_cycle_theta_atlas_v2.py:137);
- completion construction and target-only canonicalization: [lines 146–170](/Users/alec/Downloads/STC_JC_AUDITOR_PACKAGE_RETRY/02_END_TO_END_REPAIR_WORK/src/compile_cycle_theta_atlas_v2.py:146);
- public records dropping `network` and `selected_map`: [lines 198–201](/Users/alec/Downloads/STC_JC_AUDITOR_PACKAGE_RETRY/02_END_TO_END_REPAIR_WORK/src/compile_cycle_theta_atlas_v2.py:198).

That compiler is not executable from the supplied package. Its imports at lines 18–24 require absent modules, and its target builder also requires absent `k4_features.npz` and `all_F_patterns.json` at lines 47–51. The recorded failure occurs even earlier, at the missing `regenerate_nonroot_algebra` import ([compiler transcript](/Users/alec/Downloads/STC_JC_AUDITOR_PACKAGE_RETRY/01_CURRENT_FAIL_CLOSED_STATUS/STC_JC_Final_Reconciliation_Outcome_B/transcripts/compiler_failure.txt:1)).

Even if its imports were repaired, its completion key is the target graph alone; it does not key by source graph, source-target port map, restored roles, direction, or explicit raw-to-canonical transport. The source tensor in the completion loop is disabled by `if False` at line 162. The claimed `1,152` is therefore not the missing decorated-pair universe.

The older active path instead begins with eight hard-coded residual patterns, verifies that the inherited census selects exactly their `8 × 24 = 192` rows, and independently generates `1,686` target-only completed mixed graphs:

- residual selection: [`verify_seven_port_closure.py:72`](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_sharp_boundary/reproducibility/exact_release/src/verify_seven_port_closure.py:72);
- `192` graph records: [lines 579–620](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_sharp_boundary/reproducibility/exact_release/src/verify_seven_port_closure.py:579);
- target-only completion census and `1,686` assertion: [lines 689–722](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_sharp_boundary/reproducibility/exact_release/src/verify_seven_port_closure.py:689);
- exact factors and dimension witnesses: [lines 724–752](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_sharp_boundary/reproducibility/exact_release/src/verify_seven_port_closure.py:724).

The reviewer independently regenerates the same `192` rows and `1,686` target completions, factors, reduced tensor types, and rank minors ([lines 375–467](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_sharp_boundary/reproducibility/exact_release/review/review_seven_port_closure.py:375)). That validates the conditional computation

`given these 192 residual target presentations -> these 1,686 target completions are separated`,

not the upstream implication

`every one of the 4,368 primitive source-target equalities either separates earlier or appears among these 192 rows`.

## 3. Source inventory: salvage versus rewrite

### 3.1 Salvageable exact components

The following located modules are useful, deterministic building blocks:

| Component | SHA-256 | Salvageable role |
|---|---|---|
| `core_enumerator.py` | `087aa93e22d779baa776537aba397fa2350d2e6bd9d27ee5ed2faa6df26730ea` | Primitive level-2 core enumeration |
| `regenerate_nonroot_topology_atlases.py` | `ae3068e0db3d04458efdb49d56a837b46ef0365890d240c46051ab1edde15e7b` | Structural theta enumeration |
| `regenerate_nonroot_algebra.py` | `6903387f15a2f0ec01bd774705afb47321bf303b16d1482fd1656583e85ca6af` | Exact reduced tensor/signature generation |
| `regenerate_cycle_algebra.py` | `2221693e7390b0daaff724eeb1a61bb7adcef6681093a440f468f7b09e3ff296` | Cycle algebra generation |
| `regenerate_directed_pair_universe.cpp` | `b8c99e8ead05facf072b3ff81bfcba01fd32fdfe40d2790f2b21e440faeda025` | Fast subset-direction enumeration |
| `review_directed_pair_universe.cpp` | `f188dcb53c9bbb431b2280b9d00416d4e6f3342e763d2ba691448c5814ad5933` | Independent bytewise pair replay |
| `verify_seven_port_closure.py` | `fe8d523a8fffde5f696c5f538de4cf4d461fba6e8a83ab099f80f1c92863dce1` | Conditional `192 -> 1,686` exact algebra |
| `review_seven_port_closure.py` | `77f180201a214b88cf6d151d640ed5b6ebd8c186e293db6cd43b64edef11a5cd` | Independent conditional replay |
| `cycle_theta_support_completion_corrected.json` | `9277c9ab0e3050a8f746c702e50b3887e6922fd150f6acb54dd22faf41da3b16` | Historical `4,368` census input, pending provenance repair |

The historical `theta_k6_weak_signatures.bin` was recovered from `STC_JC_Reproducibility.zip`. It is 183,897,000 bytes with SHA-256 `92db30fa49ee4603ff27256d10898f785c42a252b4180503391ec09b175bb711`, matching the regenerated `k=6` summary. This makes the `k=6` table-consistency replay possible, but it does not add graph/pullback provenance.

The later Gate 2 script is also salvageable as a source of independent displayed-tree, tensor, pullback, and exact-sign routines. It should not be accepted wholesale as a certificate generator for the reasons in section 7.

### 3.2 Missing everywhere and requiring reconstruction

The following names were searched as ordinary files and archive members in:

- `/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_sharp_boundary`;
- `/Users/alec/Documents/Math/strong_level2_phylo_identifiability`;
- `/Users/alec/Downloads/STC_JC_AUDITOR_PACKAGE_RETRY`;
- `/tmp/stc_jc_retry_audit.HDx2sk/definitive_canonical_closure`;
- both repositories' complete local Git histories; and
- current `origin/main` (`941cf64f683b87a07cf7a7b5a6c11b1188a763c0`).

They were absent everywhere:

1. `all_F_patterns.json`;
2. `certificate_library.py`;
3. `cut_sign_library.json`;
4. `cycle_theta_end_to_end_assignments_v2.json`;
5. `generate_cycle_theta_end_to_end.py`;
6. `k4_features.npz`;
7. `primitive_compiler.py`;
8. `primitive_networks.py`;
9. `prototype_seven_census.py`.

The complete inventory is machine-readable in `repair/independent/atlas/dependency_inventory.json`.

The right repair is not to recreate those files solely to satisfy the old imports. A new compiler should use the salvageable primitive enumerators, independently rederive every displayed-tree pullback, preserve graph and transport provenance, and emit the schema in section 8.

## 4. Independent audit of the three large assignment JSONs

### 4.1 `k=5`

The streaming replay checked:

- 8,520 `equal` records;
- 18,480 `strict` records;
- all 27,000 source-mask-subset-target-mask directions;
- 18,840 referenced graph records;
- all 14 referenced exact sign records;
- all 13 distinct strict separator polynomials.

Every internal cross-reference, stored hash, signature direction, zero side, nonzero side, and exact sign factorization agreed. Status: **EXACTLY COMPUTED, TABLE CONSISTENCY ONLY**.

### 4.2 `k=6`

The replay checked:

- 10,980 `equal` records;
- 21,960 `strict` records;
- all 32,940 directions;
- 26,820 referenced graph records;
- both exact sign records and both strict polynomials.

Again, every internal check agreed. Status: **EXACTLY COMPUTED, TABLE CONSISTENCY ONLY**.

### 4.3 Cut assignments

The replay checked:

- 177 endpoint records: 151 `F>0`, 26 `F=0, G>0`;
- 453 single-blob records: 421 wrong-split strict, 32 rank-one;
- 598 signed records and 32 zero records;
- 528 distinct sign certificates, including seven partial Bernstein inheritance-variable certificates.

All exact polynomial/sign recomputations agreed. Status: **EXACTLY COMPUTED, TABLE CONSISTENCY ONLY**.

### 4.4 What these replays do and do not establish

They establish that the stored tables are not obviously corrupted and that their local algebra is self-consistent. They do not establish that:

- every admissible primitive topology was generated;
- every generated topology appears exactly once after the intended quotient;
- each stored graph was independently converted to the stored displayed-tree tensor;
- no source-target pair was omitted;
- canonical duplicate merges preserve the required port/parameter transport; or
- the finite universes promote to arbitrary subdivisions.

Those are precisely the properties a mutation-sensitive end-to-end reviewer must derive without trusting the assignment tables.

## 5. Direction and sign logic

Let bit `1` mean that the selected invariant has a nonzero pullback on the model. If the source model is contained in the target model, then

`I(target) subseteq I(source)`.

Therefore every invariant nonzero on the source must also be nonzero on the target:

`ones(source) subseteq ones(target)`.

The C++ condition

`source & ~target == 0`

at [`regenerate_directed_pair_universe.cpp:73`](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_sharp_boundary/reproducibility/publication/src/regenerate_directed_pair_universe.cpp:73) is thus oriented correctly. A strict record is separated when a pullback is identically zero on the source and has certified fixed nonzero sign on the target. Reversing the direction in the independent contract is rejected.

All available `k=5` and `k=6` strict-sign libraries were recomputed exactly; no sign-direction defect was found. See `repair/independent/atlas/direction_sign_audit.json`.

## 6. The `4,368 / 192 / 1,152 / 1,686` chain

These four numbers describe different objects:

| Count | Object | Audit conclusion |
|---:|---|---|
| 4,368 | Raw primitive cycle/theta equality presentations in the proposed compiler | Historical census exists; proposed end-to-end compiler is non-executable |
| 192 | Missing-three-support residual presentations, eight role patterns times 24 relabellings | Exactly replayed conditional subset |
| 1,152 | Proposed canonical completed **target** graphs over all missing-support sizes | Unexecuted assertion; not decorated pairs |
| 1,686 | Old role-normalized seven-port completed **target** graphs from the eight residual patterns | Exactly replayed for that generator; not decorated pairs |

The independent mutation test removed all 4,176 nonresidual rows from `cycle_theta_support_completion_corrected.json`, leaving only the 192 expected rows. Every selection predicate used by both the old primary and reviewer remained true. Hence both scripts are mutation-insensitive to the missing `4,368 -> 192` dependency. Exact evidence is in `repair/independent/atlas/seven_port_census_sensitivity.json`.

This is why the statement “all 1,686 valid completions are separated” is too strong. The certified statement is only “all 1,686 completions generated from these eight fixed residual role patterns are separated.”

## 7. Adversarial audit of `audit_gate2_nonroot_full_closure.py`

Audited script:

`/Users/alec/Documents/Math/strong_level2_phylo_identifiability/AUDIT/INDEPENDENT_IMPLEMENTATION/audit_gate2_nonroot_full_closure.py`

SHA-256:

`d88febb3e051378e769db3e55fcf9f9b51004f94eefe9975cc9e221a6727212d`

### 7.1 What is genuinely strong

The script independently enumerates displayed-tree descriptors and constructs exact JC coordinate polynomials and invariant pullbacks. Its strict-direction routine checks every distinct target descriptor deck, re-expands source zero identities, and sends target pullbacks through exact open-cube sign certification ([lines 2060–2149](/Users/alec/Documents/Math/strong_level2_phylo_identifiability/AUDIT/INDEPENDENT_IMPLEMENTATION/audit_gate2_nonroot_full_closure.py:2060)). This is materially stronger than replaying frozen signature bytes.

### 7.2 Missing successful pair-level binding

For each strict pair, the source side uses `representative_descriptors` ([lines 2073–2077](/Users/alec/Documents/Math/strong_level2_phylo_identifiability/AUDIT/INDEPENDENT_IMPLEMENTATION/audit_gate2_nonroot_full_closure.py:2073)); targets use every distinct descriptor deck ([lines 2085–2087](/Users/alec/Documents/Math/strong_level2_phylo_identifiability/AUDIT/INDEPENDENT_IMPLEMENTATION/audit_gate2_nonroot_full_closure.py:2085)).

Failures retain source and target signature hashes ([lines 2123–2130](/Users/alec/Documents/Math/strong_level2_phylo_identifiability/AUDIT/INDEPENDENT_IMPLEMENTATION/audit_gate2_nonroot_full_closure.py:2123)). Successful certificates do not: `factor_records` are keyed only by descriptor hash and invariant index ([lines 2131–2148](/Users/alec/Documents/Math/strong_level2_phylo_identifiability/AUDIT/INDEPENDENT_IMPLEMENTATION/audit_gate2_nonroot_full_closure.py:2131)). The output therefore cannot independently answer, for every successful source-target topology pair, which marginal, pullbacks, port transport, and sign certificate discharged that pair.

This is not proof that the finite calculation is wrong. It is a certificate-design failure that prevents adversarial replay and mutation detection.

### 7.3 Frozen primitive universe

The script loads its support source candidates from frozen encodings (function lines 1875–1917; recorded in `gate2_script_structure_audit.json`). It does not independently regenerate the primitive source universe from the locked graph rules. Therefore its finite closure remains conditional on the completeness and correctness of those frozen inputs.

### 7.4 Arbitrary-subdivision promotion is not a proof artifact

`arbitrary_subdivision_audit` constructs one fixed pattern per core with 12 extra blocks on one segment, probes every other segment, reverses the long word, and checks rational products only for lengths 1 through 8 ([lines 2714–2781](/Users/alec/Documents/Math/strong_level2_phylo_identifiability/AUDIT/INDEPENDENT_IMPLEMENTATION/audit_gate2_nonroot_full_closure.py:2714)).

The all-subdivision claims are then stored as prose strings (`compatibility_proof` and `weak_target_language_proof`) at lines 2795–2807. The Boolean derived from the finite tests is named `arbitrary_subdivision_lift_verified` at line 2809 and is load-bearing for final status at lines 3056–3070.

This proves that the reconstruction mechanism works on the constructed tests. It does not executablely establish, for every admissible source and target subdivision:

- existence of the asserted rigid support;
- triviality of every relevant labelled support stabilizer;
- coverage by support-plus-one and support-plus-two restrictions;
- consistency of pair orders under all automorphisms;
- coverage of potentially weak induced targets; or
- descent of every containment direction to a certified bounded marginal.

The mathematical prose may be a promising proof sketch, but it needs a separately written theorem proof with all quantified hypotheses and an independent checker for the finite lemmas it invokes. Finite word tests cannot carry the universal conclusion.

### 7.5 Independent crosscheck status

The separate adversarial crosscheck artifact is:

`/Users/alec/Documents/Math/strong_level2_phylo_identifiability/AUDIT/REVIEWS/gate2_nonroot_closure_adversarial_crosscheck.json`

SHA-256:

`5dd2b8dc9c0f91fb3c365bc776e489a1b7624678d64770d2f3df2cff5a277be7`

It records `UNRESOLVED` after `[Errno 32] Broken pipe`; its finite algebra sections are absent. The associated review explicitly refuses to accept the primary `PASS` without a completed independent replay. A later successful primary replay would provide useful regression evidence, but would not replace the failed independent implementation or repair the missing pair-level output.

Verdict for this script: **UNRESOLVED**.

## 8. Required mutation-sensitive end-to-end certificate

The replacement should use two independently generated manifests: a producer manifest and a reviewer manifest. The reviewer must regenerate its manifest from primitive rules and must not copy graph lists, pair lists, canonical IDs, or witness choices from the producer.

### 8.1 Primitive record

Every primitive presentation must contain:

- canonical content-addressed rooted and standard semi-directed graph encodings;
- explicit vertex types, directed arcs, ports, labels, and incoming port;
- class-validation trace;
- displayed-tree choices and retained/deleted incoming edges;
- descendant split/mask trace for every displayed edge;
- exact tensor/pullback hash;
- raw-to-canonical vertex bijection;
- induced edge, port, label, and parameter transport.

### 8.2 Directed pair record

Every ordered pair must contain:

- `pair_id = H(source_graph_hash, target_graph_hash, direction, port_map)`;
- source and target primitive IDs;
- direction and complete port correspondence;
- source/target sink and restored-support roles;
- for equality: labelled isomorphism or `T` move, plus exact parameter map;
- for strict separation: witness marginal, invariant, exact source pullback, exact target pullback, certified sign, and a binding hash over the complete record;
- for any quotient merge: explicit raw-to-canonical isomorphism and transported witness/parameter data.

### 8.3 Universe commitments

The top-level certificate must commit to:

- primitive enumerator source hashes and locked conventions;
- ordered primitive manifest hashes;
- the Cartesian or otherwise explicitly defined pair universe;
- exact expected pair count derived from those manifests;
- no duplicate pair IDs and no missing pair IDs;
- a Merkle root or canonical hash of all pair records;
- separate hashes for success and failure/unresolved records.

### 8.4 Independent reviewer

The reviewer must independently:

1. regenerate primitive networks;
2. canonicalize them with separate code;
3. enumerate displayed trees;
4. derive every tensor and pullback;
5. regenerate the complete ordered pair set;
6. select or verify a separator without trusting the producer's witness choice;
7. verify every raw-to-canonical transport;
8. compare only final content hashes and mathematical records.

### 8.5 Mandatory mutations

At minimum, CI must demonstrate rejection of:

- one omitted primitive;
- one duplicated primitive;
- one mutated edge or reticulation direction;
- one omitted pair;
- one duplicated pair;
- one reversed direction;
- one swapped polynomial between two pairs;
- one wrong zero side;
- one stale pair-set hash;
- one missing raw-to-canonical transport;
- a coordinated producer-only graph/polynomial rewrite;
- deleting the 4,176 nonresidual seven-port census rows while retaining the 192 residual rows.

The bounded prototype in `certificate_contract.py` already rejects nine representative mutations, including the coordinated internal rewrite. This demonstrates the schema behavior; it is not itself the atlas certificate.

## 9. Repair plan

### Can be retained

1. Primitive core and structural enumeration algorithms, after an independent canonicalizer replay.
2. JC displayed-tree tensor and invariant formulas.
3. Exact sign libraries, with polynomial hashes as caches rather than authority.
4. The fast bytewise subset filter as a candidate generator.
5. The old seven-port factors, target completion enumeration, and rank minors as conditional lemmas.
6. The later Gate 2 displayed-tree/pullback/sign routines as a second implementation.

### Must be rewritten or extended

1. A primitive-to-decorated-pair compiler for `k=5`, `k=6`, cut, and cycle/theta universes.
2. An independent compiler with no shared enumeration, canonicalization, or algebra code.
3. Explicit graph/signature/pullback provenance retained in durable outputs.
4. Explicit raw-to-canonical transports for every quotient merge.
5. A true `4,368 -> residual/nonresidual disposition -> completion` pair-level ledger.
6. A theorem proof for arbitrary subdivisions, separated from finite stress tests.
7. An independent replay that completes without `BrokenPipeError` and emits bounded, streamable records.

## 10. Outcome B

Outcome B states that the intended theorem is not disproved, but the positive release is not internally or reproducibly certified. That is the correct conclusion.

The strongest independently supported refinement is:

- `1,686` is exactly replayed for the old target-only role-normalized completion generator;
- the proposed `1,152` is a target-only assertion under a different scope and has not been generated from the supplied package;
- neither number is the required decorated source-target relation count;
- exact signs and stored pair-table directions check out;
- the first unresolved node is end-to-end primitive-topology-to-pullback binding and exhaustive arbitrary-subdivision promotion;
- all global classification claims depending on that node remain withheld.

This agrees with [`STATUS.md:3–16`](/Users/alec/Downloads/STC_JC_AUDITOR_PACKAGE_RETRY/01_CURRENT_FAIL_CLOSED_STATUS/STC_JC_Final_Reconciliation_Outcome_B/STATUS.md:3), [`COUNT_RECONCILIATION.md:5–83`](/Users/alec/Downloads/STC_JC_AUDITOR_PACKAGE_RETRY/01_CURRENT_FAIL_CLOSED_STATUS/STC_JC_Final_Reconciliation_Outcome_B/audit/COUNT_RECONCILIATION.md:5), and the missing-node analysis in [`CLAIM_DEPENDENCY_GRAPH.md:24–45`](/Users/alec/Downloads/STC_JC_AUDITOR_PACKAGE_RETRY/01_CURRENT_FAIL_CLOSED_STATUS/STC_JC_Final_Reconciliation_Outcome_B/CLAIM_DEPENDENCY_GRAPH.md:24).

## 11. Deterministic diagnostic replay

From the repository root:

```sh
REPAIR_CERT=/tmp/stc_jc_retry_audit.HDx2sk/definitive_canonical_closure/source/artifacts/stc_jc_end_to_end_repair/release_work/certificates
PUB_CERT=reproducibility/publication/certificates
EXACT_CERT=reproducibility/exact_release/certificates
OLD_REPO=/Users/alec/Documents/Math/strong_level2_phylo_identifiability

python3 repair/independent/atlas/direction_sign_logic.py \
  > repair/independent/atlas/direction_sign_audit.json

python3 repair/independent/atlas/audit_assignment_bindings.py \
  --assignment "$REPAIR_CERT/directed_k5_end_to_end_assignments.json" \
  --relation-tsv "$PUB_CERT/theta_k5_directed_pairs.tsv" \
  --sign-library "$EXACT_CERT/canonical_theta_k5_strict_signs.json" \
  --outgoing 5 \
  --source-signatures "$PUB_CERT/theta_k5_strong_signatures.bin" \
  --target-signatures "$PUB_CERT/theta_k5_weak_signatures.bin" \
  > repair/independent/atlas/k5_binding_audit.json

python3 repair/independent/atlas/audit_assignment_bindings.py \
  --assignment "$REPAIR_CERT/directed_k6_end_to_end_assignments.json" \
  --relation-tsv "$PUB_CERT/theta_k6_directed_pairs.tsv" \
  --sign-library "$EXACT_CERT/canonical_theta_k6_special_strict_signs.json" \
  --outgoing 6 \
  --source-signatures "$PUB_CERT/theta_k6_strong_signatures.bin" \
  --target-signatures /tmp/stc_theta_k6_weak_signatures.bin \
  > repair/independent/atlas/k6_binding_audit.json

python3 repair/independent/atlas/audit_cut_assignment_table.py \
  "$REPAIR_CERT/cut_end_to_end_assignments.json" \
  > repair/independent/atlas/cut_binding_audit.json

python3 repair/independent/atlas/seven_port_census_sensitivity.py \
  "$EXACT_CERT/cycle_theta_support_completion_corrected.json" \
  > repair/independent/atlas/seven_port_census_sensitivity.json

python3 repair/independent/atlas/audit_gate2_script_structure.py \
  "$OLD_REPO/AUDIT/INDEPENDENT_IMPLEMENTATION/audit_gate2_nonroot_full_closure.py" \
  --crosscheck "$OLD_REPO/AUDIT/REVIEWS/gate2_nonroot_closure_adversarial_crosscheck.json" \
  > repair/independent/atlas/gate2_script_structure_audit.json

python3 repair/independent/atlas/certificate_contract.py \
  > repair/independent/atlas/certificate_contract_mutation_test.json

python3 repair/independent/atlas/inventory_dependencies.py \
  /Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_sharp_boundary \
  /Users/alec/Documents/Math/strong_level2_phylo_identifiability \
  /Users/alec/Downloads/STC_JC_AUDITOR_PACKAGE_RETRY \
  /tmp/stc_jc_retry_audit.HDx2sk/definitive_canonical_closure \
  > repair/independent/atlas/dependency_inventory.json
```

The `k=6` command requires extracting the historical weak-signature member:

`reproducibility/publication/certificates/theta_k6_weak_signatures.bin`

from:

`/Users/alec/Downloads/STC_JC_AUDITOR_PACKAGE_RETRY/05_AUTHOR_READY_HISTORICAL/STC_JC_All_Level2_Author_Ready_Release_v1.1.1/submission/STC_JC_Reproducibility.zip`.

The expected extracted SHA-256 is:

`92db30fa49ee4603ff27256d10898f785c42a252b4180503391ec09b175bb711`.

## Final release recommendation

Do not submit the positive standard-class classification as proved. Retain Outcome B, preserve the exact finite computations as partial evidence, and repair the single load-bearing atlas node with a topology-indexed, transport-aware, mutation-sensitive producer/reviewer pair. Once that is complete, the bounded-support theorem still requires a standalone quantified proof before arbitrary subdivisions or the global theorem can be promoted.
