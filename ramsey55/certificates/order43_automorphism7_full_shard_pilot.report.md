# Order-43 automorphism-7 exact side cover and full-shard pilot

Date: 2026-07-24

## Scope

This checkpoint closes the finite side-model enumeration prerequisite for the
normalized cycle type \(7^6 1\), implements a fail-closed selector-lifted shard
pipeline, and certifies one maximum-size shard.  It does **not** certify the
remaining 127 shards and therefore does not exclude the complete order-7
branch.

## Exact side-model exhaustion

The 30-variable one-side formula has exactly 191,394 satisfying assignments.
They are retained as a sorted, unique model list.  Completeness is certified by
adding the corresponding 30-literal blocker for every listed assignment and
proving the resulting formula UNSAT.

- model list: 5,933,214 bytes; SHA-256
  `e5043141e771eb1c0f615c620e2ae39f3a911915f1a4385ae60351538df7eeab`
- exhaustion CNF: 30 variables, 195,012 clauses, 18,573,352 bytes; SHA-256
  `ae4f0fd947e1d4b9ac34b35bbe973e1e23231ff4f7f8c9c34125cbb1ff51deee`
- Glucose3 conflicts: 351,804
- DRAT: 26,251,320 bytes; SHA-256
  `771cbbe6f7a9bd7dcb79e2e6905eca2f59cecf7866f3d0a1c8ee1f1e216720be`
- LRAT: 49,294,605 bytes; SHA-256
  `b201172e1c5fc80d6341e89aba6cecaaa4cf0a3b5031ed4222b5de9539a09dda`
- retained exact-cover bundle: 100,058,410 bytes, below the 512 MiB cap
- independent bundle check: every listed model directly satisfies the side
  formula, the exhaustion CNF is reconstructed byte-for-byte, DRAT and LRAT
  both verify, and regenerated LRAT is byte-identical
- bundle-check SHA-256:
  `d958bc62726c9607478012803037aec93b59cdab1c683361c4518f6bbe742e53`

Thus the earlier pair quotient is no longer merely relative to an
uncertified model list: its 191,394-model input is exact.

## Fail-closed shard pipeline

The runner and independent checker implement the 128-way schedule
`pair_index modulo 128`, with 290 or 291 representative pairs per shard.
For each pair the runner:

1. solves under a hard 200,000-conflict cap;
2. directly replays any SAT assignment and immediately stops the negative
   pipeline;
3. aborts on an indeterminate result or any cap breach;
4. removes raw deletion records, lifts every proof addition under its selector,
   derives the 60-literal pair blocker, and rederives the selector;
5. checks the completed wrapper proof with pinned `drat-trim`;
6. converts it to LRAT, checks LRAT, and compresses both streams under file
   limits.

The independent checker rebuilds the 664 side classes and all 37,194 pair
representatives from the certified model list, reconstructs the selected shard
and wrapper, audits every lifted proof segment, decompresses both retained
streams, and regenerates LRAT from DRAT.

Four focused tests pass.  The runner/checker/test SHA-256 values are,
respectively:

- `dd6c4d82c599adfc881691532133e3abb08740e7cb081aadc270b4bb997073ae`
- `04a15d1250355bfba1a09ec0a3584f9676f4d644c668047f858a0e41df44f471`
- `c04fcd8229f0776006b861ac35a52e494290c5ba60caf7760a5eeb6862be3fa8`

## Maximum-size shard-73 pilot

Shard 73 was preregistered because it contains 291 pairs and includes pair
37,193, the hardest endpoint in the prior twelve-pair sample.

- pairs certified UNSAT: 291/291
- first/last pair indices: 73 / 37,193
- maximum conflicts for one pair: 9,135, versus the 200,000 cap
- total conflicts and lifted additions: 464,751
- raw deletion records discarded before lifting: 77,042,216
- sum of solver wall times: 688.394 seconds
- end-to-end runner time: 1,108.897 seconds
- wrapper: 37,323 variables, 291,454 clauses, 10,566,888 bytes; SHA-256
  `6b4d510a818e1135ba100d21dccbd362b10a53688a17e10c1dce670c8117e098`
- lifted DRAT: 32,761,321 bytes; SHA-256
  `16d4391075066c48b2066d166813b48ae931fc9ad3f95db2d198e73147783753`
- compressed DRAT: 5,135,902 bytes; SHA-256
  `6ba11da104a704b92ac7e7b107d8b3e39986985c303c758fadc59df4f1413257`
- LRAT: 146,139,966 bytes; SHA-256
  `e6201134a215485a0d8cf8f20e498863345fe6ace7f0c7fa540e2a9ad02d961f`
- compressed LRAT: 18,659,091 bytes; SHA-256
  `5668c14c7fd49d2c4adae04355dfec003af0884a9745d4147c576dae3b99ee11`
- result SHA-256:
  `43b2d1e4bea5521db4d4bf51716735543d6673c302565677d5a6b2c9f834b461`

The independent replay completed in 182.959 seconds.  It reconstructed the
certified schedule and wrapper exactly, accepted all 291 segments, verified
both proof formats and compressed artifacts, and regenerated the same LRAT
byte-for-byte.  Its SHA-256 is
`6fe337ed22aa3bf8447f82a89bb98e088df9e8efd9d22ee2740e0d76808a468c`.

## Post-pilot storage and runtime audit

The maximum-size pilot scaled across 128 shards projects:

- 657,395,456 bytes retained compressed DRAT;
- 757,453,866 bytes total when combined with the exact side-cover bundle;
- 141,938.765 seconds for production and 23,418.722 seconds for independent
  replay if run serially at the pilot rates;
- 206,697 seconds (57.42 hours) after a frozen 25% contingency, below the
  72-hour empirical runtime gate.

The proof-size, retained-volume, exact-evidence, tooling, and empirical runtime
gates pass.  At the audit instant, however, only 8,296,607,744 bytes were free,
830,197,760 bytes short of the new 9,126,805,504-byte production envelope.
Consequently the audit status is **DO NOT LAUNCH** and no production shard was
started.

The older conservative LRAT-only gate remains unchanged and frozen at
20,317,547,392 bytes.  Launch-audit plan/result SHA-256 values:

- `9818bc2a048e2189fc5463d279adb165f04edee3bd4fd5b82aaf24261786394d`
- `c84a3bf2cea28e30de0ea204dabb0d4e2d9f92618b07ca0aa59f84041a5eb620`

## Claim boundary

This checkpoint certifies:

- the complete 191,394-model side list;
- the exact 37,194-pair quotient schedule relative to that complete list;
- the correctness of the fail-closed shard proof protocol on shard 73; and
- UNSAT for the 291 representatives in shard 73.

It does not certify any representative in the other 127 shards.  No complete
order-7 exclusion, no order-43 nonexistence theorem, and no new Ramsey bound
follows from this checkpoint.
