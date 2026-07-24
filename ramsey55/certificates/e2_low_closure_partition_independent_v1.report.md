# Independent audit of the E=3/E=4 closure quotient and second-barrier run

Date: 2026-07-23 (America/Los_Angeles)

## Outcome and evidence boundary

**VALID FINITE-CORPUS CLASSIFICATION AND RUN BINDING.** An independent
graph6 implementation and a Traces-based isomorphism route reproduce the
published quotient exactly:

- the 16,082 labeled `E=3` graphs form 18 ordinary isomorphism classes and
  9 classes modulo complementation;
- the 73,788 labeled `E=4` graphs form 88 ordinary isomorphism classes and
  44 classes modulo complementation; and
- every one of the 53 published representatives, together with its
  complement, binds to exactly one reconstructed complement class.

The independently reconstructed first-edge schedule has exactly 47,675
forced barriers. Its largest height is 47, so the configured objective
ceiling 80 omits no eligible first edge. Every schedule count and height
frequency matches the completed production result.

This is a classification of the supplied finite closure and an audit of one
heuristic search run. It does not classify all low-conflict order-43 graphs,
does not prove that a Ramsey graph exists or does not exist, and changes no
Ramsey bound.

## Independent quotient method

The checker imports none of the production graph, search, or quotient
modules. It independently:

1. decodes and re-encodes every graph6 record;
2. checks order 43, canonical payload length and padding, uniqueness, file
   hashes, and exact complementation for every record;
3. canonicalizes the raw streams with `shortg -t`, using the Traces engine
   rather than the published audit's dense and sparse `labelg` runs;
4. explicitly supplies every graph and its complement, then pairs the
   resulting ordinary Traces classes under the complement involution;
5. supplies every published representative and its complement in the same
   partition, requiring exactly one representative pair per complement
   class; and
6. independently enumerates all \(K_5\) and independent five-sets in every
   retained representative.

The raw bindings are:

| objective | labeled records | stream SHA-256 | representatives | representative SHA-256 |
|---:|---:|---|---:|---|
| 3 | 16,082 | `e592a201aa862c62ed98fdb7a3442665fe625f44da8b4586f6fd759580426c58` | 9 | `0f9485a82ecb6dba9b19ea0759ba37ef7c9bc64d481cf8fd7a248480b348471d` |
| 4 | 73,788 | `62baebe26a52f34b677ef6f6b1b07a21bc1e19a44a8f20ff9939d82c751a9f04` | 44 | `2ea9964afed1205884e971fb50fce77d783925804ae9d1064460e7b89190bca4` |

The independently reconstructed class distributions are:

| objective | ordinary class sizes | complement-class sizes |
|---:|---|---|
| 3 | \(43^1,86^8,903^1,1806^8\) | \(946^1,1892^8\) |
| 4 | \(43^{10},86^{34},903^{10},1806^{34}\) | \(946^{10},1892^{34}\) |

Here an exponent is the number of classes having the indicated size. The
ordinary partition digests are
`fc5b0d8930e2bab9aef75ca53feed008b027f062cf68a2333ddb95e58ebc65a0`
for `E=3` and
`06374d52fe14204b0861501c37c9854aa07ee43192a795568fb10bd8798516d7`
for `E=4`. The complement-partition digests are
`68f1b570c45f5ae99a5ec2cffe111f35fd419a4e3c6966b50272569c5faccf8d`
and
`6aa0c733528ad35fa28ee9ea0e1b0f00b0e28c5f7f209ecddd0dadf81fa23cc2`.

The independent conflict recount reproduces the published representative
splits:

- `E=3`: four `(1 K5, 2 I5)`, one `(2 K5, 1 I5)`, and four
  `(3 K5, 0 I5)`;
- `E=4`: two `(0 K5, 4 I5)`, twenty-three `(2 K5, 2 I5)`, and nineteen
  `(4 K5, 0 I5)`.

## Exact first-edge schedule audit

For every representative, the checker independently enumerates its current
conflicts and their edge union. It then evaluates all 903 graph edges.

- An edge outside the conflict union cannot destroy a current conflict, so
  toggling it leaves the prior conflict-edge closure operator.
- A conflict-union edge is scheduled exactly when its exact post-toggle
  objective exceeds four.
- An otherwise eligible edge is omitted only if its post-toggle objective
  exceeds the configured ceiling 80.

The resulting exact counts are:

| source | seeds | non-conflict barriers | high conflict-union barriers | scheduled | remains in prior closure |
|---:|---:|---:|---:|---:|---:|
| `E=3` | 9 | 7,911 | 189 | 8,100 | 27 |
| `E=4` | 44 | 38,314 | 1,261 | 39,575 | 157 |
| total | 53 | 46,225 | 1,450 | 47,675 | 184 |

These categories partition all \(53\cdot903=47,859\) seed-edge pairs.
Scheduled heights range from 4 through 47. Therefore:

```text
eligible edges excluded by ceiling 80: 0
```

The checker also performs 206 direct post-toggle conflict re-enumerations,
covering extrema and fixed controls across every representative. The full
independently computed height histogram agrees entry-for-entry with the
production result.

## Frozen source, binary, and run binding

The source used for the completed run is retained at Git commit
`5677276e8135daec5af9fb09e360ec9b8a8dfe79`, path
`ramsey55/src/search43_e2_barrier_escape.cpp`, with SHA-256
`cdddaef4c35dfb9ccdbcc7478029c15eb909247714ffc2bef9e8fa636fb0099c`.

The checker extracts that immutable source and rebuilds it with the frozen
flags

```text
-std=c++20 -O3 -DNDEBUG -Wall -Wextra -pedantic
```

The rebuilt executable has SHA-256
`e145c90c00a6ba7058c58e0ee184ebb3bc8c6292f21c7231161422972cad4b69`,
exactly the binary hash frozen before production. The current working source
and binary have since advanced for follow-up work and are deliberately not
misidentified as the completed-run executable.

The frozen plan has SHA-256
`ebbe4ce7d5a6b9027651fe0e1d2ca70b729eda5545b6f84a44e3c5291ec8cac7`.
The completed result has SHA-256
`ce9e17cae63f40dde390cc960fbd1865156cf923f2615f8f5c36d4fac3fba993`.
The independent checker binds both input representative hashes, the frozen
source and rebuilt binary, every schedule count, all configured parameters,
and the discovery stream.

## Completed heuristic outcome

The production run performed one 256-step tabu repair per scheduled first
edge:

```text
forced barriers and exact forced replays: 47,675
repair steps:                            2,080,964
best objective:                          2
E=1 visits:                              0
E=0 found:                               false
unique returned E=2 endpoints:           1,670
```

The endpoint stream has SHA-256
`ba35df48ba6577605135fda1c893283b76420724bd9ff70b4c0641427ec96e97`.
The independent checker recounts all 1,670 endpoints to exactly two
conflicts. Every endpoint is a same-colour conflict pair with four shared
vertices.

An independent Traces pass gives four ordinary endpoint classes and two
classes modulo complement, of sizes 819 and 851. Both complement classes
match the two already-known `E=2` classes; there is no novel class. This
agrees with the separate published discovery audit, SHA-256
`fae8b82dd05df36cfc353848fb0c1ebd3f049c8975b3e02bf237d2a0ea06f2b1`.

The endpoint result is an observational negative: it found neither an
`E=1` near-construction nor an `E=0` Ramsey graph. It supplies no
nonexistence evidence.

## Design review

No omission invalidates the frozen run or its stated heuristic scope. Three
controls are important:

1. The frozen code counted but did not preserve an `E=1` state. This had no
   effect on this run because `E1_visits=0`, and the follow-up source now
   retains such a state immediately.
2. The search JSON does not contain source, binary, input, and output hashes
   internally. The independent checker in this checkpoint supplies the
   required fail-closed external binding.
3. One representative per complement-isomorphism class is exact for the
   structural first-edge schedule. A single randomized repair trajectory is
   not exhaustive modulo isomorphism or complement, because conflict order
   and random choices can change under relabeling or complementation. The
   frozen plan correctly labels the repair phase heuristic, so a negative
   outcome cannot support nonexistence.

## Retained independent audit

```text
checker:
verify/e2_low_closure_partition_independent_check.py
SHA-256 302a30ced1c7ad772c4f25710efc995541fd3e66e33c74f8743ad9f136df1c41

tests:
tests/e2_low_closure_partition_independent_tests.py
SHA-256 b73c6032bb4a56aff8ace7e1ad4af7f414bd05072036ba46628a0ce3c117856a

result:
results/verification/e2_low_closure_partition_independent_v1.json
SHA-256 38f70c21e61a2c381d7dfbba94441d988505f50536997f47503825c24eaaa9e7
valid true; errors []
```

Seven focused tests pass. They cover independent graph6/complement
round-tripping, exact conflict enumeration, post-toggle objective recounts,
Traces verbose-partition parsing, and complement-class representative
binding.
