# Paired-lobe enlargement of the five-comb construction

## Status

This note gives two exact self-cancellation theorems. It explains why the
completed 48-case common-type exhaustion is not the end of the five-comb
route and defines a much larger structured construction family.

No base sequence or Hadamard matrix is claimed.

## 1. Same-word polarized carriers

For

```text
C_i(z) = P_i(z^4) (1 + epsilon_i z^42),
epsilon_i in {+1,-1},
```

let `A_+` and `A_-` be the sums of the word norms for the two polarizations.
Then

```text
sum N(C_i)
  = 2(A_+ + A_-)(z^4)
    + (z^42+z^-42)(A_+ - A_-)(z^4).
```

The two terms have disjoint nonconstant lag supports. For eight carriers the
self norm is flat exactly when

```text
A_+ = A_- = 20.
```

Therefore each polarization contains four words forming a complementary
length-five quartet. The exact same-word family is an ordered pair
`(Q_-,Q_+)`:

```text
48^2 = 2,304 ordered inventories
48       diagonal common-type inventories
2,256    new off-diagonal inventories.
```

The theorem requires the same word in both lobes.

## 2. Distinct-lobe paired signs

The broader carrier is

```text
D[j,epsilon](z)
  = P_j(z^4) + epsilon z^42 Q_j(z^4),
j=1,...,4, epsilon=+1,-1.
```

Pairing both signs cancels the cross norm:

```text
N(D[j,+]) + N(D[j,-])
  = 2 N(P_j(z^4)) + 2 N(Q_j(z^4)).
```

Hence all eight carriers have flat self norm exactly when the combined
multiset

```text
{P_1,...,P_4,Q_1,...,Q_4}
```

is a complementary length-five octet. Neither side needs to be a quartet.

## 3. Exact finite classification

With every word normalized to begin with `+1`, exact enumeration gives:

```text
complementary octet multisets                         1,246
autocorrelation-signature profiles                       35
octets decomposable into two complementary quartets      689
genuinely nondecomposable octets                         557
decomposable signature profiles                           14
genuinely new signature profiles                          21.
```

There are 256 directed normalized pairs `(P,Q)`. Unordered multisets of four
directed pairs give:

```text
self-cancelling directed-pair inventories             768,512
both P- and Q-projections are quartets                  46,528
genuinely distinct-lobe inventories                    721,984
diagonal P=Q common-type inventories                         48.
```

The 768,512 inventories contain 753,832 with four distinct pair codes,
14,152 with one doubled code, and 528 with two doubled codes.

The canonical enumeration hashes are:

```text
octets
81b45bd47e3b12f9a0bc27e3ce31e4ac1db713e70f344c628398f63f40213fbc

signature profiles
d05912cf1df6dcc2f2ed5ddbb0b87d6d6eff30f6c4d1c7ec90a2e5eadbe30b5e

quartet-decomposable octets
ea0e821fae89c3c116a3f7339aacb8792fdf7063dd102ec3dee917cb1848c4d3

directed-pair inventories
32b52c913aab1ac7185d929b88f7527e92be558365bd33102744e7223c4e1230.
```

## 4. What remains invariant

The complete modulo-four projective quotient is independent of `P,Q`,
polarization, and carrier orientation. A scalar sign change at one occupied
position flips all four rows, whose incidence XOR is zero because the two
long rows have equal length and the two short rows have equal length.

An exhaustive 65,536-state audit therefore carries over:

```text
projective RREF rank                    9
normalized projective labelings     4,096
row-pair orbit representatives      1,440
physical hole completions             256.
```

Lags 83 and 82 also remain unchanged because all normalized `P,Q` begin with
`+1`. The 10,934-row physical table for lags 81 through 78 remains valid; its
type coupling changes only from the terminal sign of `P` to the terminal sign
of `Q`. The 2,434-row parameter projection and

```text
beta or u7 or y1 or y7
```

remain universal.

The deeper high-lag ladder must be regenerated with separate `P,Q`
coefficients. The direct lag-64-through-83 channel requires only a new scalar
carrier constructor.

## 5. Universal core-zero obstruction

The structural projective core

```text
alpha=beta=u5=u6=u7=0
```

uses only `V_0=(1,1,1,1)` and `V_2=(1,1,-1,-1)`. Consequently every
same-word or distinct-lobe carrier has row sums `(x,x,y,y)`. The
label-independent physical hole relations make the completed row sums

```text
(X+d, X-d, Y+e, Y+f),  d,e,f in {+1,-1}.
```

Writing `t=(e+f)/2`, the necessary norm 334 becomes

```text
X^2+(Y+t)^2 = 165+t^2.
```

For `t=0`, the right side is `165=3*5*11`; for `t=+/-1`, it is
`166=2*83`. In each case a prime congruent to 3 modulo 4 has odd exponent,
so neither number is a sum of two squares. Core zero is universally
impossible. It contains 128 of the 1,440 normalized row-orbit
representatives, so future construction work has only 31 structural cores.

The same exact reconstruction classifies all 768,512 paired inventories into
four possible sorted absolute `z=1` carrier profiles, with counts

```text
(0,0,0,0,2,2,6,6)      43,948
(0,0,0,2,2,2,2,8)      38,544
(0,0,2,2,2,4,4,6)     569,956
(2,2,2,2,4,4,4,4)     116,064.
```

Run `verify_five_comb_core0_obstruction.py` to replay the theorem, all 128
core maps, the 8/2,434 projected and 288/10,934 full high-lag rows removed,
and the four inventory counts. Its retained source SHA-256 is

```text
c693765752453b276f35db41bbe780f33573e1d208681142bb09a4d76ae52dff.
```

## 6. Safe and unsafe symmetries

Safe exact reductions include:

- normalize every word sign;
- sort the four directed pair codes;
- symmetry-break repeated pair occurrences;
- retain the projective row signs, row-pair swaps, global negation, and
  physical alternating symmetry.

Word reversal and tooth alternation are useful for classifying self norms but
are not safe exact symmetries of the fixed `84/83` support and hole mask.
Neither `P<->Q` nor a polarization swap is a universal construction symmetry.

## 7. Construction program

The next model should select four sorted pair codes directly, not launch
768,512 unrelated searches:

1. impose the four complementary-signature sums on the eight words;
2. instantiate both polarizations of every directed pair;
3. reuse the 31 surviving projective cores, hole fiber, and physical boundary
   table;
4. run a two-pair-plus-two-pair dyadic/high-lag filter, sharded by the 35
   signature profiles and five endpoint splits;
5. prioritize the 21 nondecomposable profiles;
6. pass only survivors to the exact all-lag model and strict `H(668)`
   verifier.

Reproduce the classification and quotient invariance with Python 3.10 or
newer:

```sh
python3 verify_five_comb_paired_lobes.py
```

The verifier source SHA-256 is

```text
ca1fb91fbff7aefd19a2383cbc3bf962c40228350193b087c9734dced3292160.
```

An independent implementation reproduced every count and hash, the hole and
projective ranks, all 4,096 label maps, and all 1,440 row-pair orbits. Its
complete audit used about 23 MB RSS and zero swaps.
