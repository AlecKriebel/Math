# One-command replay for C-035

This directory provides a fail-closed replay of the certified finite claim

> No graph \(G\) on 12 vertices satisfies
> \(\gamma(G)=\gamma^\infty(G)=3<\theta(G)\).

It does not claim a universal resolution.  The replay imports no search,
synthesis, graph-evaluation, or eternal-domination implementation.

## Fast metadata audit

From the campaign root:

```sh
python3 -I -B repro/c035/replay.py --mode fast
```

This mode:

- checks the SHA-256 and byte size of the exact accepted theorem,
  reviews, formulas, proofs, certificates, ledgers, and checker;
- expands and verifies the complete file ledgers in the C5 run, sealed C7
  package, C7 source binding, and sealed C9 package;
- checks 91 exact file bindings, including every decisive proof and the
  executing replay/lock bytes;
- independently parses the distinct C5, C7, and C9 activation states;
- checks the theorem, two reviews, disconnected-case flag, exact scope
  exclusions, and `ART-217` through `ART-220` manifest rows;
- reads accepted Git commit
  `36d8191ac72c4c04291184f2a6854fa76e181712` directly and recomputes
  SHA-256 for every tracked accepted blob.

The report names the four exact but non-Git-anchored files: the bootstrapped
checker binary and source, plus the currently executing replay and its
self-pinned lock.  The checker is still SHA-256 pinned and every full branch
auditor independently checks it; this field makes the storage boundary
explicit.

Success is exactly `PASS_METADATA_ONLY` with
`claim_status=NO_MATHEMATICAL_CLAIM` and
`proofs_freshly_replayed=false`.  This mode never presents hash checking as a
fresh mathematical certificate replay.

## Full proof replay

```sh
python3 -I -B repro/c035/replay.py \
  --mode full \
  --output /a/fresh/path/c035-full-replay.json
```

Full mode first performs the complete fast audit, then runs these four
audits sequentially in new mode-`0700` temporary directories:

1. the clean-room C5 formula/proof/post-run audit;
2. the independent C5 retained-package audit;
3. the sealed C7 addition-only auditor with `--replay-checker`;
4. the sealed C9 recovery auditor with its pinned DRAT-trim checker.

Thus all three decisive branch proofs are freshly checked.  Each child uses
isolated Python (`-I -B`), a sanitized environment, no stdin, a fresh
`HOME`/`TMPDIR`, an exact timeout, exclusive stdout/stderr files, and no
shell.  Only one child runs at a time.  Before every child, the wrapper
requires at least 3 GiB available memory and 1 GiB scratch space by default.
It also requires the one-minute load average to be at most 75% of the
detected logical CPU count (7.5 on the campaign Mac).  This ceiling is
configurable with `--maximum-one-minute-load`, but must remain strictly below
the logical CPU count.  The branch auditors add their own memory, file-size,
checker-mode, warning, and heavy-job-lock gates.

After the four replays, every accepted input and the executing replay/lock
bytes are rehashed and compared with their pre-run inode and timestamps.
Any mutation, warning, timeout, nonzero exit, extra status marker, missing
`s VERIFIED`, nonzero RAT count, malformed JSON, or nonempty stderr rejects
the run.

Full success is exactly `PASS_FULL_C035_REPLAY` with
`claim_status=CERTIFIED-FINITE` and `proofs_freshly_replayed=true`.  The
original SAT solvers are not rerun: the mathematical evidence is the
retained proof checked afresh.

The `--output` target must not exist.  The writer uses exclusive creation
and never overwrites a prior report.  Without `--output`, the canonical JSON
report is written to stdout.

## Tests

The bounded test suite exercises the real fast audit and adversarially
checks status parsing, manifest scope, duplicate JSON keys, non-finite JSON,
exclusive outputs, mutation detection, all four full-mode command lines,
and fresh isolated-child behavior:

```sh
PYTHONWARNINGS=error python3 -B -m unittest -v tests.test_c035_replay
```

The unit suite deliberately does not launch the four expensive proof
replays.  Run full mode only when the campaign heavy-job lock and resource
gates permit it.

## Portability boundary

The accepted C5 run records absolute paths and its clean-room audits bind the
exact current checkout.  The wrapper therefore requires the campaign to
remain at repository-relative path `gamma_theta_eternal_domination` and the
accepted commit to be an ancestor of `HEAD`.  Fast mode reports this
provenance boundary instead of claiming path-relocatable production.
