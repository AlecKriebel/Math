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

It now performs only lightweight frozen-certificate checks for the verified
n=4 base and n=3 graph/path layers.  It deliberately does not rerun the
withdrawn n=3 terminal routine or any other heavy job.

The n=3 path-only check is:

```bash
bash reviews/final_hard_cover_cleanroom/verify_schema3_n3_quick.sh
```

Every command reads the locked primary streams but writes only beneath
`reviews/final_hard_cover_cleanroom`.  No primary replay is invoked.

Historical scripts and certificates under
`history/superseded_pre_exact_rooted_descriptor_cache/` bind older primary
bytes and must not be used as current evidence.  Active p/q probe closure is
**UNRESOLVED**.

The withdrawn n=3 terminal attempt is preserved separately under
`history/withdrawn_n3_terminal_two_active_labels/` and must not be executed or
cited.
