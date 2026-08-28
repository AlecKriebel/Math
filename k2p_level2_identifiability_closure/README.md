# K2P Level-2 Identifiability Closure

This research folder contains the completed principal-domain classification
for binary standard semi-directed strongly tree-child level-2 phylogenetic
networks under the Kimura two-parameter model.

## Main result

On

```text
D_plus = {(s,g): 0<s<1, 0<g<1, g>2s-1},
```

a regular full-dimensional directed containment germ exists exactly when the
two labelled networks agree modulo independent ordinary-triangle
redirections. Thus no proper one-sided containment occurs; the structural
triangle class is generically identifiable and exactly reconstructible away
from a proper algebraic exceptional set. The classification restricts to the
strict continuous-time cone `0<s<1, s^2<g<1`. A separate construction shows
that strong tree-childness is sharp by producing a full-dimensional `4n-3`
ambiguity in the weak class.

The frozen theorem release is rooted at
`work/final_theorem_release/RELEASE_LOCK.json`, whose SHA-256 is

```text
0963636c3d4026a74ef926a0dc122c81a08b211b4d151ecc955c790e16cc5a9a
```

The theorem is deliberately limited to the principal positive component; no
mixed-sign extension is claimed.

## Submission package

`proof_compression_submission/` contains the adversarially reviewed article,
reader supplement, theorem-to-artifact crosswalk, and one bounded
proof-compression pass. The compression verdict is `PC-PARTIAL`: completion
arithmetic, polynomial catalogues, and arbitrary-word reconstruction now have
compact mathematical formulations, while exact direction-sensitive rank,
restoration, and probe ledgers remain load-bearing. The finite theorem and
classification universe are unchanged; the outer qualification lock has been
resealed to bind the repaired verifier-facing mutation evidence.

The final neutral-referee package is
`proof_compression_submission/output/K2P_Principal_D_Plus_Referee_Package_20260828.zip`;
its adjacent `.sha256` file is the archive authority.

## Layout

- `archives/original/`: downloaded checkpoint archives, unchanged.
- `package/original/`: extracted original checkpoints, unchanged.
- `package/referee/k2p_offline_sweep_portable/`: portable direct-sweep release.
- `work/final_theorem_release/`: promotion-grade unified release and lock.
- `work/`: graph-derived proofs, independent replays, and adversarial audits.
- `proof_compression_submission/`: article, supplement, compressed finite
  theorem, reproducibility crosswalk, and final PDFs.
- `RESEARCH_LOG.md`: project chronology.

## Reproduction

Create the pinned environment described in
`work/final_theorem_release/requirements.txt`, then run from this project root:

```bash
.venv/bin/python -B work/final_theorem_release/build_release_lock.py \
  --check --require-ready
.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py \
  --quick
.venv/bin/python -B proof_compression_submission/verify_compressed_release.py \
  --check
.venv/bin/python -B proof_compression_submission/verify_old_new_equivalence.py \
  --check
.venv/bin/python -B proof_compression_submission/run_compression_mutations.py \
  --check
```

See `STATUS.md` for the exact final qualification state and the external
publication actions deliberately left to the author.
