# Exact triage of the open Eliahou long-block cases

## Result

This folder gives a mechanically checked structural and cost
classification of canonical long cases 1 through 20.  It runs no
production support census and proves neither infeasibility nor existence
of a Hadamard matrix.

The short-block 39-pair engine does **not** generalize.  The long cases
have 57--59 characteristic-two syndrome classes, quotient dimension
36--38, no nontrivial within-case spatial reflection, and a
characteristic-three fixed-quotient graph of worst treewidth 18.

There is, however, one useful new exact fact:

> After a characteristic-two quotient is fixed, the next 2-adic digit
> (the normalized residual divided by two, modulo two) has no interaction
> between ordinary reflected-pair orientation variables.

Thus the conditioned mod-4 lift has treewidth zero in the seventeen
ordinary cases, treewidth one in case 6, and treewidth two in cases 1 and
14.  Globally it is an exact system of twenty quadratic Boolean equations
on 57 affine coordinates.  Its outer-quotient quadratic graph is dense,
so this does not turn into a small linear outer filter.

An exact quadratic-Walsh census evaluates all `2^20` linear combinations
of those forms in all twenty open cases.  The number of common zeros in
the 57-dimensional **odd-weight** affine domain is always extremely close
to `2^37`; the mod-4 layer removes essentially twenty generic bits but
hides no low-rank collapse.  Exact weight 39 is not imposed in this Walsh
census.

The search gate therefore fails on this 16 GB machine.  The mod-4
linearization is worth preserving as the next mathematical tool, but none
of the audited complete engines is projected below two hours and 8 GB.

## Indexing correction

The authoritative ordering is:

- canonical case 0 is `L0`, has 79 variables, and is already
  proof-certified UNSAT upstream;
- canonical case 1 is `L2`, has 78 variables, and remains open because its
  prior UNSAT result has no checked proof;
- cases 2 through 20 are the nineteen other open long cases requested for
  this audit.

The verifier checks this explicitly so the 79-variable boundary case
cannot be confused with open `L2`.

## Characteristic-two quotient

All open cases have 78 variables, split 39 long and 39 short.  Equal
columns of the twenty mod-2 residual equations give:

| cases | syndrome classes | class sizes | quotient rank | dimension |
|---|---:|---|---:|---:|
| 2--5, 7--13, 15--20 | 59 | 40 singletons, 19 pairs | 21 | 38 |
| 6 | 58 | 39 singletons, 18 pairs, 1 mixed triple | 21 | 37 |
| 1, 14 | 57 | 38 singletons, 17 pairs, 2 mixed triples | 21 | 36 |

In every case the projection onto the nineteen nontrivial-class parities
has rank 19, so all `2^19` such parity profiles occur.  The mixed classes
are listed exactly in `LONG_BLOCK_EXACT_TRIAGE.json`.

The verifier also computes the exact number of weight-39 supports in each
twenty-equation mod-2 slice using a complete `2^20` MacWilliams character
sum.  Counts lie between

```text
25,941,786,928,610,200
25,969,427,805,618,032
```

so the affine layer alone remains enormous.

## Conditioned characteristic-three graph

Treat each nontrivial syndrome class as one categorical orientation
variable after its parity is fixed.  Mixed differences of the exact
quadratic potentials modulo three prove:

- ordinary cases: `K_a disjoint-union K_(19-a)`;
- case 6: `K_1 join (K_a disjoint-union K_(18-a))`;
- cases 1 and 14:
  `K_2 join (K_a disjoint-union K_(17-a))`.

Every parity profile occurs, so the exact treewidth ranges are 9--18 in
the first two families and 10--18 in the two-triple family.  A
fixed-quotient separator/MITM is exact, but there are too many quotients.

Using the independently measured short-kernel rate of
`67,122,352.0968` rows/second only as a calibration:

| family | rigorous component-row lower bound | calibrated lower time | gross all-quotient time |
|---|---:|---:|---:|
| ordinary | about `7.60e13` | about 315 h | 5,044 h |
| case 6 | about `1.01e14` | about 420 h | 6,725 h |
| cases 1, 14 | about `1.52e14` | about 630 h | 8,966 h |

The row lower bounds are rigorous.  The time conversions are projections
from a different certified kernel, not production measurements.

## No free reflection gauge

For each long case the verifier enumerates every blockwise cell-dihedral
map `j -> +/-j+a (mod 42)` that preserves the support domain, then checks
the full constant, linear, and quadratic integer residual tensors.

The long domain admits only the identity.  The short domain also admits
`j -> 40-j`, but that map does not preserve the complete long-case
polynomial.  Hence only the identity survives and the free short-case
reflection gauge is absent.

## The next 2-adic digit

On a fixed mod-2 quotient every normalized residual is even.  Dividing by
two and reducing modulo two yields the next digit.  Exhaustive mixed
differences give:

| cases | conditioned graph | exact treewidth |
|---|---|---:|
| ordinary | independent 19-set | 0 |
| 6 | `K_1 join independent_18` | 1 |
| 1, 14 | `K_2 join independent_17` | 2 |

This is a theorem for every quotient, not a sample.

The orientation-aware affine parameterization has 57 coordinates in every
case: 36--38 outer quotient coordinates and 19--21 inner orientation
coordinates.  Substitution gives exactly twenty quadratic ANFs.  Degree
two is exact: XOR-affine substitution modulo four truncates at degree two,
and every original quadratic cross coefficient is even.  In every case:

- the twenty quadratic coefficient rows have rank 20;
- their outer-only quadratic coefficient rows also have rank 20;
- the outer union graph has 93.6%--100% of all possible edges.

Thus orientation elimination is low-treewidth locally, but its
rank/augmented-rank compatibility condition is a dense quadratic condition
on the outer quotient.  It can be encoded directly as 21 affine XOR
constraints plus 20 quadratic XOR constraints with shared AND variables;
enumerating `2^36`--`2^38` quotients is unnecessary.

The bounded rank controls in the certificate are deliberately labeled as
samples.  They show strong inconsistency and high internal ranks, but their
frequencies are not whole-quotient claims.

## Exact all-case mod-4 Walsh census

For quadratic Boolean forms `F_1,...,F_20` on 57 variables,

```text
# common zeros =
  2^-20 sum_(lambda in F_2^20)
    sum_x (-1)^(lambda_1 F_1(x)+...+lambda_20 F_20(x)).
```

The inner sum is obtained exactly from the polar rank, radical-linear
compatibility, and Arf sign of one quadratic form.  A bit-packed C++ kernel
therefore evaluates the complete `2^20` pencil without enumerating the
`2^57` affine points.

Across the twenty cases:

```text
minimum common zeros: 137,273,561,088   (case 17, L28)
maximum common zeros: 137,458,540,544   (case 6,  L1)
reference 2^37:        137,438,953,472
```

The effective reduction is 19.998--20.002 bits.  Minimum nonzero polar
ranks are 20, 22, or 24; there is no low-rank pencil anomaly.  Complete
rank histograms, zero-Walsh counts, signed character sums, model hashes,
and exact common-zero counts are in `MOD4_WALSH_CENSUS.json`.

Again, the affine model enforces odd weight only.  These are exact mod-4
relaxation counts, not weight-39 counts.

## Global long/short meet in the middle

The residual polynomial is exactly additive across the long and short row
blocks; all cross-block quadratic coefficients vanish.  Enumerating one
39-bit block therefore costs `2^39` states and a case costs
`2^40 = 1,099,511,627,776` raw states.

Arithmetic reuse gives:

- 26 distinct block specifications across all 30 canonical cases;
- 18 distinct specifications for requested cases 2--20;
- 19 distinct specifications for all open long cases 1--20.

The open-long raw front end is

```text
19 * 2^39 = 10,445,360,463,872 states.
```

A packed `(weight, mod-6 signature, support mask)` record needs at least
16 bytes, so one `2^39` table needs at least 8 TiB.  A straightforward
20-int16 exact record needs about 24 TiB.  Two frozen `2^20` subcube
controls are 100% and 99.9990% distinct even at the weaker mod-6 key,
supporting the expectation that compression is negligible.

Splitting each block `20+19` gives small half lists (about 144 MiB total at
48 bytes/record for both blocks), but does not create an additive four-sum:
the within-block norm has bilinear cross terms.  Natural balanced cuts have
361--362 nonzero interactions out of 380 possible, so combining the halves
still needs `2^39` pair products per block and an unsolved global join.

## Characteristic seven and exact CRT

Over `F_7`,

```text
z^42+1 = (z^6+1)^7,
z^6+1 = (z^2+1)(z^2+2)(z^2+4).
```

The seven residual Hasse layers have cumulative ranks

```text
3, 6, 9, 12, 15, 18, 20,
```

and every new residual direction remains quadratic in the Boolean support.
The three irreducible quadratic factors give the corresponding `F_49`
local decomposition.  Since `334 = 5 (mod 7)` is a unit, there is no
singular target branch.  The unrestricted two-polynomial local count is

```text
336 * 117600 * 7^54.
```

This has codimension 21 in 84 `F_7` coefficients: triangularity repackages
the norm equations but supplies no extra contraction before the Boolean
alphabet is imposed.

Every normalized residual has absolute value at most 83.  Therefore
moduli 3, 4, and 7 have lcm 84 and jointly force exact zero.  The
`exact_crt84` SAT encoding is logically equivalent to the exact integer
PB encoding.

A 10,000-conflict CaDiCaL comparison on cases 1, 2, 6, and 14 found all
sixteen bounded runs UNKNOWN:

| encoding | solve-time range |
|---|---:|
| mod 2+3 | 0.63--1.18 s |
| mod 2+3+4 | 1.60--2.48 s |
| exact CRT 2+3+4+7 | 3.14--5.42 s |
| exact integer PB | 4.04--5.85 s |

The CRT model is smaller in variables but larger in clauses than PB.  At
this cap it gives no conflict/time advantage.  This benchmark is not
evidence of SAT or UNSAT.

Modulus 42 alone is not exact: it leaves residuals `0,+/-42`.  Spectral
nonnegativity does not close that gap.  The verifier gives the explicit
nonzero pattern

```text
r_(2j) = 42 (-1)^j,   r_(odd) = 0,
```

whose exact norm spectrum is 166 at forty negacyclic roots and 3694 at
the other two.

## Verification

From the repository root:

```text
PYTHONDONTWRITEBYTECODE=1 \
  /Users/alec/Documents/tmp/hadamard-env/bin/python \
  hadamard_668_search/eliahou_long_block_exact_triage/verify_all_artifacts.py
```

Add `--rerun-sat` to repeat the sixteen empirical 10,000-conflict solver
controls as well as rebuilding their CNFs.

The detached verifier:

1. rebuilds all twenty exact quadratic models from the authoritative case
   definitions;
2. recomputes every quotient, graph, MacWilliams count, reflection audit,
   ANF hash, characteristic-seven rank, and bounded control;
3. recompiles and reruns all twenty complete Walsh pencils;
4. rebuilds and hashes every SAT CNF;
5. compares all semantic certificates.

The completed detached replay returned `PASS` in 98.66 seconds wall time
(`97.09` seconds measured internally) at 222,412,800 bytes maximum RSS.
Its semantic certificate hashes were:

```text
triage: 3a430fbf02b3c2102d66f1dcee8c03ea68f5ae66232c560df241224a69e5f325
Walsh:  c6e3f7c4e1a8458edd286ff6e550c9d7e367221a2f1989c6550fee7838c52e46
SAT:    f9a54d53a105207323d938f3e43cc644bea21be8339939e2b6d2c3fa390d6ffa
```

`SHA256SUMS` records the byte-level hashes of every delivered artifact.

No external contact, commit, push, or production search is performed.
