# Exact cost-two extensions of order-42 catalog lines 42 and 256

Date: 2026-07-23 (America/Los_Angeles)

## Certified result

**CERTIFIED, FIXED-CORE SCOPE.** For each labeled order-42 Ramsey graph on
catalog line 42 or line 256:

1. the minimum possible number of forbidden five-sets after adding one
   vertex is exactly two; and
2. exactly two of the \(2^{42}\) possible new-vertex neighborhoods attain
   that minimum.

For each core, one optimal neighborhood produces exactly two five-cliques
and the other produces exactly two independent five-sets. The two bitstrings
differ in one adjacency.

This is an exact classification of one-vertex extensions of these two fixed
cores. It is not a classification of arbitrary order-43 graphs and does not
change a Ramsey bound.

## The four neighborhoods

Bits are ordered by adjacency from the new vertex 42 to core vertices 0
through 41.

### Catalog line 42

```text
111111111011010000110000001110010111100000
```

produces two five-cliques:

```text
{10,11,13,28,42}
{11,13,18,28,42}
```

The second neighborhood,

```text
111111111011000000110000001110010111100000
```

produces two independent five-sets:

```text
{9,13,24,32,42}
{13,23,24,32,42}
```

### Catalog line 256

```text
111111111000010111001000011111101000000000
```

produces two five-cliques:

```text
{13,16,26,27,42}
{15,16,26,27,42}
```

The second neighborhood,

```text
111111111000010111001000010111101000000000
```

produces two independent five-sets:

```text
{10,12,26,34,42}
{10,23,26,34,42}
```

Canonical labeling identifies the two clique-conflict extensions of the two
cores with each other, and likewise identifies the two
independent-conflict extensions. These are exactly the two ordinary
near-miss classes that dominate the 22-candidate corpus; the corpus's third
ordinary class is the complement of the clique-conflict class.

## Encoding equivalence

There are 42 primary variables, one for each possible edge from the new
vertex to the fixed core.

Every core \(K_4\) gives a negative four-literal clause: violating it
completes a \(K_5\) with the new vertex. Every core independent four-set
gives a positive four-literal clause: violating it completes an independent
five-set. The core itself is independently verified Ramsey(5,5;42), so these
are all possible forbidden five-sets in an extension.

For each extension clause \(C=(l_1\lor\cdots\lor l_4)\), a fresh variable
\(r_C\) is defined by

\[
 (C\lor r_C)\ \land\
 \bigwedge_{i=1}^4(\lnot r_C\lor\lnot l_i).
\]

Thus \(r_C\) is true if and only if all four literals of \(C\) are false,
exactly when that forbidden five-set occurs. A forward sequential threshold
counter enforces \(\sum_C r_C\le2\).

Finally, one 42-literal clause blocks each recorded neighborhood. Therefore:

- before the two blocks, models are exactly extensions with at most two
  conflicts;
- each recorded neighborhood is independently checked to have exactly two
  conflicts; and
- UNSAT after both blocks proves no third such neighborhood exists.

It follows simultaneously that the optimum is two and that the two listed
neighborhoods are the complete optimum set.

## Formula and proof records

| core line | variables | clauses | CNF SHA-256 | Glucose conflicts |
|---:|---:|---:|---|---:|
| 42 | 9,311 | 25,492 | `7cbe0a232d3f6d4e1589229161780e85bb125f1150ed367360a582c2ec3a7521` | 5,419 |
| 256 | 9,363 | 25,635 | `5320d4a265a17099ef9edca1d8b55634429265dfbf37737ba4aadd8ee7766127` | 6,479 |

For both formulas, the independent checker:

- reconstructed every core \(K_4\) and independent four-set;
- reconstructed every definition, counter, and blocking clause;
- matched the DIMACS and metadata counts and hashes;
- directly checked that the core has no forbidden five-set; and
- directly checked each recorded full order-43 graph and its two conflicts.

Glucose3 then returned UNSAT. `drat-trim` accepted both DRAT traces and
converted them to LRAT; `lrat-check` accepted both LRAT proofs.

| core line | DRAT bytes | DRAT SHA-256 | LRAT bytes | LRAT SHA-256 |
|---:|---:|---|---:|---|
| 42 | 435,560 | `92eb542bc9cce47dd0db40334416a057b013d20f31c085e6ba12420a7494c119` | 39,087,178 | `0003e1b0cd965f9c3d739b7fb06fa989242109c8765fbc3cfe625590a338f3af` |
| 256 | 514,759 | `033185af3c4d6207100ed9b41c5453856f5037481e688551d7462a90276c1845` | 44,287,367 | `d84c203204b072f6ea3cf37dfe522b9f557cd203b9d57c90799b4c254bbd2cfe` |

Solver-result SHA-256 values:

```text
line 42
8ff7553b053457c9b95e84b83c4daf12ec453e6a7f6cd506705eccd85faac6ca

line 256
7d62e16595fad292f6dc4dace6011ac851926cf94eabe54b2ecd13f7545fd2b9
```

## Fail-closed checker recovery

The first independent checker run returned `valid: false` before any proof
was attempted. Its comparison omitted the newly added vertex when matching
a violated four-vertex extension constraint to the corresponding
five-vertex full-graph conflict.

The formula generator was unaffected. The checker was repaired to include
vertex 42, a regression assertion was added, both immutable formulas were
rechecked from scratch, and a second plan was frozen before proof
production. No result from the failed check was used.

The proof-production plan SHA-256 is:

```text
04f920c50c04c92a26e7aed02c5f332eee2c914675e30e6dd4d3504fad6f28ee
```
