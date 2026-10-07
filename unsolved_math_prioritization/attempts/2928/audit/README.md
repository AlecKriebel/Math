# Independent audit package, ID 2928

`AUDIT.md` is the complete mathematical, source and artifact assessment. It accepts the separately frozen corrected packet only as an unsolved partial result, 3/5.

- `release_pins.json`: exact original and corrected archive/manifest identities
- `orientation_clarification.patch` and `patch_replay.json`: actual repair and byte-exact replay evidence
- `dataset_verification.json`: full-input identity checks without corpus contents
- `source_verification.json`: versioned public source pins and precise inspection limits
- `history_verification.json`: bounded repeated repository checks
- `replay_audit.py`: independent finite replay driver
- `replay_results.json` and `replay_results_optimized.json`: complete normal/optimized test evidence

Place the two archives and their external manifests in a directory, then run:

    python -B replay_audit.py --release-directory /path/to/releases

Use the external audit manifest to authenticate this package before executing its script. The checker and audit are not formal mathematical proof certificates. No source text, source PDF, dataset contents or private coordination material is included.
