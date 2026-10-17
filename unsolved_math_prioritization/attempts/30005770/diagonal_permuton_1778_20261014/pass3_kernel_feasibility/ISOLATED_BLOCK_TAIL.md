# Exponential suppression of isolated macroscopic blocks at arbitrary staircase indices

Shared PASS3. This is an unconditional partial estimate for actual uniform1324-avoiders. It does not bound the largest cell without an isolation condition.

Use the exact canonical directed kernel K from PASS2. Let a_n=|Av_n(1324)|, lambda=lim a_n^(1/n), and a_0=1. Let b_(m,K) count size-m1324-avoiders whose canonical greedy staircase has at most K nonempty cells. Set

    g_K=limsup_(m->infinity) b_(m,K)^(1/m).

The accepted fixed-prefix theorem gives g_K<lambda for every fixed K. For K=1 the class is exactly Av(213), so g_1=4. In particular lambda>4.

For pi of size n, a marked block means a nonempty consecutive block of at most K canonical cells, at ANY location. Its mass m is the total number of points in those cells. Its boundary mass k is the sum of the sizes of the immediately preceding and immediately following cells; a missing neighbor has size zero.

Write Z_(n,m,K,delta) for the total number of pairs (pi, marked block) whose marked mass is exactly m and whose boundary mass is at most delta*m. Define

    Phi(delta)=(2+delta)log(2+delta)-2log2-delta*log(delta),
    Phi(0)=0.

## Finite count retaining both exteriors

For 1<=m<=n, fixed K>=1 and delta>=0,

    Z_(n,m,K,delta)
      <= (n-m+1) a_(n-m) b_(m,K)
                 binom(2m+floor(delta*m)+1, floor(delta*m)).    (1)

To prove this, encode pi by its exact normalized cell-state path and edge shuffle choices. Cutting immediately before and after the marked block leaves a prefix path, the marked path and a suffix path. Each is a valid canonical path under the homogeneous kernel; no conditional uniform law is asserted. The marked path has exactly b_(m,K) possible states-and-internal-shuffles data of total size m, summed over its possible lengths.

Suppose the exterior masses are p and q, where p+q=n-m. There are a_p a_q possible prefix/suffix path data, including the empty path. For fixed such data let the adjacent exterior cell sizes be l and r. They satisfy l+r<=floor(delta*m) for admissible marked objects. The first and last cells in the marked block have sizes at most m. The numbers of ways to restore the two cut edges are therefore bounded by

    binom(m+l,l) binom(m+r,r),                                (2)

because every allowed edge shuffle is a binary interleaving and replacing an endpoint size by m only enlarges the binomial bound. When an exterior path is empty its missing edge contributes1, correctly matching l=0 or r=0.

For k=l+r, the negative-binomial convolution identity gives

    sum_(j=0)^k binom(m+j,j) binom(m+k-j,k-j)
       = binom(2m+k+1,k).

Thus the single product (2) is no greater than binom(2m+k+1,k), which increases with k. Bound it by the binomial coefficient in (1), discard the boundary restriction on the exterior data, and sum p=0,...,n-m. Skew-sum closure gives a_p a_q<=a_(n-m). This proves (1).

All old interleavings, even those deep in either exterior, remain in a_p and a_q. The proof never replaces a biased remainder by a uniform permutation. Marking a location introduces no extra uncontrolled factor: it is determined by the prefix path, and every marked object reconstructs from its three path pieces and two boundary shuffles.

## Uniform-in-location exponential consequence

For fixed K, epsilon>0 and delta>=0 satisfying

    Phi(delta) < log(lambda/g_K),                             (3)

one has

    limsup_(n->infinity) (1/n)log P(
       some consecutive block of <=K cells has mass>=epsilon*n
       and boundary mass<=delta*(its mass))
       <= -epsilon[log(lambda/g_K)-Phi(delta)] <0.             (4)

For epsilon>1 the event is empty, so only epsilon in (0,1] matters.

Indeed, the event probability is bounded by a_n^(-1) times the sum of (1) over m>=ceil(epsilon*n). Since a_j<=lambda^j by skew closure/Fekete, log(a_n)=n log(lambda)+o(n), and

    b_(m,K)<=exp(m[log(g_K)+o(1)]),
    log binom(2m+floor(delta*m)+1, floor(delta*m))
          =m Phi(delta)+O(log(m+1)),

the mth summand has logarithm at most

    -m[log(lambda/g_K)-Phi(delta)]+o(n).

The bounds are uniform over epsilon*n<=m<=n: the defining limsup bound for b_(m,K) holds for all sufficiently large m, and Stirling errors are logarithmic. Polynomial factors and the at-most n values of m contribute o(n). This proves (4).

The definition of limsup may equivalently be used with any certified number G_K satisfying g_K<G_K<lambda, giving the slightly weaker rate with G_K before taking G_K down to g_K.

For a single cell, (4) becomes the especially explicit condition

    Phi(delta)<log(lambda/4).                                (5)

Because lambda>4 and Phi(delta)->0 as delta decreases to zero, some positive delta always works. Thus an escaping-index macroscopic cell cannot, with nonvanishing probability, have both neighbors collectively much smaller than itself. This is a statement about every index simultaneously, not only the first fixed number of cells.

## What this does not settle

A macroscopic cell can belong to a macroscopic cluster whose boundary mass is large relative to the chosen threshold. Applying (4) with K growing with n would require a uniform gap unavailable here. Even fixed K gaps may tend to zero rapidly as K increases. The argument therefore does not exclude a long cell-mass profile with gradually decaying sides, and does not imply max_j m_j=o(n).

It also does not establish that avoiding isolated macroscopic blocks is sufficient for the anti-diagonal limit. The established deterministic implication is still max_j m_j=o(n) in probability => the desired weak limit.

All ingredients are the exact PASS2 encoding, the accepted fixed-K growth gap, the credited Catalan enumeration of213-avoiders and elementary binomial counting. No new outside result or numerical growth estimate is used.
