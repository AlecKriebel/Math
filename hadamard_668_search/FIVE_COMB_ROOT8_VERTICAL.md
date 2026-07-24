# Primitive-eight vertical-pair sieve for the five-comb construction

## Status

The vertical-pair slice of the distinct-lobe five-comb construction now has
an exact primitive-eighth-root filter.  It extends the retained
`Phi_1/Phi_2/Phi_4` join by splitting the primitive-eight spectral norm into
its rational and `sqrt(2)` coefficients.

Two structural projective cores have been retained so far:

```text
core   Phi_1/Phi_2/Phi_4 survivors   Phi_8 survivors   new rejection
   4                         724,564           140,007         584,557
  27                         229,408            65,868         163,540
```

The new stage removes `80.6771%` and `71.2878%`, respectively, of the
previous survivors.  Cumulatively, the dyadic roots reject 628,505 of all
768,512 inventories at core 4 and 702,644 at core 27.

This is an exact obstruction only for the explicitly delimited
vertical-pair placement.  The physical high-lag table is still projected
independently onto its even and odd halves, so rejection is sound but
survival is a relaxation.  No arbitrary-placement exclusion, base sequence,
or Hadamard matrix is claimed.

Every formula and count is replayed by
`verify_five_comb_root8_vertical.py`.  Focused arithmetic and catalog tests
are in `test_five_comb_root8_vertical.py`.

## 1. Primitive-eight coefficient split

Let

```text
zeta = exp(pi*i/4) = (1+i)/sqrt(2).
```

After separating the even and odd translation groups, each completed
four-row evaluation has the form

```text
E + zeta O,                 E,O in Z[i]^4.
```

For one row, write `E=a+ib` and `O=c+id`.  Then

```text
|E+zeta O|^2
 = |E|^2+|O|^2
   + sqrt(2) Re((1-i) E conjugate(O)).
```

Consequently the exact base-sequence norm at this root is equivalent to two
integer equations:

```text
sum_r (|E_r|^2+|O_r|^2) = 334,

sum_r [a_r(c_r-d_r)+b_r(c_r+d_r)] = 0.          (1)
```

The second line is the vanishing `sqrt(2)` coefficient.  The checker
exhausts 625 small Gaussian fixtures and verifies both Galois embeddings.

## 2. Exact paired-carrier amplitude

For one directed pair of normalized length-five words, put

```text
p = P(-1),        q = Q(-1).
```

Its two carrier polarizations occupy physical translations `g` and `g+20`.
If their inherited row orientations are `U,L in {+1,-1}` and the upper
polarization is `epsilon`, direct reduction modulo `zeta^4=-1` gives the
paired amplitude before the common factor `zeta^g`:

```text
p(U-L) + i epsilon q(U+L).                       (2)
```

This is checked independently by expanding every monomial of all 256
directed word pairs, both polarizations, and all four orientation choices:
2,048 exact carrier checks.

Groups 0 and 2 combine as

```text
E = G_0 + i G_2,
```

while groups 1 and 3 combine as

```text
zeta O = zeta(G_1+iG_3).
```

The fourteen holes are evaluated from their physical positions
`40,41,82,83`.  Their exact split is

```text
E_holes =
 ((h0, eta), (h0, eta), (h8,-eta), (h8,-eta)),

O_holes =
 ((h1,tail), (h1,-tail), (h9,0), (h12,0)),
```

where each pair is a Gaussian `(real,imag)` coordinate.  The verifier checks
all 512 row/hole evaluations directly from their exponents modulo eight.

## 3. Refined finite inventory

The earlier roots needed only the feature

```text
(P(1), Q(1), terminal(Q)).
```

The primitive-eight stage refines it to

```text
(P(1), Q(1), terminal(Q), P(-1), Q(-1)).
```

Exact enumeration gives

```text
feature values                         108
valid directed-pair inventories    768,512
refined feature multisets            87,695.
```

The inventory source digest is checked against the retained canonical
directed-pair hash.  Collapsing the refined classes back to the four old
root-amplitude profiles reproduces their exact multiplicities.

## 4. Retained core censuses

The physical projective labels, orientations, endpoint gauges, and holes are
reconstructed from the exact high-lag boundary table.  The join imposes, in
order:

1. the roots `+1` and `-1` midpoint equations;
2. the Gaussian norm 334 at `i`;
3. the rational primitive-eight equation in (1);
4. the irrational primitive-eight equation in (1).

The resulting survivor rows are

```text
core   (profile 0, profile 1, profile 2, profile 3)
   4   (        0,     12,307,    101,157,     26,543)
  27   (        0,          0,     65,868,          0).
```

The exact feature-pair relations have SHA-256

```text
core 4:
7fd0597c2f7b75bcc604b99bca759e54487f2d53a61fb7a37d0c5d95e42f96f3

core 27:
4de8ebc0c28d8d11abc475dcacfecea0baa0b63a098415af8875cc2d2dd9f11c
```

The survivor-table hashes are

```text
core 4:
1533a8d7b698104efdf9a02610e6d96150d7f43b7afbf68df6f91cf23a6135e4

core 27:
0be791f30d80f710b6e7a49740a0b7e1890364037eaf5a3ad049f0e975802f59
```

The core-27 reference run used 247.62 seconds and 2,822,684,672 bytes maximum
resident memory.  Core 4, whose intermediate relation is much larger, used
1,669.01 seconds and 3,866,116,096 bytes maximum resident memory.  Both
recorded zero swaps.  Their larger peak virtual footprints were
4,242,886,016 and 6,046,405,240 bytes, still safely below the 16 GB
physical-memory limit.

## 5. Scope and next step

The result proves neither retained core feasible nor that any survivor
extends through the full aperiodic equations.  It proves only that the
discarded inventories cannot work in the vertical-pair slice.

The next exact tasks are:

1. replay the same `Phi_8` join on the remaining 29 structural cores;
2. retain the full compatible high-lag row rather than the current
   even/odd projection for survivors;
3. add the final `Phi_16` coefficient equations;
4. pass only surviving labelled inventories to the all-lag base-sequence
   verifier and, on exact success, to the `668 x 668` matrix gate.

Run either retained core:

```sh
python3 verify_five_comb_root8_vertical.py --cores 4
python3 verify_five_comb_root8_vertical.py --cores 27
python3 -m unittest -v test_five_comb_root8_vertical.py
```

The verifier's default `--cores all` performs the complete 31-core census.
