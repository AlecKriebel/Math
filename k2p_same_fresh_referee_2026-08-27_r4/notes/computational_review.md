# R4 independent computational/code audit (2026-08-27)

## Status

**Computational/reproducibility recommendation: HOLD.** I found no incorrect row, census, parent link, or current-file ambiguity in the clean package. However, a load-bearing independent verifier accepts a conflicting duplicate JSON member name in a compressed probe ledger after a valid layer reseal. This is a computational-completeness/reproducibility blocker under the requested fail-closed mutation standard. It is not a mathematical counterexample and does not establish that the clean stored classification is wrong.

The lead referee is running and will separately report the official `--quick`, `--full`, and release-mutation commands. Their outcomes are not duplicated or inferred here.

Source was read only at `isolated/k2p_principal_d_plus_submission_referee`; reviewer artifacts are under `independent_checks/computation`.

## Clean-package independent checks

The final independent structural script did not call a submitted classifier, replay driver, or release verifier. It used standard-library parsing and hashing, reconstructed raw coordinates, recomputed ordered roots and joins, and applied separate explicit graph predicates to graph objects produced by the primitive grammar.

Command:

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/time -l \
  /Users/alec/Documents/Math/k2p_level2_identifiability_closure/.venv/bin/python -B \
  independent_checks/computation/r4_independent_semantic_attack.py \
  --project isolated/k2p_principal_d_plus_submission_referee \
  --output independent_checks/computation/r4_independent_semantic_attack_result.json
```

Result: exit 0, 203.28 s wall, maximum RSS 3,253,387,264 bytes. Result file SHA-256 `35e56426ca918aa806e5cee66c91e4849168d4f587115562654e67ec66de730b`; internal payload SHA-256 `6c54197b205886afc87a284e77e838467dfb8bb4a6b3c520920249019bfe2a62`.

It independently confirmed:

- outer manifest payload and all 490 entries: 406 frozen plus 84 submission files, with combined root `5b7aa44ef814c3ba08eb6b6be86d9a11cf6595b236c5d33e3d7ecd4597b1aaba`;
- 233 current plain JSON documents (125,800,026 bytes) were well formed and had no repeated member names;
- 10,084 distinct primitive graph encodings with family counts `6/2814`, `4/6138`, and `2/1120`; every graph passed independent DAG, degree, label, dummy-role, and strong-tree-child predicates;
- raw4: 405,216 dense raw IDs partitioned as 360,408 quartet, 16,974 whole-map sign, 23,822 symbolic-rank, 1,472 direct-terminal, and 2,540 restoration-member rows;
- theta2: 2,946,240 dense raw IDs partitioned as 2,942,592 quartet, 2,528 whole-map sign, 800 symbolic-rank, 240 quadratic, and 80 isomorphism rows;
- every raw-composite row had canonical bytes, unique JSON names, correct source/target/permutation coordinates, no forbidden rooted token, and the declared ordered row/raw-ID roots;
- restoration: 997 canonical parents, 2,540 roots, 36,568 first children, 32 continuation parents, 256 second children, 36,824 edges, and 36,792 terminal leaves, with no duplicate row, wrong parent, cycle, or missing certificate link found;
- probes: 176 anchors; 2,206 source and target sites; 29,964 one-port rows; 2,107 equality parents; 544,571 two-port rows; 67,741 exact transports; and 4,379 restrictions, with no missing tested join or invented triangle witness;
- cycle promotion: 13,440 base rows and 536,364 children, all 5,964 obligations covered, with the printed exact terminal partitions and no wrong base/root link.

All compressed JSONL rows consumed by these raw-composite, probe, and cycle checks were parsed with a duplicate-aware decoder and required to equal their canonical serialization. Thus the finding below concerns verifier behavior under mutation, not an ambiguity observed in the current files.

## Finding 1 — compressed JSONL duplicate names are accepted after layer reseal

**Classification:** computational-completeness/reproducibility blocking; theorem not falsified.

The new duplicate-name defense is real but incomplete:

- `proof_compression_submission/crosswalk/build_revised_referee_bundle.py:91-111` has a recursive duplicate-aware JSON parser, but `validate_json_member` invokes it only when the final suffix is `.json`;
- `proof_compression_submission/crosswalk/check_revised_referee_bundle.py:108-129` independently implements the same protection, but likewise restricts it to `.json`;
- `work/probe_coherence_corrected/verify_probe_coherence_corrected.py:70-76` reads load-bearing `.jsonl.gz` rows with default `json.loads(line)` and does not compare the raw line with `canonical_bytes(row)`.

A benign disposable minimal reproducer is preserved at [r4_probe_duplicate_jsonl_attack.py](../independent_checks/computation/r4_probe_duplicate_jsonl_attack.py), with result [r4_probe_duplicate_jsonl_attack_result.json](../independent_checks/computation/r4_probe_duplicate_jsonl_attack_result.json). It placed a conflicting duplicate name in one probe row while preserving the later effective value, updated the advertised compressed-file hash, and made a valid probe-certificate logical reseal. The published independent probe verifier (SHA-256 `3facc1b51c133aa953f4a0cba86782672c86e78990d72ef2fc2aaa16a6f2a1bd`) returned exit 0 and printed `status: PASS`.

Attack execution: 17.05 s wall, maximum RSS 70,025,216 bytes. Result file SHA-256 `0b14d7dde85e323ed5ae4271e75f5f6f68d38a59f90e3c78931d828f552c7732`; internal payload SHA-256 `6a47dd00ced86fe0b6f2c51a42869cbc7c6d1ebd61707f7594dd266d2967cf79`. The original one-port ledger SHA-256 was `d5fa13d38731bff2403eeb4e4d9e139566c4983b09d30553c6260eaac64c5c90`; the disposable mutant was `3ee36f4ee9b77ac1880b0ac8e114df218ce59fe44883511cdbd17769085fcb72`; the valid mutated certificate payload seal was `3a869278dfdeaec01aa30e27724728ac82466886b5442fe1ea4f782b304aea94`.

Effect: a malformed, semantically ambiguous compressed ledger can receive PASS from the verifier intended to be an independent replay once its own layer hash is coherently resealed. An unchanged outer lock would still reject it by checksum, but that is the unrelated rejection mechanism the review protocol explicitly excludes for semantic mutation qualification. The present clean ledger is canonical and passed the separate duplicate-aware scan.

Smallest adequate remedy:

1. Use a recursive duplicate-aware decoder for every `.jsonl.gz` line and every `.json.gz` document.
2. For canonical JSONL formats, require the decompressed line bytes to equal the declared canonical serialization plus newline.
3. Extend both outer bundle scanners to inspect `.jsonl.gz` and `.json.gz`, with decompression limits and exact diagnostics.
4. Add fully layer-resealed same-valued and conflicting duplicate-name mutations to the probe suite (and preferably a shared format mutation suite), requiring rejection for duplicate/canonicality rather than a stale checksum.

Because the verifier, mutation report, release lock, theorem-artifact crosswalk, outer manifests, telemetry/source bindings, and distributed archive hashes are all frozen, the repair requires downstream regeneration and resealing.

## Prior R3 findings that are now repaired

The plain-JSON duplicate-name issue is substantively repaired. The producer and checker use separately written recursive duplicate-aware decoders, and `test_crosswalk_bundle_mutations.py` makes fully outer-resealed same-valued and conflicting duplicate-name mutations. Fresh focused execution returned exit 0 in 24.65 s with 33/33 mutations rejected; payload SHA-256 `62a056e21c8a514fe2e7e96ab952464fcb0a1489d785ccde8ff390e5f5006fe2`.

The stale printed authority hash issue is also repaired. `audit_article_sources.py` now parses exactly eight metadata rows and eighteen frozen-anchor rows, checks uniqueness/inventory/kind/path/current bytes, and the prior composite hash is corrected to the actual `96e30bae…`. Fresh audit: exit 0 in 0.17 s, 26/26 rows, payload SHA-256 `7fbb73104b5868e0ce786129575f5e054b2ce1f7967c47d7042586d01ec6a0ed`. Its focused stale/missing/duplicate/relabel mutation suite returned exit 0 with 9/9 intended rejections and payload SHA-256 `eb129858ed58ff1a645f79a5a8a56ae8b0f177dc7fb8c38c83f1eb6a1dd0d347`.

## Secondary nonblocking release-contract mismatch

`work/final_theorem_release/README.md:182` says every entry point rejects `python -O`, while the documented portable qualification entry point `package/referee/k2p_offline_sweep_portable/verify_package.py:9-63` has no such guard. Invoking its skip-heavy qualification under `-O` returned exit 0 and `K2P_OFFLINE_SWEEP_PACKAGE_PASS` in 7.74 s. Its child commands are relaunched without `-O`, so I did not establish weakened clean-result semantics; this is a documentation/QA defect, secondary to Finding 1. Add an explicit entry guard and mutation, then reseal the affected portable/release metadata.

## Bottom line

The clean finite ledgers survived broad independent census, coordinate, canonicality, parent, transport, and triangle checks, and both specific R3 fixes are present for their tested plain-JSON/printed-hash scope. Nevertheless, the compressed-ledger fail-open is exact and reproducible at a load-bearing layer. I recommend HOLD until that parser/canonicality gap is fixed, directly mutation-tested, and the dependent package is resealed.
