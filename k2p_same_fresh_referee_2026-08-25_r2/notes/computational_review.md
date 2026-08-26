# Fresh computational/code adversarial subreview

Date: 2026-08-25 PDT
Archive reviewed: `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/isolated/k2p_principal_d_plus_submission_referee`
Scratch/output root: `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/tmp`
Review boundary: computational generators, exact finite classifications, graph canonicalization, K2P maps, symbolic certificates, restoration/probe machinery, mutations, release harness, and replay telemetry. The isolated archive was treated as read-only. After the bounded adversarial work, the root referee completed the qualified clean `--full` replay and supplied its parsed report and execution telemetry; those fresh results are incorporated below.

## Bottom line

**Computational evidence: HOLD.** I found no counterexample to the corrected finite classification and no mutant that survived the revised corrected-composite production verifier. The declared raw universes and every requested census reconcile exactly. The strict K2P Fourier convention and quartet formula now agree, and the revised composite mutation path genuinely presents complete mutant ledgers to the production verifier. The fresh qualified full release replay completed all 40 layers with status PASS in 5,317.14 s, including full canonicalizer, graph-derived parameter-transport, rank, direct36, raw4, theta2, and corrected-probe regeneration/replays.

The HOLD is caused by two concrete mutation-evidence defects and two independence gaps:

1. `test_canonicalizer_mutations.py` treats **any** nonzero child exit as semantic rejection. I freshly demonstrated that a missing `networkx` dependency yields a top-level mutation **PASS** for both cases. The release binder likewise checks only nonzero exit, not the intended diagnostic. The same diagnostic-blind pattern is present in the restoration and primary probe mutation wrappers, although the probe wrapper has a clean nondefault-hash-seed baseline that catches a globally broken environment.
2. `run_parameter_transport_mutations.py` never runs a mutant through the production full verifier. It calls local row-shape validators and then declares every changed row rejected because `sha(mutant) != sha(clean)`. Four of ten fresh cases had no structural diagnostic at all and passed solely through that tautology. `release_common.py` explicitly accepts this field as sufficient.
3. The fresh independent census recomputes the primitive completion domains, raw-ID coordinates, counts, hashes, ordering, parent closure, and transport-reference closure, but it does **not** independently reclassify every analytic row. Category totals are counted from the submitted ledgers.
4. The canonicalizer certificate compares slow and optimized descriptor action on all 10,084 primitive archetypes and independently checks 4,012 raw4 relation-eligible presentations. It is not an exhaustive independent graph-orbit merge/split audit of every theta2, cycle, restoration, and probe equality presentation. The fresh full replay confirms reproducibility of the submitted graph machinery, but it does not remove that independence boundary.

These are computational-completeness/evidence defects, not a demonstrated false theorem. The completed full run establishes that the frozen artifacts reproduce under the production checks. It does not make the deficient mutation wrappers genuinely adversarial or provide an independent all-family classifier.

## Per-layer status

| Layer | Status | Fresh/inspected evidence | Exact remaining gap |
|---|---|---|---|
| Primitive directed cores and completion grammar | **PASS** | Within the declared five-core grammar: literal arc/reticulation/repair encodings inspected; independent enumerator imports no submission module | The mathematical assertion that these five cores exhaust the theorem class is proof-level, not proved by the generator |
| Raw4/theta2/cycle raw-ID domains and exactly-once ordering | **PASS** | Independent enumeration and streaming audit, 51.79 s | Analytic category predicates are not all independently recomputed |
| Corrected-composite verifier and revised mutations | **PASS** | Four bounded complete-ledger attacks plus all 22 declared raw4/theta2 semantic attacks in the fresh release-mutation run reached the production verifier and failed at intended semantic row gates | The declared suite has no dedicated reverse-direction case, but the separate fresh bounded attack supplies it; the verifier still shares the submitted atlas |
| Descriptor canonicalizer action | **PASS** | Fresh full replay regenerated the 10,084-archetype audit; exact action code inspected | No completely separate proof of primitive-core exhaustiveness |
| Strict mixed-graph relation canonicalizer | **UNVERIFIED** | Audited raw4 scope PASS: independent implementation reports 4,012/4,012 agreement; two intended triangle attacks pass in qualified environment | No exhaustive independent theta2/cycle/restoration/probe merge/split partition |
| K2P Fourier/model-map convention and strict domain | **PASS** | Fresh exact quartet replay; fresh independent rational boundary/product audit | Higher-degree full-map compiler not independently rebuilt for every descriptor here |
| Quartet terminal algebra | **PASS** | Fresh exact symbolic formula/transport replay, eight exact-diagnostic mutations, and fresh full 4,414,710-row terminal binding replay | Graph-to-split binding still uses submitted graph machinery |
| Symbolic rank upper mechanism | **PASS** | Production replay: coefficientwise exact integer systems inspected; fresh full verifier replayed all 4,379 descriptors | No second independently written engine replayed all 4,379 descriptors |
| Quadratic/cubic/quartic/quintic polynomial certificates | **PASS** | Production replay: fresh full direct36 replay and fresh release mutations for reassigned cubic/quartic/quintic certificates | Independent full-body replay remains unverified: I did not recompute every polynomial body/pullback through a separately written symbolic engine |
| Restoration forest census/ordering/reference closure | **PASS** | Production/structural evidence: independent stream checks plus fresh qualified 13/13 mutation run and full release validation | Mutation wrapper is diagnostic-blind; no separate all-child symbolic engine was written |
| Probe census/Cartesian coverage/reference closure | **PASS** | Production and submitted independent replay: independent stream checks plus fresh full regeneration, streaming replay, site partition, graph audit, and fresh qualified 15/15 mutations | Primary mutation wrapper does not bind intended diagnostics; graph auditor shares the atlas |
| Graph-derived edge/inheritance parameter transports | **PASS** | Production replay: fresh full producer regeneration/byte comparison; counts reconcile | Mutation evidence remains HOLD: four of ten dedicated cases are invalid as live attack evidence |
| Authoritative/historical/revoked separation | **PASS** | Explicit registries/gates and fresh full 40-layer release validation | Not independently re-derived beyond the signed registries |
| Release harness and replay telemetry | **PASS** | 9/9 telemetry unit tests and fresh 40/40 full replay; exit markers, source fingerprint, blockers, and output hashes checked | Wrapper defects described below remain despite successful qualified execution |

## Numbered findings

### 1. Computational-completeness-blocking: canonicalizer mutation wrapper can report PASS on dependency failure

File: `work/canonicalizer_completeness/test_canonicalizer_mutations.py`, lines 71-99. `run_mutation` requires only `completed.returncode != 0`; it does not require either intended diagnostic:

- `CANONICALIZER_COMPLETENESS_FAIL:NONORDINARY_ATLAS_ACCEPTED`
- `CANONICALIZER_COMPLETENESS_FAIL:SELECTED_TRIANGLE_ATLAS_ACCEPTED`

The release binder repeats the weakness at `work/final_theorem_release/release_common.py`, lines 4735-4752: it checks names, `rejected is True`, and nonzero exit, but not `diagnostic_tail`.

Minimal fresh reproducer:

```text
/usr/bin/time -l /opt/homebrew/bin/python3 -B \
  work/canonicalizer_completeness/test_canonicalizer_mutations.py \
  --output /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/tmp/canonicalizer_mutations_fresh.json
```

Observed top-level exit: 0; runtime 0.20 s; maximum RSS 28,295,168 bytes; report SHA-256 `f4bf1d4eb8f9ef48213ab05cf8de2f48a2f368e2809a2f62474b931e135d32c9`. Both alleged rejections contain only:

```text
ModuleNotFoundError: No module named 'networkx'
```

Nevertheless the wrapper prints `K2P_CANONICALIZER_MUTATIONS_PASS rejected=2 survived=0` and writes status `PASS`.

Control replay in the qualified venv:

```text
/usr/bin/time -l .../tmp/execution/k2p_principal_d_plus_submission_referee/.venv/bin/python -B \
  work/canonicalizer_completeness/test_canonicalizer_mutations.py \
  --output .../tmp/canonicalizer_mutations_fresh_venv.json
```

Observed exit 0; runtime 0.40 s; maximum RSS 50,413,568 bytes; report SHA-256 `10b8eebaa739f3853434527bd6b55d90cdb28028345cb6285d687a8c3961dfdc`. This time the two intended semantic diagnostics were observed. The sealed canonical mutation certificate is byte-identical to this correct control report.

Effect: the frozen cases happen to contain the right diagnostics, so this does not show that the corrected triangle guards are wrong. It does show that the mutation mechanism and release binding are not fail-closed under missing dependencies, contrary to the protocol.

Smallest remedy: require an exact expected diagnostic per case, reject traceback/import/timeout diagnostics, require no success artifact, and run a clean unmutated baseline before the attacks. Bind the exact diagnostic map in `release_common.py`. Regenerate the mutation certificate and reseal the release lock/telemetry; no mathematical source change is implied.

### 2. Computational-completeness-blocking: four inheritance-transport attacks are accepted by a tautological byte inequality

Files:

- `work/canonicalizer_completeness/inheritance_transport/run_parameter_transport_mutations.py`, lines 156-187.
- `work/final_theorem_release/release_common.py`, lines 4877-4903.

The runner imports the production verifier module but invokes only `validate_relation` or `validate_restriction` on one in-memory row. Lines 173-178 then set

```text
rederived_rejection = sha(mutant) != sha(clean)
```

and treat that inequality as a semantic replay rejection. Every nontrivial mutation satisfies it by construction. No mutant ledger is created, no certificate is resealed, and the production `main`/`rederive_and_compare` path is not invoked. The release binder explicitly requires only `rederived_exact_row_mismatch is True` for every case.

Fresh command:

```text
python3 -B work/canonicalizer_completeness/inheritance_transport/run_parameter_transport_mutations.py \
  --output /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/tmp/parameter_transport_mutation_fresh.json
```

Exit 0; runtime 28.65 s; maximum RSS 40,501,248 bytes; output SHA-256 `893d1716040315a24191a1b05fee3aa5cfcf1900b780d3f283c0921de3e20634`; payload SHA-256 `4640b0015ec251e98cf392377025956def5bd828d41fb5c8412d937921d40722`.

Four cases have `structural_diagnostic: null` and were counted rejected solely because their hash changed:

1. `triangle_edge_false_product_map`
2. `serial_product_factor_omitted`
3. `root_suppressed_incoming_incidence_hidden`
4. `source_target_reversal_without_inverse_transport`

Six other cases do trigger local schema checks (flip flag, paired products, and related constraints), but they also do not invoke the production full verifier.

The underlying full verifier is stronger: `verify_parameter_transport_certificate.py`, lines 147-176, checks ledger structure, uniqueness, paired product fields, parent-order/complement rules, and counts; lines 206-224 run the producer in a temporary directory and require byte equality of all regenerated ledgers. Thus a coherently resealed corrupted ledger should fail the full replay. What is missing is a genuine executed attack demonstrating that fact at the intended mechanism.

Smallest remedy: write each mutant into a complete disposable ledger/certificate package, coherently reseal local hashes/counts, invoke the untouched production verifier, and require an exact semantic or regenerated-byte diagnostic. Do not count bare inequality with the clean row. Update the release binder and reseal report/lock/telemetry.

### 3. Computational-evidence weakness: restoration and primary probe mutation wrappers do not require intended diagnostics

Restoration: `work/restoration_sign_reclassification/mutate_corrected_restoration_forest.py`, lines 154-181 and 198-212, sets `rejected = returncode != 0` and requires only that boolean. The release binder at `release_common.py`, lines 3014-3039, likewise checks only nonzero exits and case names. The stored report and the fresh 13-case replay contain plausible intended diagnostics, but the wrapper would also accept an unrelated import/runtime failure for every mutant. There is no clean baseline in this wrapper.

Probe: `work/probe_coherence_corrected/run_probe_coherence_mutations.py`, lines 200-213 and 351-390, also accepts any nonzero mutant exit. Its final nondefault-hash-seed clean replay is useful and prevents a globally missing dependency from producing a final PASS, but a mutation-specific unrelated crash can still be misreported as semantic rejection. The release binder at `release_common.py`, lines 2544-2572, does not bind diagnostics.

These suites do invoke their production verifiers on disposable artifacts. After the initial code audit, both were freshly executed with the qualified Python environment:

- Restoration: 13/13 nonzero rejections; outer runtime 33.61 s; peak child RSS 524,255,232 bytes; fresh report SHA-256 `e5b3763c7fca333646e86462e0ca8af1332f98f650744f87c64c8a67f39b76ab`; payload `746f6c6e6194acd3eb5b7673190efef8b95542af03f80a5cbc765c0ba991a63f`; stdout SHA-256 `fea309eafd5db60628a758dd57fed5ab4041ac113b8d6433156a98e68461055b`. Omitted first/second rows, wrong second parent, cycle attempt, and optimized mode produced directly corresponding diagnostics. Seven transport/algebra attacks stopped at the plausible package-level `CORRECTED_RESTORATION_REPLAY_FAIL:manifest transports` gate rather than distinct deepest predicates. This is successful qualified rejection evidence, but it reinforces why an exact per-case diagnostic contract is still needed.
- Probe: 15/15 nonzero rejections at case-appropriate diagnostics plus a successful clean `PYTHONHASHSEED=12345` replay; outer runtime 168.20 s; maximum RSS 71,532,544 bytes; fresh report SHA-256 `4ba412df4e92ce696a10140e742e7aad82c3a0f685580f2ff33b8b638d566b64`; payload `467dbb662127c8a8a91c0cc1f98bed576d8d6037958b8c1323b0d2c8f9e08923`; stdout SHA-256 `36e9a56591c9874877cc62c66742f0e2bd8d4c9aea9478263e1155287f14637b`.

The fresh qualified runs show that the sealed cases reject in the intended environment. They do not repair the wrapper design: neither runner nor release binder requires those observed diagnostics, and the canonicalizer counterexample proves why nonzero alone is insufficient.

Smallest remedy: exact per-case diagnostic contracts, absence-of-success-report checks, and a clean baseline for restoration. Bind these diagnostics in the release verifier and reseal.

### 4. Independence limitation: the fresh census validates domains/contracts, not every analytic classification predicate

`tmp/fresh_census_audit.py` imports only the standard library. It independently enumerates the literal core/count/repair completion grammar, decodes every raw ID and lexicographic port permutation, verifies dense order, streams all ledgers, recomputes row hashes and category totals, and checks parent/reference closure. It deliberately counts each submitted analytic category label rather than recomputing quartet, whole-map sign, rank, polynomial, or graph-relation predicates for every row.

Therefore the census is genuinely independent evidence for the finite domains, exactly-once coordinates, counts, hashes, and referential integrity. It is not an independent classifier replay. Any final report should not describe it as such.

### 5. Independence limitation: no global independent merge/split partition was completed

The canonicalizer certificate SHA-256 `dd1eca849a992a14ef7b4942e2e4e864052f210c23b132fc8dfc9cbd5f513afa` reports:

- 10,084 primitive descriptor archetypes compared by slow and optimized action, zero disagreements: raw4 source/target 6/2,814; theta2 4/6,138; cycle 2/1,120.
- An independent strict mixed-graph implementation on 4,012 raw4 topology/rank-eligible presentations: 3,932 none, 26 isomorphic, 54 ordinary triangle, zero disagreements.

The relation replay independently implements restriction, root suppression, the ordinary-triangle predicate, marked incidence expansion, and labelled graph isomorphism, but imports the atlas-generated primitive graphs. It does not claim an all-family relation partition. The submitted full probe graph auditor reconstructs all probe rows and 67,741 transports, but it also loads the same atlas for primitive graphs, restrictions, and mixed graphs. A truly independent all-family merge/split partition therefore remains **UNVERIFIED**.

## Answers to the eleven code questions

1. **Primitive encodings versus hidden topology oracle — PASS within the declared grammar.** `k2p_atlas_core.py` lines 9-41 gives literal directed arc tuples, reticulation/sink roles, and repair-segment indices for cycle/theta0/theta1/theta2/theta3. `build_graph`, lines 65-110, creates primitive nodes/arcs and validates DAG, binary degrees, unique labels, and strong tree-childness. No topology-name lookup or revoked rooted tree/sunlet classifier is used to construct corrected composite rows. The proof that these five cores exhaust all relevant level-2 cases is outside code.

2. **Every raw directed relation generated exactly once before classification — PASS.** Raw4 uses 6 sources × 2,814 targets × 24 port permutations = 405,216; theta2 uses 4 × 6,138 × 120 = 2,946,240. Corrected generators iterate `raw_id in range(total)` and decode source/target/permutation directly. Independent streaming found dense IDs, no duplicate coordinates, no omitted rows, and canonical JSON ordering.

3. **Direction, incoming/dummy roles, ports, parent order, and boundary transports — PASS production replay; mutation evidence HOLD.** Incoming and dummy roles are explicit in `target_completions` lines 140-180; physical port permutations are retained in every row. A fresh complete-ledger reversed-direction attack and a fresh wrong-port attack failed at production composite row gates. Parent-order/complement schema checks are present in `verify_parameter_transport_certificate.py` lines 89-109 and 130-144. The fresh full run regenerated and byte-compared all graph-derived parameter transports. The dedicated mutation proof remains invalid for four cases as described in Finding 2.

4. **Canonicalizer false merge/split — PASS for the audited scopes; globally UNVERIFIED.** The descriptor action enumerates all reticulation permutations and independent parent flips (`retic_variants`, lines 229-236) and lexicographically minimizes the exact integer descriptor (`model_descriptor`, lines 315-317). Strict ordinary triangles require exactly two heads into one reticulation and the forgotten edge is marked (`_mixed_triangle_edges`, lines 871-898; incidence expansion, lines 900-948). The all-family independent graph-orbit partition was not performed.

5. **Rank upper certificates symbolic and globally valid rather than sampled — PASS production replay.** `syzygy_upper.py` builds exact integer coefficient equations for the polynomial identity `J_f V=0`; upper rank is parameter count minus the exact evaluated kernel-field dimension. `verify_rank_upper_certificates.py` permits only the two symbolic mechanisms and binds all 4,379 descriptors. Sampled minors supply lower bounds only. The fresh full run completed `four_port_exact_rank_full` and byte-compared the regenerated replay. The rank mutation suite remains helper-level rather than a production-verifier mutation replay; its sampled-rank case is a shape-validator check.

6. **Polynomial coordinates/pullbacks match printed Fourier maps — PASS for quartet, UNVERIFIED for all higher-degree bodies.** Atlas character order is `(0,C,G,T)`, `ct_orbit_rep` swaps C/T while fixing G (lines 206-213), and `sector_for_mask` maps G to sector 2 and C/T to sector 1 (lines 252-257). Fresh exact quartet replay derives formulas from spectrum `(1,s,g,s)` and checks all 288 character/leaf transports. Direct residual polynomial code performs exact sparse substitution, but I did not independently rederive every quadratic/cubic/quartic/quintic pullback.

7. **All 997 restoration obligations have physical children, parent, transport, no cycle, terminal leaf — PASS production/structural.** Independent checks give 997 canonical parents, 2,540 physical/member roots, 36,568 first children, 256 second children, 36,824 edges, 36,792 leaves, depth two, and dense parent/hash closure. The production release validation and graph-derived transport regeneration closed all referenced restrictions, and a fresh qualified 13-case restoration mutation run rejected every attack. A separately written all-child algebra engine was not added.

8. **Every physical probe site and required one-/two-port relation — PASS production and submitted independent replay.** Independent checks give 176 anchors, 2,206 sites per side, all 29,964 one-port Cartesian rows, 2,107 equality parents, all 544,571 two-port rows, 67,741 exact transports, and 4,379 parent restrictions. Keys, ranges, parent inventories, and references are exact. The fresh full run regenerated the entire probe package, reran the streaming verifier, site partition, and independent primitive-graph audit, and byte-compared their outputs. A separate qualified 15-case mutation run rejected every attack and passed the clean hash-seed replay.

9. **Independent replayers do not import decisive expected classification/canonicalizer — PARTIAL/UNVERIFIED.** Corrected-composite verifier independently streams every row and recomputes evidence, but dynamically imports the same atlas. The probe graph auditor does not import the probe producer/verifier yet loads the same atlas for graph primitives and restrictions. The fresh census imports no submission code but does not recompute analytic predicates. No one replay is independent of both the expected labels and the decisive graph/map compiler across every layer.

10. **Authoritative, historical, revoked, expository artifacts fail closed — PASS.** `release_common.py` maintains explicit authoritative replacements and a historical proof-artifact registry, refuses legacy rooted fields in promoted rows, and verifies revoked-row coverage and replacement bindings. The fresh full replay scanned and bound these registries. No contrary live path was found.

11. **Optimized execution, stale hashes, missing dependencies, or malformed reports cannot turn failure into PASS — FAIL for mutation evidence; PASS for main release harness.** `verify_final_theorem_release.py` lines 52-94 requires child exit zero plus terminal markers; lines 97-141 requires exact markers for licensed expected failures; lines 1119-1176 rejects optimized mode, blockers, source drift, and nonpassing layers. Fresh telemetry tests reject dirty/attached checkout, wrong commit, bad lock payload, nonpassing/malformed report, malformed expected-failure rows, and output drift. However Finding 1 is a direct counterexample for the canonicalizer mutation wrapper, and Findings 2-3 show weaker mutation binding.

## Independent finite census

Independent script: `tmp/fresh_census_audit.py`, SHA-256 `933e2dac57fd09a409288576a5473ab5d7c54070fc8c82567793f3a099a0a163`. It imports no submission module. Output SHA-256 `844646caeadcf36885d722c85188b3f00fd29e0d6619ca7f5feb58006c791905`; payload SHA-256 `d153a47da7b01e3adc710e81a0115d8f7bbf3f05d07ff40ab4e00a97bc086946`.

### Primitive completion counts

| Ports | Incoming selected | Incoming marginalized | Total |
|---:|---:|---:|---:|
| 3 | 289 | 831 | 1,120 |
| 4 | 831 | 1,983 | 2,814 |
| 5 | 1,983 | 4,155 | 6,138 |

Source supports: raw4 6; theta2 4; cycle 2.

### Raw4

405,216 rows, ledger SHA-256 `431dac8898ad2a724d12c200687de1b377723e302214a79a11a03524a4084b96`:

| Category | Count |
|---|---:|
| Displayed quartet exclusion | 360,408 |
| Whole-map strict sign | 16,974 |
| Exact rank exclusion | 23,822 |
| Direct terminal presentation | 1,472 |
| Restoration member presentation | 2,540 |

Direct registry SHA-256 `0a1818655429d60660c1ed87f3fbe412701f386b081562b3a4caa54079069f1d`: 934 classes = 839 quadratic + 36 higher-degree + 4 hard + 20 isomorphism + 35 triangle. Higher degree = 22 quintic + 12 quartic + 2 cubic.

### Theta2

2,946,240 rows, ledger SHA-256 `805fc7f5a3de9dad2c63a210208075cf19910cf811ffd08878f32782ce71b659`:

| Category | Count |
|---|---:|
| Displayed quartet exclusion | 2,942,592 |
| Whole-map strict sign | 2,528 |
| Exact rank exclusion | 800 |
| Direct quadratic | 240 |
| Labelled isomorphism | 80 |

Dummy forest SHA-256 `e41cd1bdb8ecc9fac8e092970c7fcd11d98bf56dadde3f6b6ba7d426df751271`: 56 roots; 576 six-port children (504 quartet, 72 isomorphism); 32 continuations; 288 seven-port children (256 quartet, 32 isomorphism); 864 descendants; 832 leaves.

### Cycle

Authoritative base ledger SHA-256 `d6209dc605c9f3a3459c129d741c6b788f26dcf989afe828d8a720833bfd49da`: 13,440 = 7,452 whole-map strict sign + 5,964 restoration + 8 isomorphism + 16 triangle.

Authoritative full ledger SHA-256 `cc73d0eaf3f39939c255c8f86915093e58159eca37c147ae2854d430f1fcb2f7`: 536,364 = 535,920 quartet + 132 quadratic + 300 whole-map strict sign + 12 isomorphism.

### Restoration

Forest SHA-256 `43bd2be5e7626a954fc4fa4cf45e8d0e6483c947ddc9cba80f2b1a13351bc3a8`:

- 997 canonical parents; 2,540 member/physical roots.
- 36,568 first children; 256 second children; 36,824 edges.
- 36,792 leaves; depth two.
- 42 first-source transport classes; 4,986 first-target classes.
- All ordinals, row hashes, second-parent hashes, continuation references, and terminal coverage closed.

### Probes

- 176 anchors; 2,206 source sites; 2,206 target sites.
- 29,964 one-port rows = 27,758 quartet + 99 whole-map sign + 1,915 isomorphism + 192 triangle; 2,107 equality survivors.
- 2,107 two-port parents; 544,571 two-port rows = 511,266 quartet + 576 whole-map sign + 30,969 isomorphism + 1,760 triangle; 32,729 equality/reverse-parent survivors.
- 67,741 exact transports; 4,379 parent restrictions.
- All Cartesian keys were unique and in range; all equality-parent, transport, and restriction references resolved.

## K2P/domain attack

Independent script `tmp/k2p_domain_boundary_audit.py`, SHA-256 `aad747d88462d2e205181932b724816ab79b407c0e9fc048fdd89b12569e9e0a`; output SHA-256 `39e2101d0aacd7b4326b7f5795e1ac9ece32f2aa5f50d595fde7a63f562a3b25`; payload `9565a7c8435edef6994d5caf9b7f1e50cd2d766d123debb76d019425fac5ae47`.

Using exact `Fraction` arithmetic and no submission imports, it checked:

- Spectrum `(1,s,g,s)` with equal C/T sector.
- Inverse probabilities `(1+2s+g)/4`, `(1-g)/4`, `(1-2s+g)/4`, `(1-g)/4`.
- Strict stochasticity iff `0<s<1`, `0<g<1`, `g>2s-1` on 136 grid points.
- 20 boundary-near rational witnesses, including the oblique facet and continuous-time cone.
- Closure of `D_plus` under 10,404 pairwise coordinate products from the exact grid.
- Continuous-time implication by `s^2-(2s-1)=(1-s)^2>0`.

Exit 0; 0.07 s; maximum RSS 19,152,896 bytes.

## Revised corrected-composite mutation audit

Production verifier: `work/corrected_composite_ledgers/verify_corrected_composites_independent.py`, SHA-256 `67ddf315b400a0a96f4a5901e6a340a158d9d4fd1111e8ee17193de5d78b5690`. Production mutation runner SHA-256 `0d5f43ffe827015fe43404d627ef962b930f059752491fe77fdef5a1f4c7ec34`.

Four complete deterministic mutant ledgers were streamed through the untouched production verifier. Each failed before checksum comparison at the intended semantic row gate, wrote no verifier report, and left source hashes unchanged:

| Attack | Raw ID | Intended/observed diagnostic | Runtime | Mutant SHA-256 |
|---|---:|---|---:|---|
| Raw4 wrong port permutation | 0 | `PORT_PERMUTATION:0` | 5.837550 s | `fcd2f649befe0175b30d47c87d421826e613f465a5a31dd22e6a97d1931ad66f` |
| Raw4 alternate valid parent | 2185 | `RAW4_RESTORATION_EVIDENCE:2185` | 8.187266 s | `fbf0ddf28ec78f8bf1b1a6d07c132f43ff98d774d8089f1a07e78520e6aec3fe` |
| Raw4 source-to-target direction reversed | 2185 | `RAW4_RESTORATION_EVIDENCE:2185` | 8.501306 s | `7794d2642b93c3a23f7c9ddefdccbcf6f2fc592298ff5ab4a016558fdaeb3be2` |
| Theta2 inherited child count decremented | 166201 | `THETA2_ISOMORPHISM_EVIDENCE:166201` | 62.456625 s | `37701995f32077958f7033f582e1750d07cea33bd3bbdd60daa9cedcfe5a7faf` |

Outer runtime 85.23 s. Machine report SHA-256 `1ea89890987b6b675da080bd38fe8bcedb409c9c40466ab275d7c116bbc3612a`; payload `055ef32f589d7ec941120d5bf8f60ea58ec23066ed3db6e9f4b36c2d0123ca60`.

The raw4 suite contains 12 semantic cases plus optimized/source-tree guards; the theta2 suite contains 10 semantic cases plus the same two guards. The fresh release-mutation run executed all 22 semantic cases against the production verifier, with exact diagnostics occurring before checksum gates, and completed 27/27 top-level obligations with zero survivors. The declared suite lacks a dedicated direction-reversal case; the separate fresh bounded attack above supplies that evidence. No declared raw4/theta2 composite semantic case remains merely inspected.

## Quartet algebra and mutations

Specification SHA-256 `d193983da3322c708767a398fbe4c0e96543275d7ed769a7447aea5e893fb563`; verifier SHA-256 `783cc522c8669eb1cd89928246b998ed09b222a9e9931d4c22d7fd03b5e05ec8`.

Fresh exact verifier: exit 0, 1.32 s, maximum RSS 66,863,104 bytes; output SHA-256 `a49d8d7c02cd349f3db0df8d54d4887afa5953bfb9f16317eb5cbd43225984d1`; payload `20afb6da3e9acaf15db941cad782b8545893be260413119acc3bafdb0195a7ba`. It derived six canonical formulas, all 288 leaf/character transports, all 21 displayed-set pairs, spectrum `(1,s,g,s)`, and C/T equality.

Fresh mutation suite: 8/8 intended diagnostics (G/T spectrum swap, wrong F coordinate, wrong J coefficient, wrong character order, wrong coordinate dictionary, wrong `D_plus`, reverted printed formula, optimized Python). Exit 0, 3.62 s, maximum RSS 92,897,280 bytes; report SHA-256 `a1bf423637775b295fb1d6554401352834c59eab326798f7db4753a3855a4a9e`; payload `4f7bef166b12b41058777cf17eb172605f1d50184fb449f4dd61565c6e48fc2e`.

Unlike the deficient wrappers, this suite requires the exact per-case diagnostic and absence of a failed-mutation certificate.

## Symbolic rank and polynomial audit

Key code:

- `work/rank_upper_certificates/syzygy_upper.py`, SHA-256 `e91af12df4e82d9cd305f1f207c056fb28b083fe31a42c81a89103871fdd853e`.
- `work/rank_upper_certificates/verify_rank_upper_certificates.py`, SHA-256 `bd51596fe6bc5ddc8a4c6a185bda989479e3f7e736b0e80d9ea33ac7d1acf93e`.
- Coverage SHA-256 `c52c5730494eb894360c17b6e54ae5c260fca3cddb8702d5c796750c7df874bc`.
- Stored replay SHA-256 `c967917601f64803c96c1ba11cabc5fd3ea8d6021f9e55441c4210d9b886793d`.

The upper-bound mechanism is coefficientwise: it builds an exact integer matrix for `J_f V=0`, computes exact ranks, and derives a globally valid polynomial-kernel dimension. No sampled Jacobian establishes an upper bound. Coverage declares 3,515 base ansatz descriptors plus 864 exceptional transported descriptors, all 4,379 exactly once, with 75 exceptional representatives.

The stored seven-case rank mutation report includes omitted/duplicated coverage, altered syzygy, reassigned representative, broken port transport, false upper claim, and sampled-rank substitution. It calls verifier helper functions rather than mutating a full artifact and invoking the production verifier; several cases are manufactured direct comparisons. It is useful unit evidence, not an independent production mutation replay.

Direct higher-degree verifier `package/referee/k2p_offline_sweep_portable/proofs/verify_four_port_direct_residual_closure.py` (SHA-256 `ffa53179d7e94fdbadb05ef66a6030bb4780110504c766d030eaad907a52d6da`) performs exact sparse polynomial substitution and strict rational witnesses. The fresh full run completed both structural and full direct36 replays, and the fresh release-mutation suite rejected reassigned cubic, quartic, and quintic certificates at the direct-overlay gate. I did not independently reimplement all 36 higher-degree polynomial substitutions, so the production evidence is PASS while alternate-engine independence remains **UNVERIFIED**.

## Mutation coverage matrix

| Requested corruption | Freshly executed here | Stored/code inspected | Status/comment |
|---|---|---|---|
| Omitted/duplicated raw row | Yes through fresh release/composite suites | Raw ledger and composite exact-marker suites | **PASS**; independent dense-ID audit also detects both |
| Wrong port permutation | Yes | Composite | **PASS**, production diagnostic before checksum |
| Alternate/wrong parent | Yes | Composite and fresh restoration suite | **PASS**; raw4 alternate valid parent and restoration wrong-parent attacks rejected |
| Source-target reversal | Yes | Composite and parameter suite | **PASS** in production composite; parameter mutation itself is invalid evidence |
| Parent-order reversal/complement removed or injected | Parameter suite fresh | Full verifier code | Local schema catches six related cases; no full mutant invocation, so **HOLD** |
| Omitted inherited child | Yes | Composite | **PASS**, production theta2 diagnostic |
| Incorrect classifier precedence | Yes | Fresh probe suite | **PASS**, `CORRECTED_PROBE_REPLAY_FAIL:classifier order` |
| False canonical triangle / selected-triangle mismatch | Yes, twice | Canonicalizer | Correct venv run **PASS** semantically; wrapper also falsely PASSes dependency crashes |
| Global false merge/split | No | Canonicalizer certificate | **UNVERIFIED** outside 4,012 raw4 relation presentations |
| Altered `D_plus` declaration | Yes | Quartet | **PASS** exact diagnostic; independent boundary audit also passes |
| Invalid physical witness | Yes | Fresh restoration suite | Rejected at the package-level restoration manifest-transport gate; wrapper still lacks exact diagnostic binding |
| Sampled rank substituted for symbolic upper | No fresh production mutant | Rank helper/code | Symbolic mechanism is live; mutation is helper-level |
| Reassigned quadratic/cubic/quartic/quintic | Yes through fresh release/restoration runs | Composite/direct/restoration evidence | **PASS** production gates; independent all-body replay remains unperformed |
| Missing child/wrong parent/cycle | Yes for composite/restoration; cycle full replay | Composite/restoration/release | **PASS** production evidence |
| Broken restriction/transport | Yes | Fresh composite direction and fresh probe/restoration suites | **PASS** for exercised production gates; parameter four-case dedicated evidence remains deficient |
| Missing probe site | Yes | Fresh probe suite and independent finite coverage | **PASS**, root-suppressed site/profile gate |
| Invented triangle | Yes | Fresh canonicalizer and fresh probe global-triangle attacks | **PASS** for exercised guards; global all-family orbit independence remains open |
| Optimized Python | Yes | Quartet, restoration, probe, release harness | **PASS** for current authoritative paths; legacy provenance suites are not promotion authority |
| Stale/malformed replay report, wrong lock/commit | Yes | Telemetry unit suite | **PASS**, 9/9 |
| Missing dependency | Yes | Canonicalizer mutation suite | **FAIL**: unrelated import error becomes mutation PASS |
| Missing TeX/PDF input | No | Outside this bounded computational subreview | Root reproducibility/build track |

## Release harness and telemetry

Environment used for qualified symbolic runs: macOS 26.5.2 arm64, Apple M1 Pro, 16 GiB RAM, Python 3.14.6, NetworkX 3.5, SymPy 1.14.0. Homebrew Python 3.14.6 intentionally lacks NetworkX and exposed Finding 1.

Final release verifier SHA-256 `23c45b6796f18fffa942c7efb9d8d9eb281658f9f41fde2866ef078007826a4f`; release library SHA-256 `a723eac8b897c93d92b0098edab484b56385a82d28bc3cd421d7e75eeba40472`.

Static inspection confirms:

- Every ordinary child command must exit 0 and emit all declared terminal markers.
- Expected-failure layers require nonzero exit and exact required markers.
- Full mode regenerates canonicalizer, parameter transports, rank upper replay, raw4 overlay/raw ledger, direct36, theta2, corrected probe, and independent probe graph audit in temporary locations, comparing resulting bytes or logical JSON.
- Optimized mode is forbidden at the final entry point.
- The locked source fingerprint is compared before and after all children.
- Any release blocker makes the report `BLOCKED` and returns nonzero.

Fresh qualified full command, run in the disposable execution copy:

```text
.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --full
```

Observed exit 0; **40/40 layers PASS**; promotion ready; zero blockers; optimized mode false. Outer wall time 5,317.14 s; internal elapsed time 5,316.723762 s; maximum RSS 2,548,006,912 bytes. Stdout SHA-256 `563e77a80c335284ac068c38bbdb4c1f94fde3bcad85636ee1ad61163b5a1a2b`; stderr SHA-256 `c4ba9f170086627b0d981dd79107dce4e4d893b22f70395dffac9d5b6bc78661`; parsed report SHA-256 `8ed37521c82830dc1f642d55faf1f5838fcd0ccbd0b90646e0eed184e65532ca`. Runtime was Python 3.14.6, NetworkX 3.5, SymPy 1.14.0 on macOS arm64.

The 40 layers included full canonicalizer completeness; full graph-derived parameter-transport producer comparison; exact rank full replay; raw4 overlay/raw-ledger regeneration; direct36; theta2 regeneration; corrected-probe primitive regeneration, independent streaming replay, and site partition; and the independent probe primitive-graph audit. Every layer row in the parsed report has status PASS.

The separate fresh release-mutation command also completed 27/27 top-level mutation obligations with zero survivors in 971.54 s. It included 22 complete verifier-facing raw4/theta2 composite-ledger attacks, the eight quartet-semantic attacks, twelve quartet-terminal attacks, the two canonicalizer attacks, the ten parameter-transport report cases, omitted raw/rank attacks, direct cubic/quartic/quintic reassignments, corrected restoration/probe bindings, and historical-authority attacks. This strengthens the evidence that the frozen qualified package rejects these attacks, while Findings 1-3 remain valid critiques of what several nested wrappers actually require.

Fresh telemetry unit command:

```text
/usr/bin/time -l python3 -B proof_compression_submission/test_clean_full_replay_telemetry.py
```

9/9 tests passed; 4.62 s; maximum RSS 27,394,048 bytes. Captured stderr/time log SHA-256 `2bead2304336a9e6fd1cb61158f744cac170030935fb421e0cf1190963865a39`.

Stored clean full telemetry remains provenance evidence: telemetry SHA-256 `dc4bd8faafef195a1fd7879b2c8ac7197ebb56cf8fee46c799ab0415b1e3ec08`; referenced report SHA-256 `d26ce0841a50ebdc50a5e5d75a25ac2e12d9b647759051c8ceea29d803bd799e`; release lock SHA-256 `c319977f350923ab900a883235e32ec945d55a864338c14a08ce266ed3a1c78a`. It reports 40 layers, 5,428.67 s wall time, maximum RSS 2,548,498,432 bytes, commit `83821850e02bc6b6a0383dbc9d3d42ab24a261f5`. The separate fresh replay above, rather than this stored PASS, is the execution evidence used in the present status.

## Fresh execution ledger

| Command/purpose | Exit | Wall time | Max RSS | Output SHA-256 | Result |
|---|---:|---:|---:|---|---|
| `python3 -B tmp/fresh_census_audit.py --project isolated/... --output tmp/fresh_census_audit.json` | 0 | 51.79 s | 318,570,496 | `844646ca...` | PASS |
| `python3 -B tmp/k2p_domain_boundary_audit.py` | 0 | 0.07 s | 19,152,896 | `39e2101d...` | PASS |
| `.../.venv/bin/python -B verify_quartet_logic.py ... --output tmp/quartet_logic_fresh.json` | 0 | 1.32 s | 66,863,104 | `a49d8d7c...` | PASS |
| `.../.venv/bin/python -B test_quartet_semantics_mutations.py --output tmp/quartet_semantics_mutations_fresh.json` | 0 | 3.62 s | 92,897,280 | `a1bf4236...` | PASS, 8 exact diagnostics |
| `python3 -B run_parameter_transport_mutations.py --output tmp/parameter_transport_mutation_fresh.json` | 0 | 28.65 s | 40,501,248 | `893d1716...` | Wrapper PASS; evidence FAIL for 4/10 |
| Bounded four-case complete-ledger composite production probe | 0 | 85.23 s | not separately recorded | `1ea89890...` | PASS |
| Homebrew Python canonicalizer mutations without NetworkX | 0 | 0.20 s | 28,295,168 | `f4bf1d4e...` | **False PASS**, defect reproduced |
| Qualified venv canonicalizer mutations | 0 | 0.40 s | 50,413,568 | `10b8eeba...` | PASS, intended diagnostics |
| `python3 -B test_clean_full_replay_telemetry.py` | 0 | 4.62 s | 27,394,048 | time/log `2bead230...` | PASS, 9 tests |
| `.venv/bin/python -B verify_final_theorem_release.py --full` | 0 | 5,317.14 s | 2,548,006,912 | stdout `563e77a8...`; parsed report `8ed37521...` | PASS, 40/40 layers |
| `.venv/bin/python -B run_release_mutations.py` | 0 | 971.54 s | 1,423,196,160 | stdout `2aae993b...` | PASS, 27/27 obligations, zero survivors |
| `.venv/bin/python -B mutate_corrected_restoration_forest.py` | 0 | 33.61 s | 524,255,232 | report `e5b3763c...`; stdout `fea309ea...` | PASS, 13/13 nonzero rejections |
| `.venv/bin/python -B run_probe_coherence_mutations.py` | 0 | 168.20 s | 71,532,544 | report `4ba412df...`; stdout `36e9a565...` | PASS, 15/15 plus clean hash-seed replay |

## Principal code/artifact hash registry

| Role | Path | SHA-256 |
|---|---|---|
| Primitive graph/model/canonicalizer engine | `package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py` | `37e9b7910f7723c146a87ae2f60dfb62529b1a3e4866ccd72d65dc4efda923ad` |
| Raw producer | `work/raw_ledger_audit/generate_raw_ledger.py` | `91e58a4a9b9328448ae5e028e12b9550a16f1a6f1b4246afb156c1e1d7cb6d44` |
| Raw verifier | `work/raw_ledger_audit/verify_raw_ledger.py` | `745ece3309128b0b0a5bb824e9811be946c40bee744cd99ebdc7d709f714e371` |
| Canonicalizer auditor | `work/canonicalizer_completeness/canonicalizer_audit.py` | `3df120b4e5d36e1222fc5766346e18b79623debbdaa04236cabf5132415cf3e4` |
| Composite producer | `work/corrected_composite_ledgers/generate_corrected_composites.py` | `a117923e7b5cf90f0a13630fd21a6c454139f7e6e9c3c7bf84276229351a58ce` |
| Composite verifier | `work/corrected_composite_ledgers/verify_corrected_composites_independent.py` | `67ddf315b400a0a96f4a5901e6a340a158d9d4fd1111e8ee17193de5d78b5690` |
| Parameter transport producer | `work/canonicalizer_completeness/inheritance_transport/build_parameter_transport_certificate.py` | `a980f3c96206a1fcd8849676bfc54a773b512f2878e322d3b78ddf2a9e9cb9cb` |
| Parameter transport verifier | `work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py` | `01dbe90dfd4262e2982974a2425c33435d623ebc68e2e9751f8e258f17ead160` |
| Restoration producer | `work/restoration_sign_reclassification/build_corrected_restoration_forest.py` | `55e7196b840b98334327e81b2583ab2105a8107ee9be308781b41187c9c7de6d` |
| Restoration verifier | `work/restoration_sign_reclassification/verify_corrected_restoration_forest.py` | `e4cef28f156e1c300ed7b7cc48bb1a96f3a7686d92e2c748ec8dfa156d236f9e` |
| Probe producer | `work/probe_coherence_corrected/build_probe_coherence_corrected.py` | `f0176e1759771a01ffa3da9e8d2b8967fc9189d3f93b30c6d06554bba9a77ddf` |
| Probe verifier | `work/probe_coherence_corrected/verify_probe_coherence_corrected.py` | `3facc1b51c133aa953f4a0cba86782672c86e78990d72ef2fc2aaa16a6f2a1bd` |
| Rank symbolic core | `work/rank_upper_certificates/syzygy_upper.py` | `e91af12df4e82d9cd305f1f207c056fb28b083fe31a42c81a89103871fdd853e` |
| Rank verifier | `work/rank_upper_certificates/verify_rank_upper_certificates.py` | `bd51596fe6bc5ddc8a4c6a185bda989479e3f7e736b0e80d9ea33ac7d1acf93e` |
| Quartet verifier | `work/quartet_separation_closure/verify_quartet_logic.py` | `783cc522c8669eb1cd89928246b998ed09b222a9e9931d4c22d7fd03b5e05ec8` |
| Quartet terminal binder | `work/quartet_separation_closure/verify_quartet_terminal_bindings.py` | `b97cdf9ce0ce01a6d5ccd6843fb22b64a9b872e6dcae69de2adc9735da095b3b` |
| Final release verifier | `work/final_theorem_release/verify_final_theorem_release.py` | `23c45b6796f18fffa942c7efb9d8d9eb281658f9f41fde2866ef078007826a4f` |
| Final release semantics/registry | `work/final_theorem_release/release_common.py` | `a723eac8b897c93d92b0098edab484b56385a82d28bc3cd421d7e75eeba40472` |

## Remaining independent or out-of-track gates

1. A genuinely independent all-family graph-orbit merge/split audit, rather than a fresh replay of submitted atlas-based machinery.
2. An independently written all-row analytic classifier for every quartet/sign/rank/polynomial category.
3. An alternate symbolic engine for every one of the 4,379 rank descriptors and all 36 higher-degree direct polynomial bodies.
4. Complete disposable-ledger production-verifier attacks for the four parameter-transport cases currently represented only by changed-row hash inequality.
5. Exact diagnostic contracts for canonicalizer, restoration, and primary probe mutation wrappers.
6. TeX/PDF omission and bibliography/build mutations, which belong to the root reproducibility track and are reported separately.

## Required computational actions

1. Fix canonicalizer mutation diagnostics and binder as in Finding 1; add a clean baseline and an explicit missing-dependency attack.
2. Replace the parameter-transport hash-inequality proxy with complete disposable-ledger production-verifier attacks; bind exact diagnostics.
3. Add exact diagnostic contracts to restoration and probe mutation wrappers and release bindings; add a clean restoration baseline.
4. If an unqualified global claim of independent canonicalization is retained, add an all-family independent graph-orbit partition; otherwise narrow the evidence statement to the scopes actually audited.
5. Reseal mutation reports, release lock, source manifest, and replay telemetry after code changes. Mathematical article/PDF changes are unnecessary unless they presently claim stronger mutation independence than delivered.
