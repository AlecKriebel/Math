# Independent low-closure partition audit: fail-closed recovery v2

## Outcome

The recovery audit is valid. It independently reconstructs the finite
\(E=3/E=4\) quotient, the complete configured first-edge schedule, and the
recovered deterministic search result. This is a finite-corpus and
reproducible-search audit, not a proof that an order-43 Ramsey graph does not
exist.

The corrected audit is:

```text
results/verification/e2_low_closure_partition_independent_v2.json
SHA-256 48437f3d20788379e3ba890f73086c51777bd068d7056ac0ce613aec97fb5c4e
status VALID_FINITE_CORPUS_PARTITION_AND_SCHEDULE_AUDIT
errors 0
```

## Preserved initial failure

The first independent audit failed closed solely because it compared these
two equivalent output-path spellings literally:

```text
ramsey55/results/constructive/e2_low_closure_v2/second_barrier_new_E2.g6
results/constructive/e2_low_closure_v2/second_barrier_new_E2.g6
```

Its exact bytes remain preserved:

```text
results/verification/e2_low_closure_partition_independent_initial_invalid_v1.json
SHA-256 0a83743f5c04011efefa6f201c3c87332805d4ffa0216826de9901455f27aed8
status INVALID
```

Regression tests now resolve plan-relative, parent-relative, and absolute
paths to the independently supplied artifact, while rejecting unrelated
paths. The tests also distinguish ordinary from complement-isomorphism class
counts and reject deliberately misbound representatives.

## Non-destructive recovery

Because the v1 executable was ephemeral and later overwritten, the recovery
used the exact source blob from immutable Git commit
`5677276e8135daec5af9fb09e360ec9b8a8dfe79`:

```text
ramsey55/src/search43_e2_barrier_escape.cpp
SHA-256 cdddaef4c35dfb9ccdbcc7478029c15eb909247714ffc2bef9e8fa636fb0099c
```

It was compiled to a distinct preserved executable:

```text
results/constructive/e2_low_closure_recovery_v2/search43_e2_barrier_escape_5677276e
SHA-256 4597c7fb130edbf75c9a192a2042f44acda0a897193fcef22af98b56165b0a34
```

The independent audit rebuilt the same commit with the frozen compiler and
flags and obtained the identical executable hash. It also independently
hashed the preserved executable.

The recovery plan was frozen before execution:

```text
results/benchmark_plans/e2_low_closure_second_barrier_recovery_v2.json
SHA-256 edb75ba318df551b370112867443a1502438eaba4bda9971caf079b3f8bc42c3
```

It binds the commit and source, compiler and executable, all 22 known-\(E=2\)
seed arguments in order, both low-seed streams, every search parameter, and
distinct v2 output paths.

## Reproduced result

The recovered run produced:

```text
results/constructive/e2_low_closure_recovery_v2/second_barrier_v2.result.json
SHA-256 4969871cccbd0e07edf169fd468aafa2a3584f176ba858d706d104fc77d60da4

results/constructive/e2_low_closure_recovery_v2/second_barrier_new_E2_v2.g6
SHA-256 ba35df48ba6577605135fda1c893283b76420724bd9ff70b4c0641427ec96e97
```

All substantive result fields reproduce v1 exactly:

| quantity | value |
|---|---:|
| low-seed complement classes | 53 |
| forced first barriers | 47,675 |
| non-conflict barriers | 46,225 |
| high conflict-union barriers | 1,450 |
| exact forced-graph replays | 47,675 |
| repair steps | 2,080,964 |
| exact objective checks | 2,125,169 |
| retained labeled \(E=2\) endpoints | 1,670 |
| \(E=1\) visits | 0 |
| \(E=0\) constructions | 0 |

The recovered 1,670-record discovery stream is byte-for-byte identical to
the v1 stream.

## Independent partition and schedule checks

Traces independently found:

| stream | ordinary classes | classes modulo complementation |
|---|---:|---:|
| \(E=3\), 16,082 labeled graphs | 18 | 9 |
| \(E=4\), 73,788 labeled graphs | 88 | 44 |
| total | 106 | 53 |

Every complement class contains exactly one published representative and
its complement. Independent \(K_5/I_5\) enumeration recounted all 53
representatives and reconstructed all 47,675 scheduled first barriers with
zero ceiling exclusions.

Every one of the 1,670 recovered endpoints independently recounts to
\(E=2\); each consists of two same-color forbidden five-sets intersecting in
four vertices. Their four ordinary isomorphism classes form two classes
modulo complementation, matching the two previously known basins.

The checker and its nine focused tests are:

```text
verify/e2_low_closure_partition_independent_check.py
SHA-256 e77f4ee29c9eb1b532f0d3827e04b5d579ec7d69c818e791241e312516bc1358

tests/e2_low_closure_partition_independent_tests.py
SHA-256 7566dc4543119667a777ac5bb3ba1658805686411023c0700f8fd5b54fcfb303
```

## Claim boundary

The classification is exact only for the supplied 89,870 labeled
low-closure states. The 47,675 first forced edges exhaust the frozen
outside-closure rule on the 53 representatives, but each subsequent
256-step tabu/noise repair is heuristic. The negative result therefore
implies no global nonexistence statement and does not change the public
bound \(43 \le R(5,5) \le 46\).
