# Certified level-four branch certificate

## Result

The quotient-tower calculation gives a compact good-reduction certificate for
a new deepest leaf transposition at level four.  Together with the proved
level-three quotient and the all-level full-cycle theorem, it proves

```text
Mon(F^4) = S_3 wr S_3 wr S_3 wr S_3.
```

Its natural degree is `81` and its order is

```text
|W_4| = 6^(1+3+9+27)
      = 13,367,494,538,843,734,067,838,845,976,576.
```

The main Discovery 4 note is kept separate so that this upgrade can be
reviewed and published independently.  A bounded-memory independent audit of
the modular arithmetic, localization argument, norm-divisor formula, and
group-theoretic step was completed on 22 July 2026.  This is not external peer
review.

## Certificate data

Work at

```text
p = 1009,       s_0 = 801.
```

Let `X_i` be the `i`th inverse point over the target `(1,2,s)`, and put

```text
N_i(s) = Norm(Delta(X_i)).
```

The target discriminant followed by the three inverse-level norms is

```text
(Delta(1,2,s_0), N_1(s_0), N_2(s_0), N_3(s_0))
    = (497, 650, 840, 0)                         mod 1009.
```

Thus all lower cubic covers are etale at this parameter, while the deepest
discriminant norm vanishes.  The norms of the four cubic leading coefficients
are

```text
(2, 511, 972, 127),
```

and the norms of all nine divided-by elements in the three reconstruction
steps are

```text
(763, 881, 827, 437, 517, 668, 247, 706, 985).
```

Every one is a unit modulo 1009, so the degree-27 quotient tower and the
rational reconstruction formulas specialize without a pole or degree drop.

To check simplicity without globally reconstructing `N_3(s)`, evaluate in
`Z/(1009^2)`:

```text
1009^2                         = 1,018,081,
N_3(801)                       =   655,850 = 650*1009,
N_3(801+1009)                  =   563,022 = 558*1009,
N_3(801+2*1009)                =   470,194 = 466*1009,
N_3(801+1009)-N_3(801) mod p^2 =   925,253 = 917*1009.
```

Taylor expansion for a rational function regular at `s_0` gives

```text
N_3'(801) = 917 != 0 mod 1009.
```

The third value independently checks the same first-order law with step
`2p`.  As a coordinate-level check not using a quotient-algebra determinant,
the unique vanishing modular sheet follows the simple inverse-root path

```text
(t_1,t_2,t_3) = (803,282,899)
```

and reaches

```text
X_1 = (77,620,874),
X_2 = (984,54,608),
X_3 = (727,885,561)                         mod 1009.
```

Implicit differentiation along this path gives

```text
d Delta(X_3)/ds = 527 != 0                  mod 1009.
```

The final inverse cubic at `X_3` has the simple root `171` and the double root
`437` modulo 1009.  This explicit sheet check is recomputed by
`verify_w4_modular.py` using scalar dual-number arithmetic independent of the
norm determinant.

The full exploratory scan of `F_1009` found this single usable zero and six
exceptional reconstruction parameters.  Its SHA-256 digest is

```text
c48e3f4b7e402e6bf8076ca0b83702590a6df241bb8c42bcc08d81f0fe28fda4.
```

The scan is useful provenance but is not required for the targeted
certificate.

## Good-reduction argument

Work over `Z_(1009)[s]`, localized at the displayed leading and reconstruction
guards.  The three monic cubic quotients then form a finite free algebra `E`
of rank 27, and `d=Delta(X_3)` is regular in `E`.  The displayed nonzero lower
discriminant norms allow a further localization in which `E` is etale.  In
this ring

```text
N_3(s) = Norm_(E/R)(d) = A(s)/B(s)
```

with `A,B` in `Z_(1009)[s]` and `B(801)` a unit.  Reduction and specialization
commute with the norm because all inverted elements remain units.  Since
`N_3(801)=0` and `N_3'(801)=917`, reduction modulo 1009 gives

```text
A(801) = 0,        A'(801) = 917 B(801) != 0.
```

Hensel's lemma therefore produces a unique `sigma in Z_1009`, congruent to
801 modulo 1009, with `A(sigma)=0` and `A'(sigma)` a unit.  Let `P` be the
irreducible factor of `A` over `Q` containing `sigma`.  Then `P` occurs in
`A` with multiplicity one.  Every lower discriminant and every guard is still
a 1009-adic unit at `sigma`, so `P` divides none of them.

At the generic point of `P`, the localized rank-27 algebra is etale.  The
valuation formula for a norm is

```text
ord_P Norm(d) = sum_(q|P) f(q/P) ord_q(d) = 1.
```

All summands are nonnegative integers.  Consequently there is exactly one
prime `q` above `P` at which `d` vanishes; its residue degree and vanishing
order are both one.  Geometrically, exactly one of the 27 sheets meets
`Delta=0`, and it does so transversely.  This also makes precise why a simple
zero of the product norm cannot hide simultaneous branching on two sheets.

The actual discriminant of the final inverse cubic

```text
2 a T^3 - b T^2 + 2 T - c
```

is `-4 Delta(a,b,c)`.  Its leading coefficient is a unit, and a simple
discriminant zero cannot be the triple-root locus.  Hence local inertia on the
81 leaves is a single transposition inside one bottom three-leaf block.

The existing all-level Newton argument supplies an 81-cycle `alpha`, and the
proved level-three result supplies the full quotient `W_3`.  Because `alpha`
is transitive on 81 leaves while preserving 27 blocks of size three, it
induces a 27-cycle on the blocks and `alpha^27` restricts to a 3-cycle on each
block.  The leaf transposition and its `alpha^27`-conjugate generate `S_3` on
one bottom block.  Conjugating by powers of `alpha` supplies 27 factors with
pairwise disjoint supports, hence the entire kernel `S_3^27`.  A subgroup of
`W_4` containing this kernel and surjecting onto `W_3` is all of `W_4`.

## Verification

The implementation uses only the Python standard library:

```console
python3 test_finite_field_norm.py
python3 verify_w4_modular.py
```

The first command tests the cubic quotient arithmetic, inverses, nested root
relations, norm multiplicativity, the inverse reconstruction identity, and
the prime-square determinant path.  The second recomputes every displayed
number, the explicit scalar sheet and its dual-number derivative, scan
integrity, and the elementary `S_3^27` kernel lemma.

## Audit record and boundary

The independent audit checked the three formerly open steps: Hensel lifting
after localization, the etale norm-valuation formula, and the compatibility
of an 81-cycle with the bottom-block system.  It also recomputed the three
displayed determinants modulo `1009^2` with SymPy's exact-integer determinant
routine; the peak resident set was under 50 MB.  The repository verifier does
not require SymPy.

This remains a public computational research draft rather than a
peer-reviewed result.  Repeating the certificate at a second prime or
reconstructing the global norm would be useful corroboration, but neither is
needed for the simple-zero argument above.
