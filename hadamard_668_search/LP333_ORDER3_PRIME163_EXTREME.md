# Prime-163 obstruction to the two extreme order-three profile sectors

## Status

Two exact channel-energy sectors of the order-three `LP(333)` profile search
are impossible.

The affected aggregate targets are

```text
(4,-1,0,0),       (5,1,0,0).
```

Their trivial Fourier values have Eisenstein norm pair `(163,4)`.  In the
extreme allocation where the second channel has no nonzero-column profile
energy, that channel is exactly `B=2 delta_0`, and the complementary first
channel would have to satisfy

```text
A A^* = 163 delta_0.                                      (1)
```

No such `H`-invariant Eisenstein sequence with `A(0)=-1` exists.  The proof
is an exact cyclotomic prime-factor and CM-unit argument, not a profile
search.

The local opposite-pair sieve still has exactly `1,617,192` assignments in
each affected sector before this theorem is applied.  Thus the obstruction
removes `3,234,384` locally legal assignments.  It does **not** exclude
either whole aggregate shard: explicit nonextreme local witnesses with
physical channel energies `(37,130)` remain.

This is a profile-search pruning theorem, not an `LP(333)` or an `H(668)`.

## 1. Setup

Let

```text
omega^2+omega+1=0,
H=<10>={1,10,26} in F_37^*,
L=Q(omega,zeta_37)^H.
```

For

```text
A=sum_(x in F_37) a_x [x] in Z[omega][F_37]^H,
```

the involution is coefficient conjugation together with `x -> -x`.  At a
nontrivial additive character put

```text
alpha=A(zeta_37) in O_L.
```

Equation (1) gives

```text
alpha conjugate(alpha)=163.                               (2)
```

It also gives `S conjugate(S)=163` at the trivial character, where
`S=A(1)`.

## 2. The two primes above 163 are principal

In `Z[omega]`,

```text
pi     =14+3 omega,
pi_bar =11-3 omega=conjugate(pi),
pi*pi_bar=163.                                             (3)
```

The residue `163=15 mod 37` has multiplicative order 36.  Its image in
`F_37^*/H`, a cyclic group of order 12, therefore has order 12.  By the
standard prime-decomposition theorem for cyclotomic fields, each of the two
primes `(pi)` and `(pi_bar)` of `Q(omega)` is inert in the degree-12
extension `L/Q(omega)`.  Hence

```text
(163)=P P_bar,
P=(pi),        P_bar=(pi_bar),
Norm(P)=Norm(P_bar)=163^12.                                (4)
```

In particular, the hoped-for class-group obstruction does not occur: both
degree-12 primes are principal, with explicit generators.  No class-group
computation is needed.

Taking ideals in (2), integrality forces

```text
(alpha)=P  or  (alpha)=P_bar.                              (5)
```

Thus

```text
alpha=u*pi  or  alpha=u*pi_bar
```

for a unit `u` satisfying `u conjugate(u)=1`.

## 3. CM-unit rigidity

For every embedding `sigma:L->C`,

```text
|sigma(u)|^2=sigma(u conjugate(u))=1.
```

Kronecker's theorem therefore makes `u` a root of unity.  The ambient
cyclotomic field is

```text
Q(omega,zeta_37)=Q(zeta_111).
```

Its roots of unity can be written as `zeta_37^a zeta_6^b`.  The nonidentity
element `10 in H` fixes such a root only if

```text
(10-1)a=0 mod 37.
```

Since `gcd(9,37)=1`, this forces `a=0`.  Consequently

```text
mu(L)=mu_6.                                                (6)
```

Equations (5)--(6) imply

```text
alpha in Q(omega).
```

This is the key rigidity.  Every Galois conjugate
`A(zeta_37^j)`, `j!=0`, is the same Eisenstein integer `q=alpha`, and
`|q|^2=163`.

## 4. Fourier inversion contradiction

Fourier inversion at the zero coefficient says

```text
37 a_0
 = A(1)+sum_(j=1)^36 A(zeta_37^j)
 = S+36q.
```

The canonical zero coefficient is `a_0=-1`, so

```text
S+36q=-37.                                                 (7)
```

But `|S|=|q|=sqrt(163)`, and the reverse triangle inequality gives

```text
|S+36q| >= 35 sqrt(163) > 37.                             (8)
```

Indeed, the exact squared comparison is

```text
35^2*163 = 199675 > 1369 = 37^2.
```

This contradicts (7), proving:

> **Prime-163 extreme-sector theorem.**
> There is no `A in Z[omega][F_37]^H` with `A(0)=-1` and
> `A A^*=163 delta_0`.

The proof actually needs no profile-alphabet assumption after (1) has been
reached.

## 5. Translation to the two profile targets

For an aggregate target `(u,v,r,s)`, the two trivial Fourier values are

```text
A(1)=(-1+3u)+3v omega,
B(1)=( 2+3r)+3s omega.
```

Therefore

```text
target          A(1)             B(1)
(4,-1,0,0)      11-3 omega       2
(5, 1,0,0)      14+3 omega       2.
```

In the extreme normalized profile-energy allocation

```text
E_profile(A)=54,       E_profile(B)=0,
```

the ten-value profile alphabet has a unique zero, so every nonzero-column
coefficient of `B` vanishes.  The physical energies are `(163,4)`, and the
full equation

```text
A A^*+B B^*=167 delta_0
```

reduces to (1).  Both extreme target/energy sectors are therefore excluded.

## 6. Exact scope census

A dependency-free dynamic program gives the following ordered-profile
counts for each target:

```text
layer                                      assignments
aggregate + A-profile energy 54            1,151,042,580
plus six opposite-pair local conditions        1,617,192
after the prime-163 theorem                            0.
```

The local condition uses the zero-signature bucket of size 34 in each of
the six opposite-class pairs, and the DP checks all `34^6=1,544,804,416`
locally legal A words by exact multiplicity propagation.

The theorem is not a whole-shard exclusion.  For each of the two aggregate
targets the verifier also replays a nonextreme local witness with normalized
profile energies `(12,42)`, hence physical channel energies `(37,130)`.
Those witnesses make no claim about the later exact profile-zero equations;
they only pin the obstruction's boundary.

## 7. Independent PARI/GP audit

The theorem does not depend on PARI.  The following exact commands
independently reconstruct the degree-24 field, factor 163, compare the two
prime ideals with the explicit principal ideals, and count the roots of
unity:

```text
fpol = polsubcyclo(37,12);
gpol = x^2+x+1;
ccx  = polcompositum(fpol,gpol,1)[1];
rpol = ccx[1];
ww   = ccx[3];
nfL  = nfinit(rpol);

dec = idealprimedec(nfL,163);
vector(#dec,i,[dec[i].e,dec[i].f,idealnorm(nfL,dec[i])])

piel  = 14+3*ww;
pibel = 11-3*ww;
[lift(piel*pibel),
 idealnorm(nfL,idealhnf(nfL,piel)),
 idealnorm(nfL,idealhnf(nfL,pibel))]

vector(#dec,i,[
  idealhnf(nfL,dec[i])==idealhnf(nfL,piel),
  idealhnf(nfL,dec[i])==idealhnf(nfL,pibel)
])

nfrootsof1(nfL)[1]
```

With PARI/GP 2.17.4 the outputs are

```text
[[1,12,163^12],[1,12,163^12]]
[163,163^12,163^12]
[[0,1],[1,0]]
6
```

The two prime-ideal rows may appear in the opposite order.  Here

```text
163^12=351763888007705494736404081.
```

This audit used below 29 MB maximum resident memory.  A `bnfinit` or
class-group computation is neither used nor needed.

## 8. Exact proof dependencies

The mathematical proof uses only:

1. prime decomposition in an abelian cyclotomic extension via the order of
   Frobenius in its Galois group;
2. unique factorization of integral ideals, together with the explicit
   principal generators in (3);
3. Kronecker's theorem for an algebraic-integer unit all of whose conjugates
   have absolute value one;
4. the standard description of roots of unity in a cyclotomic field; and
5. finite Fourier inversion on `F_37` plus the reverse triangle inequality.

The dependency-free verifier checks every problem-specific finite-arithmetic
hypothesis.  The PARI audit independently checks the field construction,
prime ideals, their explicit generators, and the root-of-unity count.

## Reproduction

```text
python3 verify_lp333_order3_prime163_extreme.py
python3 -m unittest -v test_lp333_order3_prime163_extreme.py
```

Both commands use the Python standard library only.
They were replayed with the system `python3` reporting Python 3.14.6 and
with `/Users/alec/Documents/Math/tmp/hadamard-env/bin/python` reporting
Python 3.12.13; both produced the same certificate.  The verifier and tests
stayed below 35 MB maximum resident memory.

The pinned master certificate is

```text
631649252c20db62a2bd0b2200c588708b07b9eb94fa350b73cd7f3c3865f191
```
