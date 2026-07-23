# Symmetric/skew inversion obstruction for `LP(333)`

The subfamily in which **each** Legendre sequence is either symmetric or
skew under inversion is impossible.  The two permitted forms are

```text
X[-i] =  X[i]  (symmetric),
X[-i] = -X[i]  for i != 0  (skew).
```

This result does not use the conjectural fixed length-37 compression.  It
rules out the symmetric/symmetric, skew/skew, and both mixed subfamilies of
every normalized `LP(333)` search.

Normalization loses no pairs.  Summing all periodic-correlation equations of
a length-333 Legendre pair gives

```text
(sum X)^2 + (sum Y)^2 = 666 + 332(-2) = 2.
```

Both sequence sums are odd, so each is `+1` or `-1`.  Independently negating
either sequence preserves its PAF and its symmetric/skew type, letting both
sums be fixed to `+1`.

Compress a normalized sequence to its three residue-class sums.  Inversion
exchanges residues 1 and 2.  A symmetric sequence has compression

```text
(1 - 2v, v, v)
```

for an odd integer `v`.  Write the second sequence's parameter as `w`.
An inversion-skew sequence has compression

```text
(1, v, -v),
```

because all nonzero inverse pairs cancel and normalization fixes `X[0]=1`.
Compression of the Legendre PAF equations modulo three fixes the combined
energy at

```text
666 + 110(-2) = 446.
```

For two symmetric sequences, substitution gives

```text
(1-2v)^2 + 2v^2 + (1-2w)^2 + 2w^2 = 446,
```

or, after multiplying and completing squares,

```text
(3v-1)^2 + (3w-1)^2 = 668 = 4 * 167.
```

This is impossible: the prime `167` is `3 mod 4` and occurs to an odd power,
so 668 is not a sum of two integer squares.

The other cases give equally small certificates:

```text
skew/skew:  v^2 + w^2 = 222,
mixed:      (3v-1)^2 + 3w^2 = 667.
```

The first is impossible because the prime `3 mod 4` occurs to odd exponent
in 222.  In the mixed case, `667 = 23*29`; reducing modulo 23 would make
`-3` a square, but it is a quadratic nonresidue modulo 23.  Thus 23 would
have to divide both terms and hence occur squared, a contradiction.

Equivalently, the checker exhausts all 28,224 admissible compressed cases.
For a skew sequence, its odd parameter has 112 possibilities in
`[-111,111]`.  For a symmetric sequence, the additional requirement
`1-2v in [-111,111]` leaves 56 possibilities.  The four ordered type pairs
therefore contribute `56^2 + 2(56)(112) + 112^2 = 28,224` cases.

Run the independent standard-library checker with:

```sh
python3 verify_legendre_symmetry_obstruction.py
```

The scope is deliberately narrow.  It does not rule out a pair where at least
one sequence has neither inversion eigen-symmetry, a general
fixed-compression pair, a general `LP(333)`, or `H(668)`.
