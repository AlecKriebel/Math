# Research log

## 2026-08-24 — inheritance and restriction transport closure

- Inspected the frozen exact-transport, parent-restriction, restoration, and
  probe ledgers.  Confirmed that their graph maps are exact but that their
  schemas do not explicitly bind ordered reticulation parents or inheritance
  complementation.
- Independently reconstructed every probe transport occurrence.  The graph
  maps induce many genuine parent-order reversals, so the missing field is not
  vacuous.  No missing parent map, bad permutation, or counterexample was
  found.
- Implemented a separate derived certificate rather than modifying frozen
  evidence.  Root-suppressed incidences are lifted through the suppressed
  physical edge; restriction products are derived by contraction provenance;
  ordinary-triangle parameters are delegated only to the certified local
  section.
- Added deterministic gzip ledgers, a complete regeneration verifier, and ten
  targeted mutations.  Best estimate: 100% complete for the parameter-
  transport evidence gap assigned to this workstream; integration into the
  encompassing release remains the parent workstream's responsibility.

## 2026-08-25 — disposable mutation output and provenance reseal

- Required the mutation producer to write only to a caller-owned external
  path, except for an explicit exact canonical reseal.  Publication now uses
  an fsynced atomic replacement and rejects source-tree collisions, canonical
  symlinks, hardlink collisions, and optimized Python.
- Regenerated the graph-derived certificate in scratch after the producer and
  mutation-runner bytes changed.  All three transport ledgers were
  byte-identical to the frozen ledgers; only the two changed source bindings,
  the printed mutation command, and the dependent certificate seal changed.
- The rebound certificate has payload
  `984c987931ebbab36c9db38e83c63c5bb12afa015ff1d2236ebab0b67a0f0450`.
  The 10/10 mutation cases remain unchanged and rejected; the rebound report
  has payload
  `4640b0015ec251e98cf392377025956def5bd828d41fb5c8412d937921d40722`.
- The independent nested-output regression passes hardlink, late-symlink,
  canonical-symlink, collision, required-output, and source-immutability
  attacks for both this producer and the canonicalizer mutation producer.
- Completion estimate: **100% for the transport evidence repair**; global
  release qualification remains pending the ordered outer reseal.

## 2026-08-26 — production-verifier mutation qualification

- Reproduced the referee's concern: four of ten stored cases had no semantic
  diagnostic and were qualified only by inequality of clean and mutated row
  hashes.  This was an evidence defect, not a surviving transport mutation.
- Replaced those four cases by complete deterministic-ledger attacks.  Each
  attack rewrites exactly one graph-derived occurrence, recomputes every row
  hash, ordered root, action census, compressed-file binding, input binding,
  and certificate payload, passes the structural directory validator, and is
  then rejected by independent primitive regeneration in the untouched full
  verifier at one exact diagnostic.
- The other six cases now require exact local semantic diagnostics.  Wrong
  diagnostics, unrelated tracebacks, signal and positive non-one exits,
  timeouts, embedded PASS tokens, stale outputs, and optimized-mode reruns are
  explicit negative controls and cannot qualify a rejection.
- The full baseline now replays the stored authoritative certificate in place
  before any disposable copy or reseal is permitted.  Routine outputs are
  caller-owned, atomic, path-independent, and unable to leave stale PASS
  evidence after failure.
- No theorem statement, graph census, ledger row count, or transport closure
  changed.  Completion estimate: **100% for the repaired transport mutation
  evidence**, pending only final release-wide resealing and replay.

## 2026-08-26 — final frozen-input qualification

- Regenerated the authoritative certificate after all sixteen bound inputs
  were frozen.  The three generated ledgers remained byte-identical to the
  prior qualified ledgers: 67,741 relation rows, 71,022 probe-restriction
  rows, and 5,540 restoration-restriction rows, with identical ordered roots,
  action censuses, and zero unresolved transports.  Only input provenance and
  derived certificate/report seals changed.
- The producer completed in 232.73 seconds with 2,552,758,272-byte maximum
  RSS.  The final full mutation suite completed in 1,593.15 seconds with
  2,592,063,488-byte maximum RSS.  All four complete coherently resealed
  production-verifier attacks and all six exact local semantic attacks were
  rejected; zero cases survived.
- The final certificate payload is
  `a52f9c2ac63f650c7aee1e32790090dc40903a1c562e208a9c4c87d4b0d58a0a`;
  the final mutation-report payload is
  `93741cbeb50b2e2fde5d2c144de5d9943d1879fb61faf64115cf44ec5608b044`.
  The strict release binder independently accepted the complete v2 contract.
