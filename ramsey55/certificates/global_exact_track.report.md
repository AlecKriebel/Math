# Global exact track: complement/relabel degree branches

Date: 2026-07-23 (America/Los_Angeles)

## Outcome and evidence status

**REPRODUCIBLE COMPUTATIONAL OBSERVATION.** The direct global
`(5,5;43)` CNF was partitioned into four lossless degree branches and each
branch was run with the same 200,000-conflict MapleChrono budget. All four
runs returned `BUDGET_EXHAUSTED`. No model and no UNSAT proof was produced.
The global existence question therefore remains **unresolved**. In
particular, this experiment is not evidence of nonexistence and does not
change any Ramsey bound.

**CERTIFIED artifact check.** For every degree in `{18,19,20,21}`, the
independent streaming checker verified that the materialized branch contains
all 2,052,132 clauses of `certificates/direct_ramsey43.cnf`, in the same
order, followed by exactly the intended 42 unit clauses. It also checked the
DIMACS counts, variable range, metadata, byte count, and base/branch SHA-256
digests. All checks passed.

**CERTIFIED proof-path audit (limited scope).** On the nontrivial UNSAT
formula PHP(4,3), nine PySAT backends produced traces accepted by `drat-trim`;
the resulting LRAT files were then accepted by `lrat-check`. This certifies
the tested integrations on that audit instance. It does not itself certify
any global Ramsey result.

## Exact branch-cover argument

Let `F` be the direct `n=43` CNF. Its primary variables encode a graph, its
Ramsey clauses forbid a clique or independent set of order 5, and its
sequential counters enforce degree range `[18,24]`.

For any satisfying primary graph:

1. Choose a vertex and relabel it as vertex 0.
2. If its degree is greater than 21, complement the graph. The new degree is
   `42-d`. Since `18 <= d <= 24`, the resulting degree is one of
   `18,19,20,21`.
3. Permute vertices 1 through 42 so that the neighbors of vertex 0 are
   precisely vertices 1 through `d`.

Complementation exchanges clique and independent-set clauses, and maps
degree `d` to `42-d`, so both the Ramsey condition and `[18,24]` degree
range are preserved. Relabeling also preserves both properties. The
sequential-counter auxiliary variables need not be transformed
syntactically: for the normalized primary graph, fresh auxiliary witnesses
exist because the counters are complete for every primary assignment
satisfying the bounds.

In the documented lexicographic edge-variable order,
`x_(0,j) = j` for `1 <= j <= 42`. Thus branch `d` appends units

```text
1, 2, ..., d, -(d+1), ..., -42.
```

Every model of a branch is trivially a model of `F`. The normalization above
maps every model of `F` to a model of one of the four branches. Therefore:

```text
F is SAT  iff  branch_18 OR branch_19 OR branch_20 OR branch_21 is SAT.
```

A SAT result in any branch would be a global construction. A global UNSAT
result requires checked UNSAT proofs for **all four** branches. UNSAT of one
branch alone would only eliminate that degree case.

The normalization code was additionally tested on all 33,866 labeled graphs
of orders 2 through 6 and on 100 seeded random graphs of order 43. These tests
support the implementation; the equivalence itself is the argument above.
No stronger or heuristic symmetry restriction was introduced.

## Branch artifacts and bounded results

All branches have 65,403 variables and 2,052,174 clauses. The persistent
metadata and check records allow the approximately 90 MB temporary CNFs to
be regenerated and hash-checked.

| degree | branch CNF SHA-256 | bytes | conflicts observed | decisions | propagations | solver CPU s | status |
|---:|---|---:|---:|---:|---:|---:|---|
| 18 | `0d495823f5e7760dbf9022c1f79582afe919eee2d2b58ab5da79bf14427dabfe` | 90,311,699 | 200,001 | 377,923 | 93,052,916 | 14.106 | budget exhausted |
| 19 | `e7deb814512d467c8b333ca3d15e8b30fac025733716944691420f3406784521` | 90,311,698 | 200,000 | 764,113 | 124,366,433 | 36.742 | budget exhausted |
| 20 | `382a0f00bfa80ba36174a54fb5f25ab6f3a7dfb122d0f66fe41220aea7e78cc6` | 90,311,697 | 200,001 | 413,781 | 109,014,512 | 30.636 | budget exhausted |
| 21 | `ec5afb777d31dc5d0f0c099832a35fcc7279ecedce53180a2a5e42f6990501a8` | 90,311,696 | 200,002 | 461,070 | 115,819,464 | 28.654 | budget exhausted |

The small one-to-two conflict overshoot is the backend's budget-check
granularity. The aggregate observed count was 800,004 conflicts and aggregate
solver CPU time was 110.139 seconds. Wall times and resident memory are in
`results/global_exact/pilot_summary.json`.

## Solver and preprocessing audit

The solver distribution was `python-sat 1.9.dev7`; `MapleChrono` denotes the
bundled MapleLCMDistChronoBT SAT Competition 2018 version. The pinned native
solver module SHA-256 is:

```text
e9828032a114da49429305e5afcf58db259034687a9c098c996da65e5e099ded
```

The proof audit accepted these backends end-to-end on PHP(4,3):

```text
Glucose3, Glucose4, Glucose42, Gluecard3, Gluecard4,
Lingeling, MapleChrono, MapleCM, Maplesat
```

`Cadical103`, `Cadical153`, `Cadical195`, and `Cadical300` were excluded:
their returned traces were not accepted by `drat-trim` in this integration.
An UNSAT status from an excluded backend must not be used without a separate
valid proof path.

Checker pins:

```text
drat-trim SHA-256:
f58f63b0f76945d4c4c9ff6e87afaf870f579e67c0f7cca589492df8fc7ebd47

lrat-check SHA-256:
bd7eb8052623525814a0a37502b47f05375d9d9dfaf96ddc2fcd858958517cea
```

No standalone SAT preprocessor or symmetry breaker was used. A read-only
search found no matching standalone SAT/preprocessing executable in the
repository or standard `/opt/homebrew/bin`, `/usr/local/bin`, and `/usr/bin`
locations. The only preprocessing in scope is backend inprocessing while
proof logging is enabled. Any future UNSAT trace must still pass independent
DRAT and LRAT checking against the exact checked branch CNF.

The branch transformation itself is deliberately transparent: it changes the
header clause count, adds comments, copies every base clause byte-for-byte,
and appends units. The independent checker verifies the semantic content
clause-by-clause rather than trusting the generator.

## Solver selection pilot

Degree 18 was used for a 50,000-conflict comparison:

| backend | observed conflicts | wall s | decisions | propagations |
|---|---:|---:|---:|---:|
| Glucose3 | 208,684 | 19.927 | 292,563 | 67,429,596 |
| MapleChrono | 50,000 | 4.965 | 135,831 | 21,933,525 |
| MapleCM | 50,000 | 28.975 | 140,910 | backend reported 0 |
| Maplesat | 50,000 | 9.033 | 188,274 | backend reported 0 |

MapleChrono was selected because it respected the requested conflict cap and
was fastest in this bounded comparison. This is a **CONJECTURE OR HEURISTIC**
about the useful backend for larger runs, not evidence for SAT or UNSAT.

## Reproduction

The base instance is:

```text
certificates/direct_ramsey43.cnf
SHA-256 141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1
```

With the audited Python/PySAT environment available, regenerate one branch:

```bash
PYTHONPATH=src /opt/homebrew/opt/python@3.11/bin/python3.11 \
  src/global_ramsey_branches.py \
  --base-cnf certificates/direct_ramsey43.cnf \
  --base-metadata certificates/direct_ramsey43.metadata.json \
  --degree 18 \
  --output /tmp/ramsey55_global_d18.cnf \
  --metadata results/global_exact/branch_d18.metadata.json
```

Independently check it:

```bash
/opt/homebrew/opt/python@3.11/bin/python3.11 \
  verify/global_ramsey_branch_check.py \
  --base-cnf certificates/direct_ramsey43.cnf \
  --branch-cnf /tmp/ramsey55_global_d18.cnf \
  --branch-metadata results/global_exact/branch_d18.metadata.json \
  --degree 18 \
  --output results/global_exact/branch_d18.check.json
```

Run the bounded pilot:

```bash
PYTHONPATH=/tmp/ramsey55-pysat.4YSXId:src \
  /opt/homebrew/opt/python@3.11/bin/python3.11 \
  src/global_proof_worker.py \
  /tmp/ramsey55_global_d18.cnf \
  --solver MapleChrono \
  --conflict-budget 200000 \
  --proof /tmp/ramsey55_global_d18_maplechrono_200k.drat \
  --output results/global_exact/pilots/d18_maplechrono_200k.json
```

Repeat with degrees 19, 20, and 21 and matching paths. Exit code 2 denotes
budget exhaustion; it is not an error or an UNSAT result.

Re-run the proof-path audit:

```bash
/opt/homebrew/opt/python@3.11/bin/python3.11 \
  src/proof_solver_audit.py \
  --python /opt/homebrew/opt/python@3.11/bin/python3.11 \
  --pysat-path /tmp/ramsey55-pysat.4YSXId \
  --drat-trim /tmp/ramsey55-drat-trim.x3nb3p/src/drat-trim \
  --lrat-check /tmp/ramsey55-drat-trim.x3nb3p/src/lrat-check \
  --output results/global_exact/proof_solver_audit.json
```

Validate and aggregate all persistent records:

```bash
/opt/homebrew/opt/python@3.11/bin/python3.11 \
  src/global_exact_summary.py \
  --results-dir results/global_exact \
  --output results/global_exact/pilot_summary.json
```

Run implementation tests:

```bash
PYTHONPATH=src /opt/homebrew/opt/python@3.11/bin/python3.11 \
  tests/global_ramsey_branches_tests.py

/opt/homebrew/opt/python@3.11/bin/python3.11 \
  tests/global_ramsey_branch_check_tests.py
```

Six tests pass.

## Persistent artifact index

- `src/global_ramsey_branches.py`: branch generator and normalization tests'
  subject implementation.
- `verify/global_ramsey_branch_check.py`: independent streaming checker.
- `src/global_proof_worker.py`: proof-capable bounded solver worker.
- `src/proof_solver_audit.py`: DRAT-to-LRAT integration audit.
- `src/global_exact_summary.py`: consistency-checked aggregate.
- `tests/global_ramsey_branches_tests.py`
- `tests/global_ramsey_branch_check_tests.py`
- `results/global_exact/branch_d{18,19,20,21}.metadata.json`
- `results/global_exact/branch_d{18,19,20,21}.check.json`
- `results/global_exact/pilots/*.json`
- `results/global_exact/proof_solver_audit.json`
- `results/global_exact/pilot_summary.json`

The temporary materialized CNFs are not certificates and need not be retained;
the deterministic generator, base CNF, expected hashes, and independent
checker reproduce and validate them.
