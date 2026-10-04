# Tautological projection on A_g: five routes and the remaining product obstruction

Problem 30006276 / OWR-14299284-004. Status: **unsolved**.

This note does not prove or disprove the question. It gives elementary reductions,
checks the precise scope of published results, and supplies exact controls for
potential witnesses. No novelty or priority is claimed for these reductions.

## 1. Exact target and conventions

Work over the complex numbers. For every integer g >= 1, let A_g be the smooth
Deligne-Mumford stack of principally polarized abelian varieties of dimension g.
All Chow groups and cohomology groups have rational coefficients. Write

    A = CH*(A_g),  R = Q[lambda_1,...,lambda_g] inside A,
    d = g(g+1)/2,  N = g(g-1)/2.

Here lambda_i = c_i(E), for the rank-g Hodge bundle E. Chow degree means
codimension, not cohomological degree. The presentation is

    R = Q[lambda_1,...,lambda_g] / (c(E)c(E^dual)-1, lambda_g).

Its socle is in degree N, and multiplication gives perfect pairings
R^i x R^(N-i) -> R^N. The squarefree monomials in lambda_1,...,lambda_(g-1)
are an additive basis. These are established inputs [S2, S3].

For a smooth proper toroidal compactification X of A_g, let a bar denote an
extension of a Chow class to X. The Hodge bundle has its canonical extension.
Define the degree-N functional

    epsilon(a) = integral_X bar(a) lambda_g.

Boundary vanishing of lambda_g makes this independent of the extension and of
the chosen compactification [S2, Theorem 3]. The fact that lambda_g vanishes
on the open A_g does not make this integral zero: the lambda_g in the integral
is the class of the extended bundle on X.

The degree-preserving projection P:A -> R is characterized by

    epsilon(P(a) r) = epsilon(a r) for every r in R.

The full question is whether P(ab)=P(a)P(b) for every g and every a,b in A.
The original source is Question 1 on printed page 1492 of [S1]. The June 2026
version of [S4] retains precisely this assertion as Conjecture 8.

This target is not a statement about an unspecified projection, integral
coefficients, a toroidal compactification, the Chow ring of a fixed abelian
variety, or the total space of the universal abelian variety.

## 2. Route 1: Frobenius-pairing and kernel algebra

### 2.1 Exact reduction

The defining identity and the perfect pairing on R imply

    P(ar) = P(a)r  (a in A, r in R),     P|R = identity.

Indeed, test the proposed identity against any complementary s in R and use
epsilon(ars)=epsilon(P(a)rs). Thus A=R direct-sum K as graded R-modules, where
K=ker(P).

Put k_a=a-P(a). Expanding a=P(a)+k_a and b=P(b)+k_b gives

    D(a,b) := P(ab)-P(a)P(b) = P(k_a k_b).                 (2.1)

The two mixed terms vanish by R-linearity. Consequently the following are
equivalent:

1. P is a ring homomorphism.
2. K is an ideal of A.
3. P(K K)=0.
4. P(k^2)=0 for every k in K.
5. For every homogeneous k,l in K and r in R of total degree N,
   epsilon(klr)=0.

For 3 -> 2, use A=R+K and R-linearity. For 4 -> 3 use
2kl=(k+l)^2-k^2-l^2. The square in item 4 need not be homogeneous; the
polarization argument does not force a same-codimension witness.

Equivalently, extend epsilon by zero outside degree N and let

    Rad_epsilon(A) = {a in A : epsilon(ab)=0 for every b in A}.

Then the target is K=Rad_epsilon(A). The containment Rad_epsilon(A) subset K
is immediate. If K is an ideal, epsilon(kb)=epsilon(P(kb))=0. Conversely,
if K subset Rad_epsilon(A), testing (2.1) against R proves D=0.

This is an exact reformulation, not a proof that the equality of kernels holds.

### 2.2 A genuine geometric control against an automatic proof

Let X=E_1 x E_2 with product principal polarization, where the E_i are complex
elliptic curves. Let a=[{0} x E_2], b=[E_1 x {0}], and theta=a+b. In CH*(X),

    a^2=b^2=0,    degree(ab)=1,    theta^2=2ab.

On the subalgebra Q[a,b], projection to Q[theta] defined by the ordinary
intersection pairing satisfies

    P_X(a)=theta/2,    P_X(a^2)=0,    P_X(a)^2=ab/2 != 0.

Equivalently k=a-b has P_X(k)=0 and P_X(k^2)=-2ab. The restricted trace
pairing on the basis (1,theta,ab) has determinant -2, and P_X is R-linear.
Thus a perfect restricted pairing and the module property do not imply
multiplicativity, even in a Chow-theoretic example.

This is NOT a counterexample on A_2: its cycles are divisors on a single
abelian surface, and its trace is the ordinary degree. A_2 has a different
Chow ring and a lambda_2-weighted compactification pairing. [S4, Proposition
39] explains the corresponding general fixed-fibre phenomenon.

**Outcome:** the formal approach stops at the unsupported inclusion
K K subset K. The exact control prevents declaring that inclusion automatic.

## 3. Route 2: cohomology, degree bounds, and low genus

### 3.1 Homologically trivial classes cannot witness failure

Here is a direct explanation in characteristic zero. One may first pass to a
finite smooth level cover and a smooth normal-crossing toroidal
compactification X, then divide integrals by the covering degree. Let
D=X minus A_g. Boundary vanishing implies that cl(lambda_g) restricts to zero
in H^(2g)(D). By the exact sequence of the pair (X,D), choose a lift

    u in H^(2g)(X,D) = H_c^(2g)(A_g)

mapping to cl(lambda_g). For any extended algebraic class bar(a), compatibility
of relative cup product with integration gives

    integral_X cl(bar(a)) cl(lambda_g)
      = integral_(A_g) cl(a) u.

The same identity holds after inserting a tautological test class. If cl(a)=0
on A_g, every such integral is zero, and P(a)=0. Thus

    H := ker(CH*(A_g) -> H^(2*)(A_g,Q)) is an ideal contained in K.

P descends to the algebra of algebraic cohomology classes, and R embeds in
that algebra: a homologically trivial r in R satisfies r=P(r)=0. In
particular, if a-r is homologically trivial for some r in R, then

    P(ab)=r P(b) for every b in A.

It is therefore insufficient to exhibit a cycle non-tautological in Chow.
A witness to failure must have a genuinely non-tautological algebraic
cohomology component in each factor. This also explains why transferring the
fixed-fibre example of Section 2 to the moduli stack is unjustified.

The reduction does not assert that all algebraic cohomology of A_g is
tautological. That assertion, or the weaker required radical statement for
its non-tautological part, has not been proved here.

### 3.2 Finite degree tests versus an all-genus theorem

For homogeneous a in A^i and b in A^j, D(a,b)=0 whenever i+j>N, because
R^(i+j)=0. If all algebraic cohomology in degrees below r (in Chow grading)
is tautological, a failure must have i,j>=r and hence 2r<=N.

For g<=3 the entire rational Chow ring is tautological [S3, Section 1.3], so
the full projection is the identity in those genera. This gives no induction
step for higher genus. In particular, stable-cohomology statements in fixed
degree cannot by themselves cover every degree up to N as g grows.

**Outcome:** reduction to the non-tautological algebraic cohomology pairing;
no general description of that pairing, and no moduli-space counterexample.

## 4. Route 3: nonsimple support, Hodge splitting, and excess intersections

Let I be the subgroup consisting of finite sums of cycles supported on loci
of nonsimple abelian varieties. More precisely, use pushforwards from the
Noether-Lefschetz loci parametrizing abelian varieties with a nontrivial
abelian subvariety of a fixed dimension and polarization type. This excludes
the separate real-multiplication loci whose general member is simple.
Intersection with any class preserves these supports, so I is an ideal.

Set lambda=lambda_(g-1). After the finite covers used to record the subvariety
and its complementary factor, the Hodge bundle splits as E_u direct-sum
E_(g-u). Both summands have vanishing top Chern class on their open moduli
spaces. The two terms of c_(g-1) of this direct sum therefore vanish.
The projection formula, with rational coefficients to divide covering
degrees, yields

    lambda I=0, hence lambda P(I)=0.

In R one has

    Ann_R(lambda)=lambda R,     lambda^2=0.              (4.1)

For completeness, use the squarefree basis. Multiplication by lambda sends
each basis monomial not containing lambda to the distinct basis monomial
obtained by adding lambda, and kills those already containing lambda.
This proves (4.1). Consequently P(I)P(I)=0.

The remaining side, P(I I)=0, is not a consequence of this annihilator
calculation alone. It is the geometric content of [S3, Proposition 13 and
Theorem 6]. Its excess-intersection argument separates components with a
vanishing excess top Chern class from components containing a repeated
positive-dimensional isogeny factor. On the latter, the extended Hodge bundle
contains two copies of that factor's Hodge bundle; its squared top Chern
class vanishes by the compactified Chern relation. This makes the
lambda_g-weighted integrals vanish, including for supported cycles rather
than just fundamental classes.

It follows that P is multiplicative on R+I: expand two elements of R+I, use
R-linearity on the mixed terms, and use the preceding two vanishings on
I I. In particular, no pair of nonsimple-supported cycles can supply the
counterexample envisaged by a naive product-locus search.

This does not imply D(A,I)=0. For arbitrary a and i in I, both P(ai) and
P(a)P(i) are in lambda R, but they need not be equal merely because both
are in that square-zero ideal. There is also no proof here that A=R+I.
Real multiplication and cycles with generally simple members are not
covered by the two-supported-factor theorem.

**Outcome:** the proposed Noether-Lefschetz-product obstruction is unavailable;
the mixed product and general-support gaps remain. Tests of (4.1) for g=2,...,8
are controls for the algebra, not new geometric cases.

## 5. Route 4: Torelli pullback and explicit self-product targets

For g>=2 let T:M_g^ct -> A_g be the proper Torelli morphism. Use the source's
normalization J_g=T_*1, rather than silently replacing it by the reduced
image cycle. Its codimension is

    c_g=(g-2)(g-3)/2,    N-c_g=2g-3.

For a homogeneous alpha, the homomorphism property with J_g is equivalent to

    integral_(bar M_g) T^*(bar(alpha)-bar(P(alpha))) T^*(bar(r)) lambda_g = 0

for every r in R^(N-c_g-deg(alpha)). This follows by the projection formula
and the defining nondegeneracy of P. It is an intersection calculation, not
an implication from the nonzero or zero value of a Torelli pullback in Chow.

### 5.1 Product-locus pruning

For a partition g=g_1+...+g_k with k>=2, the product cycle has codimension
q=sum_(i<j) g_i g_j. Pairing it with J_g is automatic if q>2g-3.
There are exactly four possible shapes left, up to ordering:

    (1,g-1), (2,g-2), (1,1,g-2), and (3,3) at g=6,

with only positive parts and the obvious small-genus restrictions.

Proof: for two parts, put 1<=r<=g/2. For r>=3,
r(g-r)-(2g-3)=(r-2)g-r^2+3 >= (r-1)(r-3), with equality possible only
at r=3,g=6. For k>=3, the minimum of q among positive k-part partitions is
(k-1)(g-k/2), achieved by (1,...,1,g-k+1). For k=3 this is 2g-3 and
only the indicated partition attains it. For k>=4, subtracting 2g-3 and
using g>=k gives at least (k-2)(k-3)/2>0.

[S4, Theorem 7] verifies the (2,g-2) cases through g=8 and the (3,3) case.
These are established prior cases, not a general product calculation made
by this note. In particular, importing those cases cannot establish the
full question for arbitrary classes.

### 5.2 Self-intersection route

Try alpha=J_g instead. The degree bound gives

    2c_g<=N  if and only if  g<=7  (g>=2).

The classes J_g for g<=4 are tautological (the g=4 class is a divisor).
Thus only g=5,6,7 can provide a failure within this entire self-product
family. This is a filter for possible tests, not a claim that any of these
three cycles fails multiplicativity.

Using the published values of P(J_g) in [S4, Section 1.3], reduction in R
gives the following necessary right-hand sides:

    P(J_5)^2 = 55296 lambda_1 lambda_2 lambda_3 - 64512 lambda_2 lambda_4,

    P(J_6)^2 = (26844659712/691) lambda_1 lambda_2 lambda_4 lambda_5
                - (20497563648/691) lambda_3 lambda_4 lambda_5,

    P(J_7)^2 = (630538371072/691) lambda_2 lambda_3 lambda_4 lambda_5 lambda_6.

Let S_g=lambda_1...lambda_(g-1), and divide all degree-N epsilon evaluations
by epsilon(S_g), which is nonzero. The identity P(J_g^2)=P(J_g)^2 is
equivalent to the following scalar tests in each genus:

* g=5: epsilon(J_5^2 lambda_4)/epsilon(S_5)=55296 and
  epsilon(J_5^2 lambda_1 lambda_3)/epsilon(S_5)=377856.
* g=6: epsilon(J_6^2 lambda_3)/epsilon(S_6)=26844659712/691 and
  epsilon(J_6^2 lambda_1 lambda_2)/epsilon(S_6)=86881075200/691.
* g=7: epsilon(J_7^2 lambda_1)/epsilon(S_7)=630538371072/691.

The test monomials are full squarefree bases of R^4(A_5), R^3(A_6), and
R^1(A_7), respectively. Thus these are exact finite witness specifications.
The left-hand sides have NOT been computed in this attempt. Computing only
the right-hand sides provides neither evidence of equality nor a
counterexample. In particular, substituting P(J_g) for one J_g in the
left-hand integral would assume precisely the desired identity.

**Outcome:** a finite and explicit self-intersection test set, blocked on five
actual geometric intersection numbers. Even affirmative values would settle
only this family, not the full target.

## 6. Route 5: a compact realization and characteristic p

One possible proof mechanism would realize P as an actual ring-valued
restriction. Its sufficient hypothesis can be made precise without
assuming the conclusion.

Let U be a smooth ambient space with the above data (A,R,epsilon,N), and
let i:V -> U be a proper closed subspace of pure dimension N. Work in a
cohomology theory with cycle classes, pullback, and the trace pairing with
the fundamental class of V. Suppose that, in a proper compactification,

    [V] = c lambda_g,  c != 0,                           (6.1)

and that the image of algebraic cycle classes restricted from U to V equals
the image of R. Then P is a homomorphism.

Proof: restriction on R is injective. If a restricted r in R is zero, then
for every complementary s in R,

    0 = integral_V i^*(rs) = c epsilon(rs),

so r=0 by the perfect pairing. For a in A, choose r in R with equal
restriction. The same equation with a-r shows epsilon((a-r)s)=0, hence
r=P(a). Thus restriction identifies P with a ring homomorphism into its
image. No smoothness or Poincare duality for V is being assumed; the
fundamental-class trace and (6.1) suffice. In characteristic p use an
appropriate rational l-adic theory with l different from p.

Over C, the envisaged compact subvariety of codimension g does not exist
for g>=3 by Keel-Sadun [S6, Corollary 1.2]. Its absence obstructs this
particular realization and does not disprove multiplicativity.

In characteristic p, the p-rank-zero locus is a proper cycle of the right
dimension and its compactified class is a nonzero multiple of lambda_g
[S2, Section 1.3; S4, Section 1.8]. The crucial image equality required
above is not known here. Properness, the correct dimension, and the class
formula alone do not supply it. Notice again that (6.1) is a compactified
class statement, not a nonvanishing assertion about lambda_g on the open.

The June 2026 discussion in [S4] also explains a specialization route from
all positive characteristics to cycles over the algebraic closure of Q,
and thence over C using homological equivalence. This should not be confused
with the weaker conjecture printed in its January v1: that separate
formulation is absent from v3. The universal positive-characteristic
multiplicativity input, and the restriction-image calculation just described,
remain unproved in this attempt.

**Outcome:** a proved sufficient restriction criterion, with its central
geometric hypothesis missing. No characteristic-zero or characteristic-p
full solution is obtained.

## 7. What is and is not established

The strongest unconditional output here is the exact obstruction (2.1), the
cohomological reduction, the support and degree exclusions, and the five
explicit scalar tests for the three remaining Torelli self-products. The
Noether-Lefschetz multiplicativity theorem and small-genus cases are prior
results, clearly attributed above. The fixed-surface example refutes a
formal shortcut but not the problem.

The unresolved mathematical obligation remains to prove

    epsilon(klr)=0 for all k,l in ker(P) and all complementary r in R,

or to provide a single genuine pair on some A_g for which it is nonzero.
None of the computations in this packet evaluates that expression for
unknown non-tautological moduli-space cycles. See SOURCES.md for source
locations and control_results.json for the bounded exact checks.
