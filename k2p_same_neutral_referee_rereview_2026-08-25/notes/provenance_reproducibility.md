# Fresh provenance and reproducibility audit

Date: 2026-08-25 (America/Los_Angeles)  
Reviewer task: integrity, provenance, build reproducibility, dependency binding, and execution orchestration only.  
Submitted archive: `/Users/alec/Documents/Math/k2p_same_neutral_referee_rereview_2026-08-25/source_archive/K2P_Principal_D_Plus_Referee_Package_20260824.zip`  
Initially pristine extracted project: `/Users/alec/Documents/Math/k2p_same_neutral_referee_rereview_2026-08-25/isolated/k2p_principal_d_plus_submission_referee`  
Independent scratch: `/Users/alec/Documents/Math/k2p_same_neutral_referee_rereview_2026-08-25/independent_checks/provenance`

Checkpoint: this assigned audit is 100% complete. No person was contacted, no submitted file was repaired, and the global full replay was left to the coordinating referee as agreed.

## Status

| Layer | Status | Basis |
|---|---|---|
| Distributed ZIP and adjacent checksum | **PASS** | Independent reconstruction of all paths, bytes, SHA-256 values, counts, roots, and ZIP metadata; two independent byte-identical archive rebuilds. |
| Frozen and submission content ledgers | **PASS** | 399 frozen files and 80 submission files independently reconstructed; all 479 manifest rows and the included manifest matched the pristine archive. |
| Git provenance | **PASS** | All 480 archive members exactly match local annotated tag `k2p-same-biorxiv-v1.0.0`, commit `c4d299883a648ebce8500274ab1fd0c131da54f9`. |
| Article/supplement source and PDF binding | **PASS** | Five sources, PDFs, logs, build report, static audit, crosswalk, stored replay, telemetry, and lock are byte-consistent. Independent Tectonic rebuilds are byte-identical. |
| Current supplemental dependency binding | **PASS** | The current v2 manifest declares three dependencies; all are present, outer-bound, and exact at the final tag. |
| Stored clean-full telemetry as provenance | **PASS (provenance only)** | Stored 40-layer report and telemetry are internally and byte consistent with commit `1877985d...` and the frozen lock. A stored PASS is not treated as fresh computational validation. |
| Declared ordinary release-mutation command | **FAIL** | It overwrites a locked certificate in place with extraction-path-dependent traceback hashes, then fails its own source-drift guard. Independently reproduced in three disposable extraction paths and once in the original review extraction. |
| Overall reproducibility | **FAIL / scientific HOLD** | A declared ordinary qualification gate cannot run successfully from an arbitrary clean extraction and alters authoritative evidence. No theorem counterexample follows from this defect. |

Evidence types are deliberately separated: byte/hash agreement and Git matching are provenance evidence; TeX rebuilds are computational reproducibility evidence; neither validates the mathematical theorem.

## Finding PR-1 — declared mutation gate is path-dependent and mutates locked evidence

Severity: **reproducibility-blocking** and **fresh computational-gate blocking**. It is not a mathematical counterexample.

The declared ordinary qualification path in `work/final_theorem_release/README.md:85-90` includes:

```sh
.venv/bin/python -B work/final_theorem_release/run_release_mutations.py
```

The failure chain is explicit:

1. `work/final_theorem_release/run_release_mutations.py:727-744` snapshots the sealed `quartet_semantics_mutation_certificate.json`, invokes `test_quartet_semantics_mutations.py` in the authoritative directory, and requires byte equality afterward.
2. `work/quartet_separation_closure/test_quartet_semantics_mutations.py:47-74,103-117` hashes raw combined child output into seven mutation rows. Failed verifier runs produce uncaught tracebacks containing absolute script paths.
3. The test unconditionally writes `HERE / "quartet_semantics_mutation_certificate.json"` at lines 186-197 rather than accepting a disposable output path.
4. `run_release_mutations.py:628-637` then detects its own write as `MUTATION_SOURCE_TREE_FINGERPRINT_DRIFT`.

### Exact package-command reproduction

From a pristine full extraction at:

`independent_checks/provenance/pristine_archive_extract/k2p_principal_d_plus_submission_referee`

I ran the documented command with the already-created exact dependency environment:

```sh
/usr/bin/time -l /Users/alec/Documents/Math/k2p_same_neutral_referee_rereview_2026-08-25/isolated/k2p_principal_d_plus_submission_referee/.venv/bin/python -B work/final_theorem_release/run_release_mutations.py
```

Observed: exit 1; wall 3.02 s; maximum RSS 99,418,112 bytes; peak footprint 87,278,048 bytes. Stdout was only `K2P_FINAL_MUTATION_REJECTED name=optimized_mode` (SHA-256 `b947c165a7cbeab18f3dfba742f89b660e4b57d4bf828f7641878ef47108d0c9`). Stderr ended `FINAL_RELEASE_MUTATIONS_FAIL:MUTATION_SOURCE_TREE_FINGERPRINT_DRIFT` (stderr plus `/usr/bin/time -l` SHA-256 `5c80e5c76b52168e02752ba191f6d4e1db32d153c42664392b5a8db922c67c6c`). Exactly one of 479 manifest-declared files drifted:

| Path | Sealed SHA-256 | After-run SHA-256 | Bytes |
|---|---|---|---:|
| `work/quartet_separation_closure/quartet_semantics_mutation_certificate.json` | `51aca097b5a4ed7e699206d58b6e61ebc899372057ea733e83ac148e86231eb1` | `c98ded48e720b15d38daf3ec5fb69d84fdd9a4746311cb22b26314438b483574` | 2,435 |

An earlier run in the main isolated review extraction changed the same file to `d978e002ea6b03b4abdef45fbd1934f780187924dabe91385f236c9fc6426390` at mtime `2026-08-25T08:24:57-07:00`. The sealed and rewritten files have the same length but seven different `stdout_sha256` fields and a different payload hash. Evidence: `locked_file_drift_capture.json` SHA-256 `eb93afbb4b1c603f504bcc56cca923e39710462deb7916c5b4ab2992ddd67ee1`.

### Genuinely independent two-directory attack

I extracted only the nine required files twice from the ZIP into differently named directories. All eight immutable inputs were byte-identical. In each directory the quartet mutation test itself exited 0 and all eight attacks rejected semantically, but it rewrote the sealed certificate differently:

| Directory | Wall | Maximum RSS | Regenerated certificate SHA-256 | Payload SHA-256 |
|---|---:|---:|---|---|
| `.../quartet_path_reproducer/extraction_alpha` | 3.49 s | 90,079,232 | `f76ee6c8eccb6b8acc9d6ed837902ebcc560d1c46263b9712d2b964853c9c418` | `a7acdb853d08819d085404bb93b1732d7ea6975bdeaa3b9e90de5e4270c51a68` |
| `.../quartet_path_reproducer/extraction_beta_with_different_length` | 3.51 s | 90,685,440 | `e73e1ab8b8fa0f78cd2aa5560286667b6ef576f8302749c1d2adaa67ec435c7f` | `d365a90faff1e8a1e8e49763157870ad513b5d0b6b7ad97966a4f16a3386f6a8` |

Seven `stdout_sha256` fields differed; only `optimized_python` was stable. A direct single-mutation trace had raw hashes `7ca2876cebfacd4050327a786e79a5d96f7052d50358356ab9122eb18f074494` and `6aaa6de52482d40bcb74a71a67eb032eb372ce2b02bb81ed1369eee43e4f2df9`. Both traces contained the respective absolute project path. After replacing that path by `<PROJECT>`, the outputs were byte-identical, normalized hash `c03392f0905ab9a15a9b8db30b257bb1724f4050c12cfbe57abbf07c0ebb9a50`.

The independent reproducer is `quartet_path_dependence_reproducer.json`, SHA-256 `13c27197e78b7c260e4d6e964a5bbdd2a56fc8af5433d0b1aa1ea3b596e03bb7`; its independent script SHA-256 is `cfdf2532398f53d67204eec90e231dc3421e7ee2d8555356878c7fead044e21f`.

### Effect and smallest remedy

The mutation semantics still reject the intended eight attacks. The defect is that a declared ordinary release gate is not relocatable, is not source-preserving, and cannot freshly PASS from this clean extraction. Consequently the package's fresh mutation qualification remains blocked even though stored mutation evidence exists.

Smallest adequate repair:

1. Add an explicit `--output` argument to `test_quartet_semantics_mutations.py` and pass a path inside the outer suite's temporary directory, as the neighboring terminal-binding mutation gate already does.
2. Do not certificate-bind raw traceback bytes containing absolute paths. Record exit status and required semantic marker, or normalize all project/temp paths before hashing.
3. Compare the disposable report's semantic content to a path-independent expected report; never rewrite the authoritative certificate during checking.
4. Add a mutation/test that runs the suite in two differently named extraction directories and requires byte-identical reports plus no source-tree changes.

Because the repaired test, outer mutation harness, mutation certificate, and lock hashes change, regenerate the release lock, crosswalk, full replay/telemetry, outer manifest, and archive. Any document that prints one of those hashes must also be rebuilt; unchanged article/supplement PDFs need not change unless their source text changes.

## Finding PR-2 — legacy review entry points are absent

Severity: **presentation/protocol incompatibility; nonblocking relative to PR-1**.

The revised ZIP contains none of these filenames named in the prior review protocol: `START_HERE.md`, `verify_handoff.py`, `test_handoff_mutations.py`, `setup_environment.sh`, `run_all_verifiers.py`, or `SUBMISSION_BINDING.json`. The current entry points are instead `output/referee/README.md`, `work/final_theorem_release/README.md`, and `proof_compression_submission/README.md`. Exact legacy commands therefore cannot be rerun against this ZIP. This should be stated in the main report as an unrun legacy gate, not silently mapped to a PASS.

The current v2 binding is nevertheless internally explicit and independently checkable; see the dependency audit below.

## Archive integrity and deterministic rebuild

Independent code `audit_archive.py` did not import submitted code. It reconstructed the frozen universe from the outer lock and all nested manifests/locks, independently scanned the submission-source policy, validated every ZIP member, and rebuilt the archive twice.

| Quantity | Independent result |
|---|---:|
| Distributed ZIP SHA-256 | `8a86436f7ff1cdaafb18a163469569f6cf8f697db866423d30969bcca35e7535` |
| ZIP bytes | 214,790,278 |
| Members | 480 |
| Uncompressed member bytes | 482,918,533 |
| Compressed member bytes | 214,651,802 |
| Frozen files / bytes | 399 / 478,755,815 |
| Submission files / bytes | 80 / 4,065,606 |
| Manifest bytes | 97,112 |
| Manifest file SHA-256 | `c400539154c075fe03665a759966e86569dbfb3214c3d451f8a74e9395936dde` |
| Manifest payload SHA-256 | `ba92e24ba44d4b5552b405d6dd93cd367c487c6f2df97580258bb7a5a20f9350` |
| Frozen content root | `072baaa4066569acd31c552149f6afb727323e54b241bdefc98452598309dd61` |
| Submission content root | `87b62d2f793d6283bcc08635cdeb2232634c6f87a073b762572576600ce901fd` |
| Combined content root | `9cbf9264172b55ebe6fbc3a513e62a43c08de040f78c9c82d128c19c8190a86c` |
| Release-lock file / payload | `7113b1c52d577858ec20ef83cd87c870242c8ddc96018036b5c073229821eec9` / `f0342dd538b6b72eb5e31eb674df2ce6984b9e4fae6e502583e4bb195aedbb0f` |

Both independent rebuilt ZIPs were 214,790,278 bytes and had the exact distributed hash. ZIP prefix, lexicographic member order, fixed `2026-08-24 00:00:00` member timestamps, deflate compression, normalized `100644` modes, lack of duplicates/encryption, and lack of extra tree files all passed. The adjacent checksum file is itself SHA-256 `b5435841b45a18115e35ece333ee3d9b3d2bdd3269b0873167e576186f3d1eef` and names the same ZIP hash.

Archive audit result SHA-256: `fd7ae2e9e4dc9424221669228b43c9c7b7b7c61d59106c4c01bce64ee0f8a49d`. Runtime: exit 0, 42.02 s, maximum RSS 777,011,200, peak footprint 779,420,704. Stdout hash `5d8d6edc3f6c0b45bf4f9d9588d0aa9ede847fb0044106844e9476239a70c003`; time/stderr hash `260b830ec99e7e29743733d3400c5f34be64724e2009ff7649cf62048d4d6b03`.

## Git and replay provenance

Independent `git ls-tree` plus `git cat-file --batch` comparison found:

- Final annotated tag `k2p-same-biorxiv-v1.0.0` resolves to commit `c4d299883a648ebce8500274ab1fd0c131da54f9`. Every one of the package's 480 files matches that commit byte-for-byte.
- Stored replay commit `1877985d20132fb186d21a5985e8c5f760a656af` predates self-referential packaging/report additions. It matches 452/480 package members, with 27 later packaging/output differences and one then-absent referee prompt. All 399 frozen-evidence bytes and all five TeX/Bib source bytes match that replay commit.
- Stored report SHA-256 `ec5fefc3c1ab2210e9c53792240ebe008603da6abd004d093e2b95e15ff5c10b` records 40 unique PASS layers, internal elapsed 5,577.570125 s, and lock payload `f0342dd5...`. Telemetry SHA-256 `415bf36a59e6006603e4382085c784ffc4e1a1744f1e4c920cd5f0d313fb9df5` records wall 5,578.1 s, maximum RSS 2,600,484,864, peak footprint 503,350,016, clean detached checkout, Python 3.14.6, NetworkX 3.5, and SymPy 1.14.0.

The replay report and telemetry are accepted here only as correctly bound historical provenance. Fresh full execution is reported separately by the coordinating referee.

Git audit runtime: exit 0, 3.12 s, maximum RSS 791,429,120, peak footprint 780,944,392; stdout hash `08c065ed94748b17889aeec4f5e1f15acd63bdbecd5dbf45d9b502159ad148eb`, time/stderr hash `04a4c9e62db1f893b00d2337c2b9421635fa098ab49369f1feb697195e5ad627`.

## Cross-artifact consistency

An independent standard-library audit checked 19 relations without importing package checkers:

- canonical payload hashes for the outer manifest, theorem-artifact crosswalk, PDF build report, static audit, and release lock;
- all 479 declared disk rows in a pristine archive extraction;
- all 159 artifact references across all 13 theorem-crosswalk claims, including declared JSON schemas and correct frozen/submission layer assignment;
- five TeX/Bib source hashes and sizes across the PDF report, static audit, replay telemetry, manifest, and actual bytes;
- both PDF and log hashes/sizes;
- stored 40-layer report, telemetry, lock, runtime, and manifest relationships; and
- literal article bibliography and both literal generated supplement inputs.

All 19 passed. Result `artifact_consistency_audit.json` SHA-256 `2f35d56cc27c789a75b48e2e48bf42e4be0bdc59ee40ca017513656a5aac5396`; script SHA-256 `591a7fa52e05274e05de8be6b1a3eb1f6c07c897bf0b4db8458090f5ed65328c`; runtime 0.51 s, maximum RSS 162,529,280, peak footprint 151,831,056; stdout hash `ad8f2ce9923112597c0ce592f333dd6bd4e08b766ef5400185d0fd53af4e87d2`, time hash `03d275fec3b73d0cb01b11e5206254327e4230ee2c3712ca994cfd3a03ac20d5`.

## Dependency binding

The current package has no legacy `SUBMISSION_BINDING.json`. Static AST inspection of `build_revised_referee_bundle.py` and independent manifest comparison show that manifest schema `k2p-revised-referee-bundle-manifest-v2` declares exactly three supplemental execution dependencies:

| Dependency | Bytes | Current/final-tag SHA-256 | In older 399-file inner ledger? |
|---|---:|---|---|
| `output/referee/README.md` | 1,031 | `f203bf0f59a400137f144960f56ad03da7276088d0917e0f88c24576ef9ca074` | No |
| `output/referee/REFEREE_BUNDLE_CONTENTS.json` | 75,634 | `16d4d18b495fec100fb5cc2b847c2baf2d1dfda8517c56e8816b3cc0726614af` | No |
| `output/referee/build_referee_bundle.py` | 7,266 | `87bf4ef0303d11412dac28f02fcaaf0cf9df46e81d85a3c0e92c01570be3668a` | No |

All three differ from their earlier replay-commit forms and exactly match the final tag. The five TeX/Bib files are a separate PDF source-set contract, not five supplemental execution dependencies.

Both Python requirement files are identical (SHA-256 `c9716447ec239f2c91180609c0b1c972533605a387be73d001c7e6b7e9b01891`) and contain only `networkx==3.5` and `sympy==1.14.0`. The tested environment exactly satisfies them. Tectonic is required externally; tested version was 0.16.9.

Dependency audit result SHA-256 `9a4ea338aba4654c167f5f494ebfc8722f4d37822efdcbdb478ae573af61a5f4`, script SHA-256 `e51d41eb03739eb192e57662e0319266457507d97312cd9c4953213545f1d2cb`; exit 0, 0.84 s, maximum RSS 77,463,552, peak footprint 16,777,648.

## PDF rebuild and visual inspection

Environment: macOS 26.5.2 build 25F84, Apple M1 Pro (10 cores), 16 GB RAM, arm64; Python 3.14.6; NetworkX 3.5; SymPy 1.14.0; Tectonic 0.16.9; Poppler 26.08.0.

Exact five-source set:

| Source | Bytes | SHA-256 |
|---|---:|---|
| `article/main.tex` | 85,814 | `ca6dd8d750768b0c47121c8bd60c5c9c3223af194139f5f578cb8bbf5fd5c3f1` |
| `article/references.bib` | 6,977 | `14dbb4901d924b068c8cc2d050e73bae3cf996a72863a22ade90d6f8e6b4057c` |
| `supplement/supplement.tex` | 44,051 | `57275e1e5e1058306607a98583ac31e98383952ef2284515fea01f1c47ce95bd` |
| `supplement/compression_tables.tex` | 3,269 | `1ce2ef60784c1a240cdd639cd845710934c9587e4c341ad293394c8e1f758e9b` |
| `supplement/certificate_appendix.tex` | 22,405 | `f2444f0308ab2dcccc45dec0704e98b147fffe4bb11fef9ef19cb7f34e688af5` |

The submitted builder ran in a disposable copy with `--visual-pass --check`: exit 0, 19.44 s, maximum RSS 255,836,160, peak footprint 16,875,952; stdout hash `33e3306416c0279a999db2c1e244318ea5d68df0e3232ce6754af63940e9a177`; time hash `9711fce43fb30c02ea5d3fe8f5eaef28ce5e4641998a1a4bb43f4cffa01fad63`.

I also copied only the five declared sources and ran Tectonic directly with `SOURCE_DATE_EPOCH=1787529600`:

| Output | Wall | Max RSS | Bytes/pages | PDF SHA-256 | Log SHA-256 |
|---|---:|---:|---:|---|---|
| Article | 4.02 s | 252,854,272 | 194,316 / 26 | `2c4433d53c33c337d4ed028c2843cf0b5631263d7bf4a0a42106727985daa3a8` | `d243446067dd462d90921ddbb0b5891c1ae4509e3b710f6361f8b5f819dbe5e3` |
| Supplement | 3.51 s | 250,593,280 | 158,872 / 24 | `9b10797d7503e6940d80a95bc90302b3b32a9ea34cb9f63a54bee3f12f3c06e1` | `2ce17ff09bcc9a4a1d785cd6cfe928e8875556143e885e9b4a139c90ec868b89` |

Each rebuilt PDF and log is byte-identical to the submitted file. All fonts are embedded/subset; no fatal TeX error, undefined citation/reference, overfull box, or PDF-string warning was found. The supplement has one visually harmless underfull hbox at source line 830. All 50 pages were rendered at 96 dpi and inspected in four contact sheets; supplement page 14 and article page 25 were also inspected individually. No clipping, collision, truncation, or unreadable content was observed. PDF rebuild summary SHA-256 `24f92d87a7ddc34453097ab3fb2ab5e53a9965c38fe03920201afdb896d6d9b2`.

Omission behavior was correct for the stated contract:

- missing `compression_tables.tex`: Tectonic exit 1 with the named missing-file diagnostic; 2.48 s; RSS 216,776,704; stdout/stderr hashes `0a6161b17697bef0fe63029b6fb97254c30e75f8fa3dd33206a614f3077f84e3` / `c45468c04331bfae0306413ed0798b337a6643a763549425f3119cec9f5a6f5d`;
- missing `certificate_appendix.tex`: exit 1 with the named diagnostic; 0.91 s; RSS 216,547,328; hashes `8a7697e69297f0a5b5b8868c72de130422c77617dc9befe9532e0c7d95f3e241` / `ad9f02229491f59cb3f89e0156c00072b16a68df860ade6c7134bdc2be280c80`;
- missing bibliography: raw Tectonic itself exits 0 while warning that BibTeX errors were ignored. This is not contrary to the package's stated contract: bibliography omission is enforced by the outer manifest, not direct Tectonic. The independently resealed omit-bibliography manifest was rejected with the exact missing path.

## Fail-closed and mutation checks that passed

- Inner bundle check: exit 0, 0.45 s, RSS 229,507,072; stdout hash `3bdc629a55de599eda014ed5fc8b0cf033692ad9bd27da6175cd97ebed5fcb91`; time hash `47c6424cd6966fab430249151f6a8d140887d4999825d0b9afea71d1dc57fd07`.
- Outer builder `--check`: exit 0, 0.44 s, RSS 231,768,064; stdout `c5118bede592ee62ecdcbaf4f68684ff53012afb942b0179030e2ab9290e2b4b`; time `179681298506f2e553fceb7ae4c4c41e095345a832b1c3cc7fafa770c850efce`.
- Independent outer checker: exit 0, 0.51 s, RSS 292,225,024; stdout `c5118bede592ee62ecdcbaf4f68684ff53012afb942b0179030e2ab9290e2b4b`; time `7fea14b79f0202fca973ee096c193376a2efd404b13c8b3ad1b75c1654b68f2e`.
- Crosswalk/bundle mutation suite: 27/27 intended rejections, exit 0, 6.69 s, RSS 604,422,144; payload `fa1b8eeb021a10776d766077e7cc05513c1a6c25578e42a2be9b1898956fb087`; stdout `5567ad8ff3ef51d275390b8e859f733b8bc9b92666446286b5283fe83287de89`; time `a65e553ae264f9e49057942890726325db6f94d37439c510735239593396f9bb`.
- Clean-replay telemetry mutations: nine tests passed, including dirty/attached checkout, source output drift, bad commit/lock, malformed/non-PASS report/time, exact intentional expected-failure row, and project prefix. Exit 0, 4.61 s, RSS 27,394,048; stderr/time hash `67e12274ea10cf470288b13e1f5dc325a08673dacca28e484215e86b125831db`.
- Independently resealed outer-manifest mutations all failed at the intended ledger layer: omitted bibliography, omitted content ledger, stale article PDF hash, and stale full replay hash. Mutant hashes were respectively `dd7298c8d403ab6637cf9a8f13dfd81508dbbb4e78f278ac7053f167050fb6ec`, `3fda77f29fcd1b646223b781a73f7d08a93bf4cca40ef5021751718fb9d13400`, `6f8efc0771ce8b247df9c688386fb694c4ab5290c8ecc3a24f1fdfbc2e697fdf`, and `b1f41ce36022a70185c183366c1e8f896faf0afaf1d7a286056b7a9ac3a502b9`.
- Optimized Python was independently rejected by the outer checker, PDF builder, and telemetry builder, all exit 1 with their intended marker. Stderr/time hashes: `fc1e9597addf8dbec954ecae385de968a6ce134042224a75561fc849c2f9cc30`, `32d1ade153dbe7f0e06543bc9fbd0833fddba721ba8d0b9bab6853b15e793d86`, and `7799ac1117bd4a2e1013f3ca0a3d7b0dadeabbb9ee18a461978cabaa2eee0016`.

These passes do not cure PR-1: the crosswalk mutation suite verifies the stored package ledger and its own mutations but does not successfully execute the declared ordinary final release-mutation command from a relocated extraction.

## Main command ledger

Here `A=/Users/alec/Documents/Math/k2p_same_neutral_referee_rereview_2026-08-25`, `P=$A/isolated/k2p_principal_d_plus_submission_referee`, and `S=$A/independent_checks/provenance`.

| CWD | Exact command (redirections omitted) | Exit | Wall / max RSS | Principal output hash |
|---|---|---:|---|---|
| `$A` | `/usr/bin/time -l python3 -B independent_checks/provenance/audit_archive.py --project isolated/k2p_principal_d_plus_submission_referee --archive source_archive/K2P_Principal_D_Plus_Referee_Package_20260824.zip --checksum source_archive/K2P_Principal_D_Plus_Referee_Package_20260824.zip.sha256 --result independent_checks/provenance/archive_audit.json --rebuild independent_checks/provenance/rebuilt_archives/rebuild_1.zip --rebuild independent_checks/provenance/rebuilt_archives/rebuild_2.zip` | 0 | 42.02 s / 777,011,200 | result `fd7ae2e9...` |
| `$P` | `/usr/bin/time -l .venv/bin/python -B output/referee/build_referee_bundle.py --check-only` | 0 | 0.45 s / 229,507,072 | stdout `3bdc629a...` |
| `$P` | `/usr/bin/time -l .venv/bin/python -B proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check` | 0 | 0.44 s / 231,768,064 | stdout `c5118bed...` |
| `$P` | `/usr/bin/time -l .venv/bin/python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py` | 0 | 0.51 s / 292,225,024 | stdout `c5118bed...` |
| `$P` | `/usr/bin/time -l .venv/bin/python -B proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py --check` | 0 | 6.69 s / 604,422,144 | stdout `5567ad8f...` |
| `$P` | `/usr/bin/time -l .venv/bin/python -B proof_compression_submission/test_clean_full_replay_telemetry.py` | 0 | 4.61 s / 27,394,048 | stderr/time `67e12274...` |
| `$A` | `/usr/bin/time -l python3 -B independent_checks/provenance/audit_git_binding.py --repo /Users/alec/Documents/Math --project isolated/k2p_principal_d_plus_submission_referee --project-in-repo k2p_level2_identifiability_closure --revision 1877985d20132fb186d21a5985e8c5f760a656af --revision k2p-same-biorxiv-v1.0.0 --result independent_checks/provenance/git_binding_audit.json` | 0 | 3.12 s / 791,429,120 | result `99d587f6...` |
| `$S/pdf_rebuild/project` | `/usr/bin/time -l python3 -B proof_compression_submission/build_submission_pdfs.py --visual-pass --check` | 0 | 19.44 s / 255,836,160 | stdout `33e33064...` |
| `$S/pdf_rebuild/direct/article` | `/usr/bin/time -l env SOURCE_DATE_EPOCH=1787529600 tectonic --keep-logs --keep-intermediates main.tex` | 0 | 4.02 s / 252,854,272 | PDF `2c4433d5...` |
| `$S/pdf_rebuild/direct/supplement` | `/usr/bin/time -l env SOURCE_DATE_EPOCH=1787529600 tectonic --keep-logs --keep-intermediates supplement.tex` | 0 | 3.51 s / 250,593,280 | PDF `9b10797d...` |
| `$A` | `/usr/bin/time -l python3 -B independent_checks/provenance/audit_artifact_consistency.py --project independent_checks/provenance/pristine_archive_extract/k2p_principal_d_plus_submission_referee --result independent_checks/provenance/artifact_consistency_audit.json` | 0 | 0.51 s / 162,529,280 | result `2f35d56c...` |
| `$A` | `/usr/bin/time -l python3 -B independent_checks/provenance/reproduce_quartet_path_dependence.py --archive source_archive/K2P_Principal_D_Plus_Referee_Package_20260824.zip --interpreter isolated/k2p_principal_d_plus_submission_referee/.venv/bin/python --project independent_checks/provenance/quartet_path_reproducer/extraction_alpha --project independent_checks/provenance/quartet_path_reproducer/extraction_beta_with_different_length --log-dir independent_checks/provenance/logs --result independent_checks/provenance/quartet_path_dependence_reproducer.json` | 0 | 0.63 s / 64,241,664 | result `13c27197...` |
| pristine full disposable extraction | `/usr/bin/time -l $P/.venv/bin/python -B work/final_theorem_release/run_release_mutations.py` | **1** | 3.02 s / 99,418,112 | stdout `b947c165...`; stderr/time `5c80e5c7...` |

All package writers above were run only in disposable copies. The sole authoritative-tree change was the defect under test: the package's own release-mutation command rewrote the locked quartet certificate. That tree was frozen as evidence and not repaired.

## Code inspected

The following load-bearing orchestration/provenance code was read before its relevant execution:

- inner builder `output/referee/build_referee_bundle.py`, SHA-256 `87bf4ef0303d11412dac28f02fcaaf0cf9df46e81d85a3c0e92c01570be3668a`;
- outer builder `build_revised_referee_bundle.py`, `73c557839b794fe21c4d7aa3d3d4359548481b31b2360674bdde4e53ef6b128b`;
- outer checker `check_revised_referee_bundle.py`, `bad0b9ca6225346b6e1bfb1d9ddd5aef8e2fc485cf1f884c8f248bdc78605c18`;
- outer mutation suite `test_crosswalk_bundle_mutations.py`, `b5661ed1d78f77db49dff1906cf1a0bb0869e0d69fa124424f24dfbad52bd327`;
- crosswalk producer `build_theorem_artifact_crosswalk.py`, `18604fac1873593b6694abec1f9db5ed108723339670d04f9f8b1953a22abe1c`;
- PDF builder `build_submission_pdfs.py`, `337ab06167dc9522896e2e0a4c885f45c3f7674173301a09271881693c254c66`;
- telemetry producer/test, `682c9c849034c4bc77dc59f77f2bf780628ae57483db83b07c863b1121fc4f86` / `9c81701e32614504b6b6d35eb8731865e2b57b973a24f8d2a4fbad872c85fb71`;
- final replay harness `verify_final_theorem_release.py`, `f30cc4b26e45d0ed959786cf4504ae8974a3c3da5953a40072b8cc48bd82d95a`;
- release common code `release_common.py`, `f8e9c2826ccfd93b04294650c16ef8e93e7b8899cb27515f1f2f6b6b3f0fd844`;
- final mutation harness `run_release_mutations.py`, `8f98037e258b80b14cc373b1f9ce91f04a97eb9845c570d187f69c887d5805d6`;
- quartet mutation producer and verifier, `a9d52d3bf965527a4bcaa821cbe05925c045f119c3163754f6f0c3b849330e24` / `783cc522c8669eb1cd89928246b998ed09b222a9e9931d4c22d7fd03b5e05ec8`.

Static replay-harness inspection found 23 quick layers plus 17 full-only layers, matching the stored 40-layer report. It validates the release lock at entry, captures child commands/exits/stdout/stderr hashes and required markers, and treats expected-failure layers separately. The global fresh full run was intentionally not duplicated here.

## Required action ordering

1. Repair PR-1 so the mutation test writes only to a caller-provided disposable output and emits/hash-binds path-independent diagnostics.
2. Add the two-directory relocation/no-source-write regression test.
3. Rerun the documented ordinary mutation command from a fresh arbitrary extraction; require exit 0 and a byte-clean source tree.
4. Regenerate/reseal the affected certificate, release lock, crosswalk, replay/telemetry, outer manifest, tag, checksum, and ZIP; rebuild documents only if any printed hash/source changes.
5. Either restore a top-level `START_HERE.md` and legacy wrapper names or explicitly state in the handoff that the old protocol filenames were superseded, with a one-to-one command mapping.

No mathematical or code-architecture expansion is recommended; this is a localized reproducibility defect.
