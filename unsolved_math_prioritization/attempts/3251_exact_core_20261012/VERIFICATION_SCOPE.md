# Exact finite verification scope

The all-size proofs are distinct from these bounded regressions. Original programs, datasets and execution records are omitted; this is not a standalone exhaustive replay package.

## Family universe

Exactly six specifically labelled constructed family graphs, k=3 through 8, are tested. This is not all graphs of any order. Every core coloring is tested against a separate full-extension search and exact maximum-clique reconstruction.

| k | vertices | edges | core vertices | core colorings | core divisions | extendible divisions | nonextendible divisions | odd subsets inspected |
|---|---|---|---|---|---|---|---|---|
| 3 | 13 | 20 | 5 | 32 | 24 | 22 | 2 | 3,797 |
| 4 | 17 | 36 | 7 | 128 | 112 | 110 | 2 | 64,839 |
| 5 | 21 | 56 | 9 | 512 | 480 | 478 | 2 | 0 |
| 6 | 25 | 80 | 11 | 2,048 | 1,984 | 1,982 | 2 | 0 |
| 7 | 29 | 108 | 13 | 8,192 | 8,064 | 8,062 | 2 | 0 |
| 8 | 33 | 140 | 15 | 32,768 | 32,512 | 32,510 | 2 | 0 |

Total: 43,680 core colorings. Exhaustive odd-subset inspection covers k=3 and k=4 only, 68,636 subsets of odd size at least five. Higher k use elimination certificates and the all-size proof. The independent audit reconstructs adjacency directly, enumerates cliques by increasing-label recursion, and computes the four-clause projection by Davis–Putnam elimination, independently of the author's clique algorithm and depth-first extension oracle. It checks all 43,680 core colorings and the exact case stream. Additional independent enumeration of 8,192 full colorings at k=3 and 131,072 at k=4 totals 139,264; these graphs have respectively 1,458 and 61,250 full divisions.

The family author's final controls reject 42 required mutations per mode, 126 total, with two positive controls per mode. Replays and the independent mathematical outputs agree within each family under normal Python, -O and -OO. The exact k=4 fixture, clique incidences, complete elimination order and two failing core masks are checked.

## Exact-core propagation and tree universe

All 1,078 rank-tagged simple uniform hypergraphs with 3<=r<=n<=5 are included, with empty families distinguished by rank. Every partial coloring whose unassigned vertices have original incidence at most two is checked. All 1,100 labelled simple graphs of orders zero through five are enumerated; the 660 with clique number at least three supply eligible partial colorings.

| n | uniform families | uniform partial cases | graphs of clique number at least three | graph partial cases |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 | 0 |
| 3 | 2 | 54 | 1 | 27 |
| 4 | 18 | 1,285 | 23 | 1,863 |
| 5 | 1,058 | 89,230 | 636 | 147,123 |

Uniform families supply 90,569 cases: 55,235 successes and 35,334 failures. Graphs supply 149,013 cases: 133,611 successes and 15,402 failures. The exact combined case set has 239,582 records and is compared without omissions or duplicates. An independent full-coloring oracle, reverse-order propagation and enumeration of every possible tree subfamily agree on every case. There are 188,846 successes and 50,736 failures; every returned failure certificate is independently checked. The certificate sizes are 50,086 one-node, 510 two-node, 120 three-node and 20 four-node certificates. Graph failures alone have 15,372 one-node and 30 two-node certificates. The successful cases include 3,188 with repeated residual sets.

Abstract paths on 2 through 9 nodes at ranks 3, 4 and 5, and rank-r stars with r leaves, give 54 failed two-color prescriptions and 700 successful one-prescribed-vertex-flip repairs. The independent fixture universe is exactly the same. These are abstract hypergraph fixtures, not claims that every fixture is a graph maximum-clique family. Stars test internal nodes with no prescribed vertices.

The independent audit also checks 1,891 eligible partial colorings of simple nonuniform families with original edge sizes at least three on orders zero through four. Seven malformed certificates are rejected: missing consumer, repeated nodes, unordered nodes, foreign node, empty certificate, wrong signs and two shared outside vertices producing parallel edges. Explicit opposite singleton demands conflict; opposite one-sided demands on repeated residual two-sets are satisfiable. A rank-two triangle and an unprescribed Fano family test the necessity of the excluded rank and core-coverage hypotheses. Arithmetic checks cover both possible core clique numbers for 4<=k<=30, 54 instances.

Both exact-core mathematical replay families agree under normal Python, -O and -OO. The independent hostile suite has 73 mutation scenarios and 143 required program rejections per mode, 429 total. The original author has 56 negative controls per mode. All source/dependency bytes and named evidence members are rechecked. Final review-seal controls additionally reject 54 mutants per mode, 162 total, outside the sealed review. No acceptance gate relies on Python assertions.

## Interpretation and preservation

Each finite count above retains its own original universe. Family cases, general small graphs, abstract hypergraphs, supplementary nonuniform tests and arithmetic checks are not interchangeable universes and are not combined into an all-graphs conjecture claim. Source streams and receipts were matched privately; omitted raw/control/program identities are not public metadata for this edition.

Both complete proofs, both complete acceptances and the complete narrow accepted correction are preserved reversibly. The correction independently compares all 90,569 uniform-family partial cases, all 149,013 graph partial cases, and 1,891 partial cases of 37 nonuniform families. It proves component closure at all sizes; these finite tests are supplemental. Public hashes and byte sizes identify only actual distributed files and the five earlier inspected public PDFs. The publication candidate remains local; no queue integration or remote action is represented by these checks.
