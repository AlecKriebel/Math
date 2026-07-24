# LP(333) order-three primitive-nine ramified jet

## Status

The order-three multiplier quotient has a new exact necessary condition at a
primitive ninth root.  It lives in the six-coefficient local ring

```text
F_3[pi]/(pi^6),             pi = 1-zeta_9.
```

Coefficient zero is automatic.  Coefficient one is exactly the local
Eisenstein negation-pair sieve already obtained from the three-row
compression.  Coefficients two through five retain information inside the
three rows of each residue class and introduce nonzero/nonzero cyclotomic
class products.  They are therefore a genuine primitive-nine refinement.

An explicit lift of one aggregate/origin/local-mod-3 survivor passes
coefficients zero and one but fails a higher coefficient.  This proves that
the new layers are nonredundant.  It does **not** exclude any of the 1,756
row-sum catalog entries: applying the mixed jet requires a labeled
twelve-class lift, not merely a row-sum word.  It is not an `LP(333)`, a
Hadamard matrix, or an infeasibility proof.

Every claim below is replayed using exact integer and finite-ring arithmetic
by `verify_lp333_order3_primitive9_jet.py`.

## 1. Plus-support group ring

Let `P,Q` be the plus supports of a Legendre pair of length 333.  Both have
size 167, and their difference-family identity is

```text
P P^(-1) + Q Q^(-1) = 167 G + 167 e.             (1)
```

Use the CRT group

```text
Z/333 = Z/9 x F_37
```

and evaluate only the `Z/9` coordinate at a primitive ninth root `z`.
Writing

```text
A(u) = sum_c A_c(z) u^c,
B(u) = sum_c B_c(z) u^c,
```

the nontrivial row character kills the `Z/9` group sum in (1), leaving

```text
A A* + B B* = 167 e                              (2)
```

in `Z[z][F_37]`.  Here star sends `z` to `z^-1` and `u^c` to `u^-c`.

Equation (2) is a mixed-column condition.  Its augmentation at `u=1` is the
primitive-nine row-spectrum equation already encoded by the row-sum catalog,
but its twelve nontrivial cyclotomic components are additional.

## 2. The six-digit ring

Put `pi=1-z`.  Direct substitution gives

```text
Phi_9(1-pi)
 = pi^6 - 6 pi^5 + 15 pi^4 - 21 pi^3
   + 18 pi^2 - 9 pi + 3.
```

Consequently

```text
Z[z]/(3) = F_3[pi]/(pi^6).                        (3)
```

For a binary row word `f=(f_0,...,f_8)`, its jet is

```text
J(f)
 = sum_r f_r (1-pi)^r
 = sum_(k=0)^5 (-1)^k
     (sum_r binom(r,k) f_r) pi^k       mod (3,pi^6).   (4)
```

Every nonzero order-three class word has plus weight three or six.  Its
constant coefficient in (4) is therefore zero modulo three, so every
nonzero-column coefficient of `A` and `B` is divisible by `pi`.

The canonical zero-column plus supports are

```text
A_0 = (1,1,1,0,0,1,0,1,0),
B_0 = (1,1,1,1,0,0,1,0,0).
```

Their combined cyclic intersection vector is

```text
(10,5,5,5,5,5,5,5,5).
```

Thus their reciprocal power at every nontrivial ninth root is exactly five.
Writing

```text
A = A_0 e + pi X,
B = B_0 e + pi Y,
```

equation (2) becomes

```text
pi (A_0* X + B_0* Y)
 + pi* (A_0 X* + B_0 Y*)
 + pi pi* (X X* + Y Y*)
 = 162 e.                                         (5)
```

In the integral ninth-root ring, `3` has `pi`-adic valuation six, so

```text
v_pi(162) = v_pi(2*3^4) = 24.                    (6)
```

The verifier also establishes (6) by 24 successive exact divisions by
`1-z`, followed by a failed twenty-fifth division.  Modulo three, the
right-hand side of (5) vanishes through every coefficient retained in
(3).  Equivalently, if

```text
R = A A* + B B* - 167 e,
```

then the six exact jet equations are

```text
[pi^k] R_b = 0 in F_3,
             b in F_37,  k=0,1,2,3,4,5.          (7)
```

Digit zero is forced by `5=167 mod 3`.  Digit one has no
nonzero/nonzero products because all such factors begin with `pi`.
Digits two through five contain those products and successively higher row
moments.

## 3. Digit one is exactly the Eisenstein pair sieve

Normalize a high-weight binary class word by complementation, leaving a
three-subset with residue profile

```text
(p_0,p_1,p_2),             p_0+p_1+p_2=3.
```

Its first jet digit is

```text
(word/pi) mod pi = p_2-p_1 mod 3.                (8)
```

For an opposite class pair `C_j,C_(j+6)`, the digit-one equation from (7)
is

```text
d(A_(j+6))-d(A_j)
 = d(B_(j+6))-d(B_j) mod 3.                      (9)
```

If

```text
E(p)=p_0+p_1 omega+p_2 omega^2,
```

then dividing

```text
conjugate(E(p_left)) + E(p_right)
```

by `1-omega` and reducing modulo `1-omega` gives precisely the difference
in (9).  Exhausting all `10^4` profile quadruples proves that (9) accepts

```text
3,334 / 10,000
```

choices, exactly the existing Eisenstein negation-pair count.

## 4. Why the higher digits are new

The three-row compression remembers only the residue profile
`(p_0,p_1,p_2)`.  For example, the triples

```text
{0,1,2},        {0,4,8}
```

have the same profile `(1,1,1)` and the same jet through degree one, but
different full jets through degree five.  Thus the primitive-nine jet sees
placement information erased by row compression.

For a stronger exact check, the verifier takes a pinned witness that
satisfies:

- one of the 22 aggregate Eisenstein join keys;
- origin energy 54;
- all six local coefficient-one negation-pair equations.

Each of its 24 profiles is lifted canonically to a three-subset of `Z/9`,
the high-weight complementations are restored, and all 37 physical columns
are expanded.  Direct difference counting and independent group-ring jet
multiplication agree.  The witness passes digits zero and one of (7) but
has the exact nonzero-residual census

```text
digit                 0   1   2   3   4   5
nonzero column lags   0   0  18  24  30  24
```

and therefore first fails at digit two.  The pinned residual hash is

```text
e66c31bf65e52264957bc9a2aa2c6af7adaaa5cc4374b77c2f458f2fcdc857c9.
```

This proves only that digits two through five add information beyond the
aggregate/origin/local-pair sieve.  The pinned lift is not asserted to
satisfy the full thirteen-equation three-row compressed problem.

## 5. Scope and use

The primitive-nine jet is best used as a triangular propagation layer in
the exact order-three quotient:

1. enforce the row-sum catalog;
2. enforce the three-row Eisenstein equations;
3. propagate jet digit one using the 3,334-state opposite-pair join;
4. add digits two through five in order, introducing lower-digit products
   only when they become visible.

No catalog word is removed by this note alone because a row-sum word does
not label its twelve class words.  A future catalog audit must quantify over
those labeled lifts.  An `UNKNOWN` solver result would prove nothing.

Run:

```sh
python3 verify_lp333_order3_primitive9_jet.py
python3 -m unittest -v test_lp333_order3_primitive9_jet.py
```

The exact word-jet catalog hash is

```text
91138c56cf22b40b1984a5430757b436994b409095314bdcd43967e348cf71c7.
```

The verifier runs in about `0.08 s`, peaks at about `22 MB` RSS, and records
zero swaps on the reference run.
