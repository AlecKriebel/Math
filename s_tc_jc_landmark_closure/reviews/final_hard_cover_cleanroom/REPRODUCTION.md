# Reproduction

Run the quick frozen-certificate check from the repository root:

```bash
bash reviews/final_hard_cover_cleanroom/verify_schema3_n4_quick.sh
```

Regenerate the complete active n=4 graph/path/terminal audit and mutation
suite:

```bash
bash reviews/final_hard_cover_cleanroom/verify_schema3_n4_full.sh
```

The package-wide entry point is:

```bash
bash reviews/final_hard_cover_cleanroom/verify_all.sh
```

Every command reads the locked primary streams but writes only beneath
`reviews/final_hard_cover_cleanroom`.  No primary replay is invoked.

Historical scripts and certificates under
`history/superseded_pre_exact_rooted_descriptor_cache/` bind older primary
bytes and must not be used as current evidence.  Active p/q probe closure is
**UNRESOLVED**.
