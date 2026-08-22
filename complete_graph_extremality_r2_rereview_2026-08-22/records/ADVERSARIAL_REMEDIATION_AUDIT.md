# R2 adversarial remediation, supply-chain, and bypass audit

Date: 2026-08-22 (America/Los_Angeles)  
Package audited: `work/package`  
Method: static source/archive inspection only. I did **not** execute a delivered
shell or Python program, import a delivered module, install a dependency, or
make a network request. The commands used for this audit are recorded separately
in `records/ADVERSARIAL_REMEDIATION_AUDIT_COMMANDS.log`.

## Readiness verdict

**Conditionally ready for the controlled package-level replay; not safe to call
the direct replay's preflight “authenticated.”** Before execution, the referee
must use a trusted absolute CPython 3.14.6 executable, a trusted/sanitized
`PATH`, a private clean temporary/home/cache area, and an immutable fresh copy
whose source commit and manifests have been independently checked. Under those
preconditions, the R2 mandatory route is materially fail-closed and the prior
optimization-elision defect is remediated.

One new high-impact bypass remains in the *direct* entry point: an executable
selected through `PYTHON` can delegate only the preflight to genuine Python,
then return status 0 for every scientific command. It will satisfy the marker
test and let `replay.sh` exit 0 without running a verifier. The package-level
positive route does not inherit `PYTHON` for this step—it creates a fresh venv
and sets `PYTHON` itself—but the negative control using `/usr/bin/true` does not
detect this selective-wrapper attack. Therefore:

- root may proceed with `run_all_referee_checks.sh` only under the trust and
  environment preconditions below;
- a success from a separately invoked `replay.sh` is not, by itself, an
  adversarially authenticated certificate;
- no new mathematical counterexample is asserted here. This report concerns
  replay assurance and supply-chain boundaries.

## Comparison with the first-round findings

The first-round adverse report identified 406 optimization-elidable assertions
as its sole verdict-changing issue
(`complete_graph_extremality_referee_audit_2026-08-22/records/adversarial_falsification.md:68-107`),
plus inherited environment, unhashed dependency, Make, and document-resource
risks (`:141-154`). R2 makes the following substantive corrections:

1. `run_all_referee_checks.sh:4-15`,
   `submission/bootstrap_replay.sh:4-15`, and `replay.sh:4-15` reject a nonzero
   inherited `PYTHONOPTIMIZE`, unset Python/import/Make overrides, disable user
   site packages, and disable bytecode writes.
2. `submission/verify_execution_safety.py:63-70` implements an explicit
   exception-based `require`. Its fixed inventory at `:36-57` expects the same
   406 scientific conditions found in round 1, while `:119-152` rejects any AST
   `assert` and requires the per-file `require` counts exactly. Static comparison
   found all 20 scientific files migrated count-for-count and no remaining bare
   Python `assert` statement. Each delivered `require` helper raises
   `CertificateFailure` rather than depending on `__debug__`.
3. The safety runtime explicitly requires Python 3.14.6, optimization level 0,
   isolated mode, and an empty unsafe-environment set
   (`verify_execution_safety.py:73-85`). The launcher independently performs
   the version/optimization gate at `run_all_referee_checks.sh:22-29`.
4. The bootstrap clears and recreates `.venv-paper1`
   (`bootstrap_replay.sh:32-35`), then installs three exact requirements with
   `--no-deps --only-binary=:all: --require-hashes` (`:35-40`).
5. Make is no longer in the mandatory graph. The launcher checks only Tectonic
   and Poppler (`run_all_referee_checks.sh:31-52`), and `replay.sh:59-96`
   directly invokes the unit suite and all 17 named verifier/cross-check
   programs. Consequently inherited `MAKEFLAGS` cannot suppress a scientific
   failure.
6. The previously inert helper mains are now accurately disclosed at
   `CLAIM_CODE_MAP.md:20-35` and `README_FIRST.md:37-40`: their used functions
   remain reachable, while the three guarded exploratory/open-route suites are
   expressly non-load-bearing.
7. R2 adds three useful failure-path controls—explicit false under normal and
   optimized Python and inherited optimized mode—at
   `run_all_referee_checks.sh:66-106`, plus the `/usr/bin/true` control at
   `:108-120`.

These changes fix the earlier `python -O` overall-exit-0 defect for a genuine
interpreter. There is no bare-assert route left for `-O` to erase.

## Findings

### R2-SC-1 — High for direct replay: the interpreter marker is forgeable

`replay.sh:24` accepts an arbitrary caller-selected `PYTHON`. Lines `:26-40`
check only that it is executable/resolvable. Lines `:42-55` run the command,
accept any stdout containing the public constant
`PAPER1_EXECUTION_SAFETY_OK`, and then reuse the same command for every
scientific invocation at `:62-96`.

A selective wrapper can therefore:

1. recognize `verify_execution_safety.py` in its arguments and delegate that
   one call to genuine CPython, obtaining the genuine marker; and
2. return 0 without doing anything for all subsequent arguments.

All 18 child commands then have status 0 and, because there is no required
per-program output token, `replay.sh` itself reaches status 0. The negative
control at `run_all_referee_checks.sh:108-120` catches `/usr/bin/true` only
because it emits no marker. Calling this check “authenticated” at `:116` is not
supported by the protocol.

This does **not** bypass the ordinary package-level positive path when its
bootstrap Python and filesystem are trusted: `bootstrap_replay.sh:33` creates
the venv and `:45` explicitly sets `PYTHON` to that venv's interpreter. It does
invalidate direct-replay success as evidence in a hostile environment.

Recommended correction: do not permit `PYTHON` in the evidentiary direct route;
invoke only the expected freshly created venv interpreter. At minimum, have the
preflight print `sys.executable`, bind later invocations to that canonical path,
and require distinct completion tokens from every program. Even that remains
conditional on trusting the executable/OS; a command cannot cryptographically
authenticate itself.

### R2-SC-2 — High for standalone/direct replay: source audit ignores importable extras and caches

The safety preflight is isolated (`replay.sh:42-44`), but the scientific
programs are not invoked with `-I`. Instead, `run_python` deliberately supplies
`PYTHONPATH="$root"` at `replay.sh:62-64`. The source audit obtains its set from
`bundle_manifest.collect(REPO)` (`verify_execution_safety.py:119-129`). The
collector scans only the `INCLUDE` roots (`bundle_manifest.py:23-54,114-132`),
and deliberately excludes `__pycache__` and `.pyc`
(`bundle_manifest.py:56-73,90-111`). It does not require that the project tree
contain no other importable files.

Consequences for a direct extraction/replay:

- an extra project-root module (including `sitecustomize.py` or a name that
  shadows an imported module) is outside the collector's inclusion set but is
  importable through the later `PYTHONPATH`;
- a compatible adjacent `.pyc` can be read even though
  `PYTHONDONTWRITEBYTECODE=1` prevents new bytecode writes; and
- `shasum -c MANIFEST.sha256`, recommended at
  `submission/BUNDLE_REPRODUCTION.md:56-69`, verifies listed bytes but does not
  reject extra files.

The source-count audit would therefore still pass while an extra or excluded
artifact can affect later imports. The package-level route substantially
mitigates this: `verify_referee_package.py:50-72` rejects every symlink and any
unexpected regular file before the verified extracted tree is copied at
`run_all_referee_checks.sh:54-64`; the frozen package statically contains no
symlink, special node, `__pycache__`, `.pyc`, or `.pyo`. This mitigation assumes
no writer can alter the tree between verification and copy.

Recommended correction: before loading `bundle_manifest.py` or importing any
project module, reject every cache/bytecode file and require an exact
manifest-derived regular-file set. Avoid a broad project-root `PYTHONPATH`; use
an explicit, verified import root, and consider isolated scientific invocations.

### R2-SC-3 — Medium assurance boundary: document tools and cache record are trusted

`build.sh:8-9` pins the Tectonic v33 URL and a digest, but compilation occurs at
`:29-31` **before** the script reads Tectonic's URL-to-content cache record at
`:33-45`. The script checks the text stored in that record; it never opens and
independently hashes the resource bundle bytes used for compilation. The claim
is therefore conditional on Tectonic 0.16.9's cache semantics. Static inspection
cannot establish that the record still corresponds to the exact bytes consumed
in this run.

In addition, the launcher/build resolve `tectonic`, `pdfinfo`, `pdftoppm`,
`sed`, `tr`, `install`, `find`, `cmp`, and other utilities through inherited
`PATH` (`run_all_referee_checks.sh:31-52,125-128`; `build.sh:11-54`). Exact
version strings are self-reported. A coordinated hostile shim can report the
expected versions, copy the already-delivered PDF as the “build,” synthesize the
expected cache-record text, and/or make `cmp` return 0. Thus the final document
PASS is meaningful only with trusted resolved tools and a trusted cache.

This does not weaken the mathematical replay: the package itself says the exact
theorem checks are independent of document tools
(`README_FIRST.md:53-59`; `submission/ENVIRONMENT.md:49-52`). The trusted final
`cmp` does give a strong output-level check, but it is not an independent
pre-use verification of Tectonic's input bundle.

Recommended correction: download or vendor the bundle, independently SHA-256
it before use, and pass a local verified path to Tectonic. Record canonical
paths and hashes/signatures of the document tools and core utilities, or launch
under a minimal trusted `PATH`.

### R2-SC-4 — Low portability/auditability: wheel hashes have no filename/tag map

`requirements-lock.txt:2-36` contains exact pins and 32 hashes: one SymPy hash,
30 python-flint hashes, and one mpmath hash. The bootstrap's pip flags have the
right fail-closed semantics:

- `--require-hashes` requires an allowed digest for every selected artifact;
- `--only-binary=:all:` rejects source distributions; and
- `--no-deps` prevents undeclared transitives, while mpmath is explicitly
  present.

An index serving the right name/version but different bytes should fail. A
platform with no compatible hash-listed wheel should also fail, rather than
fall back to an sdist. Inherited pip index/config variables are not cleared, so
they can change availability or cause denial of service, but cannot silently
authorize different bytes under a correct SHA-256 implementation.

The static lock does not associate any hash with a wheel filename or Python/ABI/
platform tag. Consequently it is impossible from the delivered text alone to
verify the statement that these are all intended wheels, to identify all
supported platforms, or to tell which of the 30 python-flint hashes is expected
on a particular host. This is a reproducibility/documentation gap, not a
fail-open hash gap. The package should ship the PyPI release-metadata snapshot
or a generated filename/tag/hash table and state its supported platform set.

The installer itself is also not version/hash pinned: `bootstrap_replay.sh:33`
uses whatever pip is seeded by the chosen Python distribution. Record and pin
that trust component if byte-for-byte environment reproducibility is claimed.

### R2-SC-5 — Low: post-install dependency identity is version/origin, not bytes

`verify_execution_safety.py:88-107` checks distribution versions, imports, and
requires each module origin to lie under `sys.prefix`. That is a useful defense
against external `PYTHONPATH`, but it does not re-hash installed files against
the wheel's RECORD or the lock. A mutated package within the venv can retain the
same metadata/version/origin and pass. Fresh `venv --clear` plus hashed install
is adequate against stale benign state; it is not adequate against a malicious
installer, allowed malicious artifact, writable venv race, or hostile local
filesystem. Treat those as execution-substrate trust boundaries, or add a
post-install RECORD/hash audit.

### R2-SC-6 — Low: the 406-check guard is syntactic, not semantic/reachability proof

`verify_execution_safety.py:129-147` rejects AST `Assert` nodes and counts calls
whose unqualified function name is exactly `require`. It does not prove that a
condition remains nontrivial, that a call is reachable, or that the local
`require` has not been redefined. The intentional false control at
`run_all_referee_checks.sh:66-92` tests the safety module's helper, not a
theorem-bearing verifier's failure branch.

Static R2 comparison found the actual migration mechanical and count-preserving,
so this is not evidence of a present mathematical omission. For stronger future
regression protection, mutate one condition in a disposable copy of each
program family to false and require a nonzero top-level result, or require a
signed per-program completion inventory.

### R2-SC-7 — Low: integrity checks are strong but not external authentication

`verify_referee_package.py:30-47` rejects malformed, duplicate, absolute, and
parent-traversing manifest names. It rejects package symlinks and exact-matches
the regular-file set/digests at `:50-72`. It reads rather than extracts the tar,
requires sorted unique regular members, canonical safe names, exact internal
manifest coverage/hashes, and byte equality with the delivered extracted tree
at `:75-127`. Static tar inspection found 71 regular members and no link member.
These checks fail closed for archive traversal, tar symlinks/hardlinks, missing
files, extra regular files, and altered listed bytes.

Two boundaries remain:

- the verifier ignores unexpected non-regular, non-symlink nodes at
  `verify_referee_package.py:56-60`; an extra FIFO/socket is not part of its
  `actual` set. Such a node is not presently load-bearing, so this is chiefly a
  completeness/DoS issue;
- all delivered manifests/digest prose can be replaced together. They provide
  integrity relative to the package, not publisher authentication. The stated
  source commit (`README_FIRST.md:13-24`) must be compared independently with a
  trusted repository/ref or signed external digest.

## Invocation and failure-propagation result

The mandatory positive chain is:

```text
/bin/sh run_all_referee_checks.sh
  -> trusted bootstrap Python -I: version/optimization check
  -> trusted bootstrap Python -I verify_referee_package.py
  -> bootstrap_replay.sh
       -> safety --runtime
       -> venv --clear
       -> venv pip --require-hashes --only-binary --no-deps
       -> safety --runtime --dependencies --audit-sources
       -> PYTHON=<fresh venv python> replay.sh
            -> safety preflight
            -> unittest suite
            -> 17 directly named verifier/cross-check programs
  -> build.sh
       -> Tectonic compilation and cache-record check
       -> pdfinfo and pdftoppm
  -> trusted cmp against frozen PDF
  -> rebuilt-PDF SHA-256 print
```

All shell layers use `set -eu` and no scientific command is in a status-masking
pipeline or unconditional-success wrapper. Under a genuine interpreter, an
uncaught `CertificateFailure`, unit-test failure, pip failure, missing wheel,
hash mismatch, tool failure, or PDF mismatch propagates nonzero. Every one of
the 17 advertised top-level programs is present at `replay.sh:65-96`. The three
other bundled diagnostic mains remain inert, but `CLAIM_CODE_MAP.md:20-35`
correctly classifies them as exploratory/open-question code rather than a
manuscript-theorem dependency.

## Hostile-environment scenarios predicted from source

| Scenario | Expected current result | Assessment |
|---|---|---|
| `PYTHONOPTIMIZE=1` at any main replay entry | Status 2 before replay (`run_all`:4-10; bootstrap/replay:4-10) | Fail closed |
| Genuine `python -O` runs `--intentional-failure` | Nonzero because `require(False, ...)` remains (`safety:67-70,172-174`) | Fail closed |
| Inherited `PYTHONPATH`, `PYTHONHOME`, or external `PYTHONPYCACHEPREFIX` | Unset before preflight (`run_all`:11-15) | Fail closed for inherited values |
| Inherited `MAKEFLAGS=-i` | Unset; Make is not invoked | Fail closed/not applicable |
| `PYTHON=/usr/bin/true replay.sh` | Status 2: marker absent (`replay:42-54`) | Existing control is valid but narrow |
| Selective `PYTHON` wrapper delegates preflight, then returns 0 | **Overall direct replay status 0 with verifiers skipped** | Confirmed static bypass hypothesis; high priority negative test |
| Wrong-hash wheel from hostile index/cache | pip nonzero (`bootstrap:35-40`) | Fail closed, assuming genuine pip/hash implementation |
| No compatible python-flint wheel for host tags | pip nonzero; no sdist fallback | Fail closed but unsupported platform |
| Added root `sitecustomize.py` or module in direct extraction | Source audit does not include it; later `PYTHONPATH=$root` can import it | Direct-entry bypass surface |
| Added compatible `__pycache__/*.pyc` in direct extraction | Collector excludes it; bytecode writes are disabled but reads are not | Direct-entry bypass surface |
| Added regular file or symlink to frozen package | Package verifier nonzero (`verify_referee_package.py:56-71`) | Fail closed |
| Archive `../`/absolute member, symlink, or hardlink | Package verifier nonzero (`:84-103`) | Fail closed without extraction |
| Extra FIFO/socket in package | Ignored by regular-file set (`:56-60`) | Low-severity completeness gap |
| Hostile `tectonic`/`cmp` shims in `PATH` | Can self-report/copy/pass and reach final PASS | Trusted PATH is mandatory |
| Poisoned Tectonic cache record/content | Outcome depends on Tectonic's internal content-addressing; script checks record only after use | Must test with trusted Tectonic; static proof incomplete |
| Source tree changed after package verification but before copy/run | Potentially consumed | Require immutable/private tree; TOCTOU trust boundary |

## Execution preconditions

Before root runs any delivered code:

1. Verify the advertised commit `e63cc44748e4084ade67c5ff7dc5d1bf2a872f7c`
   against a trusted local Git object/ref independently of the delivered
   manifests. Then run the package verifier from a private immutable copy.
2. Set `BOOTSTRAP_PYTHON` to a **trusted absolute** CPython 3.14.6 executable,
   not a wrapper or a name resolved through hostile `PATH`. Record its canonical
   path, SHA-256/code signature, full version/build, and `sys.flags`.
3. Use a minimal trusted `PATH`. Resolve and record the paths/hashes of `sh`,
   `dirname`, `mktemp`, `cp`, `rm`, `grep`, `cat`, `sed`, `cmp`, `mkdir`,
   `install`, `find`, `tr`, Tectonic 0.16.9, and Poppler 26.08.0. Do not rely on
   version text alone.
4. Use private fresh absolute directories for `TMPDIR`, `HOME`, and
   `XDG_CACHE_HOME`, owned and writable only by the referee. Prevent concurrent
   modification of the package, temp copy, venv, and tool/cache directories.
5. Prefer an otherwise empty environment. In addition to the variables already
   cleared by the scripts, clear pip/index/config/proxy/certificate overrides or
   set a consciously trusted index/cache and `PIP_CONFIG_FILE=/dev/null`.
6. Ensure the selected platform has a hash-listed CPython 3.14 python-flint
   wheel. Record the exact selected filename/tag/hash and pip version. Absence
   should be treated as an unsupported platform, not worked around with an
   sdist.
7. Either preseed and independently verify the Tectonic v33 bundle in a private
   cache or allow the documented network fetch, then record the actual resource
   bytes/digest if possible. Do not reuse an untrusted shared Tectonic cache.
8. Run the package-level `run_all_referee_checks.sh`, not bare `replay.sh`, and
   preserve stdout, stderr, the true top-level exit status, resolved tool
   identities, selected wheel filenames/hashes, and rebuilt PDF hash.

## Post-readiness adversarial test plan for root

Run each mutation only in a new disposable copy and log the command, environment,
stdout/stderr, and exact status.

1. **Baseline:** execute the package-level route with the preconditions above;
   require status 0 and every expected per-program completion line.
2. **Optimization controls:** run with inherited `PYTHONOPTIMIZE=1` and `=2`
   (expect status 2), and invoke the safety intentional failure under `-O`
   (expect nonzero and the intentional token).
3. **Selective-interpreter bypass:** create a wrapper that delegates only the
   safety-preflight argument pattern to the trusted Python and returns 0 for
   everything else; set `PYTHON` to it for direct `replay.sh`. **Expected current
   behavior: status 0.** This confirms R2-SC-1 and must not be accepted as a
   certificate.
4. **Program-failure propagation:** in a disposable copied tree, change one
   actually reached theorem `require` condition to `False`, update no manifest,
   and invoke that copied replay only after separately accounting for integrity
   gates. Expect nonzero. Repeat for at least one unittest and one program in
   each phase family.
5. **Extra-source/cache controls:** add project-root `sitecustomize.py`, a benign
   shadow module, and an inert `__pycache__`/`.pyc` sentinel in separate direct
   extraction copies. Determine whether `--audit-sources` rejects them.
   **Expected current behavior: it does not.** Then confirm the package-level
   exact file-set verifier rejects regular/cache additions.
6. **Hash lock:** point pip at a local directory containing a same-name/version
   wheel with a nonlisted digest (expect nonzero); remove the compatible wheel
   (expect nonzero); then record the filename/tag/hash selected in the positive
   install.
7. **Pip configuration:** repeat the bootstrap with hostile `PIP_INDEX_URL`,
   `PIP_FIND_LINKS`, `PIP_CONFIG_FILE`, and cache variables. Wrong bytes must
   never install; availability failures must propagate nonzero.
8. **Package/archive mutations:** test an extra regular file, package symlink,
   altered listed byte, duplicate tar name, traversal name, tar symlink, and tar
   hardlink. Expect nonzero before copy/extraction. Separately test an extra FIFO
   to document the present low-severity omission.
9. **Document cache:** with genuine Tectonic, test an empty private cache, a
   wrong URL-record digest, a missing content object, and mismatched cached
   content. Every mismatch must be nonzero, and the used resource bytes should
   independently hash to the declared digest before accepting the build.
10. **PATH shims:** prepend shims for `tectonic`, `pdfinfo`, `pdftoppm`, and
    `cmp` in a disposable environment to demonstrate that self-reported version
    gates are not authentication. Then rerun with the trusted minimal PATH and
    record resolved executable hashes.

## Bottom line

R2 genuinely fixes the earlier optimized-Python certificate failure and closes
the inherited Python/Make environment and unhashed-wheel paths under a trusted
execution substrate. The lock is fail-closed for artifact substitution, archive
handling is strong, failure propagation is direct, and all load-bearing
top-level verifiers are reached.

The strongest remaining issue is not mathematical: direct replay can still
silently pass through a selective fake interpreter, and direct source audit can
miss importable extras/caches. The document claim also remains conditional on
trusted PATH tools and Tectonic's cache-record semantics. With the stated
preconditions, the **package-level** replay is ready to run; without them, a
terminal PASS is not independently trustworthy.

## Evidence addendum — confirmed adversarial outcomes

Added after the static audit on 2026-08-22. The root referee supplied the
following execution outcomes. I did **not** rerun any delivered program. I
independently read the preserved transcript as text to locate the supporting
entries in `records/COMMANDS.log`.

### Confirmed outcomes

1. **Authoritative clean package route: exit 0.** The recorded `env -i`
   invocation uses an absolute Python 3.14.6 and constrained `PATH` at
   `COMMANDS.log:2980-2982`. Package/archive/PDF identity succeeds at
   `:2983-2987`; all four built-in negative controls succeed at `:2988-2991`;
   the hashed environment and source audit report 406 scientific and 418 total
   explicit checks at `:3003-3010`; the unit suite and all 17 named top-level
   programs complete at `:3011-3163`; the pinned Tectonic bundle is reported at
   `:3172-3173`; and the rebuilt PDF has the frozen SHA-256 and a byte-identical
   final result at `:3191-3193`. This converts the package-level readiness
   judgment from predicted to demonstrated for the recorded clean environment.

2. **Public-token fake interpreter: direct replay exit 0.** The hostile
   `PYTHON` invocation is recorded at `COMMANDS.log:3195-3197`; the public marker
   is printed once for the preflight and for each skipped child at `:3198-3216`;
   direct replay exits 0 at `:3217`. This confirms R2-SC-1 exactly: the marker is
   presence detection, not authentication, and the `/usr/bin/true` negative
   control does not cover a marker-aware command.

3. **Hostile timestamp-valid bytecode: unchanged source, direct replay exit 0,
   payload executed.** The fixture preserves the source SHA-256
   `8be62ba2236d48b9f624e5b6df612a6bcd05534f8a1bd5771b9c7f38368a2eef`
   before and after adding the `.pyc` (`COMMANDS.log:3244-3251`). The direct
   replay safety audit still reports all 406/418 checks at `:3253-3259`, the
   replay completes with exit 0 at `:3394-3395`, and the hostile cache creates
   the `PYCACHE_EXECUTED` marker while the source retains that same hash at
   `:3397-3402`. This is code execution, not merely an ignored inert extra.

4. **The documented standalone manifest check also exits 0 with the extra
   bytecode.** After correcting two test-fixture path issues, the final check at
   `COMMANDS.log:3471-3476` reports
   `MANIFEST_STATUS_WITH_EXTRA_PYCACHE=0` while listing the hostile `.pyc`.
   Thus checking every listed source hash does not establish an exact extracted
   file set.

5. **Tampered dependency hash: rejected with status 1.** Pip reports the
   expected all-zero test digest versus the actual SymPy wheel digest and the
   captured bootstrap status is 1 (`COMMANDS.log:3307-3313`). This confirms the
   lock is fail-closed for wrong artifact bytes on the tested platform.

6. **Wrong expected Tectonic bundle digest: rejected with status 2.** The build
   reports the test digest mismatch and captured status 2 at
   `COMMANDS.log:3321-3337`. This confirms the honest-tool/cache-record mismatch
   path propagates. It does not remove the distinct static trust boundary for a
   hostile PATH tool or establish an independent pre-use hash of the resource
   bytes.

7. **Inherited optimization: rejected with status 2.** The package launcher
   emits its explicit rejection and returns 2 at `COMMANDS.log:3344-3349`.
   Together with the clean 406-check run, this confirms the first-round
   optimization-elision defect is fixed for a genuine interpreter.

### Severity reassessment

- **R2-SC-1 remains High for the direct entry point and is now dynamically
  confirmed.** It permits a complete false-positive replay transcript/status.
- **R2-SC-2 is elevated from Medium to High for the documented standalone
  extracted-archive route.** The hostile `.pyc` executed with unchanged source
  hashes, a passing source audit, a passing standalone manifest check, and an
  overall direct-replay status 0. This directly falsifies any unqualified claim
  that those checks bind executed code to listed source.
- **Both High findings are contained, but not repaired, by the clean
  package-level route.** `verify_referee_package.py` exact-matches regular files
  and rejects symlinks before copying the frozen clean tree. The authoritative
  clean run demonstrated this route successfully. Its evidentiary force still
  assumes a trusted interpreter, PATH utilities, private tree, and absence of a
  verification-to-copy race.
- The dependency-hash, bundle-record mismatch, and inherited-optimization
  controls are now empirically verified fail-closed. Residual wheel coverage,
  document-tool identity/cache semantics, and post-install mutation issues keep
  their earlier Low/Medium trust-boundary classifications; none is shown to
  have produced a false theorem result in the authoritative run.

### Required artifact corrections

1. Make `bootstrap_replay.sh` and any evidentiary direct replay perform the same
   exact regular-file/symlink/special-node comparison as the package verifier,
   and reject all `__pycache__`, `.pyc`, and `.pyo` before importing any project
   helper or running any certificate. A plain `shasum -c` is insufficient.
2. Remove arbitrary `PYTHON` selection from the certificate-bearing direct
   route and bind execution to the freshly constructed venv interpreter. If
   arbitrary interpreters remain useful for development, label that route
   non-authenticating and non-evidentiary.
3. Remove the word “authenticated” from
   `run_all_referee_checks.sh:114-120`, or implement a trust model that actually
   binds the command and each program execution. Require a distinct completion
   token/inventory from every reached program as defense in depth.
4. State explicitly that the package-level verified-copy route is the sole
   referee certificate until the two standalone defects are corrected.

### Final referee recommendation among the four offered options

**Valid after minor corrections.**

The mathematical conclusion remains supported: the authoritative clean route
executed all 406 scientific checks and all 17 load-bearing programs, reproduced
the pinned document and byte-identical PDF, and no mathematical counterexample
or proof/code mismatch emerged from either review round. The two confirmed High
findings concern whether the standalone/direct artifact can certify that its
checks ran; they do not contradict a theorem or invalidate the authoritative
clean package-level execution.

“Fully validated” would be inappropriate because two advertised entry-point
assurance properties are demonstrably false. “Major correction required” or
“invalid” would overstate the consequence because the defects have narrow scope
and small, concrete remedies—strict exact-file/cache rejection, a fixed trusted
venv interpreter, and corrected authentication/scope wording—without changing
the manuscript mathematics, certificates, expected values, or proof. The impact
on artifact evidence is High; the editorial/engineering remediation remains
Minor.
