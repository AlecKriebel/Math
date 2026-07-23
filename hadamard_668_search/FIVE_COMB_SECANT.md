# The five-comb secant: an obstruction and a spectral escape

## Status

No `BS(84,83)` or Hadamard matrix of order 668 is constructed here.  This
note turns the five-tooth carrier in `NOVEL_LIFTING_64.md` into exact
nonlinear statements: two sharply scoped no-go results and one constructive
spectral escape.

The conclusions are:

1. the literal reciprocal five-comb chord through Eliahou's seed contains no
   point on the next, modulo-32 lifting layer; and
2. every repair through the seed that keeps the common factor
   `P(z)=1-z^4+z^8-z^12+z^16` is impossible, even with overlapping
   translates and unrestricted integer quotient coefficients; but
3. replacing the single alternating comb by a minimum complementary octet
   gives an exact 32-channel, energy-320 spectral repair whose supports pack
   into lengths `(84,84,83,83)`, leaving exactly fourteen binary positions.

The remaining task is no longer to repair one common-`P` quotient.  It is to
assign those 32 nonidentical carrier channels to four packed sequences and
choose the fourteen remaining signs so that the packing cross terms cancel.
This is a finite algebraic compression problem.  It is not solved here.

As a separate exact check, an orthogonally staged disjoint-comb constructor
fails at its two endpoint rows: none of 80,896 admissible endpoint pairs is
cross-orthogonal.  This count applies to that sufficient staged system, not
to arbitrary disjoint-comb cancellations.

Reproduce every count with:

```sh
python3 verify_five_comb_secant.py
```

The checker uses exact integer arithmetic and Gaussian elimination over
`GF(2)`.  It uses no optimizer and remains well below the project memory
limit.

## 1. The defect is one rank-one spectral carrier

Let

```text
P(z) = 1-z^4+z^8-z^12+z^16
W(z) = (z^42-1)P(z).
```

For Eliahou's four base polynomials `X=(A,B,C,D)`, the factorization in
`NOVEL_LIFTING_64.md` can be sharpened to the complete norm identity

```text
sum_X N(X) = 14 + 32 N(W).                              (1)
```

This includes the constant coefficient:

```text
14 + 32*10 = 334.
```

At positive lags, the nonzero coefficients on the right are exactly

```text
k :   4    8    12   16   26   30   34   38   42   46   50   54   58
R : -256  192  -128   64  -32   64  -96  128 -160  128  -96   64  -32.
```

Thus all thirteen base residuals form the autocorrelation of one ten-sparse
ternary word, repeated with multiplicity 32.  The five failed modulo-32
lags are the Frobenius-square shadow of this same rank-one carrier.

Identity (1) explains why a nonlinear term is necessary.  A first-order
change sees only the cross term with `W`; a genuine repair must change its
self-norm.

## 2. The common-comb component is impossible

Ordinary integer-polynomial division of the four seed sequences by `P`
gives the remainders

```text
A : ( 1,-1,-1,-1)
B : ( 1,-1,-1, 1)
C : ( 1, 1, 1)
D : (-1, 1,-1).
```

These four words form `BS(4,3)`, so their summed spectral energy is the
constant 14.

Now put `y=z^4`.  The comb is the cyclotomic polynomial

```text
P = 1-y+y^2-y^3+y^4,
(y+1)P = y^5+1.
```

It therefore has roots on the unit circle.  At any such root `zeta`, every
quadruple congruent to the seed modulo the common factor `P` has

```text
sum_X |X(zeta)|^2 = 14.
```

A `BS(84,83)` quadruple would instead have spectral energy 334 at every
point of the unit circle.  Thus no binary or nonbinary modification

```text
X'_r = X_r + P Q_r
```

can repair the seed, regardless of overlap or the size of the integer
quotient coefficients.  More generally, a common-`P` representation whose
four remainders contain respectively `(4,4,3,3)` signed monomials has energy
at most

```text
4^2 + 4^2 + 3^2 + 3^2 = 50 < 334
```

at a unit-circle root of `P`.  This closes the previously proposed
overlapping-common-comb extension: at least one sequence must break the
common factor.

## 3. The literal reciprocal chord is isolated

Start with the five parameter indices

```text
C = {13,17,21,25,29}.
```

Use them in both the long and short reciprocal `q` skeletons.  This gives ten
independent `q` parameters and twenty physical positions.  Define the
literal chord family by:

- toggling any subset of those ten skeleton parameters;
- changing `s` arbitrarily at the twenty carried physical positions; and
- fixing every other `s` coordinate to the published value.

This is the complete `2^30` family suggested by the literal support, not
only the simultaneous five-tooth flip.

It is unnecessary to enumerate `2^30` points.  For each of the `2^10`
structured `q` words, substitute the 147 fixed `s` bits into the exact
modulo-four equations and row-reduce the resulting system in twenty
variables.

The exact result is:

```text
q masks inconsistent already modulo 4       1023
q masks consistent modulo 4                    1
rank of the one restricted system              15
points in its modulo-4 affine fiber             32
points surviving modulo 8                       1
points surviving modulo 16                      1
points surviving modulo 32                      0
```

The unique modulo-8 and modulo-16 point is the original seed.  Hence the
literal reciprocal chord does not escape the rank-200 tangent obstruction.
Any actual comb secant must acquire coordinates outside the twenty physical
teeth.

## 4. An orthogonally staged disjoint constructor

There is a second exact interpretation of the five-comb.  Each residue line
modulo four in a long sequence has length 21.  Remove one cell whose
compressed coordinate is

```text
g = 5a,  a in {0,1,2,3,4},
```

and tile the remaining twenty cells by four disjoint translates of `P`.
For each short sequence do the same in residue lines 0, 1, and 2; its
residue-3 line already has length 20 and needs no removed cell.

Across lengths `(84,84,83,83)` this partitions the 334 coefficients into:

```text
14 boundary signs + 64 signed copies of P.
```

Let `R=(R_A,R_B;R_C,R_D)` be the fourteen boundary signs and let
`Q=(Q_A,Q_B,Q_C,Q_D)` record the 64 tile signs.  The constructed
polynomials have the exact form

```text
X_r = R_r + P Q_r.                                      (2)
```

The supports in (2) are disjoint, so every coefficient of `X_r` is
automatically `+1` or `-1`.  Expanding norms gives

```text
sum N(X_r)
 = sum N(R_r)
 + N(P) sum N(Q_r)
 + P sum(Q_r R_r*) + P* sum(R_r Q_r*).                 (3)
```

Therefore the following three finite, sufficient conditions would construct
`BS(84,83)`:

```text
sum N(R_r)       = 14,
sum Q_r R_r*     = 0,
sum N(Q_r)       = 64.                                 (4)
```

The first line says precisely that the labelled boundary is `BS(4,3)`.
There are 256 such labelled boundaries.  These conditions deliberately
force the three terms in (3) to vanish separately; the endpoint count below
rules out this staged subfamily, not every possible cancellation among the
three terms.

## 5. Exact endpoint obstruction

The middle equation in (4) separates by comb row because consecutive rows
are twenty coordinates apart.  Relative to the boundary, a row before the
removed block has equal alignment (`E`), while a row after it has the long
pair shifted once relative to the short pair (`O`).

For each labelled `BS(4,3)`, the checker enumerates every four-word sign row
whose boundary cross term vanishes.  Exactly half of the boundaries have

```text
(number of E mates, number of O mates) = (10,6),
```

and the other half have `(6,10)`.

The first and last tile rows are separated farther than any other row pair.
Consequently their entire mutual cross-correlation must vanish separately
if the last equation in (4) is to hold.  The five boundary positions require
only three endpoint types:

```text
a=0       O--O
a=1,2,3   E--O
a=4       E--E.
```

The exact endpoint-pair counts are:

```text
O--O pairs   17,408    cross-orthogonal pairs   0
E--O pairs   15,360    cross-orthogonal pairs   0
E--E pairs   17,408    cross-orthogonal pairs   0
```

The mixed case occurs at three boundary positions, so the full aligned-gap
constructor rules out

```text
17,408 + 3*15,360 + 17,408 = 80,896
```

necessary endpoint pairs.  No interior-row enumeration is needed: every
candidate already fails at the farthest interaction.

## 6. A seed-aligned nonlinear spectral escape

Write the five nonzero comb coefficients as the binary word

```text
p = (1,-1,1,-1,1).
```

An exact dynamic program over all binary length-five autocorrelation
signatures proves that a complementary family containing `p` needs at least
eight words.  The bound is attained by the following octet (the repeated
word represents two independent channels):

```text
 ( 1,-1, 1,-1, 1)
 (-1,-1,-1,-1,-1)
 (-1,-1,-1,-1, 1)
 (-1,-1,-1, 1, 1)
 (-1,-1, 1,-1, 1)
 (-1,-1, 1, 1,-1)
 (-1,-1, 1, 1,-1)
 (-1, 1,-1,-1, 1).
```

If these words are `P_j`, then exactly

```text
sum_j N(P_j) = 40.
```

For each word, introduce both polarizations across the original separation
42,

```text
C_(j,eps)(z) = P_j(z^4) + eps*z^42 P_j(z^4),
eps in {-1,+1}.
```

The opposite polarizations cancel their separation cross terms, while
complementarity cancels every remaining nonzero lag.  Hence the sixteen
ten-sparse carriers obey

```text
sum_(j,eps) N(C_(j,eps)) = 160.
```

Two copies provide 32 carrier channels with constant energy 320.  Fourteen
singleton channels supply the remaining energy, giving an exact
46-channel complementary system of total energy 334.

The word `p` is necessary only if this construction is required to pass
through the factor in Eliahou's defect.  It is not necessary for a direct
construction of a new base sequence.  A complete normalized multiset
classification gives the following counts:

```text
family size       1    2    3    4    5    6    7      8
complementary     0    0    0   48    0    0    0   1,246
```

Here every word is normalized to begin with `+1`, since its global sign has
no effect on its autocorrelation.  Thus the unrestricted minimum is four,
not eight.  The 48 complementary quartets fall into 17 orbits under common
word reversal and common coordinate alternation.  This orbit count describes
the small word families only; those operations are not assumed to preserve a
later fixed-slot packing.

For any one of the 48 quartets,

```text
sum_j N(P_j) = 20.
```

Its eight polarized carriers have energy 80, and four copies give the same
32 channels of constant energy 320.  The original octet remains the minimum
family containing the alternating word `p`; the quartet construction is a
strictly smaller direct-construction lane.

Crucially, this abstract channel system fits the target coefficient budget.
In each target sequence, translate eight carriers by

```text
0, 1, 2, 3, 20, 21, 22, 23.
```

Their ten-point supports are pairwise disjoint.  They occupy 80 positions
and leave

```text
length 84 : 40, 41, 82, 83
length 83 : 40, 41, 82.
```

Across `(84,84,83,83)`, these are precisely the fourteen singleton slots.
Every packed coefficient is therefore automatically binary.

Packing several independent channels into one polynomial introduces cross
terms that the channel identity does not see.  The next exact problem is to
choose one of the 48 quartets, permute the four copies of its eight polarized
types among the 32 slots, choose their global signs, and choose the fourteen
hole signs so that all packing cross terms vanish.  The seed-aligned octet,
with two copies of sixteen types, remains an independent inventory.  In both
cases the carrier self-norm is already solved.

`verify_five_comb_secant.py` certifies the 48-family classification and every
flat 32-channel identity.  `search_five_comb_packing_anneal.cpp` supports the
seed-aligned inventory by default and selects a quartet with
`--quartet-index 0,...,47`.  This search is diagnostic; any zero must still
be replayed by the independent base-sequence and full-matrix verifier.
