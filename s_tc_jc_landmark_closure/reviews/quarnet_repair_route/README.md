# Independent quarnet-and-repair route

This directory tests whether exact quarnet encoding, the published induced-
subnetwork distinguishability results, and the strong repair of the weak
Theta omnian close the standard-strong JC theorem without a large atlas.

Result: they reduce the theorem to three precise lemmas, but do not yet close
it.  The aligned minimal A-C/A-F `2 x 2` repair case is exactly separated by
displayed quartets.

Read:

1. `PROOF_ATTEMPT.md` for the conditional reduction and exact finite result;
2. `ADVERSARIAL_GAPS.md` for the rejected promotions; and
3. `check_minimal_repairs.py` for the independent bounded verifier.

Run:

```text
bash reviews/quarnet_repair_route/verify.sh
```

No executable in this directory imports project code.
