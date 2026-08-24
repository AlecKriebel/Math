# Integrity, replay, and submission-build record

## Preserved target

- Version/tag: `maximally-collective-stable-turing-v1.0.8`
- Commit: `b4607c4cc9fe6931cedbbd0c5cd7e6e68a704f9f`
- Immutable snapshot: 1,064 files, 18,941,206 bytes
- Path-and-content aggregate SHA-256:
  `436fb12e206edb864acbb017f2260fea61425996bbbec0ac21418e2231f3ef87`
- Host: macOS 26.5.2 (build 25F84), Darwin 25.5.0, arm64
- Qualification Python: CPython 3.9.6 with Matplotlib 3.7.1, NumPy 1.24.3,
  Pandas 2.3.3, pypdf 6.10.0, pytest 8.4.2, SciPy 1.10.1, and SymPy 1.14.0
- Document route: TinyTeX 2022.04, pdfTeX 1.40.24, Biber 2.17
- Inspection tools: Git 2.38.2, Apple/Info-ZIP 6.00, Poppler 26.08.0

The source snapshot was never executed or edited. Every replay and mutation
occurred in a disposable copy or a detached temporary directory.

## Manifest and bundle results before execution

| Object | SHA-256 / entries | Result |
|---|---|---|
| `public/repository/sha256_manifest.txt` | `8180188e56d66728414ea4f331e32157c8ed2da331ede2c960ac8d2c2546b00f` | All entries passed |
| `release/BUNDLE_SHA256.txt` | seven canonical ZIP entries | All seven passed |
| `release/sha256_manifest.txt` | `c0d468362cc6baf44c48533e723f15c0e13298e3dfb0b0b73341dd8839a59038`; 1,633 entries | **Failed:** 1,063 existing files passed and 570 listed paths were absent |
| journal source ZIP | `256a44bdba2489cb7b682b2c708260a172af4d6ebd0054a2f318815693b69638` | ZIP valid and byte-identical to staged journal source |
| journal manuscript PDF | `19dd0602bd54f2f3e92de07c1937f503c730de98b7626d1ed53d7a6656595260` | 19 pages; fonts embedded; visually and semantically passed |
| journal supplement PDF | `868b95835c6f18d93dfe22c1e9a472d8866177905b9f9a4447d078ebc4910a13` | 19 pages; fonts embedded; visually and semantically passed |

All 570 absent release-manifest paths are under the ignored v1.0.7 audit
`source_snapshot/`, `working_packet/`, or rendered `tmp/pdfs/` directories.
They were present in the author's dirty worktree when the broad `find .` at
`release/create_release_manifest.sh:17-29` generated the manifest, but they do
not belong to the Git tag. Regeneration in a clean disposable tag yields 1,063
entries; all common hashes remain unchanged and the regenerated manifest
passes.

## Execution outcomes

| Stage | Exit / runtime | Evidentiary result |
|---|---:|---|
| pinned toolchain preflight | 0 / <1 s | engine, Biber, Python, and ordinary load-bearing TeX package checks passed |
| full portable public replay | 0 / 72.55 s (independent root run); 0 / 71.69 s (software audit) | all eight stages, shipped-baseline check, exact-artifact comparison, self-consistency manifest, `PUBLIC_REPLAY_PASS` |
| minimal verifier replay | 0 / 42.31 s | exact aggregate, generic cubic bridge, endpoint checks through `m=200`, finite floating branch regression, `MINIMAL_VERIFIER_PASS`; packaging duplicate, not extra independent proof |
| all 39 direct entrypoints, normal Python | 0 / 87.39 s | every direct entrypoint completed; semantics classified separately |
| all 39 direct entrypoints, optimized Python | 39 expected nonzero exits / 0.96 s | every entrypoint failed closed; no false `PASS` under `-O` |
| mutation/regression suite | 0 / 8.88 s | 25 tests passed, including manifest and assertion-mode controls |
| current full manuscript/stale/PDF audits | 0 / 0.10, 0.47, 1.45 s | all passed |
| clean journal source build, correct pass count | 0 / 6.50 s | main and supplement built cleanly under the pinned producer; rebuilt text equals submitted text |
| top-level release manifest check | 1 / 0.23 s | fails before release stages on 570 absent ignored paths |
| top-level one-command replay | not completed | five historical lineage archives were unavailable; even if supplied, the bad baseline manifest would stop the run at line 66 |
| embedded v1.0.7 `RUN_COMPLETE_AUDIT.sh` control | 1 / about 94 s | outer and inner hashes and historical minimal replay passed; archived full replay stopped at the known v1.0.7 PDF false-negative, `supplement PDF lacks unambiguous Latin near-threshold parameter`; this is not a v1.0.8 validation pass |

Stored outputs were used only as provenance. The pass statements above come
from current disposable executions.

The historical wrapper was executed because it was expressly named in the
original referee protocol. It is embedded unchanged under
`external_audit/full_referee_validation_packet_v1.0.7/`; its failure reproduces
the prior D1 defect that v1.0.8 repairs in the current portable package. Its
post-failure stages are not marked checked. All 39 current v1.0.8 direct
entrypoints, including the 38 historical ones, were run separately.

## Exact versus numerical boundaries

- Exact: reaction/minor/certificate algebra, table generation, direct
  entrypoint identities, manifest hashes, and deterministic source artifacts.
- Numerical: 15 illustrative simulations, refinement comparisons, and the
  finite complementary-spectrum branch regression. These are tolerance-based
  evidence only.
- Document reproducibility: PDFs are producer/page/font/semantic checked rather
  than expected to be byte-identical across creation metadata. The detached
  exact source build reproduced extracted layout text byte for byte.

## Reproducibility defects found in rereview

1. **Release-root manifest contamination.** The tagged baseline cannot verify.
   Generate it from tracked files (for example, a sorted NUL-safe
   `git ls-files` stream excluding the manifest itself) and test it against a
   fresh `git archive` before publication.
2. **Two unenforced lock rows.** `environment/check_toolchain.sh:78-85`
   deliberately skips `FORMAT` and `LATEX`, even though the lockfile and tested
   environment claim those exact versions. Impossible mutations of either row
   still print `TOOLCHAIN_LOCK_PASS`. The engine, Biber, Python, and package
   pins are genuinely enforced. Stop skipping the two rows and add negative
   tests for every special lock field.
3. **Detached supplement build is one pass short.** The package-validation loop
   at `release/one_command_replay.sh:211-220` compiles the supplement twice.
   From a clean ZIP, that leaves stale table-of-contents page numbers; a third
   pass makes the supplement byte-identical to the canonical PDF. Add the third
   pass or iterate until the auxiliary files stabilize, and compare the built
   semantic text against the canonical artifact.

None of these defects changes a theorem, formula, hypothesis, conclusion,
dimension range, or submitted source ZIP. They do prevent an unqualified
top-level reproducibility/release-ready claim for the immutable v1.0.8 tag.
