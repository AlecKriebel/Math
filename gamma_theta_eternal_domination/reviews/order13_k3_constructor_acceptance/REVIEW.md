# Final acceptance of the order-13, parameter-three constructor

**Audit date:** 2026-07-26  
**Constructor A:** `src/search/order13_k3/`  
**Independent constructor B:** `reviews/order13_k3_constructor_independent/`  
**Solver use:** none.

## Verdict

**`ACCEPT_CONSTRUCTOR_A_FOR_PROOF_PRODUCTION_INPUTS`**

Constructor A is accepted as the deterministic source of the four
order-13, \(k=3\) proof-production inputs.  This acceptance covers formula
construction, exact package generation, exhaustive package audit, and
creation of a `READY_NOT_RUN` metadata plan.  It does not accept a solver
runner, proof conversion, proof checking, an UNSAT result, or a four-branch
finite exclusion.

Every new constructor source, focused test, gate census, and README was
bound by SHA-256 and remained unchanged from the beginning to the end of the
audit.  The warnings-fatal focused suite passed all seven tests.

## Cross-implementation agreement

Fresh constructor-A packages were generated for all four templates and
audited in exhaustive mode.  Each package contained exactly:

```text
instance.cnf
coloring-bank.json
constructor-manifest.json
```

The generated DIMACS streams were then compared byte for byte with fresh
constructor-B streams:

| template | variables | clauses | literals | bytes | SHA-256 | A/B |
|---|---:|---:|---:|---:|---|---|
| `hole5` | 9,802 | 40,726 | 493,820 | 1,805,539 | `8df56270...d2fb5` | identical |
| `hole7` | 9,802 | 34,903 | 349,248 | 1,372,338 | `3e1c86cc...6c340` | identical |
| `hole9` | 9,802 | 32,108 | 281,028 | 1,168,197 | `3fff100c...e95e9ea` | identical |
| `hole11` | 9,802 | 30,853 | 250,664 | 1,076,723 | `1ab880e6...e901` | identical |

Agreement was also checked below the whole-file hash.  Constructor B's
independent semantic tags were mapped to constructor A's fourteen named
clause families.  For every family in every template, the family name,
clause count, literal count, and ordered header-free DIMACS stream SHA-256
agree exactly.  This checks, among other families:

- no-\(K_4\);
- pair common-neighbor choices and implications;
- induced-hole, hub-free, and named-common-neighbor clauses;
- connectedness cuts;
- domination clauses;
- nonempty eternal family;
- one-guard adjacency, successor, and attack-response clauses;
- forced maximum-independent states; and
- the complete coloring obstruction bank.

## Template and coloring coverage inside each formula

For `holeℓ`, the positive unit clauses contain the H-triangle
\(\{0,1,\ell\}\).  It is therefore the fixed independent triple of \(G\)
recorded in the manifest.  No unrelated anchor or heuristic symmetry
breaker is listed or present.

The installed coloring banks were compared with a third local
restricted-growth enumeration, distinct from constructor A and from
constructor B's retained evidence.  Their exact sizes and hashes are:

| template | rows | bank SHA-256 |
|---|---:|---|
| `hole5` | 10,935 | `b9a92c64...2f89e` |
| `hole7` | 5,103 | `efafa89d...e692d` |
| `hole9` | 2,295 | `a0f47a0a...872f1` |
| `hole11` | 1,023 | `b28be0de...82146` |

For each branch, the independently enumerated bank also satisfies

\[
  6|B_\ell|=(2^\ell-2)3^{12-\ell},
\]

the exact labeled-coloring count.  Thus the color-name quotient is complete,
not a heuristic restriction.

## Census, source, and package checks

The live warnings-fatal `census` output has SHA-256
`cf60c939...fb0ce`.  The retained compact census has SHA-256
`abab7510...bcd1d` and agrees with the live census and constructor B on all
formula and coloring-bank fields.

Each generated manifest binds the four runtime sources by hash and aggregate
source-set hash, records CPython 3.14.6, records the exact H-complement
semantics and fixed independent triple, and has an empty heuristic-breaker
list.  Production defaults are seed zero, one solver process, 1,800 seconds,
2 GiB solver memory, 2 GiB proof-file ceiling, 8 GiB disk reserve, and 2 GiB
memory reserve.

The exact constructor-A file bindings are retained in `evidence.json`.  The
principal source hashes are:

| file | SHA-256 |
|---|---|
| `encoding.py` | `da06a797...e1d47d` |
| `generate.py` | `35c78ecc...bf1d0` |
| focused test | `39e585b6...04d5` |
| compact census | `abab7510...bcd1d` |

## READY_NOT_RUN planner

The planner was exercised with a harmless executable whose only purpose was
to reveal accidental execution.  It was not executed.  The plan directory
contained exactly the frozen instance, `run-plan.json`, and
`checkpoint-000000.json`; no attempt directory was created.

The independent acceptance checker verified:

- status `READY_NOT_RUN`;
- empty attempt ledger and sequence zero;
- exact plan-hash binding in checkpoint zero;
- exact instance and future-tool hashes;
- exact future command, seed, and output paths;
- Apple arm64, ten logical CPUs, and 16 GiB physical memory metadata;
- positive free-disk and finite load-average metadata;
- the stated wall, memory, proof-file, disk-reserve, and single-process
  limits; and
- a 2 GiB planned solver ceiling below 75% of physical memory.

This is only a plan.  Constructor A contains no execution/resume auditor, so
the future runner must revalidate every field and enforce every resource
limit before launching a process.

## Fail-closed mutations

Constructor A's package audit rejected mutations of:

- a runtime-source binding;
- the DIMACS formula;
- the manifest census;
- the coloring bank; and
- package exclusivity via an extra file.

The independent retained-census validator rejected a changed clause count.
The independent planner validator rejected changes to:

- `READY_NOT_RUN` status;
- solver memory;
- future solver argv;
- physical-memory metadata; and
- checkpoint plan hash.

All eleven mutations were rejected.  The source bindings were rechecked
afterward and were unchanged.

## Replay

From the campaign directory:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=error \
  python3 -W error \
  reviews/order13_k3_constructor_acceptance/audit.py |
  cmp - reviews/order13_k3_constructor_acceptance/evidence.json
```

On the campaign MacBook the replay takes about fifteen seconds, peaks below
120 MB RSS, creates only temporary packages under `results/`, and invokes no
SAT solver.

The frozen acceptance artifacts are:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `audit.py` | 37,091 | `cd421fb8...21d0a6` |
| `evidence.json` | 7,248 | `8318d036...15ec74` |

## Exact remaining claim boundary

This acceptance permits the first proof-producing run to use constructor A's
exact package bytes.  It does **not** make an UNSAT claim.  A certified
template exclusion still requires a resource-enforcing runner, retained
proof, proof conversion if needed, and independent proof replay against the
exact accepted CNF.  A certified order-13, \(k=3\) exclusion additionally
requires all four accepted branches and the separate mathematical coverage
theorem.
