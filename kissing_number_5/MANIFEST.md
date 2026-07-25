# Reproducibility manifest

Checkpoint: 2026-07-24T16:33:20Z

Program state: paused, unresolved

Global bounds: \(40\le\tau(5)\le44\)

The former append-only manifest had accumulated stale duplicate hashes.  This
checkpoint replaces it with one generated checksum file:
[`PAUSE_MANIFEST.sha256`](PAUSE_MANIFEST.sha256).

## What the checksum proves

`PAUSE_MANIFEST.sha256` hashes every Git-tracked file under
`kissing_number_5/` except the checksum file itself.  From the repository root:

```sh
shasum -a 256 -c kissing_number_5/PAUSE_MANIFEST.sha256
```

A successful run proves only that the local files are byte-for-byte identical
to this checkpoint.  It does not prove the mathematical interpretation of a
certificate.  Claim scope and proof status remain governed by
[`CLAIMS_LEDGER.md`](CLAIMS_LEDGER.md).

To regenerate after an intentional edit, from the repository root:

```sh
git ls-files -z kissing_number_5 \
  | tr '\0' '\n' \
  | grep -v '^kissing_number_5/PAUSE_MANIFEST.sha256$' \
  | sort \
  | xargs shasum -a 256 \
  > kissing_number_5/PAUSE_MANIFEST.sha256
```

Review the resulting diff and rerun the checker before committing.  Do not
silently refresh hashes after an unexplained mismatch.

## Exact pause-checkpoint commands

The small construction certificate:

```sh
cd kissing_number_5
python3 verifiers/verify_d5.py certificates/d5_roots.json
```

The quarter-grid ADE package:

```sh
ADE=experiments/centered_quarter_k4_flag_psd/audit/k5_centering_products/rank5_strengthening
python3 "$ADE/verify_ade_core_shells.py"
python3 "$ADE/verify_general_quarter_grid_moments.py"
python3 "$ADE/verify_r11_profile_ade_bounds.py"
```

The scoped five-cycle package:

```sh
cd experiments/r18_c5_h_energy
python3 verify_manifest.py
python3 test_verify_lambda_max_c5_cell.py
python3 test_verify_adjacent_merge.py
```

The realized-\(D_5\) extension package:

```sh
cd experiments/weighted_common_source_attack/realized_d5_extension
python3 test_verify_small_union_hall.py
python3 test_verify_hall_counterexample.py
python3 test_verify_uniform_conflict_charge_counterexample.py
python3 test_verify_known_28.py
```

See [`RESUME.md`](RESUME.md) for a five-minute smoke test and the exact
limitations of each package.

The complete central suite was also run from `kissing_number_5/`:

```sh
python3 -m unittest discover -s tests -v
```

Final result: 155 tests passed in 1,575.892 seconds.  This includes the
long-running exact cap-domain reconstructions and their tamper checks.

## Environment

Final audit environment:

- macOS;
- Python 3.14.6;
- Git 2.38.2 or later;
- standard library only for the commands above.

The discovery stack is pinned separately in
[`requirements-discovery.txt`](requirements-discovery.txt).  NumPy, SciPy,
CVXPY, NetworkX, and solver output are not trusted by proof-facing checkers
unless a package supplies a separate exact certificate.

## Excluded local caches

The checksum covers the tracked research record, not temporary environments or
regenerable numerical caches.  The following are deliberately ignored:

- `.tmp_py/`;
- Python bytecode and test caches;
- centered-\(K_5\) matrix-cache `.npz` files and the compiled enumerator;
- root-triangle moment-table `.npz` files.

The pre-split local safety archive retains these files.  All sources and
smaller exact artifacts needed for the public scoped claims are tracked.

## Boundary and optimization policy

- A proof-facing inequality must cover closed boundaries in the direction
  needed by the claim.
- Solver feasibility, infeasibility, or a small floating eigenvalue is never a
  certificate.
- Finite support, symmetry, antipodality, or a prescribed contact graph is
  never promoted to a universal theorem without a proved reduction.
- The rank-at-most-five condition may not be dropped from the Gram formulation.
- Older historical verifiers may rely on `assert`; use ordinary Python unless
  the package explicitly audits `python -O`.

The manifest authenticates a paused research dossier, not a solution.
