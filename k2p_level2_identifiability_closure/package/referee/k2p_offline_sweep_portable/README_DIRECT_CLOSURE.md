# Four-port direct-residual closure release

This extension of the locked four-port sweep closes the **36 direct candidate
relations** isolated by the finite pass.  It is deliberately narrower than a
final network-identifiability theorem.

## Exact result in this release

The current-lock six-source run contains 1,931 canonical classes:

| Status | Count |
|---|---:|
| separated | 845 |
| isomorphic | 20 |
| ordinary triangle | 35 |
| restoration parent | 997 |
| unresolved by the sweep driver | 34 |
| error | 0 |

The direct proof overlay treats the 34 unresolved rows and independently
replays the two cubic rows already classified by the driver.  Its fixed exact
obstructions are:

- one transported quintic for 22 `theta0` repair-1 port relabelings;
- three quartics and their symmetry transports for 12 lower-theta rows; and
- one cubic, substituted separately into two `theta3` targets.

For every one of the 36 rows, the verifier reconstructs the paired-sector K2P
Fourier map from graph switches, proves that the displayed obstruction pulls
back to zero on the target, proves a nonzero source pullback, checks bridge
multihomogeneity, and evaluates a nonzero strict `D_plus` physical witness.
No atlas pickle and no separator search is used in this proof replay.

## One-command qualification

From this directory, in the pinned environment from `requirements.txt`, run:

```bash
python verify_direct_closure_release.py
```

The command first qualifies the immutable sweep engine, then validates the
separate direct-closure lock, recomputes all six 1,931-row manifest roots, and
replays the 36 exact obstructions into a temporary certificate.  The replay
must be byte-identical to the committed golden certificate.

The verifier-facing mutation qualification is run separately so that it cannot
recurse through the production verifier:

```bash
python test_direct_closure_release_mutations.py \
  --output /tmp/k2p-direct-closure-mutations.json
```

It first checks the clean locked package, then runs ten coherently relocked
content attacks plus the optimized-Python attack.  A case qualifies only with
exit status one and its exact case-specific diagnostic; tracebacks, import
failures, timeouts, signals, other non-one exits, and success terminals are
rejected.  Routine reports must be caller-owned paths outside this source tree.
The committed `direct_closure_mutation_report.json` is resealed only by naming
that exact path together with `--allow-authoritative-output`.

The published result payload under `results/four_port_release_v4/` contains:

- the complete merged status;
- all six complete residual manifests, including summaries for all 1,931
  classes; and
- the 36 raw records used by the direct proof overlay.

The other 1,895 raw records are omitted because their complete summaries are
already hash-bound in the manifests and they are not inputs to the 36 proof
replays.  A referee can regenerate every raw record with the command below.

## Full sweep regeneration

The complete run is deterministic at the semantic level and resumable:

```bash
python resumable_four_port_driver.py \
  --package-root . \
  --output-root /path/to/four_port_run \
  --manifest-every 25 \
  --source-index 0 --source-index 1 --source-index 2 \
  --source-index 3 --source-index 4 --source-index 5

python merge_manifests.py \
  --package-root . \
  --run-root /path/to/four_port_run \
  --allow-unresolved
```

On the reference M1 Pro, the one-process run took about six minutes and peaked
near 1.5 GB RSS.  The original 94-second pass was faster because it stopped at
quadratics; the current runner also exhausts every cubic block on the direct
residual stratum.

## Scope boundary

This release proves that no one of the 36 direct candidates is a generic
source-to-target containment on the positive K2P domain.  It does **not** by
itself close:

- the 997 restoration-parent child obligations;
- a graph-derived topology/rank exclusion ledger with dimension upper bounds;
- extension of positive-domain certificates to mixed-sign strict-stochastic
  parameters; or
- the final global necessary-and-sufficient theorem.

The sweep engine remains bound by `INPUT_LOCK.json`.  Direct-proof files and
the published result subset are separately bound by
`DIRECT_CLOSURE_LOCK.json`; separating the locks avoids a circular dependency
between a run and the proof package that contains it.
