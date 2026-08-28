# R4 entry-point and optimized-Python audit

## Result

**FAIL (reproducibility/fail-closed entry-point claim); main release harness PASS.**

The current referee commands and the final quick/full harness reject optimized
Python before replay.  However, the recursively bound portable sweep still has
documented production entry points that do not reject it.  In particular,
`verify_package.py` exits zero and prints `K2P_OFFLINE_SWEEP_PACKAGE_PASS`
under `python -O`, while `resumable_four_port_driver.py` will run the production
classifier and write records under `-O`.

This contradicts:

- `work/final_theorem_release/README.md:182`, “Every entry point explicitly
  rejects `python -O`”; and
- `work/final_theorem_release/RELEASE_LOCK.json:24`,
  `python_optimized_mode: forbidden and explicitly rejected`.

It is not only a literal/documentation discrepancy.  The production atlas uses
Python `assert` for exact certificate semantics, including the target-zero
recheck at `atlas/k2p_atlas_core.py:823`.  A disposable mutation demonstrates
that normal mode rejects a non-kernel “separator,” whereas `-O` writes an
invalid `separated` record.  The official outer quick/full entry point is still
protected, so this finding does not establish a counterexample to the theorem
or invalidate the sealed clean certificates.

## Authorities inspected

| Artifact | SHA-256 | Relevant fact |
|---|---|---|
| `output/referee/README.md` | `d7cd6562816484e1070e28294e248a15312baaaacb2132ff98d3c0112ef4b707` | current referee command mapping |
| `work/final_theorem_release/README.md` | `3acb7f6a04bbe4d3c13e54fb491615f4973ef743f558fedb95dd0f09cfd73553` | universal line-182 claim |
| `work/final_theorem_release/RELEASE_LOCK.json` | `30132af1b10f7aba6d49ababf14551f9f914a19dc6a0638517761b6b85cf4c8d` | binds `verify_package.py` as runtime evidence and claims explicit rejection |
| portable `README.md` | `a2de59e5be0c3fa335fefbdd29786d525eac2bda072e4a52e3f65e59d2897b78` | documents qualification, guarded runner, shell runner, comparison |
| portable `README_DIRECT_CLOSURE.md` | `21429a217bef60ec020d91a9c3d0662e5c9d63458a9d86a144e698fed45b57d8` | documents direct verifier, mutation runner, driver, merger |
| portable `INPUT_LOCK.json` | `e94c6b55947e02fb7154b41b36030560df0eeb8e115dda5c8be3e7c6c5f17a94` | binds all portable scripts and atlas |
| portable `verify_package.py` | `bc2dc5714b0928beda31e96eb15954715133ee4a8ab7ba106b7c5a1b62ba83cc` | no optimized-mode guard; prints PASS at line 60 |
| portable `resumable_four_port_driver.py` | `6f18f74e8a64fce3c92d868944c0c75015c7c2d144ad1e97ffad6205a57aedbb` | no guard in `main` at lines 781–876 |
| portable `atlas/k2p_atlas_core.py` | `37e9b7910f7723c146a87ae2f60dfb62529b1a3e4866ccd72d65dc4efda923ad` | 22 assert sites; target-zero checks are load-bearing |

The final entry-point implementations inspected were bundle builder
`a0e0c600...`, release-lock builder `a49add91...`, quick/full verifier
`700c5d43...`, outer mutations `9d64e43f...`, corrected-universe mutations
`daaf95e6...`, outer output-contract test `cca34f0f...`, nested output-contract
test `d04913bd...`, and final-replay output-contract test `0dc983ab...`.

## Entry-point census

The following project entry points are documented in the four READMEs read for
this audit.  Environment creation and `pip` are third-party setup commands and
are excluded.

| Entry point | Rejects `-O`? | Observation |
|---|---:|---|
| `output/referee/build_referee_bundle.py` | yes | exit 1, `optimized Python is forbidden` |
| `work/final_theorem_release/build_release_lock.py` | yes | exact optimized-mode diagnostic |
| `verify_final_theorem_release.py --quick/--full` | yes | exit 1 before replay |
| `run_release_mutations.py` | yes | exit 1 before mutation execution |
| `run_corrected_universe_mutations.py` | yes | exit 1 and no report |
| three documented/focused output-contract tests | yes | each exits 1 with its own marker |
| `verify_direct_closure_release.py` | yes | exit 1, exact marker |
| `test_direct_closure_release_mutations.py` | yes | exit 1, exact marker |
| `verify_package.py` | **no** | actual optimized qualification exits 0 and prints PASS |
| `guarded_run.py` | **no** | no guard; child optimization depends on interpreter/environment |
| `run_all_sources.sh` | **no** | no `__debug__` preflight; invokes two unguarded Python programs |
| `resumable_four_port_driver.py` | **no** | substantive `-O` census and record production both exit 0 |
| `merge_manifests.py` | **no** | no guard; imports driver/atlas |
| `compare_semantic_runs.py` | **no** | no guard (its comparisons themselves are explicit checks) |

The portable README itself calls `run_all_sources.sh` the “lower-level,
unguarded entry point” at line 59, which is inconsistent with the later
universal claim unless “unguarded” is narrowly intended to mean only resource
guarding.

The machine-readable guard matrix is
`independent_checks/computation/entrypoint_optimized/entrypoint_guard_matrix.json`
(SHA-256 `98ca64950a211af8eb743a6c55870b8595e48787e5a1f77ddb1f9687e47e6572`).
All ten tested main/direct entry points rejected with exit status one and the
intended diagnostic.

## Minimal clean reproducer

From the disposable execution project root:

```sh
.venv/bin/python -O -B \
  package/referee/k2p_offline_sweep_portable/verify_package.py \
  --skip-smoke --skip-mutations --skip-prepared-audit
```

Observed: exit `0` after 7.18 s; maximum RSS reported by `/usr/bin/time -l` was
1,502,920,704 bytes.  Standard output (SHA-256
`2e05df25a73f535d10e7c3f2bf72f12db880b73471c524468d9f85afacccbaf0`)
contained:

```text
EXACT_SPARSE_KERNEL_DIFFERENTIAL_PASS
K2P_OFFLINE_SWEEP_PACKAGE_PASS
```

The same command with inherited `PYTHONOPTIMIZE=1` also exited zero and printed
the identical PASS output.  This variant matters because the environment is
inherited by the subprocesses that `verify_package.py` launches.  Plain
command-line `-O` is not propagated by its `sys.executable` child commands,
but the top-level optimized invocation nevertheless falsely claims explicit
rejection.

A direct substantive command also succeeded:

```sh
.venv/bin/python -O -B \
  package/referee/k2p_offline_sweep_portable/resumable_four_port_driver.py \
  --package-root package/referee/k2p_offline_sweep_portable \
  --source-index 0 --start 0 --end 1 --output-root DRIVER_O_OUTPUT
```

Observed: exit `0`; it wrote class 0 with status `separated` and an exact
quadratic certificate.  That pristine certificate was not shown to be wrong;
the point is that load-bearing production executed with its assertions erased.

## Independent semantic mutation

Mutation directory:
`independent_checks/computation/entrypoint_optimized/driver_semantic_mutation/`.
The experiment was run in an APFS-cloned, disposable portable package.  The
large clone was then discarded to return reviewer scratch space; the exact
mutated atlas, mutated input lock, unified diffs, outputs, record, and
independent rechecker remain under `mutation_payload/` and the surrounding
directory.  The mutation makes the quadratic engine return a non-kernel unit
vector and coherently updates the two compiler hashes in its local
`INPUT_LOCK.json`; it never touched the isolated source or any outer lock.

Commands differing only by `-O` were run on source 0, class 0:

- normal mode: exit `1` at the exact target-zero `assert`, no record written;
  stderr SHA-256
  `15e48cf3775283063993dadc9db6848a7231ecfa8500096df63daf880726a6a4`;
- optimized mode: exit `0`, status `separated`, coefficients `[1,0]`, record
  SHA-256
  `ded971c15ce148fc2e4e0d6b259aa9a2fe4fc70cf47e9fd18f1d064d249d251d`.

An independent pullback recomputation
(`false_certificate_recheck.json`, SHA-256
`586d0fcd1ae00121a8051bc94139aa474a05ef38ae835d840709f76239f0ffaa`)
found:

```json
{
  "observed_source_pullback_nonzero": true,
  "observed_source_pullback_term_count": 7,
  "observed_target_pullback_term_count": 5,
  "observed_target_pullback_zero": false
}
```

Thus optimized mode changed a decisive semantic rejection into a false
certificate and successful record production.

## Severity and theorem effect

**Reproducibility-blocking / fail-closed interface defect; not theorem-fatal on
current evidence.**  The documented portable regeneration surface cannot be
said to reject optimized Python, and a latent kernel fault can become a false
classification in that surface.  The official current referee quick/full
harness, direct-closure verifier, and their mutation runners all reject `-O`
before invoking assert-bearing children; the clean sealed certificate was not
falsified.  Therefore this finding does not by itself defeat the mathematical
theorem or the central finite census.

## Smallest adequate remedy and resealing

1. Add the same earliest possible explicit optimized-mode guard to
   `verify_package.py`, `guarded_run.py`, `resumable_four_port_driver.py`,
   `merge_manifests.py`, and `compare_semantic_runs.py`; make
   `run_all_sources.sh` preflight the chosen interpreter and reject when
   `__debug__` is false.
2. Add an outer mutation gate that runs every documented project entry point
   with `-O`, requires exit status one plus a case-specific diagnostic, and
   confirms no record/manifest/PASS report was left behind.  Also test inherited
   `PYTHONOPTIMIZE=1` because the portable qualifier spawns child interpreters.
3. Prefer replacing the atlas’s certificate-semantic `assert` statements with
   explicit `if ...: raise` checks, especially target/source pullback, graph
   validity, physical-domain, and rank-minor checks.  Guards are still required
   for the historical assert-bearing proof scripts.

Changing the portable scripts or atlas requires updating `INPUT_LOCK.json`,
the direct-closure and final release locks, the recursive bundle ledger, any
crosswalk bindings that cite changed hashes, and the distributed ZIP hash.
Because these are recursively sealed runtime files, downstream release and
bundle artifacts require resealing.  TeX/PDF rebuild is needed only if a
printed hash or execution-policy statement changes there; the code-only guard
repair itself does not alter the theorem statement.
