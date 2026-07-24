# Exact row-margin plus digit-three pilot

## Status

This scratch instrument intersects the true digit-three phase prefix with
the exact physical row-margin corpus for one of the five shell-two profiles.
It exists because all nine phase-only digit-two census hits, including both
stage-2.5 points, fail the independent row-margin join.

The model works on the 54 original placement trits.  It combines:

- the rank-18 first placement digit;
- all eighteen digit-two histogram congruences;
- the delayed nineteenth digit-three linear equation;
- the other eighteen digit-three carry congruences;
- exact membership of the six Eisenstein phase sums in the compatible
  row-margin corpus.

Every future positive result is replayed against both the exact displayed
Eisenstein coefficients and the row-margin phase sums.  A solver timeout is
recorded only as `UNKNOWN`.

## Candidate-zero pilot

The all-target model for `h2-222222-0` has 72 compatible row-margin targets,
2,230 variables, and 1,124 constraints.  A four-worker 600-second CP-SAT
run ended

```text
status=UNKNOWN
branches=3,671,985
conflicts=51,454
maximum resident set size=421,527,552 bytes
```

It found no point, but this is neither an exclusion nor certified coverage.
The replayable performance checkpoint is
`row_margin_digit3_candidate0_checkpoint.json`.

## Reproduction

The optional solver environment needs OR-Tools:

```text
python search_row_margin_digit3_cp_sat.py \
  --candidate 0 \
  --seconds 600 \
  --workers 4 \
  --seed 38668 \
  --output row_margin_digit3_candidate0_checkpoint.json
```

Use `--target-index` to search one compatible row-margin shard rather than
the 72-target union.  `--initial-certificate` may provide placement hints;
it never bypasses exact replay.
