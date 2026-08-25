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
