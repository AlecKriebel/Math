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

## 6. First dyadic root sieve

The first exact stage of the order-16 compression now joins the even carrier
groups `(0,4)+(2,6)` against the odd groups `(1,5)+(3,7)` at roots `+1`
and `-1`. There are exactly 672 ordered row-sum targets at either root.
Writing the completed targets as `A,B`, the join key is the integral midpoint

```text
(A+B)/2 = E + (H_+ + H_-)/2.
```

The inventory side has the exact hierarchy

```text
768,512 directed-pair inventories
     35 octet autocorrelation profiles
    652 four-component signature profiles
  8,729 (sum P, sum Q, terminal Q) component multisets.
```

Each of the 652 component-signature profiles determines one of the four
root-amplitude profiles.

Two scopes are kept separate.

For arbitrary carrier placement, allowing every amplitude permutation and
independent sign is a rigorous relaxation of the full distinct-lobe family.
Together with the exact hole fiber and the 2,434-row physical high-lag
parameter image, it rejects 46 new nonzero-core map/profile rows. Weighted
by the four inventory counts, this removes

```text
2,576,920 / 1,864,410,112 = 0.1382%
```

of the post-core-zero inventory-by-parameter-map products. It eliminates no
entire surviving core/profile cell.

For the narrower vertical-pair placement in which the two polarizations of
one directed pair occupy `(g,g+4)`, projecting the 10,934-row high-lag table
independently onto the even and odd halves gives a stronger necessary sieve:

```text
cores 9,15,18   reject profiles 0 and 1       82,492 inventories each
core 20         rejects profile 0             43,948 inventories
core 27         rejects profiles 0,1,3 and
                340,548 of profile 2         539,104 inventories
```

Thus ten vertical-placement profile/core cells and 830,528 of the
23,823,872 inventory/core products are removed. This `3.486%` figure does
**not** apply to arbitrary placement. The even/odd projection deliberately
forgets whether both halves came from the same high-lag row, so its
infeasibility conclusions are sound but its surviving set is a relaxation.

Run the standard-library replay with

```sh
python3 verify_five_comb_root12_sieve.py
```

Its retained source SHA-256 is

```text
aa79ce46ec9e495864bd12c85d29bcd5d1633b7dbb6265f5ad95939a02fd246e.
```

The isolated vertical-stage prototype used 52.2 seconds, about 705 MB RSS,
and no swap. The retained combined replay used 123.4 seconds and
693,534,720 bytes maximum RSS with no swap. Orders `4,8,16` remain the next
dyadic stages; neither root sieve claims a base sequence or an `H(668)`.

The vertical-pair slice has also been lifted through `Phi_4`. For a pair
with word sums `p,q`, its two carrier amplitudes are `p+epsilon*q` at root
`1` and `p-epsilon*q` at root `i`; thus the two polarizations exchange
amplitudes at the new root. Retaining this exchange in the same component
join adds 75,713 inventory/core rejections:

```text
core 4    rejects all of profile 0                         43,948
core 9    additionally rejects profile 2 / profile 3       1,918 / 8,462
core 12   rejects part of profile 1 / profile 3             4,784 / 7,506
core 18   additionally rejects profile 2 / profile 3          581 / 8,327
core 23   rejects part of profile 2                            187.
```

Cumulatively, roots `+1,-1,i` remove

```text
906,241 / 23,823,872 = 3.8039%
```

of the vertical-placement inventory/core products and completely reject
eleven profile/core cells. These counts remain vertical-pair-only and do
not exclude arbitrary carrier placement.

Run the standard-library replay with

```sh
python3 verify_five_comb_root4_vertical.py
```

Its retained source SHA-256 is

```text
87b183aa0edd5f6a0f9c9898f58f8d51ab58f7880686b11a6ebebc847dea67eb.
```

The isolated all-core `Phi_4` sweep used 302.1 seconds, about 510 MB RSS,
and no swap. The focused retained replay passed in 368.2 seconds with
499,613,696 bytes maximum RSS and no swap. The `Phi_8` and `Phi_16` stages
were the next open layers at that milestone.

`FIVE_COMB_ROOT8_VERTICAL.md` now implements `Phi_8` in the same
vertical-pair slice. Exact retained joins reduce core 4 from 724,564
`Phi_4` survivors to 140,007 and core 27 from 229,408 to 65,868. These are
additional rejections of 80.6771% and 71.2878%, respectively. The current
implementation retains the independent even/odd high-lag projection, so the
survivors remain a relaxation, and no percentage applies to arbitrary
placement. The other 29 cores and `Phi_16` remain open.

## 7. Safe and unsafe symmetries

Safe exact reductions include:

- normalize every word sign;
- sort the four directed pair codes;
- symmetry-break repeated pair occurrences;
- retain the projective row signs, row-pair swaps, global negation, and
  physical alternating symmetry.

Word reversal and tooth alternation are useful for classifying self norms but
are not safe exact symmetries of the fixed `84/83` support and hole mask.
Neither `P<->Q` nor a polarization swap is a universal construction symmetry.

## 8. Construction program

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
