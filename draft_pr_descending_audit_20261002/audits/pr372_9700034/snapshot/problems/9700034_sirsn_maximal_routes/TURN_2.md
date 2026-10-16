# Author turn 2: a countably sampled increment criterion

**Original general question unresolved, 2/5 substantive turns.**
This turn gives a sufficient condition stated entirely through finite-
dimensional route-length laws, and an exact scalar obstruction at its
critical exponent. The latter is not a SIRSN counterexample. The proof uses
the classical dyadic-chaining mechanism; no novelty claim is made.

## 1. A finite-dimensional criterion with a quantitative bound

Let Q=[−1,1]^2 and write F(z)=len R(0,z), with F(0)=0. The notation refers
to the coherent, measurable finite-dimensional laws in the SIRSN definition;
a jointly measurable continuum realization is not assumed. Independently
sample U_1,U_2,... uniformly from the unit disc and use the corresponding
countable extension of the route laws. Suppose there are p≥1, alpha>2/p and
C<infinity such that for all deterministic u,v in Q,

    E |F(u)−F(v)|^p ≤ C |u−v|^(alpha p).                 (1)

The bound is about the joint law of the two lengths, not a bound on their
separate marginal moments.

**Theorem.** With M=sup_i F(U_i),

    ||M||_p ≤ 9^(1/p) 2^(alpha/2) C^(1/p)
                 / [1−2^(−(alpha−2/p))].               (2)

In particular E M<infinity. No independence between different route lengths
is required. More generally an integrable F(0) contributes its L^p norm to
the right side.

### Proof

Put h_n=2^(−n) and G_n={−1+jh_n:0≤j≤2^(n+1)}^2. Thus G_0 has nine points
and every G_n contains 0. For n≥1, send each grid point to its parent in
G_(n−1) by rounding each coordinate down to the coarser grid. The distance
to the parent is at most sqrt(2)h_n. For G_0 use 0 as the common parent.
Let A_n be the maximum absolute F-increment over these grid-parent pairs.

For a finite family of random variables, the p-th power of their maximum is
at most the sum of their p-th powers. Since |G_n|≤9·4^n, (1) gives, for n≥0,

    ||A_n||_p ≤ B 2^(−n(alpha−2/p)),
    B=9^(1/p)2^(alpha/2)C^(1/p).                         (3)

The n=0 estimate uses the bound sqrt(2) on distance to 0. Minkowski and
monotone convergence show that H=sum_(n≥0) A_n is finite almost surely and
||H||_p≤B/[1−2^(−(alpha−2/p))]. Every grid value satisfies |F(g)|≤H by
following its finite chain of parents. All statements so far concern only
a fixed countable set of endpoints.

For each sampled U_i, let g_n(U_i) be its coordinatewise floor on G_n.
The endpoint measurability in the source permits integration of the joint
law for (0,u,g_n(u)). Consequently

    E |F(U_i)−F(g_n(U_i))|^p
          ≤ C 2^(alpha p/2) 2^(−n alpha p).             (4)

For each fixed i and epsilon>0, Markov's inequality makes the probabilities
of an error exceeding epsilon summable in n. Borel–Cantelli, first for
rational epsilon>0 and then for the countably many i, proves simultaneous
convergence F(g_n(U_i))→F(U_i) almost surely. Since every grid value is
bounded by H, every F(U_i) is bounded by H. Taking the countable supremum
proves (2).

For clarity about construction: jointly sample the endpoints U_i; conditional
on their locations, the consistent measurable finite-dimensional network
kernels give joint laws for the fixed dyadic grid and these countably many
endpoints. The ordinary countable extension theorem constructs that law.
The preceding argument stays in this countable extension. It neither
selects a pathwise measurable realization on all of R^2 nor identifies an
uncountable supremum with the sampled one.

## 2. A route-length triangle hypothesis makes the criterion checkable

Add the following hypothesis to a SIRSN:

(TM) The lengths of the prescribed routes obey the triangle inequality on
     every fixed finite endpoint configuration, almost surely.

For example, (TM) holds if routes are shortest paths for Euclidean arclength
in an underlying network. It need not hold for minimum-travel-time routes
with unequal speeds, and is not part of Aldous's general axioms.

If in addition E[D^p]<infinity for some p>2, where
D=len R(0,(1,0)), then (TM) gives

    |F(u)−F(v)| ≤ len R(u,v)       almost surely,

by the two triangle inequalities using 0,u,v. Translation, rotation and
scale invariance imply

    E[len R(u,v)^p] = |u−v|^p E[D^p].

Thus (1) holds with alpha=1 and C=E[D^p], and

    ||M||_p ≤ 9^(1/p)sqrt(2) ||D||_p / [1−2^(−(1−2/p))]. (5)

This supplies an explicit sufficient pair of additional assumptions. It
is not asserted that (TM), a high route-length moment, or (1) follows from
the ordinary SIRSN axioms. The theorem in §1 also applies without (TM) if
the increment bound is obtained by some other route-stability argument.

## 3. Why the strict chaining exponent matters

We give a scalar random field on Q with all of the following properties:

- F(0)=0 and F(u)≥|u|;
- every fixed-point marginal has all positive moments, uniformly on Q;
- E|F(u)−F(v)|² ≤ (2+4pi)|u−v|²;
- nevertheless, for independent uniform U_i in the unit disc,
  sup_i F(U_i)=infinity almost surely.

This is not a planar route construction, does not satisfy the SIRSN axioms,
and does not disprove that a second moment might suffice in a SIRSN with
additional geometric structure. It proves only that the critical increment
estimate p=2, alpha=1 cannot by itself replace the strict condition in §1,
even if all individual marginal moments are also supplied.

### Construction

Use the unit flat torus, represented by [−1/2,1/2)^2. On the embedded disc
of radius exp(−1), put

    g(x)=log log(1/|x|),             0<|x|<exp(−1),

and put g=0 outside that disc and at x=0. Extend g periodically to R^2.
Changing its value at the isolated centers has no measure-theoretic effect.
The value at the disc boundary is 0, so g has no jump there.
For a uniform torus point Z and t≥0,

    P(g(Z)>t) = pi exp(−2 exp(t)).                       (6)

Thus g has all positive moments. Its weak gradient is square integrable:

    integral_T² |grad g|²
      = 2pi integral_0^(exp(−1)) dr/[r log²(1/r)]
      = 2pi.                                           (7)

One can avoid assuming any Sobolev theorem here. Truncate g at level N and give each isolated center the value N;
this changes the truncation only on a null set. The resulting g_N is
Lipschitz and radial on its support. The
fundamental theorem of calculus along line segments and Cauchy–Schwarz,
followed by integration over the uniform translation, give

    integral_T² |g_N(x+h)−g_N(x)|² dx
       ≤ |h|² integral_T² |grad g_N|² dx ≤ 2pi|h|².

The truncations converge in L² by (6); passing to the limit proves

    E |g(u−Z)−g(v−Z)|² ≤ 2pi |u−v|².                    (8)

Define the scalar field

    F(u)=|u| + |g(u−Z)−g(−Z)|.

Its measurability and the first two claimed properties are immediate.
Using reverse triangle inequalities twice, then (a+b)²≤2a²+2b² and (8),
proves the displayed critical increment bound. For every q>0, a fixed
F(u) is bounded by sqrt(2)+g(u−Z)+g(−Z), giving uniform finite q-th moments.

Finally, the representative Z lies in the interior of the unit disc, since
|Z|≤1/sqrt(2). With probability one g(−Z) is finite. For every integer m,
a punctured neighborhood of Z has F(u)>m and has strictly positive area.
Conditional on Z, the independent uniform sequence hits this neighborhood
almost surely; indeed it hits it infinitely often. Intersecting the
probability-one events over integer m proves the infinite sampled supremum.

The rare endpoint sets here shrink faster than exponentially in the length
level. This isolates why averaged increment or marginal control at a critical
exponent does not automatically control the existence of extreme endpoints.

## 4. Scope and next mechanism

The increment criterion and (TM)+p>2 corollary are sufficient conditions,
with a proof compatible with the original sampled/FDD setup. No implication
from the ordinary axioms to those conditions has been found. The scalar
critical example cannot be promoted to a network counterexample.

A distinct next route is to quantify the limiting fraction of sampled
endpoints whose route exceeds a threshold. Such a criterion can be expressed
through exchangeable finite-dimensional lengths and may avoid postulating
(TM). A useful sufficient condition must control the presence of very small
positive-mass endpoint sets; one-point moments alone control their average
mass, which is a different quantity.
