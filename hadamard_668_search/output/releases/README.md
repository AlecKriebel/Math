# H(668) research-checkpoint release assets

The release notes are in `H668_RESEARCH_CHECKPOINT_V1.0.0.md`. Stable
repository copies of the three release PDFs are:

| PDF | SHA-256 |
|---|---|
| `../pdf/h668-eliahou-repair-obstructions.pdf` | `0f203088cb77ab68b92424f0f59f4fa1dcc8d921fff4743d06a382aa010b1d39` |
| `../pdf/h668-lp333-fixed-compression.pdf` | `98df2842ae7ab6e3a505f6cb237e847b7ae837b0b662bde986c73125c8ca5da2` |
| `../pdf/h668-semiregular-c37-conference-lifts.pdf` | `c8193ce8485a2642044d11ead0e10bea15589e76bff20021218401a85153012e` |

## Short-case production manifests

`h668-short-case-production-manifests-v1.0.0.tar.gz` contains all 2,304
retained production range manifests used by the complete nine-short-case
Eliahou boundary certificate:

- 256 ranges for each of cases 21--25 and 27--29, under
  `eliahou_short_block_census/output/production-case*/`;
- 256 ranges for case 26, under
  `eliahou_global_quotient_plan/output/production/`.

The archive is 925 KiB compressed and approximately 12.5 MiB extracted.
Its SHA-256 digest is

```text
6e38f08e9c3c9798bc5ca87a46ae9ccffdb54c6f1ed3901d6ac9ce3fd5d69084
```

Extract it from the `hadamard_668_search` directory:

```sh
tar -xzf \
  output/releases/h668-short-case-production-manifests-v1.0.0.tar.gz
```

Then run the live completion audit:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  python3 \
  eliahou_short_block_census/verify_nine_case_completion.py --live
```

The expected live result covers all 2,304 ranges and reports
`3,710,853,316,608` join rows, `88,927,740` modular survivors, and zero
exact integer supports.  The archive makes the live audit available
without publishing the much larger exploratory and temporary outputs.

This is a hash-addressed computation record, not a substitute for checking
the producer, verifier, and mathematical encoding.

## Dense-shell production census

`h668-dense-shell-production-v2-v1.0.0.tar.gz` is the compact,
self-verifying production record behind the eighteen-orbit dense
\(n_9=0\) result in the fixed-compression LP(333) paper. It contains:

- all 729 complete prefix-shard JSON records;
- the v2 manifest, pinned compiled helper, and frozen aggregate;
- the production runner, aggregator, orbit replay, and regression sources;
- the characteristic-two dependency used by the detached witness replay.

The archive is approximately 328 KiB compressed. Its SHA-256 digest is

```text
493f73884ff5b5454f179b7754c0207178eeb70c70c27750daa610f3bda6c2df
```

After extracting it into a new directory, rebuild the aggregate with:

```sh
python3 \
  dense_shell_classifier_pilot/aggregate_dense_shell_production.py \
  --output dense_shell_classifier_pilot/output/production-v2 \
  --shell h0 \
  --aggregate-output rebuilt-aggregate-h0.json
```

The command strictly checks the manifest and every shard, independently
replays every retained exact orbit, and writes an aggregate whose SHA-256
must be

```text
3bccde87f456bfcd2f0c3da6ac8cf9cb3635538e831a95951003068ae87cae86
```

The packaged frozen aggregate has the same digest. The archive preserves
the historical production record; a genuinely independent validation
would also audit or reimplement the enumerator and mathematical encoding.
