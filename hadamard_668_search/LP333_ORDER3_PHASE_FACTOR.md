# LP(333) three-fiber unit-phase factorization

## Status

The exact primitive-nine equation has a smaller integral form than its 78
displayed correlation differences suggest.  Split every nine-row class word
into its three residue fibers modulo three.  A fiber of fixed size zero or
three has Fourier value zero; a fiber of size one or two has Fourier value a
signed cube root of unity.

For the row-695 profile lift, the 54 placement trits are therefore exactly
54 signed Eisenstein phases.  The complete primitive-nine equation factors
into:

1. a periodically complementary family of six sparse Eisenstein sequences
   on `C_37`;
2. one directed cross-fiber equation.

The formally third equation is the adjoint of the second.  Thus the exact
mixed-lag layer has 36 independent integer conditions, not 72 unrelated
displayed differences.

This is an exact reparameterization and a new search architecture.  It does
not yet exclude row 695, construct an `LP(333)`, or construct `H(668)`.

## 1. Three fibers of a nine-row word

Write a row as

```text
r=s+3q,                 s,q in C_3,
```

and put `omega=zeta_9^3`.  For a binary class word `w`, define

```text
U_s(w)=sum_(q in C_3) w(s+3q) omega^q
       in Z[omega].                                  (1)
```

If the fixed fiber count is `p_s`, then

```text
p_s=0 or 3:  U_s=0,
p_s=1:       U_s in {1,omega,omega^2},
p_s=2:       U_s in {-1,-omega,-omega^2}.            (2)
```

Consequently, every active fiber is encoded by one phase in `C_3`.
In terms of the placement trit `u` from `LP333_ORDER3_TRIT_LIFT.md`,

```text
p_s=1:       U_s= omega^(-u),
p_s=2:       U_s=-omega^( u).                        (3)
```

Equation (3) is a bijection in both cases.  It replaces the lookup-table
meaning of a placement trit by an intrinsic cyclotomic meaning.

## 2. Extension-basis decomposition

For each channel and physical column `c`, let `U_0(c),U_1(c),U_2(c)` be
the three values (1).  The primitive-nine evaluation of the column word is

```text
W(c)=U_0(c)+zeta_9 U_1(c)+zeta_9^2 U_2(c).            (4)
```

For Eisenstein sequences on `C_37`, define

```text
K_st = sum_(channels A,B) U_s U_t^*,
```

where `*` conjugates `omega` and reverses the column coordinate.  Expanding
`W W^*` in the basis `1,zeta_9,zeta_9^2` over `Z[omega]` gives

```text
E_0 = K_00+K_11+K_22,

E_1 = K_10+K_21+omega^2 K_02,

E_2 = K_20+omega^2 K_01+omega^2 K_12.                (5)
```

The exact primitive-nine difference-family equation is equivalent to

```text
E_0=167 e,             E_1=0,             E_2=0
                  in Z[omega][C_37].                  (6)
```

No modular reduction is used here.

## 3. Only two group-ring equations are independent

The correlation matrices obey

```text
K_st^*=K_ts.
```

Taking the adjoint of `E_1` in (5) gives the exact identity

```text
E_2=omega^2 E_1^*.                                  (7)
```

Therefore (6) is equivalent to only

```text
K_00+K_11+K_22 = 167 e,                             (8)

K_10+K_21+omega^2 K_02 = 0.                         (9)
```

Equation (8) says that the six sequences

```text
U_(A,0), U_(A,1), U_(A,2),
U_(B,0), U_(B,1), U_(B,2)
```

form a periodic complementary family over the Eisenstein integers.  At
every nontrivial character `chi` of `C_37`,

```text
sum_(channel,s) |U_(channel,s)(chi)|^2 = 167.        (10)
```

Equation (9) is the remaining directed cross-fiber coupling.

This separation is useful: the diagonal frame (8) can be sieved or lifted
without carrying the cross terms, while every survivor retains the exact
coupling (9).

## 4. Exact equation count

Order-three column invariance gives thirteen column classes.  The
self-adjoint equation (8) has:

```text
one real origin coefficient
+ six conjugate pairs of Eisenstein coefficients
= 13 independent integer conditions.
```

Equation (9) is a general invariant Eisenstein word:

```text
13 Eisenstein coefficients = 26 integer conditions.
```

Hence the complete primitive-nine layer has `13+26=39` independent integer
conditions.  At the origin, the fixed energy and exact row-direction
equations account for three of them.  The genuinely mixed-column layer has

```text
39-3=36
```

independent integer conditions.  This agrees with, and explains, the 36
triple-equality groups in the integral correlation formulation.

## 5. Row-695 specialization

The fixed row-695 profiles have exactly 54 active nonzero-class fibers, one
for each placement trit.  After each nonzero column class is expanded to its
three physical columns and the fixed zero column is included, the six
Eisenstein sequences have total support

```text
167.
```

Thus the zero coefficient of (8) is automatic on this profile.  The search
variables are 54 signed unit phases subject to the nonzero coefficients of
(8), the cross equation (9), and the exact row-margin constraints.

Both labelled mod-three certificates in the repository replay perfectly
through (1)--(7), but fail (8)--(9), exactly as their nonzero integral
primitive-nine defects require.  They are consistency fixtures, not
solutions.  Each has nonzero coefficients in all twelve nonzero invariant
classes of all three displayed components.  Their complete invariant
component hashes are:

```text
original labelled certificate
  9cada4a8eeca603b7ecef64b4c30e1ce43a1376258a95658674a8d6c902da32d

trit-lift certificate
  31f424677b10794c77867420ce0487bf51320c6d7d52a2f9f521e6848c7542d3
```

## Reproduction

```text
python3 verify_lp333_order3_phase_factor.py
python3 -m unittest -v test_lp333_order3_phase_factor.py
```

The verifier uses exact Eisenstein arithmetic and the Python standard
library only.
