# Independent package/software re-audit: Paper II v2.0.2

**Audit date:** 2026-08-22 (America/Los_Angeles)

**Audited disposable input:** `work/agent_v202_package/package_canonical`, copied
byte-for-byte and mode-for-mode from `delivered_copy`

**Scope:** package identity, archive safety and determinism, Git binding,
dependency provenance and offline replay, interpreter selection, executable
inspection, fail-closed behavior, and regression behavior.  Mathematical truth
is deliberately outside this report: successful programs are not treated as
proofs.

## Conclusion

**Package/software status: submission-ready.**  I found no submission-blocking
package, software, provenance-consistency, or replay defect in v2.0.2.  The two
prior software findings are repaired:

1. Verification-critical bare assertions have been replaced by explicit checks,
   every Python verification entry point rejects optimized execution, and
   independent mutations fail without a success sentinel.
2. SymPy and mpmath are present as upstream-identical pure-Python wheels,
   selected with `--no-index` and `--require-hashes`; a fresh replay and the
   entire deterministic rebuild succeeded while the operating-system network
   sandbox denied all network access.

There is one non-blocking documentation nit: `vendor/README.md:27` refers to an
unbundled `submission/ENVIRONMENT.md`.  The same external-tool limitation is
fully disclosed in the bundled top-level `README_FIRST.md:75-82`,
`VERSION.md:20-23`, and `BUNDLE_METADATA.txt:14-15`, so this does not impede a
referee or affect any identity, replay, or scientific claim.  I would not reopen
the frozen package solely for that cross-reference.

## Frozen identities and exact binding

| Item | Independently observed value | Status |
|---|---:|---|
| Convenience/source PDF SHA-256 | `4e86597bb0baff388e8ce7ccf6ffd808f86b5ea846acf6f2188b31016fd2572c` | PASS |
| Source/certificate archive SHA-256 | `d2145513f8abe295e9e7fab62f062fa9d0f7a6282de95e8155f3db4621485274` | PASS |
| Transferable referee archive SHA-256 | `2216c6a31545b38d9ca89c9d43c5a309bfcc6c2c1f7ab63ea5fabc171116e1d2` | PASS |
| Scientific commit | `03e94e877ce10d9d459fd284bd652934cde08bb3` | PASS |
| Annotated tag object | `be3946c051c7f7e2073d6adf81bca31ae750251a` | PASS |
| Annotated tag | `simultaneous-amplification-beyond-three-halves-v2.0.2` | PASS, unsigned |
| Wrapper commit | `0dcb450a1081e98d2ae1029d513c8343e5fd4328` | PASS; ancestor of current local/remote `main` |

The current local and remote `main` tip during this audit was
`7962e61dc0f9550a640f9637fb5c7c6d074ac20f`; the stated wrapper commit is in its
ancestry.  Thus “wrapper commit on main” remains true even though later unrelated
commits have advanced the branch.

The PDF is 213,182 bytes, has 21 letter-sized pages, no encryption, forms, or
JavaScript, and the convenience PDF is byte-identical to the PDF inside the
source tree.  This report did not perform the separate visual manuscript review.

## Independent manifest and archive audit

I did not rely on the supplied verifier for this check.  The independent
standard-library auditor in `independent_checks/agent_v202_package_audit.py`
reported:

- 34 payload files exactly covered by `PACKAGE_MANIFEST.sha256`, plus the
  manifest itself (35 files total);
- exact SHA-256 and required `0644`/`0755` mode for every payload;
- no symlinks or non-regular filesystem nodes;
- a source archive of exactly 23 unique, lexicographically sorted, regular,
  canonical relative members;
- no absolute path, `..` traversal, duplicate, link, device, or noncanonical
  member;
- exact per-member modes, UID/GID 0, owner/group `root`, and fixed mtime
  1787356800;
- exact detached checksum, exact internal manifest file set, and every internal
  SHA-256;
- byte- and mode-identity between each archived member and the supplied
  extraction;
- byte-identity between both PDF copies.

The wrapper archive was independently parsed before any extraction.  It contains
exactly 35 unique, sorted, safe regular members.  After stripping its single
top-level directory, its file set, bytes, and modes exactly match both the live
referee folder and this audit's `delivered_copy`.

The supplied verifier implements the same fail-closed boundaries at
`verify_referee_package.py:98-115` (manifest syntax/path/duplicate checks),
`:118-157` (whole-package set, mode, and hash checks), `:160-259` (detached
checksum, safe archive, internal manifest, extraction, PDF, and frozen metadata),
and `:262-277` (neutral-prompt markers).  Its normal run exited 0 and reproduced
the frozen hashes.  A one-line scientific-source mutation was rejected at
`:154-156` as an outer-manifest mismatch.

The archive builder uses an exact nonrecursive whitelist
(`bundle_manifest.py:24-49`), exact executable set (`:51-61`), symlink and mode
guards (`:106-131`), deterministic tar metadata (`:134-143`), atomic output
replacement (`:189-208`), and a post-write exact whitelist/hash audit
(`:214-277`).  Both ordinary and network-denied full runs rebuilt an archive
byte-identical to the supplied archive.

## Git/tag/blob binding

Local inspection and a fresh `git ls-remote` agreed on both tag references:

- tag object `be3946c051c7f7e2073d6adf81bca31ae750251a`;
- peeled commit `03e94e877ce10d9d459fd284bd652934cde08bb3`.

The tag object is annotated and its payload begins with that scientific commit.
An independently written auditor compared all 21 repository-backed archive
members with the Git tree at the scientific commit.  Every path existed exactly
once as a blob; every `100644`/`100755` tree mode matched the archive mode; every
blob was byte-identical.  The two remaining archive members are the declared
synthetic `BUNDLE_METADATA.txt` and `MANIFEST.sha256`.

The supplied implementation independently passed the same comparison.  Its
relevant boundaries are `verify_git_binding.py:18-55` (frozen constants and
executable set), `:94-126` (safe unique sorted archive and exact modes),
`:129-150` (annotated-tag binding), and `:152-172` (all source blobs and modes).
Lines `187-192` accurately disclose that this does not authenticate an unsigned
tag, checkout, authorship, or hosting account.

## Dependency and offline replay audit

`requirements.txt:1-9` sets `--no-index`, restricts candidates to the bundled
`vendor` directory, permits wheels only, requires hashes, and pins:

| Wheel | SHA-256 | Independent wheel audit | PyPI release metadata |
|---|---|---|---|
| `mpmath-1.3.0-py3-none-any.whl` | `a0b2b9fe80bbcd81a6647ff13108738cfb482d481d826cc0e02f5b35e5c88d2c` | 92 safe members; all RECORD hashes/sizes valid | exact match; not yanked |
| `sympy-1.14.0-py3-none-any.whl` | `e091cc3e99d2141a0ba2847328f5479b05d94a6635cb96148ccb3f34671bd8f5` | 1,570 safe members; all RECORD hashes/sizes valid | exact match; not yanked |

Both distributions declare `Root-Is-Purelib: true` and `Tag: py3-none-any`, have
the expected name/version metadata, contain their upstream license material,
contain no duplicate/encrypted/symlink/path-traversal member, and are
byte-identical to the corresponding PyPI release files by SHA-256.  This is a
strong supply-chain identity check; it is not a line-by-line security audit of
the upstream SymPy/mpmath projects.

The network-denial control first attempted HTTPS access to PyPI under
`sandbox-exec` and failed with status 6 (`Could not resolve host`).  Under the
same `(deny network*)` sandbox, a fresh `bootstrap_replay.sh`:

- created a new Python 3.14.6 virtual environment;
- installed only the two local wheels;
- reported SymPy 1.14.0 and mpmath 1.3.0;
- completed every certificate and fail-closed regression with exit 0.

An independent requirements-hash mutation changed one expected digest by one
hex digit.  Offline pip stopped with status 1 and printed the expected-versus-
actual SHA-256; no replay followed.

The entire top-level rebuild, including Tectonic and Poppler, also succeeded
under network denial and reproduced both frozen hashes.  This machine had a
populated Tectonic resource cache.  The package correctly does **not** claim that
document rebuilding is universally offline on a clean machine: Python wheels
are vendored, while Python itself, Tectonic 0.16.9, Poppler 26.08.0, and
Tectonic's TeX resources remain external.

## Executable/import inspection

Every package-controlled shell/Python entry point was read in full before its
first execution:

| File | Lines inspected | Result |
|---|---:|---|
| `run_all_referee_checks.sh` | 1-88 | Safe temporary copy; exact runtime/tool checks; local-only pip; selected venv; byte comparisons; guarded cleanup |
| `verify_referee_package.py` | 1-298 | Standard library only; fail-closed manifest/archive/PDF/prompt audit |
| `verify_git_binding.py` | 1-197 | Standard library plus fixed-argument `git` subprocess calls; no shell interpolation |
| `all.sh` | 1-6 | Sequential replay then build under `set -eu` |
| `bootstrap_replay.sh` | 1-51 | Selected bootstrap interpreter; exact runtime; fresh venv; pinned install; replay and regressions |
| `build.sh` | 1-22 | Deterministic environment; Tectonic build; PDF metadata and page rendering |
| `release_bundle.sh` | 1-36 | Selected interpreter/venv; version guard; replay-before-build-before-archive |
| `replay.sh` | 1-31 | Selected interpreter; optimized-mode rejection; ordered verifier execution |
| `bundle_manifest.py` | 1-299 | Deterministic exact-whitelist archive builder and verifier |
| `certificates/verify_leading_algebra.py` | 1-120 | Explicit checks; SymPy only |
| `certificates/verify_hybrid_lumping.py` | 1-190 | Explicit checks; standard library only |
| `certificates/verify_hybrid_coefficients.py` | 1-193 | Explicit checks; SymPy only |
| `verify_paper_claims.py` | 1-257 | Explicit finite identities/scope markers; explicitly excludes analytic proofs |
| `tests/test_verifier_fail_closed.py` | 1-312 | AST, subprocess, optimization, mutation, and failure-propagation regressions |

A package-wide static search found no `eval`, `exec`, `pickle`, `marshal`,
`os.system`, `shell=True`, networking library, or bare `assert` in controlled
Python programs.  The only subprocess use is the fixed-argument Git comparison
and the regression runner, both inspected above.  The only third-party import is
SymPy (with mpmath as its pinned dependency); the exact upstream wheel identity
and complete wheel RECORDs were verified before installation/import.

## Optimized-mode and mutation results

The independent AST scan parsed eight controlled Python entry points and found
zero `ast.Assert` nodes: the two outer verifiers, archive builder, four scientific
verifiers, and fail-closed regression program.

Each of those eight programs was then invoked independently with `python -O`.
Every one exited 1 and none printed any `PASS` sentinel.  Independently invoking
`replay.sh`, `all.sh`, `bootstrap_replay.sh`, and `release_bundle.sh` with
`PYTHONOPTIMIZE=1` likewise produced status 1, no replay-complete sentinel, and
no release archive.  The top-level runner and both outer verifiers were also
checked directly and rejected optimized mode before substantive work.

The bundled regression program independently passed all of its checks:

- AST absence of bare assertions (`test_verifier_fail_closed.py:98-109`);
- normal and optimized direct execution (`:112-168`);
- optimized shell entry points and no artifact (`:171-223`);
- early and late mathematical mutations with failure propagation (`:252-297`).

I separately changed the expected Bd rational margin from `232/17361` to
`233/17361` in a disposable verifier copy.  Normal replay exited 1 exactly at the
explicit check and did not print the coefficient-audit or replay-complete
sentinel.  With optimization enabled, replay exited 1 before any verifier.  A
separate package-source mutation was caught by the outer manifest, and the hash-
pin mutation was caught by pip.  These independent probes confirm the behavior
rather than merely trusting the regression test's success message.

## Selected-interpreter plumbing and full replay

The top-level runner selects `BOOTSTRAP_PYTHON` at
`run_all_referee_checks.sh:5`, uses it for runtime validation and the package
verifier (`:16-26`), passes it into the bootstrap (`:63-64`), and explicitly
passes the resulting venv Python into release (`:66-67`).
`bootstrap_replay.sh:6-26` uses the selected interpreter to validate Python and
create the venv; `:28-50` verifies and uses that venv.  `replay.sh:6-29` and
`release_bundle.sh:10-36` consistently honor the selected `PYTHON`/venv.

An independently created logging interpreter shim was supplied as
`BOOTSTRAP_PYTHON` during a complete network-denied run.  It observed the
top-level runtime check, package-verifier invocation, bootstrap runtime check,
`-m venv` creation, and final hash calculation.  The run exited 0, while replay
and release used the newly created venv as designed.

The ordinary canonical run and an explicit network-denied canonical run both
exited 0 and printed:

```text
REBUILT_SOURCE_ARCHIVE_SHA256: d2145513f8abe295e9e7fab62f062fa9d0f7a6282de95e8155f3db4621485274
REBUILT_PDF_SHA256: 4e86597bb0baff388e8ce7ccf6ffd808f86b5ea846acf6f2188b31016fd2572c
PASS: manifests, pinned replay, deterministic archive/PDF rebuilds, and identities
```

The canonical input copy was hash- and mode-identical before and after both
runs.  At audit completion, all 35 delivered files remained hash- and
mode-identical to the untouched canonical disposable copy.

## Findings and limitations

| ID | Severity | Status | Exact location | Assessment |
|---|---|---|---|---|
| CODE-202-01 | Prior high, now resolved | PASS | All controlled Python verifiers; explicit guards noted above | No bare assertions; optimized mode fails closed; mutations propagate failure |
| REPRO-202-01 | Prior moderate, now resolved | PASS | `requirements.txt:1-9`, `vendor/*` | Offline, hash-pinned, upstream-identical wheels; fresh network-denied replay passed |
| PKG-202-01 | Prior hardening request, now resolved | PASS | `verify_referee_package.py:98-259`, `bundle_manifest.py:24-277` | Exact sets, safe canonical regular members, hashes, and modes enforced |
| GIT-202-01 | Prior provenance request, now resolved | PASS with disclosed boundary | `verify_git_binding.py:129-192` | Exact local/remote tag and 21 blobs/modes; unsigned tag does not authenticate authorship |
| DOC-202-01 | P3 / non-blocking | Optional polish only | `vendor/README.md:27` | Dangling `submission/ENVIRONMENT.md` reference; equivalent limitation is present in three bundled documents |
| LIMIT-202-01 | Disclosed external boundary | Not a defect | `README_FIRST.md:75-82`, `VERSION.md:20-23` | Clean-machine PDF build may need Tectonic resources/network; exact comparison fails closed if output differs |
| LIMIT-202-02 | Third-party trust boundary | Not a defect | vendored SymPy/mpmath wheels | Exact PyPI bytes and RECORDs verified; upstream projects were not line-by-line security-audited |

No program result in this report is used to infer the manuscript's analytic
proofs.  `verify_paper_claims.py:2-7` itself correctly limits its claims to
finite symbolic/rational identities and identifies the weak-cut,
establishment, cleanup, reciprocal-invasion, and global-sweep arguments as
analytic manuscript proofs.

## Command record and audit hygiene

Every shell command, working directory, start/end time, and exit status is in
`logs/commands.tsv` and `logs/full_transcript.log` under labels beginning
`agent-v202-code-`.  Expected nonzero statuses are retained for optimized-mode,
mutation, manifest, dependency-hash, and network-denial controls.  The ledger
also transparently retains two auditor setup mistakes: the first wrapper call
used the wrong argument order (status 200), and an initial zsh summary loop used
the read-only variable name `status` (status 1); both were immediately corrected
and did not run or alter package code.

All execution occurred in disposable copies or tool-created temporary
directories.  The delivered package and source repository were not modified;
no commit, push, upload, message, or external write was performed.  Read-only
network checks were limited to PyPI release metadata, the public Git remote, and
the explicit network-denial control.

**Completion estimate for this package/software sub-audit: 100%.**
