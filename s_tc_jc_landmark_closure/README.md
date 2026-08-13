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
