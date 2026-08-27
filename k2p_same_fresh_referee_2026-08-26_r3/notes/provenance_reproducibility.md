# Fresh integrity, provenance, and reproducibility audit

Date: 2026-08-26 (America/Los_Angeles)  
Scope: `K2P_Principal_D_Plus_Referee_Package_20260826.zip` only  
Evidence classification: this report concerns provenance and reproducibility. Hash agreement is not treated as mathematical validation.

## Status

**Integrity of the bytes actually distributed: PASS.** Every declared path,
byte count, SHA-256, canonical content root, transitive release-lock member,
archive member, source-tag blob, PDF output, and stored replay/telemetry binding
that I recomputed agrees exactly.

**Reproducibility/fail-closed status: HOLD.** I found two theorem-neutral but
submission-blocking defects:

1. The supplement prints the pre-repair SHA-256 for one current sealed artifact
   twice. The standard source, PDF, release-lock, crosswalk, replay, and bundle
   checks all pass without detecting this false reader-facing anchor.
2. Both submitted outer-bundle checkers accept and reseal a JSON report with a
   duplicate object name. The current archive contains no duplicate-key JSON;
   this is a fail-closed mutation defect in the producer/checker surface.

Neither finding changes a certificate body, finite census, graph, proof, or
theorem implication. Both prevent a clean reproducibility PASS under the
requested protocol.

## Review isolation and environment

I inspected builder/checker code before running it and did not import package
modules in the independent ledger, Git-binding, printed-hash, or strict-JSON
checks. The shared nominal `isolated/` extraction acquired unsealed `.pyc`
files from concurrent read-only reviews, so it was not used as evidence. I
instead audited a fresh disposable extraction at
`tmp/provenance_r3/extract_a/k2p_principal_d_plus_submission_referee`. At the
time of the complete extraction-set/ledger audit it contained exactly the 489
archive files and no symlink. A disposable `.venv` was added only afterward;
it was excluded from later source inventories. No authoritative packaged file
was repaired.

- macOS 26.5.2, build 25F84; Darwin 25.5.0, arm64.
- Apple M1 Pro, 10 physical/logical cores; 17,179,869,184 bytes RAM.
- Python 3.14.6; NetworkX 3.5; SymPy 1.14.0.
- Tectonic 0.16.9; Poppler `pdfinfo`, `pdffonts`, and `pdftoppm` used for PDF QA.
- No person was contacted.

## Archive and outer/inner ledger audit

Source archive:

- bytes: **214,930,375**
- SHA-256: `86a286be82ce3c211f556eaa24cf1120aa42e41f716b46cb8752c1d2546053ba`
- sidecar contents agree; sidecar file SHA-256:
  `66866f88876f8f02990da18649ffa6a1c217588f334d2da291f0c76f633510e7`
- 489 members; 483,608,160 uncompressed bytes; 214,789,263 compressed data
  bytes; no duplicate member, directory member, symlink, or archive comment.
- member paths are lexicographically ordered; every timestamp is
  `2026-08-26 00:00:00`; every mode is `100644`; `create_system=3`; every
  member uses deflate.
- `unzip -t`: exit 0, 2.70 s, no errors. Stdout SHA-256
  `dcb909a56fc4976aa8baa7786a5d5f8be88653ff2f978c0b724e31f089c22476`;
  timing/stderr SHA-256
  `3a517883c2353a5556125f7a324f2cb6ba2f14396da656b8fd6d1f6ecf2aa194`.

The independent checker
`independent_checks/provenance/independent_bundle_audit.py` (SHA-256
`6d884a360d6a911fc50935d5e2053716cac959070ffa08d99076c6a21bd20c0a`)
uses its own path validator, strict duplicate-key JSON loader, byte hasher,
canonical-JSON root computation, nested-manifest parser, and ZIP reader. It
imports no submission module. It checked every declared row and required the
physical extraction set to equal the declared set. Exit 0 in 2.22 s; result
SHA-256
`39a46ef34d93d0801d763c98055dac823aa4fde512005a2281f96085853eda2e`.

Exact independently recomputed ledgers:

| layer | files | bytes | canonical root / file SHA-256 |
|---|---:|---:|---|
| frozen transitive evidence | 406 | 479,324,605 | root `d4385855fd9d8387080a8e789613114f047fd93aaad9a78e86924d1a29b25c3e` |
| submission sources | 82 | 4,184,639 | root `72b8df4f4d2c015d219f48960b0cba5e64e6aa0b5d9d34fa4f9b5f4a5950d45e` |
| combined, excluding manifest | 488 | 483,509,244 | root `a3aff0653f5593c3320e6c13c2e06d0e7a3896129123eb48f043c56aa93f3b16` |
| revised manifest itself | 1 | 98,916 | file `c65d4c7ce4d094f7d1e85ecfea2604c5948c345c11f9fb726505301d898f5fc2`; payload `f25590c4a20e1c7c0a05c9d0344b7dfaff640427497ba078ca2e27ffabb57c40` |
| portable content ledger | 406 | 479,324,605 | file `eef2202e6f3ec18f54835230f0d994a17693e1204ca4d5ae64c7a8d58e17b9e8`; same frozen root |

The 406-file frozen closure was independently reconstructed, rather than
copied from the portable ledger:

| partition | declared files | raw bytes | new files after earlier partitions | new bytes |
|---|---:|---:|---:|---:|
| release-lock outer map | 230 | 352,069,291 | 230 | 352,069,291 |
| rank manifest | 94 | 3,706,507 | 92 | 2,124,400 |
| cycle manifest | 17 | 5,559,818 | 13 | 5,520,703 |
| direct-closure lock | 60 | 9,471,082 | 57 | 9,296,267 |
| direct-input lock | 15 | 110,285,757 | 13 | 110,233,955 |
| release lock itself | 1 | 79,989 | 1 | 79,989 |

Pairwise overlaps are exactly: outer/rank 2, outer/cycle 4,
outer/direct-closure 3, outer/direct-input 2; all other nested pairwise
overlaps are zero. The union is exactly 406 files and 479,324,605 bytes. The
release lock file SHA-256 is
`130642e235c9beaa22061c578c3c645244cdbf45a9b416d45d94492b3d2848bd`;
payload
`b5eb26e953fbb76de671a4caa0db3068932af1e23b4fffdb0d118b5939f81756`.

After code inspection, the submitted checks also passed:

| command | exit / runtime / peak RSS | result and output hash |
|---|---|---|
| `.venv/bin/python -B output/referee/build_referee_bundle.py --check-only` | 0 / 0.46 s / 231,636,992 B | 406 files, 479,324,605 B; stdout `468aedd20bce6c1e99b4fbc7a0ec87bd227786c7d531e2341692da680a4cbcef` |
| `.venv/bin/python -B work/final_theorem_release/build_release_lock.py --check --require-ready` | 0 / 9.93 s / 516,947,968 B | 230 files, ready, zero blockers; stdout `20b3a276c444b271006edef1fb3b7a923a7cfc6d1d13b6a379c3ec615d04244c` |
| `.venv/bin/python -B proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check` | 0 / 0.81 s / 229,539,840 B | PASS; stdout `b52b015e43b75dd3d99c11024afa601b8a8a91a15cfa0fe705ad497b5cf1db0b` |
| `.venv/bin/python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py` | 0 / 0.69 s / 292,454,400 B | PASS; same stdout hash |

## Deterministic archive rebuild

I ran the inspected outer builder with `--check --archive` three times to three
new output names. Rebuild A took 20.65 s; B approximately 21 s; C 20.92 s.
Each was exactly 214,930,375 bytes and had SHA-256
`86a286be82ce3c211f556eaa24cf1120aa42e41f716b46cb8752c1d2546053ba`.
Byte comparisons source/A and A/B both returned zero. Metadata is sealed in
`tmp/provenance_r3/rebuild_metadata.md` (SHA-256
`0c03dd62ffcbc8f367e8ab960559e09e4220b638a0853a5735cb94c5d35ccacb`).
The three explicitly named disposable 205 MiB rebuilds were then deleted to
preserve disk; their hashes, sizes, completion times, and comparisons remain.

## Git, tag, and historical supplemental dependencies

Current repository state at audit time:

- `main`, HEAD and `origin/main`:
  `a011a4e0322e3dd4cb11b5dfa41026db15695d95`.
- annotated tag object `ae537c7e2dacdc1026b30b65fe04daca57b4fd84`
  (`k2p-same-biorxiv-v1.0.2`) points to commit
  `cb7559e0ba5fd72f94bce5941208be0838be878d`.
- `git diff tag..HEAD -- k2p_level2_identifiability_closure` is empty.
- untracked older/current derived ZIPs and `work/four_port_rebind_20260824/`
  are outside the tag and archive ledgers.

Independent blob comparison checked all 489 packaged files against the tag
commit: zero missing and zero differing. It separately checked the frozen 406
files plus the five replay-bound TeX/Bib sources (411 total) against telemetry
commit `f6befbce38cfb21e27b8dc4a9611d284fdcbc800`: zero missing/differing. Tool
SHA-256
`20888d46b34f9cd06d5baaf80f1ff5d847e5ba7691792aa57e5b08bccb62d9bb`;
result SHA-256
`edef15443c29109824e94ac9d6b0eeecf1379c74a060ba72d4731fef25775332`;
runtime 19.85 s.

The five supplemental dependencies named by the superseded 23 August
`SUBMISSION_BINDING.json` were also reconciled. The current release explicitly
replaces that interface with `RELEASE_LOCK.json`, the portable ledger, and the
current crosswalk. Thus only the content ledger remains an outer source; the
four legacy top-level certificate paths are intentionally absent from this ZIP.

| historical path | 23 Aug bound SHA-256 | current source SHA-256 / last content commit | current-package disposition |
|---|---|---|---|
| `output/referee/REFEREE_BUNDLE_CONTENTS.json` | `5799d8f3127a3d1e43f28610a3753a3da2a2a0de5c021ce45efc5665058d24bd` | `eef2202e6f3ec18f54835230f0d994a17693e1204ca4d5ae64c7a8d58e17b9e8` / `f6befbce...` | present; required by the current theorem-artifact crosswalk producer |
| `work/four_port_direct_residual_closure_certificate.json` | `fb6e5f1c23c8c3291ddc8c822171cae9c2df05b0d449249813b40e958e17bddc` | same / `2474e2b8...` | legacy top-level path absent; current inner authority is `9dc3f112...` |
| `work/theta0_quintic_orbit_certificate.json` | `f863afd5875a74be818141990863344fae09fd4269a803d3a1bfeb67a8a595e0` | same / `2474e2b8...` | legacy top-level path absent; current inner copy remains byte-identical (`f863afd5...`) |
| `work/theta3_cubic_obstruction_certificate.json` | `fb1512e260b5a88b5ac3a4b55d6c756e401baebd08866d6e39bb2153b63aa4d8` | same / `2474e2b8...` | legacy top-level path absent; revised inner authority is `d1501a7e...` |
| `work/theta_quartic_obstruction_certificates.json` | `5204593fb2b47914dbdf2d7846d1e9fbd5671fa9f29e89862d29b16a45bb08db` | same / `2474e2b8...` | legacy top-level path absent; revised inner authority is `11270043...` |

The historical binding correctly recorded exactly two byte-identical older
inner copies (theta0 and theta3) at checkout commit `078b573d...`. In the
revised current seal theta3 has changed, so only theta0 remains identical to
that historical outer byte string. This is version evolution, not a missing
current dependency.

## PDFs, exactly five sources, dispositions, and replay telemetry

The five declared source files and current SHA-256 values are:

| source | bytes | SHA-256 |
|---|---:|---|
| `article/main.tex` | 85,827 | `d64574e30ef3dac38c91613938a6ce29f7b07688ea791013c56a45e9af0e75c3` |
| `article/references.bib` | 6,992 | `d1b3b50f6e276cc147471dcab9f30ed3a9b629fddc19ffb7fea58d427ee5de6b` |
| `supplement/supplement.tex` | 46,057 | `7b28e0ff620b24256f4eebe61fc233dc21df8ffd7b4b552b51eb579712358bc4` |
| `supplement/compression_tables.tex` | 3,269 | `22ff0534b79cf226c9041703ab9d87ab123914bbb55ec1d44c84041a8616be81` |
| `supplement/certificate_appendix.tex` | 22,405 | `936e8d1879acd224affb053489a618dcfe8d7a7a2a5500bc8f0f85dd1b16794d` |

Source inspection found only the two unconditional supplement inputs (source
lines 319 and 453) and the shared bibliography; no external figure, class, or
style asset is required. The inspected builder stages only these five files.

`.venv/bin/python -B proof_compression_submission/build_submission_pdfs.py
--visual-pass --check` rebuilt article and supplement twice in isolated
temporary trees, compared both paired outputs byte-for-byte, ran both omission
gates, and compared PDFs, logs, JSON report, and Markdown report with the
sealed copies. Exit 0, 26.94 s; stdout SHA-256
`6617d0c7d4e5e6c9ad6a63dbc65be5729271c81894cb2eeec3aeb3d1c7a304f0`;
timing/stderr SHA-256
`c382723d7b3a8b3e4625549df4e28e2af530cc5ab92f5017aed2ba1826fa77ad`;
report payload
`d3b3095fb009e0b10870cd8afd04e7948a16c0d2c225c1ecd0989f61beceadaf`.

| PDF | pages | bytes | SHA-256 |
|---|---:|---:|---|
| article | 26 | 194,327 | `2bca627d072cf96c850a7196be9101a7e061499bbcc61ebbb8ff256d4bf864b9` |
| reader supplement | 24 | 160,133 | `4bdcfe32cf3dbcd586d9bf68f3d287e4f5f58aa3384aa5daaf454fde3e361621` |

Article log SHA-256 is `094b5b7665ab9f440ceeebad9850a02f7b57effd9c77bab43d12b1fa09d51812`;
supplement log is `2c282eaa142e3c4c5594a3f83b543c8a2c6f2c4c03697688a49cc1f3fc2928da`.
No fatal error, undefined citation/reference, hyperref PDF-string warning, or
overfull box was found. All fonts are embedded. Both are unencrypted letter
PDF 1.5 files. Using the PDF review workflow, I rendered and visually inspected
all 50 pages; no clipping, overlap, broken glyph, table overflow, or page-order
defect was observed.

Direct omission attacks, independent of the report booleans:

- omit `compression_tables.tex`: Tectonic exit 1, 3.69 s,
  `supplement.tex:319: File 'compression_tables.tex' not found`; log SHA-256
  `b5438bbab8a6434f0d6ecfd83740ec5f2dd3e12047eabedcab532d72602a87d5`.
- omit `certificate_appendix.tex`: Tectonic exit 1, 3.19 s,
  `supplement.tex:453: File 'certificate_appendix.tex' not found`; log SHA-256
  `d01a43d7fe0dbf743e3f7a92a339138ce7cc6e40f45f40624271d7b07689d52f`.
- physically omit `article/references.bib`: outer builder exit 1 with exact
  diagnostic `required submission source missing: ['proof_compression_submission/article/references.bib']`.

The PDF report file SHA-256 is
`6521cdc5ad43288ec928db747d19ab6e944ef0182cd726da021693ed582c6349`;
Markdown report `9498966c...`; feedback disposition `e489f180...`; current R2
disposition `456d6201...`; historical fresh-review disposition `73c20f67...`.
The R2 disposition's current lock, 41-layer replay, mutation, PDF, and runtime
figures agree with the sealed machine files.

Stored replay/telemetry (provenance evidence only; not inferred as a fresh
mathematical PASS by this audit):

- full replay report: 41 unique PASS layers, 40 return-code-zero commands plus
  one expected nonzero omission attack, zero blockers, internal 5,696.744942 s;
  file SHA-256
  `2489643d65c50f662d027bf5002b9f398c8fa2999d7a17fcf43a5334cb04e86e`.
- telemetry: detached clean commit `f6befbce...`, wall 5,697.15 s, maximum RSS
  2,552,119,296 B, peak footprint 506,856,192 B, exact report/lock/five-source
  bindings; file SHA-256
  `b0f379d5e9d7e3acfd4c9812711964c4f7894dfd15e28045eab8077a9e6bd18f`.
- final mutation report: 25/25 rejected, zero survivor; file SHA-256
  `f2a362e9d2606b0315f9fe6e5a7659d328bd73bcf6552f0c1cc4c4f8ecdd0026`,
  payload `05475591...`.

## Finding P1: stale reader-facing artifact SHA-256

**Classification:** reproducibility-blocking; presentation/provenance; no
mathematical effect.

`proof_compression_submission/supplement/supplement.tex` identifies
`work/final_theorem_release/composite_reseal_diff_audit.json` and prints
`bc91fee3b7541fcae72c4db2e66776fbfc69c43890718239f0eea41bb2cc0654`
at hash line **755**, then repeats it in the frozen-anchor table at hash line
**793** (row labels begin at 754 and 792). The rendered supplement contains
the same false anchors on PDF pages 20 and 21. Direct SHA-256 of the packaged
file is
`96e30bae42939fa50dd585ba900bc5bd45e5eb122334de86c34654004212db4c`,
which agrees with the release lock and current crosswalk.

Git gives an exact derivation: the printed value is the file hash at commit
`e9c68e2b...`; commit `488e8f53...` (`Fix stale composite reseal binding`)
changed that artifact to the current `96e30...` bytes. The prose anchors were
not updated.

An independent parser checked 23 printed authority/frozen-anchor rows. Exactly
these two presentations of the same file failed. Command exit 1 in 0.24 s;
checker SHA-256
`d9fd06c302fa1d3e3d0fb233296adea009eaa3346e0edd87bbc148d7be3227c7`;
result SHA-256
`3d5ec99f0b2de74518e67e0d53ee50821dc2d4aa4e8806c5a4291d7619492e02`;
payload `03bff60b...`.

**Do standard checks catch it? No.** With the stale value present, the PDF
double-build/check, static source audit (zero findings), portable-ledger check,
release-lock check, outer builder, outer checker, and stored/full replay all
pass. The 31-case crosswalk mutation suite has a useful
`false_supplement_pdf_hash` attack, but that mutates the manifest's PDF byte
hash; it never compares artifact hashes printed inside the TeX/PDF. Thus a
validly sealed source can make a false artifact claim.

**Smallest remedy:** replace both occurrences with `96e30...` and add the
independent printed-hash comparison (or equivalent strict mapping) to the
normal source/release gate. Rebuild the supplement PDF and logs, PDF report,
static source audit, theorem crosswalk, outer manifest, tag, and archive. Under
the package's present source-bound telemetry policy, changing
`supplement.tex` also requires a new clean full replay/telemetry binding (even
though the change is theorem-neutral). The frozen release lock need not change
unless its own file set/content changes.

## Finding P2: duplicate JSON object names survive a legitimate reseal

**Classification:** fail-closed reproducibility blocker; current bytes are not
corrupt; no mathematical effect.

The independent mutation
`independent_checks/provenance/test_outer_fail_closed.py` lines **115--135**
inserts a second top-level `"status": "PASS"` at mutated
`PDF_BUILD_REPORT.json` line 2 (the original current key is line 43, shifted to
44 in the mutant). It then uses the submitted builder's supported `--write`
operation to reseal the changed raw bytes before invoking both submitted
checks.

Observed in a disposable copy:

- outer builder `--write`: exit 0;
- outer builder `--check`: exit 0/PASS;
- nominally independent outer checker: exit 0/PASS;
- mutated combined root:
  `5d2837ecde6030faef677c524b3ad9487d07f5371c2f895ee5a282d071f784a5`;
- mutated manifest payload:
  `b7b64405ccc62117b5e68def4c0a6398d850586537aaa2149ebca018dc8596d2`.

The cause is ordinary `json.loads` without an `object_pairs_hook` in
`build_revised_referee_bundle.py` lines **91--95** (and lock load line 104)
and `check_revised_referee_bundle.py` lines **108--114** and **294--301**.
Python silently retains the last occurrence, so the report's canonical payload
still validates while a strict or first-key consumer sees a non-portable
object. The supposedly independent checker shares this decisive parser
behavior. In contrast, the independent ledger checker rejects a repeated name
at parse time.

Reproducer exit 0 in 3.71 s; script SHA-256
`d6f636dd6b3087d32512aacae4e3f1ec76e0547e96b702cd1cb6ee4bb1308756`;
deterministic result SHA-256
`6fbc82361dbf0e3ffc274e8f730d1dd0e99082ec14661129b4b7aa173a49443d`.
The script restored manifest, report, bibliography, and portable ledger
byte-for-byte. The same run correctly rejected a physical source symlink,
physical bibliography omission, missing portable ledger, and syntax-invalid
manifest for their intended diagnostics.

This is an acceptance vulnerability, not evidence that the distributed JSON
is presently ambiguous: a strict independent inventory parsed all **233**
current `.json` files with duplicate-name rejection and found zero failure
(exit 0, 0.62 s; inventory tool SHA-256
`9b516256294f269e08cbd0746216a0574401eafac2011cf530c288a1316231c8`; stdout
SHA-256
`1de65445d03a64f1aa2c6e1f3f3769688fdcccfb04613f39feb40344b26faa93`).

**Smallest remedy:** use one shared strict JSON decoder that rejects duplicate
object names in both outer producer and independent checker, and preferably in
all provenance readers; add same-valued and conflicting-valued duplicate-key
mutations. Then regenerate the crosswalk/outer manifest, tag, and archive. No
theorem recomputation is intrinsically required for this code-only fix.

## Other adversarial controls

- Crosswalk mutation suite: 31/31 intended mutations rejected; zero Python
  `assert` dependency; exit 0, 10.05 s; payload `0492a14d...`; stdout SHA-256
  `bd92ab6565a2a75317d7b83aa07fd7d0096ea13697b1f6457d1ac999125afd29`.
- Final replay output contract: authoritative-path, stale PASS removal,
  optimized mode, source symlink, preexisting hardlink, and late symlink swap
  controls passed; exit 0, 0.37 s; stdout SHA-256
  `4988dbe96b51dbe099727ea52b8474e94cabf68dd5c429b54aa0520740e0c4af`.
- Optimized Python was explicitly rejected by the portable builder, release
  lock builder, quick replay, outer builder, outer checker, article audit, and
  PDF builder. Every exit was 1 with its named optimized-mode diagnostic.
- A physical bibliography symlink was rejected as `non-regular submission
  source`; a missing portable ledger and malformed manifest were rejected at
  the intended gates.

## Conclusion and required actions

The archive is deterministic and byte-complete; current ledgers, tag, PDFs,
five sources, dispositions, and stored telemetry are internally byte-bound.
That evidence is computational/provenance evidence, not a mathematical proof.

Before submission:

1. Correct the two stale supplement hash anchors and add a normal printed-hash
   semantic gate.
2. Make all outer provenance JSON parsing duplicate-name-strict and add the
   two duplicate-key mutations.
3. Rebuild/reseal the affected sources, PDF/report/audit/crosswalk/manifest,
   source-bound replay telemetry, tag, and deterministic archive; rerun the
   independent byte-ledger, printed-hash, duplicate-key, omission, and archive
   comparison checks.

