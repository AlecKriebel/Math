# Static invocation and import graph

Date: 2026-08-22 (America/Los_Angeles)

Status: **complete by static inspection**. No delivered Python program or shell
entry point was executed, and no delivered module was imported while preparing
this graph.

Paths below are relative to
`source_and_certificates/universal_simultaneous_amplification/` unless prefixed
by `package/`. Line numbers refer to the frozen extracted copy.

## Mandatory package-level path

```text
package/run_all_referee_checks.sh
  9  -> BOOTSTRAP_PYTHON package/verify_referee_package.py
          176-184 -> verify_package_manifest
                       50-72: exact package file set + SHA-256 values
                    -> verify_source_archive
                       75-155: archive sidecar, member safety/order, internal
                               manifest, extracted-tree byte identity, PDF copy,
                               README/VERSION digest and count consistency
                    -> verify_neutral_prompt
                       158-173: required verdict strings and neutrality string
  11-32 -> locate make/tectonic/pdfinfo/pdftoppm and require exact document-tool
           versions for Tectonic and Poppler
  34-43 -> create a disposable directory and copy source_and_certificates
  46-47 -> paper_db_extremality/submission/bootstrap_replay.sh
  49    -> paper_db_extremality/build.sh
  50-52 -> cmp delivered PDF against rebuilt PDF
  54-61 -> inline standard-library Python computes rebuilt PDF SHA-256
```

`run_all_referee_checks.sh` has `set -eu` at line 2 and a guarded cleanup trap
at lines 35-41. A nonzero status from a child normally propagates.

## Bootstrap and replay chain

```text
paper_db_extremality/submission/bootstrap_replay.sh
  10-13 -> inline Python: assert Python == 3.14.6
  15-17 -> create project-local .venv-paper1 if absent
  19-21 -> pip install paper_db_extremality/requirements.txt
             sympy==1.14.0
             python-flint==0.9.0
             mpmath==1.3.0
  23-34 -> inline Python: assert interpreter and installed distribution versions
  36    -> PYTHON=.venv-paper1/bin/python paper_db_extremality/replay.sh

paper_db_extremality/replay.sh
  17-21 -> import-probe sympy and flint; explicit exit 2 on failure
  25-29 -> project Makefile goals: test verify directed triangle n4 phase3-check
  31-37 -> five r2_determinant programs
  39-40 -> physical-standard program
  42-44 -> marked-lift program
  46-48 -> regular-sector program
  50-52 -> paper-level integration program
```

Both scripts have `set -eu` (`bootstrap_replay.sh:2`, `replay.sh:2`). The
replay chooses `.venv-paper1/bin/python`, then `.venv/bin/python`, then
`python3` (`replay.sh:6-15`), but bootstrap explicitly sets `PYTHON` to the
fresh pinned environment (`bootstrap_replay.sh:36`).

## Makefile expansion

The call at `replay.sh:29` expands as follows (`Makefile:8-29`):

```text
make test
  -> python -m unittest discover -s tests -v
       -> tests/test_exact_markov.py
            -> imports src/exact_markov.py

make verify
  -> verification/verify_obstruction.py

make directed
  -> phase1_directed/verify_directed_db_strong.py

make triangle
  -> phase2_triangle/derive_certificate.py
  -> phase2_triangle/crosscheck_exact_solver.py
       -> imports phase2_triangle/derive_certificate.py
       -> imports src/exact_markov.py
  -> phase2_triangle/audit/independent_triangle_audit.py

make n4
  -> phase2_n4/derive_lumped_certificates.py
  -> phase2_n4/crosscheck_full_chain.py
       -> imports phase2_n4/derive_lumped_certificates.py
       -> imports src/exact_markov.py

make phase3-check
  -> phase3_asymptotic/verify_lumping.py
```

The Makefile sets `PYTHONDONTWRITEBYTECODE=1` (`Makefile:4`). The recipes set
`PYTHONPATH=.` for all goals except `phase3-check` (`Makefile:8-27`). The
archive's `paper1` target (`Makefile:29-31`) is not called by the replay; it
points to the omitted legacy `paper/` tree and is not a usable entry point in
this standalone archive.

## Direct replay programs

After Make returns, `replay.sh` invokes these programs in this exact order:

1. `phase5_exact_threshold/r2_determinant/verify_r2_determinant.py`
   (`replay.sh:31-33`).
2. `phase5_exact_threshold/r2_determinant/verify_complete_refresh_forest.py`
   (`replay.sh:34`).
3. `phase5_exact_threshold/r2_determinant/verify_antisymmetric_hessian.py`
   (`replay.sh:35`).
4. `phase5_exact_threshold/r2_determinant/verify_true_inverse_rank_symmetric_phase.py`
   (`replay.sh:36`).
5. `phase5_exact_threshold/r2_determinant/verify_hessian_sectors.py`
   (`replay.sh:37`).
6. `phase5_exact_threshold/r2_standard_physical_phase/verify_physical_standard_phase.py`
   (`replay.sh:39-40`).
7. `phase4_landmark_closure/obstruction/r2_marked_lift_v2/verify_marked_lift.py`
   (`replay.sh:42-44`).
8. `phase5_exact_threshold/r2_regular_sector/verify_local_complete_hessian.py`
   (`replay.sh:46-48`).
9. `phase5_exact_threshold/paper_db_extremality/verify_paper_claims.py`
   (`replay.sh:50-52`).

Together with the eight Makefile verifier/cross-check programs, this is the
seventeen-program set described at `package/CLAIM_CODE_MAP.md:20-23`; the unit
test suite is additional.

## Transitive project imports

Only the following delivered-module imports occur on the mandatory replay
path; all other imports are Python standard library, SymPy, or python-flint.

```text
tests/test_exact_markov.py:7-15
  -> src/exact_markov.py

phase2_triangle/crosscheck_exact_solver.py:17-33
  -> phase2_triangle/derive_certificate.py
  -> src/exact_markov.py

phase2_n4/crosscheck_full_chain.py:12-27
  -> phase2_n4/derive_lumped_certificates.py
  -> src/exact_markov.py

phase4.../r2_marked_lift_v2/verify_marked_lift.py:17-25
  -> phase4.../chi_square_channel/verify_resolvent_identities.py
       substantively uses solve() at verify_marked_lift.py:28-29
  -> phase4.../r2_collision_closure/verify_direct_flow_screen.py
       substantively uses only matrix_from_edges() at
       verify_marked_lift.py:491-495, 520-524, and 551-555
       -> imports green_data, proper_generator, stationary, transition from
          phase4.../r2_collision_closure/verify_fisher_route.py
```

The last edge is import reachability only. `verify_marked_lift.py` never calls
the four names imported by `verify_direct_flow_screen.py`, and Python's
`if __name__ == "__main__"` guards prevent either helper's `main()` from
running (`verify_direct_flow_screen.py:117-118`,
`verify_fisher_route.py:807-808`). Consequently:

- the exhaustive/sampled direct-flow screen at
  `verify_direct_flow_screen.py:99-114` is **not executed** by replay;
- the likelihood/Fisher witness suite at `verify_fisher_route.py:773-804` is
  **not executed** by replay;
- the resolvent helper's standalone examples at
  `verify_resolvent_identities.py:151-170` are **not executed**, although its
  `solve()` implementation is exercised repeatedly by the marked-lift audit.

This is narrower than a casual reading of `package/CLAIM_CODE_MAP.md:23-31`
might suggest. The map says the modules are reached as imported helpers, which
is literally true, but reachability does not run their guarded audits.

## Build path

`paper_db_extremality/build.sh:9-22` creates output directories, fixes the
document epoch/time zone, calls Tectonic, installs the resulting PDF, calls
`pdfinfo`, removes old page PNGs, and renders all pages with `pdftoppm`. The
outer script then performs byte-for-byte `cmp` against the supplied PDF
(`run_all_referee_checks.sh:49-52`). The `pdftoppm` diagnostic stream is
redirected at `build.sh:20-22`, but its nonzero status is not suppressed because
the script has `set -e`.

`all.sh:4-6` is merely `replay.sh` followed by `build.sh`; it is not used by
the package-level command. `release_bundle.sh` and `bundle_manifest.py` are
release-production tools, not part of the mandatory replay. The conditional
submission verifier in `release_bundle.sh:17-19` is absent by design and is
therefore skipped only on that nonmandatory path.

## Failure and environment notes

- Shell failures normally propagate through `set -e`, Make normally stops on
  a failed recipe, Python exceptions are not caught, and the outer PDF `cmp`
  is decisive. No Python exception-suppression construct was found on the
  mandatory path.
- Almost all scientific checks are bare Python `assert` statements. The
  bootstrap's interpreter/package checks are also asserts
  (`bootstrap_replay.sh:10-13,23-34`). `PYTHONOPTIMIZE` is not cleared and no
  program checks `sys.flags.optimize`. Running with optimization would remove
  the certification assertions while leaving PASS prints reachable.
- `MAKEFLAGS` is inherited; an external ignore-errors flag can weaken Make's
  normal failure behavior. `PYTHONPATH` is also inherited by direct replay
  calls. A clean execution should unset `PYTHONOPTIMIZE`, `PYTHONPATH`, and
  `MAKEFLAGS` (and should confirm `sys.flags.optimize == 0`).

