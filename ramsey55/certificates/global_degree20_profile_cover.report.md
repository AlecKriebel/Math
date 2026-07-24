# Exact degree-profile covers for the global degree-20 branch

Date: 2026-07-23 (America/Los_Angeles)

## Outcome and claim boundary

Two independently checked symmetry reductions were constructed for the
degree-20 case of the global order-43 formula:

1. a 253-way exact cover by sorted degree multiplicities, with a compact
   selector-union CNF; and
2. an alternative single formula that makes the existing edge counters exact
   and sorts whole-graph degrees independently inside the root's neighbour and
   antineighbour sides.

Both are **CERTIFIED ENCODING/DECOMPOSITION** results only. A 50,000-conflict
selector-union pilot and a 32-profile, 5,000-conflict-per-profile screen both
exhausted every budget. They found no SAT model and produced no UNSAT proof.
No profile, global branch, or Ramsey-number value is excluded.

## The 253-profile cover

In the normalized minmax-degree-20 case every vertex has degree 20, 21, or
22. Let

\[
  (a,b,c)=(n_{20},n_{21},n_{22}).
\]

The number of odd-degree vertices is even, so \(b\) is even. Since
\(a+b+c=43\), the sum \(a+c\) is odd and therefore \(a\ne c\).
Complementation swaps \(a\) and \(c\) and fixes \(b\), so exactly one member
of each complement pair has \(a>c\). Relabeling vertices into nondecreasing
degree order then gives one canonical labeled degree assignment for each
triple.

An independent enumeration considered all 506 nonnegative triples satisfying
the sum and parity equations. It found no complement-fixed triple and exactly
253 canonical representatives with \(a>c\). Every admissible triple or its
complement maps to exactly one representative.

### Exact degree units

The direct CNF contains forward sequential threshold counters for both the 42
incident edges and the 42 incident nonedges of every vertex. A false final
threshold is semantically one-way safe: if the actual count reached that
threshold, the forward clauses would force the threshold variable true.

For vertex \(v\), the profile cube therefore forces:

| intended degree | false edge threshold | false nonedge threshold |
|---:|---:|---:|
| 20 | 21 | 23 |
| 21 | 22 | 22 |
| 22 | 23 | 21 |

Each profile fixes all 43 exact degrees with 86 distinct negative units. The
independent checker reconstructed the direct counter layout without importing
the production generator and matched every profile's unit stream.

### Compact selector union

The union uses one fresh selector for each profile, one 253-literal
at-least-one clause, and 86 selector implications per profile:

- 65,656 variables;
- 2,073,891 clauses;
- 21,759 appended clauses;
- 90,658,060 bytes when materialized;
- union CNF SHA-256
  `ed76ec38bddd848cde9cc681c3b7c5ed18a4bde668e3d899a6a50a8fc7cc964b`;
- appended clause-stream SHA-256
  `af49472054e4c309709ea987e5908f1d1bb2eb6d4017c81baa722cfa0949891b`.

The materialized file was independently streamed against all 2,052,132 base
clauses and all 21,759 reconstructed additions. Every clause, count, byte
count, and hash matched. The temporary CNF need not be retained; the generator,
metadata, expected hash, and checker reproduce it.

## Alternative side-wise degree ordering

The original counters are forward-only, so their auxiliary values are not
generally usable as truthful symmetry predicates. The alternative encoding
adds 62,694 reverse recurrence clauses to all 43 edge counters. Together with
the existing forward clauses, these make every prefix threshold exact.

After minimum-degree normalization fixes the root star, vertices can be
relabelled independently within the root's neighbour and antineighbour sides.
Requiring nondecreasing whole-graph degrees inside each side is therefore
lossless. It adds 240, 160, and 80 ordering implications in branches 18, 19,
and 20 respectively, with no new variables.

The independent checker separately allocated all 65,403 original variables,
reconstructed every reverse and ordering clause, exhaustively checked small
counter semantics, and matched the materialized degree-20 formula
clause-for-clause:

- 65,403 variables;
- 2,115,034 clauses;
- CNF SHA-256
  `e5b54bb0f5ceb383f8276852d4e6f285c64c079256d2ea405f53df11828c5956`.

Five focused tests pass for the current checker/generator pair.

## Proof-free pilots

The compact 253-selector union was run with MapleChrono for 50,000 conflicts:

- status `BUDGET_EXHAUSTED`;
- 50,000 conflicts;
- 115,126 decisions;
- 35,973,671 propagations;
- 7.307947 solver CPU seconds;
- 1,337,311,232-byte peak RSS.

A persistent CaDiCaL 1.9.5 screen then tested the 32 profiles nearest the
normalized degree profile \((20,10,13)\) of a retained \(E=2\) near-miss.
Every profile exhausted its 5,000-conflict budget:

- 32/253 scheduled profiles completed;
- 160,015 total conflicts;
- 117.482028 wall seconds;
- no SAT model;
- no solver-UNSAT outcome;
- schedule SHA-256
  `99beecd308d4f787532ebd7a55ec98407a31feac9168fccef7bd1a773b213831`.

These runs measure hardness only. The remaining 221 profiles were not
screened, and budget exhaustion has no negative force.

## Reproducibility bindings

- profile generator:
  `src/global_degree20_profile_cover.py`
- independent checker:
  `verify/global_degree20_profile_cover_check.py`
- focused tests:
  `tests/global_degree20_profile_cover_tests.py`
- frozen profile plan SHA-256:
  `ad2ae74430f3e979dc711fe35a852bc84bfd431aa9a92ec10bf11f613c50edc7`
- independent plan-check result SHA-256:
  `db43a3e8f416e720fe04d009628cfb4e7222a8698f5a858d969a8175f21c2064`
- materialized-union check SHA-256:
  `175fff9f64affd2ea3d262cb41cb1200a0a2ef0586a805d0d80f49461889ee35`
- selector-union pilot result SHA-256:
  `53e7d662ee720ea884ecd42f9b380fc61129556d84e7c58c77765632dfe4935c`
- 32-profile screen result SHA-256:
  `287ff92fadcccfcb4ba57e11953c97d33f6e269d77d1b46e7611ec30a8092eda`
- side-order plan SHA-256:
  `1efe811dffb02b412ae8abb02dae0637f890352f114c541c7acc6008c559e523`
- side-order plan-check result SHA-256:
  `4bbb6516eecf062fa1ba5ad24f752b571390e6a45c6445bdc00d0c409ccedaa5`
- side-order materialized check SHA-256:
  `bab000f97f451d868d2b8eddbdcacaa0f8ce392ecb955a36f32d71c4cceeb7a6`

Four profile-cover tests and five side-order tests pass.
