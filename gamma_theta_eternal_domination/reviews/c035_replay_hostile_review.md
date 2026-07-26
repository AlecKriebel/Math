# Hostile review of the C-035 one-command replay

## Verdict

**ACCEPT.**

The exact replay implementation, lock, README, and bounded unit tests listed
below are accepted as a fail-closed local replay package for C-035.

This verdict means:

- `--mode fast` correctly validates accepted bytes, Git anchors, branch
  activation states, manifest scope, and the finite claim boundary while
  emitting `claim_status=NO_MATHEMATICAL_CLAIM`;
- `--mode full` can promote its report to `CERTIFIED-FINITE` only after all
  four prescribed child audits return their exact accepted semantics;
- the full child command lines point to the accepted C5, sealed C7, and
  sealed C9 auditors and require warning-fatal forward RUP-only checking; and
- resource refusal, timeout, child failure, malformed output, artifact
  mutation, and output collision all fail closed.

No full proof replay was launched during this review.  The machine's
one-minute load was about `19.87`, above the default `7.5` ceiling, and the
review instructions expressly prohibited a full replay under that load.
Accordingly, this review accepts the wrapper's implementation and bounded
tests; it is not a new replay of the three mathematical certificates and
does not add a new theorem claim.

Review date: 2026-07-26 PDT.

## Exact reviewed bytes

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `repro/c035/replay.py` | 69,321 | `327b9a9b263bac737ffbeeea48e76e0926dd6470eee183dca8f411999db15722` |
| `repro/c035/accepted_artifacts.json` | 10,042 | `10b52635d90396135b7a529b3d4bca3987cf53d3693790ace07d679d604ae81d` |
| `repro/c035/README.md` | 4,500 | `c8602e2fc7e5878fda6996d07c019ac93232afd61a2df318455319ad2a294e64` |
| `tests/test_c035_replay.py` | 16,191 | `ca4f9a66b1dab83ec6a8ab04f9ffd8603f47869c2d8b359d360796da18bc8930` |

The lock SHA-256 is hard-coded in the reviewed replay and was independently
recomputed.  The replay and lock are intentionally outside the older
accepted C-035 commit; their exact bytes above, and a later release commit,
are therefore part of the trust bootstrap for this new wrapper.

## Bounded executions

### Unit and adversarial suite

The exact command

```text
PYTHONWARNINGS=error /usr/bin/time -lp \
  python3 -B -m unittest -v tests.test_c035_replay
```

passed all 15 tests:

```text
Ran 15 tests in 3.511s
OK
```

The outer timing record was 3.83 wall seconds with 43,679,744 bytes maximum
resident set size.  The suite ran the real fast metadata audit but did not
launch any of the four full-mode proof children.

### Real fast audit

The exact reviewed fast command exited zero:

```text
PYTHONWARNINGS=error python3 -I -B \
  repro/c035/replay.py --mode fast --output <fresh-path>/fast.json
```

The report had SHA-256

`d340583291c81eac695169a148ec9cc9274d5470467a6ab2f8065a6dfb4f3e55`

and exact decisive fields:

```text
status                    PASS_METADATA_ONLY
claim_status              NO_MATHEMATICAL_CLAIM
proofs_freshly_replayed   false
locked_artifact_count     91
git_anchored_artifact_count 87
artifact_snapshot_sha256  f080579ff7c44fb5ce7f16dba86543eafc7051218c3b55ae90c6a894ee6839aa
```

It bound the accepted commit
`36d8191ac72c4c04291184f2a6854fa76e181712` and confirmed that it is an
ancestor of the current `HEAD`.  A separate review script, importing no
replay code, rehashed all 44 explicit lock records and read 43 tracked blobs
directly from that commit; every size and SHA-256 matched.  The remaining
explicit record was the bootstrapped checker binary, whose non-Git storage
boundary is explicit.  Certificate-led expansion accounts for the remaining
47 bindings checked by fast mode.

### Live refusal before proof launch

A full-mode invocation with an intentionally impossible load ceiling exited
one, wrote zero stdout bytes, and emitted:

```json
{
  "claim_status": "NO_MATHEMATICAL_CLAIM",
  "error": "ReplayFailure: full replay refused by one-minute CPU-load gate",
  "mode": "full",
  "proofs_freshly_replayed": false,
  "schema": "gamma-theta-c035-one-command-replay-v1",
  "status": "REJECT"
}
```

No C5, C7, C9, or `drat-trim` proof process was launched or left running.

## Branch and status audit

The wrapper does not accept a generic `PASS` or an unreviewed solver status.
The three branches have distinct activation rules.

### C5

The retained branch is accepted only when all of the following agree:

- exact CNF
  `c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104`;
- exact addition-only binary proof
  `c6c24853e30073e66fb396441edb176a0160d062a8558e25fa18a955f33927c3`;
- exact clean-room post-run output
  `bd7693fdad225f733c0d2e704c4de45186324cc62ffdec09a112836ceec014e5`;
- exact retained-package audit output
  `470f58bf532ae8ff68ac3b8f096ba20166e6bcd91bee4924c1f924e276fea2cb`;
  and
- activating verdict
  `ACCEPT_C5_UNSAT_CERTIFICATE_FOR_C033`.

The full child list invokes both independent C5 audits in isolated Python.
Their accepted output hashes bind binary input, forward checking,
warning-fatal behavior, RUP-only checking, exactly one `s VERIFIED`, empty
stderr, and zero RAT lemmas.  The bound checker command is
`-i -f -W -U -t 1200`.

### C7

The full command uses the package-local accepted auditor:

```text
certificates/synthesis_k3_hole7_full_bank_seed0_addition_only_v2/
  repro/hole7_deletion_strip_auditor.py
  audit --package <sealed-v2-package> --replay-checker
```

It does not use the similarly named development copy under `reviews/`.
The exact CNF and proof hashes are respectively

`6a011e685e58ef517f2ab8253ca40987bd7b742a470bedbacdc3a5e94fc995a7`

and

`e8052df40d3e0c39b945a8735889039daba55eacc351e1822828b3d94f7baae9`.

The retained certificate and fresh validator require
`VERIFIED_FINITE_CERTIFICATE`, 284,317 proof additions, an actual fresh
checker replay, warning-free output, and RUP-only mode.  The package binds
checker flags `-I -f -W -U -t 600`.

### C9

The full command uses the sealed package auditor and passes the exact pinned
checker:

```text
certificates/synthesis_k3_hole9_orphan_000170_recovery/
  repro/hole9_orphan_recovery.py
  audit --package <sealed-package> --drat-trim <pinned-checker>
```

The exact CNF and proof hashes are respectively

`2845f242a094484a8d114e70ca1a8678dfcff79fadd56bd57813e25c2e49523d`

and

`24c5647d3a57f2de221fba96747c618575a3aba086c5e4bca17aade55ce7d4ab`.

The fresh package auditor's deliberately pre-review status
`audit_passed_pending_hostile_review` is not mistaken for final acceptance:
the wrapper separately binds the accepted C-028 record
`accepted_with_two_validated_errata` and the accepted graph-implication
review.  Fresh output must report checker flags
`-I -f -W -U -t 60`, exit zero, exactly one verified marker, and zero
warnings.

Independent mutations confirmed that the wrapper rejects:

- an inflated theorem scope claiming order-12 exclusion without the
  parameter-three restriction;
- a C7 `UNSAT_UNVERIFIED` status; and
- substitution of a pending C9 status for the accepted C-028 status.

The unit suite separately rejects mutated C5 verdicts, altered verified-line
counts, false C7 checker-replay flags, nonzero C9 warning counts, duplicate
JSON keys, non-finite JSON, trailing JSON noise, duplicate manifest IDs, and
scope-inflated manifest outcomes.

## Resource, timeout, cleanup, and immutability audit

Full mode runs exactly four children, sequentially.  Before each child it
requires:

- at least 3 GiB available memory by default, with a hard configurable floor
  of 2 GiB;
- at least 1 GiB free scratch space by default, with a hard configurable
  floor of 512 MiB; and
- one-minute load at most 75% of logical CPU count by default, with every
  accepted override still strictly below the logical CPU count.

Separate adversarial calls confirmed refusal below the memory and disk
floors as well as above the load ceiling.  C5 and C9 also use the campaign
heavy-child lock in their accepted auditors.  C7 is small enough to rely on
the wrapper's immediately preceding gate, sequential execution, and its own
620-second checker timeout; it does not independently acquire that lock.

Each wrapper child has:

- `start_new_session=True`;
- no stdin and no shell;
- isolated `HOME` and `TMPDIR`;
- exclusive mode-`0600` stdout and stderr files in a mode-`0700` directory;
- sanitized locale and `PATH`;
- an outer timeout constrained to 60--3,600 seconds; and
- process-group `SIGTERM`, followed by `SIGKILL` if required.

A bounded real process-group probe started a parent and sleeping grandchild,
called the reviewed cleanup function, and confirmed that the parent exited
by signal 15 and the grandchild no longer existed after 0.0016 seconds.

Accepted inputs reject symlink components and non-regular or multiply linked
files.  The full replay snapshots size, hash, device, inode, `mtime`, and
`ctime` before running children and requires all of them to remain unchanged
afterward.  The output writer uses exclusive creation, refuses an existing
file or dangling symlink, and never overwrites a prior report.  Unit
mutations exercised both the snapshot guard and exclusive writer.

## Claim boundary

Fast mode is correctly nonclaiming.  Full promotion is exactly the finite
claim:

> No finite simple graph \(G\) on 12 vertices satisfies
> \(\gamma(G)=\gamma^\infty(G)=3<\theta(G)\).

The lock and parser require the exact three exclusions:

1. order-12 common parameter \(k\geq4\) remains open;
2. orders at least 13 remain open; and
3. the universal gamma--theta conjecture remains unresolved.

The theorem must include disconnected graphs, the exhaustive branches must
be exactly C5/C7/C9, and both accepted theorem reviews must be present.
Neither metadata success nor a single branch result is allowed to promote
the claim.

## Nonblocking limitations and release conditions

1. **No full replay in this review.**  A later low-load run is still required
   before recording a fresh `PASS_FULL_C035_REPLAY` transcript.  Its absence
   does not weaken the already accepted branch certificates, but this review
   must not be cited as that fresh transcript.
2. **Path portability is deliberately limited.**  The historical C5
   artifacts contain absolute checkout paths, and their clean-room auditors
   bind the current checkout.  The README discloses this.  A permanent
   release should either preserve the documented path-compatible layout or
   add a separate portable direct formula/proof replay; failure at another
   path is fail-closed, not evidence against the certificate.
3. **Bootstrap files are newer than the accepted theorem commit.**  Before
   release, commit the exact reviewed replay, lock, README, tests, and this
   review without byte changes, and record their hashes in the campaign
   manifest.  The checker binary and source remain explicitly non-Git
   anchored but cryptographically bound by the lock and accepted branch
   auditors.
4. **Report ergonomics.**  The machine report validates the exact theorem and
   scope exclusions but does not repeat all three exclusion strings at top
   level.  The README states them, and the returned
   `theorem_scope.universal_conjecture_resolved=false` prevents universal
   inflation.  Echoing the full scope list would improve a future schema
   version but is not a soundness blocker.

No implementation blocker was found in the reviewed bytes.
