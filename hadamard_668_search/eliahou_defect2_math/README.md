# Case-26 fixed-quotient characteristic-six contraction

This folder contains an exact algebraic contraction around the pinned
case-26 characteristic-two point from
`../eliahou_char3_jet_audit/CASE26_MOD2_BEST_DEFECT2.json`.

## Result

The twenty characteristic-two columns fall into 39 equal-syndrome
reflected pairs.  Freeze the parity of every pair to the parity at the
pinned point.  There are then:

- 23 odd pairs, each with two orientation choices;
- 16 even pairs, each empty or full;
- exactly eight full even pairs, forced by total support weight 39.

This freezes **one** of the `2^18 = 262,144` affine quotient states, not
the complete characteristic-two slice.  Consequently this one quotient
state contains exactly

```
2^23 binom(16,8) = 107,961,384,960
```

weight-39 supports.

The complete fixed-weight characteristic-two slice across all quotient
states has

```
25,941,166,955,843,488
```

supports.  Thus the census here covers one quotient state and leaves
262,143 quotient states untreated.

Substitution of the 39 pair-state bits in the characteristic-three jet
produces a quadratic interaction graph.  The cross-block pair
`{("L",20),("S",20)}` is an articulation variable.  For either value of
that variable, the remaining graph separates into components of sizes
`10, 10, 10, 8`.  The twenty-residue polynomial therefore separates into
four vector-valued component polynomials.  An exact meet in the middle
joins their residue vectors together with the full-even-pair count.

The complete result for this quotient state is:

```
joint normalized mod-6 supports: 62
exact integer supports:           0
minimum nonzero integer lags:    11
minimum integer L1 residual:    114
```

This is the first pinned simultaneous characteristic-two /
characteristic-three survivor in this anti-fold lane.  The certificate
pins the survivor minimizing

```
(nonzero lags, L1, Linf, distance from the old center, support)
```

among the 62.  Its normalized residual is

```
(6,0,0,-36,0,6,6,24,0,0,-6,-18,-6,-12,0,0,0,0,-6,-6).
```

Every entry is divisible by six, and an independent physical anti-fold
replay is performed for every one of the 62 survivors.  All 62 exact
integer replays fail; the best still has eleven nonzero normalized lags.
The witness is therefore **not** an integer Golay repair and does not
construct `H(668)`.

## Exact next census

The exact completion of this lane is now well specified:

1. Enumerate the 262,143 remaining solutions of the 18-dimensional
   pair-parity quotient.
2. For a quotient having `k` odd pairs, impose exactly `(39-k)/2` full
   even pairs; this covers its complete weight-39 fiber.
3. Substitute its 39 pair states into the mod-3 jet, condition on the
   central cross-block pair, and recompute the four reflection
   components.
4. Perform the same residue-vector / full-pair-count meet in the middle,
   and physically replay every match.

The union of those quotient censuses with this one would exhaust all
`25,941,166,955,843,488` supports in the characteristic-two slice.  The
component sizes vary with the quotient parity vector, so the present
`10,10,10,8` table cannot simply be reused unchanged.

## Verification

Run:

```
/Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  verify_fixed_quotient_join.py
```

The verifier re-derives the reflected pairs, the exact Boolean
substitution, and the four-component interaction split.  It exhaustively
joins the component tables, reconstructs all 62 supports, replays all of
them from the physical four anti-fold rows, and compares the full result
to `CASE26_FIXED_QUOTIENT_MOD6_CENSUS.json`.

The contraction enumerates at most `2^20 + 2^18` pair-table rows for each
central value, rather than the roughly `1.08e11` physical supports.
