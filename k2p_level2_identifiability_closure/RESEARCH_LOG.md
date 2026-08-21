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
