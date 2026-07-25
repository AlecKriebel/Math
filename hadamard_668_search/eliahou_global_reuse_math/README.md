# Case-26 global reuse: a free reflection gauge

## Result

The complete case-26 characteristic-six census has an exact free
involution that was not used in the first whole-quotient plan.  Spatial
reflection

```text
j -> 40-j
```

preserves the canonical short-hole set `{12,28}`, preserves weight, and
acts on the twenty normalized residuals by

```text
Q_k(reflect(x)) = (-1)^k Q_k(x),    1 <= k <= 20.
```

It therefore preserves both modular and exact zero residuals.

In the 39 reflected syndrome-pair coordinates, write `p_i` for pair
parity and `y_i` for the remaining pair state:

```text
p_i=0: (x_a,x_b)=(y_i,y_i),
p_i=1: (x_a,x_b)=(1-y_i,y_i).
```

Reflection fixes the two central cells `L_20,S_20` and acts on every
noncentral pair by

```text
y_i -> y_i xor p_i.
```

The twenty noncentral long-pair parities form an affine `[20,18]`
binary coset that does **not** contain zero.  Algebraically, the
variation matrix has rank 18, while adjoining the affine offset raises
the rank to 19.  Equivalently, its two dual checks both have syndrome
one.  Hence every one of the `2^18` quotient states has an odd
noncentral long pair.  Reflection is consequently free on every
quotient fiber.

Choose any odd long pair deterministically and impose `y_i=0`.  Every
reflection orbit has exactly one representative in this gauge.

## Exact work reduction

After conditioning the central pair, the existing universal
four-component decomposition contains 20 long and 18 short binary
variables.  The reflection gauge removes one long orientation, leaving
the exact `19+18` split

```text
long table:   2^19 rows,
short table:  2^18 rows.
```

The complete principal join count, including both central values, falls
from

```text
2^18 * 2 * (2^20 + 2^18) = 5 * 2^37
                              = 687,194,767,360
```

to

```text
2^18 * 2 * (2^19 + 2^18) = 3 * 2^37
                              = 412,316,860,416.
```

This saves exactly `2^38 = 274,877,906,944` principal rows, or 40%.
The smaller hash table remains `2^18` entries, so the contraction does
not increase memory.

There are 37 free noncentral variables after gauge fixing.  Any
two-table full-enumeration join has cost

```text
2^a + 2^(37-a),
```

whose minimum occurs at `a=18,19`.  Thus the long/short `19+18` split
attains the exact optimum inside this architecture.  A further
asymptotic improvement must exploit more than repartitioning complete
binary half-tables.

The same free action halves the exact characteristic-two weight-39
slice from

```text
25,941,166,955,843,488
```

supports to

```text
12,970,583,477,921,744
```

reflection representatives.  This is a symmetry quotient, not evidence
that a modular or integer solution exists.

## Why the obvious global reuse schemes stop here

### Walsh/Fourier reuse

Use the eighteen short parities `q` as quotient coordinates.  The long
parities have the affine form

```text
p_L = A q + b,       rank(A)=18,
```

with `A` an `18 x 20` row-map in the convention used by the verifier.
The Fourier expansion of the graph constraint is

```text
1[p_L=Aq+b]
 = 2^-20 sum_lambda (-1)^(lambda.(p_L+Aq+b)).
```

The dual map has a two-dimensional kernel and is onto all `2^18`
quotient characters.  Every frequency occurs, four times.  Thus there
is no sparse Walsh spectrum to cache; an exact transform indexed by
residue and weight densifies across the full quotient.

This rules out the tempting *few-frequency* reuse, not every possible
Fourier algorithm.

### Tensor-network elimination

The short projection is all of `F_2^18`.  For every two short pairs, the
quadratic `y_i y_j` coefficient is nonzero in exactly one adjusted-parity
equality pattern.  Therefore the direct primal graph on the eighteen
quotient bits contains all 153 edges: it is `K_18`, with treewidth 17.
Eliminating quotient bits directly must expose a `2^18` state frontier.

This is a structural explanation for the failure of a narrow
quotient-variable tensor contraction.  It is not a general complexity
lower bound on all encodings.

### Low-rank quadratic forms

At the independently certified pinned quotient, the four component
sizes are `10,10,10,8`.  For each component, the twenty polar coefficient
matrices over `F_3`

- generate the full matrix algebra `M_10(F_3)` or `M_8(F_3)`, and
- have a scalar combination of full rank.

So the forms are neither uniformly low rank nor reducible by a common
fixed invariant-block decomposition, even in this one quotient.  A
single scalar Fourier combination can be diagonalized, but that does
not simultaneously diagonalize the twenty equations; moreover a
general linear change of variables does not preserve the Boolean cube.

## Scope

This is an exact, mechanically checked 40% contraction of the proposed
whole case-26 modular-six census.  The census itself has not been run.
It does not exclude case 26, produce an exact anti-fold support, construct
`BS(84,83)`, or construct `H(668)`.

## Verification

Run:

```sh
/Users/alec/Documents/tmp/hadamard-env/bin/python \
  verify_global_reuse_math.py
```

The verifier checks the exact integer reflection identity coefficient by
coefficient, the free affine-coset action, the work count and two-list
optimality, the full Walsh support, the `K_18` tensor obstruction, and
the four complete pinned coefficient algebras.  It compares the derived
result with `EXPECTED_GLOBAL_REUSE_MATH.json` and verifies the SHA-256
inventory in `ARTIFACT_HASHES.json`.

## Benchmark and claim boundary

A reference verification on 2026-07-24 on the local Apple M1 Pro completed
in 4.76 seconds with `117,489,664` bytes maximum resident set size.  This
is a verifier benchmark, not a production-census throughput measurement.

The `412,316,860,416` figure is an exact count of principal table rows for
the contracted complete census architecture.  Those rows have **not** been
enumerated.  The result is a certified algorithmic contraction and a
boundary audit; it is not a modular survivor census, an integer
infeasibility proof, or a Hadamard construction.
