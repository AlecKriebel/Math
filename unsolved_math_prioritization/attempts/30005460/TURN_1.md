# Turn 1: circuit slices and the limit of formal SOS identities

## Outcome and route

This turn tried two routes to the original fixed-exponent convexity problem: finding a counterexample inside sparse non-SOS forms whose odd powers are SOS, and improving the published exponent-raising addition identity without using extra information about the input decompositions. Both routes yield exact restrictions on where a solution can come from, but neither settles the original target.

The first result proves convexity on every fixed single-circuit support, including its coefficient-boundary cases. The second proves that the published exponent q+t−1 is optimal for a precisely defined universal two-variable preordering certificate. The latter is an obstruction to that proof template, not a counterexample to convexity in the real polynomial ring. No historical novelty is claimed for either elementary reduction.

## 1. Credited absorption input

Write C_q for the original set at fixed n,m and odd q. We use Blekherman–Kozhasov–Reznick, published Theorem 5.1:

`C_q + Sigma_(n,m) = C_q`.

For completeness, the mechanism is the binary form

`D_q(u,v)=((u+v)^q-u^q)/v`,

extended at v=0. It is nonnegative on all real u,v because the odd power is increasing. Its degree q−1 is even, so the classical binary-form theorem writes D_q as a sum of squares. Substitution shows `(p+s)^q=p^q+s D_q(p,s)` is SOS whenever p^q and s are SOS. Positive scaling also preserves C_q. Closedness follows from the continuous power map into the closed SOS cone. These are prior inputs, not new target resolutions.

## 2. Convexity on every fixed single-circuit support

Let A={alpha_0,...,alpha_r} be affinely independent vectors in `(2 N)^n`, all of the same positive even total degree m, with r>=1. Let beta be a distinct integer vector in the relative interior of conv(A). Write its unique barycentric coordinates as

`beta=sum_i lambda_i alpha_i`, `lambda_i>0`, `sum_i lambda_i=1`.

Consider the entire real coefficient subspace of forms

`f_(a,b)(x)=sum_i a_i x^(alpha_i) - b x^beta`.

Here the support is contained in A union {beta}; coefficients may vanish. Define, for a_i>=0,

`Theta(a)=product_i (a_i/lambda_i)^(lambda_i)`,

using the continuous value zero if any a_i is zero.

**Proposition 1.** For each fixed odd q there is a constant `c_(A,beta,q) in [0,1]` such that this subspace's intersection with C_q consists exactly of:

- if every beta coordinate is even: `a_i>=0` and `b<=c_(A,beta,q) Theta(a)`;
- otherwise: `a_i>=0` and `|b|<=c_(A,beta,q) Theta(a)`.

In particular, this intersection is a closed convex cone.

**Proof for positive outer coefficients.** Put

`g_s(x)=sum_i lambda_i x^(alpha_i)-s x^beta`.

First consider even beta. The set of s for which g_s is in C_q contains all s<=0, since then g_s is itself SOS. It is closed. It contains no s>1, since `g_s(1,...,1)=1-s<0`. Let c be its maximum nonnegative element; it exists and lies in [0,1]. For 0<=s<=c, write `g_s=(s/c)g_c+(1-s/c)g_0` if c>0. The second summand is SOS, so absorption proves membership; c=0 is immediate. Thus the parameter set is exactly `(-infinity,c]`.

If beta has an odd coordinate, changing the sign of that variable preserves every outer monomial and changes s to −s. Consequently membership is symmetric in s. The same scaling-plus-absorption argument proves that its closed parameter set is exactly `[-c,c]` for some c in [0,1]. This argument does not require the interior monomial itself to be a square.

For any a_i>0, positive diagonal variable dilation takes f_(a,b) to g_(b/Theta(a)). Indeed, the rows alpha_i are linearly independent: a linear relation among them has coefficient sum zero after taking total degrees, and affine independence then makes the relation trivial. Thus there is u in R^n solving

`alpha_i dot u=log(lambda_i/a_i)` for every i.

Under `x_j -> exp(u_j)x_j`, the outer coefficients become lambda_i and the inner coefficient becomes

`b exp(beta dot u)=b product_i(lambda_i/a_i)^(lambda_i)=b/Theta(a)`.

Invertible real variable substitution preserves SOS in both directions, and it commutes with taking the q-th power. This establishes the asserted criterion when all a_i are positive.

**Coefficient boundary.** Nonnegativity forces every outer a_i to be nonnegative. To see this for a nonzero coefficient, expose alpha_i by a linear functional that is strictly larger there than at the other support points, and evaluate at positive coordinates `x_j=t^(v_j)` as t tends to infinity. A negative coefficient would eventually dominate with a negative sign.

If some a_i=0, add epsilon times the sum of all outer monomial squares. The resulting nonnegative form has positive outer coefficients. Its normalized value at a suitable point gives `b<=Theta(a+epsilon)` in the even-beta case, and `|b|<=Theta(a+epsilon)` otherwise. Letting epsilon decrease to zero gives b<=0 or b=0, respectively. Every such remaining boundary form is itself SOS. This proves the criterion on the boundary without assuming continuity of an unknown SOS representation or applying positive diagonal dilation to a zero coefficient.

**Convexity.** The weighted geometric mean Theta is concave and positively homogeneous on the nonnegative orthant. One direct proof of its superadditivity is to normalize positive coefficient vectors by their Theta-values A,B and apply concavity of log to the convex combination with weights A/(A+B), B/(A+B). The products of the normalized coordinates have weighted geometric mean one, so `Theta(a+d)>=Theta(a)+Theta(d)`. Limits include zero coordinates. Therefore `b<=c Theta(a)` is a convex hypograph. In the odd-beta case, the triangle inequality together with the same superadditivity proves convexity of `|b|<=c Theta(a)`. Closedness follows from continuity. This finishes the proof. □

The proposition is a fixed-support statement. It does not say that the union over different circuit supports, sums of arbitrary circuits, or sums of unrelated GL-transforms of a circuit form remain in C_q.

## 3. The Motzkin test family cannot supply a counterexample

Take outer exponents `(4,2,0),(2,4,0),(0,0,6)` and inner exponent `(2,2,2)`. The barycentric weights are all 1/3. Let c_k be the published threshold for

`M_s=x^4 y^2+x^2 y^4+z^6-s x^2 y^2 z^2`

at q=2k+1. Proposition 1 gives the exact, albeit threshold-parametrized, characterization

`(A x^4 y^2+B x^2 y^4+C z^6-D x^2 y^2 z^2)^q is SOS`

if and only if `A,B,C>=0` and `D<=c_k (ABC)^(1/3)`.

This includes zero outer coefficients and arbitrarily negative D. Hence arbitrary positive diagonal rescalings and positive multiples of the same Motzkin family cannot witness nonconvexity by addition. The result is stronger than checking the original one-parameter line, but does not determine the unknown c_k.

The family is genuinely larger than ordinary SOS already at q=3: the published degree-eighteen identity gives M_1^3 SOS, while the Newton-polytope coefficient argument excludes M_1 itself from SOS. The supplied checker verifies that full polynomial identity exactly. The known bound is `c_1 >= (15/13)^(1/3)`; the much larger numerical estimates in the paper are explicitly experimental and are not used as exact endpoints here.

The source's stubborn Motzkin endpoint also cannot be the sum of two forms admitting some odd SOS power, by the published convexity of the union. More generally, a fixed-exponent counterexample must have a sum that acquires an SOS representation at a later odd exponent. An all-odd-powers obstruction would contradict the known union theorem rather than solve the fixed-exponent question.

## 4. Sharp exponent barrier for universal formal identities

Let u,v be independent **formal** variables, and q,t positive odd integers. Define the preordering

`T_(q,t)=SOS[u,v]+u^q SOS[u,v]+v^t SOS[u,v]+u^q v^t SOS[u,v]`.

Substituting actual polynomials p,r with p^q and r^t SOS turns every element of T_(q,t) into an SOS polynomial. Thus a membership identity for (u+v)^N would be a universal certificate using only these two input powers and polynomial SOS multipliers in the formal variables.

**Proposition 2.** For odd N>=1,

`(u+v)^N in T_(q,t)` if and only if `N>=q+t-1`.

**Necessity.** Split all SOS multipliers into their square summands. On the positive quadrant, each weighted square is nonnegative. In a representation of a homogeneous degree-N polynomial, compare the largest total degree: its leading weighted squares cannot cancel on that quadrant, so no summand can have degree above N. Compare the smallest degree similarly, so no summand can start below N. Therefore every nonzero summand must be homogeneous of degree exactly N. This forces its squared polynomial to be homogeneous as well.

Since N is odd, the terms weighted by 1 or u^q v^t have the wrong parity and vanish. The representation reduces to

`(u+v)^N=u^q A(u,v)+v^t B(u,v)`,

with homogeneous SOS A,B of the necessarily even degrees N−q,N−t when nonnegative. In particular, the left side lies in the monomial ideal `(u^q,v^t)`. If N<q+t−1, set `i=min(q−1,N)` and `j=N−i`. Then `i<q`, `j<t`, but the coefficient of u^i v^j in (u+v)^N is the positive binomial coefficient. Neither ideal summand can contain that monomial. This is a contradiction.

**Sufficiency at N=q+t−1.** This is exactly the Blekherman–Kozhasov–Reznick Theorem 5.3 identity before substitution. Explicitly, split the binomial expansion at i=q:

`(u+v)^N = v^t sum_(i=0)^(q−1) binom(N,i) u^i v^(q−1−i)`

`             + u^q sum_(j=0)^(t−1) binom(N,q+j) u^j v^(t−1−j)`.

Both multiplier forms are nonnegative binary forms of even degree, hence SOS, by the truncated-binomial theorem of Pinelis reproduced as Theorem 5.2. Here its hypothesis N>q−1 and N>t−1 holds. The second multiplier is the same truncation with the variables exchanged and binomial coefficients reflected. For any larger odd N, multiply this certificate by the square `(u+v)^(N-(q+t-1))`. □

In particular, no same-q certificate of this formal type exists for q=t>=3: its first permitted odd output exponent is 2q−1. This exactly matches the known general addition bound.

**Crucial scope limit.** This is not a nonconvexity theorem for C_q. A genuine SOS decomposition of `(p+r)^q` may use polynomial expressions in the original variables that are not polynomials in p,r, or may exploit the actual summands in the given SOS representations. Proving nonmembership in this smaller formal preordering does not prohibit those representations. Passing from this universal algebraic obstruction to a counterexample in a real polynomial ring is an unproved step, not an implicit consequence.

## 5. Remaining original gap

No pair p,r has been certified with p^q and r^q SOS but `(p+r)^q` not SOS, and no full addition theorem has been obtained. The simple single-circuit search family is now rigorously excluded, and a formal identity that ignores input decompositions cannot improve the exponent. Further turns must use richer supports, interactions between actual Gram representations, or a justified realization of a stronger obstruction. This is substantive turn 1 of 5; the original target remains active and unresolved.
