# LP(333) order-three difference-family lift

## Status

One exact row-sum word in the viable order-three multiplier projection lifts
to twelve QPSK cyclotomic class words that satisfy:

- the alternating fixed compression `-3i,+3i`;
- the prescribed complete row-sum PAF;
- every zero-column-lag correlation equation.

The lift has a small equivalent description as 24 cyclic triples in
`Z/9`. This is a finite, exact compatibility result for two strong
projections of the order-three lane.

It is **not** an `LP(333)` candidate. At nonzero column lag, 51 of its 54
reversal-independent equations fail. In particular, its geometric
column-axis equations (`a=0`, `b!=0`) all fail. The artifact must therefore
be described as a pure-axis lift, not as a Legendre pair, a Hadamard matrix,
or a near construction.

All statements in this note are replayed with standard-library-only exact
integer arithmetic by `verify_lp333_order3_difference_family.py`.

## 1. Order-three quotient

Let

```text
H = <2^12> = {1,26,10} in F_37^*
```

and write

```text
C_j = 2^j H,                  j=0,...,11.
```

An `H`-invariant QPSK quotient consists of a zero-column word `x` and twelve
class words `z_j`, each of length nine. We use the canonical zero word

```text
x = (0,0,0,1,2,3,1,3,2)
```

in exponent-of-`i` notation. It has phase sum one and real PAF `-1` at every
nonzero lag.

The fixed Legendre compression requires

```text
sum_r z_j(r) = -3i   for j even,
sum_r z_j(r) = +3i   for j odd.                 (1)
```

The complete CRT-row sum is

```text
s_r = x_r + 3 t_r,       t_r = sum_j z_j(r).    (2)
```

The exact row-sum catalog contains 1,756 words satisfying

```text
Re PAF_s(0) = 297,
Re PAF_s(a) = -37,       a=1,...,8.              (3)
```

Its byte-level SHA-256 is

```text
e8631dc0ae2f65c475af1c2e13429778f666a0fa8a13c9f1153d07d7883a98ea
```

The lift below uses zero-based data-row index `695`.

## 2. Reduction to 24 cyclic triples

Represent a fourth root by two binary signs:

```text
z = (A+B + i(B-A))/2,       A,B in {+1,-1}.      (4)
```

Equation (1) fixes the binary weights:

```text
             A plus-weight       B plus-weight
j even             6                   3
j odd              3                   6.
```

Complement the high-weight channel: complement `A` in each even class and
`B` in each odd class. Every resulting binary word is then the sign word of
a three-subset `S` of `Z/9`. Thus the twelve QPSK words become 24 cyclic
triples in four groups:

```text
A_even, A_odd, B_even, B_odd.
```

Let `E_A(r),O_A(r),E_B(r),O_B(r)` count block incidences at row `r` in these
four groups. Summing (4) over the twelve classes gives the exact row
constraints

```text
O_A(r)-E_A(r) = (Re t_r-Im t_r)/2,
E_B(r)-O_B(r) = (Re t_r+Im t_r)/2.               (5)
```

These are signed degree constraints on four six-block, three-uniform
hypergraphs.

For a plus-weight-three sign word with support `S`,

```text
PAF_S(a) = -3 + 4 |S intersect (S-a)|.           (6)
```

Complementation does not change a binary autocorrelation. Also, (4) gives

```text
2 Re PAF_z(a) = PAF_A(a)+PAF_B(a).
```

Consequently, across all 24 normalized triples,

```text
sum_j Re PAF_z_j(a)
  = -36 + 2 sum_S |S intersect (S-a)|.           (7)
```

The zero-column-lag equations require the left side of (7) to vanish.
Therefore the QPSK signature condition is equivalent, with no relaxation,
to the cyclic difference-family condition

```text
sum over 24 blocks |S intersect (S-a)| = 18,
                                      a=1,2,3,4. (8)
```

The verifier checks (4) locally for all 16 phase pairs, checks (6) for all
84 three-subsets and four lags, and then checks (5)--(8) on the witness.

## 3. Frozen certificate

Block IDs refer to

```python
list(itertools.combinations(range(9), 3))
```

in lexicographic order. Within a group, the six IDs correspond to the six
classes of the indicated parity in increasing class order.

| group | block IDs |
|---|---|
| `A_even` | `45, 60, 43, 55, 42, 11` |
| `A_odd` | `56, 30, 55, 53, 43, 81` |
| `B_even` | `61, 62, 13, 34, 21, 26` |
| `B_odd` | `41, 49, 81, 6, 6, 25` |

Reconstructing and undoing the two complementations gives the twelve class
words, in class order `j=0,...,11`:

```text
[3,2,0,3,3,2,0,0,2]
[1,2,0,1,3,1,1,3,1]
[3,3,1,3,3,2,0,3,1]
[1,0,3,2,2,0,1,1,1]
[0,2,3,0,0,2,2,3,3]
[1,1,0,1,0,2,3,1,2]
[3,0,2,0,1,3,2,3,3]
[2,2,0,0,1,1,1,1,3]
[0,2,3,3,1,3,3,3,1]
[2,3,1,1,1,0,0,1,2]
[1,3,2,3,3,3,0,2,0]
[2,1,1,1,1,0,3,2,0].
```

Their phase sums alternate `-3i,+3i`, their four real-PAF signatures sum to
zero, and their 24 difference totals are

```text
(18,18,18,18).
```

The resulting aggregate and row-sum words are

```text
t = [(-1,1), (-3,-1), (2,0), (2,0), (1,1),
     (-1,-1), (2,0), (-1,-1), (-1,1)]

s = [(-2,3), (-8,-3), (7,0), (6,1), (2,3),
     (-3,-4), (6,1), (-3,-4), (-4,3)].
```

Expanding the quotient to all `9*37=333` positions verifies:

```text
sum q = 1,
sum A = sum B = 1,
Re PAF_s = (297,-37,-37,-37,-37,-37,-37,-37,-37),
C(a,0) = -1 for a=1,...,8.
```

Here

```text
C(a,b) =
  sum_(r,c) Re(q(r,c) conjugate(q(r+a,c+b))).
```

## 4. Exact non-candidate audit

For a genuine `LP(333)`, every nonzero two-dimensional shift must have
`C(a,b)=-1`. Define the residual

```text
E(a,b)=C(a,b)+1.
```

For one representative of each `C_j`, the pinned residual rows
`a=0,...,4` are:

```text
a=0: -6,  8,-12, 20, -4, -6, -6,  8,-12, 20, -4, -6
a=1:-12,  8, -4,-22, 12, 30,  2,  2, -2,-12, -8,  6
a=2: -4,  0, 28, 12, 10,  8,-10,  6, -8,  6,-30,-18
a=3:  0,-20, -8,-12, -2, -4, 22, 12, -2, -2, 14,  2
a=4: -6,-14,  0, 20, 18,-10, 14, -2,  8,-10,-10, -8.
```

At `a=0`, reversal duplicates the last six entries; at `a=1,...,4`, all
twelve are independent under reversal. Hence there are

```text
6 + 4*12 = 54
```

reversal-independent nonzero-column class equations. Exactly 51 are bad,
with

```text
sum E^2 = 8320,       max |E| = 30.
```

Each displayed residual row has weighted sum zero:

```text
3 sum_j E(a,C_j) = 0.
```

This cancellation is expected from the exact row-sum projection; it does not
make the individual equations true. The verifier expands all 333 entries,
checks every representative in all twelve cyclotomic classes, audits
reversal, pins the full residual matrix and its hash, and explicitly asserts
non-candidate status.

## 5. Scope

What is established:

- The order-three row-sum projection and the zero-column-lag equations are
  jointly feasible.
- Their joint lift has an exact 24-block cyclic difference-family
  formulation with signed incidence constraints.
- A complete, small witness is independently replayable.

What is not established:

- The witness does not solve the nonzero-column equations.
- It is not an `LP(333)`.
- It does not construct `H(668)`.
- Feasibility of this projection does not imply feasibility of the full
  order-three multiplier family.

Run:

```sh
python3 verify_lp333_order3_difference_family.py
python3 -m unittest -v test_lp333_order3_difference_family.py
```
