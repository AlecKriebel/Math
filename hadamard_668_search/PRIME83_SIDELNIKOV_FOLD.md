# The prime-83 Sidelnikov fold

## Status

This lane gives a clean exact exclusion, not a Hadamard matrix of order
`668`.

The quadratic-residue subgroup of `F_167` produces a striking
binary/one-zero complementary pair of length `83`.  It is perfectly adapted
to the anomalous prime fold of `BS(84,83)`, but the most natural lift fails
twice: first at the trivial character and, more strongly, at every nonzero
lag modulo eight.  A complete dependency-free hash join also excludes the
natural degree-at-most-two product extension.

Reproduce all arithmetic and finite counts with:

```sh
python3 check_bs84_sidelnikov_fold.py
```

The result has deliberately narrow scope.  It does not rule out
`BS(84,83)`, a general special Golay quadruple of length `167`, or
`H(668)`.

## 1. Why `167=2*83+1` is special

Let `chi` denote the quadratic character of `F_167`.  Since

```text
167-1 = 2*83
```

and `2` has order `83` modulo `167`, the quadratic residues are

```text
H = <2> = {h_i=2^i : i in Z_83}.
```

This identifies the additive index group `Z_83` with the multiplicative
quadratic-residue subgroup of `F_167`.

For `a in F_167`, define the Sidelnikov-type sequence

```text
S_a(i) = chi(h_i+a).                                    (1)
```

Because `167` is `3 mod 4`, `chi(-1)=-1`.

## 2. Every parameter belongs to one of two phase families

Put

```text
B_i = chi(h_i+1),
Z_i = chi(h_i-1).                                       (2)
```

If `a=h_t` is a nonzero square, then

```text
S_a(i) = chi(h_t) chi(h_(i-t)+1) = B_(i-t).             (3)
```

If `a` is a nonsquare, then `-a=h_t` is a square and

```text
S_a(i) = chi(h_t) chi(h_(i-t)-1) = Z_(i-t).             (4)
```

Thus:

- the `83` nonzero square parameters give the `83` cyclic phases of one
  binary sequence `B`;
- the `83` nonsquare parameters give the `83` phases of one sequence `Z`
  having exactly one zero;
- `S_0` is the constant-one sequence.

The row sums follow without enumeration.  For `a != 0`,

```text
sum_(h in H) chi(h+a)
 = 1/2 sum_(x != 0) (1+chi(x)) chi(x+a)
 = (-chi(a)-1)/2.                                       (5)
```

Consequently

```text
sum B = -1,              sum Z = 0.                     (6)
```

Inversion gives another useful structural fact:

```text
B_(-i) =  B_i,
Z_(-i) = -Z_i.                                          (7)
```

So `B` is symmetric and `Z` is normalized skew with its unique zero at
index zero.

## 3. Exact PAF formula

For a nonzero lag `k`, write `r=h_k` and define the cubic Jacobsthal sum

```text
T_k = sum_(x in F_167) chi(x(x+1)(r*x+1)).              (8)
```

Using the indicator `(1+chi(x))/2` of `H` on nonzero field elements gives

```text
PAF_B(k)
 = 1/2 sum_(x != 0) [1+chi(x)] chi((x+1)(r*x+1)).
```

The first quadratic-character sum is `-2`: its full-field value is `-1`
and the omitted value at zero is `+1`.  The second sum is `T_k`.  Hence

```text
PAF_B(k) = -1 + T_k/2.                                  (9)
```

Replacing `x` by `-x` in the corresponding formula for `Z` changes the sign
of the cubic sum because `chi(-1)=-1`.  Therefore

```text
PAF_Z(k) = -1 - T_k/2.                                 (10)
```

The central identity is:

> **Sidelnikov fold identity.**
>
> ```text
> PAF_B(k) + PAF_Z(k) = -2,       k != 0.              (11)
> ```

Thus `B,Z` are an exact periodic complementary pair, except that `Z`
contains the one zero required by the endpoint fold.

On the independent lags `1,...,41`, the exact distribution of `PAF_B` is

```text
value:       -13  -9  -5  -1   3   7  11
multiplicity:  3   5   7  11   7   5   3.
```

Equivalently the traces `T_k` are

```text
-24,-16,-8,0,8,16,24
```

with the same multiplicities.  The checker verifies (8)--(11) directly in
integer arithmetic for all `82` oriented nonzero lags.

## 4. The direct endpoint-fold construction

In the prime-83 endpoint fold, the normalized vectors have alphabets

```text
U[0]=0,   U[i] in {+1,-1},
V[0]=2,   V[i] in {+1,-1},
C,D       binary.
```

The direct Sidelnikov proposal is:

```text
U = a signed Z, with its zero anchored at coordinate 0;
v = a signed cyclic phase of B;
V[0]=2 and V[i]=v[i] for i != 0;
C,D = independently signed cyclic phases of B.          (12)
```

The `U` sign does not change its PAF.  The `C,D` signs and phases do not
change theirs.  Only the `83*2=166` underlying `V` states affect the periodic
equations.  Restoring all labels gives

```text
2 * 166^3 = 9,148,592
```

phase/sign states.

### 4.1 Trivial-character obstruction

If `delta=2-v[0]`, then `delta` is `1` or `3` and

```text
sum V = sum v + delta.
```

Across the `166` states the exact distribution is

```text
sum V = 0: 41 states,
sum V = 2: 84 states,
sum V = 4: 41 states.
```

Meanwhile

```text
sum U=0,        (sum C)^2=(sum D)^2=1.
```

Periodic complementarity would force

```text
(sum U)^2+(sum V)^2+(sum C)^2+(sum D)^2 = 334.
```

The left side is only `2`, `6`, or `18`.  Thus the whole direct family is
already impossible at the trivial character.

### 4.2 A lagwise modulo-eight obstruction

Changing one binary coordinate gives the exact formula

```text
PAF_V(k)
 = PAF_B(k) + delta (v[k]+v[-k]).                       (13)
```

Using (11), the desired four-block equation becomes

```text
delta (v[k]+v[-k]) = 2 - 2 PAF_B(k).                   (14)
```

For a cyclic binary sequence of odd prime length, the Hamming distance from
any nontrivial shift is even.  Hence

```text
PAF_B(k) = 83 - 2 distance = 3 mod 4.
```

The right side of (14) is therefore `4 mod 8`.  But `delta` is odd and

```text
v[k]+v[-k] in {-2,0,2},
```

so the left side is `0`, `2`, or `6 mod 8`, never `4`.  No nonzero lag can
match.  This second certificate is local and independent of the row-sum
argument.

## 5. Filling the zero does not rescue the construction

Replace `Z[0]=0` by either sign, obtaining binary sequences `F_+` and `F_-`.
Skewness (7) gives

```text
PAF_(F_+)(k) = PAF_(F_-)(k) = PAF_Z(k),       k != 0.  (15)
```

Their row sums are `+1` and `-1`.  Allowing `B,F_+,F_-` as the ordinary
binary blocks still leaves every ordinary squared row sum equal to one, and
a block with one entry raised to `2` still has squared row sum in
`{0,4,16}`.  The total is again only `2`, `6`, or `18`.  The zero-fill
variant is therefore exactly excluded.

## 6. Degree-at-most-two product extension

The next obvious extension takes pointwise products of the two phase
families.  After anchoring the unique zero of `U`, the raw libraries are:

```text
binary:
    B,
    B_i B_(i-t),                  t in Z_83;             84 templates

one-zero:
    Z,
    Z^2,
    Z_i B_(i-t),                  t in Z_83;             85 templates.
```

Products of two distinct phases of `Z` have two zeros and do not have the
endpoint-fold energy, so they are outside this one-zero extension.

The binary library has `43` distinct half-PAF signatures and the one-zero
library has `44`.  The search is an exact signature join:

1. choose one of the `85` one-zero `U` templates;
2. choose one of the `84` binary `V` templates, all `83` phases, and both
   signs, then raise coordinate zero to `2`;
3. hash every unordered pair of the `84` binary templates for `C,D` by its
   combined row norm and its `41`-entry half-PAF signature.

Signs and cyclic phases of `C,D` do not change their PAFs or squared row
sums.  A common decimation merely permutes all lag equations and also adds
nothing.  The complete raw counts are:

```text
C/D template pairs                 3,570
distinct (norm,PAF) C/D keys         946
distinct C/D norm values              33
U/V phase-sign states           1,185,240
U/V states surviving row norms      83,982
exact PAF joins                           0.
```

The five surviving remainder norms and their U/V multiplicities are

```text
 74:  6,300
 90: 13,236
122:  7,056
170: 23,328
218: 34,062.
```

The checker streams the `1,185,240` U/V states and uses only a small
`C/D` signature table.  A reference run completed in about six seconds at
roughly `20 MB` peak RSS.

This is a complete exclusion of the displayed degree-two library, including
all relevant phases and signs.  It is not an exclusion of arbitrary
higher-degree character products or independently decimated blocks.

## 7. What is proved, and what is not

### Proved

- every nonzero `S_a` is a phase of exactly one of `B,Z`;
- the row sums, symmetry types, and exact Jacobsthal PAF formulas;
- the complementary identity (11);
- nonexistence of the `9,148,592`-state direct endpoint-fold family;
- nonexistence of the filled-zero variant;
- absence of a periodic prime-fold match in the stated degree-two product
  extension.

### Not proved

- nonexistence of a prime-83 oriented supplementary difference family;
- nonexistence of `BS(84,83)`;
- nonexistence of a special Golay quadruple of length `167`;
- nonexistence of a Hadamard matrix of order `668`.

Even a periodic prime-fold match would still need the independent modulo-84
fold before it could lift to a base sequence.

## 8. Independent decimations and higher products

The independent-decimation extension proposed here has now been exhausted;
see `PRIME83_SIDELNIKOV_DECIMATIONS.md`.  Its exact quotient contains `1,723`
binary and `1,723` one-zero decimated signatures and `12,584,792` normalized
`U/V` states.  It produces no prime-fold object.

The stronger conclusion is structural.  Modulo four, any solution would
force `U_k U_-k = v_k v_-k` at all `41` inverse pairs.  The two template
fingerprint catalogs intersect only at `U=Z^2`, whose squared row sum already
exceeds `334`.  Thus further multipliers, phases, signs, or PAF-preserving
equivalences cannot rescue this degree-two family.

The next character construction must change those inverse-pair orientation
fingerprints.  Higher-degree or mixed character products should be filtered
first by that condition and by the five compatible row-norm layers above.

`prime83_sidelnikov_higher_products/` applies exactly that filter and then a
complete 41-coordinate integer PAF join.  It excludes the independently
decimated degree-at-most-three family and the un-decimated
degree-at-most-four family.  The former leaves 5,434 row-compatible `U/V`
states and the latter 325,835; neither has a `C/D` completion.  Independent
decimation at degree four, degree five and above, and arbitrary character
products remain open.

## 9. Priority caution

Sidelnikov sequences and Jacobsthal-sum correlation formulas are classical.
The exact application to this anomalous prime fold and the finite exclusion
counts were derived independently from local repository context; no external
novelty claim is made.  No outside contact is to be prepared or attempted.
