# Principal-D+ theorem assembly

This directory is a proof-first assembly area for the prospective global K2P
classification on

\[
\mathcal D_+=\{(s,g):0<s<1,\ 0<g<1,\ g>2s-1\}.
\]

It does **not** claim `K2P-SAME`.  Its purpose is to prevent theorem-level
prose, cached conversation claims, or a finite retained-class computation from
being mistaken for a replayable global proof.

## Current evidence verdict

Two substantial layers are locally replayable:

1. the continuation-2 common ordinary-triangle germ and tree--sunlet sign
   obstruction; and
2. the current-lock proof overlay separating all 36 named direct four-port
   candidates.

The archived first checkpoint contains useful formulas and a clean-room
compiler, but its `quick_check.sh` refers to domain and bridge verifiers that
are absent from the archive.  The later physical bridge, paired marginal,
conditional gluing/genericity/reconstruction, continuous-time, and weak-class
sharpness results survive only as conversation text or project summaries; the
referenced proof attachments are not present locally.

The finite release contains 997 restoration parents and 2,962 child requests,
but no bound five-port child records.  There is also no graph-derived raw
universe ledger partitioning every raw presentation into retained,
topology-excluded, and dimension/rank-excluded cases.  These are hard blockers.

## Files

- `EVIDENCE_INVENTORY.json` records exact local hashes and evidence strength.
- `THEOREM_STATEMENTS_DRAFT.md` states the candidate theorems without
  promoting them.
- `DEPENDENCY_MAP.md` gives the necessity/sufficiency dependency structure.
- `THEOREM_GATES.json` is the machine-readable promotion policy.
- `raw_universe_ledger.status.json` and
  `restoration_ledger.status.json` make the two largest open obligations
  explicit.
- `verify_theorem_gates.py` validates evidence hashes and refuses promotion
  unless every required gate, including both ledgers, is genuinely closed.
- `test_theorem_gate_fail_closed.py` adversarially checks the refusal logic.

## Reproduce the current verdict

From the project root:

```bash
.venv/bin/python -B work/theorem_assembly/verify_theorem_gates.py
.venv/bin/python -B work/theorem_assembly/verify_theorem_gates.py --replay-available
.venv/bin/python -B work/theorem_assembly/test_theorem_gate_fail_closed.py
```

The first and third commands should return success while reporting
`K2P_SAME_NOT_PROMOTABLE`.  The explicit promotion request must fail:

```bash
.venv/bin/python -B work/theorem_assembly/verify_theorem_gates.py \
  --require-promotable
```

