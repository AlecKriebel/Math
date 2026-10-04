# Ward's order-of-mixing example: a characteristic-two resolution and uniform bounds

Problem 4300001 / AMR-042-0001. Research date: 4 October 2026 (UTC).

**Disposition: partial resolution of the original, prime-unspecified target.**
For every prime the action below has mixing order either 5 or 6. In characteristic
2 its mixing order is exactly 6. This manuscript does not decide between 5 and 6
for any odd prime. No historical priority or new-discovery claim is made.
The arguments below require independent review; no external human peer review or
formal proof-assistant certification is claimed.

## 1. Exact question and dependencies

Put

\[
 A=1+x^4,\qquad B=x+x^2+x^3=x(x^2+x+1),\qquad
 f=A(1+y^2)+By.
\]

Ward's Problem A [W, p. 1] asks for the largest order of mixing of the Haar
measure-preserving algebraic Z²-action dual to

\[
 R_p/(f),\qquad R_p=\mathbb F_p[x^{\pm1},y^{\pm1}],
\]

with p chosen so f is irreducible. Here mixing of order r means convergence of
r-set correlations to the product of measures whenever every pair of translation
vectors separates. The source gives 3 ≤ M < 7. We retain the prime parameter;
settling p=2 alone is not treated as answering the full question.

We use two published inputs:

- Einsiedler–Ward [EW, Theorem 3.1] gives R−1 ≤ M < |supp(f)| when f is
  irreducible and its Newton polygon has R sides. Here the polygon is the
  rectangle [0,4] × [0,2], and the support has seven points.
- Derksen–Masser [DM, Lemma 5, provisional PDF pp. 10–12] implies that, if an
  action is n-mixing but not (n+1)-mixing, there is a vanishing sum of n+1
  elements of the radical of the monomial group in its function field, with
  no quotient of distinct summands constant. This is the imported minimal
  relation theorem, not a theorem proved in this manuscript.

The radical is taken **inside the function field**, as in [DM, p. 6]. It cannot
in general be replaced by the original monomial group. Section 3 proves that
replacement for this particular polynomial. No unsupported inference from an
ordinary sparse-multiple search to the order of mixing is used.

## 2. Absolute irreducibility for every prime

**Proposition 2.1.** f is absolutely irreducible over every F_p.

First A and B are coprime over every field. A common nonzero root of A and B
would satisfy x²+x+1=0, hence x³=1 and x⁴=x. Then A=0 gives x=−1, whereas
x²+x+1 at −1 is 1. Also A(0)=1. Thus f is primitive as a quadratic in y,
so it suffices to prove irreducibility over k(x), where k is an algebraic
closure of F_p.

For odd p its discriminant is

\[
 D=B^2-4A^2=-q r t,
\]
\[
 q=x^2-x+1,\quad r=2x^2+3x+2,\quad
 t=2x^4-x^3-x^2-x+2.
\]

The following integer identities will be useful:

\[
 r=2q+5x,\qquad t=(2x^2+x-2)q+4(1-x).
\]

If p is not 2, 3 or 5, q has two distinct roots (its discriminant is −3),
and neither is a root of r or t: the displayed remainders would force x=0
or x=1, neither of which is a root of q. Consequently D has a simple root
and is not a square in k(x).

For p=3,

\[
 D=-(x+1)^2(x^2+1)(x^4+x^3+x^2+x+1).
\]

The factor x²+1 is squarefree. At a root of x²+1, the last factor has value
1, while x+1 is nonzero. Hence D again has a simple root.

For p=5,

\[
 D=(x^2+1)(x+1)^2(x^2-x+1)^2.
\]

The factor x²+1 is squarefree and coprime to both other factors: at its roots,
x²−x+1=−x, and −1 is not a root of x²+1. Again D is not a square.
This proves the assertion in odd characteristic.

In characteristic 2 use

\[
 z=(A/B)y,\qquad w=z+A/B.
\]

The equation f=0 becomes

\[
 w^2+w=A/B.
\]

The rational function A/B has a pole of order one at x=0. Every pole of a
rational function h²+h has even order, since at a pole of h its squared term
has strictly larger pole order than h. Thus A/B is not h²+h for any h in
k(x). The quadratic Artin–Schreier polynomial is irreducible. This proves
absolute irreducibility in characteristic 2 as well. ∎

Let

\[
 K=\operatorname{Frac}(R_p/(f)).
\]

In particular, the constant field algebraic over F_p inside K is precisely
F_p. One standard justification is that absolute irreducibility makes
K geometrically integral: a proper finite constant extension inside K would,
after scalar extension to the algebraic closure, introduce zero divisors.
Both x and y are transcendental over F_p. For x this follows already from
the presentation as a quadratic extension of F_p(x), and similarly for y
by interchanging the role of the transcendence variable.

The formulas

\[
 f(x^{-1},y)=x^{-4}f(x,y),\qquad
 f(x,y^{-1})=y^{-2}f(x,y)
\]

induce two automorphisms of K, denoted σ_x and σ_y, inverting the indicated
coordinate while fixing the other.

## 3. Radical saturation of the monomial group

**Proposition 3.1.** For every prime p, the radical inside K of
G=⟨x,y⟩ is F_p^*G. In particular, distinct monomials are independent
multiplicatively modulo constants.

For odd p, on the smooth model of the curve there is a geometric valuation
with v(x)=1 and v(y)=0, at a point (0,β) with β²=−1. Indeed f_y=2β there.
There is another with v(x)=0 and v(y)=1 at (α,0), where α⁴=−1:
f_x=4α³ is nonzero. A geometric valuation can be applied to functions in K;
all their orders are integers. Thus any equation

\[
 h^N=c x^a y^b,\qquad c\in\mathbb F_p^*,\ h\in K^*,
\]

forces N|a and N|b. Dividing h by x^{a/N}y^{b/N} leaves an element algebraic
over F_p, hence a constant. This proves saturation in odd characteristic.

For p=2, the point (0,1) is smooth since f_x=1 there, and
f(0,y)=(y+1)². Its valuation has v(x)=2, v(y)=0. At (1,0) the curve is
smooth since f_y=B(1)=1, and f(x,0)=(x+1)⁴. Its valuation has v(x)=0,
v(y)=4. These assertions also follow directly by the local parameter
expansions in the smooth local rings. Therefore any odd prime dividing N
in the preceding display divides both a and b.

It remains to exclude nonsaturated square roots. The quadratic extension
K/F_2(x) is separable because f_y=B is not the zero function. The derivation
D with D(x)=1 therefore extends to K. Implicit differentiation gives

\[
 \frac{D(y)}y=\frac{1+x^2}{x(x^2+x+1)},\qquad
 R:=\frac{d\log y}{d\log x}=\frac{1+x^2}{x^2+x+1}.
\]

R is neither 0 nor 1. If h²=x^a y^b, differentiating and dividing by the
monomial gives a+bR=0, where a and b are reduced modulo 2. The three
possibilities R, 1, and 1+R are nonzero. Hence a and b are even. Taking out
the corresponding monomial square leaves h²=1, so h is constant. Peeling
off prime factors of N proves saturation. The same valuations imply that
x^a y^b constant forces a=b=0. ∎

**Corollary 3.2 (exact sparse-multiple reduction).** If w_p is the least
number of nonzero terms in a nonzero Laurent multiple of f over F_p, then

\[
 M_p=w_p-1.
\]

To see one inequality, any r-term relation ∑c_j x^{a_j}y^{b_j}=0 in K,
with distinct exponent pairs, gives the same relation at the exponents
p^e(a_j,b_j) by Frobenius. The corresponding nontrivial additive characters
have zero individual Haar means, but their product has mean 1. All pairs
of exponents separate as e→∞. Thus the action is not r-mixing. The
character formulation follows from the set formulation by approximating
bounded measurable functions with simple functions. Therefore M_p≤w_p−1.

For the reverse inequality, [EW] gives 3≤M_p≤6, so the finite minimum
nonmixing order exists. Apply [DM, Lemma 5] with n=M_p. Proposition 3.1 and
the constant-field calculation convert its n+1 summands to constant times
monomials in K. Its nonconstant-ratio condition makes their exponent pairs
distinct. Clearing a common Laurent monomial produces a nonzero multiple
of f with n+1 terms. Therefore w_p≤M_p+1. The two inequalities prove the
claim. ∎

## 4. Uniform exclusion of five or fewer terms

We use the following elementary properties of a nonzero Laurent multiple
g=f h. After multiplying by a monomial, its support may be assumed to have
minimum x- and y-coordinates zero. This normalization does not change its
number of terms or divisibility in the Laurent ring.

The coefficients on the two extreme x-columns are nonzero multiples of
1+y². The coefficients on the two extreme y-rows are nonzero multiples
of 1+x⁴. This follows by multiplying the extreme coefficients of f and h;
the coefficient rings are integral domains. Every such extreme line
therefore contains at least two terms. The support has positive width in
both directions because widths add under polynomial multiplication.

**Lemma 4.1 (two-level exclusion).** No nonzero Laurent multiple of f
has only two distinct x-coordinates in its support. The analogous
statement holds for y-coordinates.

A two-column relation in K, after a monomial normalization, is
P(y)+x^m Q(y)=0, m>0, with both P and Q nonzero Laurent polynomials.
Since y is transcendental, Q(y) is nonzero in K. Thus x^m belongs to
F_p(y). Apply σ_x to get x^{-m}=x^m. This would give x^{2m}=1, impossible
for a transcendental x, also in characteristic 2. The y version uses σ_y. ∎

**Theorem 4.2.** w_p≥6 for every prime p. Consequently 5≤M_p≤6.

Suppose g has at most five terms. Its two extreme x-columns contain at
least two terms each. If all terms lie on these columns, Lemma 4.1 is a
contradiction. Otherwise exactly one term lies strictly between them, and
each extreme column has exactly two terms.

Take any β in an algebraic closure with β²=−1. Both extreme-column
coefficients vanish at β. Thus g(x,β) is a single nonzero Laurent monomial
in x. But

\[
 f(x,\beta)=\beta B(x)=\beta x(x^2+x+1).
\]

Divisibility f|g, evaluated at this nonzero β, implies that βB divides
g(x,β) in the Laurent ring over the algebraic closure. This is impossible:
x²+x+1 has a nonzero root in every characteristic, including its repeated
root in characteristic 3. The contradiction proves the theorem. ∎

This proof treats arbitrary exponents and arbitrary nonzero coefficients
in F_p. It is not a bounded search and does not assume a rectangular
support for g.

## 5. Exact characteristic-two result

**Theorem 5.1.** w_2=7 and M_2=6.

The polynomial f itself has seven terms, so it suffices to exclude a
multiple with at most six terms. Suppose such a multiple exists. Multiply
it by a Laurent monomial and repeatedly take polynomial square roots when
all exponent pairs have the same parity. In F_2 all nonzero coefficients
are 1, and if f divides H² then f divides H, since f is prime. Each root
step reduces the positive width, so this stops. We obtain a multiple g
with at most six terms and at least two exponent-parity classes.

Every extreme row or column has an even number of terms: its coefficient
is divisible by 1+x⁴ or 1+y² and hence vanishes at 1, while every
coefficient of g is 1. An extreme line with at least four terms, together
with the opposite extreme line having at least two, would exhaust the
six available terms. All support would then lie on two levels, contrary
to Lemma 4.1. Thus each of the four extreme lines has exactly two terms.

Join the two support points on each extreme line by an edge. This is a
graph with four distinct edges and at most six vertices. A vertex has
degree at most two, because it lies on at most one extreme x-line and one
extreme y-line. Horizontal edges have x-length divisible by 4: in F_2,
a binomial on such a line is divisible by (1+x)⁴ only if its exponent
difference is divisible by 4. Vertical edges similarly have y-length
divisible by 2. (The multiplicity of 1 as a root of 1+z^d is 2^{v_2(d)}.)
Consequently every connected component has a single exponent-parity class.

If the graph has no cycle, it has at most 6−4=2 connected components,
counting isolated interior points. Therefore g has at most two parity
classes. It cannot have exactly two: writing

\[
 g=x^a y^b H^2+x^c y^d J^2
\]

would make a monomial with distinct exponent parity a square in K,
contradicting Proposition 3.1. Here H and J are nonzero in K: each has
fewer than six terms, so Theorem 4.2 excludes its divisibility by f.
The one-class case was removed by descent.

The only possible cycle is a rectangle using all four edges: a cycle must
alternate horizontal and vertical edges, and there are only four edges.
Its four vertices are the bounding-box corners. There are at most two
additional, isolated points. Unless there are three distinct parity
classes, the preceding argument again applies. The only remaining case
therefore has four corner terms in one parity class and two single terms
in different nonzero classes relative to it. Dividing by a corner
monomial, the relation in K has the form

\[
 H^2+U+V=0,\qquad U=x^a y^b,\quad V=x^c y^d,
\]

where (a,b) and (c,d) are distinct nonzero elements of (Z/2Z)².

Using the derivation and R from Section 3, differentiation gives

\[
 U(a+bR)+V(c+dR)=0.
\]

Both parenthesized factors are nonzero. Thus U/V belongs to F_2(x).
Applying σ_y gives y^{2(b-d)}=1, so b=d as integers. If b is even, the
nonzero parities of U and V would both be (1,0), a contradiction. If b is
odd, one x-exponent is even and the other odd. Therefore one of

\[
 x^{a-c}=R/(1+R),\qquad x^{a-c}=(1+R)/R
\]

must hold. But

\[
 R/(1+R)=(x+1)^2/x.
\]

Its order at x=1 is 2, and the reciprocal has order −2, whereas a monomial
x^{a-c} has order zero there. This is impossible in F_2(x).

All cases have been excluded. Therefore w_2=7, and Corollary 3.2 yields
M_2=6. ∎

The even-face-count step specifically uses coefficients in F_2. For odd
p, three nonzero coefficients can sum to zero. Merely reusing the parity
graph argument in odd characteristic would be invalid.

## 6. Odd-characteristic six-term obstruction and exact remaining gap

For an odd prime, Theorem 4.2 and Corollary 3.2 give a precise dichotomy:

- M_p=5 if a six-term nonzero Laurent multiple of f exists over F_p;
- M_p=6 if every nonzero Laurent multiple has at least seven terms.

A necessary normal form reduces the first search, without resolving it.
For a six-term multiple g, the two extreme x-columns have exactly two
terms each and exactly two terms lie between them. Indeed, zero interior
terms contradict Lemma 4.1; one interior term gives the specialization
contradiction in Theorem 4.2. After a monomial normalization write

\[
 g=P(y)+x^N Q(y)+e x^r y^u+h x^s y^v,
 \quad 0<r,s<N,
\]

where P,Q are binomials divisible by 1+y² and e,h are nonzero. If r=s,
the two interior monomials have distinct y-exponents.

**Proposition 6.1.** For every odd p a multiple of this form satisfies

\[
 3\mid(r-s),\qquad 2\mid(u-v),\qquad
 h/e=-(-1)^{(u-v)/2}.
\]

At either root β of y²+1 the extreme columns vanish, and
B(x) divides eβ^u x^r+hβ^v x^s. If r≠s and p≠3, the two distinct primitive
cube roots force 3|(r−s) and eβ^u+hβ^v=0. If p=3, x²+x+1=(x−1)²;
the value and derivative at x=1 give the same conclusions. If r=s,
divisibility forces the displayed binomial to vanish identically, and
3|(r−s) is automatic. Using both β and −β (distinct in odd
characteristic) now gives even u−v and the stated coefficient relation. ∎

These congruences are necessary, not sufficient. They do not bound N or
any exponent. The four finite searches in check.py find no smaller
multiple in their explicitly bounded multiplier boxes; they cannot prove
that no six-term multiple exists outside those boxes. Although [DM]
supplies an effective general procedure, that procedure and its effective
height bounds have not been executed here. No claim of a uniform answer
for odd primes is made.

## References

[W] Thomas Ward, *Six problems in algebraic dynamics*, updated December
2006, Problem A, p. 1. https://www.imath.kiev.ua/~skolyada/kevin.pdf

[EW] Manfred Einsiedler and Thomas Ward, *Asymptotic geometry of non-mixing
sequences*, Ergodic Theory and Dynamical Systems 23 (2003), 75–85,
Theorem 3.1. DOI: https://doi.org/10.1017/S0143385702000950 .
Author preprint: https://arxiv.org/abs/math/0204174 .

[DM] Harm Derksen and David Masser, *Linear equations over multiplicative
groups, recurrences, and mixing III*, Ergodic Theory and Dynamical Systems
38 (2018), 2625–2643; online publication 2 May 2017.
DOI: https://doi.org/10.1017/etds.2016.137 .
Author-hosted first-published PDF:
https://sites.lsa.umich.edu/hderksen/wp-content/uploads/sites/614/2018/05/A.I.a.55.pdf .
Lemma 5 is on provisional pp. 10–12; radical notation is on p. 6.
