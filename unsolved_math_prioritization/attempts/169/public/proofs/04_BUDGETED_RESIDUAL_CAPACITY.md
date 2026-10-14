# Stage 4: sharp first-order capacity of budgeted pencil residuals

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 4. Throughout, p tends to infinity through primes, k=floor(sqrt(p)), c=floor(100sqrt(p)), and A is a uniform k-subset of G=Z/pZ. All translating sets may depend on A.

## 1. Results and the remaining gap

Fix an integer R independent of p. For X subset G write

H_X=G\(X+A-A),  r=|X|.

With probability tending to one, simultaneously for all X with r<=R:

1. |H_X|=(e^(-r)+o(1))p.
2. For every s in X-A, |(A+s) intersect H_X|=0 exactly.
3. For every s outside X-A,

   |(A+s) intersect H_X|=(e^(-r)+o(1))k.                 (1.1)

All error terms are uniform over the indicated choices. R is fixed; no growing-R assertion is made.

This upgrades the earlier lower bound of order e^(-R)k on the number of remaining centres. Every full or o(p)-hole cover must now have at least (1-o(1))k centres outside every bounded union X-A. In particular, a candidate spending at least (99+eta)k centres inside such an envelope, for any fixed eta>0, leaves a positive fraction of p uncovered at the exact cap, for all sufficiently large p. The statement retains the original budget and applies to actual subsets of the envelope.

The associated fractional problem can be solved to first order. If B subset X-A has |B|<=c and H_B=G\(A+B), the minimum fractional cost of covering H_B using centres outside B is (1+o(1))k. This remains true after adding box constraints and any global lightness constraint with threshold at least 2. Its upper bound is an exact universal construction: give every centre outside B weight 1/k. Thus a linear charge or fractional-cover argument cannot generally demand more than one further k-scale block from the residual.

No estimate is obtained for the minimum residual over all unrestricted centre sets of size c. In particular, no lower bound at the requested p^(3/4) mean scale is claimed. The unresolved candidates can keep substantially more than k centres in a diffuse remainder; the integrality and collective dependence of that remainder are not controlled here.

## 2. A uniform sparse-graph input

**Lemma 2.1.** Let Gamma_p be any simple graph with n=p+O(1) vertices, maximum degree bounded by a fixed constant D, and m=r p+O(1) edges, where r is fixed. Let W be the number of edges induced by a uniform ell-subset of its vertices, with ell=k+O(1). Then

Pr[W=0]=e^(-r)+o(1),                              (2.1)

uniformly over all these graphs when the constants in the hypotheses are fixed.

**Proof.** For a fixed j, expand E(W)_j over ordered lists of j distinct edges. The number of lists with disjoint endpoints is m^j+O_j(p^(j-1)), since degree is bounded. Their joint selection probability is (ell)_(2j)/(n)_(2j), so their contribution tends to r^j.

For a list with overlapping edges, let v be the number of distinct vertices and let a be the number of connected components of the union graph. There are O_j(p^a) such lists: choose a root per component and use the bounded degree to explore its at most j edges. Its selection probability is O_j(p^(-v/2)). Every component has at least two vertices; if any edges overlap, at least one component has at least three vertices. Hence a-v/2<=-1/2. The total contribution of overlapping lists is O_j(p^(-1/2)). The same estimates are uniform over the permitted graphs. Thus

E(W)_j=r^j+o(1)

for every fixed j, uniformly. The finite Bonferroni inequalities sandwich Pr[W=0] between consecutive even and odd partial sums of sum_j(-1)^j E(W)_j/j!. First take p to infinity with the truncation fixed, then take the truncation to infinity. The limiting series is e^(-r). This proves (2.1) and its uniformity. No independent-edge approximation is used.

## 3. Two codegree bounds and a genuine endpoint Lipschitz estimate

Use the difference and sum counts

r_A(d)=#{(a,b) in A^2:a-b=d},
s_A(u)=#{(a,b) in A^2:a+b=u}.

Let m_p=ceil(10log p/log log p) and L_p=3m_p+1. With probability 1-p^(-9+o(1)),

max_{d!=0}r_A(d)<=L_p,  max_u s_A(u)<=L_p.          (3.1)

For the difference bound, the pairs {x,x+d} form a cycle. If at least 3m_p of its edges are occupied, greedy selection gives a matching of m_p occupied edges. For a fixed u, the non-diagonal pairs {x,u-x} form a matching, and s_A(u) is twice the number of occupied pairs plus at most one diagonal point. A violation of either bound implies that some m_p disjoint pairs have all their endpoints in A. A union bound gives, in either case,

Pr[violation at a specified parameter]
 <=binom(p,m_p)(k/p)^(2m_p)<=(e/m_p)^m_p.

Union over the at most 2p parameters proves (3.1). Call this shared event Good.

For a fixed Z subset G define

F_Z(A)=#{a in A: a-z notin A-A for every z in Z}.     (3.2)

If A intersects Z, then F_Z(A)=0: for z in A, every a in A has a-z in A-A. We therefore consider the slice of all k-sets avoiding Z.

**Lemma 3.2.** For any two Good sets A,A' on that slice, with |Z|=r,

|F_Z(A)-F_Z(A')|<=(1+4rL_p)|A\A'|.                (3.3)

**Proof.** Put t=|A\A'|=|A'\A|. The contribution from points not common to the two sets changes the count by at most t. For a common candidate a, the condition fails precisely when, for some z in Z, there is a pair (b,d) in the set with

a+d=b+z.                                          (3.4)

If its indicator changes, a witness to failure in one endpoint set uses at least one point y belonging to that endpoint but not the other. If b=y, possible pairs (a,d) have sum y+z, so at most L_p common candidates are affected. If d=y, possible pairs (a,b) have difference z-y. This difference is nonzero, because both endpoint sets avoid Z, so again at most L_p candidates are affected. Sum over r choices of z, over t removed points and t added points. This gives at most 4rtL_p affected common candidates, proving (3.3).

The argument compares arbitrary Good endpoint sets directly. It does not assume that a swap path between them stays Good, which would be insufficient for the extension used below.

## 4. Uniform expectation and concentration of the residual capacity

### 4.1 The conditional mean

Fix Z with r<=R. Conditional on A avoiding Z, each a outside Z has inclusion probability k/(p-r). Apart from at most binom(r,2) exceptional values satisfying 2a=z_i+z_j, the differences

a-z, z in Z,

are nonzero and pairwise distinct up to sign. For such a, the undirected graph joining vertices whose difference is plus or minus one of these values is a simple 2r-regular graph with rp edges.

Condition additionally on a belonging to A. The condition in (3.2) says there is no occupied edge in this graph. Its neighbours of a are the r already forbidden points Z and the r further points 2a-Z. The exceptional values have been excluded, so these further points are distinct and avoid Z and a. Excluding 2a-Z from the remaining sample costs probability 1-O_R(k/p)=1-o(1). Given this exclusion, the remaining k-1 selected vertices are uniform on p-2r-1 vertices. The induced graph on those vertices has maximum degree at most 2r and rp-O_R(1) edges. Lemma 2.1 yields probability e^(-r)+o(1) of no occupied edge, uniformly over Z and the nonexceptional a.

The O_R(1) exceptional candidates contribute at most O_R(k/p) to the expectation. It follows that, uniformly over |Z|=r<=R,

E[F_Z(A) | A intersect Z is empty]
  =(e^(-r)+o(1))k.                                (4.1)

The case r=0 is exact: F_empty(A)=k. Since r ranges over only finitely many values, the o(1) term can be chosen uniformly over all 0<=r<=R.

### 4.2 Concentration without assuming a Good swap path

Work on the slice of k-sets avoiding a fixed Z. Its swap distance is d(A,A')=|A\A'|. By (3.3), F_Z restricted to Good sets is D_p-Lipschitz, where D_p=1+4RL_p. Define an extension to the whole slice by

Ftilde_Z(A)=min_{B Good, B avoids Z}[F_Z(B)+D_p d(A,B)],

and clip its values to [0,k]. The Good subset is nonempty for sufficiently large p. This construction is D_p-Lipschitz, agrees with F_Z on Good sets, and is bounded between 0 and k. These assertions follow directly from the triangle inequality and (3.3).

The probability of avoiding Z is 1-O_R(k/p), hence is at least 1/2 for large p. Therefore

Pr[not Good | A avoids Z] <=2p^(-9+o(1)),

and the conditional expectations of Ftilde_Z and F_Z differ by at most 2k p^(-9+o(1)).

Expose a uniform sample without replacement on this slice. Transposition coupling of two possible next exposed elements changes the final selected set by at most one swap; consequently the Doob martingale increments of any D_p-Lipschitz function are bounded by D_p. Azuma gives

Pr[|Ftilde_Z-E Ftilde_Z|>=t | A avoids Z]
 <=2exp[-t^2/(2kD_p^2)].                           (4.2)

Take t=k^(3/4). The negative exponent has order sqrt(k)/L_p^2, which dominates R log p. There are at most (R+1)p^R sets Z of size at most R. Union-bound the extension tails, and add the single shared event not Good once. Together with (4.1), this proves that, with high probability, simultaneously for every such Z avoiding A,

F_Z(A)=(e^(-|Z|)+o(1))k.                           (4.3)

The polynomial failure probability of Good is not multiplied by the number of Z. This distinction is important when R is a large fixed constant.

### 4.3 Translation to capacities

For X and s put Z=X-s. By changing variables y=a+s,

|(A+s) intersect H_X|
 =#{a in A: a-z notin A-A for every z in Z}
 =F_Z(A).                                         (4.4)

If s belongs to X-A, then Z intersects A and the capacity is zero. Otherwise (4.3) applies. This proves the claimed uniform capacity estimate (1.1). In particular, since e^(-R)k tends to infinity, with high probability the exact containment A+s subset X+A-A holds if and only if s belongs to X-A, simultaneously for all these X and s. This inverse-containment corollary is restricted to bounded pencil unions; it is not a compression theorem for unrestricted covers.

## 5. Uniform size of the canonical residuals

For fixed X and target y, the event y in H_X means that A contains no pair with difference in y-X. Except for O_R(1) values y in X or satisfying 2y=x_i+x_j, the corresponding difference graph is simple 2r-regular with rp edges. Lemma 2.1 gives

E|H_X|=(e^(-r)+o(1))p,

uniformly over |X|=r<=R. The exceptional targets change this expectation by only O_R(1).

Exchanging one element of A changes A-A in at most 4k positions, and X+A-A in at most 4rk positions. The same without-replacement coupling gives

Pr[||H_X|-E|H_X||>=t]
 <=2exp[-t^2/(32r^2k^3)]                           (5.1)

for r>=1. At t=p k^(-1/4), the negative exponent has order sqrt(k), again dominating the logarithm of the polynomial menu of X. The case r=0 is exact. This proves simultaneously

|H_X|=(e^(-r)+o(1))p.                              (5.2)

All assertions in Section 1 follow on the intersection of the events constructed in Sections 4 and 5.

## 6. Consequences that preserve the centre budget

For any T, set s=|T\(X-A)|. Centres inside X-A cover no point of H_X. By the elementary union upper bound and (1.1), the number of holes of A+T is at least

|H_X|-sum_{t in T\(X-A)} |(A+t) intersect H_X|
 >=(e^(-r)-epsilon_p)p-s(e^(-r)+epsilon_p)k,         (6.1)

where epsilon_p tends to zero and is uniform for fixed R. Pairwise intersections are not substituted for union loss in this argument; the displayed union bound is in its valid direction.

If s<=(1-eta)p/k for fixed eta in (0,1), (6.1) is at least

(eta e^(-R)/2)p                                   (6.2)

for all sufficiently large p. Thus every full cover, and more generally every T with o(p) holes, satisfies

|T\(X-A)|>=(1-o(1))p/k=(1-o(1))k                  (6.3)

simultaneously for all |X|<=R.

At |T|<=c, if |T intersect(X-A)|>=c-(1-eta)k, then s<=(1-eta)k and (6.2) applies. Since c=100k+O(1), this excludes candidates with at least (99+eta')k centres in a bounded union of pencils, for any fixed eta'>0 after taking a slightly smaller eta. It is a statement about actual centre counts, not the size of an enlarged envelope.

If a heavy-point decomposition removes actual blocks B_i subset x_i-A and leaves S, its union B is contained in X-A. Even when those blocks are not maximal intersections, every centre of S still lying in X-A contributes nothing to H_X. Therefore the necessary cost in (6.3) applies to the remainder outside the envelope. It is stronger than the former lower bound e^(-R)k, but it does not force a contradiction when that remainder has several k-scale blocks available.

## 7. A sharp fractional obstruction with the actual heavy subset retained

Fix any A and any B subset G, and put b=|B| and H_B=G\(A+B). Consider fractional remainder variables w_t, t outside B, with

0<=w_t<=1,
sum_{t outside B} w_t 1_A(y-t)>=1 for y in H_B.

Additional global lightness constraints may be imposed by requiring the same convolution to be at most h-1 everywhere, for any integer h>=2.

The following exact weights are feasible for every A,B:

w_t=1/k for t outside B; w_t=0 for t in B.           (7.1)

Indeed their convolution is

sum_t w_t 1_A(y-t)=1-(1/k)(1_A*1_B)(y),             (7.2)

which is between zero and one globally and is exactly one on H_B. Their total fractional cost is (p-b)/k.

Now suppose B subset X-A, |X|<=R and b<=c, on the high-probability event already proved. Because H_X subset H_B, any fractional solution has

|H_X|<=sum_t w_t |(A+t) intersect H_X|
       <=(e^(-r)+epsilon_p)k sum_t w_t.

Consequently its cost is at least (1-o(1))p/k. Combining with (7.1), the fractional optimum, with or without the stated box and lightness constraints, is

(1+o(1))p/k=(1+o(1))k,                             (7.3)

uniformly over all such actual subsets B. The upper bound is compatible with the lower because b=O(k), so (p-b)/k=p/k-O(1).

With the retained heavy cost included, the explicit fractional completion stays within the original cap whenever

b+(p-b)/k<=c,
that is, b<=(kc-p)/(k-1)=99k+O(1).                 (7.4)

Thus throughout essentially the entire range b<=99k, the budgeted residual linear program already has a feasible light solution for every A. A dual linear charging argument for this relaxation cannot prove the missing nonexistence result there. This is an exact integrality limitation, not a claim that the fractional weights can be rounded to a set, or that a cover exists.

## 8. Exact remaining statements

The results leave the following substantial possibilities open.

- A cover-specific integrality estimate could show that covering H_B needs far more than its fractional cost k when B is a bounded-pencil subset of moderate size.
- A one-sided zero-mass estimate for a bounded convolution observable could use the dependence of the light remainder on A without requiring a universal Poisson law.
- A global construction could exploit that same dependence to round an appropriate fractional or structured completion, but (7.1) supplies no rounding method or error bound.

One sufficient but unproved cover-specific inverse statement would say that every candidate with o(p) holes and at most c centres has at least (99+eta)k centres in X-A for some fixed R and eta>0. Section 6 would contradict that statement on the typical event. No such compression theorem is established or assumed; it is merely an explicit possible missing reduction.

To obtain the requested unrestricted negative estimate, one would still need to control candidates with more than (1+o(1))k centres outside every bounded pencil union. No lower bound for their optimal residual or its expectation is proved here. The current result does not establish E R_c >= a c sqrt(k), nor does it establish a cap-sized cover with high probability.

## 9. Independent audit
