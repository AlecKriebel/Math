# Certified \(E\le2\) extension census of all 328 supplied order-42 cores

Date: 2026-07-23 (America/Los_Angeles)

## Certified result

**CERTIFIED, FINITE-CATALOG SCOPE.** Among all 328 labeled
\((5,5;42)\)-graphs in `data/r55_42some.g6`, exactly catalog lines 42 and
256 admit a one-vertex extension having at most two monochromatic
five-sets. Every other supplied core has at least three monochromatic
five-sets under every one of its \(2^{42}\) possible new-vertex
neighborhoods.

The complete census returned:

| terminal result | count | catalog lines |
|---|---:|---|
| independently verified SAT model | 2 | 42, 256 |
| independently verified UNSAT DRAT | 326 | every other line |

Combining this census with the separate exact-extension certificates for
lines 42 and 256 gives a sharper statement for this catalog: each of the
two exceptional cores has optimum exactly two and exactly two optimal
neighborhoods. Thus the four neighborhoods recorded in
`catalog42_lines42_256_exact_e2_extensions.report.md` are the complete
\(E\le2\) extension set across the supplied catalog.

This does **not** classify all order-42 Ramsey graphs. The supplied 328
graphs are not asserted to be a complete order-42 catalog, so this result
does not exclude an arbitrary \((5,5;43)\)-graph and does not change the
public Ramsey bound.

## Encoding equivalence

Fix one supplied order-42 core \(H\). The formula has 42 primary variables,
where primary variable \(x_v\) says that the new vertex 42 is adjacent to
core vertex \(v\).

Every \(K_4\) in \(H\) gives a negative four-literal extension clause. Its
violation means that the new vertex completes that \(K_4\) to a \(K_5\).
Every independent four-set in \(H\) gives a positive four-literal extension
clause. Its violation means that the new vertex completes an independent
five-set. An independent recursive-bitset checker first verifies that
\(H\) itself contains neither kind of forbidden five-set.

For each extension clause \(C=(l_1\lor\cdots\lor l_4)\), a fresh variable
\(r_C\) is defined by

\[
 (C\lor r_C)\ \land\
 \bigwedge_{i=1}^4(\lnot r_C\lor\lnot l_i).
\]

Consequently \(r_C\) is true exactly when its associated homogeneous
five-set occurs. A deterministic forward counter then enforces
\(\sum_C r_C\le2\). Therefore the formula is satisfiable exactly when the
fixed core has an extension with at most two monochromatic five-sets.

The independently reconstructed formulas range from 9,227 to 9,363
variables, 25,259 to 25,633 clauses, and 2,297 to 2,331 extension
constraints. Across all 328 lines, the checker matched 8,335,860 clauses
exactly.

## SAT witnesses

The batch did not accept a solver assignment merely because it satisfied
the CNF. It decoded the 42 primary variables into an order-43 graph and
independently enumerated all
\(\binom{43}{5}=962{,}598\) vertex five-sets.

For line 42, Glucose3 returned

```text
111111111011010000110000001110010111100000
```

and the exhaustive graph check found exactly the two five-cliques

```text
{10,11,13,28,42}
{11,13,18,28,42}.
```

For line 256, Glucose3 returned

```text
111111111000010111001000011111101000000000
```

and the exhaustive graph check found exactly the two five-cliques

```text
{13,16,26,27,42}
{15,16,26,27,42}.
```

The complementary-conflict optimum for each core and completeness of the
two-neighborhood list are established by the earlier blocked-enumeration
DRAT/LRAT certificates.

## UNSAT proof bundle

For each of the other 326 lines, pinned PySAT 1.9.dev7 Glucose3 returned
UNSAT and emitted an ASCII DRAT trace. Each trace was immediately checked
against that line's independently reconstructed temporary CNF by pinned
`drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Acceptance required the exact
status line `s VERIFIED`, followed by stable CNF and proof hashes.

Aggregate proof facts:

| item | value |
|---|---:|
| checked DRAT files | 326 |
| total DRAT bytes | 158,998,676 |
| total Glucose conflicts | 2,003,887 |
| total solver wall seconds | 129.107242 |
| end-to-end two-worker wall seconds | 220.961112 |

The per-line formula hash, proof hash, byte count, solver statistics, and
checker result are retained in
`catalog42_e2_extension_proof_batch_v1.result.json`. The proof-bundle digest
is the SHA-256 of the ordered stream
`line_number cnf_sha256 proof_sha256`:

```text
96a2319b3d82decb2d6910c9753a614dabf166ba9734d49207e02200dad77329
```

The 326 individual proofs are retained under
`certificates/catalog42_e2_extension_proofs_v1/`.

## Reproducibility and hashes

The run was frozen before proof production. Its acceptance policy explicitly
treated the earlier proof-free 328-line screen as a hypothesis, permitted
unexpected SAT models, and denied any complete-catalog conclusion after a
timeout or checker failure.

```text
catalog
067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb

frozen plan
a42a254a563e726feaf36c42be2f7789c920894e96146d4f23e747feeb638c29

batch source
463d849577375cb708dc0a6d83ef7f0f809e8752176304b37a480ba3c87b220c

formula generator
faf9dc82bbd749916792f7cd7ecef47e55139cc18f9f2df1772be7c9e748e9c5

independent formula checker
6e6134bedc48606e9d37f8bc617f6d56159fc45dd66e70fbd9a45413eeee908d

result manifest
1534f38464bd55180c60981b019258799512595a984011906b8d49a27eef2355
```

The exact reproducing command is:

```text
python3 src/catalog42_e2_extension_proof_batch.py \
  --catalog data/r55_42some.g6 \
  --proof-dir certificates/catalog42_e2_extension_proofs_v1 \
  --result certificates/catalog42_e2_extension_proof_batch_v1.result.json \
  --expected-count 328 \
  --expected-sha256 067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb \
  --jobs 2 \
  --generate-timeout 60 \
  --solve-timeout 60 \
  --proof-timeout 120
```

Reproduction requires an empty proof directory or a new output path; the
runner fails closed rather than overwriting an existing proof bundle.
