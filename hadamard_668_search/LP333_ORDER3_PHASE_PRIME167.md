# Prime-167 exactness for the full order-three phase frame

## Status

On the universal unit/zero support-167 phase shell, reduction modulo 167 is
lossless for **both** independent equations in the order-three phase
factorization:

```text
E0 = 167 e    if and only if    E0 = 0 modulo 167,
E1 = 0        if and only if    E1 = 0 modulo 167.
```

The first equivalence extends the two-sequence prime-167 argument to the
six-sequence diagonal frame.  The second is new to the directed cross-fiber
equation.  Its equality case is killed by the twisted three-fiber cycle:
the relevant coordinate permutation has orbit size 3 at column lag zero and
111 at every nonzero column lag, whereas the total support is 167.

After the invariant group algebra is split as `k x E x E`, the complete
primitive system becomes a three-plane annihilator.  For a fixed minus
spectral vector it is linear in the plus spectral vector and generically
leaves three free `E` coordinates.  This gives a finite algebraic search
architecture, not an `LP(333)`, a Hadamard matrix, or a claim that a physical
phase point exists.

## 1. The six-sequence phase frame

Put

```text
u = (U_A0,U_A1,U_A2,U_B0,U_B1,U_B2)
    in Z[omega][C_37]^6.
```

Every coefficient of every `U_Xs` is zero or an Eisenstein unit.  The
universal profile-norm identity gives 54 active nonzero-column class fibers,
and the fixed zero column gives five more active fibers.  Since every
nonzero column class has size three,

```text
support(u) = 3*54+5 = 167.                              (1)
```

On each channel define

```text
P(U_0,U_1,U_2) = (U_1,U_2,omega^2 U_0).                 (2)
```

Then

```text
P^3 = omega^2 I.                                        (3)
```

With group inversion and Eisenstein conjugation included in `*`, the two
independent phase equations are

```text
E0 = sum_i U_i U_i^*,
E1 = sum_i (P U)_i U_i^*.                               (4)
```

Thus the exact primitive-nine equation is equivalent to

```text
E0 = 167 e,                  E1 = 0.                    (5)
```

The third displayed extension-basis equation is
`omega^2 E1^*` and is redundant.

## 2. Exactness of the diagonal reduction

Let `T_t` be translation by `t` on `C_37`, and use the Hermitian inner
product on all `6*37` coordinates.  The lag-`t` coefficient of `E0` is

```text
(E0)_t = <T_t u,u>.
```

Because `T_t` is unitary and `||u||^2=167`, Cauchy's inequality gives

```text
|(E0)_t| <= 167.                                        (6)
```

Suppose a nonzero coefficient is zero modulo 167.  Since 167 is inert in
`Z[omega]`, it is `167 eta` for an Eisenstein integer `eta`.  Bound (6)
forces `Norm(eta)<=1`; if the coefficient is nonzero, `eta` is one of the
six units and Cauchy is an equality.

For `t != 0`, equality makes the support of `u` invariant under `T_t`.
Every translation orbit then has size 37.  The support would be a union of
37-cycles, contrary to

```text
167 = 19 modulo 37.                                    (7)
```

Therefore every nonzero-lag coefficient that vanishes modulo 167 vanishes
exactly.  The origin coefficient is exactly the support, hence 167.  This
proves

```text
E0=167 e  <=>  E0=0 modulo 167.                         (8)
```

## 3. Exactness of the directed cross reduction

The lag-`t` coefficient of `E1` is

```text
(E1)_t = <P T_t u,u>.                                   (9)
```

The operator `P T_t` is unitary, so the same bound
`|(E1)_t|<=167` applies.  A nonzero 167-divisible coefficient would again
be 167 times a unit and force Cauchy equality.  In particular, the support
would be invariant under the coordinate permutation underlying `P T_t`.

The permutation stays within each channel and acts on a fiber/column pair
as a simultaneous three-cycle and column translation.  Its orbit lengths
are

```text
t=0:       3,
t!=0:      lcm(3,37)=111.                              (10)
```

But

```text
167 = 2 modulo 3,
167 = 56 modulo 111.                                   (11)
```

The support cannot be a union of the required orbits, so equality is
impossible at every lag.  Hence

```text
E1=0  <=>  E1=0 modulo 167.                             (12)
```

The phase twist supplies an independent check on the equality obstruction.
Over either a 3-cycle or a 111-cycle, (3) gives

```text
(P T_t)^orbit_length = omega^2 I.
```

No Eisenstein unit `epsilon` satisfies
`epsilon^3=omega^2` or `epsilon^111=omega^2`: both left sides are real
units.  The verifier checks both the support-orbit and scalar versions.

The exactness argument uses only the zero/unit alphabet and (1).
Order-three column invariance is needed only for the smaller finite-field
split below.

## 4. The full `k x E x E` equations

Let

```text
k = F_167(omega) = F_(167^2),
E = F_(167^12),
sigma(z) = z^(167^5),
rho(z)   = z^(167^7) = sigma^(-1)(z).
```

For each of the six invariant words write its CRT coordinates as

```text
U_i  ->  (c_i,x_i,y_i) in k x E x E.
```

The involution previously certified in the invariant algebra is

```text
(c,x,y)^* = (c^167, sigma(y), rho(x)).                  (13)
```

Order the coordinate vectors as

```text
c=(c_A0,c_A1,c_A2,c_B0,c_B1,c_B2),
x=(x_A0,x_A1,x_A2,x_B0,x_B1,x_B2),
y=(y_A0,y_A1,y_A2,y_B0,y_B1,y_B2).
```

The complete diagonal equations modulo 167 are

```text
c . conjugate(c) = 0                         in F_167,  (14)
x . sigma(y) = 0                             in E.      (15)
```

The minus primitive coordinate is `rho` of (15), so it is redundant.  The
complete directed-cross equations are

```text
(P c) . conjugate(c) = 0                     in k,      (16)
(P x) . sigma(y) = 0                         in E,      (17)
(P y) . rho(x) = 0                           in E.      (18)
```

Unlike the diagonal primitive pair, (17) and (18) are both needed because
`E1` is not self-adjoint.  Thus the full modular system is one `F_167`
equation, one `k` equation, and three `E` equations.

The verifier reconstructs three locally valid support-167 phase frames,
computes (4) directly in the group ring, and checks every coordinate in
(14)--(18).  In particular it independently rechecks the Frobenius
exponents five and seven and the coefficient `omega^2` in (2).

## 5. Three-plane annihilator form

Let `bar(P)` denote coefficient conjugation of (2):

```text
bar(P)(v_0,v_1,v_2) = (v_1,v_2,omega v_0)
```

on each channel, and set

```text
z = sigma(y).
```

Because

```text
P^T = omega^2 bar(P)^2
```

and applying `sigma` to (18) conjugates `P`, equations (15), (17), and
(18) are exactly

```text
x . z          = 0,
x . bar(P) z   = 0,
x . bar(P)^2 z = 0.                                    (19)
```

For fixed `y`, define

```text
W(z) = span_E {z,bar(P)z,bar(P)^2 z}.
```

Then the full primitive condition is simply

```text
x in W(z)^perp.                                         (20)
```

The rank of `W(z)` is at most three, so its annihilator in `E^6` always has
dimension at least three.  A deterministic generic fixture has rank exactly
three, and the verifier checks an explicit rank-three point and an explicit
annihilator vector.

## 6. Stronger ninth-root recombination

There is an equivalent factorization that recombines all three fiber
components before splitting the column algebra.  Let `alpha=zeta_9`, so

```text
alpha^3=omega,
W_X=U_X0+alpha U_X1+alpha^2 U_X2.
```

Since

```text
ord_9(167)=6,
```

`Phi_9` is irreducible modulo 167 and

```text
K=F_167(alpha)=F_(167^6).
```

The two equations `E0=E1=0` modulo 167, together with the redundant adjoint
component, are now the single two-channel norm equation

```text
W_A W_A^* + W_B W_B^* = 0
                  in K[C_37]^H.                         (21)
```

Put `q=167^6`.  The exact modular orders are

```text
ord_37(q)=6,
q^2=10 modulo 37,
H=<10>={1,10,26}.
```

The full primitive algebra has six degree-six factors over `K`.  On every
factor, `H=<q^2>` fixes `F_(167^12)` inside `F_(167^36)`.  Therefore

```text
K[C_37]^H
    = F_(167^6) x F_(167^12)^6.                         (22)
```

This has dimension `1+6*2=13` over `K`, agreeing with the thirteen column
orbits.  The verifier explicitly partitions all 36 nonzero exponents into
six disjoint `q`-orbits of size six, splits each into its two `H`-orbits,
and obtains rank 13 from the origin indicator and twelve `H`-class
indicators after expanding every `F_(167^12)` coordinate in a quadratic
basis over `K`.  It also checks (23) on all thirteen basis words; rank 13
and linearity then certify the star action on the whole invariant algebra.

Let

```text
(c,w_0,w_1,w_2,w_3,w_4,w_5)
```

be the seven coordinates, with
`w_r=W(zeta_37^(167^r))`.  Cyclotomic conjugation on `K` is the
`167^3` Frobenius.  Direct group-ring evaluation gives

```text
c^* = c^(167^3),

w_r^*     = w_(r+3)^(167^3),    r=0,1,2,
w_(r+3)^* = w_r^(167^9),        r=0,1,2.                (23)
```

The exponents add to twelve, so the paired action squares to the identity
on `F_(167^12)`.  The verifier constructs a pinned ninth root, evaluates a
locally valid phase frame and its group-ring adjoint at all seven
coordinates, and checks every exponent in (23) directly.

Equation (21) is consequently one norm equation in the quadratic extension
`F_(167^6)/F_(167^3)` and three independent paired equations over
`E=F_(167^12)`:

```text
c_A c_A^(167^3) + c_B c_B^(167^3) = 0,                 (24)

w_(A,r) w_(A,r+3)^(167^3)
  + w_(B,r) w_(B,r+3)^(167^3) = 0,
                                      r=0,1,2.          (25)
```

This cone has a complete factorwise parameterization.  For (24):

```text
zero:
    (c_A,c_B)=(0,0);

nonzero:
    c_A=s,
    c_B=s R,
    Norm_(F_(167^6)/F_(167^3))(R)=-1.
```

The norm-minus-one fiber has `167^3+1` points, so (24) has

```text
1+(167^6-1)(167^3+1)
```

ordered solutions.

For one equation (25), abbreviate

```text
x_A=w_(A,r),  x_B=w_(B,r),
y_A=w_(A,r+3), y_B=w_(B,r+3).
```

Its two branches are

```text
degenerate:
    (x_A,x_B)=(0,0), with y_A,y_B free;

nondegenerate:
    (x_A,x_B)!=(0,0),
    y_A=(-tau x_B)^(167^9),
    y_B=( tau x_A)^(167^9),
    tau in E.
```

If `M=167^12`, each paired equation has

```text
degenerate branch:       M^2,
nondegenerate branch:    (M^2-1)M,
total:                   M^2+(M^2-1)M
```

solutions.  The three pairs are independent in the split algebra.  This is
a complete parameterization of the modular norm cone; it does **not**
parameterize the sparse inverse-CRT alphabet intersection.

In prime-field scalars, (24) contributes three equations and the three
copies of (25) contribute `3*12=36`.  Thus the recombined split recovers
exactly

```text
3+3*12=39
```

independent scalar conditions, matching the integral phase-factor count.

## 7. Search architecture

Equation (20) changes the primitive search from an unconstrained choice of
twelve `E` coordinates to the following finite algebraic pipeline:

1. Work either in the three-plane form (20), or choose one branch and its
   parameters independently in each of the three paired factors (25).
2. Apply the small trivial norm equation (24).
3. Invert the exact CRT and retain only words whose six phase components
   have the required zero/unit coefficient alphabet, support/profile
   pattern, row margins, and symmetries.
4. Use the local profile constraints during inverse CRT as a sparse
   meet-in-the-middle or constraint-programming filter, rather than
   enumerating the whole finite-field cone.
5. Verify every survivor over `Z[omega]`; by (8) and (12), no additional
   correlation lift beyond modulus 167 is required on this shell.

The difficult part is now the sparse inverse-CRT alphabet intersection, not
an unstructured `3^54` phase enumeration.  Most finite-field points will
not invert to physical phase words.

## 8. Pinned certificates

```text
diagonal/cross equality orbits
c74bc225f3d350b8ca81f118a1ca1796b676dbb6a992c0f3b6bd7dd3cf506011

locally valid support-167 frame fixtures
29bdb7ab3d7ba49e8be0e32df70592ea5d4314f27c49e3664efd1504ac30c630

full k x E x E coordinate equations
3705a0b73069eec04ca5a65fd00aa38f6f829f6d2d388d519312c3a7e6c99694

primitive three-plane annihilator
3294fad8192a163fefdcaaaee120601ebed3fda20c0ef4db4501d268b91c2257

ninth-root split, star, and complete factorwise parameterization
cc86f194497dd5b6bc9139d9a299e888596dc99d98cf4b768730a605af0dafac
```

## Reproduction

```text
python3 verify_lp333_order3_phase_prime167.py
python3 -m unittest -v test_lp333_order3_phase_prime167.py
```

The verifier uses exact arithmetic and the Python standard library only.
