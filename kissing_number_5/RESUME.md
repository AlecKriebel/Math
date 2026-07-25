# Resume guide

This is the operational handoff for the paused five-dimensional
kissing-number program.

> **Stop state:** \(40\le\tau(5)\le44\).  No exact value was established, no
> 41-point construction was found, and no universal 41-point exclusion was
> proved.

Read [`STATUS.md`](STATUS.md), then [`CLAIMS_LEDGER.md`](CLAIMS_LEDGER.md),
before restarting any lane.  The status file is the concise checkpoint; the
ledger is the authoritative scope record.

## Clean setup

The exact smoke tests use Python's standard library only.  From a clean clone:

```sh
git clone https://github.com/AlecKriebel/Math.git
cd Math/kissing_number_5
python3 --version
```

Python 3.14.6 was used for the final pause audit.  Discovery-only numerical
experiments use the pinned packages in `requirements-discovery.txt`:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-discovery.txt
```

No theorem should depend on that floating-point stack without a separate exact
or directed-interval certificate.

## Five-minute exact smoke test

Run from `kissing_number_5/`:

```sh
python3 verifiers/verify_d5.py certificates/d5_roots.json
python3 verifiers/verify_antipodal_deep_graph_branches.py
python3 verifiers/verify_quarter_grid_antipodal_pair_moment_obstruction.py
python3 verifiers/verify_local_positive_height_ladder.py
python3 verifiers/verify_r18_residual_q_energy.py
```

Then run the packages created immediately before the pause:

```sh
ADE=experiments/centered_quarter_k4_flag_psd/audit/k5_centering_products/rank5_strengthening
python3 "$ADE/verify_ade_core_shells.py"
python3 "$ADE/verify_general_quarter_grid_moments.py"
python3 "$ADE/verify_r11_profile_ade_bounds.py"

(cd experiments/r18_c5_h_energy && \
  python3 verify_manifest.py && \
  python3 test_verify_lambda_max_c5_cell.py && \
  python3 test_verify_adjacent_merge.py)

(cd experiments/weighted_common_source_attack/realized_d5_extension && \
  python3 test_verify_small_union_hall.py && \
  python3 test_verify_hall_counterexample.py && \
  python3 test_verify_uniform_conflict_charge_counterexample.py && \
  python3 test_verify_known_28.py)
```

These commands all passed on 24 July 2026.  The ADE and five-cycle verifiers
also passed in optimized mode (`python3 -O`) and their tests include tamper
cases.  Elsewhere in the historical tree, some older scripts deliberately use
`assert`; run those with ordinary Python unless their own README explicitly
says that optimized mode is audited.

For a broader run:

```sh
python3 -m unittest discover -s tests -v
```

At the pause checkpoint this completed with **155 tests passing** in
1,575.892 seconds when run from the `kissing_number_5/` directory.  Running
the discovery from the repository root without setting `PYTHONPATH` causes
import errors and is not the documented invocation.

The checksum manifest is verified from the repository root:

```sh
shasum -a 256 -c kissing_number_5/PAUSE_MANIFEST.sha256
```

## Exact scope map

| Package | What it proves | What it does not prove |
|---|---|---|
| `proofs/lower_bound_d5.md` | Exact 40-point code | Optimality |
| `proofs/antipodal_deep_graph_coupling.md` | Universal antipodal/deep-graph coupling | Exclusion of the \(r=18\) branch |
| `proofs/local_positive_height_ladder.md` | Universal local occupancy bounds | Global \(N\le40\) |
| `proofs/quarter_grid_antipodal_pair_moment_obstruction.md` | Quarter-grid \(r=14,15,16\) exclusion | Any off-grid code |
| ADE package above | One \(r=12\) endpoint and 38 stored \(r=11\) profiles | Exhaustiveness of the \(r=11/r=12\) branches |
| `experiments/r18_c5_h_energy/` | \(\lambda_{\max}\le3\) on the closed sign cell; quartic bound on \(\sum A_i=3\) | Off-face quartic bound or branch elimination |
| `experiments/root_triangle_k7_overlap/` | Exact dual on one finite catalog; exact counteratom outside it | A universal rooted-triangle inequality |
| `realized_d5_extension/` | Small-union Hall lemma and exact counterexamples on one fixed support | Arbitrary 41-code classification |

The missing upstream enumeration generators are not a cosmetic issue.  Do not
promote a stored finite list to a complete branch theorem until a fresh,
independently checked generator proves coverage.

## Numerical restart table

The best repeatedly reproduced maxima at pause were:

| \(N\) | Maximum inner product |
|---:|---:|
| 41 | 0.5149946525 |
| 42 | 0.51824116 |
| 43 | 0.52470960 |
| 44 | 0.52745771 |

The target is at most \(0.5\).  These values are warm starts and diagnostics,
not certified lower bounds on the optimum.  The \(r=18\) five-cycle branch
portfolio reached a best common load near \(0.54248\).

## Recommended restart order

1. **Seek a common-source inequality.**  The central gap is not another
   pair/triple moment or local rank-five mixture; it is compatibility of many
   local views with one global five-dimensional column space.
2. **Use rooted triangles or four-cycles only with a complete continuous
   mechanism.**  The finite \(K_7\) catalog dual has an exact counteratom.
3. **If returning to the quarter grid, first rebuild coverage.**  Recreate and
   independently verify the generators for the \(r=11\) profiles and \(r=12\)
   endpoints before extending to \(r=10\).  No theorem-strength \(r=10\),
   \(r=13\), \(r=17\), or \(r=18\) package survived.
4. **For the \(r=18\) branch, attack the off-face five-cycle region.**  The
   minimal metric face is already certified; the rest of the metric polytope
   is the precise gap.
5. **Keep construction search independent.**  A valid 41-point exact
   construction would overturn the favored obstruction narrative.  Preserve
   asymmetric starts and require exact coordinates or isolating intervals
   before treating a candidate as real.

Do not restart by simply increasing the resolution of the existing grids or
the number of random optimizer seeds.  The final rounds showed sharply
diminishing returns from those changes.

## Interrupted and missing artifacts

- The temporary `quarter_grid_r11`, `quarter_grid_r12_ade`, and standalone
  \(r=13\) packages were cleaned from `/tmp`.  Their surviving mathematical
  cores are in the ADE directory, but their completeness generators are not.
- Claimed \(r=17/r=18\) quarter-grid eliminations and the interrupted \(r=10\)
  enumeration have no surviving exact certificate.
- The root-triangle centered degree-three radical was only partly reduced.
- The full five-cycle energy lemma remains open away from \(\sum A_i=3\).

The claims ledger intentionally marks these gaps instead of reconstructing
them from memory.

## Git and local preservation

The previously unpublished omnibus state was preserved before its history was
split:

- original commit: `3c01488e26ac74598cf654ef14110de7d39215af`;
- original tree: `c927550da5cffd151997fce187a3d79b3d70cce2`;
- local safety tag: `kissing5-pre-split-2026-07-24`;
- the byte-identical split checkpoint is published as commit `ad5bfa02`.

Local recovery files are under
`/Users/alec/Documents/Math-kissing5-snapshots/2026-07-24-pre-split/`:

| File | SHA-256 |
|---|---|
| `unpublished-history.bundle` | `1577a83ae425bbfa4654e22c26e95775d85ff76d6d873953a19b35ba94dcb5ee` |
| `unpublished-history.patch` | `d60044f50bf71234c5e24b60c9d2d599c569c4b843fcc77a99e07f4e2f2ad24a` |
| `tracked-head.tar.gz` | `311cb8c246843802d136498130b002961a2ce9ade753a535f89e0c7fd6458dee` |
| `untracked-work.tar.gz` | `503b1b1cfef5dab131812e153d973f04de38fda22579ed75de3a34d9569a2fce` |

The local archive is a second recovery path, not a public dependency.  All
proof-facing sources needed for the scoped public claims are now tracked.

Regenerable local caches intentionally excluded from Git include:

- `.tmp_py/` (a 142 MiB temporary package environment);
- `centered_quarter_k4_flag_psd/.../matrix_cache/*.npz`;
- the compiled `enumerate_k5_orbits` binary;
- `root_triangle_k7_overlap/*_moments.npz`.

Their generators, exact smaller outputs, or both are tracked.  The compressed
pre-split archive retains the original cache copies if forensic recovery is
ever useful.

## Definition of a successful resumption

A resumed program should not be called successful merely for adding another
necessary condition or excluding another guessed finite support.  The target
remains one of:

- exact coordinates for a code of the largest feasible size among 41--44; or
- a universal, independently auditable proof that no 41-point code exists.

Until then, the title of this checkpoint remains: **incomplete research
dossier, not a resolution**.
