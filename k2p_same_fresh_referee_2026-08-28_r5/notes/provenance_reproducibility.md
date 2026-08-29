# R5 independent provenance, reproducibility, and document audit

Date: 2026-08-28 (America/Los_Angeles)

Reviewer workspace:
`/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-28_r5`

Read-only package root:
`isolated/k2p_principal_d_plus_submission_referee`

Source ZIP:
`/Users/alec/Documents/Math/k2p_level2_identifiability_closure/proof_compression_submission/output/K2P_Principal_D_Plus_Referee_Package_20260828.zip`

## Status

**REVISED STATUS: document/provenance consistency FAIL; byte integrity and
deterministic reconstruction PASS; release readiness HOLD.** My initial broad
PASS is withdrawn. A follow-up semantic check found that the current reader
supplement calls a 16,974-row whole-map sign overlay the “raw-four terminal
registry,” while the actual 934-class registry is a different bound file. It
also found stale current-language hashes in two release-lock-bound narratives
and in the theorem-promotion companion's frozen-evidence table. These are not
historical/quarantined statements. They do not establish a mathematical
counterexample or corrupt the machine-readable artifact bytes, but they fail
the requested mutual-consistency standard and require correction and reseal
before release. Hash agreement remains provenance evidence only; it is not
used here as mathematical validation.

The two R4 reproducibility blockers are repaired at the interfaces I tested:

1. The complete fresh crosswalk/bundle mutation suite rejected all 37
   mutations. Its coherently resealed conflicting duplicate
   `parent_anchor_id` attack was rejected by both the producer and the
   separately implemented checker for `STRICT_JSON_DUPLICATE_NAME`.
2. The portable optimized-entrypoint matrix rejected both `python -O` and
   inherited `PYTHONOPTIMIZE=1` on all 18 enumerated entrypoints. Its
   false-kernel semantic control was rejected identically in normal, `-O`,
   and environment-optimized modes. The production atlas contains zero
   Python `assert` statements.

## Post-audit correction: semantic artifact identity and stale hash prose

The review-owned
`independent_checks/provenance/semantic_anchor_audit.py` (SHA-256
`6ef84230c3ad349633f6415ab647484917a99f1775f253832dbdaf775fb17df4`)
does not import submitted code. It parses the printed source ranges, reads the
actual artifact schemas and payloads, extracts the submitted static auditor's
declared anchor map through the Python AST, and compares the named narrative
values with current release-lock-bound bytes.

Command:

```sh
python3 -B independent_checks/provenance/semantic_anchor_audit.py \
  --project isolated/k2p_principal_d_plus_submission_referee \
  --output evidence/provenance/SEMANTIC_ANCHOR_AUDIT.json
```

Expected finding exit: 1; 0.54 s; 222,593,024-byte maximum RSS. The result
has SHA-256
`a96b8549a5f77176ba638170c9e549a099c525387a0d3ec6226a69e33cf77de9`,
logical payload
`7966d7b885e32486f3599df05d544d57961e6a1253c8c066736bcf3a8020aa6a`,
status `FAIL`, and 37 independently enumerated semantic/hash mismatches.

### 1. The printed “terminal registry” is a different artifact

`proof_compression_submission/supplement/supplement.tex:780--781` (rendered
on supplement PDF page 21) prints:

```text
raw-four terminal registry
5810ffb1d023e503eaa62d9705c28a85e9c724a6ad8357f49ebe61b2dde675dc
```

That digest is byte-exact, but it belongs to
`work/raw4_sign_reclassification/raw4_corrected_terminal_ledger.json`, whose
schema is `k2p-raw4-corrected-terminal-overlay-v2` and whose
`corrected_rows=16974`. Its own `claim_boundary` says it corrects the 16,974
historical whole-map strict-sign rows. It is not the terminal registry.

The actual object named by the printed label is
`work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz`,
SHA-256
`8d821c2000da5cf2647913cbdb42f8a42dfeb6826b8b76be49d91d78ebaf9998`,
schema `k2p-raw4-terminal-certificate-registry-v1`, payload
`8f41e576ac8551ead8fd75d87c4b8d4aee85f5ba1007c0dcf8aaeb62fbfb1439`,
and `terminal_class_count=934`.

The submitted `audit_article_sources.py:41--42` hard-codes the same wrong
label-to-path association. Consequently its PASS establishes only that the
printed hash matches the hand-written mapping; it does not establish that the
mapped artifact has the printed semantic role. The printed-hash mutations
exercise stale, missing, duplicate, and extra rows relative to that map, but
do not mutate or validate role/schema identity. My prior statement that all
26 printed authority hashes were “exact” was byte-level only and was
incorrectly promoted to semantic document consistency.

### 2. Current lock-bound narratives contain stale hashes

The following current-language values disagree with the located artifacts.
The theta2 ledger file hash `805fc7...` is the one value in both compared
tables that remains current.

| Narrative role | Printed | Current |
|---|---|---|
| raw-four ledger file | `c6cd9d6b5b09371565fd3e58ff9ab3cd7266b6231b153d43f9d1e886af8eae27` | `7cf3f953fca695d612387143818843650498f84f55cf0a776f90c9afdd95eef6` |
| raw-four summary payload | `3a49bfeeb244cba84cf2e42e2acf296f112d1586c5e17f40e2d2872722c3c988` | `92880c7655e6e6d906c0d6dbe2089043289c7496d1d9883a3fdc69f4de2bd331` |
| raw-four replay payload | `dfed35eab33dcc9983b38c8cedb79ed90b12c8a5cf04b58d251637b3fb2f1191` | `6364abb6c504b511700f2256ab044640ae89a1dbba62e6447e73c252e2d8d5bc` |
| raw-four mutation payload | `eec4a56b20faa3239044db49796fa724d60a5412a8d6e89a92db5d81e9656385` | `94b2f2f90ab77eee454bdbf1c5f81b3be8fd0f89d24b45a15bfed6e92f59a04c` |
| theta2 summary payload | `c89dd764f7c66831db7f6a092fedf666a20f3594ef03647de3e85b5fbf04d0e8` | `bdf85d7d02d7a4540da2e9357c948a9e0b30aa799940240323c9d2821d4738d4` |
| theta2 replay payload | `7e4283fe726083927b14d483d55644e2892a311b0179aa70d4766576c66ab545` | `6a3902aaee5f58a0dd45ed1a65d8e5f27cc8bdda6c3999422437f52482256de5` |
| theta2 mutation payload | `5663b87d3f09eaac5e89db69ac5a1cf6069b308abf9bc4242650d0897ded1ff7` | `6395c6a79540fb05fe10fc54b55bf446d09023e2c6107148926a9c8f6848ac80` |
| outer release-replay payload (README) | `607063c6151379818a65f183d5b8b5e528621d39de5b9945550457feed8e3836` | `7e0a0ff894b9476b08dc421b381a09f3dbdb1f4189d6fef4bda2a2f900d489e1` |
| outer release-replay payload (contract) | `b746fb7a17e8ca9252c53dff0ba5722c1a00c56dc930d0c8456022ea34f60b6f` | `7e0a0ff894b9476b08dc421b381a09f3dbdb1f4189d6fef4bda2a2f900d489e1` |
| restoration forest file | `bcf91bf433c71056d1e27871dd15fe532f9ae1cc4ad79eb2373eae57071ee427` | `396d1970af17b5e90c3f1b00ceab1b810816e93ec68a566bd0479f05c722793f` |
| terminal registry file | `0a1818655429d60660c1ed87f3fbe412701f386b081562b3a4caa54079069f1d` | `8d821c2000da5cf2647913cbdb42f8a42dfeb6826b8b76be49d91d78ebaf9998` |
| raw-four uncompressed stream | `cc421e813a2c92da5ebd080003889f93e8dcb3598ba70e92e8655faf8f742f30` | `21637421a9b1a0cd4e62c6333e133b7530fd1ac5a387314069824088c74f2bff` |

The overlapping stale values occur in
`work/corrected_composite_ledgers/README.md:16--22,38--39`; the stream hash is
also stale at lines 95--100. The corresponding frozen-package statements in
`work/final_theorem_release/CORRECTED_FINITE_UNIVERSE_CONTRACT.md:144--181`
have nine stale values out of ten.

An additional independent scan found that Appendix A of
`work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md:912--920`
has 17 stale file/payload entries out of 18; only the theta2 ledger's file
hash remains current. Exact old/current pairs for all nine rows are in the
review-owned JSON result. The crosswalk says this manuscript is a machine-
bound theorem-closure companion, not current submission proof authority, so
this does not by itself invalidate the article's proof. It is nevertheless
current, cited by the supplement, and not quarantined.

### 3. These statements are current, not historical

None of the three narratives occurs among the eight paths in
`HISTORICAL_ARTIFACT_REGISTRY.json`. All three are instead current
`RELEASE_LOCK.json` members:

| path | lock layer | current file SHA-256 |
|---|---|---|
| `work/corrected_composite_ledgers/README.md` | `corrected_finite_universe:corrected_composite_readme` | `f911ccb8117b2b6b1b18360332398ac9ca29b4de06f11e6cacbc52758c9b3821` |
| `work/final_theorem_release/CORRECTED_FINITE_UNIVERSE_CONTRACT.md` | `harness` | `8e4cca6ef964c30a5b9c2c98b7ea58278ef714923af1015ce5dc34bc2a658acd` |
| `work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md` | `theorem_promotion` | `4acacb925f6aab2ee11baf1c08573b65636b7d867fb816142138ae9fe666a3d2` |

The README calls its contents “authoritative” and its replay “current”; the
contract says the authoritative producer package “is now frozen”; and the
promotion appendix says its hashes “are promotion inputs.” Historical log
entries may legitimately retain old hashes, but these present-tense release
narratives cannot be excused that way.

### Severity, remedy, and reseal scope

This is **reproducibility-blocking and presentation/provenance-blocking**, not
theorem-fatal or computational-completeness-blocking on the evidence here.
The machine-readable lock, locator, ledgers, schemas, and current payloads are
internally byte-consistent; the defect is that the documents tell a reviewer
the wrong artifact identity and obsolete current hashes. The scientific
recommendation attributable to this layer is therefore HOLD pending repair,
not REJECT.

The smallest adequate remedy is:

1. Make the supplement row semantically true: preferably keep “raw-four
   terminal registry” and replace `5810ff...` by `8d821c...`, changing
   `PRINTED_FROZEN_ANCHORS` to the actual registry path. If the sign overlay is
   also meant to be printed, give it a separate accurately named row.
2. Add a typed anchor gate that checks the registry schema and
   `terminal_class_count=934`, and a mutation that swaps the overlay and
   registry roles and must fail for a role/schema diagnostic rather than a
   checksum diagnostic.
3. Update every present-tense hash/payload in the corrected-composite README,
   corrected-universe contract, and promotion-manuscript evidence table, or
   explicitly supersede and quarantine a narrative everywhere it is cited.
   Merely leaving a stale hash inside newly sealed bytes is not a repair.
4. Add a generated semantic-hash table or a current-narrative scanner so a
   lock rebuild cannot silently preserve obsolete values.

Because the affected files span both partitions, the reseal is not local to
one PDF. At minimum it requires rebuilding the supplement PDF and
`PDF_BUILD_REPORT.json`; the printed static-audit result and mutations; the
corrected-composite `SHA256SUMS` and locator; the release lock and every
derived release report; the theorem-artifact crosswalk; submission and
combined manifests; bundle contents; and the archive/tag digest. The clean
full-replay telemetry binds the exact five source bytes and release-lock
bytes, so it must be regenerated after those changes. The unchanged large
classification ledgers need not be mathematically regenerated solely because
of this prose correction, but all release validators and required clean replay
gates must run against the new seal.

## Environment

- macOS 26.5.2 (build 25F84), Darwin 25.5.0, arm64.
- Apple M1 Pro, 10 physical/logical cores, 17,179,869,184 bytes RAM.
- Python 3.14.6; NetworkX 3.5; SymPy 1.14.0.
- Tectonic 0.16.9.
- Poppler `pdfinfo`/`pdftoppm` 26.08.0.
- Git 2.38.2.

## Independent byte reconstruction

The review-owned program
`independent_checks/provenance/independent_provenance_audit.py` (SHA-256
`0bd6c53028ab40ee53eb5f8f4f9674cf967024745a0b33e02d1cdc67d13404c2`)
does not import submitted code. It independently implements duplicate-aware
JSON decoding, canonical gzip JSON/JSONL checks, recursive ledger collection,
crosswalk binding checks, ZIP inspection, Git-blob comparison, telemetry
checks, and PDF-build-report checks.

Command:

```sh
python3 -B independent_checks/provenance/independent_provenance_audit.py \
  --project isolated/k2p_principal_d_plus_submission_referee \
  --archive /Users/alec/Documents/Math/k2p_level2_identifiability_closure/proof_compression_submission/output/K2P_Principal_D_Plus_Referee_Package_20260828.zip \
  --git-repo /Users/alec/Documents/Math/k2p_level2_identifiability_closure \
  --output evidence/provenance/INDEPENDENT_PROVENANCE_AUDIT.json
```

Result: exit 0, 146.07 s wall, 445,562,880-byte maximum RSS. Stdout SHA-256
`ac7f45d6b16ff0f76205456ff29f8d4acae6bd17211935f48684550b7aa4b7a7`;
stderr SHA-256
`ee7f2565e52e8e4798f51f8869ea09a41675f35ba545628e538edfd4cae1237a`.
The result file has SHA-256
`da8178e13da9fa24843c99d7fc06d9dbc4e3932e539157a6a2b6088b5ddef931`
and logical payload SHA-256
`e481e0a51550e11627c416d327dd6ce8e060800349cd4ac29537bc870738f0aa`.

### Archive

- ZIP SHA-256:
  `43a620bad862ad14c1b7beb6d605d69354c7da8c534e2882cd7564f7ad4a69db`.
- ZIP bytes: 214,974,312.
- Members: 495 unique regular files; no directories, duplicate names,
  symlinks, comments, encryption, or extra fields.
- Uncompressed member bytes: 483,739,832.
- Compressed member bytes: 214,831,500.
- Every member has the declared prefix, lexicographic order, DOS timestamp
  2026-08-27 00:00:00, deflate compression, Unix mode 100644, and bytes equal
  to the isolated extraction.
- The apparent one-day difference between the fixed member timestamp and the
  August 28 package name is explicitly declared archive policy, not drift.

### Recursive frozen theorem-evidence ledger

- `RELEASE_LOCK.json`: 80,180 bytes; SHA-256
  `305d38e1c3f045bc59141049e46679ccdd29d94c513d5d0e896daa7357ab0b34`;
  payload SHA-256
  `2a8d58662a45c1cb08973b7755a93259e091c0dab4a064891652883cabbf9a0b`.
- Promotion status: `promotion_ready=true`, no blockers, no missing required
  files.
- Direct outer rows: 231 files and 352,113,428 bytes.
- Nested source rows encountered: 94 rank-manifest rows, 17 cycle-manifest
  rows, 60 direct-closure-lock rows, and 16 direct-input-lock rows. After
  deduplication and addition of the release lock, the recursive closure is
  exactly 408 files and 479,382,316 bytes.
- Canonical recursive content root:
  `18555e4d365b5ddef786201c80fc358c620b2ac2200b0f2d677b61378e584dbc`.
- `REFEREE_BUNDLE_CONTENTS.json`: 77,354 bytes; SHA-256
  `d2fabb4e4b7d426811088438cdabb30350f860ed3a8e5a8dd2f376066b6c6fb6`;
  every path, byte count, and digest equals the independent reconstruction.

### Submission layer and combined manifest

- Submission ledger: 86 disjoint files, 4,257,433 bytes, canonical content
  root
  `91ca33df02687e98fddd84809c46ba495ca9121c69e644fcd2f6e676d10192c0`.
- Frozen/submission overlap: zero.
- Combined count excluding the manifest: 494.
- Combined root:
  `df5a19427a9937c0b9350aed2c9968b7ecbb9d7900013b73889350cbc80f9683`.
- `REVISED_REFEREE_BUNDLE_MANIFEST.json`: 100,083 bytes; SHA-256
  `12c627a53a3831bdcf31b23904cc454a8f22b9f6f0a8b4aa8f4ea7c361c2d088`;
  payload SHA-256
  `9cc3f9fada352d3979480de4b79b5e2c39dfa68e70cfb058d4e93d65f48b12f9`.
- The actual extraction is exactly the 408 frozen files, 86 submission files,
  and the manifest itself: 495 files, with no extras, omissions, or symlinks.

### Strict JSON scan

The independent reader checked every bound suffix-governed JSON member:

- 233 plain JSON documents;
- 9 canonical gzip JSON documents;
- 17 canonical gzip JSONL streams;
- 8,601,549 JSONL rows;
- 7,633,642,325 expanded compressed-JSON bytes.

Every object name was unique recursively; every numeric value was finite;
every compressed row/document had canonical sorted compact UTF-8 bytes and
the required terminal LF; all declared size bounds held.

## Authority and historical provenance

The lock and historical registry expose the three claimed disjoint semantic
partitions: authoritative proof inputs, bound runtime evidence, and bound
historical provenance. `HISTORICAL_ARTIFACT_REGISTRY.json` is 7,007 bytes,
SHA-256
`be7873d9f82b9d3c4746ba304bb80ccb6e6e639cfc5a8fe0c40c88cf49c1e19c`,
payload
`0dd650358fc50cdda38605e83a505d0252ed301e619befbbd5bba0b33081d431`.

All eight scanner-listed proof-like historical files are present and
byte-bound, have `promotion_authority=false`, have a `REVOKED_*`,
`HISTORICAL_*`, or `SUPERSEDED_*` classification, and name at least one
present byte-bound authoritative replacement. The registry reports zero
unclassified proof-like files in its declared scanner scope. The
authoritative theorem companion is
`work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md`;
the current submission proof authority is separately the article source.

## Supplemental execution dependencies

The August 28 layout declares three, rather than the obsolete earlier
five-dependency formulation. All three are outside the 408-file frozen
theorem-evidence closure but inside the disjoint 86-file submission ledger,
the combined manifest, the archive, and the annotated tag:

| path | bytes | SHA-256 | tagged Git blob |
|---|---:|---|---|
| `output/referee/README.md` | 2,791 | `2adefc8b448ebcea3a1b89a80de8a90e4f86dada4034fa2dd9e930c49332a3dd` | `e90fb403bf5525ccb0df81f7436f9061f635bb07` |
| `output/referee/REFEREE_BUNDLE_CONTENTS.json` | 77,354 | `d2fabb4e4b7d426811088438cdabb30350f860ed3a8e5a8dd2f376066b6c6fb6` | `7b22f1982c64fe145e9407132f9042fabb39da91` |
| `output/referee/build_referee_bundle.py` | 7,401 | `bc2ece1c2bdf3031c1691f0b21d02ae8f48ae287ff1605cee0bdde4a9a0bb222` | `a4ced3301a45707841a41635518647e0ed4546e8` |

The theorem-artifact crosswalk producer is no longer an unbound fifth
dependency: it is a normal submission-ledger member at
`proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py`,
SHA-256
`9b1546cf7a72ddca3c2f59ee01515efca12a651525bcef976fc81db5cb564338`.

## Source tag and clean replay telemetry

- Annotated tag: `k2p-same-biorxiv-v1.0.4`.
- Tag object: `07dd367e917a9f595db4ff658460cb96715e0777`.
- Peeled tag commit: `2e862d1940078ab3c7516b98d26519c6d1002941`.
- Full-replay commit:
  `0b9cbb6eb0de99ad07142609da47f4db657d3ed7`, an ancestor (in fact the
  direct parent) of the tag commit.
- All 495 package files are byte-identical to the corresponding tagged Git
  blobs. Four executable tagged source files are deliberately normalized to
  archive mode 100644; 491 tagged files already have mode 100644.
- The five TeX/Bib sources and `RELEASE_LOCK.json` are unchanged between the
  full-replay commit and the tagged commit.
- The tag's tracked archive-digest file exactly names the observed ZIP SHA-256.
  The large ZIP itself is intentionally derived/untracked.

Fresh telemetry reconciliation:

- Full report SHA-256:
  `4153c5c3da0566e79e724c744712813dbb4c89d0a7da05ff787cbd3c606331f7`.
- Telemetry SHA-256:
  `fd0b0aa56a44f011dbc94c69ada2774a21609d328905dfc80c30de7f018ae671`.
- 41 full layers, PASS, promotion ready, zero blockers.
- Internal elapsed: 6,259.437869 s; measured wall time: 6,259.77 s.
- Maximum RSS: 2,568,503,296 bytes; macOS peak footprint: 508,969,824
  bytes.
- Runtime: Python 3.14.6, NetworkX 3.5, SymPy 1.14.0.
- Telemetry binds the exact five current TeX/Bib bytes and exact current lock
  bytes/payload.

## Theorem-artifact and printed-document consistency

`THEOREM_ARTIFACT_CROSSWALK.json` has SHA-256
`1430e065692c0c40d6fbd319daf913701ca9fb8bfd6faaaade3457ce5e4b75c5`,
payload
`ed8c4ebbdaf76e20774653801930dff6e6ea50a847bbf11a53718965f91d1f55`,
and status `PASS_PC_PARTIAL`. The 13 ordered claims C01--C13 contain 173
binding rows over 137 unique paths. Every path, byte count, SHA-256, and
frozen/submission flag agrees with the independently reconstructed disjoint
ledgers.

The fresh submitted article-source audit mechanically passed and checked 26
printed authority hashes (8 metadata rows and 18 frozen-anchor rows) against
its own declared path map. The byte comparisons are exact, but the follow-up
semantic audit shows that one map entry assigns the wrong artifact role, so
this command is not evidence that all printed labels are correct. It also
reconciled the current finite censuses, release telemetry, approved metadata,
five sources, generated appendix, and weak-sharpness column crosswalk. Its
stdout SHA-256 is
`b90f4d3ecd74284e58f77ecdc9b10260126ad8a80381eef00ada0bedaffd0022`.

Focused producer/replayers also passed:

- theorem-artifact crosswalk: 13 claims, payload `ed8c4e...`, 0.43 s;
- printed appendix: 23 quadratics, 5 high-degree bases, 36 transports, 36
  four-port and 52 five-port coordinates, 3 worked examples, 12.31 s;
- weak-sharpness column crosswalk: exact named columns 0--8 for both graphs,
  0.31 s.

## Archive rebuilds

The review-owned archive builder
`independent_checks/provenance/independent_archive_rebuild.py`, SHA-256
`de4c44a2ab9991fa7ffad1ce727f43ad418b5626df0030d9f7f0a194b1f58483`,
does not import submitted code. Two simultaneous rebuilds in separately named
review scratch directories both produced 214,974,312 bytes and SHA-256
`43a620...`. `cmp` returned zero for rebuild A versus B and for rebuild A
versus the source archive.

- Rebuild A: exit 0, 21.08 s, maximum RSS 273,842,176 bytes.
- Rebuild B: exit 0, 21.07 s, maximum RSS 272,596,992 bytes.
- Evidence file:
  `evidence/provenance/INDEPENDENT_ARCHIVE_REBUILDS.json`, SHA-256
  `eabcf286a49e2d9072e57403894c33662beafc88416e0a30e34946da22286b22`,
  payload
  `139c840c9b1e260ee8bb196217e13b1d0d410cbbed36b51a4f073bae8ae57f69`.

The two derived temporary ZIPs were deleted only after hashes and byte
comparisons were recorded. They are reproducible and contained no unique
evidence; the source ZIP and all logs remain.

## R4 repair attacks

### Strict JSON

Fresh command:

```sh
.venv/bin/python -B \
  proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py \
  --check
```

Result: exit 0, 3,884.99 s, maximum RSS 391,577,600 bytes; 37/37 mutations
rejected; payload
`0217ccc3cfdcb9f3142257aadf1ea0725f532e2389085b1df211c99cc031dfeb`.
Stdout SHA-256
`7be72305124618ad1739b165e5c62c23d818111a3d5e01a0d60cebb8caca2826`;
stderr SHA-256
`a1e91ee7e6ee5a98efa5d86892527b8852ed5ecb93f6634eeadef5b4d4341125`.

The fresh run includes valid outer reseals, hard-linked clean projects, both
complete bundle programs, exact diagnostics, and these relevant cases:

- same-valued duplicate plain JSON name: rejected by producer and checker;
- conflicting duplicate plain JSON name: rejected by producer and checker;
- same-valued duplicate compressed JSONL name: rejected by both;
- conflicting duplicate compressed JSONL `parent_anchor_id`: rejected by
  both for `STRICT_JSON_DUPLICATE_NAME`;
- noncanonical compressed JSONL: rejected by both for
  `STRICT_JSON_NONCANONICAL_BYTES`;
- omitted bibliography and each of the three supplemental execution
  dependencies: rejected for the intended missing-ledger member.

The focused shared-parser suite separately passed 2 clean documents and 17
syntax/canonicality mutations in 0.04 s.

### Optimized entrypoints and assert removal

Fresh command:

```sh
.venv/bin/python -B \
  package/referee/k2p_offline_sweep_portable/test_optimized_entrypoints.py
```

Result: exit 0, 2.86 s, maximum RSS 151,076,864 bytes, terminal marker
`K2P_PORTABLE_OPTIMIZED_ENTRYPOINT_MATRIX_PASS`. Stdout SHA-256
`4b25654b34ece9abe5f14dfca1da1a45bde74507d37c88b21e8a59c6a9593e46`;
stderr SHA-256
`7f3c3335ded4f01a9b119a2239b6b62a762bc9651916ef3745ffb0e10a4dd8a5`.

Independent AST inspection found 18 enumerated portable entrypoints and zero
`ast.Assert` nodes in `atlas/k2p_atlas_core.py`. The test attacks all 18 with
both optimization mechanisms, forbids residual output, fingerprints the
package before/after, and runs the false-target-kernel control in three modes.

## PDF/source/build consistency

The exact five source files are:

| source | SHA-256 |
|---|---|
| `article/main.tex` | `20387611077cf1bfb128456e523b34f46c5a98537c6bbf6ddb5436911f8c9dec` |
| `article/references.bib` | `781dd3503c00d9bbd9c1a7d551786fc4be393e883f7ac4c0b0fd712943a9e5c6` |
| `supplement/supplement.tex` | `adccd175bfff5707d0d4d938287040636e40bd4071e64716292a5c03b003b631` |
| `supplement/compression_tables.tex` | `22ff0534b79cf226c9041703ab9d87ab123914bbb55ec1d44c84041a8616be81` |
| `supplement/certificate_appendix.tex` | `1f7590b2930f8ac1536724763d0b30e330f817fd3127edae0df3ee520180c649` |

`PDF_BUILD_REPORT.json` is 2,102 bytes, SHA-256
`6bd098c65d59a889dcdda28342c0a5954c1fea53d7e3521809ee9bfefb30afd4`,
payload
`a3c6b81b053be86811d56bb763a8a139c4d5e03cdf78a06da36887b2aa982d46`.
Its source set, source hashes, output hashes/bytes/pages, log hashes, engine,
epoch, and status all match current bytes. The submitted builder's fresh
`--visual-pass --check` completed with exit 0 in 13.93 s and reproduced that
payload exactly.

I staged only those five source files into each of two review-owned scratch
trees and compiled both documents in each tree with Tectonic 0.16.9 and
`SOURCE_DATE_EPOCH=1787788800`:

| build | document | exit | seconds | max RSS bytes | output result |
|---|---|---:|---:|---:|---|
| A | article | 0 | 3.15 | 249,020,416 | byte-identical to B and authoritative PDF/log |
| A | supplement | 0 | 2.51 | 245,596,160 | byte-identical to B and authoritative PDF/log |
| B | article | 0 | 3.09 | 250,249,216 | byte-identical to A and authoritative PDF/log |
| B | supplement | 0 | 2.46 | 250,003,456 | byte-identical to A and authoritative PDF/log |

Outputs:

- Article: 194,515 bytes, 26 letter pages, PDF 1.5, SHA-256
  `186522a14070fc872e67e75736804fa14621104803225f73615d7f76d09f9a11`;
  22/22 font rows embedded.
- Supplement: 160,293 bytes, 24 letter pages, PDF 1.5, SHA-256
  `5ea090740046fbafa0c10b9397e610be8584d49dbf8cd560d190e24420e344f2`;
  28/28 font rows embedded.
- Both are unencrypted, contain no form or JavaScript, and extract readable
  title, theorem-scope, census, PC-PARTIAL, and hash-anchor text.

Omission checks in separate review scratch trees behaved fail-closed:

- Removing `compression_tables.tex`: exit 1 in 1.43 s with the exact missing
  file at `supplement.tex:319`.
- Removing `certificate_appendix.tex`: exit 1 in 1.39 s with the exact missing
  file at `supplement.tex:453`.
- The fresh 37-case outer mutation run rejected omission of
  `article/references.bib` for the intended submission-ledger mismatch.

All 50 pages were rendered at 90 dpi and inspected in complete contact sheets;
dense/table/figure pages article 15, 16, 23, 24 and supplement 10, 14, 19, 21
were additionally inspected at full rendered size. No clipped, overlapping,
missing, corrupt, or unreadable content was found. The logs contain zero
fatal errors, overfull boxes, undefined citations/references, or hyperref
PDF-string warnings. The supplement retains one harmless underfull hbox
(badness 1817, source lines 843--856); it creates no clipping or ambiguity.
The derived PDF builds and PNG renders were deleted after their byte hashes,
comparison results, and visual verdict were recorded; no authoritative PDF or
source file was deleted or changed.

This layout/source-byte PASS does not cure the semantic anchor defect: the PDF
faithfully reproduces the erroneous source label/hash pair on supplement page
21. Visual readability and deterministic compilation are distinct from the
truth of the printed provenance statement.

Review-owned PDF evidence:

- `independent_checks/provenance/pdf_source_consistency_audit.py`, SHA-256
  `ed25bac34265f9978dae53c68e0da12fcf372d900c5d92db28f90deb75f792d6`.
- `evidence/documents/PDF_SOURCE_CONSISTENCY_AUDIT.json`, SHA-256
  `48ed02d95f19631f4e2562f3da795eba775bc284d8357562d9134af1675ba81b`,
  payload
  `84cae8559368c01131d908799a5b04f63385b0c2584ebc1406829e1bbd9758b6`.
- `evidence/documents/PDF_REBUILD_VISUAL_RESULT.json`, SHA-256
  `65ac9f6add5f99a1bc6d5800acc8e3cbaadbaa1b94774ffdb598d1613aed59d5`,
  payload
  `b17a7da731bf595e7cad406f9422a538bcb17d6b579a664c5b555e964ddae4ef`.

## Submitted checks executed after code inspection

| command | exit | seconds | max RSS bytes | stdout SHA-256 |
|---|---:|---:|---:|---|
| `python3 -B output/referee/build_referee_bundle.py --check-only` | 0 | 0.64 | 230,703,104 | `dc6c0926ed937e24ceb37058eb76ac13d92766a8bec912bf5ab0dcfb66b302dd` |
| `.venv/bin/python -B work/final_theorem_release/build_release_lock.py --check --require-ready` | 0 | 16.91 | 509,837,312 | `58fb9da56b6d1d045d3b0df9a1899f76d67be2e8022bb12f230fc39d51b636d6` |
| `python3 -B .../build_revised_referee_bundle.py --check` | 0 | 127.67 | 272,596,992 | `1fc00d24feab80f4d8a86ab240df1be8d652cf8f611156f5bb4cca61b94d327d` |
| `python3 -B .../check_revised_referee_bundle.py --manifest ...` | 0 | 129.37 | 268,173,312 | `1fc00d24feab80f4d8a86ab240df1be8d652cf8f611156f5bb4cca61b94d327d` |
| `.venv/bin/python -B .../audit_article_sources.py --check` | 0 | 0.74 | 42,631,168 | `b90f4d3ecd74284e58f77ecdc9b10260126ad8a80381eef00ada0bedaffd0022` |
| `.venv/bin/python -B .../build_theorem_artifact_crosswalk.py --check` | 0 | 0.43 | 176,734,208 | `998285a0dc40880457565f2bc8316aa6910a8205992a46899de702b601061ff5` |
| `.venv/bin/python -B .../verify_printed_certificate_appendix.py` | 0 | 12.31 | 162,889,728 | `74c2e8f13a3cd35b4a6556826388ae87c416a382812f0e048579843fe9729c61` |
| `.venv/bin/python -B .../verify_weak_sharpness_column_crosswalk.py` | 0 | 0.31 | 44,695,552 | `08119dce7f8892abd89c1a3ca73da91f8e3d1c83c3da76b4424eb9332ce3f550` |
| `.venv/bin/python -B .../build_submission_pdfs.py --visual-pass --check` | 0 | 13.93 | 254,476,288 | `f60d5968b6f14c8a2e6bd2da28bc6ff9588d91048cca9ffb3dde488d0bc60898` |
| `.venv/bin/python -B .../test_crosswalk_bundle_mutations.py --check` | 0 | 3884.99 | 391,577,600 | `7be72305124618ad1739b165e5c62c23d818111a3d5e01a0d60cebb8caca2826` |
| `python3 -B .../test_strict_json.py` | 0 | 0.04 | 19,333,120 | `5efaf2b222f7ecaed14101d4a552a2320591b9faf89eeccf4ac424b3d60ec344` |
| `.venv/bin/python -B .../test_optimized_entrypoints.py` | 0 | 2.86 | 151,076,864 | `4b25654b34ece9abe5f14dfca1da1a45bde74507d37c88b21e8a59c6a9593e46` |

The bundle producer and the separately implemented checker agree on the same
counts and roots, but their agreement was not used in place of the independent
byte reconstruction above.

## Scope and unrun gates

- Per delegation, I did **not** invoke the global quick/full theorem harness
  or the 25-case final release mutation harness; those are assigned to the
  root/computational review and must not be inferred PASS from stored reports.
- I did not write or reseal any authoritative file. All source-building and
  rendering occurred in review-owned scratch or the disposable execution
  clone; the isolated package remained byte-identical to the source archive.
- I did not contact any person or perform any external release action.
- I verified the local annotated tag object and commit graph, but no signed-tag
  or remote-host availability claim is made. No GitHub Release, Zenodo deposit,
  or DOI is claimed by the package.
- The PDFs were checked for byte reproducibility, source binding, parseability,
  embedded fonts, extracted text, and visual layout. Those checks do not by
  themselves validate the mathematical arguments printed in the documents.
