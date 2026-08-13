# Sharp generic-identifiability boundary for level-2 JC networks

**Outcome P is proved and independently verified.**

For binary already-simple standard semi-directed strongly tree-child
level-2 networks, open-JC source-relative full-dimensional regular
containment occurs exactly when the labelled reduced bridge trees agree and
each pair of corresponding blobs is labelled-isomorphic or differs by
ordinary triangle redirection `T`.  There are no proper one-sided generic
containments.  Hence generic JC data identify the standard semi-directed
topology modulo `T`.

Strong tree-childness is sharp: for every `n >= 4`, the frozen weak-class
package supplies a weakly-but-not-strongly tree-child non-`T` pair whose open
JC images have a common full-dimensional regular region of dimension `2n`.

## Main files

- `submission/Strong_Tree_Childness_Sharp_Level2_JC_Boundary.pdf` — final
  manuscript.
- `source/paper/main.tex` — manuscript source.
- `docs/SHARP_BOUNDARY_THEOREM.md` — expanded theorem proof.
- `FINAL_OUTCOME.json` — authoritative machine-readable outcome.
- `THEOREM_CERTIFICATE_CROSSWALK.md` — theorem-to-evidence map.
- `reviews/final_outcome_p_referee_v2/` — terminal independent referee.
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

All three commands above passed in clean detached worktrees at commit
`35291bba72f52ac800e99ea797ddad20d9852a67`, and each worktree remained clean
after replay.  Exact transcripts and timings are in `release/`, with the
machine-readable summary in `release/CLEAN_REPRODUCTION.json`.

The deterministic source-and-certificate archive is intentionally not stored
as an ordinary Git blob because it is 336 MB.  Its tracked checksum and exact
construction command are in `release/`; the archive itself is suitable for a
repository release asset.
