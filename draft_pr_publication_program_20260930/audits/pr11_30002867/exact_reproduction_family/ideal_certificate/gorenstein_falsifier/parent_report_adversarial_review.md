# Independent adversarial review of the parent ideal certificate

Reviewed `../REPORT.md` directly at 2026-10-01 05:08:33 UTC. Scope:
the replacement plane ideal and its resolution, tensor extension,
the lex-colon/minimal-cone proof for `m^2`, and the subsequently
requested rational equal-squares example. Parent computation results
are not used as proof premises.

**Disposition: verified within the stated field assumptions.** No
mathematical error was found. The equal-squares transfer must remain
explicitly over `C`; the two source algebras are not isomorphic over
`Q` or `R`.

## Replacement plane ideal and generator orientation

Write `F=(u^4,uv-u^3,v^2)` and substitute `a=u`, `b=v-u^2`.
The inverse is `u=a`, `v=b+a^2`, and `(u,v-u^2)=(u,v)`, so this
automorphism preserves localization at the origin.

For the matrix displayed in the parent report,

\[
T=\begin{pmatrix}1&0&-1\\0&1&-2u\\0&0&1\end{pmatrix},
\]

the transformed monomial generators satisfy exactly

\[
G=(u^4,u(v-u^2),(v-u^2)^2)=FT.
\]

Indeed `(v-u^2)^2=v^2-2u(uv-u^3)-u^4`. The determinant is 1;
the identity and invertibility also hold in characteristic 2.

For `(a^4,ab,b^2)`, use

\[
H=\begin{pmatrix}b&0\\-a^3&b\\0&-a\end{pmatrix}.
\]

A relation `Aa^4+Bab+Cb^2=0` forces `A=bp`; then
`a(pa^3+B)+Cb=0` forces `C=-aq`, and cancellation in the
polynomial domain gives `B=-pa^3+bq`. Thus `H` generates the entire
syzygy module. Its first and last rows prove its injectivity.

If `H'` denotes the transformed matrix, `G=FT` implies that the
matrix for `F` is `B=TH'`. This is exactly

\[
B=\begin{pmatrix}v-u^2&u\\-u^3&v+u^2\\0&-u\end{pmatrix}.
\]

There is no missing transpose or inverse. Its signed deleted-row
minors are `u^4`, `u(v-u^2)`, and
`(v-u^2)(v+u^2)+u^4=v^2`. Hence the direct syzygy proof, rather
than the name Hilbert--Burch, proves exactness. Every matrix entry
is in the origin maximal ideal, so the localized resolution is
minimal with vector `(1,3,2)`.

The monomial quotient has the independent basis `1,a,a^2,a^3,b`.
The generators `a^4,ab,b^2` are distinct monomials outside `mI`;
termwise membership in a monomial ideal gives their independence
modulo `mI`. Thus length 5 and generator number 3 are proved.

An additional independent check gives

\[
\operatorname{Soc}(S/K)=k u^3\oplus k(v-u^2).
\]

For `h=h0+h1u+h2u^2+h3u^3+h4v`, multiplication by `u` gives
`h0u+h1u^2+(h2+h4)u^3`, and multiplication by `v` gives
`h0v+h1u^3`. The two-dimensional socle follows in every
characteristic, agreeing with last Betti number 2. Since `u^3`
survives, the homogeneous parts of `uv-u^3` are not individually
in `K`; the original ideal is indeed nonhomogeneous.

## Tensor extension, including exponent one

Independent bases tensor over a field, proving the length product.
For generator minimality, specialize all new variables to zero:
the image of `mI` lies in `m0 I0`, forcing the old scalar
coefficients to vanish. For each new generator, specialize every
other variable to zero. The image of `mI` is `(ti^(qi+1))`, so a
scalar multiple of `ti^qi` can belong to it only with scalar zero.
This works for `qi=1` as well.

At every resolution step the next variable is polynomial over the
previous quotient. Multiplication by `t^q` is injective over any
coefficient ring, including one with nilpotents, because it shifts
polynomial coefficients. The tensor cone is consequently exact.
Its entries are old maximal-ideal entries and `t^q`, so it is
minimal. Each step multiplies the Betti polynomial by `(1+s)`.
The stated vectors `(1,5,9,7,2)` and `(1,7,16,16,7,1)` expand
correctly. The tensor Frobenius pairing for the Gorenstein extension
is nondegenerate over every field; its socle is `kqst`.

## Decreasing-lex colon formula

Let `g` be a quadratic monomial with largest variable index `j`,
and `L` the ideal of the preceding monomials in decreasing lex
order. For `q<j`, replacing one factor `xj` by `xq` gives an
earlier monomial dividing `xq*g`. Thus every `xq` is in `L:g`.

Conversely, if a monomial `f` satisfies `fg in L`, an earlier
quadratic monomial `h` divides `fg`. At the first exponent index
`q` where `h` and `g` differ, lex order gives `h_q>g_q`. One
must have `q<j`: if `q>=j`, agreement at earlier indices and
absence of variables after `j` in `g` would force `h` to have
degree greater than two. Divisibility forces `f_q>0`, so `xq`
divides `f`. Multiplication by the monomial `g` cannot cancel
distinct terms, so the colon is monomial and these two containments
prove `L:g=(x1,...,x_(j-1))`.

The first generator `x1^2` has colon zero, as required. There are
exactly `j` monomials with largest variable index `j`.

## Cone exactness and minimality

The colon formula proves the injection in
`0 -> S/(L:g)(-2) --g--> S/L -> S/(L,g) -> 0`.
The source has a Koszul resolution with shift `p+2` at
homological degree `p`. Inductively the target has shift `p+1`
for `p>=1`, and shift zero for `p=0`. A homogeneous comparison
map exists by lifting successively through the exact graded target
resolution, choosing each lift in the homogeneous degree of its
cycle. Its entries therefore have degree one at positive degrees
and degree two at degree zero.

In the cone at homological degree `i>=1`, both its old summands
and its source summands from degree `i-1` have shift `i+1`.
Cone differential entries are old entries, Koszul variables, or
these comparison entries. Every entry belongs to the maximal
ideal; no scalar entry can permit cancellation. This proves exact
minimal cones and propagates the induction's degree pattern.
Hence

\[
\beta_i(S/m^2)=\sum_{j=1}^d j\binom{j-1}{i-1}
=i\sum_{j=i}^d\binom ji=i\binom{d+1}{i+1}
\quad(1\le i\le d).
\]

No higher terms occur. These arguments survive characteristic 2;
Koszul signs and cone signs specialize consistently.

## Additional boundary: the rational equal-squares example

Let `G=(u^2-v^2,u^2-w^2,uv,uw,vw)` over `Q`. Starting with the
already certified ideal `J=(a^2,b^2,ac,bc,c^2-ab)`, pass to `C`
and set `s=sqrt(2)` and

\[
u=(a+b)/s,\qquad v=(a-b)/(is),\qquad w=c.
\]

The determinant is `i`, and the inverse is
`a=(u+iv)/s`, `b=(u-iv)/s`, `c=w`. In the quotient by `J`,
`u^2=v^2=w^2=q` and all three cross-products vanish. Conversely,

\[
\begin{aligned}
a^2&=(u^2-v^2)/2+iuv,\\
b^2&=(u^2-v^2)/2-iuv,\\
ac&=(uw+ivw)/s,\\
bc&=(uw-ivw)/s,\\
c^2-ab&=-(u^2-w^2)+(u^2-v^2)/2.
\end{aligned}
\]

Every identity is correct. The containments give exact ideal
equality under this complex linear coordinate change. It preserves
the origin and grading, so it transports the exact minimal
resolution of `J` over `C`.

Faithfully flat field extension `Q -> C` preserves the Betti ranks:
tensoring any rational minimal graded free resolution gives an
exact complex over `C` still minimal, since its differential entries
remain in the maximal ideal. Equivalently, residue-field Tor
commutes with this field extension. Thus the rational equal-squares
quotient has Betti vector `(1,5,5,1)`.

**Field boundary:** this argument is not a rational or real
coordinate isomorphism, and it cannot be. In the equal-squares
quotient the square of a degree-one class `pu+rv+tw` is
`(p^2+r^2+t^2)q`, anisotropic over `Q` and `R`. In the `J`
quotient the nonzero degree-one classes `a,b` have square zero.
Any local algebra isomorphism would preserve this property on
`m/m^2`. Passing to `C` removes this obstruction and is sufficient
for the stated rank transfer. The displayed coordinate formulas
also make no assertion in characteristic 2, where division by 2
is unavailable; the previously reviewed `J`, `K`, tensor and
`m^2` arguments themselves work in every characteristic.

## Exact gap

No correction to the parent arguments is required within their
stated fields. The finite local examples and the independent
`m^2` formula are verified. Their connection to any separate
general PR11 target remains outside this review. No parent file
was edited. Completion of this independent review: **100%**.
