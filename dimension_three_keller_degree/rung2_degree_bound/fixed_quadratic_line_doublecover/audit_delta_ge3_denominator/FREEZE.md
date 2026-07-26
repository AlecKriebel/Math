# Frozen blinded denominator audit

Frozen at `2026-07-25T18:19:18-07:00`.

Verdict: `PASS`.

Strict replay marker:

```text
DELTA_GE3_DENOMINATOR_STRICT_PASS_26
```

SHA-256 manifest:

```text
24e0be9c44e7c2f57ba4a584af8ec23f98703a3b1b10e74d8b3d0191edbe8200  REPORT.md
440df4694f98b1b361a09e136afb4365c3aa302c5532e5291f4b76a2a068c65a  DENOMINATOR.json
ab67801af94865644f6aa655a9311b915a9d2999b99c25600c4abd2becc8e7fb  verify_delta_ge3_denominator.py
beae3835b086b2bec72ef9be3554b0277549d76dfb16746977d212377ffa4f07  verify_strict.sh
1d46f677af587d918b75b48c37270d6405b893051a5a71d345e22f783b98b0c9  RESEARCH_LOG.md
```

The frozen audit did not inspect the prohibited primary directory, did not
read or reconcile against primary-agent results, and did not attempt any
lower Keller-equation exclusion.
