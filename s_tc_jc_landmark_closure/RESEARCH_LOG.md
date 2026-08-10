# Research log

## 2026-08-09T20:15:00-07:00 — final-closure program opened

- Created a dedicated closure directory and branch from the verified
  weak-class release.
- Froze the sharpness theorem and its two independent verifiers.
- Rejected the withdrawn reciprocal-only bridge chart and every old atlas
  table lacking a primitive decorated graph-to-polynomial binding.
- Locked the only terminal outcomes as a fully certified positive sharp
  boundary or an exact certified `S_TC` counterexample.
- Began parallel work on corrected projective peeling, one-sided cut
  preservation, primitive generator enumeration, decorated-relation
  compilation, and adversarial counterexample search.

## 2026-08-09T20:27:23-07:00 — frozen weak theorem replayed

- Ran `../s_tc_jc_sharp_boundary/reproducibility/verify_release.py` from the
  verified release at parent commit `0c66eefc`.
- The release verifier checked the 288-file manifest, graph/class membership,
  six invariant identities, the exact quadratic interior point, all 256
  Fourier and pattern coordinates, and nonzero rank-eight minors for both
  parameterizations.
- The independent certificate SHA-256 reported by the release is
  `38266537a7966d83bdb94c6fb90fa68f93fbd227b82579f1bf311005925366d7`.
- The verifier entry point has SHA-256
  `90901ab2111c2aecf9eb27989f7136dd44f936cf2e6f9929772a8bba575fbba5`.
- This replay freezes only the theorem in `W_TC \\ S_TC`; it supplies no
  positive-classification input for `S_TC`.

## 2026-08-09T20:32:00-07:00 — independent gates dispatched

- Assigned the bridge/cut theorem to an implementation that may write only
  under `independent/bridge_cut/`.
- Assigned primitive decorated-atlas regeneration to a separate implementation
  that may write only under `independent/decorated_atlas/`.
- Assigned bounded exact counterexample search to a third implementation that
  may write only under `independent/counterexample_search/`.
- The primary implementation will not share graph canonicalization,
  switching, descendant-mask, relation-assignment, or separator-selection code
  with those implementations.
