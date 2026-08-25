# Fresh computational-semantic referee audit (2026-08-25)

## Bottom line

**Computational classification code: PASS with an independence qualification.** I found no counterexample, surviving ledger corruption, false canonical merge, sampled rank substituted for a symbolic upper bound, broken restoration parent, or incoherent probe/parameter transport in the revised package. A fresh standard-library implementation rebuilt all 10,084 primitive source/target archetypes, checked their graph axioms, derived the three raw-direction universes, and independently reproduced every required census and frozen-ledger hash. Twelve real raw4 ledger corruptions were all rejected by the submitted independent verifier at the intended semantic invariant.

**Published mutation/release evidence: FAIL (reproducibility/computational-evidence blocking, not theorem-fatal).** `work/corrected_composite_ledgers/run_composite_mutations.py` does not perform the ledger mutations it claims. It compares altered Python dictionaries to their originals, implements omission and duplication as tautological arithmetic, and never gives a mutant ledger to `verify_corrected_composites_independent.py`. The final release layer incorrectly states that this producer executed every case in temporary copies. Higher-level corrected-universe and compression mutations alter summaries/certificates, not primitive ledger rows, so they do not repair this evidentiary defect.

The important distinction is:

- the underlying corrected-composite verifier was genuinely fail-closed in my attacks; but
- the submitted mutation report and the release claim about how it was produced are false descriptions of executed evidence.

This defect warrants **HOLD until the mutation runner/report and downstream seals are replaced**. It does not establish that the finite classification or theorem is false.

## Scope and independence

I treated all stored PASS reports as assertions. I inspected the primitive generator, raw generator, model-map implementation, slow and optimized canonicalizers, quartet closure, symbolic rank machinery, corrected composite producer/replayer, restoration forest, probe graph audit, parameter-transport producer/replayer, release verifier, release mutations, and compression mutations. I did not edit the submitted package and did not run the global full replay.

Fresh artifacts are confined to:

- `independent_checks/computation/independent_primitive_and_census.py`
- `independent_checks/computation/independent_primitive_and_census_report.json`
- `independent_checks/computation/composite_mutations/run_real_composite_mutations.py`
- `independent_checks/computation/composite_mutations/final_cases/`

The primitive/census implementation imports no submitted module and no graph library. It uses direct incidence lists, weak compositions, explicit repair words, a standard-library DAG test, binary-degree checks, and a direct tree-child predicate. It parses every authoritative ledger row, rather than consulting the package's reported totals.

## Finding 1 — the corrected-composite mutation suite is not a mutation suite

**Classification:** reproducibility-blocking and computational-evidence-blocking; not theorem-fatal.

**Minimal reproducer / derivation:** read `work/corrected_composite_ledgers/run_composite_mutations.py`.

- Lines 41–62 define `rejects_reference_mutation`. It returns true whenever a mutated field differs from the original exemplar. This is an in-memory inequality predicate, not the production verifier.
- Lines 65–68 clone one row, alter it, and pass the two dictionaries to that comparison predicate. No ledger is written and no verifier is invoked.
- Lines 91–93 report omission and duplication via the tautologies `TOTALS[family] - 1 != TOTALS[family]` and `len({0, 0}) != 2`. Neither case removes or duplicates a record.
- Lines 95–100 alter only an exemplar dictionary. The verifier named on line 82 is used only by the optimized-Python test at lines 102–106.
- Lines 108–113 append a byte to a scratch copy of the *summary* and merely observe that its SHA changes.
- Lines 115–145 similarly compare altered parent, transport, and degree/certificate fields to their originals; no altered primitive ledger reaches a verifier.

The suite nevertheless emits PASS reports claiming 14/14 raw4 and 12/12 theta2 mutations. The release layer compounds the issue:

- `work/final_theorem_release/run_release_mutations.py:336-369` says in its docstring that the producer “already executes all cases in independent temporary copies.” It does not.
- That function calls `validate_corrected_finite_universe()`, reads the two frozen mutation payload hashes, appends a synthetic `status="REJECTED"` row, and prints a rejection marker. It does not execute `run_composite_mutations.py` or mutate a ledger.

No higher-level test genuinely covers these primitive fields:

- `work/final_theorem_release/run_corrected_universe_mutations.py:43-77` changes counts and artifact digests in the unified certificate. Lines 104–138 do invoke the unified verifier, but only against the altered certificate; the underlying ledgers are pristine.
- `proof_compression_submission/run_compression_mutations.py:52-101` changes compressed summary objects. Its verifier is explicitly called with `verify_files=False` at lines 134–138, so it is not a primitive-ledger mutation.

The defect is thus not an “unrelated checksum rejection” issue; the advertised mutant artifacts never exist.

**Effect:** the frozen mutation reports and the final release mutation row cannot support claims that omission, duplication, false rank, wrong parent/transport, or degree reassignment attacks were executed against primitive ledgers. Hash agreement proves only that these inadequate reports were sealed.

**Smallest adequate remedy:** rewrite `run_composite_mutations.py` so each case creates a real disposable ledger (and, where appropriate, a coherently resealed disposable summary/registry), invokes `verify_corrected_composites_independent.py`, requires a nonzero exit, and requires the intended semantic diagnostic rather than a generic SHA mismatch. Replace both mutation reports, correct the release prose, rerun the release mutation layer, and reseal every manifest/crosswalk/archive/PDF appendix that binds the changed bytes.

## Real attacks against the actual composite verifier

I implemented the missing test mechanism independently. Each case rewrote the complete raw4 gzip ledger in scratch, preserved canonical JSONL/gzip encoding, changed the smallest relevant record(s), and ran:

```text
<project>/.venv/bin/python -B
  <project>/work/corrected_composite_ledgers/verify_corrected_composites_independent.py
  --family raw4
  --ledger <scratch-mutant.jsonl.gz>
  --summary <project>/work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_summary.json
  --report <scratch-report.json>
  --skip-heavy-full-map
```

The authoritative summary was opened read-only. All ledgers and requested reports were under `independent_checks/computation`. Results:

| Real mutation | Actual diagnostic | Intended semantic rejection? |
|---|---|---:|
| omit raw ID 0 | `RAW_ID_ORDER:0` | yes |
| duplicate raw ID 0 | `RAW_ID_ORDER:1` | yes |
| wrong physical port permutation at raw 0 | `PORT_PERMUTATION:0` | yes |
| substitute a different independently valid quartet witness | `QUARTET_WITNESS:0` | yes |
| make a rank row's source rank equal its target rank | `RAW4_RANK_EVIDENCE:97` | yes |
| substitute a different valid direct certificate | `RAW4_TERMINAL_EVIDENCE:1849` | yes |
| reassign a quadratic row to a valid cubic binding | `RAW4_TERMINAL_EVIDENCE:1849` | yes |
| reassign a cubic row to a valid quartic binding | `RAW4_TERMINAL_EVIDENCE:357409` | yes |
| reassign a quartic row to a valid quintic binding | `RAW4_TERMINAL_EVIDENCE:154800` | yes |
| reassign a quintic row to a valid quadratic binding | `RAW4_TERMINAL_EVIDENCE:69457` | yes |
| wrong restoration parent | `RAW4_RESTORATION_EVIDENCE:2185` | yes |
| wrong restoration presentation transport | `RAW4_RESTORATION_EVIDENCE:2185` | yes |

All 12 exited 1 and were rejected before an output replay report was created. Crucially, each failed at the intended semantic marker, not at a ledger SHA mismatch. The complete suite took 413.97 s wall time under concurrent load; `/usr/bin/time -l` reported maximum RSS 1,104,183,296 bytes. Individual actual-verifier times and stdout hashes are in the report.

Artifacts:

- driver SHA-256: `7ca72d10eacf8f2d25d931db855b7e36430356cbbd85ae548f6350723c790378`
- report SHA-256: `8bf09b30f9be51ebb48b8523cafe4eae767f0972f9c32cd4682c88d23c2d4086`
- report payload SHA-256: `5d7f477a53b75d9b8debdd0561dad2fd34ebf363402b58b3bc45c4f5c6399039`

This is affirmative evidence that the actual raw4 verifier is not blind to the tested corruptions. It does not rehabilitate the submitted mutation reports, and it does not by itself test every theta2 field.

## Independent primitive universe and census

### Primitive enumeration

The submitted atlas begins with five primitive directed core encodings, not topology names or a rooted tree/sunlet oracle (`package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py:9-41`). Its generator constructs the graph from the incidence list and ordered subdivision words (`:65-109`), builds source supports (`:112-137`), and builds targets from every sink mask, weak composition, and repair choice (`:140-181`).

My independent implementation copied the mathematical incidence lists, not the submitted functions, and for every record checked:

- no duplicate directed edge survives the subdivision encoding;
- the root has degree `(0,2)`, tree vertices `(1,2)`, reticulations `(2,1)`, and leaves `(1,0)`;
- the directed graph is acyclic by an independent Kahn traversal; and
- every nonleaf has a tree or leaf child.

It enumerated these targets by core:

| Boundary convention | cycle | theta0 | theta1 | theta2 | theta3 | total |
|---|---:|---:|---:|---:|---:|---:|
| `k=3`, incoming selected | 5 | 40 | 40 | 136 | 68 | 289 |
| `k=3`, incoming marginalized | 7 | 100 | 100 | 416 | 208 | 831 |
| `k=4`, incoming selected | 7 | 100 | 100 | 416 | 208 | 831 |
| `k=4`, incoming marginalized | 9 | 210 | 210 | 1,036 | 518 | 1,983 |
| `k=5`, incoming selected | 9 | 210 | 210 | 1,036 | 518 | 1,983 |
| `k=5`, incoming marginalized | 11 | 392 | 392 | 2,240 | 1,120 | 4,155 |

The independent closed form for one core with `m` arc bins, `r` repair choices, `h` sinks, and `o` outgoing real boundaries was

```text
r * sum_{j=0}^{min(h,o)} binom(h,j) binom(o-j+m-1,m-1).
```

Thus it independently derives `C(4,1)=831`, `C(4,0)=C(5,1)=1983`, and `C(5,0)=4155`, rather than reading those constants from a summary.

The source-support counts were six raw4 sources (two each for theta0, theta1, theta3), four five-port theta2 sources, and two cycle sources. Including all port permutations gives exactly:

- `6 * 2,814 * 4! = 405,216` raw4 directions;
- `4 * 6,138 * 5! = 2,946,240` theta2 directions; and
- `2 * 1,120 * 3! = 13,440` cycle directions.

Across the three layers, the independent graph builder checked 10,084 primitive source/target archetypes.

### Streamed authoritative censuses

Every row of the authoritative composite, cycle, and probe ledgers was independently JSON-parsed. Raw IDs were required to equal the zero-based stream ordinal. Gzip SHA-256, uncompressed SHA-256/byte counts where declared, partitions, and unique transport/restriction IDs were recomputed.

Results matched exactly:

- raw4: 405,216 = 360,408 quartet + 16,974 whole-map sign + 23,822 rank + 1,472 direct + 2,540 restoration;
- theta2: 2,946,240 = 2,942,592 quartet + 2,528 whole-map sign + 800 rank + 240 quadratic + 80 isomorphism;
- cycle base: 13,440 = 7,452 whole-map sign + 5,964 restoration + 8 isomorphism + 16 triangle;
- cycle full: 536,364 = 535,920 quartet + 300 whole-map sign + 132 quadratic + 12 isomorphism;
- one-port: 29,964 = 27,758 quartet + 99 whole-map sign + 1,915 isomorphism + 192 triangle;
- two-port: 544,571 = 511,266 quartet + 576 whole-map sign + 30,969 isomorphism + 1,760 triangle;
- exact graph transports: 67,741 rows and 67,741 unique IDs; and
- parent restrictions: 4,379 rows and 4,379 unique IDs.

The 934 terminal certificate classes independently split as 839 quadratics, 36 direct higher-degree classes, four hard bindings, 20 isomorphisms, and 35 triangles. The 36 split as two cubics, 12 quartics, and 22 quintics. Presentation multiplicities produce the stated 1,472 raw direct terminals.

The restoration forest was not accepted from its census object. I checked all 36,568 first rows against their row-hash list, all 256 second rows against their row-hash list, each second-row parent index/hash/root ID, and the continuation-parent set. The derived result is 997 canonical parents, 2,540 member roots, 36,824 edges, 36,792 leaves, depth two, with the printed proof partitions. Stored cycle/missing/unresolved counts are all zero.

For the 176 probe anchors, I recomputed the site count `2k+3r-3` from each source and target profile, checked it against every listed site transport, and summed 2,206 source and 2,206 target sites. Site types reproduced 682 core-unheaded, 720 pendant, 628 reticulation-incoming, and 176 root-suppressed sites on each side.

Independent census execution:

```text
/usr/bin/time -l python3 -B independent_checks/computation/independent_primitive_and_census.py \
  --project isolated/k2p_principal_d_plus_submission_referee \
  --output independent_checks/computation/independent_primitive_and_census_report.json
```

- exit: 0
- wall: 26.59 s (`elapsed_seconds` inside report 26.539060)
- maximum RSS: 159,891,456 bytes
- script SHA-256: `f6ad6a8161fb8f8cea41fb187180e6947a72960b21b13ce66fca83f71f1c19df`
- report SHA-256: `7fe83d590f90cdf03dc0c88c7eff72902b040fb9019b825f254538a50cd1613d`
- report payload SHA-256: `33d20ead0ee37d5ffab23f05005d645f977271d1cc2762be71b3d50e313b692a`

## Code-to-claim audit

### Corrected quartet binding — PASS

The revised source consistently declares Fourier order `(0,C,G,T)` and K2P spectrum `(1,s,g,s)` (`proof_compression_submission/article/main.tex:303-314`). The corrected quartet formulas and pullback table at `main.tex:417-450` use the C/T-equal sector; I found no remaining C/G confusion.

`work/quartet_separation_closure/verify_quartet_logic.py` derives tree Fourier coordinates directly from the Klein group law, verifies all six displayed formulas, all 288 leaf-permutation/global-C/T transports, all 21 unequal displayed-split-set pairs, and the strict `D_plus` signs. `verify_quartet_terminal_bindings.py` then streams every promoted quartet terminal across raw4, theta2, theta2 restoration, cycle, restoration, and probe layers (4,414,710 rows) and binds graph-derived split sets to the corrected literals. The new mutation suite covers wrong sector, formula, order, domain, manuscript binding, terminal substitution, and reversed source/target sign. This closes the prior convention defect.

The remaining independence qualification is explicit: the terminal replay takes graph-derived displayed split sets as inputs; its independent content is the split-set-to-literal algebra and exhaustive binding, not a second implementation of every upstream graph generator. My separate primitive enumeration reduces, but does not eliminate, that shared-input dependence.

### Primitive generator and raw-ID exhaustion — PASS

`generate_raw_ledger.py:56-94` forms the six sources, 831 selected targets, 1,983 marginalized targets, and 24 permutations before any classification lookup. Raw ID is the lexicographic source/target/permutation product. The independent graph/count implementation and dense stream checks found no omission or duplication.

The atlas encodes incoming and dummy roles in leaf metadata, stores the selected sink mask and repair index in `ModelRecord`, and relabels only integer physical labels. It does not dispatch on topology names to decide the classification. Target repair descriptors preserve ordered subdivision words and repair tags even when their selected mixed graph later becomes isomorphic to another presentation.

### Canonicalizer — PASS with shared-generator qualification

`work/canonicalizer_completeness/canonicalizer_audit.py` compares an explicit slow boundary-permutation orbit canonicalizer with the optimized canonicalizer on all 10,084 primitive archetypes. It separately reconstructs the labelled mixed-graph relation on all 4,012 relation-reachable raw4 presentations: 3,932 none, 54 ordinary triangle, and 26 isomorphism, with no disagreement.

This is strong evidence against an optimized false merge/split. It is not perfectly independent of primitive generation because both sides start from the same submitted graph objects. My separate incidence enumeration verifies the universe and graph axioms but does not reimplement the full isomorphism orbit search. I found no concrete collision or role loss.

Relevant frozen hashes inspected:

- atlas: `37e9b7910f7723c146a87ae2f60dfb62529b1a3e4866ccd72d65dc4efda923ad`
- canonicalizer audit payload: `4f3d241323d5079dec29bd738cae78a62fa98a26d33d8813121bd1ad50522207`

### K2P Fourier/model maps — PASS

The atlas compiles coordinates from zero-sum Klein assignments, reticulation switch choices, physical edge path classes, and C/T orbits (`k2p_atlas_core.py:199-337`; optimized descriptor compiler at `:466-527`). Sparse polynomial pullbacks and quadratics are built from those descriptors (`:621` onward). The printed quartet formulas now agree with this sector convention.

I found no coordinate reordering, hidden rooted oracle, or source/target reversal in the corrected composite producer. It regenerates the primitive source/target records and permutation, then applies the declared precedence: quartet, whole-map `T_i`, exact directed rank, and direct/restoration terminal. The independent verifier rebuilds the expected evidence row rather than accepting the row's category label.

### Symbolic rank certificates — PASS

`work/rank_upper_certificates/syzygy_upper.py` represents polynomial vector fields and verifies `J_f V=0` coefficientwise; exact independence is witnessed at a rational interior point. This is a symbolic generic upper bound, not sampled-point evidence. `generate_exception_syzygies.py` supplies exact log-field polynomial syzygies for the 75 exceptional orbits. `verify_rank_upper_certificates.py` and `work/raw_ledger_audit/rank_upper_binding.py` bind all 4,379 regenerated descriptors, check port transport, and require exact lower rank to match the symbolic upper rank.

The actual false-rank ledger mutation failed at `RAW4_RANK_EVIDENCE`, independently confirming that a locally plausible but false source/target rank binding is not accepted.

### Direct polynomial certificates — PASS at the binding layer

The registry has one semantic row per `(source_index,class_id)`, not one globally unique local class number. It binds exact quadratics, two cubics, 12 quartics, 22 quintics, four hard cases, isomorphisms, and ordinary triangles. The corrected composite verifier rejected substitutions using other *valid* registry bindings for every tested degree, so it does not merely check digest shape or registry membership.

This audit did not independently recompute every high-degree polynomial body. It inspected the exact sparse-pullback mechanism and checked the complete registry/census/binding layer. Separate mathematical/polynomial replay evidence should therefore remain identified as the source of algebraic validity, rather than this census alone.

### Restoration forest — PASS

The producer retains the fixed full pair, enumerates every physical child, and records source/target parent transports. Second-layer rows point to a unique first-layer continuation and preserve the same root ID. My direct parent-index/hash checks found no missing, duplicated, cyclic, or wrong-parent occurrence in the frozen forest. The independent counts and partitions are listed above.

### Probe machinery — PASS with an independence qualification

`work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit.py` reconstructs the 176 anchors from the frozen primitive input contract, independently enumerates sites and child graphs, computes quartet decks, exact mixed transports, parent restrictions, reversed marginals, and full-map pullbacks. It uses the atlas for primitive graph reconstruction/root-suppressed mixed conversion but has its own labelled graph isomorphism and polynomial compiler. It does not import the decisive expected probe classification or the production canonicalizer.

My stream/site audit confirmed all 29,964 one-port rows, 2,107 one-port equality survivors, 544,571 two-port rows, 32,729 two-port equality survivors, 67,741 unique exact transports, and 4,379 unique restrictions. No missing site or duplicate transport ID was found.

### Parameter transports — PASS in full-replay design; mutation evidence is weak

`work/canonicalizer_completeness/inheritance_transport/build_parameter_transport_certificate.py` derives paired physical-edge product actions from exact graph maps, records root-suppressed pairs, and complements an inheritance parameter only when the graph transport reverses the certified parent order. Ordinary-triangle local sections are kept separate from the exact external transport. It covers all 67,741 probe transports, 4,379 restriction records, 997 restoration parents, 2,540 roots, and 256 second edges.

The full parameter verifier deterministically reruns the producer and compares the regenerated ledgers/certificate byte-for-byte. The final release verifier uses only `--structural-only` in its structural phase (`verify_final_theorem_release.py` near line 605), but the full phase invokes the verifier without that flag (near line 1041). Thus full mode, when actually executed, closes semantic rederivation.

The dedicated parameter mutation report should nevertheless be described cautiously. `run_parameter_transport_mutations.py:119-124` treats a changed exact-row SHA as “rederived rejection” without installing the mutant ledger and running the full replayer. This resembles the composite evidentiary weakness, although here a separately executed full verifier really does regenerate the complete ledgers. I classify this as nonblocking misleading mutation evidence if a fresh full parameter replay is available; absent that replay it would become a computational-evidence gap.

### Release harness — mixed

The release verifier has genuine structural and full phases and, in full mode, invokes the expensive canonicalizer, parameter, raw-regeneration, rank, restoration, and probe checks. I did not run that global command in this subaudit.

The release mutation harness is fail-closed for many outer-certificate corruptions, but its corrected-composite row is only a frozen-report binding and its prose overstates execution. The outer lock therefore prevents silent artifact substitution; it does not transform an in-memory comparison into a semantic mutation replay.

## Certificate semantics and finite universes

The finite mathematical universes and classifiers are identifiable in code:

- **Raw4:** six graph-generated source supports × 2,814 graph-generated targets × 24 label permutations. Classifier order is displayed-quartet split mismatch, full-map `T_i` strict sign, exact source-lower/target-symbolic-upper rank, then exact direct/restoration terminal binding.
- **Theta2:** four theta2 source supports × 6,138 targets × 120 permutations. Classifier order is quartet, full-map sign, exact rank, quadratic, labelled isomorphism; dummy roots continue through the separate 56-root/864-child/832-leaf forest.
- **Cycle:** two cycle source supports × 1,120 targets × six permutations. Base survivors are exact no-dummy relations or fixed-full roots; all 536,364 physical children are then quartet/sign/quadratic/isomorphism terminals.
- **Restoration:** 997 canonical raw4 parents, expanded through every labelled physical insertion descriptor, with explicit parent and transport hashes and depth at most two.
- **Probes:** every site in the 176 exact physical anchors, then every ordered second site above the complete one-port equality universe; exact relations take precedence over quartet and original-full-map sign.

For each layer the evidence-binding semantics are explicit: graph-derived displayed split and strict side; coefficientwise whole-map pullback and strict physical witness; exact source lower minor plus globally symbolic target upper; registry-bound sparse polynomial identity; labelled mixed-graph mapping or ordinary-triangle witness; and fixed-parent restoration/probe transport.

## Execution notes

1. An early exploratory real-mutation driver used the system Python; its package verifier children failed because NetworkX was unavailable. Those failures were unrelated dependency errors, were discarded, and were not counted as mutation rejection. The final driver explicitly used the package's qualified `.venv/bin/python`.
2. The first development run of the independent census failed on an overstrong scratch assertion that local terminal `class_id` values were globally unique. Inspection showed the intended key is `(source_index,class_id)`. I corrected only the scratch implementation and reran; this was not a package defect.
3. Successful independent census: exit 0, 26.59 s, 159,891,456-byte maximum RSS.
4. Successful 12-case real composite mutations: exit 0 for the driver; every child verifier exited 1 at its intended marker; 413.97 s, 1,104,183,296-byte maximum RSS.

## Status by computational layer

| Layer | Status | Evidence type | Exact remaining qualification |
|---|---|---|---|
| Primitive graph universe and raw-ID exhaustion | PASS | independent computational + combinatorial | none found |
| Corrected quartet convention and terminal binding | PASS | exact symbolic + exhaustive computational | upstream graph split sets still share submitted encoding |
| Canonicalizer merge/split behavior | PASS | exhaustive dual-implementation computational | slow/fast audits share primitive graph objects |
| K2P coordinate/model-map implementation | PASS | code audit + exact quartet replay | not every high-degree pullback independently recomputed here |
| Symbolic rank upper/lower binding | PASS | exact symbolic computational | none found |
| Raw4 corrected-composite verifier | PASS | actual independent mutations + exhaustive replay design | theta2 real-ledger mutation not rerun here |
| Submitted corrected-composite mutation reports | FAIL | source-code derivation + real replacement attacks | producer never makes/invokes mutant ledgers |
| Cycle finite closure | PASS | independent census + inspected verifier | polynomial validity relies on exact package replay |
| Restoration forest | PASS | independent parent/hash/census attack | none found |
| Probe site/relation closure | PASS | independent census + separate graph audit | primitive reconstruction shares atlas |
| Parameter transport | PASS in full mode | exact graph-derived producer/rederive design | dedicated mutation report overstates its mechanism |
| Release mutation gate for composite layer | FAIL | source-code derivation | binds inadequate frozen reports and states they were real |

## Required actions

1. Replace `run_composite_mutations.py` with real disposable artifact mutations invoking the actual verifier and checking exact semantic diagnostics.
2. Regenerate both raw4 and theta2 mutation reports. Include at least omission, duplication, port reversal, valid-but-wrong quartet/rank/certificate substitution, wrong restoration parent, broken transport, and every direct polynomial degree.
3. Correct `run_release_mutations.py` so it either executes those suites or accurately labels them as frozen evidence; remove the false claim that the current producer already performed the cases.
4. Make the parameter-transport mutation report similarly explicit about which failures are structural comparisons and which come from a full regenerated replay.
5. Regenerate/reseal the final release lock, theorem-artifact crosswalk, source manifest, archive, and any printed appendix/PDF that binds changed report or source hashes.

## Research log checkpoint

**2026-08-25 — computational-semantic rereview complete.** Fresh primitive enumeration, full finite census, load-bearing source audit, and 12 actual composite-ledger attacks are complete. Best estimate of completion for this assigned computational audit: **100%**. Strongest result: no classification counterexample found and the actual raw4 verifier rejected every attack semantically. Exact blocker: the submitted mutation and release evidence falsely represents in-memory comparisons as executed disposable-ledger mutations.
