# Stage 5: the exact integral-completion frontier

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 5. The original model is unchanged: p is prime, k=floor(sqrt(p)), c=floor(100 sqrt(p)), and A is a uniform k-subset of G=Z/pZ. Every choice below may depend on all of A.

## 1. Decision and direct target

**No unconditional completion theorem or lower bound for the unrestricted optimal residual is proved.** In particular, this argument does not establish either a c-centre cover with probability tending to one or E R_c >= a c sqrt(k) for a fixed a>0 along unbounded primes.

The direct attempt retained every actual heavy subset and the original centre budget. It did not replace a heavy subset by its full pencil. The precise unresolved integer problem is stated in Section 2. The proposed closure by coordinate restriction of that integer problem fails in a stronger and quite concrete way than the ordinary fractional-cover bound: the real uniform law on exactly the remaining number of centres satisfies every cylinder-lifted covering inequality through a number of conditioned coordinates proportional to k. It can also satisfy the lifted global lightness constraints. This is an obstruction to that particular attempted proof mechanism, not a feasible integer completion, not a new forbidden algorithm class, and not a claim about arbitrary nonlinear certificates or sum-of-squares relaxations.

The remaining task is genuinely global: distinguish the exceptionally successful centre sets, if there are any, from an exponentially large family whose bounded coordinate conditionings all pass these necessary linear tests.

## 2. Exact integral completion with the actual heavy subset

Fix 0<delta<=1 and put h=ceil(delta k). Starting with an arbitrary candidate T of size at most c, repeatedly choose x_i with

|T^(i-1) intersect (x_i-A)| >= h,

and remove the actual block

B_i=T^(i-1) intersect (x_i-A).

The B_i are disjoint. If B is their union, X={x_i}, and S=T\B, then

|X| <= floor(c/h),
B subset X-A,
|B|+|S| <= c,
max_y |S intersect (y-A)| <= h-1.

For the fixed delta, floor(c/h) is bounded as p grows. Define

H_B=G\(A+B),   V=G\B,   n=p-|B|,   m=c-|B|.

If the original T covers G, then S subset V covers H_B. Conversely, any B and any S subset V that covers H_B gives a cover B union S; if |S|<=m, its size is at most the exact c. Thus, allowing all B subset X-A with the stated bounded X, the existence of a light completion is an exact reformulation of the original event. The forward direction is the peeling; the reverse direction is simply the definition of H_B. This is a reformulation, not a solution.

For every y in H_B, the residual neighbourhood

N_y=(y-A) intersect V

has **exactly k** elements, because (y-A) intersect B is empty. For arbitrary y in G the same intersection has at most k elements. The integral feasibility problem is therefore

z_t in {0,1} for t in V;
sum_(t in V) z_t <= m;
sum_(t in N_y) z_t >= 1 for y in H_B;
sum_(t in (y-A) intersect V) z_t <= h-1 for every y in G.

The actual B, its cost, its omitted centres, and all of its residual targets remain in this system.

The audited Stage 4 theorem shows that, with high probability, for every bounded X and every cover T,

|T\(X-A)| >= (1-o(1))k.

It already excludes candidates spending more than (99+eta)k centres inside a bounded pencil envelope. It leaves unrestricted candidates with a diffuse budget between approximately k and 100k. The following calculation directly tests whether local coordinate restriction can force additional integral cost in that remaining range.

## 3. Exact-cardinality conditioning lemma

The lemma is deterministic and does not use primality, randomness of A, or a pencil envelope.

Let V be a set of n elements, let N subset V have size k, and let S be uniform among the m-subsets of V. Assume

1 <= k <= m < n,
0 <= r <= min(k,m,n-m),
r < n.

A coordinate cylinder specifies disjoint sets P,Q subset V and the event

E_(P,Q)={P subset S, Q intersect S is empty}.

Write a=|P|, b=|Q|, u=|P intersect N|, v=|Q intersect N|. If a+b<=r, the event has positive probability and exact conditioning gives

E[|S intersect N| | E_(P,Q)]
 = u + (m-a)(k-u-v)/(n-a-b).                       (3.1)

This follows because the other m-a selected elements are a uniform subset of V\(P union Q).

**Minimum.** Simultaneously over all cylinders with a+b<=r,

E[|S intersect N| | E_(P,Q)]
 >= m(k-r)/(n-r).                                 (3.2)

The bound is sharp: take P empty and take Q to be any r-subset of N.

Proof. Put s=a+b. Since 0<=(m-a)/(n-s)<=1, the right side of (3.1) is at least

(m-a)(k-b)/(n-s).

For fixed s, the numerator (m-a)(k-s+a) is concave in a on [0,s]. Its endpoint values are m(k-s) and k(m-s); the former is smaller because m>=k. The conditional mean is consequently at least m(k-s)/(n-s). This last expression is nonincreasing in s because n>=k, proving (3.2). The claimed choice of P,Q attains equality in (3.1).

**Maximum for neighbourhoods of size at most k.** If also n>=m+k, then every N' subset V with |N'|<=k satisfies

E[|S intersect N'| | E_(P,Q)]
 <= r+(m-r)(k-r)/(n-r).                           (3.3)

Proof. Formula (3.1), with |N'| in place of k, is at most

a+(m-a)(k-a)/(n-s)
 <= a+(m-a)(k-a)/(n-r).

Here a<=r<=k. The final expression is a convex quadratic in a. Its endpoint at a=r exceeds its endpoint at a=0 by

r(n-m-k)/(n-r) >= 0.

Thus its maximum on [0,r] is the stated value. When |N'|=k the maximum is attained by conditioning on r selected elements of N'.

## 4. What this says about the actual budgeted integer system

Set z_t=1_(t in S) under the real uniform m-subset law on V. For disjoint P,Q put

M_(P,Q)(z)= product_(t in P) z_t product_(t in Q)(1-z_t).

Consider the linear inequalities obtained by multiplying each original cover, budget, box, or lightness inequality by every such nonnegative cylinder monomial of degree at most r, taking expectations, and using the Boolean identities z_t^2=z_t. The multipliers have degree at most r, so the resulting linear-constraint products use moments through degree r+1. This is the degree convention throughout; no unnamed hierarchy-level convention is invoked. This description specifies the entire relaxation used here; no more general class of multipliers is being asserted.

The moment values of the uniform m-subset law are real, nonnegative, and mutually consistent. Moreover:

- Boolean identities and box inequalities hold pointwise.
- The exact budget sum_t z_t=m holds pointwise, even after multiplication by any cylinder.
- Every multiplied covering inequality holds if

  m(k-r)/(n-r) >= 1,

  equivalently

  (m-1)r <= mk-n.                                (4.1)

  Indeed, every residual N_y has size exactly k, and (3.2) applies to each cylinder separately.

- If n>=m+k, every multiplied lightness inequality holds whenever

  r+(m-r)(k-r)/(n-r) <= h-1.                      (4.2)

  This follows from (3.3), since the global neighbourhoods have at most k elements.

These same moment values satisfy all the inequalities simultaneously. Multiplying by a cylinder and taking expectations is equivalent to its positive probability times the conditional expectation, so no conditioning normalization is missing.

Consequently, any certificate formed by a nonnegative linear combination of precisely these lifted inequalities, together with Boolean and exact-budget identities, cannot refute the system in the range (4.1)-(4.2). Its expectation under these moment values could not be a strictly negative constant. This is the concrete proposed coordinate-restriction closure that fails.

The same conclusion includes an arbitrary nonnegative multiplier depending on at most r coordinate values: it is a nonnegative linear combination of their full-assignment cylinders. With A and B held fixed, it also includes adaptive inspection of at most r coordinates, with the tested target chosen from the resulting observations. Each decision-tree leaf is a cylinder of degree at most r, so its chosen target still has conditional expected coverage at least one. This is only a bounded-coordinate observation statement; it does not cover a procedure that uses the entire centre set or conditions on global coverage.

This conclusion does **not** say the uniform m-subset is a cover. The distribution is not supported on feasible integer completions. It satisfies the inequalities only in the specified low-degree weighted average. It also does not address arbitrary nonnegative polynomial multipliers, positive-semidefinite constraints, nonlinear use of the cover event, or a cover-specific restriction chosen using the fact that the candidate is a cover.

### Exact cap, no retained heavy centres

With B empty, n=p and m=c. Ignoring a separate lightness constraint, (4.1) allows

r <= floor((ck-p)/(c-1)) = (0.99+o(1))k.           (4.3)

Thus even conditioning on almost 99 percent of a single k-element target neighbourhood can leave every lifted linear cover constraint feasible at the original budget. For r=k, conditioning on exclusion of all k neighbours instead gives conditional coverage zero, so this real moment law fails the corresponding lifted constraint. The distinction is quantitative and exact.

### Retained B and global lightness

Suppose |B|/k tends to beta<99, so m/k tends to D=100-beta>1 and n/k^2 tends to one. Let h=ceil(delta k). For every fixed

0 < alpha < min(1-1/D, delta),

take r=floor(alpha k). Then (4.1) holds for all sufficiently large p, since its left conditional-coverage side tends to D(1-alpha)>1. Also

r+(m-r)(k-r)/(n-r)
 = r+(D-alpha)(1-alpha)+o(1),

so (4.2) holds eventually because alpha<delta. All other hypotheses of the lemma also hold eventually.

Therefore, even with the actual B, exact remaining cardinality, and the global peeling lightness constraints, the cylinder-lifted relaxation remains feasible through a positive multiple of k coordinate conditionings throughout every fixed-margin range beta<=99-eta. This statement is uniform in the geometry and adaptivity of B. It does not replace H_B by H_X.

Using an exact m-subset in this calculation does not assert that an arbitrary light feasible completion can be padded to m while preserving lightness. Exact cardinality is only the stronger budget constraint imposed on the displayed moment solution. A solution of that stronger relaxation is also a solution of the at-most-m relaxation.

## 5. Direct expectation and completion attempts: where the estimate fails

For a fixed A and actual B, let U_B(S)=|H_B\(A+S)|. The same exact m-subset law gives

E_S U_B(S)
 = |H_B| binom(n-k,m)/binom(n,m),                 (5.1)

with the usual zero convention. Each residual target has the same k available neighbours. No independence among different targets is asserted.

For bounded-pencil B, the audited Stage 4 estimate gives |H_B|>=|H_X|=(e^(-|X|)+o(1))p. If m/k tends to a fixed D>0, the binomial ratio in (5.1) tends to e^(-D). Thus the displayed real moment solution typically retains a positive-order-p residual in expectation, even though all the lifted linear tests can pass. That positive expectation is **not** a lower bound on the optimum over S.

A centre swap changes U_B by at most k. The exact-size exposure coupling gives

Pr_S[U_B <= E_S U_B-t] <= exp[-t^2/(2mk^2)].      (5.2)

At a fixed positive-density deviation this suppresses a prescribed random completion by exp(-Omega(k)). It cannot be union-bounded over all binom(n,m)=exp(Theta(k log k)) possible completions. The law of the optimizer is not the uniform law used in (5.1)-(5.2). Optimizing before taking expectations is exactly the missing step.

Other direct closures examined in this pass have the same unresolved point:

- A restriction of an already existing cover can use its cover-conditioned incidence information, but averaging a restriction of a generic centre set supplies only (3.1) and the preceding residual mean. Conditioning on bounded coordinate choices does not create the missing cover-conditioned law.
- Adding a uniformly shifted block to any actual residual multiplies its expected size by the block's uncovered fraction. This is the previously proved exact amplification mechanism. With only fixed positive-density residual bounds at constant k-scale budgets, finitely many blocks still leave a positive-density upper bound, rather than the o(k) holes that can be repaired within a fixed additional k-scale budget.
- The canonical residual H_X has uniform capacity (e^(-|X|)+o(1))k per outside centre. Charging targets to their covering centres forces only approximately k outside centres. Counting overlaps, or treating the remaining light convolution as universally Poisson or compound Poisson, would require an additional theorem about the optimizer; none is established here.

None of these statements excludes all successful completions or provides one. They identify the precise invalid exchange or missing joint estimate rather than adopting it as an assumption.

## 6. Strongest original gap remaining after this argument

Write

R_j(A)=min_(|T|<=j) |G\(A+T)|,   mu_j=E_A R_j(A).

At the original cap, the only unrestricted lower bound obtained remains zero. Deterministically, averaging uniformly chosen c-centre sets gives

0 <= R_c(A) <= floor[p binom(p-k,c)/binom(p,c)]
              = (e^(-100)+o(1))p.

The sufficient negative bridge is unchanged:

mu_c >= a c sqrt(k)

for a fixed a>0 along unbounded primes would force a covering failure probability bounded away from zero there by the audited optimum-residual concentration theorem. No such lower estimate is proved.

The sufficient positive bridges are also unchanged: mu_(49k)=o(p^(3/4)) or mu_(33k)=o(p^(5/6)) would yield exact-cap complete covers through the audited amplification and repair construction. No such smaller-budget estimate is proved, and a bound at c cannot be transferred to a smaller budget without justification.

The missing original estimate can equivalently be sought as a genuine infeasibility or construction theorem for the actual residual integer system in Section 2. The present calculation shows that a broad range of local coordinate-conditioned linear tests is too weak to supply that theorem. It supplies no new favorable or unfavorable asymptotic probability for the unrestricted original event.

## 7. Independent checks and a finite integral separation

The public cylinder checker reproduces the following finite separation in the actual additive model:

p=19, k=4, A={0,1,2,4}, B empty, m=6, r=1.

Here (m-1)r=5=mk-n, so the cover inequalities pass every cylinder multiplier of degree at most one, with minimum conditional occupancy exactly one. The lightness upper bound is 1+5*3/18=11/6, so the same moment law also passes these lifted global constraints with an upper limit of two. However, exhaustive enumeration of all binom(19,6)=27,132 six-centre sets gives R_6(A)=1. One optimum is {0,1,5,6,11,14}.

This is a verified finite separation between the stated relaxation and integer covering, not a counterexample to the original coefficient-100 claim: the auxiliary budget here is six, and the original cap is vacuous at this small prime. It confirms why neither consistency of the moments nor the locally feasible exact budget can be promoted to an actual completion.

