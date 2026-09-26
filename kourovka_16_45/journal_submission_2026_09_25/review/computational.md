# Independent exact computational review

**Final status: PASS. Computational-review scope 100% complete at 2026-09-26
04:09 UTC (2026-09-25 21:09 PDT). No mathematical or implementation discrepancy
was found.** This is an AI-assisted internal audit, not external peer review or
a proof-assistant formalization. Completion is relative to this finite-check
assignment, not a probability that a journal will accept the paper.

## Independence and audit boundary

The reviewer first read `../../proof.tex` and fixed a mechanism without reading
the supplied verifiers or earlier audit results: raw matrix tuples over finite
fields, Cayley-graph generation of candidate homomorphisms, verification of
every multiplication identity, subgroup generation by adjoining every element,
bitset intersection tests, and direct affine closures and intersections. The
checker `independent_exact.py` was then written from that specification. The
supplied code was inspected only after the independent checker passed. The
implementations share standard mathematical algorithms; separate authorship
here means separately written AI-agent code, not independent human review.

The reviewer additionally enumerated all subgroups of the largest scalar
line group, `F_29 ⋊ C_4`, to test the finite input behind the small affine
lemma. This computation was absent from the supplied verifiers.

The universal upper bounds for all actions of the large affine group are
structural mathematical claims; none of these checks pretends to enumerate
all subgroups of the group of order 100920. Structural proof review is a
separate assignment. Bibliographic novelty and editorial policies are also
outside this audit's scope.

## Results

All computations use exact integer arithmetic and the Python standard library.

| Check | Verified result |
|---|---|
| Displayed complement generators | Determinant one; `A²=B³=(AB)⁵=−I`; generated order 120 |
| Explicit map from `SL₂(5)` | Bijection on all 120 matrices; all 14400 products checked |
| Explicit quotient onto `A₅` | All 60 even permutations; kernel `{I,−I}`; all 14400 products checked |
| Involutions and normal subgroups of `H` | Unique involution `−I`; normal subgroup orders 1, 2, 120 |
| Three displayed `R_i` | Stated words and squares verified; omission subgroup orders 8, 12, 20; product orders 4, 3, 10; triple generates `H` |
| Pair-subgroup intersections and cores | Total intersection `{I,−I}`; each core in `H` exactly `{I,−I}` |
| Complete subgroup lattice of `H` | 76 actual subgroups, not only conjugacy classes |
| Irredundant families in `H` | Rank-one count 75; rank-two 2461; rank-three 900; rank-four 0 |
| Faithful irredundant families in `H` | Rank-one count 1; rank-two 996; rank-three 0; rank-four 0 |
| Coverage of finite upper-bound search | All 1215450 four-families and all 67525 three-families of proper subgroups checked |
| All projective lines over `F_29` | 30 lines; every stabilizer cyclic of order 4 |
| Scalar line group `F_29 ⋊ C_4` | Order 116; 62 actual subgroups; 1711 irredundant pairs; no irredundant triple |
| Affine independent four-set | Generates all 100920 elements; omission subgroup orders 120, 6728, 10092, 16820; every omitted generator excluded |
| Affine four-family | Intersection exactly `Z₀`; deletion-intersection orders 1682, 4, 4, 4; displayed conjugation proves nonnormality |
| Faithful affine three-family | Orders 58, 58, 58; each displayed pair intersection verified element-for-element; total intersection trivial; degree 5220 |
| Core/normality checks | The complement intersects its stated translation conjugate trivially; `V⋊Z` is normal under each group generator |
| Characteristic-11 boundary | Exact displayed `C` lies in the order-120 complement and has order 10; four subgroup orders 110, 110, 242, 605; total intersection trivial; deletion orders 11, 11, 5, 2 |

The subgroup-order distribution for `H` is
`1:1, 2:1, 3:10, 4:15, 5:6, 6:10, 8:5, 10:6, 12:10, 20:6, 24:5, 120:1`.

Enumeration is exhaustive because every subgroup has a generating sequence,
and adjoining every possible next element from every discovered subgroup
traverses every such sequence. The absence of rank-four irredundant families
excludes higher ranks since every subfamily of an irredundant family is
irredundant. The unique rank-one faithful family is the trivial subgroup.

## Replays and cross-comparison

The supplied Python verifier was replayed with a fresh output directory. The
supplied C++ verifier was freshly compiled with C++17, optimization, and warning
flags, then replayed with a fresh output path. Neither the historical outputs
nor the original source files were modified. Both programs exited successfully;
the compiler emitted no warnings. The supplied comparison utility also passed.

A new comparison utility converted all three enumerations to actual matrices:
all 76 subgroup sets agree exactly, regardless of indexing. The SHA-256 digest
of all 100920 sorted affine elements also agrees between the fresh checker and
the supplied Python program. Affine orders, omission orders, action degree,
and the characteristic-11 deletion orders agree.

Evidence is in `../evidence/computational/`:

- `independent_exact.json`: stable exact-check summary.
- `independent_subgroups.json`: all 76 subgroups as actual matrix entries.
- `replay_python/`: fresh supplied-Python certificate and summary.
- `replay_python.log`, `replay_cpp.log`: successful replay outputs.
- `subgroups_cpp.txt`: fresh C++ subgroup export.
- `supplied_comparison.log`: successful supplied comparator.
- `compare_fresh.py`, `fresh_comparison.log`: successful three-way comparison.
- `environment.json`: runtime/compiler versions and SHA-256 of audited inputs.

The C++ executable is scratch data in `../tmp/computational/`; it should not
be uploaded to the journal or committed as a portable verification artifact.

Reproduction from the problem directory:

```sh
python3 journal_submission_2026_09_25/review/independent_exact.py --subgroups-output journal_submission_2026_09_25/evidence/computational/independent_subgroups.json > journal_submission_2026_09_25/evidence/computational/independent_exact.json
python3 src/verify_counterexample.py --outdir journal_submission_2026_09_25/evidence/computational/replay_python > journal_submission_2026_09_25/evidence/computational/replay_python.log
c++ -O2 -std=c++17 -Wall -Wextra -pedantic src/verify_counterexample.cpp -o journal_submission_2026_09_25/tmp/computational/verify_counterexample_cpp
./journal_submission_2026_09_25/tmp/computational/verify_counterexample_cpp journal_submission_2026_09_25/evidence/computational/subgroups_cpp.txt > journal_submission_2026_09_25/evidence/computational/replay_cpp.log
python3 src/compare_certificates.py journal_submission_2026_09_25/evidence/computational/replay_python/finite_certificate.json journal_submission_2026_09_25/evidence/computational/subgroups_cpp.txt > journal_submission_2026_09_25/evidence/computational/supplied_comparison.log
python3 journal_submission_2026_09_25/evidence/computational/compare_fresh.py > journal_submission_2026_09_25/evidence/computational/fresh_comparison.log
```

## Submission supplement recommendation

The mathematical paper can and should stand alone: state that exact programs
corroborate the explicitly specified finite inputs, while the proof of the
all-actions upper bound is in the paper. Avoid making the abstract sound as
though the central proof requires exhaustive enumeration or software trust.

For a concise portable supplement, include a short README giving scope and
commands, `verify_counterexample.py`, `verify_counterexample.cpp`,
`compare_certificates.py`, and the three supplied replay outputs (Python
summary, Python finite certificate, C++ subgroup export). Include the fresh
`independent_exact.py` and its JSON summary if claiming this additional fresh
audit. Include the matching subgroup sidecar and comparison script only if
the supplement describes the three-way comparison. A simple Makefile and
SHA-256 manifest are useful packaging aids.

Exclude compiled binaries, exploratory MILP programs/results, the full audit
history, temporary working files, and duplicate old certificates. Those may
remain in the repository for provenance. Journal policy, the final editorial
choice, and licensing should determine which optional files accompany the
submission. No external communication or commit was performed by this reviewer.

## Checkpoints

- **2026-09-26 04:04 UTC — 10%:** manuscript inputs read; independent mechanism
  fixed before supplied code/history inspection; no discrepancy apparent.
- **2026-09-26 04:07 UTC — 70%:** new exact checker passed, including additional
  scalar-group enumeration; supplied Python replay passed; C++ replay and
  cross-comparison pending.
- **2026-09-26 04:09 UTC — 100%:** supplied Python/C++ replays passed, all three
  complete matrix subgroup sets agreed, full affine-element digest agreed,
  evidence and this report saved. No numerical or mathematical correction
  is required by this audit.
