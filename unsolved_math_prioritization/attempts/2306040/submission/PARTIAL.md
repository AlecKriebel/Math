# Problem 2306040: coefficient-sum partials and obstructions

Status: **unsolved; five substantive approaches exhausted**. This is an
AI-assisted research checkpoint, not a solution or a novelty claim.

## 1. Exact question and source status

Let S consist of holomorphic injective functions on D={z:|z|<1}, normalized
by f(z)=z+sum_{k>=2} a_k z^k; set a_1=1. The target is

    Delta_n(f) := sum_{j=0}^{n-1} |a_{2j+1}| - |a_n|^2 >= 0
    for every f in S and every integer n>=1.                         (Q)

Hayman–Lingham, arXiv:1809.07200v2, printed p.132, Problem 6.40,
formula (6.16), is the exact source. The preceding real-coefficient
inequality (6.15) is background, not the entire open question. The
update reports no progress. The original 1977 collection gives the same
question on p.140, equations (6.2)–(6.3), attributed to C. FitzGerald.
A bounded literature search on 2026-10-04 found no full resolution.
That is not a certification that all literature has been searched.

The source attributes an eventual-in-n result for each f to unpublished
work of D. Bshouty. We do not possess or reconstruct that complete proof,
and do not count that attribution as an already-solved full target.
The proof of the Bieberbach conjecture does not by itself settle (Q).

## 2. Approach 1: a positive-measure identity

Suppose

    f(z)=integral_{-1}^1 z/(1-2tz+z^2) dmu(t),

where mu is a probability measure. Put U_0(t)=1, U_1(t)=2t and
U_{m+1}(t)=2t U_m(t)-U_{m-1}(t). Expansion of the denominator gives

    a_k=integral U_{k-1}(t) dmu(t).

For every n>=1 the polynomial identity

    U_{n-1}(t)^2 = sum_{j=0}^{n-1} U_{2j}(t)                      (1)

holds. To prove it, first put t=cos(theta), 0<theta<pi. The recurrence
gives U_m(cos(theta))=sin((m+1)theta)/sin(theta), while summing the
geometric progression of exp(i(2j+1)theta) gives
sum_{j=0}^{n-1}sin((2j+1)theta)=sin(n theta)^2/sin(theta).
The two sides of (1) agree on (-1,1), hence as polynomials, including
at t=+/-1.

Consequently the exact deficit has the expression

    Delta_n(f)
      = Var_mu(U_{n-1})
        + sum_{j=0}^{n-1} (|a_{2j+1}|-a_{2j+1}) >= 0.           (2)

Indeed, the signed sum is integral U_{n-1}^2 and a_n is its first
moment; subtracting a_n^2 gives the variance. Both terms in (2) are
nonnegative. This proves (Q) for the entire positive-measure class.
The standard Robertson representation theorem identifies this with the
normalized typically-real class, which is exactly the representation
invoked in the primary problem statement.

Every real-coefficient f in S is typically real: conjugation commutes
with f; if f(z) is real, injectivity implies z=conjugate(z). On the
connected upper half-disc, Im f therefore has constant sign, and the
normalization makes the sign positive near zero. Rotations
f_theta(z)=exp(-i theta) f(exp(i theta)z) preserve coefficient moduli,
so this conclusion also applies to rotations of this class.

**Extension obstruction.** Real-part symmetrization does not preserve S.
The normalized rotations k_i(z)=z/(1-i z)^2 and k_{-i}(z)=z/(1+i z)^2
are univalent, but their arithmetic mean is

    h(z)=z(1-z^2)/(1+z^2)^2,
    h'(z)=(1-6z^2+z^4)/(1+z^2)^3.

It has a critical point z=sqrt(2)-1 in D, and is not univalent.
Thus the representation cannot be transferred to general complex
coefficients by this symmetrization. The variance proof is a
reconstruction of known background, not a new universal theorem.

## 3. Approach 2: the exterior area theorem

The cases n=1 and n=2 hold for all f in S. The first is equality.
For n=2, define F(zeta)=1/f(1/zeta) on |zeta|>1. Injectivity and
normalization of f make F univalent with expansion

    F(zeta)=zeta-a_2+(a_2^2-a_3)/zeta+O(zeta^-2).

The exterior area theorem says that if
F(zeta)=zeta+b_0+sum_{k>=1}b_k zeta^-k is univalent there, then
sum_{k>=1}k|b_k|^2<=1. In particular |a_2^2-a_3|<=1, whence

    |a_2|^2 <= |a_3|+|a_2^2-a_3| <= |a_3|+1.

For completeness the area inequality follows by Green's area formula
on the Jordan curve F(R exp(it)), R>1: its bounded interior has area
pi(R^2-sum_{k>=1}k|b_k|^2 R^-2k)>=0. The curve is Jordan because
F is analytic and injective on a neighborhood of the circle; it has
positive orientation by its behavior at infinity. Taking R down to 1
and using monotone convergence proves the stated inequality.

**Gap.** The higher Laurent coefficients contain mixed products and
even-index coefficients. For example
b_3=a_2^4-3a_2^2a_3+a_3^2+2a_2a_4-a_5.
No elimination giving the required odd-modulus sum was obtained.
The area-theorem argument settles only n<=2 in unrestricted S.

## 4. Approach 3: the Robertson square-root route

For f in S, the normalized odd square root

    g(z)=sqrt(f(z^2))=z sum_{j>=0} b_j z^{2j}, b_0=1,

is holomorphic and univalent. Holomorphicity follows since f(z^2)/z^2
is nonvanishing on simply connected D; if g(z)=g(w), injectivity of f
gives z^2=w^2, and oddness excludes w=-z except z=0. The convolution
relation is

    a_n=sum_{j=0}^{n-1}b_j b_{n-1-j}.

The Robertson inequalities give sum_{j=0}^{m-1}|b_j|^2<=m; together
with Cauchy–Schwarz they imply |a_n|<=n. Attempting to obtain (Q) from
these numerical inequalities alone fails, as the following exact
control shows.

Take the formal polynomial B(w)=1+w^2-w^4/2. Its coefficient squares
have every initial sum <=m: the successive nonzero cumulative sums
are 1,2,9/4, reached at m=1,3,5 respectively; after m=5 the sum is
constant. Yet

    z B(z)^2=z+2z^3-z^7+z^9/4

has Delta_3=1+2+0-4=-1. It also satisfies all numerical Bieberbach
bounds |a_k|<=k.

This is **not** a counterexample to (Q). It is not univalent. At z=i y,
its derivative is 1-6t+7t^3+(9/4)t^4, with t=y^2; this is positive
at t=0 and negative at t=1/4, so it vanishes for some 0<t<1/4.
The control establishes exactly that the Robertson and Bieberbach
coefficient bounds, without additional univalence information, cannot
imply (Q). It does not rule out a deeper use of de Branges's theorem.

## 5. Approach 4: asymptotic regularity and bounded functions

Assume |a_k|/k tends to alpha with 0<alpha<1. Then

    (1/n^2) sum_{j=0}^{n-1}|a_{2j+1}| -> alpha,
    |a_n|^2/n^2 -> alpha^2,
    Delta_n/n^2 -> alpha(1-alpha)>0.                            (3)

To justify the first limit, for any epsilon>0 choose K so that
||a_k|-alpha k|<=epsilon k for k>=K. The finitely many earlier terms
have sum C independent of n, and sum_{j=0}^{n-1}(2j+1)=n^2. Thus
the absolute error after division by n^2 is at most C/n^2+epsilon.
Equation (3) follows, giving eventual strict positivity.

Hayman's regularity theorem supplies a limit 0<=alpha<=1 for f in S,
with alpha=1 only for Koebe rotations. These have
|a_k|=k and Delta_n=n^2-n^2=0 for every n. A primary proof and
statement are in Bshouty–Hengartner (1978), especially pp.228 and
231–233. This argument does not prove the alpha=0 case in general.

There is a separate elementary alpha=0 subclass: bounded f. If
|f|<=M on D, Parseval on each circle gives
sum_{k>=1}|a_k|^2 r^{2k}<=M^2, and monotone convergence gives
sum |a_k|^2<=M^2. Hence a_n->0. Eventually |a_n|<=1, and the term
a_1=1 alone proves (Q). The same last conclusion applies whenever
one independently knows a_n->0.

**Gap.** These results do not control the finite initial range n>=3
for general f, nor provide a uniform threshold. An eventual theorem,
even the stronger unpublished one reported by the source, cannot
settle the all-n question.

## 6. Approach 5: explicit slit-map constructions

Write k_u(z)=z/(1-u z)^2 for |u|=1 and define

    s_{q,u}=k_u^{-1}(q k_u(z)),  0<q<1,
    F_{q,u}(z)=q^-1 k_1(s_{q,u}(z)).                           (4)

The inverse is the branch taking zero to zero. Since k_u maps D
conformally onto the plane slit along the ray starting at -1/(4u),
q k_u(D) is contained in k_u(D). Thus s_{q,u} is an injective
self-map of D with derivative q at zero, and (4) belongs to S.
The same holds for a composition of such s maps, followed by k_1
and divided by the product of the q's. These are an explicit valid
family for counterexample searches, not arbitrary coefficient lists.

The inverse series is

    k_u^{-1}(y)=sum_{m>=1} (-1)^{m-1} C_m u^{m-1}y^m,
    C_m=(1/(m+1)) binomial(2m,m).

It follows by Lagrange inversion from z=y(1-u z)^2. Degree-N
truncations compute exactly the first N Taylor coefficients, since
all composed series have zero constant term.

Exact controls: verify.py tests q in {1/4,1/2,3/4} and
u in {1,-1,i,-i,(3+4i)/5,(3-4i)/5,(-3+4i)/5,(-3-4i)/5}.
All 24 functions pass n=1,...,5, for 120 inequalities. Coefficients
are Gaussian rationals; moduli are enclosed by certified rational
square-root bounds with denominator 10^40. A nonnegative lower
bound certifies each individual inequality.

Two exact controls prevent normalization errors. For u=1, (4)=k_1.
For u=-1,

    F_{q,-1}(z)=z/[1-2(2q-1)z+z^2],

which follows from k_1(w)=k_{-1}(w)/(1-4k_{-1}(w)). Its
coefficients are U_{k-1}(2q-1), also verified exactly.

Exploratory SciPy differential-evolution runs tested a one-switch
family for n=3,...,5 and a two-switch family for n=3,...,6. Seven
reported double-precision minima were slightly negative, between
about -6.2e-15 and -7.7e-10. Re-evaluation of the saved parameters
with 80 decimal digits gave positive deficits in every case. These
are cancellation artifacts at near-equality configurations, not
counterexamples. High-precision re-evaluation is a diagnostic, not
an interval proof; the 120 rational controls are the separate
certified computations.

**Gap.** Neither the exact finite grid nor the heuristic optimization
covers its continuous parameter box, functions with more switches,
or all S. No global optimization certificate or general inequality
was obtained.

## 7. Outcome and verification limits

The complete target (Q) remains unresolved here. Strongest proved
partials: n<=2 for all S; all n for the positive-measure/typically-real
class and rotations; eventual validity for positive Hayman index
and for bounded functions. These are reconstructions or elementary
consequences of established facts; no priority is claimed.

The exact controls demonstrate specific failed shortcuts and finite
valid examples. They are not a computer proof of an infinite family
or of univalence of an arbitrary coefficient list. The function
constructions' univalence comes from the analytic argument in §6.
The remaining task is to prove (Q) for arbitrary complex-coefficient
f in S at every n>=3, or produce one genuinely univalent violation.

Reproduce the exact controls with `python3 verify.py`. Optional
floating searches and 80-digit diagnostics live in `exploratory/`;
their dependencies and seeds are recorded there. No network access
is needed for either verification path.
