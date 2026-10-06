# A fixed rational moment separator with no rational quadratic-module certificate

Status: first-turn complete candidate for the literal question in OWR 14/2023,
printed pp.803–804. Independent source and proof review is required. The result
uses Scheiderer's explicit example and makes no novelty claim.

## 1. Exact claim and quantifiers

Write Q_F(g) for finite sums of squares of polynomials over F, together with
such sums multiplied by the displayed generators g_i, where F is Q or R.
No degree bound is imposed on the multipliers. A *rational SOS certificate*
means all polynomials being squared have rational coefficients. Merely listing
rational multiplier polynomials that are SOS over R is a weaker notion.

There exist a rational generator g with compact support K={g>=0}, an
Archimedean Q_Q(g), a rational vector y indexed by all monomials of total
degree at most four with y_0=1, and a rational polynomial p of degree four such
that:

1. y has no nonnegative Borel representing measure on K;
2. p>=1 on K and L_y(p)=0;
3. p belongs to 1+Q_R(g);
4. p does not belong to 1+Q_Q(g), even with arbitrarily high-degree multipliers.

This is an existential statement about one fixed p. It does not assert that y
has no other separator admitting rational SOS, that p itself has no rational
positivity certificate of any kind, or that a numerical relaxation necessarily
returns this p. In fact, the same example has a simpler rational separator.

The minimum of the exhibited p is exactly one. The stronger requirement
min_K p>1 is not asserted: for this ball it would exclude the phenomenon by
Powers's rational Putinar theorem. SOURCE_SCOPE.md explains why this distinction
matters when reading the companion preprint rather than the OWR question.

## 2. The explicit data

Use variables x,y,z and the known Scheiderer quartic

f = x^4 + x*y^3 + y^4 - 3*x^2*y*z - 4*x*y^2*z
    + 2*x^2*z^2 + x*z^3 + y*z^3 + z^4.

Set

    g = 1-x^2-y^2-z^2,   K = {g>=0},   p = 1+f.

For the moment vector, use the distinct notation m=(m_alpha)_{|alpha|<=4}:

    m_(0,0,0)=1,   m_(4,0,0)=-1,
    all other m_alpha=0.

There are binomial(7,3)=35 entries, all rational. Thus L_m(p)=1-1=0.
The vector cannot be represented by a nonnegative measure, even on all of R^3,
since the x^4 moment would be -1. Equivalently, a representing measure has
mass one while the integral of p>=1 could not vanish. No positive-semidefinite
moment-matrix hypothesis appears in the original question, and this vector
does not have that extra property.

The ball is nonempty and compact. Its rational quadratic module is
Archimedean because its displayed generator is 1-(x^2+y^2+z^2).

## 3. Credited input: the quartic is real SOS and not rational SOS

The explicit quartic is Scheiderer, JEMS 18 (2016), Theorem 2.1 and
Example 2.8, pp.1499–1502. For clarity the underlying argument is reproduced
below in independent wording; no theorem about moment separators is imported.

Let h(t)=t^4-t+1. It has no real roots. For t<=0 its value is at least one;
for 0<=t<=1, t^4+(1-t)>0; and for t>=1 it is at least one.
Its reduction modulo 2 is irreducible: it has no linear factor and is not
divisible by the sole irreducible monic quadratic t^2+t+1. Modulo 3 it factors
as (t+1)(t^3-t^2+t+1), whose cubic has no root in F_3; the factors are distinct.
The usual unramified factorization-cycle theorem gives a 4-cycle and a 3-cycle
in the Galois group. Its order divides 24 and is divisible by 12; a subgroup
of order 12 would be the index-two subgroup A_4 and contain no 4-cycle.
Consequently the group is S_4. This is also the computation in Example 2.8.

For the four roots alpha_i put l_i=x+alpha_i*y+alpha_i^2*z. A direct norm
calculation gives f=product_i l_i. Any three l_i are linearly independent by
the Vandermonde determinant. Complex conjugation partitions the four roots
into two pairs. Choosing one root from each pair, f=|l_1*l_2|^2 is a sum of
two squares of real quadratic forms. Hence f>=0 on R^3, p>=1, and p is in
1+Q_R(g). Since f(0)=0, min_K p=1.

Here is the obstruction to rational SOS. Each conjugate pair of the complex
projective lines {l_i=0} meets at a real projective point: their intersection
is stable under conjugation, hence its one-dimensional vector space has a
nonzero real vector. At both such points f=0. If f were a sum of squares
of rational quadratic forms q_j, each q_j would vanish at those real zeros.
Applying the S_4 Galois group to these rational equations forces each q_j
to vanish at all six intersections of pairs of the four lines. On any one
line the other three lines give three distinct points, by the Vandermonde
independence. A binary quadratic vanishing at three distinct projective
points is zero on that line. Thus each l_i divides each q_j. Their product
has degree four, so a quadratic q_j divisible by all four is zero. This
contradicts f nonzero.

There is no escape through inhomogeneous rational squares: for a sum of
squares equal to a homogeneous quartic, the highest-degree parts cannot
cancel and each summand has degree at most two. Evaluating the degree-zero
and then degree-two parts forces the constant and linear parts to vanish.
The summands would therefore be the rational quadratic forms just excluded.

An optional explicit real SOS identity is provided by any negative real root
beta of beta^3-4*beta-1=0, which exists in (-2,-1):

 U = 2*x^2 + beta*y^2 - y*z + (2+1/beta)*z^2,
 V = 2*x*y - y^2/beta + 2*x*z/beta + beta*y*z - z^2,

                    4*f = U^2 - beta*V^2.

Thus f=(U/2)^2+(sqrt(-beta)*V/2)^2. This is Scheiderer's displayed identity;
verify.py checks it exactly modulo the cubic, without floating point.

## 4. The quadratic-module obstruction has no degree loophole

Suppose, contrary to the claim, that

    f = sum_j a_j^2 + (1-x^2-y^2-z^2)*sum_k b_k^2

with a_j,b_k rational polynomials of arbitrary finite degrees. At the origin
both weights equal one. Since f(0)=0, every a_j(0) and b_k(0) is zero.
The homogeneous degree-two part of this identity is now the sum of the
squares of all their linear parts; the negative quadratic part of g contributes
nothing because the b_k constants vanish. Since f has no degree-two part,
all those linear parts vanish as well.

Every a_j and b_k now vanishes to order at least two. Taking homogeneous
degree four gives exactly

                  f = sum_j (a_j^[2])^2 + sum_k (b_k^[2])^2,

where [2] means the quadratic homogeneous part. Terms involving g-1 have
order at least six. This would be a rational SOS representation of f,
contradicting Section 3. The argument did not bound the degrees of a_j,b_k.
It proves p not in 1+Q_Q(g) with the original displayed generator unchanged.

More generally, if rational generators are strictly positive at a rational
point, the first nonzero homogeneous part of an element of Q_Q(g) at that
point must be rational SOS, after absorbing the positive rational weights
as rational sums of squares. The concrete ball proof needs no such additional
number-theoretic absorption because both weights at the origin are one.

## 5. Boundary controls and limitations

A different separator for the very same m is q=1+x^4. It has L_m(q)=0,
and q-1=(x^2)^2 is rational SOS. Therefore the claim cannot be reformulated
as unavoidable irrationality for all separators of the moment vector.

For every rational c>1, the rescaled separator cp still satisfies L_m(cp)=0,
but cp-1>=c-1>0 on K. Since g is a rational ball generator, Powers (2011),
Theorem 7, gives cp-1 in Q_Q(g). That theorem is credited, and no degree or
bit-size bound for its certificate is claimed. Thus the fixed normalization
p=1+f is essential; the associated ray contains rationally certifiable points.

Likewise, rationalizing the coefficients of the already rational polynomial f
is not the desired task. It is the decomposition into rational polynomial
squares, including the generator multiplier, that Section 4 excludes.

The example addresses the literal fixed-p existence question printed in OWR.
It does not settle the separate general descent question for arbitrary real
Archimedean rationally generated modules, the existence of rational certificates
at an algorithm's minimal relaxation degree, or the strict min p>1 variant
without a rational Archimedean certificate.
