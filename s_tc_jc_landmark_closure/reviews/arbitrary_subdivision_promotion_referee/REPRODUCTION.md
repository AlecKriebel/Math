# Deterministic reproduction

Run from `s_tc_jc_landmark_closure`:

```bash
bash reviews/arbitrary_subdivision_promotion_referee/verify_all.sh
```

Expected final line:

```text
VERIFIED_AFTER_CORRECTION: arbitrary-subdivision promotion; exact bound 10; 16/16 mutations rejected
```

The replay is sequential and lightweight. It streams the existing compressed
records, never invokes an atlas generator or symbolic graph-algebra compiler,
and normally completes in under ten seconds on the project machine.

The replay verifies exact input hashes, compact path coverage, packed p/q
partitions, accepted-transport restriction, the compact/verbose clean-room
gate commitments, final weak-target role records, abstract word-order
reconstruction, the exact ten-port bound, and all theorem-logic mutations.

The scripts import no module under `primary` or another review directory.
