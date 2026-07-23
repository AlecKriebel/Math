# A theory-first route to `BS(84,83)`

## Status and scope

No `BS(84,83)` and hence no Hadamard matrix of order 668 is constructed
here.  The useful outcome is a new exact formulation of the problem as the
intersection of two adjacent cyclic difference-family problems:

```text
an order-84 padded periodic complement
                  ∩
an order-83 endpoint-folded periodic complement.
```

Either cyclic condition by itself is only a relaxation.  Together they are
**equivalent** to all 83 aperiodic base-sequence equations.  At the prime
modulus 83, the second condition has an exact oriented supplementary
difference-set formulation on the 41 inverse pairs of
`Z/83Z`.  It also has a characteristic-two norm formulation over
`GF(2^82)/GF(2^41)`.

These observations suggest a construction program that is materially
different from searching 334 unrestricted signs.  First construct the
prime-83 oriented difference family, using its 41-pair and finite-field norm
structure.  Then try the finite cyclic phases and multipliers that can make
the order-84 fold complementary.  The adjacent-fold theorem says that a
successful join is already an exact `BS(84,83)`; there is no final
aperiodic solver stage.

`check_bs84_cyclic_folds.py` checks every identity in this note, exhausts the
general theorem for small lengths, and records two finite character-template
experiments.

This is an internal research note.  I have not established whether the
adjacent-fold or oriented-SDS formulations have appeared elsewhere, so no
priority claim is made.

## 1. The original identity

Let

```text
|A|=|B|=84,       |C|=|D|=83,
```

with every entry in `{+1,-1}`.  Write

```text
R_k = c_k(A)+c_k(B)+c_k(C)+c_k(D),     0 <= k <= 83,
```

where a term is omitted once the lag reaches the length of its sequence.
Then

```text
R_0=334,
```

and `(A;B;C;D)` is in `BS(84,83)` exactly when

```text
R_1=...=R_83=0.                                      (1)
```

The existing variable-`q` lane, its margin shards, endpoint-quad products,
and its factor-84 compressions all concern this identity.

## 2. The adjacent cyclic-fold theorem

The statement is cleaner for a general `BS(n+1,n)`.

### Theorem 1 (adjacent cyclic folds)

Let `A,B` be binary sequences of length `n+1`, let `C,D` be binary
sequences of length `n`, and define `R_k` as above.

Form two cyclic quadruples.

1. **The modulo-`n+1` padded fold**

   ```text
   A, B, (C,0), (D,0),       all of length n+1.
   ```

2. **The modulo-`n` endpoint fold**

   ```text
   A^ = (a_0+a_n,a_1,...,a_(n-1)),
   B^ = (b_0+b_n,b_1,...,b_(n-1)),
   C, D,                     all of length n.
   ```

Then `(A;B;C;D)` is in `BS(n+1,n)` if and only if both cyclic quadruples
have summed periodic autocorrelation

```text
(4n+2,0,...,0).                                      (2)
```

### Proof

For `1 <= k <= n`, wrapping the padded length-`n+1` vectors gives

```text
P_(n+1)(k) = R_k + R_(n+1-k).                        (3)
```

For the endpoint fold,

```text
P_n(0) = R_0 + 2R_n,                                 (4)
P_n(k) = R_k + R_(n-k),       1 <= k < n.            (5)
```

These are coefficient identities, not spectral approximations.

If every positive `R_k` is zero, (2) follows immediately.  Conversely,
the required energy in (4) first gives `R_n=0`.  Equations (3) and (5)
then give

```text
R_(n+1-k)=R_(n-k),       1 <= k < n.
```

Thus

```text
R_n=R_(n-1)=...=R_1=0.
```

This proves the equivalence.  The checker verifies (3)--(5) on random
integer fixtures and exhausts every binary quadruple for `n=1,2,3`.

### Why this is useful

The factor-84 compression work used only the first cyclic image and then
compressed it to small divisors of 84.  The endpoint fold is different:
it is a full cyclic condition at the adjacent prime 83.  Most importantly,
the two cyclic conditions are not merely simultaneous necessary tests.
Their intersection is the exact aperiodic target.

For `n=83`, the first fold has two binary length-84 vectors and two
length-84 vectors with one zero.  The second fold has two anomalous
length-83 vectors and two binary vectors.  Both are group-ring objects,
so cyclic difference-family constructions and multipliers become directly
relevant.

## 3. The prime-83 fold as an oriented SDS

The energy equation in the endpoint fold forces

```text
a_0 a_83 + b_0 b_83 = R_83 = 0.
```

One long sequence therefore has opposite endpoints and the other has equal
endpoints.  After exchanging and negating the long sequences, normalize the
folded vectors as

```text
U_0=0,       V_0=2.
```

Let `G=Z/83Z`.  Describe the negative entries by subsets

```text
X,Y subset G\{0},       Z,W subset G,
```

so that

```text
U_i = 1-2[ i in X ]       (i != 0),   U_0=0,
V_i = 1-2[ i in Y ]       (i != 0),   V_0=2,
C_i = 1-2[ i in Z ],
D_i = 1-2[ i in W ].
```

For a block `T`, put

```text
d_T(g) = |{t in T : t+g in T}|,
e_T(g) = [g in T]+[-g in T].
```

### Theorem 2 (oriented supplementary difference sets)

The prime-83 fold is periodic complementary if and only if, for every
nonzero `g in G`,

```text
d_X(g)+d_Y(g)+d_Z(g)+d_W(g)
       +(e_X(g)-e_Y(g))/2
     = |X|+|Y|+|Z|+|W|-83.                           (6)
```

In particular,

```text
e_X(g) == e_Y(g)  (mod 2).                           (7)
```

### Proof

For nonzero `g`, direct expansion gives

```text
PAF_U(g) = 83-2-4|X| +2e_X(g)+4d_X(g),
PAF_V(g) = 83+2-4|Y| -2e_Y(g)+4d_Y(g),
PAF_C(g) = 83  -4|Z|          +4d_Z(g),
PAF_D(g) = 83  -4|W|          +4d_W(g).
```

Their sum is zero exactly when (6) holds.  Its integrality gives (7).
The checker compares this formula with direct periodic autocorrelation on
random subsets.

Equation (7) is the prime-fold image of the familiar endpoint-quad parity.
The exact integer equation (6), however, is much stronger.  It asks for a
supplementary difference family with a signed charge on each inverse pair:

```text
+1  if X contains both of {g,-g} and Y contains neither,
-1  in the opposite case,
 0  otherwise.
```

That is why “oriented SDS” is an apt internal name.

### Size profiles

Write

```text
x=|X|, y=|Y|, z=|Z|, w=|W|.
```

The four folded row sums are

```text
82-2x,   84-2y,   83-2z,   83-2w,
```

and hence

```text
(82-2x)^2+(84-2y)^2+(83-2z)^2+(83-2w)^2=334.         (8)
```

There are 672 raw size tuples satisfying (8).  The sign of `V` is fixed by
`V_0=2`, while `U,C,D` may be negated and `C,D` exchanged.  Requiring

```text
sum(U)>=0,       sum(C)>=sum(D)>=0
```

leaves exactly **45 anchored-canonical size profiles**.  These are the
natural top-level shards for an oriented-SDS construction; they are not the
same as the 288 ordinary/alternating aperiodic margin shards.

## 4. The characteristic-two norm shadow

The prime 83 has a particularly favorable arithmetic property:

```text
ord_83(2)=82,       2^41 == -1 (mod 83).              (9)
```

Consequently the cyclotomic polynomial

```text
Phi_83(t)=1+t+...+t^82
```

is irreducible over `GF(2)`.  Let

```text
F = GF(2)[t]/(Phi_83) = GF(2^82),
q = 2^41.
```

At a primitive element `xi`, inversion is the relative conjugation

```text
f(xi^-1)=f(xi)^q.
```

Let the capital letters also denote the integral set polynomials evaluated
at a complex primitive 83rd root.  The folded norm identity is

```text
(-1-2X)(-1-2X*) +(1-2Y)(1-2Y*)
       +4ZZ*+4WW* =334.
```

After subtracting 2 and dividing by 2,

```text
X+X* -Y-Y* +2(XX*+YY*+ZZ*+WW*)=166.                 (10)
```

Condition (7) makes

```text
H=(X+X* -Y-Y*)/2
```

an integral inverse-symmetric polynomial.  Reducing (10) modulo 2 gives
the 41-dimensional subfield equation

```text
h + x x^q + y y^q + z z^q + w w^q = 1
                                      in GF(2^41).   (11)
```

Every quadratic term in (11) is the relative norm

```text
N_F/GF(2^41)(r)=r^(q+1).
```

### Consequence

Once `x,y,z` and the pair charge `h` are selected, (11) puts `w` in one
relative-norm fiber.  A nonzero fiber has exactly

```text
q+1 = 2^41+1
```

elements, a coset of the norm-one circle.  Thus the mod-2 shadow of the
fourth 83-bit block can be parameterized by about 41 bits rather than
chosen as another unrestricted block.  The two subsets represented by
complementary 83-bit incidence vectors give the same element of `F`,
because `Phi_83(xi)=0`; the required block size chooses between them when
possible.

Equation (11) is not by itself an existence theorem.  It is the algebraic
first layer of the exact integer equations (6).  Its value is a
construction parameterization and a strong consistency check, not an
obstruction.

## 5. Exact lift from the prime fold

Suppose an oriented SDS satisfying (6) has been found.

1. Reconstruct `U,V,C,D`.
2. Unfold

   ```text
   U_0=0  -> A_0=1, A_83=-1,
   V_0=2  -> B_0=1, B_83= 1,
   ```

   with coordinates 1 through 82 unchanged.
3. Test the modulo-84 padded cyclic equations.

By Theorem 1, a pass in step 3 is already an exact `BS(84,83)`.

There is a useful finite lift portfolio before discarding an oriented SDS.

- Translating `C` or `D` independently in `Z/83Z` preserves its individual
  periodic autocorrelation, hence preserves (6).  This gives `83^2=6,889`
  relative phase choices.
- A common multiplier `i -> r i`, `r in (Z/83Z)^*`, preserves the entire
  oriented SDS and fixes the two anomalous coordinates.  This gives 82
  multiplier choices.
- Negating or exchanging `C,D` also preserves their PAFs.

Thus one prime-fold object gives at most

```text
82 * 83^2 = 564,898
```

basic phase/multiplier lifts, each checked by only the 42 distinct
modulo-84 PAF lags.  This is tiny compared with a new 334-sign search and
parallelizes without large solver state.

## 6. Derived construction experiments

### 6.1 Quadratic-character template: excluded

The first exact template used the Legendre character `chi` modulo 83:

```text
U_i = chi(i),
B_(t,a)(i) = chi((i-a)^2-t),       chi(t)=-1.
```

The polynomial in `B_(t,a)` has no root, so it is binary.  `V` is obtained
by replacing coordinate zero of either sign of such a block by 2; `C,D`
are two more quadratic blocks.  A PAF-signature join checks all 41
nonsquare parameters and all translations exactly.

There is no prime-fold match.  In fact the row sums already explain the
failure: every ordinary quadratic block in this family has row-sum
magnitude 1, while `U` has sum 0 and the possible anomalous `V` sums still
leave no representation of the remaining square required by (8).  The
full PAF scan is retained as a regression.

### 6.2 Root-free cubic-character template: excluded

The more serious family uses the two affine square classes of depressed
monic cubics

```text
f_(a,t)(i)=i^3+a*i+t,       a in {1,2},
```

where 2 is a nonsquare modulo 83.  Only root-free cubics are retained, and

```text
B_(a,t)(i)=chi(f_(a,t)(i))
```

is then binary.  This family has the row-sum diversity absent from the
quadratic family: its ordinary row sums cover every needed odd magnitude
from 1 through 17 (within the family actually attained).

The exact template was:

```text
U_i = chi(i) B_(a,t)(i-s)   for i != 0,   U_0=0,
V_i = +/- B_(b,u)(i-r)      for i != 0,   V_0=2,
C,D = root-free cubic blocks.
```

Translations of `C,D` do not change their PAF signatures.  Identical
`(row sum, PAF)` states were merged, then an exact two-pair signature join
was performed.  The checked counts are

```text
root-free cubic templates                  56
distinct U states                       2,324
distinct V states                       4,648
row-compatible U/V signature joins  3,013,755
prime-fold matches                           0
```

This rules out only the displayed character family.  It does not rule out
oriented SDSs, base sequences, or more general character combinations.

Reproduce both finite scans with

```sh
python3 check_bs84_cyclic_folds.py --quadratic-scan --cubic-scan
```

The complete run is deterministic, uses exact integers, takes about
11 seconds on the present machine, and stays below 30 MB RSS.

## 7. Failed composition ideas

These failures are worth recording so they are not rediscovered as
“obvious doublings.”

### 7.1 A universal diagonal interleaving cannot work

For

```text
I(P,Q)=(p_0,q_0,p_1,q_1,...),
```

the pair

```text
I(P,Q), I(P,-Q)
```

cancels every odd-lag cross term and contributes

```text
2(N(P)+N(Q))
```

at even lags.  Applying this independently to the long and short pairs
would reduce `BS(84,83)` to four complementary binary sequences of lengths

```text
42,42,42,41.
```

That reduced object is impossible: at lag one it has

```text
3*(42-1)+(41-1)=163
```

binary product terms, an odd number, so their sum cannot be zero.

### 7.2 `BS(42,41)` does not automatically double

Wang and Zhu recently exhibited the first `BS(42,41)`.  A length-two
Golay/interleaving kernel doubles its norm energy from 166 to 332, but the
target energy is 334 and the two added endpoint signs create uncancelled
cross terms.  Appending signs to two sequences of a complementary
quadruple preserves complementarity only under a strong pointwise mate
relation; a generic base sequence does not have it.

Several bordered interleavings were derived.  In every universal version,
either:

- the lag-83 endpoint equation has the wrong sign;
- the added endpoint leaves a nonzero copy of a 41-sign sequence in the
  odd-lag cross polynomial; or
- cancellation requires two source sequences to be equal up to sign or
  reversal, reducing to a normal/Turyn-like subclass.

The independent `TU(41)=empty` certificate already warns against forcing
that much symmetry.  A half-size construction could still exist with an
additional nontrivial cross-correlation mate, but no universal
`BS(42,41) -> BS(84,83)` law was found.

### 7.3 Four unmodified Legendre blocks miss by one

For `p=83`, a modified Legendre binary sequence has periodic
autocorrelation `-1` at every nonzero lag.  Four such blocks therefore sum
to `-4`, not zero.  Adding zero to the Paley difference set changes every
difference count from 20 to 21, but four Paley-type blocks still miss the
Hadamard SDS parameter by exactly one.  The two anomalous long-fold
coordinates do not repair this with unmodified Paley interiors; the
corresponding remaining two row sums would have to satisfy

```text
c^2+d^2=330,
```

which is impossible because 330 is not a sum of two integer squares.

## 8. Conjectures and heuristics

These are explicitly not proved.

### Conjecture A: a prime-fold object exists

At least one of the 45 anchored size profiles admits an oriented SDS
satisfying (6).  This is substantially weaker than the existence of
`BS(84,83)`, but it is the first clean construction milestone.

Evidence is only indirect: every factor-84 compression shard survives, and
the unrestricted base-sequence conjecture predicts abundance.  The failed
quadratic and cubic character templates show that the oriented charge
cannot be supplied by the most rigid Paley/elliptic families.

### Conjecture B: cyclic phase freedom is enough for a lift

For some oriented SDS, a common multiplier and independent cyclic phases of
`C,D` make the modulo-84 fold complementary.  There is no statistical
evidence for this yet; it is a focused construction hypothesis motivated by
the 564,898 exact lifts available per prime-fold object.

## 9. The precise next construction attempt

The next implementation should be an **oriented-SDS constructor**, not
another full aperiodic CP-SAT run.

### Stage A: construct the prime-83 fold

Process the 45 anchored size profiles independently.

1. Use one state for each inverse pair `{g,-g}` to impose (7) at the
   variable-definition level.
2. Represent the fourth block through the relative norm equation (11):
   after `X,Y,Z` are chosen and the target norm is nonzero, write

   ```text
   w = w_0 u,       u^(2^41+1)=1.
   ```

   Parameterize the norm-one circle by a 41-bit subfield element rather
   than 82 unrelated bits.  If the target norm is zero then `w=0` in the
   field, with only the incidence-vector/complement ambiguity left.
3. Impose the 41 distinct exact integer equations (6), one for each
   inverse pair.  Use the fixed block sizes from (8), common-multiplier
   normalization, and a canonical first nonzero pair state.
4. Emit each oriented SDS with a direct integer verifier and its complete
   PAF vector.

This can reasonably use several gigabytes of RAM.  A practical ceiling on
the 16 GB host is 10--12 GB RSS, leaving room for the operating system.
The expensive object should be a hash join of pair-difference signatures
or a Boolean circuit for the 41-bit norm-circle parameter, not an
enumeration of its `2^41+1` elements and not a monolithic 334-sign branch
tree.

### Stage B: exact adjacent-fold join

For every Stage-A object:

```text
for common multiplier r in F_83^*:
    for shift_C in Z_83:
        for shift_D in Z_83:
            unfold the anomalous endpoints
            test the 42 distinct modulo-84 PAF equations
```

Include `C/D` exchange and the independent PAF-preserving sign choices.
If the modulo-84 test passes, Theorem 1 certifies every `R_k=0`; run the
existing `verify_variable_q.py` path to produce and verify the
`668 x 668` Goethals--Seidel matrix.

This gives an unambiguous intermediate finish line:

```text
first exact oriented SDS at 83,
then first simultaneous 83/84 cyclic complement,
then H(668).
```

## References used for orientation

- `VARIABLE_Q_LANE.md`, `VARIABLE_Q_COMPRESSION.md`, and
  `VARIABLE_Q_JOINT_COMPRESSION.md` in this repository.
- X. Wang and J. Zhu, *On Base, Normal and Near-normal Sequences*,
  [arXiv:2506.20296](https://arxiv.org/abs/2506.20296), current v3
  (2026).  It gives explicit `BS(42,41)`, `BS(43,42)`, and `BS(44,43)`
  representatives.
- D. Ž. Đoković, *Classification of base sequences `BS(n+1,n)`*,
  [arXiv:1002.1414](https://arxiv.org/abs/1002.1414), for the standard
  base-sequence equivalences and quad language.
