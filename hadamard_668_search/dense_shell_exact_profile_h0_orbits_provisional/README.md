# Three additional exact dense-shell `h=0` profile orbits

## Certified result

Two completed cells of the running exhaustive `h=0` census produced three
previously unrecorded exact profile representatives:

| label | source | target | production digest |
|---|---|---|---|
| provisional orbit 3 | `h0-p00-p07` | `(-3,0,0,3)` | `0xc90c2887b652140a` |
| provisional orbit 4 | `h0-p00-p08` | `(0,3,-4,-2)` | `0x6e45edfb0bfb0974` |
| provisional orbit 5 | `h0-p00-p08` | `(2,-2,-2,2)` | `0x533a4ccf9d6a91d8` |

For each representative, an independent expansion from the twelve
order-three cyclotomic classes to all positions of `F_37` gives, in exact
integer Eisenstein arithmetic,

```text
D_0 = 167,
D_t = 0 for t=1,...,36.
```

Each has shell census `(n9,n3,n0)=(0,18,6)`.  Each is canonical with trivial
stabilizer and orbit size 24 under the exact profile action

```text
C6 x C2(A-star) x C2(B-star).
```

The verifier also reconstructs both earlier exact `h=0` profile orbits.
All ten pairwise orbit intersections among the five representatives are
empty.  Thus these are genuinely three additional profile orbits, rather
than alternate expressions of either earlier point or one another.

“Provisional” refers only to the still-running global census: the three
individual exact-profile and inequivalence checks are complete.  These
objects are compressed profiles, not labelled placements, a Legendre pair
of length 333, or a Hadamard matrix of order 668.

## Independent verification

From the repository root:

```text
python3 \
  hadamard_668_search/dense_shell_exact_profile_h0_orbits_provisional/verify_provisional_h0_orbits.py
```

The verifier is dependency-free and imports no classifier or prior profile
verifier.  It reconstructs:

1. the twelve cyclotomic classes of `F_37^*`;
2. the compressed Eisenstein values and aggregate target;
3. all 37 physical autocorrelation equations directly;
4. shell membership;
5. all 24 group images, stabilizers, lexicographic canonical
   representatives, and orbit hashes;
6. the production digests; and
7. all ten pairwise orbit-intersection tests.

The source-result, production-source, and production-binary hashes are
recorded in `certificate.json`.  The verifier does not depend on the
ignored live census output, so the certificate remains reproducible after
that output is archived or removed.

## Census scope

Cells `h0-p00-p07` and `h0-p00-p08` are complete, but the 729-cell `h=0`
census is not.  No claim is made here about the final number of exact
profile orbits in the shell.  A shell-classification statement requires the
production runner and strict aggregator to finish every cell.
