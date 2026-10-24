# Finite-search report for Kourovka 21.130

Checkpoint: 2026-10-24. Overall discovery estimate: **20%**. The universal arbitrary-subset conjecture remains unresolved. This work produced exact bounded confirmations and an elementary structured construction; neither is claimed novel. The separate priority investigation reports historical bounded checks below 30, so these computations must not be presented as the first small-case evidence.

## Strongest exact computational statements

1. For **every** odd-order abelian group of order at most 15 and every subset of size greater than two, a rainbow cyclic enumeration exists. The models checked were C3, C5, C7, C9, C3², C11, C13, C15. Their 22,028 zero-containing subsets all have certificates. Translation covers every other subset: subtracting a from all vertices subtracts 2a from each edge sum. The trivial group contributes no eligible subset.
2. For C3³ and C5², **every** subset of cardinality 3 through 7 has such an enumeration. Their exhaustive zero-containing domains have 313,885 and 190,026 members respectively. Translation again covers remaining subsets of these sizes.
3. A separate larger experiment has **4,294** checked successful witnesses among 4,311 attempted group-subset pairs. This is a listed sample, not an exhaustive assertion about all larger subsets. Exact totals: C3³ 806/806, C5² 513/513, C3×C9 810/810, C7² 431/431, C3⁴ 861/861, C5³ 873/890. Seventeen C5³ samples remain UNKNOWN.

There are **530,233** successful certificate rows and **530,155 distinct group-subset pairs**; 78 larger samples overlap the exhaustive cardinality domains. Bounded checking does not prove the universal claim and supplies no counterexample.

## Certificates and verification

Each JSONL file starts with a group/domain header, then gives subset masks and complete vertex cycles. For factors (m1,...,md), integer IDs use mixed-radix coordinates, first coordinate least significant. A mask has bit x set exactly when x belongs to its subset. Every stored cycle begins with 0; its final edge returns to 0.

- `exhaustive_order15/`: eight exhaustive small-group domains, search statistics, and verification report.
- `exhaustive_sizes7/`: both exhaustive cardinality domains, search statistics, and verification report.
- `larger_samples/`: successful sample certificates, original history (`summary.json`), rescue history (`rescue_summary.json`), final status (`final_summary.json`), and verification report.
- `CERTIFICATE_MANIFEST.json` and `SHA256SUMS`: all 16 certificate files, byte counts, and SHA-256 hashes.

`verify.py` is a standalone **nonsearch** checker. It imports no search code or addition tables. It decodes modular coordinates, checks each cycle is exactly a permutation of its stated subset, computes every adjacent sum including closure, and checks distinctness. Exhaustive coverage follows from checking all expected masks, or equivalent per-cardinality counts with unique valid masks. All saved certificates passed. Root separately checked the order≤15 certificates using tuple arithmetic; a parent-level independent audit of the cardinality≤7 certificates is ongoing.

The complete DFS fixes vertex 0 and discards reversal duplicates by requiring the second ID smaller than the last. It rejects only used vertices or colors. The positive bounded statements require trusting only the witness checks, not the DFS's completeness. Small-group generation took about 5.825 seconds; larger cardinality generation about 3.006 seconds; checking the latter about 3 seconds. Exact group counts and elapsed times are saved.

The larger generator uses seed 211302026 plus group index and four uniform samples per cardinality. It also includes whole groups, every single nonzero omission, every pair of nonzero omissions for order≤27, all initial coordinate boxes, coordinate-prefix subgroup coset unions (all if quotient order≤9, sampled otherwise), and centrally symmetric samples. Duplicate masks are merged. Initial local search allows at most 5 restarts × 30,000 2-opt proposals; rescue allows at most 3 restarts × 10,000 conflict-focused swap proposals. Failure is UNKNOWN. Exact translations, natural whole-group cycles, and product lifts subsequently resolved many stalls.

## Structured mathematical partial

`PRODUCT_LIFTING.md` proves a shared-edge fiber construction. If row indices R⊆H have a rainbow cycle, and fibers B_h⊆G have rainbow cycles containing one common edge {u,v}, cut that edge and concatenate the u→v paths in R-order. Internal colors have different second coordinates 2h and avoid first color u+v; joins have that first color and distinct second colors. This implies Cartesian-product closure for admissible subsets.

Explicit whole/punctured cycles sharing an edge in C5 and C3² give the family (G×H) minus ({0}×D), for arbitrary D⊆H and odd abelian H, with G=C5 or C3². Affine changes of coordinates cover complements in affine hyperplanes of F5^d or in affine subspaces of codimension at least two in F3^d. In particular, every complement of at most three points in F5³ and F3⁴ is covered. `product_constructions.py` constructs exact witnesses and affine maps; `verify.py` then checks the cycles.

The boundary is explicit: prescribed-edge cycles need not exist. In C5, {0,1,2,4} has no rainbow cycle containing {0,1}; both such undirected cycles repeat color 1. Assuming common-edge cycles for arbitrary fibers would transfer the central difficulty. No novelty is asserted for these elementary constructions.

## Remaining heuristic UNKNOWN cases

All 17 lie in C5³ and have complements of full affine rank three, of sizes 4 through 9. They are **not counterexamples**. Coordinates encode x+5y+25z. The table below lists the omitted IDs B, with A=C5³ minus B. Search budgets, categories, exact masks, and best deficiencies are preserved in `larger_samples/final_summary.json`.

| Size of A | Omitted IDs B | Mask of A |
|---:|:---|---:|
| 121 | 48, 75, 89, 120 | 41206067868713384261443184299102699519 |
| 121 | 77, 96, 108, 117 | 42368817767862221392090277468224618495 |
| 121 | 65, 83, 90, 109 | 42534646826762379596732474161213997055 |
| 121 | 76, 77, 103, 108 | 42534961205358621006768653056354549759 |
| 120 | 51, 70, 89, 92, 123 | 31901471893267249592313285692457222143 |
| 120 | 16, 52, 55, 110, 118 | 42201690791956445257748209143172235263 |
| 120 | 13, 57, 75, 111, 113 | 42522315122970933084774521542910402559 |
| 120 | 29, 35, 44, 47, 66 | 42535295865117307859134691269561810943 |
| 119 | 2, 6, 7, 23, 67, 119 | 41870681867224849848895969809146052411 |
| 119 | 6, 39, 56, 69, 72, 114 | 42514526677683163309673352571509538751 |
| 119 | 13, 41, 51, 59, 83, 92 | 42535295860155876368644673044836507647 |
| 119 | 11, 19, 55, 57, 68, 69 | 42535295865117307047297966405817202687 |
| 118 | 5, 33, 47, 73, 96, 107, 117 | 42368980027139192276448014389513027551 |
| 118 | 13, 14, 21, 24, 57, 58, 98 | 42535295548204657875432129990548758527 |
| 117 | 14, 15, 39, 55, 69, 77, 105, 119 | 41870641302405490987069782970200965119 |
| 117 | 4, 13, 65, 84, 86, 99, 103, 108 | 42534960571436833463782471569577598959 |
| 116 | 12, 15, 39, 40, 41, 47, 58, 83, 107 | 42535133605830807312713142355632287743 |

## Reproduction

Run from this folder with Python 3.14; only standard-library modules are needed:

```sh
python3 search.py --output exhaustive_order15
python3 exhaustive_sizes.py
python3 larger_samples.py --output larger_samples --random-per-size 4
python3 rescue_samples.py
python3 product_constructions.py
python3 verify.py exhaustive_order15/*.jsonl exhaustive_sizes7/*.jsonl larger_samples/*.jsonl --report combined_verification.json
```

All scripts use finite budgets. All processes started for this checkpoint completed; no live process handles remain. Rerunning overwrites matching generated outputs. The current final certificate hashes are in the manifests. Timestamps and timing fields change between runs; seeded witness generation is deterministic for the same implementation and Python random behavior. This computational subagent performed no external communication or Git operation.
