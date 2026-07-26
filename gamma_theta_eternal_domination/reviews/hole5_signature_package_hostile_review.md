# Hostile audit of the retained `hole5` signature package

## Verdict

**ACCEPT as exact, source-bound formula infrastructure.**

The retained package
`results/synthesis_k3_hole5_signature_package/` is byte-for-byte the frozen
complete `hole5` coloring-bank CNF with its DIMACS header updated and the
independently proved 315-clause signature-order suffix appended.

This acceptance is not a SAT or UNSAT result.  The package manifest explicitly
records `production_solve_gate.enabled=false` and
`claim_status=NO_MATHEMATICAL_CLAIM`; this audit does not alter either field
and launched no solver.

Review date: 2026-07-25 PDT.

## Independent audit artifacts

The package audit was performed by
`reviews/hole5_signature_package_hostile_probe.py`, SHA-256

`ddf75d62dda73779cca880d2c3ec60ee00b91d5f1110ffa84426678a8ef32cc9`.

It uses only the Python standard library and imports neither the author
signature-breaker module nor any synthesis or search code.  Its canonical,
deterministic output is
`reviews/hole5_signature_package_hostile_probe_log.json`, SHA-256

`58edf995b84de703c466e956f47d50443de025fa8b5c5268d781f8962a39d694`.

The exact audit command was:

```text
python3 reviews/hole5_signature_package_hostile_probe.py \
  --output reviews/hole5_signature_package_hostile_probe_log.json
```

Repeated stdout-only executions produced the same log hash.

## Filesystem and package binding

The package contains exactly three entries.  Every path component is a real
directory rather than a symbolic link; every artifact is a regular file with
link count one.

| artifact | bytes | SHA-256 |
|---|---:|---|
| `instance.cnf` | 754,323 | `c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104` |
| `signature_breaker.json` | 38,296 | `62ce8f60ecfe74f58bcd113166009637f854d7d663aea2e59395ae224682d18a` |
| `manifest.json` | 5,530 | `da33bc1708f7d21b92ceedc68710d5433a1aacbe6e32b8a7432bbab45d8cc788` |

The directory has mode `0700`; each file has mode `0644`.  The sorted
three-file tree has 798,149 bytes and SHA-256

`dd9ac46fb91efb1efdbb318b4434619d46389aed5256050f5fb04cb787331542`

under the recorded length-delimited relative-path/payload convention.

The frozen source package also contains exactly its expected three regular,
single-link artifacts:

| source artifact | bytes | SHA-256 |
|---|---:|---|
| complete-bank `instance.cnf` | 742,899 | `76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7` |
| `coloring_bank.json` | 335,343 | `b3c24db61e7a33c3d8803e2bbadcdda92b950fb04445e59e7930330e92b74a00` |
| source `manifest.json` | 3,079 | `99a56197074ad3373691578527e41baff4d76eb1e86141366c4edf8bc5871402` |

No source or retained-package byte was changed.

## Independent CNF reconstruction

The auditor reconstructed edge variables without consulting the author
module:

\[
e_{uv}=1,2,\ldots,66
\]

in lexicographic order on the pairs
\(\binom{\{0,\ldots,11\}}2\).  Consequently, the six signature coordinates
for vertex 6 are variables

\[
(6,16,25,33,40,46),
\]

and the corresponding rows for vertices 7 through 11 were independently
reproduced exactly.

For each adjacent pair
\[
(6,7),(7,8),(8,9),(9,10),(10,11)
\]
and each possible first differing coordinate and common prefix, the auditor
constructed the clause forbidding the first difference \(1,0\).  This gave:

- 63 clauses and 642 literals per comparator;
- 315 clauses and 3,210 literals total;
- clause-length distribution
  \(2:5,4:10,6:20,8:40,10:80,12:160\); and
- an 11,424-byte canonical DIMACS suffix with SHA-256
  `ddd32969558030c22b7b4f182dfd9f96b65bb572a7e240957d202fb32b0158c6`.

All \(5\cdot64^2=20{,}480\) ordered signature pairs were reevaluated.  Each
comparator accepted exactly 2,080 nondecreasing pairs and rejected exactly
2,016 decreasing pairs, with zero mismatches.  Every one of its 63 clauses
had a unique forbidden-pair witness.

The retained `signature_breaker.json` is canonical JSON and is byte-identical
to the independently constructed object, including clause order, literal
order, signature-variable rows, counts, and metadata.

The source CNF parsed strictly as:

```text
p cnf 6886 23653
```

with 188,959 literals.  The derived CNF parsed strictly as:

```text
p cnf 6886 23968
```

with 192,169 literals.  After their respective headers, the first 23,653
derived clause lines are byte-for-byte the complete source body.  The
remaining bytes are exactly the independently reconstructed 315-clause
stream.  Equivalently,

```text
derived CNF
= updated header
+ exact source clause body
+ exact independent breaker stream.
```

This reconstructs the complete derived file byte-for-byte and yields the
required SHA-256
`c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104`.

As a separate order-insensitive anchor, sorting every source clause and then
sorting the full clause multiset gives header-free stream SHA-256
`201496666b255837ff7692ce13ef058f867a11ea7404d571429b7bf0589b1b78`,
matching the covariance record.

## Exact manifest and Git audit

The package manifest was not merely spot-checked.  The auditor independently
constructed the entire expected nested object and required byte equality
with its canonical JSON serialization.  This rejects missing or extra keys,
wrong types, reordered runtime rows, path substitutions, count changes, and
any altered source, suffix, artifact, symmetry, or no-claim field.

The manifest records generation commit

`126071c723b8b9e4276f962b40a89f3049e6b5a5`.

At audit time, both `HEAD` and `origin/main` were that commit.  Each of the
six runtime rows was checked in two independent locations:

1. its current regular worktree file; and
2. `git show` of the exact recorded object at the generation commit.

All twelve hash comparisons matched.  The independently recomputed runtime
source-set SHA-256 is

`770b9f8c7cfa1814716ce6d8b601e514313fb4dd7e95cd8dfefb6c58df25bdd6`.

Thus `runtime_sources_match_head=true`, the empty mismatch list, the recorded
campaign-relative path, and `global_worktree_cleanliness_required=false`
are accurate.

## Independent S6 replay

The previously accepted mathematical probe remained:

- source SHA-256
  `3515adc846e961738b86c572a90aa0f42945cfa6794e3700986c392999c4ab66`;
- retained output SHA-256
  `f1d8f6d8d6f85bdffadcf39e5d4c4504b9cf0d1b8a609d8e5fe540523091b9de`.

The package auditor launched that probe as a separate process without
importing it.  It exited zero, emitted empty stderr, and reproduced the
retained output byte-for-byte.  This rechecks the five full 6,886-variable
covariance generators, all comparator truth tables, complete-bank binding,
and the hostile counterexamples to unsound symmetry shortcuts.

## Exact claim boundary and next gate

Accepted:

- the retained package has complete and exact source coverage;
- its symmetry clauses encode the accepted six-signature ordering;
- its strengthened CNF is equisatisfiable with the frozen complete `hole5`
  CNF by the separately accepted S6 theorem; and
- it is suitable as an immutable input to a separately gated
  proof-producing run.

Not accepted:

- a production solve launched directly from this disabled package;
- SAT or UNSAT for the strengthened CNF;
- exclusion of the `hole5` branch;
- completion of the \((n,k)=(12,3)\) slice; or
- resolution of the universal gamma--theta conjecture.

Before any solve, a separate run configuration must bind this exact package,
the pinned solver and checker, the independently accepted binary-DRAT intake
pipeline, resource limits, commands, and new output paths.  A solver terminal
alone remains `NO_MATHEMATICAL_CLAIM`; only a retained, independently replayed
proof can promote the finite result.
