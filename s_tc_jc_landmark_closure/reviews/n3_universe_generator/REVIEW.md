# Independent n3 universe-generation report

Verdict: **VERIFIED**.

The final whole-proof referee correctly found that the earlier n3 clean-room
program validated a primary-supplied relation stream but did not generate the
stream's complete target grammar.  This package closes that scope failure.

The new generator starts from explicit primitive cores and repairs, builds
all source supports and both target incoming modes, evaluates the complete
exact invariant orbit, applies the directed necessary filter, and constructs
the normalized raw and merged theorem objects.  It obtains exact multiset
agreement, not merely the advertised counts:

```text
8 sources
831 selected-incoming completions
1,983 marginalized-incoming completions
10,826 raw relations
10,466 merged relations
```

The primary stream is opened only after independent generation.  Its
classification labels are not used to select a relation.  The independently
generated raw and merged multiset hashes agree exactly with the claim.

This package establishes relation-universe exhaustiveness.  The existing
bounded clean-room package establishes recordwise graph/algebra/sign and
terminal correctness.  Neither package alone is silently promoted as the
other.

Run:

```bash
bash reviews/n3_universe_generator/verify.sh
```

