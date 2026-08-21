# Research Log

## 2026-08-20 18:41 PDT — Program relocation and optimization start

- Established this dedicated top-level research folder on the repository's
  `main` publication line without disturbing unrelated active worktrees.
- Recovered the prior conversation's theorem status: all global proof layers
  are closed conditional on the finite assertion `FA+`; the remaining gate is
  the exhaustive four-port dummy-role/restoration relation sweep with bound
  five-port children.
- Began recovery of the exact conversation attachments.  The referenced
  projectless workspace was empty and the available in-app browser session was
  not authenticated, so the originating conversation was asked to re-surface
  its retained byte-identical archive and SHA-256 inventory.
- Fixed a 60-minute optimization budget beginning when the package is locally
  available.  The optimization may stop earlier once the safe worker count and
  dominant hot path are addressed and equivalence tests pass.
- Hardware constraint: Apple M1 Pro, 10 CPU cores, 16 GB RAM.  The full run
  must leave headroom for concurrent research workloads and must never trade
  exactness or resumability for speed.

## 2026-08-20 18:45 PDT — Resource and provenance audit

- The retained portable package contains 13 files.  Its two K2P-specific exact
  caches are `atlas/descriptors_4.pkl` (80,293,252 bytes) and
  `atlas/rank_certs_4.pkl` (29,859,039 bytes); they do not coincide with any
  local JC cache or Git object.
- The topology provenance is the JC closure grammar on `origin/main`:
  `core_universe.py`, `graph_model.py`, `support_universe.py`, and
  `completion_universe.py`, with the optimized relation architecture in
  `atlas_compiler.py`.  The package counts agree with 831 selected completions
  plus 1,983 marginalized-incoming completions, giving 67,536 raw
  target/port presentations per source.
- Current machine state is not safe for an unguarded production launch: about
  3.1 GiB disk is free, 6.57/7.68 GiB swap is occupied, and a separate exact
  computation has held one CPU core for several days.  That process is not to
  be disturbed.
- Production policy: require at least 20 GiB free before a fresh launch and
  pause safely below 10 GiB; default to two single-threaded long-lived lanes;
  use bounded queues and atomic streamed records; cap aggregate sweep memory
  near 5 GiB.  Four workers are admissible only if a representative pilot
  proves less than roughly 1 GiB peak RSS per worker.
- Planned source balance for two lanes is 1,023 classes versus 908 classes:
  lane A `theta0(1) + theta1(0)` and lane B
  `theta0(0) + theta1(1) + theta3(0) + theta3(1)`.
- Referee determinism requirements include fixed hash seed, single-threaded
  numerical libraries, sorted semantic JSON, timing/RSS excluded from record
  hashes, validated pickle hashes before unpickling, and serial-versus-parallel
  normalized record equivalence.

## 2026-08-20 19:07 PDT — Exact artifacts imported

- The user downloaded the retained chat archives into `~/Downloads`, removing
  the cross-conversation attachment transport blocker.
- Moved five K2P archives into `archives/original/`, including both names of
  the byte-identical first checkpoint archive, the second continuation, the
  non-pickle transport subset, and the complete four-port package.
- Extracted the two checkpoints and complete four-port package under
  `package/original/`.  The original files remain untouched; optimization will
  occur only in a separate `package/referee/` copy.
- The complete four-port ZIP matches the preserved archive SHA-256
  `53d8f6771589197b16690ff0fb790cc2aa845fa91e86424e589476ffe352c875`.
- The 60-minute optimization clock starts after the artifact-import commit is
  published to `main`.

## 2026-08-20 19:48 PDT — Bounded optimization and qualification complete

- Stopped optimization inside the fixed 60-minute budget.  All changes are in
  `package/referee/k2p_offline_sweep_portable`; the original package remains
  byte-for-byte preserved.
- Measured pickle/compiler startup at about 4 seconds and 1.39–1.50 GB peak
  RSS per independent process.  Six workers are unsafe on this 16 GB machine.
  The referee runner supports one worker by default and at most two staggered,
  balanced long-lived lanes.  Current local launch policy is one worker.
- Reused validated pickle hashes rather than rereading 110 MB, compacted the
  separately unpickled rank-descriptor graph, retained fixed-source quadratic
  products lazily across classes, discarded target-local products, prepared
  fixed-source exact mixed graphs, and cleared source caches between sources.
- Replaced six sequential universe loads with one multi-source load per lane.
  Changed growing-manifest checkpoints from every class to every 25 classes;
  the estimated logical manifest writes fall from about 2.20 GB to 95 MB.
- Repaired two frozen-package fail-closed defects found during qualification:
  resume previously accepted a removed hard certificate after a recomputed
  outer checksum, and the merge previously returned success for fabricated
  incomplete manifests.  Record semantics, class/source identities, current
  package bindings, exact ID coverage, and merge completion are now checked.
- Added deterministic semantic record, source-manifest, and complete-sweep
  hashes that exclude only operational timing/platform diagnostics.
- Found and repaired an exact-kernel zero-column defect that could miss a
  separator, plus a rational-coefficient conversion defect in the SymPy
  differential oracle.  The seeded width-1-through-16 differential suite now
  passes.
- Narrowed graph-conversion error handling so unexpected implementation or
  dependency faults abort instead of becoming mathematical nonrelations.
- The prepared exact graph path matched the frozen path on all 4,012 eligible
  presentations.  Frozen-versus-optimized output matched on eight declared
  benchmark records (four direct hard cases and four ordinary source-5
  classes), semantic aggregate SHA-256
  `74663db39da3e87bd3042ed16e1da7bf1cc72adcd5cc5414fb09ef3cf3913d59`.
- Full hash, dependency, census, rank, hard-binding, graph-path, resume, exact
  kernel, and adversarial mutation qualification passed in 45.61 seconds at
  1,507,999,744 bytes maximum RSS.
- Built and integrity-tested the 5,397,019-byte referee archive
  `archives/k2p_four_port_referee_optimized_20260820.zip`, SHA-256
  `dcdfe50f36d231a2940a53f2ec196dba52c5850078f2e92ee24ec3ca2747dc82`.

## 2026-08-20 19:49 PDT — Production launch safely gated

- The guarded full-run invocation was issued with one low-priority worker.
  Preflight correctly refused to start: 2.61 GiB disk was free versus the
  20.00 GiB safety requirement.  No production relation process was launched.
- The guard will stop below 10 GiB free disk or above 3.5 GiB aggregate sweep
  RSS, propagates termination/hangup to the detached process group, forces all
  numerical-library thread counts to one, and preserves every atomic class for
  resume.
- Independent audit identified theorem-level gates not solved by runner
  optimization: an explicit topology/rank exclusion ledger and dimension
  upper-bound certification, bound five-port restoration children, explicit
  graph witnesses/exact certificate replay in the released package, and a
  careful restriction of the hard-case conclusion to its proven `D_plus`
  domain.  These are recorded as closure requirements; the optimized sweep
  must not itself be described as a completed final theorem.
