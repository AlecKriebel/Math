# Spectral units for the order-three LP(333) profile gate

## Status

The prime-167 profile cone has no degenerate or coordinate-axis branch on
the physical ten-value profile alphabet.

More precisely, suppose two order-three-invariant Eisenstein sequences
`A,B` on `F_37` satisfy

```text
A A* + B B* = 167 e.                                    (1)
```

Their reductions in the invariant algebra

```text
F_(167^2)[C_37]^H = k x E x E,
k=F_(167^2),             E=F_(167^12),                  (2)
```

are both units: the trivial coordinate and both primitive coordinates of
each channel are nonzero.  Thus one may divide the channels and write

```text
U=A B^(-1),             U U*=-1.                        (3)
```

The complete physical part of the modular cone is a single algebraic torus.
For a fixed aggregate target its primitive coordinates have exactly

```text
(167^12-1)^3
```

points before imposing the small integral coefficient alphabet.

This is an exact structural reduction, not a profile survivor, an
`LP(333)`, or an `H(668)`.  It does not make the torus small enough for
unrestricted enumeration.  Its value is that spectral inversion and ratio
arguments are now rigorous and no search has to retain the old degenerate or
axis cases.

## 1. The profile polynomial and its seven energy sectors

For a composition `p=(p_0,p_1,p_2)` of three, put

```text
z(p)=p_0+p_1 omega+p_2 omega^2,
omega^2+omega+1=0.
```

The ten distinct values are exactly the roots of

```text
P(X)=X(X^3-27)(X^6+27).                                 (4)
```

They consist of zero, three values of norm 9, and six values of norm 3:

```text
{0} union 3 mu_3 union (1-omega) mu_6.
```

The actual channel coefficients include the prescribed class-parity signs.
Those signs do not change norms or sixth powers.  If `n_d` is the total
number of the 24 profile letters having norm `d`, normalized profile energy
54 gives

```text
n_0+n_3+n_9=24,
3 n_3+9 n_9=54.
```

Consequently there are only seven exact type sectors:

| `n_9` | `n_0` | `n_3` | nonzero letters | `sum z^6` |
|---:|---:|---:|---:|---:|
| 0 | 6 | 18 | 18 | -486 |
| 1 | 8 | 15 | 16 | 324 |
| 2 | 10 | 12 | 14 | 1,134 |
| 3 | 12 | 9 | 12 | 1,944 |
| 4 | 14 | 6 | 10 | 2,754 |
| 5 | 16 | 3 | 8 | 3,564 |
| 6 | 18 | 0 | 6 | 4,374 |

Indeed

```text
(n_0,n_3,n_9)=(6+2h,18-3h,h),             0<=h<=6,
sum z^6=-27 n_3+729 n_9=-486+810h.                       (5)
```

This power-moment partition is a small independent propagation layer.  The
spectral-unit theorem below is stronger than (5) and uses only the fact that
the nonzero-column alphabet has norms `0,3,9`.

## 2. Primitive Fourier values cannot vanish over the complex numbers

Let

```text
F(X)=sum_(c in F_37) f(c) X^c
```

be either channel polynomial and let `zeta` be a primitive 37th root.
The polynomial `Phi_37` remains irreducible over `Q(omega)`.  A direct
certificate is available: with

```text
pi=7+3 omega,             Norm(pi)=37,
37=pi conjugate(pi),
```

the two factors `pi` and `conjugate(pi)` are nonassociate, and

```text
Phi_37(X+1)
```

is Eisenstein at `pi`.  Its constant coefficient is 37, its nonleading
coefficients are divisible by 37, and its leading coefficient is one.

If `F(zeta^r)=0` for a nonzero `r`, irreducibility and `deg(F)<=36` force

```text
F(X)=c Phi_37(X).
```

All 37 coefficients would then equal `c`.  This is impossible for either
profile channel: the distinguished coefficients have norms 1 and 4, while
every nonzero-column profile coefficient has norm 0, 3, or 9.  Therefore

```text
F(zeta^r) != 0                       for every r!=0.      (6)
```

Applying (6) to both channels and evaluating (1) at `zeta^r` gives the
strict inequalities

```text
0 < |A(zeta^r)|^2 < 167,
0 < |B(zeta^r)|^2 < 167.                                (7)
```

This is the spectral uncertainty input to the norm argument.

## 3. The twelve-factor field norm

Put

```text
K=Q(omega,zeta),             L=K^H,
H={1,10,26}.
```

The coefficient words are `H`-invariant, so

```text
alpha_F=F(zeta)
```

lies in `L`.  The field has degree 12 over `Q(omega)` and degree 24 over
`Q`.  Its embeddings are indexed by an embedding of `Q(omega)` and a coset
`rH` in `F_37^*/H`.

Complex conjugation pairs the embedding

```text
(omega,zeta) -> (omega,zeta^r)
```

with

```text
(omega,zeta) -> (conjugate(omega),zeta^(-r)).
```

Hence the absolute field norm has exactly twelve positive factors:

```text
N_F = Norm_(L/Q)(alpha_F)
    = product_(rH in F_37^*/H) |F(zeta^r)|^2.             (8)
```

Because `alpha_F` is an algebraic integer, `N_F` is a positive rational
integer.  Equation (7) gives the strict universal gap

```text
1 <= N_F < 167^12.                                      (9)
```

There is also a target-dependent sharpening.  Let

```text
E_F=sum_c |f(c)|^2,             n_F=|F(1)|^2.
```

The Fourier values are constant on the three-element `H`-orbits, so Parseval
gives

```text
T_F=sum_(rH) |F(zeta^r)|^2
   =(37 E_F-n_F)/3.                                     (10)
```

Arithmetic-geometric mean applied to (8) yields

```text
1 <= N_F <= (T_F/12)^12 < 167^12.                       (11)
```

All quantities in (10) are exact integers or rational numbers; no numerical
approximation enters this bound.

## 4. The two residue primes above 167

The rational prime 167 is inert in `Z[omega]`, so its residue field there is

```text
k=F_(167^2).
```

The relevant residue orders are

```text
ord_37(167)=36,             ord_37(167^2)=18.
```

Moreover `H` is contained in the order-18 subgroup generated by `167^2`.
On `F_37^*/H`, Frobenius therefore has exactly two cycles, each of length
six.  Thus 167 has two primes in `L`,

```text
P_+, P_-,
Norm(P_+)=Norm(P_-)=((167)^2)^6=167^12.                 (12)
```

With the pinned prime-167 CRT convention, reduction at these primes is

```text
alpha_F modulo P_+ = F(zeta)       = x_F,
alpha_F modulo P_- = F(zeta^167)   = y_F.               (13)
```

Here the first root belongs to the displayed factor `f_+`; multiplication
of its exponent by 167 gives the other Frobenius orbit and the factor
`f_-`.

If either coordinate in (13) were zero, `alpha_F` would lie in the
corresponding prime ideal.  Its absolute norm would then be divisible by
`167^12`, contradicting (9).  Therefore

```text
v_(P_+)(alpha_A)=v_(P_-)(alpha_A)=0,
v_(P_+)(alpha_B)=v_(P_-)(alpha_B)=0.                    (14)
```

In particular both primitive resultant norms are coprime to 167.

The trivial coordinates are nonzero as well.  Their Eisenstein norms sum to
167.  An Eisenstein norm is only 0 or 1 modulo 3, whereas `167=2 modulo 3`,
so neither coordinate can be zero.  Each norm is then strictly between zero
and 167, which also prevents the coordinate itself from being divisible by
167.  For the 22 fixed aggregate targets the norm-pair histogram is

```text
(19,148)   4,
(28,139)   4,
(64,103)   2,
(91, 76)   8,
(100,67)   2,
(163, 4)   2.
```

Equations (14) and the trivial argument prove that both channel reductions
are units in all three factors of (2).

## 5. Unitary ratio and the single torus

Write the CRT involution as

```text
(c,x,y)*=(c^167, y^(167^5), x^(167^7)).                 (15)
```

Since `B` is a unit, divide (1) modulo 167 by `B B*` and put

```text
U=A B^(-1).
```

Then (3) follows.  Conversely, any unit `B` and any `U` satisfying (3)
give a modular complementary pair.

For

```text
U=(u_0,u,v),
```

equation (3) is

```text
u_0^(167+1)=-1,
u v^(167^5)=-1.
```

The two Frobenius exponents in (15) are inverse on `E` because `5+7=12`.
Thus the complete parameterization is

```text
u_0 in k^* with Norm(u_0)=-1,
u in E^* arbitrary,
v=(-u^(-1))^(167^7).                                    (16)
```

There are

```text
168(167^12-1)
```

unitary ratios.  The unit group of (2) has

```text
(167^2-1)(167^12-1)^2
```

elements, so the complete all-unit cone contains

```text
(167^2-1) * 168 * (167^12-1)^3                         (17)
```

ordered pairs before the integral alphabet is imposed.

For a fixed aggregate target, the trivial coordinates are already fixed.
The primitive part can equivalently be written

```text
x_A,x_B,tau in E^*,
y_A=(-tau x_B)^(167^7),
y_B=( tau x_A)^(167^7).                                 (18)
```

It therefore contains exactly

```text
(167^12-1)^3
=104182064987932057052334092363939654793506843306556203540643277710721708855296000
```

points.

The old complete primitive cone had

```text
M^2+(M^2-1)M,             M=167^12.
```

The spectral-unit theorem removes exactly

```text
(2M-1)^2
=885636075678447434280943181982337697777274907219559041
```

boundary points.  Those are the degenerate branch, both nondegenerate axis
cases, and the `tau=0` boundary.  In particular, the previously useful
`A`-axis and `B`-axis recovery fixtures remain valid tests of the ambient
finite-field parameterization, but they cannot be reductions of a physical
profile-zero pair.

## 6. Search consequence

Any future spectral profile constructor may now:

1. split the ten-value alphabet into the seven exact type sectors (5);
2. discard the zero and axis branches of the prime-167 cone;
3. invert either channel in every CRT factor;
4. use the single unitary-ratio equation `U U*=-1`;
5. intersect the torus (16) or (18) with the 24 small integral coefficient
   constraints;
6. replay any intersection point through the exact integer profile gate.

This does not license a search over all points in (17).  The remaining
problem is the sparse inverse-CRT intersection, and no point in that
intersection is currently known.

## Reproduction

```text
python3 verify_lp333_order3_spectral_units.py
python3 -m unittest -v test_lp333_order3_spectral_units.py
```

The verifier uses only the Python standard library.  It checks the
ten-root polynomial, all seven energy sectors, Eisenstein irreducibility at
`7+3 omega`, the two length-six Frobenius cycles, all twelve embedding
pairs, the target norm histogram, the exact norm gap and trace formula, the
unitary-ratio exponents, the torus counts, and the forbidden old axis
patterns.

Pinned certificate hashes:

```text
alphabet
ef638caa35d133e285ffaa6e781bdaff3788d6a95e3df7eb5733e7be7466a725

field and residue primes
8ee4b74642b7e2ffdbc44c9b71d49132faf776457aa53f1220a709571c6f2566

norm gap and target traces
cc16fbfca0fabfdf1535ce898ccf06c5174e77f547bfb94352be31c24fa467cc

unitary ratio and torus
970b3cf1db191292a59cff91db42ba902c935373d106ae65bf0a74fd85e95a51

master
a8f551c9c7933f17178d7f63e2df78871b393462d890ccba9753bdc74bcae6ac
```
