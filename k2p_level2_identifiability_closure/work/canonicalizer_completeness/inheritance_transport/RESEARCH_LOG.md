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
