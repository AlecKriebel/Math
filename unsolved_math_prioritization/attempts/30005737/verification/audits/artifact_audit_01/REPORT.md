# Independent artifact audit of PR 894 / problem 30005737

Audit completed 2026-10-16 UTC against eligible head 401f86e018e8cc5075e37a29bae9350eb9f89c36. This is validation of the original 18-file packet. Original author effort remains **1/5**. No original proof, checker, candidate archive, Git state, or remote object was changed.

## Decision

**Original artifact integrity and finite-diagnostic reproducibility: accepted under the explicitly controlled runtime used here.** The original normal and genuinely optimized checker processes both returned 0, emitted exactly the frozen 966 bytes, and emitted no stderr. The original publication verifier returned 0 in both process modes, with the same 271-byte output. The original nine-member archive is byte-preserved and its members exactly match the frozen authored payload.

**Hostile-environment validation: insufficient.** A controlled Python startup hook made the unchanged original packet report success without executing the algebra checker. Isolating the verifier's parent process does not isolate the child processes it launches. A separate hostile-optimization test made both purported normal/optimized children actually use optimization level 2.

**Mathematical disposition: this artifact audit supplies no new global proof acceptance or rejection.** The 2,896 conditions establish example-specific algebra consistency, as detailed below. They do not establish the global theorem. No current-priority or broad literature conclusion was investigated. The complete native pair was authenticated and its exact target was read; its native status is open, while the original publication separately claims solved. Those are provenance/status observations, not a resolution of that discrepancy by this artifact audit.

## Authentication and preservation

The external SOURCE_MANIFEST.json was hashed before its contents were trusted or any original checker code was read/executed:

- 4,654 bytes; SHA-256 1d677ef16697e1e294f9f86800c10fe3189270cf2d9771a75d7c4e64954c0d1c, exactly the parent-supplied pin.
- All 18 exported files matched its byte counts, SHA-256 values, and recomputed Git blob identities: 91,564 bytes total. Every exported source was a regular nonsymlink file; the supplied Git modes are 100644.
- Complete private canonical pair: 3,524 bytes; SHA-256 b27d5dbb0f92c0ab330bf44891ec4467f7d8c593cef610196cbd82d4cc6d5298. The entire pair and ROOT_NATIVE_RECEIPT.json were read. No raw native corpus is included in the safe output.
- The root receipt's observed identity is recorded in NATIVE_RECEIPT_METADATA.json; no externally supplied hash for that receipt was available, so it is not independently authenticated merely by recording its hash.
- Final independent rereads confirmed all 18 original source files and the restored private packet still match their original external pins. FINAL_PRESERVATION.json records this after all supplemental tests.

Both complete actual Python files and all actual manifests were read before original-code execution. Copies in ORIGINAL_CODE are exact original bytes:

| Original code | Bytes | SHA-256 |
|---|---:|---|
| verify_publication.py | 3,300 | 8e9fba86534cfb75167f9b47a24206d6ca2e03ada94c91725b9023dd026e125b |
| authored/check_algebra.py | 8,097 | c927b95210e0ce19144f0dddab2e1e18fca2520c42d94a7de1cfa00a67593446 |

AUTHENTICATION.json covers every original member; it is an audit observation anchored to the external manifest, not a proof of mathematical truth.

## Actual execution and receipts

The existing Homebrew CPython 3.14.6 interpreter was used with its standard library. No packages or runtimes were installed. Primary direct runs used a minimal environment and the flags -I -S -B, adding -O for genuine optimization. FLAGS_NORMAL.json and FLAGS_OPTIMIZED.json record optimize=0 and optimize=1, respectively, and __debug__ true and false. Both original Python sources implement their guards through explicit RuntimeError exceptions, not assert statements.

| Actual primary process | UTC start | UTC end | Return | stdout bytes | stdout SHA-256 |
|---|---|---|---:|---:|---|
| Original checker, normal | 07:07:44.717293 | 07:07:45.135110 | 0 | 966 | 2a0062610f5116c92c3689cbb2d12747260d0f42664a277cbb41aee3424046ff |
| Original checker, optimized | 07:07:46.056283 | 07:07:46.468347 | 0 | 966 | 2a0062610f5116c92c3689cbb2d12747260d0f42664a277cbb41aee3424046ff |
| Original verifier, normal | 07:07:45.162900 | 07:07:46.055385 | 0 | 271 | db9f193a84e264810bfafd0c02c0edfc8a654d2033decf0920120aa0c3e1769c |
| Original verifier, optimized | 07:07:46.494829 | 07:07:47.396009 | 0 | 271 | db9f193a84e264810bfafd0c02c0edfc8a654d2033decf0920120aa0c3e1769c |

All four stderr streams are empty, SHA-256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855. Exact positive stdout is in ORIGINAL_STDOUT; these files were copied from actual process streams, not reconstructed JSON.

There are 61 recorded test processes, 58 outcome observations, 32 accepted observations and 26 intentional rejections. Three processes are flag/condition-attribution probes rather than outcome tests. Every subprocess's actual start/end/return code and raw stdout/stderr identities were persisted before checking its outcome. RECEIPT_VALIDATION.json independently confirms all 122 retained raw streams match their receipts. Raw stderr and working copies stay under private_tmp and are excluded from SAFE_MANIFEST.json because they can expose local paths.

Two audit drivers returned 0. The first driver's stderr contains the expected zipfile duplicate-member warning from constructing a negative control; that warning is retained. It was not emitted by the pristine verifier or checker.

## Original archive inventory

AUTHOR_CANDIDATE.zip is 15,158 bytes, SHA-256 eefe13f2f40137a39a248bd0fbab4421e83db3e1429ca44e74695db8449741ef. It has exactly these nine regular Unix-mode 100644 members:

| Member | Uncompressed bytes |
|---|---:|
| CHECKS.md | 2,189 |
| CHECK_RESULTS.json | 966 |
| MANIFEST.json | 1,287 |
| PROOF.md | 10,996 |
| READINESS.md | 3,297 |
| README.md | 1,647 |
| SOURCES.md | 4,483 |
| SOURCE_HASHES.json | 1,342 |
| check_algebra.py | 8,097 |

All nine decompressed members are byte-identical to their corresponding authenticated authored files. Neither audit is in the archive. Every stored member date is [2026,10,7,17,22,0]; ZIP timestamps carry no timezone, so the archive alone does not authenticate the original research log's UTC interpretation. ZIP_INVENTORY.json records all exact central records and local headers as base64, raw central names, member hashes and sizes, compressed-data hashes, CRCs, flags, attributes, versions, extras/comments, offsets, and exact EOCD/trailing bytes. The complete original archive remains unchanged in the source and final private packet; the inventory does not regenerate or normalize it.

## What 2,896 means

COUNT is the number of calls to require during one main invocation, not the number of independent mathematical facts. CONDITION_ATTRIBUTION.json was obtained by instrumenting the original require at runtime without changing its source bytes. It records 49 message categories:

| Counted category | Calls |
|---|---:|
| SL2 determinant preconditions and det Ad checks | 1,253 = 822 + 431 |
| PA1, PA2, PA3, source Jacobi on basis inputs | 1,354 = 88 + 422 + 422 + 422 |
| Explicit j1/j2 homomorphism checks | 126 |
| Triangular/mixed covariance and modular/constant determinant checks | 136 |
| Remaining rank, trace, boundary, and invalid-R conditions | 27 |
| Total | 2,896 |

A require may check an entire list of 17 values or a conjunction of several equalities. Many helper calls repeat the same determinant preconditions. PA1 is true by the construction of source at original checker line 92, so those 88 checks are algebraic implementation consistency rather than an independent restriction on a proposed post-Lie product.

The exact rational computations verify the displayed products on sl2 for R=0, R=-I, and the triangular projection; the mixed six-dimensional R(a,b)=(0,a) example; and the five-dimensional reductive-target example. For these explicitly bilinear products/brackets, PA1 is bilinear and the other displayed identities are trilinear. Thus basis verification, together with the inspected formulas and dimension conventions, establishes those identities for all complex vectors in those particular examples. This is stronger than checking a few arbitrary vectors, but it remains restricted to those examples.

The resulting ranks and traces reproduce the frozen JSON: derived ranks 3,3,1,6 for the first four sources; triangular adjoint trace (0,0,-2); zero traces for the perfect examples; reductive source derived rank 5, target rank 3, with a verified two-dimensional nonzero abelian ideal. The source definitions identify these as the stated boundary/positive examples. They do not enumerate arbitrary post-Lie products.

The 17 rational SL2 matrices are distinct sampled group points. Triangular full covariance/modular factors are tested at 51 selected combinations, and mixed covariance at 17 selected combinations. Equality of determinants to a squared or constant formula at those points is not a symbolic verification on the whole group. No finite group sample here proves global determinant nonvanishing, transitivity, or completeness.

The original invalid-R control at lines 198–200 checks that 3 times the sl2 bracket differs from the sl2 bracket on some basis pair, which is a necessary obstruction when R=I. An additional independent invocation of the original verify_pa rejects the actual R=I product at PA2. Both that failure and deliberate require(False) raise RuntimeError under actual optimize=0 and optimize=1 processes. ALGEBRA_NEGATIVE_NORMAL.json and ALGEBRA_NEGATIVE_OPTIMIZED.json preserve the exact observed messages.

The diagnostics do not certify integration of arbitrary homomorphisms, the determinant identity for arbitrary inputs, analytic continuation, all-orbit transitivity, closed stabilizers, covering-space conclusions, solvable-group contractibility, compact real forms, Levi decomposition, top homology, or the general post-Lie nonexistence theorem. Those are the exact remaining mathematical proof-review obligations. The theorem may be established by independent mathematical reasoning; this artifact result does not replace that reasoning.

## Successful rejection controls

With no public payload-hash refresh, proof size changes, same-size byte changes, unlisted files, missing files, duplicate public manifest paths, unsafe public path substitutions, and malformed public JSON were rejected. Each of these seven controls was run normally and under genuine -O. The unsafe-path example is rejected by inventory equality before the later explicit unsafe-path guard, so it does not independently exercise that later guard.

After deliberately refreshing the outer ZIP digest to reach its inner checks, wrong ZIP payload bytes, eight-member archives, extra members, duplicate members, and a traversal-name substitution were rejected. The byte-mismatch and membership rejection messages are retained.

Changing frozen output while leaving the original checker intact was rejected for stdout mismatch. A mutually consistent stub/frozen pair with checks=2895 was rejected by the literal scope/count guard. Supplemental controls independently reached original-freeze hash mismatch, original unique-name count, malformed original-manifest JSON, and invalid_R_identity_detected values false and integer 1; all rejected. The identity comparison is True correctly distinguishes JSON true from numeric 1.

## Every accepted false case, explicitly inspected

All 12 cases below were first observed in the main run and then individually reconstructed, inspected, input-inventoried, and reexecuted. Each returned 0 with the same original success stdout. ACCEPTED_CASE_INPUTS.jsonl contains the actual pre-run inventory of each replay; ACCEPTED_CASE_INSPECTION.json gives its explicit semantic/content inspection. Each replay's input inventory was unchanged after verification.

| Case | Actual accepted false condition | Required mutation/trust boundary |
|---|---|---|
| wrong_metadata | problem_id=-1, rank=-1, status=formally_proved, turns=999/5, original_archive_contains_audits=true | Public manifest alone changed; these fields are never checked |
| duplicate_json_key | Two files keys and two problem_id keys; first files=[] and first problem_id=-1, final originals used | Public manifest alone changed; json.loads retains final duplicate keys |
| nonbytecode_cache_file | Unlisted __pycache__/not_bytecode.txt contains arbitrary nonbytecode text | Original manifest and payload bytes untouched; the whole directory-name class is ignored |
| external_symlink | authored/PROOF.md is a symlink outside the packet whose target has matching proof bytes | Content pins remain satisfied; regular-file and root-containment rules absent |
| dangling_symlink | Extra dangling symlink ignored | is_file returns false; inventory omits it |
| zip_symlink_metadata | CHECKS.md archive member uses Unix symlink mode 0120777 but retains original file-text payload | Outer ZIP hash refreshed; ZIP member modes are unchecked |
| zip_comment_trailer | Altered archive comment and non-ZIP trailing bytes, all member payloads unchanged | Outer ZIP hash refreshed; payload equality does not pin raw archive identity |
| original_manifest_duplicate | Nine original manifest entries but only eight unique names, with CHECKS.md repeated | Original manifest, its ZIP copy, and public hashes refreshed; only unique count is checked |
| original_manifest_traversal | Original manifest and ZIP use ../authored/PROOF.md, resolving to the same proof bytes | Matching original manifest/ZIP/public hashes refreshed; original paths are not safety-checked |
| false_proof_rehashed | Proof text says Every complex Lie algebra is semisimple. No proof. | All affected internal hashes/ZIP bytes refreshed; prose truth is outside this verifier's scope |
| checker_stub_rehashed | Checker replaced by a two-line program printing the frozen JSON | All affected internal hashes/ZIP bytes refreshed; self-consistent output is not proof of execution of the original calculations |
| hostile_sitecustomize | All 18 original files unchanged; child startup hook prints frozen bytes and calls os._exit(0) before the checker executes | Hostile PYTHONPATH inherited by original verifier children |

The false proof is explicitly refuted by a one-dimensional abelian complex Lie algebra. This control demonstrates that packet-integrity success cannot mean mathematical proof acceptance. The self-rehashed cases differ from the external authenticated original pins. The content-only symlink/cache cases show why complete filesystem inventory is a separate requirement. The original verifier never extracts the ZIP, so acceptance of unsafe archive names here is not evidence of an extraction exploit; the demonstrated defect is insufficient validation of the asserted original packet contract.

The hostile startup case is materially different: it preserves the authenticated original file bytes. The source at original verifier line 51 launches sys.executable without -I/-S or a sanitized environment. A benign sitecustomize recorder observed actual children with optimize=[0,1] in the controlled baseline and [2,2] under inherited PYTHONOPTIMIZE=2, while the parent itself used -I -S -B. Both calls still printed normal_and_optimized_outputs_match=true. The startup-spoof script was read in full and is preserved in SITE_SPOOF_SOURCE.json. It supplies frozen bytes before original checker execution; source hashes alone cannot secure interpreter startup behavior.

These observations bound the original verifier's assurance. Its own docstring and output correctly say it is not a theorem prover. Metadata and proof-semantic false acceptance are not evidence that the original mathematical theorem is false.

## Runtime, dependencies, failures, and limits

The trusted computing base includes the selected interpreter, its standard-library fractions/hashlib/json/subprocess/zipfile implementations, operating system filesystem/process behavior, and this audit's own Python/Node orchestration. Hash agreement authenticates bytes relative to an externally supplied expected hash; it does not establish authorship, priority, source authority, or truth. SOURCE_HASHES.json contains only historical source metadata; no cited scholarly source was downloaded or authenticated in this artifact audit.

The initial unified shell tool failed to create a process. Local Node APIs were used subsequently. An actual /usr/bin/python3 probe returned 69 with an Xcode-license diagnostic; no license/system change was attempted. An existing Homebrew interpreter probe returned 0, but immediate persistence twice failed ENOSPC. Its real in-memory output buffers were retained and later written; RUNTIME_PROBE2_RECEIPT.json candidly leaves exact process end time null. That discovery probe is not counted among the 61 original-code/control processes and is not offered as a fully timed validation run.

Intermittent ENOSPC also prevented an attempted authentication-record compaction. Only an audit-owned file was deleted, its parsed data stayed in memory and the research log, and AUTHENTICATION.json was restored before the original audit run. All original-code/control processes ran only once durable raw-output persistence was available. No synthetic process recovery or invented success receipt was used. The original-code and control runs have complete start/end/return/output receipts. No foreign cleanup was performed.

The safe payload excludes private_tmp, raw native records/corpora, raw stderr, credentials, and private absolute paths. SAFE_MANIFEST.json lists each included path, byte count, and SHA-256 and excludes itself. Own audit code, exact original checker code, exact positive stdout, public-safe receipts, inventories, and decisions are included. Raw diagnostics and the pristine private original packet are retained locally for further inspection.

## Exact remaining gap and next engineering constraint

The verified artifact result is: authentic preserved source, exact nine-member author freeze, reproducible original finite examples in normal and optimized CPython, and precisely delimited original-verifier false acceptance. Artifact auditing cannot close the theorem's global Lie theory/topology obligations by adding more finite samples or internal hashes. Such a route transfers the mathematical difficulty and is blocked as a proof route.

A hardened future artifact tool should authenticate its source and expected manifest externally, apply strict JSON/list/path/type/file-mode rules, preserve raw archive identity, and isolate every actual child interpreter and its environment. It should separately label integrity, exact finite algebra, and global mathematical review. This audit implements no replacement publication verifier and changes no original packet. Such engineering would improve artifact assurance, while the global mathematical proof still requires its own independent check.

Audit completion: **100% of this artifact-validation assignment**, with the stated scope and limitations. Original substantive effort: **1/5 unchanged**. No Git write, push, remote mutation, external individual communication, release, DOI, or Zenodo action occurred.
