# Fresh 2026-08-25 provenance and reproducibility subreview

## Scope and status

Package reviewed, read-only:

`isolated/k2p_principal_d_plus_submission_referee`

Distributed archive reviewed:

`source_archive/K2P_Principal_D_Plus_Referee_Package_20260825.zip`

All submitted writers and mutation runners were executed only in clean
extractions under `tmp/provenance/` or in the review team's separate
`tmp/execution/` extraction.  I authored only review notes, independent
checkers, and review registries outside the isolated tree.

**Provenance/integrity: PASS. Reproducibility: PASS, with one nonblocking
documentation defect (P1 below).**  These statuses mean that the bytes,
bindings, archive, sources, and current fail-closed entry points checked here
are reproducible.  Hash agreement and successful replay are not mathematical
validation.  The stored 5,428-second full replay is treated only as sealed
provenance; the review team's fresh full mathematical/computational replay is
reported separately.

The two defects from the preceding candidate that were explicitly assigned to
this subreview are fixed:

1. **The path-dependent/source-writing quartet mutation defect is fixed.**
   The runner now requires a caller-owned output outside the project, the
   relocation regression obtains byte-identical reports from different path
   lengths, direct alpha/beta runs produce the frozen report hash, and both
   extracted source trees remain byte-identical to the isolated package.
2. **The stale C02 promotion authority is fixed.**  The current v2 certificate
   is restricted to raw displayed-quartet/tree-of-blobs direction and
   expressly disclaims restoration and whole-map `T_i` authority.  The old
   646/36,404 narrative remains in the ZIP, but only as a hash-bound,
   `promotion_authority:false` historical artifact.  Current restoration v3,
   the supplement, and the lock agree on 35,758 + 606 + 148 + 24 + 32 first
   children, 248 + 8 second children, 36,824 edges, and 36,792 leaves.

Machine-readable summary:
`reports/provenance_reproducibility_registry.json`, SHA-256
`15a0808f42745d9233e028a3aa5e2ec6a0d72b240f6f9540ee10d763b776063e`.

## Environment

- macOS 26.5.2 (build 25F84), Darwin 25.5.0, arm64.
- Apple M1 Pro, 10 physical/logical cores, 17,179,869,184 bytes RAM.
- CPython 3.14.6; qualified environment: NetworkX 3.5 and SymPy 1.14.0.
- Tectonic 0.16.9; Poppler/pdfinfo 26.08.0; Info-ZIP 6.00; Git 2.38.2.
- Exact requirements (both copies): 28 bytes, SHA-256
  `c9716447ec239f2c91180609c0b1c972533605a387be73d001c7e6b7e9b01891`.

The dependency audit was repeated with the fresh review's qualified
interpreter at
`/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/tmp/execution/k2p_principal_d_plus_submission_referee/.venv/bin/python`.
It produced the same registry bytes. This virtual environment is execution
infrastructure, not submitted evidence.

## Independent checker command ledger

The following exact rerun commands all had exit status 0:

```sh
python3 -B /Users/alec/Documents/Math/k2p_same_neutral_referee_rereview_2026-08-25/independent_checks/provenance/audit_git_binding.py --repo /Users/alec/Documents/Math --project isolated/k2p_principal_d_plus_submission_referee --project-in-repo k2p_level2_identifiability_closure --revision 83821850e02bc6b6a0383dbc9d3d42ab24a261f5 --revision k2p-same-biorxiv-v1.0.1 --result reports/provenance_git_registry_rerun.json

python3 -B independent_checks/provenance/audit_dependency_binding_v2.py --project isolated/k2p_principal_d_plus_submission_referee --git-audit reports/provenance_git_registry.json --interpreter tmp/execution/k2p_principal_d_plus_submission_referee/.venv/bin/python --output reports/provenance_dependency_registry_current.json

python3 -B /Users/alec/Documents/Math/k2p_same_neutral_referee_rereview_2026-08-25/independent_checks/provenance/audit_artifact_consistency.py --project isolated/k2p_principal_d_plus_submission_referee --result reports/provenance_artifact_consistency_raw_rerun.json

python3 -B independent_checks/provenance/audit_c02_authority_v2.py --project isolated/k2p_principal_d_plus_submission_referee --output reports/provenance_c02_authority_registry.json
```

| checker | real time | maximum RSS | raw output SHA-256 |
|---|---:|---:|---|
| Git/commit/tag byte audit | 4.88 s | 723,894,272 | `d0381229893306b83abca4ddf92e82b5ebff46ff9716ef0c0c72f3573a3fe0b9` |
| dependency/runtime audit | 1.01 s | 76,300,288 | `b1dcce8dd2a9f45e2868215d31c5ebf447389583159589c625d46d357954e6ce` |
| artifact/source/report consistency | 0.93 s | 161,071,104 | `e78b3199656ac3502c239ffc7a699b60dbac0a86ac2c093705ca5af3663c6d3f` |
| C02 authority audit | 0.18 s | 151,650,304 | `d132ebe102ec66719efb100e39724b864d0ca1b910de6aa59fc815555c835205` |

The artifact-consistency value in this table is the raw generated registry.
The normalized registry cited below changes only its stale human-readable
“479” label to the dynamically computed and actually checked value 483.

## File and content ledgers

Independent code `independent_checks/provenance/audit_archive_v2.py`
(SHA-256 `81235c09044d4a9596440fc3464bfa0a659642fe592882145a9119e97d0754b1`)
imports no submitted module.  It reconstructed the closure from the outer
release lock, rank and cycle SHA manifests, the direct closure lock and input
lock, and the outer submission-source policy.  It then checked every ZIP
member against disk and rebuilt the ZIP twice.

Results:

| layer | files | bytes | canonical root / file SHA-256 |
|---|---:|---:|---|
| outer release-lock map | 227 | — | release lock `c319977f350923ab900a883235e32ec945d55a864338c14a08ce266ed3a1c78a` |
| distinct recursively frozen closure | 403 | 478,865,262 | `de6c2f7162164bb460bc608bffefb96b0494965c734c1063f304530a0cc36b82` |
| submission-source layer | 80 | 4,090,352 | `923e8e0741557a013af2b480e4735894833ea4ff792c1e62aefe4f24dd2e0953` |
| outer manifest | 1 | 97,909 | file `bebf82e4d0a406c129d38ceb2433583720bb24f5fea1f6f6ba5a1f05478ef0ce`; payload `1a4b0999d6c7c2cc6f4ff9cb322ab3189f90aa9b4cdf020464d666aa78148c81` |
| complete extracted tree / ZIP | 484 | 483,053,523 | ZIP `ca08a3f50154610c7297ca83f92f0c9517fa5422ac7acf53b89582e1e14edbde` |

The nested raw counts were 95 rank-manifest rows, 17 cycle-manifest rows, 60
direct-lock rows, and 15 input-lock rows; after overlaps, the closure has
exactly 403 paths.  There were no unsafe paths, missing/extra files, symbolic
members, duplicates, encrypted members, non-lexicographic members, timestamp
drift, mode drift, compression drift, or disk/ZIP byte mismatch.  All ZIP
members use prefix `k2p_principal_d_plus_submission_referee`, timestamp
2026-08-25 00:00:00, deflate level 9, and mode 100644.  Compressed member bytes
are 214,683,757; archive bytes are 214,823,405.

Both independent rebuilds are 214,823,405 bytes and have SHA-256
`ca08a3f50154610c7297ca83f92f0c9517fa5422ac7acf53b89582e1e14edbde`,
byte-for-byte equal to the distributed ZIP.  `unzip -tq` also passed (exit 0,
2.52 s, maximum RSS 2,768,896 bytes).  The archive registry is
`reports/provenance_archive_registry.json`, SHA-256
`8e778a81a1e2ad6c0a2ada93d9bc95fd385e775e3b5b88e976c28ce3d9f09434`.

For an exactly timed repetition I ran:

`python3 -B independent_checks/provenance/audit_archive_v2.py --project isolated/k2p_principal_d_plus_submission_referee --archive source_archive/K2P_Principal_D_Plus_Referee_Package_20260825.zip --output reports/provenance_archive_registry_timed.json --rebuild tmp/provenance/rebuilds/rebuild_c.zip --rebuild tmp/provenance/rebuilds/rebuild_d.zip`

It exited 0 in 42.59 s with maximum RSS 632,242,176 bytes.  Both timed
rebuilds are again byte-identical to each other and the distributed ZIP.  The
timed registry SHA-256 is
`55be5239a28ccfd3546ed42175fea768ad0db1b15e4b6d74cce6f07dbc39eba1`.

The copy in `source_archive/` is byte-identical to the file in the author's
named output directory.  The latter has an adjacent external sidecar whose
line is the same ZIP hash and whose own SHA-256 is
`021115cbca75aad96555256203147e05f3eb5ef5f3bb841394e69882413038db`;
`sha256sum -c` passed.  `REFEREE_ARCHIVE_REPORT.json` (SHA-256
`527e22e66c38539241f20f2448933e458bddbdcaee79552e56aea18a95a6c823`)
records the same size, member count, hash, second-build hash, and manifest
roots.  The review staging directory copied only the ZIP, but the actual
source location contains the promised external sidecar.

## Dependency, commit, and tag bindings

The new package intentionally has no `SUBMISSION_BINDING.json`.  Its portable
README maps that legacy name to `work/final_theorem_release/RELEASE_LOCK.json`
and `output/referee/REFEREE_BUNDLE_CONTENTS.json`.  The current outer manifest
has exactly three supplemental execution dependencies, not the five in the
older handoff:

| path | bytes | SHA-256 | in current recursive 403-file frozen closure? |
|---|---:|---|---|
| `output/referee/README.md` | 2,304 | `15571630e9bee72f10ccf5b58caba2fc183533415c4c033a81d4924b29b5a672` | no |
| `output/referee/REFEREE_BUNDLE_CONTENTS.json` | 76,398 | `56d190d412f916c7c88992f8609ebc8686b6dab5d2409fcd1b36feaad67e4286` | no |
| `output/referee/build_referee_bundle.py` | 7,266 | `2989db5f646d8931c64e964be1f17dc2344efd93c57bde517caec60eb1628301` | no |

All three are exact outer-manifest rows and exact at replay commit
`83821850e02bc6b6a0383dbc9d3d42ab24a261f5`.  This dependency audit is in
`reports/provenance_dependency_registry.json`, SHA-256
`b1dcce8dd2a9f45e2868215d31c5ebf447389583159589c625d46d357954e6ce`.

An independent `git cat-file` audit found all 484 package files byte-exact at
annotated tag `k2p-same-biorxiv-v1.0.1`, tag object
`40980e2be87e3d5fcba8ce414f18f821492b099b`, resolving to commit
`57f50ab46cde634b9450c5a01be4b3a12ba5a864`.  The earlier full-replay commit
matches 473/484 package files with no missing package path; the 11 differences
are the subsequently sealed prompt/disposition, crosswalk/manifest, static
audit, and clean-replay report/telemetry artifacts enumerated in
`reports/provenance_git_registry.json` (SHA-256
`d0381229893306b83abca4ddf92e82b5ebff46ff9716ef0c0c72f3573a3fe0b9`).
The five TeX/Bib sources and release lock used by telemetry are exact, and the
final tag binds the complete package.  This is provenance evidence only.

## Article, supplement, source, replay, and lock consistency

Independent artifact reconciliation checked 19 conditions and all 483
declared ledger rows, 159 theorem-crosswalk artifact references, all declared
JSON schemas, canonical payload seals, disjoint evidence layers, release-lock
and telemetry bindings, the exact five-source set, both PDFs and logs, and the
literal `\bibliography`/`\input` relationships.  All passed.  Registry:
`reports/provenance_artifact_consistency_registry.json`, SHA-256
`ad255e97a0ece3864c4bedfd3ee31f83ffed9f959426b559636097575d896c86`.
The reused independent generator's legacy hard-coded check label said 479,
although its dynamic count and the actual loop both used 483; I normalized
that review-registry label after execution and recorded the correction inside
the JSON.  No submitted byte was changed.

Key sealed artifacts are:

| artifact | SHA-256 |
|---|---|
| `work/final_theorem_release/RELEASE_LOCK.json` | `c319977f350923ab900a883235e32ec945d55a864338c14a08ce266ed3a1c78a` |
| `proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json` | `d26ce0841a50ebdc50a5e5d75a25ac2e12d9b647759051c8ceea29d803bd799e` |
| `proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json` | `dc4bd8faafef195a1fd7879b2c8ac7197ebb56cf8fee46c799ab0415b1e3ec08` |
| theorem-artifact crosswalk | `550282c891c3d925f2e06379338f55d7fce6062aeadbaf411fbf45b1374b8d5b` |
| PDF build report | `3471e7eda0e45f998652a3134f15bb31cf18ff583833b2d19e7bf4d7beac2098` |

The stored full report has 40 unique passing layer rows, mode `full`, no
blockers, internal elapsed time 5,428.031056 seconds, and bound external
runtime 5,428.67 seconds / maximum RSS 2,548,498,432 bytes.  These are sealed
historical execution facts, not a fresh replay and not a mathematical premise.

## Independent five-source PDF rebuild

The five inputs and SHA-256 values are:

| source | bytes | SHA-256 |
|---|---:|---|
| article `main.tex` | 85,814 | `983ddc75e568ff9278481c5e43159a9dc566c3dfc9aa1db9c6e31ae6c13c5c3c` |
| `references.bib` | 6,977 | `14dbb4901d924b068c8cc2d050e73bae3cf996a72863a22ade90d6f8e6b4057c` |
| supplement `supplement.tex` | 44,173 | `4166832734f84cd0752f283be6a094249f969e863d084bd11957031f256b8140` |
| `compression_tables.tex` | 3,269 | `22ff0534b79cf226c9041703ab9d87ab123914bbb55ec1d44c84041a8616be81` |
| `certificate_appendix.tex` | 22,405 | `f2444f0308ab2dcccc45dec0704e98b147fffe4bb11fef9ef19cb7f34e688af5` |

The submitted builder check was run in a disposable extraction:

`python3 -B proof_compression_submission/build_submission_pdfs.py --visual-pass --check`

It exited 0 in 19.77 s (maximum RSS 255,983,616 bytes), reproduced its sealed
payload `556ba6792d8dd1e27a3e35d52e306d74d835c1f8d35a49f698039127964dc94d`,
and exercised both missing generated-input gates.

Separately, I copied only the five files to two clean review directories and
ran Tectonic directly with `SOURCE_DATE_EPOCH=1787529600`:

```sh
(cd tmp/provenance/pdf_direct/run_a/article && env SOURCE_DATE_EPOCH=1787529600 tectonic --keep-logs --keep-intermediates main.tex)
(cd tmp/provenance/pdf_direct/run_a/supplement && env SOURCE_DATE_EPOCH=1787529600 tectonic --keep-logs --keep-intermediates supplement.tex)
(cd tmp/provenance/pdf_direct/run_b/article && env SOURCE_DATE_EPOCH=1787529600 tectonic --keep-logs --keep-intermediates main.tex)
(cd tmp/provenance/pdf_direct/run_b/supplement && env SOURCE_DATE_EPOCH=1787529600 tectonic --keep-logs --keep-intermediates supplement.tex)
```

- article A: exit 0, 2.54 s, maximum RSS 253,247,488 bytes;
- article B: exit 0, 3.99 s, maximum RSS 255,541,248 bytes;
- supplement A: exit 0, 1.98 s, maximum RSS 250,396,672 bytes;
- supplement B: exit 0, 3.36 s, maximum RSS 251,035,648 bytes.

The two article PDFs, two article logs, and frozen article PDF/log are all
byte-identical: PDF SHA-256
`9934a92091d069c8764cf8c3aba6b496d482e4e0d5d0a526586f5a0d133f0411`,
log SHA-256
`d243446067dd462d90921ddbb0b5891c1ae4509e3b710f6361f8b5f819dbe5e3`.
The supplement equivalents are PDF
`66161998ec9b30355ac3f6f6467462e8be32230ee52ebf4fbfcaff77fe663866`
and log
`8859def133582903cd3f036af1145c1711581bb41ad9f33b2d6ef77f8a1f722d`.
The supplement log has one nonblocking underfull-hbox warning; it has no
overfull box, undefined citation/reference, PDF-string warning, or fatal
error.  All fonts are embedded.

Direct omission attacks gave the intended results:

- missing `compression_tables.tex`: Tectonic exit 1, 2.38 s, diagnostic names
  that file;
- missing `certificate_appendix.tex`: exit 1, 0.85 s, diagnostic names that
  file;
- missing bibliography: Tectonic itself exits 0 with a BibTeX-error warning,
  so the outer ledger is load-bearing; an independently resealed manifest
  omission is rejected (exit 1) specifically with
  `missing=['proof_compression_submission/article/references.bib']`.

I rendered all 26 article and 24 supplement pages at 90 dpi and inspected both
complete contact sheets.  I found no clipping, blank/missing page, table
overflow, or other visible layout failure.  The rendered contact-sheet hashes
are `a08bed0941f58e66cb743750f5302d0e1e5b01d96a333515caf8b4dd5c6752a8`
(article) and
`44b77ff53d9b2ff4a3fd03eb9c0ad8c9336cbf3a8f2d4d5ce9b86acd6fcac5bc`
(supplement).  This visual inspection is presentation evidence, not theorem
evidence.

## Stale, missing, malformed, and optimized-mode attacks

`test_crosswalk_bundle_mutations.py --check` passed 31 resealed semantic
attacks (exit 0, 7.26 s, maximum RSS 597,491,712 bytes), including C02
overbreadth, erased C02 exclusions, missing bibliography and generated inputs,
missing portable dependencies, stale PDF/full-report bindings, telemetry
source/lock drift, wrong release metadata, and optimized checker/audit mode.
Its sealed payload is
`0492a14d8efc310b4bed1e0d0217f4408ea5e3c827372be366582e7bc047efae`.

I also independently resealed and submitted four manifest mutations to the
current checker.  Each failed at the intended ledger layer rather than a
top-level payload checksum:

| mutation | mutated-file SHA-256 | exit | diagnostic |
|---|---|---:|---|
| omit bibliography | `76c1c834bc33523024f84e3b948c67f3e393a3b65e92b08521cdcd7633dc5e80` | 1 | submission ledger missing bibliography |
| omit portable ledger | `acba2ca5520a8f87d4afc2468f5c82e1287324db51a9fa0c8de73fa5f4c159d3` | 1 | submission ledger missing portable content ledger |
| stale article PDF hash | `aaa9b7f36630af7340b91be511218d78df6c42cbeb73dca46a8dede9a497705d` | 1 | submission ledger mismatch |
| stale full-replay hash | `5037df5143d564d9c13f74ffee74d8518c38b5beccb79dea79fd6680f10d0abe` | 1 | submission ledger mismatch |

The stale-hash diagnostics do not identify the changed path when the path sets
agree; that is a diagnostic-quality issue only, because the semantic ledger
comparison rejects the resealed mutation.

`proof_compression_submission/test_clean_full_replay_telemetry.py` passed 9/9
focused tests (exit 0, 4.67 s, maximum RSS 27,230,208 bytes).  It rejected a
nonpassing or malformed full report, malformed intentional-mutation rows,
wrong commit, invalid lock payload, attached/dirty checkout, unsafe project
prefix, malformed `time -l`, and output drift.  This is submitted-code evidence
using independent temporary fixtures, not an independent implementation of
the telemetry semantics.

Optimized-mode probes found explicit nonzero rejection markers for the
release-lock builder, quick/full harness, release mutation harness, PDF
builder, manifest checker and builder, crosswalk builder and mutation suite,
and telemetry builder.  One current entry point is the exception: the portable
403-file bundle checker accepts `python -O` on a valid package.  It contains
zero Python `assert` statements and no `__debug__` branch.  On a disposable
copy with a bound proof file changed, ordinary and optimized invocations both
failed with the identical semantic diagnostic
`outer lock mismatch: work/domain_rooting_closure/PROOF.md` (ordinary exit 1,
0.50 s; optimized exit 1, 0.47 s).  Thus optimized execution did not turn the
tested failure into PASS, but the README sentence “Every entry point
explicitly rejects `python -O`” is literally false; see P1.

## Previous path-dependent mutation defect: direct retest

Relevant submitted code hashes:

- quartet mutation runner: `84f4adc6b2984a989afc5a864747538b05fefb541207859501739bbf7a043efe`;
- quartet relocation regression: `24eef3408063b021ba1b05080e84bad4524c5e173a0efc7738a65d78bc2a4c1b`;
- outer mutation harness: `b70d17e66fcdb1bda22500e8a61ed716977ab3c6d2a4be64891aa25ed078438f`;
- outer output-contract regression: `819b22ff79bb81986f8c6d2ab6d51bf5ded542462795f0146589b2e12e16016a`;
- nested output-contract regression: `fa751ca8bab7a1d4d7ea004dc011a82dd5c2b453d4a46c5e970d7079016ba0fa`.

Observed attacks:

The two independent source trees were made with
`unzip -q source_archive/K2P_Principal_D_Plus_Referee_Package_20260825.zip -d tmp/provenance/disposable/relocation_alpha`
and the same command with destination
`relocation_beta_with_a_much_longer_name`.  Both exited 0; measured real times
were 5.50/5.46 s and maximum RSS values 2,981,888/2,965,504 bytes.

1. Direct invocation without `--output` exits 2 at argument parsing and writes
   nothing.
2. A routine output path inside the project exits 1 with
   `QUARTET_MUTATION_OUTPUT_POLICY_FAIL` and writes nothing.
3. Direct executions in two differently named clean extractions both exit 0
   in 2.32/2.30 s, report eight attacks and payload
   `4f7bef166b12b41058777cf17eb172605f1d50184fb449f4dd61565c6e48fc2e`,
   and produce byte-identical 2,833-byte reports with SHA-256
   `a1bf423637775b295fb1d6554401352834c59eab326798f7db4753a3855a4a9e`.
4. The dedicated relocation test passes all eight cases (exit 0, 10.30 s,
   maximum RSS 70,041,600 bytes), including path-length independence,
   terminal output policy, canonical override equality, collision, symlink,
   hardlink, and late-symlink safety.
5. The outer v2 output-contract regression passes (exit 0, 0.33 s, maximum RSS
   48,922,624 bytes) with byte-identical two-path report SHA-256
   `a1f01d2ad623d09ca393e0b4e7bfc6b7c80600d4d4d973b948b00e6d7e695cff`.
6. The two nested writers' output-contract regression passes (exit 0, 0.32 s,
   maximum RSS 25,280,512 bytes).
7. A fresh post-test byte manifest of both extractions and the isolated tree
   gives 484 files, 483,053,523 bytes, and the same independently formatted
   manifest root `4cf4cae6057aaae433ca768df531424d7ba0faa5719acffb645283ecb7bfc9a2`;
   there are zero missing, extra, or changed files.

This is strong direct evidence that the earlier source-writing and
path-dependent failure is repaired.

## C02 authority retest

Independent checker `independent_checks/provenance/audit_c02_authority_v2.py`
(SHA-256 `4d5d1b3d235c87d4563fb65d7a7b1b2f881f90d1b67e5030d5f1c4c0f2a31f91`)
imports no submitted module.  It passed 17 exact scope, hash, registry, lock,
forest-census, and supplement-source checks (exit 0, 0.18 s, maximum RSS
151,650,304 bytes).  Registry:
`reports/provenance_c02_authority_registry.json`, SHA-256
`d132ebe102ec66719efb100e39724b864d0ca1b910de6aa59fc815555c835205`.

Current authority is
`work/adversarial_proof_review/topology_direction_certificate.json`, schema
`k2p-displayed-quartet-direction-audit-v2`, 2,148 bytes, SHA-256
`249fdf29ce371e60d7cd8593b98ab0d96759e1ee1e0034af6e1a14e33fb1f7d4`.
The crosswalk role is exactly “raw displayed-quartet graph-direction
certificate; no restoration or whole-map T_i authority”; the certificate
excludes rooted tree/sunlet classification, restoration-child classification,
and whole-map `T_i` classification, and no longer has the old
`published_ledgers` or `restoration_topology_binding` fields.

The stale narrative SHA-256 is
`0c10de904bc233e95c3ff776f9d2ab8e887f2e93fc05362a47039164d8833f1b`.
It remains explicitly discoverable, but its lock layer is
`historical_proof_provenance`; the historical registry calls it
`REVOKED_ROOTED_TOPOLOGY_ORACLE_NARRATIVE` and sets
`promotion_authority:false`.  It is absent from C02 authoritative artifacts.
This is an authority/provenance repair, not by itself a proof that C02 is
mathematically true.

## Current entry points exercised

All ordinary commands below were run in disposable copies.  The first five
were code-inspected before execution.

| command | exit | real time | maximum RSS | result/output hash |
|---|---:|---:|---:|---|
| `python -B output/referee/build_referee_bundle.py --check-only` | 0 | 0.87 s | 225,329,152 | 403 files / 478,865,262 bytes / frozen root PASS |
| `python -B work/final_theorem_release/build_release_lock.py --check --require-ready` | 0 | 10.56 s | 502,988,800 | 227 files, promotion ready, payload `dcc15…` |
| `python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py` | 0 | 0.97 s | 286,425,088 | 403 + 80 files, combined root `ab13…` |
| `python -B proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check` | 0 | 0.77 s | 232,439,808 | manifest payload `1a4b…` |
| `python -B proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py --check` | 0 | 0.49 s | 159,186,944 | 13 claims, payload `c57a…` |
| `python -B work/final_theorem_release/verify_final_theorem_release.py --quick` | 0 | 386.76 s | 1,441,939,456 | 23/23 layers PASS; stdout SHA-256 `ee1ea2d6560df3a74fda6d8373b3be1b022b16999a23bf0ea20f08866d392f71` |
| `python -B work/final_theorem_release/test_release_mutation_output_contract.py` | 0 | 0.33 s | 48,922,624 | stdout SHA-256 `1f2f194e5d4249d6d2a713ec492dcb0a34c1b49ab5cabb85ec5552dca2127029` |
| `python -B work/final_theorem_release/test_nested_mutation_output_contract.py` | 0 | 0.32 s | 25,280,512 | stdout SHA-256 `bbe1d0401efaa645a1a02f6ac04792153e83185b68b4f899f1ea07d5de20700d` |
| `python -B work/final_theorem_release/run_release_mutations.py` | 0 | 971.54 s | 1,423,196,160 | 27/27 gates rejected, zero survivors, payload `b7e1776e44ff5b50f92ed58f8b62d3c15ea49a358819bd8bc9dfac76ebd9df37`; stdout SHA-256 `2aae993baa3c626c0cb1aea54b6b246dc3a910339a3476acf0ff4249d8469037` |

The quick replay is computational evidence using submitted producers and
replayers (several labelled independent by the submission); it is not an
independent proof.  The external archive/ledger, Git, artifact-consistency,
direct Tectonic, path-relocation, and C02-scope checks above are independently
authored review code or direct tool invocations as explicitly labelled.

The ordinary outer mutation command freshly executed all 27 conceptual gates,
including 26 corrected primitive-composite producer mutations (22 are direct
disposable-ledger attacks), and reported zero survivors.  Its exact 484-file
pre/post SHA-256 ledgers are byte-identical, both with file SHA-256
`a995e62e73d2ef2d0f1c9455bec4acab5264cea1b2eeb59d2a178ab1637b3fe5`.
Thus the no-output ordinary command did not modify any package file.

## Findings

### P1 — Nonblocking documentation defect: one entry point accepts `-O`

`work/final_theorem_release/README.md` says “Every entry point explicitly
rejects `python -O`.”  `output/referee/build_referee_bundle.py` (SHA-256
`2989db5f646d8931c64e964be1f17dc2344efd93c57bde517caec60eb1628301`)
has zero `assert` statements and no optimized-mode guard; its clean
`python -O -B ... --check-only` invocation exits 0.  A locked-file mutation is
rejected identically in ordinary and optimized mode, so I found no fail-open
effect.  Severity: presentation/documentation, nonblocking.  Smallest remedy:
either add the same explicit `__debug__` guard used by every other named entry
point and reseal the outer submission layer/archive/tag, or narrow the README
sentence to exclude this assert-free portable checker.  No theorem artifact
needs regeneration; the changed outer package would need resealing.

No other provenance, dependency, source/PDF, archive, path-dependence, C02
authority, stale-input, malformed-report, or release-entry-point defect was
found in this subreview.

## Evidence classification

- **Mathematical evidence:** none claimed by this note.
- **Computational evidence:** fresh ordinary checkers/replayers, mutation
  suites, direct Tectonic compilation, fail-closed output/path attacks, and
  optimized-mode probes.
- **Provenance evidence:** SHA-256/file/byte/path ledgers, archive equality,
  Git/tag comparison, source/report/PDF cross-bindings, and historical/current
  authority partitioning.
- **Presentation evidence:** 50-page visual inspection and P1.
