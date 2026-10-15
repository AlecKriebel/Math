# Author turn 3: tail visibility in the sampled route law

**Original unresolved, 3/5 substantive turns.**
This turn stays in Aldous's countably sampled finite-dimensional setup. It
gives sufficient conditions and a two-route obstruction criterion through
the mass of long-route endpoints. The basic exchangeability mechanism is
classical; the needed special case is proved below, so no unverified
continuum representation or de Finetti input is hidden.

Let L_i=len R(0,U_i) and M=sup_i L_i. The measurable FDDs and the independent
identically distributed endpoints make (L_i) exchangeable: every finite
permutation has the same joint law. Distinct lengths are not assumed
independent. For t≥0 define

    a(t)=P(L_1>t),       b(t)=P(L_1>t,L_2>t).

## 1. Exact asymptotic endpoint frequencies

There is a jointly measurable nonincreasing right-continuous random function
Q(t), 0≤Q(t)≤1, such that, for each deterministic t,

    Q(t)=lim_(N→infinity) N^(−1) sum_(i=1)^N 1{L_i>t}
             almost surely and in L²,                  (1)
    E Q(t)=a(t),             E Q(t)²=b(t),               (2)
    {M>t}={Q(t)>0} almost surely.                        (3)

The equality in (3) can be taken simultaneously for every real t. Thus

    E M = integral_0^infinity P(Q(t)>0) dt.              (4)

By contrast E L_1 is the integral of E Q(t). The distinction between the
presence of a positive tail mass and its average magnitude is the central
issue. Neither quantity can be replaced by the other without an estimate.

### Elementary exchangeability proof

Fix t and put I_i=1{L_i>t}, Q_N=N^(−1)sum I_i. For m≥n, symmetry gives

    E Q_n² = a/n+(1−1/n)b,
    E Q_n Q_m = a/m+(1−1/m)b,
    E(Q_n−Q_m)² = (a−b)(1/n−1/m).                       (5)

Hence Q_n has an L² limit Q with E(Q_n−Q)²=(a−b)/n. Taking n=k² and using
Chebyshev plus Borel–Cantelli gives Q_(k²)→Q almost surely. The counts
sum_(i≤n) I_i are nondecreasing; squeezing between consecutive squares,
whose ratio tends to one, gives Q_n→Q almost surely along every n.

The limit is unchanged by any finite permutation of the sequence. For any
event B invariant under finite permutations, exchangeability implies

    E[I_1 1_B]=E[Q_n 1_B]→E[Q 1_B].                     (6)

With B={Q=0}, this shows I_1=0 on B almost surely, and the same holds for
every i. Conversely, if all I_i vanish, their empirical limit is zero.
Therefore Q>0 is precisely the event that some L_i>t. Passing to limits
in (5) proves (2).

Do this first for all nonnegative rational t on a common probability-one
event. Their limits are nonincreasing. Define

    Q(t)=sup{Q(r): rational r>t}.

This is right-continuous and jointly measurable. Since E Q(r)=P(L_1>r),
monotone convergence as rationals decrease to t shows that the new Q(t)
agrees almost surely with the empirical L² limit at each fixed t: that
limit dominates all Q(r) with r>t, and the two nonnegative quantities have
the same expectation.
Moreover {M>t} is the union of {M>r} over rational r>t, which proves the
simultaneous (3). Tonelli gives (4). Equation (6) extends by truncation to
nonnegative invariant random multipliers, a fact used below.

## 2. Lower visible mass gives sufficient conditions

Let h(t) be a deterministic measurable function with 0<h(t)≤1. Suppose,
for almost every t, almost surely,

    Q(t)=0 or Q(t)≥h(t).                                (V_h)

Then 1{Q(t)>0}≤Q(t)/h(t), and

    E M ≤ integral_0^infinity a(t)/h(t) dt.              (7)

This is a checkable non-concentration requirement on the sampled endpoint
law, not a consequence of exchangeability.

In a SIRSN, invariance gives the distributional identity

    L_1 =_law R D,       P(R∈dr)=2r dr, 0≤r≤1,          (8)

with R and a representative of the unit-distance length D independent.
It follows by conditioning on the endpoint, and implies

    a(t)=integral_0^1 2r P(D>t/r) dr ≤P(D>t),
    E L_1^s = [2/(s+2)] E D^s, s>0.                     (9)

For h(t)=c(1+t)^(−alpha), 0<c≤1 and alpha≥0, (7) becomes

    E M ≤ E[((1+L_1)^(alpha+1)−1)]/[c(alpha+1)].          (10)

Thus E D^(alpha+1)<infinity and (V_h) suffice. A uniform positive visible
mass (alpha=0) requires only the ordinary first moment and gives
E M≤E L_1/c. The mass hypothesis itself remains additional.

### Random visibility without an independence assumption

Suppose V≥1 is measurable with respect to the invariant sigma-field of
the sampled length sequence
and for almost every t,

    Q(t)>0 implies Q(t)≥V^(−1)(1+t)^(−alpha).            (11)

Using (6) with truncated V and then monotone convergence gives

    E M ≤ E[V ((1+L_1)^(alpha+1)−1)/(alpha+1)].           (12)

Consequently, for any r>1 with conjugate r'=r/(r−1), it suffices that
E[V^r]<infinity and E[D^((alpha+1)r')]<infinity. Hölder applies to the joint
law; V is not presumed independent of L_1. In a stronger jointly measurable
continuum realization, Q(t) equals the normalized area of the set of
endpoints whose route length exceeds t. Then a geometric lower bound on
that area's positive values implies (V_h) or (11). This interpretation is
optional, not a realization theorem from the bare FDD axioms.

## 3. Negative-frequency moments and a two-route lower bound

A hard positive lower bound on every nonzero Q can be relaxed. For q>0 set

    R_q(t)=E[Q(t)^(−q) 1{Q(t)>0}],

with the product assigned value zero when Q=0. Hölder on the positive set,
with exponents (q+1)/q and q+1, gives

    P(M>t) ≤ a(t)^(q/(q+1)) R_q(t)^(1/(q+1)).            (13)

Indeed write 1=Q^(q/(q+1))Q^(−q/(q+1)) there. Thus integrability of the
right side of (13) is sufficient. For example, if R_q(t)≤C(1+t)^beta for
t≥1 and some beta≥0, and E D^s<infinity with

    s q > beta+q+1,                                    (14)

Markov and (9) make that integral finite at infinity. The initial interval
is bounded by one using the trivial probability bound. These are additional
joint-law conditions; they do not follow from one-point moments.

In the other direction, Cauchy–Schwarz and (2) yield

    P(M>t) ≥ a(t)²/b(t),                               (15)

where 0/0 is assigned zero. If a>0 then b≥a²>0 by (2), so no positive
numerator is divided by zero. Therefore

    integral_0^infinity a(t)²/b(t) dt=infinity
         implies E M=infinity.                        (16)

This obstruction involves just two sampled routes. It can also be seen
without the limiting frequency: for S_N=sum_(i≤N)1{L_i>t},

    P(S_N>0) ≥ (E S_N)²/E S_N²
             = N a(t)²/[a(t)+(N−1)b(t)],                (17)

and then N→infinity gives (15). The pair correlation is essential. Applying
(16) to an abstract exchangeable law is not a SIRSN counterexample unless
that law has been realized by routes satisfying all geometric axioms.

## 4. Finite maximal lengths can still have infinite mean

Here is an explicit scalar diagnostic different from turn 2's infinite
almost-sure maximum. Let J≥1 have P(J=j)=2^(−j). Conditional on J=j, let
the L_i be independent, each equal to 2^j with probability epsilon_j=2^(−j²)
and equal to 1 otherwise. This is an exchangeable sequence, and

    E L_1^s ≤ 1+sum_(j≥1) 2^(−j²+(s−1)j)<infinity
                      for every finite s>0.            (18)

The negative quadratic exponent dominates its linear term; for sufficiently
large j it is at most −j²/2. But conditional on every J=j, an infinite
independent sample hits the value 2^j almost surely. Thus

    M=2^J<infinity almost surely,
    E M=sum_(j≥1) 2^(−j)2^j=infinity.                   (19)

More generally E M^q is finite precisely when q<1. The long-route tail mass
is positive but exceptionally small in the large-J environments. All
individual moments fail to control that positivity event. This sequence
has no asserted planar embedding, scaling covariance, route compatibility
or major-road intensity. It is an obstruction to scalar-moment shortcuts
only, and is not a counterexample to the original SIRSN question.

## 5. Remaining geometric question

The new criteria are formulated through the countably sampled laws already
available in the source. They need no route-length triangle inequality or
jointly measurable continuum realization. What is missing is a derivation
of suitable visibility/negative-frequency estimates from ordinary SIRSN
geometry, or construction of an actual SIRSN violating integrability.
The explicit scalar laws in this and the previous turn do neither.

A next substantive route should exploit compatibility and the rooted route
union, or investigate a genuine invariant network construction. Rephrasing
the missing visibility estimate as an assumption is not counted as solving
the unrestricted problem. All three proof mechanisms to date remain scoped.
