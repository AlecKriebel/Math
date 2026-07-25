# H(668) research-checkpoint release assets

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
