# Independent bounded preflight: live order-13, k=3, hole9 package

## Verdict

**`ACCEPT_LIVE_HOLE9_PACKAGE_PREFLIGHT`**

The live package is byte-identical to a private reconstruction from committed
HEAD
`20eca759c2b0919366c2355d859e62a0933542dd`, to the independent clean-room
constructor's DIMACS stream, and to the `hole9` record in the frozen
constructor-acceptance evidence.

No formula or package discrepancy was found.

This is a constructor-input preflight only.  No SAT solver was launched, no
SAT or UNSAT result was obtained, and no template or finite slice is
excluded.

## Reviewed live package

The package `instances/order13_k3_hole9` contains exactly three regular,
single-link files:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `instance.cnf` | 1,168,197 | `3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea` |
| `coloring-bank.json` | 227,208 | `a0f47a0aaa3be4659ce483f27a963d351f3a13424cac6a6a99ef6ac9e0c872f1` |
| `constructor-manifest.json` | 5,408 | `8f55019121df7280368528c1b7c0808d3cc06e7bd0f871be516057763c87ad5b` |

The total artifact size is 1,400,813 bytes.

For a deterministic package-set binding, sort the artifact names and hash
the ASCII records

```text
name SP sha256 SP size_bytes LF
```

The resulting package-set SHA-256 is
`ba05d99b67816c1f1eeac2569b694ec1fc4412a584e95f359452bdfe12eaad6a`.

## Formula census

Independent strict DIMACS parsing gives:

| field | value |
|---|---:|
| variables | 9,802 |
| clauses | 32,108 |
| literals | 281,028 |
| base clauses | 29,813 |
| base literals | 227,028 |
| coloring-obstruction rows | 2,295 |

The manifest records 14 clause families, whose clause and literal totals
agree with the parsed DIMACS.  It fixes the independent triple
\(\{0,1,9\}\) in \(G\), records no heuristic symmetry breaker, and binds
the runtime source set at SHA-256
`6dc5f770c792dfcc3ebaa8dd74485220832005e8c8026b030883356af38fcf64`.

## Private reconstruction and accepted audits

The preflight used a clean `git archive` snapshot of exact HEAD
`20eca759c2b0919366c2355d859e62a0933542dd` under a private temporary
directory.  Within that snapshot:

1. constructor A generated a fresh `hole9` package with the explicit
   validation gate;
2. constructor A's exhaustive package audit returned `accepted: true`,
   `exhaustive_reconstruction: true`, and `solver_launched: false`;
3. constructor B independently emitted the `hole9` DIMACS, which matched
   constructor A byte-for-byte;
4. constructor B's semantic audit recovered the same 9,802 variables,
   29,813 base clauses, 227,028 base literals, 2,295 coloring rows, 32,108
   full clauses, 281,028 full literals, formula size, and formula hash;
5. the independent coloring audit found 2,295 canonical rows, with six
   labeled colorings per orbit and 13,770 labeled rows;
6. the seven warnings-fatal focused constructor tests passed; and
7. the complete frozen constructor-acceptance replay matched its committed
   evidence byte-for-byte.

Finally, each of the three private package files was compared directly with
the corresponding live file.  All three comparisons were byte-identical.
The private directories were then removed.

Operational note: the first attempted location used macOS `/tmp`, which is a
symlink to `/private/tmp`.  The fail-closed generator correctly rejected the
symlinked path component.  Repeating the same operation through the canonical
`/private/tmp` path succeeded.  This is a path-safety behavior, not a package
discrepancy.

## Frozen acceptance comparison

The read-only replay binds
`reviews/order13_k3_constructor_acceptance/evidence.json` at:

- 7,248 bytes;
- SHA-256
  `8318d036867da89c2b2b7b9599bde17f50e160731d21243584609d34a515ec74`.

Its accepted `hole9` record agrees exactly with the live formula, bank,
manifest, fixed triple, exhaustive-constructor audit, clean-room byte
comparison, clause-family stream comparison, coloring coverage, and package
exclusivity.

## Read-only replay

From the campaign directory:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=error \
  python3 -B -W error \
  reviews/order13_k3_hole9_preflight_constructor/audit.py |
  cmp - reviews/order13_k3_hole9_preflight_constructor/evidence.json
```

The checker launches no subprocess and writes no file.  It validates the
live package in place and emits canonical JSON only to standard output.
