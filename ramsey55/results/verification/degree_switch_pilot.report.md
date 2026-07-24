# Degree-preserving 2-switch multistart pilot

Date: 2026-07-23 (America/Los_Angeles)

## Outcome

**REPRODUCIBLE COMPUTATIONAL OBSERVATION:** all nine preregistered runs
completed, but none improved on \(E=C_5+I_5=2\). No \(E=1\) or \(E=0\)
graph was found.

```text
starts                                  3
fixed production seeds                 3
completed runs                          9 / 9
accepted degree-preserving moves        162,000
candidate moves evaluated               2,099,473
primitive 2-switch candidates           1,781,819
compound two-switch candidates            317,654
breakout penalty updates                    501
periodic/final full objective audits        657
aggregate search runtime                651.709593 seconds
strict objective improvements           0
positive-Hamming equal-E=2 retentions   0
best E                                  2
```

Every final artifact was the corresponding registered start graph. This means
the bounded trajectories did not encounter an \(E\leq2\) graph at positive
edge-Hamming distance under the registered retention policy. It does **not**
prove that the starts are isolated, locally optimal under all 2-switches, or
that their degree-sequence components contain no Ramsey graph.

| Start basin | Seed | Final \(C_5\) | Final \(I_5\) | Final \(E\) | Search seconds |
|---|---:|---:|---:|---:|---:|
| exoo | 20260801 | 0 | 2 | 2 | 69.287505 |
| exoo | 20260802 | 0 | 2 | 2 | 67.981420 |
| exoo | 20260803 | 0 | 2 | 2 | 67.354901 |
| incident | 20260801 | 2 | 0 | 2 | 67.228158 |
| incident | 20260802 | 2 | 0 | 2 | 78.485528 |
| incident | 20260803 | 2 | 0 | 2 | 75.020657 |
| core-kick | 20260801 | 2 | 0 | 2 | 86.712372 |
| core-kick | 20260802 | 2 | 0 | 2 | 66.108581 |
| core-kick | 20260803 | 2 | 0 | 2 | 73.530471 |

## Search design

A primitive move removes two disjoint present edges and inserts an absent
opposite matching on the same four vertices. Therefore each labeled vertex
keeps exactly the same degree. Moves were biased to remove an edge from a
violating clique or add an edge to a violating independent set. Each step
also sampled global moves and compound moves comprising two edge-disjoint
legal 2-switches.

The selection rule used seeded `mt19937_64`, integer random-walk decisions,
edge tabu, violated-set breakout weights, exact incremental objective deltas,
and periodic full enumeration. Restart zero began at the registered graph;
later restarts began after 24 seeded legal 2-switches.

The plan was frozen before using production seeds:

```text
plan
results/benchmark_plans/degree_switch_multistart_v1.json

plan SHA-256
e28917fd98477625af28bbaf19ed247471f0fb1b0fcc317ca745cb121ca91f43
```

## Validation and retained-artifact checks

Before preregistration, the move kernel passed:

- 100 primitive and 50 compound move checks against full all-5-subset
  objective and weighted-objective recomputation;
- an exact labeled-degree-vector check after every tested move;
- complete rollback checks; and
- duplicate 200-step calibration runs with byte-identical graphs and
  identical semantic JSON.

For every production run, the final retained graph was checked independently
by:

1. direct Python enumeration of every 5-subset and its ten pairs;
2. the separately compiled C++ recursive-bitset graph/complement verifier;
3. a structural audit comparing every labeled degree, balanced added/removed
   incidence, objective, graph6 value, Hamming distance, and search record.

All 27 verifier invocations accepted their registered facts. There were no
strict improvements to audit. The search engine itself checked the exact
labeled degree vector after every accepted move and recomputed the full
objective 657 times.

Had any run reached \(E=0\), the engine would have stopped that run
immediately, the runner would have launched no later search, and canonical
plus adversarial artifact audits would have been required before labeling a
construction certified. That branch was not reached.

## Principal retained hashes

```text
result summary
8d94e6976c4579385ed0c1de3781c5f7bde14877d2b014ab61750de6debbe9e6

search source
ceea9d1a7132c9928d2ce6a15018d2be590bd37bb845e8e33d6ce9aae0ae4bb9

compiled search binary
b7142ba147e44bf0b5d4236729678e4d897c143d1eab2419589bda514246f4db

independent structural checker
572ad6defe5449d92250c0e6661c1ccef740b06d82e3e2791ea4611e0bb01604
```

The nonzero outcome is a bounded search observation only; it supplies no
construction and no nonexistence evidence.
