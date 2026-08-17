# Sharp generic-identifiability boundary for level-2 JC networks

**Final Outcome A is proved and checked by exact primary and separately
implemented replay certificates.**

For binary already-simple standard semi-directed strongly tree-child
level-2 networks, open-JC source-relative full-dimensional regular
containment occurs exactly when the labelled reduced bridge trees agree and
each pair of corresponding blobs is labelled-isomorphic or differs by
ordinary triangle redirection `T`.  There are no proper one-sided generic
containments.  Hence generic JC data identify the standard semi-directed
topology modulo `T`.

Strong tree-childness is sharp even without triangles: for every `n >= 4`,
the bounded Omega audit supplies a triangle-free weakly-but-not-strongly
tree-child non-`T` pair whose open JC images have a common full-dimensional
regular region of dimension `2n+1`. The frozen Theta package supplies a
second triangle-containing family of dimension `2n`.

## Main files

- `biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC.pdf` — final
  manuscript.
- `biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf`
  — reader-oriented supplement.
- `source/paper/main.tex` — manuscript source.
- `docs/SHARP_BOUNDARY_THEOREM.md` — expanded theorem proof.
- `FINAL_OUTCOME.json` — authoritative machine-readable outcome.
- `THEOREM_CERTIFICATE_CROSSWALK.md` — theorem-to-evidence map.
- `reviews/v1_1_proof_hardening/` — terminal bounded independent
  mathematical review, repair response, and proof-hardening regressions.
- `REFEREE_GUIDE.md` — suggested specialist audit path.

## Exact reproduction

From the repository root:

```bash
bash s_tc_jc_landmark_closure/reproducibility/verify_quick.sh
bash s_tc_jc_landmark_closure/reproducibility/verify_full.sh
bash s_tc_jc_landmark_closure/reproducibility/verify_regenerate_all.sh
```

The bootstrap creates a pinned local environment.  Regeneration is confined
to the structurally proved finite support universe; it does not initiate an
open-ended topology search.

Historical failed releases and withdrawn claims are retained only as
fail-closed audit history and are not consumed by the active verifiers.

`docs/GLOBAL_THEOREM_DRAFT.md` is a frozen pre-promotion proof ledger retained
because several historical independent reviews hash it.  The active theorem
is `docs/SHARP_BOUNDARY_THEOREM.md`; the authoritative outcome is
`FINAL_OUTCOME.json`.

## Sealed release evidence

The exact source commit, clean-clone transcripts, environment versions,
output hashes, and deterministic archive checksum are bound by the two-layer
seal described in `RELEASE_METADATA.json`. The GitHub Release identified in
`release/PUBLIC_RELEASE_ASSETS.md` becomes authoritative only after
`verify_public_release.py` downloads and verifies its exact eight-asset set.
No persistent DOI is claimed before issuance. Historical 18-page replay
records are isolated under
`history/superseded_release_evidence/` and are not active evidence.

Format-specific upload bundles for bioRxiv, Systematic Biology, and the
Journal of Mathematical Biology are in `biorxiv_submission/` and
`journal_submission/`.  Their upload maps identify every remaining human
portal action; no script submits or communicates externally.
