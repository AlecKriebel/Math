# Primitive support of the six order-three phase fibers

## Status

For an exact order-three phase frame

```text
E0 = sum_i U_i U_i* = 167 e,
```

each of the six `H`-invariant words `U_i` has coefficients in zero plus the
six Eisenstein units.  This physical alphabet imposes a sharp constraint on
the two prime-167 primitive coordinates:

```text
U_i = 0
    if and only if x_i = 0
    if and only if y_i = 0.                            (1)
```

Five words are nonzero already at the fixed zero column.  The only optional
word is `U_B0`.  Consequently

```text
zero support of x = zero support of y
                  = empty or {B0}.                    (2)
```

Thus the primitive three-plane is not allowed to use arbitrary coordinate
degeneracies.  Of the `4^6=4096` joint zero/nonzero patterns for `(x,y)`,
exactly two remain.  This is an exact physicality obstruction and a useful
search cut.  It is not a profile, an `LP(333)`, or an `H(668)`.

## 1. A nonzero fiber has no zero primitive complex value

Let

```text
K = Q(omega),
L = K(zeta_37),
H = {1,10,26},
F = L^H.
```

The polynomial `Phi_37` is irreducible over `K`.  The verifier gives a
short reduction certificate: `13` splits in `Z[omega]`, one residue map is
`omega -> 3`, and `Phi_37` is irreducible over `F_13`.  Rabin's criterion
is checked directly in degree 36; equivalently, `13` has order 36 modulo
37.

Regard one phase word as a polynomial of degree at most 36,

```text
U(X) = sum_(j=0)^36 u_j X^j.
```

If `U(zeta_37^a)=0` for one primitive exponent `a`, irreducibility forces

```text
U(X) = q Phi_37(X),              q in K.               (3)
```

The coefficients of `U` lie in zero plus the Eisenstein units.  Hence
either `q=0`, so `U=0`, or every coefficient is the same Eisenstein unit.
The latter is impossible in an exact frame: its trivial Fourier value is
`37q`, of squared modulus

```text
37^2 = 1369 > 167,
```

whereas evaluation of `E0=167e` at the trivial character gives

```text
sum_i |U_i(1)|^2 = 167.                               (4)
```

Therefore every primitive complex Fourier value of every nonzero `U_i` is
nonzero.  The argument works at all primitive exponents, not just at a
chosen representative.

Order-three invariance makes `U(zeta_37)` lie in `F`, whose degree over
`K` is `36/3=12`.  It is used below to make the norm have exactly twelve
factors.

## 2. The strict twelve-factor norm gap

Fix a nonzero `U_i` and put

```text
alpha = U_i(zeta_37) in O_F.
```

The fixed zero column makes

```text
U_A0, U_A1, U_A2, U_B1, U_B2
```

nonzero.  Thus, for every choice of `i`, some other word `U_j` is nonzero.
Section 1 says that both words remain nonzero at every primitive complex
embedding.  Evaluating the diagonal equation at the twelve embeddings of
`F/K` gives, for each embedding `sigma`,

```text
0 < |sigma(alpha)|^2 < 167.                           (5)
```

The strict upper bound uses the positive contribution of `U_j`; this is
where the five forced nonzero words close the equality edge case.
Multiplication over the twelve embeddings yields

```text
0 < |Norm_(F/K)(alpha)|^2 < 167^12.                   (6)
```

The middle quantity is the ordinary Eisenstein norm of an element of
`Z[omega]`, so it is a positive integer.

## 3. Why a zero prime-167 coordinate contradicts the gap

The rational prime 167 is inert in `K`, so the prime ideal `(167)` has norm
`167^2`.  On the twelve cosets of `H` in `(Z/37Z)^*`, multiplication by
`167^2` has two orbits, each of length six.  Therefore `(167)` has two
primes in `F`, both with relative residue degree six:

```text
O_F / P_x = F_(167^12),
O_F / P_y = F_(167^12).                               (7)
```

These are precisely the two primitive coordinates `x_i` and `y_i` in the
finite-field split.

If, for example, `x_i=0`, then `alpha` lies in `P_x`.  The ideal norm
formula forces

```text
Norm_(F/K)(alpha) in (167)^6.
```

Taking its Eisenstein norm makes the positive integer in (6) divisible by

```text
Norm_K/Q((167)^6) = (167^2)^6 = 167^12.               (8)
```

This contradicts (6).  The same proof applies to `P_y`.  Conversely the
zero word plainly has both primitive coordinates zero, proving (1).

No cancellation or equality case is hidden here: irreducibility makes the
field norm nonzero, another forced word makes every energy inequality
strict, and the residue degree supplies exactly the divisibility exponent
needed to meet the strict upper threshold.

## 4. Exact pruning of the three-plane

Before physicality, each of six positions can have four joint states:

```text
(x_i,y_i) = (0,0), (0,nonzero), (nonzero,0),
             or (nonzero,nonzero).
```

There are therefore `4^6=4096` joint zero patterns.  Equality of the two
zero supports removes 4,032 mismatched patterns.  Of the remaining 64
matching patterns, fixed zero-column activity removes 62.  The survivors
are exactly:

```text
all six coordinates nonzero;
B0 zero in both vectors, all other coordinates nonzero. (9)
```

In the three-plane notation

```text
z = sigma(y),
W(z) = span {z, bar(P)z, bar(P)^2 z},
x in W(z)^perp,
```

Frobenius preserves the same zero support.  Rank zero is impossible.  If
`W(z)` has rank one, the zero set of `z` must be invariant under the two
three-cycles of `bar(P)`; within each channel either all three coordinates
vanish or none do.  Hence the `B0`-zero branch has

```text
rank W(z) >= 2,                                        (10)
```

while the dense branch can still have rank one.  The theorem does **not**
force rank three: over `F_(167^12)` there are ninth roots, so dense
eigenvector configurations remain algebraically possible.  It removes
coordinate-degenerate branches rather than solving the surviving
three-plane equations.

## 5. Search value

The result supplies exact no-zero clauses for ten always-active primitive
coordinates and a single synchronized optional pair at `B0`.  It deletes
all global and one-sided degenerate branches of the finite-field
annihilator and strengthens the `B0`-zero branch to plane rank at least
two.

Its limitation is equally clear.  Nonzero field coordinates need not come
from zero/unit physical words, and the two surviving support strata are
still enormous.  The theorem is best used before inverse-CRT alphabet
decoding: reject every spectral tuple with a mismatched zero, a zero
outside `B0`, or a rank-one `B0`-zero plane, then apply the stronger trace
and coefficient tests.

## Reproduction

```text
python3 verify_lp333_order3_phase_fiber_support.py
python3 -m unittest -v test_lp333_order3_phase_fiber_support.py
```

The verifier uses only the Python standard library.

Pinned certificate:

```text
c15e8357dc55e49f63469888dc306113165cf39c0cfc19b66aec15c747b2669e
```
