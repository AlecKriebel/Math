# Review 1 independent rational checks: exact execution source

The accompanying `review1_independent_checks.py` is the exact Python source recovered from reviewer 1's executed tool-call transcript, not a newly substituted experiment. Its source SHA256 is `ad246d668ac55a7f80b1567d2cb8ff46d2959659da5bcd00a7165e2fd41b7907`. The unchanged original output is `review1_independent_checks_original_output.json`, SHA256 `da371485669b1c1342df065a0bf3d29fa0c0b2348ca2b9969a2649ce977a5530`, timestamp 2026-10-07T05:25:38.532968+00:00 (October 6, approximately 22:25 America/Los_Angeles). Python 3.14.6 ran the original experiment.

## Reproduce

From `/Users/alec/Documents/Math/openai_followon_nonlinear_maurey`:

```sh
mkdir -p work/package_review_1
python3 reviews/review1_independent_checks.py
```

Use ordinary Python with assertions enabled; do not use `-O` or `-OO`. Only Python's standard library is required. The exact original script writes `work/package_review_1/independent_checks.json`, so make its parent directory first. It prints the same JSON. A rerun replaces that scratch result; the preserved original output in `reviews/` remains unchanged.

Compare every result field except `timestamp_utc`, which records the time of each execution. Expected deterministic fields are:

- weighted multidimensional quartic cases: 1000;
- exact stationary-chain cases: 180;
- nonreversible cases: 106;
- tested time choices: 1, 2, 3, 7, 13;
- largest sampled squared cotype ratio: 5110968311/5357817576;
- its floating display: 0.9539272732790035;
- `all_passed`: true.

The random seed is 497233. Quartic cases use exact Fractions, independently chosen bit centers, cube points and positive weights over multiple scales. Chain matrices are averages of three permutation matrices, hence stationary for the uniform law. A rational Gaussian elimination solves the geometric resolvent. The checks test the cotype inequality directly for weighted binary input vectors and cubic witnesses. These are finite error-detection experiments, not a proof, formalization, exhaustive search or estimate of the sharp universal constant. They do not test arbitrary measure spaces by computation; that scope is established by the manuscript's proof.

This addendum preserves reproducibility evidence only. It changes no reviewed-input mathematical verdict, manuscript, live root documentation, or held-package hash.
