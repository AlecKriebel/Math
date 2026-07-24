# Factor/slack active-deflation construction round

Status: **NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE.**

No candidate reached maximum inner product \(1/2\), and no candidate improved
the input records by the declared \(10^{-13}\) significance margin.

## Mechanism

This search keeps an explicit factor \(X\in\mathbb R^{N\times5}\), so every
Gram matrix has rank at most five without spectral projection.  Its rows are
renormalized after every tangent-space step.

For each unordered edge \(ij\) and current homotopy target \(c\), the iteration
updates

\[
s_{ij}=\max(c-\langle x_i,x_j\rangle,0),\qquad
r_{ij}=\langle x_i,x_j\rangle-c+s_{ij}.
\]

It evolves a separate dual penalty and IRLS weight for every edge, combines
the weighted residual gradient with a log-sum-exp guard, and updates \(X\)
in its row-sphere tangent space.  Every run has three active-set deflation
windows.  Each deletes a seeded block of dominant constraints, applies a
small asymmetric tangent kick, and then reintroduces the deleted edges with a
tenfold penalty boost that decays to one.  Two escaped factors per run are
finally polished by an all-edge epigraph SLSQP solve.

This differs from the earlier Gram projection search: there is no \(N\times N\)
PSD/rank projection.  All state evolution occurs in the five-column factor
and the explicit edge slack/penalty arrays.

## Portfolio

The production command was:

```text
./.venv/bin/python \
  experiments/four_point_depth_projection/construction_homotopy_deflation/deflate_search.py \
  --n 41 42 43 44 \
  --restarts 10 \
  --warm-restarts 5 \
  --epochs 10000 \
  --checkpoint-period 1000 \
  --polish-iterations 1500 \
  --seed-base 2026072700 \
  --output experiments/four_point_depth_projection/construction_homotopy_deflation/deflate_results.json
```

There were 40 runs: 20 current-record/perturbed starts and 20 fresh
asymmetric Gaussian starts.  The exact seed ranges were:

- N=41: 2026072700–2026072709;
- N=42: 2026072800–2026072809;
- N=43: 2026072900–2026072909;
- N=44: 2026073000–2026073009.

The run performed 400,000 factor/slack epochs, 120 deflation/re-entry events,
and 80 all-edge polish solves.  Every polish solver reported success.
Recorded elapsed time was 667.83 seconds.

## Results

The retained records are unchanged:

| N | retained maximum | best fresh-start maximum | best fresh seed |
|---:|---:|---:|---:|
| 41 | 0.5149946525121660 | 0.5198598268736591 | 2026072708 |
| 42 | 0.5182411558622624 | 0.5259930035292503 | 2026072805 |
| 43 | 0.5247096018290193 | 0.5300476975776088 | 2026072906 |
| 44 | 0.5274577123235322 | 0.5374852549898422 | 2026073005 |

Warm-start polish values differing from an input by less than
\(4\times10^{-15}\) were treated as binary64 normalization noise, not record
improvements.

Every run in `deflate_results.json` contains:

- its full best coordinates and independently recomputable diagnostics;
- all checkpointed slack, residual, dual, and effective-weight summaries;
- the exact three deleted-edge manifests and re-entry epochs;
- complete terminal per-edge slack, residual, dual, and weight arrays; and
- both polish outcomes.

Failure of this finite heuristic portfolio is not evidence for an upper
bound.

## Verification

Run:

```text
/usr/bin/python3 \
  experiments/four_point_depth_projection/construction_homotopy_deflation/deflate_verify.py

./.venv/bin/python \
  experiments/four_point_depth_projection/construction_homotopy_deflation/deflate_tests.py -v
```

The independent checker uses only the Python standard library.  It does not
import the search program, NumPy, SciPy, or a solver.  It reconstructs all
stored best inner products, hashes, norm errors, violation counts, seed
formulas, source hashes, threshold/record flags, edge-state dimensions and
nonnegativity, slack/residual complementarity, and all deflation manifests.

All seven regression and tamper tests pass.  They independently verify that
every stored factor has unit rows and a PSD Gram matrix of numerical rank at
most five, and that the checker rejects corrupted coordinates, hashes,
maxima, flags, seeds, source hashes, slacks, and deleted-edge manifests.

Artifact hashes:

- `deflate_results.json`:
  `6a08f95d643a1b157b37ecd5e5a91d19a1d2561b515a5a4121590de9c08b6579`;
- `deflate_verification.json`:
  `6ef5e50bb0a83b7e42b4030c2c53bf4c4d20630e24d507daf74914f3f24408f5`.

## Safe staging scope

Only these six files belong to this mechanism and are safe to stage together:

1. `deflate_search.py`
2. `deflate_results.json`
3. `deflate_verify.py`
4. `deflate_verification.json`
5. `deflate_tests.py`
6. `deflate_report.md`

No `split_*`, `thermal_*`, shared, or central file was edited.
