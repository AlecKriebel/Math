# Reproduce round 3

All commands below operate from this review directory. `PYTHON` denotes the
repository shard's pinned `tooling/math-venv/bin/python`; preserve the venv
executable path rather than resolving its symlink. Set TMPDIR to this review's
tmp directory if a fully local scratch destination is desired.

```
PYTHON -B routine_offline_controls.py
PYTHON -O -B routine_offline_controls.py
PYTHON -B independent_checks.py
PYTHON -O -B independent_checks.py
```

The routine harness is an exact copied source of the frozen author's
offline_controls.py. It loads the CURRENT repaired helper source and reports
its hash. Its 147 controls use synthetic service fixtures and a disposable
toy Git repository. There are no real fetch, push, append or API writes.

The independently authored checks use the two actual published receipts,
the accepted eleven inputs, and read-only access to the actual corrected
prepared Git tree. A synthetic 2099 preparation time deliberately distinguishes
that field from the actual 2026 receipt confirmation time. Negative timestamp
fixtures are copied under this review. The normal run performs an additional
full actual proposed-layout replay; the optimized run has the same other
82 control outcomes. Both keep original attempt and archive inputs unchanged.

Use the review-local numerical environment at
`../covariance_source_01/tmp/numerical-venv/bin/python` for:

```
NUMERICAL_PYTHON -B replay_optional_numerical.py
```

It reproduces saved numerical examples as floating-point checks. It does not
run the optimizer or certify any numerical error bound or extremum. The
complete analytic proof remains a written proof rather than a formal
certificate. The full archive verifier also replays the exact and symbolic
controls and required hostile mutations.

The frozen old replay_proposed_tree.py is deliberately NOT changed. Its
synthetic receipt placeholders omit verified_utc and consequently cannot be
passed through the repaired build_publication. The independent negative control
checks this version incompatibility explicitly. Current proposed-layout replay
uses actual receipts, not a silently altered historical fixture.

The actual parent prepared receipt/tree identities are pinned in
ACTUAL_PREPARED_TREE_CHECK.json. Reproduction against a later regenerated
tree should use that new receipt and rebind the read-only expected identity;
the historic result here describes the exact tree reviewed, not future states.

No live tracker read or public download was repeated by this round. The
actual prior receipt readbacks, exact public hashes and native metadata are
pinned and cross-checked. No unprepared future transport adapter is approved.

The separate OPERATOR_SIDE_EFFECT.json documents a reviewer command that
unexpectedly rewrote pre-existing generated local CLI documentation. It is
outside the intended review workflow and is not a reproduction step. No such
command should be rerun; no cleanup or restoration is implied by these tests.
