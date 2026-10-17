# Stage 2: private points do not compress the candidate family

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 2.

**Outcome.** No resolution of the exact construction contract. This argument tests the suggested private-witness route on a genuine high-probability class of A, rather than on rare interval samples. It proves that almost every candidate translating set already has many private points for every translate, while still leaving a positive fraction of the group uncovered. Thus irredundancy alone contributes essentially no entropy reduction. The same calculation establishes a quantitative obstruction to monotone local repair from a typical random starting set.

## 1. Model and terminology

Let p tend to infinity through primes, k=floor(sqrt(p)), and A be uniformly distributed among the k-element subsets of G=Z/pZ. Fix C>0 and let m=floor(C sqrt(p)). The target uses C=100. All assertions below are for sufficiently large p that 1<=k,m<p and the displayed binomial coefficients have nonnegative parameters.

For fixed A and T, define

U(A,T)=|G\\(A+T)|,
P_t(A,T)=(A+t)\\(A+(T\\{t})),
V_t(A,T)=|P_t(A,T)|, for t in T.

The elements of P_t are the private points of translate t. Call T **irredundant** when V_t>=1 for every t in T. An inclusion-minimal cover is an irredundant family that also covers G. Irredundancy by itself does not mean coverage, minimal covering cardinality, or local optimality for uncovered-point count.

The distinction is essential throughout this report.

## 2. A genuine typical-A event, proved in the exact-size model

Define the maximum nonzero difference multiplicity

L(A)=max_{d in G, d!=0}|A intersect (A+d)|.

For p>e, let r=ceil(4 log p/log log p), and L_p=3r. Then

Pr[L(A)>=L_p] <= p (e/r)^r = p^(-3+o(1)).           (2.1)

Here and below logarithms are natural. The asymptotic claim concerns sufficiently large p, so the small-p sign of log log p is immaterial.

**Proof.** For fixed nonzero d, the undirected graph with edges {x,x+d} is a p-cycle, since p is odd and d generates G. The number of its edges with both endpoints in A equals |A intersect (A+d)|. Every graph of maximum degree two with at least 3r edges contains a matching of r edges: greedily selecting one edge removes at most three edges each time.

There are at most binom(p,r) possible r-edge matchings, a harmless overcount by all edge subsets. For any fixed matching, its 2r distinct endpoints lie in a uniform k-set with probability

(k)_{2r}/(p)_{2r} <= (k/p)^(2r),

or probability zero if 2r>k. Consequently

Pr[|A intersect (A+d)|>=3r]
 <= binom(p,r)(k/p)^(2r)
 <= (e k^2/(pr))^r
 <= (e/r)^r,

because k^2<=p. Union over d proves (2.1). In particular,

L(A)<=L_p=O(log p/log log p)

holds with high probability, with no Bernoulli conditioning or unverified model transfer.

## 3. Exact private-point expectation and conditional concentration

Fix an arbitrary k-set A and choose T uniformly among the m-element subsets of G. Conditional on a specified t belonging to T, the remaining m-1 centres are uniform in G\\{t}. For any x in A+t, the centres that cover x are x-A, a k-set containing t. Thus precisely k-1 of the other p-1 possible centres are forbidden for x to remain private. Therefore

nu = E[V_t | t in T]
   = k binom(p-k,m-1)/binom(p-1,m-1).              (3.1)

The expectation is independent of the geometry of A and of t. It does not assert independence among different private-point events.

**Exchange bound.** Let T\\{t} change by exchanging one centre u for v, where u,v!=t. Relative to the union of the common translates, either additional translate covers at most

|(A+t) intersect (A+u)|<=L(A)

points of A+t. The two increments both lie in [0,L(A)], so the private-point count changes by at most L(A), not twice that amount.

Expose a random ordering of T\\{t}. Couple completions after two possible next values by swapping those two values throughout the remaining universe. Final unordered samples agree or differ by one exchange. The Doob martingale increments are consequently bounded by L(A). For m>=2 and L(A)>0, Azuma gives

Pr[V_t<=nu-z | t in T]
 <= exp[-z^2/(2(m-1)L(A)^2)].                     (3.2)

The degenerate zero-codegree case has no interference between distinct translates and can be handled directly. It is not needed in the asymptotic square-root regime.

Taking z=nu/2 and summing over selected t, using Pr[t in T]=m/p, gives

Pr[there exists t in T with V_t<nu/2]
 <= m exp[-nu^2/(8(m-1)L(A)^2)].                  (3.3)

This is a conditional-on-fixed-A estimate. No assumption that T is independent of a subsequently selected private-point certificate is used.

For k=floor(sqrt(p)), m=floor(C sqrt(p)),

nu=(e^(-C)+o(1))k.                                (3.4)

This follows directly from

binom(p-k,m-1)/binom(p-1,m-1)
 = product_{i=0}^{m-2}(1-(k-1)/(p-1-i)).

The linear terms sum to C+O_C(p^(-1/2)), and the squared terms sum to O_C(p^(-1/2)). Floors produce only the same vanishing error.

Uniformly over every A with L(A)<=L_p, the right-hand side of (3.3) tends to zero: its negative exponent is

(e^(-2C)/(8C)+o(1)) k/L_p^2,

and k/L_p^2 grows faster than log p. Therefore almost every m-set T has at least (e^(-C)/2-o(1))k private points per translate, uniformly over this high-probability class of A.

For an explicit fixed asymptotic margin, V_t>=e^(-C)k/3 for every t with probability tending to one.

## 4. The same candidates still leave linearly many holes

For any fixed A of size k and uniform m-set T,

mu = E U(A,T)
   = p binom(p-k,m)/binom(p,m)
   = (e^(-C)+o(1))p.                              (4.1)

Exchanging a single centre changes U by at most k. The same exposure coupling gives

Pr[|U-mu|>=epsilon p]
 <= 2 exp[-epsilon^2 p^2/(2m k^2)]                (4.2)

for every epsilon>0. This bound is uniform over all A of size k, with no typicality condition.

Combine (3.3) and (4.2). On the event L(A)<=L_p, uniformly over such A, a proportion 1-o(1) of all m-element T simultaneously satisfy

V_t>=e^(-C)k/3 for every t in T,
U(A,T)>=e^(-C)p/2.                                (4.3)

For the second inequality, take a fixed concentration margin smaller than e^(-C)/2 and use (4.1). Both constants are positive for C=100, however small; no useful finite numerical threshold is claimed.

Consequently, with high probability over A,

#{T: |T|=m, T irredundant, A+T!=G}
 = (1-o(1)) binom(p,m).                           (4.4)

More precisely, the lower bound in (4.4) holds uniformly on L(A)<=L_p, and the reverse bound is automatic. This statement counts noncovers, not minimal covers.

Its logarithm is

log binom(p,m)+o(1)
 = (C/2+o(1))sqrt(p)log p.                        (4.5)

Thus adding the condition “every translate has a private point” removes only an o(1) fraction of the entire candidate family. It does not reduce the leading candidate entropy, or even reduce its logarithm by a fixed positive constant asymptotically. A generic injective description of all such irredundant candidates must still encode essentially the full log binom(p,m) information.

This conclusion does not contradict the possibility of compressing the much smaller class of *covers*. Such compression must use the global coverage condition in an essential way; irredundancy alone cannot establish it.

## 5. Exact incidence interpretation and the private-witness counting trap

For an irredundant T, choose one private point x_t in P_t for each t. Private sets for distinct translates are disjoint, so the x_t are distinct. The bipartite incidence graph with left vertices T, right vertices {x_t}, and edge t--x when x-t belongs to A is a perfect induced matching:

x_t-t belongs to A,
x_t-u does not belong to A for all u!=t in T.      (5.1)

For a minimal cover, (5.1) is a necessary certificate. But (4.4) proves that these incidence constraints can be realized for nearly every candidate T on a genuine typical-A event, despite the continued presence of Theta(p) holes.

One must not count x_t or the differences x_t-u as if they had been chosen independently of A. They are adaptively selected from the private sets after A and T are known. In fact, on (4.3), each T admits at least

(e^(-C)k/3)^m

different indexed choices of private-point certificates. Counting all such certificates introduces substantial witness multiplicity; choosing canonical private points removes that multiplicity but does not reduce the number of T satisfying (5.1).

The result directly addresses a possible typical-A truncation strategy: conditioning on the high-probability small-codegree event does not make private-point certificates rare. No rare interval A is responsible for this obstruction.

## 6. A collective-move lower bound for monotone repair

The private-point calculation also gives a deterministic repair lemma.

**Lemma.** Fix A,T and write L=L(A)>0. Suppose every t in T has at least v private points. If another set T' satisfies

A+T subset A+T'

and deletes at least one original centre t in T\\T', then

|T'\\T| >= v/L.                                  (6.1)

**Proof.** Choose such a removed t. None of its private points is covered by a retained centre from T\\{t}. Every private point must therefore be covered by a newly added centre in T'\\T. Each new translate intersects A+t in at most L points. Covering all v private points requires at least v/L new centres.

For A and a typical random T satisfying (4.3), every monotone replacement that deletes a centre therefore introduces at least

e^(-C)k/(3L_p)
 = Omega_C(sqrt(p)log log p/log p)                 (6.2)

new centres. In particular, a size-nonincreasing strict improvement of the covered union must be a move of at least that size: it must delete a centre because adding centres without deleting any would increase |T|.

This rules out bounded-size, and more generally o(k/L_p)-size, **monotone** exchanges from a typical random starting set. It does not rule out:

- nonmonotone moves that temporarily uncover previously covered points;
- monotonicity only of the number of covered points rather than set inclusion;
- highly collective changes of Omega(k/L_p) or more centres;
- a specially designed initial T outside the typical random-candidate class;
- a construction that adds new centres while retaining all old ones and has sufficient unused budget.

The exact preserved-set condition matters. Merely improving the number of covered points does not imply (6.1).

## 7. The unresolved step

The private-point route alone cannot force A to be atypical or provide the required witness compression: almost every candidate T has many private points for typical A. A complete negative argument still needs to combine global coverage with private incidences, or impose an additional necessary condition that discards most irredundant noncovers at a quantitatively adequate rate.

On the affirmative side, the monotone-exchange bound identifies the scale of dependence that a repair proof must address if it starts from typical random translates. It supplies no construction achieving that repair, and nonmonotone/global optimization remains unaddressed.

No conclusion is drawn about whether a typical A admits some exceptional m-set T with A+T=G. The target at C=100 remains open within this work.

