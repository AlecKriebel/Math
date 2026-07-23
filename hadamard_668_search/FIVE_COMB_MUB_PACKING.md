# Two-basis algebra for the five-comb packing

## Status

No `BS(84,83)` or Hadamard matrix of order `668` is constructed here.

This lane turns the remaining packing problem in `FIVE_COMB_SECANT.md` into
small exact group quotients.  Its main conclusions are:

1. the eight projective four-row sign vectors are two mutually unbiased
   Hadamard bases, and a construction confined to one global basis has a
   sum-of-two-squares obstruction;
2. the fourteen holes have a modulo-four image of rank only six;
3. in the original octet geometry, an exact meet in the middle reduces
   `24^8` projective orthogonal-pair assignments to `32,768`, and any
   survivor must change at least four of the natural first-lobe columns;
4. among all `8!=40,320` projective-column bijections in the four-copy
   complementary-quartet construction, exactly `64` survive modulo four;
   their eight row-sign orbits split evenly into four affine and four
   genuinely quadratic-shear orbits; and
5. all `1,056,964,608` exact hole completions in those eight orbits have
   been checked, with no `BS(84,83)`.

A second natural quartet action, using affine Pauli signed permutations, is
even more rigid: all `1,935,360` actions fail already modulo four.

Subsequent work removed the bijective-label restriction altogether.
`FIVE_COMB_PROJECTIVE_EXHAUSTION.md` gives the rank-nine quotient with 4,096
normalized label maps and reports all 1,536 common-type quartet/core models
`INFEASIBLE`. `FIVE_COMB_PAIRED_LOBES.md` gives the strictly broader live
construction using distinct words in the two lobes.

Reproduce the algebraic counts with:

```sh
python3 check_five_comb_mub_reductions.py
```

Compile the exact binary packing verifier with:

```sh
c++ -O3 -std=c++20 -o search_five_comb_mub_quartet \
    search_five_comb_mub_quartet.cpp
```

Each normalized quartet is selected by an index from `0` through `47`.
The complete run is:

```sh
for q in $(seq 0 47); do
    ./search_five_comb_mub_quartet "$q"
done
```

The search uses about `1.5 MB` RSS.  It stores every sequence as two machine
words and verifies all `83` aperiodic correlations exactly.

## 1. The two projective Hadamard bases

Up to a global sign, there are eight vectors in `{+1,-1}^4`.  Normalize the
first entry to `+1`.  They split by the parity of their remaining three
signs into two sets of four:

```text
H  = the four columns of a normalized H4,
H' = eta * H,                 eta=(1,1,1,-1).           (1)
```

Within either set the vectors are mutually orthogonal.  Between the two
sets every inner product is `+2` or `-2`.  Thus `H,H'` are two real mutually
unbiased bases.

This is exactly the geometry of polarization.  If the first and second
lobes of one octet carrier have row-sign vectors `g,h`, then using each
polarization twice is equivalent to

```text
g dot h = 0.                                             (2)
```

Projectively, `g,h` are two different columns of the same one of the bases
in (1).  There are

```text
2 * 4 * 3 = 24
```

ordered projective choices per slot.

The opposite geometry occurs for the four-copy quartet construction.  All
four copies of a polarized type occupy one slot, so its two lobes have
parallel projective vectors.  The eight slots may then use the eight vectors
in (1) exactly once.

## 2. Why a single global `H4` basis cannot finish the job

Suppose every column at the common positions `0,...,82`, including the
three common holes, is a signed column of one fixed `H4`.  The summed
four-row contribution at every core lag is then a multiple of four.

The extra coordinate `83` occurs only in the two long rows.  Its inner
product with a core column is `0` or `+/-2`.  Exact cancellation therefore
forces it to be orthogonal to every core column.  Only two of the four
Hadamard columns have this property.

Consequently the common core would reduce to two disjoint-support scalar
sequences whose summed autocorrelation is flat and whose total energy is
`83`.  At `z=1` their row sums would give

```text
x^2+y^2 = 83,                                            (3)
```

which is impossible because the prime `83` is `3 mod 4`.

This excludes a pure global orthogonal-array labeling.  It does not exclude
arbitrary signs at the holes; those are retained in every finite scan below.
It shows why cross inner products `+/-2`, hence both bases in (1), are a
necessary algebraic escape.

## 3. The rank-six hole quotient

Write every binary coefficient as `(-1)^b`.  At lag `k`, changing a sign
changes the correlation by `2 mod 4`, so every modulo-four equation becomes
linear over `GF(2)`.

There are fourteen variables at

```text
long rows:  40,41,82,83
short rows: 40,41,82.
```

Their `83`-equation incidence matrix has exact rank

```text
rank_GF(2) = 6.                                         (4)
```

Every consistent carrier assignment therefore has exactly

```text
2^(14-6) = 256                                          (5)
```

hole assignments on the modulo-four layer.

There is also a direct reciprocal interpretation.  If `D(k)` is the parity
of the total Hamming distance at lag `k`, then a base sequence must have

```text
D(k)=1,                 k=1,...,83.                     (6)
```

Successive differences of (6) give the oriented inverse-pair conditions.
The checker represents their quotient by the hole image as one exact
`83`-bit integer signature.

## 4. Original octet: the exact projective reduction

Keep the same five-tooth word in the two lobes of every carrier.  At each
slot choose any ordered projective pair `(g,h)` satisfying (2).  This is the
complete `24^8` projective problem; global lobe signs have not yet been
chosen.

A four-plus-four meet in the middle against the rank-six hole quotient gives
exactly:

```text
projective modulo-four survivors     32,768.
```

Relative to the natural first-lobe `H4` columns at shifts

```text
0,1,2,3,20,21,22,23,
```

the survivor distribution is:

```text
first-lobe columns changed   survivors
4                                  320
5                                2,048
6                                6,784
7                               11,776
8                               11,840.
```

In particular, neither changing only the second-lobe polarization columns
nor making one, two, or three local first-lobe twists can work even modulo
four.  A nonzero packing tail requires at least four coordinated changes.

This is an exact reduction before any scalar-sign solver.  It replaces
roughly `1.1e11` projective assignments by `32,768` candidates.

## 5. Complementary quartets

Normalize a binary length-five word by fixing its first sign.  Exact
enumeration gives:

```text
complementary multisets of size 1       0
complementary multisets of size 2       0
complementary multisets of size 3       0
complementary multisets of size 4      48.
```

Let `Q_0,...,Q_3` be any one of these complementary quartets.  Polarize each
word with both signs across the separation `42`.  Four copies of every
polarized type give `32` carrier channels and total energy `320`.

The clean common-type packing puts all four copies of one polarized type in
one slot.  A slot has one row-sign vector `v_t`; its second lobe is the same
vector or its negative according to the polarization.  Assign the eight
polarized types bijectively to the eight slots.

First allow an arbitrary projective-sign bijection

```text
v : {eight slots} -> H union H'.                         (7)
```

An exact enumeration of all `8!=40,320` bijections gives:

```text
modulo-four survivors before row-sign quotient          64
affine survivors                                        32
non-affine survivors                                    32.
```

The affine half consists of maps

```text
v(x) = L(x)+b,                  x in F_2^3.              (8)
```

Of the `|AGL(3,2)|=1,344` maps in (8), exactly `32` survive the hole
quotient.  They are the eight translations of four linear maps:

```text
(4,5,2), (4,7,2), (6,5,2), (6,7,2),                    (9)
```

where a triple records the images of the standard basis as three-bit
integers.

Translating every projective label multiplies all common columns by one
fixed four-row sign vector.  Independent row negations and the complete hole
fiber make those eight translations equivalent.  Thus only four maps in
(9) remain.  The same label-XOR action is free on all `64` survivors.
Consequently the complete bijective quotient has exactly eight
representatives: four affine and four non-affine.

The eight representatives are not an unstructured list.  Write a slot as
`x=(x_0,x_1,x_2)` in `F_2^3`, identify output labels with three-bit
integers, and let `L` be the linear map `(4,5,2)`.  Every one of the `64`
survivors has the unique triangular-shear form

```text
v(x) = L(x) XOR t
             XOR 2*(a*x_0 XOR b*x_1 XOR c*x_0*x_1),     (10)
```

where `a,b,c` lie in `F_2` and `t` lies in `F_2^3`.  The final term points
in the output direction labeled `2`.  It changes the third coordinate by
a Boolean function of the first two, so (10) is automatically bijective.
The four cases with `c=0` are affine after quotienting `t`; the four cases
with `c=1` are genuinely quadratic.  Equivalently, every survivor obeys

```text
v(x XOR 4) = v(x) XOR 2.                                (11)
```

Thus the modulo-four equations have selected a complete degree-two
algebraic family, rather than 64 accidental permutations.  The checker
verifies equality of the enumerated survivor set with (10), not only its
cardinality.

Without the affine restriction, exactly

```text
32,768 of 8^8
```

projective slot labelings survive modulo four.  The affine family is the
smallest group-structured slice of this exact set; the complete bijective
slice is now exhausted below.

## 6. Full surviving-bijection quartet exhaustion

For each of the `48` quartets, the exact C++ constructor uses:

```text
projective maps after row-sign quotient        8
  affine                                        4
  non-affine                                    4
affine type-to-slot bijections              1,344
affine slot-sign characters                    8
carrier packings                           86,016
hole assignments per packing                  256
full binary completions                22,020,096.
```

The constant slot-sign character is removed exactly: changing it and
complementing all fourteen holes negates every target sequence and leaves
all correlations unchanged.

Across all `48` quartets the exhaustive totals are:

```text
carrier packings                         4,128,768
modulo-four hole completions         1,056,964,608
row-square-compatible completions        7,962,624
exact BS(84,83) objects                          0.
```

The affine and non-affine halves contribute:

```text
                                      affine       non-affine
carrier packings                    2,064,384        2,064,384
modulo-four hole completions      528,482,304      528,482,304
row-square-compatible completions   4,276,224        3,686,400
exact BS(84,83) objects                      0                0.
```

Half the quartets have `159,744` row-compatible completions and half have
`172,032`.  Within those totals, the affine contribution is respectively
`86,016` or `92,160`, while the non-affine contribution is `73,728` or
`79,872`.

The closest row-compatible point under lexicographic
`(number of bad lags, squared residual energy)` has:

```text
quartet index             39
normalized word indices   6,7,12,13
projective-label map      0,4,5,1,2,6,7,3
projective map class      affine
row sums                  14,-4,-11,-1
bad lags                  30
squared residual energy   1,248.
```

Here the normalized word catalog is `(1,) + product((-1,1), repeat=4)`,
with the last coordinate changing fastest; this is the same catalog used by
`verify_five_comb_secant.py`.

Its nonzero correlations are:

```text
 2:  4,   5: -4,   6: -4,   8:  4,  10:  4,
14:  4,  16: -4,  18:  4,  19: -4,  21: -4,
23:  4,  24:  4,  32:  4,  37: -4,  40:-20,
42:  4,  44: 12,  49: -4,  52:-12,  57:  4,
60: 12,  66:  4,  68:  4,  69: -4,  70:  4,
74: -4,  76: -4,  77:  4,  78: -4,  82: -4.
```

This is a diagnostic near point, not a candidate lift.

## 7. Pauli signed-permutation action

A second natural quartet construction places all four different quartet
words in every slot through a signed permutation matrix `M_t`.  Choose four
positive and four negative polarized slots.  Then every word/polarization
type occurs four times, each slot is internally complementary, and the
separation-42 self terms cancel.

The algebraically smallest choice takes `M_t` from the real two-bit Pauli
signed permutations

```text
(M_(a,b) q)_r = (-1)^(b dot r) q_(r+a),
```

and labels the eight slots by an affine injection

```text
F_2^3 -> F_2^4.
```

There are `2,520` linear injections and `16` translations.  The checker
tests all

```text
48 * 2,520 * 16 = 1,935,360
```

quartet actions.  None is consistent with the rank-six modulo-four hole
system.  Polarization and global slot signs cannot alter this certificate,
so the entire affine Pauli family is excluded before an integer correlation
test.

## 8. Consequences and next algebraic target

The literal global-Hadamard labeling is too orthogonal, while the affine
Pauli action has the wrong reciprocal parity.  The common-type two-basis
construction reaches the correct modulo-four layer, but its complete
bijective projective slice with affine type and scalar labels has now been
exhausted exactly.

That once-open target has now been completed for all 48 common-type
quartets. The next finite target is the distinct-lobe family:

1. select four sorted directed word pairs whose eight words form one
   complementary octet;
2. retain both polarizations of every pair;
3. reuse the rank-nine label quotient, row-pair symmetries, 256-point hole
   fiber, and physical high-lag table;
4. apply the exact modulo-16 two-pair-plus-two-pair filter before all-lag
   solving;
5. run strict order-668 verification immediately if an aperiodic object
   appears.

No outside contact was made or prepared.  These are exact exclusions of the
displayed algebraic constructions, not a nonexistence result for
`BS(84,83)` or `H(668)`.

The early bijective projective slice has an independent deterministic
exhaustion. The later unrestricted common-type conclusion is instead backed
by 1,536 CP-SAT `INFEASIBLE` records with integrity checks but no independent
UNSAT proof certificates; the two evidence levels must not be conflated.
