# Subcritical WARM on bounded-degree graphs: a candidate homogenization proof

Status: author-checked candidate proof, prepared for independent adversarial review.
No priority, publication-readiness, or independent-verification claim is made.

## 1. Precise claim and conventions

Let G=(V,E) be a countable, undirected, simple graph. Remove isolated vertices,
which have no effect on any edge. Assume 1 <= d(v) <= D < infinity and let the
vertex firing rates satisfy 0 < p_v <= P < infinity. There is **no** assumption
that inf_v p_v is positive. Fix 0 < alpha < 1 and write

    c = 1-alpha,        beta = alpha/c.

The continuous-time WARM starts with N_e(0)=1 on every edge. Independently at
vertex v, a rate-p_v Poisson clock rings. At each ring an incident edge e is
selected with probability N_e^alpha / S_v(N), where

    S_v(N) = sum_{f incident to v} N_f^alpha,

and its count is increased by one. Write X_e(t)=N_e(t)/t. The bounded-degree,
bounded-rate assumptions give the usual locally finite graphical construction.
All stochastic assertions below are on the common probability-one event for the
countably many relevant coordinates.

**Candidate theorem.** There is exactly one strictly positive equilibrium x,
meaning an array with x_e>0 for every edge and

    x_{uv} = x_{uv}^alpha [p_u/S_u(x) + p_v/S_v(x)].                 (1)

Moreover, for every edge e, X_e(t) -> x_e almost surely as t -> infinity.
The convergence is coordinatewise; no spatially uniform stochastic convergence
is asserted. The endpoint alpha=0 is treated separately in Section 9.

The strict-positivity qualifier is indispensable. If arbitrary nonnegative
fixed points are allowed, even the infinite path with p_v=1 has the two
alternating arrays (2,0,2,0,...) and (0,2,0,2,...), in addition to the all-ones
array, as fixed points for every 0<alpha<1. Each vertex sees one nonzero incident
edge, so its denominator is nonzero. Thus the literal assertion of uniqueness
among all nonnegative fixed points is false. The intended non-vanishing
homogenization problem is addressed here. Initially zero edges also require a
different statement, because the dynamics never reinforce them.

## 2. Positive equilibria in vertex coordinates

For a positive edge equilibrium set

    z_v = p_v/S_v(x).

Equation (1), after division by x_{uv}^alpha, gives

    x_{uv}^c = z_u+z_v,
    x_{uv} = (z_u+z_v)^(1/c).

Consequently the vertex variables solve

    z_v T_v(z) = p_v,
    T_v(z) = sum_{w adjacent to v} (z_v+z_w)^beta.                 (2)

Conversely a positive solution of (2) gives a positive edge equilibrium by the
same formula. The correspondence is bijective. Every solution of (2) obeys

    z_v <= (p_v/d(v))^c <= B := P^c,                              (3)

because T_v(z) >= d(v) z_v^beta and beta+1=1/c. In particular every
positive equilibrium gives a bounded vertex array, without any prior
boundedness assumption on that equilibrium.

### 2.1. Existence, with a genuine infinite-volume passage

Choose finite sets F_n increasing to V. For a fixed F=F_n set z_w=0 outside F
and minimize, over z_v>0 for v in F,

    Phi_F(z) = sum_{edges {u,v} meeting F}
                 (z_u+z_v)^(beta+1)/(beta+1)
               - sum_{v in F} p_v log z_v.                      (4)

There are finitely many terms. Every coordinate belongs to at least one edge.
The positive-power terms dominate the logarithms at infinity. For example,
the edge sum dominates a positive multiple of sum_{v in F} z_v^(beta+1),
since each vertex is counted at least once and an edge has at most two
endpoints in F. Thus sublevel sets are bounded. On a bounded sublevel set,
approaching any coordinate hyperplane makes the corresponding -p_v log z_v
term diverge to plus infinity, while the other terms remain bounded below.
Therefore Phi_F has an interior minimum. It is strictly convex, because each
-p_v log z_v is strictly convex and the other terms are convex.

The first-order equations at the minimum are exactly (2) for v in F, using
zero external values. Estimate (3) holds. Using it in the opposite direction
also gives, for v in F,

    z_v >= L_v := p_v/[d(v)(2B)^beta] > 0.                        (5)

For a vertex in F its neighbors, including external zero values, are all at
most B. These bounds depend on v but not on n once v belongs to F_n.
By a diagonal subsequence in the countable product of compact intervals,
the finite-volume minimizers converge coordinatewise. Local finiteness permits
passage through each finite sum in (2), and (5) keeps each limiting coordinate
strictly positive. This produces a positive solution z. This step invokes
compactness explicitly; finite-volume strict convexity alone is not a proof
of infinite-volume uniqueness.

### 2.2. Uniqueness by an approximate maximum principle

Let z and y be two positive solutions of (2), both bounded by B. Suppose
M=sup_v |z_v-y_v|>0. By swapping z and y if necessary, for arbitrarily small
epsilon>0 there is v with z_v-y_v>M-epsilon. For every neighbor w,

    (z_v+z_w)-(y_v+y_w) >= -epsilon.

Let omega(epsilon) be a modulus of continuity of r -> r^beta on [0,2B].
Then

    T_v(z) >= T_v(y)-D omega(epsilon).

Since z_v>=M-epsilon, T_v(z)>=(M-epsilon)^beta. Subtracting the two
vertex equations in the following order gives

    0 = z_v T_v(z)-y_v T_v(y)
      = (z_v-y_v)T_v(z) + y_v[T_v(z)-T_v(y)]
      >= (M-epsilon)^(beta+1)-BD omega(epsilon).

For sufficiently small epsilon the final expression is strictly positive,
a contradiction. Thus z=y. By the correspondence, the positive edge
equilibrium is unique.

## 3. The exact transform and positive linear growth

This estimate does not require a spatially uniform random starting time.
For an edge e={u,v}, its reinforcements are a subset of the firings at u and v.
Poisson strong laws therefore imply

    limsup_{t -> infinity} X_e(t) <= p_u+p_v <= 2P.               (6)

Set

    q_e(t) = p_u/S_u(N(t-)) + p_v/S_v(N(t-)),
    Q_e(t) = integral_0^t q_e(s) ds.

The stochastic intensity of N_e(t)-1 is

    lambda_e(t) = N_e(t-)^alpha q_e(t).                          (7)

Define for positive integers n

    H(n) = sum_{j=1}^{n-1} j^(-alpha),       H(1)=0.

Its jump from n to n+1 is exactly n^(-alpha). Integral comparison gives

    H(n)=n^c/c+O(1),                                            (8)

where the O(1) is deterministic and uniform in n. Equation (7) gives the
exact compensated decomposition

    H(N_e(t)) = Q_e(t)+M_e(t),                                  (9)

with M_e a square-integrable martingale on every finite time interval,
M_e(0)=0, and

    <M_e>(t) = integral_0^t N_e(s-)^(-alpha) q_e(s) ds <= Q_e(t).  (10)

Here N_e>=1. Also lambda_e<=p_u+p_v and q_e<=p_u+p_v, so the asserted
finite-time integrability is immediate.

### 3.1. A compensator-normalized martingale law

Whenever Q_e(t)->infinity, (10) implies

    M_e(t)/Q_e(t) -> 0 almost surely.                           (11)

Here is a direct proof to specify the normalization precisely. Put A=1+Q_e
and L(t)=integral_0^t A(s)^(-1) dM_e(s). Since A is adapted and continuous,
the integrand is predictable. Its bracket satisfies

    <L>(infinity) <= integral_0^infinity (1+Q_e(s))^(-2) dQ_e(s)
                  <= 1.

Thus L is L2 bounded and converges almost surely. Integration by parts gives

    M_e(t)/A(t) = L(t)-A(t)^(-1) integral_0^t L(s) dA(s).

On A(t)->infinity the two terms have the same limit: this is the elementary
weighted Cesaro fact for an increasing continuous A. Hence M_e/A->0, and
(11) follows. This argument uses no independence among the edges and no
pure-birth coupling.

### 3.2. The compensator diverges fast enough

Fix epsilon>0. There are only finitely many edges incident to u or v, so (6)
implies that after a finite random time all their counts are at most
(2P+epsilon)t. Consequently, eventually,

    q_e(t) >= k_{e,epsilon} t^(-alpha),
    k_{e,epsilon} = [p_u/d(u)+p_v/d(v)]/(2P+epsilon)^alpha > 0.    (12)

In particular Q_e(t)->infinity and

    liminf Q_e(t)/t^c >= k_{e,epsilon}/c.

Equations (8), (9), and (11) now give

    N_e(t)^c/(c Q_e(t)) -> 1,

and therefore, letting epsilon decrease to zero,

    liminf X_e(t) >= m_e :=
        ([p_u/d(u)+p_v/d(v)]/(2P)^alpha)^(1/c) > 0.               (13)

This holds simultaneously for all e by countability. The m_e need not be
bounded away from zero. Neither (6) nor (13) asserts a common random time
after which all edges satisfy their bounds.

## 4. The scaled vertex representation and its error

By (6) and (8), H(N_e(t))=O(t^c) almost surely. From (9) and (11),
Q_e(t)/H(N_e(t))->1. Hence Q_e(t)=O(t^c), and another application of
(11) yields

    M_e(t)/t^c -> 0 almost surely.                              (14)

This deduction is coordinatewise and does not require any spatial martingale
maximum bound. The positive lower growth estimate was not used to prove
(11), so there is no circular dependence.

Introduce nonnegative vertex variables

    A_v(t) = c t^(-c) integral_0^t p_v/S_v(N(s)) ds,      t>0.     (15)

The value at a jump time in the Lebesgue integral is immaterial. Equations
(8), (9), and (14) imply the key identity

    X_{uv}(t)^c = A_u(t)+A_v(t)+r_{uv}(t),
    r_{uv}(t) -> 0 almost surely.                               (16)

The cancellation in (9) is exact; no Taylor-remainder summation or assumed
convergence of the original stochastic process is hidden in (16).

## 5. Coordinate bounds and logarithmic-time dynamics

Nonnegativity in (15), together with (6) and (16), gives

    limsup A_v(t) <= K := (2P)^c                                (17)

for every v, since v has a neighbor. Also, eventually for every fixed v,
S_v(N(t)) <= d(v)(2P+epsilon)^alpha t^alpha. Integrating this lower bound
for the integrand in (15), and letting epsilon decrease to zero, gives

    liminf A_v(t) >= ell_v := p_v/[d(v)(2P)^alpha] > 0.           (18)

Write a_v(s)=A_v(exp(s)). Direct differentiation of (15) gives, for almost
every s,

    a_v'(s) = c [p_v/S_v(X(exp(s)))-a_v(s)].                     (19)

The derivative is meant in the locally absolutely continuous sense.
For each fixed v, (6) and (13) for the finitely many incident edges bound the
right-hand side in absolute value at all sufficiently large s. Thus the
translates a_v(s_n+.) are uniformly Lipschitz on each compact time interval,
once s_n -> infinity, with a bound allowed to depend on v.

## 6. Complete limiting trajectories: the infinite-dimensional step

Take any sequence s_n -> infinity. On each compact time interval, (17)-(19)
give uniform boundedness and equicontinuity for each fixed coordinate.
Arzela-Ascoli followed by a diagonal subsequence over the countable vertices
and the intervals [-j,j] produces coordinatewise locally uniform limits

    a_v(s_n+s) -> b_v(s),       s in R.

Every limit is a complete trajectory, defined for all real s, and obeys

    ell_v <= b_v(s) <= K.                                      (20)

Because r_e(t)->0, it tends to zero uniformly on every shifted compact
logarithmic-time interval. Passing through the finite incident-edge sums in
(16) and (19) is justified by local uniform convergence and strictly positive
coordinate lower bounds. The limiting integral equation, and hence the
classical differential equation, is

    b_v'(s) = c [R_v(b(s))-b_v(s)],
    R_v(b) = p_v/T_v(b),
    T_v(b) = sum_{w adjacent to v}(b_v+b_w)^beta.                 (21)

This passage uses only finite neighborhoods and a countable diagonal
extraction. It does not assume compactness or uniform convergence in the
supremum norm. In particular, the failure of uniform spatial Poisson bounds
at a fixed time has not been discarded.

## 7. Rigidity of bounded positive complete trajectories

**Lemma.** Let z be the positive solution of (2). Every coordinatewise positive
complete classical solution b of (21) with a common upper bound K_0 is
identically z. No common positive lower bound for b or p is required.

**Proof.** Increase K_0 if necessary so that K_0>=B. Let

    M = sup_{v in V, s in R} |b_v(s)-z_v| < infinity.

Assume M>0. Set d_v(s)=b_v(s)-z_v. Let omega be a modulus of continuity of
r^beta on [0,2K_0]. Choose epsilon with 0<epsilon<M/4 so small that

    BD omega(epsilon)/(M/2)^beta < M/4.                         (22)

Such an epsilon exists for every fixed beta>0.

If d_v(s)>=M-epsilon, then d_w(s)>=-M for every neighbor w, so
T_v(b)>=T_v(z)-D omega(epsilon). Also b_v(s)>=M-epsilon>M/2, and therefore
T_v(b)>=(M/2)^beta. Since p_v=z_v T_v(z),

    R_v(b)-z_v = z_v[T_v(z)-T_v(b)]/T_v(b)
               <= BD omega(epsilon)/(M/2)^beta < M/4.

Equation (21) implies throughout this upper strip

    d_v'(s) <= -cM/2.                                         (23)

If d_v(s)<=-M+epsilon, then d_w(s)<=M for all w, giving
T_v(b)<=T_v(z)+D omega(epsilon). Now z_v>=M-epsilon>M/2, so
T_v(z)>=(M/2)^beta, and

    R_v(b)-z_v
      >= -z_v D omega(epsilon)/[T_v(z)+D omega(epsilon)]
      >= -BD omega(epsilon)/(M/2)^beta > -M/4.

Thus throughout the lower strip

    d_v'(s) >= cM/2.                                          (24)

By definition of M some v,s_0 has |d_v(s_0)|>M-epsilon. Suppose first the
sign is positive. Going backwards in time, d_v cannot leave the upper strip
through its lower boundary: (23) forces it strictly downwards in forward
time there. More formally, a first forward crossing from below the boundary
into the upper strip would contradict (23), and integrating (23) on any
interval in the strip excludes such a crossing. Hence d_v stays in the
strip for all s<=s_0. Integrating (23) backwards then gives

    d_v(s) >= d_v(s_0)+(cM/2)(s_0-s),       s<=s_0,

contradicting d_v(s)<=M. If the sign is negative, the identical backwards
argument with (24) contradicts d_v(s)>=-M. Therefore M=0. QED.

The use of a supremum over both space and all real times is deliberate.
No vertex attaining a spatial supremum is assumed. The lemma avoids a
potentially unjustified differentiability assertion for an infinite
supremum norm. It also avoids any infinite sum of Lyapunov-function terms.

## 8. Completion of the stochastic argument

Every logarithmic time-shift subsequential limit from Section 6 is a bounded
positive complete trajectory of (21), and hence is z by Section 7.
It follows that a_v(s)->z_v for each v: otherwise a sequence of times at
which one fixed coordinate remains a fixed distance from z_v would have a
subsequence as in Section 6, whose value at time zero contradicts Section 7.
Finally (16) gives

    X_{uv}(t)^c -> z_u+z_v,
    X_{uv}(t) -> (z_u+z_v)^(1/c)=x_{uv}.

The convergence holds simultaneously for all edges because E is countable.
Section 2 proves that x is the unique positive equilibrium. This establishes
the candidate theorem under the exact hypotheses stated in Section 1.

## 9. Endpoint, scope, and checks against overclaiming

* For alpha=0 the incident choice is uniform, and the reinforced-edge count
  has deterministic asymptotic rate p_u/d(u)+p_v/d(v), by Poisson thinning and
  the strong law. The unique positive equilibrium has these coordinates.
* Negative alpha is not part of the nonnegative reinforcement exponent
  convention in the cited model and is not claimed here.
* Alpha=1 is excluded; c=0 destroys both the transform asymptotics and the
  damping argument. The alternating positive equilibria at criticality on
  even cycles are consistent with this exclusion.
* Bounded degree and bounded above positive rates are used. Mere local
  finiteness with unbounded degrees is not asserted.
* Neither connectivity, regularity, transitivity, amenability, nor a uniform
  positive rate lower bound is used. Isolated vertices are ignored.
* The stated stochastic proof uses unit initial counts, the initialization
  in the cited paper. It extends without changing any estimates to arbitrary
  deterministic positive integer initial counts, finite on each edge: in
  (12) subtract H(N_e(0)), whose contribution after scaling vanishes. No
  uniform bound on those initial counts is needed for the coordinatewise
  estimates. Fractional starting weights can be handled by replacing H with
  the edge-specific sum over N_e(0)+j, but that extension is not needed for
  the stated theorem.
* No claim is made of uniqueness among boundary fixed points, uniform-in-edge
  stochastic convergence, a quantitative stochastic rate, or prior novelty.
* Finite-graph simulations and algebra checks accompanying this manuscript
  are diagnostics, not a replacement for the infinite-graph argument.

## 10. Primary context and bibliographic references

1. V. Kleptsyn, joint work with C. Hirsch and M. Holmes, “Graph-based interacting
   Pólya urns,” in MATRIX-MFO Tandem Workshop: Stochastic Reinforcement Processes
   and Graphs, Oberwolfach Reports 12/2023, pp. 653-656, especially pp. 654-655,
   Conjecture 1. https://doi.org/10.4171/OWR/2023/12
2. Y. Couzinié and C. Hirsch, “Weakly reinforced Pólya urns on countable networks,”
   Electronic Communications in Probability 26 (2021), paper 35.
   https://doi.org/10.1214/21-ECP404 ; inspected author version:
   https://arxiv.org/abs/2010.03347 (v2, 25 June 2021).
3. Y. Couzinié, “Sublinearly reinforced Pólya urns on graphs of bounded degree,”
   master's thesis, Ludwig-Maximilians-Universität München, 17 September 2018.
   https://www.theorie.physik.uni-muenchen.de/TMP/theses/couziniethesis.pdf

The cited results and their dated status motivate the question; they are not
used as substitutes for the new arguments in Sections 2-8. The strong law for Poisson processes, compensated counting-process
martingales, L2-bounded martingale convergence, weighted Cesaro convergence,
and Arzela-Ascoli are the standard general tools explicitly used in the proof.
