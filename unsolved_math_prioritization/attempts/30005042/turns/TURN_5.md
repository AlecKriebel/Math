# Turn 5: common genealogical jump control at the exact endpoint

**Fifth substantive author turn, scoped partial. The original problem remains unresolved after5/5 turns.** This turn attacks a genuinely functional obstruction using the branching genealogy. Under the exact X log X hypothesis, all generations' macroscopic jumps lie at finitely many common random times, and the complete vectors of jump sizes converge in l2. This is stronger than the generic martingale observations in the earlier turns. It still leaves cumulative small-jump/path tightness unproved.

## 1. Statement

Use the original nondecreasing càdlàg integer-valued offspring process X, with E X(lambda)=lambda, and its coupled normalized generation sizes W_n. On a compact[a,b] contained in I, 1<a<b, assume

    E[X(b) log(e+X(b))]<infinity.                              (L)

For a càdlàg function f write Delta f(t)=f(t)-f(t-). There is a countable random set T contained in(a,b], containing every jump time of every W_n, with these almost-sure properties:

1. If

       B_t=sup_(n>=0) Delta W_n(t),

   then for every eta>0 only finitely many t in T have B_t>eta.

2. In fact

       sum_(t in T) B_t² < infinity.                           (1.1)

3. For each t in T there is a nonnegative limit j_t, and

       sum_(t in T) |Delta W_n(t)-j_t|² ->0.                    (1.2)

   Consequently the jump-size errors also converge uniformly over all t in T.

The set T can be taken to be the union of the actual prelimit jump sets, not a different set for each generation. The result is about jump vectors. Until path convergence is established, j_t is not automatically the jump of a càdlàg version of the scalar limit family.

There is also a quantitative count bound. Let C_(a,b) be any finite constant with

    sup_(theta in[a,b]) E sup_(r>=0) W_r(theta) <= C_(a,b).       (1.3)

Turn4 provides such a constant, for example2+R_1 in its notation. Then

    E #{t in T:B_t>eta}
       <= C_(a,b)(b-a)/[eta(a-1)].                             (1.4)

The parameter supremum in(1.3) remains outside expectation. The proof below uses it only after conditioning on a birth parameter independent of the relevant descendant subtree.

## 2. An equivalent nested genealogical realization

Attach independent copies X_v of the complete offspring process to every vertex v of the countable Ulam tree. At parameter lambda, retain child i of an existing vertex v exactly when i<=X_v(lambda). The active generation sets T_k(lambda) are nested in lambda, finite on each compact at each finite k, and have expected size lambda^k.

This realization has the same law as the source's generation-indexed iid-array recursion, jointly over the generation sequence and parameter functions. To see this, condition on all copies used before generation k. Order the finitely many generation-k vertices active at b by their first appearance in the parameter, breaking ties by an ancestral-data rule. The copies attached to these vertices are still independent with law X, independent of that past. At every parameter the active vertices form an initial segment of this ordering, so the conditional next-generation function is exactly the sum of the source's iid copies over an initial segment of length Z_k(lambda). Induction proves the same transition law on the càdlàg function space.

Equivalently, finite parameter lists give the same joint Markov kernel, and countable dense evaluations determine the finite-generation càdlàg laws. Thus the almost-sure path statements proved in this realization apply to the original coupling in law. They do not assert a pathwise equality under an arbitrary pre-existing relabelling of the arrays.

## 3. Intrinsic offspring jumps have no deterministic atoms or coincidences

On[a,b], each X_v has finitely many intrinsic jumps, because it is nondecreasing, integer-valued and bounded by the finite random variable X_v(b). At every deterministic theta in(a,b],

    E Delta X(theta)=theta-lim_(s up to theta)s=0.

Nonnegativity implies Delta X(theta)=0 almost surely. Independent copies therefore almost surely have no coinciding intrinsic jump times: condition on the finite jump set of one copy and use the preceding zero-probability statement for the other. Taking a countable union covers all pairs of Ulam vertices and a countable compact exhaustion.

An active intrinsic birth event e consists of a vertex v of depth k, an intrinsic jump time theta in(a,b] at which v was already present on the left, and the positive integer batch size

    J=Delta X_v(theta).

If v only becomes active later through an ancestral birth, its earlier intrinsic jumps are not counted as active events. Its already available descendants are instead part of that ancestral birth's new subtree. This distinction avoids double-counting simultaneous activation of an entire descendant cohort.

Let nu(dtheta,dJ) be the expected marked jump measure of a single offspring copy. Its first-moment identity is

    integral J nu(dtheta,dJ)=dtheta                              (3.1)

as measures on(a,b]. Indeed, summing the jump sizes on(c,d] gives X(d)-X(c), whose expectation is d-c. No Poisson assumption or independent increments are needed. The expected number of intrinsic jumps on a compact is finite as well, since J>=1.

## 4. Exact jump formula and a common envelope

At an active event e=(v,theta,J) of depth k, let W_r^(e,i)(theta), 1<=i<=J, be the normalized generation-r populations in the J newly added child subtrees, evaluated at theta, with W_0=1. The subtree copies are independent of the parent process and the ancestral data determining whether v is present. They remain iid after conditioning on the random child-label interval and its size J.

There are no other intrinsic jumps at theta, almost surely. Conditional on theta and the parent/ancestral data, all the new subtree copies have no intrinsic jump at that deterministic parameter. Therefore the exact finite-generation jump is

    Delta W_n(theta)=0,                              n<=k,
    Delta W_n(theta)=theta^(-k-1)
           sum_(i=1)^J W_(n-k-1)^(e,i)(theta),       n>=k+1.     (4.1)

This formula includes descendants already present at theta; no first-passage or asymptotic approximation is used. The normalizing factor lambda^(-n) is continuous, so it does not create another jump.

Put

    M_(theta,J)=sup_(r>=0) sum_(i=1)^J W_r^(i)(theta),
    B_e=theta^(-k-1) M_(theta,J).                              (4.2)

Then B_e is exactly the supremum of the jump sizes of all W_n at that event. Equation(1.3) gives

    E M_(theta,J) <= J C_(a,b).                                (4.3)

The maximum in(4.2) is over generations at one parameter; it is not a maximum over the parameter. The random parameter theta is independent of the descendant copies, so Fubini permits evaluation of the uniform pointwise bound(4.3) at theta. This is the precise independence needed here.

Each batch martingale in(4.2) is finite almost surely, and its sequence converges almost surely to sum_i W^(i)(theta). Scalar convergence first holds for each deterministic theta; conditioning on the independent random birth time and then taking a countable union over all possible events makes it simultaneous. Thus the right side of(4.1) has a limit at every active birth time.

## 5. Counting all macroscopic jumps in every generation

At fixed theta, the expected number of active depth-k parents on the left is theta^k. Their presence depends only on ancestral copies and is independent of their own marked jump processes and newly created child subtrees. Tonelli and conditioning therefore give

    E #{events e of depth k:B_e>eta}
       = integral theta^k
           P(M_(theta,J)>eta theta^(k+1)) nu(dtheta,dJ).          (5.1)

For any theta>1 and x>=0, summing the finite geometric prefix yields

    sum_(k>=0) theta^k 1_(x>eta theta^(k+1))
       <=x/[eta(theta-1)].                                    (5.2)

The subtree-batch law in(5.1) is independent of the parent's depth. Sum over k and apply(5.2), then(4.3) and(3.1):

    E #{e:B_e>eta}
       <= integral E M_(theta,J)/[eta(theta-1)] nu(dtheta,dJ)
       <= C_(a,b)(b-a)/[eta(a-1)].                             (5.3)

This proves(1.4) and finiteness of the macroscopic event set almost surely. There is no multiplication by the number of generations: the same intrinsic event's whole future jump sequence is bounded once by B_e.

The identity

    min(x²,1)=integral_0^1 2eta 1_(x>eta) d eta

and(5.3) show

    E sum_e min(B_e²,1)
       <=2 C_(a,b)(b-a)/(a-1)<infinity.                         (5.4)

Thus the small envelopes have summable squares and only finitely many envelopes exceed1. Each envelope is finite almost surely, so sum_e B_e²<infinity almost surely. This last uncapped sum need not have finite expectation.

By the noncoincidence result, active events have distinct times and account for every actual prelimit jump. Every event is visible already in generation k+1, when its jump is theta^(-k-1)J>0. We may consequently identify the events with the common jump set T of the sequence W_n, proving(1.1).

## 6. Convergence of the complete jump-size vectors

For each event of depth k define

    j_theta=theta^(-k-1) sum_(i=1)^J W^(e,i)(theta).

Section4 gives Delta W_n(theta)->j_theta simultaneously at all event times. Both quantities lie in[0,B_theta]. Equation(1.1) and dominated convergence for the countable sum give

    sum_theta |Delta W_n(theta)-j_theta|² ->0

almost surely. This proves(1.2), and its square root bounds the supremum of the jump-size errors.

In particular, after fixing eta>0, no arbitrarily late genealogy can introduce a new jump larger than eta across any generation: the finite set in(1.4) has finite maximum depth. Individual jump sizes at that set stabilize. This is an endpoint statement for the actual branching model, rather than the generic functional-martingale countercontrol from Turn3.

If a subsequence does converge in J1 to a càdlàg process, its jumps must be exactly the positive j_theta at these same times, and it has no negative jumps. One way to verify this conditional assertion is to use the J1 time changes. Uniform convergence after the time changes forces each nonvanishing jump to match a prelimit jump. For a fixed positive size threshold those prelimit locations range over the finite set in(1.4); since the time changes tend to the identity, a matching nonvanishing location must eventually be the same time. Conversely a positive limiting j_theta cannot disappear under uniform convergence after such time changes. This is a constraint on any possible J1 limit, not a proof of existence.

Under the stronger logarithmic hypothesis of Turn3, where locally uniform convergence is already proved, these j_theta are therefore the actual jumps of W. The present theorem supplies additional path information for that established partial result.

## 7. What remains missing

The proof controls individual jumps, their common locations and their aggregate squared envelope. It does not control the cumulative effect of arbitrarily many small positive jumps against the continuous normalizing drift. Between its jumps,

    d W_n(lambda)/d lambda = -n W_n(lambda)/lambda,

so the negative continuous drift bound grows with n. A square-summable common jump envelope alone is not a uniform bound on total variation or on the J1 oscillation modulus. Replacing that missing estimate by scalar temporal control, first-moment continuity, or finite-dimensional convergence would again exchange different notions of convergence.

No valid offspring-model counterexample has been obtained. The most precise remaining analytic task is a branching-specific bound on those cumulative small-jump oscillations, sufficient for local J1 tightness under the exact X log X endpoint. The source's simple binary, geometric and Poisson full-process descriptions also remain beyond the proved fixed-point and bivariate continued-fraction results.

This completes five substantive author turns. The original problem is still **unsolved in this attempt**, with the stronger-moment functional theorems and the exact-endpoint partials preserved for separate independent review.

## 8. Checks and credit

The finite checker verifies the mean jump-measure identity on an explicit coupled offspring family, nested-tree/generation-array laws, event-depth normalization and batch-jump formula, the exact geometric counting bound and truncated-square integral identity, and finite jump-vector convergence controls. Infinite countability, conditional independence, Tonelli and the passage to all generations are proved above rather than inferred from these tests.

This argument uses classical Galton–Watson root decomposition and scalar maximal estimates, together with elementary marked-measure bookkeeping. The source theorem and its exact model retain Mailler–Marckert's credit. No new historical-priority claim, unrestricted functional theorem or counterexample to the source is asserted.
