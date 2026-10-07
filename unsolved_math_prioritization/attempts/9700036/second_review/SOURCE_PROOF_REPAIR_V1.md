# Source-proof clarification and sufficient rectifiable-hull corollary

This is an authored mathematical audit of the argument in David Aldous, *Route lengths in invariant spatial tree networks*, ECP 26 (2021), article 31, Theorem 1.2 and Section 2, DOI https://doi.org/10.1214/21-ECP401. It is not a reproduction of the source, a claim to a new obstruction theorem, human peer review, or formal verification. The published theorem remains the credited prior result. The details below make explicit the proof variant used for the application.

## What the argument requires

Let Pi have the rate-one planar Poisson marginal. The joint sampled route law is translation invariant. Every route is a measurable, finite-length simple compact arc. Any two routes that meet twice agree between the meeting points. For every finite terminal set, all its routes lie in a finite rectifiable topological tree and are the unique connecting arcs there. No joint ergodicity, independent route mechanism, scale invariance, finite vertex intensity, or straight-edge representation is needed in this corollary.

Write D_r for the pair-intensity normalized route-length law for ordered pairs of distinct Poisson terminals at displacement of norm at most r. Under these assumptions, E D_r is infinite for at least one finite r, and hence for every larger r. This is the part of the published theorem needed for the SIRSN contradiction.

## 1. Balanced strips and local pair counts

In the published p.3 balanced-square definition, the strips must span the full side m of the m-by-m square. The printed two occurrences of [0,1] must be read as [0,m]. This is a visible source typo, confirmed in the PDF image; a unit-height strip has the wrong expected Poisson count. Use five vertical and five horizontal strips, each of area m^2/5, requiring every strip count to lie between 0.98 m^2/5 and 1.02 m^2/5.

The resulting square has between 0.98 m^2 and 1.02 m^2 points. In two adjacent balanced squares, unless both blue counts are below 0.1 m^2 or both exceed 0.88 m^2, there are at least 0.088 m^4 red-blue pairs at distance at most sqrt(2)m. Indeed, an intermediate blue count y in [0.1,0.88]m^2 gives y(0.98m^2-y) >= 0.088m^4. Otherwise translate an m-square across the two squares by steps m/5; each step adds at most 0.204m^2 blue points. Some translated square has an intermediate count. Each such translated square is made from five balanced full-height strips, so its total count is at least 0.98m^2. The same reasoning applies vertically.

## 2. Uniform contour event, with quantitative slack

The following restates and checks the contour ingredients from the published Lemma 2.2. Bad sites in a k-by-k grid are independent with probability at most q0=2^(-1000); couple them below sites of probability exactly q0. Set p=1-(1-q0)^2 <= 2^(-999).

For any dual self-avoiding path or circuit of length ell, greedily choose at least floor(ell/7) disjoint adjacent primal-site pairs crossed by its edges. Their bad-pair indicators are independent, each with probability p. For ell>=28, if fewer than ell/20 selected pairs have both endpoints good, at least ell/20 selected pairs are bad. A union bound over subsets bounds this event by 2^ell p^(ell/20). There are at most 4k^2 3^ell possible paths/circuits of length ell. Since 6 p^(1/20) < 2^(-47), the probability that any contour of length ell>log k fails to have at least ell/20 good edges is at most

4k^2 sum_{ell>log k} 2^(-47ell),

which tends to zero. Natural logarithms are used. Only sufficiently large k, with log k>=28, are at issue.

For a zero-cost circuit enclosing a specified lattice site, greedily choose at least ceil(ell/7) disjoint crossed primal pairs. The event that all circuit edges have a bad endpoint has probability at most p^(ell/7). The number of possible length-ell circuits surrounding that site is bounded by 4(2ell+1)^2 3^ell. Since p<=2^(-70), their total probability is bounded by

4 sum_{ell>=4} (2ell+1)^2 (1/256)^ell
<= 4 (9/256)^4 / (1-9/256) < 1/20.

Here (2ell+1)^2<=9^ell for ell>=1. Let A_k(v) mean that a zero-cost circuit of length at most log k surrounds v. This event depends on bad sites within lattice distance at most log k+1. Consequently, for X_k=sum_v 1_{A_k(v)} over the k^2 grid sites,

E X_k <= k^2/20,
Var X_k <= k^2(4 log k+5)^2,
P(X_k>k^2/10) <= 400(4 log k+5)^2/k^2 -> 0.

The independence distance here is 2 log k+2, rather than the source's inessential shorter distance. The variance estimate remains the same order.

These two high-probability events depend only on bad sites. They hold simultaneously for all colorings, including colorings selected from the random network.

## 3. Color fractions and exclusion of a small square

On the events above, consider any grid coloring with at least 0.20k^2 sites of each color. Its total internal color boundary has length at least k/2. For completeness, if every row or every column is mixed, this boundary has at least k edges. Otherwise the monochrome rows and columns have the same color, or all columns/rows would be mixed. The other color is contained in the intersection of mixed rows and mixed columns. If their counts are a,b, then ab>=0.20k^2 and boundary length is at least a+b>=2 sqrt(0.20)k>k/2.

Use the usual edge-disjoint dual-contour decomposition, resolving fourfold contacts consistently. If contours longer than log k have total length greater than k/10, they supply at least k/200 good boundary edges. We count edges here, not a matching; edges of distinct contours are distinct, so no additional factor of two is lost.

Otherwise long-contour interiors contain at most k^2/100 sites. Short paths that end on the external boundary contain at most 4k log k sites in their smaller boundary-side interiors. The standard maximal-contour decomposition used in the source leaves a common exterior color. Hence sites of the other color lie inside these paths or circuits. For sufficiently large k, with 4k log k<=0.01k^2, maximal short circuits with disjoint interiors enclose at least 0.18k^2 sites. Each has area at most log^2 k. Outside the exceptional event X_k>0.10k^2, these circuits therefore supply at least

(0.18-0.10)k^2/log^2 k = 0.08k^2/log^2 k

good boundary edges. For sufficiently large k this also exceeds k/200. This reproduces the source's short-contour argument with an explicit color-fraction margin. Thus the good-edge bound k/200 is uniform over colorings with both fractions at least 0.20.

Now start with both fractions at least 0.21 and exclude any grid square Q of side s=ceil(k/1000). For k>=8000, s<=k/800. Recolor all of Q to one color. Each color still occupies at least (0.21-1/640000)k^2>0.20k^2 sites. The new coloring has at least k/200 good boundary edges. At most 4s<=0.004k+4 of them meet Q. All remaining edges are unchanged from the original coloring, have both endpoints outside Q, and are good. Their number is at least

k/200 - 4s >= k/1000-4 >= k/2000.

This establishes the required small-square exclusion uniformly in Q, even if its position depends on all the data. It supplies explicit details for the published Corollary 2.3; simply subtracting the square perimeter from the corollary's weaker printed k/400 bound would not suffice.

## 4. Terminal counts and the source's asymmetric thresholds

Fix an integer m sufficiently large that the probability q_m of an unbalanced Poisson m-square is at most q0. Existence is elementary: a union of ten Chebyshev bounds gives q_m<=125000/m^2, so m=2^510 already suffices. For the Poisson count M in such a square,

E[M 1_unbalanced]/m^2 <= sqrt((1+1/m^2) q_m) < 1/2000.

The natural squares are independent. Thus, with probability tending to one as k tends to infinity, their total bad-square terminal count is at most m^2k^2/1000. For example Chebyshev bounds the exceptional probability by 4000000(1+1/m^2)/k^2. Also their total terminal count N is at least 0.99m^2k^2 except with probability at most 10000/(m^2k^2).

Take the finite rectifiable terminal hull in the full n-by-n square, n=mk. A terminal-weighted centroid has every branch carrying at most N/2 terminals. Include the centroid itself as a singleton group if it is a terminal. Group branches into two classes each containing between N/3 and 2N/3 terminals: if one group already has size between N/3 and N/2, use it; otherwise accumulate groups smaller than N/3 until passing N/3, then take the smaller class. Every path between the two classes passes through the centroid. Both color totals are at least 0.33m^2k^2 on the event above.

Among balanced squares let S count blue populations in [0.09,0.89]m^2; let S< and S> count those below and above that interval. Put psi=0.001. Counting blue points gives

0.24 k^2 <= 0.8 S + 0.93 S> + psi k^2.

The correct corresponding upper bounds for red points are 1.02m^2 in an S< square, 0.93m^2 in an S square, and 0.13m^2 in an S> square. Therefore red counting gives

0.20 k^2 <= 0.89 S< + 0.8 S + psi k^2.

In particular, when S<=0.005k^2,

S>/k^2 >= 0.235/0.93 = 47/186 > 0.21,
S</k^2 >= 0.195/0.89 = 39/178 > 0.21.

This uses 0.21, not the 1/4 threshold in the source's displayed (2.16). The printed red/blue thresholds are asymmetric; an unexplained symmetric substitution is insufficient. The uniform contour result above was deliberately proved with enough margin for these exact inequalities. This is an explicit audit adjustment, not a claim that the published text already contains these calculations.

Color a square yellow if its blue count is below 0.1m^2 and green otherwise. S< squares are yellow and S> squares green. For S<=0.005k^2, Section 3 supplies at least k/2000 adjacent balanced opposite-color pairs outside Q. The grid's edges can be split into four matchings (horizontal parity and vertical parity). One matching has at least k/8000 such pairs. Section 1 supplies at least 0.088m^4 red-blue terminal pairs in each. Thus the number of distinct close red-blue terminal pairs outside Q is at least

beta0 m^4 k, where beta0=0.088/8000=11/1000000.

If S>0.005k^2, every such balanced square contains at least 0.08m^4 red-blue pairs internally. Removing Q discards at most s^2<=k^2/640000 squares, so at least 0.004k^2 remain. This gives at least 0.00032m^4k^2 pairs, more than beta0 m^4k. Both cases are uniform in Q.

## 5. Centroid geometry and divergent mean

Let h=n/10000. Choose Q so that its physical square contains every point of [0,n]^2 within L-infinity distance h of the centroid. Such a grid-aligned square exists for k>=8000: each clipped coordinate interval has length at most 2h, and covering it after grid rounding needs at most 2h+2m<=sm. Clamp the interval to [0,n] if the centroid is outside the domain. If one coordinate interval is empty, every point is already at distance greater than h and Q may be chosen arbitrarily.

Both endpoints of every counted pair outside Q have Euclidean distance greater than h from the centroid. Their unique tree arc passes through it and therefore has length at least 2h=n/5000. Set r=sqrt(2)m and d_k=mk/5000. With probability tending to one, at least beta0 m^4 k unordered pairs inside [0,n]^2 have separation at most r and route length at least d_k.

For all sufficiently large k, the expected count is at least beta0 m^4k/2. Translation invariance and the rate-one Poisson pair marginal bound this same expectation above by

(1/2) n^2 pi r^2 P(D_r>=d_k) = pi m^4 k^2 P(D_r>=d_k).

This is an anchored pair-intensity bound: the event that the second endpoint also lies in the square only reduces the integral. It does not assume that route length and displacement are independent. Consequently

P(D_r>=d_k) >= beta0/(2 pi k).

The increments d_(k+1)-d_k are m/5000. Summing tail integrals over successive such intervals yields a positive constant times the divergent harmonic series. Hence E D_r=infinity. Increasing the radius retains the divergent numerator while dividing by a finite disk area, so every larger radius also has infinite mean.

All graph geometry in this argument concerns a finite terminal hull, a terminal-weighted centroid, and the inequality that arc length dominates Euclidean distance. It therefore applies directly on the measurable finite-hull event described in the accepted application note. It neither straightens jagged routes nor assumes that every infinite union of finite trees is a topological tree.
