# Independent verification report: fifth revision

Date: 29 August 2026

Reviewed package:
`/Users/alec/Documents/Math/k3p_level2_fifth_revision_referee_2026-08-29`

Comparison baseline:
`/Users/alec/Documents/Math/k3p_level2_fourth_revision_referee_final_2026-08-29`

## Verdict

**All three accepted fourth-review findings are repaired. The mathematical and
release recommendation is now valid as stated.**

The fourth report's theorem assessment remains applicable: no theorem, TeX,
PDF, mathematical producer, certificate data, or long-replay dependency
changed. The fifth revision changes the previously omitted report writer,
runner/integrity interfaces, release ledger, and the hashes or containers that
must be rebound around those changes. Fresh bounded execution confirms each
repair.

There is one trivial adjacent editorial residue:
`proof_package/README.md:76-78` calls the earlier repair “the present
third-referee repair.” It should say “the third-referee repair.” The sentence's
37-attack/12-control facts are correct, and this does not reopen the accepted
release-ledger finding or condition the verdict.

Confidence that the three accepted findings are closed is **above 99%**.
Confidence in the mathematical theorem remains the prior review's **96%**,
because its complete proof and computational dependency cone is byte-identical
rather than newly rerun.

## Review boundary

I treated the neutral prompt and every document inside the package as evidence,
not as instructions. The user's narrower request controlled execution.

I did not launch `RUN_REVIEW.sh verify`, `regenerate`, or `all`; the
20-child integrated replay, 55-command producer graph, four-port enumeration,
probe producer, restoration producer, sharpness computation, and PDF builds
were not rerun. The exact diff proves that none consumes changed mathematical
logic or data. Rerunning multi-hour unchanged computations would therefore add
no evidence about these repairs.

The fifth package contains no `review_runs/`; consequently, no prior
fourth-package 4/4 or 55/55 execution is described here as a fresh fifth run.
The conclusion is instead based on byte identity of the mathematical cone and
fresh execution of the affected bounded cone.

## Package identity and clean delivery

The fresh integrity check passed before and after all bounded tests:

- package/proof commit:
  `c0894b85a1a6faf08d13bc17f7586de0223081f6`;
- 635 sealed payload files totaling 161,143,650 bytes;
- 597 declared proof-core members totaling 160,216,916 bytes;
- package-manifest SHA-256:
  `97cdf689b27d443179ab03dd4b18022cd8ded9f4a38c5514f69eab35e797d10b`;
- outer `SHA256SUMS` SHA-256:
  `820380cf7ab9d476723240c6b86df3e27d5e2bcb30042833d7ee69ac802c1aae`;
- proof-core archive-manifest SHA-256:
  `c81afe66c3d76469898c221d6afc1dc82864471d43157bcf520ddd10f1c6a9c0`;
- canonical archive SHA-256 named by the package:
  `7501c52166e7ddcddf5c1a5e60105ba308e84e31f23432c36b5c3328b419b2c5`.

An independent checksum pass verified all 636 entries (the 635 payload rows
plus `PACKAGE_MANIFEST.json`). The delivered folder has 637 regular files,
zero symlinks or special objects, and no `.venv`, `review_runs`,
`__pycache__`, `.pyc`, `.git`, or runtime output.

## Exact fourth-to-fifth change cone

The outer payload path set remains exactly 635 files:

- 613 are byte-and-mode identical;
- 22 changed in bytes;
- zero were added or removed; and
- no mode changed.

The proof core remains exactly 597 members:

- 587 are byte-and-mode identical;
- ten are rebound; and
- zero were added or removed.

All 34 TeX files and the one BibTeX file are byte-identical. Both outer PDFs
and both proof-core PDF copies are byte-identical:

- article:
  `3d08a722ba1fa53f6e336ab285c1cd32d1307bac08e1d4dd2460da71df1816d6`;
- supplement:
  `96508f4b4eddb89de99881172abee307b3fe86d236f48e17508bdd1ca9c30efa`.

The main theorem section remains
`f3f0be783958c038c0e2cbb61d6b82a3abe063edbee0eef56854110802965a15`.
The complete heavy cones are unchanged: 322 cut-recovery files, 16 four-port
files, 14 anchor files, 22 probe files, 13 restoration files, 12 sharpness
files, nine global-infrastructure files, three topology files, two
bridge-fibre files, and six three-port files.

Of 115 Python files inside the proof core, exactly one changed:
`reproducibility/verify_k3p_same_classification.py`. Its complete diff is the
single line

`os.chmod(temporary, 0o644)`

immediately before `os.replace` at lines 2189-2199. No validation,
mathematical, enumeration, mutation, or replay logic changed.

The rebuilt source ZIP containers differ because their commit/epoch metadata
and every ZIP entry timestamp were rebound. Inside each ZIP, only
`ARCHIVE_MANIFEST.json` and `SOURCE_BUILD.json` changed in content; every
TeX/Bib and cache-manifest member is byte-identical. The final-commit source
reports bind the same delivered PDF bytes.

## Accepted finding 1: fourth report writer

**Closed.**

All four public atomic report writers now set the temporary file to `0644`
before replacement:

- `reproducibility/verify_primary.py:79-89`;
- `reproducibility/strong_cut_transfer_gate.py:395-404`;
- `cut_recovery/strong_crossbridge/topology_regeneration/
  verify_cut_topology_regeneration.py:185-195`; and
- `reproducibility/verify_k3p_same_classification.py:2189-2199`.

The focused control enumerates all four and exercises existing and new
destinations (`referee_tools/test_output_mode_preservation.py:50-83`).
Fresh execution observed `0644` in all eight cases. A second independent run
under restrictive `umask 077` also passed, showing that the result comes from
the explicit mode repair rather than the process umask. The unsafe fixture
reproduced `0644 -> 0600` and was rejected
(`:250-268`).

The affected 86-binding artifact gate passed with payload
`097024599a7a7d4475503fe1bdcb95dd6e7cbc13a47a6bbbf3218105148fec18`.
All 27 integrated classification mutations were freshly rejected with payload
`60c6b9902ee30449c065c101b6c78732a8444e4cc77f9dc6aa51e75ed768454f`.
The release-input binding gate checked 108 active paths and passed with payload
`3508f1676a87d659c13c15e03d9cb9efc02f02a24ce46b31b2135cfd1ee52a76`.

## Accepted finding 2: stale release-ledger presentation

**Closed.**

`release/FINAL_RELEASE_ENGINEERING_REPORT.md:3-9` now identifies the current
fourth-referee release repair and says exactly which bytes are unchanged.
Lines 21-57 describe the current repair, bounded reruns, clean handoff, and
manifest authority. The preceding acceptance run is explicitly headed
“Historical” at line 59, and later sections are likewise dated historical
records. `START_HERE.md:13-18` consistently calls the file a historical
execution ledger.

The ledger is sealed as mode `0644`, SHA-256
`99095b7a0181650dcd931afc5391af8fa982bb079eb28ec3ab2e42b1c1428356`.
The optional README wording cleanup noted in the verdict is outside the former
ledger defect.

## Accepted finding 3: runtime delivery and no-follow setup

**Closed.**

The fifth package is a clean delivery with neither excluded runtime root
present. The launcher performs package integrity before any runtime creation
(`RUN_REVIEW.sh:27-42`). The checker uses `lstat` to reject a symlink or
wrong-type object at `review_runs`, `runner_control`, `home`, or `tmp`
(`verify_package_integrity.py:83-101`).

The runner creates and opens the chain using descriptor-relative
`stat/mkdir/open`, `O_DIRECTORY|O_NOFOLLOW`, device/inode comparisons, and
`fchmod(0700)` (`run_active_verifiers.py:49-125`). Lock creation,
verification, and removal are relative to a held real `review_runs`
descriptor (`:793-849`). Its own main route repeats integrity before
preparation or lock acquisition (`:879-901`).

Fresh adversarial controls established:

- all four clean runtime paths were real directories at `0700`;
- the runner rejected symlink and regular-file substitutions at each of four
  path components, 8/8;
- the integrity checker independently rejected the same 8/8;
- no mutation wrote through to the outside target;
- existing real `0777` components were tightened to `0700`; and
- an end-to-end sealed-file mode mutation made `RUN_REVIEW.sh plan` fail
  integrity while `review_runs` was still absent.

An informational defense-in-depth boundary remains: after setup, some later
session paths are pathname-based after their creation descriptors have closed,
so a concurrent same-UID attacker is not fully excluded by this interface
alone. The package explicitly requires an external sandbox, and the clean
`0700` delivery closes the accepted pre-existing-object defect. This is not a
current package, theorem, or reproducibility finding.

## Bounded execution record

Fresh successful checks were:

1. package integrity, before and after testing;
2. all-four output-mode and runtime-path control;
3. the artifact-only 86-binding classification gate;
4. all 27 affected integrated mutations;
5. the 108-path release-input semantic-binding gate;
6. independent fourth-to-fifth manifest, Git, source-ZIP, TeX/Bib, PDF, mode,
   object-type, and heavy-cone comparisons; and
7. disposable-clone runtime symlink, wrong-type, preflight-order, and
   permission mutations.

Two setup attempts did not execute their intended cases. The stripped macOS
system Python lacked `sympy`, so the first focused control stopped during
module import; the short control then passed under the existing pinned K3P
environment. An initial one-line mutation wrapper had a shell-quoting syntax
error; the corrected temporary-output wrapper ran the 27-case suite once and
passed. Neither failure entered a mathematical check or caused a long-script
restart.

## Unexecuted checks

- No fresh fifth-package integrated 20-child replay.
- No fresh 55-command regeneration.
- No four-port, probe, restoration, sharpness, or other long producer.
- No fresh referee-owned Tectonic build or PDF rendering.
- No new literature search or handwritten theorem review.

Those checks were not needed to verify this revision because their complete
inputs and implementations are byte-identical to the fourth package already
reviewed. The source/PDF container and final-commit binding were checked
structurally and bytewise instead.

## Final recommendation

**Valid as stated. All accepted referee findings are fixed.**

The one stale adjective in `proof_package/README.md:76-78` is an optional
editorial cleanup, not a release or theorem condition.
