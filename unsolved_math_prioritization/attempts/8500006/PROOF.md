# An exact polynomial-shift obstruction in the ADKT family

## Status and scope

This is an authored restricted result for problem 8500006 / AMR-084-0006. It **does not solve** the requested existence of infinitely many positive integral D(1)-triples with three further distinct integer shifts.

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The complete written proof and explicit polynomial and finite-field certificates are retained. This is not a computational reproduction package: executable code, raw integer search tables and square-root witnesses, copied source documents and images, and private coordination material are omitted. Historical finite checks are supporting evidence; the universal restrictions follow from the written arguments. The historical computations cannot be reproduced from this edition alone.

The original infinite four-total-shift question remains unresolved by this work. No novelty, priority, exhaustive literature-survey, or current-openness claim is made.

The family below is the family of Corollary 5 in Adžaga–Dujella–Kreso–Tadić,
*Triples which are D(n)-sets for several n's*, arXiv:1703.10659v1, physical
pages 6–8, https://arxiv.org/abs/1703.10659 (2017; Journal of Number Theory
184 (2018), 330–341, DOI https://doi.org/10.1016/j.jnt.2017.08.024).
The polynomial classification and elementary consequences here are derived
in this manuscript. The finite divisor method is already described in that
paper, Remark 3.1; its historical implementation and checks were independently authored and are not distributed here.

## 1. The family and the restricted theorem

Put x=i+1 and define

- a=2x(x−1),
- b=2x(x+1),
- c=4(2x²−1)(4x²−1).

Define

- n₁=1,
- n₂=4(8x⁴−5x²+1),
- n₃=4(64x⁸−112x⁶+64x⁴−13x²+1).

**Theorem.** If n∈Q[x] and each of ab+n, ac+n, bc+n is a square in Q(x),
then n is one of n₁,n₂,n₃. Conversely, all three have this property.
Thus the complete set of polynomial shifts for this family has size three.

This statement includes polynomial shifts with negative values and zero;
there is no sign restriction on n in the classification.

The converse follows from these polynomial square roots, in the order
(ab+n, ac+n, bc+n):

- n₁: (2x²−1, 8x³−4x²−4x+1, 8x³+4x²−4x−1).
- n₂: (2(3x²−1), 2(4x³−2x²−x+1), 2(4x³+2x²−x−1)).
- n₃: (2(8x⁴−7x²+1), 2(8x⁴−6x²−x+1), 2(8x⁴−6x²+x+1)).

For every integer x≥2 the entries are distinct positive integers. Indeed,
b−a=4x>0 and c−b=2(4x²−x−2)(4x²+x−1)>0. They give distinct triples as x
varies, since a(x+1)−a(x)=4x>0. The known shifts are distinct and positive:

n₂−1=(2x−1)(2x+1)(8x²−3)>0,

n₃−n₂=32x²(x−1)(x+1)(2x−1)(2x+1)(2x²−1)>0.

Moreover n₂=a+b+c and n₃=(a+b+c)²/4−ab−ac−bc, agreeing with the
source's two additional shifts. These checks establish only an infinite
three-total-shift family, not the requested four-total-shift family.

## 2. Reduction to eight factor patterns

If the square of a rational function is a polynomial, the rational
function is itself a polynomial: write it p/q in lowest terms and use
q²|p². Therefore we may write

ab+n=t², ac+n=s², bc+n=r² with r,s,t∈Q[x].

Set

f=4x²+x−2, g=4x²−x−1,
N=b(c−a)=4x(x+1)fg,
D=c(b−a)=16x(2x²−1)(4x²−1).

The four factors x,x+1,f,g are distinct irreducibles over Q. The
quadratics have discriminants 33 and 17. Thus N is squarefree, apart
from its nonzero constant factor. With U=r−t and V=r+t, UV=N, so

U=k d, V=4e/k,

where k∈Q\{0}, d is a product of a subset of {x,x+1,f,g}, and de=x(x+1)fg.
Changing the sign of t swaps U,V. We may therefore take deg(d)≤deg(e)
and choose one representative from each complementary equal-degree pair.
The resulting eight possibilities are

1. d=1, e=x(x+1)fg; degrees (0,6).
2. d=x, e=(x+1)fg; degrees (1,5).
3. d=x+1, e=xfg; degrees (1,5).
4. d=x(x+1), e=fg; degrees (2,4).
5. d=f, e=x(x+1)g; degrees (2,4).
6. d=xf, e=(x+1)g; degrees (3,3).
7. d=(x+1)f, e=xg; degrees (3,3).
8. d=g, e=x(x+1)f; degrees (2,4).

The eight patterns are labeled by masks 0,1,2,3,4,5,6,8,
respectively. The bit order is x,x+1,f,g.

The remaining square condition is

Q=(U+V)²−4D=(2s)².

Write m=max(deg d,deg e). The leading coefficient L of U+V is nonzero.
For unequal degrees it comes only from V. In the equal-degree cases it
is 4(k²+4)/k, nonzero for rational k≠0. After changing the sign of s,
there is a unique possible polynomial square root B=2s with leading
coefficient L. Its coefficients are forced by comparing coefficients of
x^(2m),x^(2m−1),...,x^m in B²=Q, in descending order. Explicitly,
start with B=Lx^m; when coefficients of x^m,...,x^(j+1) of B have been
chosen, set its x^j coefficient to the x^(m+j) coefficient of Q−B²
divided by 2L. The lower-degree remainder R=Q−B² must then vanish.

This recurrence is just coefficient comparison, and introduces no
choice or omitted square root. The computation is finite because m≤6.

## 3. The unequal-degree cases

Put z=k². The recurrence above gives the following necessary remainder
coefficients. Each listed nonzero constant coefficient excludes its case.

- Mask 0: [x⁵]R=−512.
- Mask 1: [x⁴]R=512.
- Mask 2: [x³]R=−32.
- Mask 3: R=8(z−4)x³−8(z−4)x².
- Mask 4: [x⁰]R=−96z.
- Mask 8: [x⁰]R=−360z.

Since z=k²≠0, only mask 3 survives, and it requires k=±2. Substitution
in n=(V−U)²/4−ab gives n=n₃. This also supplies the square roots in
Section 1, so it is sufficient.

## 4. The two cubic-versus-cubic cases

For these cases m=3. The recurrence can equivalently be written

B₃=L,
B₂=q₅/(2L),
B₁=(q₄−B₂²)/(2L),
B₀=(q₃−2B₂B₁)/(2L),

where Q=Σqⱼxʲ and B=ΣBⱼxʲ. Thus

R₂=q₂−B₁²−2B₂B₀,
R₁=q₁−2B₁B₀.

Only these two necessary remainder equations will be needed.

### Mask 5: d=xf

Define

A₅=5z⁵−60z⁴+5088z³−38528z²+81152z−23552,

B₅=−z⁷+28z⁶−432z⁵+11584z⁴−124672z³+263168z²−249856z+49152.

Direct coefficient comparison gives

R₂=8(z−4)A₅/(z+4)⁶,
R₁=16(z−4)B₅/(z+4)⁸.

The polynomials A₅,B₅ are relatively prime over Q. Here is a small,
explicit certificate. Reduce modulo 3 and write bars for reduction:

bar(A₅)=−z⁵+z²−z+1,
bar(B₅)=−z⁷+z⁶+z⁴−z³−z²−z.

In F₃[z],

(−z⁵+z³+z²+1)bar(A₅)+(z³+z²−1)bar(B₅)=1.

Both leading coefficients remain nonzero modulo 3. By Gauss's lemma,
a nonconstant common factor over Q would reduce to a nonconstant common
factor modulo 3, contradicting this identity. Consequently, if R₂=R₁=0,
then z=4. Hence k=±2, and n=(V−U)²/4−ab=1.

### Mask 6: d=(x+1)f

Define

A₆=73z⁵−3948z⁴+5472z³+6016z²−7936z−3072,

B₆=15z⁷+2012z⁶−26320z⁵+8384z⁴+56576z³+5120z²+4096z+16384.

Here

R₂=8(z−4)A₆/(z+4)⁶,
R₁=8(z−4)B₆/(z+4)⁸.

Reduce modulo 7:

bar(A₆)=3z⁵−2z³+3z²+2z+1,
bar(B₆)=z⁷+3z⁶−2z⁴+2z³+3z²+z−3.

The explicit F₇[z] identity is

(−2z⁶+z⁵+2z³+2z²−z+3)bar(A₆)
+(−z⁴+3z²−2z+3)bar(B₆)=1.

Again neither leading coefficient vanishes modulo the prime, so A₆,B₆
are relatively prime over Q. Necessarily z=4, hence k=±2, and direct
substitution gives n=n₂. The identities of Section 1 prove sufficiency.

This exhausts every factor pattern and proves the theorem.

## 5. A rational-section obstruction, including finite unions

**Lemma.** A nonpolynomial F∈Q(x) takes integer values at only finitely
many positive integers x where it is defined.

**Proof.** Divide F=P+H, where P∈Q[x] and H is a nonzero proper rational
function, hence H(x)→0 as x→+∞. Choose an integer M≥1 clearing all
coefficients of P. If F(x)∈Z at an integer x, then MH(x)=MF(x)−MP(x)
is an integer. For sufficiently large x it has absolute value below 1,
so it must be zero. A nonzero rational function has finitely many zeros.
Only finitely many smaller integers and poles remain. QED.

**Corollary.** Let F∈Q(x) satisfy that ab+F,ac+F,bc+F are squares in
Q(x). If F is not one of the three known shifts, it gives an integral
fourth shift at at most finitely many positive integer parameters x.
The same holds for any fixed finite collection of such rational sections.

Indeed an infinite collection of integral specializations of a single F
would force F∈Q[x] by the lemma, and the theorem would then identify it
as one of the three known shifts. A finite union of finite sets is finite.
This rules out obtaining the requested infinite family within Corollary 5
from any fixed finite list of rational-function elliptic sections. It
requires no assertion about the rank or generators of the elliptic curve.

## 6. A further uniform-formula consequence

For clarity about the role of the square-root hypothesis, here is a
separate elementary fact. If P∈Q[x] is a rational square at every
sufficiently large integer, then P is the square of a polynomial in Q[x].
The zero polynomial is immediate. Otherwise it is eventually positive.
Choose M clearing coefficients of P, and let u_n=M sqrt(P(n)); this is
an integer, because u_n²=M²P(n) is an integer and u_n is rational.
If d=deg P and K=floor(d/2)+1, the K-th derivative of M sqrt(P(x)) is
O(x^(d/2−K)), tending to zero. The K-th forward difference is the
integral of that derivative over a K-dimensional unit cube, so Δ^K u_n
is an integer tending to zero. It is eventually zero. Thus the eventual
integer sequence u_n is a rational-coefficient polynomial in n of degree
at most K−1 (Newton's forward-difference formula). Squaring identifies
that polynomial squared with M²P as polynomials. This proves the fact.

Therefore a rational-function shift formula valid with integer squares
and an integer shift at every sufficiently large integer x must be one
of the three known shifts. The same statement holds on any fixed
arithmetic progression x=qj+r, q>0: first substitute the progression,
apply the integrality lemma and the square-value fact, and then use the
invertible affine substitution Q[j]=Q[x].

## 7. What remains unresolved

The theorem does not limit the number of shifts at one specialized
integer. Historical finite checks include parameters with a fourth integer shift; their raw values are omitted from this edition. Nor does it exclude infinitely many exceptional integer
parameters whose extra points vary without belonging to a fixed finite
list of rational sections. Algebraic base changes, Pell-type subfamilies,
other positive D(1)-triple families, and parameter-dependent arithmetic
constructions are not excluded. No historical finite computation proves that
there are only two exceptional parameters in this family. The requested
infinite four-total-shift family remains unresolved by this work.
