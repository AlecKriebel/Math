# Independent ideal certificates for the PR11 exact reproduction family

Author: audit subagent, independently of the coordinate-matrix rank computation.
First checkpoint: 2026-10-01T05:02:10Z (2026-09-30 22:02:10 PDT).
Final validated checkpoint: 2026-10-01T05:15:53Z (2026-09-30 22:15:53 PDT).

## Scope and assumptions

Let `k` be any field. All ideals below are in the indicated polynomial ring,
and their local versions are obtained by localization at the origin. The
stress suite uses `k = Q`. The certificates prove lengths, minimal numbers
of ideal generators, and the asserted minimal free resolutions. They are
elementary finite examples, not a proof of a general matrix criterion, not a
priority or novelty claim, and not evidence for global generation of arbitrary
ideals.

For an ideal `I` in a local ring `(R,m)`, the minimal generator count is
`mu(I) = dim_k I/mI`. A displayed generating list only gives an upper bound;
the lower bounds below are separately certified. Each algebra is finite and
supported only at the origin. Thus its polynomial quotient and its quotient
after localization at the origin coincide: a polynomial with nonzero constant
term is a unit because its remaining part is nilpotent. Localization therefore
does not change length. Exact polynomial-ring resolutions remain exact upon
localization; all entries of their differentials lie in the origin maximal
ideal, so the localized resolutions are minimal.

## 1. Adversarial correction: the proposed plane ideal is a complete intersection

In `k[u,v]`, let

`P = (f1,f2,f3) = (u^2-v^3, uv, v^4)`.

There is an integral polynomial identity

`v f1 - u f2 = -f3`.

Consequently `P = (u^2-v^3, uv)` and the proposed minimal count of three is
false. A lexicographic Groebner basis with `u > v` is
`{u^2-v^3, uv, v^4}`. The only nonzero new S-polynomial of the first two
generators is the displayed multiple of `v^4`; the other pairs reduce to zero.
Its standard monomials are

`1, u, v, v^2, v^3`.

Hence the length is five. Equivalently, the quotient has the exact multiplication
rules `u^2=v^3`, `uv=0`, `v^4=0`, with the five displayed basis vectors.
They form an associative algebra, providing an independent lower-bound model
for the dimension as well as the reduction upper bound.

The two generators are minimal: `P` is contained in `m^2`, so `mP` is
contained in `m^3`; their degree-two initial forms `u^2` and `uv` are linearly
independent. A minimal resolution is

`0 -> R -> R^2 -> R -> R/P -> 0`,

with maps `1 -> (-uv, u^2-v^3)` and `(a,b) -> a(u^2-v^3)+buv`.
Exactness can be checked without a homological criterion. Neither `u` nor
`v` divides `u^2-v^3`, so it is coprime to `uv`. A relation
`a(u^2-v^3)+buv=0` forces `uv | a`, and hence is a multiple of the
displayed relation. The first map is injective because the ring is a domain.
Thus the Betti vector is `(1,2,1)` and `mu(P)=2`, over every field.

**Disposition:** exclude this ideal from non-complete-intersection stress
examples; retain it as a hidden-redundancy falsifier.

## 2. Same-length genuinely nonhomogeneous plane replacement

Use

`K = (F1,F2,F3) = (u^4, uv-u^3, v^2)`.

The automorphism `a=u`, `b=v-u^2`, with inverse `u=a`, `v=b+a^2`, fixes
the origin. It carries the monomial ideal `(a^4,ab,b^2)` to

`(u^4, u(v-u^2), (v-u^2)^2)`.

These are generators of `K`, because

`(v-u^2)^2 = v^2 - 2u(uv-u^3) - u^4`.

This identity is valid in characteristic two as well. The monomial quotient
has basis `1,a,a^2,a^3,b`; therefore `K` has length five. In the reduced
presentation, a convenient basis is `1,u,u^2,u^3,v`, with
`u^4=0`, `v^2=0`, `uv=u^3`. These relations reduce every monomial to the
five listed vectors, and their exact associative multiplication table supplies
an independent dimension lower bound.

This ideal itself is nonhomogeneous and nonmonomial, rather than merely
having an inconvenient generating list: `uv-u^3` belongs to `K`, while
the basis proves that both `uv=u^3` and `u^3` are nonzero in the quotient.
Its two homogeneous or monomial terms therefore do not individually
belong to the ideal.

The generators `a^4,ab,b^2` are minimal modulo `m(a^4,ab,b^2)`: none of
these three monomials belongs to that monomial ideal, and no nonzero scalar
combination of distinct monomials belongs to it. The origin-preserving
automorphism preserves `I/mI`, so `mu(K)=3`. In particular this length-five
ideal is not a complete intersection in the two-dimensional local ring.

An explicit minimal Hilbert--Burch resolution is

`0 -> R^2 --B--> R^3 --(F1,F2,F3)--> R -> R/K -> 0`,

where

```
B = [ v-u^2      u     ]
    [ -u^3       v+u^2 ]
    [  0         -u    ].
```

The two columns are syzygies, and the signed maximal minors (signs
`+,-,+` for deleted rows 1,2,3) are exactly `u^4, uv-u^3, v^2`.
There is a direct proof of exactness, so the name of the resolution is not
being used to hide a grade assumption. Before the automorphism, every
syzygy `(A,B,C)` of `(a^4,ab,b^2)` satisfies

`A a^4+B ab+C b^2=0`.

First `b | A`; writing `A=b p` gives
`a(p a^3+B)+Cb=0`, so `a | C`. Write `C=-a q`. Then
`B=-p a^3+bq`. Thus the entire kernel is generated by
`(b,-a^3,0)` and `(0,b,-a)`. These columns give an injective map, since
its first and last rows force `p=q=0` in the domain. Applying the automorphism
and the invertible generator change

```
T = [ 1  0  -1  ]
    [ 0  1  -2u ]
    [ 0  0   1  ]
```

to the transformed columns produces the displayed matrix `B`. This proves
its exactness over the polynomial ring and after localization. Its entries
are all in `m`, so its Betti vector is `(1,3,2)`.

## 3. The three-variable Gorenstein non-complete-intersection example

Let

`J = (x^2, y^2, xz, yz, z^2-xy)` in `k[x,y,z]`.

All monomials of degree three lie in `J`: those containing `x^2`, `y^2`,
`xz`, or `yz` are immediate, and
`z^3 = z(z^2-xy)+xyz`. The five displayed quadratic relations are
linearly independent in the six-dimensional quadratic space. Therefore
`A=k[x,y,z]/J` has basis

`1,x,y,z,q`, where `q=xy=z^2`,

and length five. Its only nonzero products between degree-one basis vectors
are `xy=q` and `z^2=q`; also `mq=0`. A socle vector with a degree-one
part `a x+b y+c z` must have `b=0` after multiplication by `x`,
`a=0` after multiplication by `y`, and `c=0` after multiplication by `z`.
Hence the socle is exactly `kq`. Equivalently, taking the coefficient of `q`
in products gives a nondegenerate pairing: on degree one its matrix is
`[[0,1,0],[1,0,0],[0,0,1]]`, of determinant `-1`. Thus `A` is an
Artinian Gorenstein algebra, including in characteristic two.

Since `J` is homogeneous and generated in degree two, `mJ` has no
degree-two part. The five independent quadrics therefore give a basis of
`J/mJ`, proving `mu(J)=5`; this is greater than the ambient dimension three.
The separate child report in `gorenstein_falsifier/` independently checks the
same claims and supplies an exact minimal resolution with Betti vector
`(1,5,5,1)`. That resolution is not required for the lower bound `mu(J)=5`.

## 4. Nonlinear triangular coordinate complete intersection

Let

`C=(u^3,(v-u^2)^2,w-uv)` in `k[u,v,w]`.

The origin-preserving polynomial coordinate change

`a=u, b=v-u^2, c=w-uv`

has the explicit polynomial inverse

`u=a, v=b+a^2, w=c+ab+a^3`.

It identifies `C` with `(a^3,b^2,c)`. This is a regular sequence: `a^3`
is a nonzerodivisor in the polynomial ring; multiplication by `b^2` is an
injective coefficient shift in `k[a]/(a^3)[b,c]`; multiplication by `c`
is an injective coefficient shift in `k[a,b]/(a^3,b^2)[c]`.
Thus its Koszul resolution is exact. For this particular coordinate ideal,
one can also obtain exactness by tensoring the three two-term resolutions,
each split as vector-space complexes over the field.

The quotient basis is

`1,a,a^2,b,ab,a^2b`,

so the length is six. The three monomial ideal generators represent
independent nonzero classes modulo the maximal ideal times the ideal, by
the same monomial-divisibility argument as for `K`. The automorphism
preserves that quotient, so `mu(C)=3`. Its minimal resolution has Betti
vector `(1,3,3,1)`. The linear generator `w-uv` is still minimal: linear
terms do not make its class lie in `mC`.

## 5. Tensor extension lemma and two larger dimensions

Suppose `I0` is any of the preceding origin-supported ideals in
`k[x1,...,xe]`, with length `n` and minimal generator count `r0`. In the
ring enlarged by `t1,...,th`, set

`I = I0 R + (t1^q1,...,th^qh)`, with each `qi >= 1`.

The quotient is the tensor product over `k` of the original quotient and
the truncated one-variable algebras `k[ti]/(ti^qi)`. Tensor products of
their explicitly independent bases give length `n product(qi)`.

There is also a direct minimal-generator certificate. Suppose a scalar
combination of the `r0` old minimal generators and the `h` new powers lies
in `mI`. Set every new variable equal to zero. This implies that the old
scalar combination lies in `m0 I0`, so all its coefficients vanish. To
isolate the coefficient of `ti^qi`, set all old variables and all other new
variables equal to zero. The image of `mI` is `(ti^(qi+1))`, forcing that
coefficient to vanish as well. Thus `mu(I)=r0+h`.

For resolutions, extend a free resolution of the old quotient and tensor
it with the two-term complex for each new power. Multiplication by
`ti^qi` is injective before imposing that variable's relation, as a
coefficient shift in a polynomial variable over any coefficient ring.
Consequently the mapping cone is exact at each step. Every differential
entry remains in the maximal ideal, so the tensor resolution is minimal.
Its Betti polynomial is the old Betti polynomial times `(1+s)^h`.

The agreed larger stress examples are therefore:

| Ideal | Ambient dimension | Length | Minimal generators | Minimal Betti vector |
| --- | ---: | ---: | ---: | --- |
| `K+(s^2,t^2)` | 4 | 20 | 5 | `(1,5,9,7,2)` |
| `J+(s^2,t^2)` | 5 | 20 | 7 | `(1,7,16,16,7,1)` |

Both are supported only at the origin and fail the local complete-intersection
generator count. The second remains Gorenstein: tensor the nondegenerate
pairing for `A` with the coefficient-of-`st` pairing on
`k[s,t]/(s^2,t^2)`, or directly check that its socle is `kqst`.

## 6. Independent full Betti certificate for the square of the maximal ideal

For `S=k[x1,...,xd]` and `M=(x1,...,xd)^2`, the quotient has basis
`1,x1,...,xd` and length `d+1`. Every degree-two monomial is nonzero
modulo `mM=m^3`, so `mu(M)=binomial(d+1,2)`.

The full Betti vector also has a certificate independent of the proposed
coordinate-matrix formula. Order the degree-two monomials by decreasing
lexicographic order, with `x1 > ... > xd`. For a generator `g` whose
largest variable index is `j`, let `L` be the ideal of preceding generators.
Then

`L:g = (x1,...,x_(j-1))`.

Indeed, for each `q<j`, replacing a factor `xj` of `g` by `xq` gives
an earlier degree-two monomial dividing `xq*g`. Conversely, for any
earlier degree-two monomial `h`, its first exponent surplus over `g`
occurs at an index less than `j` and survives in `h/gcd(h,g)`. The
usual monomial expression for a colon ideal therefore shows both inclusions.
There are exactly `j` generators whose largest variable index is `j`.

Adding `g` uses the short exact sequence

`0 -> S/(L:g)(-2) --g--> S/L -> S/(L,g) -> 0`.

The Koszul resolution of the quotient `S/(L:g)` has ranks
`binomial(j-1,p)` and, after the shift by two, shifts `p+2`.
Inductively, the old quotient resolution has its module at positive
homological degree `p` generated in degree `p+1`; its degree-zero module
is `S`. A graded comparison map therefore has positive-degree entries:
degree one at positive homological degree and degree two in degree zero.
Thus the mapping cone is minimal, and continues the indicated degree
pattern. Each such generator contributes `binomial(j-1,i-1)` to
the quotient's `i`th Betti number. Hence for `1<=i<=d`,

`beta_i(S/M) = sum_(j=1)^d j binomial(j-1,i-1)`

`= i sum_(j=i)^d binomial(j,i) = i binomial(d+1,i+1)`.

All higher Betti numbers vanish and `beta_0=1`. For `d=5`, the exact
vector is `(1,15,40,45,24,5)`, with length six and minimal generator
count fifteen. The script separately checks the colon assertion for
every degree-two generator in dimensions one through seven and expands
the stated dimension-five formula.

## 7. Equal-squares Gorenstein presentation and rational Betti numbers

The suite's other Gorenstein presentation is

`G=(u^2-v^2,u^2-w^2,uv,uw,vw)` over `Q`.

Its quotient directly has basis `1,u,v,w,q`, where
`q=u^2=v^2=w^2`; every mixed quadratic product vanishes and `mq=0`.
The independent five quadratic relations prove length five and `mu=5`.
The coefficient-of-`q` pairing is nonsingular (its degree-one block is
the identity matrix), so it is Gorenstein.

There is an independently checkable complex linear equivalence to `J`.
Write the coordinates for `J` as `(a,b,c)` to avoid ambiguity. Set

`u=(a+b)/sqrt(2), v=(a-b)/(i sqrt(2)), w=c`.

The determinant is `i`, and the inverse is

`a=(u+i v)/sqrt(2), b=(u-i v)/sqrt(2), c=w`.

In the `J` quotient these new coordinates satisfy
`u^2=v^2=w^2=q` and `uv=uw=vw=0`. Exact equality of the
transformed ideals, rather than just an inclusion, follows from the inverse
identities

```
a^2 = (u^2-v^2)/2 + i uv,
b^2 = (u^2-v^2)/2 - i uv,
ac = (uw+i vw)/sqrt(2),
bc = (uw-i vw)/sqrt(2),
c^2-ab = -(u^2-w^2) + (u^2-v^2)/2.
```

The invertible coordinate change transports the explicit exact minimal
resolution of `J` over `C` to one for `G`, giving `(1,5,5,1)`.
This is also the Betti vector over `Q`: tensoring a minimal graded
polynomial-ring resolution with a field extension is exact, and all
positive-degree differential entries remain positive-degree, so minimality
and free ranks are preserved. Localizing at the origin preserves the same
minimal ranks. The coordinate equivalence is over `C`; the rational
conclusion is equality of Betti ranks under field extension. The script
checks the coordinate identities exactly
in `Q[i,r]/(i^2+1,r^2-2)`.

## Checkable artifacts and remaining gap

`check_certificates.py` uses exact integer/rational polynomial arithmetic and exact
finite multiplication tables without external packages. It checks all
displayed polynomial identities, the plane resolution minors and syzygies,
associativity and defining relations for every finite quotient model,
the tensor Betti polynomial expansions, and the square-maximal-ideal
colon certificates. `CHECK_RESULTS.json` records its
results. These computations verify finite certificates; the proofs above
explain why their models exhaust the quotients and why the resolutions are
exact and minimal.

The exact generator counts and lengths are proved. No remaining gap exists
for these examples and the separate elementary `m^2` formula. Any implication from these examples to the
general PR11 target remains the responsibility of the separate theorem and
matrix audits. Completion toward this certificate subtask: **100%**;
the child report and exact script output have been read and checked.
