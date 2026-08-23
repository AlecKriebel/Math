# R3 certified-route audit

Date: 2026-08-23 (UTC)

Revised package:
`/Users/alec/Documents/Math/complete_graph_extremality_r3_rereview_2026-08-23/work/package`

Frozen comparison package:
`/Users/alec/Documents/Math/complete_graph_extremality_r2_rereview_2026-08-22/work/package`

## Scope and phase boundary

This audit traces the R3 package's sole certified execution route, its exact
file/directory inventories, all pre-import checks, the private interpreter and
bytecode-cache path, the six advertised hostile controls, failure propagation,
the seventeen directly invoked verifier programs, and lower-stage assurance
boundaries. It compares those changes against frozen R2 and the two reproduced
R2 direct-entry defects, SR-1 (forgeable public-token `PYTHON`) and SR-2
(timestamp-valid adjacent bytecode).

The readiness decision was made **before executing or importing any delivered
R3 code**. Before that gate I used only read-only host tools (`diff`, `find`,
`comm`, `shasum`, `tar`, `rg`, `nl`, `sed`, `stat`, and `cmp`) to inspect text,
node types, modes, archive members, hashes, and R2/R3 byte equality. After I
sent a READY gate, the root referee explicitly authorized a narrowly scoped
hostile test in a disposable verified extraction. That post-gate test is
reported separately under SCA-1; I did not run the full positive replay in this
subaudit.

Commands and statuses are preserved in
`records/static_certified_route_commands.log`.

For compact references below:

- `P/` means the revised package root above.
- `U/` means
  `P/source_and_certificates/universal_simultaneous_amplification/`.
- `D/` means
  `U/phase5_exact_threshold/paper_db_extremality/`.

## Readiness gate

**READY for the authoritative dynamic execution of
`P/run_all_referee_checks.sh`.**

R3 closes both reproduced R2 bypasses on the represented interface:

1. the package launcher, bootstrap, and replay reject any inherited `PYTHON`,
   even an explicitly set empty value; replay no longer selects or
   “authenticates” an arbitrary command by a public stdout token;
2. the certified route scans an exact manifest-bound tree before any project
   import, rejects adjacent cache artifacts and all unexpected nodes, and then
   supplies an empty private command-line cache prefix to every process capable
   of importing project code.

No alternate route is described as a certificate. R3 consistently calls the
package-root launcher the sole certified entry point and labels development,
bootstrap, and replay status as lower assurance. Bare `replay.sh` now rejects
standalone invocation.

One **low-severity, nonblocking negative-control observability defect** remains:
the hostile bytecode's sentinel is written relative to the caller's working
directory, while the launcher searches only inside the contaminated extraction.
The cache is nevertheless rejected by the expected exact-tree diagnostic before
any project import, so this does not reopen SR-2. It does mean the additional
“sentinel absent” assertion would miss execution if a future ordering regression
both executed that bytecode and later emitted the expected tree-rejection
message. See SCA-1.

## Bottom line

The substantive R3 security changes are coherent and fail closed:

- verified bytes, rather than a recursive copy of an ambient tree, are written
  to a new mode-0700 extraction (`P/verify_referee_package.py:143-160,216-221`;
  `P/run_all_referee_checks.sh:58-80`);
- outer and inner scanners compare both regular-file and implied-directory sets
  and reject symlinks, nonregular nodes, `__pycache__`, `.pyc`, and `.pyo`
  (`P/verify_referee_package.py:53-122`; `D/submission/verify_execution_safety.py:152-242`);
- the first certified bootstrap safety process is isolated and performs the
  manifest/tree/hash and AST scan without importing a bundled module
  (`D/submission/bootstrap_replay.sh:45-47`;
  `D/submission/verify_execution_safety.py:206-242,270-316,332-344`);
- the fresh virtual environment and its cache are created outside the source
  tree under a new mode-0700 runtime root (`D/submission/bootstrap_replay.sh:53-85`);
- every subsequent process that can import project code receives `-B` and an
  explicit `-X pycache_prefix=<fresh-empty-private-directory>`
  (`D/submission/bootstrap_replay.sh:86-93`; `D/replay.sh:45-64`), and the cache
  is checked empty before, during, and after the verifier sequence
  (`D/submission/verify_execution_safety.py:245-258,334-348`;
  `D/replay.sh:45-48,97-101`);
- the scientific execution list is still one unit-test discovery plus exactly
  seventeen direct verifier/cross-check calls, all seventeen bytes unchanged
  from frozen R2 (`D/replay.sh:64-95`); and
- no Makefile of any spelling is present anywhere in R3.

The R3 code changes are operational hardening and assurance-boundary changes.
The dependency lock, `requirements.txt`, document build, and all seventeen
direct scientific programs are byte-identical to R2. The manuscript change in
Section 7 replaces the old bare-`replay.sh` instruction with the package-root
certified route and explains the lower-stage boundary
(`D/sections/07_implications_reproducibility.tex:98-114,118-136`).

## R2-to-R3 remediation matrix

| R2 issue / required property | R3 implementation | Static result | Residual |
|---|---|---|---|
| SR-1: direct `PYTHON` accepted an arbitrary token-printing command | Any set `PYTHON` is rejected by the package launcher (`P/run_all_referee_checks.sh:4-7`), bootstrap (`D/submission/bootstrap_replay.sh:4-7`), and replay (`D/replay.sh:4-7`), then removed from the environment (`run_all:15-20`; bootstrap/replay `:15-20`). Replay derives its interpreter only from the private runtime argument (`D/replay.sh:22-48`). The public-token hostile control is `P/run_all_referee_checks.sh:126-141`. | **Closed.** The old stdout-token authentication branch is gone. The fake executable is required not merely to fail, but never to be invoked. | The explicitly selected `BOOTSTRAP_PYTHON` remains a host trust input, as every source verifier necessarily trusts some host interpreter. It is not an inherited `PYTHON` bypass. |
| SR-2: reused-tree imports could consume timestamp-valid adjacent `.pyc` while the AST scanner read `.py` | Exact-tree scanners reject `__pycache__`, `.pyc`, and `.pyo` (`P/verify_referee_package.py:63-98`; safety verifier `:162-203`); both file and directory sets must equal manifest implications (`P/verify_referee_package.py:101-122`; safety verifier `:206-242`). Replay imports use a new empty private prefix (`D/bootstrap:53-95`; `D/replay:39-64`). | **Closed on the certified route and also isolated in development replay.** Adjacent caches cannot be accepted by the certified scanner and cannot be selected by later imports because `sys.pycache_prefix` is redirected to a fresh directory. | SCA-1 affects only the negative fixture's execution sentinel, not rejection or cache selection. |
| R2 presented package and direct replay with insufficiently distinct assurance levels | The package README names `run_all_referee_checks.sh` as sole certified entry (`P/README_FIRST.md:34-37,44-63`); the claim map repeats this (`P/CLAIM_CODE_MAP.md:20-27`); source README, environment, bundle metadata, reproduction instructions, referee prompt, and manuscript do the same (`D/README.md:23-49`; `D/submission/ENVIRONMENT.md:14-50`; `P/source_and_certificates/BUNDLE_METADATA.txt:12-14`; `D/submission/BUNDLE_REPRODUCTION.md:57-79`; `P/REFEREE_PROMPT.md:113-147`; Section 7 `:98-114`). | **Closed.** Bare replay exits at its argument boundary (`D/replay.sh:22-25`). `all.sh` and release generation use the explicit `--development` mode (`D/all.sh:4-6`; `D/release_bundle.sh:28-31`). | A knowledgeable user can manually supply replay's documented internal flag and a runtime-shaped directory, but the resulting status is explicitly noncertifying. This is an internal API, not an alternate artifact certificate. |
| Certified source must be an exact regular-node tree, including empty-directory attacks and special nodes | Package inspection and extracted-source inspection use `lstat`/`scandir(..., follow_symlinks=False)`, enumerate file and directory sets separately, and reject all other node modes (`P/verify_referee_package.py:63-122`; `D/submission/verify_execution_safety.py:162-242`). Extraction is reconstructed from verified tar payload bytes, not copied from the ambient convenience tree (`P/verify_referee_package.py:143-160,172-221`). | **Closed.** The frozen outer and inner trees exactly equal their manifest-derived file and directory inventories; see the inventory section. | Ordinary same-user concurrent mutation between scan and use remains outside the frozen-package replay model; private mode-0700 run roots substantially constrain it. |
| Six hostile controls must be reachable and fail for the intended boundary reason | Fake interpreter (`run_all:126-141`), timestamp bytecode (`:143-173`), extra regular file (`:143-174`), extra empty directory (`:143-175`), symlink (`:143-176`), and FIFO (`:143-177`) are constructed in fresh separately verified extractions. Each contaminated bootstrap must exit nonzero and contain its mode-specific diagnostic (`:155-165`). | **Substantively closed.** Every fixture branch is reachable and each expected message comes from the intended scanner branch. | SCA-1: the bytecode execution sentinel is searched in the wrong root. |
| Failure propagation, including optimization-hostile cases | All shell stages use `set -eu` (`run_all:1-2`; bootstrap/replay `:1-2`). The explicit false condition must propagate nonzero (`run_all:82-94`), remains active under `python -O` (`:96-109`), and inherited `PYTHONOPTIMIZE=1` is explicitly rejected (`:111-124`). Positive bootstrap, replay, build, `cmp`, PDF hash, and final package verification are unguarded success-path commands (`:179-197`). | **Closed.** There is no success-output parser on the scientific programs; a nonzero status stops the chain. | Host shell/core utilities, `PATH`, explicitly selected `BOOTSTRAP_PYTHON`, Tectonic, and Poppler remain ordinary host trust inputs, as already recorded for R2. |

## Exact inventory and archive results

The following were established with host-side static enumeration and hashing;
the delivered verifier was not executed before the gate.

| Object | Manifest expectation | Actual regular files | Actual implied directories | Links / special nodes / cache entries | Hash result |
|---|---:|---:|---:|---:|---:|
| Whole package `P/` | 83 listed payloads plus unlisted `PACKAGE_MANIFEST.sha256` | 84 | 26 | 0 / 0 / 0 | 83/83 listed payload hashes match |
| Convenience extraction `P/source_and_certificates/` | 72 listed payloads plus unlisted `MANIFEST.sha256` | 73 | 25 | 0 / 0 / 0 | 72/72 listed payload hashes match |
| Compressed source archive | 72 manifest payloads plus `MANIFEST.sha256` | 73 tar members | directories are implicit (no directory members) | all 73 members regular | exact member-name equality |

For both filesystem trees, independent `comm` comparisons of (a) the manifest
file set plus the manifest itself and (b) every directory prefix implied by
those file names against the actual `find` inventories produced no output.
The tar member list is already bytewise sorted, has no duplicate name, matches
the inner 73-name set exactly, and has no nonregular member. All launcher,
bootstrap, replay, safety, and fixture entry files are regular mode-0755 files.

These static results match the algorithms R3 will apply dynamically:

- the package manifest excludes itself but its presence as a regular file is
  required, and exact files/directories are checked before hashing
  (`P/verify_referee_package.py:125-140`);
- tar names must be canonical, safe, sorted, unique, and regular
  (`P/verify_referee_package.py:163-204`);
- the convenience extraction must exactly equal tar bytes and node sets
  (`:205-214`); and
- a certified run's fresh source tree is written from those already verified
  payload bytes, has executable bits normalized from tar modes, and is rescanned
  for exact nodes (`:143-160,216-221`).

## Certified pre-import path

### 1. Package boundary and safe extraction

`P/run_all_referee_checks.sh` rejects an inherited `PYTHON` before doing
anything else and rejects nonzero optimization (`:4-14`). It clears Python
import/cache/executable and Make overrides (`:15-20`). The chosen host
interpreter must execute isolated, report exactly Python 3.14.6, and have
optimization level zero (`:23-33`). Required document commands and exact
versions are checked next (`:35-56`).

A unique run root is made beneath the selected temp base, pattern-checked,
changed to mode 0700, and protected by a guarded cleanup trap (`:58-73`). Logs
and source directories are also mode 0700 (`:75-77`). Crucially, the launcher
does **not** recursively copy the convenience tree. It invokes the package
verifier with `--extract-to` (`:78-80`), which first validates the outer exact
tree and hashes, validates the archive member and internal-manifest sets and
bytes, and only then reconstructs a fresh extraction from in-memory verified
regular payloads (`P/verify_referee_package.py:125-221,270-283`).

Thus the later bootstrap receives a new source tree containing only verified
regular files and exactly the 25 directory prefixes implied by those files.

### 2. Certified bootstrap before project imports

The bootstrap independently rejects `PYTHON` and optimization and repeats the
environment clearing (`D/submission/bootstrap_replay.sh:4-20`). It resolves its
paper, project, and bundle roots from its own location (`:22-27`). In certified
mode, its first executable child is:

```text
<trusted-bootstrap-python> -I verify_execution_safety.py \
  --runtime --bundle-root <fresh-source-root> --audit-sources
```

(`D/submission/bootstrap_replay.sh:45-47`). Isolated mode is required by the
safety verifier (`D/submission/verify_execution_safety.py:77-89`), so neither
the script directory nor the caller's current directory supplies an import.
The safety verifier's top-level imports are standard-library modules only
(`:1-16`).

Within `main`, runtime validation occurs first (`:332-333`), then the supplied
bundle root is resolved and `check_bundle_tree` runs (`:336-340`). That function
uses its own standard-library manifest parser and scanner, compares exact file
and directory sets, rejects all forbidden node/cache types, and verifies every
payload hash (`:114-242`). Only after this does `check_sources` parse the Python
source ASTs (`:343-344`). Because a verified manifest was supplied, the branch
at `:277-284` obtains candidates directly from that manifest; it does **not**
call `load_bundle_manifest` at `:261-267`. Reading and AST-parsing a verified
source file is not importing it.

This establishes the promised ordering: the exact-tree scanner is
standard-library-only and no bundled module is imported before the certified
tree/node/hash audit succeeds.

### 3. Fresh private runtime and cache

Only after the preceding scan succeeds does bootstrap create a new temp runtime
directory, pattern-check it, set mode 0700, and install a guarded cleanup trap
(`D/submission/bootstrap_replay.sh:53-70`). The virtual environment,
`setup-pycache`, and later `pycache` are children of this private directory
(`:71-85`). Venv creation and hashed wheel installation both use isolated mode,
`-B`, and a command-line setup-cache prefix (`:76-83`). Installation retains
R2's `--no-deps`, `--only-binary=:all:`, and `--require-hashes`; the lock and
build inputs are byte-identical to R2.

The fresh venv then repeats runtime/dependency/source validation with `-I -B`
and the final command-line prefix, while also repeating exact-tree verification
in certified mode (`:86-93`). `check_cache_prefix` resolves and compares the
actual `sys.pycache_prefix`, requires `dont_write_bytecode == 1`, and requires
the directory empty (`D/submission/verify_execution_safety.py:245-258`). It is
called both before and after the other selected checks (`:334-335,347-348`).

The initial safety process, venv creation, and pip installation do not import a
project module. Every process from the point where a project import becomes
possible has both `-B` and the private command-line prefix.

### 4. Internal replay

Bootstrap invokes replay only as
`replay.sh --internal-from-bootstrap <absolute-private-runtime>`
(`D/submission/bootstrap_replay.sh:95`). Replay rejects any `PYTHON`, clears the
same environment variables, rejects any other argument shape, requires an
absolute existing runtime, derives the venv interpreter from that runtime, and
requires the private cache to exist and still be empty
(`D/replay.sh:4-48`). It does not consult `PATH`, `PYTHON`, or a public stdout
token for its scientific interpreter.

Replay's safety preflight at `:52-54` uses `-I -B -X pycache_prefix=...`. This
development-style AST scan loads `bundle_manifest.py`, but it does so only now,
under the fresh prefix and after the certified bootstrap scan. Every subsequent
program call goes through `run_python`, which supplies the single controlled
project `PYTHONPATH` and the same `-B -X` options (`:56-64`). An adjacent
timestamp cache is therefore not a candidate: Python's cache lookup is
redirected to the checked-empty private prefix. The final cache search at
`:97-101` must remain empty.

## Hostile controls and reachability

R3 advertises six interface/tree hostile controls in
`P/REFEREE_PROMPT.md:144-147`. All six are statically reached before the
positive bootstrap (`P/run_all_referee_checks.sh:126-180`):

| # | Hostile condition | Construction and invocation | Intended rejecting branch | Static result |
|---:|---|---|---|---|
| 1 | Public-token non-Python `PYTHON` | Fixture prints only the old public token (`D/submission/fake_python_public_token.sh:1-7`); launcher sets it as `PYTHON` for direct replay (`run_all:126-128`). | Replay's first boundary rejects any set `PYTHON` (`D/replay.sh:4-7`). Launcher also requires the old token to be absent, proving the fake was not invoked (`run_all:132-140`). | Reachable and reason-specific. |
| 2 | Timestamp-valid adjacent bytecode with unchanged companion source | Creator substitutes a same-size class-body statement in a temporary source, preserves mtime, compiles timestamp-mode cache to the real source's cache path, deletes the temporary, and rechecks original source text (`D/submission/create_tree_negative_control.py:19-50`). Called as `bytecode` (`run_all:173`). | Tree scanner rejects the `__pycache__` directory (`safety:184-188`), and launcher requires that exact diagnostic (`run_all:143-165`). | Core rejection reachable; sentinel-location defect SCA-1. |
| 3 | Extra regular file | Creator `:63-65`; launcher `:174`. | Exact regular-file set mismatch (`safety:218-234`). | Reachable and reason-specific. |
| 4 | Extra empty directory | Creator `:66-68`; launcher `:175`. | Exact implied-directory set mismatch (`safety:218-234`). | Reachable and reason-specific. |
| 5 | Symlink | Creator `:69-71`; launcher `:176`. | `lstat`/no-follow scanner rejects symlink (`safety:178-183`). | Reachable and reason-specific. |
| 6 | FIFO | Creator `:72-74`; launcher `:177`. | Nonregular/non-directory node reaches the special-node failure (`safety:191-200`). | Reachable and reason-specific. |

Each tree control starts from its own empty mode-0700 directory, reconstructs a
new verified extraction with the package verifier, contaminates only that
disposable tree, and invokes certified bootstrap (`run_all:143-157`). Success is
an immediate top-level failure; a nonzero status with the wrong diagnostic is
also a failure (`:158-165`). The positive source tree at `run_all:75-80` is
separate from all five tree fixtures.

Three additional fail-semantics controls precede those six: intentional false
check (`run_all:82-94`), the same explicit condition under `python -O`
(`:96-109`), and inherited `PYTHONOPTIMIZE=1` (`:111-124`). These are not part
of the prompt's enumerated six interface/tree attacks, but they retain the R2
optimization and exit-propagation coverage.

## Positive failure propagation and direct program reach

The positive certified bootstrap is a direct command under `set -e`
(`P/run_all_referee_checks.sh:179-180`). Bootstrap's venv creation, install,
both safety passes, and replay are likewise direct commands under `set -e`
(`D/submission/bootstrap_replay.sh:76-95`). Replay invokes its safety preflight,
unit suite, and programs sequentially under `set -e` (`D/replay.sh:1-101`). No
scientific output token is interpreted as success; only process status controls
the path.

The exact direct reach is:

| # | Replay line | Direct program |
|---:|---:|---|
| — | 64 | `python -m unittest discover -s tests -v` (unit suite; separate from the seventeen-program count) |
| 1 | 65 | `verification/verify_obstruction.py` |
| 2 | 66 | `phase1_directed/verify_directed_db_strong.py` |
| 3 | 67 | `phase2_triangle/derive_certificate.py` |
| 4 | 68 | `phase2_triangle/crosscheck_exact_solver.py` |
| 5 | 69 | `phase2_triangle/audit/independent_triangle_audit.py` |
| 6 | 70 | `phase2_n4/derive_lumped_certificates.py` |
| 7 | 71 | `phase2_n4/crosscheck_full_chain.py` |
| 8 | 72 | `phase3_asymptotic/verify_lumping.py` |
| 9 | 76 | `phase5_exact_threshold/r2_determinant/verify_r2_determinant.py` |
| 10 | 77 | `phase5_exact_threshold/r2_determinant/verify_complete_refresh_forest.py` |
| 11 | 78 | `phase5_exact_threshold/r2_determinant/verify_antisymmetric_hessian.py` |
| 12 | 79 | `phase5_exact_threshold/r2_determinant/verify_true_inverse_rank_symmetric_phase.py` |
| 13 | 80 | `phase5_exact_threshold/r2_determinant/verify_hessian_sectors.py` |
| 14 | 83 | `phase5_exact_threshold/r2_standard_physical_phase/verify_physical_standard_phase.py` |
| 15 | 87 | `phase4_landmark_closure/obstruction/r2_marked_lift_v2/verify_marked_lift.py` |
| 16 | 91 | `phase5_exact_threshold/r2_regular_sector/verify_local_complete_hessian.py` |
| 17 | 95 | `phase5_exact_threshold/paper_db_extremality/verify_paper_claims.py` |

All seventeen direct program files compare byte-for-byte equal with frozen R2.
R3's changed executable source is limited to the outer verifier/launcher,
bootstrap/replay/safety path, negative fixtures, development wrappers, and
bundle construction hardening.

The relevant transitive project-import description remains accurate:

- unit tests import `src/exact_markov.py`;
- the triangle and K4 cross-checks import their derivation modules and
  `src.exact_markov`;
- `verify_marked_lift.py:27-35` imports `solve` from
  `verify_resolvent_identities.py` and `matrix_from_edges` from
  `verify_direct_flow_screen.py`; `solve()` is called beginning at
  `verify_marked_lift.py:39`, and `matrix_from_edges()` at `:502,531,561`;
- importing `verify_direct_flow_screen.py:17-22` loads four names from
  `verify_fisher_route.py`, but the marked-lift route calls only
  `matrix_from_edges`; no Fisher function or any of the three guarded helper
  mains is invoked.

This matches `P/CLAIM_CODE_MAP.md:25-39`: function reach, transitive module
loading, guarded-main execution, and proof status are not conflated.

After replay returns successfully, the outer launcher directly invokes the
unchanged pinned build, byte-compares the rebuilt PDF, reports its SHA-256 with
the trusted Python, reruns package verification, and only then prints the sole
certified success line (`P/run_all_referee_checks.sh:182-197`). Build and lock
details remain as audited in R2: exact Python dependencies and hashes,
Tectonic 0.16.9, the v33 bundle-content digest, Poppler 26.08.0, and decisive
final PDF byte identity.

## Alternate-path analysis

I found no alternate path that both bypasses the R3 controls and is represented
as package certification.

- `D/replay.sh` rejects a bare call and any inherited `PYTHON` before validating
  its internal flag (`:4-25`). Its private-runtime argument is not a secret
  capability, but documentation explicitly states that lower-stage status does
  not establish package identity or execution of delivered bytes.
- `D/submission/bootstrap_replay.sh --development` skips certified exact-tree
  status and announces that only the enclosing package launcher is certified
  (`:45-51`). It still creates a fresh private runtime/cache and protects its
  project imports from adjacent bytecode (`:53-95`).
- `D/all.sh:4-6` and `D/release_bundle.sh:28-37` select that development mode;
  neither prints or claims the package-level certified result.
- Direct `--certified-package-stage` is named “certified” because it is the
  certified launcher's internal stage, but the README, claim map, manuscript,
  environment, and bundle metadata all deny certificate status to a direct
  lower-stage run. Outside the enclosing launcher, its internal manifest is
  not anchored to the outer package identity. This distinction is now explicit.
- The explicitly selected host `BOOTSTRAP_PYTHON`, core shell tools, executable
  `PATH`, Tectonic, Poppler, package-index transport, and absence of a hostile
  same-user concurrent filesystem mutator remain trust assumptions. This is
  unchanged from R2 and is not an inherited `PYTHON` or adjacent-cache bypass.

## Remaining finding

### SCA-1 — Low: hostile-bytecode execution sentinel is checked in the wrong directory

**Locations:**

- sentinel statement:
  `D/submission/create_tree_negative_control.py:23-31`, especially `:26`;
- contaminated bootstrap invocation:
  `P/run_all_referee_checks.sh:143-157`;
- sentinel search:
  `P/run_all_referee_checks.sh:166-169`.

The negative creator replaces a class docstring with:

```text
open("PYCACHE_EXECUTED", "w").close()
```

That is a relative path. `run_all_referee_checks.sh` does not change directory
to `negative_tree` before invoking the contaminated bootstrap; the child
inherits the launcher's working directory. The later check searches only
`find "$negative_tree" -name PYCACHE_EXECUTED`. Consequently, if the hostile
cache executes, the sentinel is normally created in the caller's working
directory and the search returns empty.

After root authorized a disposable hostile test, I confirmed this behavior
without changing the frozen package. I used the delivered package verifier to
write a fresh private extraction, used the delivered fixture creator to make
the timestamp-valid cache, then deliberately imported the targeted helper from
a different private working directory under Python 3.14.6 with `-B` and no
alternate prefix. The results were:

```text
marker_in_caller=yes
marker_in_negative_tree=no
```

This does **not** reopen the scientific bypass. In the actual certified control,
bootstrap's first action in certified mode is the isolated safety scan
(`D/submission/bootstrap_replay.sh:45-47`), and the scanner reaches the
`__pycache__` rejection before `check_sources`, dependencies, or replay can
import a project module (`D/submission/verify_execution_safety.py:332-344`).
The launcher also requires the exact “forbidden bytecode/cache directory”
diagnostic (`P/run_all_referee_checks.sh:161-165`). The code ordering and
reason-specific rejection therefore establish the current fail-closed result.

The defect narrows what the extra sentinel assertion proves. If a future
regression imported the hostile helper first but still reached and printed the
expected scanner failure afterward, the current `find` would miss the execution.

**Correction:** make the injected statement write inside the fixture, for
example a same-size padded statement based on `__file__`:

```text
open(__file__ + ".PYCACHE_EXECUTED", "w").close()
```

or pass an explicit sentinel path inside `negative_tree` to the generated code.
The existing recursive `find` will then observe it. Also consider checking the
launcher's working directory for the sentinel as a defense-in-depth cleanup
until the fixture is regenerated.

**Classification:** low-severity test-instrumentation correction; nonblocking
for authorized positive replay; no mathematical or delivered-code-identity
impact.

## Non-findings and retained trust boundary

- `-B` alone would not prevent reading an existing cache. R3 does not rely on
  `-B` alone: the decisive protection is the fresh command-line cache prefix
  plus certified exact-tree rejection.
- The safety script itself and the bootstrap shell must execute to perform the
  internal tree audit. On the sole route their bytes are already supplied by
  the outer verified archive extraction. The promise is correctly phrased as
  no **project import** before the standard-library exact-tree scanner, not no
  instruction execution before any verifier can verify itself.
- A self-contained package manifest is not an external signature. The source
  commit string and published/communicated digests still require an independent
  trusted comparison when provenance, rather than internal consistency, is at
  issue. This was already an R2 trust boundary.
- File modes beyond regular/directory/link/special classification are not
  cryptographic identity. Extraction normalizes executable versus nonexecutable
  modes and the delivered mandatory entry files are executable. No mode-based
  bypass was found.
- Ordinary filesystem time-of-check/time-of-use races require a concurrent
  same-user adversary able to mutate private mode-0700 directories. They are not
  part of the frozen, single-referee replay model and no such mutation path is
  supplied by the package.

## Final static conclusion

R3 materially closes the two reproduced R2 interface defects. The official
route now has a single documented assurance boundary, safe verified extraction,
two layers of exact tree/hash checking, reason-specific hostile controls, a
fresh private runtime and cache lookup prefix, rejection of arbitrary
`PYTHON`, unchanged exact scientific programs, direct reach to all seventeen
advertised programs, and normal nonzero failure propagation through replay and
build.

I found no residual capable of producing a certified zero status without the
intended scientific execution, nor a path by which adjacent delivered-tree
bytecode can be selected on the certified route. The only new actionable item
is SCA-1, which weakens the observability of one defense-in-depth negative-test
sentinel but not the actual pre-import rejection. The package is therefore
ready for the authorized dynamic certified replay. For a final journal
classification, SCA-1 is at most a minor reproducibility-test correction and
should be weighed together with the separate mathematical/PDF and full dynamic
records.
