# Immutable baseline before the final Omega audit

This directory freezes the verified 18-page Outcome-P manuscript and its
active theorem metadata before any final Omega work or submission editing.

- Baseline commit: `1478af79fa51b1e139361cd73ab7188f216172e4`
- Branch at freeze: `codex/stc-jc-biorxiv-final`
- Freeze date: 2026-08-14 (America/Los_Angeles)
- Working tree before replay: clean
- Working tree after all three advertised replays: clean
- Main manuscript SHA-256: `a6981ccec9bd8c3786d413235d370b393ec754ed762b13974dfdfd30874ec760`
- LaTeX source SHA-256: `aae593bdc5405013242689bf859c375fa7fb0188796b6afc737fcab245a8896f`

The three advertised commands were run in a newly created clean worktree at
the exact baseline commit:

```sh
cd s_tc_jc_landmark_closure
bash reproducibility/verify_quick.sh
bash reproducibility/verify_full.sh
bash reproducibility/verify_regenerate_all.sh
```

All passed. Complete outputs are in `transcripts/`. The source, PDF, active
dependency graph, theorem/certificate crosswalk, and status metadata are
copied here byte-for-byte.

## Deterministic full archive

The local release asset `stc_jc_baseline_1478af79.tar.gz` has SHA-256

```text
c7c5a2a9ed594a015913506126387990edfb5527edccf3401c767a3673e92060
```

It is intentionally ignored by Git because it is 320 MB. It is reproduced
exactly from the commit by:

```sh
COPYFILE_DISABLE=1 TZ=UTC git archive --format=tar \
  --prefix=stc_jc_baseline_1478af79/ \
  1478af79fa51b1e139361cd73ab7188f216172e4 \
  s_tc_jc_landmark_closure s_tc_jc_sharp_boundary \
  | gzip -n -9 > stc_jc_baseline_1478af79.tar.gz
```

This history directory is immutable after the freeze. Later corrections and
submission files must live outside it.
