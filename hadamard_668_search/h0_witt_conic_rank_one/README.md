# Witt-conic rank-one lift obstruction for the `c90c` orbit

## Status

Every normalized local block in the complete exact `h=0` shell has a
uniform finite-geometric description.  Write a row of `Z/9` as

```text
r=s+3q,                     s,q in F_3.
```

If `p(s)` is the prescribed residue profile and `u_s` is the existing
placement trit, put

```text
t_s=-p(s)u_s.
```

Then the local three-subset is exactly

```text
(q-t_s)^2=p(s)-1.                                    (1)
```

For `p=0,1,2`, equation (1) has respectively zero, one, or two points in
the fiber.  Thus it handles all seven profile letters occurring in all 18
exact `h=0` orbits.  On active fibers the center is unique, so (1) is a
lossless change of coordinates rather than an ansatz.

For the priority orbit

```text
c90c2887b652140a
```

the verifier exhausts the structured center laws

```text
t_X(j,s)
  = P_X(x,s,p_X,j(s)) + a_X h_j R(x,s,p_X,j(s)),       (2)

x=j mod 3,
h_j=+1 for j<6 and -1 for j>=6.
```

Here `P_A` and `P_B` are arbitrary total-degree-at-most-two polynomials in
three variables over `F_3`; `R` is a shared nonzero quadratic polynomial,
up to scalar; and `a_A,a_B` are independent channel amplitudes.  Equivalently,
the two opposite-class corrections have coefficient rank at most one.
This is a profile-aware, channel-asymmetric half-turn-breaking family.

The exact census is:

```text
projective nonzero shapes R                       29,524
canonical shape/amplitude affine centers          78,729
base-polynomial coefficient kernel dim.                3
canonical coefficient-space point incidences   2,125,683
canonical physical incidences before dedup.       236,187
distinct physical placements                       65,601
```

After quotienting duplicate coefficient descriptions, the verifier
evaluates every distinct physical placement in the family in all 18 active
second-placement equations.  None survives:

```text
maximum active equations satisfied        16 / 18
exact second-digit survivors                     0
```

This is an exact finite obstruction, not a timeout or a random search.  It
does not exclude the full `c90c` lift space, the order-three Legendre-pair
lane, `LP(333)`, or `H(668)`.

## Why this lane matters

The conic coordinate (1) turns the placement trits into geometric centers
on the non-split two-digit row group `Z/9`.  Family (2) is the first audit
here whose phase law depends simultaneously on:

- the cyclotomic class coordinate;
- the row residue;
- the exact local profile value; and
- an opposite-class correction shared projectively across the channels.

It therefore reaches profile-covariant constructions missed by the earlier
profile-blind affine, helical, and anti-tensor tests.  Its failure says that
any exact `c90c` lift needs either higher-rank opposite corrections or a
nonquadratic dependence on the conic data.

## Verification

From `hadamard_668_search/` run:

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  /Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  h0_witt_conic_rank_one/verify_witt_conic_rank_one.py
```

The verifier:

1. checks that the frozen complete-classification certificate contains
   exactly 18 exact `h=0` orbits;
2. exhausts the local conic/trit identity;
3. reconstructs all 29,524 projective quadratic shapes;
4. eliminates the 20 base-polynomial coefficients exactly over `F_3`;
5. deduplicates the resulting physical placements;
6. evaluates every distinct placement in the exact quadratic second layer;
7. directly replays one deterministic physical point at every attained
   score; and
8. compares the complete semantic result with the pinned JSON certificate.

It is single-core when the displayed environment limits are used and stays
well below 1 GB RAM.  The final reference verification used 2.06 seconds
wall, 1.82 seconds user, 0.03 seconds system, and 98,156,544 bytes maximum
resident memory.  Its semantic hash is

```text
0c68683c63f9116179530430435e9da69728e198b7e5d8a2e63d8d69c8696a3c
```
