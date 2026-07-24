# Delete-three/add-three screen of the two \(E=2\) complement classes

Date: 2026-07-23 (America/Los_Angeles)

## Outcome and claim boundary

**COMPLETE FINITE SCREEN; NO CONSTRUCTION FOUND.** Every labeled triple of
vertices was deleted from each of two certified order-43 \(E=2\) near misses,
and the resulting 40-vertex core was completed by three fully unconstrained
new vertices. The exact terminal ledger is:

| terminal class | count |
|---|---:|
| retained homogeneous five-set: exact fixed-core obstruction | 18,204 |
| solver UNSAT: proof-free observation | 6,478 |
| unresolved limit | 0 |
| independently verified SAT construction | 0 |
| **total labeled triples** | **24,682** |

Thus this replacement neighborhood contains no observed
\((5,5;43)\)-graph. The 18,204 structural obstructions are exact. The 6,478
UNSAT solver answers are reproducible observations, not negative
certificates: no DRAT, LRAT, or other independently replayed UNSAT proof was
generated.

This is a finite search around two fixed near misses. It is **not** a global
nonexistence theorem for order 43, does not determine \(R(5,5)\), and does
not change the bound on \(R(5,5)\).

## Frozen representatives

The two input graph6 records are retained in
`data/e2_complement_class_representatives.g6`. They were copied byte for byte
from models already certified in
`catalog42_lines42_256_exact_e2_extensions.report.md`:

| input | catalog source | selected optimum | conflict colour | conflicts |
|---:|---:|---:|---|---|
| 1 | line 42 | model 0 | clique | \(\{10,11,13,28,42\}\), \(\{11,13,18,28,42\}\) |
| 2 | line 256 | model 1 | independent | \(\{10,12,26,34,42\}\), \(\{10,23,26,34,42\}\) |

This choice takes one clique-conflict and one independent-conflict
representative, spanning the two complement classes identified by the
certified finite-corpus isomorphism audit. Both source graphs were directly
re-enumerated before the plan was frozen: each has exactly two homogeneous
five-sets, of one colour, intersecting in exactly four vertices.

No isomorphism or automorphism deduplication was used. All
\(2\binom{43}{3}=24{,}682\) labeled deletion triples have their own record.

## Exact structural reduction

For either representative, write the two conflicts as
\(C\cup\{a\}\) and \(C\cup\{b\}\), where \(|C|=4\). A retained forbidden
five-set cannot be repaired by changing edges incident to the three new
vertices. Consequently a deletion triple is solver-eligible exactly when it
hits both conflicts.

The independently checked partition for each input is:

| condition after deletion | count |
|---|---:|
| both conflicts retained | \(\binom{37}{3}=7{,}770\) |
| exactly one conflict retained | \(2(\binom{38}{3}-\binom{37}{3})=1{,}332\) |
| neither conflict retained; send to completion solver | \(3{,}239\) |
| **all triples** | **12,341** |

Thus 9,102 triples per input, 18,204 total, are exact fixed-core
obstructions. The remaining 3,239 triples per input give genuine
40-vertex Ramsey cores.

## Completion formula

For each eligible core, the three new vertices have 123 unknown edges:
120 core-to-new edges and their three mutual edges. For every five-set
containing at least one new vertex:

- a negative monotone clause forbids a five-clique whenever the fixed core
  pairs in that five-set are all edges; and
- a positive monotone clause forbids an independent five-set whenever those
  fixed core pairs are all nonedges.

The formulas contain 13,266 through 13,509 clauses. A separate Python
implementation reconstructed formula statistics for eight frozen samples
in the v1 coverage audit. The targeted v2 checker then reconstructed all 117
retry formulas and matched their deterministic formula SHA-256 values,
variable counts, and clause counts.

A SAT assignment would therefore be a genuine \((5,5;43)\)-graph. Both
production runners were fail-fast on SAT and were prepared to preserve:

- the raw model;
- graph6;
- adjacency lists and matrix rows;
- an edge list and degree sequence; and
- results from both the exhaustive five-subset verifier and the independent
  recursive-bitset verifier.

No SAT stop occurred, so no candidate artifact was created.

## Resume-safe production

### v1: all labeled triples

The v1 plan split the two lexicographic triple spaces into 98 atomic shards
of at most 256 triples. A completed shard was promoted by atomic rename and
validated with an independent fixed-width parser. Interrupted partial
shards would be preserved under diagnostics and recomputed, while complete
validated shards would be reused.

The conservative custom-DPLL bounds were 100,000 nodes and 0.5 seconds per
eligible core. The full v1 run took 1,162.611725 seconds, including its
independent coverage audit. The 98 shard invocations account for
1,152.812779 seconds. They produced:

| input | structural obstruction | observed UNSAT | time limit |
|---:|---:|---:|---:|
| line-42 clique representative | 9,102 | 3,155 | 84 |
| line-256 independent representative | 9,102 | 3,206 | 33 |
| **total** | **18,204** | **6,361** | **117** |

No solver record hit the node cap. The 117 limits were retained honestly
and did not support a negative conclusion.

### v2: exact limit retry

After v1 was complete, a second immutable plan extracted exactly its 117
limit records, including the base-shard hashes, and nothing else. Each
target formula was regenerated and sent to pinned PySAT 1.9.dev7
Cadical195 with a 10,000,000-conflict bound and a 60-second worker timeout.

All 117 targets returned UNSAT observations and none returned SAT or LIMIT:

| source input | v1 limits retried | observed UNSAT | remaining limit |
|---:|---:|---:|---:|
| line 42 | 84 | 84 | 0 |
| line 256 | 33 | 33 | 0 |
| **total** | **117** | **117** | **0** |

The v2 invocation, including independent regeneration of all 117 formulas,
took 186.707568 seconds. Production formula generation totaled
75.165075 seconds; Cadical solving totaled 1.406118 seconds and 68,961
conflicts. The hardest retry used 1,074 conflicts and 0.046017 solver
seconds.

Combining v1 and v2 gives exact labeled-triple coverage with 18,204 exact
structural obstructions, 6,478 proof-free UNSAT observations, zero limits,
and zero SAT models.

## Checks and tests

Before each production phase, the plan froze all relevant source, binary,
input, checker, test, and solver-runtime hashes. Focused tests covered:

- certified-model provenance and direct \(E=2\) enumeration;
- the exact 9,102/3,239 structural partition;
- independent clause-count agreement on eligible cores;
- compact-format corruption rejection;
- exact shard coverage and immutable-plan validation;
- exact extraction of all 117 v1 limits;
- independent retry formula hashing; and
- fail-closed behavior for incomplete retry ledgers.

Five focused v1 tests and four focused v2 tests passed before their
respective plans were frozen. The v1 coverage checker inspected every
record's labels and independently recomputed whether its original conflicts
survived. The v2 checker regenerated every retried formula rather than
trusting the worker's formula identity.

## Principal hashes

```text
representative corpus
376fce9067c2d50da09c6eaa5df40b03ce96768bcdc4273fffef93eefc1eea48

v1 frozen plan
edd273371349fe072d027a8118d4982094842df5e8efc221aaf454ea75d32757

v1 result
021ddca560267c5e5c7f4ea2520bba6461abc16f97d632b0b581baea80148a9a

v1 independent coverage audit
e830f3581311006c544195aed014d69d067bf7f243368492d153299c89c27a29

v1 ordered shard bundle
492bcd0ed3a5b2e2a2e7385c0beda60c8d80a865754477707557817eba4486ab

v1 producer binary
a02af711e102aa9817194ed66a004ea99ad2555a814cad3054ef8e69ea5b7589

v2 frozen retry plan
2836f147d3f57258233771a7161c950b2ec0e8c6394fae3baae9ff0e267c2dcc

v2 result
37a1fa28d4744784a753230c92507357d9731ba464dad211d28533843f3678d7

v2 independent check
8cb43be4db0642bb4ed7dc51a0a0997d7e6cfc64c3fca11d35b9d9cd31d6a382

v2 ordered retry-record bundle
fbcfed53ef23065061db4505566cc81ea4743c049c5129e940f09b8efc2e5c6e
```

Pinned Cadical runtime components:

```text
Python 3.11 executable
831365631dac62f232a720858703d0b2ddca5eed33e0a51986cf06aac9d38bc0

pysat/solvers.py
253654d8efabae650a0d136ad2f2e6d30b57206b1fb70846c714197468a28f7e

pysolvers.cpython-311-darwin.so
e9828032a114da49429305e5afcf58db259034687a9c098c996da65e5e099ded
```

## Reproduction entry points

The frozen plans and their outputs are:

```text
results/benchmark_plans/e2_triple_replacement_screen_v1.json
results/constructive/e2_triple_replacement_screen_v1/

results/benchmark_plans/e2_triple_replacement_limit_retry_v2.json
results/constructive/e2_triple_replacement_limit_retry_v2/
```

With the hash-bound dependencies present, the resume-safe entry points are:

```text
python3 src/e2_triple_replacement_screen.py --run
python3 src/e2_triple_replacement_limit_retry.py --run
```

Both commands reuse complete records and fail closed on a hash mismatch,
missing coverage, malformed solver output, verifier failure, disk-reserve
breach, or output-cap breach.
