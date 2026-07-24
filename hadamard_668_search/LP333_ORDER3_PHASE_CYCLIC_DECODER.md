# Mod-seven cyclic decoder audit for the order-three phase shell

## Result

Reduction modulo seven gives a much smaller exact factorwise **necessary
sieve** for the 54-trit phase problem.  It does not, by itself, give a
sub-6.34-billion exhaustive decoder.

Let `alpha` be a primitive ninth root.  Modulo seven,

```text
Phi_9(X) = X^6+X^3+1
         = (X^3-2)(X^3-4).
```

Both cubics are irreducible, so each coefficient component is

```text
K = F_(7^3),                         |K|=343.
```

Moreover,

```text
7^3 = 10 (mod 37),                   H=<10>={1,10,26}.
```

Consequently Frobenius on the coefficient field acts on the column roots
by exactly `H`.  Every `H`-period evaluation is already a scalar in `K`, and
the invariant algebra in each conjugate ninth-root component is

```text
K[C_37]^H = K^13.                                      (1)
```

The verifier constructs the 13-by-13 Gaussian-period transform inside
`F_(7^9)`, checks that every entry lies in `F_(7^3)`, and proves rank 13.
It also expands deterministic local phase alphabets back to `C_37`,
performs the cyclic products directly, and matches all thirteen scalar
products with the required inversion/conjugation factor pairing.

This is a sharper computational split than the degree-12 prime-167 factors:
there are thirteen scalar equations over a 343-element field.  The caveat is
that the target is not zero.  An exact phase frame must satisfy, at every
factor,

```text
x_A y_A + x_B y_B = 167 = 6 (mod 7),                  (2)
```

where `x` is the chosen ninth-root component and `y` is the
inversion/conjugation component at the paired column factor.

## Exact coefficient alphabets

For a residue profile `p=(p_0,p_1,p_2)`, each active fiber has size one or
two.  At residue `s`, its plus-component contribution is

```text
p_s=1:   alpha^s omega^(-u),
p_s=2:  -alpha^s omega^( u),             u in C_3,
```

and its conjugate-component contribution is obtained by
`alpha -> alpha^(-1)` and `omega -> omega^(-1)`.

Because `1,alpha,alpha^2` are a basis of `F_(7^3)` over `F_7`, the plus
coefficient alone decodes all local trits.  Thus the exact one-channel
alphabet sizes are

```text
active fibers       0       2       3
alphabet size       1       9      27.
```

Across two channels the 100 ordered profile pairs have the exact census

```text
local alphabet size       profile-pair count
1                                  9
9                                 36
27                                 6
81                                36
243                               12
729                                1.
```

The mod-seven transform therefore loses no local phase information before
the spectral join.

## Scalar compatibility table

Put `q=343`.  Since the right side of (2) is nonzero, `x=(x_A,x_B)` cannot
vanish.  For every one of the `q^2-1` nonzero values of `x`, the compatible
`y` values form an affine line of size `q`.  Hence one scalar factor has

```text
(q^2-1)q = 40,353,264
```

compatible quadruples.

This table is practical in isolation:

```text
four 9-bit field codes, byte-aligned         5 bytes/entry
complete fixed-width table                    192.4 MiB
one uint64 per entry                          307.9 MiB.
```

It need not actually be stored.  If `x_A != 0`, all solutions are

```text
y = (6/x_A,0) + tau(-x_B,x_A),       tau in K,
```

with the analogous formula pivoting on `x_B` when `x_A=0`.  The verifier
checks the parameter and its recovery on both exhaustive pivot axes, a
deterministic mixed projective slice, and three distinct `tau` fixtures.
The complete count follows algebraically from the unique affine-line
parameterization.

## Why this is not yet a decoder

The local compatibility table is not a trellis state compression.
Processing physical classes changes four independent partial spectral sums

```text
(x_A,x_B,y_A,y_B) in K^4.
```

Even for one factor, the raw ambient state count is

```text
|K|^4 = 343^4 = 7^12 = 13,841,287,201,
```

already 2.18 times the 6,338,555,429-signature profile fallback.  A Boolean
bitset would fit in about 1.61 GiB, but a full sweep already exceeds the
operation target, and a 32-bit predecessor per state would require about
51.6 GiB.  Tracking two or more factors multiplies, rather than reduces,
this state space.

The complete canonical zero-column words remove the tempting independent
channel-phase gauges.  Their certified affine stabilizers contain no row
translation: the `A` stabilizer is trivial and the only nonidentity `B`
map is a reflection.  The labelled transport group therefore does not
uniformly delete any placement trit.  A plain balanced MITM must retain all
54 trits and has

```text
3^27 = 7,625,597,484,987
```

entries on each side, before storing any field signature.  Splitting into
three balanced 18-trit lists makes each raw list
`3^18=387,420,489`, but does not
create a three-sum problem.  For a factor quadric `Q`,

```text
Q(a+b)=Q(a)+Q(b)+B(a,b),
```

and the polar term `B(a,b)` depends on both full partial spectral states.
A Wagner join on `Q(a)` alone is therefore unsound.  Enumerating the
intermediate pair restores `3^36` combinations.  A minimax four-block
split has sizes `14,14,13,13`.  Pairing the two small blocks first still
costs `3^26` and leaves a `3^28` join; balancing the exact pair joins costs
`3^27` on each side.

The usual BCH shortcut is also weak here.  The full period transform (1) is
an isomorphism, so there is no linear spectral redundancy.  The kernel of
one scalar factor has unrestricted parameters `[13,12,2]`: every transform
entry is nonzero, excluding weight one, and any two columns give an explicit
weight-two kernel word.  Local alphabets can make a particular profile
harder, but no alphabet-independent single-factor BCH bound can do so.

These are rejections of the raw-state trellis, plain balanced MITM, additive
Wagner join, and one-factor BCH architectures—not a complexity lower bound
against every possible algorithm.

## Useful continuation

The mod-seven equations should be kept as propagation constraints in a
future fixed-profile solver:

1. use one 1/9/27-state coefficient variable per channel and class;
2. carry the deterministic plus/conjugate lookup together;
3. evaluate the 13 scalar factors through the pinned period transform;
4. impose (2) by the affine-line formula, not a 40-million-row table;
5. combine this with the existing Eisenstein-adic affine kernel or another
   independent structural reduction before attempting enumeration.

There is a compact exact CP-SAT encoding; the 40-million-row compatibility
table should not be used.  In the basis `1,alpha,alpha^2`, with
`alpha^3=2`,

```text
(xy)_0 = x_0 y_0 + 2 x_1 y_2 + 2 x_2 y_1,
(xy)_1 = x_0 y_1 +   x_1 y_0 + 2 x_2 y_2,
(xy)_2 = x_0 y_2 +   x_1 y_1 +   x_2 y_0        (mod 7).
```

The thirteen factor equations need 26 field products.  Each field product
uses nine scalar products, and a scalar product modulo seven has a 49-row
table.  The complete nonlinear multiplication layer is therefore only

```text
26 * 9 = 234 scalar tables,
234 * 49 = 11,466 table rows,
```

plus linear period transforms and the local `1/9/27` coefficient lookups.
The verifier checks the coordinate formula on the complete bilinear basis.
This is a credible sub-gigabyte propagator, but it has deliberately not been
benchmarked: no exact-zero profile survivor exists to supply a legitimate
phase input, and CP-SAT memory size does not certify a sub-6.34-billion
search runtime.

Without that additional reduction, calling (1) a practical decoder would be
misleading.

The corrected composite certificate SHA-256 is

```text
0605563ad589018e39ac73a41ecf880c678f38ad6941730b9dd7fcb2e33e84cf
```

## Reproduction

```text
python3 verify_lp333_order3_phase_cyclic_decoder.py
python3 -m unittest -v test_lp333_order3_phase_cyclic_decoder.py
```

The verifier uses exact arithmetic and the Python standard library only.
