# Primitive-eight obstruction for the Eliahou seed

This note gives a dependency-free algebraic obstruction in the live
`BS(84,83)` lane. It proves two sharply scoped statements:

1. Eliahou's published `s` cannot be held fixed while `q` varies arbitrarily.
2. Every exact base sequence is at raw labelled Hamming distance at least 34
   from Eliahou's published base quadruple.

The second result closes the complete raw ball through radius 33 without a
solver. It supersedes the earlier radius-18 solver report as a distance
bound, but it neither constructs nor rules out `BS(84,83)` globally.

## 1. The norm identity over `Q(sqrt(2))`

Let `X` be one of the four base sequences and let

```text
c_r = sum of X_i over i == r (mod 8).
```

At `z=exp(pi*i/4)`, define

```text
x     = c_0-c_4,
y     = c_2-c_6,
alpha = c_1-c_5,
beta  = c_3-c_7.
```

Direct expansion in the basis `1,sqrt(2)` gives

```text
|X(z)|^2
  = x^2+y^2+alpha^2+beta^2
    + sqrt(2) * (alpha*(x+y) + beta*(y-x)).
```

For `(A,B;C,D) in BS(84,83)`, the polynomial norm identity has value
`2(84+83)=334` at every point of the unit circle. Since `sqrt(2)` is
irrational, the sixteen root-eight coordinates must obey the two integer
equations

```text
sum_X (x_X^2+y_X^2+alpha_X^2+beta_X^2) = 334,       (R)
sum_X (alpha_X*(x_X+y_X)+beta_X*(y_X-x_X)) = 0.     (I)
```

Equation `(R)` is a 16-square shell. The coordinate group sizes are

```text
A,B: (21,21,21,21)
C,D: (21,21,21,20).
```

Thus fourteen coordinates are odd signed sums in `[-21,21]`, and the last
coordinate of each short sequence is an even signed sum in `[-20,20]`.

## 2. Exact seed arithmetic

For Eliahou's published base quadruple, the four coordinate vectors are

```text
A = ( 11,-11,19,-1)
B = ( 11,-11,19, 1)
C = ( -9, 11, 1, 0)
D = (-11,  9, 1, 0).
```

Their rational square energy is

```text
604 + 604 + 203 + 203 = 1614,
```

and their irrational coefficients cancel. The exact target is only 334.
This exposes a large obstruction that the previously used primitive
third-, fourth-, and sixth-root filters do not see.

## 3. Fixed `s` is impossible

Holding `s` fixed holds `A=s[:84]` and `C=s[84:]` fixed, even if every sign
of `q` is allowed to change. At the chosen eighth root, these two fixed
sequences alone contribute

```text
|A(z)|^2+|C(z)|^2 = 807 + 24*sqrt(2) > 334.
```

The remaining quantities `|B(z)|^2` and `|D(z)|^2` are nonnegative. They
therefore cannot bring the total down to 334. This proves that an exact
special quadruple cannot retain Eliahou's `s`.

There is also a simpler proof at `z=1`. The fixed sums are `sum(A)=-2` and
`sum(C)=3`, so exactness would require

```text
sum(B)^2 + sum(D)^2 = 334-4-9 = 321.
```

If 3 divides a sum of two squares, it divides both summands; their squares
would then make the left side divisible by 9, whereas 321 is not divisible
by 9. `verify_novel_lifting_64.py` checks this shorter obstruction. The
primitive-eight partial norm above is retained because it arises naturally
from the distance reduction and independently reaches the same conclusion.

This obstruction is independent of the fixed-`q` reduction to `TU(41)`.
Together, the two results show that both published factors must genuinely
move.

## 4. A sharp distance-33 root obstruction

Each of the sixteen coordinates is a sum of independent transformed signs.
Flipping one source sign changes exactly one coordinate by two. If a
coordinate starts at `u` in a group of size `n`, then every target

```text
v in {-n,-n+2,...,n}
```

is reachable, and its exact minimum flip cost is `|u-v|/2`.

Consequently, minimizing raw Hamming distance subject only to `(R)` is the
finite separable problem

```text
minimize  (1/2) * sum_j |u_j-v_j|
subject to sum_j v_j^2 = 334
and the fourteen odd / two even coordinate domains above.
```

`variable_q_root8.py` exhausts this problem by dynamic programming. For
each prefix of the sixteen coordinates it retains the cheapest realization
of every square energy from 0 through 334. Its exact optimum is 33.
Because every base sequence must satisfy `(R)`, no exact `BS(84,83)` can
occur within raw distance 32 of the seed.

The bound is sharp for the complete primitive-eight relaxation, not merely
for `(R)`. The following target has distance 33 and satisfies both `(R)`
and `(I)`:

| sequence | target `(x,y,alpha,beta)` | flip cost |
|---|---:|---:|
| `A` | `(7,-7,7,-1)` | 10 |
| `B` | `(5,-5,5,1)` | 13 |
| `C` | `(-7,5,1,0)` | 4 |
| `D` | `(-5,3,1,0)` | 6 |

The target's rational contributions are `148,76,75,35`, summing to 334;
its irrational contributions are `14,-10,-2,-2`, summing to zero. The
checker explicitly realizes these coordinate vectors by 33 source-sign
flips and rechecks both equations.

This distance-33 witness is only a witness for the root-eight relaxation. It
is not a base sequence and is not a Hadamard candidate.

## 5. Exact margins raise the bound to 34

Every exact base sequence also satisfies the two rational norm identities

```text
sum_X sum(X)^2 = 334,
sum_X altsum(X)^2 = 334.
```

The root sphere has exactly 1,350 coordinate targets at its minimum distance
33. Exactly 66 of them also satisfy the irrational equation `(I)`.
For each of those 66 targets, the checker exhausts all ordinary and
alternating sums attainable at the same minimum cost. None satisfies both
margin norm identities. Therefore every exact base sequence has raw distance
at least 34.

This stronger necessary-condition bound is sharp. The checker stores an
explicit distance-34 sign witness with:

```text
root-eight coordinates:
A ( 3,-7,5,-1)   B ( 5,-5,7,-1)
C (-7, 5,1, 0)   D (-5, 7,1, 0)

(ordinary, alternating) margins:
A (-8,-8)   B (14,-14)   C (-5,-7)   D (7,5).
```

Both margin square sums are 334, both primitive-eight equations hold, and all
83 mandatory endpoint-quad products agree with the seed. The witness still
has 57 bad full-correlation lags and is explicitly rejected as nonexact.
Thus radius 34 is the first shell surviving all of these inexpensive exact
invariants.

## 6. Search consequence

The exact CP-SAT model now includes `(R)` and `(I)` by default. They are
logical consequences of the full 83 lag equations, so they remove no exact
solution. Their purpose is propagation: the entire 16-square energy budget
is visible before the individual correlation XORs settle.

The old seed-centered program should not be extended shell by shell from
radius 18. Radius 34 is the first shell surviving the primitive-eight
equations, exact margins, and endpoint-quad constraints. A useful continuation
must begin from this compressed shell rather than replaying the obsolete
smaller balls.

## Reproduce

```sh
python3 variable_q_root8.py
python3 -m unittest -v test_variable_q_root8.py
```

Expected summary:

```text
seed_root8=1614
fixed_s_partial_root8=807+24*sqrt(2)>334
minimum_raw_base_distance_to_root8_sphere=33
distance33_rational_shell_targets=1350
distance33_full_root8_targets=66
minimum_raw_base_distance_with_exact_margins=34
PASS primitive-eighth-root obstruction and sharp margin distance bound
```
