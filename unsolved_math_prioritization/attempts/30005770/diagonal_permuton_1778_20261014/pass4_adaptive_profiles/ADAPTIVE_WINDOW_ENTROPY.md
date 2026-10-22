# Exact boundary entropy gives a conditional adaptive-window theorem

Shared PASS4, row 1778 / 30005770, 14 October 2026. This is a conditional sufficient theorem. No divergence assertion about the actual finite-window gaps is proved.

## Definitions and fixed inputs

Let a_n count 1324-avoiders, let lambda=lim a_n^(1/n), and let b_(n,K) count those whose canonical greedy staircase has at most K nonempty cells. Put

    g_K=limsup_(n->infinity) b_(n,K)^(1/n),
    delta_K=log(lambda/g_K).

The accepted fixed-prefix theorem proves delta_K>0 separately for each fixed K. Since b_(n,K) is nondecreasing in K, delta_K is nonincreasing. No rate in K follows from these statements alone.

For x,y>=0 define the homogeneous binary-shuffle entropy

    e(x,y)=(x+y)log(x+y)-x log x-y log y,
    e(0,0)=0,

with 0 log 0=0. Thus e(x,y)=(x+y)h(x/(x+y)), where h is binary entropy with natural logarithms. We use

    0<=e(x,y)<=(x+y)log 2.                                  (1)

A normalized finite positive cell-mass profile is (p_1,...,p_t), with sum p_i=1. Extend it by zero outside [1,t]. For a consecutive nonempty block W, let M(W) be its mass. If its actual endpoint masses are a,b and the immediately exterior neighboring masses are l,r (zero when absent), its exact two-boundary entropy is

    E(W)=e(a,l)+e(b,r).                                      (2)

A singleton has a=b, as it should: its two distinct cut edges each have that endpoint.

## Theorem 1: summable total boundary entropy

Fix an index i with p_i>=epsilon>0. For j=0,1,... let W_j=[i-j,i+j] intersected with [1,t]. Its width is at most 2j+1. Let M_j=M(W_j), and E_j=E(W_j). Then

    M_j>=epsilon,
    sum_(j>=0) E_j<=2 log 2.                                (3)

Consequently, for arbitrary nonnegative numbers d_K and any N>=0 such that

    epsilon sum_(j=0)^N d_(2j+1)>2 log 2,                   (4)

at least one j in {0,...,N} satisfies

    M_j d_(2j+1)-E_j>=c,
    c=[epsilon sum_(j=0)^N d_(2j+1)-2 log 2]/(N+1)>0.       (5)

Both N and c depend only on epsilon and the chosen finite list of d_K, not on the number of cells or the location of the heavy cell.

Proof. Zero padding gives the identity

    E_j=e(p_(i-j-1),p_(i-j))+e(p_(i+j),p_(i+j+1)).

When a centered interval extends beyond an end of the profile, that side contributes zero in both this formula and the actual nonempty block. As j runs through the nonnegative integers, the two rays of edges cover every adjacent edge exactly once. Each p_k occurs in at most two edge endpoints. Equation (1) therefore yields (3). Summing M_j d_(2j+1)-E_j from j=0 to N and using M_j>=epsilon gives at least the numerator in (5). One of the N+1 summands is at least its average. QED.

Repeated clipped windows cause no problem: after both ends have been reached, their entropy is zero. The bound concerns the radius-indexed candidates, and their number is fixed before n grows.

## Theorem 2: exact uniform-law consequence

Suppose d_K are certified numbers satisfying

    0<=d_K<=delta_K,
    sum_(j>=0) d_(2j+1)=infinity.                           (6)

Then for every fixed epsilon>0 there is c_epsilon>0 such that

    P(maximum canonical cell size of uniform Pi_n>=epsilon*n)
       <=exp(-c_epsilon*n+o(n)).                            (7)

In particular, the accepted deterministic bound d_BL(mu_pi,mu_anti)<=3 maxcell/n gives weak convergence in probability to the anti-diagonal permuton.

Proof. Fix epsilon and choose N satisfying (4), with c as in (5). All K=2j+1 used below are fixed members of {1,3,...,2N+1}. Theorem 1 selects a block of width at most K and mass m>=epsilon*n for which, in integer size units,

    m d_K-[e(a,l)+e(b,r)]>=cn.                              (8)

Here a,b,l,r are now the integer endpoint and neighbor sizes. Homogeneity converts (8) exactly to the normalized inequality (5).

Cut immediately before and after such a marked block in the accepted exact canonical kernel path. This leaves an exterior prefix of mass p, a marked path of mass m with at most K cells, and an exterior suffix of mass q, where p+q=n-m. The path data have at most a_p b_(m,K) a_q choices. Both exterior completion factors are retained. Given this data, restoring the two lost edge shuffles has at most

    binom(a+l,l) binom(b+r,r)
       <=exp(e(a,l)+e(b,r))
       <=exp(m d_K-cn)                                    (9)

choices for those data eligible under (8). One can partition by the endpoint and neighbor integer masses before summing; there are only polynomially many such choices. Equivalently, eligibility is determined by the three path pieces and (9) bounds every eligible summand directly.

Skew-sum closure gives a_p a_q<=a_(n-m). Summing p=0,...,n-m, and, if desired, the polynomially many endpoint classes, bounds the marked count for each m,K by

    polynomial(n) a_(n-m) b_(m,K) exp(m d_K-cn).             (10)

For every fixed K and every eta>0, the definition of g_K and (6) give, for all sufficiently large m,

    b_(m,K)<=exp(m[log(lambda)-d_K+eta]).                    (11)

The same threshold works for the finite list of K under consideration. Since m>=epsilon*n, all counted m eventually meet it. Together with a_(n-m)<=lambda^(n-m), log a_n=n log lambda+o(n), and (10), this gives after division by a_n

    exp(-cn+eta*m+o(n))<=exp(-(c-eta)n+o(n)).                 (12)

Choose eta=c/2. The finite choices of K, the at most n choices of m, and all marking/composition factors are polynomial and absorbed into o(n). This proves (7) with c_epsilon=c/2. The selected block need not be chosen measurably or uniquely: counting the union of all eligible marked blocks suffices. QED.

## Corollary and the unresolved rate

If

    sum_(K>=1) log(lambda/g_K)=infinity,                    (13)

then (7) holds. Indeed, delta_K is nonincreasing, so its odd-indexed subseries diverges whenever the full series does; apply Theorem 2 with d_K=delta_K.

This is a weaker required rate than a uniform positive gap. It is still unproved. The explicit local-reroot certificates obtained in the other PASS4 lane are summable. Their summability does not imply that (13) fails, because they are lower bounds on delta_K, not upper bounds. Conversely, positivity delta_K>0 alone does not imply (13).

The companion EXACT_CANONICAL_WINDOW_OBSTRUCTION.md proves that every adaptive bounded-window selector fails if one substitutes the sharp certificate based only on the accepted one-edge reroot losses for the unknown true delta_K. It does not disprove Theorem 2 or the permuton conjecture.

## Input scope

The exact kernel and cut reconstruction are the accepted PASS2 EXACT_GREEDY_TRANSFER.md. The accepted PASS3 ISOLATED_BLOCK_TAIL.md proves the same three-path counting mechanism with a coarser boundary envelope; here the endpoint-specific binomial factors are retained. The fixed-K gap is from PASS2 FIXED_STAIRCASE_PREFIX_THEOREM.md. No new external literature input, finite-data extrapolation, changing-K coefficient asymptotic, or conditional-uniformity replacement is used.
