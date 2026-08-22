# Pre-execution static replay audit — revised R2 package

Date: 2026-08-22

Package: `paper_i_complete_graph_extremality_referee_package_2026-08-22_r2`

Frozen copy audited: `/Users/alec/Documents/Math/complete_graph_extremality_r2_rereview_2026-08-22/work/package`

## Scope and constraint

This is a source-only gate performed before any delivered replay. I read the
entire mandatory shell/Python topology, every directly invoked verifier, every
project helper imported on that path, the package verifier, dependency lock,
document build, revised navigation/proof-status wording, and the corresponding
R1 files and findings. I did **not** execute a delivered shell or Python entry
point and did not import a delivered module. Text inspection used `rg`, `nl`,
`sed`, `diff`, `find`, `stat`, and read-only Git object queries. Commands and
statuses are in `records/static_commands.log`.

## Readiness gate

**READY for the authoritative package-level replay through
`run_all_referee_checks.sh`, preferably in the referee's independently
sanitized `env -i` environment.**

The official path first verifies the exact package file set and all hashes,
then copies the manifested source into a newly created directory. That fact is
important: it closes the two residual direct-entry trust issues described
below. The official path has normal fail propagation throughout, provisions a
fresh virtual environment from hash-locked wheels, runs explicit negative
controls, invokes the unit suite and all 17 advertised programs directly,
builds with pinned document resources, and performs a byte comparison against
the delivered PDF.

Do **not** treat `replay.sh` by itself, with an arbitrary `PYTHON` override or
inside a reused source checkout, as equivalent to the package-level path. Its
remaining limitations are findings SR-1 and SR-2 below. They do not block the
official replay because `bootstrap_replay.sh` overwrites `PYTHON` with its new
environment and `run_all_referee_checks.sh` supplies a manifest-verified fresh
source copy.

## Bottom line

All five R1 final-report corrections are materially implemented on the
authoritative path:

1. all 406 optimization-elidable scientific assertions were migrated to
   explicit fail-closed checks;
2. Python/import/Make overrides are cleared, isolated preflights and negative
   controls were added, and a fresh environment is mandatory;
3. all accepted Python wheels are SHA-256 locked and the Tectonic v33 bundle
   content is pinned;
4. helper reachability and finite-check-versus-analytic-proof language now
   match the actual execution graph; and
5. the standalone archive no longer ships or calls the legacy Makefile, while
   the historical full-repository target remains internally valid at the
   claimed source commit.

The assertion migration is mathematical-logic preserving by static diff: the
changed scientific programs add a uniform `CertificateFailure`/`require`
helper and replace the prior conditions without changing the checked
expressions. The only other verifier-source changes are corrected finite-scope
output wording and the expected new symmetric-verifier digest. The manuscript
change is confined to proof-status wording in Section 7 and that digest in
Appendix A; no theorem statement or proof algebra changed.

Two narrower hardening claims remain incomplete for the *direct* replay entry
point. SR-1 is a concrete public-token spoof of the claimed false-interpreter
authentication. SR-2 is a pre-existing adjacent-bytecode issue in a reused
tree. Both should be corrected if `replay.sh` is to remain advertised as a
standalone certificate command, but neither can affect the prescribed R2
package-level replay.

## R1-to-R2 remediation matrix

| Prior finding | R2 implementation and exact references | Static result | Residual |
|---|---|---|---|
| F1: optimization removes certification | `run_all_referee_checks.sh:4-29` rejects inherited optimization, clears Python overrides, and checks exact unoptimized 3.14.6 under `-I`; `bootstrap_replay.sh:4-15,32-45` repeats the boundary and creates a fresh environment; `verify_execution_safety.py:63-85,119-152` defines an explicit failure and scans all bundled Python ASTs; every scientific verifier defines the same raising `require`; negative controls are `run_all_referee_checks.sh:66-106`. | **Closed on official path.** R1 has 406 scientific `assert` lines; R2 has zero AST `Assert` statements. The R2 inventory has the same 406 scientific conditions plus 12 safety-verifier `require` calls. Every inspected `require` raises `CertificateFailure` when false, including under `-O`. | Direct arbitrary-interpreter token spoof remains (SR-1), but it is not an assertion-erasure issue and is unreachable through the fresh bootstrap interpreter. |
| F2: imported helper mains described too broadly | `CLAIM_CODE_MAP.md:20-35` now distinguishes function calls from guarded mains. Actual imports are `verify_marked_lift.py:34-35`; `solve()` is called at `:39`; `matrix_from_edges()` at `:502,531,561`; `verify_direct_flow_screen.py:17-22` only loads Fisher names transitively. Guarded mains remain at `verify_resolvent_identities.py:161,183`, `verify_direct_flow_screen.py:109,127`, and `verify_fisher_route.py:783,817`. | **Closed.** The wording is function-accurate and explicitly says import reachability is not execution or proof. | None. The inert suites concern open/exploratory routes and are not theorem-bearing. |
| F3: inherited flags and unpinned artifacts | Sanitization is duplicated at `run_all_referee_checks.sh:4-15`, `bootstrap_replay.sh:4-15`, and `replay.sh:4-15`; runtime isolation and unsafe-environment checks are at `verify_execution_safety.py:73-85`; `bootstrap_replay.sh:33-43` clears the venv, installs with `--no-deps --only-binary=:all: --require-hashes`, then verifies exact distribution versions and module origins (`verify_execution_safety.py:88-107`). `requirements-lock.txt:2-36` has three exact pins and 32 valid SHA-256 wheel hashes. `build.sh:8-9,29-46` fixes the v33 endpoint and checks its content digest. | **Closed for the originally identified risks.** `PYTHONOPTIMIZE`, `PYTHONPATH`, `PYTHONHOME`, cache-prefix/user-base/interpreter variables, and all identified Make override variables are removed; Make is no longer used. The universal SymPy and mpmath wheel digests match official PyPI metadata; pip's hash mode is the decisive check for the selected python-flint platform wheel. | The host interpreter and external executables selected through `BOOTSTRAP_PYTHON`/`PATH`, the configured package-index transport, and Tectonic itself remain ordinary trusted inputs. A referee-side `env -i` remains prudent and was already planned. |
| F4: finite executable output looked like an all-order proof | `CLAIM_CODE_MAP.md:10,15`; `sections/07_implications_reproducibility.tex:86-96`; `submission/BUNDLE_REPRODUCTION.md:73-76`; revised antisymmetric docstring/output at `verify_antisymmetric_hessian.py:2,158-167`; revised finite wording at `verify_marked_lift.py:351`; revised cross-sector context wording at `verify_hessian_sectors.py:234-235`. | **Closed.** Directed checks are now described as selected `n=3,4` literal-chain tests with Section 5 carrying the universal algebra. Antisymmetric output says finite checks agree with the Appendix-A all-n proof; it no longer prints that the finite program itself proves all orders. | None. Exact finite ranges versus manuscript analytic arguments are now expressly separated. |
| F5: stale archive-unsafe Make target | No `Makefile`, `makefile`, or `GNUmakefile` exists in the R2 package; `replay.sh:59-96` invokes everything directly and `run_all_referee_checks.sh:31-36` no longer requires Make. At Git commit `e63cc44748e4084ade67c5ff7dc5d1bf2a872f7c`, the full repository still has `universal_simultaneous_amplification/Makefile:29-31`; its `paper/main.tex` input and `output/pdf/no_universal_death_birth_amplifier.pdf` destination both exist in that full tree. | **Closed in the package; historical target retained and path-valid in its intended full repository.** | The historical target was inspected but not executed, as required by this pre-run gate. |

## Mandatory invocation graph

### Package boundary

`run_all_referee_checks.sh` has `set -eu` (`:2`) and performs:

1. inherited-environment rejection/clearing and isolated exact-Python preflight
   (`:4-28`);
2. isolated package verification (`:29`);
3. exact Tectonic/Poppler availability and version checks (`:31-52`);
4. guarded temporary-directory creation, cleanup trap, and source copy
   (`:54-64`);
5. four negative-control families: explicit false check, the same check under
   `python -O`, inherited optimized mode, and `/usr/bin/true` as direct replay
   interpreter (`:66-120`);
6. clean hashed bootstrap/replay (`:122-123`);
7. document build, byte-for-byte PDF comparison, and rebuilt SHA-256 reporting
   (`:125-139`).

The integrity verifier is explicit rather than assertion-based. It rejects
symlinks and any unexpected/missing package file
(`verify_referee_package.py:50-72`), verifies the detached archive and safe sorted regular members
(`:75-103`), verifies every internal hash and exact equality with the
convenience extraction (`:104-127`), binds both PDF copies and metadata
digests (`:129-155`), and checks prompt neutrality (`:158-184`).

### Bootstrap boundary

`bootstrap_replay.sh` also has `set -eu` and repeats environment clearing
(`:2-15`). It resolves the fixed project paths (`:17-22`), makes its intentional
failure an `exec` of the safety verifier (`:24-26`), checks the bootstrap
runtime (`:32`), clears and recreates `.venv-paper1` (`:33`), performs the
wheel-only hashed install (`:35-40`), checks runtime/dependencies/source
inventory inside that venv (`:42-43`), and passes the exact new interpreter to
`replay.sh` (`:45`). A nonzero child status propagates.

### Direct program reach

`replay.sh:65` invokes the unit-test suite. It then invokes exactly the
advertised 17 verifier/cross-check programs:

| # | `replay.sh` line | Program |
|---:|---:|---|
| 1 | 66 | `verification/verify_obstruction.py` |
| 2 | 67 | `phase1_directed/verify_directed_db_strong.py` |
| 3 | 68 | `phase2_triangle/derive_certificate.py` |
| 4 | 69 | `phase2_triangle/crosscheck_exact_solver.py` |
| 5 | 70 | `phase2_triangle/audit/independent_triangle_audit.py` |
| 6 | 71 | `phase2_n4/derive_lumped_certificates.py` |
| 7 | 72 | `phase2_n4/crosscheck_full_chain.py` |
| 8 | 73 | `phase3_asymptotic/verify_lumping.py` |
| 9 | 77 | `r2_determinant/verify_r2_determinant.py` |
| 10 | 78 | `r2_determinant/verify_complete_refresh_forest.py` |
| 11 | 79 | `r2_determinant/verify_antisymmetric_hessian.py` |
| 12 | 80 | `r2_determinant/verify_true_inverse_rank_symmetric_phase.py` |
| 13 | 81 | `r2_determinant/verify_hessian_sectors.py` |
| 14 | 84 | `r2_standard_physical_phase/verify_physical_standard_phase.py` |
| 15 | 88 | `r2_marked_lift_v2/verify_marked_lift.py` |
| 16 | 92 | `r2_regular_sector/verify_local_complete_hessian.py` |
| 17 | 96 | `paper_db_extremality/verify_paper_claims.py` |

The `run_python` function sets `PYTHONPATH` to the single resolved project root
for each call (`replay.sh:62-64`); this is a controlled replacement after the
inherited value is removed. There is no Make expansion, shell loop that skips a
program, or success-output parser on these 17 calls. `set -e` stops on the
first nonzero result.

### Transitive project imports

The local import graph remains narrow:

- `tests/test_exact_markov.py:7-15` imports `src/exact_markov.py`;
- `phase2_triangle/crosscheck_exact_solver.py:27-43` imports its derivation and
  `src.exact_markov`;
- `phase2_n4/crosscheck_full_chain.py:22-37` imports its derivation and
  `src.exact_markov`;
- `verify_marked_lift.py:27-35` imports `solve` and `matrix_from_edges`;
- importing `verify_direct_flow_screen.py:17-22` loads four Fisher-route names,
  but none of them is called by the marked-lift program.

Thus the current `CLAIM_CODE_MAP.md:20-35` exactly describes execution versus
mere import reach. No new helper or hidden subprocess appeared in R2.

## Fail-closed and negative-control assessment

### Scientific conditions

The R1 tree contains 406 scientific `assert` statement lines. The R2 tree has
no Python AST `Assert` statement. The 20 scientific verifier/helper files each
contain the same explicit implementation:

```text
if not condition:
    raise CertificateFailure(str(detail))
```

The static per-file `require` counts match
`verify_execution_safety.py:36-57` exactly and total 406. Twelve additional
`require` calls implement the safety verifier itself. The scanner parses all 26
bundled Python files and rejects either a bare assertion or a count mismatch
(`verify_execution_safety.py:119-152`). The tests use `unittest` assertion
methods, which are ordinary method calls and are not removed by `-O`.

Static R1/R2 diffs show a one-for-one migration of checked expressions. I found
no altered equality, inequality, quantifier range, expected rational, matrix,
polynomial, loop bound, or exception-swallowing construct. Parenthesis changes
only wrap former assertion conditions as function arguments.

### Environment and interpreter controls

The three shell boundaries clear inherited optimization, module search/home,
startup/interactive/warnings, pycache-prefix, platform/user-base/executable,
and Make override variables, and set `PYTHONNOUSERSITE=1` plus
`PYTHONDONTWRITEBYTECODE=1`. Runtime preflights use `-I` and require exact
Python 3.14.6, optimization level zero, and isolated mode. Dependency imports
must originate below the new environment prefix.

The first three negative controls are structurally sound:

- an intentional false explicit check must exit nonzero and emit its marker;
- the same explicit check under `python -O` must still fail; and
- inherited `PYTHONOPTIMIZE=1` must be rejected before the check runs.

The fourth catches `/usr/bin/true`, which emits no safety token. It does not
authenticate every arbitrary interpreter; see SR-1.

### Dependency and document resources

The lock has exactly three version pins and 32 syntactically valid lowercase
SHA-256 entries: one universal SymPy wheel, 30 python-flint platform wheels,
and one universal mpmath wheel. The SymPy and mpmath values match official
[SymPy](https://pypi.org/pypi/sympy/1.14.0/json) and
[mpmath](https://pypi.org/pypi/mpmath/1.3.0/json) PyPI release metadata;
[python-flint's metadata](https://pypi.org/pypi/python-flint/0.9.0/json)
confirms CPython 3.14 macOS arm64 wheel support. The bootstrap requires hashes, forbids source
distributions, disables dependency resolution, and lists mpmath explicitly,
so an index cannot substitute a different byte sequence without a SHA-256
collision. A missing platform wheel fails closed.

The build specifies Tectonic 0.16.9 and the v33 bundle URL, then reads
Tectonic's URL-content record and requires digest
`6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c`
(`build.sh:8-9,29-46`). Poppler versions are exact (`:15-22`). The outer PDF
`cmp` (`run_all_referee_checks.sh:126-128`) remains the final decisive build
identity check. Suppressed `pdftoppm` output does not suppress its exit status
because `build.sh` has `set -e`.

## Remaining findings

### SR-1 — Medium: direct `PYTHON` “authentication” is a forgeable public token

**Affected route:** `replay.sh` invoked directly, not the official fresh
bootstrap path.

**Locations:** `replay.sh:24-40,42-55,62-96` and
`run_all_referee_checks.sh:108-120`.

`replay.sh` accepts an inherited arbitrary command through `PYTHON`. Its only
semantic authentication is that the command exits zero and its captured
stdout contains the public literal `PAPER1_EXECUTION_SAFETY_OK`. Every later
scientific invocation uses the same command and trusts only its exit status.
Therefore a non-Python executable that prints that literal and returns zero
for every argv statically passes the preflight and all 17 purported program
calls. No code execution is needed to establish the path:

```text
PYTHON=/path/to/token-printing-zero-exit-command ./replay.sh
```

The included negative control uses `/usr/bin/true`, which returns zero but does
not print the token; it proves only that a silent no-op is rejected. The log
message calling this token test “authenticated”
(`run_all_referee_checks.sh:114-120`) is too strong.

**Impact.** This does not compromise `run_all_referee_checks.sh`:
`bootstrap_replay.sh:33-45` creates `.venv-paper1` from the already preflighted
bootstrap Python and explicitly assigns that exact interpreter to `PYTHON`.
The spoof requires bypassing the prescribed bootstrap and choosing a hostile
direct override. It nevertheless falsifies the editor's broad claim that the
direct false-interpreter bypass is closed.

**Correction.** For certificate mode, reject `PYTHON` overrides and require the
canonical newly provisioned `.venv-paper1/bin/python`, or make
`bootstrap_replay.sh` the sole public entry point and remove direct replay as a
standalone certified route. A known public stdout token cannot authenticate an
arbitrary executable.

### SR-2 — Medium/low: direct replay in a reused tree can consume pre-existing bytecode

**Affected routes:** `replay.sh` or `bootstrap_replay.sh` in a non-clean source
tree. The package-level launcher and a genuinely clean extraction are safe.

**Locations:** environment setup at `replay.sh:11-15`; non-isolated scientific
imports at `:62-96`; cache exclusions at `bundle_manifest.py:56-72,90-111`;
source loading/scanning at `verify_execution_safety.py:110-152`.

[`PYTHONDONTWRITEBYTECODE=1`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE)
prevents Python from *writing* `.pyc`; it does not prevent Python from reading
a valid existing cache. `PYTHONPYCACHEPREFIX` is
correctly removed, which closes the inherited external-prefix bypass, but
adjacent `__pycache__` directories and `.pyc` files are not rejected. In fact,
the bundle collector explicitly excludes them from the source inventory. A
timestamp-valid pre-existing cache can therefore supply bytecode for imported
project helpers while the AST safety audit reads the corresponding `.py`
text. The potentially imported files include `bundle_manifest.py`,
`src.exact_markov`, the triangle/K4 derivation helpers, and the marked-lift
helper chain.

**Impact.** No such cache is delivered. More importantly,
`verify_referee_package.py:55-68` treats any extra package file as a file-set
mismatch, and `run_all_referee_checks.sh:54-64` copies the verified cache-free
tree into a new directory. Thus SR-2 cannot affect the official replay. It is a
reused-tree/direct-entry integrity gap, not a defect in the frozen R2 run.

**Correction.** Before any source import, fail if a source include tree
contains `__pycache__`, `*.pyc`, or `*.pyo` outside the newly created venv; or
perform direct replay from another manifest-verified fresh copy. A controlled
new empty `PYTHONPYCACHEPREFIX` can also isolate cache lookup. `-B` or
`PYTHONDONTWRITEBYTECODE` alone is not a no-read guarantee.

## Non-finding trust boundaries

- `BOOTSTRAP_PYTHON` is an explicitly selected host interpreter, and Tectonic,
  Poppler, core shell tools, and `PATH` remain host trust inputs. Version,
  content, and final-output checks substantially constrain them but do not
  cryptographically attest the executables themselves.
- The package verifier continues to bind the source-commit string rather than
  independently querying Git objects (`verify_referee_package.py:141-155`). A
  referee must still compare package payloads against a trusted checkout, as in
  the R1 audit. This is unchanged and outside the five editor corrections.
- Wheel files are fetched rather than embedded. Hash mode gives content
  identity; offline availability is not promised. An unavailable wheel fails
  rather than silently falling back to an sdist.
- The source inventory/count scan is a regression guard, not a proof that each
  mathematical condition is sufficient. Static expression comparison and the
  forthcoming dynamic/independent mathematical audits carry that question.

## Static conclusion

The R2 package is substantially and correctly hardened. On its prescribed
package-level path, the original optimization, environment, artifact, wording,
and stale-Make defects are closed, and no new theorem/code mismatch was
introduced by the migration. The code is ready for positive replay and hostile
negative-control execution.

The editor's additional statement that false-interpreter and bytecode-cache
bypasses are closed needs qualification: it is true for the official
manifest-verified fresh-copy bootstrap, but not for `replay.sh` as an arbitrary
direct-entry certificate. SR-1 and SR-2 should be retained in the final
re-review record and weighed as localized reproducibility corrections rather
than mathematical defects.

## Post-readiness addendum: reproduced bypasses and verdict classification

I did not execute delivered code for this addendum. I independently read the
preserved dynamic transcript after the authorized tests were completed.

The positive and adversarial results confirm the static classification:

- The credential-free `env -i` package-level run passed package/archive
  identity, all four built-in negative-control families, the 406 scientific
  and 418 total explicit-check inventory, all six unit tests, all 17 directly
  invoked verifier/cross-check programs, the pinned document build, and final
  PDF identity. It exited 0 and rebuilt SHA-256
  `22142ee518e75c00d1948b19c210818ec797946df86a5e3272c9d1017800b0f4`
  (`records/COMMANDS.log:2982-3193`). This confirms that the authoritative
  package route is both functional and fail-closed against the included
  controls.
- A non-Python command that only printed the public
  `PAPER1_EXECUTION_SAFETY_OK` token caused bare `replay.sh` to emit the token
  for every purported program and exit 0 (`records/COMMANDS.log:3195-3217`).
  SR-1 is therefore reproduced, not hypothetical.
- A timestamp-valid malicious in-tree `.pyc` was created while its companion
  `.py` SHA-256 remained unchanged (`records/COMMANDS.log:3246-3251`). Bare
  replay passed its 406-check source audit and exited 0
  (`records/COMMANDS.log:3253-3299`), while the bytecode-created marker proved
  that the cached code executed (`records/COMMANDS.log:3397-3402`). SR-2 is
  likewise reproduced.

These defects are relevant to the distributed interface, not merely to an
undocumented developer shortcut. The source README advertises
`bootstrap_replay.sh` for a fresh extraction and `replay.sh` for a prepared
development tree (`paper_db_extremality/README.md:23-35`); the manuscript calls
`./replay.sh` the one-command replay
(`sections/07_implications_reproducibility.tex:98-101`); the package claim map
calls it the top-level replay (`CLAIM_CODE_MAP.md:20-22`); and bundle metadata
names it the replay entry point (`BUNDLE_METADATA.txt:12`). Conversely,
`README_FIRST.md:34,47` correctly directs a referee to the sound package-level
launcher. The package thus currently presents two different assurance levels
without making the distinction sufficiently explicit.

### Recommendation among the four permitted verdicts

**Valid after minor corrections.** This is the best-supported classification.

- **Not fully validated:** two specifically claimed hardening properties fail
  reproducible hostile tests on an advertised replay entry point. A zero exit
  status can be obtained without running any scientific program, and checked
  source text need not be the imported code.
- **Not major correction required:** the complete, referee-facing
  `run_all_referee_checks.sh` path passed cleanly and is structurally insulated
  from both bypasses by exact file-set verification, a fresh copy, and a new
  pinned environment. The mathematical proofs, theorem scopes, exact
  calculations, and built PDF are unaffected. Closing the defects requires
  localized launcher/cache checks and documentation, not a new proof,
  certificate family, or redesign of the scientific computation.
- **Not invalid:** neither bypass supplies a mathematical counterexample or
  contradicts a theorem; both concern reproducibility/certification plumbing.

The minimum correction is to make `bootstrap_replay.sh` or the package-level
launcher the sole certified entry point, reject arbitrary `PYTHON` overrides
in direct certificate mode, and fail before import when project-source cache
artifacts are present (or always replay from a manifest-verified fresh copy).
The README, manuscript reproducibility section, claim map, and bundle metadata
should identify the same certified route. With those changes and equivalent
negative controls for a token-printing interpreter and an in-tree valid
bytecode cache, the software-side basis for **fully validated** would be
restored.
